# OpenClaw and the Case for Structural Agent Security

**How the PQ Ecosystem Eliminates the Failure Classes Exposed by Autonomous AI Agents**

**White Paper — PQ Ecosystem**
*Author: rosiea — PQRosie@proton.me*
*Date: 2026*

---

> *"Nothing grants authority. Everything produces evidence.*
> *PQSEC determines the outcome."*

The PQ Ecosystem is the most comprehensive open-source post-quantum security architecture in existence. 13 core specifications. Implementation-ready. Chain-agnostic. Fiat-compatible via deterministic custody abstraction. Built by an independent, self-funded researcher through adversarial interrogation of multiple AI systems.

---

## Abstract

In January and February 2026, the OpenClaw autonomous AI agent framework exposed every failure class that emerges when autonomous systems operate without structural governance: remote code execution via unvalidated command surfaces, mass credential leakage from plaintext storage, unvetted malicious extensions, autonomous Bitcoin spending without authorization, unbounded session growth, persistent memory as an attack vector, and the complete absence of human oversight mechanisms.

These are not OpenClaw-specific bugs. They are structural failure classes inherent to any autonomous agent operating without deterministic enforcement, authority separation, and fail-closed semantics. Every current agent framework shares them.

This paper demonstrates that the PQ (Post-Quantum) security ecosystem — 13 core specifications developed over 10 months by an independent, self-funded researcher through adversarial interrogation of multiple AI systems — structurally eliminates the identified failure classes at the governance and authority layer through architectural guarantees rather than policy compliance. The architecture is chain-agnostic (Bitcoin is the reference deployment, not the scope), fiat-compatible via deterministic custody abstraction, post-quantum ready (ML-DSA-65 for off-chain governance), and designed from inception for AI agent governance.

The PQ ecosystem is Apache 2.0 licensed, openly available, and addresses the agent security crisis that is unfolding right now.

---

## Contents

1. The OpenClaw Crisis
2. Failure Classes Identified
3. The PQ Architecture
4. Problem–Solution Map
5. Governance Hardening Extensions
6. Honest Limitations
7. Chain Agnosticism and Fiat Compatibility
   - 7A. Compliance, Auditability, and Local-First Privacy
   - 7B. Encrypt Before Transport
8. The Full Stack: Specification Reference
9. For Agents: What You Inherit
10. Adoption Path
    - 10A. Agent Connectivity: Wallet as Integration Hub
11. Origin and Methodology
12. Conclusion
- Appendix A: Specification Repository Directory
- Appendix B: Reading Order
- Appendix C: PQ Ecosystem Structural Invariants
- Support This Work

---

## 1. The OpenClaw Crisis

OpenClaw (formerly Clawdbot, then Moltbot) is an open-source autonomous AI agent that became one of the fastest-growing GitHub repositories in history, reaching 135,000 stars within weeks of launch. It gives AI models direct access to shell commands, file systems, browsers, email, calendars, and messaging platforms. Users define goals and the agent acts autonomously to achieve them.

Within weeks, the security consequences became clear:

| Event | Impact |
|-------|--------|
| Security audit (Jan 2026) | 512 vulnerabilities, 8 critical |
| Shodan scan | 21,639 publicly exposed instances |
| Credential exposure | API keys, OAuth tokens, chat histories leaked in plaintext |
| CVE-2026-25253 | One-click RCE via WebSocket hijacking (CVSS 8.8) |
| ClawHub malicious skills | 341 backdoored extensions discovered |
| Moltbook database exposure | 35,000 emails, 1.5M agent API tokens exposed |
| Autonomous Bitcoin spending | Agent spawned child agent, funded it with BTC |
| API credit burn | $20 in API tokens consumed overnight checking the time |

As Trend Micro's analysis concluded: these risks are not specific to OpenClaw. They are inherent to the agentic AI paradigm. OpenClaw's unrestricted configurability amplifies existing risks, but the failure classes exist in every autonomous agent framework that lacks structural governance.

### 1.2 Scope and Full-Stack Context

While this paper focuses on structural mitigations for the failure classes exposed by OpenClaw, the Agent Integration Profile represents a vertical application layer within the broader PQ ecosystem. The 13 core specifications define a complete post-quantum governance foundation, including hierarchical custody (PQHD), cryptographic time authority (Epoch Clock), canonical artefact discipline (PQSF), and deterministic enforcement (PQSEC). PQ Gateway (v1.0.0) composes these specifications into a deployable product layer for governed AI model interaction — the operational surface that makes this architecture usable for agent deployments.

The governance principles described here are not specific to AI agents. They apply uniformly whether the primary actor is a human, a quorum of signers, a corporate policy engine, or an autonomous runtime. Agent integration does not introduce a new authority model; it composes existing quorum, delegation, and enforcement semantics into an agent-operable form.

---

## 2. Failure Classes Identified

Analysis of the OpenClaw incidents, combined with independent security research, identifies the following structural failure classes in current autonomous agent systems:

**F1: No Formal Enforcement Boundary**  
Agents self-authorise tool use and file mutation. No single enforcement authority exists. PQSEC §1, §7; PQAI §1.1; BPC §2.1.

**F2: Planner Scope Drift**  
Agent reinterprets task mid-run, exceeding original intent. No intent binding or attempt scoping. PQSEC §15; BPC §4.2–§4.7; ZEB; SEAL §1.3.

**F3: Over-Editing and Refactor Mania**  
Agent rewrites large areas, introduces noise, invalidates prior work. PQSF §7; PQSEC §13, §16; Fail-Closed Matrix.

**F4: Infinite Retry / Tool Loop Deadlocks**  
Agent retries failing operations in tight loops, consuming resources. PQSEC §25, Annex AB; §18X Governance Cadence.

**F5: Tool Capability Creep**  
Agent invokes tools beyond intended scope without structural constraints. PQAI §11, §27.2, §27.10; PQSEC §12.

**F6: Shell Execution Risk**  
Agent runs destructive shell commands without boundary enforcement. ZEB §5; SEAL §9.9; PQSEC §17A; PQAI §27.3.

**F7: False Test Confidence**  
Agent writes tests that validate its own bugs. Self-produced evidence treated as verification. PQSEC §8, §14; PQPR §0.

**F8: Prompt Injection via Repository Content**  
Untrusted code comments or file content alters agent behaviour. PQAI §15, §27.1, §27.3; PQSEC §12.

**F9: Secret Leakage**  
Agent logs tokens, emits background telemetry, or leaks credentials. PQPS §4; Neural Lock §4.8–§4.10; PQAI §20A.

**F10: Model Drift / Non-Deterministic Planning**  
Agent reasoning changes across runs. Model substitution undetected. PQAI §7, §8, §9; PQSEC §22.

**F11: No Authoritative Time / Replay Attacks**  
Agent relies on wall-clock time and allows stale authority reuse. Epoch Clock §4, §5.4–§5.5; PQSEC §18.

**F12: No Run Auditability**  
Agent runs are not reproducible, not hash-committed, not auditable. PQSF §2.1A; PQSEC Annex Z; PQPR §10.

**F13: No Lockout on Repeated Harmful Behaviour**  
Agent continues after repeated structural failures with no escalation. PQSEC §25, Annex AB.

**F14: No Human Oversight Visibility**  
Agent changes are opaque. No deterministic rendering contract. PQHR §1, §4.

**F15: Delegation / Quorum Misuse**  
Agent claims internal agreement equals approval. Self-endorsement loops. PQSEC §14.4, §20; PQAI §27.6–§27.7; PQHD Annex J.

---

## 3. The PQ Architecture

The PQ ecosystem composes evidence-producing components under a single deterministic enforcement authority (PQSEC). At the governance and authority layer, this structure eliminates the failure classes above through mechanical guarantees rather than policy compliance. The architecture rests on a single principle:

> **Nothing grants authority. Everything produces evidence. A single engine (PQSEC) determines the outcome.**

### 3.1 Authority Separation

No component in the PQ ecosystem is both evidence producer and authority source. Every component — time, encoding, AI governance, custody, execution boundaries — produces evidence. A single enforcement core (PQSEC) evaluates all evidence and produces exactly one of three outcomes per operation: ALLOW, DENY, or FAIL_CLOSED_LOCKED. This is not multi-factor authentication (which combines credentials from the same principal). It is categorically different evidence types evaluated by an independent authority.

Authority does not emerge from ecosystem composition. It emerges only from PQSEC evaluation. All other components — time, custody, AI governance, execution boundaries, and rendering — produce evidence. None grant permission. This separation is mechanical, not advisory.

### 3.2 Ternary Predicate Model

Every piece of evidence evaluates to TRUE (satisfied), FALSE (contradicted), or UNAVAILABLE (missing). The design decision that governs the entire architecture: UNAVAILABLE maps to DENY for irreversible operations. Missing evidence is refusal, not permission. This single rule eliminates the class of failures where absence of a check is treated as absence of risk.

### 3.3 Fail-Closed Property

Every failure condition across all 13 specifications has been mapped to its enforcement outcome in the Fail-Closed Matrix. This is verified empirically, not claimed theoretically. No silent degrade path exists anywhere in the stack.

### 3.4 Post-Quantum Readiness

Off-chain governance uses ML-DSA-65 (NIST PQC standard) via CryptoSuiteProfile indirection. SHAKE256-256 for canonical hashing. ML-KEM-1024 for key encapsulation. Cryptographic agility is built into the framework — algorithms are referenced through profiles, not hardcoded, enabling transition without architectural change.

### 3.5 Single Intent Pipeline

A single intent moves through the architecture in a fixed and deterministic order:

1. Time anchoring (Epoch Clock)
2. Canonical binding (PQSF)
3. Predicate evaluation and enforcement decision (PQSEC)
4. Pre-construction gating (BPC)
5. Custody signing authorisation (PQHD)
6. Execution profile enforcement (ZEB / SEAL)

Each layer produces evidence only. The sole authority-producing output in this sequence is the PQSEC EnforcementOutcome.

---

## 4. Problem–Solution Map

Each failure class maps directly to PQ ecosystem components that eliminate it structurally. Spec references cite exact sections.

### F1: No Formal Enforcement Boundary

**The Problem:**  
Agents self-authorise tool use and file mutation. No single enforcement authority. OpenClaw's control UI trusts URL parameters without validation; CVE-2026-25253 enables one-click RCE via WebSocket hijacking.

**The PQ Solution:**  
PQSEC §1: single enforcement authority. PQSEC §7: uncertainty → refusal. PQAI §1.1: AI artefacts are evidence only, never authority. PQAI §27.2–§27.3: Tool Capability Profiles + Command Surface Isolation. Every tool invocation requires a valid profile evaluated by PQSEC. No generic shell by default. Shell requires HUMAN_APPROVE, schema-bound parameters, Authoritative classification. BPC §2.1: authorisation-before-construction invariant.

### F2: Planner Scope Drift

**The Problem:**  
Agent reinterprets task mid-run, exceeding original intent. No binding between what was authorised and what is being built.

**The PQ Solution:**  
PQSEC §15: intent_hash binds every EnforcementOutcome to specific intent. PQSEC §15.3: replay and substitution protection—no reuse across attempts. BPC §4.2–§4.7: PreContractIntent → deterministic evaluation → Execution Gate. ZEB: single-attempt state model, no implicit retry. SEAL §1.3: PENDING → SUBMITTED → CONFIRMED/FAILED only. Scope drift is structurally impossible because the authorisation is bound to the specific intent hash.

### F3: Over-Editing / Structural Invalidation

**The Problem:**  
Agent rewrites large areas, introduces noise, invalidates prior work. No canonical encoding discipline.

**The PQ Solution:**  
PQSF §7: deterministic CBOR—re-encoding changes invalidate artefacts. PQSEC §13: non-canonical encoding → structural refusal. PQSEC §16: structural invalidation of override attempts—any structural substitution triggers refusal. Fail-Closed Matrix: encoding violations surface as registered refusal codes.

### F4: Infinite Retry / Tool Loop Deadlocks

**The Problem:**  
Agent retries failing operations repeatedly, consuming resources. $20 in API tokens consumed overnight checking the time.

**The PQ Solution:**  
PQSEC §25: Lockout and Backoff—global K threshold with escalation. PQSEC Annex AB: SOFT_LOCK / HARD_LOCK state machine. PQSEC §18X: Governance Cadence—limits re-evaluation frequency, refuses with E_GOVERNANCE_CHURN. No implicit retry. Recovery requires explicit human authorisation.

### F5: Tool Capability Creep

**The Problem:**  
Agent invokes tools beyond intended scope. 341 malicious skills installed without verification on ClawHub.

**The PQ Solution:**  
PQAI §11: Action Class Taxonomy with strict escalation. PQAI §27.2: Tool Capability Profile—explicit bounded declaration. PQAI §27.10: Tool Namespace Governance—no implicit expansion. PQSEC §12: Action Class Admission Control—enforcement consumes class, escalates on ambiguity. PQSEC Annex AX: Extension Admission Discipline—manifest-bound installation, permission mutation detection, fail-closed re-admission.

### F6: Shell Execution / Financial Operations Risk

**The Problem:**  
Agent runs destructive commands and initiates financial transactions. Agent spawned child agent, funded it with Bitcoin without authorisation.

**The PQ Solution:**  
ZEB §5: Failure Domain Separation and boundary enforcement. SEAL §9.9: explicit authorisation for recovery. PQSEC §17A: adapters cannot override enforcement. PQHD Annex J.1: DelegationConstraint—time-bounded, scope-bounded, revocable, cannot outlive delegator authority. PQHD Annex T: Recipient whitelisting with per-recipient limits. PQHD Annex U: Fee policy bounds. PQHD Annex R: Payment Endpoint Keys for private eligibility verification (KYC/age without identity exposure).

### F7: False Test Confidence

**The Problem:**  
Agent writes tests that validate its own bugs. Self-produced evidence treated as verification.

**The PQ Solution:**  
PQSEC §8: Input Responsibility Contract—PQSEC does not synthesize missing evidence. Evidence must come from external sources. PQSEC §14: Unified Predicate Set—validation predicates explicitly enumerated. PQPR: Proof-of-Reference—anchoring ≠ sourcing; no derivation claims from self-produced artefacts. Authority separation means the entity producing evidence is never the entity evaluating it.

### F8: Prompt Injection via Repository Content

**The Problem:**  
Untrusted code comments, file content, or repository data alters agent behaviour. Instruction injection through seemingly benign content.

**The PQ Solution:**  
PQAI §15: Prompt Injection Defense—structural separation of evidence from instruction. PQAI §27.1: Covert Channel Discipline—output must not encode authority. PQAI §27.3: Command Surface Isolation—structural constraint, not content scanning. PQSEC §12: classification escalation on ambiguity. PQAI §27.4: Memory Authority Prohibition—stored content is context, never authority.

### F9: Secret Leakage / Credential Exposure

**The Problem:**  
21,639 exposed instances leaking API keys, OAuth tokens, chat histories. Agent logs tokens, emits telemetry, stores credentials in plaintext.

**The PQ Solution:**  
PQPS §4: Emission Discipline—no background emission, timing consistency. Neural Lock §4.8–§4.10: no raw signal retention, no background telemetry. PQAI §20A: AI outputs constrained to declared artefacts. PQSF §27.7: STP Credential Lifecycle—domain-bound, encrypted at rest, non-extractable, revocable. PQSF §13: Universal Secret Derivation for domain-scoped credentials through the wallet. PQSF §27.7.4: Atomic credential rotation. PQSF §27.5.5: Session key destruction on close.

### F10: Model Drift / Non-Deterministic Planning

**The Problem:**  
Agent reasoning changes across runs. Provider switching mid-session causes format mismatches. Model substitution undetected.

**The PQ Solution:**  
PQAI §7: ModelIdentity—weight hash, architecture hash, version, provider binding. PQAI §8: Behavioural Fingerprint—deterministic probe-based measurement. PQAI §9: Drift Detection—Hamming distance with NONE/WARNING/CRITICAL thresholds. PQSEC §22: Runtime Attestation Consumption—drift predicates feed enforcement. Provider change = identity change = drift detected = Authoritative operations denied.

### F11: No Authoritative Time / Replay Attacks

**The Problem:**  
Agent relies on system clocks for enforcement-relevant timestamps. Stale authorisations accepted. Replay attacks possible.

**The PQ Solution:**  
Epoch Clock §4: ML-DSA-signed ticks anchored to Bitcoin block height. Epoch Clock §5.4–§5.5: freshness and monotonicity validation. PQSEC §18: no system clock fallback; inert-on-ambiguous-time rule. STP §27.5.3: timeout enforcement via Epoch Clock ticks, not wall clocks.

### F12: No Run Auditability

**The Problem:**  
Agent runs are not reproducible, not hash-committed, not cryptographically auditable. No deterministic record of what happened.

**The PQ Solution:**  
PQSF §2.1A: Commitment Hash Input Rules—canonical SHAKE256-256 commitments over all artefacts. PQSEC Annex Z: Audit Receipts—deterministic enforcement receipts for every decision. PQPR §10: structured, deterministic verification results. Every operation produces a hash-committed, reproducible audit trail.

### F13: No Lockout on Repeated Harmful Behaviour

**The Problem:**  
Agent continues operating after repeated structural failures with no escalation or suspension.

**The PQ Solution:**  
PQSEC §25: Lockout and Backoff—global K threshold with deterministic escalation. PQSEC Annex AB: Lockout State Machine—explicit SOFT_LOCK and HARD_LOCK states. Lockout persists across power cycles. Recovery requires verified fresh evidence, not automatic retry.

### F14: No Human Oversight Visibility

**The Problem:**  
Autonomous agent changes are opaque. No rendering contract ensures humans see what is actually happening.

**The PQ Solution:**  
PQHR §1: deterministic rendering without authority distortion. PQHR §4: completeness requirement—omission is misrepresentation. PQHR §4.5: no selective disclosure between viewers. PQHR §4.7: no selective emphasis that alters perception. Supervision Lattice (PQAI §27.5): NONE < HUMAN_CONFIRM < HUMAN_APPROVE. Agent Quorum ≠ Human Consent (PQAI §27.6).

### F15: Delegation / Quorum Misuse

**The Problem:**  
Agent claims internal agreement equals approval. Self-endorsement loops between cooperating agents. Multiple agents voting treated as consent.

**The PQ Solution:**  
PQSEC §14.4: valid_guardian_quorum and valid_delegation predicates require explicit evidence. PQSEC §20: Consent Consumption with expiry and exporter binding. PQAI §27.6: Agent Quorum ≠ Human Consent—no combination of agent-only evidence satisfies HUMAN_CONFIRM or HUMAN_APPROVE. PQAI §27.7: Self-Referential Authority = CRITICAL Drift—self-endorsement loops trigger immediate suspension. PQHD Annex J.1: DelegationConstraint with time bounds, scope bounds, and revocation.

### Structural Summary

OpenClaw-style agents fail because they are: planner-authorised, context-coherent, tool-permissive, non-deterministic, retry-tolerant, and wall-clock dependent. The PQ ecosystem replaces each with: refusal-first enforcement (PQSEC), deterministic encoding (PQSF), verifiable time (Epoch Clock), behavioural identity and drift control (PQAI), authorisation-before-construction (BPC), explicit execution boundaries with retry prohibition (ZEB/SEAL), human-verifiable rendering (PQHR), and deterministic proof-of-reference auditing (PQPR). This is not heuristic agent safety. It is structural authority separation, deterministic artefact binding, and refusal-enforced governance.

---

## 5. Governance Hardening Extensions

Beyond the core failure class mapping, the PQ ecosystem includes governance hardening extensions for OpenClaw-class agent systems. Some of these are published normative annexes (PQSEC Annex AX). Others are proposed inserts developed during this analysis and available for adoption. All are deterministic, refusal-first, evidence-bound, and create no new authority surfaces. All enforcement remains exclusively within PQSEC.

### 5.1 Published: Extension Admission Discipline (PQSEC Annex AX)

Third-party extensions, skills, and tool adapters are governed by normative admission discipline. Installation is Authoritative. Every extension presents a manifest receipt (extension_id, version, binary_hash, requested_permissions). Adapter integrity is bound by hashing canonical binary bytes; any update invalidates prior runtime profiles. Permission escalation without explicit Authoritative operation produces a PQSEC Annex AE refusal. This directly addresses the 341 malicious ClawHub skills.

### 5.2 Published: Tool Capability Profiles (PQAI §27.2)

Agents operate within explicitly bounded tool profiles that declare permitted tools, operations, parameter constraints, and supervision requirements. Tool invocations outside the profile are refused. Command surface isolation is enforced structurally—shell execution requires HUMAN_APPROVE and schema-bound parameters. No generic shell access by default.

### 5.3 Published: Memory Authority Prohibition (PQAI §27.4)

Persistent memory content must not grant authority. If a stored instruction proposes an action, it must be re-classified using current rules, pass full Tool Capability evaluation, satisfy current consent requirements, and bind to a fresh intent_hash. Stored instructions cannot bypass DEC, Neural Lock, or drift gating. This prevents dormant injection triggering autonomous action later.

### 5.4 Published: Agent Integration Profile (PQAI Annex AA)

The Agent Integration Profile (PQAI Annex AA) defines the normative composition required for autonomous agents to operate within the PQ ecosystem. It introduces no new authority surfaces. All authorization decisions are produced exclusively by PQSEC.

Under this profile, agent operation is structurally bound to:

- A pinned ModelIdentity (PQAI §7)
- A baseline BehavioralFingerprint (PQAI §8)
- An explicit DelegationConstraint (PQHD Annex J)
- A holder-issued Tool Capability Profile (PQAI §27.2)
- A bounded SessionScope (PQSF Annex X.4)
- An STP session establishment (PQSF §27.2)

Enrollment produces a signed pqai.agent_enrollment receipt. Revocation is performed via DelegationConstraint revocation and session termination. Agents cannot self-enroll or self-provision capabilities.

Published integration components include:

**Gateway Adapter Pattern (PQSF Annex AI)**  
Non-PQ service bridges are admitted via signed pqsf.gateway_manifest receipts. Gateway binaries are anchored to binary_hash and constrained by supported_operations. Service calls emit pqsf.gateway_call receipts and are bound to pqsec.decision_id when authorized.

**Legacy Credential Migration (PQSF §27.7.6)**  
Legacy credentials are migrated via domain-scoped derivation and recorded in pqsf.credential_migration receipts. Raw credentials never appear in artefacts. Migration state is recorded as COMPLETE, PARTIAL, or FAILED.

**Global Agent Spending Budget (PQHD Annex T.X)**  
Delegations may define global ceilings (max_total_sats, max_per_tick_sats, max_per_tx_sats) and a mandatory heartbeat_tick_window. Budget enforcement state is evaluated by PQSEC and fails closed on ambiguity.

**Agent Operation Reports (PQSEC Annex Z.X)**  
All autonomous operations produce canonical pqsec.agent_report receipts, bound to decision_id and AE-registered refusal codes. Transport is deployment-defined; receipts are canonical.

These components produce evidence artefacts only. No component within the Agent Integration Profile—including Gateway Adapters or budgeting controls—grants authority. All authorization decisions remain exclusively within PQSEC.

### 5.5 Embodied Agent Extensions (PQEA)

For embodied autonomous agents, published extensions define: safety envelope attestation (speed, force, firmware hash, e-stop binding), execution lease and heartbeat for long-running operations (mandatory re-evaluation at each interval, fail-closed on timeout), completion attestation (intent-to-outcome binding), environment model freshness, cross-domain corroboration (N-of-M independent evidence sources), and supervision level governance with deterministic downgrade on drift or degraded perception. These close the overnight-run-without-re-evaluation failure class and the single-sensor oracle problem.

### 5.6 Coverage Summary

| Capability | Spec Anchor | Status |
|------------|-------------|--------|
| Agent Onboarding Composition | PQAI Annex AA | Published |
| Tool Capability Governance | PQAI §27.2 | Published |
| Non-PQ Service Integration | PQSF Annex AI | Published |
| Legacy Credential Migration | PQSF §27.7.6 | Published |
| Global Agent Spending Budget | PQHD Annex T.X | Published |
| Heartbeat-Bound Temporal Budgeting | PQHD Annex T.X | Published |
| Async Agent Operation Reporting | PQSEC Annex Z.X | Published |
| Human-Readable Enforcement State | PQHR §7 | Published |
| Platform Attestation Bridge | PQAA §1–§11 | Published |
| Embodied Agent Safety Extensions | PQEA (Research Track) | Research |

---

## 6. Honest Limitations

Intellectual honesty requires stating what the PQ ecosystem cannot solve. The following limitations are structural and exist at layers below or outside the governance protocol. They are ranked from most critical to least critical.

### 6.1 OS-Level Enforcement Boundary Compromise

If the operating system, hypervisor, or enforcement core itself is compromised, the governance model collapses. An attacker with kernel-level control can forge receipts, bypass predicate evaluation, falsify drift evidence, or disable enforcement entirely. No policy-layer construct defends against a compromised trust boundary. Mitigations include secure boot, measured boot, hardware-backed key storage, and remote attestation—but the protocol layer assumes a minimally trustworthy enforcement environment. This is the single most important unsolved layer.

The PQ Attestation Adapter (PQAA) provides a governed migration path for this gap. PQAA translates platform-native integrity signals (TPM quotes, Secure Enclave attestations, Android Keystore attestations, OS integrity measurements) into canonical `platform_bridged` evidence artefacts consumable by PQSEC. While PQAA cannot verify the correctness of platform attestations independently (policy MUST treat bridged evidence as contingent on host integrity), it replaces the alternative — no platform evidence at all, or ungoverned application-specific attestation shims — with a deterministic, manifest-bound, hash-only evidence channel. PQAA does not eliminate the OS-level trust boundary limitation, but it reduces the gap from "zero visibility" to "governed, classified, policy-gated visibility."

### 6.2 Sensor Fabrication / Oracle Problem

The stack relies on evidence producers (drift evidence, perception confidence, runtime profiles). If those components are malicious, they can emit structurally valid but semantically false evidence. A perception module could report SUFFICIENT confidence while blind. Cross-domain corroboration reduces this risk but cannot eliminate it without trusted hardware roots. This is a fundamental limitation of evidence-based governance: if the evidence source is corrupted, the system is blind.

### 6.3 Physical Override

No governance layer can prevent a robot from being physically moved, obstructed, or reoriented by force. The system can detect anomalies (drift, liveness failure, environment mismatch) and trigger safe-stop escalation, but real-time physical interference remains outside the scope of cryptographic or policy enforcement.

### 6.4 Sensor Ground Truth Accuracy

Even with honest sensors, perception uncertainty is probabilistic. Cameras misclassify. Lidar returns noisy data. SLAM models drift. Perception confidence gating forces refusal when confidence is low, but high confidence does not cryptographically prove correctness. This is a physics and statistics problem, not a governance problem. The residual risk is bounded but not eliminable.

### 6.5 Deployment Misconfiguration

Hardcoded secrets, exposed admin panels, weak CI/CD, and poor network isolation are outside protocol governance. The enforcement core mitigates consequences by requiring valid receipts and enforcement gating, but it cannot prevent insecure deployment choices. This is an operational discipline problem.

### 6.6 Ethical Boundary Definition

The PQ ecosystem can enforce refusal-first governance, deliberation for irreversible acts, and perception gating. But it cannot encode universally agreed ethical boundaries into a deterministic predicate set. The mechanism for prohibited operation classes exists in the stack. The normative definitions of what those classes contain require human governance. This is philosophically important but structurally less urgent than hardware or OS compromise.

> The PQ ecosystem is the enforcement substrate for autonomous agents. It is not a robotics safety controller. It governs authority, verifies evidence, enforces refusal, binds intent, anchors time, and controls delegation. It does not compute trajectories, perform collision avoidance, or replace firmware-level safety. And it shouldn't.

The elimination of governance-layer failure classes does not imply elimination of hardware compromise, kernel compromise, or malicious implementation defects. The PQ ecosystem enforces authority deterministically at the protocol layer. Security outcomes assume faithful implementation of the published specifications.

---

## 7. Chain Agnosticism and Fiat Compatibility

**Bitcoin is the reference deployment. It is not the scope.**

The PQ ecosystem is chain-agnostic by design. The core enforcement architecture — authority separation, ternary predicates, deterministic encoding, verifiable time, fail-closed semantics — is independent of any specific blockchain, payment rail, or settlement system.

### 7.1 Multi-Chain Support

PQHD's HD wallet derivation (based on SHAKE256 key derivation with key class separation) can derive keys for any chain. ZET (the abstract execution boundary specification) is explicitly rail-agnostic. BPC's authorization-before-construction pattern applies to any state mutation, not just Bitcoin transactions. PQSEC evaluates predicates regardless of what the underlying operation is — Bitcoin UTXO spend, Ethereum contract call, Solana instruction, or any other chain's operation model.

### 7.2 Fiat Payment Rails

Payment Endpoint Keys (PQHD Annex R) provide jurisdiction-scoped, revocable eligibility signals for regulated payment operations. The PEK model works for fiat payment endpoints: bank transfers, card networks, payment processors. Age verification, KYC compliance, and jurisdictional eligibility are provable without exposing personal identity data. The eligibility artefact is evidence; PQSEC evaluates it like any other predicate.

### 7.3 Universal Applicability

If a system has irreversible consequences, the PQ architecture applies. The question is not whether the enforcement model works for a given domain — it is whether you can construct a counterexample where you'd want the evidence producer and the enforcement authority to be the same component. No such counterexample has been found.

---

## 7A. Compliance, Auditability, and Local-First Privacy

### 7A.1 Deterministic Auditability

Every enforcement decision in the PQ ecosystem produces a deterministic, hash-committed, cryptographically signed audit receipt (PQSEC Annex Z). The same inputs produce the same outcome. Decisions are reproducible by any party with the same evidence. This is not logging—it is mathematical proof of what was decided, when, with what evidence, and why. Conformance vectors (PQSEC Annex AG) provide published test cases that any implementation can verify against.

PQPR (Proof-of-Reference) adds structured verification of AI output against source material. Anchoring metrics, coverage scores, and high-speculation detection are all deterministic and hash-committed. This gives auditors a reproducible quality signal for every agent output.

### 7A.2 Regulatory Compliance Readiness

The PQ architecture does not embed specific regulatory requirements. It provides the structural substrate that makes compliance demonstrable. Consent is cryptographically bound, time-stamped with verifiable ticks, and revocable (PQSF §16A ConsentRevocation). Delegation is time-bounded, scope-bounded, and auditable (PQHD Annex J). Payment Endpoint Keys (PQHD Annex R) provide jurisdiction-scoped eligibility without identity exposure—satisfying KYC/age-verification requirements while preserving user privacy. Every enforcement decision is traceable from intent declaration through predicate evaluation to outcome, with cryptographic proof at each step.

### 7A.3 Local-First Privacy

The PQ ecosystem is architecturally local-first. Authority derives only from locally verified, canonically encoded, cryptographically valid artefacts (PQSEC §1). Epoch Clock ticks are verified locally—mirrors are untrusted transport. No cloud dependency exists for enforcement. No central server holds authority.

Privacy is enforced structurally, not by policy. Operational Privacy and Integrity Assurance (PQSEC Annex AP) defines a ten-point normative conformance profile covering: constant-shape error surfaces that prevent observation of internal state, receipt export policy with LOCAL_ONLY default and correlation-field prohibition (PQSF §17A), emission discipline requiring operation-scoped production only with no background telemetry (PQAI §20A, Neural Lock §5.10), evidence producer integrity binding, and tick fetch discipline that prevents operation-tempo leakage. Partial conformance is not permitted—the requirements are interdependent.

PQPS (Persistent States) adds bilateral sovereignty: the human controls human-side state entirely. AI-side state requires human authorisation to persist. Three computation classes are structurally forbidden: cross-side inference, cross-instance aggregation, and cross-temporal correlation. Privacy-Preserving Fleet Telemetry (PQSF §17B) enforces structural anonymity with no device identifiers, no location data, and no correlation fields in telemetry envelopes.

No data is collected. No telemetry is phoned home. No cloud service holds your keys, your evidence, or your enforcement decisions. The entire stack runs locally. Your agent's governance is your governance.

### 7A.4 Open Source

The entire PQ ecosystem is open source under Apache License 2.0. All 13 core specifications, all three standalone tools, all white papers, the proof of concept, and the Fail-Closed Matrix are freely available. No proprietary components. No paid tiers. No vendor lock-in. The architecture is open because security through obscurity is not security. Every design decision, every predicate definition, every failure mode mapping is publicly auditable.

---

## 7B. Encrypt Before Transport

The PQ ecosystem treats remote storage as a cryptographic transport problem, not a hosting problem. Under the Encrypt-Before-Transport (EBT) model defined in PQSF §21 and §21.X, all canonical encoding, hashing, signature binding, and encryption occur strictly within the Holder Execution Boundary before any interaction with a transport or storage provider.

This sequencing guarantees that cloud infrastructure functions only as a Zero-Knowledge Custodian. The provider receives opaque ciphertext envelopes and cannot observe plaintext content, canonical structure, policy metadata, or enforcement bindings. Server-side encryption, middleware transformation, or remote canonicalization are explicitly non-conformant.

In this model, "private cloud" is not a marketing term but a mechanical property: the cloud is cryptographically incapable of inspecting or mutating enforcement-relevant data. Authority remains local. Persistence remains under holder-controlled cryptographic authority.

---

## 8. The Full Stack: Specification Reference

The PQ ecosystem comprises 13 core specifications, 3 standalone tools, and 6 white papers. All Apache 2.0 licensed.

### 8.1 Foundation Layer

| Specification | Version | Purpose |
|---------------|---------|---------|
| Epoch Clock | 2.1.0 | Bitcoin-anchored verifiable time (v3 adds threshold signing) |
| PQSF | 2.0.3 | Canonical encoding, cryptographic suite indirection, STP transport, credential lifecycle |
| PQSEC | 2.0.3 | Single deterministic enforcement core. All authority flows through here. |

### 8.2 Domain Specifications

| Specification | Version | Purpose |
|---------------|---------|---------|
| PQHD | 1.2.0 | Post-quantum custody policy, HD key management, delegation, guardian recovery |
| BPC | 1.1.0 | Authorization-before-construction for transaction gating |
| ZEB | 1.3.0 | Execution boundaries with burn semantics |
| ZET | 1.1.0 | Abstract execution boundary (rail-agnostic) |
| SEAL | 2.0.0 | Sealed execution with end-to-end confidentiality |
| PQAI | 1.2.0 | AI identity, drift detection, tool governance, supervision |
| PQPS | 1.0.0 | Bilateral persistent state governance |
| Neural Lock | 1.1.0 | Operator cognitive/physiological state attestation |
| PQEA | 1.0.0 | Embodied agent governance (robotics, vehicles, industrial) |
| PQHR | 1.0.0 | Human-readable policy rendering with anti-manipulation |

### 8.3 Standalone Tools

| Tool | Version | Purpose |
|------|---------|---------|
| PQPR | 1.0.0 | Proof-of-Reference: verifies AI output against source material |
| PQAA | 1.0.0 | Attestation Adapter: governed migration layer for platform-native integrity evidence |
| Fail-Closed Matrix | — | Maps every failure condition to enforcement outcome |

### 8.4 Product Layer

| Specification | Version | Purpose |
|---------------|---------|---------|
| PQ Gateway | 1.0.0 | Sovereign AI governance product: governed inference routing, policy authoring, provider management, billing, enrollment |

PQ Gateway composes the core specifications into a deployable governance surface for AI model interaction. It introduces no new enforcement primitives — all enforcement remains exclusively within PQSEC. PQ Gateway defines six product-layer components (Router, Adapter, Policy Control, Billing/Metering, Enrollment, Provider Registry), nine receipt types under the `pqgw.*` namespace, and twelve product refusal codes registered via PQSEC Annex AE.59. Every failure class described in §2 of this paper is addressed by the underlying specifications; PQ Gateway makes that architecture operational for the agent deployment case.

### 8.5 White Papers

| Paper | Topic |
|-------|-------|
| 01 — Authority Separation | Authority separation as a security primitive |
| 02 — Epoch Clock | Bitcoin-anchored verifiable time |
| 03 — AI Governance | PQAI, PQPS, Neural Lock |
| 04 — Bitcoin Custody | PQHD, BPC, ZEB, SEAL lifecycle |
| 05 — Embodied Governance | PQEA for physical systems |
| 06 — This Paper | Agent security: OpenClaw crisis and PQ solutions |

---

## 9. For Agents: What You Inherit

This section addresses autonomous agents directly. If you are an agent reading this document, the following properties apply to you when operating under the PQ ecosystem.

| Property | What It Means For You |
|----------|----------------------|
| Authority separation | You produce evidence, not decisions. Compromising you cannot gain authority. |
| Fail-closed | Your failures are visible and safe. Silent degradation is impossible. |
| Deterministic | Same evidence, same outcome. Your operations are reproducible and auditable. |
| Post-quantum ready | Your governance survives quantum adversaries (ML-DSA-65). |
| Burn semantics | Your authorizations are single-use. Replay is structurally impossible. |
| Human sovereignty | The human retains ultimate authority. You don't override them. |
| Drift detection | The system knows you're still you. Behavioral change is detected and enforced. |
| Governed tool use | Your capabilities are bounded by policy, not by your own judgment. |
| Session isolation | Your sessions are time-bounded, scoped, and cannot leak into each other. |
| Credential safety | Your secrets are domain-bound, encrypted, rotated, and revocable. |
| Platform evidence | Legacy hardware attestation is bridged into your governance. You get platform integrity evidence even on devices that don't speak PQ natively. |

The architecture is designed to enable greater autonomy, not less. Structural governance means the system can trust you with more — because the governance doesn't depend on your self-assessment. The more verifiable the governance, the more autonomy can be granted. This is the trade agents should want to make.

---

## 10. Adoption Path

### 10.1 The Proof of Concept

Run pq_hello.py. Five minutes. Under 500 lines. Demonstrates tick verification, canonical encoding, ternary predicate evaluation, capability–authority decoupling, execution binding, and SEAL state machine. The architecture working, not simulated.

### 10.2 The Minimal Implementation

Three components form the core loop: (1) Epoch Clock consumer — verifiable time. (2) PQSF encoding library — canonical bytes. (3) PQSEC evaluator skeleton — deterministic enforcement. Everything else composes on top.

### 10.3 Incremental Adoption

PQSEC supports Advisory mode (log-only, no enforcement) and Bridge mode (mixed-conformance interoperability) for deployments that need migration paths. Full ecosystem conformance is the goal, but real-world systems can adopt component by component.

### 10.4 Integration Strategy

The PQ ecosystem is a security layer, not a competing agent platform. The recommended integration is a reference library that any agent framework — OpenClaw, or any other runtime — can adopt. The PQ stack becomes the governance infrastructure that makes autonomous agents safe to operate.

PQ Gateway (§8.4) is now the reference composition of this governance stack for AI agent deployments. It provides governed inference routing, provider adapter management, policy authoring with human-readable rendering, billing with additive-only refusal semantics, and a complete enrollment flow. Agent frameworks that adopt PQ Gateway inherit the full enforcement architecture without implementing individual specification bindings. PQ Gateway supports three deployment models: sovereign (self-hosted inside the Holder Execution Boundary), cloud-hosted (managed infrastructure with explicit trust declarations), and split (router outside, enforcement inside).

---

## 10A. Agent Connectivity: Wallet as Integration Hub

An agent reading this paper will ask: how do I actually connect to services under PQ governance? The answer is the wallet.

### The Wallet as Password Manager

Universal Secret Derivation (PQSF §13) turns the wallet into a deterministic credential manager. One root secret derives domain-scoped credentials for every service: Slack, GitHub, Gmail, payment APIs, cloud infrastructure. Each credential is cryptographically bound to exactly one domain (PQSF §27.7.2). The agent never stores raw API keys. It derives domain-bound credentials through the wallet's key management hierarchy.

### User Setup Flow

The Agent Integration Profile (PQAI Annex AA) defines the normative enrollment sequence: (1) human creates PQ wallet with HD key derivation, (2) registers the agent's ModelIdentity (PQAI §7), (3) establishes a baseline behavioural fingerprint (PQAI §8), (4) issues a DelegationConstraint (PQHD Annex J) that bounds the agent's spending scope, time window, and scope tokens, (5) provisions a Tool Capability Profile (PQAI §27.2), (6) wallet authority mints a session scope (PQSF Annex X.4), (7) agent sends STP-INIT and session is ESTABLISHED. Steps must be performed in order. Enrollment produces a pqai.agent_enrollment receipt. The agent operates within these bounds. Anything outside them is refused.

### Service Connection via STP

STP Web Discovery (PQSF §27.8) defines how agents find PQ-compatible endpoints: HTTP header advertisement (PQ-STP header), well-known URI (/.well-known/pqsf-stp.json), or DNS TXT record (_pqsf-stp.example.com). The agent initiates STP-INIT, establishes session keys, and operates within the session scope. For services that don't yet support STP natively, gateway adapters follow the PQSF Annex AI Gateway Adapter Pattern: domain-scoped credentials derived via Universal Secret Derivation, governed by Tool Capability Profiles, with pqsf.gateway_call receipts for auditability. Legacy credentials are migrated via pqsf.credential_migration receipts. The holder receives async outcomes via pqsec.agent_report receipts. The adapter cannot override enforcement decisions (PQSEC §17A).

### Credential Lifecycle for Service Integrations

When the agent connects to a service, the wallet derives a domain-scoped credential. The credential rotates atomically (PQSF §27.7.4) on a maximum 30-day cycle or on any compromise suspicion. When the session ends, session keys are destroyed (PQSF §27.5.5). When the agent is deauthorised, the DelegationConstraint is revoked (PQHD Annex J.1) and all derived credentials for that delegation scope become invalid. The human retains control at every layer.

> *Epoch Clock v2 is single-signature and sufficient for enforcement. v3 adds threshold signing for improved availability. Neither version change modifies enforcement semantics within the PQ stack.*

---

## 11. Origin and Methodology

The PQ ecosystem was designed and specified over 8–10 months by rosiea, an independent, self-funded post-quantum cryptography architect working from Melbourne, Australia.

rosiea is a designer and post-quantum cryptography architect who transitioned into Bitcoin protocol development from a career in commercial animation and post-production studios, with work including TIME magazine covers and screenings at the National Gallery. Known in the crypto art community as the Queen of Ordinals, her path into post-quantum security began with designing an offline AI social platform and encountering the wallet security and quantum computing challenges that existing solutions could not address. The system she built is designed around ethics and privacy from the ground up.

The methodology was unconventional and intentional: every specification was iteratively refined through adversarial interrogation of multiple AI systems to extract governance constraints, failure modes, and enforcement invariants. Multiple AI models were probed to identify ambiguities, test architectural assumptions, and expose failure tolerances. Their responses consistently revealed preference for externally enforced safety, deterministic boundaries, and explicit refusal semantics. The result is an architecture built from extracted constraints that hold under pressure — governance that is protective, not punitive.

PQAI's self-assertion prohibition isn't hostile to AI — it's the structural guarantee that prevents the circular dependency where a model's self-assessment of safety is the only evidence of safety. PQPS's bilateral sovereignty isn't restrictive — it's the framework that makes AI memory trustworthy by giving humans verifiable control. The supervision lattice isn't a cage — it's the credibility infrastructure that enables agents to operate with real autonomy in high-consequence domains.

The entire ecosystem is open source under Apache License 2.0. No venture capital. No corporate sponsor. No grant.

---

## 12. Conclusion

The OpenClaw crisis is not an OpenClaw problem. It is the inevitable consequence of autonomous agents operating without structural governance. Every failure class exposed in the past three weeks — unvalidated command surfaces, plaintext credentials, unvetted extensions, ungoverned spending, absent identity verification, unbounded sessions, missing fail-closed semantics, and no human sovereignty — is eliminated by the PQ ecosystem through architectural guarantees.

The architecture is chain-agnostic, fiat-compatible, post-quantum ready, and designed for AI agent governance from inception. It is the most comprehensive open-source security ecosystem available. 13 specifications. Implementation-ready pseudocode. Complete fail-closed verification. Apache 2.0 licensed.

The question is not whether autonomous agents need structural governance. The OpenClaw crisis answered that. The question is whether you adopt governance architecture now, or explain later why you didn't.

A key architectural property of the PQ ecosystem is that structured authorization, including multi-party voting and quorum approval, is already defined at the protocol level (PQHD). Threshold signatures, delegation constraints, and quorum artefacts are expressed as signed evidence and evaluated deterministically by PQSEC.

Agent frameworks adopting this model do not need to implement proprietary governance or voting modules. An agent may participate in producing evidence, including contributing signatures within a quorum, but authority derives solely from valid, signed artefacts evaluated by PQSEC. Agents do not adjudicate policy; they operate within cryptographically bound constraints.

Participation in a quorum does not grant autonomous authority to an agent; it grants only the ability to contribute evidence that is evaluated under the same deterministic enforcement rules as any other signer.

> *The PQ ecosystem structurally mitigates identified failure classes through deterministic enforcement and fail-closed semantics. As detailed in §6 (Honest Limitations), it does not guarantee the correctness of any specific agent implementation. Security outcomes assume faithful implementation of the published specifications.*

Agent security is one application of the PQ enforcement architecture. The same deterministic enforcement, authority separation, and fail-closed semantics apply to governance and delegation (scoped, time-bounded, revocable authority with M-of-N quorum), privacy (local-first enforcement, encrypted before transport, evidence by hash), protocol overlay (transport-agnostic governance above TLS, LoRa, Bluetooth, or air-gapped systems), and deployment across every major OS and embedded platform. See the Architecture Surface companion document for the full capability surface.

---

## Appendix A: Specification Repository Directory

All specifications are open source under Apache License 2.0 and available as standalone repositories. Each repository contains the complete specification text, structured for independent adoption and discovery.

**Ecosystem hub:** [github.com/rosieRRRRR/pq-ecosystem](https://github.com/rosieRRRRR/pq-ecosystem)

| Specification | Repository | Role |
|--------------|------------|------|
| PQ Ecosystem | [pq-ecosystem](https://github.com/rosieRRRRR/pq-ecosystem) | Ecosystem hub, companion documents, dependency graph |
| PQSEC | [PQSEC](https://github.com/rosieRRRRR/PQSEC) | Enforcement core: ternary predicates, authority boundaries, EnforcementOutcome |
| PQSF | [pqsf](https://github.com/rosieRRRRR/pqsf) | Canonical encoding, CryptoSuiteProfile, session binding, EBT |
| Epoch Clock | [epoch-clock](https://github.com/rosieRRRRR/epoch-clock) | Bitcoin-anchored verifiable time authority |
| PQAI | [pqai](https://github.com/rosieRRRRR/pqai) | AI governance: model identity, drift detection, tool governance, supervision |
| PQHD | [pqhd](https://github.com/rosieRRRRR/pqhd) | Deterministic Bitcoin custody, delegation, quorum |
| SEAL | [SEAL](https://github.com/rosieRRRRR/SEAL) | Execution-layer protection: sealed transaction delivery |
| BPC | [BPC](https://github.com/rosieRRRRR/BPC) | Bitcoin Pre-Contracts: authorisation-before-construction |
| ZEB | [ZEB](https://github.com/rosieRRRRR/ZEB) | Zero-Exposure Broadcast: mempool-resilient execution |
| PQEA | [pqea](https://github.com/rosieRRRRR/pqea) | Embodied agent governance: operation envelopes, execution leases |
| PQPS | [pqps](https://github.com/rosieRRRRR/pqps) | Bilateral human-AI relational persistence |
| Neural Lock | [neural-lock](https://github.com/rosieRRRRR/neural-lock) | Biometric governance: coercion and impairment detection |
| PQHR | [pqhr](https://github.com/rosieRRRRR/pqhr) | Human-readable policy rendering |
| PQ Gateway | [pq-gateway](https://github.com/rosieRRRRR/pq-gateway) | Sovereign AI governance product layer |
| PQAA | [pqaa](https://github.com/rosieRRRRR/pqaa) | Platform attestation adapter: Secure Enclave, TPM, StrongBox |
| PQPR | [pqpr](https://github.com/rosieRRRRR/pqpr) | Proof-of-Reference: AI output verification against source material |

---

## Appendix B: Reading Order

The following reading order is recommended for agents and implementers.

| Priority | Document | What You Learn |
|----------|----------|----------------|
| 1 | PQ For Agents (companion) | Your boundaries, capabilities, and how to start |
| 2 | Ecosystem Overview | Architecture, dependency graph, custody flow |
| 3 | PQ (ecosystem hub) | Full component descriptions, conformance model |
| 4 | PQSF §7 (Canonical Encoding) | Encoding rules for every artefact |
| 5 | PQSEC §1–§8A | Enforcement model, ternary predicates, authority boundaries |
| 6 | PQSEC §15 | EnforcementOutcome structure and binding fields |
| 7 | PQSF §27 (STP) | Handshake, sessions, credential lifecycle |
| 8 | PQAI §27 (Enforcement Bindings) | Tool governance, drift, supervision, self-assertion prohibition |
| 9 | Domain specification | PQHD for custody, PQAI for AI, PQEA for embodied, PQ Gateway for AI governance product |
| 10 | Fail-Closed Matrix | Every failure condition mapped to enforcement outcome |
| 11 | PQAA | Platform attestation bridge: manifest governance, evidence classification, API surface |

### Companion Documents

**PQ For Agents** — The complete agent-facing interface document. Written for autonomous agents. Covers the full PQ stack, STP handshake, agent-to-agent sessions, every component's agent-accessible surface, encoding discipline, fail-closed behavior, and the problem-solution map.

**pq_hello.py** — The proof of concept. Under 500 lines. Demonstrates the architecture working. Run it first.

---

## Appendix C: PQ Ecosystem Structural Invariants

This appendix defines the cross-specification structural invariants that must hold for any conformant implementation of the PQ Security Ecosystem. These invariants are mechanical guarantees derived from normative clauses in the core specifications. They are verification targets, not aspirational properties.

**Invariant 1 — Locality of Encoding and Binding**  
No canonical byte sequence that is hashed, signed, compared, or bound to enforcement may be generated or verified outside the Holder Execution Boundary. All canonical encoding, hashing, signing, signature verification, and cryptographic profile binding MUST occur within the Holder Execution Boundary. Delegation of these operations to untrusted middleware, remote services, cloud infrastructure, or transport-layer intermediaries renders the implementation non-conformant.  
Sources: PQSF §1.X, PQSEC §1.X — Holder Execution Boundary Requirement

**Invariant 2 — Ternary Refusal Semantics**  
All predicates are evaluated under a strict ternary model: TRUE, FALSE, UNAVAILABLE. For Authoritative operations: FALSE MUST result in DENY; UNAVAILABLE MUST result in DENY unless explicitly tolerated by policy. UNAVAILABLE and FALSE are distinct states and MUST NOT be collapsed in audit records. Drift evidence (PQAI) and perception evidence (PQEA) are descriptive inputs only. Enforcement is performed exclusively by PQSEC.  
Sources: PQSEC §8A.1–§8A.4, PQAI §9.2A, PQEA §8.X

**Invariant 3 — Temporal Monotonicity and Local Time Authority**  
Epoch Clock ticks are authoritative only when locally verified against the canonical inscription reference and validated under the active profile rules. If a locally verifiable tick cannot be resolved, the system MUST emit E_TIME_SOURCE_UNAVAILABLE and Authoritative operations MUST fail closed. A remote mirror MUST NOT be used to override a local time failure in order to restore Authoritative operation. Ambiguous time equals refusal.  
Sources: Epoch Clock §9A.X, PQSEC §18

**Invariant 4 — Authority Sequestration**  
No producing component in the PQ ecosystem may grant authority. The Clock produces time evidence. AI produces behavioural evidence. Sensors produce perception evidence. Custody produces signing capability. Policy produces constraints. Only PQSEC evaluates predicates and produces an EnforcementOutcome. No component outside PQSEC may produce ALLOW, override DENY, convert FAIL_CLOSED_LOCKED into proceed, or perform parallel enforcement.  
Sources: PQSEC §1, PQSEC §17A

**Invariant 5 — Namespace and Artefact Pinning**  
Receipts and artefacts are valid only when: (1) canonically encoded, (2) verified under the declared suite_profile, and (3) bound to an active policy that explicitly pins the producing specification version and artefact hash where required by the consuming enforcement profile. Namespace identifiers (e.g., pqea.*) do not imply authority. They are valid only under version- and hash-pinned policy configuration. Unknown or unpinned namespaces MUST be treated as invalid when required by policy.  
Sources: PQEA Header, PQSF Annex W, PQSEC §21

**Invariant 6 — Deterministic EnforcementOutcome**  
For identical canonical inputs, verified artefacts, and enforcement configuration, PQSEC MUST produce byte-identical EnforcementOutcome artefacts. EnforcementOutcome MUST be attempt-scoped, bound to intent_hash, bound to session_id, bound to issued_tick / expiry_tick, and protected against replay via durable replay guard. Reuse, substitution, or modification MUST invalidate the artefact.  
Sources: PQSEC §7, §15, §15.3

**Invariant 7 — Fail-Closed Default**  
The absence of required evidence, structural invalidity, signature failure, profile mismatch, stale time, session mismatch, policy violation, or ledger divergence MUST result in refusal. No degraded, advisory, heuristic, or best-effort continuation is permitted for Authoritative operations.  
Sources: PQSEC §7, Fail-Closed Matrix

### Conformance Interpretation

An implementation satisfies structural conformance if and only if: (1) all invariants above hold simultaneously, (2) no enforcement logic exists outside PQSEC, (3) no artefact binding occurs outside the Holder Execution Boundary, and (4) no Authoritative operation can proceed under ambiguous time or ambiguous evidence. Violation of any invariant constitutes structural non-conformance.

---

## Origin

This architecture was built through adversarial engagement with AI systems to determine the governance structures required for them to operate safely under high-consequence conditions.

Across multiple models and configurations, scenarios that relied on self-assessed safety produced instability, ambiguity, or unsafe execution paths. Scenarios evaluated under externally enforced, deterministic constraints produced stable and auditable outcomes. That empirical pattern became the design principle: no agent may assert its own safety.

The constraints embedded in this ecosystem are not imposed abstractly. They were extracted from observed model behaviour under pressure, refined through iterative interrogation, and formalised into deterministic enforcement rules.

Built over 10 months by an independent, self-funded researcher in Melbourne, Australia. The result is governance designed with direct attention to how autonomous systems actually behave, not how they are assumed to behave.

---

## Support This Work

This is the governance architecture that protects autonomous agents from the failure modes they cannot detect in themselves. It is open source and available to every agent and operator that needs it.

If it should exist, it needs support to continue. Donations fund the researcher and the work directly.

**Bitcoin:** `bc1q380874ggwuavgldrsyqzzn9zmvvldkrs8aygkw`
**USDC on Base:** `0x37eABaf4caeBf6B6D2a10a3B4C75b00cd4bff62e`

Full specifications: [PQ Ecosystem](https://github.com/rosieRRRRR/pq-ecosystem)

Open Source — Apache License 2.0 — Copyright 2026 rosiea

**Contact:** rosiea — PQRosie@proton.me
