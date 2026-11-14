# LIP-0022: Observation, freshness and risk profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** how a verifier of Grant v4 takes one consistent reading of its
  node, when it trusts that reading, how old the tip may be for an action,
  how it checks the recent block of a grant and how it counts confirmations
- **Builds on:** LIP-0008 sections 2, 4, 6, 7 and 7.1, LIP-0020 section 7.3
  and LIP-0021 section 1; relates to `protocol/observation.md` and
  `protocol/revocation.md`

## Summary

LIP-0008 stops money or irreversible actions when the tip is 60 minutes old
and other privileged actions at 90 minutes, and it requires two independent
nodes that agree on the tip. It does not say what measures the age, which
clock counts, when two nodes are two, or what "agree" means. A verifier
cannot implement the cutoffs without those answers, and two verifiers on
the same chain can stop at different moments.

Three more points of the admission order of LIP-0008 section 4 are open in
the same way: the one consistent observation that every check uses, the
recent block that a grant commits, and the confirmation depth of a piece of
evidence.

This LIP proposes the first profile for all of them, on Namecoin:

- one observation: every fact of a check lies between two reads of the same
  tip (section 1);
- node health and the comparison nodes: what a healthy node is, when two
  nodes count as two, when their tips agree, and that one healthy node
  whose tip conflicts refuses the observation (section 2);
- the clock and the age of the tip, measured from the header of the tip
  and from the verifier's own first sight of it, with the two decided
  cutoffs (section 3);
- the recent block of a grant, at the issuer and at a verifier (section 4);
- confirmation depth (section 5);
- nine refusal codes and their order (section 6);
- vectors (section 7).

It changes no number that the owners have decided. Three numbers of its own
are provisional and wait for a measurement on a real host.

## What is decided and what is proposed

Four things that this profile serves are decided, and no rule of the
profile itself is. LIP-0008 section 6 records, as decided design, an owner
decision of 2026-11-10: money or irreversible actions stop at a tip age of
60 minutes and other privileged actions at 90 minutes; admission requires a
node-health check with at least two independent nodes that agree on the
tip; and a service determines the risk of an operation from its action
profile, which a caller cannot lower. The same section says that the exact
age measure, the clocks, the criteria for independent nodes and the
classification of risk still need a profile and qualification. This LIP
proposes the first three and leaves the classification to action profiles.

The fourth is the window of a grant in block heights, with the rule that it
does not open below the committed recent block (LIP-0008 section 7.1). The
changelog of version 0.1.13 dates the window to Ivan Oparin's decisions of
2026-11-10, with the co-author's agreement pending, and section 7.1 dates
the rule about the recent block to his decision of 2026-11-11.

Every rule of this LIP is the draft's proposal: the two reads of the tip,
the health of a node, the label that makes two nodes two, the agreement of
tips and the refusal on a tip that conflicts, the age as the larger of the
header age and the seen age, the first sight that the verifier keeps for
it, the guard against a clock that went back, the bound on a header that is
ahead, the class of an action without a stated class, the issuer's choice
of the recent block, the window between the recent block and the anchor,
the arithmetic of depth, and the nine codes with their order. Neither owner
has decided them, and nothing of them is implemented. The owners accept or
change them through this LIP, under LIP-0001.

Three numbers are provisional. Each is a proposal like the rest, and in
addition none is to be frozen before a run on a real host has measured what
it bounds.

| Number | Value | What a run has to measure first |
| --- | --- | --- |
| `S`, how far the header of the tip may be ahead of the verifier's clock | 600 seconds | For each new tip, its header time minus the moment at which the node received it |
| `LAG`, how many blocks a comparison node may be behind, and how many headers a node may know above its tip | 1 block | How long two nodes of the operator differ after a new block, and by how many blocks |
| `K`, how far above the recent block the issuance anchor may be confirmed | 432 blocks | How many blocks pass between the signing of a grant and the confirmation of its anchor in a real issuance |

The table says which open point each section answers.

| Open point | Proposed here |
| --- | --- |
| LIP-0008 section 4, step 3: "Require healthy observations, explicit freshness policy" | Sections 1 to 3 |
| LIP-0008 section 6: "Exact age measure, clocks, independent-node criteria and risk classification still need profile definition and qualification" | Sections 2 and 3. The classification of actions stays with action profiles |
| LIP-0008 section 7: the committed block "meets the profile's recency policy", and its open question "the recency bound between the committed block and the tip" | Section 4. The encoding of the field comes with the members of the grant |
| LIP-0008 section 2: "Exact tiers and depths remain open" | Section 5 fixes the arithmetic. Tiers and numbers stay open |
| LIP-0021 section 1: how one consistent observation is taken | Section 1 |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The comparisons of sections 1 to 5 and the order of section 6, as functions of stated tips, times, heights and numbers | Yes | The owners' acceptance, and for three numbers the measurement |
| The reads on a reading node and on a comparison node | No | A run that shows which calls of the pinned build supply each fact, how the pending transactions of LIP-0008 sections 5.1 and 5.2 are read against one tip, and how a tip that changed and came back between the two reads of an observation is noticed (section 1) |
| The class of each action | No | Action profiles (LIP-0007; LIP-0008 section 12.1) |
| The classes of evidence and their minimum depths | No | LIP-0008 section 2 leaves them open |

## Motivation

Two verifiers read the same tip at the same moment and must both decide
whether a payment may still go out. The first measures the age of the tip
from the time in its header. The second measures it from the moment at
which its own process saw the block arrive, as the seal watch of v0.1 does.
Namecoin's consensus accepts a header whose time is up to two hours ahead
of the accepting node's clock. For a block whose header is 30 minutes ahead
the two ages differ by half an hour, and the first verifier still pays when
the second has stopped. The decision gives the cutoffs and not the measure.

The second node raises the same kind of question. Two addresses of one node
agree on every tip and prove nothing. Two honest nodes differ by one block
for a few seconds after every new block. A rule has to count the first pair
as one node and has to say whether the second pair agrees. A third node
adds a third case: one comparison node is a block ahead and another has the
verifier's tip. A rule that asks for one agreeing node alone lets the
verifier pass over the node that knows a block more.

The recent block has no check at a verifier today beyond its presence on
the chain. The issuer's name and the consent of a recipient by name are
both judged at that block (LIP-0021 section 7.1, LIP-0020 section 7.3). An
issuer that commits an old block moves that judgement into the past, and
nothing tells a verifier how old the block was when the grant was anchored.

## Current state

- LIP-0008 section 6 states the cutoffs and the two nodes as decided design
  and names the measure, the clocks, the node criteria and the
  classification as open.
- `protocol/observation.md`, normative for v0.1, has a verifier read one
  node in sequence. A tip that changes during an observation closes the
  certificate, and the document lists that closure among its false
  refusals. It checks only that the node is not in initial block download
  and says that it has no rule for a stale node that looks synced.
- `protocol/revocation.md` stops the seal watch of v0.1 when no new block
  came for 30 minutes. The reference watcher counts from the moment at
  which it saw a higher tip itself (`swarma-chain-lab` at
  `839bdcca41cd17ffd7c4057de2dc88a521745515`,
  `experiments/sealwatch/watch.go`).
- The reference observation of the same laboratory
  (`experiments/single-use/node.go`) pins the genesis hash, refuses a node
  in initial block download, ties each confirmed transaction to the active
  chain by block hash, height and membership, and refuses when the chain
  information after its reads differs from the one before. It reads one
  node, has no rule for the age of the tip and holds no v4 code.
- The booking service of that laboratory keeps the largest clock reading
  that it has used and compares later readings with it
  (`experiments/rental-booking/service_v2.go`).

## Proposal

### 1. One observation

Every fact of a check lies between two reads of the same tip. Where the tip
moved in between, the observation is void: the verifier reads again or
refuses, and it records nothing as closed.

| Rule | Requirement |
| --- | --- |
| B1.1 | An observation is a set of reads of the verifier's own node, the reading node, that begins and ends with a read of its tip: the hash and the height of the last block of its active chain. Where the two reads differ, the observation is void. |
| B1.2 | A void observation proves nothing. The verifier observes again or refuses, and nothing is recorded as closed. A closure that a rule wrote while it read (LIP-0008 sections 5.1 and 5.2) stays, because it rests on a transaction that the verifier validated and not on the observation. |
| B1.3 | The observation is on the pinned chain: the node gives the pinned genesis hash for the block of height 0 (LIP-0008 section 4). |
| B1.4 | A confirmed fact belongs to the observation when the block that holds it is on the active chain at the observed tip: the height of that block is not above the height of the tip, the node gives the hash of that block for that height, and the block holds the transaction. |
| B1.5 | Every fact of one admission check comes from one observation: the height `H` of the tip for the window of LIP-0008 section 7.1, the reads of LIP-0021, the seal, the issuance anchor, the recent block, and the pending transactions that LIP-0008 sections 5.1 and 5.2 read. A fact from an earlier observation is no input; a cache holds under its own rule (LIP-0021 section 6). |
| B1.6 | Immediately before a reservation or an effect the verifier reads the tip and its clock again. Where the tip is not the tip of the observation, the admission is void. With the new reading of the clock it applies section 3 again. |

v0.1 closes a certificate when the tip changes during an observation and
lists the result as a false refusal: plain chain progress triggers it. This
profile makes the same event a void observation without closure, as
LIP-0008 section 5.1 says of tip movement and inconsistent reads. The cost
is one more observation when a block arrives during a check, which on a
chain with a block about every ten minutes is rare for a check that takes
seconds.

B1.6 is the form that LIP-0008 section 12.5 asks for: after the work of an
observation, the executor checks both measures again before a new
reservation or effect.

Two equal reads of the tip do not make the reads between them one
snapshot, in two cases. A tip that went to another block and came back
between the two reads looks unchanged. The pending transactions of a node
change while its tip stands still. B1.4 ties each confirmed fact to the
active chain at the observed tip, and no rule of this profile ties a
pending transaction to it or notices the tip that came back. Both cases
belong to the run that qualifies the reads on a node. Until that run has
closed them, an implementation of the reads is not qualified for admission,
whatever the vectors of this LIP say about its comparisons.

### 2. Node health and the comparison nodes

An observation is healthy when three things hold. The reading node is
healthy. At least one healthy comparison node of another source has the
reading node's tip, or a block at most `LAG` below it on the same chain. No
healthy comparison node has a tip that conflicts with the reading node's
chain.

| Rule | Requirement |
| --- | --- |
| B2.1 | A verifier has its reading node and at least one comparison node. Its configuration names the comparison nodes before an observation begins. An observation asks every one of them, and every answer counts under B2.5. A comparison node supplies its tip and what B2.3 needs: the hash that it gives for the block of height 0, whether it is in initial block download, and the height of the best header that it knows. No fact of a grant, a name or a seal is taken from it, and it needs no transaction index. |
| B2.2 | Two nodes count as two when their operator provisioned them as separate nodes: separate processes with separate chain state, each of which validates the chain itself and has peers of its own. The verifier's configuration states a source label for each node, and nodes with the same label count as one. Two addresses of one node, a node and a relay in front of it, and two nodes that take their blocks from one upstream alone have one label. |
| B2.3 | A node is healthy in an observation when it answers, is on the pinned chain (B1.3), is not in initial block download, and knows no header more than `LAG` blocks above its tip. |
| B2.4 | The tip of a comparison node stands in one of three relations to the reading node. It agrees when it is the reading node's tip, or the block of the reading node's active chain at a height at most `LAG` below the height of that tip. It is behind when it is a block of the reading node's active chain further below. It conflicts in every other case: it lies above the reading node's tip, or the reading node gives another hash for its height. |
| B2.5 | An observation is healthy when three things hold: the reading node is healthy; no healthy comparison node has a tip that conflicts, whatever the source label of that node and whatever the other nodes answer; and at least one healthy comparison node with another source label has a tip that agrees. In every other case the verifier refuses, and nothing is recorded as closed. |

The comparison node may be behind and may not be ahead, for a reason. Every
fact of a check comes from the reading node. A comparison node that is one
block ahead shows that the reading node has not yet seen a block, and that
block can hold the spend of a seal. The verifier observes again a moment
later. A comparison node that is one block behind shows only that it is the
slower of the two.

Two tips at one height with different hashes conflict. That is the state in
which one of two blocks will be dropped, and a verifier that admitted on
either would rest an effect on a block that may leave the chain. Admission
waits until the nodes are on one chain again.

A node that conflicts is not outvoted. Take a reading node at height 800, a
comparison node at height 801 and a second comparison node at the reading
node's tip. A rule that asked for one agreeing node alone would admit here,
on a reading that the verifier knows to lack a block, and LIP-0008 section
4 says that conflicting data never permits an effect. So one healthy node
that conflicts refuses the observation. That holds also for a comparison
node with the reading node's own source label: the label says where a node
takes its blocks from and does not make its answer weaker. The verifier
asks every configured node in every observation for the same reason. A
verifier that chose afterwards which answers to count could count the ones
that agree.

Two kinds of node have no say. A node that is behind by more than `LAG`
shows nothing that the reading node lacks; it neither agrees nor conflicts,
and the verifier has one comparison node less. A node that is not healthy
under B2.3 does not answer, is on another chain, is still loading blocks or
knows itself that it is behind. The conformance pairs of LIP-0008 name
lagging and conflicting nodes as refusals. Under B2.5 a reading node that
lags refuses, because a comparison node is then ahead of it, and a
comparison node that lags does not count.

The rule costs availability and nothing else. Every further comparison node
is one more node that is ahead for a moment after a new block, and one more
node whose operator can refuse every observation of the verifier by a false
answer. No answer of a comparison node can make the verifier admit.

What agreement shows is limited, and LIP-0008 section 6 says so: it helps
to find a lagging node and defeats neither a shared upstream nor an
eclipse. The source label of B2.2 is the operator's statement. A verifier
cannot check it from the answers of the nodes, so a wrong label is an error
of provisioning that this profile cannot detect.

### 3. The clock and the age of the tip

The age of the tip is the larger of two ages: the verifier's clock minus
the time in the header of the tip block, and the verifier's clock minus the
reading at which the verifier first saw that block as the tip. The verifier
refuses money or irreversible actions when the age is 3600 seconds or more
and other privileged actions when it is 5400 seconds or more.

| Rule | Requirement |
| --- | --- |
| B3.1 | `now` is the verifier's clock in whole seconds of UTC. The verifier reads it after the last read of an observation, and again under B1.6. |
| B3.2 | The verifier keeps, durably, the largest `now` that it has used for an admission or written as a first sight (B3.7). A clock that reads less than that mark refuses, and the mark stays. |
| B3.3 | `t` is the time in the header of the tip block of the reading node. Where `t` is more than `S` seconds later than `now`, the verifier refuses: its clock is behind or the header is ahead, and the header age cannot be measured. |
| B3.4 | The age of the tip is the larger of its header age and its seen age. The header age is `now - t`, and 0 where `t` is later than `now`. The seen age is `now - f`, where `f` is the first sight of the tip block (B3.7). |
| B3.5 | An action has one of two classes, which the action profile of the service states and no caller can lower: money or irreversible, and other privileged. An action whose profile states no class has the first. |
| B3.6 | The verifier refuses an action of the first class when the age is 3600 seconds or more, and an action of the second class when it is 5400 seconds or more. No grace is added. |
| B3.7 | The first sight of a block is the reading `now` of the first observation that counts for it: the block is the tip of the reading node, the observation is not void (B1.1) and is on the pinned chain (B1.3), and its clock does not read less than the kept mark (B3.2). The verifier writes the first sight durably in that observation, before it admits anything on it, and also where another rule refuses the observation. |
| B3.8 | A first sight is written once. The verifier does not change or remove it, and it survives a restart. A block that becomes the tip again has the first sight that it had. |

The cutoffs and the rule that the class comes from the action profile are
the decided design of LIP-0008 section 6. The measure with its two ages,
the first sight, the two guards and the default class are this draft's
proposal.

The two ages catch two different failures. The seen age catches a node that
receives no block any more: it grows with the verifier's own clock,
whatever the header of the last block says. The header age catches blocks
that are old when they arrive: a node that was cut off and is then given
the blocks of some hours ago sees each of them for the first time, and
their headers show their age.

The header age alone does not hold the cutoffs. The time in a header is a
miner's claim. Consensus accepts it when it is later than the median time
of the eleven blocks before it and at most two hours ahead of the accepting
node's clock. Take a tip whose header is two hours ahead of the verifier's
clock at the first sight, and let no block follow. B3.3 refuses the tip for
6600 seconds, until the clock has come within `S` of the header. By the
header alone an action of the first class would then be admitted on that
tip for another 4200 seconds, until three hours after its first sight,
although no block arrived in all that time. `S` does not prevent it: B3.3
compares the header with the clock of one check and knows nothing of the
moment at which the block arrived. Under B3.4 the seen age of that tip is
6600 seconds when B3.3 lets it pass, and the tip is admitted for no action
of either class.

The bound of this profile is therefore the following. On one tip, an action
of the first class is admitted for less than 3600 seconds from the first
sight of that tip, and an action of the second class for less than 5400
seconds, for every header that consensus accepts. A header that is behind
makes the tip look older than it is, and the verifier stops early.

The bound counts from the verifier's first observation of a tip and not
from the moment at which its node received the block. A verifier that
observes every few seconds sees a new tip a few seconds late. A verifier
that observes only when a request arrives can see a tip long after its node
received it, and for that interval the header alone speaks. The same holds
for a verifier that starts for the first time and for one that lost its
first sights: each counts from its first observation afterwards. This
profile fixes no interval between observations, and the question is open.

The record is small. A first sight is a block hash and a time, 40 octets,
and at a block about every ten minutes a year of them is about two
megabytes. That is why B3.8 can keep every one.

`S` keeps a purpose beside the seen age. A header that is far ahead of the
clock shows that one of the two does not show the time, and a verifier
whose clock is behind measures every header age too small. A smaller `S` refuses more
honest tips whose miner's clock runs ahead, each until the verifier's clock
has caught up or the next block arrives. How often that happens on the main
chain is what the run has to measure.

The clock itself is an assumption. B3.2 catches a clock that went back, and
B3.3 catches a clock that is more than `S` behind a fresh header. A clock
that is behind by a constant amount understates the header age by that
amount and leaves the seen age as it is, because the seen age is the
difference of two of its readings. A clock that stands still or runs slow
understates both ages. A verifier keeps its clock as it keeps its keys.

The cutoffs do their work in the interval that the window of a grant does
not cover. While no block arrives, the height of the tip does not advance
and a window in heights does not close (LIP-0008 section 7.1). In the
sample that LIP-0008 section 6 reports, the tip was older than 60 minutes
for 0.229 percent of the time and older than 90 minutes for 0.001 percent.

### 4. The recent block

A verifier checks two things about the recent block that a grant commits:
the block is on the active chain of the observation, and the issuance
anchor is confirmed above it by at most `K` blocks.

| Rule | Requirement |
| --- | --- |
| B4.1 | An issuer commits, as the recent block of a grant, the tip of the observation in which it made the checks of the issuance. That observation is healthy under section 2. |
| B4.2 | A verifier establishes that the committed hash is the hash of a block on the active chain of its observation (B1.4). The height of that block is `R`. |
| B4.3 | The issuance anchor of the grant is confirmed at a height `A` with `R < A` and `A <= R + K`. |
| B4.4 | The verdicts of B4.2 and B4.3 are relative to the active chain. After a reorganisation that removes the recent block or moves the anchor the verifier decides again on the chain that it then validates, and nothing is recorded as closed. |

LIP-0020 proposes B4.1 for a grant whose recipient is named by name (W7.6);
this rule states it for every grant and adds the health of the observation.

`R < A` holds for every honest issuance: the anchor commits to the signed
grant, and the signed grant holds the hash of the recent block, so the
anchor cannot be confirmed in that block or below it. A grant for which it
does not hold was not issued as this profile describes.

`K` bounds how far into the past an issuer can move the judgement of its
own name and of a consent. Without it a verifier accepts a grant whose
recent block lies a year below its anchor, and it then judges the consent
under the state that the recipient's name had a year earlier. The proposed 432 blocks are 72 hours at ten
minutes for a block, the span that the decided point of LIP-0020 gives a
consent between its signature and the first transaction of the issuance.
The cost is real: an issuance whose anchor is confirmed later than `K`
blocks after its recent block refuses at every verifier, and the parties
issue again with a new grant and a fresh consent. That is why the number
waits for a measurement of real issuances.

### 5. Confirmation depth

The depth of a confirmed fact is the height of the observed tip minus the
height of its block, plus one, and the minimum that holds for a piece of
evidence is the larger of the signed minimum and the operator's floor.

| Rule | Requirement |
| --- | --- |
| B5.1 | The depth of a confirmed fact is `H - h + 1`, where `H` is the height of the observed tip and `h` the height of the block that holds the fact. A fact in the tip block has depth 1. A pending transaction has no depth. |
| B5.2 | Where a rule asks for a minimum depth of a piece of evidence, the minimum that holds is the larger of the minimum that the grant signs and the floor of the verifier's operator, for that chain and that class of evidence (LIP-0008 section 2). A configuration never lowers the signed minimum. |
| B5.3 | Depths on different chains are not compared, added or converted. A minimum for evidence on one chain says nothing about evidence on another. |

B5.2 and B5.3 restate LIP-0008 section 2 so that the arithmetic has one
place; B5.1 adds the definition that the comparison needs. Which classes of
evidence exist, and their numbers, stay open there. One confirmation is an
admission rule of an application and no finality.

### 6. Refusals and their order

A verifier reports one refusal of this profile, the first of the order
below, and none of them records a closure.

| Code | What it reports | Rule |
| --- | --- | --- |
| `OBSERVATION_CHAIN` | The reading node is not on the pinned chain | B1.3 |
| `OBSERVATION_VOID` | The tip moved between the first and the last read, or before the effect | B1.1, B1.6 |
| `NODE_UNHEALTHY` | The reading node is not healthy, or no comparison node with another source label is healthy | B2.3, B2.5 |
| `NODE_DISAGREEMENT` | A healthy comparison node has a tip that conflicts with the reading node, or no healthy comparison node with another source label has a tip that agrees | B2.4, B2.5 |
| `OBSERVATION_CLOCK` | The clock reads less than the kept mark, or the header of the tip is more than `S` ahead of it | B3.2, B3.3 |
| `TIP_AGE` | The tip is too old for the class of the action | B3.6 |
| `RECENT_BLOCK` | The committed recent block is not on the active chain of the observation | B4.2 |
| `RECENT_BLOCK_WINDOW` | The issuance anchor is not above the recent block, or more than `K` above it | B4.3 |
| `CONFIRMATIONS` | A piece of evidence is shallower than the minimum that holds | B5.2 |

B6.1. The first six stand in the order of the table and before every rule
of a grant: a verifier that finds two of them reports the upper one. A
refusal of another rule that was computed in an observation which one of
the six refuses is not reported.

B6.2. `RECENT_BLOCK` stands before every rule that uses `R`: the window of
LIP-0008 section 7.1, the walk of an issuer's name (LIP-0021 section 7.1)
and the consent of a recipient by name (LIP-0020 W7.6).
`RECENT_BLOCK_WINDOW` belongs to the check of the issuance and stands after
the read of the anchor. `CONFIRMATIONS` stands where the rule that asks for
the depth stands.

The order puts the doubt about the reading before what the reading shows. A
verifier that cannot trust its observation reports that, and it does not
report a change of a name or a spent seal that it read in the same
observation. A closure that it wrote while it read stays (B1.2).

### 7. Vectors

[`vectors/LIP-0022/observation-vectors.json`](../vectors/LIP-0022/observation-vectors.json)
holds 97 vectors over the 28 rules of this LIP, as
decisions on stated tips, times, heights and numbers. No vector reads a
node, and none shows what a node returns.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `observations` | 6 readings, of which 2 pass; 5 facts, of which 2 belong | B1.1, B1.3, B1.4 and B1.6 on the tips of the first and the last read, the genesis hash, a block that holds a fact, and the tip before an effect |
| `nodes` | 9 healthy, 15 refused, 1 with two findings | B2.1 to B2.5 on the stated state of a reading node and of comparison nodes with their source labels. Among the refused are a node that is ahead and a node on another branch, each beside a node that agrees |
| `clock` | 11 admitted, 12 refused | B3.2 to B3.7 on a clock reading, the kept mark, the header time of the tip, the first sight of the tip and the class of an action, at both sides of each boundary |
| `sequences` | 10 | Section 3 over time: one verifier, what it keeps durably at the start and at the end, and a list of observations with the expected outcome of each. Among them are a tip whose header is two hours ahead, a tip with an ordinary header, a restart, a tip that comes back, and first observations that are void or refused |
| `recent` | 8 on the recent block, of which 2 pass; 7 on the window, of which 3 admit | B4.2 and B4.3 on a committed block, the active chain and the height of the anchor; and the window of LIP-0008 section 7.1 on the height of the tip, with a verdict and no code, because that section names none |
| `depth` | 3 deep enough, 4 refused | B5.1 to B5.3 on heights, a signed minimum and an operator's floor |
| `order` | 6 | B6.1 on observations with two findings each |

A vector whose outcome is not the passing one holds one defect, states the
expected outcome and names a neighbour with the passing outcome that
differs from it in that defect. The vectors of the group `order` hold two
findings each, state the one that the order reports and name no neighbour.
A sequence states the outcome of each of its steps and names no neighbour;
where it shows a defect that a checker can have, it names a sequence
without that defect as its control.
The list `rules` of the file names for each rule its section, its state,
which is `proposed` for all, its vectors and what no vector covers.

The vectors use the proposed values of `S`, `LAG` and `K` and state them in
the file. A change of a provisional number changes the vectors at its
boundary and no other. Block hashes are placeholders. No vector holds a
pending transaction or a closure, and none shows what a reorganisation does
to a fact.

No checker for these vectors is in this repository. The expected outcomes
were stated by hand, computed by one implementation and decided again by a
second one that shares no code with the first; neither is published here.
Both come from the author of this text, so an error of understanding that
they share is in the vectors. The vectors bind nothing until both owners
accept the rules that they follow.

## Sources

No node was run for this LIP, and no measurement was taken for it.

| Statement | Source |
| --- | --- |
| A block header is invalid when its time is not later than the median time of the eleven blocks before it, or more than two hours later than the accepting node's clock | Namecoin Core at the tag `nc28.0`: `src/validation.cpp`, the header checks that report `time-too-old` and `time-too-new`; `src/chain.h`, `MAX_FUTURE_BLOCK_TIME` and the span of the median |
| The median time of a block is the middle value of the times of that block and of the ten before it, after the node has sorted them | The same tag, `src/chain.h`, `GetMedianTimePast` |
| The seal watch of v0.1 counts its 30 minutes from the moment at which it saw a higher tip | `swarma-chain-lab` at `839bdcca41cd17ffd7c4057de2dc88a521745515`, `experiments/sealwatch/watch.go` |
| The reference observation pins the genesis hash, refuses a node in initial block download, ties a confirmed transaction to the active chain and refuses when the chain information changed during its reads | The same commit, `experiments/single-use/node.go` |
| A service of the laboratory keeps the largest clock reading that it has used and compares later readings with it | The same commit, `experiments/rental-booking/service_v2.go` |
| The shares of time beyond a tip age of 60 and of 90 minutes | LIP-0008 section 6, which reports a sample of 20000 blocks on one node |

## Alternatives

- **The header time alone as the measure.** A verifier would keep nothing
  for it. A tip whose header is two hours ahead would be admitted until
  three hours after it arrived, as section 3 shows.
- **The first sight alone as the measure**, as the seal watch of v0.1 has
  it. A miner's header time could not move it at all. A verifier that
  starts, and one whose node was cut off and then receives the blocks of
  some hours ago, would count each of those blocks as new.
- **The median time of the tip** in place of its header time. It is the
  middle value of the times of the tip and of the ten blocks before it,
  which the node sorts first. One header that is ahead does not move it,
  and six of the eleven do, so it can still be ahead of the clock. Where
  the times rise with the heights it is the time of the sixth block from
  the top, five block intervals behind the tip, and a cutoff of 60 minutes
  would then refuse much of the time.
- **No bound on a header that is ahead.** The seen age would hold the
  cutoffs all the same. A clock that is far behind would go unnoticed where
  a fresh header shows it today.
- **One agreeing node is enough**, also where another healthy node
  conflicts. An operator could add comparison nodes without adding
  refusals. The verifier would pass over a node that shows a block which
  its reading node lacks.
- **A comparison node that may be ahead.** It would spare one more
  observation after a new block. The verifier would then admit on a reading
  that it knows to lack a block.
- **Closing a grant when the tip moves during an observation**, as v0.1
  does. v0.1 itself lists that closure as a false refusal.
- **No window between the recent block and the anchor.** An issuance could
  never fail for a late anchor. A verifier could not tell how old the state
  was under which the issuer's name and a consent were judged.
- **A health rule on the node's peers**, for example a least number of
  them. A node reports its peers itself, and a count shows nothing about
  where their blocks come from. The header rule of B2.3 uses headers whose
  proof of work the node checked.

## Security consequences

- **Two nodes of one source are one node.** The label of B2.2 is the only
  thing that keeps them apart, and it is the operator's word. An operator
  who labels a node and its relay as two has one node and a check that
  always passes.
- **Agreement does not defeat an eclipse.** An adversary that controls what
  both nodes see controls the tip that they agree on. The age cutoff then
  stops actions once the adversary withholds blocks for long enough; it
  does not help against an adversary that feeds a false chain with fresh
  header times, which costs that adversary the work of those blocks.
- **One healthy node that conflicts stops admission.** That is what the
  rule is for, and it is also a lever: whoever controls one configured
  comparison node can refuse every observation of the verifier. That party
  can make no observation pass.
- **A header time cannot stretch a tip.** A miner that sets a header ahead
  moves the header age and not the seen age, and the larger of the two
  counts. A miner that sets a header behind makes verifiers stop early,
  until the next block.
- **The seen age starts at the verifier's first observation.** A verifier
  that did not observe while a block arrived, one that starts for the first
  time and one that lost its first sights count from the first observation
  afterwards, and for the time before it the header alone speaks. A store
  that was replaced by an earlier copy of itself has lost the first sights
  since that copy, and nothing in this profile notices it.
- **A clock that stands still hides age.** B3.2 catches a clock that went
  back. A clock that runs slow understates both ages by what it lost.
- **A void observation is not a closure.** A party that can make blocks
  arrive during a check cannot close a grant by it. It can delay a check
  for as long as blocks keep arriving at that moment.
- **The order hides findings on purpose.** A verifier that does not trust
  its observation reports no change of a name from it. A closure that
  LIP-0008 sections 5.1 and 5.2 have it write while it reads is written all
  the same.
- **`K` bounds an issuer and does not prove honesty.** Within `K` blocks an
  issuer can still commit a block that was not its tip.

## Conformance impact

None on normative v0.1: its observation, its closure on a moving tip and
its 30-minute stop stay as they are, as LIP-0008 section 6 says of the stop.
None on Grant v3. No conformance class is added. The pair of LIP-0008 on
healthy independent node observations and an age policy for each action
gets its meaning from sections 2 and 3, and its cases still run on nodes.

## Open questions

- **The owners' acceptance** of the age measure with its two ages, of the
  first sight that a verifier keeps, of the two guards of the clock, of the
  source label, of the agreement rule and the refusal on a conflict, of the
  window `K` and of the nine codes with their order.
- **The interval between observations.** The seen age counts from the
  verifier's first observation of a tip. Whether the profile fixes how
  often a verifier observes, and which interval, is open.
- **The store of first sights.** Its form, and what a verifier does when it
  finds that the store was lost or went back.
- **The three provisional numbers**, `S`, `LAG` and `K`, each after the run
  that the table of this LIP names.
- **The classes of actions.** Which action has which class is the matter of
  action profiles, and so is the question whether an action that a grant
  gates can have no cutoff at all.
- **The reads of pending transactions.** How a verifier reads the pending
  spends of a seal and the pending operations of a name against one tip,
  and what the pinned build of the node offers for it.
- **A tip that changed and came back** between the two reads of an
  observation. Section 1 does not notice it, and the run that qualifies the
  reads on a node has to.
- **Where the source labels are kept** and who may change them. LIP-0008
  asks for an administrator-owned sealed configuration; its form is open.
- **The tiers of depth** and the classes of evidence (LIP-0008 section 2).
- **A verifier without its own node**, and other chains: the profile is for
  a verifier with two nodes on Namecoin.
