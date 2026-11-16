# LIP-0027: Row stop profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** what a v4 parent states for the stop coin of a row, what a
  verifier reads of that coin at an admission, when it records a row as
  closed for cause and how it keeps that record, and how the notary of the
  row derives, funds and spends the coin
- **Builds on:** LIP-0014 section 10.1 (J2), LIP-0008 sections 5.1 and 5.2,
  LIP-0022 sections 1 and 4, LIP-0025 and LIP-0026

## Summary

On v4 the notary of a row ends the row for cause by spending a coin: the
row names a stop coin, and every verifier whose node shows its spend
refuses every child of the row (LIP-0014 section 10.1, J2.7). The decision
fixes that the coin exists before the parent is signed, that the notary
alone can spend it, and that a row whose coin is not there refuses. It
names one code, for the spent coin. A node answers the question "is this
output unspent" with no for a coin that was spent and for a coin that was
never there. A verifier that took the second for the first would record a
closure for cause, which nothing lifts, although nobody signed a spend.

This LIP proposes the first profile for the stop coin, on Namecoin:

- what a row states for its stop coin, and which outputs it cannot be
  (section 1);
- the reads of a verifier at an admission, with three outcomes that are
  kept apart: the coin is there and unspent, the coin is spent, the coin is
  not there (section 2);
- the record of a row closed for cause in a journal of LIP-0025, its entry
  and what a verifier does when it cannot write it (section 3);
- the stop account of the notary, the funding of the coin and the form of
  its spend (section 4);
- three refusal codes, two of them new, and their order (section 5);
- vectors, among them traces of a witness, of a verifier that starts later
  and of a coin that is not on the chain (section 6).

It does not define the attestation of a child on v4 or the frame that
states a cause. Both come with the profile of the attestation.

Under J9, decided and agreed by both owners on 2026-11-15 (LIP-0014 section
8.3 and LIP-0026 section 10), a v4 row inside one owner may have no certifier.
Such a row states no stop coin, and no rule of this profile applies to it. A
child of such a row is admitted through the class and the holders of J10 and
J11, in force since version 0.1.51 (LIP-0014 section 8.3). Under a second
decision of that day, in force since the same version without the co-author's
answer (J12; LIP-0026 section 8), a parent states its rows in groups, and
where the stop coins of the rows of a group stand is open.

## What is decided and what is proposed

The stop coin is Ivan Oparin's decision of 2026-11-14 (J2), recorded as
Draft text in LIP-0014 section 10.1; the co-author's agreement is pending.
The durable closure of a spend that a verifier validated is text of
LIP-0008 section 5.1 for seals, and section 5.2 holds the same for an
issuer's name under a decision of 2026-11-13 (J6), agreement pending. This
LIP changes none of them.

| Decided, or text in force | Where | This profile |
| --- | --- | --- |
| A v4 row gains a member `stop`, an outpoint, "given like a notary seal by transaction, index and script" | LIP-0014 J2.7 | States the same as a fact that a parent signs (H1.1). No octets |
| The output exists and is confirmed before the parent is signed | The same | Confirmed at or below the parent's committed recent block (H2.3), the reading that LIP-0026 gives the same words for the coin of a row |
| It is an output that the notary alone can spend, with no new spending condition, and it pays a key of the notary that is not its attestation key | The same | A witness key hash script (H1.2), and an account of its own at the notary (H4.1) |
| A verifier requires the coin to exist with the named script and to be unspent, the mempool included, and journals a validated spend as it journals a seal spend | The same | Sections 2 and 3 |
| A spent stop coin refuses every child of the row as `ROW_CLOSED_FOR_CAUSE`, in every view that holds that spend | The same; case S2-10 | The same code (H2.4) |
| "A stop coin that does not exist with the named script refuses as well"; after a reorganisation that removes the output the row refuses until the output is confirmed again | Case S2-10; J2.7 | A code of its own, `ROW_STOP`, and no closure (H2.3, H2.6). A reorganisation that removes the coin also removes the parent's recent block, so the parent refuses first, under LIP-0022 |
| The record of a row closed for cause survives restart, eviction, non-confirmation, reorganisation and a rotation of the notary's key | LIP-0014 J2.4a | The same for a closure by the stop coin (H3.4) |
| The fee of the spend is the notary's own and does not hang on a coin that somebody else can spend first | LIP-0014 J2.7 | H4.5 |
| A journal of rows closed for cause has to tell an empty store from a lost one; what its recovery charges is "Not stated yet" | LIP-0014 section 9.1; LIP-0025 section 7 | Section 3: a journal of LIP-0025, and a recovery that charges nothing |

Every rule of this LIP is the draft's proposal, and neither owner has
decided one. Four points are more than a restatement, and the owners should
look at them first:

1. A missing stop coin and a spent one are two outcomes with two codes. A
   missing coin writes no closure (H2.6).
2. A verifier records the closure when its own node shows the coin spent,
   in a block or in its mempool, without the spending transaction in hand
   (H2.4, H2.5). Only the holder of the stop key can bring that state
   about.
3. A closure that cannot be written makes the journal lost for its
   verifier, which then admits nothing until its operator has acted
   (H3.3). LIP-0008 section 5.1 says the same of a seal.
4. The stop coin is neither a seal nor the output after a seal: not of the
   parent (H1.3) and not of the child (H2.2). The anchor of a grant spends the
   output after its seal, and a stop coin there would turn an issuance into a
   closure. The notary keeps its stop keys in an account of their own (H4.1).

Nothing of this profile is implemented. The owners accept or change its
rules through this LIP, under LIP-0001.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The checks of sections 1 and 2 and the journal of section 3, as functions of stated facts and of octets | Yes | The owners' acceptance |
| The reads of the stop coin on a node: its transaction, and whether the output is unspent with the mempool included, against one tip | No | A run under LIP-0022, which leaves the reads of pending transactions open |
| A closure journal on a store | No | A store that is qualified for LIP-0025 |
| The stop account at a notary, and the spend | No | The owners' choice of the account, and the custody of a notary's keys |
| The cause as evidence: the frame, the attestation and the claim of misconduct | No | The profile of the attestation on v4 |

## Motivation

A notary ends row 2 of a parent for cause and spends the row's stop coin.
The spend is in the mempool of verifier A, which refuses the child. Before
the spend is confirmed it drops out of the mempools, for example because
another transaction spent one of its inputs; or it was confirmed, and a
reorganisation drops its block. Verifier B starts an hour
later, sees the coin unspent and admits the child. LIP-0014 accepts that
for B: a spend that never reached a verifier's chain or mempool is unknown
to it. It does not accept it for A. A saw the spend, and what A saw must
hold across the eviction, across a restart and across the reorganisation.
That needs a record, and the record needs a store that cannot go back
unnoticed.

A third verifier C reads a row of another parent whose stop coin was never
confirmed: the parent was signed while the transaction of the coin was
still pending. C's node has no such unspent output. If C read "no unspent
output" as "spent", it would record that a notary ended the row for cause,
for good, although nobody signed a spend. C needs a refusal that closes
nothing and states no cause.

## Current state

- LIP-0014 section 10.1 holds the decided rule J2.7 and the case S2-10. It
  names `ROW_CLOSED_FOR_CAUSE` for a spent stop coin and no code for a
  missing one. Step V18 of its section 8 reads the seal of the attestation,
  the journal and, on v4, the stop coin.
- LIP-0008 section 5.1 has an executor persist a permanent closure when it
  observes a validated spend of a seal, before any further admission, and
  says that a failure to persist permits no effect and requires a recovery
  of the journal. Rule J6.9 of section 5.2 makes a verifier whose closure
  journal is lost a newcomer.
- Draft LIP-0025 proposes the form of such a journal and lists the journal
  of rows closed for cause among those whose entries and recovery are not
  stated yet.
- Draft LIP-0026 proposes what a row states and reads "confirmed before the
  parent is signed" as "confirmed at or below the parent's committed recent
  block".
- The key registry describes the row stop key: the notary holds it for the
  life of the parent, and it is not the attestation key. It gives no path.
- The reference laboratory has no rows on v4 (LIP-0026, current state).

## Proposal

The parent is called `P`, a child `C`, and the ordinal of the child's row
`k`. A view is the active chain of a node together with its mempool, and a
witness is a verifier that recorded a closure, as in LIP-0014 section 10.1.

### 1. The stop coin of a row

A row states its stop coin as an outpoint and a script, and that outpoint
is used for nothing else in the parent.

| Rule | Requirement |
| --- | --- |
| H1.1 | A row of a v4 parent states its stop coin, as an outpoint and a script, beside the five things of LIP-0026 R1.1. |
| H1.2 | The script is a witness key hash: the octets `00 14` and 20 further octets. |
| H1.3 | The stop coins of the rows of one parent are different outpoints. None of them is the coin of a row of that parent, none is the seal of the parent, and none is the output after that seal in the same transaction, which is the linkage output that the parent's own anchor spends (LIP-0023 C2.3). |
| H1.4 | A parent that does not meet H1.1 to H1.3 is refused as a whole, as LIP-0026 R1.5 says of a row: it admits no child and no request of its own. A verifier judges H1.1 to H1.3 on the signed octets of the parent before any check of section 2, so that it reads no stop coin and writes no closure under a parent that it refuses. |

One stop coin for each row keeps a cause local. LIP-0014 has a cause close
the row of the attestation that it concerns and no other, also where
several rows share a seal (J2.4a), and its case S2-10 has another row of
the same parent stay admissible "with its own unspent stop coin".

A stop coin that was also the coin of a row would be spent by the issuance of
that row's child (LIP-0026 R3.3), and the issuance would close a row.

A stop coin that was the output after the parent's seal would be spent by the
issuance of the parent itself, because the anchor of every grant spends that
output (LIP-0023 C2.3). Take a parent whose seal is the output 0 of a
transaction and whose row names the output 1 as its stop coin. The parent's
anchor spends the output 1 and leaves the seal alone, as it must. A verifier
that read this row under section 2 would find the coin on the chain as stated
and spent, and it would record the issuance of the parent as a closure for
cause, which nothing lifts. H1.3 excludes the case by a comparison of two
outpoints that the parent signs: the seal with its index, and the same
transaction with the index one higher. The comparison asks nothing about who
holds the key of the linkage output. Another output of the parent's seal
transaction can be a stop coin; nothing spends it but its key.

### 2. The stop coin at an admission

A verifier admits a child only while the stop coin of its row is on the
active chain as the row states it and unspent in the verifier's view. A
coin that is spent closes the row at that verifier for good, and a coin
that is not there closes nothing.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| H2.1 | The verifier reads its journal of closures first (section 3). Where the journal holds a closure of the pair of `P`'s identifier and `k`, the child refuses, whatever the node shows. | `ROW_CLOSED_FOR_CAUSE`; a journal that is lost or fenced: `JOURNAL_LOST`, `JOURNAL_FENCED` (LIP-0025) |
| H2.2 | The stop coin of the child's row is neither the seal outpoint that the child names nor the outpoint after it in the same transaction, which is the linkage output of LIP-0023 C2.3. A verifier compares them on the signed octets of the parent and of the child. | `ROW_STOP_ALIAS` |
| H2.3 | The verifier establishes on its own node, in the observation of the check (LIP-0022 section 1), that the transaction of the stop coin's outpoint has an output at the stated index with exactly the stated script, and that this transaction is confirmed on the active chain at a height that is not above the height of `P`'s committed recent block (LIP-0022 section 4). | `ROW_STOP` |
| H2.4 | In the same observation that output is unspent in the verifier's view, the mempool included. Where H2.3 holds and the output is spent, the row is closed for cause, and the verifier writes the closure under section 3 before any further admission. | `ROW_CLOSED_FOR_CAUSE` |
| H2.5 | A spend is established only by an observation that LIP-0022 does not refuse, in which H2.3 holds. A void observation, a node that does not answer and a read that contradicts another read establish nothing, and the verifier writes nothing for them. | The code of LIP-0022 |
| H2.6 | A stop coin that is not on the active chain as H2.3 asks is no spent coin. The verifier writes no closure for it and states no cause, and the next observation decides again. | `ROW_STOP` |
| H2.7 | The checks stand in this order, at the place where LIP-0014 section 8 puts step V18, and before the check of the seal that the attestation names. | The first that refuses |

H2.4 lets a verifier close a row without the spending transaction in its
hands. What it has is its own node: the creating transaction is confirmed
on the active chain with the stated script, and the output is not among the
unspent outputs of the view. A node takes an output out of that set only
for a transaction that it validated, in a block or in its mempool, and a
valid spend of a witness key hash carries a signature of its key. So the
state shows a spend that the holder of the stop key signed. The verifier
records that state and the tip at which it found it; the transaction that
spent the coin is not part of the record.

The two refusals differ in what they leave behind. `ROW_CLOSED_FOR_CAUSE`
is permanent at the verifier that reports it. `ROW_STOP` is a statement
about one observation and leaves nothing.

`ROW_STOP` reports a coin that never was as the row states it: another
script, a transaction that is pending or unknown, or a confirmation above
`P`'s recent block. Such a row was not well issued, and a new parent is
what helps. The reorganisation of J2.7 is another case and has its refusal
elsewhere. A reorganisation that removes the block of the coin removes
every block above it, and `P`'s recent block is that block or lies above
it. The parent then refuses under LIP-0022 (`RECENT_BLOCK`) before the stop
coin is read, nothing is recorded, and the row is admitted again when the
chain holds those blocks again.

H2.2 keeps three states apart that LIP-0014 keeps apart: a child that is
revoked, an attestation that is withdrawn, and a row that is closed for cause.
A stop coin that was the seal of the child would turn the revocation of that
child into the closure of its row. A stop coin that was the output after the
seal would be spent by the child's own anchor (LIP-0023 C2.3), and the issuance
would close the row. Another output of the child's seal transaction can be a
stop coin; nothing spends it but its key. H1.3 makes the same two comparisons
with the seal of the parent, for every row and before this section is reached.

The same question exists for the seal that an attestation names. An
attestation whose seal is the stop coin of its row would make a plain
withdrawal a closure for cause. H2.7 gives the verdict for a verifier, the
closure, because the stop coin is read before that seal. Whether such an
attestation is well formed is a matter of the profile of the attestation,
and H4.7 keeps a notary from signing one.

H2.7 follows the place that the decision gives the read: step V18 "keeps
the seal check and adds that the journal holds no closure", and on v4 the
verifier "also reads the stop coin of the row". A child whose attestation
refuses at an earlier step gets that refusal.

### 3. The closure and its journal

A verifier keeps its closures of rows in a journal of the form of LIP-0025,
one entry for each row, and it admits nothing while it cannot write one.

| Rule | Requirement |
| --- | --- |
| H3.1 | A closure of a row is an entry of the kind `row-closed/1` with exactly the members `entry`; `parent`, the identifier of `P` (LIP-0020 section 6), 64 lowercase hexadecimal characters; `ordinal`, the ordinal of the row, an integer of 1 or more; `stop_txid`, 64 lowercase hexadecimal characters, and `stop_vout`, an integer, the outpoint of the stop coin; `tip`, the hash of the tip of the observation that showed the coin spent, 64 lowercase hexadecimal characters; and `height`, the height of that tip. The integers are in the number form of LIP-0020 section 2, and `stop_vout` is at most 4294967295. |
| H3.2 | The verifier writes the entry in the order of LIP-0025 section 3. The search for an entry of the same `parent` and `ordinal` and the write are one atomic step of the store: a row has at most one entry. |
| H3.3 | Where a closure is due and cannot be written, the journal is lost for that verifier (LIP-0025 M5.1): it admits no child of any parent until its operator has restored the journal or started it anew. A restart does not end that state, also where the store and its outside record still agree because nothing was written. The child for which the closure was due refuses as `ROW_CLOSED_FOR_CAUSE` all the same. |
| H3.4 | A closure survives restart, eviction, replacement, non-confirmation, reorganisation and a rotation of the notary's attestation key. A stop coin that is unspent again in a later view reopens nothing, and deleting an entry is no recovery. |
| H3.5 | A closure closes one row: the pair of `parent` and `ordinal`. Another row of the same parent is not touched by it. |
| H3.6 | A verifier whose journal is lost is a newcomer (LIP-0008 J6.9). A recovery by starting anew charges nothing: the new journal holds no closure, the verifier reports none that it does not hold, and it closes a row again when its own view shows the stop coin spent. The journal needs no block boundary. |

H3.3 takes the sentence of LIP-0008 section 5.1 for seals: a failure to persist
a closure permits no effect and requires a recovery of the journal. A verifier
that went on after a failed write would hold a closure in memory alone, and its
next restart would turn a witness into a newcomer without anybody having
decided so. A restart that ended the lost state would do the same one step
later. The continuity check of LIP-0025 compares a store with its outside
record, and after a write that failed the two still agree, so that check alone
would call the journal intact. A verifier therefore keeps a durable mark that
it is lost, outside the journal that could not be written. This profile
requires that behaviour and defines no such mark, and no store was run for it.

H3.6 completes the table of LIP-0025 section 7 for this journal. Nothing
can be charged, because the lost journal held refusals and no allowance:
the only safe charge would be to close every row, and that would end rows
that nobody ended. What is lost with the journal is the closures whose
spends are no longer in the view. LIP-0014 names that limit for both forms
(case S2-K3), and J6.9 makes the verifier say that it is a newcomer.

Whether a verifier keeps these entries in the journal that holds its
closures of seals and of issuers' names is its operator's choice. A reader
of a journal knows every kind of entry that the journal holds (LIP-0025
M1.5).

### 4. The stop account of the notary

The notary keeps the keys of its stop coins in an account that holds
nothing else, creates each coin before the parent is signed, and spends it
with inputs that nobody else can spend first.

These are rules for the notary. A verifier cannot observe them and refuses
nothing for them.

| Rule | Requirement |
| --- | --- |
| H4.1 | Under the Witness profile on Namecoin a stop key has the path `m/84'/7'/<stop-account>'/0/<i>`, the layout of a seal key (LIP-0008 section 11.1). `<stop-account>` is a hardened account index of 10 or above that is no seal account and no row account of the same seed. The account holds stop keys alone. A stop key is not the attestation key (LIP-0014 J2.7). |
| H4.2 | One index `<i>` serves one stop coin. The notary records the index durably before it gives out the address, and it records the outpoint, the parent and the ordinal as each becomes known. An index is not used for a second coin. |
| H4.3 | The notary creates the stop coin in a transaction of its own and gives its outpoint and script to the issuer of the parent. It does so before the parent is signed, and the coin is confirmed by then. |
| H4.4 | The notary keeps the stop key for the life of the parent (LIP-0014 J2.7). |
| H4.5 | The transaction that spends a stop coin takes its fee from the coin itself or from confirmed outputs that the notary alone can spend. No input of that transaction, and no input of an unconfirmed transaction that it depends on, is spendable by another party or by a service that signs without an act of the notary. Its signatures have the hash type `01`. |
| H4.6 | The notary keeps the signed spend and broadcasts it again for as long as it can still confirm. Where its node shows the spend gone and the coin unspent, it spends the coin again. |
| H4.7 | A plain withdrawal leaves the stop coin alone (LIP-0014 J2.7). The notary names no stop coin as the seal of an attestation, and it certifies a child only where the stop coin of the child's row is one that it created and whose key it holds. |
| H4.8 | The notary signs with a stop key one kind of input: the input that spends the recorded stop coin. |

The last clause of H4.7 is what makes "the notary alone can spend it" true
for a verifier that cannot check it. A parent can name any witness key hash
as a stop coin. If the notary certified children under a row whose stop
coin it does not hold, the row could not be ended for cause, and the
stronger form of D5 that LIP-0014 gives v4 would rest on nothing.

H4.5 repeats for the notary what LIP-0008 J6.6 asks of an issuer's break. A
spend that pays its fee from an output which a hot service can also spend
can be displaced by a spend of that output, and a cause that can be
displaced is a cause that a third party can lift for every verifier that
starts later. A coin that carries its own fee needs no second input; the
amount that this takes is the notary's choice and no rule.

The layout has the weakness that LIP-0008 section 11.1 names for the seal
account, as the row account of LIP-0026 has it: the extended public key of
the account together with one private key below it gives every key of the
account. A party with every stop key can end rows. An ended row stays
ended, and such a party creates no authority.

A notary that loses a stop key can no longer end that row for cause. What
remains are the stops of the v3 form: the notary does not certify the row
again, and its witnesses of an authenticated cause refuse it (LIP-0014
J2.7).

### 5. Refusals and their order

| Code | What it reports | Rule | Name |
| --- | --- | --- | --- |
| `ROW_CLOSED_FOR_CAUSE` | The journal holds a closure of the row, or the stop coin of the row is spent in the verifier's view | H2.1, H2.4 | LIP-0014 J2 |
| `ROW_STOP_ALIAS` | The stop coin of the row is the seal of the child or the output after it | H2.2 | New |
| `ROW_STOP` | The stop coin of the row is not on the active chain as the row states it, or is confirmed above the parent's recent block | H2.3, H2.6 | New |

H5.1. The order is that of H2.7: the journal, with the two codes of LIP-0025
for a journal that cannot be read or written and then a closure that it holds;
`ROW_STOP_ALIAS`; `ROW_STOP`; and the spent coin. A refusal of LIP-0022 for the
observation stands before all of them (LIP-0022 B6.1), and so does a refusal of
the parent itself. That includes the refusal of section 1: a parent that H1.4
refuses reaches no check of this order, and no closure is written under it. The
refusal of a parent has no code of this profile; LIP-0026 R1.5 leaves that code
to the members of a grant.

H5.2. `ROW_CLOSED_FOR_CAUSE` is the only one of the three that records
something. `ROW_STOP_ALIAS` and `ROW_STOP` write nothing and state no
cause.

### 6. Vectors

[`vectors/LIP-0027/stop-vectors.json`](../vectors/LIP-0027/stop-vectors.json)
holds 52 vectors over the 27 rules of this LIP, as decisions on stated
facts and on octets.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `parents` | 5 valid, 9 refused | Section 1 on the stated seal and rows of a parent |
| `stops` | 3 passing, 13 refused, 3 compound | Section 2 on a row's stop coin, the seal that the child names, the state of the journal and what a node gives, with the outcome and whether a closure is written |
| `entries` | 1 entry of the kind, 6 that are no entry, 1 of an unknown kind | H3.1 on octets |
| `traces` | 11 traces | Sections 2 and 3 as a state machine: one verifier, its journal, and a list of admissions and of events with the expected outcome of each and the journal at the end |

A vector of the first three groups whose outcome is not the passing one
holds one defect, states the expected outcome and names a neighbour with
the passing outcome that differs from it in that defect. A vector marked
compound holds two defects, states the one that the order reports and names
no neighbour. A trace states the outcome of each of its steps and names no
neighbour. Where a step of a trace states the parent, section 1 is judged
on it first, and the outcome of a refused parent is written
`parent refused`, which is no code.

The traces hold the histories of the section "Motivation". In `trace-01` a
verifier sees the spend in its mempool, the spend is evicted, and the row stays
closed across a restart. In `trace-02` a verifier that starts after the
eviction admits the child. In `trace-04` the coin is not on the chain as the
row states it: the row refuses as `ROW_STOP`, and the journal stays empty.

Six vectors of the group `parents` are about the seal transaction of the
parent. `parent-09` names the output after the seal as a stop coin and is
refused, and `parent-10` names the output two after the seal and is valid.
`parent-11` to `parent-13` have the seal at index 5: the output 6 is refused,
and the outputs 7 and 4 are valid. `parent-14` has the output after the seal in
its second row. In `trace-10` a verifier meets such a parent at the admission
of a child, while its node shows that output spent by the parent's own anchor:
it refuses the parent, and its journal stays empty. In `trace-11` a verifier
restarts after a closure could not be written. It stays lost, also after the
spend has left its view, until its operator starts the journal anew.

The limits of the file are these. Identifiers, transaction ids, block
hashes and scripts are placeholders. The journal of a trace is a list of
entries with a state; its commitments and its outside record are those of
LIP-0025 and are not repeated here. A trace runs its steps one after
another: no vector holds two admissions at one moment. No vector reads a
node or a mempool.

No checker for these vectors is in this repository. The expected outcomes
were stated by hand, computed by one implementation and decided again by a
second one that shares no code with the first; neither is published here.
Both come from the author of this text, so an error of understanding that
they share is in the vectors. The vectors bind nothing until both owners
accept the rules that they follow.

## Sources

No node, no signer and no store was run for this LIP.

| Statement | Source |
| --- | --- |
| The stop coin, the three states of a row and their codes, and the cases S2-10 and S2-K3 | LIP-0014 section 10.1 |
| A validated spend of a seal is persisted before any further admission, and a failure to persist requires a recovery of the journal | LIP-0008 section 5.1 |
| A verifier whose closure journal is lost is a newcomer; no input of an issuer's break is spendable by a hot service | LIP-0008 section 5.2, rules J6.9 and J6.6 |
| A transaction that spends an output which is missing or already spent is invalid | Namecoin Core at the tag `nc28.0`, `src/validation.cpp`, the check that reports `bad-txns-inputs-missingorspent` |
| The path of a seal key and the weakness of its layout | LIP-0008 section 11.1 |
| The row stop key: its owner, its holder and what it signs | The key registry, entry "Row stop key, v4" |

## Alternatives

- **One code for a missing coin and a spent one.** A verifier would need
  one read. A row whose coin was never confirmed would then be recorded as
  ended by its notary, at every verifier that read it, and a closure is
  evidence that a key signed.
- **A closure only with the spending transaction in hand.** The record
  would name the transaction that spent the coin. A node without an index
  of spent outputs gives that transaction only to a verifier that watches
  every block and its mempool, and a verifier that starts later would see a
  spent coin and record nothing.
- **Going on after a failed write**, with the closure held in memory. A
  verifier would stay available. Its next restart would forget the closure,
  and LIP-0008 section 5.1 requires a recovery of the journal for a seal.
- **Charging every row as closed after a lost journal**, as a lost ledger
  charges every row as consumed. It would end rows that nobody ended, and a
  closure cannot be undone by a new parent for the same row.
- **One stop coin for every row of a notary in a parent.** The parent would
  carry one outpoint. A cause for one row would close all of them, against
  the locality of LIP-0014 J2.4a.
- **The stop coin anywhere outside the child's seal transaction**, as
  LIP-0026 asks of the coin of a row. It is one comparison of two
  transaction ids. An output of that transaction that is neither the seal
  nor the output after it is spent by nothing but its key, so the narrower
  rule refuses only what misbehaves.

## Security consequences

- **A closure is as permanent as its journal.** A witness that keeps its
  journal refuses the row for good. A witness that loses it is a newcomer
  and says so (H3.6).
- **A newcomer admits a row whose spend left the view.** That is the limit
  of every state that is read from one view, and LIP-0014 accepts it with
  the decision (case S2-K3). H4.6 has the notary spend again.
- **Whoever holds the stop key can end the row.** A thief of that key ends
  rows and creates no authority. A row that is ended stays ended; the
  parties issue a new parent.
- **A closure does not show misconduct.** It shows that the stop coin was
  spent. Who was at fault, and whether a cause was stated, is read from the
  evidence that the profile of the attestation defines.
- **A verifier cannot see who holds the stop key.** H4.7 puts that check on
  the notary: it certifies no child under a row whose stop coin is not its
  own.
- **A journal that cannot be written stops the verifier.** A party that can
  make a store fail can stop admissions there. It cannot make the verifier
  admit a closed row.
- **`ROW_STOP` is no evidence.** A missing coin says nothing about the
  notary, the issuer or the delegator, and it MUST NOT be reported as a
  cause.

## Conformance impact

None on normative v0.1 and none on Grant v3: profile `/2` of LIP-0014 has
no stop coin. No conformance class is added. The cases S2-10 and S2-K3 of
LIP-0014 get a reading for v4 from sections 2 and 3, and they still run on
nodes and on a real store.

## Open questions

- **The owners' acceptance** of each rule, and first of the four points
  that the section "What is decided and what is proposed" lists.
- **The reads on a node.** How a verifier reads, against one tip, whether
  an output is unspent with the mempool included, and what the pinned build
  offers for it (LIP-0022, open questions).
- **The index and the custody of the stop account**, and the custody of a
  notary's keys in general (LIP-0014 section 6.3).
- **The amount of a stop coin** and the fee of its spend over the life of a
  parent.
- **The attestation on v4**: its members, its anchor, the frame that states
  a cause, and whether an attestation may name a seal that is the stop coin
  of its row.
- **The octets of a row**, with its stop coin, in a v4 grant.
- **Closures across replicas.** LIP-0008 section 5.1 leaves the propagation
  of a closure between replicas open, and so does this profile.
- **The mark of a lost journal.** H3.3 has a journal stay lost across a restart
  after a write that failed, while its store and its outside record still
  agree. What a verifier keeps durably to know that, and where, is not defined.
- **A run** of the cases S2-10 and S2-K3 on nodes and on a qualified store.
