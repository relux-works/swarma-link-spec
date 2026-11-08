# Observation

This document is normative.

An observation is one verifier decision about one presented grant at one
moment: **admit** or **refuse**. An admit says the chain state the verifier
read supports the grant. It is not, by itself, permission to perform an
effect; effect admission is out of scope for v0.1.

## 1. Node route

1. The verifier MUST read the chain from a full node it trusts, through a
   route that cannot write: no wallet calls, no transaction submission, no
   name writes. v0.1 was exercised with Namecoin Core 28.0 and a dedicated RPC
   user restricted by `rpcwhitelist`.
2. The node MUST maintain a transaction index (`txindex=1`), because the
   verifier looks up confirmed transactions by id without a block hash.
3. Read methods used in v0.1. Verifier: `getblockchaininfo`, `getblockhash`,
   `getblockheader`, `getrawtransaction`, `gettxout` (mempool-inclusive),
   `name_show`. Seal watcher: `getblockchaininfo`, `getblockhash`,
   `getrawtransaction`, `gettxout`, `getrawmempool`, `getblock`.
4. The verifier SHOULD check route health immediately before each
   observation (chain, genesis, anchor header and transaction readable, names
   readable, seal unspent) and SHOULD NOT start an observation when any part
   fails. A failed health check is not a refusal and creates no closure.

## 2. Inputs

1. The verifier takes the presented grant envelope and signed request.
2. It obtains independently of the presenter: the owner name, the requester
   name, the anchor transaction id, the anchor block hash, the seal outpoint,
   and the expected policy (owner identity, subject, audience, action and
   target profile, and the pinned envelope verifier). These pins MUST NOT be
   taken from fields the presenter controls.
3. The reference verifier of 2026-11-08 admits one action profile only
   (`repository.create` on one lab repository). The envelope semantics belong
   to keyvault; the profile values are operator policy, not part of this
   specification.

## 3. Admit conditions

A verifier MUST refuse unless all of the following hold in one observation:

1. the anchor transaction is confirmed in the pinned anchor block on the
   active chain, and it is the current generation of the owner name;
2. the owner value carries the certificate SHA-256 of the presented envelope
   and the pinned seal outpoint, and the anchor transaction carries exactly
   one `6a20` output with that SHA-256 ([issuance](issuance.md) §2);
3. the requester name's current generation has at least one confirmation on
   the active chain at or below the observed tip, carries the requester SPKI, and the
   owner and requester SPKIs differ;
4. the seal output is unspent at the observed tip, including the mempool,
   with at least one confirmation, paying to the owner name's address;
5. neither name is expired;
6. the envelope verifies offline (keyvault rules) against the owner SPKI and
   the requester SPKI read from the chain, for the presented request, at the
   observation time;
7. the owner name, the requester name and the chain tip did not change
   during the observation.

## 4. Closures

A closure is a persistent refusal of one certificate. The verifier MUST
write it durably before reporting the refusal; if the write fails, the
observation still refuses and the verifier MUST NOT admit that certificate
until the closure is written. Once written, the verifier MUST refuse that
certificate in every later observation, including after restart. A closure is never reopened; recovery is a fresh grant with a
new certificate and a new issuance.

1. The verifier MUST record a closure for exactly these causes:

| Closure | Cause |
|---|---|
| `seal-spent-or-unknown` | the seal check returns spent (mempool or block), unknown, or the read fails |
| `confirmed-issuance-replacement` | the owner name's current confirmed generation is not the pinned anchor (a later update, a transfer, or an anchor observed before it was confirmed) |
| `confirmed-owner-generation-change` | the owner name changed generation during the observation |
| `confirmed-requester-generation-change` | the requester name changed generation during the observation |
| `canonical-block-displacement` | the pinned anchor block is proved no longer on the active chain |
| `observed-tip-change` | the chain tip changed during the observation |

2. Precedence. The displacement check runs on every refusal, so a refusal
   for any other reason still closes the certificate when the anchor block is
   proved displaced. A proved generation replacement closes the certificate
   before, and regardless of, the validity of the replacement's value.
3. Refusals with no closure: wrong pins, a wrong or foreign signature, an
   expired request, a malformed value at the pinned generation, equal owner
   and requester keys, an expired name, and any refusal for which §4.1 has no
   cause.

## Limitations

- An observation started before the anchor is confirmed closes that
  certificate (`confirmed-issuance-replacement`, against the previous
  generation). Start observing only after the anchor is confirmed.
- Closures that are false refusals, recorded as limitations and not fixed in
  v0.1: a transient read failure on the seal check (F4) and a new block during
  the observation (F5). The verifier's own node route or plain chain progress
  triggers them; a third party cannot through chain data. F5 can repeat on a
  fresh grant.
- Sequential reads are not atomic; an away-and-back change between reads is
  not excluded.
- Admission safety rests on the trusted node being current. v0.1 checks only
  that the node is not in initial block download; it has no rule for a stale
  but synced-looking node. Operators of the reference run cross-checked tips
  between two independent nodes.
