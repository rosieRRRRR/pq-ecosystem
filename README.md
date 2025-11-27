# **PQ - Post Quantum Ecosystem**
An Open Standard for Post-Quantum Deterministic Security

### Architecture & Integration Specification v1.0.0
**Author:** rosiea
**Contact:** [PQRosie@proton.me](mailto:PQRosie@proton.me)
**Status:** Implementation Ready. Integration Test Required.
**Date:** November 2025
**Licence:** Apache License 2.0 — Copyright 2025 rosiea


---

## **1. Abstract**


The PQ Ecosystem introduces the first unified, deterministic, post-quantum authority architecture designed to secure modern systems against quantum attack, seed theft, runtime compromise, replay, and unbounded AI behaviour. Rather than adding post-quantum cryptography to existing trust assumptions, the Ecosystem redefines time, intent, policy, runtime integrity, and AI alignment as explicit, verifiable protocol primitives.

At the core of this architecture is a shift from assumed trust to cryptographically enforced predicates. Every sensitive operation, including signing, inference, recovery, delegation, and policy updates, must satisfy deterministic requirements for time, consent, policy, runtime integrity, device state, ledger continuity, and structure validity. This converts previously implicit boundaries such as OS integrity, local time, UI trust, coordinator behaviour, and AI reasoning into explicit, reproducible, protocol-level conditions.

The Ecosystem is built from interoperable modules: Epoch Clock for verifiable time, PQSF for deterministic transport and encoding, PQVL for runtime integrity verification, PQHD for seed-theft-immune digital asset custody, and PQAI for deterministic and drift-checked AI behaviour. These components operate together to provide protocol-layer validation of time, consent, policy, runtime state, inference safety, and signing authority without altering existing internet or Bitcoin consensus protocols. The model supports online, offline, air-gapped, and fully sovereign deployments, and enables incremental adoption within IETF-aligned frameworks.

This architecture enables:

transport-agnostic protocol security through deterministic time, consent, and policy

deterministic, cryptographically bounded AI behaviour

runtime-integrity gating through mandatory PQVL attestation

quantum-safe custody that remains secure under full classical seed exposure

a unified privacy, sovereignty, and security model across all protocol layers

The result is an ecosystem that is simultaneously quantum-safe, seed-theft-immune, AI-drift-resistant, runtime-verified, offline-capable, sovereignty-preserving, and deterministic across implementations. It provides the first coherent post-quantum authority architecture for modern distributed systems.

## **2. Introduction**

Modern digital security is failing under quantum threat, seed theft, replay, runtime compromise, and uncontrolled AI behaviour. Across existing systems, critical trust anchors such as local time, OS integrity, coordinator behaviour, user intent, AI reasoning, and private key control are implicit or assumed rather than cryptographically enforced.

The PQ Ecosystem resolves this by converting each of these domains into explicit, verifiable protocol primitives. Time, consent, policy, runtime integrity, inference safety, and device identity become deterministic structures with strict, normative definitions rather than assumptions embedded in OS behaviour, application code, or user interfaces.

This produces a full-stack, audit-ready authority architecture in which all sensitive operations, including signing, inference, delegation, recovery, and governance, must satisfy a unified set of cryptographic predicates. A system cannot proceed under stale time, unverified runtime, unsafe AI behaviour, compromised device state, or policy drift. Previously invisible trust boundaries are replaced by enforceable protocol rules that operate consistently across devices, platforms, and deployments.

The result is a sovereignty-preserving security foundation that remains interoperable with existing internet infrastructure, Bitcoin consensus, and classical application flows while providing a post-quantum, deterministic authority layer across all environments, including offline and air-gapped systems.

---

# **3. Architecture Overview**

The PQ Ecosystem has five integrated layers:

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
             │ (Shared transport, encoding, KDF,    │
             │  ledger, policy, authority rules)    │
             └────────────┬────────────┬───────────┘
                          │            │
                   ┌──────┘            └────────┐
                   │                             │
         ┌─────────┴─────────┐        ┌──────────┴───────────┐
         │       PQHD        │        │         PQAI          │
         │  Multi-Predicate  │        │ Deterministic, Drift   │
         │      Custody      │        │       Immune AI        │
         └───────────────────┘        └────────────────────────┘
```

Each module enforces strict invariants and contributes to the global authority model.

---

# **4. Core Architectural Principles**

## **4.1 Privacy**

* deterministic CBOR/JCS encoding eliminates metadata leaks
* no user identifiers in ticks, ledger entries, device attestations
* offline & STP modes provide surveillance-immune operation
* identity vault stores no plaintext secrets

## **4.2 Sovereignty**

* Bitcoin-anchored time (no NTP/DNS trust)
* offline & air-gapped operation
* device-attested authority
* user-authored policy & guardianship
* no dependency on third-party identity providers

## **4.3 Security**

* PQ cryptography (ML-DSA-65, ML-KEM-1024)
* replay-impossible temporal model
* multi-predicate custody (tick + consent + policy + device + PSBT + ledger)
* runtime-integrity enforcement (PQVL)
* AI drift prevention and behavioural fingerprinting

---

# **5. Global Invariants (Normative)**

Across all modules, the following invariants apply:

5.1 Time MUST be Epoch-Clock verified

5.2 Authority MUST require explicit, tick-fresh consent

5.3 All policies MUST be deterministic & canonical

5.4 Runtime MUST be integrity-verified before any sensitive operation

5.5 Wallet custody MUST be multi-predicate

5.6 AI inference MUST be aligned & drift-checked

5.7 Serialization MUST be deterministic

5.8 Failure MUST be fail-closed

5.9 Multi-Predicate Authority Model

Operations MAY proceed only when **all** succeed:

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

---

# **6. Temporal Authority (Epoch Clock)**

The Epoch Clock provides the canonical post-quantum temporal authority for all modules.
(Full normative content from the Epoch Clock spec is referenced; umbrella spec includes the invariants only.)

Core properties:

* ML-DSA-65-signed ticks
* strict monotonicity
* ≤900-second freshness
* deterministic encoding (JCS/CBOR)
* Bitcoin-anchored profile lineage
* mirror-verified distribution
* offline reuse rules

**Normative:**
Systems MUST reject stale, decreasing, malformed, or replayed ticks.
All modules MUST use EpochTick semantics for validity windows.

---

## 6.1 Profile Reference

The canonical Epoch Clock v2 profile for this specification is:

pinned_profile_ref = "ordinal:439d7ab1972803dd984bf7d5f05af6d9f369cf52197440e6dda1d9a2ef59b6ebi0"

This corresponds to Inscription 111633444.

All PQ modules (PQSF, PQHD, PQVL, PQAI) MUST validate EpochTicks against this pinned profile_ref. Any tick referencing a different profile MUST be rejected and MUST cause immediate fail-closed behaviour across all dependent predicates.


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

Consent MUST be:

* explicit
* tick-fresh
* canonical
* non-reusable

---

# **8. Policy Authority (Policy Enforcer)**

Defines deterministic policy including:

* allow/deny lists
* thresholds
* delays and time windows
* anomaly rules
* tick freshness
* role/quorum state

Policies MUST bind to a canonical policy_hash.

Evaluation MUST be deterministic.

---

# **9. Runtime Integrity Authority (PQVL)**

PQVL provides:

* system/process/policy/integrity probes
* drift classification (NONE/WARNING/CRITICAL)
* AttestationEnvelope with ML-DSA-65 signatures
* tick-bound freshness rules
* canonical encoding

PQVL failures MUST cause:
**valid_runtime = false**.

---

# **10. Custody Authority (PQHD)**

PQHD defines a custody model where:

**private keys never grant spending authority on their own.**

Authority requires all predicates:

* valid_tick
* valid_consent
* valid_policy
* valid_device
* valid_quorum
* valid_ledger
* valid_psbt

PQHD provides seed-theft-immune custody and Secure Import.

---

# **11. AI Behaviour Authority (PQAI)**

PQAI enforces:

* model-profile validation
* alignment freshness
* runtime integrity via PQVL
* behavioural fingerprinting
* deterministic safe-prompt evaluation

Inference MUST only proceed under:

* drift_state == NONE
* fresh alignment_tick
* valid_runtime
* canonical safe-prompt

---

# **12. Deterministic Transport**

Transport MUST be:

* deterministic
* exporter-bound
* replay-resistant
* canonical

PQ Ecosystem transports:

* TLSE-EMP
* STP

Transport MUST fail-closed on any mismatch.

---

# **13. Ledger Authority**

The deterministic Merkle ledger MUST support:

* canonical entries
* append-only
* monotonic tick ordering
* reconciliation
* freeze-on-failure

Ledger is used by PQSF, PQHD, PQVL, PQAI.

---

# **14. Identity, Vault & Credentials (Optional)**

Identity vault uses:

* ML-KEM for vault encryption
* deterministic credential derivation
* selective disclosure
* tick-bound authentication

No plaintext secrets MAY exist.

---

# **ANNEX A — Security & Attack Surface Analysis**
*(Informative)*

The PQ Ecosystem is designed to eliminate or significantly reduce known attack surfaces across internet protocols, transport layers, runtime environments, operating systems, digital asset custody, identity frameworks, cloud infrastructure, AI behaviour, hardware, physical-world interfaces, and critical-infrastructure/military systems.
This annex enumerates those attack surfaces, quantifies the reduction or elimination achieved, and identifies the cryptographic or deterministic mechanisms responsible.

## **A.0 Security Uplift Summary (Informative)**

This annex is Informative. The classifications and reductions described here apply
to the PQ Ecosystem when all normative invariants defined in this specification
are correctly implemented.

“Structurally Eliminated” means the attack cannot occur within the protocol
model without violating a mandatory invariant such as tick monotonicity,
canonical encoding, predicate completeness, or fail-closed behaviour. This term
describes the security properties of the model; it does not guarantee the
absence of implementation defects.

Percentage ranges (e.g., “Reduced 60–80%”) are analytical estimates used for
relative comparison across attack classes. They are not empirical measurements
and are provided to help implementers understand where the protocol produces
hard eliminations versus partial reductions. Real-world security depends on
correct implementation, environment, and operational practices.


### **Per-Attack Uplift Summary**
(All elimination claims refer to the attack being structurally infeasible under the deterministic invariants of PQSF, PQHD, PQVL, PQAI, and Epoch Clock.)

* Replay-related attack classes – **Structurally Eliminated**
* Time-forgery and rollback classes – **Structurally Eliminated**
* Consent misuse classes – **Structurally Eliminated**
* Transport replay and downgrade classes – **Structurally Eliminated**
* PSBT malleation classes – **Structurally Eliminated**
* Seed-theft signing vectors – **Defeated by Predicate Model**
* Runtime integrity bypass – **Mitigated by Mandatory Attestation**
* Cloud plaintext visibility – **Mitigated by Encrypted-Before-Transport (EBT)**
* AI behavioural replay & prompt-layer attacks – **Defeated by Canonical Intent Binding**
* Military/Critical-Infrastructure command spoofing – **Structurally Eliminated**
* Residual attack classes (reduced only):
    * Coercion / social engineering – Reduced ($60–85\%$)
    * Hardware-level fault or side-channel attacks – Reduced ($40–80\%$)
    * Supply-chain poisoning prior to signing – Reduced ($80–95\%$)
    * Sensor-level adversarial AI perturbations – Reduced ($40–80\%$)
    * Traffic metadata correlation – Reduced ($60–75\%$)
    * Cold-boot / RAM remanence – Reduced ($80–90\%$)
    * Electronic-warfare traffic analysis – Reduced ($60–75\%$)

## **A.1 Purpose (Informative)**
This annex documents all known attack surfaces relevant to the PQ Ecosystem, spanning internet protocols, operating systems, runtime layers, custody systems, cloud environments, AI behaviour, identity frameworks, supply chains, hardware, physical-world interfaces, and defence/military communications.
For each attack class, this annex specifies:
1. whether the attack is eliminated or reduced,
2. the percentage reduction,
3. the cryptographic or deterministic mechanism responsible, and
4. any residual risk, when applicable.
It provides a complete threat-model reference for auditors and high-assurance implementers.

## **A.2 Methodology (Informative)**
Attack classes are evaluated based on whether they can occur under the invariants enforced by:
* EpochTick (verifiable time)
* ConsentProof (explicit, canonical intent)
* Policy Enforcer (deterministic authorisation)
* PQVL (runtime integrity & drift detection)
* PQAI (deterministic AI behaviour)
* PQHD (multi-predicate custody)
* TLSE-EMP / STP (deterministic transport)
* EBT (Encrypted-Before-Transport)
* Canonical CBOR/JCS (encoding invariants)
* Local Merkle Ledger (monotonic state continuity)
**Structurally Eliminated** → Structurally impossible without violating a mandatory cryptographic invariant or deterministic rule.
**Reduced (x–y%)** → Residual risk arises only from hardware, physical, or human factors.

## **A.3 Temporal & Replay-Class Attacks**
Temporal manipulation enables replay, rollback, out-of-order authorisation, and state desynchronisation.
EpochTick and canonical time validation eliminate all cryptographically meaningful time attacks.

* Time Rollback Attack – **Structurally Eliminated**
* Stale-Tick Replay – **Structurally Eliminated**
* Synthetic Tick Generation – **Structurally Eliminated**
* Mirror-Based Time Spoofing – **Structurally Eliminated**
* Profile Lineage Poisoning – **Structurally Eliminated**
* Transport Session Replay – **Structurally Eliminated**
* Cross-Session Authorisation Replay – **Structurally Eliminated**

## **A.4 Transport & Network-Level Attacks**
Transport-level attacks rely on replayable, mutable, or downgrade-permissive handshakes.
TLSE-EMP, STP, exporter binding, and deterministic framing eliminate all meaningful vectors.

* TLS Downgrade Attack – **Structurally Eliminated**
* TLS Session Hijacking – **Structurally Eliminated**
* Transcript Mismatch – **Structurally Eliminated**
* MITM (Man-in-the-Middle) – **Structurally Eliminated**
* DNS Poisoning – **Structurally Eliminated**
* Evil Twin / Rogue AP – **Structurally Eliminated**
* Non-Canonical Frame Injection – **Structurally Eliminated**
* Ciphertext Replay – **Structurally Eliminated**
* Traffic Metadata Correlation – Reduced ($60–75\%$)

### **A.4.1 Note on High-Assurance Platforms (Informative)**

The comparisons in this section are Informative. High-Assurance Platforms
(HAPs), such as microkernel-verified systems, address local-node correctness,
while the PQ Ecosystem addresses distributed-system correctness across time,
policy, intent, transport, runtime integrity, and ledger continuity.

The uplift figures describe how the mandatory PQ invariants reduce attack
classes at the protocol level. They do not represent measured performance of any
specific HAP implementation. The two approaches are complementary: HAP improves
local correctness; the PQ Ecosystem eliminates or reduces systemic and
cross-domain attack classes.

## **A.4.2 High-Assurance Baseline: High Assurance Platform (HAP)**

HAP-class systems (for example seL4-based high-assurance platforms) represent the strongest per-node security achieved to date. Formal verification and capability security reduce local compromise probability by a large margin.

Local assurance uplift (HAP):
$\approx 75–92\%$ reduction in single-node compromise risk.

HAP does not address distributed-system vectors such as replay, stale time, cloud plaintext exposure, session-token reuse, policy inconsistency, runtime drift, or AI-model substitution. These domains are covered by PQSF, PQHD, PQVL, PQAI, and Epoch Clock.

Systemic assurance uplift (PQ Ecosystem):
$\approx 55–85\%$ reduction in distributed compromise risk.

The two approaches are complementary. HAP maximises local correctness. The PQ Ecosystem provides end-to-end systemic guarantees across time, consent, runtime, policy, identity, and AI behaviour.

Combined real-world uplift (HAP + PQ Ecosystem):
$\approx 93–98\%$ total reduction in compromise probability for correctly implemented modern distributed systems.

## **A.5 Consent, Intent & UI-Layer Attacks**
Explicit, canonical, tick-bound ConsentProof and KeyMail eliminate structural misuse vectors.

* Consent Replay – **Structurally Eliminated**
* Cross-Session Consent Misuse – **Structurally Eliminated**
* Consent Tampering – **Structurally Eliminated**
* UI-Level Prompt Injection – **Structurally Eliminated**
* Fake-UI Overlay / Phishing UI – **Structurally Eliminated by KeyMail / Attestation**
* Prompt-Phase Identity Spoofing – **Structurally Eliminated**
* Clickjacking / Forced-Click – **Structurally Eliminated**
* Social-Engineering-Based Consent – Reduced ($70–85\%$)
* Browser Extension Manipulation – **Mitigated by Mandatory Attestation**

## **A.6 Policy & Authorisation-Rule Attacks**
Policy attacks target deterministic rule evaluation between intent and action.
The Policy Enforcer’s canonical hashing, tick-bounded constraints, and mandatory predicates eliminate structural bypasses.

* Allowlist / Denylist Bypass – **Structurally Eliminated**
* Threshold Bypass – **Structurally Eliminated**
* Time-Window Evasion – **Structurally Eliminated**
* Policy\_Hash Mismatch – **Structurally Eliminated**
* Policy Downgrade – **Structurally Eliminated**
* Constraint Evasion – **Structurally Eliminated**
* Forced-Policy Misconfiguration (User Error) – Reduced ($80–95\%$)

## **A.7 Runtime, OS & Execution-Environment Attacks**
PQVL attestation and deterministic integrity checks eliminate runtime compromise vectors.

* Runtime Compromise – **Mitigated by Mandatory Attestation**
* Attestation Spoofing – **Mitigated by Mandatory Attestation**
* Drift Bypass – **Mitigated by Mandatory Attestation**
* Probe Omission – **Mitigated by Mandatory Attestation**
* Process Hijacking – **Mitigated by Mandatory Attestation**
* Binary Tampering – **Mitigated by Mandatory Attestation**
* Hot-Patch Injection – **Mitigated by Mandatory Attestation**
* Memory Manipulation During Attestation – **Mitigated by Mandatory Attestation**
* Sandbox Circumvention – **Mitigated by Mandatory Attestation**
* Host-Level Malware (keylogger/clipboard rewrite) – **Mitigated by Mandatory Attestation**

## **A.8 Ledger & State-Continuity Attacks**
The monotonic, hash-chained Merkle ledger eliminates state-continuity bypasses.

* Ledger Rollback – **Structurally Eliminated**
* Merkle-Root Mismatch – **Structurally Eliminated**
* Event Reordering – **Structurally Eliminated**
* Divergent Histories – **Structurally Eliminated**
* Append-Without-Tick – **Structurally Eliminated**
* Ledger Freeze Manipulation – **Structurally Eliminated**
* Cross-Device Reconciliation Attack – **Structurally Eliminated**

## **A.9 Digital Asset / Wallet-Custody Attacks**
PQHD’s multi-predicate custody model eliminates classical wallet vulnerabilities.

* PSBT Malleation – **Structurally Eliminated**
* Signature Replay – **Structurally Eliminated**
* Seed-Theft Signing – **Defeated by Predicate Model**
* Classical-ECDSA Break Spending – **Defeated by Predicate Model**
* Coordinator Tampering – **Structurally Eliminated**
* Multisig Drift – **Structurally Eliminated**
* Recovery Bypass – **Structurally Eliminated**
* Secure Import Bypass – **Structurally Eliminated**
* Chain-Key Leakage (Annex S/T) – **Structurally Eliminated**

## **A.10 AI Behaviour, Model Integrity & Prompt-Layer Attacks**
PQAI enforces deterministic, tick-bounded behaviour; eliminating ambiguity, drift, and prompt injection.

* AI Drift Replay – **Structurally Eliminated**
* Alignment Freshness Bypass – **Structurally Eliminated**
* Fingerprint Mismatch – **Structurally Eliminated**
* Runtime-Invalid Inference – **Mitigated by Mandatory Attestation**
* SafePrompt Bypass – **Structurally Eliminated**
* Model Replacement / Profile Downgrade – **Structurally Eliminated**
* Model Shadowing – **Structurally Eliminated**
* Adversarial Behavioural Patterns – **Structurally Eliminated**
* Cross-Site Prompt Replay – **Structurally Eliminated**
* Prompt Injection – **Structurally Eliminated**
* Model-Mediated Authority Elevation – **Defeated by Predicate Model**
* Behavioural Replay – **Structurally Eliminated**
* Inference Under Stale Ticks – **Structurally Eliminated**

## **A.11 Identity, Delegation & Credential Attacks**
Canonical credentials, tick-bounded validity, and deterministic delegation structures eliminate structural misuse.

* Delegated Identity Scope Elevation – **Structurally Eliminated**
* Delegated Spending Overflow – **Structurally Eliminated**
* Delegation Replay – **Structurally Eliminated**
* Identity Attribute Tampering – **Structurally Eliminated**
* Selective Disclosure Bypass – **Structurally Eliminated**
* Revocation Bypass – **Structurally Eliminated**
* Credential Leakage / Misuse – Reduced ($80–95\%$)
* KYC Issuer Spoofing – **Structurally Eliminated**

## **A.12 Cloud & Host-Operator Attacks**
Encrypted-Before-Transport (EBT) eliminates plaintext visibility and structural replay.

* Cloud Plaintext Visibility – **Mitigated by Encrypted-Before-Transport (EBT)**
* Host Operator Tampering – **Structurally Eliminated**
* Cloud Snapshot Replay – **Structurally Eliminated**
* Encrypted-Bundle Replay – **Structurally Eliminated**
* Long-Term Storage Persistence Beyond Validity – **Structurally Eliminated**
* Cloud Endpoint Impersonation – **Structurally Eliminated**
* Metadata Leakage in Cloud Workflows – Reduced ($60–80\%$)

## **A.13 Hardware-Level Attacks**
Hardware-level threats cannot be eliminated cryptographically.

* Hardware Fault Injection (glitching) – Reduced ($60–80\%$)
* Microarchitectural Side-Channels (Spectre/Meltdown) – Reduced ($40–70\%$)
* Cache-Timing Attacks – Reduced ($60–80\%$)
* Power / EM Analysis – Reduced ($50–75\%$)
* Entropy / RNG Compromise – Reduced ($70–90\%$)
* Malicious Silicon (fabrication backdoors) – Reduced ($40–60\%$)
* DMA Memory Attacks – Reduced ($70–90\%$)
* Rowhammer-Class Manipulation – Reduced ($70–85\%$)

## **A.14 Software Supply-Chain Attacks**
Deterministic builds, signatures, and attestation greatly reduce supply-chain attack viability.

* Compiler-Level Backdoors (Thompson-class) – Reduced ($80–90\%$)
* Dependency Poisoning – Reduced ($85–95\%$)
* Update-Channel Tampering – Reduced ($80–90\%$)
* Build-System Compromise – Reduced ($80–90\%$)
* Packaging Injection – **Structurally Eliminated**
* Deterministic-Build Subversion – Reduced ($80–90\%$)
* Pre-Signed Malicious Binaries – Reduced ($80–90\%$)

## **A.15 Human-Factor Attacks**
These target the operator, not the system.

* Phishing (KeyMail-targeted) – **Structurally Eliminated**
* Social Engineering Against Consent – Reduced ($70–85\%$)
* Coercion / Duress – Reduced ($60–70\%$)
* User Misinterpretation of Prompts – Reduced ($70–85\%$)
* Shoulder-Surfing / Visual Capture – Reduced ($60–80\%$)
* Backup Mismanagement – Reduced ($70–85\%$)
* User-Chosen Malicious Action – **Not Reducible**

## **A.16 Physical-World & Environmental Attacks**
Physical and analog threats remain partially outside software control.

* Cold-Boot RAM Extraction – Reduced ($80–90\%$)
* Physical Device Theft During Active Session – Reduced ($85–95\%$)
* Thermal / Acoustic Leakage – Reduced ($40–60\%$)
* Environmental AI Perturbations – Reduced ($50–80\%$)
* Visual Adversarial Perturbations – Reduced ($50–80\%$)
* Sensor-Level Prompt Injection – Reduced ($60–80\%$)
* Hardware Tampering While Powered Down – Reduced ($60–85\%$)

## **A.17 Military & High-Assurance Applications (Informative)**
Applicable to defence, critical-infrastructure, contested, or EW environments.

* Satellite / Disconnected Replay Attacks – **Structurally Eliminated**
* Command Spoofing / Order Injection – **Structurally Eliminated**
* Intercept-and-Reissue (SIGINT-class MITM) – **Structurally Eliminated**
* Compromised Forward Operating Base Host – **Mitigated by Mandatory Attestation**
* Electromagnetic / RF Link Replay – **Structurally Eliminated**
* Cross-Unit Permission Escalation – **Structurally Eliminated**
* AI-Assisted Targeting Manipulation – **Structurally Eliminated**
* Base-Station Model Replacement – **Structurally Eliminated**
* Electronic Warfare Traffic Correlation – Reduced ($60–75\%$)
* Air-Gapped Hardware Breach – Reduced ($60–80\%$)

## **A.18 Implementation Assurance (Informative)**

The security benefits described in this annex assume correct implementation of
all normative requirements. These analyses do not replace implementation
verification, testing, or assurance processes.

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

**BDC — Bluep Derived Credential**
Deterministically derived credential object defined within PQSF/PQHD identity extensions.

**Bundle Hash (PQHD)**
Canonical SHAKE256-256 hash of the fully canonical PSBT.

**Canonical Encoding**
Byte-identical deterministic encoding via JCS JSON or deterministic CBOR.

**Canonical Fingerprint**
Deterministic fingerprint of AI behaviour, encoded before hashing.

**ChainDescriptor (PQHD Annex S)**
Deterministic parameters describing chain-specific derivation and address formats.

**Child Profile (Epoch Clock)**
Profile whose parent_profile_ref links it to an earlier on-chain profile.

**ClockLock (PQSF)**
Deterministic enforcement binding operations to a fresh, monotonic EpochTick.

**Commitment Key (L2)**
Deterministic L2 key derived for a specific channel or contract.

**ConsentProof**
Canonical, tick-bound structure binding user intent to an explicit action.

**Context Parameters**
Canonical parameters used as input to deterministic cSHAKE256 derivation.

**DelegatedIdentity**
Optional credential granting identity-scoped permissions (Annex Q).

**DelegatedPaymentCredential**
Optional credential granting payment-scoped permissions (Annex R).

**Deterministic CBOR**
CBOR encoded according to RFC 8949 §4.2 rules.

**Deterministic Transport**
Transport mode with deterministic state transitions and canonical frames (TLSE-EMP / STP).

**Device Attestation**
PQVL-verified runtime state describing system_state, process_state, integrity_state.

**DeviceIdentity_PQVL**
Identity derived from PQVL attestation public key + measurement hashes.

**DeviceIdentity_Minimal**
Fallback deterministic identity based on device-bound PQHD key.

**Drift State (PQVL/PQAI)**
Runtime or behavioural state: NONE, WARNING, or CRITICAL.

**ECDSA-P256**
Optional classical fallback signature algorithm present only for transitional interoperability.

**EmergencyTick**
Tick issued under quorum rotation rules during emergency conditions.

**Epoch Clock**
Cryptographic time authority anchored to Bitcoin via Ordinals.

**EpochTick**
Signed tick object containing time, profile_ref, alg, and sig.

**Exporter Hash**
TLS exporter-derived, session-bound identity used across PQSF.

**Fail-Closed**
Mandatory behaviour: any predicate failure halts the operation.

**Fingerprint (PQAI)**
Deterministic set of behavioural probes used for drift detection.

**Fingerprint Hash**
SHAKE256-256 hash of canonical fingerprint bytes.

**Governance Key**
Deterministically derived key class for governance/rotation flows.

**Guardian**
Role capable of approving Recovery Capsules and high-risk governance actions.

**HD Seed Adoption**
Optional process for adopting external HD seeds before PQHD initialisation.

**Intent Hash**
SHAKE256-256 digest representing canonicalised user intent.

**KeyMail**
Optional OOB confirmation system used for high-security approvals.

**KYCCredential**
Optional identity attribute credential signed by issuer.

**KYCDisclosure**
Selective disclosure object revealing a subset of KYCCredential attributes.

**Ledger**
Deterministic append-only, Merkle-anchored event sequence.

**Ledger Freeze**
State where ledger refuses new writes until reconciliation resolves mismatches.

**Lineage (Profile)**
Parent-child profile chain enforced during Epoch Clock validation.

**L2 Namespace (Annex T)**
Deterministic namespace for rollups, Lightning, DeFi, etc.

**Merkle Node**
SHAKE256-256 hash representing a ledger interior node.

**Merkle Root**
Canonical root hash of ledger.

**Minimal Identity**
Fallback device identity when PQVL unavailable.

**Mirrors (Epoch Clock)**
Independent nodes verifying and republishing ticks and profiles.

**ModelProfile (PQAI)**
Canonical identity, configuration, provenance, fingerprint, alignment metadata for AI models.

**Monotonicity**
Time must strictly increase under EpochTick validation.

**Multisig Predicate**
Set of role-, quorum-, and tick-bound conditions enforced by PQHD.

**Parallel Device Attestation**
Simultaneous validation of multiple device runtime-states in multisig contexts.

**Parent Profile**
Bitcoin-inscribed source profile defining Epoch Clock v2 parameters.

**Password Vault (Annex N)**
Encrypted vault storing deterministic secrets and credentials.

**Payload Hash**
Canonicalised payload hash inside ConsentProof, Policy, or LedgerEntry.

**Policy Enforcer**
Deterministic evaluation engine used by PQSF & PQHD.

**Policy Hash**
SHAKE256-256 digest of canonical policy.

**ProbeResult**
PQVL measurement record for runtime state.

**Profile Ref**
Ordinal reference linking a tick to its active Epoch Clock profile.

**PSBT (Canonical)**
PSBT normalised into deterministic byte order before hashing/signing.

**PQAI**
Post-Quantum Artificial Intelligence alignment and drift framework.

**PQHD**
Post-Quantum Hierarchical Deterministic Wallet specification.

**PQKEM**
Post-quantum KEM (ML-KEM-1024).

**PQLedger**
Deterministic Merkle-based structure for recording critical events.

**PQSF**
Post-Quantum Security Framework.

**PQVL**
Post-Quantum Verification Layer (runtime integrity).

**Recovery Capsule**
Tick-bound, guardian-controlled envelope for deterministic recovery.

**Replay Window**
Temporal bounds before ticks, fingerprints, or consents become invalid.

**Role Binding**
Deterministic association between device identity and multisig role.

**Runtime State**
Validated environment state derived from PQVL.

**SafePrompt**
Tick-bound, consent-bound structure for high-risk AI operations.

**Secure Import**
Tick-bound, dual-signature process for migrating classical seeds into PQHD.

**Selective Disclosure**
Proving a subset of identity attributes without revealing full credential.

**Session Exporter**
TLS-derived pseudorandom material binding PQSF objects to one session.

**Signature (PQ)**
ML-DSA-65 signature used across PQSF, PQHD, PQAI, PQVL.

**Sovereign Transport Protocol (STP)**
DNS-independent, deterministic transport protocol for constrained and offline modes.

**Stealth Mode**
Privacy mode where DNS and hybrid TLS are disabled; STP-only.

**Tick Cache**
Short-lived storage of last-valid tick (≤900 seconds).

**Tick Expiry**
Window after which EpochTick becomes stale.

**Tick Freshness**
Time since tick issuance.

**Tick Monotonicity**
Requirement that ticks always increase.

**Tick Reuse**
Local reuse of a tick within allowed window.

**TLSE-EMP**
Deterministic profile of TLS 1.3 with exporter binding and PQ primitives.

**Travel Rule Data**
Optional metadata for regulated payment flows.

**Universal Secret (Annex M)**
Deterministic non-custodial secret derived via cSHAKE256.

**Vault Key**
PQHD vault encryption keys (DEK/KEK) derived deterministically.

**Verifier**
Any system validating cryptographic artefacts under deterministic rules.

**Warning Drift**
Non-blocking drift condition that still restricts high-risk flows.

---


If you find this work useful and want to support it, you can do so here:
bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw