# LIP-0025: Journal continuity profile for Grant v4

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** the form of a journal that must not go back unnoticed, its
  record outside the store, the check that tells an intact journal from a
  lost one, the recovery of a lost journal, and the issuer's journal of
  consumed consents
- **Builds on:** LIP-0014 section 9.1 (J1.4), LIP-0008 sections 4, 5.1 and
  5.2, LIP-0020 sections 1, 4 and 7.4, and LIP-0022 section 2

## Summary

An issuer records a consent as consumed and signs a grant. Its store is
then restored from the backup of the day before. The record is gone, the
same consent passes again, and nothing in the store says that anything is
missing. LIP-0020 makes a consent single-use through that record, LIP-0014
bounds the consumption of a row through a ledger, and LIP-0008 closes a
grant for good through a journal. Each of them holds only while the journal
is the journal that was written.

LIP-0014 section 9.1 states the contract for such a store: its continuity
is proved against a record outside it, and equal positions prove nothing.
It calls the form of that record an open deployment profile and names a log
whose entries are bound by hashes as one possible form. This LIP proposes
that form:

- a journal as a sequence of entries whose history is bound by hashes
  (section 1);
- the outside record, which takes a new state only as the successor of the
  exact state that it holds (section 2);
- the order of one write: the store, then the outside record, then the
  effect (section 3);
- the continuity check with four outcomes: intact, pending, fenced, lost
  (section 4);
- a lost journal and its recovery, with a block boundary that the writer's
  node cannot have accepted before the loss (section 5);
- the first journal on this form: the issuer's journal of consumed consents
  (section 6);
- what the other journals of the specification take from the profile
  (section 7);
- three refusal codes (section 8) and vectors (section 9).

It selects no product. Which store holds a journal and which service holds
the outside record are choices of a deployment, and no store is qualified
by this text.

## What is decided and what is proposed

The contract is decided, and its form is not. LIP-0014 section 9.1 records
Ivan Oparin's decision of 2026-11-14 on rows (J1), with the co-author's
agreement pending; its rule J1.4 has the ledger of a row live in a store
whose continuity is proved against a record outside the store, and it
states the order of a reservation, the continuity check, the fenced writer
and the two ways of recovery. The same section says that this is a contract
and no format. LIP-0008 section 5.2 has a verifier whose closure journal is
lost become a newcomer (J6.9; accepted on 2026-11-13, agreement pending).
LIP-0020 section 7 records the decision of 2026-11-14 under Ivan Oparin's
delegation, open to his override and awaiting the co-author, that a consent
is used once and that the issuer records its identifier as consumed. This
LIP changes none of them.

Every rule of this LIP is the draft's proposal: the hash-bound history and
its tag, the act that creates a journal, the one operation of the outside
record, the four outcomes of the check and their order, what a reader that
does not write does, the two entries of a recovery, the block boundary with
its two hours, the entry and the steps of the consent journal, and the
three codes. Neither owner has decided them, and nothing of them is built
or run. The owners accept or change them through this LIP, under LIP-0001.

| Open point | Proposed here |
| --- | --- |
| LIP-0014 section 9.1: "How the outside record commits to the history, and how continuity is proved, is an open deployment profile" | Sections 1, 2 and 4 |
| The same section: "How the profile knows that the boundary is later than the loss, with a node that may lag, is part of the open profile" | Section 5 (M5.4) |
| LIP-0008 section 5.1: evidence is kept "under a recovery and anti-rollback profile", whose encoding is open | Sections 1 to 5 give the profile. The entries of a closure journal come with the rules that write them |
| LIP-0020 W7.9: the issuer records a consumed consent "durably and before it signs the grant" | Section 6 |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The history commitment, the operation of the outside record and the continuity check, as functions of stated values (sections 1, 2 and 4) | Yes | The owners' acceptance |
| The issuer's journal of consumed consents, as a state machine (section 6) | Yes | The same |
| A store and an outside record that meet sections 2 and 3 | No | The choice of a store, of the service that holds the outside record and of the fencing service, and the cases of LIP-0014 (S1-5, S1-5-ABA, S1-6) on that real store |
| The ledger of a row, the closure journals and the notary's record on this form | No | Their entries, which come with the rules that write them |

## Motivation

Three failures look alike from inside a store, and only one of them is
harmless.

**A restore.** A backup brings a store back to an earlier state. Every
entry is well formed, and the position is a position that the store once
had. A journal that trusts its own contents continues from there.

**Two histories at one position.** LIP-0014 gives the trace. Rows A and B
each have a cap of 60. A reservation of 40 for A is written at position 1,
and the process stops before the outside write; that image of the store is
kept. The store is restored to position 0, a reservation of 40 for B takes
position 1, the outside record follows, and the effect is performed. Then
the first image is restored. Its position equals the outside position, it
holds no record of B, and a further 40 under B passes as a first use: 80
against a cap of 60. A record of positions cannot tell the two images
apart.

**A crash between two writes.** The store has an entry that the outside
record has not yet taken. Here nothing was lost: no effect was performed
for that entry, and the write can be completed.

A profile has to refuse the first two and to complete the third, and it has
to do so from what a process finds when it starts.

## Current state

- LIP-0014 section 9.1 (J1.4) states the contract and says that nothing of
  it was built or run, and that no executor qualifies for `spend` without a
  profile and before the cases S1-5, S1-5-ABA and S1-6 pass on its real
  store. It adds that the closure journals of its section 10.1 and of
  LIP-0008 section 5.2 and the denials of LIP-0013 section 3.6 also have to
  tell an empty store from a lost one.
- LIP-0008 section 4 has the replicas of one executor share one
  authoritative durable journal and admit no new effect when it is
  unavailable. Its open questions list the consistency, the recovery and
  the anti-rollback requirements of that journal.
- LIP-0020 W7.9 has the issuer record the identifier of a consent as
  consumed, durably and before it signs the grant, and says that a verifier
  cannot check the single use.
- The reference laboratory states the same gap for its v4 code: durable
  consumption of a consent before signing needs an issuer journal with its
  own contract for concurrency and recovery (`swarma-chain-lab` at
  `b03c6f10fad1be135e780d8b1f556fc46805eb06`,
  `experiments/grant-v4/wire/UNRESOLVED_QUESTIONS.md`).

## Proposal

### 1. A journal and its history

A journal is a sequence of entries in one store, and one hash value stands
for the whole sequence: two journals with the same value hold the same
entries in the same order.

| Rule | Requirement |
| --- | --- |
| M1.1 | A journal has an identity, 32 octets that its operator generates at random when it creates the journal, and a position, the number of its entries. Entries are added at the end and never changed or removed. |
| M1.2 | An entry is one JSON object in the canonical form of LIP-0020 section 1, of at most 2048 octets, with a member `entry` that names its kind and the members that the rule of that kind lists. |
| M1.3 | The history commitment of a journal at position `n` is `c(n)`, a value of 32 octets. `c(0)` is `D` of the 32 octets of the identity. `c(n)` is `D` of the 32 octets of `c(n-1)` followed by `e(n)`, the octets of the entry at position `n`; the earlier commitment enters as its octets and never as hexadecimal text. For any octets `x`, `D` of `x` is the SHA-256 of three parts in sequence: the SHA-256 of the tag, the SHA-256 of the tag once more, and `x`. The tag is the 16 octets of `swarma-journal/1`. |
| M1.4 | The store writes an entry and the new position in one atomic write. |
| M1.5 | A store that holds an entry which is not as M1.2 says, or of a kind that its reader does not know, is a lost journal for that reader (section 5). |

Written out, with `||` for one string of octets after another:

```text
D(x) = SHA-256( SHA-256(tag) || SHA-256(tag) || x )
c(0) = D( identity )
c(n) = D( c(n-1) || e(n) )
```

`D` is the tagged hash that LIP-0020 W4.1 uses for a typed digest, applied
here to octets that are no payload. W4.2 takes the tag of a typed digest
from the `type` of its payload; a history commitment has no payload and no
`type`, so M1.3 states its tag. The tag is no entry of the registry of
LIP-0020: a history commitment is no object and is never signed. It uses
the same construction so that no commitment can be taken for a signing
digest.

The canonical form matters although an entry never leaves its operator. A
replica, a recovery tool and a second implementation each compute the
commitment from the entries, and they agree only on the same octets.

### 2. The outside record

The outside record holds the identity, the position and the commitment of
one journal, and it takes a new commitment only as the successor of the
exact one that it holds.

| Rule | Requirement |
| --- | --- |
| M2.1 | The outside record of a journal holds four values: the identity of the journal, a position, the history commitment at that position, and the current write token, a number. |
| M2.2 | It lives outside the domain that a restore of the store reaches: no backup, snapshot or copy that can bring the store back to an earlier state brings the outside record back with it. A file on the host of the store that is backed up with the store is no outside record. |
| M2.3 | It has one operation that changes the history, `advance`, with five inputs: an identity, a token, a position, a commitment `from` and a commitment `to`. It accepts the operation only when the identity, the token, the position and `from` equal the four values that it holds. It then holds the next position and `to`. In every other case it changes nothing. |
| M2.4 | The write token changes only by the operator's act of fencing, which sets a larger number. The store accepts a write only from a writer that holds the current token, and so does the outside record (M2.3). |
| M2.5 | No operation lowers the position of an outside record, replaces its commitment at an unchanged position or changes its identity. |
| M2.6 | A journal is created in one act of its operator: a store with the identity and no entry, and an outside record that holds that identity, position 0, the commitment `c(0)` and a first write token, a number that the operator chooses. An outside record is created once for an identity. A store without its outside record is a lost journal (M4.5), so an act that stops halfway creates none. |

The outside record does not read entries and computes no hash. It is a
register with a compare-and-swap, which is what keeps the demand on the
service that holds it small. Whether the journal is the journal that it
describes is decided by the reader of the journal, in the check of section
4.

Where the outside record lives decides what the check is worth, and
LIP-0014 says so: one that is restored together with the store notices
nothing. The profile states the property in M2.2 and does not name a place.

### 3. The order of one write

An entry is written to the store first and to the outside record second,
and only then does the effect happen that the entry stands for.

| Rule | Requirement |
| --- | --- |
| M3.1 | A writer adds an entry in this order: the continuity check of section 4; the atomic write of the entry and the new position to the store; `advance` at the outside record, from the commitment before the entry to the commitment with it. |
| M3.2 | The act that the entry records, an effect, a signature or an acknowledgement of success, happens only after `advance` was accepted. |
| M3.3 | The other order, the outside record first, is another profile and is not mixed with this one. |

This is the order of a reservation in LIP-0014 J1.4, stated for any entry.
A crash after the store write and before `advance` leaves the store one
entry ahead. No effect was performed for that entry, so the write can be
completed (M4.3), and the entry stays. Under a row the reservation stays
charged, and the same request completes on a retry without a second charge
(LIP-0014 section 9.1). A consent stays consumed and unused, and the
recipient consents again (LIP-0020 W7.9).

### 4. The continuity check

A reader compares what the store holds with the outside record and reaches
exactly one of four outcomes; only the first lets it write.

| Rule | Requirement |
| --- | --- |
| M4.1 | The check runs when a process starts, when a replica joins, and before every write. The reader computes the commitment from the identity and the entries that the store holds; it does not take a commitment that the store states about itself. |
| M4.2 | **Intact:** the identities are equal, the positions are equal and the commitments are equal. |
| M4.3 | **Pending:** the identities are equal, the store is exactly one position ahead, and the commitment of the store at the position of the outside record equals the commitment of the outside record. The writer completes `advance` for that entry before it does anything else, and the journal is then intact. The entry stays. Whether the act that it records may still follow is stated by the rule of that kind of journal. |
| M4.4 | **Fenced:** the writer does not hold the token of the outside record. It writes nothing to the store and nothing to the outside record. |
| M4.5 | **Lost:** every other state. Among them: an outside record that is absent or cannot be read; a store that is absent, cannot be read or was created anew; another identity; equal positions with different commitments; a store behind the outside record; a store ahead by more than one position; a store one position ahead whose earlier history is not the history of the outside record. |
| M4.6 | The reader decides in this order, and the order alone gives the outcome: the outside record can be read; the store can be read (M1.5); the identities are equal; the writer holds the token; then the positions and the commitments. M4.2, M4.3 and M4.5 say what the last step finds for a writer that holds the token. A writer that does not hold it is fenced, whatever the positions and the commitments are. |
| M4.7 | A reader that does not write holds no token, and its check has no step for one. Where the outcome is intact it reads. Where it is pending it cannot complete the write: it takes no decision from the journal and reads again later or refuses. Where it is lost it refuses as a writer does. |

The token stands before the comparison of histories for a reason. A replica
that was cut off sees an old copy of the store beside a newer outside
record. That is the picture of a restore, and it is no loss: another writer
went on. A reader that called it lost would have its operator recover a
journal that is in order.

Equal positions never suffice. The trace of the section "Motivation" ends
with equal positions and different commitments, and M4.5 refuses it.

A pending journal is a moment between two writes. Its last entry is in the
store, and no act has followed it yet (M3.2). A reader that only reads
cannot tell whether the writer will complete the write or was fenced, so
under M4.7 it waits for the outside record and decides nothing meanwhile.

### 5. A lost journal and its recovery

A lost journal refuses every act that needs it, and it comes back in one of
two ways: the store is restored and passes the check, or the operator
starts a new journal that charges everything that the old one could have
held.

| Rule | Requirement |
| --- | --- |
| M5.1 | A reader of a lost journal refuses every act that needs the journal. It never takes a missing entry as a sign that nothing happened. |
| M5.2 | **Restoring.** The operator puts a store in place. It is the journal again only when the check of section 4 gives intact or pending against the outside record that the journal had. |
| M5.3 | **Starting anew.** In one attended act the operator fences the writers of the lost journal, reads its clock, and creates a journal with a new identity under M2.6. The first entry of the new journal, written under section 3, has the kind `recovery/1` and exactly the members `entry`; `previous`, the identity of the lost journal, 64 lowercase hexadecimal characters; and `fenced_at`, the reading of the clock in seconds, an integer in the number form of LIP-0020 section 2. The outside record of the lost journal is kept. |
| M5.4 | **The block boundary.** A journal whose rules count from a block gains, after its recovery entry, one entry of the kind `boundary/1` with exactly the members `entry`; `block`, the hash of a block, 64 lowercase hexadecimal characters in the byte order in which a node prints it (LIP-0020 W3.5); `height`, the height of that block; and `header_time`, the time in its header in seconds. The last two are integers in the number form of LIP-0020 section 2. The block is on the active chain of a healthy observation (LIP-0022 section 2), and the time in its header is more than 7200 seconds later than `fenced_at`. |
| M5.5 | What a new journal charges is stated by the rule of each kind of journal, and it covers everything that the lost journal could have held, whether or not a list of it survived. Until a journal that needs a block boundary has one, nothing under it counts as new. |

Starting anew is a recovery by charging, as LIP-0014 names it for rows: the
operator cannot know what the lost journal held, so the new journal treats
all of it as used. For a row that means fully consumed; for a consent,
consumed (M6.6); for a closure journal, that its reader is a newcomer and
reports no witness state (LIP-0008 J6.9).

The two hours of M5.4 are the bound of consensus and no tuning. A node
accepts a block only when the time in its header is at most two hours ahead
of the node's clock; LIP-0022 lists the place in the source of Namecoin
Core where that rule was read. A block that a node had accepted before the
fencing therefore has a header time of at most `fenced_at` plus 7200
seconds, and a block with a later header time had been accepted by no node
whose clock was right. A node connects a block only after the block below
it, so the same holds for every block above the boundary. The writer of the
lost journal acted only on blocks that its own node had accepted, all of
them before the fencing. Everything that the lost journal could hold
therefore rests on blocks below the boundary, and nothing in it rests on
the boundary block or on a block above it.

That is less than the words of LIP-0014 section 9.1, and enough for what
they serve. LIP-0014 asks for a boundary block that is known to have been
mined after the loss and says of a parent above it that it was signed after
the loss. A header time cannot show when a block was mined: a miner can
build a block whose header is ahead, keep it, and publish it when nodes
accept it, and a party that works with that miner can sign a parent against
the block before the fencing. M5.4 does not exclude such a parent. It shows
what the charging needs: the lost journal held no record under that parent,
because the writer's node did not have the block and the writer admits
nothing on a block that its node does not have. Whether the owners take
this reading is an open question of this LIP.

The argument assumes that the operator's clock is right at the act, and
that the writer's node kept the consensus rule with a right clock while the
lost journal was written. The cost is that a boundary appears two hours
after the fencing at the earliest, and usually a few blocks later.

A reorganisation that removes the boundary block from the active chain is
not treated here. The rules of the journals that count from a block
(section 7) have to say what such a journal does then, and this LIP defers
the point to them.

### 6. The issuer's journal of consumed consents

An issuer consumes a consent by one entry in one journal for its grant key,
written before the grant is signed, and after a loss it treats every
consent that existed before the recovery as consumed.

| Rule | Requirement |
| --- | --- |
| M6.1 | One grant key has one journal of consumed consents. Every signer that signs grants with that key consumes in it, and no replica keeps a journal of its own. |
| M6.2 | A consumed consent is an entry of the kind `consent-consumed/1` with exactly the members `entry`; `consent`, the `id` of the consent event; `contract`, the identifier of the contract; `created_at`, the `created_at` of the event; and `consumed_at`, the issuer's clock at the write, in seconds. The two identifiers are 64 lowercase hexadecimal characters each, and the two times are integers in the number form of LIP-0020 section 2. |
| M6.3 | The issuer consumes a consent after the checks of LIP-0020 W7.4 to W7.8 passed, and before it signs the grant. The steps, in order: the continuity check (section 4); the clock (M6.5); the boundary (M6.6); the search for an entry with this `consent`; the write of the entry under section 3. It signs the grant only after `advance` was accepted. |
| M6.4 | The search and the write are one atomic step of the store. Of two attempts with one consent, one writes the entry and the other finds it. |
| M6.5 | The issuer's clock does not read less than the largest `consumed_at` or `fenced_at` of the journal. |
| M6.6 | After a recovery by starting anew, the issuer treats as consumed every consent whose `created_at` is not later than the `fenced_at` of the recovery entry. |
| M6.7 | The journal keeps every entry. Nothing releases a consumed consent: not a crash before the signature, not an issuance that failed, not a revocation of the grant. |

| Step of M6.3 | Refusal |
| --- | --- |
| The continuity check gives lost | `JOURNAL_LOST` |
| The continuity check gives fenced | `JOURNAL_FENCED` |
| The clock reads less than the journal's largest time | `JOURNAL_CLOCK` |
| The consent is not later than the boundary of a recovery | `CONSENT_CONSUMED` |
| An entry with this consent exists | `CONSENT_CONSUMED` |

M6.6 rests on the issuer's clock. A consent cannot have been consumed
before it was created: W7.8 refuses a `created_at` that is later than the
issuer's clock at the consumption. Whatever the lost journal held was
consumed before the loss, so its `created_at` is not later than a reading
that the clock gave before the fencing. That reading is not later than
`fenced_at` where two things hold: the clock did not run ahead of the true
time while the lost journal was written, and it is right at the act of
recovery. The boundary then covers every consent of the lost journal.

Where the first does not hold, the boundary has a gap. A clock that ran ten
minutes ahead before the loss let the issuer consume consents whose
`created_at` lay up to ten minutes ahead. Those whose `created_at` is later
than `fenced_at` are not covered, and such a consent passes once more until
the age rule of W7.8 refuses it.

The cost of the boundary falls on recipients: a consent that was given
before the recovery and not yet used has to be given again.

An entry older than 72 hours decides nothing any more, because the age rule
of W7.8 refuses its consent before the journal is asked. It stays, since
the commitment covers every entry.

M6.5 gives the issuer the guard against a clock that went back, and the
journal protects the guard: the largest time is part of a history that the
outside record binds.

What LIP-0020 says about the limit of single use stands. The journal makes
an honest issuer use a consent once, also across a crash and a restore. A
verifier still sees one issuance and cannot see the journal.

### 7. What the other journals take from the profile

The profile is the same for every journal of the specification that must
not go back; what differs is the entries and what a recovery charges.

| Journal | Rule that needs it | What a recovery by starting anew charges |
| --- | --- | --- |
| Consumed consents of an issuer | LIP-0020 W7.9 | Section 6 of this LIP |
| The ledger of a row at its executor | LIP-0014 J1.3 and J1.4 | Every row that could have had a record is fully consumed; a row has a first use only where its parent's checkpoint lies above the block boundary (LIP-0014 section 9.1) |
| Closures of a seal and of an issuer's name at a verifier | LIP-0008 sections 5.1 and 5.2 | The verifier is a newcomer and reports no witness state (J6.9) |
| A row closed for cause, at a verifier | LIP-0014 section 10.1 (J2.4a) | Not stated yet; LIP-0014 section 9.1 says only that this journal has to tell an empty store from a lost one |
| The notary's records of one child for each row and of the succession of its seals | LIP-0014 J1.6 and J2.3 (a) | Not stated yet |
| Denials of a key holder | LIP-0013 section 3.6 | Not stated yet |
| The signer's record of a seal index and of the recorded revocation | LIP-0008 sections 11.1 and 11.3 | Not stated yet; custody is open (LIP-0024 section 5) |

This LIP defines the entries of the first journal alone. The entries of the
others come with the rules that write them, and each of those rules has to
say what "could have held" means for it.

### 8. Refusal codes

| Code | Meaning |
| --- | --- |
| `JOURNAL_LOST` | The continuity check gives lost. The act that needed the journal is refused, and the operator has to restore the journal or to start anew |
| `JOURNAL_FENCED` | The writer does not hold the current token. Another writer is the writer of this journal |
| `JOURNAL_CLOCK` | The clock reads less than the largest time that the journal holds |

None of them says anything about a grant, a consent or a name. A refusal
with one of them is retried after the journal is in order.

### 9. Vectors

[`vectors/LIP-0025/journal-vectors.json`](../vectors/LIP-0025/journal-vectors.json)
holds 66 vectors over the 33 rules of this LIP.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `commitments` | 7 histories, of which 1 holds a recovery entry and a boundary entry; 12 octet strings, of which 3 are entries of a known kind | M1.3 on an identity and the octets of entries; M1.2 and M1.5 on octets, with the forms of M5.3, M5.4 and M6.2 |
| `continuity` | 5 intact or pending, of which 2 are for a reader that does not write; 3 fenced; 8 lost | Section 4 on the stated state of a store, of an outside record and of a writer, or of a reader without a token |
| `outside` | 2 accepted, 8 refused | M2.3 and M2.4 on a record and one operation |
| `boundaries` | 5 blocks, of which 1 is a boundary; 4 parents, of which 1 is new | M5.4 on a time of fencing and a block; M5.5 on the block that a parent signs |
| `consents` | 12 traces | Section 6 as a state machine: a trace of steps on a journal and its outside record, with the outcome of every step and the positions and commitments at the end |

A vector of the first four groups whose outcome is not the passing one
holds one defect and names a neighbour with the passing outcome. A trace
states the expected outcome of each of its steps; it has no neighbour,
because its steps are its controls.

The limits of the file are these. Identities, identifiers of consents and
of contracts and block hashes are placeholders. A trace runs its steps one
after another: no vector holds two writers at the same moment, so M6.4 is
shown only as the outcome that it must have. No vector runs a store, an
outside record or a clock; a crash is a step of a trace that says where the
write stopped.

No checker for these vectors is in this repository. The expected outcomes
were stated by hand, computed by one implementation and decided again by a
second one that shares no code with the first; neither is published here.
Both come from the author of this text, so an error of understanding that
they share is in the vectors. The vectors bind nothing until both owners
accept the rules that they follow.

## Alternatives

- **A record of positions alone.** It is the smallest outside record. The
  trace of the section "Motivation" passes it.
- **The outside record first, the store second.** No crash then leaves the
  store ahead. Every crash between the two writes leaves the outside record
  ahead instead, which is a lost journal. LIP-0014 names this order as
  another profile.
- **An outside record that verifies entries.** It would compute the next
  commitment itself and could refuse an entry that does not extend the
  history. It would have to receive every entry, and the service that
  holds it would see the contents of the journal.
- **A signed journal.** Each entry could carry a signature of its writer.
  A signature shows who wrote an entry and not that the journal is
  complete; a restored store has valid signatures throughout.
- **A waiting time in place of the boundary of M6.6.** After a loss the
  issuer could issue nothing for 72 hours, after which no consent of the
  lost time passes the age rule. The boundary reaches the same result at
  once and costs the recipients of the last 72 hours a new consent.
- **A shorter time than two hours in M5.4.** It would end a recovery
  sooner. A block that was accepted before the fencing can carry a header
  time up to two hours ahead, so a shorter time proves nothing.

## Security consequences

- **The outside record is the root of the journal's worth.** Whoever can
  replace the store and the outside record together can go back unnoticed.
  M2.2 states what a deployment has to achieve and cannot enforce it.
- **A lost journal is an outage by design.** A reader refuses until its
  operator acts. An attacker that can corrupt a store can stop its
  executor or its issuer; it cannot make it spend twice or sign twice.
- **Starting anew costs what the journal protected.** Rows are charged as
  consumed, consents have to be given again, and a verifier forgets what it
  witnessed. That is the price of not trusting a store that cannot show
  its history, and an operator pays it only by an attended act.
- **A header time does not date a block.** The boundary shows that the
  writer's node had not accepted a block before the fencing, and not when
  the block was made. A parent that was signed before the loss against a
  block which a miner kept back has a first use after a recovery. The lost
  journal held no record under it.
- **The clock enters twice.** `fenced_at` decides the boundary of a
  recovery, and `consumed_at` guards against a clock that went back. A
  clock that is behind at the act of recovery sets the boundary too early,
  and consents of the difference could pass again. A clock that ran ahead
  while the lost journal was written leaves the consents of that difference
  outside the boundary as well (section 6). The operator checks the clock
  as part of the act.
- **A new kind of entry stops every reader that does not know it.** Under
  M1.5 such a reader finds the journal lost, and a recovery by starting
  anew charges everything. A deployment that adds a kind of entry, or a
  second version of one, updates every reader before the first such entry
  is written.
- **The fencing service is trusted.** A writer that holds the current
  token is the writer. Who may raise the token, and how a writer learns it,
  is a choice of the deployment.
- **Single use still rests on the issuer.** The journal binds an issuer
  that keeps it. An issuer that signs without it is not held back by
  anything that a verifier can see (LIP-0020 W7.9).

## Conformance impact

None on normative v0.1 and none on Grant v3. No conformance class is added.
The cases S1-5, S1-5-ABA and S1-6 of LIP-0014 keep their meaning and still
run on a real store; the traces of this LIP state the same histories for
the consent journal as decisions on stated values.

## Open questions

- **The owners' acceptance** of the hash-bound history, of the one
  operation of the outside record, of the four outcomes and their order, of
  the block boundary and of the consent journal.
- **"Mined after the loss".** LIP-0014 section 9.1 asks for a boundary
  block that is known to have been mined after the loss. M5.4 shows that
  the writer's node had not accepted the block before the fencing, which a
  header time can show, and not when the block was mined, which it cannot.
  Whether that reading satisfies the decided text is the owners' to say.
- **A boundary block that a reorganisation removes.** Section 5 defers
  it to the journals that count from a block. The reading that fails closed
  is that such a journal has no boundary until a new one is written.
- **New kinds of entry.** How a kind is added to a journal in use without a
  reader that finds the journal lost (M1.5).
- **The store and the outside record of a deployment.** Which products,
  where the outside record lives so that M2.2 holds, and the cases on the
  real store.
- **The fencing service.** Who raises a token, how a writer learns the
  current one, and how a replica joins.
- **The entries of the other journals** of section 7, and what a recovery
  charges for the four journals that do not state it yet.
- **Two writers at one moment.** M6.4 states the outcome; how a store
  provides the atomic step is part of its qualification.
- **How long an issuer may stay without its journal** before its operator
  starts anew, and who attends the act.
