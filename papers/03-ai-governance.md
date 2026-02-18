# Externalised AI Governance: Behavioural Verification, Persistent State, and Operator Evidence

**White Paper — PQ Ecosystem**
*Author: rosiea — PQRosie@proton.me*
*Date: 2026*

---

## Abstract

AI systems cannot be trusted to self-assert safety, permission, or behavioural consistency. This paper presents an externalised AI governance architecture comprising three interconnected specifications: PQAI (behavioural verification and drift detection), PQPS (persistent relational state governance), and Neural Lock (operator state evidence).

The architecture enforces three invariants. First, AI models cannot self-classify their authority—action classification is externally verified. Second, AI systems cannot mutate persistent state without human holder authorization. Third, operator physiological state is available as predicate evidence for high-risk operations.

All governance is evidence-only. Enforcement decisions are made exclusively by PQSEC. The AI governance stack produces no authority and makes no enforcement decisions.

This paper also describes how the governance stack composes into a deployable product surface through PQ Gateway, the Agent Integration Profile (PQAI Annex AA), and the PQ Attestation Adapter (PQAA) for platform-native evidence bridging.

---

## 1. Introduction

The standard approach to AI safety relies on model alignment: training models to behave safely and hoping the training generalises. This approach is fragile. Models can be fine-tuned, quantised, substituted, or simply drift over time. Self-reported safety is circular—a compromised model reports itself as safe.

The PQ AI governance stack takes a different approach: externalised verification. Rather than trusting models to behave correctly, the architecture requires models to produce verifiable evidence of their identity, behaviour, and state, which is evaluated by an external enforcement engine.

### 1.1 Four Problems, Four Specifications

**PQAI** addresses model identity, behavioural drift, and tool governance. How do you know the model running today is the model you approved yesterday? How do you detect silent behavioural changes? How do you structurally bound what tools an agent can invoke?

**PQPS** addresses persistent relational state. When AI systems maintain memory of interactions with humans, who controls that state? Who can inspect, edit, or delete it?

**Neural Lock** addresses human operator state. When a human authorises a high-risk AI operation, are they acting freely or under coercion?

**PQAA** addresses the platform evidence gap. Hardware attestation, secure boot, and enclave measurements exist on most platforms but speak protocols the enforcement layer cannot consume directly. How do you bridge this evidence into structured governance?

### 1.2 Shared Principles

All specifications share three principles: evidence-only (no specification grants authority), fail-closed (missing evidence results in refusal for Authoritative operations), and human sovereignty (the human retains ultimate control).

---

## 2. PQAI: Model Identity, Behavioural Verification, and Agent Governance

### 2.1 Model Identity Binding

PQAI binds AI model identity to cryptographic artefacts. A ModelIdentity contains the model's weights hash, architecture hash, version, and provider, signed under the deployment's key. This creates a verifiable assertion: "the model responding to queries is the model with these exact weights."

### 2.2 Behavioural Fingerprinting

Static identity is insufficient—a model with correct weights could still behave unexpectedly due to runtime conditions. PQAI addresses this through behavioural fingerprinting: the model is evaluated against a canonical probe set, responses are hashed, and the resulting fingerprint represents the model's observable behaviour.

Fingerprinting requires deterministic inference (temperature=0 or equivalent). The inference configuration must be cryptographically bound to the fingerprint artefact, not merely recorded externally. For models where deterministic inference is unachievable, a statistical fingerprinting strategy with majority-vote response selection is defined, with the fallback of classifying fingerprint stability as UNAVAILABLE (which fails closed).

### 2.3 Drift Detection

Drift is measured as the Hamming distance between the current fingerprint and a baseline. Drift is classified as NONE (below warning threshold), WARNING (above warning, below critical), or CRITICAL (above critical threshold). Drift classification is represented using fixed-point arithmetic—no floating-point values appear in any PQAI artefact.

PQSEC maps drift states to enforcement outcomes: NONE permits all operations, WARNING denies Authoritative operations, CRITICAL denies all operations.

### 2.4 Self-Assertion Prohibition

A key PQAI invariant: models cannot self-classify their action authority. If a model claims its output is "low risk," that claim has no enforcement weight. Action classification must come from external evaluation. Self-referential authority loops (model asserts safety → PQSEC permits based on assertion → model continues) are classified as CRITICAL drift.

### 2.5 Tool Capability Governance

PQAI defines structured tool capability profiles (§27.2) that constrain which tools an AI can invoke, with what parameters, under what supervision level, and with what action class classification. Tool invocation without a matching capability profile is refused by PQSEC.

**Supervision lattice.** Every tool invocation carries a supervision requirement: NONE (autonomous), HUMAN_CONFIRM (human must acknowledge), or HUMAN_APPROVE (human must explicitly approve with full understanding). No combination of agent-only evidence satisfies HUMAN_CONFIRM or HUMAN_APPROVE. Agent quorum is not human consent.

**Command surface isolation (§27.3).** Generic shell execution is not a default capability. Shell access, if permitted at all, requires explicit enumeration in the tool capability profile, schema-bound parameters, and HUMAN_APPROVE supervision. This is a structural constraint enforced through the signed profile artefact, not content scanning.

**Memory authority prohibition (§27.4).** Persistent memory content must not grant authority. If a stored instruction proposes an action, it must be re-classified using current rules, pass full tool capability evaluation, satisfy current consent requirements, and bind to a fresh intent_hash. Stored instructions cannot bypass enforcement, drift gating, or consent requirements. This prevents dormant injection—malicious content stored in memory triggering autonomous action at a later time.

**Tool namespace governance (§27.10).** Tool identifiers follow a structured namespace with a reserved `pq.` prefix for ecosystem-defined tools and schema registry binding for deterministic parameter validation.

### 2.6 Agent Integration Profile (Annex AA)

PQAI Annex AA defines the normative composition required for an autonomous agent to operate within the PQ ecosystem. It introduces no new authority surfaces. An agent is enrolled by binding it to a pinned ModelIdentity, baseline BehavioralFingerprint, DelegationConstraint (PQHD Annex J), ToolCapabilityProfile, SessionScope (PQSF Annex X.4), and STP session. Enrollment steps must occur in order; skipping or reordering is non-conformant. Enrollment produces a `pqai.agent_enrollment` receipt. Agents cannot self-enroll or self-provision capabilities.

The Agent Integration Profile also defines DelegationConstraint scope vocabulary (AA.5), providing structured scope tokens (`custody:btc:spend`, `tool:<tool_id>:invoke`, `gateway:<service_id>:call`, etc.) that bind agent authority to deterministic, evaluable tokens rather than natural language descriptions.

---

## 3. PQPS: Persistent Relational State

### 3.1 The Problem of AI Memory

As AI systems maintain persistent memory of interactions, fundamental governance questions arise: Who owns the memory? Who can inspect it? Who can edit or delete it? Can the AI modify its own memory of you without your knowledge?

### 3.2 Bilateral State with Holder Sovereignty

PQPS defines a bilateral model. Human-side state (faceted into general context, communication preferences, intimate context, and professional context) is fully holder-controlled. AI-side state (categorised into behavioural observations, relational patterns, communication history, and capability boundaries) is proposed by the AI runtime but requires holder authorization to persist.

The human always retains sovereignty over both sides. The AI cannot mutate state autonomously. All mutation requires authorization through BPC's authorization-before-construction pattern, enforced by PQSEC.

### 3.3 Drift Control

PQPS includes drift control mechanisms for AI-side state. If the AI's observations about the human drift beyond configurable thresholds (e.g., confidence changes too rapidly, or new observations contradict anchored facts), the drift is detected and the holder is notified. Anchor contradiction—where a new AI observation directly contradicts a holder-established fact—is a hard refusal condition.

### 3.4 Forbidden Computation Classes

PQPS defines three forbidden computation classes: cross-side inference (AI must not infer human-side state from AI-side state), cross-instance aggregation (AI must not aggregate state across different human-AI relationships), and cross-temporal correlation (AI must not correlate state observations across time to build profiles the holder hasn't approved). These are enforced as PQSEC predicates.

---

## 4. Neural Lock: Operator State Evidence

### 4.1 Coercion as a Security Problem

Custody systems that rely on human authorization are vulnerable to coercion. If signing requires human approval, an adversary can coerce the human to approve. Traditional systems have no defence: the authorization looks identical whether voluntary or coerced.

### 4.2 Four-State Classification

Neural Lock produces attestations classifying operator state as NORMAL, STRESSED, DURESS, or IMPAIRED. Classification is deliberately coarse because it is risk-reduction evidence, not proof of coercion. A four-state model is robust against sensor noise while still providing meaningful signal.

### 4.3 Evidence, Not Authority

Neural Lock attestations do not determine enforcement outcomes. They provide evidence that PQSEC can use as an additional predicate. When Neural Lock evidence is unavailable (sensor failure, unconfigured deployment), the predicate evaluates as UNAVAILABLE and PQSEC applies fail-closed semantics for Authoritative operations—requiring compensating controls such as guardian approval or reduced transaction limits.

### 4.4 Anti-Habituation

Neural Lock includes anti-habituation requirements. If the system always reports NORMAL, operators habituate to the green light and stop paying attention. Emission discipline alignment prevents background emission patterns that leak timing information or create false confidence.

---

## 5. PQAA: Platform Attestation Bridge

### 5.1 The Platform Evidence Gap

Most modern devices contain hardware security elements that produce integrity evidence—TPM quotes, Secure Enclave attestations, Android Keystore attestations, OS integrity measurements. This evidence is valuable for enforcement (it can attest to boot state, enclave integrity, or key storage security) but arrives in platform-native formats that the PQ enforcement layer cannot consume directly.

Without a governed bridge, the evidence either never reaches PQSEC (making platform integrity invisible to policy) or reaches it through ungoverned application-specific shims (creating unstructured, unauditable translation paths).

### 5.2 Governed Translation

PQAA provides a governed translation layer. Platform-native attestations are translated into canonical `platform_bridged` evidence artefacts with deterministic classification, manifest-bound adapter governance, and hash-only evidence channels. The translation adapter is admitted via extension admission discipline (PQSEC Annex AX), governed by a signed manifest, and produces evidence bound to `session_id`, `decision_id`, `intent_hash`, and tick windows.

PQAA does not validate the truthfulness of platform attestations. It classifies the translation path so that PQSEC can evaluate the evidence under policy. Policy must treat bridged evidence as contingent on host integrity. The gap is reduced from "no visibility" to "governed, classified, policy-gated visibility."

---

## 6. PQ Gateway: Operational Surface for AI Governance

The AI governance specifications (PQAI, PQPS, Neural Lock) define what evidence is produced and how it is classified. PQ Gateway composes these specifications into a deployable product surface for governed AI model interaction.

### 6.1 How PQ Gateway Applies AI Governance

PQ Gateway routes inference requests to model providers through governed adapters. Each request is bound to an `intent_hash`, evaluated by PQSEC, and wrapped in a GovernedRequestEnvelope that carries the EnforcementOutcome. The provider adapter translates the canonical request into the provider's API format, normalises the response, classifies tool calls against PQAI §11 action classes, and destroys raw prompt and response content beyond the operation boundary.

Provider management includes signed, time-bounded registry snapshots with identity verification and adapter manifest governance. Policy authoring includes human-readable rendering (PQHR) before activation, monotonic versioning, and no in-place mutation.

### 6.2 Deployment Models and Trust

PQ Gateway operates in three deployment models: Sovereign (all components inside the Holder Execution Boundary—strongest guarantees), Cloud-hosted (components on managed infrastructure—holder trusts operator with prompt content during operation), and Split (PQSEC inside HEB, router/adapters outside—EnforcementOutcome is signature-bound and cannot be forged by the router).

The deployment model affects trust assumptions, not protocol semantics. AI governance rules apply identically across all models.

---

## 7. Cross-Specification Integration

The specifications compose naturally through PQSEC:

A high-risk AI operation might require: model identity verified (PQAI), drift state NONE (PQAI), SafePrompt consent bound (PQAI), tool invocation within capability profile (PQAI §27.2), supervision level satisfied (PQAI §27.5), operator state NORMAL (Neural Lock), persistent state not paused (PQPS), holder authorization for any state mutation (PQPS via BPC), platform integrity evidence acceptable (PQAA), and provider registered and verified (PQ Gateway).

Each specification produces its evidence independently. PQSEC evaluates all predicates in a single pass. No specification needs to be aware of requirements from the others.

---

## 8. Comparison to Existing Approaches

**Model cards and datasheets** document model properties statically. PQAI verifies them dynamically and continuously through fingerprinting and drift detection.

**RLHF and constitutional AI** train alignment into models. PQAI externalises verification—alignment is checked, not assumed.

**AI memory systems** (e.g., ChatGPT memory, Claude memory) provide user-facing controls but typically lack cryptographic enforcement, holder sovereignty guarantees, or formal drift control. PQPS provides all three.

**Biometric authentication** verifies identity. Neural Lock verifies state—it does not authenticate the operator but attests to their cognitive/physiological condition.

**Agent frameworks** (e.g., OpenClaw, LangChain agents) provide tool orchestration but no structural enforcement boundary. Tools are invoked based on model judgment, not signed capability profiles evaluated by an external enforcement core. The PQ architecture enforces that tool capability is declared in a signed artefact, evaluated by PQSEC, and structurally bounded—not derived from conversation context or model self-assessment.

---

## 9. Conclusion

The PQ AI governance stack demonstrates that AI safety can be architecturally enforced rather than behaviourally assumed. By externalising verification, mandating holder sovereignty over persistent state, making operator state available as predicate evidence, bridging platform-native integrity signals, and composing the stack into a deployable product surface, the architecture creates structural guarantees that survive model substitution, behavioural drift, and coercion.

All specifications produce evidence only. They grant no authority. Enforcement decisions are made exclusively by PQSEC through deterministic predicate evaluation with fail-closed semantics.

---

## References

- PQAI AI Evidence Specification v1.2.0
- PQPS Persistent State Governance v1.0.0
- Neural Lock Operator State Evidence v1.1.0
- PQAA PQ Attestation Adapter v1.0.0
- PQ Gateway v1.0.0
- PQSEC Enforcement Core v2.0.3
- PQSF Security Framework v2.0.3
- BPC Pre-Construction Gating v1.1.0 (authorization-before-construction for PQPS)
- PQHR Human-Readable Rendering v1.0.0
- Fail-Closed Matrix v1.0.0

*All specifications available at: [repository URL]*
