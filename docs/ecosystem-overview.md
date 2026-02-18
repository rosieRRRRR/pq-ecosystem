# PQ Ecosystem Overview

**A Technical Introduction for Reviewers, Collaborators, and Grant Committees**

*Version 1.0.0 — 2026*
*Author: rosiea — PQRosie@proton.me*

---

## What PQ Is

PQ is a post-quantum security ecosystem comprising 13 core specifications, 3 standalone tools, and 1 product layer (PQ Gateway). It eliminates classes of security failures that succeed daily—replay, time forgery, silent runtime compromise, consent reuse, execution-gap exploitation—while preparing for quantum-capable adversaries.

PQ is not a single protocol. It is a composed system where each specification produces evidence or defines structure, and a single enforcement core (PQSEC) makes all authority decisions. Bitcoin is the reference deployment. It is not the scope.

---

## The Core Innovation: Authority Separation

The fundamental architectural insight is: **nothing grants authority unilaterally.**

Every component produces evidence. No component is both evidence producer and authority source. Compromising any single component—sensor, model, clock, key—cannot gain authority because authority lives exclusively in PQSEC's predicate evaluation, and PQSEC doesn't produce the evidence it evaluates.

This creates a new security primitive: architectural guarantee that authority requires composition of independent evidence sources, evaluated by a single deterministic engine.

| Component | Produces | Does NOT Do |
|-----------|----------|-------------|
| Epoch Clock | Signed time artefacts | Enforce freshness |
| PQSF | Canonical encoding rules | Grant authority |
| PQAI | Model identity, drift classification | Permit AI operations |
| PQHD | Custody policy requirements | Sign transactions |
| BPC | Pre-construction authorization evidence | Authorize without PQSEC |
| Neural Lock | Operator state attestations | Determine coercion |
| PQPS | Persistent state evidence | Mutate state autonomously |
| PQEA | Embodied operation envelopes | Actuate without lease |
| ZEB/ZET | Execution intents and results | Broadcast without approval |
| PQAA | Canonical `platform_bridged` evidence from native attestation APIs | Evaluate predicates or grant authority |
| **PQSEC** | **EnforcementOutcome: ALLOW / DENY / FAIL_CLOSED_LOCKED** | **Produce evidence** |
| PQ Gateway | Governed inference routing, policy authoring, provider management (PRODUCT) | Grant authority or evaluate predicates |

---

## How It Fits Together

### Dependency Graph

```
Epoch Clock ──────────────────────────┐
  (Bitcoin-anchored time)             │
                                      ▼
PQSF ─────────────────────────────► PQSEC ◄──── PQAI
  (canonical encoding)           (enforcement)    (AI evidence)
                                      │
                 ┌────────┬───────┬───┴───┬────────┬────────┬────────┐
                 ▼        ▼       ▼       ▼        ▼        ▼        ▼
               PQHD     BPC   ZEB/ZET   PQPS     PQEA   Neural    PQHR
                                                          Lock
                 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                                      │
                                      ▼
                                 PQ Gateway
                              (product layer)
```

Three specifications sit above PQSEC in the artefact-definition dependency graph: Epoch Clock (time), PQSF (encoding), and PQAI (AI evidence). Everything else depends on PQSEC for enforcement.

The ecosystem distinguishes between artefact-definition dependencies and enforcement-consumption integration. Artefact-definition dependencies form a directed acyclic graph. Enforcement-consumption integration (where a specification's artefacts are evaluated by PQSEC) does not constitute a normative dependency and therefore does not create circularity.

### Canonical Custody Flow (Bitcoin Example)

The simplest way to understand PQ is to trace a single Bitcoin signing operation:

1. **Intent** — Holder expresses intent to send Bitcoin.
2. **BPC Pre-Construction** — BPC gates construction: evidence is collected, PQSEC evaluates, produces PreConstructionOutcome. No transaction exists yet.
3. **Construction** — Only after ALLOW: PSBT is constructed from the approved intent.
4. **PQSEC Signing Evaluation** — PQSEC evaluates the full predicate set: time (Epoch Clock), consent (ConsentProof), policy (PolicyBundle), runtime (PQAI drift), operator state (Neural Lock if configured), quorum, ledger continuity. Produces EnforcementOutcome.
5. **Signing** — PQHD signing component verifies EnforcementOutcome bindings (session, intent hash, expiry) and produces signature. Key possession alone is insufficient.
6. **Execution** — ZEB manages broadcast discipline, exposure detection, and confirmation observation. SEAL provides execution confidentiality if configured.

At every stage, failure results in refusal. There is no fallback, no degraded mode, no "try anyway."

---

## Fail-Closed Property

PQ uses a ternary predicate model: TRUE / FALSE / UNAVAILABLE.

The critical design choice: **UNAVAILABLE maps to DENY for Authoritative operations.** This means "no evidence" is treated the same as "evidence says no" for any operation with irreversible effects.

Every failure condition across all 13 core specifications has been mapped to its enforcement outcome in the Fail-Closed Matrix (companion document). The matrix confirms: no silent degrade path exists anywhere in the stack.

---

## Scope Beyond Bitcoin

While Bitcoin is the reference deployment, the following specifications are application-agnostic:

| Specification | Applicability |
|---------------|---------------|
| PQSEC | Any system requiring deterministic enforcement |
| PQAI | Any system governing AI behaviour |
| PQPS | Any system managing human-AI relational state |
| PQEA | Any system governing embodied agents or robotics |
| Neural Lock | Any system requiring operator state evidence |
| Epoch Clock | Any system requiring verifiable time |
| PQSF | Any system requiring canonical encoding |
| BPC | Any system requiring authorization-before-construction |
| PQHR | Any system requiring human-readable policy rendering |
| PQ Gateway | Any deployment requiring governed AI model interaction with sovereign policy |

ZEB (Bitcoin execution profile), PQHD (Bitcoin custody), and SEAL (Bitcoin execution confidentiality) are Bitcoin-specific in their current profiles but architecturally rail-agnostic. ZET (the abstract execution boundary) is explicitly rail-agnostic.

---

## Current State and Maturity

**Specifications:** 13 CORE + 3 STANDALONE, totalling approximately 1.5MB of specification text. All are at Implementation Ready status.

**Pseudocode:** Implementation-ready pseudocode is included in PQSF, PQSEC, PQHD, PQAI, BPC, ZEB, PQPS, PQEA, and Epoch Clock. A capable developer can build from these.

**Reference Implementation:** Not yet built. This is the primary gap. A minimal reference implementation (Epoch Clock consumer + PQSF encoding library + PQSEC evaluator skeleton) is the next milestone.

**Review Posture:** The specifications have undergone systematic cross-reference verification, adversarial review, and fail-closed validation. The Fail-Closed Matrix documents every failure condition. The Hash Discipline registry (PQSEC Annex AT.8) documents every execution-binding hash across specifications.

**Review Posture:** The specifications have undergone systematic cross-reference verification, adversarial review, and fail-closed validation. The Fail-Closed Matrix documents every failure condition. The Hash Discipline registry (PQSEC Annex AT.8) documents every execution-binding hash across specifications.

---

## Reading Order for Reviewers

| Priority | Document | Time | What You Learn |
|----------|----------|------|----------------|
| 1 | This document | 15 min | Architecture, relationships, flow |
| 2 | PQ (ecosystem hub) | 30 min | Full component descriptions, conformance, security model |
| 3 | Fail-Closed Matrix | 20 min | Every failure → enforcement outcome across all specs |
| 4 | PQSEC §1–§8A | 45 min | Enforcement model, ternary predicates, authority boundaries |
| 5 | Domain spec of interest | Variable | PQHD for custody, PQAI for AI, PQEA for embodied, PQ Gateway for AI governance product |

---

*For normative definitions, see PQSEC. For the complete specification list with versions, see PQ §7.1.*
