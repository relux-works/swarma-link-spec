# Revocation

This document is normative.

## 1. Revoking

1. The issuer revokes a grant by spending its seal. In v0.1 the revocation
   transaction spends only the seal and pays the remainder back to the owner
   address.
2. Revocation acts on the future only. Anything the grantee did before the
   spend is not undone.

## 2. Verifier

1. Any observation that finds the seal spent, in the mempool or in a block,
   refuses and closes the certificate (`seal-spent-or-unknown`,
   [observation](observation.md) §4). The verifier MUST NOT wait for a block
   to refuse.
2. The closure stands even if the spend never confirms. Only the holder of
   the seal key can create such a spend, so no third party can close another
   party's grant this way.

## 3. Seal watcher

A seal watcher follows one seal over a bounded operation and reports its
state. It refuses in every state except `UNSPENT`.

| State | Meaning |
|---|---|
| `UNSPENT` | the seal is unspent at the tip and not spent in the mempool |
| `SUSPEND` | a transaction spending the seal is in the mempool and not yet in a block (`MEMPOOL_SEAL_INPUT`); or a carried pending spend is no longer visible (`PRIOR_SPEND_REQUIRES_RECONCILIATION`), which never returns to `UNSPENT` |
| `FINALREVOKED` | a transaction spending the seal is in one of the first six blocks after the operation's start tip (`FIRST_ACTIVE_BLOCK_SPEND`) |
| `UNKNOWN` | the seal state cannot be established (for example an older spend no longer visible through `gettxout`) |
| `STOP` | the operation ended without a verdict: six successors without a spend, no new block for 30 minutes, deadline or cancellation, or an expired proof |

1. Each watch operation has a start tip, a deadline and a proof validity
   bound. It MUST end in `STOP` when any bound is reached.
2. Continuity. A watcher that advances from one operation to the next MUST
   carry the previous tip as the new start tip, and MUST carry a previous
   `SUSPEND` or `FINALREVOKED` verdict as the prior. An `UNSPENT` verdict is
   carried as the start tip only. No block between two operations may be
   skipped.
3. A block that arrives without the spend leaves the state at `SUSPEND`
   while the spend stays in the mempool.
4. `FINALREVOKED` is laboratory policy (one confirmation), not consensus
   finality. A chain reorganisation can in principle undo the spend; v0.1 does
   not reopen a grant on that ground.

## Limitations

- Spend and revocation can race for the same seal; consensus gives no
  priority to revocation.
- A spend mined within seconds of broadcast may never be visible in the
  mempool to a given watcher; it then goes from `UNSPENT` to `FINALREVOKED`,
  which is still a correct refusal.
- A spend first seen more than six blocks after the start tip ends the
  watch operation in `STOP`, not `FINALREVOKED`; the verifier still refuses
  through its own seal check.
