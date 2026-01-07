# PQ — Post-Quantum Security Ecosystem

**An Open Standard for Deterministic, Post-Quantum-Safe Custody, Compliance, and AI Operations**

* **Specification Version:** 2.0.0
* **Status:** Implementation Ready
* **Date:** 2026
* **Author:** rosiea
* **Contact:** PQRosie@proton.me
* **Licence:** Apache License 2.0 — Copyright 2025 rosiea

---

## Summary

PQ is a composed ecosystem of specifications that eliminates entire classes of security failures present in modern systems while ensuring cryptographic agility for the post-quantum transition.

Most post-quantum projects focus narrowly on future cryptography. PQ addresses attacks that succeed daily—replay, time forgery, silent runtime compromise, consent reuse, execution-gap exploitation—while preparing for quantum-capable adversaries.

PQ replaces trust assumptions with explicit, verifiable predicates. No component grants authority in isolation. All enforcement flows through a single deterministic core: **PQSEC**.

**This document is a conceptual overview and ecosystem guide. For normative enforcement semantics, predicate definitions, and implementation requirements, see PQSEC.**

---

## Non-Normative Overview — For Explanation and Orientation Only

**This section is NOT part of the conformance surface.  
It is provided for explanatory and onboarding purposes only.**

### Plain Summary

PQ is a family of specifications that work together to provide deterministic, auditable security for custody, AI operations, and regulated transactions. Each specification produces evidence or defines structure. None grants authority alone. Authority emerges only when all required predicates are satisfied and evaluated by PQSEC.

### What PQ Is / Is Not

| PQ IS | PQ IS NOT |
|-------|-----------|
| An ecosystem of composed specifications | A single monolithic protocol |
| A conceptual and architectural framework | An enforcement engine (that's PQSEC) |
| A guide to component relationships | A replacement for component specs |
| Post-quantum ready | Post-quantum only |

### The Core Insight

**Nothing grants authority. Everything produces evidence. PQSEC refuses or doesn't refuse.**

That's the entire security model.

### Why This Exists

Modern systems fail because they assume:

* clocks are honest
* runtimes are stable
* models behave consistently
* signatures imply authority
* stored data can be protected indefinitely

These assumptions are routinely false. PQ replaces them with structural guarantees: explicit verification of time, runtime state, intent, consent, policy, and authority—all enforced deterministically through a single refusal-only core.

---

## 1. Reading Guide

### Where to Start

| If you want to... | Start with... |
|-------------------|---------------|
| Understand the architecture | This document (PQ) |
| Implement enforcement | **PQSEC** — the enforcement core |
| Implement Bitcoin custody | PQHD → PQSEC |
| Implement AI governance | PQAI → PQSEC |
| Understand time semantics | Epoch Clock |
| Understand encoding rules | PQSF |
| Implement execution boundaries | ZET/ZEB → PQEH |

### Specification Relationships

```
                    ┌─────────────────────────────────────────┐
                    │              PQ (this document)         │
                    │         Conceptual hub and guide        │
                    └─────────────────────────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
   ┌─────────────┐              ┌─────────────┐              ┌─────────────┐
   │ Epoch Clock │              │    PQSF     │              │    PQVL     │
   │  Verifiable │              │  Canonical  │              │   Runtime   │
   │    Time     │              │  Encoding   │              │ Attestation │
   └──────┬──────┘              └──────┬──────┘              └──────┬──────┘
          │                            │                            │
          └────────────────────────────┼────────────────────────────┘
                                       │
                                       ▼
                         ┌───────────────────────┐
                         │        PQSEC          │
                         │  ━━━━━━━━━━━━━━━━━━━  │
                         │   ENFORCEMENT CORE    │
                         │   All authority flows │
                         │   through here        │
                         └───────────┬───────────┘
                                     │
          ┌──────────────┬───────────┼───────────┬──────────────┐
          │              │           │           │              │
          ▼              ▼           ▼           ▼              ▼
   ┌───────────┐  ┌───────────┐ ┌─────────┐ ┌─────────┐  ┌────────────┐
   │   PQHD    │  │   PQAI    │ │ ZET/ZEB │ │  PQEH  │  │Neural Lock │
   │  Custody  │  │    AI     │ │Execution│ │Quantum  │  │  Human     │
   │  Policy   │  │ Identity  │ │Boundary │ │Hardening│  │  State     │
   └───────────┘  └───────────┘ └─────────┘ └─────────┘  └────────────┘
```

### Dependency Summary

All specifications in the PQ ecosystem produce evidence or define structure.
No specification grants authority in isolation.
All enforcement and refusal semantics are defined exclusively by **PQSEC**.

| Specification | Depends On |
|---------------|------------|
| PQSEC | PQSF, Epoch Clock, PQVL |
| PQHD | PQSEC, PQSF, Epoch Clock |
| PQAI | PQSEC, PQSF, Epoch Clock, PQVL |
| ZET / ZEB | PQSEC, Epoch Clock |
| PQEH | PQSEC, PQHD, ZET / ZEB, Epoch Clock |
| Neural Lock | PQSEC, PQSF, PQHD, Epoch Clock |
| PQVL | PQSF, Epoch Clock |
| Epoch Clock | Bitcoin |
| PQSF | Epoch Clock |

---

## 2. Architecture Principles

### 2.1 Refusal-Only Enforcement

PQ does not ask "is this allowed?" It asks "is there any reason to refuse?"

No artefact, key, model, device, or component grants authority. An operation proceeds only if PQSEC does not refuse it after evaluating all required predicates.

This is not a semantic distinction. It changes the failure mode from "fail-open on missing permission" to "fail-closed on missing evidence."

### 2.2 Evidence Production vs Authority

Every component except PQSEC produces evidence:

| Component | Produces |
|-----------|----------|
| Epoch Clock | Time artefacts (ticks) |
| PQVL | Runtime attestation envelopes |
| PQAI | Model identity, behavioural fingerprints, drift classification |
| PQHD | Custody policy, predicate requirements |
| ZET/ZEB | Execution intents and results |
| Neural Lock | Operator state attestations |

None of these artefacts carry authority. They are inputs to PQSEC, which produces the sole authoritative output: an EnforcementOutcome.

### 2.3 Single Enforcement Authority

PQSEC is the only component that produces enforcement decisions.

Any parallel enforcement logic outside PQSEC is non-conformant and creates bypass vectors. This is not a recommendation; it is a structural requirement.

### 2.4 Determinism

Given identical inputs, PQSEC produces identical outputs. There is no probabilistic evaluation, no heuristic judgment, no "usually works." Enforcement is reproducible and auditable.

### 2.5 Fail-Closed

Uncertainty results in refusal:

* Missing input → refuse
* Non-canonical encoding → refuse
* Ambiguous time → refuse
* Unverifiable signature → refuse
* Partial predicate satisfaction → refuse

There are no degraded modes for Authoritative operations.

---

## 2.6 Negative Capability Theorem (Normative)

**Location:** PQ Specification → Section 2 (Architecture Principles)

PQ defines a single enforcement authority boundary across the ecosystem.

1. **Only PQSEC MAY produce an allow signal** for any operation attempt.
2. No specification other than PQSEC MAY emit any artefact whose semantics are “ALLOW”, “APPROVE”, “PERMIT”, or any equivalent authority-granting output.
3. All other specifications define structure or produce evidence only. They MUST NOT grant authority, directly or indirectly.
4. Any implementation or component that produces an allow signal outside PQSEC is **non-conformant** and creates enforcement bypass vectors.

This theorem is an ecosystem-wide invariant and applies uniformly across custody, execution, time, runtime evidence, AI operations, and human-state extensions.

---

## 3. Component Overview

### 3.1 Epoch Clock — Verifiable Time

**Problem:** System clocks lie. Network time can be manipulated.

**Solution:** Bitcoin-anchored, threshold-signed time artefacts.

Epoch Clock produces signed ticks that can be verified independently. Profiles are inscribed as Bitcoin ordinals (immutable). Ticks are distributed via mirrors without trust requirements. Consumers verify signatures locally.

Epoch Clock produces time artefacts only. It does not enforce freshness—PQSEC does.

**Specification:** Epoch Clock v2.1.1

### 3.2 PQSF — Canonical Encoding and Cryptographic Indirection

**Problem:** Ambiguous encoding breaks signatures. Algorithm transitions break systems.

**Solution:** Deterministic CBOR, JCS Canonical JSON (for Epoch Clock), and CryptoSuiteProfile indirection.

PQSF defines how artefacts are encoded, hashed, and signed. It provides cryptographic agility through profile references—algorithm changes don't require architectural changes.

PQSF defines grammar and encoding only. It grants no authority.

**Specification:** PQSF v2.0.2

### 3.3 PQVL — Runtime Attestation

**Problem:** Compromised runtimes produce compromised outputs.

**Solution:** Deterministic probe collection, baseline comparison, and drift classification.

PQVL produces attestation envelopes describing measured runtime state. Drift is classified as NONE, WARNING, or CRITICAL. Attestation is evidence, not permission—PQSEC decides what to do with it.

**Specification:** PQVL v1.0.3

### 3.4 PQSEC — Enforcement Core

**Problem:** Distributed enforcement creates bypass vectors.

**Solution:** Single, deterministic, refusal-only enforcement authority.

PQSEC consumes evidence from all other components and produces exactly one outcome per operation: ALLOW, DENY, or FAIL_CLOSED_LOCKED. It evaluates predicates, enforces freshness and monotonicity, manages lockout, and maintains audit trails.

**PQSEC is where authority lives. All other components feed into it.**

**Specification:** PQSEC v2.0.1

### 3.5 PQHD — Custody Authority

**Problem:** Key possession is treated as authority. Keys can be stolen.

**Solution:** Predicate-driven custody where keys are necessary but not sufficient.

PQHD defines what must be true before Bitcoin signing is allowed: time bounds, consent, policy, runtime integrity, quorum, ledger continuity. Key possession alone conveys no authority.

PQHD defines custody policy. PQSEC enforces it.

**Specification:** PQHD v1.1.0

### 3.6 ZET/ZEB — Execution Boundary

**Problem:** Executable artefacts exist before authorization completes, enabling front-running and reaction attacks.

**Solution:** Strict phase separation between intent and execution.

ZET defines a rail-agnostic execution boundary: intents are non-authoritative and safe to observe; execution occurs only after PQSEC approval. ZEB implements the Bitcoin profile with broadcast discipline and exposure detection.

ZET/ZEB provide execution mechanics only. They grant no authority.

**Specification:** ZEB v1.2.0 (includes ZET)

### 3.7 PQEH — Post-Quantum Execution Hardening

**Problem:** Classical signatures can be observed before broadcast, enabling quantum pre-construction attacks.

**Solution:** S1/S2 revelation pattern that denies pre-construction.

PQEH separates commitment (S1, non-executable) from execution revelation (S2). No valid transaction exists until S1 is revealed, which happens only after PQSEC approval and immediately before broadcast. This reduces the quantum attack window from signing-to-confirmation to broadcast-to-confirmation.

PQEH does not provide full post-quantum immunity (a Bitcoin consensus limitation). It provides state-of-the-art denial-of-pre-construction within current consensus.

**Specification:** PQEH v2.1.1

### 3.8 PQAI — AI Identity and Drift

**Problem:** AI systems cannot be trusted to self-assert safety or permission.

**Solution:** Externalized behavioural verification through inspectable artefacts.

PQAI defines model identity binding, behavioural fingerprinting, drift detection, and SafePrompt consent binding. Models cannot self-classify their action authority. PQSEC gates AI operations based on PQAI artefacts.

**Specification:** PQAI v1.1.1

### 3.9 Neural Lock — Human State Attestation (Extension)

**Problem:** Coercion attacks succeed because keys equal authority.

**Solution:** Operator state as an additional predicate dimension.

Neural Lock produces attestations about human cognitive/physiological state (NORMAL, STRESSED, DURESS, IMPAIRED). It does not authorize or sign transactions—it provides evidence that PQSEC can use to gate high-risk operations.

Neural Lock is optional and deployment-specific.

**Specification:** Neural Lock v1.0.0

---

## 4. What PQ Eliminates

PQ structurally eliminates the following failure classes:

| Failure Class | Eliminated By |
|---------------|---------------|
| Replay attacks | Epoch Clock ticks + single-use binding |
| Time forgery | Bitcoin-anchored, threshold-signed time |
| Silent runtime compromise | PQVL attestation + PQSEC drift gating |
| AI behavioural drift | PQAI fingerprinting + drift classification |
| Consent reuse | Session-bound, single-use ConsentProof |
| Execution-gap attacks | ZET boundary + PQEH S1/S2 pattern |
| Key-equals-authority | PQHD predicate composition |
| Distributed enforcement bypass | PQSEC consolidation |

These are structural guarantees, not probabilistic mitigations.

---

## 5. What PQ Does Not Define

PQ explicitly does NOT define:

* Identity federation or SSO protocols
* OAuth, JWT, SAML, or X.509 compatibility
* Transport-layer authorization
* Optimistic execution models
* Heuristic or probabilistic enforcement
* Implicit trust assumptions
* Privacy or anonymity guarantees
* Censorship resistance
* Miner behaviour or mempool strategy

These are either out of scope or explicitly rejected as incompatible with PQ's security model.

---

## 6. Conformance

### 6.1 Ecosystem Conformance

An implementation claiming PQ ecosystem conformance MUST:

1. Delegate all enforcement to PQSEC
2. Use Epoch Clock ticks for all time references
3. Use PQSF canonical encoding for all signed/hashed artefacts
4. Treat no artefact as authoritative until PQSEC evaluation
5. Fail closed on any ambiguity, missing input, or verification failure

### 6.2 Component Conformance

Each component specification defines its own conformance requirements. See individual specifications for details.

### 6.3 Non-Conformance

The following patterns are explicitly non-conformant:

* Parallel enforcement logic outside PQSEC
* System clock usage for authority decisions
* Non-canonical encoding of signed artefacts
* Implicit trust in network identity, coordinator identity, or mirror identity
* Degraded modes for Authoritative operations
* Model self-assertion of action class or permission

---

## 7. Version Compatibility

### 7.1 Current Versions

| Specification | Version | Status |
|---------------|---------|--------|
| PQ (this document) | 2.0.0 | Implementation Ready |
| Epoch Clock | 2.1.1 | Implementation Ready |
| PQSF | 2.0.2 | Implementation Ready |
| PQSEC | 2.0.1 | Implementation Ready |
| PQVL | 1.0.3 | Implementation Ready |
| PQHD | 1.1.0 | Implementation Ready |
| ZEB (includes ZET) | 1.2.0 | Implementation Ready |
| PQEH | 2.1.1 | Implementation Ready |
| PQAI | 1.1.1 | Implementation Ready |
| Neural Lock | 1.0.0 | Domain Evaluation Requested |

### 7.2 Deprecated Specifications

| Specification | Status | Superseded By |
|---------------|--------|---------------|
| UDC (User-Defined Control) | DEPRECATED | PQAI + PQSEC |

---

## 8. Security Considerations

### 8.1 Threat Model

PQ assumes adversaries may:

* Compromise individual devices, coordinators, or mirrors
* Manipulate system clocks and network time
* Replay, reorder, or suppress messages
* Present stale or fabricated artefacts
* Possess future quantum computation capability
* Exploit ambiguity in encoding or representation
* Attempt model substitution or behavioural manipulation
* Coerce or impersonate legitimate operators

### 8.2 Trust Assumptions

PQ operates under minimal trust assumptions:

* Bitcoin blockchain consensus is honest majority
* Threshold signature schemes resist minority compromise
* Hash functions (SHA-256, SHAKE-256) are pre-image resistant
* Cryptographic verification is performed locally
* Canonical encoding eliminates representation ambiguity

PQ does NOT assume:

* Trusted system clocks
* Trusted networks or coordinators
* Trusted runtimes without attestation
* Honest model self-reporting
* Secrecy of classical key material (for post-quantum readiness)

### 8.3 Residual Risks

PQ does not protect against:

* Total compromise of all threshold signers
* Bitcoin consensus failure
* Post-broadcast quantum attacks (within current Bitcoin consensus)
* Long-term captivity with patient adversaries
* Miner censorship or transaction exclusion

These are acknowledged limitations, not specification failures.

---

## Annex A — Quick Reference: Predicates

The following predicates are evaluated by PQSEC. This list is informative; see PQSEC for normative definitions.

| Predicate | Evaluated From |
|-----------|----------------|
| valid_structure | PQSF canonical encoding |
| valid_tick | Epoch Clock artefacts |
| valid_policy | Policy bundles |
| valid_runtime | PQVL attestation envelopes |
| valid_consent | ConsentProof artefacts |
| valid_quorum | Custody quorum satisfaction |
| valid_ledger | Ledger continuity |
| valid_action_class | PQAI action classification |
| valid_model_identity | PQAI ModelIdentity |
| valid_drift | PQAI drift classification |
| valid_delegation | DelegationConstraint artefacts |
| valid_guardian_quorum | Guardian approvals |
| recovery_delay_elapsed | Time since RecoveryIntent |
| safe_mode_active | SafeModeState |
| valid_payment_endpoint | PaymentEndpointKey (compliance) |
| operator_state_ok | Neural Lock attestation |

---

## Annex B — Glossary

**Artefact** — A cryptographically signed, canonically encoded data structure produced by a PQ component.

**Authoritative Operation** — An operation with irreversible effects (signing, custody mutation, policy change). Requires PQSEC ALLOW outcome.

**Drift** — Measured deviation from baseline behaviour. Classified as NONE, WARNING, or CRITICAL.

**EnforcementOutcome** — The authoritative decision produced by PQSEC: ALLOW, DENY, or FAIL_CLOSED_LOCKED.

**Epoch Clock Tick** — A signed, monotonic time artefact anchored to Bitcoin.

**Execution Gap** — The dangerous period when executable artefacts exist before authorization completes.

**Fail-Closed** — Security posture where uncertainty results in refusal rather than permission.

**Non-Authoritative Operation** — A read-only operation with no irreversible effects.

**Predicate** — A boolean condition that must be satisfied for an operation to proceed.

**Refusal-Only** — Enforcement model where the engine only refuses; it never grants authority.

**S1/S2 Pattern** — PQEH revelation pattern separating commitment (S1) from execution capability (S2).

---

PQ — Post-Quantum Security Ecosystem
Changelog
Version 2.0.0 (Current)
Enforcement Centralization: Centralized all enforcement logic and authority decisions into a single deterministic core: PQSEC.

Scope Expansion: Shifted from "PQ-ready" cryptography to addressing modern "execution-gap" exploits, including replay, time forgery, and consent reuse.

Structural Decoupling: Redefined the relationship between modules (Clock, VL, AI) such that no component grants authority in isolation; they now provide verifiable predicates for the core enforcement layer.

Deprecation Management: Formally retired the UDC specification and moved its normative functions into the PQAI module.

---

Changelog
Version 2.0.0 (Current)
Architectural Refactoring: Re-defined the ecosystem as a composed set of specifications where no component grants authority in isolation.

Authority Externalization: Formally delegated all enforcement, refusal, and gating semantics to the PQSEC module.

Scope Update: Expanded the ecosystem's focus to address "execution-gap" exploits—such as replay, time forgery, and consent reuse—alongside long-term quantum-capable adversary protection.

Lifecycle Management: Formally retired the UDC specification and coordinated the migration of its functionality into the PQAI and PQSEC modules.

---

## Acknowledgements

The PQ ecosystem builds on decades of work in cryptography, distributed systems, protocol design, and adversarial security analysis.

### Foundational Contributions

* **Satoshi Nakamoto** — for Bitcoin's trust-minimised consensus model
* **Whitfield Diffie and Martin Hellman** — for public-key cryptography
* **Ralph Merkle** — for Merkle trees and tamper-evident structures
* **Daniel J. Bernstein** — for cryptographic engineering and constant-time design
* **The NIST Post-Quantum Cryptography Project** — for standardising post-quantum primitives

### Protocol and Systems Influences

* **The IETF CBOR, COSE, and TLS working groups** — for canonical encoding and session binding primitives
* **Bitcoin Core developers and BIP contributors** — for PSBT, Taproot, and script semantics
* **Zero-trust architecture researchers** — for refusal-based security models
* **Byzantine fault tolerance researchers** — for threshold and quorum patterns

### AI Safety Contributions

* **Stuart Russell, Paul Christiano, and AI alignment researchers** — for externalised oversight models
* **Anthropic, OpenAI, and model evaluation researchers** — for behavioural analysis frameworks

### Specification Development

This ecosystem was developed through extensive collaboration with AI systems, demonstrating that human-AI partnership can produce rigorous, auditable security specifications. The architectural patterns, authority boundaries, and fail-closed semantics emerged from iterative refinement across hundreds of review cycles.

Any errors or omissions remain the responsibility of the author.

---

If you find this work useful and want to support continued development:

**Bitcoin:**  
bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw
