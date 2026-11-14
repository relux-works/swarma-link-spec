# Swarma Link: Human-to-Agent Mandates in an Untrusted Environment

**Version:** 0.1.37

**Date:** 2026-11-14

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

## Draft profiles and design decisions in v0.1.37

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
and needs no path. These remain Draft semantics without bytes, fixtures or
an implementation.

Decisions of 2026-11-11 by Ivan Oparin change three rules of the v4 draft.
The issuer name is bound by its registration and owner key: a grant lives
while the name's updates change neither the owner nor `swarma`, the verifier
walks the name's history through its transaction index on the active chain,
and a renewal closes nothing. One hire is one grant for the whole term in blocks, with the hour
as a limit and payment period only. A counted payment whose block is
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
notary-certified re-delegation and records the owners' decisions of
2026-11-12. Every child grant is admitted only with a valid notary
attestation, and every verifier still checks the countable conditions of the
child itself: a wider child refuses for that reason even when it is
certified. The parent's signed right of re-delegation names one to four
notaries by `id/` name; each publishes its attestation key in its own name,
in a `swarma` shape that a Draft amendment of LIP-0010 proposes. The notary
is neither the delegator nor the delegatee. On Grant v3 the landlord's
signer issues the child on a signed request of the parent's grantee, under
contract profile `swarma-trust-contract/2`, and no v3 byte changes. The
draft proposes the attestation object, its anchor as LIP-0005 action `0x04`,
the order of an executor's checks and the refusal codes. It belongs to the
second phase of Goal 1: after the first proof, in shadow mode first, and no
part of the first proof. Nothing of it is implemented.

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
recorded each as an open question. Each now has Draft text, labelled J1 to
J8. Ivan Oparin decided them, J3, J6 and J8 on 2026-11-13 and J1, J2, J4, J5
and J7 on 2026-11-14, and the co-author's agreement on each is pending. One
point of J5 is agreed by both owners: in the first version of v4 a
re-delegation narrows only typed fields and appends no text. Nothing of the
rest is adopted before both owners agree. The rules in force stay beside the
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

LIP-0004 also distinguishes the implemented V2 main issuance route and its
offline test coverage from the regtest-only v1 route and mainnet qualification.

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

Source review precedes tagging and rendering. This repository has no general
executable conformance runner; `tools/trustcheck` checks only the LIP-0013
draft vectors. Its one direct dependency is `github.com/btcsuite/btcd/btcec/v2`
v2.3.5, the BIP-340 library the chain-lab v3 code uses; it reads no network,
node, clock or key file.
