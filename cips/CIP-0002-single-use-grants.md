# CIP-0002: Single-use grants

- **Status:** Draft
- **Created:** 2026-11-08
- **Affects:** issuance, observation, revocation; adds an executor class

## Summary

A single-use grant is consumed when it is used. Its seal can be spent by the
issuer (revocation) or by the grantee (use). The grantee spends the seal in a
transaction that also carries the SHA-256 of one signed request in an
`OP_RETURN` output, so the spend is bound to exactly one request. The
executor acts only after that spend is in a block.

## Proposal (to be specified and tested before adoption)

1. Seal: a 1-of-2 output spendable by the issuer key or the grantee key.
2. Use: the grantee spends the seal; the same transaction has exactly one
   `OP_RETURN` output with the request hash.
3. Executor: computes the hash of the presented request, finds the spend of
   that seal signed by the grantee with that hash, and acts only after one
   confirmation. A spend in the mempool means pending: no effect.
4. Ledger: the executor writes the request to its own journal before acting.
   This gives at most one execution per executor. Exactly-once across a crash
   between journal write and effect is not claimed.
5. A spend with a different hash, or by the issuer, is a refusal for every
   other request.

## Evidence required before `Proposed`

At least 25 negative controls on regtest, each with a valid neighbour, then a
mainnet run under the same custody and exact-hex review rules as v0.1.

## Working design for the regtest experiment (2026-11-08)

- Seal: legacy P2SH 1-of-2, redeem `OP_1 <issuer key> <grantee key> OP_2
  OP_CHECKMULTISIG`, fixed issuer-first order, distinct compressed keys.
- Attribution: the executor recomputes the legacy signature hash and verifies
  the single signature against both keys. Grantee only means use; issuer only
  means revocation, even with a matching request hash; anything else refuses.
- Request hash: SHA-256 of the exact signed request envelope bytes, in exactly
  one zero-value `OP_RETURN PUSH32` output. Other funding and change outputs
  are allowed; the grantee's `SIGHASH_ALL` commits to them.
- Ordering: seal height < anchor height < spend height; the same block refuses.
- Chain keys: operator pins in v0. A future name field could be
  `swarma.keyvault_single_use_secp256k1`.
- Journal: per executor, chain and seal; reservation fsynced before the effect;
  a surviving reservation never retries.

## Evidence so far (2026-11-08)

- Regtest: a matrix of 47 controls on genuine Namecoin Core 28.0, each next
  to a valid neighbour (receipt outcomes across the matrix: 37 refusals,
  3 pending, 9 replays without a second effect, plus the executions of the
  neighbours), and five traffic-noise scenarios; independent review accepted.
- Mainnet, one complete run: seal (P2SH 1-of-2) at height 850684, anchor at
  850686, grantee use with the request hash at 850690. The executor reported
  pending while the use was in the mempool, executed once after one
  confirmation, answered a replay with already-executed, and refused a second
  valid request. Exactly one effect.

## Lesson: unrelated traffic must not decide the verdict

The first mainnet confirmed-use observation refused falsely. While searching
for spends of the seal, the executor strictly decoded every unrelated block
and mempool transaction with a legacy-only decoder, so unrelated traffic
could make it refuse. The exact transaction that triggered the mainnet
refusal was not identified; each mechanism (a third-party segwit
transaction, a transaction with many inputs, a large mempool) was
reproduced separately on regtest. That is a refusal any third party can
trigger. Rule for this
proposal: discovery reads only the exact projected inputs of each
transaction; only candidates that spend the seal are strictly validated; a
candidate that fails strict validation aborts the observation as a refusal,
never as "no spend". Resource bounds stay explicit and fail closed.

## Open questions

- Fee source for the grantee's spend (seal value or an extra input).
- Whether the grantee chain key moves into the name value (schema change).
