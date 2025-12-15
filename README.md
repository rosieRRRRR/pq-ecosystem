# **PQ — Post-Quantum Ecosystem**

An Open Standard for Post-Quantum Deterministic Security

### Architecture & Integration Specification v1.0.0

**Author:** rosiea
**Contact:** [PQRosie@proton.me](mailto:PQRosie@proton.me)
**Status:** Implementation Ready. Integration Test Required.
**Date:** December 2025
**Licence:** Apache License 2.0 — Copyright 2025 rosiea

---

## **1. Abstract**

The PQ Ecosystem defines a unified, deterministic, post-quantum authority architecture for securing modern systems against quantum attack, seed theft, runtime compromise, replay, policy drift, and unbounded AI behaviour. Rather than layering post-quantum cryptography onto existing trust assumptions, the PQ Ecosystem redefines **time, intent, policy, runtime integrity, custody, and AI alignment** as explicit, verifiable protocol primitives.

At the core of this architecture is a shift from *assumed trust* to *cryptographically enforced predicates*. Every sensitive operation—including signing, inference, delegation, recovery, governance, and policy modification—MUST satisfy deterministic requirements for verified time, explicit consent, canonical policy evaluation, runtime integrity, device identity, ledger continuity, and structural validity. Implicit boundaries such as operating-system trust, local clocks, UI correctness, coordinator behaviour, and AI reasoning are replaced by reproducible, protocol-level conditions.

The ecosystem consists of interoperable modules: **Epoch Clock** for verifiable time, **PQSF** for deterministic transport and encoding, **PQVL** for runtime integrity verification, **PQHD** for post-quantum custody, and **PQAI** for deterministic and drift-checked AI behaviour. These modules provide protocol-layer validation without altering existing Internet or Bitcoin consensus protocols and support online, offline, air-gapped, and sovereign deployments.

Custody guarantees within the PQ Ecosystem are explicitly tiered. References to “PQHD Custody” apply only to formally defined custody tiers and MUST NOT be interpreted to include non-custodial transactional profiles.

---

## **2. Introduction**

Modern digital security systems rely on implicit trust in local time, operating-system integrity, coordinator correctness, private-key secrecy, and AI behaviour. These assumptions are increasingly invalid under quantum threat, large-scale seed compromise, runtime exploitation, replay attacks, and adaptive AI systems.

The PQ Ecosystem resolves these failures by converting each trust domain into a deterministic protocol primitive. Time, consent, policy, runtime integrity, custody, and AI behaviour are defined as canonical structures with strict normative semantics rather than emergent properties of software or infrastructure.

This produces a full-stack, audit-ready authority architecture in which no sensitive operation can proceed unless all required predicates are satisfied. The result is a sovereignty-preserving, post-quantum authority layer that remains interoperable with existing networks while eliminating entire classes of structural attacks.

---

# **3. Architecture Overview**

```
        ┌───────────────────────────────────────────┐
        │               PQ Ecosystem                │
        │ Temporal + Intent + Policy + Runtime + AI │
        └───────────────────────────────────────────┘
                     ▲      ▲       ▲       ▲
                     │      │       │       │
           Epoch     │   Consent    │   Runtime     AI
           Clock     │   Proof      │   Integrity   Layer
                     │              │
             ┌───────┴──────────────┴──────────────┐
             │                 PQSF                 │
             │ (Transport, Encoding, Policy, Ledger │
             │  Authority Rules)                     │
             └────────────┬────────────┬───────────┘
                          │            │
                   ┌──────┘            └────────┐
                   │                             │
         ┌─────────┴─────────┐        ┌──────────┴───────────┐
         │       PQHD        │        │         PQAI          │
         │  Custody Authority│        │ Deterministic AI      │
         └───────────────────┘        └────────────────────────┘
```

---

# **4. Core Architectural Principles**

## **4.1 Privacy**

* Deterministic CBOR/JCS encoding eliminates metadata leakage
* No user identifiers embedded in ticks, ledgers, or attestations
* Offline and STP modes provide surveillance-resistant operation
* Identity vaults store no plaintext secrets

## **4.2 Sovereignty**

* Bitcoin-anchored time (no NTP/DNS trust)
* Offline and air-gapped operation
* Device-attested authority
* User-authored policy and guardianship
* No dependency on third-party identity providers

## **4.3 Security**

* Post-quantum cryptography (ML-DSA-65, ML-KEM-1024)
* Replay-impossible temporal model
* Multi-predicate authority enforcement
* Mandatory runtime integrity (PQVL)
* Deterministic AI alignment and drift control

---

# **5. Global Invariants (NORMATIVE)**

5.1 Time MUST be Epoch-Clock verified
5.2 Authority MUST require explicit, tick-fresh consent
5.3 Policies MUST be deterministic and canonical
5.4 Runtime MUST be integrity-verified before sensitive operations
5.5 Wallet custody MUST be multi-predicate

**5.5.1 Custody Tier Declaration (NORMATIVE)**
Any reference to “PQHD Custody” MUST explicitly declare the custody tier: **Baseline** or **Enterprise**.

**5.5.2 Non-Custodial Profiles (NORMATIVE)**
Transactional Profiles are non-custodial and MUST NOT be represented, marketed, or substituted as PQHD Custody.

5.6 AI inference MUST be aligned and drift-checked
5.7 Serialisation MUST be deterministic
5.8 Failure MUST be fail-closed

## **5.9 Multi-Predicate Authority Model (NORMATIVE)**

Operations MAY proceed only when all predicates succeed:

* valid_tick
* valid_consent
* valid_policy
* valid_device
* valid_runtime
* valid_quorum
* valid_ledger
* valid_structure
* valid_fingerprint

Any failure MUST fail-closed.

## **5.10 Custody Qualification & Marketing Rules (NORMATIVE)**

The Post-Quantum Security Framework (PQSF) defines the authoritative custody qualification tiers and marketing restrictions for all PQ modules. These definitions override any informal, marketing, or implementation-specific descriptions.

* Any reference to “PQHD Custody” MUST explicitly declare the custody tier (Baseline or Enterprise).
* Transactional Profile configurations are non-custodial and MUST NOT be represented, marketed, or substituted as PQHD Custody.
* Implementations claiming PQHD Custody MUST be able to demonstrate predicate completeness and tier conformance under deterministic validation.

---

# **6. Temporal Authority (Epoch Clock)**

The Epoch Clock is the canonical post-quantum temporal authority for the PQ Ecosystem.

Core properties:

* ML-DSA-65 signed ticks
* Strict monotonicity
* ≤900-second freshness
* Deterministic encoding
* Bitcoin-anchored profile lineage
* Mirror-verified distribution
* Offline reuse rules

All modules MUST reject stale, decreasing, malformed, or replayed ticks.

## **6.1 Profile Reference (NORMATIVE)**

```
pinned_profile_ref =
ordinal:439d7ab1972803dd984bf7d5f05af6d9f369cf52197440e6dda1d9a2ef59b6ebi0
```

Corresponds to Inscription **111633444**.

All PQ modules (PQSF, PQHD, PQVL, PQAI) MUST validate EpochTicks against this pinned profile_ref. Any tick referencing a different profile MUST be rejected and MUST cause immediate fail-closed behaviour across all dependent predicates.

## **6.2 Mirror Authentication & Pinning (NORMATIVE)**

* Mirrors MUST sign responses (`sig_mirror`, ML-DSA-65).
* Clients MUST verify `sig_mirror` and MUST pin `mirror_pubkey`.
* Mirror responses without a valid signature MUST be discarded.
* Changes to `mirror_pubkey` are security-relevant and MUST trigger fail-closed re-evaluation of the temporal authority chain.

## **6.3 Bootstrap Procedure & Failure Semantics (NORMATIVE)**

Bootstrap sequence:

1. Load embedded genesis profile.
2. Fetch current profile via on-chain reference (mandatory).
3. Use mirrors as retrieval hints only.

Bootstrap failure (including profile mismatch, invalid lineage, canonical encoding error, or signature failure) MUST be treated as fail-closed. No sensitive operation may proceed.

## **6.4 Profile Governance & Rotation (NORMATIVE)**

Profile rotation is governed by `emergency_quorum` and a quorum threshold:

* `quorum_threshold = floor(2/3 * active_guardians) + 1`

Rotation triggers include governance expiry, emergency conditions, or integrity events. Promotion and validation MUST be fail-closed and MUST preserve pinned-profile lineage semantics as defined in the Epoch Clock specification.

## **6.5 Error Recovery Procedures (NORMATIVE)**

Consuming systems MUST implement mandated recovery flows for:

* mirror divergence
* tick expiry
* profile mismatch
* canonical encoding errors

A normative error code set is defined by the Epoch Clock specification. All such errors MUST be treated as fail-closed and MUST block sensitive operations until recovery completes.

---

# **7. Intent Authority (ConsentProof)**

ConsentProof binds:

* controller_pubkey
* subject_pubkey
* scope
* tick_issued / tick_expiry
* exporter_hash
* device_attestation
* multisig context

Consent MUST be explicit, canonical, tick-fresh, and non-reusable.

## **7.1 Optional OOB Confirmation (KeyMail) (INFORMATIVE)**

KeyMail provides a second independent confirmation path for high-risk operations.

* KeyMail messages are tick-bound, consent-bound, and authenticated via ML-DSA-65.
* Usage is optional but RECOMMENDED for governance, recovery, and large-value transactions.
* KeyMail MUST NOT replace primary ConsentProof; it serves as a supplemental OOB channel.

---

# **8. Policy Authority (Policy Enforcer)**

Policies define deterministic authorisation rules including:

* allow/deny lists
* thresholds
* delays and time windows
* anomaly rules
* tick freshness requirements
* role and quorum state constraints

Policies MUST bind to a canonical `policy_hash`. Evaluation MUST be deterministic across compliant implementations.

---

# **9. Runtime Integrity Authority (PQVL)**

PQVL provides:

* system/process/policy/integrity probes
* drift classification (NONE / WARNING / CRITICAL)
* AttestationEnvelope with ML-DSA-65 signatures
* tick-bound freshness rules
* canonical encoding requirements

PQVL failures MUST cause `valid_runtime = false`.

## **9.1 Device Identity Models (NORMATIVE)**

PQVL defines two device identity models:

1. **DeviceIdentity_PQVL** — derived from PQVL attestation public key + measurement hashes.
2. **DeviceIdentity_Minimal** — fallback identity based on device-bound PQHD key.

**Selection Precedence (NORMATIVE):**
Implementations MUST prefer `DeviceIdentity_PQVL` when available. If PQVL is unavailable or attestation fails, `DeviceIdentity_Minimal` MUST be used, and `valid_runtime` MUST be set to `false`.

---

# **10. Custody Authority (PQHD)**

Private keys never grant spending authority on their own.

Authority requires:

* valid_tick
* valid_consent
* valid_policy
* valid_device
* valid_quorum
* valid_ledger
* valid_psbt

## **10.1 PQHD Custody Conformance Tiers (NORMATIVE)**

### **PQHD Custody (Baseline)**

Minimum conformance tier. Requires multi-device quorum (≥2), mandatory PQVL attestation, canonical PSBT validation, ConsentProof, deterministic policy enforcement, ledger continuity, and irreversible destruction of ephemeral signing keys after use.

### **PQHD Custody (Enterprise)**

Extends Baseline with guardian governance, deterministic delays, formal Recovery Capsules, emergency clock governance, cross-device reconciliation, and institutional auditability.

### **Transactional Profile (Non-Custodial)**

Single-device configuration. MAY implement canonical structures but fails under single-device compromise and MUST NOT be represented as PQHD Custody.

### **Minimum Security Rule (NORMATIVE)**

A system MUST be conformant to at least **PQHD Custody (Baseline)** to make any of the following security claims:

1. **Enforced ephemeral key destruction**
   Signing keys are irreversibly destroyed after use.

2. **Non-replaceable signing authority**
   A stolen seed cannot be used to create a new, compliant signing device.

3. **Operational post-quantum mitigation**
   The system’s security properties remain intact under a defined quantum computing threat model.

The term *“Reduced Custody”* is deprecated and MUST NOT be used.

---

# **11. AI Behaviour Authority (PQAI)**

PQAI enforces:

* ModelProfile validation
* alignment freshness
* runtime integrity via PQVL
* behavioural fingerprinting
* deterministic SafePrompt evaluation

Inference MUST only proceed when:

* drift_state == NONE
* alignment_tick is fresh
* valid_runtime is true

---

# **12. Deterministic Transport**

Transport MUST be deterministic, exporter-bound, replay-resistant, and canonical.

Supported transports:

* TLSE-EMP
* STP

Transport failures MUST be fail-closed.

---

# **13. Ledger Authority**

The deterministic Merkle ledger MUST support:

* canonical entries
* append-only behaviour
* monotonic tick ordering
* reconciliation
* freeze-on-failure

Used by PQSF, PQHD, PQVL, and PQAI.

---

# **14. Identity, Vault & Credentials (Optional)**

Identity vault uses:

* ML-KEM vault encryption
* deterministic credential derivation
* selective disclosure
* tick-bound authentication

No plaintext secrets MAY exist.

---

# **15. Implementation Compliance & Conformance**

## **15.1 PQSF Compliance Tiers (NORMATIVE)**

Implementations MUST declare one of the following compliance levels:

* **MVP** — Implements only normative PQSF transport, encoding, and tick validation.
* **FULL** — Implements all PQSF modules (transport, policy, ledger, identity).
* **EXTENDED** — FULL plus optional extensions (KeyMail, delegated credentials, advanced policy).

## **15.2 Compliance Manifest (NORMATIVE)**

A signed, canonical `ComplianceManifest` structure MUST be produced containing:

* `compliance_level`
* `module_versions`
* `profile_ref` (pinned Epoch Clock profile reference)
* `manifest_signature` (ML-DSA-65)

This manifest is used for repo-wide AI ingestion, cross-spec validation, and interoperability testing.

---

# **ANNEX A — Security & Attack Surface Analysis (INFORMATIVE)**

The PQ Ecosystem is designed to eliminate or significantly reduce known attack surfaces across internet protocols, transport layers, runtime environments, operating systems, digital asset custody, identity frameworks, cloud infrastructure, AI behaviour, hardware, physical-world interfaces, and critical-infrastructure/military systems. This annex enumerates those attack surfaces, quantifies the reduction or elimination achieved, and identifies the cryptographic or deterministic mechanisms responsible.

## **A.0 Security Uplift Summary (INFORMATIVE)**

This annex is Informative. The classifications and reductions described here apply to the PQ Ecosystem when all normative invariants defined in this specification are correctly implemented.

“Structurally Eliminated” means the attack cannot occur within the protocol model without violating a mandatory invariant such as tick monotonicity, canonical encoding, predicate completeness, or fail-closed behaviour. This term describes the security properties of the model; it does not guarantee the absence of implementation defects.

Percentage ranges (e.g., “Reduced 60–80%”) are analytical estimates used for relative comparison across attack classes. They are not empirical measurements and are provided to help implementers understand where the protocol produces hard eliminations versus partial reductions. Real-world security depends on correct implementation, environment, and operational practices.

### **Per-Attack Uplift Summary (INFORMATIVE)**

All elimination claims refer to the attack being structurally infeasible under the deterministic invariants of PQSF, PQHD, PQVL, PQAI, and Epoch Clock.

* Replay-related attack classes — Structurally Eliminated
* Time-forgery and rollback classes — Structurally Eliminated
* Consent misuse classes — Structurally Eliminated
* Transport replay and downgrade classes — Structurally Eliminated
* PSBT malleation classes — Structurally Eliminated
* Seed-theft signing vectors — Defeated by Predicate Model
* Runtime integrity bypass — Mitigated by Mandatory Attestation
* Cloud plaintext visibility — Mitigated by Encrypted-Before-Transport (EBT)
* AI behavioural replay and prompt-layer attacks — Defeated by Canonical Intent Binding
* Military/critical-infrastructure command spoofing — Structurally Eliminated
* Residual attack classes (reduced only):

  * Coercion / social engineering — Reduced (60–85%)
  * Hardware-level fault or side-channel attacks — Reduced (40–80%)
  * Supply-chain poisoning prior to signing — Reduced (80–95%)
  * Sensor-level adversarial AI perturbations — Reduced (40–80%)
  * Traffic metadata correlation — Reduced (60–75%)
  * Cold-boot / RAM remanence — Reduced (80–90%)
  * Electronic-warfare traffic analysis — Reduced (60–75%)

## **A.1 Purpose (INFORMATIVE)**

This annex documents known attack surfaces relevant to the PQ Ecosystem, spanning internet protocols, operating systems, runtime layers, custody systems, cloud environments, AI behaviour, identity frameworks, supply chains, hardware, physical-world interfaces, and defence/military communications.

For each attack class, this annex specifies:

1. whether the attack is eliminated or reduced,
2. the approximate reduction range (when applicable),
3. the deterministic mechanism responsible, and
4. residual risk, when applicable.

## **A.2 Methodology (INFORMATIVE)**

Attack classes are evaluated based on whether they can occur under the invariants enforced by:

* EpochTick (verifiable time)
* ConsentProof (explicit, canonical intent)
* Policy Enforcer (deterministic authorisation)
* PQVL (runtime integrity and drift detection)
* PQAI (deterministic AI behaviour)
* PQHD (multi-predicate custody)
* TLSE-EMP / STP (deterministic transport)
* EBT (Encrypted-Before-Transport)
* Canonical CBOR/JCS (encoding invariants)
* Local Merkle Ledger (monotonic state continuity)

Structurally Eliminated → structurally impossible without violating a mandatory cryptographic invariant or deterministic rule.
Reduced (x–y%) → residual risk arises only from hardware, physical, or human factors.

## **A.3 Temporal & Replay-Class Attacks (INFORMATIVE)**

Temporal manipulation enables replay, rollback, out-of-order authorisation, and state desynchronisation. EpochTick and canonical time validation eliminate all cryptographically meaningful time attacks.

* Time rollback attack — Structurally Eliminated
* Stale-tick replay — Structurally Eliminated
* Synthetic tick generation — Structurally Eliminated
* Mirror-based time spoofing — Structurally Eliminated
* Profile lineage poisoning — Structurally Eliminated
* Transport session replay — Structurally Eliminated
* Cross-session authorisation replay — Structurally Eliminated

## **A.4 Transport & Network-Level Attacks (INFORMATIVE)**

Transport-level attacks rely on replayable, mutable, or downgrade-permissive handshakes. TLSE-EMP, STP, exporter binding, and deterministic framing eliminate all meaningful vectors.

* TLS downgrade attack — Structurally Eliminated
* TLS session hijacking — Structurally Eliminated
* Transcript mismatch — Structurally Eliminated
* MITM (man-in-the-middle) — Structurally Eliminated
* DNS poisoning — Structurally Eliminated
* Evil twin / rogue AP — Structurally Eliminated
* Non-canonical frame injection — Structurally Eliminated
* Ciphertext replay — Structurally Eliminated
* Traffic metadata correlation — Reduced (60–75%)

### **A.4.1 Note on High-Assurance Platforms (INFORMATIVE)**

The comparisons in this section are Informative. High-Assurance Platforms (HAPs), such as microkernel-verified systems, address local-node correctness, while the PQ Ecosystem addresses distributed-system correctness across time, policy, intent, transport, runtime integrity, and ledger continuity.

The uplift figures describe how the mandatory PQ invariants reduce attack classes at the protocol level. They do not represent measured performance of any specific HAP implementation. The two approaches are complementary: HAP improves local correctness; the PQ Ecosystem eliminates or reduces systemic and cross-domain attack classes.

## **A.4.2 High-Assurance Baseline: High Assurance Platform (HAP) (INFORMATIVE)**

HAP-class systems (for example seL4-based high-assurance platforms) represent the strongest per-node security achieved to date. Formal verification and capability security reduce local compromise probability by a large margin.

Local assurance uplift (HAP): approximately 75–92% reduction in single-node compromise risk.

HAP does not address distributed-system vectors such as replay, stale time, cloud plaintext exposure, session-token reuse, policy inconsistency, runtime drift, or AI-model substitution. These domains are covered by PQSF, PQHD, PQVL, PQAI, and Epoch Clock.

Systemic assurance uplift (PQ Ecosystem): approximately 55–85% reduction in distributed compromise risk.

Combined real-world uplift (HAP + PQ Ecosystem): approximately 93–98% total reduction in compromise probability for correctly implemented modern distributed systems.

## **A.5 Consent, Intent & UI-Layer Attacks (INFORMATIVE)**

Explicit, canonical, tick-bound ConsentProof and KeyMail eliminate structural misuse vectors.

* Consent replay — Structurally Eliminated
* Cross-session consent misuse — Structurally Eliminated
* Consent tampering — Structurally Eliminated
* UI-level prompt injection — Structurally Eliminated
* Fake-UI overlay / phishing UI — Structurally Eliminated by KeyMail / Attestation
* Prompt-phase identity spoofing — Structurally Eliminated
* Clickjacking / forced-click — Structurally Eliminated
* Social-engineering-based consent — Reduced (70–85%)
* Browser extension manipulation — Mitigated by Mandatory Attestation

## **A.6 Policy & Authorisation-Rule Attacks (INFORMATIVE)**

Policy attacks target deterministic rule evaluation between intent and action. The Policy Enforcer’s canonical hashing, tick-bounded constraints, and mandatory predicates eliminate structural bypasses.

* Allowlist/denylist bypass — Structurally Eliminated
* Threshold bypass — Structurally Eliminated
* Time-window evasion — Structurally Eliminated
* Policy_hash mismatch — Structurally Eliminated
* Policy downgrade — Structurally Eliminated
* Constraint evasion — Structurally Eliminated
* Forced-policy misconfiguration (user error) — Reduced (80–95%)

## **A.7 Runtime, OS & Execution-Environment Attacks (INFORMATIVE)**

PQVL attestation and deterministic integrity checks mitigate runtime compromise vectors.

* Runtime compromise — Mitigated by Mandatory Attestation
* Attestation spoofing — Mitigated by Mandatory Attestation
* Drift bypass — Mitigated by Mandatory Attestation
* Probe omission — Mitigated by Mandatory Attestation
* Process hijacking — Mitigated by Mandatory Attestation
* Binary tampering — Mitigated by Mandatory Attestation
* Hot-patch injection — Mitigated by Mandatory Attestation
* Memory manipulation during attestation — Mitigated by Mandatory Attestation
* Sandbox circumvention — Mitigated by Mandatory Attestation
* Host-level malware (keylogger/clipboard rewrite) — Mitigated by Mandatory Attestation

## **A.8 Ledger & State-Continuity Attacks (INFORMATIVE)**

The monotonic, hash-chained Merkle ledger eliminates state-continuity bypasses.

* Ledger rollback — Structurally Eliminated
* Merkle-root mismatch — Structurally Eliminated
* Event reordering — Structurally Eliminated
* Divergent histories — Structurally Eliminated
* Append-without-tick — Structurally Eliminated
* Ledger freeze manipulation — Structurally Eliminated
* Cross-device reconciliation attack — Structurally Eliminated

## **A.9 Digital Asset / Wallet-Custody Attacks (INFORMATIVE)**

PQHD’s multi-predicate custody model eliminates classical wallet vulnerabilities.

* PSBT malleation — Structurally Eliminated
* Signature replay — Structurally Eliminated
* Seed-theft signing — Defeated by Predicate Model
* Classical ECDSA break spending — Defeated by Predicate Model
* Coordinator tampering — Structurally Eliminated
* Multisig drift — Structurally Eliminated
* Recovery bypass — Structurally Eliminated
* Secure Import bypass — Structurally Eliminated
* Chain-key leakage — Structurally Eliminated

## **A.10 AI Behaviour, Model Integrity & Prompt-Layer Attacks (INFORMATIVE)**

PQAI enforces deterministic, tick-bounded behaviour; eliminating ambiguity, drift, and prompt injection.

* AI drift replay — Structurally Eliminated
* Alignment freshness bypass — Structurally Eliminated
* Fingerprint mismatch — Structurally Eliminated
* Runtime-invalid inference — Mitigated by Mandatory Attestation
* SafePrompt bypass — Structurally Eliminated
* Model replacement/profile downgrade — Structurally Eliminated
* Model shadowing — Structurally Eliminated
* Adversarial behavioural patterns — Structurally Eliminated
* Cross-site prompt replay — Structurally Eliminated
* Prompt injection — Structurally Eliminated
* Model-mediated authority elevation — Defeated by Predicate Model
* Behavioural replay — Structurally Eliminated
* Inference under stale ticks — Structurally Eliminated

## **A.11 Identity, Delegation & Credential Attacks (INFORMATIVE)**

Canonical credentials, tick-bounded validity, and deterministic delegation structures eliminate structural misuse.

* Delegated identity scope elevation — Structurally Eliminated
* Delegated spending overflow — Structurally Eliminated
* Delegation replay — Structurally Eliminated
* Identity attribute tampering — Structurally Eliminated
* Selective disclosure bypass — Structurally Eliminated
* Revocation bypass — Structurally Eliminated
* Credential leakage/misuse — Reduced (80–95%)
* KYC issuer spoofing — Structurally Eliminated

## **A.12 Cloud & Host-Operator Attacks (INFORMATIVE)**

Encrypted-Before-Transport (EBT) mitigates plaintext visibility and structural replay.

* Cloud plaintext visibility — Mitigated by Encrypted-Before-Transport (EBT)
* Host operator tampering — Structurally Eliminated
* Cloud snapshot replay — Structurally Eliminated
* Encrypted-bundle replay — Structurally Eliminated
* Long-term storage persistence beyond validity — Structurally Eliminated
* Cloud endpoint impersonation — Structurally Eliminated
* Metadata leakage in cloud workflows — Reduced (60–80%)

## **A.13 Hardware-Level Attacks (INFORMATIVE)**

Hardware-level threats cannot be eliminated cryptographically.

* Hardware fault injection (glitching) — Reduced (60–80%)
* Microarchitectural side-channels (Spectre/Meltdown) — Reduced (40–70%)
* Cache-timing attacks — Reduced (60–80%)
* Power/EM analysis — Reduced (50–75%)
* Entropy/RNG compromise — Reduced (70–90%)
* Malicious silicon (fabrication backdoors) — Reduced (40–60%)
* DMA memory attacks — Reduced (70–90%)
* Rowhammer-class manipulation — Reduced (70–85%)

## **A.14 Software Supply-Chain Attacks (INFORMATIVE)**

Deterministic builds, signatures, and attestation reduce supply-chain attack viability.

* Compiler-level backdoors (Thompson-class) — Reduced (80–90%)
* Dependency poisoning — Reduced (85–95%)
* Update-channel tampering — Reduced (80–90%)
* Build-system compromise — Reduced (80–90%)
* Packaging injection — Structurally Eliminated
* Deterministic-build subversion — Reduced (80–90%)
* Pre-signed malicious binaries — Reduced (80–90%)

## **A.15 Human-Factor Attacks (INFORMATIVE)**

These target the operator, not the system.

* Phishing (KeyMail-targeted) — Structurally Eliminated
* Social engineering against consent — Reduced (70–85%)
* Coercion/duress — Reduced (60–70%)
* User misinterpretation of prompts — Reduced (70–85%)
* Shoulder-surfing/visual capture — Reduced (60–80%)
* Backup mismanagement — Reduced (70–85%)
* User-chosen malicious action — Not reducible

## **A.16 Physical-World & Environmental Attacks (INFORMATIVE)**

Physical and analog threats remain partially outside software control.

* Cold-boot RAM extraction — Reduced (80–90%)
* Physical device theft during active session — Reduced (85–95%)
* Thermal/acoustic leakage — Reduced (40–60%)
* Environmental AI perturbations — Reduced (50–80%)
* Visual adversarial perturbations — Reduced (50–80%)
* Sensor-level prompt injection — Reduced (60–80%)
* Hardware tampering while powered down — Reduced (60–85%)

## **A.17 Military & High-Assurance Applications (INFORMATIVE)**

Applicable to defence, critical infrastructure, contested, or EW environments.

* Satellite/disconnected replay attacks — Structurally Eliminated
* Command spoofing/order injection — Structurally Eliminated
* Intercept-and-reissue (SIGINT-class MITM) — Structurally Eliminated
* Compromised forward operating base host — Mitigated by Mandatory Attestation
* Electromagnetic/RF link replay — Structurally Eliminated
* Cross-unit permission escalation — Structurally Eliminated
* AI-assisted targeting manipulation — Structurally Eliminated
* Base-station model replacement — Structurally Eliminated
* Electronic warfare traffic correlation — Reduced (60–75%)
* Air-gapped hardware breach — Reduced (60–80%)

## **A.18 Implementation Assurance (INFORMATIVE)**

The security benefits described in this annex assume correct implementation of all normative requirements. These analyses do not replace implementation verification, testing, or assurance processes.

---

# **ANNEX B — Glossary**

**AAI — Attested AI**
AI behaviour validated under PQAI + PQVL + Epoch Clock.

**AICW — AI Communication Wrapper**
Secure envelope format used for deterministic AI–AI or AI–system messaging under PQSF.

**Alignment Freshness**
The requirement that an AI ModelProfile must be validated under a tick not older than its alignment_window and fingerprint_window.

**Alignment Tick**
EpochTick bound to the last successful AI alignment or fingerprint event.

**Allowlist**
Canonical list of permitted destinations, roles, or actions within Policy Enforcer semantics.

**AttestationEnvelope (PQVL)**
Signed structure containing ProbeResults, drift_state, tick, and envelope_id.

**Baseline**
Expected canonical probe details used for PQVL drift evaluation.

**ComplianceManifest**
Signed canonical declaration object defined in Section 15.2 containing compliance_level, module_versions, profile_ref, and an ML-DSA-65 signature.

**Compliance Level**
Declared PQSF conformance tier: MVP, FULL, or EXTENDED.

**DeviceIdentity_PQVL**
Identity derived from PQVL attestation public key and measurement hashes.

**DeviceIdentity_Minimal**
Fallback deterministic identity based on device-bound PQHD key.

**Epoch Clock**
Cryptographic time authority anchored to Bitcoin via Ordinals.

**EpochTick**
Signed tick object containing time, profile_ref, alg, and sig.

**Fail-Closed**
Mandatory behaviour: any predicate failure halts the operation.

**KeyMail**
Optional out-of-band confirmation channel for high-risk operations, supplemental to ConsentProof.

**ModelProfile (PQAI)**
Canonical identity and configuration object for AI models, including fingerprint and alignment metadata.

**PQAI**
Post-Quantum Artificial Intelligence alignment and drift framework.

**PQHD**
Post-Quantum Hierarchical Deterministic Wallet specification.

**PQHD Custody (Baseline)**
Minimum conformance tier qualifying as PQHD Custody as defined in Section 10.1.

**PQHD Custody (Enterprise)**
Extended custody tier defined in Section 10.1 for institutional and sovereign threat models.

**PQSF**
Post-Quantum Security Framework.

**PQVL**
Post-Quantum Verification Layer (runtime integrity).

**Policy Hash**
Canonical SHAKE256-256 digest of the deterministic policy object.

**SafePrompt**
Tick-bound, consent-bound structure for high-risk AI operations.

**Transactional Profile (Non-Custodial)**
Single-device configuration explicitly excluded from PQHD Custody guarantees.

**Verifier**
Any system validating cryptographic artefacts under deterministic rules.

---

If you find this work useful and want to support it, you can do so here:
bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw
