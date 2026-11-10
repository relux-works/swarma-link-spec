# LIP-0003: Detached grants under an agent identity

- **Status:** Draft
- **Created:** 2026-11-08
- **Affects:** names, issuance, observation, revocation
- **Motivation:** many grantees in parallel under one agent identity, no per-grant name updates, expiry by
  time, no dependency on a web site.

## Summary

The agent's Namecoin name holds only the agent's keys. A grant is a certificate signed by the agent's grant key,
naming the grantee's key, a scope, a validity window and its own seal. It needs no name update and no anchor
transaction. Revocation is a spend of that grant's seal. Expiry is the window in the certificate. An unlimited number
of grants can be live at once, one per renter.

## 1. Name value

```
{"swarma":{"agent":{"nostr":"<64 hex x-only>","grant":"<64 hex x-only>"}}}
```

- `nostr`: the agent's public messaging key (the gateway holds the secret).
- `grant`: the key that signs grants (held by the trusted component outside the sandbox, never by an instance).
- Exact shape, ASCII, compact, as v0.1 `names` §2. A `name_update` happens only on key change.
- **Custody.** The name is owned by a cold owner key (the operator's wallet). The `grant` and `nostr`
  keys are hot, held by the trusted component outside the sandbox, which never holds the owner key. A leak of the hot
  keys is recoverable by an owner `name_update`; a leak of the owner key is out of scope.
- **Key rotation.** A confirmed name generation whose `grant` key differs closes every grant signed by the old key.
  A pending rotation — a `name_update` of the agent name in the mempool that changes the `grant` key — makes
  verifiers refuse at once without closing (suspend); the closure is written when the rotation confirms. Verifiers
  see a pending rotation with the same mempool scan they already use for seal spends (`name_pending` for the agent
  name, or the mempool-inclusive read of the name output). Rotation is the emergency brake for leaked hot keys.

## 2. Certificate

Canonical compact JSON, fixed field order:
`version, network, genesis, agent_name, issuer_key (= grant key), grantee_key (renter's BIP-340 key),
grantee_name (optional Namecoin name, informative), contract_sha256, scope (closed action set), not_before,
not_after, seal {txid, vout}, budget (optional)`; BIP-340 signature by `issuer_key` over SHA-256 of those bytes;
certificate id = SHA-256 of the signed envelope.

## 3. Seal

- One unspent output per grant, drawn from a pool of confirmed outputs the issuer created in advance at an address
  only the issuer controls. Optional (recommended): the seal script pays to a key listed in the name value (e.g.
  P2WPKH or P2TR key path of the `grant` key), and the verifier checks the script, so anyone can see that only the
  issuer can revoke. A pool output is used for at most one certificate, ever (journalled before signing).
- **Early termination** (revocation) = spend of that seal. **Normal end** = `not_after`; no transaction.
- At or after `not_after` the issuer may sweep expired seals back into the pool's funding in batches; a spend after
  expiry changes nothing for a verifier (the grant is already over).

## 4. Anchoring (optional)

A certificate is valid without an anchor. Two optional anchors, for publication and audit:
- **Batched:** one transaction per batch with one `6a20` output carrying a Merkle root of certificate ids issued in
  the batch; inclusion proofs published with the slot.
- **Per grant:** a `6a20<certificate id>` output in any transaction of the issuer.
An anchor adds a public timestamp and makes later denial of issuance visible; it is not needed for verification.

**Privacy.** Without per-grant anchors the renter's key is not on chain at all; with batched anchors only Merkle
roots are. Only the parties who see the certificate learn the renter's key. The rental privacy notice says this
instead of the v0.1 warning that the key becomes public on chain.

## 5. Verification (kernel)

Live iff all hold, on the verifier's own node:
1. The agent name's current value has the exact shape and its `grant` key equals `issuer_key`; the name is not
   expired.
2. The certificate signature verifies under `issuer_key`; canonical bytes exact.
3. The seal exists, is confirmed, and is unspent with mempool-inclusive `gettxout`.
4. `not_before <= now < not_after`.
5. The presenting key equals `grantee_key` (the authenticated sender: the NIP-17 seal key).
Closures (durable, fsync before the verdict): a seal spend seen in the mempool or a block; a confirmed name
generation with a different `grant` key. A pending rotation refuses without closing (§1). Read failures refuse
without closure.

**Presentation.** A detached certificate must reach the verifier. The grantee attaches the certificate (or a
fetchable reference plus its id) to its first message; the gateway verifies it, caches it per sender, and replaces a
cached certificate for the same sender only with another one that is live. This is what makes agent-to-agent use
work, where the verifier (another operator's agent) is not the issuer.

**Acceptance-time rule.** `not_before` earlier than the seal's block time is
refused. This constrains acceptance, not the signing time: a transaction ID can
be known before confirmation and even before broadcast, so the grant can name
its future seal in advance. A real cryptographic lower bound on construction
requires a recent block hash inside the signed grant; LIP-0008 proposes that
for a new version. No block-hash field is added to this draft's existing bytes.

**Txid stability (informative successor note).** LIP-0008 proposes two
construction profiles selected by the authenticated chain pin. W uses only
native P2WPKH/SIGHASH_ALL seal and anchor inputs, confirmed ordinary funding
and explicit validated unconfirmed linkage/payment dependencies. L waits for
confirmed referenced outpoints and builds the anchor after seal confirmation;
it permits no unconfirmed dependent chain. Both refuse changed references and
require reissuance rather than unsafe admission or silent rebinding. Low-S
and strict DER do not guarantee legacy txid stability. Revocation in either
profile follows the consumed seal outpoint. Current P2PKH funding does not meet
W or by itself establish L support. This note changes neither the existing
bytes here nor the normative historical v0.1 profile.

## 6. Parallel renters

Each live grant maps to one instance (sandbox) for its grantee; the gateway routes by authenticated sender key to
that grantee's instance. Capacity is the number of instances the host runs, not a number of names.

## 7. Rental exchange without a site

A sender with no live grant reaches only a deterministic exchange in the gateway, never the model:
`terms` (agent name, profiles, contract templates and prices) → `contract` (the renter's chosen template filled with
their key and window; contract_sha256) → `consent` (the renter's signed message carrying contract_sha256) →
`pay` (a unique NMC address and amount) → after 1 confirmation the issuer signs the certificate and the gateway
sends it to the renter with "ready". A web page is one optional client of the same exchange.

## 8. What changes against v0.1

| v0.1 | LIP-0003 |
| --- | --- |
| Owner value holds certificate hash + seal; one grant per name | Name holds keys only; unlimited grants |
| Anchor `name_update` + `6a20` per grant | No per-grant transaction; anchoring optional/batched |
| Closure on generation replacement of the value | Closure on grant-key change only |
| Envelope by keyvault P-256 requester key | Grantee = renter's Nostr key (BIP-340) |
| End by revocation | End by time; seal spend only for early termination |

## 9. Effect on the reference implementation

Keeps: canonical certificate encoding and BIP-340 signing/verification; the seal pool, its journal and the
one-seal-ever rule; mempool-inclusive seal checks and durable closure; read-failure refusal without closure; online
admission (package, confirmed payment, hold expiry, surplus, witness payments).
Changes: issuer signs a detached certificate instead of planning a station `name_update`; the kernel reads the agent
name's keys instead of a station value and drops the per-grant anchor checks; an optional batched-anchor planner.
Drops: station names and the idle-value renewal template.

## 10. Open questions

- Whether grantee may be a Namecoin name resolved at check time (key may change) or only a pinned key (proposal: pin
  the key; the name is informative).
- Batch anchoring cadence, if any, for the public demo.
- The enforcement point: one trusted component per agent outside the sandbox holding the grant key and
  the agent keys.
