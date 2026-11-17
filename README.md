# Swarma Link: Human-to-Agent Mandates in an Untrusted Environment

**Version:** 0.1.57

**Date:** 2026-11-17

**Status:** Draft

**Authors:** Alexey Grigorev, Ivan Oparin

**License:** text under CC BY 4.0; code under MIT. See [LICENSE.md](LICENSE.md).

Swarma Link binds participant keys to names on a public chain and carries
grants between participants through that chain, so that a verifier on another
machine can check a grant without trusting the issuer's server or the
transport. Version 0.1 is deliberately small: it fixes only what the first
mainnet experiment proved, on Namecoin, with one issuer, one grantee and a
full-node verifier.

Out of scope here, specified elsewhere and referenced by name:

| Concern | Owner |
|---|---|
| Grant (certificate) envelope, signing and offline verification | keyvault |
| Message envelopes between agents | waggle |
| Trust policy: who may issue what to whom | curator-trust |

## Specification set

| Part | Role |
|---|---|
| [Names](protocol/names.md) | Normative: Namecoin name binding and value format |
| [Issuance](protocol/issuance.md) | Normative: seal, anchor and the issuance transaction |
| [Observation](protocol/observation.md) | Normative: how a verifier reads the chain and decides |
| [Revocation](protocol/revocation.md) | Normative: seal spend closes the grant; watcher states pending and final |
| [Conformance](conformance/README.md) | Normative classes and the v0.1 evidence vectors |
| [Key map](KEY-MAP.md) | Informative: custody, rotation and compromise boundaries for rental and wallet keys |
| [Key registry](KEY-REGISTRY.md) | Draft: the one list of every key the specification names, with owner, holder, use, danger level and recovery; each entry has the status of the part that defines its key |
| [`lips/`](lips/) | Link Improvement Proposals (LIPs; not normative until adopted) |
| [`RELEASE.md`](RELEASE.md) | How each revision is released with its PDF |
| [`decisions/`](decisions/) | Adopted design decisions with context and consequences |

The normative keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL
NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**,
and **OPTIONAL** are interpreted as described by RFC 2119 and RFC 8174 when,
and only when, they appear in all capitals.

Prose defines behaviour; vectors define exact values and required outcomes.
If they disagree, the release is defective; an implementation is never the
normative oracle.

## Status of v0.1

v0.1 describes the shape that ran on Namecoin mainnet on 2026-11-08 (two full
cycles, see [conformance](conformance/README.md)). Known gaps are listed in each
part under "Limitations" and are not hidden by the normative text.

The normative v0.1 profile and evidence are frozen as historical. Its permanent
read-failure and tip-change closures remain recorded, not recommended for a new
working profile. Successor proposals distinguish transient refusal from proved
closure and require their own adoption and conformance evidence.

[Decision 0003](decisions/0003-seal-check-precedence.md) clarifies the historical
v0.1 precheck wording: route readiness alone creates no closure, but every
spent, unknown or failed seal-state read, including in a precheck, follows
Observation §4 and refuses/closes. Historical protocol files remain unchanged.

## Draft profiles and design decisions in v0.1.57

The [child-issuer integration proposals](lips/LIP-0014-source-contract-proposals.md)
collect proposed readings of the remaining identity, contract/profile,
O1–O8 and ordinal-count inputs. Each remains **PROPOSED**, with an explicit
acceptance condition and paired positive/forbidden cases. The companion
carries version 0.1.56's decided corrections and worker-name rule as its
baseline; those are not new proposals. It changes no existing rule, wire
member or implementation, and supplies no native or end-to-end qualification.

This revision reconciles informative draft descriptions with the public
implementation: [LIP-0004](lips/LIP-0004-landlord-grants.md) covers landlord
grants, optional social name metadata and separate discovery;
[LIP-0005](lips/LIP-0005-op-return-locator.md) records the landed framed writer
and exact bare compatibility; [LIP-0006](lips/LIP-0006-grant-gated-actions.md)
describes grant-gated services and the concrete wallet service v1 profile,
with examples and a separately scoped delegated-issuance capability.

[LIP-0007](lips/LIP-0007-service-types.md) proposes service types, action tables
and a typed self-declaration in a service's Namecoin value.
[LIP-0008](lips/LIP-0008-grant-v4.md) proposes Grant v4 signed rental limits,
an issuer name pinned by registration and owner key with a history walk,
owner-pinned recipients and concrete executor budgets.
It also records issuer-instance renewal pins, typed self-computed signing
digests, durable validated issuer-branch mempool closure, value-dependent
confirmation minima, per-seal keys, a topology/threat model and a dependent
issuance evaluation. Risk-tier freshness is decided design as of 2026-11-10;
implementation follows in GV4. The signing-time-bound correction remains a
proposal. Canonical/signature/error/state vectors, a public runner and
an independent Swift implementation are planned. These two proposals
specify design semantics with unresolved wire/proof details; they do not
reconcile a v4 implementation or assert interoperability.

The v4 pre-freeze requirements now include a separate signed invocation,
bounded explicit issuance-capability paths (at most two authority links),
at-use attenuation and ancestor budget accounting, exact service commands,
non-authoritative signed metadata, typed envelopes, canonical object IDs,
half-open time windows and receiver-verified proof bundles. The complete
action set stays under one seal and each grant signs its concrete executor.
Agent-issued child grants are decided as part of the protocol (section 12.6,
2026-11-11): an agent issues one only under a grant with the right of
re-delegation, and a child is never broader than its parent. Both owners
concur. Issuance by the operator's signer is implemented first; re-delegation
follows once the breadth check is designed. Scope written in words is not
checked by a verifier; a separate check by a notary is the decided mechanism,
and LIP-0012 proposes the notary. Since 2026-11-12 a notary attestation is
mandatory for every child, whatever its scope (LIP-0014).
A reserved stateless `policy` form has no adopted syntax or evaluator. These
are Swarma requirements with UCAN provenance, not UCAN compatibility; exact
wire profiles and the post-freeze qualification spike remain open.

Three amendments of 2026-11-10 follow Ivan Oparin's decisions and await the
co-author's agreement. A v4 grant names its recipient by key or by name and
carries no recipient name as metadata; in the name mode the request key is
read from the channel member of the name's current value, `nostr.names._` for
the Nostr channel. The signed window is a pair of block heights compared with
the validated tip, with approximate dates shown in the contract for people.
Keys of revocable-only seals are derived under BIP-32 in a dedicated account,
on Namecoin by the BIP-84 layout in profile W and the BIP-44 layout in
profile L with coin type 7; the single-use seal keeps two distinct branches
and its output profile stays open. The verifier checks the typed endorsement
and needs no path; Draft text of 2026-11-16 moves the seal key into the grant
and drops the endorsement (LIP-0008 section 11.4). These remain Draft semantics without bytes, fixtures or
an implementation.

Decisions of 2026-11-11 by Ivan Oparin change three rules of the v4 draft.
The issuer name is bound by its registration and owner key: a grant lives
while the name's updates change neither the owner nor `swarma`, the verifier
walks the name's history through its transaction index on the active chain,
and a renewal closes nothing. A grant covers the whole term in blocks, with
the hour as a limit and payment period only. The hire decision of 2026-11-15,
in force in version 0.1.52, requires a contract plus at least TEXT and
EFFECT grants (LIP-0008 section 2.1). A counted payment whose block is
displaced is awaited for `N` blocks while it stays valid, and the grant is
revoked when the same coins are spent differently. The co-author's agreement
is pending; no implementation follows these rules yet.

[LIP-0011](lips/LIP-0011-termination-for-violation.md) proposes termination
for violation: the contract carries the hash of the moderation rules and names
the applier, a model or a person; each violation is a signed verdict record
with the request hash, the violated rule and the response hash; the seal spend
refers to the verdict in a LIP-0005 frame with action `0x03`. Closure still
follows the seal spend alone, and a refund is a contract term. It records Ivan
Oparin's decisions of 2026-11-11 and awaits the co-author's agreement. Nothing
of it is implemented.

[LIP-0012](lips/LIP-0012-notary.md) proposes the notary: an additional link
that certifies a grant and can revoke it, performed by an agent or a person.
For a child grant it certifies that the child does not exceed its parent,
including the conditions written in words. The mechanism, a separate
attestation with the notary's own seal, follows the laboratory comparison and
is the draft's proposal. It records Ivan Oparin's decisions of 2026-11-11 and
awaits the co-author's agreement. Nothing of it is implemented in a grant
profile.

On 2026-11-11 Ivan Oparin also decided six points that the drafts had
listed as open. In LIP-0010: a duplicate or aliased `nostr` refuses the whole
value, and the pair rule covers every `id/` name with a `d/` counterpart. In
LIP-0008: a window may not open below the committed block's height; the
invocation's `iat`/`exp` stay in clock time; the revocable-only seal uses the
single-key script of its construction profile; non-hardened seal indices are
the default, with the extended public key as the operator's secret. The
co-author's agreement on all of them is pending.

[LIP-0013](lips/LIP-0013-trust-contract.md) proposes the trust contract
profile `swarma-trust-contract/1` for Goal 1, trust between our own agents on
Grant v3. It defines only the preimage of the v3 `contract_sha256`: four
actions, `instruct`, `land`, `review` and `spend`, the v3 scope and budget each
one implies, and the consent tags of a trust grant. No v3 byte, signing domain
or `rental.Check` rule changes. It also proposes the kind-8185 signed
instruction envelope and the order of an executor's admission checks; an
executor stays in shadow mode, where peer messages remain data, until the
first proof has passed and both owners approve enforcing mode. Draft
vectors in [`vectors/LIP-0013/`](vectors/LIP-0013/) are recomputed by the
reference checker in [`tools/trustcheck`](tools/trustcheck). Nothing of it is
implemented in a product.

[LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) proposes
notary-certified re-delegation and records the owners' decisions of 2026-11-12.
Every child grant is admitted only with a valid notary attestation, and every
verifier still checks the countable conditions of the child itself: a wider
child refuses for that reason even when it is certified. The one exception is
J9, decided and agreed by both owners on 2026-11-15: a v4 child of a row
without a certifier, which a parent may hold only inside one owner, needs no
attestation (LIP-0014 section 8.3). The parent's signed
right of re-delegation names one to four notaries, each by its `id/` name, the
registration of that name and its owner key, and it holds one row for each
child that the grant permits. Each notary publishes its attestation key in its
own name, in a `swarma` shape that a Draft amendment of LIP-0010 proposes. The
notary is neither the delegator nor the delegatee. On Grant v3 the landlord's
signer issues the child on a signed request of the parent's grantee, under
contract profile `swarma-trust-contract/2`, and no v3 byte changes. The draft
proposes the attestation object, its anchor as LIP-0005 action `0x04`, the
order of an executor's checks and the refusal codes. It belongs to the second
phase of Goal 1: after the first proof, in shadow mode first, and no part of
the first proof. Nothing of it is implemented.

The [key map](KEY-MAP.md) records four owners' decisions of 2026-11-12: a
principal has three keys, the name-owner key, the Nostr key and the grant
key, without an administrative key; an agent has its own name whose owner
key its operator holds; only an owner creates an identity; and sections of
an agent host's configuration are not signed until a trust anchor exists.
It also restates four Grant v3 rules for deployments. A name is written only
in the exact LIP-0004 values until LIP-0010 readers are deployed, because
one additional member makes every v3 grant under that name refuse. Grant v3
binds no owner key, so a transfer of a landlord name closes nothing there,
while a change of the grant key ends every grant signed by the old key; a
table gives the effect of each name change on v3 and on v4. No agent holds a
grant key on v3. The landlord pointer is a name on v3 and binds a
registration and owner key only in v4. Three requirements on a key service
follow: a grant-key purpose, presence per signature and typed display. By
Ivan Oparin's decision of 2026-11-12 the landlord grant key is held, for the
interim, as a software secp256k1 item in the Mac Keychain, read under Touch
ID per signature with every signed field shown first; the keyvault's BIP-85
path is the later target, once its grant-signing purpose is qualified.

Two further drafts are proposals that both owners decide. Ivan Oparin
accepted their direction as a whole on 2026-11-14, and the co-author's
agreement is pending. [LIP-0015](lips/LIP-0015-trust-root-and-statements.md) proposes the
trust anchor that signed configuration waits for: a pin written at
installation outside the agent's reach, the root name resolved on the
loader's own node, and typed statements signed by the grant key under
separate signing domains, for configuration sections, root rotation and
certificates that bind other keys to a name. A statement binds and gives no
authority. [LIP-0016](lips/LIP-0016-certificate-store.md) proposes the store
for such statements: signed records, a signed head over the complete set
anchored as LIP-0005 action `0x06`, each anchor spending the previous head's
output, and hosts trusted for availability only. The key map adds a proposed
key layout, with the name-owner key on a seed of its own, and a proposed
flow for registering an agent's identity in which no private key leaves its
host. LIP-0010 section 8 adds a proposed plan for the 520 bytes of a value.
An organization identity and release statements for binaries are sketches
in LIP-0015 and are not proposed.

Two independent reviews of the design found eight gaps, and version 0.1.24
recorded each as an open question. Each now has text, labelled J1 to J8.
Ivan Oparin decided them, J3, J6 and J8 on 2026-11-13 and J1, J2, J4, J5
and J7 on 2026-11-14. The co-author agreed to J1 and J3 on 2026-11-15; on
the other six the co-author's agreement is pending. One point of J5 is
agreed by both owners as well: in the first version of v4 a re-delegation
narrows only typed fields and appends no text. Nothing of the rest is
adopted before both owners agree. For it the rules in force stay beside the
Draft text as they are, and no gap is called closed for a property that its
text lists as open. Five decisions stand in LIP-0014. The parent signs rows
that fix the executor, the grantee, the cap and the certifier of each child;
on v4 each row also pins a coin that the issuance of its child must spend,
so that one child for each row holds on the active chain; the coin pays a
separate key, derived from the seed of the operator's signer (J1, section
9.1). Each row has one notary, with one succession of seals and a cause that
counts only when the notary's signature covers its frame; on v3 that narrows
D5, and on v4 each row names a stop coin of its notary whose spend ends the
row for every verifier that sees it (J2, section 10.1). A notary is pinned
by name, registration and owner key (J3, section 7.1). A delegation key that
the parent names signs children on v4 and nothing else, because the
messaging key never grants authority (J4, section 11.1). On v3 a child
carries its parent's scope text unchanged, and no executor performs a
landing or a payment automatically under a grant with a text: it refuses
such a request, and the owner's confirmation of one operation stays as an
exception. On v4 a child narrows only typed fields and appends no text (J5,
section 3.4). In LIP-0008 section 5.2 an owner-signed change of an issuer's
name that a verifier saw closes that issuer's grants durably (J6). In
LIP-0013 section 3.6 the service that holds an agent's key signs a run's
objects only under what its operator listed for the origin of that run; that
gate is a condition of enforcing mode and takes the place of presence for an
agent's key (J7). In LIP-0011 section 7 the signed invocation is the request
of a verdict (J8). No v3 byte changes, and neither does any rule or vector
of the profile `swarma-trust-contract/1`.

[LIP-0009](lips/LIP-0009-replaceable-services.md) proposes replaceable services:
compatible type profiles, portable state, fenced cut-over with replacement
executor-bound grants, Namecoin discovery and separate authorization,
accounting and settlement. It records Ivan Oparin's five accepted RS1 design
choices: start with `store.blob`; replacement grants before rebind; operator
reconciliation by default; small capped prepaid contracts;
native Blossom BUD-07 where offered plus a separately versioned grant-aware
NMC/BTC/LTC option. Exact profiles and independent conformance remain open.
This is spec/book work, not an M5 or first-demo implementation gate.

[LIP-0010](lips/LIP-0010-name-value.md) proposes the name value of the landlord
profile: `swarma` is the only member Link defines, the reader ignores the
owner's other members and stays strict inside `swarma`; the agent key is
written once, in `nostr` in the NIP-05 shape, and both published forms of
`nostr` yield the same key. `d/` stays discovery only, with a deployment rule
to register `d/<label>` together with `id/<label>`. A note of 2026-11-13
records that this pair is a convention outside Namecoin consensus and that
an additional convention with a single level of registration is under
consideration; it changes no rule. The LIP records Ivan Oparin's
four decisions of 2026-11-10 and awaits the co-author's agreement. No reader
implements these rules yet; LIP-0004 values keep their own rules.

Two further drafts of 2026-11-14 record decisions of Ivan Oparin and await
the co-author's agreement. [LIP-0017](lips/LIP-0017-contracts.md) makes the
contract an object of its own: one document that two or more parties sign,
with free text and machine members, whose identifier commits to a salt and
to a salted hash of each clause, so that single clauses can be disclosed.
A contract is anchored as LIP-0005 action `0x07` and may exist without any
grant, and every grant binds a contract. A grant's window lies inside its
contract's window, a framework contract covers several grants over time,
and a contract can name a seal whose script is its termination clause and
whose spend, with action `0x08`, ends every grant under it. Grant v3 does
not change. [LIP-0018](lips/LIP-0018-extension-guide.md) lists what a
proposal for a contract profile, a limit kind or an action name has to
state, and LIP-0008 section 2 names the further limit kinds of the same
decision, each with a meaning that is the draft's proposal. These are semantics without bytes, and nothing of them is
implemented.

Version 0.1.32 records five further directions of Ivan Oparin of
2026-11-14, with the co-author's agreement pending. LIP-0013 section 3.7
states the pattern for instructions across owners: the grantee is an agent
of the receiving owner, which signs the envelopes under the gate of
section 3.6, and a transport only carries. The key map describes a
personal key service for each person, records decision K6, a separate
authority key for grants issued to a person, and settles the scope of K2:
permanent roles have names, and a worker agent may stay key-only. LIP-0008
section 1 states that Grant v3 is frozen after the first public
demonstration and remains for verification once v4 is qualified.

Version 0.1.33 extends those two drafts. In LIP-0015 the pin and the
configuration statements get a first use, the signing of Curator profiles
and manifests; of the two Matrix kinds of a certificate statement
`matrix-cross-signing` is preferred; and keys of other transports get
kinds of their own through LIP-0018, which gains a list for them. In
LIP-0016 the draft answers the open questions of its first version, as
proposals: a Git provider whose files are the exact bytes of the head and
of the records, one head for one issuer, one anchor for one head, and no
verified set between a change of the grant key and the first head under
the new key. The vector set is described and not built.

Version 0.1.34 adds four things at Ivan Oparin's decisions of 2026-11-14,
with the co-author's agreement pending.
[LIP-0019](lips/LIP-0019-retrieval-by-hash.md) proposes how a reader
obtains an object that a locator names by its hash: a loader that takes
endpoints from its configuration or, under its operator's policy, from an
unsigned hint, fetches by SHA-256 and checks the hash, after which the
object is checked like a presented one. A presentation is not fetched: the
reader completes it from the fetched signed grant and an issuance locator. LIP-0008 section 11.2 lists the members of the seal-key
endorsement and the order of a verifier's checks, and section 11.3 has the
issuer's signer show, before issuance, that it can spend the seal. LIP-0008
also says that Grant v3 keeps its byte names while the prose and Grant v4
name the roles issuer, recipient and executor. Under LIP-0017 section 8 a
contract under which the platform starts an agent carries the hash of the
agreed configuration manifest, which the platform executes exactly.

Version 0.1.37 adds [LIP-0020](lips/LIP-0020-grant-v4-wire-registry.md),
the first proposal of bytes for Grant v4. It covers the layer that every v4
object shares: one canonical form, RFC 8785 over a restricted set of
values; two exact forms for an integer, so that no amount passes through a
binary64 number; a registry of seven object types, each with one identifier
that stands in the signed bytes and names its signing digest; the signed
form; an identifier that leaves the signature out; the consent of both
parties to a contract, with the rule for a recipient that a grant names by
name; what an issuance anchor commits to, in a LIP-0005 frame with payload
version `0x02`; and the pipelines of a reader with one order of refusals.
Two points of its consent rules were decided on 2026-11-14 under Ivan
Oparin's delegation; he may override them, and the co-author's agreement is
pending. The state of a name at the issuance snapshot authorises, and no
earlier or later state does. And a consent is bound to its contract, its
issuer and its recipient, is used for one issuance, and is at most 72 hours
old when the issuer starts that issuance. Every other rule is the draft's
proposal, and neither owner has decided a byte of it. The grant, the
invocation, the receipt, the seal-key endorsement and the successor of the
notary attestation have an identifier and no members, and no reader accepts
one of them yet. The 205 vectors in [`vectors/LIP-0020/`](vectors/LIP-0020/)
were computed by two implementations that share no code, and no checker for
them is published.

Version 0.1.38 corrects one order in LIP-0020. An issuance is checked in
six steps, and the mode of the grant with the presence of the evidence
outpoint is checked before the consent event. A presentation for a
recipient by name that lacks the outpoint therefore refuses as
`ISSUANCE_MODE`; under the order of 0.1.37 the consent step came first and
could only report `CONSENT_EVIDENCE` for an output that it was never given.
Fourteen vectors hold the order, and the file now has 219.

Version 0.1.39 adds
[LIP-0021](lips/LIP-0021-name-ownership-and-history.md), the first ownership
and history profile for Grant v4, on Namecoin. LIP-0008 binds a grant to
the owner key of its issuer's name and left open how that key is written
and which output scripts it controls. The draft proposes the owner pin as a
compressed public key; three exact prefixes of a name output and two
address scripts, which pay the hash of one key with and without a witness,
with three outcomes of a reading: controlled, another key, unsupported; a
writer check that reads the hash type of the name input; the comparison for
a live name; the walk of a name's history with an operator's bound; and,
for the issuer rule and for a recipient by name, five refusal codes with
their order. An unsupported script proves nothing: the rule that needed the
reading refuses, and the script is never taken for a transfer. One point that the profile serves was decided on 2026-11-14
under Ivan Oparin's delegation, open to his override and awaiting the
co-author: authorisation by name at issuance is judged under such a
profile. Every rule of the profile is the draft's proposal, and neither
owner has decided one. The 140 vectors in
[`vectors/LIP-0021/`](vectors/LIP-0021/) state octets and facts and read no
chain; no node was run for the draft, and no checker for the vectors is
published.

Version 0.1.40 adds
[LIP-0022](lips/LIP-0022-observation-freshness-and-risk.md), the first
observation, freshness and risk profile for Grant v4, on Namecoin. The
cutoffs of 60 and 90 minutes and the two independent nodes that agree on
the tip are decided design in LIP-0008, which left the age measure, the
clocks and the criteria for the nodes open. The draft proposes: one
observation between two reads of the same tip, void and without closure
when the tip moved; comparison nodes that the configuration names, of
which one of another source has the reading node's tip or the block below
it on the same chain, and of which no healthy one has a tip that conflicts;
the age of the tip as the larger of two ages, the verifier's clock minus
the header time and the clock minus the verifier's own first sight of the
tip, which it keeps durably, with a guard against a clock that went back
and a bound on a header that is ahead; the recent block of a grant on the
active chain, with the issuance anchor confirmed above it within a window;
the arithmetic of confirmation depth; and nine refusal codes with their
order. Every rule is the draft's proposal, and neither owner has decided
one. Three of its numbers are provisional and are not to be frozen before a
run on a real host has measured what they bound: 600 seconds for a header
that is ahead, one block of lag, and 432 blocks between the recent block
and the anchor. The 97 vectors in
[`vectors/LIP-0022/`](vectors/LIP-0022/) state tips, times and heights and
read no node; no node was run and no measurement was taken for the draft.

Version 0.1.41 adds [LIP-0023](lips/LIP-0023-witness-construction.md), a
first construction profile for Grant v4: the Witness profile of LIP-0008 on
Namecoin, in its narrowest useful form. A verifier takes the profile from
its own authenticated configuration. The anchor of every grant spends the
linkage output, which is the output that follows the seal in the seal
transaction, so that only the holder of the key of that one output can
publish the anchor. Every input of the two transactions spends a witness
key hash with a signature of hash type `01`.
The linkage output is the one parent that may be unconfirmed, and every
other input spends an output that is confirmed below its spender. An
unconfirmed payment output, which LIP-0008 permits, refuses under this
profile until a proposal says how a verifier authenticates it. An effect
needs a confirmed anchor. Thirteen refusal codes have an order; twelve of
their names are reasons that the reference laboratory already reports for
its own subset. Every rule is the draft's proposal, and neither owner has
decided one. The 63 vectors in [`vectors/LIP-0023/`](vectors/LIP-0023/)
state octets and facts and read no node; no node was run for the draft.

Version 0.1.42 adds [LIP-0024](lips/LIP-0024-seal-endorsement.md), the
octets of the seal-key endorsement. LIP-0008 section 11.2 fixes what an
endorsement states and the order in which a verifier checks it, by a
decision of Ivan Oparin of 2026-11-14 that awaits the co-author, and leaves
the bytes and the codes open. The draft proposes the nine members of
`swarma-seal-endorsement/1`, signed by the issuer's grant key, for a
revocable-only seal whose script is the witness key hash of its seal key.
It keeps the decided order: the output on the verifier's own node and its
script come before the signature, which is the one point where the order
differs from the pipeline of a signed object in LIP-0020, and the draft
says so. Five codes are new. The provisioning and custody of the seal
account are open and before an owner; the draft proposes five points about
them and nothing more: seal and funding accounts are separate, the grant
key signs no transaction and pays no fee, the seal account is not the
account `m/84'/7'/0'`, no seal account is derived from a grant key, and
each account has a provisioning sitting and a wrapping of its own. Every
rule is the draft's proposal, and neither owner has decided one. The 47
vectors in [`vectors/LIP-0024/`](vectors/LIP-0024/) hold signed
endorsements under published test keys and read no node.

Version 0.1.43 adds [LIP-0025](lips/LIP-0025-journal-continuity.md), a
profile for a journal that must not go back unnoticed. LIP-0014 states the
contract of such a store for the ledger of a row and calls its form an open
deployment profile; LIP-0008 needs the same for its closure journals and
LIP-0020 for the record of a consumed consent. The draft proposes one form:
entries in the canonical form of LIP-0020 whose history is bound by hashes;
an outside record that takes a new state only as the successor of the exact
state that it holds, from the writer with the current token; a continuity
check with four outcomes, intact, pending, fenced and lost, in which equal
positions never suffice; and a recovery by starting anew, with a block
boundary whose header time lies more than two hours after the fencing. On
that form it defines the first journal, the issuer's journal of consumed
consents: one entry before the grant is signed, and after a loss every
consent that existed before the recovery counts as consumed. Every rule is
the draft's proposal, and neither owner has decided one. The draft selects
no store and no service for the outside record, and nothing of it was built
or run. The 66 vectors in [`vectors/LIP-0025/`](vectors/LIP-0025/) hold
histories, decision tables and twelve traces of the consent journal.

Version 0.1.44 adds [LIP-0026](lips/LIP-0026-rows-and-accounts.md), a first
profile for the rows of a v4 parent. The rows, their two ledgers and the
coin of a row are decided in LIP-0014 section 9.1; who funds the coin, the
account and the path of its key, and which counter an executor keeps under
which key are open there. The
draft proposes: what a row states, and a pool that bounds the rows for each
kind of limit; the checks of a child against the row of its ordinal, on
signed octets alone; a coin with a witness key hash script that is
confirmed at or below the parent's recent block and is no output of the
child's seal transaction, and an input of the child's anchor that spends
it; a row account of the signer, apart from
seals and funding, whose keys sign that one kind of input; and the accounts
of an executor's ledger, in which a request under a child debits the own
account of the child and the row of its parent, and never the parent's own
account. Every rule is the draft's proposal, and neither owner has decided
one. The 64 vectors of `rows-vectors.json` in
[`vectors/LIP-0026/`](vectors/LIP-0026/) state rows, coins and requests as
facts, among them a trace of one parent over three
executors; no node, no signer and no store was run for the draft.

Version 0.1.45 adds [LIP-0027](lips/LIP-0027-row-stop.md), a first profile
for the stop coin of a row. LIP-0014 section 10.1 decides, with the
co-author's agreement pending, that on v4 the notary of a row ends the row
for cause by spending a coin that the row names, and that every verifier
whose node shows the spend refuses the row. It names one code, for the
spent coin. The draft proposes: a stop coin with a witness key hash script
for each row, which is no coin of a row, no seal of the parent or of the
child, and not the output after either seal; three outcomes that
a verifier keeps apart, the coin unspent, the coin spent and the coin not
on the chain as the row states it, of which only the second records
something; the record of a row closed for cause as an entry of a journal of
LIP-0025, written when the verifier's own node shows the coin spent, and
permanent at that verifier; a verifier that cannot write the record and
then admits nothing until its operator has acted; and a stop account of the
notary whose keys sign one kind of input, with a spend whose fee nobody
else can take away. Every rule is the draft's proposal, and neither owner
has decided one. The 52 vectors in [`vectors/LIP-0027/`](vectors/LIP-0027/)
state facts and octets, among them the traces of a witness and of a
verifier that starts later; no node and no store was run for the draft.

Version 0.1.46 gives the contract profile `swarma-trust-contract/2` of
[LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) one member set.
Since version 0.1.31 the LIP had described the right of re-delegation twice:
with the lists of its first draft, and with the rows and the pins of a notary's
name that Ivan Oparin decided on 2026-11-14 and 2026-11-13 (J1, J3), as Draft
text that waited for the co-author. One profile string stood for two sets of
members. The co-author agreed to both decisions on 2026-11-15, and the first
set is removed. A right of re-delegation holds `depth`, `actions`, `budget`,
`slots`, `notaries` and `checkpoint`: one row for each child, with its
executor, grantee, cap and certifier, and one entry for each notary, with its
name, the registration of that name and its owner key. The attestation has
eighteen members; the two that added up a sum over siblings are gone. The
decisions J2, J4 and J5 still await the co-author and keep their Draft text.
The names, the bytes and the codes of the profile stay the draft's proposal.
The revision fixes them for an implementation and states what each of a
reader's nine rules owns and in which order it reports. Four points of form
are the draft's choice and belong to no decision: the owner pin of a notary as
a compressed public key, which is the form that LIP-0021 proposes; the range
of an output index; a largest integer; and that the key of a row is a valid
key. The 190 vectors in [`vectors/LIP-0014/`](vectors/LIP-0014/) hold 151
contracts and 39 pairs of a parent and a child. No checker for them is
published, and nothing of the profile is implemented.

Version 0.1.47 records four decisions of Ivan Oparin of 2026-11-15 on the rows
of a v4 parent, as Draft text. The co-author agreed to J9 on 2026-11-15, and
version 0.1.49 puts it in force. Version 0.1.51 puts the other three in force,
on Ivan Oparin's decision of 2026-11-16 not to wait for the co-author, whose
answer is folded in by amendment. A parent
states its rows in groups, a template with ranges of coins and one ordinal
across them, so that a parent can permit thousands of children (J12;
[LIP-0026](lips/LIP-0026-rows-and-accounts.md) section 8). A row may name the
recipient of its child by a class of landlords, each pinned like a notary, and
the executor then checks that the recipient's name is an agent of such a
landlord, that a key which the landlord lists holds it, and that such a key
wrote its value (J10; section 9). The landlord lists those keys (J11;
[LIP-0010](lips/LIP-0010-name-value.md) section 10): in version 0.1.51 in a
member `holders` of its own name value, and since version 0.1.53 in a
holders list off the value, one entry for each agent or station name, which
the value pins by hash and version. A row inside one owner may have no certifier, and its child then
needs no attestation; across owners a certifier stays mandatory (J9;
[LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) section 8.3 and
LIP-0026 section 10). The bounds of a group, the eight refusal codes of a class
and every rule that the sections mark as the draft's are proposals. Two
consequences are stated in place: in the inline form of version 0.1.51 a
change of `holders` changes the `swarma` member and so ends the v4 grants
that the landlord issued before it, which the list of version 0.1.53 no
longer does, and a holder that renews a name which was sent to it adopts
the value of that name.
The contract profile `swarma-trust-contract/2` of Grant v3 does not change. The
33 vectors in [`vectors/LIP-0010/`](vectors/LIP-0010/) hold name values, and
103 further vectors in [`vectors/LIP-0026/`](vectors/LIP-0026/) hold groups,
templates and admissions. No checker for them is published, and nothing of the
four decisions is implemented.

Version 0.1.48 adds [LIP-0028](lips/LIP-0028-sessions.md), Draft text for a
decision of Ivan Oparin of 2026-11-15 that awaits the co-author's agreement
(J13): a service whose client cannot sign its requests admits a session, and
the model proxy is the first case. The key holder of the recipient signs one
invocation that opens a session with a slot binding, a window of at most one
hour and limits within the grant. The service admits it like any invocation and
returns a bearer token of 32 random octets, which its journal binds to the
grant, the slot and the window. The LIP states the eight parts of the decision
first; the rules beyond them are the draft's proposals. Among those: before
every reservation in a session the service makes the checks of the proof path
again, in an observation of its own, so a spent seal stops the next request; a
repeated session-open request returns no token, also after the journal of the
service was started anew; the journal never holds the token; a token travels
only on a local socket or on a channel that authenticates the service and that
others cannot read; and the eleven refusal codes. A token works until the last
end of the window that the key holder signed, and every signed request sets
that end at most 3600 seconds ahead. Four consequences are stated in place: the
proof path has to allow the commands of a session, so the issuer decides
whether its authority may be used through a bearer; every process of a slot can
read the token, so a session equals a signature on every request only where the
slot holds runs of one origin; the binding by user id needs a local socket, and
how a harness with a base URL reaches one is open; and a grant that leaves the
key holder's table keeps its session for up to an hour. The LIP defines no
octets and adds no vector, because the invocation has no members yet. Until the
co-author agrees, a v4 service admits signed invocations alone. Nothing of it
is implemented.

Version 0.1.49 puts J9 in force, decided and agreed by both owners on
2026-11-15: a child needs an attestation only where its row names a certifier,
a v4 row without a certifier is valid only where its recipient constraint is
limited to the issuer's own landlord, across owners a certifier stays
mandatory, and a row without a certifier states no stop coin
([LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) section 8.3, rules
J9.1 to J9.4; [LIP-0026](lips/LIP-0026-rows-and-accounts.md) section 10). The
two recipient constraints that J9 admits, a class of exactly the issuer's
landlord and an exact name that passes the checks of a class against it, rest
on J10 and J11. Until version 0.1.51 put J10 and J11 in force, no child of a
row without a certifier was admitted, and every admitted v4 child was
certified. The
texts that restate D1 (LIP-0006, LIP-0008, LIP-0012) say how J9 narrows it on
v4. D8, J1 and the member `notary` of profile `swarma-trust-contract/2` do not
change; LIP-0014 section 8.3 states how each is read for a row without a
certifier. Grant v3 does not change, every v3 child is certified, and nothing
of J9 is implemented.

Version 0.1.50 adds [LIP-0029](lips/LIP-0029-owner-control.md), Draft text for
thirteen decisions that Ivan Oparin accepted on 2026-11-15 on owner control
(R4), written optimistically: the co-author's agreement was not awaited and is
pending. Section 1 now carries the labelled M0 transition of 2026-11-16;
free text directs work, and an effect happens only through typed fields that the executor's gate compares with the
actual arguments. The owner's name value pins, outside `swarma`, the hash and
version of a device list whose records hold a key, its algorithm (BIP-340 or
P-256), a claimed presence flag, a level ceiling and a revocation seal. The
envelope is `swarm-envelope/2` with three typed body kinds, its identifier and
replay journal exclude the signature, and a launch inherits the level of the
envelope that started it. At every level that level bounds what the run's key
holder signs under the agent's own grants: no effect at L0, and at L1 and L2
only the classes that the executor's policy admits at that level, within its
limits there; the key holder takes the policy from the owner's L2 device.
Policy lives in configuration sections signed by an L2
device; a device is revoked by the spend of its seal and added only by a name
update. The grant key grants to others only, no statement key is added, and the
authority key of a person leaves the key map in favour of device keys, which
closes R5. The LIP lists its conflicts with `swarm-envelope/2`, the platform
book and curator-spec for the owners, defines no vector, and needs a reviewed
change of `swarm-envelope/2` before any verifier admits its body kinds. Nothing
of it is implemented, and until the co-author agrees the texts it revises stand.

Version 0.1.51 adds Draft text for eleven decisions of Ivan Oparin of
2026-11-16, written optimistically: the co-author's agreement is pending, and
until it is given every text that they revise stands. A v4 grant carries its
seal key, so the separate seal-key endorsement is redundant, as the spec
review confirmed, and is dropped; every text that reads it points to
[LIP-0008](lips/LIP-0008-grant-v4.md) section 11.4. Every v4 parent names a
child-seal key, which is neither the grant key nor the delegation key and
which every child's seal pays
([LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) section 11.2).
Every statement set of an owner has its head in the owner's name value, and
only the last head confirmed in the active chain counts, after a
reorganisation too, while the refusals that a reader journaled stay
([LIP-0010](lips/LIP-0010-name-value.md) section 11;
[LIP-0016](lips/LIP-0016-certificate-store.md) section 3.1). The emergency
brake on v4 names its stops and their window before confirmation and after a
reorganisation, and reserves a UTXO of a cold wallet for the fee of an
emergency name update (LIP-0008 section 5.3). An administrator may overwrite
the trust-root pin after a stated delay, counted from the first notice that
names the effect height, and the old key can cancel until the pin takes effect; an
administrator account that rewrites the pin directly is outside the rule
([LIP-0015](lips/LIP-0015-trust-root-and-statements.md) section 5.1). The
authority frame reaches the agent in a separate channel; a signature on it
is NOT established (corrected in version 0.1.52)
([LIP-0013](lips/LIP-0013-trust-contract.md) section 3.4). In
[LIP-0029](lips/LIP-0029-owner-control.md), Figure 1 shows the device seal in
the words of the decision (section 8.3); the sender attaches the device list
when it changes and at first contact with a receiver, otherwise the envelope
carries the hash, an unknown hash refuses by name and the sender re-sends,
and the owner's domain and a Nostr replaceable event are secondary paths
(section 3.5); a Matrix device is an ordinary record at L1 without
presence, whose end-to-end encrypted events count only when bound to its
session, never when forwarded, restored from backup or sent in plaintext
(section 4.1); and an algorithm registry gives every device algorithm its
encodings, its presence semantics and its highest level, enforced per
algorithm value, with a strengthened L2 for Secure Enclave keys through a
signer qualified on a real Mac, of which only the Matrix entry has a verifier
in M5n (section 3.6).

Version 0.1.51 also puts J10, J11 and J12 in force on Ivan Oparin's decision
of 2026-11-16 not to wait for the co-author, whose answer is folded in by
amendment: groups of rows, the landlord class
([LIP-0026](lips/LIP-0026-rows-and-accounts.md) sections 8 and 9) and the list
`holders` ([LIP-0010](lips/LIP-0010-name-value.md) section 10). A child of a
row without a certifier (J9) is therefore admitted through the checks of a
class, where 0.1.49 admitted none. Nothing of version 0.1.51 is implemented,
and no vector outcome changes.

Version 0.1.53 replaces the member `holders` by a hash-pinned holders list
([LIP-0010](lips/LIP-0010-name-value.md) section 10), in force on an owner
decision of 2026-11-16 without the co-author's answer, which is folded in by
amendment. The landlord's name value pins the hash and the version of the
list in a member `swarma-holders`, outside `swarma`, on the method of the
LIP-0029 device list, and the list lives off the value with no cap of five.
It has one entry for each agent or station name: the name, the key that
holds it and a seal. A change of the list is a name update that ends no v4
grant, because a grant depends on the owner and on the `swarma` member, which
no longer holds the holders. The spend of an entry's seal revokes that one
name at every verifier that validates it on its own node, with no name
update; it ends no grant, and the name stays with its key holder. A seal
counts only while its funding output is confirmed, a verifier that cannot
validate the spend refuses without a closure, and until the fee of the
prepared spend is settled nobody claims the fast path. Names may be listed
ahead and kept in reserve. A verifier that cannot get the pinned list
refuses the child and falls back to nothing. The member of version 0.1.51
stays readable as the inline form for the transition, at a verifier that
never took a pinned list for that landlord. The entry of agent name, owner
pin and seal outpoint, the refusal of a current owner other than the pin,
and the answer to a stolen key by the spend of the seal of every entry with
that pin are owner decisions of 2026-11-16. A seal is bound for each
landlord, so a landlord that copies the seal of another landlord's entry
harms only itself, and a removed entry stays refused after a
reorganisation at every verifier that took the list which dropped it. The
bounds of a list, the nine new refusal codes beside four reused ones, and
every rule that the section marks NEW are this text's choices for the
owners. No vector of the list is published, and
no historical vector byte or outcome changes.

Version 0.1.52 records the specification-side reconciliation closures in
[Decision 0004](decisions/0004-reconciliation-closures.md). LIP-0029 and
LIP-0013 carry signed-at-minimum, encrypted-at-maximum communication, with
unsigned work delivered but labelled during the transitional stage M0, no
effect given to the unsigned message itself, and unsigned input ignored
after the M6 switch (LIP-0029 section 1). Which effects the key holder
signs for a run that unsigned work starts is open. Chain rules also apply
inside one host, which is one node. The LIP-0029 device list stays in its
existing format. The authority frame arrives in a separate channel, with
its signature unestablished; the dependent frame format and key are
withdrawn, and the draft's proposal of a local, unsigned frame stands.
LIP-0008 and LIP-0003 limit issuance to the issuer name expiry
observed at issuance. LIP-0008 records the hire split and distinguishes grant
closure from project and installation stops. LIP-0006 records wallet request
signing through Keymaker, and LIP-0028 states today's bearer authority and
on-use checks. The owner decisions first recorded in this version are in
force in it; the co-author's answer is folded in later by amendment and
gates nothing (Decision 0004, "Status of the decisions of this version").

LIP-0026, "Owner decision proposals", gives one proposed text for each of
whole-parent atomic refusal, ordinal-to-row mapping, class checkpoint
derivation and normative class refusal codes. Each is proposed, owner
decision pending. The in-force profile stays exactly at its version 0.1.51
classification, and whole-parent checks remain unavailable. Completion of
v4 and landing of the laboratories precede freeze; no freeze is declared.
Every LIP remains Draft, and no historical protocol byte, tool or vector
outcome changes.

LIP-0004 also distinguishes the implemented V2 main issuance route and its
offline test coverage from the regtest-only v1 route and mainnet qualification.

Version 0.1.53 gives the v4 grant its members.
[LIP-0020](lips/LIP-0020-grant-v4-wire-registry.md) section 11 states every
member of `swarma-grant/4` with its form: the issuer pin and the grant key,
the recipient by key or by name, one executor, the actions and the typed
limits, the window in block heights, the recent block, and the seal with its
key in the grant. A root grant may carry the right of re-delegation, with a
delegation key, a child-seal key, pools, pinned notaries and at most 16
groups of rows; a group is a template and at most 16 ranges of at most 4096
coins, and a signed grant has at most 65536 octets. A template states its
certifier or states in so many octets that it has none, and a range of a
group with a certifier states a stop coin for each of its rows. A child
names its parent and its ordinal and is signed by the parent's delegation
key. Two codes are new, `GRANT_SHAPE` and `GRANT_DELEGATE`. The section is
text in force on Ivan Oparin's order of 2026-11-16 that Grant v4 does not
wait; the co-author's agreement has not been given, and the co-author's
answer is folded in by amendment. It carries the rules of LIP-0008, LIP-0014,
LIP-0026 and LIP-0027 in octets and changes none of them, and it says where
it chose a form that no decision gives. Every decision that it carries
binds a reader of `swarma-grant/4` from this version, and a draft's own
additions bind no reader until they are accepted. The four bounds are
decided limits (J12) with one status in LIP-0020 and LIP-0026; no statement
of J12 in the specification names the numbers, which rest on the owners'
decision register alone and are marked so. For each rule of a parent the
section says which decision gives it. Every reader judges whether a range
has its stop coins, where their run ends and that each row has its own.
Two points are carried as proposals that a reader need not judge, the
witness key hash form of a range script and of a stop script and the
placement of a stop coin; a reader that judges one reports
`GRANT_DELEGATE`. The 112 vectors of
[`vectors/LIP-0020/grant-v4.json`](vectors/LIP-0020/grant-v4.json) hold
signed grants, and [`tools/grantv4`](tools/grantv4/grantv4.py) reads and
recomputes them. Four of them state "`ok` or `GRANT_DELEGATE`", for those
two points. No vector reads a chain, nothing of it is
implemented in the reference laboratory, and one implementation computed
the file: no second one has recomputed it. Every LIP remains Draft, and no
earlier vector changes.

Version 0.1.54 records three owner decisions and changes no octet of a
grant, no tool and no vector. The first is the reservation ledger of the
service that signs children with a delegation key
([LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) section 11.1,
rules J4.4 (a) to J4.4 (g)), decided by Ivan Oparin on 2026-11-16. For one
place of one parent, which is one row of the parent by its ordinal, the
service makes one signature, ever, and makes a record durable before it
signs. The same request is answered with the stored signature and never
with a new one, another payload for the same place refuses as
`PLACE_CONFLICT`, and an interrupted write or one whose outcome is unknown,
a stop between the signature and its record included, holds the place as
`PLACE_HELD`: the service does not retry, and it answers with no new key
and no other place. A held place has two exits, each a reconciliation by
the operator that never uses the delegation key: it confirms a signature
that the service itself wrote into the ledger, or it proves that the key
was never used, over the whole life of the key from its making, which
frees the place. Where neither is proved the place stays held for ever.
The ledger has one writer and is one chain whose head the service keeps
outside it. The audit that is proof stands in that chain, as part of each
entry; an operational audit beside it proves nothing. Every write is a
mark, then the entry, then the kept head, and each partial outcome has one
state; the service appends nothing beyond an entry that the kept head does
not cover before it has recorded the hold of that place in the chain. A
ledger that is absent, rolled back or forked is lost and holds every place
of every parent whose delegation key the service holds, until it is
restored whole or the operator starts a new one by a genesis, with those
places held for good. A key that the ledger does not show from its making
has every place held. A restore of the whole host that reaches the kept
head is a loss that the service cannot find by itself; keeping the head
out of that reach, and a key in one custody, is the operator's duty. The
section states all of this as one table of states and events, from which
its rules, codes and cases are read. The duty is one that no verifier can
observe,
and it proves nothing to a consumer; the two codes are answers of the
service to its caller and no codes of a verifier. Cases S4-11 to S4-30 and a
plan of vectors stand in the same section, and no vector of it exists. The
second decision, of the same day, is a statement of terms: a v4 grant keeps
block heights and has no clock member, a calendar interval is converted to
heights at issuance, and a clock check of an issuer is its own rule
([LIP-0008](lips/LIP-0008-grant-v4.md) section 7.1). The third corrects the
holder of an agent's request key: under J7 the key holder is Keymaker and
not the messaging daemon, by Ivan Oparin's decision of 2026-11-14 for his
deployment, where
[LIP-0013](lips/LIP-0013-trust-contract.md) section 3.6, the
[key registry](KEY-REGISTRY.md) and the [key map](KEY-MAP.md) named the
gateway of the agent's host; the gateway stays the holder in the
implemented rental profile. Keymaker holds the request key and signs the
typed J7 objects, and the messaging daemon only asks for signatures over
the socket. Whether NIP-17 messages use the same key, and through which
holder, is not decided. The holder is named per owner: another owner names
its own under the same J7 rules, and naming one gives no waiver from J4.
The co-author's answer to the ledger is folded
in by amendment. Nothing of this version is implemented, and every LIP
remains Draft.

Version 0.1.55 proposes a step table for a v4 child.
[LIP-0014](lips/LIP-0014-notary-certified-redelegation.md) section 8.4
states the steps F1 to F24 of one predicate, for the signing service of the
delegation key before it signs a child and for a verifier at every
admission, with the code of each step, what a refusal leaves behind, the
status of each step (carried from a landed text, new, or amending one) and,
for each pair of neighbouring steps, the sentence that states their order
or the mark NEW with a reason; where an order is not decided, the section
says "unordered". A child states the contract
identifier of its parent (`CHILD_CONTRACT_DIFFERS`); a contract that is not
presented (`CONTRACT_NOT_PRESENTED`) or does not recompute (`CONTRACT_ID`)
refuses before the parent is read; a refusal of the parent keeps the code
of the rule that refused it; and a child that is wider than its parent in
an action or in its window, or that names another chain, takes the codes
of the same comparisons on v3. An absent and a wrong child-seal key refuse
before any row is read, the coin of a row is checked before the
attestation, and section 8.5 orders the checks of the signing service as
the inner order of step 1 of the order of one request of section 11.1,
whose steps 2 to 9, the reservation ledger of version 0.1.54, follow, with
two of them amended in place: step 3 by one branch and step 6 by the checks
that it repeats on a fresh observation.
[LIP-0020](lips/LIP-0020-grant-v4-wire-registry.md) W11.11 holds the four
comparisons of a child against its parent and one table that registers the
codes, and its section 11.14 the registries of action identifiers and of
limit kinds, both without a defined entry. Six codes are new with this
version: `CHILD_CONTRACT_DIFFERS`, `CONTRACT_NOT_PRESENTED`, `CONTRACT_ID`,
`CHILD_NOT_LIVE`, `ACTION_UNDEFINED` and `LIMIT_KIND_UNDEFINED`. Until a
profile defines an action, a v4 grant has no effect at an executor, and
until a profile defines a limit kind, a child that states a limit is
neither signed nor admitted. Eight points stay open and are named there:
the order of the seal and the issuance blocs, the code of a request that
is not authenticated, the checks of an invocation, the codes that follow
the contract identifier, which wait for a v4 contract profile, the code of
a closure journal that cannot be read, the place of a spent seal among the
checks of the issuance, a defect of a parent outside the group of the
child, which waits for proposal Q1 of LIP-0026, and the class under which
a signing service judges the age of the tip. All
of this is a proposal of version 0.1.55, in force by no word of the draft:
it binds a reader of `swarma-grant/4` when the version lands, the owner's
order of 2026-11-16 that Grant v4 does not wait covers the members of the
grant and is not stretched to it, and the co-author's answer is folded in
by amendment. The order in which
[LIP-0026](lips/LIP-0026-rows-and-accounts.md) R8.3 counts the rows of a
parent is proposed in force by this version, with the owner's explicit
acceptance pending. No member of the grant, no tool and no vector octet
changes; the vectors of the step order are planned and not generated.
Every LIP remains Draft, and nothing of it is implemented.

Version 0.1.56 closes three findings on that step table and on the
reservation ledger. The Amends list of section 8.4 names rule J4.4 (c) and
event 12 beside step 6 of the order of one request, whose words step 6
reads as naming the checks that it lists, no rule of J4.4 (a) to
J4.4 (g) changes its words, and event 12 keeps those words and gains one
marked sentence. Where the confirmed issuance anchor of a child spends
the coin of its row between step 1 and step 6, the repeat refuses as
`ROW_COIN_REQUIRED` with the place held, and the service writes the entry
of the operational audit and gives its operator the notice of event 39
that a signature exists outside the ledger. The sentence is introduced
with version 0.1.56 as normative text, in step 6 and in event 12 alike;
case S4-30b states it. The entry-kind list of J4.4 (g) is carried
unchanged into the text of the
table of states where the kinds are referenced. The version also records
the owner's decision of 2026-11-16 in the [key map](KEY-MAP.md): a
long-lived working agent has an `id/` name of its own, a one-task executor
that a grant names by key may stay key-only, and the flow for registering
an agent's identity applies to a long-lived working agent as it does to a
permanent role. Two proposals stand in
[UNRESOLVED_QUESTIONS.md](UNRESOLVED_QUESTIONS.md) alone and bind no
reader: that no new key assents to a child's contract, the child's
contract equalling the parent's with the delegator's existing signature on
it counting; and that the agent's message key is pinned in the value of
the agent's own `id/` name. One further line there names a contradiction
that both texts keep: the order of the count of LIP-0026 R8.3, which
LIP-0020 W11.6 states in force and LIP-0026 section 8 states proposed in
force with the owner's explicit acceptance pending, with the two ways
out. No member of the grant, no tool and no vector octet changes. Every
LIP remains Draft, and nothing of it is implemented.

Version 0.1.57 puts in force the order in which
[LIP-0026](lips/LIP-0026-rows-and-accounts.md) R8.3 counts the rows of a
parent, by Ivan Oparin's explicit decision of 2026-11-17. LIP-0026
section 8 and LIP-0020 W11.6 now give that order one state, and the
contradiction recorded by version 0.1.56 is closed. No member of the
grant, no tool and no vector octet changes.

Three additions of 2026-11-14 record decisions of Ivan Oparin and await the
co-author's agreement. [LIP-0006](lips/LIP-0006-grant-gated-actions.md)
section 7 states the rule for words in a grant: text always governs an
agent's work and never a service's effect. A service that performs an
effect, such as a payment, a landing or the release of a secret, decides
from members that a machine compares and refuses a grant whose terms carry
a text. A service that carries requests to an agent passes the text on, and
the agent applies it. [LIP-0013](lips/LIP-0013-trust-contract.md) section
3.4 adds the authority frame. The admission gate, the program that runs an
executor's checks, hands each admitted instruction to the agent inside a
read-only frame that names the principal, the grant, the contract terms and
any scope text; the agent's standing instructions carry one rule and no
contract. The [key registry](KEY-REGISTRY.md) lists every key the
specification names, with its owner, the place where it is published, its
holder, what it signs, a danger level, the effect of a leak and the
recovery. It includes the v4 keys of the same day's decisions, whose rules
stand in LIP-0014 sections 9.1, 10.1 and 11.1. No implementation is claimed
for any of the three.

These drafts do not replace the normative v0.1 profile, adopt new conformance
requirements or rewrite historical evidence. LIP-0002's signed-envelope
commitment remains distinct from the wallet service's unsigned-request
commitment. Adoption needs a decision plus protocol and profile-specific
conformance changes under LIP-0001; that is outside this patch revision.
Open decisions are indexed in [UNRESOLVED_QUESTIONS.md](UNRESOLVED_QUESTIONS.md)
and remain detailed in the individual proposals.

## Tools and release artifacts

Release steps and the complete input order are in [RELEASE.md](RELEASE.md).
Placeholders below refer to that version, ordered tagged inputs and selected
serif print theme; HTML is an intermediate artifact in the release workspace.

| Tool | Purpose and entry point | Output |
| --- | --- | --- |
| Git | `git archive v<version>` | Tagged source archive on stdout. |
| Pandoc | `pandoc --from=markdown --to=html5 --standalone <ordered-inputs> -o <html>` | Intermediate HTML. |
| WeasyPrint | `weasyprint --stylesheet <serif-print-theme.css> <html> swarma-link-spec-v<version>.pdf` | Whole-specification PDF. |
| Poppler | `pdftotext swarma-link-spec-v<version>.pdf -` | Extracted text on stdout for section coverage checks. |
| GitHub CLI | `gh release create v<version> --verify-tag swarma-link-spec-v<version>.pdf swarma-link-spec-v<version>.pdf.sha256` | Release with PDF and SHA-256 assets. |
| Go 1.26, `tools/trustcheck` | LIP-0013 reference checker: `go -C tools/trustcheck run . check ../../vectors/LIP-0013/trust-vectors.json` | One `PASS`/`FAIL` line per vector and a `SUMMARY` line on stdout; exit 0 only if every vector gives its expected result, 1 on a mismatch, 2 on a usage or input error. |
| Go 1.26, `tools/trustcheck` | Regenerate the LIP-0013 vectors: `go -C tools/trustcheck run . gen > vectors/LIP-0013/trust-vectors.json` | The vector file, byte for byte deterministic; review it as a diff. |
| Go 1.26, `tools/trustcheck` | Checker self-tests: `go -C tools/trustcheck test ./...` | Test result on stdout: BIP-340 vector 0 reproduced, generator equal to the committed file, planted defects caught. |
| Python 3, `tools/grantv4` | Reader of a v4 grant and checker of its vectors (LIP-0020 sections 11 and 12): `python3 -I tools/grantv4/grantv4.py check vectors/LIP-0020/grant-v4.json` | One `PASS` or `FINDING` line per vector and a `SUMMARY` line on stdout; exit 0 only if every vector gives its expected result and its stated values, 1 on a finding, 2 on a usage or input error. The checker reads each vector with the proposal points of W11.10 and without them: for the four vectors of the group `undetermined` the first read must give `GRANT_DELEGATE` and the second `ok`, and any other code is a finding; for every other vector both reads must give the stated outcome. The checker shares its code with the generator: it shows that the file is what this one reader gives. |
| Python 3, `tools/grantv4` | Regenerate the grant vectors: `python3 -I tools/grantv4/grantv4.py gen > vectors/LIP-0020/grant-v4.json` | The vector file, byte for byte deterministic. The generator writes nothing when its reader disagrees with a stated expectation; review the file as a diff. |

Source review precedes tagging and rendering. This repository has no general
executable conformance runner; `tools/trustcheck` checks only the LIP-0013
draft vectors. Its one direct dependency is `github.com/btcsuite/btcd/btcec/v2`
v2.3.5, the BIP-340 library the chain-lab v3 code uses; it reads no network,
node, clock or key file. `tools/grantv4` checks only the grant vectors of
LIP-0020 section 12. It uses the Python standard library alone, carries its
own secp256k1 and BIP-340 arithmetic for the public test scalars of that
file, and reads no network, node, clock or key file.
