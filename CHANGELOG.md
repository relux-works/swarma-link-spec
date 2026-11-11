# Changelog

## 0.1.15 — 2026-11-11

Adds Draft LIP-0011, Termination for violation, by decisions of Ivan Oparin
of 2026-11-11; the co-author's agreement is pending. The contract carries the
hash of the moderation rules and names who applies them, a model or a person.
Each violation is a signed verdict record with the request hash, the violated
rule and the hash of the moderator's response; verdicts of one grant form a
chain. The transaction that spends the seal for a violation carries a
72-byte LIP-0005 frame with the new action `0x03`: a termination commitment
over `grant_id`, `contract_sha256` and `verdict_id`, and a blob-store pointer
to the verdict. Closure does not depend on the reference; a refund is a
contract term. LIP-0005 lists the action as proposed and not accepted by the
reference parser. Nothing is implemented; no canonical bytes for the records;
no change to v3, wallet-v1 or historical v0.1.

## 0.1.14 — 2026-11-11

Amends Draft LIP-0008 by three decisions of Ivan Oparin of 2026-11-11; the
co-author's agreement is pending.

Issuer name (section 3 rewritten; section 4 step 1 aligned): the grant binds
the issuer name's registration and owner key instead of its exact current
output. It lives while the name's updates change neither the owner nor the
`swarma` member. The verifier walks the name's history back to the bound
registration through the node's transaction index; an owner or `swarma`
change since the committed recent block refuses the grant for every verifier
of that chain without local memory. The verdict is relative to the active
chain and is not journalled: a change orphaned by a reorganisation no longer
refuses, for a fresh and an existing verifier alike, while a seal spend seen
in the mempool stays a durable closure. Renewal, a `nostr` update and owner-member updates
close nothing. The earlier exact-output rule moves to Alternatives. The start
point of the constrained stretch (the committed block) is this draft's
choice and is listed as open.

Term and period (new section 2.1): one grant per hire for the whole term in
block heights, about 13,000 blocks for three months; early end by seal
spend; an hour is a period of a limit and of payment, never a grant window.

Payment after a reorganisation (new section 2.2): a displaced payment that
stays valid is awaited for `N` blocks and nothing is revoked; the same coins
spent by a different transaction revoke. `N` and the still-unconfirmed case
are open. The reference booking service implements the earlier rule.

Conformance plan rows, open questions, key map, README and index follow. No
bytes, fixtures or implementation; v3, wallet-v1 and historical v0.1 are
unchanged.

## 0.1.13 — 2026-11-10

Amends Draft LIP-0008 in three places, following Ivan Oparin's decisions of
2026-11-10; the co-author's agreement is pending.

Recipient (new section 3.1): a v4 grant names its recipient by key or by name,
never both. A grant by key carries no recipient name; v3's unresolved
`grantee_name` has no v4 counterpart. A grant by name carries the name and its
owner key and no request key; the request key is read at admission from the
channel member of the name's current value, which is `nostr.names._` or the
key string for the Nostr channel (LIP-0010).

Validity (new section 7.1, section 12.5 aligned): the signed window is
`not_before_height` and `not_after_height`, half-open, compared with the height
of the verifier's validated tip. The window may not open below the committed
recent block. Contracts show approximate dates for people; a date is never an
admission input. The invocation keeps `iat`/`exp` in clock time. States the
variance from the section 6 sample and the interplay with the 60/90-minute
freshness cutoffs.

Seal keys (new section 11.1): BIP-32 derivation in an account that holds only
seal keys, for the revocable-only seal on Namecoin:
`m/84'/7'/<seal-account>'/0/<i>` in profile W and
`m/44'/7'/<seal-account>'/0/<i>` in profile L. The single-use seal keeps its
two distinct branches and its output profile stays open. The signer holds the
extended private key; a watch-only node may hold the extended public key.
States the non-hardened-index weakness, its blast radius and the hardened
alternative. The verifier checks the typed endorsement and needs no path.

The admission outline of section 4 authenticates the request by the signed
recipient mode. Adds six paired conformance-plan rows and updates the open questions and the
key map. No bytes, fixtures, implementation or normative adoption; v3,
wallet-v1 and historical v0.1 are unchanged.

## 0.1.12 — 2026-11-10

Adds Draft LIP-0010, Name value. `swarma` is the only member of a name value
that Link defines: a reader ignores the owner's other top-level members and
refuses only a duplicate or a fold alias of `swarma` or `nostr`; parsing inside
`swarma` stays strict. The agent key is written once, in `nostr` in the NIP-05
shape, and `swarma.agent` keeps only the landlord pointer. A reader accepts the
key string and the NIP-05 object and derives the same key for `_`; a `nostr`
member it does not understand removes the key and never the authority. `d/`
stays discovery only; the deployment rule registers `d/<label>` with
`id/<label>` because the two names are unrelated on chain. Recomputes every
example against the 520-byte limit. Records Ivan Oparin's four decisions of
2026-11-10; the co-author's agreement is pending. No implementation, normative
adoption or change to LIP-0004 bytes or historical v0.1 evidence.

## 0.1.11 — 2026-11-10

Adds Draft LIP-0009, Replaceable services: compatible type interfaces, portable
data and accounting evidence, exclusive cut-over with replacement executor-bound
grants, Namecoin discovery, bounded prepaid liability and a Blossom-backed
`store.blob` first profile. Records Ivan Oparin's acceptance of the five RS1
design choices on 2026-11-10. Rebind, exact wire/export/accounting/payment
profiles and qualification remain separate; no existing native NMC/BTC/LTC BUD
or automatic budget/credit migration is claimed. This is specification/book
work, not an M5 or first-demo implementation requirement. No historical v0.1,
wallet-v1/v3 or existing v4 draft bytes change; no implementation is added.

Adds decision 0003 as v0.1 errata: a route-health precheck cannot suppress a
spent/unknown/failed seal-state result or its durable refuse-and-close rule.
Route-only failure alone creates no closure; the historical protocol body,
evidence and documented failed-write/crash limitation remain unchanged. This
clarifies §1.4 under existing §4 and decision 0002, without new runtime evidence.

## 0.1.10 — 2026-11-10

Adds pre-freeze Swarma requirements to Draft LIP-0008: separate signed
invocations; signed subject, command, arguments, ordered proof IDs, nonce,
times and concrete executor; explicit issuance-capability paths of at most
two authority links, fixed parent binding, at-use attenuation and per-ancestor
budget accounting. Each grant keeps its complete action set under one seal.

Aligns LIP-0007's lowercase slash-command naming and reserved `swarma/`
namespace. Requires signed but non-authoritative metadata, signed type/version
consistent with application hash domains, canonical object IDs and strict
BIP-340 signatures without assuming unique signatures per message. Defines
half-open time/intersection checks and receiver-recomputed proof bundles;
reserves a future `policy` kind without syntax or an evaluator.
Corrects LIP-0007's wallet-v1 action listing to wire `spend`, consistent with
LIP-0006; `pay` retains its grant-scope/executor meaning.

Adds paired conformance-plan cases for the new rules. UCAN is provenance only,
with no new dependency or compatibility claim. General agent sub-delegation
retains its separate both-owner gate. Exact wire/proof/accounting profiles,
canonical fixtures and the post-freeze spike remain open; no implementation,
runtime result, normative adoption or historical v0.1/v3/wallet-v1 change.

## 0.1.9 — 2026-11-10

Records owner acceptance on 2026-11-10 of the proposed Grant v4 change: replace
the 30-minute
stop with risk cutoffs of 60 minutes for money or irreversible actions and
90 minutes for other privileged actions, plus a node-health check requiring
at least two independent nodes to agree on the tip. This is decided design;
implementation follows in GV4. The reported basis remains 70.7 min/day beyond
the 30-minute cutoff over 137.2 days on one node, not service availability or
a future bound. Historical normative v0.1 and its 30-minute STOP stay unchanged.

## 0.1.8 — 2026-11-10

Adds Draft LIP-0007 for service types/actions and typed name self-declaration,
and Draft LIP-0008 for Grant v4: directly signed rental limits, mirrored
contract terms, operator-wide ceilings and name recipients pinned to current
output ownership before channel-key checks. Includes v3 compatibility and a
semantic conformance outline; exact wire bytes, ownership proofs and accounting
profiles remain open. Binds issuer closure to the exact name output, including
issuer renewal. Grantee names bind their owner key, permitting same-owner
renewal/channel rotation and checking current listed channel keys. General
agent sub-delegation stays a separate open both-owner decision. Scopes budgets/
single use to concrete executors with shared replica journals.
Records proposed 60/90-minute risk cutoffs alongside node health and corrects
LIP-0003's seal-time inference as an acceptance rule, with a recent-block
commitment proposed for v4. Records chain-pin-selected W/L construction:
W uses native P2WPKH/SIGHASH_ALL with explicit unconfirmed linkage/payment
dependencies; L references confirmed outputs and builds the anchor after seal
confirmation. Both keep the same grant checks and fail closed on changed
parents; current P2PKH funding alone qualifies neither construction. No implementation claim, normative adoption or historical
conformance change.

Second design review adds registration-instance pins across grant, agent pointer
and verifier; typed signing from validated full objects; durable validated
issuer-branch mempool closure; confirmation minima; dependent T/L/A issuance and
profile-specific timing; topology/trust boundaries and per-seal keys. Plans JCS exact
unit schemas, canonical/signature/error/state vectors, runner and independent
Swift verification. Static signing audit found both issuer paths recompute authenticated contract
hashes, with no demonstrated oracle. Matched role/version migration and
wire/profile decisions remain open; historical v0.1 is frozen, including its documented false closures.

The immutable-config decision assigns configuration to the administrator, with
service-group read-only access (file `0640`, directory `0750`), a pre-start
manifest hash check and new reviewed packages for ceiling changes. This is
accepted design without an implementation or host-qualification claim.

## 0.1.7 — 2026-11-10

Defines the common grant-gated service term and examples in LIP-0006. Records
delegated grant issuance as a capability requiring a separate authority and
delegation profile, outside wallet v1 and the current rental rehearsal. No new
wire action, normative adoption or conformance change.

## 0.1.6 — 2026-11-10

Adds an informative key map for the rental path and wallet service: separate
custodians, signing roles, rotation dependencies and compromise limits, with
a schematic authority diagram. Model caps are identified as signed contract
terms, without claiming the proposed integration is landed. No normative
change or proposal adoption. Historical profiles and evidence remain unchanged.

## 0.1.5 — 2026-11-10

Clarifies LIP-0004 section 6 after the main issuance funding fix: the V2 route
prepares framed main issuance plans with explicit pins and fees; the v1 payment
route remains regtest-only. Describes offline regression coverage and its
regtest observation projections without claiming mainnet qualification or
extending historical conformance evidence. No normative change or proposal
adoption.

## 0.1.4 — 2026-11-10

Reconciles Draft LIP-0004/0005 with the landed 72-byte issuance writer, exact
bare-commitment compatibility and completed-plan replay boundaries. Describes
optional typed social metadata in authority names and the separate discovery
mirror without granting it authority; removes unsupported blob/tracker name
field suggestions. Adds LIP-0006 (Draft), recording the wallet service v1 request,
unsigned single-use commitment, signed/pinned reads, reserved receive allocation,
receipts and recovery semantics. Historical LIP-0002 and v0.1 conformance evidence
are unchanged. No normative change or proposal adoption.

## 0.1.3 — 2026-11-09

Adds LIP-0004 (Draft): landlord grants — the agent name holds only its messaging key and a
pointer to its landlord; the landlord's grant key signs grants v3 that carry the renter's signed
consent event and the landlord's countersignature; one mandatory on-chain commitment per grant;
funding never from the seal script. Adds LIP-0005 (Draft): an OP_RETURN locator micro-protocol
(own protocol id, action, location type and pointer), with the bare v0.1 anchor kept as legacy.
No normative change.

## 0.1.2 — 2026-11-09

Adds LIP-0003 (Draft): detached grants under an agent identity — the agent's name
holds only its keys; each grant is a certificate signed by the grant key with its
own seal and validity window; no per-grant transaction; closure on seal spend or
grant-key rotation. RELEASE.md renders LICENSE-MIT too. No normative change.

## 0.1.1 — 2026-11-09

Improvement proposals are now Link Improvement Proposals (LIPs): `cips/` is
`lips/`, CIP-0001 is LIP-0001 and CIP-0002 is LIP-0002. No normative change.

## 0.1.0 — 2026-11-08

First public draft. Names, issuance, observation and revocation as proved by
the first Namecoin mainnet experiment; conformance cases and mainnet vectors;
decisions 0001-0002; CIP-0001 (process) and CIP-0002 (single-use grants,
Draft, with regtest and mainnet evidence).
