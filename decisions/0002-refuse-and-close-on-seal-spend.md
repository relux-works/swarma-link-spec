# Decision 0002: refuse and close on any seal spend; the watcher separates pending from final

## Context

A revocation is a seal spend. Waiting for a confirmation before refusing
would leave a window in which a revoked grant is still admitted. The
reference verifier reads the seal with mempool-inclusive `gettxout`, so an
unconfirmed spend already looks spent to it.

## Decision

A verifier that finds the seal spent, in the mempool or in a block, refuses
and closes the certificate at once. The closure is never reopened, even if
the spend never confirms. The seal watcher keeps the finer view for operators:
`SUSPEND` while the spend is pending, `FINALREVOKED` once it is in a block.

## Consequences

- No revoked grant is admitted after the spend is visible to the verifier's
  node.
- A spend that is broadcast but never confirms still ends the grant. Only the
  seal key holder can create it, so this is a cost the issuer chooses, not a
  third-party attack.
- A transient failure of the seal read also closes the grant (a recorded
  false refusal, F4). This trades availability for never admitting a revoked
  grant.
- The watcher must read the mempool and carry its previous verdict and tip
  between operations ([revocation](../protocol/revocation.md) §3).
