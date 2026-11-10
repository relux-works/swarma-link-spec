# LIP-0008: Grant v4

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** signed scope, issuer-instance pins, executor accounting and observation policy
- **Builds on:** LIP-0004; relates to LIP-0006 and LIP-0007

## Summary

Grant v4 binds per-rental resource limits directly in the grant's signed scope.
The contract mirrors those limits. Service configuration sets operator-wide
ceilings and cannot supply or enlarge the tenant's missing authority.

The grant binds the landlord name's owner key and exact output at issuance. A name-bound
grantee also binds any Namecoin name, its exact output and the public key owning
that output. Any later confirmed operation spending a bound name output closes
the grant, including renewal. Every verifier on the same validated chain view
can detect this without having observed the transition.

The grant names a concrete executor by service name and key. Limits belong to
that executor; a single-use request also commits to its chosen executor.

These are proposed semantics, not an adopted or executable wire profile. This
LIP deliberately leaves canonical bytes and ownership-proof encoding open.
It changes no normative protocol file or historical conformance record.

## Motivation

Limits reachable only through a contract hash require the verifier to obtain
and parse that separate contract. Directly signed limits make the grant the
source of each rental's bounded authority. The matching contract preserves
agreement on the same terms.

A current name/key pair alone cannot reveal a transfer followed by a return
to the same key. An exact name-output binding makes that transition visible
as a spent output even to a first observer. The deliberate cost is that a
renewal or channel-key update also ends grants bound to the old output.

A service type alone cannot stop two independent executors from each consuming
the same apparent budget. Concrete executor bindings and explicit partitions
make the accounting boundary part of the signed authority.

## Current state

LIP-0004 records implemented grant v3: its scope is a closed action set, its
optional budget has its existing meaning, and `grantee_name` is syntax-checked
metadata. That field does not trigger name resolution or channel-key admission.
The reference baseline is `swarma-chain-lab` commit
`11084e3a31175907e77644a7596e7802283e7c1e`.

The current model proxy accepts a gateway-prepared slot/grant/window/cap binding
and enforces its expiry; it does not independently observe the chain. Proposed
signed contract caps and a future independent grant-gated proxy do not establish
v4 support. No v4 implementation or conformance result is claimed here.

## Proposal

### 1. Versioned signed authority

V4 binds the network/genesis, issuer, target, recipient, validity interval,
seal, contract hash, landlord name/owner-key/output reference, concrete executor bindings,
recent block reference and action/resource scope in its signed grant. Name-mode
recipients also bind their own name output and owner key. These terms are signed
data, covered transitively by the issuance commitment.
Both parties' consent binds the matching contract. Changing any of these terms
requires a newly agreed grant; an unsigned presentation or runtime configuration
cannot override them.

The exact ordered schema, signature domain, consent binding and issuance
encoding need version-specific canonical fixtures before implementation.
V3 bytes and domains are not reinterpreted as v4. No JSON shown in this LIP is
an executable fixture, and this LIP assigns no new OP_RETURN bytes.

### 1.1. Txid stability before confirmation

In the proposed v4 funding profile, transactions creating grant seals and
transactions carrying issuance commitments **MUST** spend only witness inputs.
A mixed transaction with even one legacy input does not meet this requirement.
This constrains funding inputs, not the script type of the newly created seal.
The funding profile also fixes and authenticates the non-witness transaction
body; a witness serialization flag alone is insufficient.

Witness data is outside `txid` under [BIP141](https://bips.dev/141/). With fully
signed witness inputs, third-party changes to input signature data cannot
replace the pre-confirmation txid used by the grant or presentation. With
legacy inputs, a valid transaction may confirm under a different txid from the
one referenced by a pre-signed grant. The expected seal or commitment then
fails to resolve as confirmed: admission fails closed. That is a liveness
failure, not permission to accept a different object or bypass the chain check.

Revocation checks follow the consumed seal outpoint. A malleated revocation
still spends that same output and revokes under the selected observation rule;
its own changed txid does not create a new live seal.

Compatibility: the pinned rental implementation's funding policy uses legacy
P2PKH funding scripts, distinct from its P2PKH seal script. It does not satisfy
this proposed v4 witness-only funding rule. No migration, witness planner,
re-signing, deployment or historical v0.1 change is implied by this draft.

### 2. Per-rental limits

The signed scope contains typed limits assigned to a concrete executor, with
explicit resource identity, unit, period and aggregation rules. The following
are initial semantic kinds, not final field names or a complete registry:

| Kind | Meaning that its profile must bind |
| --- | --- |
| Coins | Asset/network, atomic unit, permitted targets and total spending including the applicable fees. Rental price and authority to spend funds are separate terms. |
| Model requests | Selected service/model and maximum admitted requests in the rental window. |
| Model tokens | Separate cumulative input and output token ceilings, with the model/token-accounting profile. |
| Model cost | Cumulative cost ceiling, exact currency/scale and the price or conservative reservation policy used to account for it. |
| Maximum answer length | Maximum output tokens per request under that model profile. A default output allowance is also signed and cannot exceed the per-request maximum or remaining cumulative allowance. |
| Required confirmation depth | Minimum active-chain depth for the profile's named evidence, with explicit chain and evidence class. Value-dependent risk increases the required minimum; this is not an upper resource cap. |

Defaults select an allowance only within signed authority; they cannot provide
missing authority. A request for a larger answer refuses or requires a newly
agreed grant. Missing required limits, unknown kinds, duplicate/contradictory
limits and unsupported units refuse the affected admission rather than becoming
unlimited access. A zero spending allowance authorizes no spending.

New limit kinds and their accounting semantics arrive through separate LIPs.
The corresponding type profile defines exact integers, bounds, rounding,
reservation, concurrency, uncertain outcomes, replay and whether denied requests
consume a resource. A generic integer counter is not a complete cost contract.

The contract mirrors all grant limits by executor, kind, resource, unit and
amount; a mismatch refuses admission. The contract may retain additional human
terms, but cannot widen the signed scope. Operator configuration may impose a lower global
ceiling or refuse service. It never increases a rental ceiling or substitutes a
per-rental cap absent from the grant. An accepted request must fit both the
signed limits and applicable operator ceilings.

Those ceilings and their enforcement configuration belong outside the agent's
write authority. Under the immutable-boundaries design, a service reads the
sealed configuration, checks it against the approved manifest before startup
and refuses a mismatch. Changing operator ceilings requires a new reviewed
package; a runtime request or writable local override cannot relax them. This
is a deployment requirement, not evidence of completed host qualification.

For confirmation depth the effective minimum is the **maximum** of the
issuer-signed minimum and the operator's risk floor. Configuration cannot lower
the issuer's minimum. The action profile determines how value raises that floor
and which issuance, payment, name or use-spend evidence it covers. Exact tiers
and depths remain open. One confirmation is an application admission rule,
not proof-of-work finality. Higher-value payments follow the separate BTC/LTC
payment paths where selected; their proofs and risk policies do not establish
equivalence between confirmation counts on different chains.

Before an external effect, the service reserves sufficient allowance durably
under its accounting profile and prevents duplicate or concurrent overspending.
Uncertain effects retain their reservations until reconciled. Enforcement
requires intact service credentials and journal; stealing the upstream API key
can bypass this service's rental accounting.

### 3. Name-output closure and recipient modes

At issuance the signed grant binds the landlord's exact Namecoin name, its
owner key and its current registration/update output, identified by transaction
ID and output index. The agent's landlord pointer and independently provisioned
verifier pins MUST bind the same registration instance and owner key. A name
string alone is insufficient: after expiry, a new registration cannot inherit
the old issuer's authority, even under the same spelling or owner key. Expired
names refuse without waiting for another registration. This name output
acts as an additional seal; it does not replace the grant's separate seal.
Every admission requires that same bound output to remain current and unspent
on the verifier's validated active chain.

Any later confirmed name operation spends that output and closes the grant:
key change, transfer, a return to the original key, value update or renewal.
Equal current key/value bytes cannot recreate the old outpoint. A first observer
can reject the spent binding without reconstructing the intermediate name
history or relying on another verifier's durable closure flag. "Every verifier"
means verifiers checking the same validated state; it does not promise instant
observation across partitions or different tips.

The operator tracks remaining lifetime in blocks, schedules access to the owner
key, and renews before expiry. An operational proposal wakes the owner key about
every 220 days per name; block age and the validated expiry rule remain
authoritative, so the calendar reminder is not an admission rule. After the
renewal confirms, update the agent pointer and independent verifier pins through
their authorized provisioning procedure, then issue replacement grants with
fresh consent on the new output. No live grant is silently rebound. Renew
between rentals where possible. Updating a channel descriptor has the same cost.
Name continuity under an unchanged owner does not exempt an update. The pin
update/rollout procedure must fail closed while participants disagree. An
alternative would verify the name history
from the commitment height, requiring history-index support on every verifier;
that is not this draft's chosen closure rule.

A direct-key recipient remains bound to its signed request key. A name-mode
recipient binds three signed facts: the exact Namecoin name, its current output
at issuance and the public key owning that output. No `d/`, `id/` or other
namespace prefix is an admission condition. Name and owner key are mandatory;
the output binding additionally prevents transfer-and-return from restoring
access. The v3 `grantee_key` field acquires no new owner-key meaning.

The owner key has a different role from a listed channel key. An address or a
key asserted inside the value does not prove control of the name output. A
supported ownership-proof profile must connect the pin to that output's spending
condition. Exact key encoding and script coverage remain open; unsupported or
ambiguous proof refuses. Not every script can be reduced to one public key.

Missing, stale or malformed reads refuse without recording a permanent closure.
A pending name spend can suspend admission under the selected profile; only
proved active-chain facts establish the name-output closure described here.
The separate issuer-seal mempool rule below is an explicit durable exception. Reorg
handling must revalidate those facts; no permanent historical v0.1 read-failure
rule is imported into this working draft. Journal records of already attempted
effects remain durable regardless of the name's later chain state.

### 4. Admission order and concrete executor

The verifier uses one consistent observation with pinned network/genesis:

1. Resolve each bound name and its output. Check the landlord name, owner key,
   output, agent pointer and independent verifier pins agree on the issuer
   instance, and that its output is still current and unspent. In name mode require the grantee output
   to be unchanged and prove its owner equals the grant's pinned owner key,
   before consulting channel keys. A changed output rejects even if the key
   returned to its former value.
2. Read the channel descriptor from that same name state and verify the request
   under a key listed for its selected channel. Unknown or removed keys refuse.
   A confirmed update already closes the previous output-bound grant; a new
   grant binds the replacement output and its permitted keys.
3. Require healthy observations, explicit freshness policy and unexpired names.
   Unavailable, stale, conflicting or unproved data never permits an effect.
4. Check the durable closure journal, grant interval, issuer/target, confirmed issuance, separate seal,
   recent-block reference and exact requested action. Require the service name
   and public key to equal an executor binding in the grant and request.
5. Check that executor's signed resource partition, operator ceilings, service
   peer authentication and shared durable journal before authorizing a reserve
   or effect. A valid name or service type alone gives no action authority.

An executor is a particular service's Namecoin name plus pinned public key,
not just `wallet.nmc` or another type. The executor profile binds that key to
the service identity and receipt verification role; the name declaration alone
cannot choose its trusted pin. Exact key/transport encoding remains open.

A budget belongs to that executor. Multiple executors require explicit signed
partitions naming each service/key and its allowance; one total cannot be
independently spent in full at several services. Partitions of one resource
must fit the grant's agreed total, without implicit transfers or double-counted
allowances. An executor cannot borrow another partition's remainder. The
contract mirrors the same assignments.

A single-use request includes its concrete executor in the committed request
before the seal is spent. Another service rejects it even if its type, action
and request parameters otherwise match. Existing LIP-0002 and wallet-v1 request
bytes are not claimed to contain this new binding; the v4 single-use encoding
needs its own profile and vectors.

Replicas acting as the same executor share one authoritative durable journal
for request identity, single-use claims, reservations and remaining allowance.
Independent replica-local journals do not enforce one budget or one effect.
If shared state or its serialization mechanism is unavailable, replicas admit
no new effect.
Recovery reconciles that journal with the chain and preserves uncertain effects;
a spent seal alone is not proof of which external effect completed.

### 5. Services and independent observation

A future model proxy following LIP-0006 verifies the presentation, signed limits,
validity and seal against its own chain view. A gateway can deliver data but
cannot substitute its prepared binding for that verification. Seal spend closes
new admission according to the selected profile. This is a follow-on service
direction, not a property of the current gateway-bound proxy.

Delegated issuance remains a separate capability and profile under LIP-0006;
v4 limits do not implicitly authorize issuing another grant.

### 5.1. Observed issuer spend and durable closure

An executor that observes a **validated issuer-branch spend** of the grant's
seal in its own mempool MUST persist permanent closure before any further
admission. The executor validates the actual spending transaction, exact seal
outpoint, script and branch authorization against the grant's authenticated
seal binding. A caller's label or a reported transaction ID is not branch proof.
Unsupported or ambiguous branch evidence refuses admission without asserting
that an issuer revocation has been proved.

This closure survives restart, eviction, replacement, non-confirmation and a
later reorg. In particular, a higher-fee single-use grantee spend cannot reopen
a grant after this executor proved the issuer's competing spend. A grantee's
valid use-branch spend follows its single-use pending/confirmed/journal rules;
it is not automatically issuer-branch closure. The profile must distinguish
branches cryptographically. Failure to persist closure permits no effect and
requires journal recovery; deleting a closure is not recovery.

This is a deliberate local safety policy, not a consensus preference for issuer
transactions. It protects observers that obtained and validated that evidence;
a first observer cannot infer an evicted issuer spend from the eventual chain.
Persist the evidence and its validated branch conclusion under a recovery and
anti-rollback profile. Exact proof/journal encoding and cross-replica propagation
remain open. Transient RPC failures, tip movement and inconsistent reads
retry or refuse without creating this permanent closure.

### 6. Freshness and operation risk (proposal under review)

Node health, history freshness and operation risk are separate signals. A healthy
node may wait a long time for the next proof-of-work block. Check peer headers
and compare the tip through at least two independent nodes; tip agreement helps
identify a lagging node but does not defeat a shared upstream or an eclipse.
No new block by itself proves neither a broken node nor a fresh name answer.

A reported 2026-11-10 sample covered 20000 blocks over 137.2 days on one Namecoin
node, with mean interval 9.88 minutes. Its time spent beyond each tip-age cutoff
was:

| Tip age cutoff | Share of sampled time | Average cutoff time per day |
| --- | ---: | ---: |
| 30 min | 4.908% | 70.7 min/day |
| 60 min | 0.229% | 3.3 min/day |
| 90 min | 0.001% | 0.01 min/day |

These are reported chain-gap measurements, not service availability or future
bounds. Proposed defaults for review stop money/irreversible
actions at 60 minutes and other privileged actions at 90 minutes, alongside the
node-health checks. A service determines operation risk from its action profile;
a caller cannot downgrade it. Exact age measure, clocks, independent-node
criteria and risk classification need adoption and qualification. This proposal
does not change normative v0.1's existing 30-minute `STOP` rule.

### 7. Acceptance interval versus signing-time bound

A seal transaction ID is known before confirmation and can be known before
broadcast. Requiring `not_before` not to precede the seal's block time restricts
acceptance; it cannot prove the grant was signed after that block.

V4 therefore commits a recent block hash inside the signed grant when asserting
a cryptographic lower bound on its construction. The verifier checks that the
block is on the selected chain and meets the profile's recency policy. This
binds construction to knowledge of that block hash, not to a precise wall-clock
signing time. Block-time labels, a caller timestamp or a future seal outpoint
cannot substitute. Exact field encoding, recency/reorg policy and vectors remain
open; no such field is retroactively added to LIP-0003 bytes.

### 8. Typed signing and canonicalization plan

Each new-profile object type has a distinct application tagged hash: grant,
contract assent, issuance preparation, request, receipt and seal-key endorsement
cannot share an application signing domain. The proposed construction follows
the tagged-hash approach of [BIP340](https://bips.dev/340/). BIP340's internal
signature tags do not assign these application domains. Exact tag bytes,
versioning and the object registry require fixtures before adoption.

A signer MUST accept the complete object, validate its type, schema and
authorized meaning, canonicalize it under the selected version, and compute
the digest itself. It MUST NOT expose these authority keys as a raw-digest
signing interface. Receiving an asserted contract hash is insufficient.
Verification recomputes the corresponding typed digest from the same bytes.
The static signing audit at `swarma-chain-lab`
`839bdcca41cd17ffd7c4057de2dc88a521745515` found that both inspected issuer paths
recompute the contract hash from the authenticated typed contract before
signing. No caller-selected-digest oracle was demonstrated. Landlord consent,
provider contract countersignatures and detached v2 still lack application
prefixes; grant v3 and wallet request/receipt signatures already have their
specified prefixes. New role/version-specific domains require matched producer
and verifier migration, with no silent legacy fallback. Current signed objects
retain their original rules. NIP-01 event IDs and Namecoin SIGHASH_ALL retain
their standard preimages; custom application tags do not replace them. This is
a static provenance finding, not a complete authorization audit or security
proof. Exact successor domains and fixtures remain open.

The next-format canonicalization plan uses
[RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html). JCS uses UTF-16
property ordering, preserves Unicode strings, rejects duplicate properties and
uses IEEE 754 binary64 number serialization. It does not by itself preserve an
arbitrary atomic-unit integer supplied through a rounded number parser.
Each amount/counter schema must choose either an explicitly bounded exact
integer numeric range or a canonical decimal-string representation with fixed
grammar and bounds. No implicit number/string coercion or silent rounding is
permitted. Those per-field choices and migration bytes remain open. Existing
fixed-order v0.1/v3 and wallet-v1 bytes retain their own canonical rules.

### 9. Dependent issuance transactions (evaluation only)

Let seal transaction T create both the grant seal and an additional output L.
After T's body is fixed, the parties sign a grant naming T's seal outpoint.
Anchor A spends L and carries the commitment to that signed preparation. A
therefore depends on the exact T; both may confirm in one block with T before A.
The seal itself remains unspent. This avoids a circular dependency between a
grant and the transaction that commits it. It does not guarantee inclusion,
fees or one-block waiting time, and admission still requires confirmation.

A further proposal makes A also spend the exact renter payment output. This
could bind confirmation of the anchor to that payment dependency. A replacement
that removes that output leaves this A unable to confirm; no mempool-only
issuance is permitted. A Namecoin transaction can directly spend only Namecoin
outputs. BTC/LTC payments require their separate validated proofs and cannot be
consumed by this Namecoin anchor. Output control, authorization, settlement
destination, fees, consent coverage and the exact dependency proof remain open.
There is no implemented payment/anchor optimization claim.

The following **SW1 candidate**, recorded for the funding work, is not an
adopted input profile or a code change. Every T/A input is native P2WPKH;
transaction signatures use SIGHASH_ALL without ANYONECANPAY. The parent is never
rebuilt after the grant is signed. The seal output may remain P2PKH, while L is
P2WPKH. Ordinary funding UTXOs are confirmed. A's deliberate spend of an
unconfirmed L conflicts with a blanket confirmed-input rule; the new profile
must explicitly specify and validate that parent-dependency exception, or wait
for T to confirm. Whether a payment input may be unconfirmed needs the same
explicit decision. No blanket exception is implied. The historical v0.1 anchor
spends a P2PKH name output, so this candidate also requires a new profile and an
authorized name move before applying its all-native-input rule. Namecoin support
and the complete dependency/signing path require qualification.

If a successor anchor also updates a name, the profile must reconcile that
operation with the signed name-output pin without a circular reference or an
immediately spent binding. T/L/A alone does not resolve that question; the
historical name-update anchor is not automatically the new v4 construction.

### 10. Threat model and topology

Assume uncompromised signer/service keys, validated chain evidence under the
selected chain/risk profile, an independently provisioned issuer instance and
intact authoritative accounting. The adversary may control the presenter,
transport, storage endpoint or one name after expiry; suppress transactions;
race issuer revocation with single use; replay requests; and attempt replica
or budget duplication. Name-instance pins, typed signatures, own observation
and durable journals address different parts of that model. Chain reorgs,
censorship, partitions and stolen operator credentials remain explicit limits.

| Topology/profile | Chain benefit and remaining trust |
| --- | --- |
| Independent issuer and executor, anchored admission | The executor requires confirmed publication of the exact signed preparation before admission and observes seals/names itself. A transport cannot present an unpublished preparation as issued; suppression and chain risk remain. |
| Issuer and executor controlled by one operator, anchored admission | The chain supplies independently checkable publication/revocation evidence for a dispute. It cannot compel that operator to enforce its own limits or protect renter data. |
| Explicit no-block-wait profile in one operator domain | A separately agreed profile may authorize action without awaiting an issuance block. Local authorization and journals remain necessary; confirmed-publication-before-admission evidence is absent. This mode is never an automatic fallback. |

Offline signature verification checks authorship and object integrity without an
anchor. Mandatory anchored admission additionally gates the effect on confirmed
publication; it does not prove honest custody, data handling or completion.
Permission to send data to an operator is not evidence that the operator is
trustworthy. The no-block-wait profile needs explicit signed selection, exact
admission/evidence semantics and review before use. If anchored mode is selected
and its evidence is unavailable, refuse rather than switching modes.

### 11. Per-seal keys and privacy

The new design uses a separately derived key for each seal. A typed issuer
endorsement binds its public key and exact spending script to the exact seal
outpoint and the grant/profile context. The verifier checks that endorsement
under its trusted issuer pin before accepting the seal or classifying an issuer
spend. This is a per-seal script pin, separate from the name-owner key and
registration-instance pins. Rotating or re-registering a name cannot substitute
a new script for an existing seal. KDF/path, derivation authority, custody,
recovery and exact endorsement bytes remain open.

Distinct seal addresses reduce linkage through a shared seal address. Public
names, funding transactions, anchor dependencies, timing and disclosed grants
can still link activity. This is no anonymity claim or modification to existing
name-derived seal scripts.

## Alternatives

Keeping limits only in the contract preserves the existing indirect commitment
but requires its bytes. Name-history verification can preserve grants across
renewals but requires a trustworthy history index and complete proofs. Binding
the exact output instead trades that dependency for mandatory reissuance after
every name operation. A type-only executor cannot provide a shared global budget
across independently operated services.

## Security consequences

The name resolver, ownership proof, receipt pins, service custody and durable
accounting form separate boundaries. A correct request signature proves neither
fresh ownership nor remaining budget. A name value cannot attest its own owner.
Expiry, unavailable chain data and unsupported units refuse admission without
turning a transient read failure into proved name-output closure. Reorgs
and revocation can race a completed external effect and cannot undo it. Raw
issuer, money-key or upstream-secret compromise remains outside service limits.

## Conformance impact and v3 compatibility

V3 and normative v0.1 retain their formats, domains, name semantics, checks and
historical evidence. An implementation selects a supported version explicitly;
unsupported v4 refuses without v3 fallback. There is no automatic v3 upgrade,
new normative conformance class or mainnet qualification in this draft.

Future vectors must publish exact bytes, independent expected verdicts and
post-refusal state. The semantic outline pairs these controls:

| Valid control | Rejection or invariant |
| --- | --- |
| Matching grant/contract limits and a request within all ceilings | Signed-limit mutation, contract mismatch, unknown kind/unit, missing required cap or cumulative/per-request overshoot: no effect or new authorized reservation. |
| Signed default within maximum and remaining allowance | Default above per-request/cumulative bounds, missing authority or config-only rental limit: refuse; config cannot enlarge authority. |
| Same bound name outputs, proved owner, listed channel key and fresh unexpired names | Spent/replaced output, owner mismatch, value-only assertion, unsupported proof, removed key or stale/expired/missing name: no effect. |
| Arbitrary namespace with supported owner proof | Prefix-only admission or rejection is wrong; malformed exact names still refuse under the name profile. |
| Unchanged name outputs and a newly started verifier | Transfer-and-return, renewal, same-key value/channel update: old outpoint is spent, so all such grants refuse even without local observation history. A reissued grant on the new output is the positive neighbour. |
| Exact executor name/key and its allocated budget | Wrong executor of the same type, reused full budget at a second executor, partition overspend or single-use executor substitution: no effect. |
| Replicas sharing one authoritative journal; recovery with chain evidence | Independent journals, lost journal authority, concurrent duplicate or uncertain retry: no second reservation/effect. |
| Healthy independent node observations and action-specific age policy | Lagging/conflicting nodes or exceeded risk cutoff refuse; a healthy gap under the proposed cutoff alone is not node failure. |
| Recent block committed in signed grant and verified on the selected chain | Seal confirmation alone proves no signing-time lower bound; unknown, stale or wrong-branch block reference refuses under the selected profile. |
| Seal-creation and issuance transactions with only fully signed witness inputs | One legacy input or witness marker alone fails the proposed funding rule. A changed legacy txid that leaves the signed reference unconfirmed yields no admission; revocation still follows the spent seal outpoint. |
| Valid v3 and independently valid v4 fixtures | Version/domain substitution, ambiguous recipient mode, name without owner pin and silent downgrade: reject without changing preserved v3 results. |
| Independent proxy observation and durable remaining allowance | Gateway-only authority assertion, spent seal, conflicting concurrent reservations or uncertain retry: no second effect or overspending. |
| Matching issuer instance in grant, agent pointer and independent verifier pins | Expiry/re-registration, same-key new registration, pointer-only or presenter-chosen pin replacement refuses; authorized renewal plus new pins and a fresh grant is the positive neighbour. |
| Complete validated objects and distinct typed signing domains | Caller-supplied digest, wrong object tag/version, malformed or changed canonical bytes refuse without a signature/effect; current static provenance audit does not replace these successor vectors. |
| Exact-unit numeric values within the chosen range or string schema | Overflow, parser rounding, duplicate properties, invalid Unicode and silent number/string conversion refuse; include URL escaping and non-ASCII ordering fixtures. |
| Valid issuer-branch mempool evidence durably recorded, then restart/replacement | Permanent refusal survives eviction and a competing grantee use-spend. A valid use-branch spend alone must not be mislabeled as issuer closure; transient read/tip errors create no closure. |
| Evidence reaching both signed confirmation minimum and operator risk floor | Insufficient depth under either floor refuses; applying MIN or silently equating NMC/BTC/LTC depth is wrong. |
| Typed endorsement for the exact per-seal key/script/outpoint | Different seal, swapped endorsement, untrusted issuer or substituted script refuses; separate valid per-seal keys remain admissible. |
| Explicit supported admission profile and its required publication evidence | An unpublished preparation refuses in anchored mode; evidence failure cannot activate no-block-wait mode. |

Publish canonical input bytes, typed digests, public keys/signatures, expected
errors and state/journal transitions together with a deterministic runner.
Include known-invalid controls proving the runner catches each claimed invariant,
plus valid neighbours. A second Swift implementation must consume the same
fixtures independently; agreement between two implementations alone is not the
oracle. Freeze historical v0.1 fixtures and report successor results separately.
This is a conformance plan, not a published runner or interoperability result.

## Open questions

- Exact versioned bytes, signature domain, commitment/consent encoding, name
  outpoints, executor/single-use bindings, recent block field and cross-language
  vectors; reissuance after channel updates and renewal.
- Owner-key encoding and supported scripts; proof of current unspent name
  outputs, reorg policy, channel descriptors and Matrix key support.
- Adoption of the proposed 60/90-minute risk cutoffs, explicit freshness/clock
  measure, independent-node health criteria and block-recency policy.
- Executor identity/key profile, partition validation and shared-journal
  consistency, recovery and anti-rollback requirements.
- Limit-kind wire registry, asset/model identities, numeric bounds, cost units,
  rounding, price binding and reservation/reconciliation rules per service.
- Witness-only funding/signature policy, exact input-profile validation and
  migration from current P2PKH funding; normative adoption and independently
  reviewed implementation.
- Issuer-instance pin provisioning and renewal rollout; typed-hash registry,
  matched producer/verifier migration and per-field JCS integer/string schemas.
- Durable issuer-branch evidence, branch classification and replica recovery;
  value/depth tiers; explicit no-block-wait profile and its consent/evidence.
- T/L/A and same-chain payment dependency, SW1 confirmed-input exceptions,
  transaction authorization and fee/settlement control; per-seal key derivation,
  custody/recovery and endorsement format; public runner and independent Swift
  implementation.
