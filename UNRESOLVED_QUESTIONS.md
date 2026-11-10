# Unresolved questions

Draft implementation descriptions do not adopt normative profiles. Their
decision, protocol and conformance work follows LIP-0001.

| Question | Location and boundary |
| --- | --- |
| Adoption and coexistence of landlord, locator and action-service profiles | LIP-0004/0005/0006 remain Draft; historical v0.1 requirements and evidence retain their own meaning. |
| Common action vocabulary versus wallet-specific encoding and limits | [LIP-0006 open questions](lips/LIP-0006-grant-gated-actions.md#open-questions); cross-language canonical rules and complete vectors precede normative interoperability claims. |
| Further locator networks and endpoint discovery | [LIP-0005 open questions](lips/LIP-0005-op-return-locator.md#5-open); current closed name schemas do not acquire blob/tracker fields. |
| Name-action continuation, remote transport, broker routing and non-coin budgets | LIP-0006 specifies the implemented wallet v1 choices; extensions need separate action/effect contracts. |
| Deployment qualification, key/UID provisioning and journal migration/recovery | LIP-0006; mainnet configuration support and same-UID fixtures do not establish actual cross-user custody or anti-rollback guarantees. |
| Booking-to-wallet terms and an agent-controlled small-wallet tier | LIP-0006; incompatible byte formats cannot be substituted, and refill/lease policy needs an explicit contract. |

Existing questions for single use and detached grants remain in LIP-0002 and
LIP-0003. This index does not change their status or the preserved evidence.

## New design drafts

| Question | Location and boundary |
| --- | --- |
| Typed service declaration and action profiles | [LIP-0007](lips/LIP-0007-service-types.md); member path, canonical bytes, key/endpoint profiles, size and parser coexistence remain open. A declaration is not authority. |
| Pre-freeze invocation and capability naming | LIP-0008 section 12 fixes signed logical request fields, exact lowercase slash commands and the reserved `swarma/` namespace, with LIP-0007 alignment. Exact request/registry grammar, leaf assignments, principal/time/nonce encoding and legacy-action mappings remain open; no existing parser/action is extended. |
| Bounded explicit issuance-capability paths | LIP-0008 requires at most two authority links, exact parent-ID binding, current checks and at-use attenuation at every link, plus per-ancestor budget accounting. Exact proof/wire/consent, shared-journal serialization and recovery need profiles. This does not settle the separate both-owner general agent sub-delegation decision. |
| Canonical object identity and reserved stateless policy | LIP-0008 requires signed type/version, typed hash alignment, one canonical ID preimage per version and strict signature validation; signature inclusion, wire encoding and replay/journal keys remain open. The future `policy` kind needs a separate LIP, syntax/evaluator and vectors; unsupported policy authority refuses. |
| Grant v4 exact encoding and resource accounting | [LIP-0008](lips/LIP-0008-grant-v4.md); signed limits and matching contract are the proposed design, with units, numeric bounds and reservation rules still requiring exact profiles. |
| Issuer-output closure and grantee owner proof | LIP-0008 pins the landlord output, while a name-mode grantee binds any name plus its owner public key without an exact output pin. Issuer updates close; same-owner grantee renewal/channel rotation preserve the grant. Current owner proof, script coverage, reorgs and any separate grantee transfer-history policy remain open. |
| Consent, renewal and channel updates | Issuer name updates require reissuance. Grantee renewal/rotation under the same owner keeps the grant and checks current listed keys. Exact consent and replacement-grant bytes remain open. |
| Concrete executor and replica accounting | LIP-0008/LIP-0007 require service name/key, explicit budget partitions, single-use executor binding and one authoritative replica journal; exact key/wire and consistency/recovery profiles remain open. |
| W/L construction-profile qualification | The authenticated chain pin selects W (native P2WPKH/SIGHASH_ALL, confirmed ordinary funding, explicit validated linkage/payment dependencies) or L (confirmed references, anchor after seal confirmation, no unconfirmed chains). Exact pin/input/dependency validation, planner, vectors and migration remain open. W starts with Namecoin; L is spec-only until a non-SegWit chain is pinned. Account-based chains need another seal design. Namespace choice is settled; owner-proof support remains separate. |
| Freshness risk tiers and construction-time reference | LIP-0008 records the decided 60/90-minute risk cutoffs and at least two independent nodes agreeing on the tip (owner decision 2026-11-10); implementation follows in GV4. Exact age/clock, independence and risk-classification profiles need qualification. The separate signed recent-block reference still needs recency/reorg policy and exact bytes; historical normative v0.1 STOP is unchanged. |
| Independent model-proxy authority observation | Follow-on to LIP-0008/LIP-0006; the current proxy does not independently read the chain. No implementation or qualification is claimed. |

General agent-issued child grants remain a separate both-owner decision; the
signer service capability does not authorize arbitrary sub-delegation.

## Second design review

| Question | Location and boundary |
| --- | --- |
| Issuer-instance provisioning and renewal | LIP-0008 binds owner key/output in grant, agent pointer and independent verifier pins. Authorized rollout/reissuance and the approximately 220-day key-access reminder need an operational profile; expiry uses chain state. |
| Typed signing and migration | Static audit at chain-lab 839bdcca found self-recomputed authenticated contract hashes in both issuer paths, with no demonstrated oracle. Landlord/provider/detached-v2 application domains need versioned matched signer/verifier migration; standard NIP-01 and transaction preimages remain unchanged. Exact tags/bytes/vectors are open. |
| Issuer-branch mempool proof and recovery | LIP-0008 permanently closes after validated issuer evidence, including replacement/eviction. Exact branch/evidence encoding, shared journal and anti-rollback recovery are open; ordinary grantee use and transient reads remain distinct. |
| Confirmation risk policy | Typed minimum depth uses MAX of signed minimum and operator floor. Chain/evidence classes and value-dependent tiers need profiles; no cross-chain finality equivalence or numerical tiers are adopted. |
| T/L/A and payment dependency | W explicitly permits validated unconfirmed linkage/payment dependencies; L requires confirmed inputs and separate seal/anchor stages. Namecoin anchors spend only NMC outputs; BTC/LTC keep separate proofs. Name-output migration/self-reference, payment control, consent, fees and exact proofs remain open. No implementation or latency result. |
| Topology, no-block-wait selection and operator trust | LIP-0008 separates publication gating from offline verification. A no-block-wait profile needs explicit signed selection and evidence semantics; anchored failures never select it. Operator data trust is outside permission proof. |
| Per-seal derived keys | Typed issuer endorsement binds key/script/exact outpoint and context. Derivation/path, custody/recovery and encoding remain open; funding/names/anchors still expose linkage. |
| JCS and public conformance | Per-field exact integer range or decimal-string grammar must precede next-format RFC8785 adoption. Canonical/signature/error/state fixtures, runner and independent Swift implementation are plans. Historical v0.1 files remain frozen. |

Editorial and layout reconciliation, primary Core checks and historical wording
fixes are tracked for the next build; they are not silently applied to frozen
protocol files or evidence. LIP-0006's 32-record wallet journal limit remains a
laboratory bound, not a production retention policy. UCAN-derived pre-freeze
rules are expressed only as Swarma requirements in Draft LIP-0008. The planned
post-freeze spike, evaluator/resolver implementation and independent vectors
remain separate work and grant no implicit delegated issuance authority.
