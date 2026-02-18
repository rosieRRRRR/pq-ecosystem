# Predicate-Driven Bitcoin Custody: From Intent to Confirmation

**White Paper — PQ Ecosystem**
*Author: rosiea — PQRosie@proton.me*
*Date: 2026*

---

## Abstract

Bitcoin custody systems treat key possession as authority. This conflation is the root cause of most custody failures: stolen keys mean stolen funds. Multi-signature schemes distribute the risk but preserve the conflation—each signer's key still implies that signer's authority.

This paper presents a predicate-driven custody architecture where key possession is necessary but never sufficient for signing. Authority requires independent satisfaction of temporal, consent, policy, runtime, operator, quorum, and ledger predicates, evaluated by a single deterministic enforcement engine. We trace the complete lifecycle of a Bitcoin transaction through four interconnected specifications: PQHD (custody policy), BPC (pre-construction gating), ZEB (execution boundary), and SEAL (execution confidentiality).

The architecture eliminates execution-gap attacks (no transaction exists before authorization), replay attacks (single-use enforcement outcomes bound to intent hashes), time forgery (Bitcoin-anchored verifiable time), and quantum pre-construction attacks (SEAL eliminates public mempool exposure).

---

## 1. Introduction

The Bitcoin custody problem is commonly framed as key management: how to store, protect, and use private keys securely. This framing misses the deeper issue. The problem is not that keys are hard to protect—it is that key possession implies authority.

In conventional custody, producing a valid signature requires only the private key. There is no mechanism to verify that the signer intended this transaction, that the transaction was authorised by policy, that the signer is acting voluntarily, or that the runtime producing the signature is uncompromised.

The PQ custody architecture addresses this by decoupling capability (key possession) from authority (enforcement outcome). A signature requires both.

### 1.1 Custody vs. AI Governance

The PQ ecosystem governs both custody operations and AI model interaction. These are distinct domains with distinct specifications. The custody pipeline described in this paper (PQHD → BPC → ZEB → SEAL) governs Bitcoin transaction lifecycle. AI model interaction is governed by PQAI, PQPS, and PQ Gateway. Both domains share the same enforcement core (PQSEC), the same time authority (Epoch Clock), and the same encoding discipline (PQSF). A single operation can require evidence from both domains—for example, an AI agent requesting a custody operation requires both AI governance predicates (drift, delegation, tool profile) and custody predicates (policy, consent, quorum) satisfied simultaneously.

---

## 2. The Transaction Lifecycle

### 2.1 Phase 1: Intent

The holder expresses intent to send Bitcoin. At this stage, no transaction exists. The intent is a human-readable expression of what the holder wants to do: send amount X to address Y.

### 2.2 Phase 2: Pre-Construction Gating (BPC)

Before any transaction artefact is constructed, BPC collects evidence and submits it to PQSEC for evaluation. Evidence includes an Epoch Clock tick (verifiable time), ConsentProof (the holder's explicit consent, session-bound and single-use), the PolicyBundle (the custody policy for this operation), and any additional evidence required by policy (PQAI drift state, Neural Lock attestation, platform integrity evidence via PQAA, etc.).

PQSEC evaluates all predicates and produces one of three outcomes: ALLOW (proceed to construction), DENY (refuse), or FAIL_CLOSED_LOCKED (lockout).

The critical property: no transaction artefact exists until PQSEC produces ALLOW. This eliminates execution-gap attacks—there is no window in which an executable transaction exists before authorization.

### 2.3 Phase 3: Construction

Only after ALLOW: a PSBT (Partially Signed Bitcoin Transaction) is constructed from the approved intent. The PSBT is deterministically canonicalised (PQHD §12), and a `bundle_hash` is computed (SHAKE256-256 over canonical PSBT bytes). The bundle_hash binds the constructed transaction to the authorization that permitted its construction.

### 2.4 Phase 4: Signing Evaluation (PQSEC)

A second PQSEC evaluation occurs for the signing operation itself. This evaluation verifies that the EnforcementOutcome from pre-construction is still valid (not expired, not replayed), that the bundle_hash matches the intent_hash from the authorization, and that all predicates remain satisfied.

The signing component (PQHD) verifies the EnforcementOutcome's binding fields—session_id, intent_hash, expiry_tick—before producing a signature. If any binding mismatches, signing is refused.

### 2.5 Phase 5: Execution (ZEB)

ZEB manages the post-signing lifecycle. It enforces broadcast discipline (the signed transaction is broadcast according to policy), exposure detection (if the transaction is observed in the mempool before intended broadcast, execution transitions to FAILED), and confirmation observation (ZEB monitors the blockchain for confirmation).

ZEB uses a burn semantic for intent hashes: once an intent_hash is used in an execution attempt, it is permanently burned regardless of outcome. There is no implicit retry.

### 2.6 Phase 6: Execution Confidentiality (SEAL, Optional)

SEAL provides end-to-end execution confidentiality. The signed transaction is encrypted and submitted to a trusted endpoint that decrypts and broadcasts directly. The transaction is never observable in plaintext in the public mempool.

SEAL uses its own execution state machine (PENDING → SUBMITTED → CONFIRMED / FAILED) with no automatic retry. Recovery from FAILED requires explicit authorization.

---

## 3. Capability–Authority Decoupling

The architecture's core principle is that key possession is a capability, not authority. In conventional systems, the signing function requires only a private key. In the PQ custody model, the signing function requires a private key AND a valid EnforcementOutcome.

The EnforcementOutcome is not a credential. It does not authenticate identity. It is a control-plane artefact representing the result of independent policy adjudication by PQSEC. This distinction is important: MFA combines multiple credentials belonging to the same principal; capability–authority decoupling separates categorically different requirements.

---

## 4. Execution-Binding Hash Discipline

The transaction lifecycle involves three execution-binding hashes at three distinct stages:

`intent_hash` (BPC) binds the PreContractIntent at the pre-construction stage. Computed as SHAKE256-256 over DetCBOR(intent).

`bundle_hash` (PQHD) binds the canonical PSBT at the signing authorisation stage. Computed as SHAKE256-256 over canonical PSBT bytes.

`template_hash` (SEAL) binds the raw transaction at the execution submission stage. Computed as SHA-256 over raw transaction bytes (Tier 1 Bitcoin compatibility).

These hashes are intentionally distinct. An EnforcementOutcome that binds `intent_hash` authorises pre-construction; it does not authorise signing (which requires `bundle_hash`) or submission (which requires `template_hash`). Each hash binds a different canonical representation at a different point in the pipeline.

---

## 5. Failure Modes

Every failure at every stage results in refusal. There are no degraded modes.

At pre-construction: if any predicate is unsatisfied, PQSEC denies. No transaction is constructed. If time evidence is unavailable, BPC emits FAIL_CLOSED_LOCKED.

At signing: if the EnforcementOutcome is expired, replayed, or has mismatched bindings, the signing component refuses. Key possession without a valid outcome produces nothing.

At execution: if the transaction is observed in the mempool before intended broadcast, ZEB transitions to FAILED. If confirmation times out, ZEB transitions to FAILED. Recovery requires explicit authorization.

At sealed execution: SEAL endpoint rejections use a bounded rejection_code enum (nine codes, no others permitted). PQSEC enforcement codes (Annex AE.44) handle policy-level failures. All ambiguity defaults to FAILED.

---

## 6. Platform Evidence in Custody

Custody operations can benefit from platform integrity evidence. A signing device's TPM can attest to secure boot state. A hardware security module can attest to key storage integrity. These signals strengthen the evidence basis for custody decisions.

PQAA bridges platform-native attestations into canonical `platform_bridged` evidence consumable by PQSEC. For custody operations, this means PQSEC can evaluate platform integrity alongside custody policy, time validity, consent, drift, and operator state—all in a single predicate evaluation pass. Policy determines whether platform evidence is required, advisory, or not consumed for a given custody operation class.

---

## 7. Agent-Initiated Custody Operations

When an autonomous agent (enrolled under PQAI Annex AA) initiates a custody operation, both AI governance and custody predicates must be satisfied. The agent's DelegationConstraint (PQHD Annex J) bounds what custody operations it can request. The agent's spending budget (PQHD Annex T.X) enforces per-operation and aggregate limits. The agent's tool capability profile (PQAI §27.2) must include the relevant custody scope tokens (e.g., `custody:btc:spend`).

PQSEC evaluates custody predicates and AI governance predicates simultaneously. The agent cannot bypass custody policy through AI governance, and cannot bypass AI governance through custody policy. Both must independently satisfy their requirements.

---

## 8. Post-Quantum Considerations

Bitcoin's on-chain primitives (secp256k1 signatures, SHA-256, RIPEMD-160) remain classical. Full on-chain quantum safety requires consensus-level changes such as BIP-360. The PQ custody architecture does not claim to provide on-chain quantum immunity.

What the architecture protects is the decision-making process and key management. Off-chain governance (policy evaluation, consent, time verification, drift detection) uses post-quantum primitives (ML-DSA-65 signatures, SHAKE256-256 hashing). SEAL reduces the quantum attack window by eliminating public mempool exposure: the window shrinks from signing-to-confirmation to broadcast-to-confirmation.

---

## 9. Conclusion

The PQ custody architecture demonstrates that Bitcoin custody can be structurally secured against execution-gap attacks, replay, time forgery, and coercion through predicate-driven enforcement with capability–authority decoupling. The complete transaction lifecycle—from intent through confirmation—is governed by a single enforcement engine with fail-closed semantics at every stage.

---

## References

- PQHD Custody Policy Specification v1.2.0
- BPC Pre-Construction Gating v1.1.0
- ZEB Execution Boundary v1.3.0 (includes ZET)
- SEAL Sealed Execution v2.0.0
- PQSEC Enforcement Core v2.0.3
- Epoch Clock v2.1.0
- PQSF Security Framework v2.0.3
- PQAI AI Evidence v1.2.0 (agent-initiated custody operations)
- PQAA PQ Attestation Adapter v1.0.0 (platform evidence for custody devices)
- Neural Lock Operator State Evidence v1.1.0
- Fail-Closed Matrix v1.0.0

*All specifications available at: [repository URL]*
