# Names

This document is normative.

## 1. Chain and name space

1. v0.1 uses the Namecoin main chain (genesis
   `000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770`). A
   verifier MUST pin the network and the genesis hash explicitly and MUST
   refuse a node that reports a different chain or is in initial block
   download. A verifier MUST NOT rely on a library default for the network.
2. Participants are named with Namecoin names. Issuers SHOULD use the `id/`
   name space, for example `id/alice` for an owner and `id/alice-agent` for an
   agent acting under a grant. A verifier binds to the owner and requester
   names it pins, not to the prefix; the prefix is an issuer convention and is
   not checked.
3. Whoever controls the name output controls the name. Transferring the name
   output to another address is a chain-level transfer. For every grant
   anchored to the previous generation of that name, a transfer is a
   generation replacement and closes those grants
   ([observation](observation.md) §4); it never carries a grant to the new
   holder.
4. A verifier MUST refuse a name that is expired at the observed tip.

## 2. Value format

1. Issuers MUST write the value as a JSON object, ASCII, compact (no
   insignificant whitespace), with members sorted by code point, no longer
   than 520 bytes (the Namecoin consensus limit). Verifiers are not required
   to check whitespace or member order.
2. The value has one top-level member, `swarma`, whose value is a JSON
   object. Members of `swarma` defined in v0.1:

| Member | Type | Meaning |
|---|---|---|
| `keyvault_owner_spki` | string | Owner public key: DER SubjectPublicKeyInfo of a P-256 key, base64url without padding |
| `keyvault_requester_spki` | string | Requester (grantee) public key, same encoding |
| `keyvault_certificate_sha256` | string | Lowercase hex SHA-256 of the full grant envelope bytes, as issued |
| `keyvault_seal` | object | The seal outpoint: `{"txid": <64 lowercase hex>, "vout": <integer ≥ 0>}` |

3. Issuers MUST NOT write members other than those defined here. A verifier
   ignores members it does not define, unless they are aliases or fold
   conflicts (§3.1).
4. An owner name carries `keyvault_owner_spki`. After an issuance it also
   carries `keyvault_certificate_sha256` and `keyvault_seal`
   ([issuance](issuance.md)). A requester name carries
   `keyvault_requester_spki`.
5. The owner SPKI and the requester SPKI of one grant MUST differ. A verifier
   MUST refuse a grant whose owner and requester keys are equal.

## 3. Reading values and node replies

1. A reader MUST match member names exactly. A member whose name equals a
   defined member under Unicode simple case folding (a fold alias), any two
   members that are fold-equal to each other (a fold conflict, defined or
   not), and a duplicate member MUST cause refusal. This applies at every
   level: the top level, inside `swarma`, and inside `keyvault_seal`.
2. The same rule applies to every node reply a verifier or seal watcher
   decodes on the way to a decision: chain info, block, header, transaction,
   output, mempool and name replies.
3. A value that is invalid under §2 causes refusal of that observation. A
   malformed value alone MUST NOT create a closure. A proved generation
   replacement closes the grant whatever the replacement's value is
   ([observation](observation.md) §4.2).

## Limitations

- The reference implementation of 2026-11-08 (keyvault candidate `529984e0`)
  does not meet §3.1 and §3.2: its seal check (`gettxout`, review finding F1),
  its seal watcher (F2), its displaced-header path (F3) and its name value
  reader select the exact member and do not refuse aliases or fold conflicts.
  The fix passed independent review on 2026-11-08 and landed in rebased
  form (keyvault main `6775a18f`, chain-lab `e6c6c579`); a conforming build
  is not yet deployed. Until one is
  deployed, only a verifier that reads genuine Namecoin Core output directly,
  with nothing in between, is in scope; Core emits official spellings only.
- Name expiry (36000 blocks without an update) is enforced as a refusal
  (§1.4); renewal is the issuer's duty and is not otherwise specified.
