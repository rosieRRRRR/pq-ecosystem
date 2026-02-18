# Bitcoin-Anchored Verifiable Time: The Epoch Clock Protocol

**White Paper — PQ Ecosystem**
*Author: rosiea — PQRosie@proton.me*
*Date: 2026*

---

## Abstract

Distributed systems require time for ordering, freshness, expiry, and monotonicity guarantees. System clocks are untrusted. Network time protocols are vulnerable to manipulation. This paper presents Epoch Clock, a verifiable time protocol that anchors temporal authority to Bitcoin's proof-of-work chain through inscribed profiles and threshold-signed ticks.

Epoch Clock produces signed, monotonic time artefacts that can be verified independently without trusting the issuer, network, or any intermediary. Profiles are inscribed as Bitcoin ordinals, making the time authority's configuration immutable and publicly auditable. Ticks are distributed via mirrors without trust requirements. Consumers verify signatures locally.

We describe the protocol's architecture, the mirror consensus model, the v3 multi-signature extension, and the integration with the PQ enforcement architecture where Epoch Clock provides the sole time authority for all temporal predicates.

---

## 1. Introduction

Time is a foundational dependency in security systems. Expiry, freshness, ordering, replay detection, and monotonicity all require temporal reference. Yet the most common time source—system clocks synchronised via NTP—is trivially manipulable by network adversaries.

Epoch Clock addresses this by anchoring time authority to Bitcoin's proof-of-work chain, the most computationally expensive ordering mechanism available. The protocol produces signed time artefacts (ticks) that carry cryptographic proof of their validity, enabling consumers to verify time without trusting any intermediary.

### 1.1 Design Goals

The protocol has four design goals. First, verifiability: any consumer can independently verify a tick's authenticity without trusting the issuer network. Second, immutability: the time authority's configuration (profile) is inscribed on Bitcoin and cannot be altered retroactively. Third, distribution: ticks are distributed via mirrors without trust requirements; mirror compromise cannot produce valid ticks. Fourth, post-quantum readiness: tick signatures use ML-DSA-65, a NIST-standardised post-quantum signature scheme.

---

## 2. Architecture

### 2.1 Profiles

An Epoch Clock profile defines the time authority's configuration: signing keys, tick interval, mirror list, hash algorithm, and signature scheme. The genesis profile is inscribed as a Bitcoin ordinal, creating an immutable, publicly auditable anchor.

Profile updates follow a parent-child lineage model. Each child profile references its parent's inscription ID, creating a verifiable chain from any current profile back to the genesis inscription.

### 2.2 Ticks

A tick is a signed, monotonic time artefact containing a sequence number, timestamp, profile reference, and cryptographic signature. Ticks are produced at a defined interval and distributed to mirrors.

Tick signatures use ML-DSA-65 (post-quantum) by default. The signature covers the canonical JCS JSON representation of the tick body, ensuring deterministic verification across implementations.

### 2.3 Mirrors

Mirrors distribute ticks to consumers. Mirrors are untrusted: they cannot produce valid ticks (they lack signing keys) and consumers verify tick signatures locally. Mirror divergence (mirrors serving different ticks for the same sequence) is a detectable failure condition.

Consumer tick validation requires checking signature validity, monotonicity (sequence must be strictly increasing relative to last accepted tick), profile reference (must match the consumer's pinned profile), and freshness (tick must be within the configured reuse window).

### 2.4 Encoding Exception

Epoch Clock uses JCS Canonical JSON (not Deterministic CBOR) for tick and profile encoding. This is because profiles are inscribed as Bitcoin ordinals, which require JSON-compatible content. The PQ ecosystem explicitly handles this exception: PQSF §7.4 and PQSEC §13.2 define no-re-encoding rules ensuring JCS artefacts are never re-encoded to CBOR. Re-encoding breaks byte identity and produces invalid artefacts. This is a documented implementation trap that agent and implementer documentation (PQ For Agents §6.2) calls out explicitly.

---

## 3. Multi-Signature Extension (v3)

Version 3 profiles support multi-signature tick issuance. A threshold number of signers must contribute valid signatures before a tick is considered valid. This eliminates the single-issuer risk present in v2, where compromise of one signing key compromises all tick production.

The v3 profile defines a `tick_sig_threshold` (minimum valid signatures required) and a set of authorised signer keys. Consumers verify that the tick carries at least `tick_sig_threshold` valid signatures from distinct authorised signers.

---

## 4. Integration with PQ Enforcement

Within the PQ ecosystem, Epoch Clock is the sole time authority. No specification may use system clocks, NTP, or any other time source for authority, freshness, or expiry decisions.

PQSEC consumes Epoch Clock ticks as inputs to temporal predicates: `valid_tick` (tick is structurally valid and signed), tick-based freshness (tick is within the staleness window), and tick-based expiry (artefact expiry ticks have not been reached).

When Epoch Clock is unavailable, PQSEC maps this to `E_TIME_SOURCE_UNAVAILABLE` with outcome DENY. There is no fallback time source. This is the fail-closed property applied to time: uncertainty about time results in refusal.

### 4.1 Consumers Across the Ecosystem

Epoch Clock ticks are consumed by every component that produces or evaluates time-bounded artefacts:

**Enforcement core (PQSEC).** All temporal predicates—expiry, freshness, staleness, replay guard—reference Epoch Clock ticks. Lockout timers, governance cadence limits, and policy staleness windows are all tick-denominated.

**Custody (PQHD, BPC, ZEB, SEAL).** DelegationConstraint expiry, pre-construction gating tick windows, execution attempt tick bounds, and SEAL submission timeout are all Epoch Clock tick-denominated.

**AI governance (PQAI).** Agent enrollment expiry, drift evidence tick windows, tool capability profile expiry, and behavioural fingerprint baseline validity are tick-denominated.

**Attestation (PQAA).** Attestation bundle expiry (`expiry_tick`), request validity windows, and evidence freshness are tick-denominated. PQAA cannot produce valid evidence without a verified tick.

**Product layer (PQ Gateway).** Billing period boundaries, provider registry snapshot validity, inference receipt tick stamps, and enrollment tick windows consume Epoch Clock ticks. PQ Gateway bootstraps its Epoch Clock connection during enrollment (PQGW-ONBOARD) and requires a verified tick before any governed operation.

**Embodied operations (PQEA).** Execution lease duration, heartbeat re-evaluation intervals, and operation envelope validity are tick-denominated.

The uniformity of tick consumption is a design property: every time-dependent decision in the ecosystem references the same authoritative time source.

---

## 5. Threat Model

### 5.1 Threats Addressed

Epoch Clock addresses clock manipulation (system clocks lie, NTP is attackable), time forgery (adversary presents fabricated time to trick expiry or freshness checks), replay with stale time (adversary replays old ticks to bypass freshness), and mirror compromise (adversary controls tick distribution infrastructure).

### 5.2 Residual Risks

The protocol does not protect against total compromise of all threshold signers (v3 mitigates by requiring threshold), Bitcoin consensus failure (anchor becomes unreliable), or the window between issuer key compromise and detection. The last risk is inherent to hierarchical trust anchors and is acknowledged as an audit-relevant exposure window rather than a design flaw.

---

## 6. Related Work

Roughtime (Google) provides authenticated time but relies on server trust and does not anchor to proof-of-work. Blockchain timestamps provide ordering but not signed, distributable time artefacts suitable for consumption by enforcement systems. Certificate Transparency logs provide temporal ordering for certificates but are not general-purpose time authorities.

Epoch Clock combines Bitcoin's ordering guarantee with threshold-signed distributable artefacts and post-quantum signatures, creating a time authority suitable for adversarial environments where no individual party is trusted.

---

## 7. Conclusion

Epoch Clock provides verifiable, Bitcoin-anchored, post-quantum-signed time artefacts for distributed security systems. Its design eliminates trust in system clocks, network time, and distribution infrastructure while providing a simple consumer interface: verify signature, check monotonicity, check freshness.

The protocol is operational, with a genesis profile inscribed on Bitcoin mainnet. Within the PQ ecosystem, it serves as the sole time authority for all temporal predicates evaluated by the enforcement core, consumed uniformly by custody, AI governance, attestation, embodied, and product-layer components.

---

## References

- Epoch Clock Specification v2.1.0
- PQSF Security Framework v2.0.3 (§7.4, JCS encoding exception)
- PQSEC Enforcement Core v2.0.3 (§13.2, time validation)
- PQAI AI Evidence v1.2.0 (tick-denominated drift and enrollment windows)
- PQAA PQ Attestation Adapter v1.0.0 (tick-denominated attestation validity)
- PQ Gateway v1.0.0 (tick-denominated billing and enrollment)
- PQEA Embodied Agent Governance v1.0.0 (tick-denominated leases)
- NIST FIPS 204: ML-DSA (Module-Lattice-Based Digital Signature Standard)
- Bitcoin Ordinals Protocol

*All specifications available at: [repository URL]*
