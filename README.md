# Swarma Link: Human-to-Agent Mandates in an Untrusted Environment

**Version:** 0.1.15

**Date:** 2026-11-11

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

## Draft profiles and design decisions in v0.1.15

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
General agent sub-delegation still needs its separate both-owner decision.
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
to register `d/<label>` together with `id/<label>`. It records Ivan Oparin's
four decisions of 2026-11-10 and awaits the co-author's agreement. No reader
implements these rules yet; LIP-0004 values keep their own rules.

LIP-0004 also distinguishes the implemented V2 main issuance route and its
offline test coverage from the regtest-only v1 route and mainnet qualification.

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

Source review precedes tagging and rendering. This repository has no general
executable conformance runner.
