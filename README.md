# Swarma Link: Human-to-Agent Mandates in an Untrusted Environment

**Version:** 0.1.0

**Date:** 2026-11-08

**Status:** Draft

**Authors:** Alexey Grigoryev, Ivan Oparin

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
| [`cips/`](cips/) | Improvement proposals (not normative until adopted) |
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
