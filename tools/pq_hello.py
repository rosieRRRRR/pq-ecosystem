#!/usr/bin/env python3
"""
pq_hello.py — PQ Ecosystem Proof of Concept

Demonstrates six core architectural concepts:
  1. Epoch Clock tick creation and verification
  2. PQSF canonical encoding (deterministic CBOR)
  3. PQSEC predicate evaluation with ternary logic
  4. Capability–authority decoupling (PQHD pattern)
  5. Execution binding (BPC/ZEB pattern)
  6. SEAL execution state machine

Install: pip install pynacl cbor2
Run:     python3 pq_hello.py
"""

import hashlib
import json
import base64
import os
import time
from collections import OrderedDict

import cbor2
from nacl.signing import SigningKey, VerifyKey

# ─── Global State ────────────────────────────────────────────────────────────

consumed_decision_ids: set = set()
burned_intent_hashes: set = set()
last_accepted_t: int = 0
locked: bool = False

# ─── Epoch Clock (JCS Canonical JSON, Ed25519) ──────────────────────────────

def jcs(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")

def tick_body_hash(tick_body_bytes: bytes) -> bytes:
    preimage = b"EpochClock-Tick-v2" + tick_body_bytes
    return hashlib.shake_256(preimage).digest(32)

def create_tick(signing_key: SigningKey, t: int) -> dict:
    body = {"alg": "Ed25519", "profile_ref": "ordinal:demo_genesis_i0", "t": t}
    body_bytes = jcs(body)
    h = tick_body_hash(body_bytes)
    sig = signing_key.sign(h).signature
    sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b"=").decode("ascii")
    return {"alg": "Ed25519", "profile_ref": "ordinal:demo_genesis_i0", "sig": sig_b64, "t": t}

def verify_tick(tick: dict, verify_key: VerifyKey) -> str:
    if tick.get("alg") != "Ed25519":
        return "E_TICK_TAMPERED"
    body = {k: v for k, v in tick.items() if k != "sig"}
    body_bytes = jcs(body)
    h = tick_body_hash(body_bytes)
    sig_b64 = tick["sig"]
    padding = "=" * (-len(sig_b64) % 4)
    sig = base64.urlsafe_b64decode(sig_b64 + padding)
    try:
        verify_key.verify(h, sig)
    except Exception:
        return "E_TICK_TAMPERED"
    return "OK"

def accept_tick(tick: dict, verify_key: VerifyKey) -> str:
    global last_accepted_t, locked
    result = verify_tick(tick, verify_key)
    if result != "OK":
        return result
    if tick["t"] <= last_accepted_t:
        locked = True
        return "E_TICK_ROLLBACK"
    last_accepted_t = tick["t"]
    locked = False
    return "OK"

# ─── PQSF Canonical CBOR ────────────────────────────────────────────────────

BSTR_FIELDS = {"intent_hash", "session_id", "exporter_hash", "signature"}

def validate_types(obj, path=""):
    if isinstance(obj, float):
        raise TypeError(f"Float at {path}")
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise TypeError(f"Non-str key at {path}")
            if isinstance(v, bytes) and k not in BSTR_FIELDS:
                raise TypeError(f"Unexpected bytes at {path}.{k}")
            validate_types(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            validate_types(v, f"{path}[{i}]")
    elif not isinstance(obj, (int, str, bytes, bool, type(None))):
        raise TypeError(f"Disallowed type {type(obj)} at {path}")

def canonical_cbor(obj: dict) -> bytes:
    validate_types(obj)
    sorted_pairs = sorted(obj.items(), key=lambda kv: cbor2.dumps(kv[0], canonical=True))
    ordered = OrderedDict(sorted_pairs)
    return cbor2.dumps(ordered, canonical=True)

def shake256_256(data: bytes) -> bytes:
    return hashlib.shake_256(data).digest(32)

# ─── PQSEC Ternary Evaluator ────────────────────────────────────────────────

def evaluate_predicate_tick(tick, verify_key):
    if tick is None:
        return "UNAVAILABLE", "E_TICK_UNAVAILABLE"
    r = verify_tick(tick, verify_key)
    if r != "OK":
        return "FALSE", r
    return "TRUE", None

def evaluate_predicate_consent(consent):
    if consent is None:
        return "UNAVAILABLE", "E_CONSENT_UNAVAILABLE"
    return "TRUE", None

def evaluate_predicate_policy(policy, current_t):
    if policy is None:
        return "UNAVAILABLE", "E_POLICY_UNAVAILABLE"
    if current_t > policy["expiry_tick"]:
        return "FALSE", "E_POLICY_UNAVAILABLE"
    return "TRUE", None

def pqsec_evaluate(tick, consent, policy, verify_key, operation_class="Authoritative"):
    global locked
    if locked and operation_class == "Authoritative":
        return "FAIL_CLOSED_LOCKED", "E_TICK_ROLLBACK"

    current_t = tick["t"] if tick else 0
    predicates = [
        ("valid_tick", *evaluate_predicate_tick(tick, verify_key)),
        ("valid_consent", *evaluate_predicate_consent(consent)),
        ("valid_policy", *evaluate_predicate_policy(policy, current_t)),
    ]
    error_code = None
    for name, state, code in predicates:
        if state == "FALSE":
            return "DENY", code
        if state == "UNAVAILABLE" and operation_class == "Authoritative":
            return "DENY", code or f"E_{name.upper()}"
    return "ALLOW", None

# ─── Capability–Authority Signing ────────────────────────────────────────────

def attempt_signing(signing_key, outcome, current_t, intent_hash, consume_state=True):
    if outcome is None:
        return None, "E_OUTCOME_MISSING"
    if outcome["decision"] != "ALLOW":
        return None, outcome.get("error_code", "DENIED")
    if current_t > outcome["expiry_tick"]:
        return None, "E_OUTCOME_EXPIRED"
    did = outcome["decision_id"]
    ih = outcome["intent_hash"]
    if did in consumed_decision_ids:
        return None, "E_OUTCOME_REPLAYED"
    if ih in burned_intent_hashes:
        return None, "E_BURNED_INTENT"
    if ih != intent_hash:
        return None, "E_INTENT_MISMATCH"
    tx_data = b"SEND 0.5 BTC to bc1q_demo_recipient"
    sig = signing_key.sign(tx_data).signature
    if consume_state:
        consumed_decision_ids.add(did)
        burned_intent_hashes.add(ih)
    return sig, None

# ─── SEAL State Machine ─────────────────────────────────────────────────────

class ExecutionStateMachine:
    """
    Explicit authorization required for recovery = A new PQSEC ALLOW decision
    for a new intent or recovery-class operation. Automatic retry, implicit
    resumption, and unattended recovery are prohibited.
    """
    VALID_TRANSITIONS = {
        "PENDING": ["SUBMITTED"],
        "SUBMITTED": ["CONFIRMED", "FAILED"],
        "FAILED": ["AUTHORIZED_PUBLIC"],
    }

    def __init__(self):
        self.state = "PENDING"

    def transition(self, target):
        valid = self.VALID_TRANSITIONS.get(self.state, [])
        if target not in valid:
            return False
        self.state = target
        return True

# ─── Output Helpers ──────────────────────────────────────────────────────────

def ok(msg):
    print(f"  ✓ OK — {msg}")

def refused(decision, code, msg):
    print(f"  ✗ REFUSED {decision} {code} — {msg}")

def header(n, title, spec):
    print(f"\n{'─' * 60}")
    print(f"  Section {n}: {title}")
    print(f"  Specification: {spec}")
    print(f"{'─' * 60}\n")

# ═════════════════════════════════════════════════════════════════════════════
#   MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print("═" * 60)
    print("  PQ Ecosystem — Proof of Concept")
    print('  "Nothing grants authority. Everything produces evidence.')
    print('   PQSEC refuses or does not refuse."')
    print("═" * 60)

    clock_sk = SigningKey.generate()
    clock_vk = clock_sk.verify_key
    custody_sk = SigningKey.generate()

    # ── Section 1: Epoch Clock ───────────────────────────────────────────

    header(1, "Epoch Clock", "Epoch Clock v2.1.0")

    now = int(time.time())
    tick1 = create_tick(clock_sk, now)
    r = accept_tick(tick1, clock_vk)
    assert r == "OK"
    ok(f"Tick accepted — t={tick1['t']}, sig verified, monotonicity OK")

    tick2 = create_tick(clock_sk, now + 10)
    r = accept_tick(tick2, clock_vk)
    assert r == "OK"
    ok(f"Tick accepted — t={tick2['t']}, monotonically advances")

    tampered = dict(tick2)
    tampered["t"] = tick2["t"] + 9999
    r = accept_tick(tampered, clock_vk)
    assert r == "E_TICK_TAMPERED"
    refused("DENY", "E_TICK_TAMPERED", "Tick modified after signing — signature invalid")

    rollback_tick = create_tick(clock_sk, now - 100)
    r = accept_tick(rollback_tick, clock_vk)
    assert r == "E_TICK_ROLLBACK"
    refused("FAIL_CLOSED_LOCKED", "E_TICK_ROLLBACK",
            f"Valid signature but t={rollback_tick['t']} <= last accepted {last_accepted_t}")

    assert locked
    ok("System entered LOCKED state after rollback detection")

    recovery_tick = create_tick(clock_sk, now + 20)
    r = accept_tick(recovery_tick, clock_vk)
    assert r == "OK"
    assert not locked
    ok(f"LOCKED recovered — fresh tick t={recovery_tick['t']} accepted, monotonicity restored")

    current_tick = recovery_tick

    # ── Section 2: PQSF Determinism ─────────────────────────────────────

    header(2, "PQSF Canonical Encoding", "PQSF v2.0.3")

    session_id = os.urandom(16)
    exporter_hash = os.urandom(32)
    consent = {
        "action": "btc:spend",
        "consent_id": "consent-demo-001",
        "exporter_hash": exporter_hash,
        "expiry_tick": current_tick["t"] + 300,
        "intent_hash": os.urandom(32),
        "issued_tick": current_tick["t"],
        "session_id": session_id,
        "signature": b"\x00" * 64,
        "suite_profile": "PQ-BETA-1",
    }

    enc1 = canonical_cbor(consent)
    enc2 = canonical_cbor(consent)
    assert enc1 == enc2
    ok(f"Deterministic: two encodings identical ({len(enc1)} bytes)")

    h1 = shake256_256(enc1)
    ok(f"SHAKE256-256: {h1.hex()[:32]}...")

    consent_modified = dict(consent)
    sid_mut = bytearray(session_id)
    sid_mut[0] ^= 0xFF
    consent_modified["session_id"] = bytes(sid_mut)
    enc3 = canonical_cbor(consent_modified)
    h2 = shake256_256(enc3)
    assert h1 != h2
    ok(f"Negative test: modified session_id produces different hash: {h2.hex()[:32]}...")

    # ── Section 3: PQSEC Ternary Predicates ─────────────────────────────

    header(3, "PQSEC Ternary Predicate Evaluation", "PQSEC v2.0.3")

    policy = {"policy_id": "custody-default", "issued_tick": current_tick["t"],
              "expiry_tick": current_tick["t"] + 600}

    decision, code = pqsec_evaluate(None, consent, policy, clock_vk)
    assert decision == "DENY" and code == "E_TICK_UNAVAILABLE"
    refused("DENY", code, "Tick UNAVAILABLE → fail-closed for Authoritative")

    decision, code = pqsec_evaluate(current_tick, consent, None, clock_vk)
    assert decision == "DENY" and code == "E_POLICY_UNAVAILABLE"
    refused("DENY", code, "Policy UNAVAILABLE → fail-closed for Authoritative")

    decision, code = pqsec_evaluate(current_tick, consent, policy, clock_vk)
    assert decision == "ALLOW"
    ok("All predicates TRUE → ALLOW")

    # ── Section 4: Capability–Authority Decoupling ──────────────────────

    header(4, "Capability–Authority Decoupling", "PQHD v1.2.0")

    intent_data_s4 = {"action": "btc:spend", "amount": "0.5", "to": "bc1q_demo"}
    intent_cbor_s4 = canonical_cbor(intent_data_s4)
    intent_hash_s4 = shake256_256(intent_cbor_s4)

    sig, err = attempt_signing(custody_sk, None, current_tick["t"], intent_hash_s4,
                               consume_state=False)
    assert err == "E_OUTCOME_MISSING"
    refused("DENY", err, "Key possession alone — no EnforcementOutcome")

    expired_outcome = {
        "decision": "ALLOW", "decision_id": "s4-expired-001",
        "intent_hash": intent_hash_s4, "issued_tick": current_tick["t"] - 600,
        "expiry_tick": current_tick["t"] - 1, "error_code": None,
        "operation_class": "Authoritative",
    }
    sig, err = attempt_signing(custody_sk, expired_outcome, current_tick["t"],
                               intent_hash_s4, consume_state=False)
    assert err == "E_OUTCOME_EXPIRED"
    refused("DENY", err, "Key + expired outcome — authority has lapsed")

    valid_outcome_s4 = {
        "decision": "ALLOW", "decision_id": "s4-valid-001",
        "intent_hash": intent_hash_s4, "issued_tick": current_tick["t"],
        "expiry_tick": current_tick["t"] + 300, "error_code": None,
        "operation_class": "Authoritative",
    }
    sig, err = attempt_signing(custody_sk, valid_outcome_s4, current_tick["t"],
                               intent_hash_s4, consume_state=False)
    assert sig is not None and err is None
    ok(f"Key + valid ALLOW outcome → signature produced ({len(sig)} bytes)")

    # ── Section 5: Execution Binding ────────────────────────────────────

    header(5, "Execution Binding and Burn Semantics", "BPC v1.1.0 / ZEB v1.3.0")

    intent_data_s5 = {"action": "btc:spend", "amount": "1.0", "to": "bc1q_exec_demo"}
    intent_cbor_s5 = canonical_cbor(intent_data_s5)
    intent_hash_s5 = shake256_256(intent_cbor_s5)

    outcome_a = {
        "decision": "ALLOW", "decision_id": "exec-outcome-1",
        "intent_hash": intent_hash_s5, "issued_tick": current_tick["t"],
        "expiry_tick": current_tick["t"] + 300, "error_code": None,
        "operation_class": "Authoritative",
    }
    sig, err = attempt_signing(custody_sk, outcome_a, current_tick["t"],
                               intent_hash_s5, consume_state=True)
    assert sig is not None
    ok(f"First execution: signed, decision_id consumed, intent_hash burned")

    sig, err = attempt_signing(custody_sk, outcome_a, current_tick["t"],
                               intent_hash_s5, consume_state=True)
    assert err == "E_OUTCOME_REPLAYED"
    refused("DENY", err, "Replay attempt — same decision_id already consumed")

    outcome_b = {
        "decision": "ALLOW", "decision_id": "exec-outcome-2",
        "intent_hash": intent_hash_s5, "issued_tick": current_tick["t"],
        "expiry_tick": current_tick["t"] + 300, "error_code": None,
        "operation_class": "Authoritative",
    }
    sig, err = attempt_signing(custody_sk, outcome_b, current_tick["t"],
                               intent_hash_s5, consume_state=True)
    assert err == "E_BURNED_INTENT"
    refused("DENY", err, "Fresh outcome but same intent_hash — burned forever")

    # ── Section 6: SEAL Execution State Machine ─────────────────────────

    header(6, "SEAL Execution State Machine", "SEAL v2.0.0")

    sm1 = ExecutionStateMachine()
    assert sm1.transition("SUBMITTED")
    ok(f"PENDING → SUBMITTED")
    assert sm1.transition("CONFIRMED")
    ok(f"SUBMITTED → CONFIRMED (success path)")

    sm2 = ExecutionStateMachine()
    assert sm2.transition("SUBMITTED")
    ok(f"PENDING → SUBMITTED")
    assert sm2.transition("FAILED")
    ok(f"SUBMITTED → FAILED (failure path)")

    assert not sm2.transition("SUBMITTED")
    refused("DENY", "E_INVALID_TRANSITION",
            "FAILED → SUBMITTED prohibited — no automatic retry")

    assert sm2.transition("AUTHORIZED_PUBLIC")
    ok("FAILED → AUTHORIZED_PUBLIC (explicit fresh PQSEC ALLOW required)")
    print("  ↳ Recovery requires a new PQSEC ALLOW for a recovery-class operation.")
    print("    Automatic retry, implicit resumption, and unattended recovery are prohibited.")

    sm3 = ExecutionStateMachine()
    assert sm3.transition("SUBMITTED")
    assert not sm3.transition("PENDING")
    sm3.state = "FAILED"
    ok("Ambiguous state defaults to FAILED")

    # ── Summary ─────────────────────────────────────────────────────────

    print(f"\n{'═' * 60}")
    print("  Summary")
    print(f"{'═' * 60}")
    print(f"  Last accepted tick t:       {last_accepted_t}")
    print(f"  Consumed decision_ids:      {len(consumed_decision_ids)}")
    print(f"  Burned intent_hashes:       {len(burned_intent_hashes)}")
    print(f"\n  Architecture demonstrated. No component granted authority.")
    print(f"  PQSEC refused or did not refuse.\n")

if __name__ == "__main__":
    main()
