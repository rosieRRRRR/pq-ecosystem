# Governing Embodied AI: Operation Envelopes, Execution Leases, and Physical Safety Boundaries

**White Paper — PQ Ecosystem**
*Author: rosiea — PQRosie@proton.me*
*Date: 2026*

---

## Abstract

Embodied AI systems—robotics, autonomous vehicles, industrial automation—introduce governance challenges absent in software-only systems. Physical actions are irreversible. Actuation latency conflicts with governance-layer evaluation time. Sensor failure creates perception gaps that software systems never face.

This paper presents PQEA (Post-Quantum Embodied Agent governance), a specification that extends the PQ enforcement architecture to physical systems. PQEA introduces operation envelopes (cryptographically signed descriptions of intended physical actions), execution leases (time-bound governance authorizations with heartbeat re-evaluation), and perception sufficiency as a first-class refusal condition.

The specification enforces a strict separation between the governance layer (PQSEC predicate evaluation) and the real-time control layer (adapter-managed servo loops). Paper compliance without hardware capability is explicitly non-conformant.

---

## 1. Introduction

Existing AI governance frameworks assume software-only systems. They govern model outputs—text, classifications, tool invocations—where the cost of refusal is delay, not physical consequence. Embodied systems break this assumption. A refused robot command may leave a physical process in an unsafe state. A governance-layer timeout may cause a servo loop to lose control.

PQEA addresses the unique challenges of governing AI systems that interact with the physical world, while preserving the PQ ecosystem's core properties: evidence-only governance, fail-closed enforcement, and single enforcement authority through PQSEC.

### 1.1 Design Constraints

PQEA operates under three constraints not present in software governance. First, the hardware reality constraint: governance must account for physical sensor capabilities, actuator limitations, and environmental conditions. Second, the real-time separation constraint: governance-layer predicate evaluation cannot run at servo-loop frequency. Third, the irreversibility constraint: physical actions cannot be undone.

---

## 2. Operation Envelopes

### 2.1 Structure

An operation envelope is a cryptographically signed description of an intended physical action. It contains the operation schema (what type of action), a constraint map (bounds on parameters like force, velocity, position), intent hash (binding to the specific operation), and temporal bounds (issued_tick, expiry_tick).

The constraint map defines maximum allowable values for each parameter. An operation that exceeds any constraint is refused. This provides deterministic bounds on physical actions before they occur.

### 2.2 Schema Allowlisting

Each deployment defines a runtime profile containing an operation schema allowlist. Only operations whose `op_schema` appears in the allowlist may be evaluated. Unknown operation types are refused with `E_EMBODIED_OP_SCHEMA_NOT_PERMITTED`. This prevents capability escalation: an embodied agent cannot perform operations not anticipated by the deployment's safety analysis.

---

## 3. Execution Leases

### 3.1 The Governance-Control Boundary

PQSEC cannot evaluate predicates at servo-loop frequency (sub-millisecond). Physical control loops cannot wait for governance-layer authorization on every actuation command. PQEA resolves this through execution leases: time-bound authorizations that permit the adapter to manage real-time control within governance-defined bounds.

A lease grants the adapter permission to execute operations matching the lease's scope for a bounded duration. The adapter is responsible for real-time safety within lease bounds. PQSEC re-evaluates predicates at lease renewal (heartbeat).

### 3.2 Heartbeat Re-evaluation

Leases require periodic heartbeat messages from the adapter. Each heartbeat must carry a strictly increasing sequence number and a valid issued_tick. PQSEC re-evaluates predicates at each heartbeat. If predicates are no longer satisfied (e.g., drift state has changed, perception has degraded, safety state has faulted), the lease is not renewed and the adapter must cease governed operations.

Missing heartbeats trigger refusal (`E_EMBODIED_HEARTBEAT_MISSING`). The adapter must implement safe-state transition procedures for lease expiry, independent of governance-layer communication.

### 3.3 Lease Expiry During Motion

A critical edge case: a lease expires while the adapter is mid-physical-operation in a non-interruptible state (e.g., a robotic arm mid-grasp, a vehicle mid-lane-change). PQEA requires the adapter to implement safe completion or safe abort procedures for this scenario. The governance layer does not dictate real-time safety responses; it requires the adapter to have them.

---

## 4. Perception Sufficiency

### 4.1 Refusal Condition

PQEA treats perception sufficiency as a first-class refusal condition. Existing robotics frameworks treat perception uncertainty as a planner input—the planner decides how to act given uncertain perception. PQEA makes a stronger claim: if perception is insufficient for safe operation, the operation is refused before it reaches the planner.

Perception sufficiency is classified as SUFFICIENT, DEGRADED, or INSUFFICIENT. INSUFFICIENT is a hard refusal regardless of supervision level. There is no override for inadequate perception.

### 4.2 Evidence

Perception evidence includes sensor availability, measurement quality, and environmental model freshness. Stale or absent environment model evidence triggers `E_EMBODIED_ENV_MODEL_STALE`. The classification is evidence; PQSEC makes the enforcement decision.

---

## 5. Safety State

PQEA defines safety state evidence including e-stop status, fault conditions, and safety profile satisfaction. When safety state is FAULT or e-stop is active, operations are refused with `E_EMBODIED_SAFETY_NOT_OK`.

Safety profiles define minimum safety requirements for classes of operations. A deployment may define different profiles for different operation types (e.g., high-speed movement requires higher safety margins than stationary manipulation).

---

## 6. Delegation

PQEA supports bounded delegation for multi-agent coordination. A delegating agent can grant a receiving agent permission to execute operations within a defined scope. Delegations are bounded by maximum uses, scope restrictions, and expiry. The delegation receipt is cryptographically signed and verified by PQSEC.

If the uses counter state is lost or corrupted, the delegation fails closed for Authoritative operations. There is no "assume unused" fallback.

---

## 7. Hardware Reality Clause

PQEA §1.4 states: "paper compliance without hardware capability is non-conformant." A system cannot claim PQEA conformance if its hardware cannot actually perform the sensing, actuation, or safety functions the specification requires. This is unusual for a specification—most define logical requirements without addressing physical capability. PQEA's position is that a governance specification for physical systems must acknowledge physical reality.

---

## 8. Platform Attestation for Embodied Systems

Embodied systems commonly include hardware security elements—TPM modules on industrial controllers, Secure Enclaves on mobile robotic platforms, hardware-backed keystores on edge devices. These elements produce integrity evidence (boot state, firmware measurement, key storage attestation) that is directly relevant to governance: a robot whose firmware has been tampered with should not be trusted to execute safety-critical operations.

PQAA bridges platform-native attestations into canonical `platform_bridged` evidence that PQSEC can evaluate alongside perception, safety, drift, and operator state evidence. For embodied deployments, PQAA enables policy such as: "refuse Authoritative operations if secure boot attestation is missing or stale" or "require fresh TPM quote before lease renewal for safety-critical operation classes."

PQAA does not validate the truthfulness of platform attestations—it governs the translation path and classifies the evidence. Policy determines whether platform evidence is required, advisory, or not consumed for a given operation class. The hardware reality clause applies: if the deployment's hardware does not support the attestation sources required by policy, the evidence evaluates as UNAVAILABLE and fails closed.

---

## 9. Operator State in Embodied Contexts

Embodied operations frequently involve human operators in proximity to physical systems. Neural Lock operator state evidence (NORMAL, STRESSED, DURESS, IMPAIRED) is directly relevant to embodied governance: an impaired operator should not authorise a high-risk robotic operation, and a coerced operator should not be able to override safety-critical bounds.

PQSEC can compose Neural Lock evidence with PQEA evidence in a single predicate evaluation. A lease renewal might require: perception SUFFICIENT, safety state OK, drift NONE, operator state NORMAL, and platform integrity attested. Each evidence source is independent; PQSEC evaluates all simultaneously.

When Neural Lock evidence is unavailable (no sensors configured, sensor failure), the predicate evaluates as UNAVAILABLE and PQSEC applies fail-closed semantics. For embodied deployments where operator proximity is expected, policy should define compensating controls for Neural Lock unavailability rather than silently proceeding.

---

## 10. Integration with PQ Ecosystem

PQEA integrates with the PQ stack through standard mechanisms. Epoch Clock provides time authority for lease expiry and heartbeat timing. PQSF provides canonical encoding for operation envelopes and evidence artefacts. PQAI provides drift evidence for the AI model governing the embodied agent. Neural Lock provides operator state evidence for human-proximate operations. PQAA provides platform integrity evidence for hardware attestation. PQSEC evaluates all predicates and manages the embodied-specific refusal codes registered in Annex AE.45.

PQEA introduces no new enforcement mechanisms. All enforcement flows through PQSEC.

---

## 11. Conclusion

PQEA demonstrates that the PQ enforcement architecture—evidence-only governance with single deterministic enforcement—extends to physical systems. The key innovations are execution leases (bridging governance-layer latency and real-time control requirements), perception sufficiency as a first-class refusal condition (not a planner input), the hardware reality clause (paper compliance is not compliance), and integration with platform attestation (PQAA) and operator state evidence (Neural Lock) for composed governance of physical operations.

The specification governs what embodied AI systems are permitted to do. It does not dictate how they do it within permitted bounds. The governance layer sets the boundaries; the real-time control layer operates within them.

---

## References

- PQEA Embodied Agent Governance v1.0.0
- PQSEC Enforcement Core v2.0.3 (Annex AE.45, embodied refusal codes)
- PQAI AI Evidence v1.2.0 (drift evidence for embodied models)
- PQAA PQ Attestation Adapter v1.0.0 (platform attestation for embodied hardware)
- Neural Lock Operator State Evidence v1.1.0 (operator state in embodied contexts)
- Epoch Clock v2.1.0 (lease timing)
- PQSF Security Framework v2.0.3 (canonical encoding)
- Fail-Closed Matrix v1.0.0

*All specifications available at: [repository URL]*
