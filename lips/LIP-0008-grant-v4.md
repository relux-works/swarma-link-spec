# LIP-0008: Grant v4

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** signed scope, issuer-instance pins, executor accounting and observation policy
- **Builds on:** LIP-0004; relates to LIP-0006 and LIP-0007

## Summary

Grant v4 binds per-rental resource limits directly in the grant's signed scope.
The contract mirrors those limits. Service configuration sets operator-wide
ceilings and cannot supply or enlarge the tenant's missing authority.

The grant binds the landlord name's registration and owner key. It stays
live while the name's later updates change neither the owner nor the `swarma`
member; the verifier walks the name's history back to the bound registration
through its transaction index. Renewal closes nothing, and a transfer, a
re-registration and a grant-key change are visible to a verifier that starts
today. A name-bound grantee instead binds any
Namecoin name plus its owner public key. At admission the current owner must
equal that key, then the current listed channel keys are checked. Same-owner
renewal and channel-key rotation preserve the grant, while an owner mismatch
refuses admission. No exact grantee name output is signed into this binding.

A grant names its recipient in exactly one way, by key or by name, and carries
no recipient name as metadata. Its signed validity window is a pair of block
heights. Each seal has its own key; the key of a revocable-only seal is
derived under BIP-32 in an account that holds only seal keys.

The grant names a concrete executor by service name and key. Limits belong to
that executor; a single-use request also commits to its chosen executor.
The action set shares one seal and closure; an invocation is a separate signed
type. Bounded issuance-capability chains preserve every ancestor's constraints
and consumed budget. They do not authorize free agent sub-delegation.

These are proposed semantics, not an adopted or executable wire profile. This
LIP deliberately leaves canonical bytes and ownership-proof encoding open.
It changes no normative protocol file or historical conformance record.

## Motivation

Limits reachable only through a contract hash require the verifier to obtain
and parse that separate contract. Directly signed limits make the grant the
source of each rental's bounded authority. The matching contract preserves
agreement on the same terms.

A current name/key pair alone cannot reveal a transfer followed by a return
to the same key. The history of the issuer name between the grant's
construction and the current tip does reveal it, to a first observer too:
every name operation spends the previous name output, so the transactions
form one chain. Its cost is a transaction index on the verifier's node and
one transaction read per name operation. Recipient channel keys follow
current name resolution under the pinned owner key; no history walk is part
of that rule.

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

V4 binds the network/genesis, issuer, target, recipient, validity interval in
block heights (section 7.1), seal, contract hash, landlord name, registration and owner key, concrete executor bindings,
recent block reference and action/resource scope in its signed grant. Name-mode
recipients bind their name and owner key, without an exact name-output pin. These terms are signed
data, covered transitively by the issuance commitment.
Both parties' consent binds the matching contract. Changing any of these terms
requires a newly agreed grant; an unsigned presentation or runtime configuration
cannot override them.

One grant MUST bind its complete closed action set to one seal. An action
outside that set MUST refuse, even if its service type advertises it. Validated
issuer closure of that seal closes admission to every action in the grant;
splitting a request or presenting another proof path MUST NOT reopen them.
This does not relabel a valid grantee use-branch spend as issuer revocation.
An explicitly authorized child grant has its own seal and issuance evidence,
while remaining dependent on its committed parent under section 12.

The exact ordered schema, signature domain, consent binding and issuance
encoding need version-specific canonical fixtures before implementation.
V3 bytes and domains are not reinterpreted as v4. No JSON shown in this LIP is
an executable fixture, and this LIP assigns no new OP_RETURN bytes.

### 1.1. Witness and Legacy construction profiles

The chain pin selects one transaction-construction profile: Witness (W) or
Legacy (L). W is the default for a pinned UTXO chain with activated SegWit,
including Namecoin, Bitcoin and Litecoin. L covers UTXO chains without SegWit.
The selected profile belongs to the authenticated chain context; exact pin
encoding and fixtures remain open. An unknown or mismatched profile refuses
admission, without automatic fallback. Both profiles preserve the same signed
grant semantics, name/seal checks, consent, limits and confirmation-risk rules.
They differ in transaction construction and timing.

In W, **every input** of a seal-creation transaction and of an issuance anchor
**MUST** be native P2WPKH. Signatures use **SIGHASH_ALL only**, without
ANYONECANPAY. The seal transaction's complete non-witness body is fixed and
authenticated before the grant is signed; it is not rebuilt afterwards. The
anchor is constructed after the grant is signed, then fixed and authenticated
before any dependent reference uses its txid. A witness marker, a wrapped
witness input or a single legacy input does not satisfy W. The rule constrains
inputs, not the script type of the new seal output.

Ordinary funding comes from confirmed UTXOs. W explicitly permits two
unconfirmed protocol dependencies: the linkage output created with the seal,
and a same-chain payment output spent by the anchor. These exceptions do not
permit arbitrary unconfirmed wallet funding. Each permitted unconfirmed parent
must also have a fixed authenticated body and only fully signed native P2WPKH
inputs with SIGHASH_ALL, with its funding ancestry ending at confirmed UTXOs.
The exact dependency and payment checks still need versioned fixtures.
Seal and anchor may confirm in the same block, in dependency order. No mempool
observation alone authorizes an effect, and inclusion or one-block latency is
not guaranteed.

[BIP141](https://bips.dev/141/) excludes witness from `txid`; its protection
against third-party signature-data malleability requires fully signed witness
inputs. The SIGHASH_ALL rule uses the chain's standard witness signing preimage
([BIP143](https://bips.dev/143/) for version 0), not a Link application tag.
A changed transaction body or an authorized replacement invalidates the pending
references even in W; it cannot silently rebind an existing signed grant.

In L, the grant references **only confirmed outpoints**. The issuer waits for
the seal transaction to confirm before signing its exact outpoint into the
grant and building the issuance anchor. All anchor inputs, including linkage
and payment outputs where used, are already confirmed. **No unconfirmed
dependent chains** are allowed. A newly created seal and its issuance anchor
therefore require two sequential confirmation stages in distinct blocks:
seal first, anchor afterwards. An already confirmed pool seal has completed
the first stage. Higher risk floors, censorship or reorgs can require more
blocks; two stages are not a bounded delivery time or finality guarantee.

A malleated or replaced parent invalidates the pending preparation or grant.
Admission fails closed. Reissue from validated confirmed outputs and obtain
new signatures/consent for changed signed terms; never substitute a different
txid into an old signed object. This is a liveness cost, never permission for
unsafe admission. Low-S and strict DER reduce particular malleability avenues
where enforced by the chain's rules, but do not guarantee a stable legacy txid.
[BIP66](https://bips.dev/66/) specifies strict DER; its presence alone does not
provide W's dependency guarantee.

Revocation in both profiles follows the consumed seal outpoint. A malleated
revocation still spends that same output; its own txid cannot recreate a live
seal. Account-based chains such as Ethereum and Tron are outside both profiles
and require a separate seal design.

Compatibility: the pinned rental implementation funds with legacy P2PKH. It
does not satisfy W; its script choice alone does not prove L's confirmed-only
construction and timing. W for Namecoin is the first implementation direction;
L remains specification-only until a non-SegWit chain is pinned and qualified.
No migration, implementation result or historical v0.1 change is implied.

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

Ivan Oparin decided on 2026-11-14 that further kinds join this list; the
co-author's agreement is pending. The decision names the kinds. For coins
it adds a maximum for one spend, a maximum for a period, and an explicit
identifier of the asset and of the payment system: a chain with its asset,
or a rail outside a chain. It also says for every kind what this section
says of spending: an allowance of zero authorizes nothing.

The table below lists the kinds of that decision. The meaning beside each
kind is the draft's proposal and no part of the decision; it waits for the
owners' agreement. A type profile binds such a meaning only if it adopts
it, and a profile that reads a kind otherwise states its own meaning. Each
kind needs a type profile with the items that
[LIP-0018](LIP-0018-extension-guide.md) section 2 lists.

| Kind named by the decision | Meaning proposed by the draft |
| --- | --- |
| External service cost | Cumulative cost ceiling for a service that is billed by cost, with the exact currency and scale and the price or conservative reservation policy. Model cost is its first case. |
| Runtime and concurrency | The running time in hours, and the number of instances or runs that may be active at once. |
| Rate | A modifier of another kind: the number of operations in an interval. |
| Outbound messages | The number of messages, and the recipients they may go to. |
| Repository writes | The number of writes in a period, and the repositories and refs they may go to. |
| Storage and egress | Bytes stored and bytes sent out, with the hosts that outgoing traffic may reach. The allowlist can name bare IPv4 and IPv6 addresses. |
| Name operations | The number of name registrations and updates. |
| Secret releases | The number of releases, and the secrets that may be released. |
| Owner-confirmation threshold | A threshold for an effect beyond which the owner's confirmation is needed. Whose owner confirms, and what the threshold measures, is for the type profile. |

Defaults select an allowance only within signed authority; they cannot provide
missing authority. A request for a larger answer refuses or requires a newly
agreed grant. Missing required limits, unknown kinds, duplicate/contradictory
limits and unsupported units refuse the affected admission rather than becoming
unlimited access. A zero spending allowance authorizes no spending, and a zero allowance of
any other kind authorizes nothing of that kind.

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
write authority. The administrator owns the sealed configuration; the service
group has read-only access (file mode `0640`, directory mode `0750`). Before
startup, the launching side checks the configuration hash against the sealed
manifest and refuses to start on a mismatch. The service cannot rewrite the
configuration at runtime. Changing operator ceilings requires a new reviewed
package; a request or writable override cannot relax them. This is the accepted
deployment decision of 2026-11-10, not evidence of implementation or completed
host qualification.

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

### 2.1. One grant for the term; the period belongs to limits and payment

This section records the decision of 2026-11-11 by Ivan Oparin.

One hire is one grant. Its window covers the whole agreed term in block
heights (section 7.1): about 13,000 blocks for three months at the nominal
ten minutes. The chain holds one issuance record for the hire. The hire ends
at `not_after_height`, or earlier when the issuer spends the seal.

A shorter interval, such as an hour, is not a grant window. It is a period:
a term of a typed limit ("so many requests per period") and of payment ("so
much per period"). A period divides the one window for accounting and
payment. A new period needs no new grant, no new seal and no new issuance
record. A payment for a period may itself be a chain transaction; that is
the payment's record, not the grant's.
Whether a period is counted in blocks or in clock time belongs to the limit's
type profile and to the contract; this LIP does not fix it.

The contract states what follows when a period is not paid. The protocol
offers one consequence: the issuer ends the grant by spending the seal.

### 2.2. Payment evidence after a reorganisation

This section records the decision of 2026-11-11 by Ivan Oparin. No LIP held
this rule before; it concerns the issuer's reaction to payment evidence and
sits here beside the confirmation-depth rule.

A payment that was counted for an issued grant can leave the active chain
when its block is displaced. The issuer distinguishes two cases:

| What the issuer's node shows for the counted payment | Issuer's action |
| --- | --- |
| The same payment transaction is still valid: it is back in the mempool or confirmed again in another block | Wait `N` blocks for it to confirm again. Revoke nothing. |
| The coins of that payment are spent by a different transaction | Revoke: spend the seal. |

A third state is neither of these. When the issuer's node cannot establish
the state of the payment (the node is unavailable, its answers conflict, or
the transaction is absent from its mempool without a conflicting spend in
view), nothing is proved. Absence alone is not a conflicting spend. The
issuer revokes nothing on that ground and reads again; how long it may wait
in this state is part of the same open profile parameter.

`N` is a parameter of the payment profile and has no value yet. What the
issuer does when the payment is still valid and still unconfirmed after `N`
blocks is not decided. The reference booking service at chain-lab
`839bdcca41cd17ffd7c4057de2dc88a521745515` implements the earlier rule: it
requests revocation as soon as the block of a counted payment is displaced
or the payment disappears, and a payment that returns does not clear that
request.

### 3. Issuer registration, owner key and recipient modes

This section records the decision of 2026-11-11 by Ivan Oparin. It replaces
the earlier draft rule that bound the grant to the exact current output of
the issuer name and closed it on every name operation, renewal included.

At issuance the signed grant binds three facts about the issuer: the exact
Namecoin name, the registration of that name, and the owner key. The
registration is identified by the transaction and output that first
registered the name (`name_firstupdate`). The owner key is the key that
controls the name's outputs. The agent's landlord pointer and independently
provisioned verifier pins MUST bind the same registration and owner key. A
name string alone is insufficient: after expiry, a new registration cannot
inherit the old issuer's authority, even under the same spelling or owner
key. Expired names refuse without waiting for another registration.

The grant lives while the name's updates change neither the owner nor the
`swarma` member. At every admission the verifier walks the history of the
name on its validated active chain:

1. Start at the name's current output. Each name operation spends the
   previous name output, so the verifier follows that input to the previous
   operation, transaction by transaction, through the node's transaction
   index.
2. The walk MUST reach the bound registration. A walk that ends at another
   registration, or that cannot be completed, refuses: the name was
   re-registered, or the history is not available.
3. Let `R` be the height of the grant's committed recent block (section 7).
   The name output that was current at `R`, and every later output up to the
   current one, MUST be controlled by the bound owner key and MUST carry the
   `swarma` member under which the grant was issued: the same bytes, with the
   grant key equal to the grant's issuer key.
4. An output on that stretch with another owner or another `swarma` refuses
   the grant for every verifier that validates this chain: a transfer, a
   change of the grant key, and a change followed by a return are all in the
   history. No local memory of earlier observations is needed for this
   verdict.
5. The verdict of this walk is relative to the active chain. The verifier
   computes it at every admission and writes no closure for it into its
   durable journal. While the change stays in the active chain, the refusal
   repeats at every check, for a verifier that saw the change and for one
   that starts today alike. If a reorganisation removes the name operation
   that changed the owner or `swarma`, and the history on the new active
   chain satisfies rules 2 and 3, the grant is admissible again for both
   verifiers. Their answers on the same validated chain are the same.

Renewal closes nothing: it changes neither the owner nor `swarma`. The same
holds for an update of the `nostr` member and of the owner's other members
([LIP-0010](LIP-0010-name-value.md)). The seal remains the only way to end
one grant early; the name rule ends all grants of an issuer whose name
changed hands or whose grant key was replaced.

This differs from the two durable records of this LIP on purpose. A validated
issuer spend of the seal seen in the mempool closes the grant durably
(section 5.1), and the journal of effects already attempted stays whatever
the chain does later. Those record what a verifier observed or did. The name
rule records nothing: it is a property of the chain's history, and a history
that a reorganisation replaced is no longer the chain's history. An effect
performed while the grant was admissible is not undone by a later refusal,
and a refusal is not undone for the time it lasted.

A verifier MAY cache the result of a walk. A cached result is valid only for
the predicate it was computed for: the same active chain up to the cached
output, the same bound registration, owner key and `swarma`, and the same
`R`. Reaching the registration once is not a result for another grant with
another `R` or another issuer key. The cache is a saved computation, not a
source of authority. After a reorganisation that touches the cached stretch
the verifier discards it and repeats the walk on the chain it then validates.

"Every verifier" means verifiers checking the same validated state; it does
not promise instant observation across partitions or different tips. The
walk needs the transactions of the name's history. A node without a
transaction index, and a light client without proofs for every step, cannot
perform it and refuse.

The operator still tracks the name's remaining lifetime in blocks, schedules
access to the owner key and renews before expiry. An operational proposal
wakes the owner key about every 220 days per name; block age and the
validated expiry rule remain authoritative, so the calendar reminder is not
an admission rule. Grants, agent pointers and verifier pins survive a
renewal unchanged.

Which point starts the constrained stretch of rule 3 is this draft's choice:
the committed recent block. The decision fixes the rule (registration, owner
key, unchanged owner and `swarma`, history walk) and does not name that
point; the choice needs confirmation.

A direct-key recipient remains bound to its signed request key. A name-mode
recipient binds two signed facts: the exact Namecoin name and its owner public
key. No `d/`, `id/` or other namespace prefix is an admission condition. The
verifier resolves the name at check time, proves its current owner equals the
pinned key, then accepts a request key listed for the selected channel in that
same state. The v3 `grantee_key` field acquires no new owner-key meaning.
Section 3.1 fixes the two modes and the channel member.

A grantee channel-key rotation or renewal under the same owner preserves the
grant. A removed channel key refuses requests, while a newly listed supported
key may use the same live grant. An owner change that no longer matches the
signed key voids admission. This current-owner comparison cannot by itself
prove an unobserved transfer-and-return; permanent grantee-history closure
would need a separate rule and evidence, not an invented exact-output pin.

The current output is evidence of ownership, not a signed grantee-output term.
An address or key asserted inside the value does not prove control of that
output. A supported ownership-proof profile must connect the pinned owner key
to its spending condition. Exact key encoding and script coverage remain open;
unsupported or ambiguous proof refuses. Not every script reduces to one key.

Missing, stale or malformed reads refuse without recording permanent closure.
Expired names refuse. A pending name spend can suspend admission under the
selected observation profile; the issuer-history refusal and the current
grantee-owner check remain distinct. Reorg handling revalidates those facts.
The issuer-seal mempool rule below is an explicit durable exception. Journals
of already attempted effects remain durable regardless of later name state.

### 3.1. Recipient by key or by name

A v4 grant names its recipient in exactly one of two modes:

| | Recipient by key | Recipient by name |
| --- | --- | --- |
| Signed in the grant | The request key | The exact Namecoin name and the public key that owns the name's output |
| Recipient name in the grant | None: the mode has no name member | The signed name, which is the source of truth |
| Request key | The signed key | Read at every admission from the channel member of the name's current value |
| What the verifier proves first | Nothing about a name; no name is read | The name's current output is controlled by the signed owner key |
| Change of the request key | A new grant | An update of the name by the same owner; the grant stays |

1. A grant MUST select one mode. A verifier MUST refuse a grant that carries
   both a request key and a recipient name, and a grant that carries neither.
2. A grant by key MUST NOT carry a recipient name in any member, signed or
   unsigned. V3's `grantee_name`, a name that the verifier checks for
   spelling and never resolves, has no counterpart in v4. A name that a
   verifier does not resolve can disagree with the key beside it, and the
   reader of the grant cannot tell which of the two the issuer meant.
3. A grant by name MUST NOT carry a request key. The name and its owner key
   decide who the recipient is. The request key is whatever the name lists
   for the channel at the moment of admission.
4. The two keys of the name mode do different work. The owner key controls
   the name's output; it proves which party the recipient is and signs
   nothing in a request, so it can stay offline. The channel key signs
   requests and is the key a service sees online. Losing the channel key
   costs one name update by the owner. Losing the owner key loses the name.
5. The channel is fixed by the profile under which the service authenticates
   the request. The presenter cannot select a channel that the profile does
   not define. An unknown channel, and a channel member that yields no key,
   refuse.

| Channel | Member of the recipient name's current value | Request authentication |
| --- | --- | --- |
| Nostr | The key that `nostr` yields for `_`: `nostr.names._`, or the key string ([LIP-0010](LIP-0010-name-value.md) section 4) | BIP-340 signature by that key |

Another channel needs its own profile, which names the member and the
signature scheme. Other entries of `nostr.names` are not the recipient.

In the name mode a name and a key cannot disagree inside the grant, because
the grant carries no request key. The remaining mismatch is between the
signed owner key and the name's current owner: it refuses admission and
records no closure, as section 3 states.

### 4. Admission order and concrete executor

The verifier uses one consistent observation with pinned network/genesis:

1. Resolve each bound name. Check that the landlord name, registration and
   owner key in the grant, the agent pointer and the independent verifier
   pins agree, and walk the issuer name's history under section 3: it reaches
   the bound registration, and since the committed block neither the owner
   nor `swarma` changed. A grant-key change rejects even if the key returned
   to the former value. In grantee name mode prove the current name owner
   equals the signed owner key before consulting channel keys. No exact
   grantee-output equality is required.
2. Authenticate the request by the grant's signed recipient mode (section
   3.1). By key: verify the request under the signed request key; no recipient
   name exists and none is read. By name: read the channel member from that
   same name state and verify the request under the key it yields for the
   request's channel. A wrong key, an unknown channel and a removed key
   refuse in either mode that can produce them. Same-owner grantee
   rotation/renewal keeps a grant by name; removed channel keys refuse. An
   issuer-name update that changes the owner or `swarma` refuses the grant
   on the chain that holds it and requires a replacement grant; any other
   issuer-name update keeps it.
3. Require healthy observations, explicit freshness policy and unexpired names.
   Unavailable, stale, conflicting or unproved data never permits an effect.
4. Check the durable closure journal, grant interval, issuer/target, confirmed issuance, separate seal,
   recent-block reference and exact requested action. Require the service name
   and public key to equal an executor binding in the grant and request.
5. Check that executor's signed resource partition, operator ceilings, service
   peer authentication and shared durable journal before authorizing a reserve
   or effect. A valid name or service type alone gives no action authority.

The invocation and any committed issuance-capability chain MUST satisfy
section 12 before any new reservation or effect. The grant's signed executor,
the invocation's executor and the authenticated service's pinned name/key MUST
agree; an invoker-selected executor never supplies missing grant authority.

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

### 6. Freshness and operation risk (decided design)

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
bounds. The owner decision of 2026-11-10 replaces the 30-minute stop in the
Grant v4 design: stop money or irreversible actions at 60 minutes and other
privileged actions at 90 minutes. Admission also requires a node-health check
with at least two independent nodes agreeing on the tip. This is decided design;
implementation follows in GV4. A service determines operation risk from its
action profile; a caller cannot downgrade it. Exact age measure, clocks,
independent-node criteria and risk classification still need profile definition
and qualification. This decision does not rewrite historical normative v0.1's
existing 30-minute `STOP` rule.

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

### 7.1. Validity in block heights

The signed window of a v4 grant is a pair of block heights,
`not_before_height` and `not_after_height`, next to the committed recent block.
These are logical names; their encoding needs fixtures like every other field.

1. Both heights MUST be present, finite non-negative integers with
   `not_before_height < not_after_height`. The window is half-open:
   `[not_before_height, not_after_height)`.
2. Let `H` be the height of the tip of the verifier's validated active chain
   in the same consistent observation that supplies the name and seal reads.
   Admission requires `not_before_height <= H < not_after_height`. No clock
   enters this comparison, and no grace is added.
3. Let `R` be the height of the committed recent block. A grant with
   `not_before_height < R` MUST refuse. This is a policy against backdated
   windows, decided by Ivan Oparin on 2026-11-11. It is not a cryptographic
   necessity: the committed block bounds when the grant was constructed and
   does not by itself bound the window an issuer may sign.
4. Every authority link of section 12 states its window in heights. A child
   window lies inside its parent's, and the usable window is the intersection
   of the link windows.
5. The same measure applies to every other signed validity bound that a
   verifier compares with chain state, including the expiry of a key
   attestation. This LIP defines no attestation format.

Heights are chosen for three reasons. The verifier already validates the
chain, so the window needs no trusted clock, and every verifier on the same
chain state computes the same `H`. Block timestamps are set by miners within
consensus tolerances; the height is not adjustable. The other chain terms of
the grant are already counted in blocks: the recent block reference, the
confirmation depth and the 36000-block name expiry.

The cost is that a window has no exact length in wall-clock time. In the
sample of section 6 the mean interval was 9.88 minutes, so 1000 blocks took
about 6.9 days, against 6.94 days at the nominal ten minutes. Single gaps
vary far more: in that sample the tip was older than 60 minutes for 0.229% of
the time and older than 90 minutes for 0.001%. A window therefore opens and
closes at a moment that is known in blocks and only estimated in hours.

While no block arrives, `H` does not advance and the window does not close.
Section 6 covers that interval: the freshness cutoffs stop money and
irreversible actions at a tip age of 60 minutes and other privileged actions
at 90 minutes.

A reorganisation can lower `H`. The verifier repeats the comparison on the
chain it then validates, at the effect boundary. An effect that was already
performed is not undone.

For people, the contract shows approximate dates computed at issuance: the
issuance time plus ten minutes for each block between the tip at issuance
and the stated height. The contract marks them as estimates. The contract
mirrors the two heights exactly, and a mismatch refuses like any other
mirrored term. A date is never an admission input.

The invocation keeps its own short interval in signed clock time, `iat` and
`exp` (section 12.5); Ivan Oparin decided this on 2026-11-11. One request
lives for seconds, which is below the resolution of a block. V3 keeps `not_before` and `not_after` in Unix seconds.

### 8. Typed signing and canonicalization plan

Each new-profile object type has a distinct application tagged hash: grant,
contract assent, issuance preparation, request, receipt and seal-key endorsement
cannot share an application signing domain. The proposed construction follows
the tagged-hash approach of [BIP340](https://bips.dev/340/). BIP340's internal
signature tags do not assign these application domains. Exact tag bytes,
versioning and the object registry require fixtures before adoption.

The object type and version MUST also be inside the signed canonical bytes.
An unsigned transport label or the hash tag alone is insufficient. Signers
and verifiers MUST reject unknown or mismatching type/version combinations;
a grant, invocation or receipt cannot be reinterpreted as another type.
The signed envelope and its application tagged hash MUST
select the same registered type/version. Exact member paths, tag bytes and
the registry remain open; this assigns no successor wire bytes.

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

#### 8.1. Object identity and canonical signatures

For each type/version, the profile MUST define one canonical ID preimage and
one SHA-256 object ID. The preimage MUST bind the signed type/version and
entire signed payload, including metadata; the exact signature inclusion and
envelope layout remain open. A fixed canonical signed object MUST have one
recomputed ID regardless of the proof bundle carrying it. A caller-supplied ID, alternate
encoding or transport wrapper MUST NOT create a second accepted identity for
those same canonical object bytes. Unknown or noncanonical representations
MUST refuse rather than being silently transcoded into a different signed token.

The signature profile MUST use strict BIP-340 validation of its 64-byte
signature, including its range and even-Y verification rules, with one
version-defined wire encoding. This is not a claim that a message has only
one possible valid signature: BIP-340 permits different signing nonces.
Re-signing or another object ID MUST NOT restore a seal, nonce claim,
consumed parent budget or reservation. Stateful admission binds the underlying
authority and logical request as well as object identity. Exact ID preimages,
signature encoding, replay keys and cross-version journal bindings require
fixtures; existing v3 signed-grant IDs and wallet-v1 commitments stay unchanged.

### 9. Dependent issuance transactions and profile timing

Let seal transaction T create both the grant seal and an additional output L.
Here L names the linkage output, not the Legacy profile. After T's body is
fixed, the parties sign a grant naming T's seal outpoint. Anchor A spends L and
carries the commitment to that signed preparation. The seal remains unspent;
separating its creation from the commitment avoids a circular grant/txid
reference.

Under W, the explicit dependency exception in section 1.1 allows A to spend
unconfirmed L. T and A may confirm in one block, with T before A. Ordinary
funding is confirmed and every T/A input is native P2WPKH with SIGHASH_ALL only.
The linkage output must therefore be native P2WPKH to be spent by A under W;
the seal output's script is independent of that input rule. A may also spend
an exact unconfirmed same-chain payment output under the same validated-parent
exception. This is a construction permission, not mempool-only issuance or a
claim of implemented payment/anchor optimization.

Under L, T confirms before the grant is signed and A is built. L and every
other A input must already be confirmed; T and A cannot share a confirmation
block. Parent malleation or replacement requires fail-closed reissuance, not
rebinding. The two sequential stages do not promise a maximum waiting time.

A Namecoin anchor can directly spend only Namecoin outputs. BTC/LTC payment
paths keep their separate validated proofs; this draft does not turn a Namecoin
anchor into a cross-chain spend. Output control, authorization, settlement
destination, fees, consent coverage and exact dependency proofs remain open.
The historical v0.1 anchor spends a P2PKH name output, so it cannot satisfy W's
all-native-input rule unchanged. A new input/name profile and qualification are
required; current legacy scripts do not establish L support either.

If a successor anchor also updates a name, that update keeps the grant as
long as it changes neither the owner nor `swarma` (section 3); the earlier
concern about an immediately spent name-output pin no longer applies. The
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
a new script for an existing seal. Section 11.1 proposes where the key comes
from. Custody qualification, the recovery procedure and exact endorsement
bytes remain open.

Distinct seal addresses reduce linkage through a shared seal address. Public
names, funding transactions, anchor dependencies, timing and disclosed grants
can still link activity. This is no anonymity claim or modification to existing
name-derived seal scripts.

### 11.1. Derivation of seal keys (proposal)

In v3 the seal pays to the grant key, so one secret signs grants under
BIP-340 and seal spends under ECDSA (LIP-0004 section 5). BIP-340 advises
against that. For nonces derived without fresh randomness it calls not
reusing the same private key across signing schemes the most reliable
safeguard, and it gives the example of RFC 6979 nonces in both schemes
leaking the secret key. V4 separates the two uses.

Seal keys are derived by BIP-32 in an account of the signer's seed that holds
only seal keys. The proposal covers the revocable-only seal: the seal of a
grant that only its issuer may spend, where every spend is a revocation. On
Namecoin the construction profile of section 1.1 selects the layout:

| Profile | Script of a revocable-only seal | Path on Namecoin |
| --- | --- | --- |
| W | Native P2WPKH | `m/84'/7'/<seal-account>'/0/<i>`, the BIP-84 layout |
| L | P2PKH | `m/44'/7'/<seal-account>'/0/<i>`, the BIP-44 layout |

The coin type 7 is Namecoin's registered SLIP-0044 value. Another chain
selected under W or L uses its own registered coin type. `<seal-account>` is
a hardened account index reserved for seals, and `<i>` is the index of one
seal. The single-key script is chosen for the revocable-only seal because
wallets already implement that layout. Section 1.1 is unchanged: it
constrains transaction inputs and leaves a seal's script type free.

A single-use seal is outside this table. Its script must give the issuer's
revocation and the grantee's use two cryptographically distinct branches
(sections 4 and 5.1). A single-key output admits one key: with distinct keys
the grantee cannot spend it, and with a shared key the two spends cannot be
told apart, and a caller's label is not branch evidence. The output profile
of the single-use seal, its endorsement and the source of its issuer-branch
key stay open.

1. The seal account is separate from the funding account. The name-owner key
   and the grant key are outside both: the name-owner key stays in cold
   custody, and the grant key signs no transaction.
2. The signer alone holds the account's extended private key. The operator's
   watch-only node MAY hold the account's extended public key to monitor seal
   outputs.
3. An index MUST NOT be used twice. The signer's journal records the index
   with its seal before the first signature that uses the key.
4. A verifier needs no knowledge of the derivation. It checks the typed
   seal-key endorsement, signed by the grant key, that binds the public key
   and script to the exact outpoint and grant. The path is an issuer-side
   rule; a verifier cannot observe it and does not refuse for it.

The layout has one known weakness. The seal indices are non-hardened, and
BIP-32 states that an extended public key together with any non-hardened
private key below it reveals the extended private key. A party that obtains
the account's extended public key and one seal's private key can therefore
compute every seal key of the account. That party can spend the seals, which
closes the grants early and takes the seal amounts. It cannot sign a grant
or an endorsement, move a name, or spend funding outputs, because those keys
are outside the account.

Hardened seal indices, `…/0'/<i>'`, remove the weakness. They also remove
public derivation: an extended public key no longer yields the seal keys.
The watch-only node then imports each seal script one by one, from the
endorsement or the signer's journal, and a lost journal cannot be rebuilt by
scanning from a public key. Non-hardened indices are the default, with the
extended public key kept as a secret of the operator; Ivan Oparin decided
this on 2026-11-11, together with the single-key script of the
revocable-only seal in each construction profile. A deployment that must hand that key to another party uses
hardened indices instead; rule 4 makes the two interchangeable for a
verifier.

The extended public key also links every seal of the account. Whoever holds
it sees the per-seal addresses as one set, so it is not published.

Three points need qualification before use: import of the account's public
descriptor into a watch-only wallet of the pinned Namecoin Core build;
support for coin type 7 and Namecoin addresses in the chosen signing device;
and recovery, where the BIP-44 gap limit of 20 unused addresses assumes that
indices are used in order.

### 12. Invocation and bounded issuance-capability chains

These are requirements for the proposed Swarma v4 profile before its freeze,
not an implemented resolver. LIP-0006's signer service still needs explicit
issue authority.

Earlier revisions left agent-issued child grants as a separate decision of
both owners. Ivan Oparin decided on 2026-11-11 that child grants are part of
the protocol, and Alexey Grigorev concurred the same day; section 12.6
records the decision and its staging. The issue capability of this section
is the right of re-delegation of that decision.

#### 12.1. Signed invocation

A grant and an invocation MUST be separate signed object types. An invocation
MUST bind the following logical fields; these names do not assign a canonical
JSON schema or change wallet-v1 request bytes:

| Logical field | Required meaning |
| --- | --- |
| Subject | The exact authority-bearing resource/service target, constant along its proof chain; not an optional or wildcard principal. |
| Command | One exact leaf action from the type profile's closed action table. |
| Arguments | The complete typed action parameters and targets covered by the request signature. |
| Ordered proof IDs | One ordered authority path from its trusted root to the final grant, including the exact committed issue-capability parent. |
| Nonce | A request identity under the selected executor/journal profile; not a replacement for a seal or durable accounting. |
| `exp` | Required finite, exclusive invocation expiry. |
| `iat` | Signed claimed invocation time, not proof of actual signing time. |
| Executor | The concrete service name and key, equal to a signed grant executor and the authenticated service pin. |

The final audience/grantee MUST authenticate the invocation under the selected
key/name-recipient profile. Type, version, subject, command, arguments, proof
order, nonce, times and executor MUST all be signature-bound. Mutating any of
them invalidates that request. Issuance locators and fetched evidence are not
authority merely because a bundle contains them. Wallet-v1 `proof.use_txid`
remains outside its unsigned-request hash; neither that commitment nor
LIP-0002's different signed-envelope commitment is redefined here.

#### 12.2. Proof path, attenuation and budget accounting

Depth counts signed grant/issue-capability links, not the invocation or evidence
objects. A direct landlord-to-grantee grant has depth 1. The maximum is depth 2:
landlord to authorized delegated issuer, then delegated issuer to grantee.
A third signed authority link MUST refuse; repeated IDs and cycles MUST refuse.

Each link's audience MUST equal the next link's authenticated issuer under
the exact principal/name-owner profile. The subject MUST remain constant.
The root MUST be independently trusted for that subject; a self-signed bundle
cannot select its own trust root. Every link MUST pass its own signature,
current name/owner/instance, issuance, seal, interval and closure checks at use.
An invalid or closed ancestor MUST refuse the dependent request, including
when the child itself is current and correctly signed.

A child MUST commit to the exact ID of the issue capability under which it
was issued. That capability MUST explicitly authorize issuance for the child's
subject, permitted commands, grantee, executor, limits and lifetime. Ordinary
action authority, possession of a grant or an audience key MUST NOT imply
re-delegation. A different proof path MUST NOT replace the committed parent
or bypass its closure. Final requests MUST satisfy both the child's constraints
and the issuing capability's permitted descendant-action constraints; an
issuance command is not silently treated as an ordinary effect command.

Known action sets and numeric ceilings MUST NOT widen in a child. Attenuation
MUST also be checked against the actual invocation at execution: it MUST
satisfy every link's applicable argument, target, executor, time and resource
constraints. A child's claim to be narrower is insufficient. Missing authority,
unknown constraint semantics or an unsupported proof profile MUST refuse;
no unimplemented policy evaluator may stand in for these checks.

Each child resource budget MUST be at most its parent's applicable ceiling.
All direct and descendant consumption/reservations together MUST fit each
ancestor's budget; siblings do not each inherit another full copy. The
authoritative executor journal MUST atomically check and reserve the request
against every applicable link before its effect. Each ancestor is accounted
once for that request, not once per duplicate proof. Failed admission MUST
create no effect or newly authorized partial allocation; uncertain existing
reservations remain charged under their recovery profile. Restart, retry or
reissuance MUST NOT reset an ancestor's consumed allowance.

This chain uses one concrete executor and authoritative accounting domain.
Independent executors require the explicit signed partitions of section 4;
independent journals MUST NOT consume a shared apparent parent remainder.
Distributed serialization, reservation/reconciliation encoding and recovery
remain open, not an implementation claim.

Proof bundles carry complete signed objects or exact resolvable references.
The receiver MUST recompute each ID under section 8.1 and match it to the
ordered path and committed parent. Unresolved, mismatched or ambiguous proofs
MUST refuse before a new reservation/effect. A fetched token or cache entry
does not prove its seal is live; all current-state checks still run. The bundle
format, transport/resolution bounds and canonical proof encoding remain open.

#### 12.3. Capability names and signed metadata

A capability binds subject, command and applicable policy/constraints. Command
names MUST use lowercase slash-separated segments under the versioned service
action registry described in LIP-0007. Commands match exact leaf identifiers;
neither a prefix nor the top command `/` grants sibling or descendant actions.
The `swarma/` namespace is reserved for protocol-defined capabilities; a
provider MUST NOT allocate its own commands there. Exact grammar, leaf names
and registry assignments remain open and need their own profiles. This rule
does not rename existing wallet-v1 actions or expand a closed parser.

Metadata MUST be signed when included, but MUST NOT add authority or override
an authority-bearing field. V3's `grantee_name`, social descriptions and a
service self-declaration do not supply grants, identity pins, budgets or issue
permission. The separate v4 name/owner recipient binding remains authoritative;
placing a name in metadata is not that binding, and a v4 grant carries no
recipient name as metadata at all (section 3.1). A declaration may select a
known interface and advertise an endpoint/key for verified discovery, but it
cannot authorize an effect or replace an independently established trust pin.
Changing signed metadata changes signed bytes; ignoring it for authority does
not permit unsigned mutation.

#### 12.4. Reserved stateless policy form

Reserve `policy` as a future stateless-limit kind only. Its syntax, numeric
semantics, evaluation bounds and exact registry encoding require a separate
LIP and paired vectors. No evaluator or UCAN policy language is adopted here.
A profile without that adopted capability MUST refuse a request requiring
`policy`; it MUST NOT ignore it or convert it to unlimited authority. Any
future stateless predicate remains separate from seal state, single-use claims
and cumulative budgets, which require executor accounting.

#### 12.5. Time terms and post-freeze work

A link's validity interval is half-open and stated in block heights:
`[not_before_height, not_after_height)`, compared with the tip height `H` of
section 7.1. Invocation time is the signed `iat` claim; execution time is the
verifier's trusted current time at the effect boundary. Invocation admission
requires `iat <= now < exp`. All bounds MUST be present and finite, with
well-ordered values; a null or unbounded bound and an added grace allowance,
in blocks or in clock time, MUST refuse. `iat` does not establish a
cryptographic signing-time bound; section 7 still applies.

Admission requires two predicates together: `H` lies in the intersection of
all link height windows, and `iat <= now < exp` holds on the verifier's
clock. Heights and clock times are never compared with each other. An empty
intersection of the link windows MUST refuse. A child interval MUST NOT widen its parent's. Every link MUST be
valid at execution, not only when parsed, issued or first observed. After
observation work, the executor MUST recheck both measures before a new
reservation/effect. At `H == not_after_height` or `now == exp`, new admission
MUST refuse; an expired middle link is sufficient.
Pending/terminal replay and retained uncertainty keep their type-specific
journal rules and never renew authority or permit another effect.

The planned post-freeze spike measures size, verification cost and proof depth,
and qualifies canonical bytes, proof resolution, accounting and any proposed
policy evaluator with requirement-derived positive/negative fixtures. It does
not select a library, publish a runner or establish interoperability now.

Provenance only: these rules adapt UC1's review of
[UCAN core](https://github.com/ucan-wg/spec/blob/8072f3f23f451eaa1271269fe763aebcf294f4db/README.md),
[delegation](https://github.com/ucan-wg/delegation/blob/1cb32dbc9d4d15a23bf9844a02515d760b81e816/README.md)
and [invocation](https://github.com/ucan-wg/invocation/blob/0f4c11325af6aca298b565cc19e90009d10e0197/README.md).
They remain the Swarma profile, with no UCAN dependency, codec adoption or
compatibility claim. The signature distinction above follows
[BIP-340](https://github.com/bitcoin/bips/blob/d71d60687b4c250ae9c73c1cc29897dbd56e9903/bip-0340.mediawiki)
Default/Alternative Signing and Verification, not an assumption of one unique
signature per message.

#### 12.6. Re-delegation (decision of 2026-11-11)

Ivan Oparin decided the following on 2026-11-11, and Alexey Grigorev
concurred the same day and added the staging of R6. The owners' decision of
2026-11-12 on notary certification follows the table and the comparison of
the two ways of issuing. Nothing of either is implemented.

| Decision | Direction |
| --- | --- |
| R1. Child grants | Child grants are part of the protocol. An agent may issue a child grant only when it holds a grant with the right of re-delegation. A child grant is never broader in authority than its parent. |
| R2. Countable conditions | Resources carried in the grant, such as limits, budgets, tokens, counts and expiry, are checked mechanically: the child's value is at most the parent's. |
| R3. Conditions in words | Scope expressed in words cannot be checked mechanically. A separate mechanism is required to verify that a child's textual scope does not exceed its parent's. |
| R4. Sensitive scenarios | Recommended: a grant with the right of re-delegation plus a notary. |
| R5. Two ways of issuing | Re-delegation is the main mechanism for large swarms. Issuance of every grant by the operator's own signer stays the baseline for simpler systems and for the most sensitive ones. |
| R6. Staging | Issuance by the operator's own signer is implemented first. Re-delegation by an agent follows once a mechanism exists that checks that a child is not broader than its parent. |

The right of re-delegation is the issue capability of section 12.2. R1 and
R2 are what section 12.2 already requires: the capability is explicit, a
child commits to its exact ID, known action sets and numeric ceilings do not
widen, the invocation satisfies every link, and descendants are accounted
against every ancestor. Ordinary action authority still implies no
re-delegation, and managing an agent implies none either.

The two ways of issuing compare as follows. Both use the same grant format.

| | Re-delegation | Issuance by the operator's signer |
| --- | --- | --- |
| Signer of the grant an agent receives | The agent that holds the right of re-delegation | The operator's signer service, with the grant key |
| Authority path | Two links | One link |
| Cost | Every link is checked at every request; conditions in words are not checked by the verifier and need a separate check | Every grant passes through the operator's signer |
| Use | Large swarms | Simple systems; the most sensitive resources |
| Stage | Second, after the breadth check is designed | First |

The child is signed by the recipient of the parent: "each link's audience
MUST equal the next link's authenticated issuer" (section 12.2). For a
parent issued by key, that is the grantee key. For a parent issued by name,
it is the key the name's value yields for the selected profile under
section 3.1. An agent's name value carries no `swarma.grant` member
([LIP-0010](LIP-0010-name-value.md)), so the issuer rule of section 3
applies to the root of the path only. On v3 only the landlord's grant key
signs a grant (LIP-0004 section 2), so an agent signs no child there: the
landlord's signer issues the child on the delegator's signed request
([LIP-0014](LIP-0014-notary-certified-redelegation.md) section 5). Whether
an agent that re-delegates on v4 needs a grant key of its own, separate from
its channel key, is open; LIP-0014 gives the case that shows why, under its
open questions.

R3 is not met by this LIP. Conditions written in words live in the contract
text and in task scope; section 12.2 compares only known action sets and
numeric ceilings and refuses unknown constraint semantics. Two decisions
cover them.

Decided on 2026-11-11: a separate mechanism is required to verify that a child's textual
scope does not exceed its parent's (R3), and the party that performs this
check for a re-delegated grant is the notary. A verifier's own mechanical
check never establishes that textual scope is within the parent's, and
nothing in this section lets a verifier treat it as established.

Decided on 2026-11-12 by the owners: every child grant carries a notary
attestation that the verifier checks at admission, whatever the child's
scope. A child without a valid attestation refuses. The attestation is
required in addition to the mechanical checks of section 12.2 and never in
place of one: a child that is wider in an action set, a ceiling, a budget or
a window refuses for that reason even when it is certified. The same
decision fixes these points, recorded as D1 to D12 in
[LIP-0014](LIP-0014-notary-certified-redelegation.md):

| Point | Decision of 2026-11-12 |
| --- | --- |
| Which children | Every child is certified (D1). A root grant with a right of re-delegation names its notaries and needs no attestation (D2). |
| Who certifies | The parent's signed right of re-delegation names one to four notaries by name; each publishes its attestation key in its own name (D3). One of them is enough (D9). The notary is the issuer's within one owner and an agreed third party across owners (D8). |
| Budgets | Children draw on a separate pool that the parent signs, in partitions (D6). |
| Depth | Two links (D7). |
| Withdrawal | Durable; the same child may be certified again after a plain withdrawal and may not after one for cause (D5). |
| Anchor and cost | One LIP-0005 frame per attestation (D10); the issuer pays within one owner, the contract decides across owners (D11). |
| Staging | After the first proof of LIP-0013, in shadow mode first; enforcing mode for children needs each owner's separate approval (D4). In Goal 1 `instruct`, `review` and `land` are delegable and `spend` is not (D12). |

The notary is a party that compares a child with its parent and
certifies that the child does not exceed it. [LIP-0012](LIP-0012-notary.md)
proposes the role, and LIP-0014 proposes the fields, the checks and their
order.

The breadth check that R6 waits for is now designed in LIP-0014, as a draft
without an implementation: the countable part is checked by every verifier,
and the part in words by the notary. Of the five ways to strengthen the "not
broader" check that this section proposed on 2026-11-11, the decision of
2026-11-12 settles three:

| Proposal | State after the decision of 2026-11-12 |
| --- | --- |
| (a) Machine-readable scope: actions and resources as structured caveats, so that a child's scope is a subset any verifier can check | Not decided. Known action sets and numeric ceilings must not widen; unknown constraint semantics refuse. No caveat language is adopted (section 12.4 reserves a stateless policy form). |
| (b) A maximum re-delegation depth in the parent grant; 0 means no right of re-delegation | Decided: two links (D7). LIP-0014 proposes the member `depth` with the values 0 and 1. |
| (c) The child commits the parent's grant ID, and the verifier walks the chain to the root | Already required. |
| (d) The sum of the children's budgets does not exceed the parent's, enforced at spend time, on chain where possible | Decided: a separate signed pool with a partition per child (D6), serialized at issuance and enforced by each executor's journal. No on-chain enforcement is described. |
| (e) A notary attestation is required for any child whose scope is free text | Decided more broadly: for every child (D1). |

## Alternatives

Keeping limits only in the contract preserves the existing indirect commitment
but requires its bytes. Binding the exact current output of the issuer name
needs no history index, and it forces reissuance after every name operation,
renewal included; that was this draft's earlier rule. The adopted rule
verifies the issuer name's history instead: grants survive renewals, at the
price of a transaction index and complete history on every verifier. A type-only executor cannot provide a shared global budget
across independently operated services.

## Security consequences

The name resolver, issuer registration pin and history walk, grantee-owner proof, receipt pins, service custody and durable
accounting form separate boundaries. A correct request signature proves neither
fresh ownership nor remaining budget. A name value cannot attest its own owner.
Expiry, unavailable chain data and unsupported units refuse admission without
turning a transient read failure into proved name-output closure. Reorgs
and revocation can race a completed external effect and cannot undo it. Raw
issuer, money-key or upstream-secret compromise remains outside service limits.

Replacing a leaked grant key stops an issuer's grants more slowly and less
finally than a seal spend stops one grant. The name rule of section 3 gives
its verdict on the active chain: a pending update at most suspends admission,
under an observation profile that is not defined, and a reorganisation that
removes a confirmed update makes the grants admissible again. A validated
issuer spend of a seal closes its grant durably from the mempool (section
5.1). The gap is stated under Open questions.

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
| Issuer history from the bound registration with unchanged owner and `swarma` since the committed block, matching current grantee owner and listed channel key on fresh unexpired names | Changed issuer owner or `swarma` on that stretch, grantee-owner mismatch, value-only owner assertion, unsupported proof, removed key or stale/expired/missing name: no effect. |
| Arbitrary namespace with supported owner proof | Prefix-only admission or rejection is wrong; malformed exact names still refuse under the name profile. |
| Issuer renewal, `nostr` update or owner-member update after issuance, checked by a newly started verifier | The grant stays live; closing it for a renewal is wrong. Issuer transfer, transfer-and-return, grant-key change and change-and-return are found in the history and refuse without local memory. |
| History walk that reaches the bound registration through the transaction index | A walk that ends at another registration (expiry and re-registration, same spelling, same key), an incomplete walk, or a node without the index refuses; a remembered walked output is a cache, and a presenter-supplied history is not accepted. |
| An owner or grant-key change that stays in the active chain, checked by a verifier that saw it and by one that starts afterwards | Both refuse at every check, also after the key returned; admitting on the later return is wrong. |
| The same change orphaned by a reorganisation, with `R` and the issuance kept and an unchanged history on the new chain | Both verifiers admit; a verifier that keeps a durable name closure from the orphaned branch is wrong, and so is one that reuses a cached walk across the reorganisation. A seal spend it saw in the mempool still closes durably. |
| A grant whose window covers the whole term with hourly limit periods | Requiring a new grant, seal or issuance record at a period boundary is wrong; admission at `H == not_after_height` refuses. |
| A counted payment displaced and seen again as the same valid transaction, then confirmed within `N` blocks | Revoking on the displacement is wrong. The same coins spent by another transaction revoke. An unavailable node or an absent transaction without a conflicting spend proves neither and revokes nothing. |
| Same-owner grantee renewal and a newly listed supported channel key under the same grant | Refusing solely because the grantee output changed is wrong; accepting a removed key or mismatched owner is wrong. Current-owner equality alone proves no permanent transfer-and-return history. |
| Exact executor name/key and its allocated budget | Wrong executor of the same type, reused full budget at a second executor, partition overspend or single-use executor substitution: no effect. |
| Replicas sharing one authoritative journal; recovery with chain evidence | Independent journals, lost journal authority, concurrent duplicate or uncertain retry: no second reservation/effect. |
| Healthy independent node observations and action-specific age policy | Lagging/conflicting nodes or exceeded risk cutoff refuse; a healthy gap under the decided cutoff alone is not node failure. |
| Recent block committed in signed grant and verified on the selected chain | Seal confirmation alone proves no signing-time lower bound; unknown, stale or wrong-branch block reference refuses under the selected profile. |
| W with native P2WPKH/SIGHASH_ALL inputs, confirmed ordinary funding and validated linkage/payment dependencies | One legacy or wrapped input, another sighash mode, witness marker alone, unproved parent or arbitrary unconfirmed funding refuses; no effect before required confirmations. |
| W with a permitted unconfirmed parent (the transaction that creates the linkage output, or a same-chain payment) whose inputs are all fully signed native P2WPKH with SIGHASH_ALL and whose funding ancestry ends at confirmed outputs (section 1.1) | The same parent with one legacy or wrapped input of its own refuses: section 1.1 allows it only fully signed native P2WPKH inputs. The same parent funded through a further unconfirmed transaction that has a legacy or wrapped input refuses as well, also when that transaction spends confirmed outputs. For a legacy input the reason is that a third party could change the transaction's txid and with it every dependent reference; a wrapped input refuses because W admits native inputs only. |
| L with confirmed referenced outpoints and an anchor built after seal confirmation | An unconfirmed reference, dependent chain or same-block seal/anchor construction refuses. A changed parent requires reissuance; no silent txid substitution or unsafe admission. |
| Matching authenticated chain/profile pin and identical grant checks under W and L | Unknown profile, profile substitution or automatic fallback refuses. Account-based chains have no seal profile here. |
| Administrator-owned sealed config, service-group read-only access and matching manifest hash | Writable service config or a hash mismatch forbids startup; operator ceilings cannot change through a runtime override. New reviewed packages remain the authorized change path. |
| Valid v3 and independently valid v4 fixtures | Version/domain substitution, ambiguous recipient mode, name without owner pin and silent downgrade: reject without changing preserved v3 results. |
| Independent proxy observation and durable remaining allowance | Gateway-only authority assertion, spent seal, conflicting concurrent reservations or uncertain retry: no second effect or overspending. |
| Matching issuer registration and owner key in grant, agent pointer and independent verifier pins | Expiry/re-registration, same-key new registration, pointer-only or presenter-chosen pin replacement refuses; a renewal keeps grant, pointer and pins as they are. |
| Complete validated objects and distinct typed signing domains | Caller-supplied digest, wrong object tag/version, malformed or changed canonical bytes refuse without a signature/effect; current static provenance audit does not replace these successor vectors. |
| Exact-unit numeric values within the chosen range or string schema | Overflow, parser rounding, duplicate properties, invalid Unicode and silent number/string conversion refuse; include URL escaping and non-ASCII ordering fixtures. |
| Valid issuer-branch mempool evidence durably recorded, then restart/replacement | Permanent refusal survives eviction and a competing grantee use-spend. A valid use-branch spend alone must not be mislabeled as issuer closure; transient read/tip errors create no closure. |
| Evidence reaching both signed confirmation minimum and operator risk floor | Insufficient depth under either floor refuses; applying MIN or silently equating NMC/BTC/LTC depth is wrong. |
| Typed endorsement for the exact per-seal key/script/outpoint | Different seal, swapped endorsement, untrusted issuer or substituted script refuses; separate valid per-seal keys remain admissible. |
| Explicit supported admission profile and its required publication evidence | An unpublished preparation refuses in anchored mode; evidence failure cannot activate no-block-wait mode. |

The additional pre-freeze rules need these paired public vectors. These are
planned assertions, not results from a chain validator or policy evaluator:

| Valid control | Refusal or invariant to assert |
| --- | --- |
| Separately signed grant and complete typed invocation | Substituted subject, command, arguments, proof order, nonce, times or executor fails the request binding; no new reservation/effect. |
| Grant executor = invocation executor = authenticated service pin | Wrong executor, including another service of the same type, refuses without effect or new allocation. |
| One granted action from the set under its live seal | An action outside the sealed set refuses; validated issuer closure refuses every action in that set, without relabeling a valid grantee use-spend. |
| Trusted root, constant subject and exact audience-to-issuer alignment | A self-selected root, changed subject or wrong next issuer refuses even with otherwise valid signatures. |
| Direct depth-1 grant; depth-2 explicitly authorized issuance path | A third authority link, duplicate link or cycle refuses before any new reservation/effect. |
| Explicit issue capability covering this child and its descendant action | Ordinary action authority, audience-key possession or re-delegation without issue capability refuses. |
| A child whose countable conditions are within its parent's and whose contract text equals the parent's | A child with a wider action set or a higher ceiling refuses mechanically. A child whose textual scope differs from the parent's is not shown to be within it by this LIP; treating the mechanical check as covering the text is wrong. |
| Narrower child action set, window and numeric ceilings; actual request fits every link | Wider child, larger ceiling or an invocation violating any ancestor constraint refuses, without trusting the child's attenuation assertion. |
| Child commits the exact issue-capability parent ID | A substituted parent or alternative path cannot bypass that parent's closure; dependent admission refuses. |
| Every link independently passes current names, issuance and seal checks | A closed seal, changed issuer instance or unproved/stale ancestor refuses even when the child alone passes. |
| Complete ordered proof bundle with receiver-recomputed IDs | Unresolved proof, recomputed-ID mismatch, ambiguous reference or path-order mismatch refuses; a bundle/cache alone cannot supply live-seal evidence. |
| Child budget within parent; serialized direct and sibling usage fits all ancestor ceilings | Child budget above parent or concurrent sibling/direct overspend refuses the excess request; no effect or newly authorized partial allocation on failure. |
| Same authoritative journal survives an exact retry and restart | Re-signing, another object ID, reissuance or replica-local reset cannot recreate consumed ancestor allowance or a second logical effect. |
| Explicit signed partitions assigned to independent executors | Two journals using the full same parent remainder refuse; each executor can use only its partition. |
| Known exact leaf command and a registered protocol command | Prefix/top-command admission, an unknown leaf or provider allocation under reserved `swarma/` refuses. |
| Signed descriptive metadata beside complete authority fields | Unsigned metadata mutation fails signature validation; signed metadata-only name/type/key/limit/issue assertions cannot add authority or replace pins. |
| Supported existing typed limits with no required future policy form | A required reserved `policy` kind refuses while its separate profile/evaluator is absent; no ignored constraint or unlimited fallback. |
| Matching signed type/version, canonical schema and application hash domain | Unsigned-label substitution, wrong type/version/tag, noncanonical encoding or unknown schema refuses. |
| Same canonical signed object carried in different bundles | All compute the same profile-defined ID; an asserted alternate ID or wrapper-derived identity refuses. |
| Valid strict BIP-340 signature, including another valid signing nonce | Invalid length/range/parity or changed-message signature refuses; a legitimately re-signed payload still cannot reset a logical request, seal or budget. |
| Nonempty half-open intersection of link height windows, all links live at execution | Empty/widened child interval, expired middle link or expiry during observation work refuses new admission; keep any existing uncertain reservation. |
| `iat <= now < exp` and `not_before_height <= H < not_after_height` at the effect boundary | Future `iat`, null/unbounded bound, added grace in blocks or time, `now == exp` or `H == not_after_height` refuses new admission; no inclusive-end weakening. |
| Height window at or above the committed recent block's height | `not_before_height` below that block's height, a window given in seconds, or a date used as an admission input refuses; a long block gap alone neither closes nor extends the window, and the freshness cutoffs still apply. |
| Grant by key with no recipient name, its request verified under the signed key with no recipient-name read; grant by name with name and owner key and no request key | Both a request key and a recipient name, neither of them, or a name carried as metadata refuses; a by-key request under another key refuses; requiring a channel lookup for a grant by key is wrong; a v3 `grantee_name` reading is not applied to v4. |
| Name-mode request signed by the key the name currently yields for the Nostr channel | A former channel key, another `nostr.names` entry, a channel without a profile, or a value that yields no key refuses without closure; an owner-key mismatch refuses even when the channel key matches. |
| Revocable-only seal on a single-key output of a per-seal key, behind a valid typed endorsement, whatever its derivation path | Reuse of a seal index by the signer, a seal paid to the grant key in v4, or an endorsement that names another key, script or outpoint refuses; the verifier never requires path knowledge. |
| Single-use seal whose script has distinct issuer and grantee branches: use by the grantee's own key, and a validated issuer closure | A single-key output offered as a single-use seal, one shared key for both branches, or a caller's branch label in place of script evidence refuses. |
| Preserved v3 and wallet-v1 IDs, domains and their separate single-use commitments | Applying successor ID/request rules to historical bytes refuses substitution; legacy evidence and replay outcomes remain unchanged. |

Publish canonical input bytes, typed digests, public keys/signatures, expected
errors and state/journal transitions together with a deterministic runner.
Include known-invalid controls proving the runner catches each claimed invariant,
plus valid neighbours. A second Swift implementation must consume the same
fixtures independently; agreement between two implementations alone is not the
oracle. Freeze historical v0.1 fixtures and report successor results separately.
This is a conformance plan, not a published runner or interoperability result.

## Open questions

- **The name rule as an emergency stop** (a gap found in review). The grant
  key leaks, and the name owner broadcasts an update that replaces it. The
  walk of section 3 runs on the active chain, so while the update is
  unconfirmed it finds no change, and every grant under the leaked key stays
  admissible. Section 3 lets a pending name spend suspend admission under
  the selected observation profile; no such profile is defined, and a
  suspension is no closure: it ends when the pending transaction is evicted
  or replaced. Once the update is confirmed, those grants refuse. If a
  reorganisation removes it, they are admissible again, because the verifier
  journals nothing for the name rule (rule 5). A validated issuer spend of
  one grant's seal closes that grant durably as soon as a verifier sees it
  in its mempool, and that closure survives eviction, replacement and a
  reorganisation (section 5.1). Stopping every grant of an issuer is
  therefore slower and less final than stopping one. For a grant that the
  thief signs, the owner has no seal to spend, because the thief endorses a
  seal key of its own (section 11); the name rule is then the stop the owner
  relies on. The decision of 2026-11-11 fixes the name rule and names
  neither case; the answer after a reorganisation is this draft's choice,
  like the start point of rule 3. Candidate fix, a proposal that the owners
  decide: a change of the owner or of `swarma` that the name owner signed
  and a verifier saw in its mempool closes the issuer's grants in that
  verifier's journal, as a seal spend does. With it goes a deployment rule:
  the fee of such an update is not paid with coins that a hot service can
  spend, so that a conflicting spend of the fee input cannot displace the
  update.
- Exact versioned bytes, signature domain, commitment/consent encoding, name
  registration reference, executor/single-use bindings, recent block field and
  cross-language vectors; the start point of the issuer-history constraint
  (this draft uses the committed recent block) and history proofs for a
  verifier without a full node.
- Invocation subject/command/argument and ordered-proof schema, principal
  encoding, time units/ranges, nonce/replay keys and bounded proof resolution;
  capability registry grammar, leaf assignments and existing-action mappings.
  The `swarma/` reservation and exact-match rule add no deployed action strings.
- Explicit issuance-capability profile; the v4 bytes of the breadth check
  that LIP-0014 drafts for v3 (section 12.6); structured scope and on-chain
  budget enforcement, which stay proposed; whether a re-delegating agent on
  v4 needs a grant key of its own, separate from its channel key;
  parent-ID binding, per-link issuance/seal evidence and atomic ancestor/sibling
  budget accounting, recovery and executor partitions. Depth is at most two
  signed authority links; exact wire/consent and accounting fixtures remain open.
- Signed metadata envelope, canonical object-ID preimages/signature inclusion,
  strict signature wire representation and cross-version journal bindings.
  The reserved future `policy` kind has no adopted evaluator or syntax.
- Owner-key encoding and supported scripts; proof of current unspent name
  outputs, reorg policy, channel profiles beyond Nostr and Matrix key support;
  whether a grant by name may restrict the channels it admits.
- Height windows: the recency bound between the committed block and the tip,
  and how the consent event's NIP-01 `created_at`, which stays in seconds,
  relates to the window.
- Implementation and qualification of the decided 60/90-minute risk cutoffs;
  explicit freshness/clock measure, independent-node health criteria and
  block-recency policy.
- Executor identity/key profile, partition validation and shared-journal
  consistency, recovery and anti-rollback requirements.
- Limit-kind wire registry, asset/model identities, numeric bounds, cost units,
  rounding, price binding and reservation/reconciliation rules per service.
- Exact authenticated W/L chain-pin encoding, dependency/input validation,
  migration from current P2PKH funding, chain-specific activation/risk rules,
  normative adoption and independently reviewed implementation. L requires a
  pinned non-SegWit chain before implementation qualification.
- Issuer registration pin provisioning; typed-hash registry,
  matched producer/verifier migration and per-field JCS integer/string schemas.
- Durable issuer-branch evidence, branch classification and replica recovery;
  value/depth tiers; explicit no-block-wait profile and its consent/evidence.
- T/L/A and same-chain payment dependency proofs under the explicit W exceptions
  and L confirmation barrier, transaction authorization and fee/settlement
  control; qualification of the per-seal derivation of section 11.1, the
  custody boundary of the account's extended public key under the decided
  non-hardened default, the output profile of the
  single-use seal, custody/recovery and endorsement format; public runner
  and independent Swift implementation.
