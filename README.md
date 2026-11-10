# Swarma Link: Human-to-Agent Mandates in an Untrusted Environment

**Version:** 0.1.8

**Date:** 2026-11-10

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

## Draft profiles and design proposals in v0.1.8

This revision reconciles informative draft descriptions with the public
implementation: [LIP-0004](lips/LIP-0004-landlord-grants.md) covers landlord
grants, optional social name metadata and separate discovery;
[LIP-0005](lips/LIP-0005-op-return-locator.md) records the landed framed writer
and exact bare compatibility; [LIP-0006](lips/LIP-0006-grant-gated-actions.md)
describes grant-gated services and the concrete wallet service v1 profile,
with examples and a separately scoped delegated-issuance capability.

[LIP-0007](lips/LIP-0007-service-types.md) proposes service types, action tables
and a typed self-declaration in a service's Namecoin value.
[LIP-0008](lips/LIP-0008-grant-v4.md) proposes Grant v4 signed rental limits and
name-output closure, owner-pinned recipients and concrete executor budgets.
It also records issuer-instance renewal pins, typed self-computed signing
digests, durable validated issuer-branch mempool closure, value-dependent
confirmation minima, per-seal keys, a topology/threat model and a dependent
issuance evaluation. Risk-tier freshness and the signing-time-bound correction
remain proposals. Canonical/signature/error/state vectors, a public runner and
an independent Swift implementation are planned. These two proposals
specify design semantics with unresolved wire/proof details; they do not
reconcile a v4 implementation or assert interoperability.

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
