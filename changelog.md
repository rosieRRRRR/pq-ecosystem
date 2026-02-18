# PQ Ecosystem — Unified Changelog

**Date:** 2026
**Author:** rosiea
**Contact:** [PQRosie@proton.me](mailto:PQRosie@proton.me)
**Licence:** Apache License 2.0 — Copyright 2026 rosiea

---

This document consolidates the changelogs from all specifications in the PQ Ecosystem into a single reference. Individual specification changelogs remain authoritative within their respective documents.

---

## Specification Versions at a Glance

| Specification | Version | Status |
|---|---|---|
| PQSF — Post-Quantum Security Framework | 2.0.3 | Implementation Ready |
| PQSEC — Post-Quantum Security Enforcement Core | 2.0.3 | Implementation Ready |
| Epoch Clock — Cryptographic Time Authority | 2.1.0 | STABLE / INSCRIBED |
| PQHD — Post-Quantum Hierarchical Deterministic Custody | 1.2.0 | Implementation Ready |
| PQAI — Post-Quantum AI | 1.2.0 | Implementation Ready |
| BPC — Bitcoin Pre Contracts | 1.1.0 | Implementation Ready |
| Neural Lock — Operator State Evidence | 1.1.0 | Implementation Ready |
| ZEB — Zero Exposure Broadcast | 1.3.0 | Implementation Ready |
| PQHR — Human-Readable Policy Interface | 1.0.0 | Implementation Ready |
| PQPS — Post-Quantum Persistent States | 1.0.0 | Implementation Ready |
| PQPR — Proof-of-Reference Tool | 1.0.0 | Implementation Ready |
| PQAA — PQ Attestation Adapter | 1.0.0 | STANDALONE — Migration Layer |
| PQEA — Post-Quantum Embodied Agent Governance | 1.0.0 | Implementation Ready |
| PQ Gateway — Sovereign AI Governance Layer | 1.0.0 | Implementation Ready |

---

## PQSF v2.0.3 — Post-Quantum Security Framework

### Added

* **§8.7 Cryptographic Sunset Discipline**: monotonic sunset states (ACTIVE, SUNSET_PENDING, SUNSET_FINAL), bounded dual-acceptance windows, rollback prohibition, and offline deployment rules for algorithm retirement. Introduces `E_PROFILE_SUNSET_FINAL` refusal code.
* **§17B Privacy-Preserving Fleet Telemetry Envelope**: constant-shape, correlation-minimized telemetry with `FleetTelemetryEnvelope` and `TelemetryBudget`. Enforces structural anonymity (no stable device identifiers, tick-windowed timing, operation-scoped emission).
* **§21X BufferedMeasurementEnvelope**: deterministic store-and-forward measurement batching with `MeasurementRecord`, tick-bounded batches, ordering rules, and export governance.
* **§22X CaptureReceipt and MediaCommitment**: tamper-evident capture commitments with `MediaCommitment`, `CaptureReceipt`, and `MediaDeleteReceipt`. Includes PQPS interaction clause establishing deletion semantics precedence.
* **§32A Schema Version Governance**: deterministic schema version handling with deployment version bounds, session floor ratcheting, and mixed-version refusal. Introduces `E_SCHEMA_VERSION_UNSUPPORTED` and `E_SCHEMA_DOWNGRADE_ATTEMPT` refusal codes.
* **§32B Evidence Classification Vocabulary**: provenance taxonomy (hardware_attested, secure_boot_bound, software_measured, model_inferred, user_asserted, external_asserted) and `EvidenceDescriptor` artefact. Introduces `E_EVIDENCE_DESCRIPTOR_REQUIRED` refusal code.
* **§31.1 Canonical Encoding Verification**: normative requirement for PQSF Canonical CBOR Test Vector Suite processing, byte-identical encoding, hash equivalence, and encoder drift regression testing.
* **Annex AD Determinism Verification Harness**: required test classes, minimum determinism properties, equivalence class partitions, and publication requirements.
* **Annex AE STP KEM Fallback Derivation Example**: reference pseudocode for both KEM fallback and PQ TLS key derivation paths.
* **Annex AG PQ Stack Starter Pack and Conformance Harness**: starter pack directory structure, mandatory examples, fixture requirements, harness coverage, and conformance obligation.
* **Annex AH Bootstrap in Hostile or Isolated Networks**: cold-start tick provisioning requirements complementary to PQSEC BOOTSTRAP mode.
* STP extended with normative STP-DATA and STP-CLOSE message types (§27.2.5, §27.2.6) providing framed application data with monotonic sequencing, body hashing, session-bound MAC, and orderly session termination with key destruction mandate.
* Harmonised `session_id` type across all STP message types, exporter binding context (§15), ConsentProof (§16), EBTEnvelope (§21), and KeyMail (Annex V) to `bstr(16)`.
* Added `kem_ciphertext` to STP-INIT and `kem_confirm` to STP-ACCEPT for inline §27.6A fallback KEM negotiation.
* Expanded STP canonical encoding requirements (§27.3) for body_hash, mac, and payload signature computation ordering.
* Normative STP Handshake State Machine (§27.5) with 7 states, valid transitions, timeout bounds, error recovery, and key material lifecycle.
* Normative STP-to-TLS Binding (§27.6) with exporter binding derivation, channel binding verification, and operational classification.
* Normative STP-Layer PQ KEM Fallback (§27.6A) for Authoritative sessions without PQ TLS, including ML-KEM-1024 exchange, kem_confirm verification, and dual-path key derivation.
* Normative STP Integrity and KDF Primitives (§27.6B) specifying HKDF-SHA256 and HMAC-SHA256 with byte-precise input/output lengths.
* Normative STP Credential Lifecycle (§27.7) covering derivation, domain binding, storage, non-extractability, atomic rotation, and revocation.
* Informative STP Web Discovery (§27.8) with HTTP header, well-known URI, and DNS TXT mechanisms.
* Expanded Annex G with 5 lifecycle diagrams including DATA/CLOSE flows, error recovery, idle timeout, and KEM fallback path.
* Updated Conformance (§29) and Conformance and Verification (§31) for STP state machine, framing, binding, credential, and determinism verification.

### Changed

* Clarified PQSF's role as protocol-layer foundation only (grammar, canonical encoding, cryptographic indirection; enforcement and authority remain external).
* Standardised deterministic CBOR for all PQSF-native artefacts; formalised Epoch Clock JCS Canonical JSON exception with strict no-re-encoding rules.
* Expanded CryptoSuiteProfile governance: signed distribution, revocation, downgrade prevention, emergency cryptographic transition.
* Refined exporter binding primitives for deterministic, session-scoped security independent of network trust.
* Tightened ConsentProof, PolicyObject, and PolicyBundle definitions as inert, non-authoritative structures.
* Consolidated supply-chain artefact grammars, reproducible build support, and ledger anchoring.
* Finalised Encrypted-Before-Transport (EBT) wrapper structure and key-derivation rules.
* Finalised Sovereign Transport Protocol (STP) grammar and capability negotiation.
* Cleaned annex boundaries (normative, optional, informative).

---

## PQSEC v2.0.3 — Post-Quantum Security Enforcement Core

### Added

* **§1 Policy Activation**: all enforcement requirements are policy-activated; policy determines which are active per operation class. Policy MUST NOT weaken profile floors.
* **§1 Centralised Enforcement Rationale**: architectural justification for centralised predicate evaluation as enabling composable fail-closed semantics.
* **§22A.7 Platform-Bridged Evidence Consumption (Informative)**: admissibility of `platform_bridged` evidence from governed adapters (PQAA).
* **§18X Governance Cadence and Churn Refusal**: prevents excessive predicate re-evaluation frequency, decouples governance cadence from real-time control loops. Introduces `GovernanceCadence` artefact and `E_GOVERNANCE_CHURN` refusal code.
* **§22B Evidence Strength and Independence**: structural independence classes (`independent`, `diverse`, `any`) for evidence sets, prevents single-source masquerading as quorum. Introduces `E_EVIDENCE_NOT_INDEPENDENT` refusal code.
* **Annex AU.X Embedded-Minimal Enforcement Profile**: minimum viable enforcement for constrained MCU devices. Introduces `E_PROFILE_CAPABILITY_INSUFFICIENT` and `E_REPLAY_GUARD_UNAVAILABLE` refusal codes.
* **Annex AV Deliberation Enforcement Class (DEC)**: composite enforcement for irreversible, high-consequence operations requiring intent declaration, deliberation delay, interactive human approval, dual-phase Neural Lock, optional witness attestation, and durable replay protection.
* **Annex AX Extension and Adapter Admission Discipline**: admission rules for third-party extensions, plugins, skills, and tool adapters. Manifest-bound installation, permission mutation detection, adapter integrity binding, fail-closed re-admission on update.
* **Annex BA Implementation Profiles (Normative)**: three deployment posture profiles (`minimal-v1`, `standard-v1`, `highassurance-v1`) with bounded requirements, privacy-safe profile declaration, conformance evidence, and non-conformant claim prohibitions.
* **Annex BA.3A Profile Floor (Normative)**: profiles define minimum enforcement floor that policy MUST NOT weaken.
* **Annex BA.3B Bridged Evidence Restrictions by Profile (Normative)**: per-profile `platform_bridged` restrictions. `highassurance-v1` prohibits blanket admission across custody predicates.
* **Annex BA.3C Minimal-v1 Reading Scope (Informative)**: sections required for `minimal-v1` conformance.
* Policy staleness enforcement (`POLICY_FRESH`, `POLICY_STALE_WARN`, `POLICY_STALE_LOCK`).
* Evidence producer governance: build allowlists, predicate scope limits, evidence freshness constraints.
* External error surface discipline with constant-shape, constant-latency responses.
* Execution profile enforcement, consent and delegation boundaries, and replay protection.
* Canonical PQ Ecosystem Registry for predicate names, hash usage, and cross-spec anchors.

### Changed

* Refined §4 Trust Assumptions: strengthened Epoch Clock invariant; added policy binding invariant.
* **Annex AE Registry Restructure**: replaced AE.0 and removed AE.34 with unified AE.0 (Registry Governance and Classification Model). Added 12 new refusal codes across AE.4, AE.8, AE.45–AE.50.
* Harmonised `session_id` type to `bstr(16)` / `bytes` across EnforcementOutcome grammar, AdmissionContext, and exporter hash derivation pseudocode.
* Updated Annex AN ecosystem minimum versions and Annex AT cross-spec anchor registry.
* Updated dependency table to require PQSF ≥ 2.0.3 and PQAI ≥ 1.2.0 (when AI bindings are used).
* Consolidated PQSEC as sole enforcement authority. All predicate evaluation, refusal, escalation, lockout, and EnforcementOutcome production occur exclusively within PQSEC.
* Finalised ternary predicate result model (`TRUE` / `FALSE` / `UNAVAILABLE`) with strict fail-closed for Authoritative operations.
* Strengthened Epoch Clock enforcement: inert-on-ambiguous-time, prohibition of fallback time sources.
* Expanded lockout and recovery semantics: multi-instance coordination, deterministic recovery.
* Formalised execution profile enforcement, consent boundaries, and replay protection.

### Removed

* Privacy predicates from core (now enforced via policy and execution discipline).

### Subsumed

* **PQVL** subsumed into PQSEC as runtime-evidence subsystem. RuntimeMeasurementEvidence → Annex AQ; Drift classification → §22; Probe validation → §22 and Annex M; Lockout escalation → §25. Implementations MUST NOT implement PQVL as a separate enforcement surface.

---

## Epoch Clock v2.1.0 — Cryptographic Time Authority

### Added

* **Profile v3 schema** with multi-signature governance and threshold tick validation.
* **Tick v3 multi-signature format** (`tick_sigs`, `tick_body_hash`, threshold validation).
* Content-addressed identifiers: `governance_config_id`, `tick_keyset_id`.
* Explicit profile signature preimage rules.
* Version detection rules (v2 vs v3 profiles and ticks).
* Genesis profile defaults for backward compatibility.
* **CompromiseRevocationNotice** structure and issuer key compromise response.
* Expanded mirror reconciliation and state-machine behaviour.
* Formalised error-code registry (including v3-specific refusal codes).
* Offline degradation semantics (§9A) with defined staleness thresholds.
* Clarified Strict Unix Time base for `t`.
* Explicit SHAKE256 output length requirement (32 bytes).
* Sovereign deployment and bootstrap hardening language.

### Changed

* Status updated to STABLE / INSCRIBED.
* Canonical profile reference formalised in §1.2A.
* Expanded integration guidance across PQSF, PQSEC, PQHD, PQAI.
* Strengthened fail-closed semantics for mirror divergence and lineage mismatch.
* Clarified authority boundaries (time artefacts only; enforcement external).
* Tightened canonical encoding requirements (JCS only, no CBOR).
* Strengthened mirror identity verification requirements.

### Unchanged

* Core v2 profile structure and canonical inscription.
* ML-DSA-65 as required signature algorithm.
* SHAKE256-256 hashing.
* 900-second tick reuse window.
* Mirror-majority validation requirement.
* No consensus-layer changes.
* Refusal-only enforcement model.

---

## PQHD v1.2.0 — Post-Quantum Hierarchical Deterministic Custody

### Changed

* **Authority separation finalised**: formally decoupled Bitcoin signing authority from key possession. Private keys are necessary inputs but never sufficient for authorisation.
* **External enforcement locked**: all predicate evaluation, refusal, freshness, monotonicity, escalation, and lockout semantics delegated exclusively to PQSEC. PQHD defines policy and structure only.
* **Unified custody predicate stabilised**: canonicalised custody predicate composition (`valid_tick`, `valid_consent`, `valid_policy`, `valid_runtime`, `valid_quorum`, `valid_ledger`, `valid_psbt`) with fail-closed on ambiguity.
* **Custody tiers clarified**: finalised Baseline and Enterprise tiers with explicit qualification requirements. Removed implicit or reduced authority modes.
* **Deterministic key hierarchy hardened**: standardised PQ root and child key derivation with strict domain separation. Prohibited authority inference from key derivability.
* **Canonical PSBT discipline enforced**: strict PSBT v2 canonicalisation, equivalence rules, and deterministic intent hashing to prevent malleability and signer divergence.
* **Dual-control signing mandated**: valid, single-use PQSEC EnforcementOutcome for every signing attempt with binding and replay-protection requirements.
* **Recovery governance formalised**: guardian-based recovery with enforced delay, quorum approval, SafeMode integration, and full PQSEC enforcement. Recovery cannot bypass custody predicates.
* **Execution boundary integration clarified**: non-authoritative integration with ZET and ZEB. Execution method selection does not modify custody authority semantics.
* **Auditability without surveillance**: hash-only audit logging with explicit prohibition of payload, address, and descriptor leakage.

---

## PQAI v1.2.0 — Post-Quantum AI

### Added

* **§27.10 Tool Namespace Governance**: namespace structure for tool_id values, reserved `pq.` prefix, schema registry binding, `E_TOOL_SCHEMA_UNSUPPORTED` refusal code.
* **§27.11 AggregationScope**: cross-device, cross-tenant, and fleet aggregation boundary rules with scope types, linkage prohibition, `E_AGGREGATION_SCOPE_REQUIRED` refusal code. Generalised stable join key prohibition.
* **§27.12 Probabilistic Normalisation**: deterministic fixed-point normalisation for classifier outputs with floor-based conversion and cross-platform determinism.
* **§27.13 SafetyDomain Classification**: safety domain taxonomy (general_assistant, content_moderation, autonomous_agent, safety_critical, embodied_control) with PQEA interaction rules for embodied_control domain.
* **§27.3 Command Surface Isolation**: structural constraints prohibiting generic shell execution as a tool unless explicitly enumerated, schema-bound, and interactively approved.
* **§27.4 Memory Authority Prohibition**: persistent memory content MUST NOT grant authority. Stored instructions must be re-classified, re-bound, and re-evaluated under current policy.
* **§20A Emission Discipline**: constrained artefact production to operation scope to prevent timing and telemetry leakage.
* **Annex V Authority Mutation Classification**: AI authority mutation categories and required evidence for model replacement, policy changes, and tool elevation.
* Tool Capability Profile (`pqai.tool_profile` receipt type) with deterministic parameter schemas, supervision lattice, and fail-closed PQSEC enforcement hooks.

### Changed

* Updated dependency table to require PQSEC ≥ 2.0.3 and PQSF ≥ 2.0.3.
* Updated Conformance Determination (§25) with entries for all new sections.
* Authority boundary hardened: formalised prohibition on AI self-asserted authority, permission, or execution semantics.
* Deterministic drift framework finalised: replaced float drift scoring with fixed-point representation (`drift_score_value` / `drift_score_scale`) and canonicalised drift state classification (NONE / WARNING / CRITICAL).
* Behavioural fingerprint governance expanded: probe rotation, hybrid probe sets, probe immutability constraints.
* SafePrompt strengthened: bound to session, exporter hash, consent reference, and expiry with mandatory canonical encoding and signature validation.
* Consolidated fail-closed semantics, non-authority statements, and enforcement delegation to PQSEC.

---

## BPC v1.1.0 — Bitcoin Pre Contracts

### Added

* Explicit dependency table for Epoch Clock and PQSF.
* PQ Stack compatibility note clarifying relationship to PQSEC.
* Dual-hash interoperability clarification with SEAL.
* Opaque `proofs` + `proof_schema` pattern aligned with PQSF.
* Explicit execution binding hash definition using SHAKE256-256.
* Annex J: Pre-Contract Fulfilment Proof (informative).
* Receipt integration section aligned with PQSF Annex W and PQSEC Annex AE.
* Packaging statement clarifying BPC as execution-discipline only.

### Changed

* Upgraded intent and template hashing from SHA-256 to SHAKE256-256 for PQ stack consistency.
* Replaced `LOCKED` with `FAIL_CLOSED_LOCKED` in normative preauth_result states.
* Updated time profile resolution to use PQSF profile lineage rather than hardcoded ordinal.
* Clarified monotonic time as ingress guard only, not part of deterministic evaluation.
* Strengthened fail-closed language across evaluator and execution gate.
* Updated SEAL terminology (Seal-360 → SEAL).
* v1.1.0 defines the canonical hash discipline for `version: 1` BPC objects (SHAKE256-256). Earlier draft hashing behaviour is not supported.

### Removed

* Hardcoded Epoch Clock profile requirement.
* Implicit SHA-256 execution binding language.
* Ambiguity around evaluator authority vs PQSEC authority.

---

## Neural Lock v1.1.0 — Operator State Evidence

### Added

* Explicit `ClassifierOutcome` model with strict UNAVAILABLE attestation handling rules.
* Normative Graceful Degradation integration with PQSEC ternary predicate model.
* **§4.12 Manual Duress Signal**: optional, non-authoritative manual duress path with one-way DURESS transition semantics, anti-coercion safety requirements, and rotation rules.
* **§6A Domain-Agnostic Integration** section.
* **Annex I** generic gating interface examples.
* `classifier_build_hash` requirement with manifest option for multi-component classifiers and CryptoSuiteProfile hash domain binding.
* Optional `session_id` and `intent_hash` binding fields with normative PQSEC binding validation.
* Retraining frequency governance, baseline reset controls, and operator variability accommodation rules.
* Expanded Annex E scenarios.
* Compliance Checklist (Annex K).
* Liveness and power-management requirements.

### Changed

* Operation-scoped attestation production only with rate limiting and external non-distinguishability requirements.
* ReceiptEnvelope transport alignment.

---

## ZEB v1.3.0 — Zero Exposure Broadcast

### Changed

* **Execution boundary clarified**: formalised ZET packaging statement; ZET defined as Part I of ZEB with no independent authority surface; strengthened authority boundary language.
* **§1A Canonical Scope and Limitation Disclaimer**: explicitly disclaimed censorship resistance, replacement-proof claims, and quantum immunity.
* **Replay discipline strengthened**: EnforcementOutcome structure standardised (decision vs allowed clarified); replay guard made mandatory with explicit error signalling.
* **Execution discipline formalised**: prohibited pre-approval material injection.
* **Burn semantics clarified**: mandatory burn discipline for exposure, timeout, and invalidation; persistent burned intent tracking required.
* **Bridge execution rules formalised**: lock–attest–release multi-phase rule; explicit cross-domain binding to session_id, exporter_hash, and decision_id.
* **Error codes normalised**: consolidated deterministic error signalling with explicit normative error code list.
* **Dependencies updated**: Epoch Clock minimum version increased; explicit PQSF dependency clarified for session binding.

---

## PQHR v1.0.0 — Human-Readable Policy Interface

### Added

* **§4.9 PQPS Deletion Rendering Obligation**: renderers MUST NOT display "deleted" for PQPS-managed state without validated pqps.delete_receipt. MediaDeleteReceipt alone is insufficient.
* **Annex A Rendering Threat Model and Anti-Manipulation Controls (Normative)**: adversarial rendering goals, mechanical prohibitions, environment isolation, optional RenderAttestation artefact schema with locale and build hash binding, unknown field handling discipline.
* Two mandatory fidelity levels: Summary View, Detail View.
* Optional Raw View for technical holders.
* Rendering requirements for seven artefact classes.
* Six prohibited rendering patterns.
* Five holder inspection rights.
* Rendering integrity requirements.
* Cross-specification alignment.
* Updated §9 Conformance Checklist with Annex A requirements (REQUIRED for high-assurance profiles).
* Updated dependency table to require PQSF ≥ 2.0.3, PQSEC ≥ 2.0.3, PQAI ≥ 1.2.0, PQPS ≥ 1.0.0.

---

## PQPS v1.0.0 — Post-Quantum Persistent States

### Added

* **§C.1.3.1 Verifiable Deletion Cross-Reference**: DeleteReceipt as authoritative deletion evidence, prohibition of external deletion claims without valid pqps.delete_receipt, PQHR 4.9 rendering obligations link. Introduces `E_PQPS_DELETE_UNCONFIRMED` refusal code.
* Updated dependency table to require PQSEC ≥ 2.0.3, PQSF ≥ 2.0.3, PQAI ≥ 1.2.0.
* Initial specification.

---

## PQPR v1.0.0 — Proof-of-Reference Tool

* Initial specification.
* Standalone auditing tool for verifying AI output against supplied source material.
* No changelog entries (first release).

---

## PQAA v1.0.0 — PQ Attestation Adapter

* Initial specification.
* Governed migration layer for platform-native integrity and attestation signals.
* No changelog entries (first release).

---

## PQEA v1.0.0 — Post-Quantum Embodied Agent Governance

* Initial specification.
* Deterministic, evidence-only governance for embodied autonomous agents (robots, drones, autonomous vehicles, industrial manipulators).
* Operation envelopes with cryptographic constraint maps.
* Execution leases bridging governance latency and real-time control.
* Perception sufficiency as a first-class refusal condition.
* Paper compliance without hardware capability is non-conformant.
* Normative clarification: `collection_status` is an evidence-layer diagnostic only; MUST NOT be interpreted as a validity signal or mapped to predicate truth values by evidence producers.
* No changelog entries (first release).

---

## PQ Gateway v1.0.0 — Sovereign AI Governance Layer

* Initial specification.
* Deployable governance surface composing PQSEC, PQSF, PQAI, PQPS, Epoch Clock, and PQHR into a user-facing product layer.
* No new enforcement primitives. All enforcement remains exclusively within PQSEC.
* Session-bound, tick-bounded prompt governance with intent hashing.
* Provider-agnostic routing with fail-closed enforcement boundary.
* Billing as additive refusal only — MUST NOT permit what PQSEC has denied.
* No changelog entries (first release).

---

## Funding (Non-Normative)

If you find this work useful and want to support continued development:

**Bitcoin:**
`bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw`
