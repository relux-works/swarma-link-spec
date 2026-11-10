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
| Grant v4 exact encoding and resource accounting | [LIP-0008](lips/LIP-0008-grant-v4.md); signed limits and matching contract are the proposed design, with units, numeric bounds and reservation rules still requiring exact profiles. |
| Name-output closure and owner proof | LIP-0008 binds the landlord output and, in name mode, any grantee name plus its output/owner key. Any later confirmed name operation closes, including renewal. Current-output proof, script coverage and reorg handling remain open; local transition history is not the closure criterion. |
| Consent, renewal and channel updates | LIP-0008; every bound name update requires reissuance. Exact consent and replacement-grant bytes remain open. |
| Concrete executor and replica accounting | LIP-0008/LIP-0007 require service name/key, explicit budget partitions, single-use executor binding and one authoritative replica journal; exact key/wire and consistency/recovery profiles remain open. |
| Witness-only funding migration | LIP-0008 requires only witness inputs for seal-creation and issuance-commitment transactions. Current funding is P2PKH; exact signature/input policy, planner, vectors and migration remain open. Namespace choice is settled: any Namecoin name; ownership-proof support is a separate constraint. |
| Freshness risk tiers and construction-time reference | LIP-0008 proposes 60/90-minute cutoffs with node-health checks and a signed recent block reference. Adoption, clock/recency/reorg policy and exact bytes remain open; normative v0.1 STOP is unchanged. |
| Independent model-proxy authority observation | Follow-on to LIP-0008/LIP-0006; the current proxy does not independently read the chain. No implementation or qualification is claimed. |

## Second design review

| Question | Location and boundary |
| --- | --- |
| Issuer-instance provisioning and renewal | LIP-0008 binds owner key/output in grant, agent pointer and independent verifier pins. Authorized rollout/reissuance and the approximately 220-day key-access reminder need an operational profile; expiry uses chain state. |
| Typed signing and migration | Static audit at chain-lab 839bdcca found self-recomputed authenticated contract hashes in both issuer paths, with no demonstrated oracle. Landlord/provider/detached-v2 application domains need versioned matched signer/verifier migration; standard NIP-01 and transaction preimages remain unchanged. Exact tags/bytes/vectors are open. |
| Issuer-branch mempool proof and recovery | LIP-0008 permanently closes after validated issuer evidence, including replacement/eviction. Exact branch/evidence encoding, shared journal and anti-rollback recovery are open; ordinary grantee use and transient reads remain distinct. |
| Confirmation risk policy | Typed minimum depth uses MAX of signed minimum and operator floor. Chain/evidence classes and value-dependent tiers need profiles; no cross-chain finality equivalence or numerical tiers are adopted. |
| T/L/A and payment dependency | Evaluation only, directly spendable payment limited to NMC. SW1 native P2WPKH/SIGHASH_ALL candidate needs name migration and an explicit confirmed-funding exception for L, plus a decision on payment dependencies. Control, consent, fees and proofs remain open. |
| Topology, no-block-wait selection and operator trust | LIP-0008 separates publication gating from offline verification. A no-block-wait profile needs explicit signed selection and evidence semantics; anchored failures never select it. Operator data trust is outside permission proof. |
| Per-seal derived keys | Typed issuer endorsement binds key/script/exact outpoint and context. Derivation/path, custody/recovery and encoding remain open; funding/names/anchors still expose linkage. |
| JCS and public conformance | Per-field exact integer range or decimal-string grammar must precede next-format RFC8785 adoption. Canonical/signature/error/state fixtures, runner and independent Swift implementation are plans. Historical v0.1 files remain frozen. |

Editorial and layout reconciliation, primary Core checks and historical wording
fixes are tracked for the next build; they are not silently applied to frozen
protocol files or evidence. LIP-0006's 32-record wallet journal limit remains a
laboratory bound, not a production retention policy. Delegation/UCAN research is
separate from this draft and grants no implicit delegated issuance authority.
