# PQ Architecture Surface

**Privacy, Protocol Overlay, Governance Primitives, and Deployment Surface**

*Companion document to the PQ Ecosystem README*
*Version 1.0.0 — 2026*
*Author: rosiea — PQRosie@proton.me*

---

PQ is an enforcement architecture. All capabilities described in this document — privacy, governance, delegation, compliance, protocol overlay, deployment breadth — are compositional consequences of that design. They emerge from the interaction of deterministic enforcement, authority separation, canonical encoding, and fail-closed semantics. They are not separate features.

---

## Privacy Architecture

PQ implements privacy structurally, not as a feature toggle. Privacy is a consequence of the enforcement model, not an addition to it.

### Local-First Enforcement (Holder Execution Boundary)

All enforcement runs within the Holder Execution Boundary. Canonical encoding, hashing, signing, signature verification, and cryptographic profile binding MUST occur locally. Delegation of these operations to cloud infrastructure, middleware, or remote services renders the implementation non-conformant.

No enforcement data leaves the device unless explicitly exported under governed policy. The architecture enforces locally and exports selectively.

**Source:** PQSEC — Holder Execution Boundary Requirement

### Encrypted Before Transport (EBT)

Sensitive artefacts are encrypted before entering any transport or storage boundary outside the originating security domain. Not "encrypted in transit" — encrypted before transit. The transport layer sees ciphertext only. Compromise the transport and you get nothing.

EBT encryption keys are derived deterministically via PQSF Universal Secret Derivation with domain-separated customisation strings. This applies regardless of whether the transport is TLS, LoRa, Bluetooth, UART, or physical media.

**Source:** PQSF — Encrypted-Before-Transport Wrapper

### Evidence by Hash, Not by Content

Audit records reference artefacts by hash, not by content. Reports MUST NOT contain raw secrets, credentials, or sensitive evidence. Enforcement logs prove that evaluation happened and what the outcome was — without exposing the evidence that was evaluated.

A compliance officer can verify: "a valid ConsentProof was present, KYC receipt was valid, quorum was met, outcome was ALLOW at tick 847293." They never see the consent content, the KYC documents, or the quorum participants' identities unless policy explicitly permits that disclosure.

**Source:** PQSEC — Audit and Reporting; PQSEC — HRI Manifest

### Structural Anonymity (Fleet Telemetry)

When operational data does need to leave the device, FleetTelemetryEnvelope enforces structural anonymity:

- No stable device identifiers permitted in the envelope body
- Timing windowed to ticks — no sub-tick precision
- Fault hashes derived from fixed deterministic vocabulary — no stack traces, memory addresses, or device-specific diagnostics
- Build hash shared across device class, not per-device unique
- Constant-shape envelopes — zero counts for absent event types, not omitted keys
- Emission is operation-scoped, not periodic — no heartbeat fingerprinting
- TelemetryBudget caps volume, frequency, and size with mandatory enforcement

**Source:** PQSF §17B — Privacy-Preserving Fleet Telemetry Envelope

### Sovereign Deletion

Persistent state belongs to the human. All of it — both human-side and AI-side relational state. The human holds sole authority. Deletion produces a cryptographic DeleteReceipt. After deletion, the predicate evaluates UNAVAILABLE (not FALSE — the distinction matters). Implementations MUST NOT retain deleted content.

**Source:** PQPS — Human Authority Model; PQPS — Verifiable Deletion

### Stealth Mode and Operational Tempo Protection

Epoch Clock defines Stealth Mode for environments where tick fetch patterns could leak operational intent. Tick caching is mandatory. Implementations MUST NOT fetch ticks in direct response to individual operation requests. Fetch schedules are fixed and independent of operation frequency.

**Source:** Epoch Clock — Stealth Mode; Epoch Clock — Tick Fetch and Caching Discipline

### Auditable Compliance Without Data Exposure

KYC, consent, and authorisation can be audited via receipts without exposing underlying data, subject to policy-defined export and disclosure rules.

| Compliance Need | Privacy Mechanism |
|---|---|
| Prove KYC was checked | PQAA receipt — hash, not content. Auditor sees: valid receipt from approved provider, issued at tick X, expires tick Y. |
| Prove consent was obtained | ConsentProof bound to intent_hash. Auditor sees: consent present, valid signature, scope matches, unexpired. |
| Prove spending was authorised | EnforcementOutcome references evidence by hash. Auditor sees: ALLOW, predicates evaluated, quorum met. |
| Prove AI model was verified | PQAI ModelIdentity + drift classification. Auditor sees: model hash, drift NOMINAL, fingerprint valid. |
| Prove time was valid | Epoch Clock tick reference. Auditor sees: tick number, Bitcoin-anchored, verified locally. |

**Source:** PQAA — Adapter Workflow; PQSF §17A — Receipt Export Policy

---

## Protocol Overlay

PQ does not replace existing protocols. It is the governance layer above them.

### The Fundamental Gap

Existing protocols answer "is this channel secure?" PQ answers "should this operation be permitted?" These are fundamentally different questions.

TLS protects the pipe. HAP authenticates the accessory. OAuth grants a token. None of them evaluate whether the operation should proceed given all available evidence — time, consent, policy, operator state, model identity, quorum, delegation scope — and refuse if anything is missing, stale, or unverifiable.

### Transport-Agnostic

STP (Sovereign Transport Protocol) binds to TLS 1.3 via exporter hash, but PQ enforcement runs independently of transport. The same governance layer operates over:

- TLS 1.3 (standard web/API)
- LoRa mesh (Meshtastic, Sidewalk)
- Bluetooth Low Energy
- UART / serial
- Air-gapped media (USB, SD card)
- Satellite links (laser, RF)
- Any future transport

The transport carries ciphertext. PQ governs the decision.

**Source:** PQSF — Sovereign Transport Protocol; PQSF — Encrypted-Before-Transport Wrapper

### Connectivity-Independent

The enforcement engine runs locally. It does not require network connectivity for any enforcement decision.

- Epoch Clock caches verified ticks with deterministic staleness model
- BufferedMeasurementEnvelope stores evidence offline for later flush
- Bootstrap in hostile or isolated networks is a normative annex
- No-Tick Mode provides safe degradation when completely offline

**Source:** Epoch Clock — Offline Degradation Semantics; PQSF — BufferedMeasurementEnvelope; PQSF Annex AH — Bootstrap in Hostile or Isolated Networks

### OS-Agnostic

PQAA normalises platform-native trust anchors into canonical PQ evidence. Resulting evidence classification is policy-dependent and varies by deployment configuration:

| Platform | Typical Trust Anchor | Typical Evidence Class |
|---|---|---|
| iOS / macOS | Secure Enclave | `hardware_attested` |
| Android | StrongBox / TEE | `hardware_attested` or `platform_bridged` |
| Windows | TPM 2.0 | `hardware_attested` or `platform_bridged` |
| ChromeOS | Titan C | `hardware_attested` or `platform_bridged` |
| Linux | TPM (where present) / IMA | `hardware_attested` or `platform_bridged` |
| RTOS / bare metal | Secure element (ATECC608, SE050) | `hardware_attested` or `platform_bridged` |

PQSEC enforcement profiles scale to hardware capability:

| Profile | Target |
|---|---|
| `high-assurance-v1` | Security infrastructure, HSMs, high-value custody |
| `standard-v1` | General-purpose servers, desktops, mobile devices |
| `embedded-minimal` | Constrained MCU devices (ESP32, nRF52, kilobytes of RAM) |

**Source:** PQAA — Architecture; PQSEC Annex AU.X — Embedded-Minimal Enforcement Profile; PQSEC Annex BA — Conformance Profiles

---

## Governance Primitives

The combination of scoped delegation, M-of-N quorum, single-use consent, evidence-without-data attestation, and deterministic audit constitutes a general-purpose governance framework. These are not extensions to the architecture — they are predicates within PQSEC, available to any deployment.

### Delegation

DelegationGrant is scoped (what operations), time-bounded (issued_tick to expiry_tick), and revocable (without the delegate's cooperation via DelegationRevocation). Delegation cannot bypass consent, policy, time, runtime, or quorum predicates. Absent delegation artefacts evaluate to UNAVAILABLE, which maps to DENY for Authoritative operations.

Delegation chains are cryptographically verifiable. A DelegationGrant can reference a ConsentProof via consent_ref, binding the delegation to explicit human consent.

**Source:** PQSEC — valid_delegation_grant predicate

### Quorum

M-of-N evaluation is a first-class predicate. The Coordinator is untrusted — it MUST NOT evaluate predicates, produce enforcement decisions, select which signers participate based on expected outcome, suppress or delay EnforcementOutcome delivery, or aggregate signatures unless each contributing signer has independently verified the EnforcementOutcome.

**Source:** PQSEC — Coordinator Trust Model

### Consent

ConsentProof is single-use via burn semantics. Replay produces `E_CONSENT_REPLAY_DETECTED`. Consent is scoped to a specific intent via intent_hash and bound to a specific enforcement decision. ConsentRevocation invalidates a ConsentProof before expiry — revocations may arrive before, after, or independently of the proofs they reference.

**Source:** PQSF — ConsentProof Grammar; PQSEC — valid_consent predicate

### Voting

A vote is a consent artefact. One entity, one burn — structurally unreplayable. Time-bounded polls anchored to Epoch Clock. Ballot secrecy via EBT. Delegation of votes via DelegationGrant with mid-stream revocation via DelegationRevocation. Coercion resistance via Neural Lock operator state attestation.

### KYC Privacy

PQAA bridges identity attestation into ReceiptEnvelope. The receipt proves "this entity passed KYC at provider X at tick Y" without containing the identity documents. Counterparties verify the receipt signature and expiry without seeing the identity behind it. Cross-border portability via policy-driven provider namespace acceptance — policy decides which KYC providers are trusted, not the protocol.

**Source:** PQAA — Adapter Workflow; PQSF §17A — Receipt Export Policy

### Spending Authority

BPC pre-construction gating composes with DelegationGrant and valid_quorum to create governed spending: "entity X can spend up to amount Y from account Z, requiring 2-of-3 board approval, with CFO consent, valid until tick T." The transaction is not constructed until all predicates evaluate TRUE. Every spending decision produces a verifiable EnforcementOutcome.

**Source:** BPC — Pre-Construction Gating; PQSEC — Predicate Model

---

## Deployment Surface

PQ applies to any system where operations should be governed by evidence rather than trust.

### By Transport

| Transport | PQ Integration |
|---|---|
| TLS 1.3 | STP binds via TLS exporter hash. Standard deployment. |
| LoRa / mesh | EBT over radio. BufferedMeasurementEnvelope for offline nodes. Embedded-minimal profile. |
| Bluetooth | STP or raw EBT. Device-to-device governance without internet. |
| Satellite | STP over laser or RF. Same governance at 550km altitude. |
| Air-gapped | Evidence on physical media. Tick cached locally. Full enforcement without connectivity. |

### By Scale

| Scale | PQ Profile | Example |
|---|---|---|
| MCU (kilobytes) | Embedded-minimal | Sensor node, Meshtastic radio, insulin pump |
| Mobile device | Standard | Phone wallet, field device, delivery terminal |
| Desktop / server | Standard or high-assurance | Workstation, API server, custody node |
| Cloud infrastructure | High-assurance | HSM cluster, key management, enforcement service |
| Fleet | Standard + fleet telemetry | Vehicle fleet, device fleet, satellite constellation |

### By Domain

The specifications are domain-agnostic at the enforcement layer. Domain-specific behaviour is expressed through policy configuration and predicate selection, not through enforcement engine modification.

This is not a compliance certification. It is an evidence and enforcement substrate that can support compliance regimes. The following candidate domains have been mapped against the specification text (informative):

- Financial custody (Bitcoin, fiat, multi-asset)
- AI model governance (identity, drift, safety)
- Embodied systems and robotics
- Autonomous agent orchestration
- Smart home and IoT
- Healthcare (prescriptions, patient data, telehealth)
- Supply chain and logistics
- Media licensing and royalties
- Satellite operations
- Enterprise access governance
- Voting and collective decision-making
- Regulatory compliance substrates (SOC2, HIPAA, GDPR, PCI-DSS)
- Identity and KYC privacy

---

*This document is a companion to the PQ Ecosystem README. For normative definitions, see PQSEC. For the complete specification list with versions, see the PQ Ecosystem Hub.*
