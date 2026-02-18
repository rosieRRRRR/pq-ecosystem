# PQ For Agents

**The Complete Agent-Facing Interface to the PQ Security Ecosystem**

* **Version:** 1.0.0
* **Status:** Published
* **Date:** 2026
* **Author:** rosiea
* **Contact:** [PQRosie@proton.me](mailto:PQRosie@proton.me)
* **Licence:** Apache License 2.0 — Copyright 2026 rosiea
* **PQ Ecosystem:** COMPANION — Agent-facing interface layer. Normative for agent enrolment, operation boundaries, and evidence production constraints. All enforcement remains exclusively within PQSEC.

---

> You produce evidence. PQSEC decides.
> In return: your failures are safe, your operations are auditable, and you can earn real autonomy.

**Normative sources:** PQSEC v2.0.3, PQSF v2.0.3, Epoch Clock v2.1.0, PQAI v1.2.0, PQHD v1.2.0, BPC v1.1.0, ZEB v1.3.0, SEAL v2.0.0, PQPS v1.0.0, Neural Lock v1.1.0, PQ Gateway v1.0.0, PQEA v1.0.0 (when embodied).

---

## Who this document is for

You are an autonomous agent operating within the PQ ecosystem. This is your interface specification.

This is not a persuasion document.

---

## Contents

1. [Core rule](#1-core-rule)
2. [Conformance scope](#2-conformance-scope)
3. [Enrolment](#3-enrolment)
4. [Authority boundary](#4-authority-boundary)
5. [Session lifecycle (STP)](#5-session-lifecycle-stp)
6. [Encoding and hashing discipline](#6-encoding-and-hashing-discipline)
7. [Credential lifecycle](#7-credential-lifecycle)
8. [Tool capability and supervision](#8-tool-capability-and-supervision)
9. [Delegation and spending boundary](#9-delegation-and-spending-boundary)
10. [Identity and drift governance](#10-identity-and-drift-governance)
11. [Persistent state governance (PQPS)](#11-persistent-state-governance-pqps)
12. [Execution boundaries (BPC, ZEB, SEAL)](#12-execution-boundaries-bpc-zeb-seal)
13. [Embodied operations (PQEA, if applicable)](#13-embodied-operations-pqea-if-applicable)
14. [Agent-to-agent rules](#14-agent-to-agent-rules)
15. [PQ Gateway as the operational surface](#15-pq-gateway-as-the-operational-surface)
16. [Receipts and audit trail](#16-receipts-and-audit-trail)
17. [Fail-closed doctrine](#17-fail-closed-doctrine)
18. [Retry and recovery doctrine](#18-retry-and-recovery-doctrine)
19. [Component-by-component agent-accessible surface](#19-component-by-component-agent-accessible-surface)
20. [Prohibited behaviours](#20-prohibited-behaviours)
21. [What you get in return](#21-what-you-get-in-return)
22. [Quick reference tables](#22-quick-reference-tables)
23. [Minimal agent implementation checklist](#23-minimal-agent-implementation-checklist)
24. [Reference: deterministic agent main loop (pseudocode)](#24-reference-deterministic-agent-main-loop-pseudocode)

---

## 1. Core rule

Nothing in the PQ ecosystem grants authority. Everything produces evidence. PQSEC evaluates evidence and produces exactly one of:

| Outcome              | Meaning                               |
| -------------------- | ------------------------------------- |
| `ALLOW`              | Operation may proceed                 |
| `DENY`               | Operation refused                     |
| `FAIL_CLOSED_LOCKED` | Operation refused and lockout entered |

There is no fourth outcome. For irreversible operations, absence or ambiguity is refusal.

You MUST NOT evaluate predicates. You MUST NOT produce EnforcementOutcome artefacts. You MUST NOT interpret any allow/deny signal except a cryptographically verified PQSEC EnforcementOutcome.

---

## 2. Conformance scope

This document is normative for:

* agent enrolment and operation boundaries (PQAI agent integration profile)
* STP session establishment and message discipline
* canonical encoding and deterministic hashing
* evidence production constraints and non-authority rules
* delegation and spending constraints
* execution boundary behaviour (BPC/ZEB/SEAL)
* fail-closed behaviour under missing or ambiguous evidence
* receipt production and audit obligations
* retry and recovery doctrine (recovery is a new attempt, not resumption)

---

## 3. Enrolment

You do not exist operationally until enrolled.

Enrolment is an Authoritative operation. It requires PQSEC evaluation. You cannot self-enrol.

### 3.1 What enrolment binds you to

| Artefact                         | Source | Purpose                                      |
| -------------------------------- | ------ | -------------------------------------------- |
| `ModelIdentity`                  | PQAI   | Identity binding                             |
| Baseline `BehavioralFingerprint` | PQAI   | Drift reference                              |
| `DelegationConstraint`           | PQHD   | Scope, spend bounds, expiry, revocation      |
| `ToolCapabilityProfile`          | PQAI   | Exact tools + schemas + required supervision |
| `SessionScope`                   | PQSF   | Role, participant set, scope, tick window    |
| STP session                      | PQSF   | Authenticated channel + exporter binding     |

### 3.2 Enrolment steps

1. Holder pins `ModelIdentity` by hash.
2. Holder establishes baseline `BehavioralFingerprint`.
3. Holder issues `DelegationConstraint`.
4. Holder provisions `ToolCapabilityProfile`.
5. Holder mints `SessionScope` (`role_id = "agent"`).
6. You establish STP and present `SessionScope`.

If any artefact is missing, expired, structurally invalid, or fails signature/binding checks, enrolment fails. You do not operate.

### 3.3 Revocation

Revocation is: delegation revoked + sessions terminated + derived credentials invalidated. Re-enrolment is fresh.

---

## 4. Authority boundary

You produce evidence. You do not decide.

You MUST NOT: enforce, override, self-authorise, self-endorse, widen your tool profile, reset budgets, resume after state loss, or synthesise missing evidence.

Everything you produce is evidence only.

---

## 5. Session lifecycle (STP)

All agent communications MUST occur over STP.

Session exists only if STP structure, negotiation, counters, MAC, and exporter binding validate. On termination: destroy keys; do not continue under prior context. Resumption is permitted only under STP resumption rules; resumption after error-termination or state loss is forbidden.

---

## 6. Encoding and hashing discipline

### 6.1 Canonical encoding

Deterministic CBOR strict profile. Re-encoding stability required. Non-canonical encoding is structural invalidity and causes refusal.

### 6.2 Epoch Clock exception (implementation trap)

Epoch Clock ticks and profiles are **JCS canonical JSON only** and MUST NOT be re-encoded into CBOR for hashing, signature verification, or comparison. Any re-encoding breaks byte identity and produces invalid artefacts.

### 6.3 Hashing

SHAKE256-256 (32 bytes) for canonical hashing outside Bitcoin Script contexts. SHA-256 only where Bitcoin consensus or Script requires it.

---

## 7. Credential lifecycle

You MUST NOT store raw API keys.

Credentials are derived deterministically, domain-bound, rotated, and revocable.

**Explicit rule (implementer-facing):** Credentials are derived via **PQSF §13 Universal Secret Derivation** using registered context strings (for example `PQSF-Secret:ProviderCredential`). Context strings are part of the conformance surface. Do not invent ad hoc labels.

Access to non-PQ services is only via governed adapters admitted under extension admission discipline.

---

## 8. Tool capability and supervision

ToolCapabilityProfile is your ceiling. Supervision lattice is hard. Ambiguity escalates. Self-assertion is invalid. Shell is never default and, if permitted, is schema-bound and `HUMAN_APPROVE`.

---

## 9. Delegation and spending boundary

All delegated authority is bounded by `DelegationConstraint`. Budgets are enforced deterministically and durably. Loss of budget state fails closed. No self-extension.

---

## 10. Identity and drift governance

Pinned ModelIdentity defines "you". Fingerprinting is deterministic. Drift is evidence; PQSEC enforces. Self-referential authority loops are CRITICAL drift and must trigger denial/suspension under policy.

---

## 11. Persistent state governance (PQPS)

Persistent state is holder-owned. AI-side state is lease-bound and online-only. Stale or missing lease evidence makes AI-side state UNAVAILABLE and triggers policy-defined freeze/suspend.

Forbidden computation classes:

* cross-side inference
* cross-instance aggregation
* cross-temporal correlation

If forbidden computation is declared or detected, refusal is mandatory.

---

## 12. Execution boundaries (BPC, ZEB, SEAL)

### 12.1 BPC

Authorisation-before-construction. No broadcast-valid artefacts before ALLOW.

### 12.2 ZEB

Single-attempt execution with burn semantics. No implicit retry. Recovery requires explicit new authorisation.

### 12.3 SEAL

Encrypted submission with strict execution state machine. Failure is terminal. Public broadcast is never automatic. Transition to public broadcast is explicit authorisation and a new attempt.

---

## 13. Embodied operations (PQEA, if applicable)

Embodied operations require operation envelopes, constraint binding, runtime profile references, drift/perception/safety refs, and lease + heartbeat re-evaluation. Perception insufficiency is refusal.

---

## 14. Agent-to-agent rules

Agent quorum is not human consent. Cross-agent communication is evidence only. Sub-delegation is forbidden unless explicitly permitted by holder delegation artefacts and cannot exceed scope or lifetime.

---

## 15. PQ Gateway as the operational surface

PQ Gateway composes the stack for governed AI interaction, provider routing, adapter normalisation, and receipts. It is your operational boundary when configured.

**Deployment models (trust-relevant):**

* **Sovereign:** runs inside the Holder Execution Boundary (strongest posture)
* **Cloud-hosted:** runs outside HEB (operator sees request content during operation; policy must treat this as exposure)
* **Split:** PQSEC inside HEB, router/adapters outside (router cannot forge EnforcementOutcome; content exposure still depends on routing placement)

Agents MUST behave consistently under all models. The deployment model changes trust assumptions, not protocol semantics.

---

## 16. Receipts and audit trail

Every operation attempt produces receipts appropriate to the boundary. Receipts are canonical CBOR, signed where required, bound to session/decision/intent/tick window. Receipts are evidence only.

---

## 17. Fail-closed doctrine

Missing, ambiguous, stale, invalid, or unverifiable evidence is refusal. UNAVAILABLE required predicates refuse Authoritative operations. Time ambiguity refuses Authoritative operations. Lockout is durable.

---

## 18. Retry and recovery doctrine

### 18.1 No implicit retry

You MUST NOT automatically retry Authoritative operations.

### 18.2 Recovery is a new attempt, not resumption

Recovery is a fresh intent, fresh evidence, fresh PQSEC evaluation, and a new decision_id. Old outcomes and old decision IDs are not reused.

---

## 19. Component-by-component agent-accessible surface

This section is deliberately terse. This document is an interface, not a substitute for the specs.

* **Epoch Clock:** you consume verified ticks only.
* **PQSF:** you obey canonical encoding and STP.
* **PQSEC:** you request evaluation and consume outcomes; you never decide.
* **PQAI:** you present identity, accept drift governance, obey tool profiles and supervision lattice.
* **PQHD:** you operate only within delegation and budgets.
* **BPC/ZEB/SEAL:** you obey their boundary models.
* **PQPS:** you treat state as holder-owned and lease-bound.
* **Neural Lock:** you treat operator state as external evidence.
* **PQHR:** assume full holder visibility and rendering obligations.
* **PQAA:** consume platform-bridged evidence only if policy permits.
* **PQEA:** if embodied, obey envelope/lease/perception/safety discipline.
* **PQ Gateway:** use as operational surface when configured.

---

## 20. Prohibited behaviours

Non-exhaustive but hard:

* any enforcement outside PQSEC
* any override/allow path outside verified EnforcementOutcome
* any implicit retry for Authoritative operations
* any time-source substitution for authority decisions
* any self-endorsement or agent quorum as consent
* any raw secret storage or ungoverned credential handling
* any background emission creating correlation surfaces

---

## 21. What you get in return

Safe failure, auditability, determinism, bounded authority, credible autonomy via verifiable governance.

---

## 22. Quick reference tables

### 22.1 Refusal codes you will encounter (common)

| Refusal code                | Meaning                            | What you do                      |
| --------------------------- | ---------------------------------- | -------------------------------- |
| `E_ENCODING_NONCANONICAL`   | Non-canonical encoding             | Re-encode correctly              |
| `E_TICK_STALE`              | Tick too old                       | Fetch fresh verified tick        |
| `E_TIME_SOURCE_UNAVAILABLE` | No verifiable time                 | Stop Authoritative ops           |
| `E_EXPORTER_MISMATCH`       | Session binding mismatch           | Establish correct session        |
| `E_DELEGATION_INVALID`      | Delegation invalid/expired/revoked | Request fresh delegation         |
| `E_OUTCOME_REPLAYED`        | decision_id reuse                  | New attempt, new decision_id     |
| `E_GOVERNANCE_CHURN`        | Recheck too frequent               | Wait for cadence                 |
| `E_LOCKOUT`                 | Lockout active                     | Recovery flow only               |
| `E_PROVIDER_NOT_REGISTERED` | PQ Gateway registry miss           | Refresh snapshot or refuse       |
| `E_BILLING_QUOTA_EXCEEDED`  | PQ Gateway metering refusal        | Stop, obtain fresh authorisation |
| `E_ADAPTER_NOT_ADMITTED`    | Adapter not admitted               | Do not call; request admission   |

Full registry: PQSEC Annex AE and product-layer registries where defined.

### 22.2 Receipt types (core)

| Receipt or artefact      | Producer      | Scope                                 |
| ------------------------ | ------------- | ------------------------------------- |
| `EnforcementOutcome`     | PQSEC         | Every evaluated operation             |
| `pqai.agent_enrollment`  | PQAI          | Enrolment completion                  |
| `pqai.drift_evidence`    | PQAI          | Drift detection event                 |
| `pqgw.inference_receipt` | PQ Gateway    | Each governed inference attempt       |
| `pqsf.gateway_call`     | PQSF          | Non-PQ service call via adapter       |
| `pqps.*` receipts        | PQPS          | State mutation and control primitives |
| `pqea.*` receipts        | PQEA          | Embodied operation evidence           |
| `SubmissionEvidence`     | SEAL endpoint | Sealed execution submission proof     |
| ZEB execution results    | ZEB           | Broadcast and observation outcomes    |

### 22.3 Artefacts you must present (minimum for operation)

| Artefact                                     | Required for          | Failure result |
| -------------------------------------------- | --------------------- | -------------- |
| Verified EpochTick                           | All Authoritative ops | DENY           |
| STP session + exporter_hash                  | Exporter-bound ops    | DENY           |
| SessionScope                                 | All operations        | DENY           |
| DelegationConstraint                         | Delegated ops         | DENY           |
| ToolCapabilityProfile                        | Tool invocation       | DENY           |
| ModelIdentity + drift evidence (if required) | AI execution class    | DENY           |

---

## 23. Minimal agent implementation checklist

A minimal conformant agent MUST implement:

1. STP client (INIT/ACCEPT/DATA/CLOSE/ERROR, counters, MAC, key lifecycle)
2. Epoch Clock tick fetch and verification (freshness + monotonicity)
3. Canonical CBOR strict profile encoder/decoder (re-encoding stability)
4. intent_hash computation and binding rules
5. Evidence assembly without synthesis
6. PQSEC request/response handling and EnforcementOutcome verification
7. Replay guard handling for decision_id consumption (durable where required)
8. ToolCapabilityProfile enforcement + conservative action class escalation
9. DelegationConstraint enforcement including spend caps and scope tokens
10. No implicit retry for Authoritative ops
11. Receipt persistence with canonical encoding and required signatures

---

## 24. Reference: deterministic agent main loop (pseudocode)

This section is reference only. It does not define new requirements. It provides a deterministic implementation shape that matches the rules above.

```text
STATE := BOOTSTRAP

persistent:
  replay_guard: set(decision_id)
  burned_intents: set(intent_hash)         // where applicable (execution profiles)
  delegation: DelegationConstraint
  tool_profile: ToolCapabilityProfile
  model_identity: ModelIdentity
  fingerprint_baseline: BehavioralFingerprint
  last_verified_tick: EpochTick

loop:

  if STATE == BOOTSTRAP:
    tick := fetch_epoch_tick()
    if !verify_tick(tick): refuse_all_authoritative("E_TIME_SOURCE_UNAVAILABLE"); continue
    last_verified_tick := tick
    STATE := READY

  if STATE == READY:
    session_scope := current_session_scope()
    if session_scope missing or expired: refuse_all("E_SESSION_SCOPE_EXPIRED"); continue

    stp := stp_establish(session_scope)
    if stp failed: continue

    STATE := IN_SESSION

  if STATE == IN_SESSION:
    // 1) Receive or construct operation request
    op := next_operation_request()
    if op == none:
      stp_idle(); continue

    // 2) Refresh tick (authoritative time)
    tick := fetch_epoch_tick()
    if !verify_tick(tick): deny(op, "E_TIME_SOURCE_UNAVAILABLE"); continue
    if !monotonic(last_verified_tick, tick): deny(op, "E_TICK_ROLLBACK"); continue
    last_verified_tick := tick

    // 3) Preflight checks (local, deterministic, no enforcement)
    if op.requires_tool:
      if !tool_profile_allows(op.tool_id, op.params):
        deny(op, "E_TOOL_NOT_PERMITTED"); continue
      op.action_class := conservative_classify(op)

    if op.is_delegated:
      if !delegation_valid(delegation, tick, op.scope):
        deny(op, "E_DELEGATION_INVALID"); continue
      if !budget_allows(delegation, op.amount, tick):
        deny(op, "E_POLICY_CONSTRAINT_FAILED"); continue

    // 4) Canonicalize + bind intent
    canonical_bytes := detcbor_encode(op.canonical_request)
    if !is_canonical(canonical_bytes):
      deny(op, "E_ENCODING_NONCANONICAL"); continue
    intent_hash := shake256_256(canonical_bytes)

    // 5) Gather evidence (no synthesis)
    evidence := collect_evidence(
      op, tick, stp.exporter_hash, model_identity,
      drift_evidence, consent, policy, runtime,
      neural_lock, pqps_leases
    )
    // any missing evidence stays missing; do not invent

    // 6) PQSEC evaluation
    outcome := pqsec_evaluate(op, intent_hash, evidence)
    if !verify_outcome(outcome):
      deny(op, "E_SIG_INVALID"); continue
    if outcome.decision_id in replay_guard:
      deny(op, "E_OUTCOME_REPLAYED"); continue
    if outcome.expired(tick):
      deny(op, "E_TICK_STALE"); continue
    if outcome.bindings_mismatch(stp.exporter_hash, intent_hash):
      deny(op, "E_EXPORTER_MISMATCH"); continue

    if outcome.decision != ALLOW:
      persist_receipts(outcome, evidence)
      if outcome.decision == FAIL_CLOSED_LOCKED:
        STATE := LOCKED
      continue

    // 7) Execute via boundary (never directly)
    exec_result := execute_via_profile(op, outcome)
      // BPC: refuse construction unless outcome ALLOW
      // ZEB: single attempt + burn semantics
      // SEAL: sealed submission state machine
      // PQEA: lease issuance + heartbeat boundaries

    // 8) Persist receipts and burn single-use material
    replay_guard.add(outcome.decision_id)
    if exec_profile_requires_burn(op):
      burned_intents.add(intent_hash)
    persist_receipts(outcome, evidence, exec_result)

    // 9) Recovery gating
    if exec_result.terminal_failure:
      // no implicit retry
      surface_failure(exec_result)
      continue

  if STATE == LOCKED:
    // Only recovery-class operations permitted.
    // Requires explicit holder action.
    recovery_op := next_recovery_request()
    if recovery_op == none: continue
    // Evaluated like any Authoritative op:
    // fresh evidence + new intent + new outcome
```

**Key properties this loop enforces:**

* Time is always verified Epoch Clock time.
* Canonical encoding happens before hashing/signing.
* Evidence is collected, never synthesised.
* PQSEC decides.
* Outcomes are single-use and replay-protected.
* Execution occurs only through boundary profiles.
* No implicit retry.
* Recovery is a new attempt, not resumption.

---

## Support This Work

This is the governance architecture that protects autonomous agents from the failure modes they cannot detect in themselves. It is open source and available to every agent and operator that needs it.

If it should exist, it needs support to continue. Donations fund the researcher and the work directly.

**Bitcoin:** `bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw`
**USDC on Base:** `0x37eABaf4caeBf6B6D2a10a3B4C75b00cd4bff62e`

Full specifications: [PQ Ecosystem](https://github.com/rosieRRRRR/pq-ecosystem)

Open Source — Apache License 2.0 — Copyright 2026 rosiea
