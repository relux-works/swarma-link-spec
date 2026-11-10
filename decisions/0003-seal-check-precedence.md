# Decision 0003: a seal read cannot be hidden by a route-health precheck

## Context

[Observation](../protocol/observation.md) §1.4 includes "seal unspent" in a
SHOULD route-health precheck and says its failure is not a refusal and creates
no closure. Read alone, that sentence could let a verifier see a mempool seal
spend, skip the observation without closing, then admit the same certificate
after eviction. That contradicts §4 and [decision 0002](0002-refuse-and-close-on-seal-spend.md).

The historical v0.1 body and evidence remain unchanged. This decision is its
interpretive erratum, recorded in v0.1.11; it adds no successor-profile rule.

## Decision

The no-closure sentence in §1.4 applies only to route readiness. It does not
exempt a seal-state read from §4. For a presented certificate's independently
pinned seal (§2), a spent, unknown or failed seal-state read is an authority
observation for the closure rule, even when performed inside a health check
or before other observation steps. The rule is asymmetric: an unspent
precheck read is route readiness only, not a seal verdict for the observation.
It does not satisfy Observation §3 item 4; the observation performs its own
seal check.

If that seal read finds spent (mempool or block), unknown, or fails, the verifier
MUST refuse and record `seal-spent-or-unknown` under §4. It MUST write the
closure durably before reporting refusal. A route-health failure, early return,
or label such as "precheck" MUST NOT discard that result or bypass closure.
The rule applies when a route-only failure and a seal-state result occur in
the same batch. A successful unspent seal read inside the observation alone
never authorizes admission; all applicable observation conditions still have
to hold.

Once written, that closure never reopens after mempool eviction, a later
unspent response or restart. Recovery needs a fresh certificate and issuance.
If the durable write fails, the observation still refuses and MUST NOT admit
the certificate until the closure is written, exactly as §4 requires. This
does not repair v0.1's documented crash gap after a failed write: the in-process
bar may be lost on a crash (Observation, Limitations, F6).

A route-only check that fails before any seal-state read may prevent starting
an observation without itself creating a refusal or closure. It cannot erase
a seal result already obtained or any other closure cause under §4. This
decision does not require every route check to read the seal, change independent
pin selection, or close a certificate for an unrelated/presenter-selected seal.

## Consequences and contract examples

These examples clarify existing obligations; they are not new published
conformance vectors or passing implementation tests. In closing cases the
valid neighbour uses a fresh certificate and issuance, as the existing
[conformance rules](../conformance/README.md#3-required-negative-cases-v01) require.

| Valid control | Required refusal or invariant |
| --- | --- |
| Healthy route, live independently pinned seal and all other conditions satisfied can admit | A precheck finding that seal spent in mempool/block refuses and durably closes before reporting. |
| Seal read inside the observation and all other admit conditions satisfied | Admission resting only on an earlier unspent precheck result refuses; the observation cannot skip its own seal check. |
| Route-only failure before any seal read may skip starting the observation without a new closure | Unknown seal or failed seal-state read in a precheck refuses and closes; calling it route failure cannot suppress §4. |
| A route failure with no seal result creates no seal closure by itself | A mixed batch containing both route failure and a spent/unknown/failed seal read still refuses and closes. |
| A fresh unclosed certificate/issuance with all conditions satisfied can admit | After a recorded precheck closure, mempool eviction, later unspent state and restart cannot reopen the old certificate. |
| Successful durable closure write preserves refusal across restart | Failed closure persistence still refuses and bars admission until written; no claim of crash-safe persistence is made for the historical F6 gap. |
| Independently pinned correct seal is checked for its certificate | An unrelated or presenter-selected outpoint cannot be substituted to create a closure for another certificate. |

The false-closure tradeoff on transient seal read failure (F4) is unchanged.
The watcher's pending/final distinction is unchanged. Successor proposals
that separate transient refusal from proved closure still need their own
adoption and qualification; they cannot be backported by interpretation here.

At chain-lab
[`59773ed1`](https://github.com/relux-works/swarma-chain-lab/tree/59773ed1becce26b8696a64f4db2969219c5aac5),
the inspected [Python verifier functions](https://github.com/relux-works/swarma-chain-lab/blob/59773ed1becce26b8696a64f4db2969219c5aac5/experiments/fullnode-trusts/protocol.py)
perform the seal read inside the authority decision, with no separate
seal-unspent health precheck; the [Go grantcheck entry point](https://github.com/relux-works/swarma-chain-lab/blob/59773ed1becce26b8696a64f4db2969219c5aac5/experiments/grantcheck/checker.go)
delegates to its kernel backend without such a precheck of its own. This is a
bounded source read, not a v0.1 closure-conformance claim or a new runtime result.
