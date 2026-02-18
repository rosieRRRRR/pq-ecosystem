# PQ Ecosystem — Fail-Closed Matrix

**Purpose:** Every failure condition across all specifications, mapped to its enforcement outcome, producing specification, and consuming enforcement path. This document validates that no silent degrade path exists.

**Scope:** All 13 CORE specifications + SEAL (STANDALONE) + PQAA (STANDALONE) + PQEH (RESEARCH, included for completeness)

**Enforcement Authority:** All enforcement outcomes are produced exclusively by PQSEC. Domain specifications define failure conditions and refusal codes; PQSEC evaluates and enforces.

**Conformance Boundary:** The Fail-Closed Matrix is an audit artefact and does not expand normative requirements beyond component specs. It maps existing normative requirements from their source specifications into a single cross-reference view.

**Refusal Code Discipline:**
All refusal codes shown in this matrix are PQSEC Annex AE codes. Epoch Clock producing codes are mapped to Annex AE codes per PQSEC §18.4 prior to enforcement. Producing-specification internal codes MUST NOT appear in enforcement surfaces or audit artefacts.

**Outcome Key:**

**PQSEC EnforcementOutcome (strict three-value enum, §15.1):**
- **ALLOW** → Operation permitted
- **DENY** → Operation refused, may retry with corrected inputs
- **FAIL_CLOSED_LOCKED** → Operation refused, lockout state entered

**Execution State Machine Terminal (ZEB/ZET, SEAL, BPC execution phase only — not a PQSEC decision):**
- **FAILED** → Execution state terminal, explicit authorization required for recovery. This is an execution-layer state, not a PQSEC EnforcementOutcome. "Explicit authorization" means a fresh PQSEC ALLOW for a recovery-class operation (or a fresh intent/outcome in the relevant execution profile). Automatic retry, implicit resumption, and unattended recovery are prohibited.

---

## 1. PQSF — Security Framework (Foundation Layer)

PQSF defines structural validation rules. Failures here prevent artefacts from being accepted by any consuming specification.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Non-canonical CBOR encoding | `E_ENCODING_NONCANONICAL` | DENY | Yes | Re-encode correctly |
| Floating-point value in canonical artefact | `E_ENCODING_NONCANONICAL` | DENY | Yes | Use fixed-point |
| Indefinite-length CBOR items | `E_ENCODING_NONCANONICAL` | DENY | Yes | Use definite-length |
| Duplicate map keys | `E_ENCODING_NONCANONICAL` | DENY | No | Structural corruption |
| Non-bytewise-lexicographic map key order | `E_ENCODING_NONCANONICAL` | DENY | Yes | Re-sort keys |
| Unsupported hash algorithm | `E_HASH_ALG_UNSUPPORTED` | DENY | No | Algorithm not available |
| Profile in SUNSET_FINAL state | `E_PROFILE_SUNSET_FINAL` | DENY | No | Must migrate to successor |
| Schema version outside deployment bounds | `E_SCHEMA_VERSION_UNSUPPORTED` | DENY | No | Version incompatible |
| Schema version downgrade within session | `E_SCHEMA_DOWNGRADE_ATTEMPT` | DENY | No | Ratchet violation |
| Evidence descriptor required but absent | `E_EVIDENCE_DESCRIPTOR_REQUIRED` | DENY | Yes | Supply descriptor |
| Receipt body duplicates envelope fields | `E_RECEIPT_BODY_DUPLICATES_ENVELOPE` | DENY | No | Structural error |
| Receipt field mismatch | `E_RECEIPT_FIELD_MISMATCH` | DENY | No | Integrity failure |
| Checkpoint invalid | `E_CHECKPOINT_INVALID` | DENY | No | |
| STP capability mismatch | `E_CAPABILITY_MISMATCH` | DENY | Yes | Renegotiate |
| STP channel binding mismatch | `E_CHANNEL_BINDING_MISMATCH` | DENY | No | Session terminated, key material destroyed |
| STP PQ KEM confirm failed | `E_PQ_KEM_CONFIRM_FAILED` | DENY | No | Session terminated |
| STP PQ channel required but unavailable | `E_PQ_CHANNEL_REQUIRED` | DENY | No | Partial key material destroyed |
| STP resume on error-terminated session | `E_RESUME_FORBIDDEN` | DENY | No | Must establish new session |
| STP unknown payload type | `E_UNKNOWN_PAYLOAD_TYPE` | DENY | Yes | |
| STP sequence violation | (reject) | DENY | No | Replay or reorder attack |
| STP invalid MAC | (reject) | DENY | No | Integrity failure |
| STP credential revoked | `E_CREDENTIAL_REVOKED` | DENY | No | Credential lifecycle |
| Session scope issuer invalid | `E_SESSION_SCOPE_ISSUER_INVALID` | DENY | No | |
| Session scope expired | `E_SESSION_SCOPE_EXPIRED` | DENY | Yes | Renew scope |
| Session fixation detected | `E_SESSION_FIXATION_DETECTED` | DENY | No | Security violation |
| Role policy violation | `E_ROLE_POLICY_VIOLATION` | DENY | No | |
| Agent capabilities missing | `E_AGENT_CAPABILITIES_REQUIRED` | DENY | Yes | Supply capabilities |
| Delegation invalid | `E_DELEGATION_INVALID` | DENY | No | |
| Message counter invalid | `E_MESSAGE_COUNTER_INVALID` | DENY | No | Replay/reorder |
| KeyMail structure invalid | `E_KEYMAIL_STRUCTURE_INVALID` | DENY | No | |
| KeyMail encoding non-canonical | `E_KEYMAIL_ENCODING_NONCANONICAL` | DENY | No | |
| KeyMail signature invalid | `E_KEYMAIL_SIGNATURE_INVALID` | DENY | No | |
| KeyMail expired | `E_KEYMAIL_EXPIRED` | DENY | No | |
| KeyMail future tick | `E_KEYMAIL_FUTURE` | DENY | No | |
| KeyMail session mismatch | `E_KEYMAIL_SESSION_MISMATCH` | DENY | No | |
| KeyMail decryption failed | `E_KEYMAIL_DECRYPTION_FAILED` | DENY | No | |
| KeyMail sender unknown | `E_KEYMAIL_SENDER_UNKNOWN` | DENY | No | |
| GatewayManifest signature invalid | `E_SIG_INVALID` | DENY | Yes | Admission fails; gateway unusable |
| GatewayManifest binary_hash mismatch | `E_HASH_MISMATCH` | DENY | Yes | Detected as tampered extension |
| Gateway operation not in manifest | `E_POLICY_CONSTRAINT_FAILED` | DENY | Yes | Operation outside permitted scope |
| Credential migration state FAILED | `E_POLICY_CONSTRAINT_FAILED` | DENY | Yes | Refuse ops requiring the credential |

---

## 2. Epoch Clock — Time Authority

Epoch Clock failures prevent time-dependent predicates from being satisfied. All consuming specs that bind to time (which is all of them) fail closed when time is unavailable.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Tick structure malformed | `E_TICK_INVALID` | DENY | No | |
| Tick signature verification failed | `E_TICK_SIG_INVALID` | DENY | No | |
| Tick beyond reuse window | `E_TICK_STALE` | DENY | Yes | Fetch fresh tick |
| Tick rollback (non-monotonic) | `E_TICK_ROLLBACK` | DENY | No | Attack or corruption |
| Tick profile_ref mismatch | `E_TICK_PROFILE_MISMATCH` | DENY | No | Wrong profile |
| Profile structure invalid | `E_TICK_PROFILE_MISMATCH` | DENY | No | |
| Profile hash_pq mismatch | `E_HASH_MISMATCH` | DENY | No | Tampered profile |
| Profile signature invalid | `E_SIG_INVALID` | DENY | No | |
| Mirror divergence | `E_MIRROR_DIVERGENCE` | DENY | Yes | Retry with different mirrors |
| Insufficient mirrors reachable | `E_MIRROR_UNAVAILABLE` | DENY | Yes | Network connectivity |
| JCS canonical encoding mismatch | `E_CANONICAL_MISMATCH` | DENY | No | |
| v3 tick signatures below threshold | `E_TICK_SIG_THRESHOLD_UNMET` | DENY | Yes | Collect more signatures |
| v3 profile schema incomplete | `E_PROFILE_SCHEMA_INCOMPLETE` | DENY | No | |
| Profile version unrecognised | `E_PROFILE_VERSION_UNSUPPORTED` | DENY | No | |
| Mirror state FAILED | (internal) | No ticks served | Yes | Operator restart → INIT |
| Mirror state STALE exceeds max window | (FAILED transition) | No ticks served | Yes | Operator restart |
| Epoch Clock unavailable (PQSEC mapping) | `E_TIME_SOURCE_UNAVAILABLE` | DENY | Yes | Restore connectivity |

---

## 3. PQSEC — Enforcement Core

PQSEC is the sole enforcement authority. Its failure conditions are the terminal enforcement outcomes.

### 3A. Core Predicate Failures

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| valid_structure = FALSE | `E_STRUCTURE_INVALID` | DENY | Yes | Fix artefact |
| valid_tick = FALSE | `E_TICK_INVALID` | DENY | Yes | Supply valid tick |
| valid_session = FALSE | `E_SESSION_MISMATCH` | DENY | Yes | Rebind session |
| valid_consent = FALSE | `E_CONSENT_INVALID` | DENY | Yes | Supply valid consent |
| valid_policy = FALSE | `E_POLICY_CONSTRAINT_FAILED` | DENY | No | Policy violation |
| valid_runtime = FALSE | (domain-specific) | DENY | Yes | Supply attestation |
| valid_drift = FALSE (WARNING, Authoritative) | `E_RUNTIME_DRIFT_WARNING` | DENY | Yes | Drift may recover |
| valid_drift = FALSE (CRITICAL) | `E_RUNTIME_DRIFT_CRITICAL` | DENY | No | Model replacement needed |
| Any required predicate = UNAVAILABLE (Authoritative) | (predicate-specific) | DENY | Yes | Supply missing evidence |
| Any required predicate = UNAVAILABLE (Non-Auth, no policy tolerance) | (predicate-specific) | DENY | Yes | Supply missing evidence |
| Exporter hash mismatch | `E_EXPORTER_MISMATCH` | DENY | No | Session integrity |
| Policy rollback detected | `E_POLICY_ROLLBACK` | DENY | No | Attack or misconfiguration |
| Consent replay detected | `E_CONSENT_REPLAY_DETECTED` | DENY | No | |
| Replay detected (general) | `E_REPLAY_DETECTED` | DENY | No | |
| Replay guard unavailable | `E_REPLAY_GUARD_UNAVAILABLE` | DENY | Yes | Restore replay state |
| Nonce required but missing | `E_NONCE_REQUIRED` | DENY | Yes | Supply nonce |
| Operation class missing | `E_OP_CLASS_MISSING` | DENY | Yes | Declare op_class |

### 3B. Lockout and Security State (AE.39)

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Global lockout active | `E_LOCKOUT` | FAIL_CLOSED_LOCKED | Yes | Lockout recovery required |
| Authority temporarily locked | `E_LOCKED` | DENY | Yes | SOFT_LOCK recovery |
| Authority frozen | `E_FROZEN` | FAIL_CLOSED_LOCKED | No | Recovery required |
| Permanent lock | `E_PERMANENT_LOCK` | FAIL_CLOSED_LOCKED | No | Irreversible |
| Recovery required | `E_RECOVERY_REQUIRED` | DENY | Yes | Complete recovery |
| Dependency missing | `E_UNAVAILABLE` | DENY | Yes | Supply dependency |

### 3B.1 Custody and Recovery Operational Codes (AE.40)

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Safe mode active (custody workflows) | `E_SAFE_MODE_ACTIVE` | DENY | Yes | Registry-only (AE.40); surfaced by implementations performing custody workflows; PQHD does not define the triggering conditions. |
| Guardian quorum insufficient (custody workflows) | `E_GUARDIAN_QUORUM_INSUFFICIENT` | DENY | Yes | Registry-only (AE.40); surfaced by implementations performing custody workflows; PQHD does not define the triggering conditions. |
| Delegation required (custody workflows) | `E_DELEGATION_REQUIRED` | DENY | Yes | Registry-only (AE.40); surfaced by implementations performing custody workflows; PQHD does not define the triggering conditions. |

### 3C. Policy and Profile Governance

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Policy stale (warn window) | POLICY_STALE_WARN | DENY (Authoritative) | Yes | Refresh policy; maps to SOFT_LOCK |
| Policy stale (lock window) | POLICY_STALE_LOCK | FAIL_CLOSED_LOCKED | Yes | Refresh policy; maps to HARD_LOCK |
| Governance churn (excessive recheck) | `E_GOVERNANCE_CHURN` | DENY | Yes | Wait for cadence interval |
| Policy profile invalid | `E_POLICY_PROFILE_INVALID` | DENY | No | |
| Policy profile issuer not pinned | `E_POLICY_PROFILE_ISSUER_NOT_PINNED` | DENY | No | |
| Policy profile version downgrade | `E_POLICY_PROFILE_VERSION_DOWNGRADE` | DENY | No | |
| Policy profile equivocation | `E_POLICY_PROFILE_EQUIVOCATION_DETECTED` | DENY | No | Same version, different hash |
| Policy dependency invalid | `E_POLICY_DEPENDENCY_INVALID` | DENY | No | |
| Policy downgrade prohibited | `E_POLICY_DOWNGRADE_PROHIBITED` | DENY | No | Would weaken security |
| Profile capability insufficient | `E_PROFILE_CAPABILITY_INSUFFICIENT` | DENY | No | |

### 3D. Evidence Governance

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Evidence not independent | `E_EVIDENCE_NOT_INDEPENDENT` | DENY | Yes | Supply diverse evidence |
| Evidence descriptor required but absent | `E_EVIDENCE_DESCRIPTOR_REQUIRED` | DENY | Yes | Add descriptor |
| Aggregation scope required | `E_AGGREGATION_SCOPE_REQUIRED` | DENY | Yes | Supply scope artefact |

### 3E. Session and Transport

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Session scope missing | `E_SESSION_SCOPE_MISSING` | DENY | Yes | Establish scope |
| Session scope invalid | `E_SESSION_SCOPE_INVALID` | DENY | No | |
| Multi-agent boundary violation | `E_MULTI_AGENT_BOUNDARY_VIOLATION` | DENY | No | |
| Resumption evidence invalid | `E_RESUMPTION_EVIDENCE_INVALID` | DENY | No | |
| Resumption evidence expired | `E_RESUMPTION_EVIDENCE_EXPIRED` | DENY | Yes | Re-establish session |
| Resumption exporter mismatch | `E_RESUMPTION_EXPORTER_MISMATCH` | DENY | No | |
| Resumption policy changed | `E_RESUMPTION_POLICY_CHANGED` | DENY | No | Re-establish session |

### 3F. Transcript and Delegation

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Transcript binding missing (required) | `E_TRANSCRIPT_BINDING_MISSING` | DENY | Yes | Supply binding |
| Transcript binding invalid | `E_TRANSCRIPT_BINDING_INVALID` | DENY | No | |
| Transcript binding required | `E_TRANSCRIPT_BINDING_REQUIRED` | DENY | Yes | Supply binding |
| Delegation chain violation | `E_DELEGATION_CHAIN_VIOLATION` | DENY | No | |
| Self-authority prohibited | `E_SELF_AUTHORITY_PROHIBITED` | DENY | No | |
| Deferred authority prohibited | `E_DEFERRED_AUTHORITY_PROHIBITED` | DENY | No | |
| Social authority prohibited | `E_SOCIAL_AUTHORITY_PROHIBITED` | DENY | No | |

### 3G. Tool and AI Governance

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Tool profile missing | `E_TOOL_PROFILE_MISSING` | DENY | Yes | Supply profile |
| Tool profile invalid | `E_TOOL_PROFILE_INVALID` | DENY | No | |
| Tool capability violation | `E_TOOL_CAPABILITY_VIOLATION` | DENY | No | |
| Tool prohibited by policy | `E_TOOL_PROHIBITED_BY_POLICY` | DENY | No | |
| Tool schema unsupported | `E_TOOL_SCHEMA_UNSUPPORTED` | DENY | No | |
| Parameter constraints invalid | `E_PARAM_CONSTRAINTS_INVALID` | DENY | No | |
| Supervision required | `E_SUPERVISION_REQUIRED` | DENY | Yes | Obtain consent |
| Consent scope mismatch | `E_CONSENT_SCOPE_MISMATCH` | DENY | No | |

### 3H. Diagnostic and Simulation (Annex AH)

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Unsupported execution class | `E_UNSUPPORTED_EXECUTION_CLASS` | DENY | No | |
| Simulation receipt invalid | `E_SIMULATION_RECEIPT_INVALID` | DENY | No | |
| Simulation context mismatch | `E_SIMULATION_CONTEXT_MISMATCH` | DENY | No | |
| Simulation stale | `E_SIMULATION_STALE` | DENY | Yes | Re-simulate |
| Observation receipt invalid | `E_OBSERVATION_RECEIPT_INVALID` | DENY | No | |
| Observation stale | `E_OBSERVATION_STALE` | DENY | Yes | Re-observe |
| Override audit missing | `E_OVERRIDE_AUDIT_MISSING` | DENY | No | |
| Approval stability violated | `E_APPROVAL_STABILITY_VIOLATED` | DENY | No | |

---

## 4. PQHD — Custody Policy

PQHD defines custody failure conditions. All enforcement is performed by PQSEC.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Signing without EnforcementOutcome | (refuse) | DENY | Yes | Obtain outcome |
| EnforcementOutcome expired | `E_OUTCOME_EXPIRED` | DENY | Yes | Request fresh outcome |
| EnforcementOutcome session mismatch | `E_SESSION_MISMATCH` | DENY | No | |
| EnforcementOutcome replayed | `E_OUTCOME_REPLAYED` | DENY | No | |
| PSBT modified since commitment | `E_PSBT_INTEGRITY_VIOLATION` | DENY | No | |
| PSBT metadata tampered | `E_PSBT_METADATA_TAMPERED` | DENY | No | |
| Address reuse detected (override available) | `E_ADDRESS_REUSE_DETECTED` | DENY | Yes | Override or new address |
| Address reuse detected (quantum mode, no override) | `E_ADDRESS_REUSE_PROHIBITED` | DENY | No | |
| Recipient not allowlisted | `E_RECIPIENT_NOT_ALLOWLISTED` | DENY | Yes | Add to allowlist |
| Recipient limit exceeded | `E_RECIPIENT_LIMIT_EXCEEDED` | DENY | No | |
| Recipient supervision required | `E_RECIPIENT_SUPERVISION_REQUIRED` | DENY | Yes | Obtain supervision |
| Fee policy violation | `E_FEE_POLICY_VIOLATION` | DENY | Yes | Adjust fee |
| Change output invalid | `E_CHANGE_OUTPUT_INVALID` | DENY | No | |
| Output manifest mismatch | `E_OUTPUT_MANIFEST_MISMATCH` | DENY | No | |
| RBF prohibited | `E_RBF_PROHIBITED` | DENY | No | |
| Session resumption invalid | `E_SESSION_RESUMPTION_INVALID` | DENY | No | |
| Dormant UTXO selection denied | `E_DORMANT_UTXO_SELECTION_DENIED` | DENY | Yes | Obtain approval |
| Restricted UTXO recipient mismatch | `E_RESTRICTED_UTXO_RECIPIENT_MISMATCH` | DENY | No | |
| Quarantine UTXO mixing | `E_QUARANTINE_UTXO_MIXING_PROHIBITED` | DENY | No | |
| Consolidation approval required | `E_CONSOLIDATION_APPROVAL_REQUIRED` | DENY | Yes | Obtain approval |
| Display manifest missing | `E_DISPLAY_MANIFEST_MISSING` | DENY | Yes | Supply manifest |
| Display manifest hash mismatch | `E_DISPLAY_MANIFEST_HASH_MISMATCH` | DENY | No | |
| UI approval not bound | `E_UI_APPROVAL_NOT_BOUND` | DENY | No | |
| UI approval expired | `E_UI_APPROVAL_EXPIRED` | DENY | Yes | Re-approve |
| UI render unverifiable | `E_UI_RENDER_UNVERIFIABLE` | DENY | No | |
| Audit log compromised | `E_AUDIT_LOG_COMPROMISED` | DENY | No | |
| Authority frozen | `E_AUTHORITY_FROZEN` | FAIL_CLOSED_LOCKED | No | Recovery required |
| Freeze recovery required | `E_FREEZE_RECOVERY_REQUIRED` | DENY | Yes | Complete recovery |
| Freeze token invalid | `E_FREEZE_TOKEN_INVALID` | DENY | No | |
| Transcript binding missing | `E_TRANSCRIPT_BINDING_MISSING` | DENY | Yes | Supply binding |
| Transcript binding invalid | `E_TRANSCRIPT_BINDING_INVALID` | DENY | No | |
| Recovery too early | `E_RECOVERY_TOO_EARLY` | DENY | Yes | Wait for delay. Code defined in PQSEC AE.40. |
| Heartbeat tick window exceeded | `E_POLICY_CONSTRAINT_FAILED` | DENY | Yes | Stale time fails closed (refusal, not lockout by default) |
| Budget enforcement state unavailable | `E_REPLAY_GUARD_UNAVAILABLE` | DENY | Yes | No state, no spend |
| Spend exceeds tick/tx/global ceiling | `E_POLICY_CONSTRAINT_FAILED` | DENY | Yes | Standard policy refusal |

---

## 5. PQAI — AI Evidence

PQAI defines AI evidence failure conditions. All enforcement is performed by PQSEC.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Model identity validation failed | valid_model_identity = FALSE | DENY | No | |
| Fingerprint encoding non-canonical | (structure failure) | DENY | No | |
| Aggregate hash mismatch | (fingerprint validation) | DENY | No | |
| Drift state WARNING (Authoritative) | `E_RUNTIME_DRIFT_WARNING` | DENY | Yes | May recover |
| Drift state CRITICAL | `E_RUNTIME_DRIFT_CRITICAL` | DENY | No | Model replacement needed |
| SafePrompt expired | (tick validation) | DENY | Yes | Reissue |
| SafePrompt replay | (single-use) | DENY | No | |
| Action class self-asserted by model | (admission control) | DENY | No | Classification required |
| Non-deterministic model, stability UNAVAILABLE | (§8.3A) | DENY | Yes | Configure deterministic inference or use statistical fingerprinting |
| Inference config not bound to fingerprint | (§8.3A.3) | DENY | Yes | Bind config |
| Tool profile required but absent | `E_TOOL_PROFILE_MISSING` | DENY | Yes | Supply profile. Code emitted by PQSEC (§22C). |

---

## 6. BPC — Bitcoin Pre Contracts

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Tick missing | `E_TICK_MISSING` | FAIL_CLOSED_LOCKED | Yes | Supply tick |
| Tick profile mismatch | `E_TICK_PROFILE_MISMATCH` | FAIL_CLOSED_LOCKED | No | |
| Tick signature invalid | `E_TICK_SIG_INVALID` | FAIL_CLOSED_LOCKED | No | |
| Mirror divergence | `E_MIRROR_DIVERGENCE` | FAIL_CLOSED_LOCKED | Yes | Retry with different mirrors |
| Tick stale | `E_TICK_STALE` | FAIL_CLOSED_LOCKED | Yes | Fetch fresh tick |
| Intent hash mismatch | `E_INTENT_HASH_MISMATCH` | DENY | No | |
| Intent expired | `E_INTENT_EXPIRED` | DENY | Yes | Create new intent |
| Outcome expired | `E_OUTCOME_EXPIRED` | DENY | Yes | Request fresh outcome |
| Outcome replayed | `E_OUTCOME_REPLAYED` | DENY | No | |
| PSBT template mismatch | `E_PSBT_TEMPLATE_MISMATCH` | DENY | No | |
| PSBT template non-canonical | `E_PSBT_TEMPLATE_NONCANONICAL` | DENY | No | |
| Policy deny | `E_POLICY_DENY` | DENY | No | |
| Approvals missing | `E_APPROVALS_MISSING` | DENY | Yes | Collect approvals |
| Approval invalid | `E_APPROVAL_INVALID` | DENY | No | |
| Proof invalid | `E_PROOF_INVALID` | DENY | No | |
| Authorization denied | `E_AUTHORIZATION_DENIED` | DENY | No | |
| Signing failed | `E_SIGNING_FAILED` | DENY | No | |
| Broadcast failed | `E_BROADCAST_FAILED` | FAILED (execution terminal) | Yes | Retry broadcast |
| Final TX template divergence | `E_FINAL_TX_TEMPLATE_DIVERGENCE` | DENY | No | |

---

## 7. ZEB/ZET — Execution Boundary

ZEB uses an internal execution state machine with FAILED as the terminal error state.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| No EnforcementOutcome provided | `E_OUTCOME_MISSING` | DENY | Yes | Obtain outcome |
| Outcome replayed | `E_OUTCOME_REPLAYED` | DENY | No | |
| PQSEC refused authorization | `E_DENIED` | DENY | No | |
| Intent hash burned | `E_BURNED_INTENT` | DENY | No | Burned intents are permanent |
| Transaction observed in mempool (exposure) | `E_EXPOSURE_DETECTED` | FAILED (execution terminal) | No | Requires explicit authorization for recovery |
| Confirmation timeout | `E_CONFIRMATION_TIMEOUT` | FAILED (execution terminal) | Yes | Explicit authorization required for new attempt |
| Replay state lost/corrupted | `E_OUTCOME_REPLAYED` / `E_FAIL_CLOSED_LOCKED` | FAIL_CLOSED_LOCKED | Yes | Restore from backup |

---

## 8. Neural Lock — Operator State Evidence

Neural Lock produces attestation artefacts only. Failure maps to PQSEC ternary predicate model.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Attestation cannot be produced | operator_state_ok = UNAVAILABLE | DENY (Authoritative) | Yes | Sensor recovery |
| Classification: STRESSED | operator_state_ok = policy-dependent | Policy-dependent | Yes | State may normalise |
| Classification: DURESS | operator_state_ok = FALSE | DENY | Yes | Duress response activated |
| Classification: IMPAIRED | operator_state_ok = FALSE | DENY | Yes | State may recover |
| Attestation version unsupported | (reject) | DENY | No | Version incompatible |
| Attestation session binding mismatch | (reject) | DENY | No | |
| Enforcement mode, compensating controls absent | (refuse) | DENY | Yes | Obtain guardian approval or accept delays |

---

## 9. PQPS — Persistent State

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Required evidence absent | `E_PQPS_EVIDENCE_MISSING` | DENY | Yes | Supply evidence |
| Evidence expired | `E_PQPS_EXPIRED` | DENY | Yes | Refresh evidence |
| Facet/category paused | `E_PQPS_PAUSED` | DENY | Yes | Holder unpause. Predicate evaluates UNAVAILABLE. |
| Scope violation | `E_PQPS_SCOPE_VIOLATION` | DENY | No | |
| AI instance mismatch | `E_PQPS_INSTANCE_MISMATCH` | DENY | No | |
| Signature invalid | `E_PQPS_SIGNATURE_INVALID` | DENY | No | |
| Payload commitment mismatch | `E_PQPS_COMMITMENT_MISMATCH` | DENY | No | Integrity failure |
| Epoch mismatch on update | `E_PQPS_EPOCH_MISMATCH` | DENY | Yes | Sync epoch |
| AI-side connectivity stale | `E_PQPS_CONNECTIVITY_STALE` | DENY | Yes | Restore connectivity. Predicate evaluates UNAVAILABLE. |
| Mandatory review overdue | `E_PQPS_REVIEW_OVERDUE` | DENY | Yes | Complete review |
| Drift threshold triggered | `E_PQPS_DRIFT_THRESHOLD_TRIGGERED` | DENY | Yes | Holder review |
| Anchor contradiction | `E_PQPS_ANCHOR_CONTRADICTION` | DENY | No | Hard contradiction |
| Delete unconfirmed | `E_PQPS_DELETE_UNCONFIRMED` | DENY | Yes | Supply deletion receipt |
| Request replayed | `E_PQPS_REQUEST_REPLAYED` | DENY | No | |
| Transport invalid | `E_PQPS_TRANSPORT_INVALID` | DENY | No | |

---

## 10. PQEA — Embodied Agent Governance

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Envelope encoding non-canonical | `E_EMBODIED_ENCODING_NONCANONICAL` | DENY | No | |
| Intent hash mismatch | `E_EMBODIED_INTENT_HASH_MISMATCH` | DENY | No | |
| Envelope expired | `E_EMBODIED_ENVELOPE_EXPIRED` | DENY | Yes | Reissue |
| Operation schema not permitted | `E_EMBODIED_OP_SCHEMA_NOT_PERMITTED` | DENY | No | |
| Constraint schema mismatch | `E_EMBODIED_CONSTRAINT_SCHEMA_MISMATCH` | DENY | No | |
| Constraint hash mismatch | `E_EMBODIED_CONSTRAINT_HASH_MISMATCH` | DENY | No | |
| Runtime profile invalid | `E_EMBODIED_RUNTIME_PROFILE_INVALID` | DENY | No | |
| Adapter identity mismatch | `E_EMBODIED_ADAPTER_MISMATCH` | DENY | No | |
| Drift evidence invalid | `E_EMBODIED_DRIFT_EVIDENCE_INVALID` | DENY | Yes | Supply valid evidence |
| Drift state CRITICAL | `E_EMBODIED_DRIFT_CRITICAL` | DENY | No | |
| Perception insufficient | `E_EMBODIED_PERCEPTION_INSUFFICIENT` | DENY | No | Cannot override |
| Perception evidence absent | `E_EMBODIED_PERCEPTION_UNAVAILABLE` | DENY | Yes | Sensor recovery |
| Safety state FAULT or E-Stop | `E_EMBODIED_SAFETY_NOT_OK` | DENY | Yes | Clear fault |
| Execution lease invalid/expired | `E_EMBODIED_LEASE_INVALID` | DENY | Yes | Renew lease |
| Heartbeat missing | `E_EMBODIED_HEARTBEAT_MISSING` | DENY | Yes | Resume heartbeat |
| Delegation invalid | `E_EMBODIED_DELEGATION_INVALID` | DENY | No | |
| Environment model stale | `E_EMBODIED_ENV_MODEL_STALE` | DENY | Yes | Refresh model |
| Peer posture invalid | `E_EMBODIED_PEER_POSTURE_INVALID` | DENY | Yes | Peer refresh |
| Prohibited operation | `E_EMBODIED_PROHIBITED_OPERATION` | DENY | No | Unconditionally prohibited |
| Actuation domain unsupported | `E_EMBODIED_ACTUATION_DOMAIN_UNSUPPORTED` | DENY | No | |

---

## 11. SEAL — Execution-Layer Submission (STANDALONE)

SEAL operates at two distinct layers, each with its own failure vocabulary:

- **Submission Endpoint layer:** Uses `rejection_code` (SEAL §10.6.1). These are endpoint-to-wallet rejection classifications — not PQSEC decisions.
- **PQSEC enforcement layer:** Uses `E_*` codes registered in PQSEC Annex AE.44. These are PQSEC enforcement outcomes for sealed execution policy.

The execution state machine (PENDING → SUBMITTED → CONFIRMED / FAILED) governs wallet-side state transitions. FAILED is an execution terminal state, not a PQSEC decision.

### 11A. Submission Endpoint Rejection Classes (SEAL §10.6.1)

| Failure Condition | rejection_code | Wallet Response | Notes |
|---|---|---|---|
| Decryption of sealed transaction failed | `DECRYPTION_FAILED` | FAILED (execution terminal) | |
| Template hash does not match | `TEMPLATE_HASH_MISMATCH` | FAILED (execution terminal) | |
| Transaction structurally invalid | `INVALID_TRANSACTION` | FAILED (execution terminal) | |
| Replay detected at endpoint | `REPLAY_DETECTED` | FAILED (execution terminal) | |
| Encryption key expired or revoked | `KEY_EXPIRED_OR_REVOKED` | FAILED (execution terminal) | |
| Endpoint policy rejected submission | `POLICY_REJECTED` | FAILED (execution terminal) | |
| Transaction already confirmed | `ALREADY_CONFIRMED` | Wallet verifies confirmation | Not a failure if confirmation is valid |
| Transaction already in mempool | `ALREADY_IN_MEMPOOL` | FAILED (execution terminal) | Exposure detected |
| Endpoint internal error | `INTERNAL_ERROR` | FAILED (execution terminal) | |

No other rejection codes are permitted (SEAL §10.6.1).

### 11B. PQSEC Enforcement Codes for SEAL (Annex AE.44)

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Submission evidence missing when required | `E_SUBMISSION_EVIDENCE_MISSING` | DENY | No | |
| Submission evidence invalid | `E_SUBMISSION_EVIDENCE_INVALID` | DENY | No | |
| Sealed transaction observed in public mempool | `E_EXECUTION_LEAK_DETECTED` | DENY | No | Exposure is permanent |
| Sealed submission timeout (no confirmation) | `E_SEAL_TIMEOUT` | DENY | Yes | Policy-defined window |
| Sealed execution replay | `E_SEAL_REPLAY_DETECTED` | DENY | No | |

### 11C. Execution State Machine Terminals

| Failure Condition | State Transition | Recovery | Notes |
|---|---|---|---|
| Any failure or ambiguity during SUBMITTED | SUBMITTED → FAILED | Explicit authorization required | |
| Unexpected public exposure | SUBMITTED → FAILED | Explicit authorization required | |
| Reorganization after confirmation | CONFIRMED → FAILED | Explicit authorization required | |
| Observer failure, status unknown | SUBMITTED → FAILED | Explicit resolution required | |

Prohibited: automatic retry, implicit FAILED → SUBMITTED, any transition bypassing FAILED after failure.

---

## 12. PQHR — Human-Readable Policy Interface

PQHR failures are rendering obligations, not enforcement conditions. Included for completeness.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| PQPS rendering incomplete | `E_RENDER_PQPS_INCOMPLETE` | Non-conformant rendering | Yes | Fix renderer |
| Accessibility non-conformant | `E_RENDER_ACCESSIBILITY_NONCONFORMANT` | Non-conformant rendering | Yes | Fix renderer |
| Internationalisation non-conformant | `E_RENDER_I18N_NONCONFORMANT` | Non-conformant rendering | Yes | Fix renderer |

---

## 13. PQPR — Proof-of-Reference Tool (STANDALONE)

PQPR is standalone audit tooling with no enforcement failure conditions. Not included in matrix.

---

## 14. PQAA — PQ Attestation Adapter (STANDALONE)

PQAA is a migration compatibility layer that translates platform-native attestation signals into `platform_bridged` evidence artefacts. PQAA produces evidence only and does not evaluate predicates or grant authority. Failure conditions map to existing PQSEC Annex AE codes. PQAA Annex B reason codes are descriptive diagnostics only and do not constitute PQSEC refusal codes.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| PQAA manifest signature invalid | `E_SIG_INVALID` | DENY | Yes | Manifest admission fails; adapter unusable until re-signed |
| PQAA binary hash mismatch | `E_HASH_MISMATCH` | DENY | No | Adapter tampered or updated without re-admission |
| PQAA manifest expired (tick window) | `E_TICK_STALE` | DENY | Yes | Reissue manifest with valid tick window |
| PQAA source_map exceeds 16 entries | `E_POLICY_CONSTRAINT_FAILED` | DENY | No | Manifest structurally non-conformant |
| PQAA evidence from unadmitted adapter | `E_ATTESTATION_PROFILE_MISSING` | DENY | Yes | Admit adapter before use |
| PQAA request_nonce replay detected | `E_REPLAY_DETECTED` | DENY | No | Replay attack or nonce reuse |
| PQAA request tick window expired | `E_TICK_STALE` | DENY | Yes | Submit fresh request |
| PQAA source_id not in manifest | `E_POLICY_CONSTRAINT_FAILED` | DENY | No | Source not declared in admitted manifest |
| PQAA payload exceeds max_payload_bytes | `E_POLICY_CONSTRAINT_FAILED` | DENY | No | Platform artefact too large |
| PQAA claim_hash mismatch | `E_HASH_MISMATCH` | DENY | No | Evidence integrity failure |
| PQAA signing key class undeclared | `E_EVIDENCE_DESCRIPTOR_REQUIRED` | DENY | Yes | Bundle missing signing_key_class |
| PQAA evidence class not `platform_bridged` | `E_EVIDENCE_DESCRIPTOR_REQUIRED` | DENY | No | Adapter must classify as platform_bridged |
| PQAA update authority revoked | `E_SIG_INVALID` | DENY | No | All manifests under revoked key invalid |
| PQAA evidence unavailable (all sources) | (predicate UNAVAILABLE) | DENY | Yes | No platform evidence collected; fail-closed for Authoritative |
| `platform_bridged` not permitted by policy | `E_POLICY_CONSTRAINT_FAILED` | DENY | No | Policy does not admit bridged evidence for this predicate/op class |

---

## 15. PQ Gateway — Sovereign AI Governance Layer (PRODUCT)

PQ Gateway is a product-layer composition of existing PQ specifications into a deployable AI governance gateway. PQ Gateway introduces no new enforcement primitives. All enforcement remains exclusively within PQSEC. The codes below are product-layer refusal codes (PQSEC Annex AE.59), not PQSEC predicate failures. They represent operational routing and product gating decisions.

| Failure Condition | Refusal Code | Outcome | Recoverable | Notes |
|---|---|---|---|---|
| Provider or model not in registry snapshot | `E_PROVIDER_NOT_REGISTERED` | Product DENY | Yes | Register provider or wait for snapshot update |
| Provider suspended pending verification | `E_PROVIDER_SUSPENDED` | Product DENY | Yes | Provider re-verification + holder approval required |
| Registry snapshot unavailable or expired | `E_PROVIDER_DISCOVERY_UNAVAILABLE` | Product DENY | Yes | Await fresh snapshot; fail-closed for Authoritative |
| Adapter not admitted via PQSEC Annex AX | `E_ADAPTER_NOT_ADMITTED` | Product DENY | No | Admit adapter before use |
| Adapter binary hash does not match manifest | `E_ADAPTER_BINARY_MISMATCH` | Product DENY | No | Potential tampering; Lockout Contributing |
| Policy not compiled | `E_POLICY_NOT_COMPILED` | Product DENY | No | Complete policy authoring (P3) before operation |
| Policy not rendered and reviewed via PQHR | `E_POLICY_NOT_REVIEWED` | Product DENY | No | Complete PQHR review before activation |
| Enrollment sequence not complete | `E_ENROLLMENT_INCOMPLETE` | Product DENY | No | Complete all enrollment steps (P5) |
| Model target resolution failed | `E_MODEL_TARGET_AMBIGUOUS` | Product DENY | No | Specify explicit model_id or fix policy-default |
| Provider privacy classification not permitted | `E_PROVIDER_PRIVACY_MISMATCH` | Product DENY | No | Update policy to permit classification, or use different provider |
| Usage exceeds billing period allocation | `E_BILLING_QUOTA_EXCEEDED` | Product DENY | Yes | Wait for next billing period or upgrade tier |
| Request rate exceeds tier or policy limit | `E_BILLING_RATE_LIMITED` | Product DENY | Yes | Reduce request rate or upgrade tier |

All product DENY outcomes are additive: they can refuse an operation that PQSEC has allowed, but cannot permit an operation that PQSEC has denied. Product refusal codes MUST be rendered distinctly from PQSEC enforcement refusal codes (PQHR rendering discipline).

---

## Integrity Verification

### Silent Degrade Path Analysis

A silent degrade path exists when a failure condition results in continued operation without explicit denial or lockout.

**Result: No silent degrade paths found.**

Every failure condition in every specification maps to one of:
- **PQSEC EnforcementOutcome:** DENY or FAIL_CLOSED_LOCKED (strict three-value enum; ALLOW is the non-failure case)
- **Execution state machine terminal:** FAILED (ZEB/ZET, SEAL, BPC execution phase only — not a PQSEC decision, requires explicit authorization for recovery)
- **Non-conformant** (PQHR rendering — does not affect enforcement)

### UNAVAILABLE → DENY Consistency

Every specification that produces evidence consumed by PQSEC handles the UNAVAILABLE case:
- Neural Lock: operator_state_ok = UNAVAILABLE → DENY for Authoritative (PQSEC §8A.4)
- PQAI: fingerprint stability UNAVAILABLE → DENY for Authoritative (PQSEC §8A.4)
- Epoch Clock: time unavailable → `E_TIME_SOURCE_UNAVAILABLE` → DENY
- PQPS: paused facet → UNAVAILABLE → DENY for Authoritative (PQSEC §8A.4)
- PQPS: connectivity stale → UNAVAILABLE → DENY for Authoritative (PQSEC §8A.4)
- PQEA: perception unavailable → DENY regardless of operation class
- PQAA: all sources unavailable or adapter unadmitted → UNAVAILABLE → DENY for Authoritative (PQSEC §8A.4)

No specification allows UNAVAILABLE to silently proceed for Authoritative operations.

### Cross-Spec Failure Propagation

Failures propagate upward through the dependency graph:
- PQSF encoding failure → every consuming spec rejects artefact
- Epoch Clock failure → every time-bound predicate fails → DENY
- PQSEC lockout → all operations refused globally

No specification has an independent path that bypasses PQSEC for enforcement decisions.

---

*Matrix compiled from: PQSF 2.0.3, PQSEC 2.0.3, PQHD 1.2.0, Epoch Clock 2.1.0, PQAI 1.2.0, Neural Lock 1.1.0, BPC 1.1.0, ZEB 1.3.0, PQPS 1.0.0, PQEA 1.0.0, PQHR 1.0.0, PQPR 1.0.0, SEAL 2.0.0, PQAA 1.0.0, PQ Gateway 1.0.0.*
