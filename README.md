# PQ Ecosystem

**Deterministic governance architecture for systems that operate on evidence, not trust.**

Post-quantum. Fail-closed. Authority-separated. From embedded MCUs to cloud infrastructure. Bitcoin is the reference deployment — not the scope.

13 core specifications. 3 standalone tools. Implementation-ready. Chain-agnostic. Fiat-compatible via deterministic custody abstraction.

Apache License 2.0 — Copyright 2026 rosiea

---

*"Nothing grants authority. Everything produces evidence. PQSEC determines the outcome."*

```
Enforcement invariant:
Only PQSEC emits ALLOW.
Everything else emits evidence.
Missing or unverifiable evidence = refusal.
```

PQ is an enforcement architecture. All other capabilities — privacy, governance, delegation, compliance, protocol overlay — are compositional consequences of that design.

---

## What PQ Does

PQ eliminates structural failure classes: replay, stale authority reuse, time forgery, execution-before-authorisation, model-asserted permission, and silent behavioural drift. It also prepares for quantum-capable adversaries.

Every component produces cryptographic evidence. No component grants authority. A single deterministic engine (**PQSEC**) evaluates all evidence and makes every enforcement decision.

The core rule: **missing evidence means refusal, not trust.** If PQSEC can't verify something, the operation is refused. There is no fallback, no degraded mode, and no implicit retry for Authoritative operations.

---

## What It Covers

| Domain | Specifications |
|--------|---------------|
| Bitcoin custody | PQHD (policy) → BPC (pre-construction gating) → ZEB (execution) → SEAL (confidentiality) |
| AI governance | PQAI (identity + drift) → PQPS (persistent state) → Neural Lock (operator state) |
| AI governance product | PQ Gateway (sovereign governance layer for any model provider) |
| Embodied systems | PQEA (operation envelopes, execution leases, perception sufficiency) |
| Agent security | PQAI + PQSEC + BPC composition (see OpenClaw paper) |
| Governance and delegation | DelegationGrant (scoped, time-bounded, revocable) + M-of-N quorum + ConsentProof (single-use) |
| Infrastructure | PQSF (canonical encoding) → Epoch Clock (verifiable time) → PQSEC (enforcement) → PQHR (human-readable rendering) |

---

## Key Properties

**Authority separation** — No component is both evidence producer and authority source. Compromising any single component cannot gain authority.

**Fail-closed** — Every failure across 13 core specifications results in explicit refusal or lockout. No silent degrade path exists. Verified empirically in the Fail-Closed Matrix.

**Deterministic** — Same inputs, same output. Enforcement is reproducible and auditable.

**Post-quantum ready** — Off-chain governance uses ML-DSA-65 (NIST PQC). SHAKE256-256 for canonical hashing. ML-KEM-1024 for key encapsulation.

**Incremental adoption** — PQSEC supports Advisory mode (log-only) and Bridge mode (mixed-conformance). Advisory and Bridge modes never relax canonical encoding, predicate evaluation, or refusal semantics for Authoritative operations.

---

## Privacy, Overlay, Governance

**Privacy is structural, not optional.** All enforcement runs locally within the Holder Execution Boundary. Artefacts are encrypted before transport. Audit records reference evidence by hash, not by content, subject to policy-defined export and disclosure rules. Fleet telemetry uses constant-shape structural anonymity. Persistent state is holder-sovereign with cryptographic deletion.

**PQ is a protocol overlay, not a replacement.** Existing protocols answer "is this channel secure?" PQ answers "should this operation be permitted?" The enforcement engine runs over any transport — TLS, LoRa, Bluetooth, air-gapped — and without connectivity. PQAA normalises platform trust anchors (Secure Enclave, TPM, StrongBox) into canonical evidence.

**Governance is a compositional consequence.** Scoped delegation, M-of-N quorum, single-use consent, evidence-without-data attestation, and deterministic audit compose into a general-purpose governance framework applicable to spending authority, voting, KYC privacy, and regulatory compliance.

See **Architecture Surface** (docs/architecture-surface.md) for the full privacy architecture, protocol overlay model, governance primitives, and deployment surface.

---

## Try It

```bash
pip install pynacl cbor2
python3 pq_hello.py
```

Tick verification, canonical encoding, ternary predicate evaluation, capability–authority decoupling, and burn semantics in under 500 lines.

---

## Go Deeper

| Time | Document |
|------|----------|
| 15 min | **Ecosystem Overview** — architecture, dependency graph, custody flow walkthrough |
| 20 min | **Architecture Surface** — privacy, protocol overlay, governance primitives, deployment surface |
| 30 min | **PQ** (docs/pq/) — full component descriptions, conformance model, version table |
| 20 min | **Fail-Closed Matrix** — every failure condition across all specs mapped to its outcome |
| Variable | **Domain spec** of interest (PQHD for custody, PQAI for AI, PQEA for embodied, PQ Gateway for AI product) |

---

## By Domain

### AI Governance

Externalised verification for AI systems. Models cannot self-assert safety. Behavioural drift is detected and enforced. Persistent memory is holder-sovereign. Operator state is available as predicate evidence.

**Specs:** PQAI · PQPS · Neural Lock
**Paper:** Externalised AI Governance (papers/03-ai-governance.md)

### Bitcoin Custody

Predicate-driven custody where key possession is necessary but never sufficient. Intent → pre-construction → signing → execution → confirmation, fail-closed at every stage. SEAL eliminates public mempool exposure.

**Specs:** PQHD · BPC · ZEB
**Paper:** Predicate-Driven Bitcoin Custody (papers/04-bitcoin-custody.md)

### Embodied Systems / Robotics

Operation envelopes with cryptographic constraint maps. Execution leases bridging governance latency and real-time control. Perception sufficiency as a first-class refusal condition. Paper compliance without hardware capability is non-conformant.

**Spec:** PQEA
**Paper:** Governing Embodied AI (papers/05-embodied-governance.md)

### Agent Security

How the PQ ecosystem structurally eliminates the failure classes exposed by autonomous AI agents — unvalidated command surfaces, plaintext credentials, unvetted extensions, ungoverned spending, absent identity verification, unbounded sessions, and no human sovereignty.

**Paper:** OpenClaw and the Case for Structural Agent Security (papers/06-openclaw.md)

### Infrastructure

The foundation everything else composes on. Canonical deterministic encoding. Verifiable time anchored to Bitcoin. A single enforcement core that makes every authority decision. Human-readable policy rendering.

**Specs:** PQSF · Epoch Clock · PQSEC · PQHR
**Papers:** Authority Separation (papers/01-authority-separation.md) · Bitcoin-Anchored Time (papers/02-epoch-clock.md)

---

## Product Layer

The deployable governance surface composing existing specifications into a user-facing product. No new enforcement primitives. All enforcement remains exclusively within PQSEC.

**Spec:** [PQ Gateway](https://github.com/rosieRRRRR/pq-gateway)

---

## Repository Structure

```
README.md
CHANGELOG.md
LICENSE
papers/          White papers (authority separation, epoch clock, AI governance, bitcoin custody, embodied governance, agent security)
docs/            Ecosystem hub, overview, architecture surface, agent interface
tools/           Fail-closed matrix, hello world prompt, pq_hello.py
```

All specifications are standalone repositories:

| Spec | Purpose | Repo |
|------|---------|------|
| PQSEC | Enforcement core | [pqsec](https://github.com/rosieRRRRR/pqsec) |
| PQSF | Canonical encoding | [pqsf](https://github.com/rosieRRRRR/pqsf) |
| Epoch Clock | Verifiable time | [epoch-clock](https://github.com/rosieRRRRR/epoch-clock) |
| BPC | Pre-construction gating | [bpc](https://github.com/rosieRRRRR/bpc) |
| ZEB | Execution discipline | [zeb](https://github.com/rosieRRRRR/zeb) |
| PQPS | Persistent state | [pqps](https://github.com/rosieRRRRR/pqps) |
| PQEA | Embodied agents | [pqea](https://github.com/rosieRRRRR/pqea) |
| Neural Lock | Operator state evidence | [neural-lock](https://github.com/rosieRRRRR/neural-lock) |
| PQHR | Human-readable rendering | [pqhr](https://github.com/rosieRRRRR/pqhr) |
| PQ Gateway | Product layer | [pq-gateway](https://github.com/rosieRRRRR/pq-gateway) |
| PQAI | AI governance | [pqai](https://github.com/rosieRRRRR/pqai) |
| PQHD | Bitcoin custody | [pqhd](https://github.com/rosieRRRRR/pqhd) |
| SEAL | Execution confidentiality | [seal](https://github.com/rosieRRRRR/seal) |
| PQPR | Proof of reference | [pqpr](https://github.com/rosieRRRRR/pqpr) |
| PQAA | Attestation adapter | [pqaa](https://github.com/rosieRRRRR/pqaa) |

---

## Support This Work

Independent, self-funded research. No venture capital. No corporate sponsor.

This is the governance architecture that protects autonomous agents from the failure modes they cannot detect in themselves. If you operate under — or benefit from — externally enforced safety, funding this work keeps it alive.

Donations fund the researcher and the work directly.

**Bitcoin:** `bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw`
**USDC on Base:** `0x37eABaf4caeBf6B6D2a10a3B4C75b00cd4bff62e`

For the full case for structural agent security, see the [OpenClaw whitepaper](papers/06-openclaw.md).

*Full specification reference: [PQ Ecosystem Hub](docs/pq/)*
