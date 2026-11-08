# Conformance

This document is normative. A conformance claim names the specification
version, the class, the implementation and its exact version, the node it
read, and the vector set it was checked against.

## 1. Classes

### Issuer

An issuer builds seal, anchor and revocation transactions that satisfy
[issuance](../protocol/issuance.md) and [revocation](../protocol/revocation.md),
and owner values that satisfy [names](../protocol/names.md) §2.

### Verifier

A verifier satisfies [observation](../protocol/observation.md) and
[revocation](../protocol/revocation.md) §2, reads names under
[names](../protocol/names.md) §3, and reproduces every verdict in the vector
sets below when given the same chain and the same grant.

## 2. Vector sets

| Set | Content |
|---|---|
| [`v0.1/mainnet-2026-11-08.json`](v0.1/mainnet-2026-11-08.json) | Two complete cycles on Namecoin mainnet: issuance, admit, revocation and the verdicts observed at each tip |

The mainnet set is evidence of the reference run: chain data is public and
anyone can check the transactions, heights and scripts. The grant envelopes
themselves are not published here; only their SHA-256 is. A verifier
reproduces the verdicts with envelopes issued under the same shape.

## 3. Required negative cases (v0.1)

A verifier claim MUST include passing results for each case. Each case states
its closure expectation. Each refusal is paired with a valid neighbour that
admits; where a case closes the certificate, the neighbour MUST use a fresh
certificate and issuance, not the closed one.

| # | Case | Verdict | Closure |
|---|---|---|---|
| 1 | owner SPKI on chain differs from the envelope issuer | refuse | none |
| 2 | requester SPKI on chain differs from the envelope grantee | refuse | none |
| 3 | envelope signed by a key other than the owner's | refuse | none |
| 4 | malformed owner value at the pinned generation | refuse | none |
| 5 | observation started before the anchor is confirmed | refuse | `confirmed-issuance-replacement` |
| 6 | seal already spent before the first observation | refuse | `seal-spent-or-unknown` |
| 7 | seal spend in the mempool | refuse; watcher `SUSPEND` | `seal-spent-or-unknown` |
| 8 | seal spend in a block | refuse; watcher `FINALREVOKED` | `seal-spent-or-unknown` |
| 9 | restart after a closure | refuse | unchanged |
| 10 | a later name update replaces the anchored generation | refuse | `confirmed-issuance-replacement` |
| 11 | chain tip changes during the observation | refuse | `observed-tip-change` |
| 12 | requester name changes generation during the observation | refuse | `confirmed-requester-generation-change` |
| 13 | fold alias, fold conflict or duplicate member in a name value, or in a chain, block, header, transaction, name or mempool reply | refuse | none |
| 14 | the same in the seal output (`gettxout`) reply | refuse | `seal-spent-or-unknown` (the seal read fails) |
| 15 | the pinned anchor block is proved displaced from the active chain | refuse | `canonical-block-displacement` |
| 16 | expired owner or requester name | refuse | none |

Cases 13 and 14 are not met by the reference implementation of 2026-11-08 (see
[names](../protocol/names.md), Limitations). Regtest vectors for these cases
will be added as files in `v0.1/` once their publication form is agreed.
