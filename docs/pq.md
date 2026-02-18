# PQ — Post-Quantum Security Ecosystem

**An Open Standard for Deterministic, Post-Quantum-Safe Custody, Compliance, and AI Operations**

* **Version:** 3.0.0
* **Date:** 2026
* **Author:** rosiea
* **Contact:** [PQRosie@proton.me](mailto:PQRosie@proton.me)
* **Licence:** Apache License 2.0 — Copyright 2026 rosiea
* **PQ Ecosystem:** HUB — Living index and architectural overview. Not an implementable specification.

---

## PQ in 60 Seconds

**What it does:** PQ prevents security failures that succeed daily — replay attacks, time forgery, consent reuse, execution-gap exploits, silent AI drift — while preparing for quantum-capable adversaries.

**How it works:** Every component produces cryptographic evidence. No component grants authority. A single deterministic engine (PQSEC) evaluates all evidence and makes every enforcement decision. Missing evidence means refusal, not trust.

**What it covers:** Bitcoin custody, AI governance, embodied robotics, persistent state, verifiable time — all governed by the same architecture.

**Try it now:** Run `python3 pq_hello.py` to see the architecture working in under 500 lines.

**Go deeper:** Read the Ecosystem Overview (5 pages) → this document → the specification for your domain.

---

## Summary

PQ is a composed ecosystem of specifications that eliminates entire classes of security failures present in modern systems while ensuring cryptographic agility for the post-quantum transition.

Most post-quantum projects focus narrowly on future cryptography. PQ addresses attacks that succeed daily—replay, time forgery, silent runtime compromise, consent reuse, execution-gap exploitation—while preparing for quantum-capable adversaries.

PQ replaces trust assumptions with explicit, verifiable predicates. No component grants authority in isolation. All enforcement flows through a single deterministic core: **PQSEC**.

Bitcoin is the reference deployment. It is not the scope.

**This document is a conceptual overview and ecosystem guide. For normative enforcement semantics, predicate definitions, and implementation requirements, see PQSEC.**

---

## Non-Normative Overview — For Explanation and Orientation Only

**This section is NOT part of the conformance surface.
It is provided for explanatory and onboarding purposes only.**

### Getting Started

The fastest way to understand PQ is to run the proof-of-concept: `python3 pq_hello.py` (in this repository). It demonstrates the core architecture—tick verification, canonical encoding, ternary predicate evaluation, capability–authority decoupling, and burn semantics—in under 500 lines.

If you're evaluating PQ for adoption, start with the Ecosystem Overview (companion document), then read this document's architecture principles (§2), then look at the specification relevant to your domain.

PQ is designed for incremental adoption. Full ecosystem conformance is the goal, but PQSEC's enforcement profiles (Annex AU) define Advisory mode (log-only, no enforcement) and Bridge mode (mixed-conformance interoperability) for deployments that need migration paths. Real-world systems can adopt PQ component by component, beginning with the enforcement core and time authority and expanding as implementation matures.

### Plain Summary

PQ is a family of specifications that work together to provide deterministic, auditable security for custody, AI operations, embodied systems, and regulated transactions. Each specification produces evidence or defines structure. None grants authority alone. Authority emerges only when all required predicates are satisfied and evaluated by PQSEC.

### What PQ Is / Is Not

| PQ IS | PQ IS NOT |
|-------|-----------|
| An ecosystem of composed specifications | A single monolithic protocol |
| A conceptual and architectural framework | An enforcement engine (that's PQSEC) |
| A guide to component relationships | A replacement for component specs |
| Post-quantum ready | Post-quantum only |
| Rail-agnostic in core design | Bitcoin-specific (Bitcoin is reference deployment) |

### The Core Insight

**Nothing grants authority. Everything produces evidence. PQSEC determines the outcome.**

That's the entire security model.

### Why This Exists

Modern systems fail because they assume:

* clocks are honest
* runtimes are stable
* models behave consistently
* signatures imply authority
* stored data can be protected indefinitely
* physical actuators can be trusted without governance

These assumptions are routinely false. PQ replaces them with structural guarantees: explicit verification of time, runtime state, intent, consent, policy, and authority—all enforced deterministically through a single refusal-only core.

---

## 1. Reading Guide

### Where to Start

| If you want to... | Start with... |
|-------------------|---------------|
| Understand the architecture | This document (PQ) |
| Implement enforcement | **PQSEC** — the enforcement core |
| Implement Bitcoin custody | PQHD → BPC → PQSEC |
| Implement AI governance | PQAI → PQPS → PQSEC |
| Understand time semantics | Epoch Clock |
| Understand encoding rules | PQSF |
| Implement execution boundaries | ZET/ZEB or SEAL |
| Implement embodied agent governance | PQEA → PQSEC |
| Build human-readable policy interfaces | PQHR |
| Review the fail-closed property | Fail-Closed Matrix |

### Specification Map

```
                    ┌─────────────────────────────────────────┐
                    │              PQ (this document)         │
                    │      Conceptual hub and ecosystem guide │
                    └─────────────────────────────────────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
   ┌─────────────┐              ┌─────────────┐              ┌─────────────┐
   │ Epoch Clock │              │    PQSF     │              │    PQAI     │
   │  Verifiable │              │  Canonical  │              │     AI      │
   │    Time     │              │  Encoding   │              │  Evidence   │
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
       ┌──────────┬─────────┬────────┼────────┬──────────┬──────────┐
       │          │         │        │        │          │          │
       ▼          ▼         ▼        ▼        ▼          ▼          ▼
  ┌────────┐ ┌────────┐ ┌───────┐ ┌─────┐ ┌────────┐ ┌──────┐ ┌──────┐
  │  PQHD  │ │  BPC   │ │ZET/ZEB│ │PQPS │ │  PQEA  │ │Neural│ │ PQHR │
  │Custody │ │Pre-Con │ │ Exec  │ │State│ │Embodied│ │ Lock │ │Render│
  │ Policy │ │ Gate   │ │Bounds │ │ Gov │ │ Agents │ │      │ │      │
  └────────┘ └────────┘ └───────┘ └─────┘ └────────┘ └──────┘ └──────┘
                                                          
       STANDALONE (optional, independently implementable):
       ┌────────┐ ┌────────┐ ┌────────┐
       │  SEAL  │ │  PQPR  │ │  PQAA  │
       │Sealed  │ │Proof of│ │Attestn │
       │  Exec  │ │  Ref   │ │Adapter │
       └────────┘ └────────┘ └────────┘

       PRODUCT (composes specs into deployable surface):
       ┌──────────────────────────────────┐
       │           PQ Gateway             │
       │  Sovereign AI Governance Layer   │
       │  Composes: PQSEC, PQSF, PQAI,  │
       │  Epoch Clock, PQHD, PQHR, PQPS │
       └──────────────────────────────────┘
```

### Dependency Summary

All specifications in the PQ ecosystem produce evidence or define structure.
No specification grants authority in isolation.
All enforcement and refusal semantics are defined exclusively by **PQSEC**.

| Specification | Classification | Depends On |
|---------------|----------------|------------|
| PQSF | CORE — FOUNDATION | Epoch Clock (JCS encoding exception) |
| PQSEC | CORE — ENFORCEMENT | PQSF, Epoch Clock, PQAI |
| PQHD | CORE — CUSTODY_POLICY | PQSEC, PQSF, Epoch Clock |
| Epoch Clock | CORE — TIME_AUTHORITY | Bitcoin |
| BPC | CORE — PRECONSTRUCTION_GATING | PQSF, Epoch Clock |
| ZEB (includes ZET) | CORE — EXECUTION_PROFILE | PQSEC, PQSF, Epoch Clock |
| PQAI | CORE — AI_EVIDENCE | PQSF, Epoch Clock |
| PQPS | CORE — STATE_GOVERNANCE | PQSEC, PQSF, Epoch Clock, PQAI, BPC |
| PQEA | CORE — EMBODIED_EVIDENCE | PQSEC, PQSF, Epoch Clock, PQAI |
| Neural Lock | CORE — OPERATOR_EVIDENCE | PQSEC, PQSF, Epoch Clock |
| PQHR | CORE — HOLDER_RENDERING | PQSEC, PQSF, Epoch Clock, PQPS |
| SEAL | STANDALONE — EXECUTION_PROFILE | Independently implementable. PQ alignment optional. |
| PQPR | STANDALONE — AUDIT_TOOLING | Independently implementable. PQ alignment optional. |
| PQAA | STANDALONE — ATTESTATION_ADAPTER | Independently implementable. PQ alignment optional. |
| PQ Gateway | PRODUCT — AI_GOVERNANCE_LAYER | PQSEC, PQSF, PQAI, Epoch Clock, PQHD, PQHR, PQPS, PQAA (optional) |

**Integration notes:**
BPC: In PQ ecosystem deployments, BPC evaluation is consumed by PQSEC prior to execution. PQSEC is not a normative dependency of BPC itself but is required for authoritative PQ stack deployments.
PQAI: PQAI artefacts are evaluated by PQSEC in composed deployments. PQAI artefact definitions are self-contained.
PQ Gateway: PQ Gateway composes existing specifications into a deployable AI governance product. It introduces no new enforcement primitives. All enforcement remains exclusively within PQSEC.

---

## 2. Architecture Principles

### 2.1 Refusal-Only Enforcement

PQ does not ask "is this allowed?" It asks "is there any reason to refuse?"

No artefact, key, model, device, or component grants authority. An operation proceeds only if PQSEC does not refuse it after evaluating all required predicates.

This is not a semantic distinction. It changes the failure mode from "fail-open on missing permission" to "fail-closed on missing evidence."

---

### 2.2 Evidence Production vs Authority

Every component except PQSEC produces evidence:

| Component | Produces |
|-----------|----------|
| Epoch Clock | Time artefacts (ticks) |
| PQAI | Model identity, behavioural fingerprints, drift classification |
| PQHD | Custody policy, predicate requirements |
| BPC | Pre-construction authorization outcomes |
| ZET/ZEB | Execution intents and results |
| PQPS | Persistent relational state evidence |
| PQEA | Embodied agent operation envelopes |
| Neural Lock | Operator state attestations |
| SEAL | Submission evidence for sealed execution |
| PQHR | Rendered policy interfaces (non-enforcement) |

None of these artefacts carry authority. They are inputs to PQSEC, which produces the sole authoritative output: an EnforcementOutcome.

---

### 2.3 Single Enforcement Authority

PQSEC is the only component that produces enforcement decisions.

Any parallel enforcement logic outside PQSEC is non-conformant and creates bypass vectors. This is not a recommendation; it is a structural requirement.

---

### 2.4 Determinism

Given identical inputs, PQSEC produces identical outputs. There is no probabilistic evaluation, no heuristic judgment, no "usually works." Enforcement is reproducible and auditable.

---

### 2.5 Fail-Closed

Uncertainty results in refusal:

* Missing input → refuse
* Non-canonical encoding → refuse
* Ambiguous time → refuse
* Unverifiable signature → refuse
* Partial predicate satisfaction → refuse

There are no degraded modes for Authoritative operations. The Fail-Closed Matrix (see companion document) maps every failure condition across all specifications to its enforcement outcome and confirms no silent degrade path exists.

---

### 2.6 Authority Separation

No component is both evidence producer and authority source. Compromising any single component—sensor, model, clock, key—cannot gain authority because authority lives exclusively in PQSEC's predicate evaluation, and PQSEC doesn't produce the evidence it evaluates.

Every specification includes an explicit Authority Boundary section stating it grants no authority. This is structurally enforced through the dependency graph.

---

### 2.7 Enforcement Invariant (Ecosystem Requirement)

The enforcement invariant is normatively defined in PQSEC. This section summarizes that invariant for explanatory purposes only.

Across the entire PQ ecosystem, enforcement authority is centralized. Only PQSEC may emit an authoritative ALLOW outcome for any operation attempt. No other specification, component, artefact, or subsystem may emit any signal whose semantics imply permission, approval, or execution capability. All other specifications define structure or produce evidence only. Any implementation that produces an allow or approval signal outside PQSEC is non-conformant and creates enforcement bypass vectors.

This invariant applies uniformly across custody, execution, time, AI operations, embodied systems, persistent state, and human-state extensions.

---

## 3. Component Overview

### 3.1 Epoch Clock — Verifiable Time

**Problem:** System clocks lie. Network time can be manipulated.

**Solution:** Bitcoin-anchored, threshold-signed time artefacts.

Epoch Clock produces signed ticks that can be verified independently. Profiles are inscribed as Bitcoin ordinals (immutable). Ticks are distributed via mirrors without trust requirements. Consumers verify signatures locally. V3 supports multi-signature tick issuance.

Epoch Clock produces time artefacts only. It does not enforce freshness—PQSEC does.

**Specification:** Epoch Clock v2.1.0

### 3.2 PQSF — Canonical Encoding and Cryptographic Indirection

**Problem:** Ambiguous encoding breaks signatures. Algorithm transitions break systems.

**Solution:** Deterministic CBOR, JCS Canonical JSON (for Epoch Clock), and CryptoSuiteProfile indirection.

PQSF defines how artefacts are encoded, hashed, and signed. It provides cryptographic agility through profile references—algorithm changes don't require architectural changes. PQSF also defines the Secure Transport Protocol (STP) for session binding, the ReceiptEnvelope standard consumed by all specifications, and schema version governance.

PQSF defines grammar and encoding only. It grants no authority.

**Specification:** PQSF v2.0.3

### 3.3 PQSEC — Enforcement Core

**Problem:** Distributed enforcement creates bypass vectors.

**Solution:** Single, deterministic, refusal-only enforcement authority.

PQSEC consumes evidence from all other components and produces exactly one outcome per operation: ALLOW, DENY, or FAIL_CLOSED_LOCKED. It evaluates predicates using a ternary model (TRUE / FALSE / UNAVAILABLE), enforces freshness and monotonicity, manages lockout via accumulative escalation, maintains audit trails, and hosts the ecosystem's refusal code registry (Annex AE), enforcement profiles (Annex AU), and specification classification registry (Annex AT).

**PQSEC is where authority lives. All other components feed into it.**

**Specification:** PQSEC v2.0.3

### 3.4 PQHD — Custody Policy

**Problem:** Key possession is treated as authority. Keys can be stolen.

**Solution:** Predicate-driven custody where keys are necessary but not sufficient.

PQHD defines what must be true before Bitcoin signing is allowed: time bounds, consent, policy, runtime integrity, quorum, ledger continuity. Key possession alone conveys no authority. This is capability–authority decoupling: possession of a valid private key is necessary but never sufficient for signing. Authority derives exclusively from predicate satisfaction as evaluated by PQSEC.

PQHD defines custody policy. PQSEC enforces it.

**Specification:** PQHD v1.2.0

### 3.5 BPC — Pre-Construction Gating

**Problem:** Transaction construction without prior authorization creates execution-gap exploits.

**Solution:** Authorization-before-construction with evidence-bound outcomes.

BPC prevents the creation of executable Bitcoin transactions before authorization is obtained. No broadcast-ready transaction may exist prior to PQSEC approval. BPC's core pattern—authorization-before-construction—is rail-agnostic and is reused by other specifications (including PQPS for state mutation governance).

BPC does not grant authority. All authorization decisions are made by PQSEC.

**Specification:** BPC v1.1.0

### 3.6 ZET/ZEB — Execution Boundary

**Problem:** Executable artefacts exist before authorization completes, enabling front-running and reaction attacks.

**Solution:** Strict phase separation between intent and execution.

ZET defines a rail-agnostic execution boundary: intents are non-authoritative and safe to observe; execution occurs only after PQSEC approval. ZEB implements the Bitcoin profile with broadcast discipline, burn semantics, and exposure detection.

ZET/ZEB provide execution mechanics only. They grant no authority.

**Specification:** ZEB v1.3.0 (includes ZET)

### 3.7 PQAI — AI Identity and Drift

**Problem:** AI systems cannot be trusted to self-assert safety or permission.

**Solution:** Externalized behavioural verification through inspectable artefacts.

PQAI defines model identity binding, behavioural fingerprinting, drift detection, SafePrompt consent binding, tool capability governance, and safety domain classification. Models cannot self-classify their action authority. Self-referential loops are classified as CRITICAL drift. PQSEC gates AI operations based on PQAI artefacts.

**Specification:** PQAI v1.2.0

### 3.8 PQPS — Persistent State Governance

**Problem:** AI relational memory creates privacy, sovereignty, and governance challenges.

**Solution:** Bilateral human-AI relational persistence with explicit facets, holder sovereignty, and drift control.

PQPS defines the primitives, storage semantics, update mechanics, and governance for persistent relational state between a human and an AI system. The human always retains sovereignty over both sides. State presence never grants authority. All mutation requires holder authorization (via BPC's authorization-before-construction pattern) and PQSEC enforcement.

**Specification:** PQPS v1.0.0

### 3.9 PQEA — Embodied Agent Governance

**Problem:** Physical AI systems (robotics, autonomous agents) require governance that accounts for hardware reality and real-time constraints.

**Solution:** Operation envelopes, execution leases, perception sufficiency, and safety state evidence.

PQEA governs AI systems that interact with the physical world. It defines operation schemas, constraint maps, safety profiles, execution leases with heartbeat re-evaluation, perception sufficiency as a first-class refusal condition, and delegation with bounded scope. The §1.4 hardware reality clause requires that paper compliance without hardware capability is non-conformant.

PQEA produces evidence only. PQSEC enforces it.

**Specification:** PQEA v1.0.0

### 3.10 Neural Lock — Human State Attestation

**Problem:** Coercion attacks succeed because keys equal authority.

**Solution:** Operator state as an additional predicate dimension.

Neural Lock produces attestations about human cognitive/physiological state (NORMAL, STRESSED, DURESS, IMPAIRED). It does not authorize or sign transactions—it provides evidence that PQSEC can use to gate high-risk operations. Classification is deliberately coarse (four states) because it is risk-reduction evidence, not proof of coercion.

Neural Lock is optional and deployment-specific.

**Specification:** Neural Lock v1.1.0

### 3.11 PQHR — Human-Readable Policy Interface

**Problem:** Security policies rendered poorly or misleadingly undermine the security they represent.

**Solution:** Normative rendering requirements for holder-facing policy interfaces.

PQHR defines how custody state, enforcement outcomes, refusal conditions, and persistent state are rendered to humans. Prohibited rendering patterns ensure structural refusals are not collapsed, degraded states are not minimised, and AI-side state is not presented as fact.

PQHR defines rendering obligations. It does not grant authority.

**Specification:** PQHR v1.0.0

### 3.12 SEAL — Sealed Execution (STANDALONE)

**Problem:** Classical signatures can be observed before broadcast, enabling quantum pre-construction attacks.

**Solution:** End-to-end execution confidentiality from construction through confirmation.

SEAL provides encrypted submission to trusted endpoints, eliminating the public mempool exposure window. Transactions are never observable in plaintext until confirmed on-chain. SEAL uses a bounded execution state machine (PENDING → SUBMITTED → CONFIRMED / FAILED) with no automatic retry and explicit authorization required for recovery from FAILED.

SEAL is independently implementable. PQ ecosystem alignment is optional.

**Specification:** SEAL v2.0.0

### 3.13 PQPR — Proof of Reference (STANDALONE)

**Problem:** Cross-specification references can drift, creating ambiguity.

**Solution:** Automated reference verification tooling.

PQPR provides tooling for verifying that cross-specification references (section numbers, refusal codes, predicate names) remain accurate as specifications evolve. It is audit infrastructure, not enforcement.

PQPR is independently implementable. PQ ecosystem alignment is optional.

**Specification:** PQPR v1.0.0

### 3.14 PQAA — PQ Attestation Adapter (STANDALONE)

**Problem:** Platforms provide integrity evidence (TPM quotes, Secure Enclave attestations, Android Keystore attestations, OS integrity measurements) through proprietary APIs that produce non-PQ artefacts. Without a governed bridge, this evidence is either ignored entirely or consumed through ungoverned application-specific shims that bypass enforcement discipline.

**Solution:** Manifest-bound attestation translation with hash-only evidence transport.

PQAA translates platform-native attestation signals into canonical `platform_bridged` evidence artefacts consumable by PQSEC. Every adapter is governed by a signed manifest that declares its identity, binary hash, permitted attestation sources, and tick-bounded validity. PQAA carries only the SHAKE256-256 hash of the original platform artefact — never the raw payload — preventing the evidence channel from becoming a data exfiltration vector. Evidence is classified under the `platform_bridged` evidence class (PQSF §32B.2) and evaluated by PQSEC under profile-specific admission rules (PQSEC Annex BA.3B).

PQAA produces evidence only. It does not evaluate predicates or grant authority. All enforcement decisions remain exclusively within PQSEC.

PQAA is independently implementable. PQ ecosystem alignment is optional.

**Specification:** PQAA v1.0.0

---

### 3.15 PQ Gateway — Sovereign AI Governance Layer (PRODUCT)

**Problem:** AI model providers offer no structural governance guarantees. Users accept terms of service, hope alignment works, and have no mechanical control over what models can do, what tools they can access, or how their data is handled. Every governance approach in the current landscape is top-down — the platform decides the rules.

**Solution:** A sovereignty-preserving governance layer that sits between users and any model provider.

PQ Gateway composes existing PQ specifications into a single deployable product. Users define their own policy through a structured authoring interface (PQGW-CONTROL). The gateway enforces it structurally. Every prompt is session-bound via STP (PQSF §27), tick-bounded by Epoch Clock, intent-hashed, and evaluated against the user's policy by PQSEC before it reaches any provider. Every response returns through the same enforcement surface. Every operation produces a signed ReceiptEnvelope artefact.

Models do not need to be modified, trusted, or aware they are governed. Enforcement does not depend on model behaviour. It depends on deterministic evaluation of evidence.

PQ Gateway introduces six product-layer components: Gateway Router (PQGW-ROUTER), Policy Authoring (PQGW-CONTROL), Provider Adapters (PQGW-ADAPTER), Billing and Metering (PQGW-METER), Enrollment and Onboarding (PQGW-ONBOARD), and Provider Registry (PQGW-REGISTRY). All six are evidence producers and orchestration layers only. None evaluates predicates or produces EnforcementOutcome artefacts. All enforcement remains exclusively within PQSEC.

**Specification:** PQ Gateway v1.0.0

---

## 4. What PQ Eliminates

PQ structurally eliminates the following failure classes:

| Failure Class | Eliminated By |
|---------------|---------------|
| Replay attacks | Epoch Clock ticks + single-use binding |
| Time forgery | Bitcoin-anchored, threshold-signed time |
| Silent runtime compromise | PQAI attestation + PQSEC drift gating |
| AI behavioural drift | PQAI fingerprinting + drift classification |
| Consent reuse | Session-bound, single-use ConsentProof |
| Execution-gap attacks | ZET boundary + BPC pre-construction gating |
| Quantum pre-construction | SEAL execution confidentiality |
| Key-equals-authority | PQHD capability–authority decoupling |
| Distributed enforcement bypass | PQSEC consolidation |
| Unverified AI persistent state mutation | PQPS holder sovereignty + BPC authorization |
| Ungoverned embodied agent actuation | PQEA operation envelopes + lease governance |
| Coercion attacks | Neural Lock operator state evidence |
| Ungoverned AI model interaction | PQ Gateway policy enforcement + provider governance |

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

* **Emergency Revocation and Kill-Switches:**
  PQ does not define emergency revocation or "kill switch" orchestration at the ecosystem level. Revocation semantics, including identity or session invalidation under compromise, are expected to be defined by producing specifications and enforced by PQSEC through existing refusal, lockout, and monotonicity guarantees.

* **Hardware-Rooted Attestation:**
  PQ does not define manufacturer trust anchors, hardware roots of trust, or device-specific measurement grammars (e.g., TPM, SGX, TEE). Where hardware attestation is required, it MUST be provided by an external producing specification and consumed as evidence by PQSEC. PQ intentionally avoids embedding vendor- or jurisdiction-specific trust assumptions into the core ecosystem.

* **Social Recovery Orchestration:**
  While PQ supports multi-signature custody models, guardian quorums, and recovery delays via PQHD and PQSEC, it does not define the user-experience, communication, or coordination protocols for social recovery. Recovery orchestration is the responsibility of the implementing wallet or custody service.

* **Real-Time Control Loops:**
  PQEA governs embodied agent operations at the governance layer. Real-time servo-loop control (sub-millisecond actuation) is the responsibility of the adapter within PQEA execution lease bounds. PQ does not define real-time control algorithms.

---

## 6. Conformance

### 6.1 Ecosystem Conformance

An implementation claiming **PQ ecosystem conformance** MUST:

1. Delegate all enforcement to PQSEC.
2. Use Epoch Clock ticks for all time references.
3. Use PQSF canonical encoding for all signed or hashed artefacts.
4. Treat no artefact as authoritative until PQSEC evaluation.
5. Fail closed on any ambiguity, missing input, or verification failure.

Ecosystem conformance asserts that enforcement authority is centralized, deterministic, refusal-only, and structurally consolidated within PQSEC.

---

### 6.2 Component Conformance

Each component specification within the PQ ecosystem defines its own conformance requirements.

An implementation MAY be conformant to individual component specifications without claiming PQ ecosystem conformance.

Component-level conformance does not imply enforcement correctness unless all ecosystem conformance requirements are also satisfied.

---

### 6.3 Non-Conformance

The following patterns are incompatible with PQ's security model. Implementations exhibiting these patterns cannot claim PQ ecosystem conformance, but may still benefit from individual component specifications (see §6.2).

- Parallel enforcement logic outside PQSEC.
- Use of system clocks for authority, freshness, or expiry decisions.
- Non-canonical encoding of signed or hashed artefacts.
- Implicit trust in network identity, coordinator identity, or mirror identity.
- Degraded, heuristic, or best-effort modes for Authoritative operations.
- Model self-assertion of action class, permission, or authority.
- AI self-mutation of persistent state without holder authorization.
- Embodied agent actuation without valid execution lease.

Deployments transitioning toward conformance can use PQSEC's Advisory mode (Annex AU) to evaluate enforcement decisions without blocking operations, providing a safe migration path.

---

## 7. Version Compatibility

### 7.0 Ecosystem Minimum Versions

Implementations claiming **PQ ecosystem conformance** MUST meet the minimum specification versions below.

These minimums define the lowest versions at which the specifications are considered mutually compatible at the ecosystem level. They do not replace or override component-specific conformance requirements defined in individual specifications.

| Specification | Minimum Version | Notes |
|---------------|-----------------|-------|
| Epoch Clock | ≥ 2.1.0 | Verifiable time artefacts |
| PQSF | ≥ 2.0.3 | Canonical encoding, STP, ReceiptEnvelope |
| PQSEC | ≥ 2.0.3 | Deterministic enforcement core |
| PQAI | ≥ 1.2.0 | AI evidence (when applicable) |

Implementations MAY evaluate using earlier versions for testing or research purposes, but MUST NOT claim PQ ecosystem conformance while below the stated minimum versions.

---

### 7.1 Current Versions

The following specification versions are aligned and implementation-ready within the PQ ecosystem:

| Specification | Version | Classification | Status |
|---------------|---------|----------------|--------|
| PQ (this document) | 3.0.0 | HUB | Implementation Ready |
| Epoch Clock | 2.1.0 | CORE | Implementation Ready |
| PQSF | 2.0.3 | CORE | Implementation Ready |
| PQSEC | 2.0.3 | CORE | Implementation Ready |
| PQHD | 1.2.0 | CORE | Implementation Ready |
| BPC | 1.1.0 | CORE | Implementation Ready |
| ZEB (includes ZET) | 1.3.0 | CORE | Implementation Ready |
| PQAI | 1.2.0 | CORE | Implementation Ready |
| PQPS | 1.0.0 | CORE | Implementation Ready |
| PQEA | 1.0.0 | CORE | Implementation Ready |
| Neural Lock | 1.1.0 | CORE | Implementation Ready |
| PQHR | 1.0.0 | CORE | Implementation Ready |
| SEAL | 2.0.0 | STANDALONE | Implementation Ready |
| PQPR | 1.0.0 | STANDALONE | Implementation Ready |
| PQAA | 1.0.0 | STANDALONE | Implementation Ready |
| PQ Gateway | 1.0.0 | PRODUCT | Implementation Ready |

---

### 7.2 Deprecated and Historical Specifications

The following specifications are formally deprecated and MUST NOT be used in new implementations:

| Specification | Status | Superseded By |
|---------------|--------|---------------|
| UDC (User-Defined Control) | TOMBSTONED | PQAI + PQSEC |
| PQVL (Runtime Attestation) | TOMBSTONED | PQSEC (runtime evidence handling, §22) and PQAI (behavioural fingerprinting and drift evidence) |
| PQEH (Execution Hardening) | HISTORICAL | SEAL (execution confidentiality) |

PQEH v2.2.0 remains available as a research specification. It is not part of the production stack.

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
* Compromise AI persistent state through gradual drift
* Exploit governance-layer latency in embodied systems

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
* Physical actuator safety without governance-layer oversight

### 8.3 Residual Risks

PQ does not protect against:

* Total compromise of all threshold signers
* Bitcoin consensus failure
* Post-broadcast quantum attacks (within current Bitcoin consensus)
* Long-term captivity with patient adversaries
* Miner censorship or transaction exclusion
* Governance-layer latency exceeding physical safety requirements (PQEA boundary)

These are acknowledged limitations, not specification failures.

---

## 9. Companion Documents

The following documents are maintained alongside this specification in the PQ repository. Companion documents are audit and onboarding artefacts. They do not expand normative requirements beyond what is defined in component specifications.

| Document | Purpose |
|----------|---------|
| **Fail-Closed Matrix** | Maps every failure condition across all specifications to its enforcement outcome. Validates no silent degrade path exists. Audit artefact only; normative requirements are defined by component specs. |
| **Ecosystem Overview** | Five-page onboarding document for reviewers, grant committees, and collaborators. |

---

## Annex A — Quick Reference: Predicates

The following predicates are evaluated by **PQSEC**.
This list is **informative only**; see **PQSEC** for normative definitions, evaluation rules, and enforcement semantics.

Predicates listed here **do not grant authority**.
They are evaluated exclusively by PQSEC according to the active enforcement configuration and policy.

| Predicate | Evaluated From |
|-----------|---------------|
| valid_structure | PQSF canonical encoding |
| valid_tick | Epoch Clock artefacts |
| valid_policy | Policy bundles |
| valid_consent | ConsentProof artefacts |
| valid_quorum | Custody quorum satisfaction |
| valid_ledger | Ledger continuity |
| valid_action_class | PQAI-derived action classification evidence |
| valid_model_identity | PQAI ModelIdentity |
| valid_drift | PQAI drift classification |
| valid_delegation | DelegationConstraint artefacts |
| valid_guardian_quorum | Guardian approvals |
| recovery_delay_elapsed | Time since RecoveryIntent |
| safe_mode_active | SafeModeState |
| valid_payment_endpoint | PaymentEndpointKey |
| operator_state_ok | Neural Lock attestation |
| valid_build_provenance | BuildAttestation and supply-chain artefacts |
| valid_runtime_signature | RuntimeSignature |
| valid_publish_signature | PublishSignature |
| valid_operation_key | OperationKey |
| valid_audit_chain | AuditSignature and ledger continuity |
| valid_human_state | PQPS human-side state evidence |
| valid_ai_state | PQPS AI-side state evidence |
| valid_embodied_envelope | PQEA operation envelope |
| valid_execution_lease | PQEA execution lease |
| valid_perception | PQEA perception sufficiency |
| valid_safety_state | PQEA safety state evidence |

---

### Annex A.1 Interpretation Boundary (Informative)

1. Predicates are **refusal-only signals**.
2. No predicate grants authority, permission, or execution capability.
3. Absence of a predicate requirement MUST NOT be interpreted as trust.
4. Supply-chain predicates are evaluated **only when explicitly required** by policy or enforcement configuration.
5. All enforcement, refusal, escalation, and lockout behaviour is defined exclusively by **PQSEC**.

This annex provides a reference map only.
Normative behaviour is defined by PQSEC.

---

## Annex B — Glossary

**Artefact** — A cryptographically signed, canonically encoded data structure produced by a PQ component.

**Authoritative Operation** — An operation with irreversible effects (signing, custody mutation, policy change). Requires PQSEC ALLOW outcome.

**Authorization-Before-Construction** — Pattern (BPC) requiring evidence-bound authorization before an executable artefact may be constructed.

**Capability–Authority Decoupling** — Architectural principle (PQHD) where possession of cryptographic capability (private key) is necessary but never sufficient for authority.

**Drift** — Measured deviation from baseline behaviour. Classified as NONE, WARNING, or CRITICAL.

**EnforcementOutcome** — The authoritative decision produced by PQSEC: ALLOW, DENY, or FAIL_CLOSED_LOCKED.

**Epoch Clock Tick** — A signed, monotonic time artefact anchored to Bitcoin.

**Execution Gap** — The dangerous period when executable artefacts exist before authorization completes.

**Execution Lease** — Time-bound, heartbeat-governed permission for embodied agent operation (PQEA).

**Fail-Closed** — Security posture where uncertainty results in refusal rather than permission.

**Holder** — The human who retains sovereignty over persistent relational state (PQPS).

**Non-Authoritative Operation** — A read-only operation with no irreversible effects.

**Predicate** — A ternary condition (TRUE / FALSE / UNAVAILABLE) evaluated by PQSEC. UNAVAILABLE maps to DENY for Authoritative operations.

**ReceiptEnvelope** — Standardised evidence container (PQSF Annex W) consumed across all specifications.

**Refusal-Only** — Enforcement model where the engine only refuses; it never grants authority.

---

## Annex C — Proof of Ignorance for Dangerous Artefacts (Experimental)

**Status:** OPTIONAL
**Maturity:** DOMAIN EVALUATION
**Authority:** Evidence-only (non-authoritative)

### C.1 Purpose and Scope

This annex exists to support auditability of refusal and neutralisation workflows under PQSEC, not to assert containment.

It defines an experimental, evidence-only protocol for producing a
Proof of Ignorance (PoI): a cryptographic artefact asserting that a classified
dangerous input was handled within a constrained execution boundary, without
the artefact becoming externally available, and that a defined neutralisation
procedure was completed.

This annex defines structure, validation rules, and evidentiary boundaries only.
All enforcement, refusal, escalation, and policy interpretation are defined
exclusively by PQSEC.

This annex introduces no authority, no allow semantics, and no mandatory
behaviour.

### C.2 Authority and Safety Boundary

1. Proof of Ignorance MUST NOT be interpreted as:
   - proof of global deletion,
   - proof of human non-awareness,
   - proof of legal or regulatory compliance,
   - proof of moral correctness, or
   - proof of absolute containment.
2. Proof of Ignorance MUST NOT grant permission, capability, or execution rights.
3. Proof of Ignorance MUST NOT override refusal, lockout, or policy constraints.
4. Absence, invalidity, or expiry of Proof of Ignorance MUST evaluate to UNAVAILABLE
   when consumed as predicate evidence by PQSEC.
5. No construct in this annex may emit ALLOW semantics.

Proof of Ignorance is conditional evidence only, produced under explicit
assumptions.

### C.3 Definitions

| Term | Definition |
|---|---|
| Dangerous Artefact | Information classified as potentially enabling catastrophic harm |
| Proof of Ignorance (PoI) | Evidence that neutralisation occurred without artefact export |
| Neutralisation | Deterministic destruction rendering artefact unrecoverable |
| AD_MODE | Ignorance-preserving execution mode |
| Secure Execution Boundary | Runtime boundary attested externally |
| Context Hash | Hash binding PoI to canonical context |

### C.4 Protocol States (Informative)

| State | Description |
|---|---|
| NORMAL | Default operation |
| AD_MODE | Ignorance-preserving handling |
| NEUTRALISED | Artefact neutralised |
| REFUSED | Operation blocked |

### C.5 Proof of Ignorance Artefact

```cddl
ProofOfIgnorance = {
  poi_version: uint,
  event_id: tstr,
  issued_tick: uint,
  epoch_tick_hash: bstr,
  context_hash: bstr,
  action: "neutralised" / "refused",
  drift_class: "NONE" / "WARNING" / "CRITICAL",
  proof_payload: bstr,
  suite_profile: tstr,
  signature: bstr
}
```

### C.6 Signature Computation

Signing and verification follow PQSF canonical CBOR rules with signature omission.

### C.7 Validation Rules

ProofOfIgnorance is valid if and only if:

* canonical encoding is valid (PQSF)
* poi_version == 1
* signature is valid under suite_profile
* issued_tick is valid under the active time model
* context_hash is present
* action == "neutralised" implies drift_class == "NONE"
* no unknown fields are present

Validation failures MUST be treated as UNAVAILABLE when consumed as predicate evidence by PQSEC.

### C.8 Assumptions and Limits

PoI correctness is conditional on documented assumptions including:

* valid runtime attestation, when required by policy
* deterministic neutralisation
* proof generated post-neutralisation

### C.9 Integration Guidance (Informative)

PQAI → PQSEC → AD_MODE → Neutralisation → PoI → PQSEC

### C.10 Non-Goals

This annex does not define:

* censorship
* compliance claims
* cognition claims
* enforcement logic
* classification criteria for dangerous artefacts (classification is a policy decision outside PQ's scope)

### C.11 Conformance Statement

Support MAY be claimed if:

* ProofOfIgnorance is produced canonically
* enforcement remains delegated exclusively to PQSEC
* assumptions and operating limits are documented

---

## Changelog

### Version 3.0.0 (Current)

* Added **§3.15 -- PQ Gateway — Sovereign AI Governance Layer (PRODUCT)**: component overview for PQ Gateway, a product-layer composition of existing PQ specifications into a deployable AI governance gateway.
* Updated **architecture diagram** with PQ Gateway in PRODUCT classification.
* Updated **dependency summary table** with PQ Gateway and integration note.
* Updated **§7.1 current versions table** with PQ Gateway 1.0.0.
* Updated **§4 failure class table** with "Ungoverned AI model interaction" eliminated by PQ Gateway.

* **Ecosystem Expansion:** Added BPC (pre-construction gating), PQPS (persistent state governance), PQEA (embodied agent governance), PQHR (human-readable policy), SEAL (sealed execution, standalone), PQPR (proof of reference, standalone), and PQAA (attestation adapter, standalone) to the ecosystem.
* **Specification Lifecycle:** Tombstoned UDC and PQVL. Reclassified PQEH as HISTORICAL (superseded by SEAL). Updated all version references to current production versions.
* **Authority Separation:** Added §2.6 documenting the authority separation architecture as a core principle.
* **Capability–Authority Decoupling:** Updated PQHD description to reflect the dual-control clarification (§13.1A).
* **Rail-Agnostic Framing:** Clarified that BPC's authorization-before-construction pattern is rail-agnostic and reused by PQPS for state mutation governance.
* **Dependency Graph:** Updated specification map and dependency table to reflect the full 13 CORE + 3 STANDALONE structure.
* **Version Table:** Updated all versions. Added Classification column. Added STANDALONE specifications.
* **Predicate Table:** Added PQPS, PQEA, and supply-chain predicates to Annex A.
* **Glossary:** Added Authorization-Before-Construction, Capability–Authority Decoupling, Execution Lease, Holder, ReceiptEnvelope, and updated Predicate definition to reflect ternary semantics.
* **Fail-Closed Matrix:** Referenced as companion document (§2.5, §9).
* **Companion Documents:** Added §9 with conformance boundary statement. Companion documents are audit and onboarding artefacts that do not expand normative requirements.
* **Adoption Guidance:** Added "PQ in 60 Seconds" quick-start. Added "Getting Started" section acknowledging incremental adoption, Advisory mode, and Bridge mode as migration paths. Referenced `pq_hello.py` proof-of-concept.
* **Tone:** Softened non-conformance section (§6.3) to acknowledge component-level adoption and migration paths without weakening normative requirements.
* **Annex C:** Added "why it's here" rationale (auditability of refusal workflows) and classification non-goal to Proof of Ignorance annex.

### Version 2.0.0

* **Enforcement Centralization:** Centralized all enforcement logic and authority decisions into a single deterministic core: PQSEC.
* **Scope Expansion:** Shifted from "PQ-ready" cryptography to addressing modern execution-gap exploits, including replay, time forgery, and consent reuse.
* **Structural Decoupling:** Redefined the relationship between modules such that no component grants authority in isolation; they now provide verifiable predicates for the core enforcement layer.
* **Deprecation Management:** Formally retired the UDC specification and migrated its normative functions into PQAI and PQSEC.

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

The specifications were iteratively refined through adversarial interrogation of multiple AI systems to extract governance constraints, failure modes, and enforcement invariants, then formalised into deterministic, implementation-ready standards. The architectural patterns, authority boundaries, and fail-closed semantics emerged from iterative refinement across hundreds of review cycles.

Any errors or omissions remain the responsibility of the author.

---

If you find this work useful and want to support continued development:

**Bitcoin:**
bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw
