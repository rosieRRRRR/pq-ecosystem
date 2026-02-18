# Authority Separation as a Security Primitive: The PQ Enforcement Architecture

**White Paper — PQ Ecosystem**
*Author: rosiea — PQRosie@proton.me*
*Date: 2026*

---

## Abstract

Modern security systems fail because authority is distributed, implicit, and conflated with capability. Key possession implies signing authority. Clock readings imply temporal validity. Model outputs imply behavioural trust. Each conflation creates a bypass vector that adversaries exploit routinely.

This paper presents authority separation as a security primitive: a structural guarantee that no component in a composed security system is both evidence producer and authority source. We describe the PQ enforcement architecture, in which a single deterministic engine (PQSEC) evaluates evidence produced by independent components and produces the sole authoritative output. We demonstrate that this architecture eliminates entire classes of attacks—replay, time forgery, consent reuse, execution-gap exploitation, silent runtime compromise—through structural guarantees rather than probabilistic mitigations.

We present the fail-closed property formally: every failure condition across 13 interconnected specifications maps to an explicit refusal outcome, with no silent degrade path. We discuss the ternary predicate model (TRUE / FALSE / UNAVAILABLE) and its critical design choice that absence of evidence is treated identically to negative evidence for irreversible operations.

---

## 1. Introduction

Security systems are traditionally built on trust assumptions: clocks are honest, runtimes are stable, models behave consistently, signatures imply authority. These assumptions are routinely false, and their failure is the primary mechanism through which real-world attacks succeed.

The PQ ecosystem replaces trust assumptions with structural guarantees. Rather than assuming components behave correctly, PQ requires every component to produce cryptographically verifiable evidence of its state, and delegates all authority decisions to a single enforcement engine that evaluates this evidence deterministically.

This paper describes the architectural principles underlying this approach, with emphasis on the authority separation primitive and the fail-closed enforcement model.

### 1.1 Contributions

This paper makes three contributions. First, we identify authority separation—the structural guarantee that no component is both evidence producer and authority source—as a security primitive with formal properties. Second, we describe a concrete architecture (the PQ ecosystem) implementing this primitive across custody, AI governance, embodied systems, persistent state, and product-layer deployment. Third, we present a complete fail-closed analysis demonstrating that no silent degrade path exists across the composed system.

### 1.2 Scope

This paper describes architecture. Implementation details, cryptographic constructions, and protocol-level specifications are defined in the component specifications referenced throughout. Bitcoin is the reference deployment for custody and execution components; the architecture is application-agnostic.

---

## 2. The Problem: Authority Conflation

### 2.1 Key Possession as Authority

In conventional custody systems, possession of a private key is sufficient for signing. This creates a single point of failure: an adversary who obtains key material obtains full authority. Multi-signature schemes distribute this risk but do not eliminate the conflation—each signer's key still implies that signer's authority.

### 2.2 Clock Trust as Temporal Authority

Systems that rely on system clocks for expiry, freshness, and ordering are vulnerable to time manipulation. NTP attacks, clock skew, and time-of-check-to-time-of-use gaps enable replay, premature expiry circumvention, and ordering attacks.

### 2.3 Runtime Self-Attestation

AI systems that self-report their safety state, behavioural alignment, or action classification create circular trust dependencies. A compromised model can report itself as uncompromised. Self-referential safety is not safety.

### 2.4 Platform Self-Attestation

Hardware security modules, secure enclaves, and trusted platform modules produce integrity evidence in platform-native formats. Without governed translation, this evidence either never reaches the enforcement layer (invisible to policy) or reaches it through ungoverned application-specific shims that bypass structured evaluation. The evidence exists; the integration path does not.

### 2.5 Distributed Enforcement

When enforcement logic is distributed across multiple components, each component becomes a potential bypass vector. An adversary who compromises any enforcement point can authorise operations that the composed system should refuse.

---

## 3. Authority Separation

### 3.1 Definition

Authority separation is the structural property that no component in a composed security system simultaneously produces evidence and makes enforcement decisions based on that evidence. Formally:

For a system with components C₁, C₂, ..., Cₙ and enforcement engine E:

- Each Cᵢ produces evidence eᵢ.
- E evaluates {e₁, e₂, ..., eₙ} and produces an enforcement outcome.
- No Cᵢ produces enforcement outcomes.
- E does not produce evidence.

### 3.2 Security Property

Authority separation guarantees that compromising any single component Cᵢ cannot gain authority, because:

- Cᵢ can produce false evidence eᵢ, but cannot produce an enforcement outcome.
- E evaluates eᵢ alongside evidence from other components. Unless all required evidence sources are compromised, the composed evaluation detects or compensates for the false evidence.
- E's enforcement logic is deterministic and auditable, making policy bypass detectable.

### 3.3 Comparison to Existing Models

**Multi-factor authentication** requires multiple credentials from the same principal. Authority separation requires evidence from categorically different sources evaluated by an independent authority.

**Zero-trust architecture** assumes no implicit trust but does not mandate a single enforcement authority. Authority separation is a stronger constraint: not only is trust absent, but enforcement is structurally consolidated.

**Capability-based security** grants authority through unforgeable tokens. Authority separation decouples capability (possession) from authority (enforcement outcome). In the PQ custody model, key possession is a capability; it is necessary but never sufficient for authority.

---

## 4. The PQ Enforcement Architecture

### 4.1 Component Roles

The PQ ecosystem implements authority separation through strict role assignment across 13 core specifications, 3 standalone tools, and 1 product layer. Each specification includes an explicit Authority Boundary section stating: this specification grants no authority. PQSEC—and PQSEC alone—evaluates predicate evidence and produces enforcement outcomes.

**Foundation layer.** Epoch Clock produces verifiable time anchored to Bitcoin's proof-of-work chain. PQSF defines canonical encoding, cryptographic suite indirection, the Sovereign Transport Protocol (STP), and credential lifecycle. PQSEC evaluates all predicates and produces the sole enforcement outcome.

**Domain specifications.** PQHD defines custody policy and hierarchical key management. BPC gates pre-construction (no executable artefact before authorisation). ZEB and ZET manage execution boundaries with burn semantics. SEAL provides sealed execution with end-to-end confidentiality. PQAI produces AI behavioural evidence—model identity, drift detection, tool governance, supervision lattice. PQPS governs bilateral persistent state with holder sovereignty. Neural Lock produces operator physiological state attestations. PQEA governs embodied operations with execution leases and perception sufficiency. PQHR defines deterministic human-readable rendering with anti-manipulation guarantees—ensuring that what the holder sees accurately reflects what the system decided.

**Standalone tools.** PQPR provides proof-of-reference verification—structured, deterministic verification of AI output against source material. PQAA translates platform-native integrity signals (TPM quotes, Secure Enclave attestations, Android Keystore attestations) into canonical `platform_bridged` evidence consumable by PQSEC. The Fail-Closed Matrix maps every failure condition across all specifications to its enforcement outcome.

**Product layer.** PQ Gateway composes the core specifications into a deployable governance surface for AI model interaction. It provides governed inference routing, policy authoring, provider management, billing, and enrollment. PQ Gateway introduces no new enforcement primitives—all enforcement remains exclusively within PQSEC. It defines product-layer refusal codes that are additive only: billing may refuse what PQSEC has allowed, but can never permit what PQSEC has denied.

### 4.2 Ternary Predicate Model

PQSEC evaluates predicates using a ternary model: TRUE (evidence satisfies the predicate), FALSE (evidence contradicts the predicate), or UNAVAILABLE (evidence is absent or unverifiable).

The critical design choice: UNAVAILABLE maps to DENY for Authoritative operations (those with irreversible effects). This eliminates the common failure mode where absence of evidence is treated as absence of risk.

### 4.3 Enforcement Outcome

PQSEC produces exactly one of three outcomes per operation: ALLOW (all required predicates satisfied), DENY (one or more predicates unsatisfied), or FAIL_CLOSED_LOCKED (system enters lockout state). No other outcome is possible. No component may produce, cache, reinterpret, or override an enforcement outcome.

### 4.4 Fail-Closed Property

The fail-closed property states: every failure condition across all specifications results in explicit refusal or lockout. No failure condition results in continued operation.

This property has been verified empirically across the full specification corpus. The Fail-Closed Matrix documents every failure condition, refusal code, and enforcement outcome across all 13 core specifications, 3 standalone tools, and the PQ Gateway product layer.

### 4.5 Rendering and Transparency

Authority separation requires visibility. PQHR enforces a deterministic rendering contract: policy decisions, enforcement outcomes, and receipts are rendered for the holder with completeness guarantees (omission is misrepresentation), no selective disclosure between viewers, and no selective emphasis that alters perception. Without PQHR, authority separation is structurally sound but operationally opaque—the holder cannot verify that the system is behaving as governed.

---

## 5. Capability–Authority Decoupling

The PQ custody model (PQHD) exemplifies authority separation applied to Bitcoin. Signing requires both cryptographic capability (key possession) and externalised authority (a valid EnforcementOutcome from PQSEC). The EnforcementOutcome is not a credential; it is a control-plane artefact representing the result of independent policy adjudication.

This architecture is more accurately described as capability–authority decoupling than multi-factor authentication. MFA combines multiple credentials belonging to the same principal. PQHD separates categorically different requirements: what you possess (key) versus what the system has independently determined (authority).

---

## 6. Composed Evidence and Cross-Domain Governance

Authority separation scales across domains. The same architectural pattern governs custody (PQHD + BPC), AI operations (PQAI + PQPS), embodied systems (PQEA), human state (Neural Lock), and governed AI model interaction (PQ Gateway). Each domain produces domain-specific evidence. PQSEC evaluates all evidence uniformly through its predicate model.

Cross-domain composition is natural: a custody operation can require AI drift evidence (PQAI), operator state (Neural Lock), time validity (Epoch Clock), custody policy satisfaction (PQHD), and platform integrity evidence (PQAA) simultaneously. PQSEC evaluates all predicates in a single pass. No domain component needs to be aware of requirements from other domains.

### 6.1 The Platform Evidence Gap

A practical challenge in composed evidence systems is that platform-native integrity signals (hardware attestation, secure boot measurement, enclave state) speak platform-native protocols that the enforcement layer cannot consume directly. PQAA addresses this by providing a governed translation layer: platform attestations are translated into canonical `platform_bridged` evidence artefacts with deterministic classification, manifest-bound adapter governance, and hash-only evidence channels. PQAA does not validate the truthfulness of platform attestations—it classifies and governs the translation path so that PQSEC can evaluate the evidence under policy. This reduces the gap from "no platform visibility" to "governed, classified, policy-gated visibility."

---

## 7. Limitations and Residual Risks

Authority separation does not protect against total compromise of the enforcement engine itself. If PQSEC is compromised, all authority decisions are compromised. This is an inherent property of consolidated enforcement and is mitigated by PQSEC's determinism (identical inputs produce identical outputs, enabling independent verification).

Authority separation does not protect against compromise of all evidence sources simultaneously. If every component produces false evidence, PQSEC will produce a false ALLOW. This is mitigated by the independence requirement: evidence sources are structurally independent, making simultaneous compromise increasingly difficult.

The OS-level enforcement boundary remains the most critical unsolved layer. If the operating system, hypervisor, or enforcement core runtime is compromised, governance collapses. PQAA provides a governed migration path for this gap by bridging platform-native integrity signals into the enforcement model. While PQAA cannot independently verify the correctness of platform attestations (policy must treat bridged evidence as contingent on host integrity), it replaces the alternative—no platform evidence at all—with structured, governed visibility.

The Epoch Clock's single-issuer bootstrap creates a hierarchical trust anchor. This is an inherent property of hierarchical PKI, mitigated by Bitcoin inscription immutability and v3 multi-signature tick issuance.

---

## 8. Conclusion

Authority separation is a security primitive that eliminates the conflation of capability with authority, evidence production with enforcement, and component trust with system trust. The PQ ecosystem demonstrates that this primitive can be implemented across custody, AI governance, embodied systems, persistent state, platform attestation, and product-layer deployment through a composed architecture with a single deterministic enforcement core.

The architecture comprises 13 core specifications, 3 standalone tools, and 1 product layer, with every failure condition mapped to an explicit enforcement outcome. Bitcoin is the reference deployment; the architecture is application-agnostic.

---

## References

- PQ Ecosystem Overview
- PQSEC Enforcement Core v2.0.3
- PQSF Security Framework v2.0.3
- Epoch Clock v2.1.0
- PQHD Custody Policy v1.2.0
- PQAI AI Evidence v1.2.0
- BPC Pre-Construction Gating v1.1.0
- ZEB Execution Boundary v1.3.0
- SEAL Sealed Execution v2.0.0
- PQPS Persistent State Governance v1.0.0
- Neural Lock Operator State Evidence v1.1.0
- PQEA Embodied Agent Governance v1.0.0
- PQHR Human-Readable Rendering v1.0.0
- PQAA PQ Attestation Adapter v1.0.0
- PQPR Proof-of-Reference v1.0.0
- PQ Gateway v1.0.0
- Fail-Closed Matrix v1.0.0

*All specifications available at: [repository URL]*
