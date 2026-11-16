# LIP-0030: Action profile no. 1, an agent session on a host

- **Status:** Draft. Nothing in this file is in force by its own word. Every
  rule is marked as restating a cited text, as proposed here, or as open.
- **Created:** 2026-11-16
- **Affects:** what a v4 grant lets an executor do when the executor is the
  service set of a host that starts the run of an agent: the action texts,
  the limit kinds, what the executor checks at a start, what it checks while
  the session lasts, and which events end or suspend the authority
- **Builds on:** LIP-0006 section 7, LIP-0007 section 1, LIP-0008 sections 2,
  2.1, 3.1, 4, 5, 5.1, 5.2, 7.1, 11.4 and 12, LIP-0010 section 10, LIP-0013
  section 3.6, LIP-0014 sections 8 and 11.1, LIP-0017 section 8, LIP-0018
  sections 2 and 3, LIP-0020 section 11, LIP-0022 sections 1 to 3 and 6,
  LIP-0025 sections 3, 4, 5, 7 and 8, LIP-0026 sections 2, 3, 5, 6 and 9,
  LIP-0027 sections 2 and 3, LIP-0028 and LIP-0029 sections 1, 2, 6, 8 and 11
- **Deciders:** both owners

## Summary

A grant of version 4 names an executor, a recipient, a list of action texts
and a list of limits (LIP-0020 W11.2 to W11.4). No profile defines an action
text or a limit kind yet: "Which texts name an action is for the action
registry (LIP-0007; LIP-0008 section 12.3), which is open" (W11.4). Until a
profile defines an action, a v4 grant has no effect at an executor.

This draft proposes the first such profile. It defines the **authority** of
an agent session and not the life of a process. It states:

1. the executor as a set of three services, which part writes which journal,
   and the verdict that one part hands to the other, as an object with fixed
   content (section 2);
2. five action leaves, of which four may stand in `actions`, and three limit
   kinds, each with its full text and the registry section that it would
   enter (section 3);
3. one table of the five states of the authority against 36 events. Each
   cell has one outcome: the next state, who acts, the durable record that
   is written before the effect, and a refusal code of the one list of
   section 6; or it says that the event cannot occur, with the reason
   (section 4);
4. the rules that hang off single cells of that table (section 5);
5. the one closed list of refusal codes (section 6);
6. what the profile does not decide, and what it needs from the station
   contract of the host (section 7).

The states of a process belong to the station contract of the host. This
draft names the rows of that contract where it hands a process over and
defines none of them.

The draft adds no member to the grant, changes no other LIP and defines no
octets: the requests are signed invocations, and the invocation has no
members yet (LIP-0020 section 3, type `swarma-invocation/1`). It has no
vectors. Nothing of it is implemented.

## What is decided and what is proposed

**Decisions of one owner.** One owner decided the following. No record in
`decisions/` holds any of it yet, and the co-author's answer is not known.

| Date | Decision | Where it stands here |
| --- | --- | --- |
| 2026-11-16 | The default agent is long-lived. Each runs in an OS account of its own, with an identity of its own and with keys that services hold. The run for one task is a special case | The reason for this profile; it decides none of its rules |
| 2026-11-16 | A v4 grant has no clock member. The time of a session and of its renewal is counted in block heights | It agrees with the text that the specification holds: the window of a v4 grant is a pair of heights (LIP-0008 section 7.1; LIP-0020 W11.2) |
| 2026-11-16 | The grant names the agent that works, and not the party that asks | Section 3.1, member `recipient` |
| 2026-11-16 | The budget of a model is a separate grant | Section 7 |
| 2026-11-16 | A restart is by a signed request, and the host must be able to bring a crashed session back | Section 5.2. How the host does so alone is proposed there and awaits the owner's yes (Q15) |

**Marks.** Every rule carries one of three marks. A mark that restates also
carries the state of its source.

| Mark | Meaning |
| --- | --- |
| **R** | Restates the cited text and adds nothing. The tag after it is the state of that text: **[F]** text that the specification carries as its rule for v4, in a LIP whose status is Draft; **[C]** carried or decided by one owner, with the co-author's agreement pending; **[D]** a proposal of a Draft that neither owner has accepted |
| **P** | Proposed here. Neither owner has decided it |
| **O** | Open. The question and who decides it are in the section "Open questions" |

An **R** inside a sentence covers the quoted words only. The rest of the
sentence takes the mark that is printed for the rule, and where none is
printed it is **P**.

**States of the cited texts,** as each states it of itself in the base of
this draft (version 0.1.54):

| Text | Tag | Its own statement |
| --- | --- | --- |
| LIP-0008 sections 2, 4, 5, 5.1, 12.1 to 12.4 | [F] | The text of that LIP, whose status is Draft: "These are proposed semantics, not an adopted or executable wire profile" |
| LIP-0008 sections 2.1, 3.1, 7.1, 12.5 and 5.2 (J6); LIP-0013 section 3.6 (J7); LIP-0014 J4, sections 8 and 11.1; LIP-0029 | [C] | Decisions of one owner that await the co-author's agreement |
| LIP-0020 section 11; LIP-0010 section 10 | [C] | The carried decisions bind a reader of `swarma-grant/4` from version 0.1.53 under one owner's order; "Neither owner has reviewed the octets member by member, and no verifier implements them" |
| LIP-0017 section 8; LIP-0022; LIP-0025; LIP-0026; LIP-0027; LIP-0028 | [D] | Proposals of their drafts. LIP-0026: "Every rule of this LIP is the draft's proposal, and neither owner has decided one" |
| LIP-0008 section 11.4 (SB1 to SB4) | [C] | Draft text under a decision of 2026-11-16 that awaits the co-author's agreement, as that section states of itself |
| LIP-0014 sections 8.4 to 8.7; LIP-0020 W11.11 and W11.14, as release 0.1.55 has them (not in the base of this branch) | [D] | Proposals of version 0.1.55: "No rule, code or order that they add is in force by this draft's own word" (LIP-0014 section 8.4). This draft cites them only for the orders O-1 to O-6 of section 5.1 |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The authority of a session as a function of stated facts: the table of section 4 | Yes, as a model | The owners' answers to Q4, Q8 (b), Q11, Q14, Q15 and Q16 |
| The requests as octets | No | The members of the invocation and of the receipt (N1) |
| The limits as members of a grant | Yes for the three keys of section 3.3, as proposed texts | Acceptance of this LIP, which enters them into the registry |
| The grant checker's verdict | Its content: yes (AS2.1). Its first code where two defects meet: for a parent and a child, yes as far as version 0.1.55 orders it; beyond that, no | A run of the observation under LIP-0022, and the parts of section 5.1, O-1 to O-6 that stay open: a root and a longer path, the blocs of the seal and the issuance, the checks of an invocation, and a whole parent |
| The session journal | No | The entries of a service journal on the form of LIP-0025 (N6) |
| The stop of a process after an end, and the proof behind a clearance | No | The station contract (section 7.2) |

## Motivation

The forms that a host has today start one bounded run of an existing worker
account and are finished with it. A long-lived agent needs more: an authority
that survives a restart of its process, a lifetime that follows the grant and
not a local timer, and a stop when the authority behind the session ends.

The specification has most of the parts: the order of an admission (LIP-0008
section 4), the signed invocation and the proof path (section 12), the
durable closure of a spent seal (section 5.1), the observation (LIP-0022),
rows and accounts (LIP-0026), the stop of a row (LIP-0027), the list of a
landlord's agents (LIP-0010 section 10) and the owner's command (LIP-0029).
What is missing is the profile that says which action a grant names for a
session, which limits bound it, and which events take the authority away
from a run that lasts for thousands of blocks.

## Proposal

`G` is the final grant of a proof path. `H` is the height of the tip of an
observation (LIP-0008 section 7.1, rule 2). `A` is the recipient of `G`, the
agent. `E` is the lease end of a session, a block height. The executor is
`X`; section 2 says what `X` is. C is the grant checker and D is the
dispatching service.

### 1. Scope and terms

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS1.1 | An **agent session** is the authority under which `X` runs one agent in one slot on the strength of one admitted start request. It belongs to one final grant with its proof path, to one executor and to one slot, and none of the three changes. That proof path is **the session's path**: the path of the admitted start that created the session, as D recorded it at the start (check D10). Every later verdict that may move the session's state is a verdict on the session's path, and no other path moves it (AS2.1, convention 3). The path of the grant that a later request cites is **the cited path**; the two are the same path except for a restart under a restart grant (AS3.4). Its record is an entry of the session journal (section 2). It has no token and is no session of LIP-0028; this draft always writes "agent session" | **P**, in the words of LIP-0028 T1.2 [D] |
| AS1.2 | The authority has one of five **states**. `none`: the session journal is intact and holds no record of it, or holds only an annulled start record (events 29 and 36), which is kept for replay alone, counts for nothing and is no session. `session held`: the record has no end, and D holds a current sound verdict for it (AS2.5), with `H < E`. `suspended`: the record has no end, and D holds no current sound verdict. `ended`: the record has an end. An end is final. `quarantined`: the continuity check of the session journal gives lost; or the journal holds a recovery entry and no clearance of the slot after it; or a restore entry (section 5.6) stands and the replay of the ends that fell due during the loss is not complete for the slot (section 5.6). `suspended` is derived and is not written. `quarantined` is derived from the check, from the recovery entry and from the restore entry. The word "held" alone is never used for a state of this profile: the station contract uses `held:*` for an unknown outcome of an effect | **P**. "An end is final" is LIP-0028 T5.4 [D] |
| AS1.3 | The **slot** of an agent session is one OS account of the host, identified by the user id under which it runs (the first form of LIP-0028 T6.1 [D]). A session has **runs**, numbered from 1: the start creates run 1, and a restart creates the next run only in its transition write, after the last check (section 5.2). Each run has a recorded **start-order outcome**, exactly one of: not ordered (events 29, 31, 36); ordered and started; ordered and proved not started (event 30); unknown (event 27). Beside it a run may have a recorded end (the proof P1 that its account holds no process). A session **counts** from the write of its start until its **clearance**, and an annulled start record never counts | **P** |
| AS1.4 | A position in the session journal is always named as a pair: the **identity of the session journal and the position** in it, as the verdict names a closure journal (AS2.1 (b)). A **clearance** is an entry of the session journal with fixed content: the session, the slot with its account and generation; the reference to the station contract's proof that the account holds no process (its rule P1, which is a proof for an account, so that one session for each slot is assumed); the statement, which is D's and which rests on D's own journal, that every run of the session has a recorded outcome and that no start order of the session is outstanding (a start order is outstanding where it was ordered and has no recorded outcome and no proof of event 30); and its own pair of identity and position. The starter of the station contract executes no start order for the slot whose identity is a fenced identity (section 5.6), and none whose pair is the identity of the clearance with an earlier position. D writes no clearance while a run of the session has the outcome "unknown". **The one clearance without P1:** where a session has an end and no start order was ever sent for its only run (the ended subcase of events 29, 31 and 36), D may write the clearance in the form "no start was ordered" in the place of P1, with the statement, from its own journal or from the starter's proof of event 36, that no order was sent or can still land, and with the reference to the compensating entry of section 5.1; the slot was free at the admission and no process was ordered into it, so there is no process for P1 to prove absent | **P**. The proofs and the starter's refusal are needs of the station contract (section 7.2) |
| AS1.5 | The **station contract** is the agreement between the operator of a host and the parties that use it, with the host's signed policy. It owns the states of a process and every proof about a process. It is out of this specification. Where this profile hands a process over, it names the row of that contract in section 7.2 and defines nothing of it | **P**, as a name only |
| AS1.6 | An executor under this profile reads seals on its own node, as a witness (LIP-0008 section 5.1 [F]), or its conformance claim states that it is a non-witness. At a non-witness every spend of a seal that is shown but not validated as the issuer's is event 13 of section 4 and never event 12: it only suspends. The suspension is no closure: where the spend is evicted and a later sound verdict shows the seal unspent again before `E`, the session is `session held` again (cell S7). The span of section 3.3 therefore bounds only how long such a session can last, because it still ends at `E` by height; it does not make an unvalidated spend permanent, and it is not the delay of every revocation. The stop coin of a row is no seal: at a non-witness it is event 16 only where a spend is established in an observation that LIP-0022 does not refuse and the closure is written (LIP-0027 H2.4, H2.5 [D]), or the closure fell due and could not be written (event 22); a spend that is only shown, in no such observation, is event 18 (`ROW_STOP` or the code of the observation) and closes nothing | **P**, after LIP-0010 H50 [C] |

### 2. The executor is a service set

`X` is the service set of one host under one executor name and key
(LIP-0020 W11.4 [C]). It has three parts. (**P**; a grant checker inside the
dispatching service is the rejected alternative, see "Alternatives".)

| Part | Holds | Writes | Does |
| --- | --- | --- | --- |
| The **grant checker** C, behind the message origin | The chain view of its own node, the observation, the watch of the mempool, the executor key, and the durable inputs of AS2.6 | The **closure journals** (AS2.6) | Reads every signed request and every grant, makes every check that needs a document or the chain, and gives the **verdict** (AS2.1): for a request, and for every proof path that D names (AS2.4) |
| The **dispatching service** D | The slot table of the host and the configuration that it started | The **session journal**: the session records with their runs, the identities of admitted requests, the accounts of the starts kind, the ends, the clearances, the run fences, the compensating entries, the halt marks, the recovery entries and the restore entries | Consumes the verdict, makes the checks that need its own journal, writes, and only then orders the effect. It verifies no grant and reads no chain |
| The **key holder** of the recipient | The request key of `A`, the record of each run and its origin, and the table of permissions (LIP-0013 J7.1, J7.2 [C]) | Its own records under LIP-0013 section 3.6 | Binds each run to its origin and signs the requests of section 3.2. Neither other part can observe its gate (J7.7 [C]) |

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS2.1 | **The verdict is an object with fixed content.** It has these logical fields and no other; their octets are open (N6). (a) **Checker and sequence:** the executor name and key of the set, and a sequence number that C assigns strictly increasingly for each path that D names, from a durable counter (AS2.6); it is the order of the verdicts of that path, and no clock reading orders them (AS2.2). (b) **Journal mark:** for every closure journal that a check of a path in (d) or (d2) reads, its identity and the position at which the verdict was given. (c) **Tip and times:** the hash and the height `H` of the tip of its observation; the reading of C's clock at the observation (`now`, the observation's own time); and the reading of the same clock at delivery. C and D are parts of one host's set and read one clock source for elapsed time; a conformance claim for a set whose parts do not states their greatest skew, and that skew counts against the margin of AS2.5. (d) **Cited path:** the ordered proof identifiers of the path of the grant that the request cites, or, for a path verdict, of the path that D named; for every link its identifier, its `not_before_height` and `not_after_height`, its seal outpoint and the height of its recent block; for a child its parent identifier and ordinal; the recipient in its mode; the executor name and key; the Subject. (d2) **Session path:** only where a request names a session and its cited path is not the session's path (a restart under a restart grant), the same fields a second time, for the session's path. Where the two are one path, (d) is that path stated once. (e) **Limits of the cited path:** for each of the three keys of section 3.3, the amount that the final grant of the cited path states or "not stated", under a child also the amount of its row, and whether that grant states a limit with any other key; these are the only limits that a write debits (section 5.2). (f) **Lease:** the lease end that was judged for the session's path, which is the `E` that D named for a path verdict, the requested `lease_end_height` for a start or a renewal, and the `E` that stands for a restart. (g) **Session path result:** for the session's path (for a start, for the cited path, which an admitted start makes the session's path): `sound`; or `suspended` with one code of section 6; or `ended` with the code of the closure and the journal identity and position of that closure, or with the cause "height" and the hash and height of the block that shows it (AS5.1). This result alone may move a session's state, and only through convention 3. (h) For a request only: the identity, the command and the arguments of the request, its mode and channel, its `iat` and `exp`, the entry of the recipient for a child of a class row, and the **request result** on the cited path: passes, or refused with one code of section 6. A builder reads it so: debit the accounts of (d) with the amounts of (e) where (h) passes and D admits the request; move no state by (d), (e) or (h); move the state of the one session whose recorded session's path is the path of (g), by (g) alone, after the gates of convention 3. Section 5.2 gives a worked restart under two paths D takes no fact about a grant from any other source | **P**. "A gateway can deliver data but cannot substitute its prepared binding for that verification" (**R** LIP-0008 section 5 [F]) holds for the set as a whole: C is the part that verifies |
| AS2.2 | The signed invocation is the object that reaches C. The verdict is what C hands to D. Its authenticated delivery, its retry and its ordering in transit are the station contract's (its rule J1). D accepts a verdict for a path only where its checker is the set's own, its sequence number (AS2.1 (a)) is greater than that of the verdict last accepted for that path, and every identity of its journal mark equals the identity that the session record holds for that journal; a verdict with another identity is event 32 and is accepted only after the end is written. A verdict whose sequence is not greater is dropped, whatever its clock readings say; an `ended` verdict given in the same second as the last accepted one has the greater sequence and is never dropped for its second | **P** |
| AS2.3 | C writes a closure into its closure journal before it gives any further verdict, and its next verdict for every proof path that holds the closed link has the session path result `ended`. For a validated issuer spend it writes the closure from the spending transaction itself, whether or not an observation is healthy at that moment. **A closure that falls due and cannot be written makes that journal lost for C** (event 22), also where its continuity check still gives intact because nothing was written: C at once sets the durable lost-mark of AS2.6 for that journal, gives no sound verdict for a path that needs it from then on, and refuses the admission for which the closure was due with the code of the closure. A restart of C does not clear the mark; only a restore of that journal or its recorded start anew does (section 5.6), and a spend that has since left the view revives nothing | **P**. The cited rule speaks of an admission, not of a verdict: an executor that observes a validated issuer-branch spend "MUST persist permanent closure before any further admission" (**R** LIP-0008 section 5.1 [F]). That a due closure that cannot be written is a loss is the cited texts': "Failure to persist closure permits no effect and requires journal recovery" (**R** LIP-0008 section 5.1 [F]); "A restart does not end that state, also where the store and its outside record still agree because nothing was written" (**R** LIP-0027 H3.3 [D], of the journal of rows; the same sentence for the holder journal is LIP-0010 H43 (1) [C]). That C keeps the lost-mark as AS2.6 states it, and for every closure journal, is **P**: LIP-0027 requires "a durable mark that it is lost, outside the journal that could not be written" and "defines no such mark" (**R** [D], its paragraph after H3.6), and LIP-0010 H43 (1) leaves how the state after a failed write is carried across a restart open (**R** [C]) |
| AS2.4 | **Who delivers the next verdict.** For every proof path of a session without an end, which D names to it, C delivers a path verdict (AS5.1): (a) at every new tip of its reading node; (b) at once after every write of a closure journal that concerns a link of the path, before any other verdict; (c) at least every 60 seconds on its own clock where neither occurred, each time with a new reading of the clock under LIP-0022 section 3, so that a tip which does not move ages into `TIP_AGE`; (d) whenever D asks. A checker that cannot make a check delivers `suspended` with the code of what failed, subject to the height part of AS5.1; it does not stay silent. Where D asks for the verdict of a start, of a restart, of a renewal or of a stop and C does not answer within the answer bound of section 5.1, the request is refused as `AGENT_SESSION_NO_VERDICT` and nothing is written in the session journal | **P**. The 60 seconds are this draft's number (N9); a conformance claim may state a smaller one and never a larger one. LIP-0022 "fixes no interval between observations" |
| AS2.5 | **When a verdict is current.** D holds a verdict as current only while it is the newest that D accepted for the path, fewer than 120 seconds have passed on D's own monotonic clock since D received it, and fewer than 120 seconds have passed since the observation's own time in the verdict (AS2.1 (c), on the one clock source that the set reads, or within the skew that its conformance claim states). The earlier of the two bounds ends the currency; a verdict that reaches D at or after 120 seconds from its observation time is never current, however fresh its receipt is. The 120 seconds give a stated margin of 60 seconds over the 60-second delivery duty of AS2.4: the margin is for the computation of the verdict and for its transit to D together, and one lost delivery is covered only where the next delivery reaches D inside that margin; a conformance claim that states a smaller delivery interval states a larger margin. Without a current sound verdict the authority is `suspended`, whoever failed: this is the cell H8, and D is the part that produces it when C is silent. After its own restart D holds no verdict and asks one for every session without an end before it admits a request. D answers a question about the state of a session with "session held" only after it asked C at that moment and received `sound`; in every other case it answers "no session held" | **P**. With two journals this stands where LIP-0028 T4.6 [D] has one atomic step. The 120 seconds are this draft's number (N9) |
| AS2.6 | **The durable inputs of the checker.** C keeps, in journals of the form of LIP-0025, each with an identity: the closures of seals and of issuers' names (LIP-0008 sections 5.1 and 5.2); the rows closed for cause (LIP-0027 section 3); the holder journal with its five kinds of record (LIP-0010 H39). These are the **closure journals**. C also keeps durably: for every path that D names, the grant documents and the contract; for every session's path, the list and attestation octets that it last took or held under the pinned hash in a check on that path (AS5.12); the sequence counter of AS2.1 (a) for every such path; outside every closure journal, a **lost-mark** for each closure journal that records that a due record of that journal could not be written (AS2.3), which a restart of C does not clear and which only the recorded restore or start anew of that journal clears; the highest device list version, the device closures and the replay journal of owner commands (LIP-0029 section 11, steps 4, 8 and 11); beside that replay journal, the **halt record** of every halt command that passed steps 1 to 12 and that D could not act on because the session journal was lost (the identifier of the command and the session that its fields name), for the replay at a restore (section 5.6); and the first sights and the clock mark of its observations (LIP-0022 B3.2, B3.7). A checker that cannot show an input which a check of a path needs, its sequence counter included, gives `suspended` for that path with `JOURNAL_LOST`, subject to the height part of AS5.1, under which it gives `ended` where it can show the block that AS5.1 states although another input is missing. A closure journal whose lost-mark stands cannot be shown at all, whatever its continuity check gives | **P**. Whether the closure journals are one store or several is the deployment's; the journal mark of AS2.1 names each |
| AS2.7 | Replicas of a part share that part's journals, and a replica that cannot reach them admits nothing and orders no effect | **P** for the split by part. The cited rule speaks of one executor: "Replicas acting as the same executor share one authoritative durable journal"; "If shared state or its serialization mechanism is unavailable, replicas admit no new effect" (**R** LIP-0008 section 4 [F]) |

### 3. The actions and the limit kinds

#### 3.1. The grant members

No new member is needed (**R** LIP-0020 W11.2 [C]: "A grant carries nothing
beside these members").

| Member | Meaning under this profile | Mark |
| --- | --- | --- |
| `executor` | The service set `X` of one host. Only `X` holds an authority under `G` | **P** on W11.4 |
| `recipient` | `A`, the agent that works, and not the party that asks | Decided by one owner on 2026-11-16. It agrees with the base: a row names the recipient of its child (LIP-0026 R2.3 [D]), so a grant that named the asking party could not fix the worker |
| `actions` | The leaves of section 3.2 that the issuer allows. A leaf that the list lacks is a right that no issuer gave: commands "match exact leaf identifiers" (**R** LIP-0008 section 12.3 [F]). A grant without the stop leaf has a recipient that cannot end its own session | **P** for the consequence |
| `limits` | The three keys of section 3.3. A grant under this profile states no limit with another key (check D3) | **P** |
| `not_before_height`, `not_after_height` | No authority stands outside the window of any link | **P** for an authority that is `session held`. For an admission: "`H` lies in the intersection of all link height windows" (**R** LIP-0008 section 12.5 [C]) |
| `seal` | The stop of every session under the grant by its issuer. This profile admits a grant only where `seal.kind` is `revocable-only`; another kind refuses as `SEAL_PROFILE`, until a profile states what a use-branch spend does to an authority that is `session held` | **P** for the restriction. The code is that of LIP-0008 SB2 [C] for a kind "that the verifier supports" |
| `contract` | Open: P1 of "Open questions". This profile reads no member of the contract except to mirror the limits (section 5.1, check C6) | **O** |
| `parent`, `ordinal` | A child names the executor and the recipient of its row, and each of its own limits has a key of its row at no greater amount (**R** LIP-0026 R2.2 to R2.4 [D]). The row bounds the limits of a child and does not fix them: a child may state fewer keys, and check D3 then refuses it for this profile's own reasons | **P** for the last sentence |

#### 3.2. The leaves

The leaves have the form that LIP-0018 section 3 requires: "in lowercase
segments separated by slashes" (**R**, with LIP-0008 section 12.3 [F]:
"Command names MUST use lowercase slash-separated segments"). That text
settles the separator. The alphabet of a segment is open there; every
segment here uses the letters `a` to `z` alone. No leaf holds the word
"session", which is the word of LIP-0028. Each leaf has one list of
arguments. (**P** for the exact texts.) There are five leaves; four may
stand in `actions`, and the fifth is an owner command.

**Registry section that each would enter:** the action table of a service
type in LIP-0007 section 1, under the `swarma/` namespace of LIP-0008
section 12.3. They are the texts that LIP-0020 W11.4 expects in `actions`.

| Item (LIP-0018 section 3) | `swarma/station/agent/start` | `swarma/station/agent/restart` | `swarma/station/agent/renew` | `swarma/station/agent/stop` | `swarma/station/agent/halt` |
| --- | --- | --- | --- | --- | --- |
| What it asks | Start one agent session | Start a new run of a session whose state is `session held` | Move the lease end to a higher height | End the session | End the session, by the owner |
| Signer | The key holder of `A`, under the recipient mode of `G` | The key holder of `A` under `G`; or the session service of the host under a restart grant (AS3.4, **O** Q15) | The key holder of `A` under `G` | The same | A device of the owner, as a signed owner command (LIP-0029 [C]). It is no request under `G`, needs no text in `actions` and is never listed there |
| Arguments, as logical fields | `lease_end_height` | `session` | `session`, `lease_end_height` | `session` | The typed fields of the command class: `session` |
| Subject (LIP-0008 section 12.1) | The executor of the grant that the request cites, name and key, with the recipient of that grant | The same | The same | The same | Not an invocation |
| Service type | `slot.station`, the candidate of LIP-0007 section 1, whose row would say "recipient" where it says "renter". That is an amendment of LIP-0007 by a change of its own (N4) | The same | The same | The same | The class of an owner command is one exact leaf of the registry (LIP-0029 O2.1 [C]) |
| Effect or work | **O** (Q4) | **O** (Q4) | **O** (Q4) | **O** (Q4) | **O** (Q4) |
| Class under LIP-0022 B3.5 | Not stated here. "An action whose profile states no class has the first" (**R** B3.5 [D]) | The same | The same | The same | The level of the command is **O** (Q13) |
| Limits that bound it | All three of section 3.3; it consumes one unit of the starts kind and nothing else | One unit of the starts kind of the grant that the request cites | The span kind | None | None |
| Receipt | **O** (N1) | **O** (N1) | **O** (N1) | **O** (N1) | LIP-0029 |

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS3.1 | The Subject is constant along the path: a child names the executor and the recipient of its row (LIP-0026 R2.2, R2.3 [D]), and a root grant names its own. A request whose Subject is not that pair refuses as `REQUEST_SUBJECT`. The comparison of a child with its parent beyond the row, which reads the genesis, the actions and the window of both, has no v4 code in the base: "For the last row no text names a v4 code" (**R** LIP-0020 section 11.11 [C]); section 6 proposes three | **P** |
| AS3.2 | **The signer of a start, and the run.** The key holder of `A` signs a start for a run that it has bound to an origin: the admitted instruction for `A`, or the owner's command (LIP-0013 J7.1 [C]). This draft reads the run as the key holder's record that exists before any process: the launcher, which is D, has the key holder create the run for that origin, and the start request is the first object that the key holder signs for it, on the channel of that run, and only where every grant of the proof path is in the `use` list of that origin (J7.3 (a)). A renewal and a stop are signed for the current run of the session, also while no process of it runs. The cited sentences say when a run is bound ("when the run is created", J7.1) and how the key holder derives it (J7.4); neither says that a run may be created to sign the request that starts its own process. If the editors of LIP-0013 reject the reading, the first start needs an amendment there (N5) | **P** throughout |
| AS3.3 | Every field of a request is covered by its signature (LIP-0008 section 12.1 [F]). A request states its lease end itself, and `X` shortens none and takes none from a default | **P** |
| AS3.4 | **The restart grant.** A host brings a crashed session back alone under a second grant `G_r`: its executor is `X`; its recipient is the **session service** of the host, which is D acting under a request key of its own that a key holder holds under LIP-0013 section 3.6; its `actions` hold the restart leaf; it states a limit of the starts kind, which bounds the restarts by the host over the window of `G_r`, a span of heights; and it has the issuer of `G`: for two root grants the same issuer name, registration and grant key, and for two children the same parent. A restart request under `G_r` is a signed invocation like every other: C reads the chain for `G_r` and for the path of the session, a revocation of either stops it, and no person has to be awake | **P**, and **O** (Q15): this form awaits the owner's yes |

#### 3.3. The limit kinds

The key of a limit is "all of its members but the amount" (**R** LIP-0020
W11.4 [C]). The table gives each key in full. None has a `period`. A grant
that states a limit whose key is not one of these three refuses in one of
two ways. Where the text of its `kind` is none of the three and no type
profile at C defines it, C refuses it as `LIMIT_KIND_UNDEFINED` at the place
that version 0.1.55 gives it for a child (LIP-0014 section 8.4, row F17 (b),
after the keys of the limits and before their amounts; for a request, row E2
and LIP-0020 W11.14 [D]). Where its `kind` is one of the three texts and the
full key differs in another member (a `period`, a resource, a unit), D
refuses it as `AGENT_SESSION_LIMIT_KEY` (check D3). (**P** for the second,
after LIP-0018 section 2, a limit that is "missing, unknown or contradictory
refuses"; the first is the code and the place of version 0.1.55 for the rule
of W11.4: "A verifier refuses the admission that an unknown kind affects".)

**Registry section that each would enter:** the registry of limit kinds
that LIP-0020 W11.4 leaves to "the type profile of the kind". The texts are
**P**.

| Item (LIP-0018 section 2) | Starts | Level | Span |
| --- | --- | --- | --- |
| `kind` | `swarma/station/agent/starts` | `swarma/station/agent/level` | `swarma/station/agent/span` |
| `resource` | `swarma/station/agent` | `swarma/station/agent` | `swarma/station/agent` |
| `unit` and scale | `start`; whole starts | `session`; whole sessions | `block`; whole blocks |
| Bounds and rounding | 0 and above; an amount of 0 is well formed and authorizes nothing. Nothing is rounded | The same | The same |
| What it is | An **account** of LIP-0026 R5.1 and R5.2 [D], for the whole window | A **level**: a check of this profile and no account. LIP-0026 section 5 does not apply to it | A **maximum of one request**: a check of this profile and no account |
| What a request consumes | A start and a restart debit 1: the own account of the grant that the request cites, and under a child also the row account (R5.3, R5.4). This is the only key that a request "consumes" in the sense of R5 | Nothing | Nothing |
| Arithmetic | Never lowered (R5.1, R5.8). The own account before the row account (R5.6) | Own: the number of sessions under `G` that count (AS1.3), after the start, is at most the amount. Row, under a child: the number of sessions that count under every document that is a child of the same parent and ordinal, after the start, is at most the amount that the row states for this key | `H < lease_end_height <= H + amount`, with the `H` of the verdict of that request. Under a child the child's own amount holds; R2.4 already holds it at or below the row's |
| Missing limit | The ceiling is 0 (R5.2): `OWN_LIMIT_OVER`, `ROW_CAP_OVER` | Refuses: "Missing required limits ... refuse the affected admission rather than becoming unlimited access" (**R** LIP-0008 section 2 [F]). `AGENT_SESSION_LIMIT_MISSING` | The same |
| Reservation, uncertainty, denial | Reserved in the atomic write of a start or of a restart. An unknown outcome keeps it (**R** LIP-0008 section 2: "Uncertain effects retain their reservations until reconciled"). A request that is refused before its write reserves nothing (R6.2). A debit that was written is given back in one case alone: where no start order was ever sent for the run that it reserved (events 29, 31 and 36), D writes a **compensating entry** that releases the debit and the level count of that admission, so that a start that was never ordered consumes no start (**P**; R5.8 leaves a release to the type profile, and this is the one release that this profile states). In every other case a debit stands, also where an order was sent and the run proved not started (event 30) or a restart was blocked after its transition began (event 35) | Counted from the same write. Released by the clearance, or by the compensating entry where no order was ever sent, as the starts kind states in its own column | Nothing is reserved |
| Replicas | One session journal (AS2.7) | The same | No state |
| Child and row (LIP-0026 R2.4 [D]) | A smaller amount is stricter | A smaller amount is stricter | A smaller amount is stricter |
| The pool of a parent (LIP-0020 W11.10, rule 6 [C]) | The reader rule bounds the sum of the row amounts in the signed octets; no runtime account of a pool exists (R5.5) | The same rule; it bounds the most sessions that can count at once under all rows | The rule still asks for the member and its sum. The number bounds nothing under this profile |
| Contract mirror | By executor, kind, resource, unit and amount (LIP-0008 section 2 [F]); check C6 | The same | The same |
| Kind of LIP-0008 section 2 | A new kind | "Runtime and concurrency" | "Runtime and concurrency", counted in blocks (section 2.1) |

One slot holds one session at a time (cell H1), a recipient maps to one
slot, and D refuses a start while another session of the same recipient
counts at `X` in any slot (check D5). So under a grant that names one
recipient at most one session counts, whatever the level says. The level
bounds a row whose documents name several recipients.

No kind of this profile bounds a model or gateway budget. "A budget belongs
to that executor" (LIP-0008 section 4 [F]), and a grant has one executor
(LIP-0020 W11.4 [C]); the budget of a model is a separate grant, by the
owner's decision of 2026-11-16 (section 7.1).

### 4. The table of the authority

Rows are the five states of AS1.2, with the letters N (`none`), H (`session
held`), S (`suspended`), E (`ended`) and Q (`quarantined`). Columns are the
events, 36 of them, in nine bands. A cell is named by the letter of its
state and the number of its event. Each cell gives the next state, who acts,
the durable record that is written before any effect, and a code of the one
list of section 6; or it says that the event cannot occur in that state, and
why. Every rule of this draft hangs off a cell, and nothing outside this
section and section 5 restates one. Each cell is **P** unless it carries
another mark.

Five conventions hold for every cell.

1. **The row of a request.** A request that names a session is judged in
   the row of that session. A start names none: its row is the state of the
   newest session of the slot that the recipient maps to, and Q where the
   slot is quarantined.
2. **A request cell is read after the checks before it.** Section 5 runs
   the checks of C before those of D. A cell gives the code of the check
   that the cell is about, and a request with an earlier defect gets the
   code of that earlier check. A request for a session that a closure ended
   therefore refuses with the code of the closure and not with
   `AGENT_SESSION_ENDED`.
3. **The verdict of a request moves a state only through three gates, and
   only its own session's.** Its session path result (AS5.2) becomes an
   event of bands 2 to 5 for a session only after D has passed, in this
   order: the continuity read (check D1); the replay read (check D2); and
   the read that the session that the request names is in the journal with
   a recorded session's path equal to the path that the session path result
   was judged on (AS2.1 (d) or (d2)). Only then does the result move that
   one session's state, and then the request is judged in the row that
   results. Where one of the gates refuses, the request is refused with
   that gate's code, no state moves and nothing is written in the session
   journal: a resent old request whose verdict result is `suspended` or
   `ended` suspends and ends nothing, and a request under a second document
   of a row, or under a restart grant whose verdict carries another
   session's path, moves no session but its own. What C wrote in its own
   journals while it judged the request stands (section 4, last paragraph
   before band 1), and a closure so written still reaches its sessions by
   the next path verdict that AS2.4 (b) owes, as that verdict's own event
   and not as this request's. A failure of the request alone moves no state.
   A start names no session: for it the three gates have no session to
   name, its verdict result is its admission result and moves nothing.
4. **One object, several columns.** The order of section 5 decides: the
   first check that fails names the cell. Inside the checks of D a repeated
   request is event 5 before it is any other event, because the replay read
   D2 stands before the slot reads; a refusal of C that stands before D
   answers first all the same (convention 2), and convention 3 applies a
   verdict result only after D2.
5. **One tip, several events.** An end stands before a suspension, and a
   suspension before a sound verdict (AS5.3). Among ends a closure stands
   before a height. D writes one end, with the first cause in that order.

A request that is refused before its write writes nothing into the session
journal. What C wrote into its own journals while it judged the request (a
closure, the take of a list) stands, as the cited texts have it. In the Q
row "lost" means that the continuity check gives lost, and it also covers
a slot whose restore entry stands and whose replay is not complete
(section 5.6, item 7): until the replay is complete for that slot a
request or a command for it is refused as the "lost" branch of its cell
states, because the journal is not yet read as an authority again.
"Anew" means that the journal holds a recovery entry and the slot has no
clearance after it.

**Band 1: the requests.**

| State | 1. Start request | 2. Restart request | 3. Renew request | 4. Stop request |
| --- | --- | --- | --- | --- |
| `none` | **N1.** Admitted where every check of section 5.1 passes: then `session held` to the stated `E`. C gives the verdict; D writes one atomic entry (the session record with run 1, the debit of one start, the count of the level); then the last check (D11); only then D orders the start. Codes: section 5.1. A last check that fails is event 29 | **N2.** `AGENT_SESSION_UNKNOWN` | **N3.** `AGENT_SESSION_UNKNOWN` | **N4.** `AGENT_SESSION_UNKNOWN` |
| `session held` | **H1.** Refused: `AGENT_SESSION_SLOT`. A slot holds one session that counts, whoever asks and under whichever grant | **H2.** Admitted where section 5.2 passes, in the one order of AS5.7: stays `session held`; `E` and the identifier do not change. D first writes the admission entry (the identity and the debit of one start in the accounts of the cited path); then the last check; then, in the transition write, the end of the earlier run with the proof of the empty account, the run fence and the next run; then the start order. A run whose outcome is unknown or a start order that is outstanding refuses before any write (`AGENT_SESSION_RUN_OPEN`); an end or a proof that fails inside the transition is event 35; a last check that fails is event 29 and leaves the earlier run untouched | **H3.** Admitted where section 5.3 passes: stays `session held`, to the new `E`. D writes the identity, the new `E` and the channel of this request in one atomic entry. Nothing is debited | **H4.** Admitted where section 5.4 passes: `ended`. D writes the end and the identity. The stop of the process is the station contract's |
| `suspended` | **S1.** Refused: `AGENT_SESSION_SLOT` | **S2.** Through the gates of convention 3: where the session path result is `sound`: `session held`, and the cell is H2. Where it is `ended`: `ended`; D writes the end, and the request refuses with the code of the closure, or with `AGENT_SESSION_ENDED` for the cause "height". Where it is `suspended`: refused with its code; stays `suspended`; nothing is written. Where a gate refuses first, that gate's code and no move (convention 3) | **S3.** Through the gates of convention 3: where the session path result is `sound`: `session held`, and the cell is H3; a renewal that then refuses for its own defect leaves the state `session held`, to the `E` that stands. Where it is `ended`: as S2. Where it is `suspended`: refused with its code; stays `suspended` | **S4.** Through the gates of convention 3: where the session path result is `sound`: `session held`, and the cell is H4. Where it is `ended`: as S2. Where it is `suspended`: refused with its code; stays `suspended`. Cells S19 and S21 still end it |
| `ended` | **E1.** Before the clearance (event 28): `AGENT_SESSION_SLOT`. After it: as N1; the new session has a new identifier | **E2.** `AGENT_SESSION_ENDED` | **E3.** `AGENT_SESSION_ENDED` | **E4.** `AGENT_SESSION_ENDED`; nothing is written. A stop is not answered as done, so that a caller reads the state from the code |
| `quarantined` | **Q1.** Lost: `JOURNAL_LOST`. Anew: `AGENT_SESSION_SLOT` | **Q2.** Lost: `JOURNAL_LOST`. Anew: `AGENT_SESSION_UNKNOWN` | **Q3.** As Q2 | **Q4.** As Q2 |

**Band 2.**

| State | 5. A repeated request: its identity is in the session journal, or its `iat` is not later than the `fenced_at` of a recovery entry | 6. A request under a second document of the same row | 7. A sound path verdict is delivered and current | 8. No current sound verdict, and nothing has ended |
| --- | --- | --- | --- | --- |
| `none` | **N5.** `AGENT_SESSION_REPLAY`. Nothing is written | **N6.** A start: as N1. The second document has own accounts of its own and shares the row account with the first: "Two documents of one row have two own accounts and share the row account" (**R** LIP-0026 section 5 [D]). It also shares the row level | **N7.** No change: there is no authority | **N8.** No change. A start refuses with the code of the verdict, one of those of check C3 or `JOURNAL_LOST`. Where C does not answer the ask for the verdict within the answer bound of section 5.1, the start refuses as `AGENT_SESSION_NO_VERDICT`; nothing is written (AS2.4) |
| `session held` | **H5.** `AGENT_SESSION_REPLAY`. No change, whatever the session path result of the resent request's verdict is: the replay gate stands before that result is applied (convention 3) | **H6.** A start for the same slot: `AGENT_SESSION_SLOT`. A start for another slot is judged in the row of that slot, and the shared row level decides (`AGENT_SESSION_LEVEL_ROW`). A restart, renew or stop that names this session with the other document: `AGENT_SESSION_UNKNOWN` at the third gate of convention 3, and the verdict result on the other document's path moves nothing here. The authority never moves to the other document | **H7.** Stays `session held`. D writes nothing | **H8.** `suspended`. Nothing is written. C produces it by a session path result `suspended`, at the next tip or within 60 seconds of the cause (AS2.4); D produces it when it holds no current verdict under either bound of AS2.5. D answers "no session held" |
| `suspended` | **S5.** As H5 | **S6.** As H6 | **S7.** `session held`. D writes nothing | **S8.** Stays `suspended`. No clock ends it (**O**, Q8 (b)). While blocks of the pinned chain arrive, event 9 ends it at `E` |
| `ended` | **E5.** As H5 | **E6.** A start: as E1. A request that names this session with the other document: `AGENT_SESSION_UNKNOWN` | **E7.** No change. From the record of the end no request and no later chain reopens the session | **E8.** No change |
| `quarantined` | **Q5.** Lost: `JOURNAL_LOST`. Anew: `AGENT_SESSION_REPLAY` | **Q6.** As Q1 for a start and as Q2 for another request | **Q7.** No change. D acts on no verdict while it cannot read or has replaced its journal | **Q8.** No change |

Only an admitted request writes its identity (check D2). A request that was
refused left no record and can be sent again; it is no event 5.

**Band 3.** A sound verdict takes its height only from a healthy
observation. An end by height is taken also from any block that the checker
can show under AS5.1: a block that its reading node validated, on that
node's active chain, where that node is on the pinned chain (it gives the
pinned genesis hash for the block of height 0, LIP-0022 B1.3), at a height
at or above `E`, healthy observation or not: an end only takes authority
away (**P**). A block on another chain, or from a node that does not give
the pinned genesis, shows nothing and ends nothing. The end that D writes
names the hash and the height of the block that showed it.

| State | 9. Lease end: `H >= E` | 10. Grant window end: `H` at or above the `not_after_height` of a link | 11. Tip below the opening of a window, after a reorganisation | 12. Seal of a link spent, and C validated the issuer's spend |
| --- | --- | --- | --- | --- |
| `none` | **N9.** Cannot occur: no lease exists | **N10.** No change. A start refuses: `GRANT_WINDOW` | **N11.** No change. A start refuses: `GRANT_WINDOW` | **N12.** No change in the session journal. C writes the closure (AS2.3). A later start refuses: `GRANT_CLOSED` |
| `session held` | **H9.** `ended`. D writes the end with the hash and the height of the tip that showed it and the cause "height", before it does anything else | **H10.** Cannot occur apart from H9: `E` is at most the `not_after_height` of every link (check D7 and check 4 of section 5.3), so the same tip has reached `E` | **H11.** `suspended`; nothing is written. `E` stands | **H12.** `ended`, for every session whose proof path holds the closed link, the root included. C writes the closure first and delivers the verdict at once (AS2.4 (b)); D writes the end with the journal identity and position of the closure before it admits anything |
| `suspended` | **S9.** `ended`, as H9 | **S10.** As H10 | **S11.** Stays `suspended` | **S12.** `ended`, as H12 |
| `ended` | **E9.** No change | **E10.** No change | **E11.** No change. A reorganisation undoes no end | **E12.** No change |
| `quarantined` | **Q9.** No change: D can write nothing (lost) or holds no lease (anew). At a restore the height is applied in the replay of section 5.6 before any session leaves `quarantined`; it does not wait for a later verdict of its own | **Q10.** As Q9 | **Q11.** No change | **Q12.** C writes the closure. D writes nothing. At a restore the closure is applied in the replay of section 5.6 before any session leaves `quarantined` |

**Band 4.** Events 14 and 15 exist only for a child of a class row.

| State | 13. Seal of a link shown spent, and C validated no issuer's spend, or C is a non-witness | 14. An admission took a new list of the landlord's agents and wrote the removal mark of the recipient's entry | 15. The landlord's value pins another list, and C holds no octets under the pinned hash for the session's path (AS5.12) | 16. Row stop: the stop coin of the row is spent, and C wrote the closure |
| --- | --- | --- | --- | --- |
| `none` | **N13.** No change. A start refuses: `GRANT_SEAL` | **N14.** No change. A start refuses: `CLASS_HOLDER` | **N15.** No change. A start refuses: `LIST_UNKNOWN` | **N16.** No change. A start refuses: `ROW_CLOSED_FOR_CAUSE` |
| `session held` | **H13.** `suspended`; nothing is written. The cited rule speaks of an admission: such evidence "refuses admission without asserting that an issuer revocation has been proved" (**R** LIP-0008 section 5.1 [F]); that an authority which is `session held` is suspended by it is this profile's | **H14.** `suspended`. C wrote the mark in the take of a list; D writes nothing. The mark is no closure: it is lifted by the take of a list with a higher `seq` that holds the same entry (LIP-0010 H40, point 6; H41 [C]). The exit is a renew request that presents such a list, or any cell that ends | **H15.** `suspended`. The exit is a renew request that presents the list: its admission takes the list, and where the list holds the same entry the cell is S3, and where it does not the mark is written and the cell is S14 | **H16.** `ended`, for every session whose final grant is a child of that row, under either document. A session under another row is untouched: "Another row of the same parent is not touched by it" (**R** LIP-0027 H3.5 [D]) |
| `suspended` | **S13.** Stays `suspended` | **S14.** Stays `suspended`. A renew request whose own take wrote the mark refuses as `CLASS_HOLDER`; the mark stands, and the state does not change | **S15.** Stays `suspended` | **S16.** `ended`, as H16 |
| `ended` | **E13.** No change | **E14.** No change | **E15.** No change | **E16.** No change |
| `quarantined` | **Q13.** No change | **Q14.** No change. The mark stands in C's journal | **Q15.** No change | **Q16.** As Q12 |

A change of the list or a spent seal "decides whether such a child is
admitted from then on; it does not end the child, and it does not end its
parent" (**R** LIP-0010 section 10.4 [C]). A list that still holds the same
entry, which is the same landlord, name, key and seal (H39), changes no
fact; to a checker that does not hold its octets it is event 15 all the
same, until a presentation supplies them (AS5.12). The same name under
another key or another seal is another entry, and for the session it is
event 14 once the list is taken. A validated spend of the seal of the entry
is event 17.

**Band 5.**

| State | 17. Another closure of a link | 18. Another refusal of a path check, which closes no link | 19. Owner control: a halt command | 20. Owner control: a start by a command without a grant |
| --- | --- | --- | --- | --- |
| `none` | **N17.** No change. A start refuses with the code of the closure: `ISSUER_NAME_CLOSED` or `HOLDER_REVOKED` | **N18.** No change. A start refuses with the code of the check, one of those that the text below the table lists | **N19.** `AGENT_SESSION_UNKNOWN`, where steps 1 to 12 of LIP-0029 section 11 passed and the lookup of the session then names none; step 13 is not reached | **N20.** Cannot occur as a start under this draft: a command to `X` starts nothing, in any row. The command can arrive all the same: addressed to `X` it is judged by the steps of LIP-0029 section 11 and refuses there, as `NOT_FOR_ME` where its audience is not `X` and as `ACTION_UNKNOWN` where its class names a start leaf that no owner-command class of `X` is, with no write in the session journal and no state change. As the origin of a run at the key holder (LIP-0029 O6.5 [C]) it is no command to `X`, and the start that follows it is event 1. The other answer is **O** (Q11) and would need rows that this table does not have |
| `session held` | **H17.** `ended`. C wrote the closure; D writes the end with its journal identity and position | **H18.** `suspended`; nothing is written in the session journal | **H19.** `ended`. C admits the command by steps 1 to 12 of LIP-0029 section 11 and gives the code of that table where one refuses; D then looks the session up; step 13 then recomputes the actual arguments, the session as looked up among them, against the fields (`FIELDS_MISMATCH`) immediately before the effect; only then D writes the end, and the halt mark of section 5.8 in the same entry, with the identifier of the command | **H20.** As N20 |
| `suspended` | **S17.** `ended` | **S18.** Stays `suspended` | **S19.** `ended`, as H19 | **S20.** As N20 |
| `ended` | **E17.** No change | **E18.** No change | **E19.** `AGENT_SESSION_ENDED` | **E20.** As N20 |
| `quarantined` | **Q17.** As Q12 | **Q18.** No change | **Q19.** Lost: `JOURNAL_LOST`, where the command passed steps 1 to 12; C keeps it in the halt record for the replay at a restore (the text below this band). Anew: `AGENT_SESSION_UNKNOWN`; the recovery entry already counts as the end (section 5.6) | **Q20.** As N20 |

Event 17 is exactly two closures: that of the issuer's name where C holds
it (`ISSUER_NAME_CLOSED`, LIP-0008 sections 5.2 and 5.3 [C]), and that of
the seal of the recipient's entry after a validated spend (`HOLDER_REVOKED`,
LIP-0010 section 10.7 [C]). With events 12 and 16 these are all the
closures of a link, and only a closure of a link or a height ends an
authority.

Event 18 is every other refusal of a path check of AS5.1. Some leave a
durable record at C and still close no link. Its codes are: `REQUEST_AUTH`
where the owner of the recipient's name is not the signed owner key, which
"refuses admission and records no closure" (**R** LIP-0008 section 3.1
[C]), or where the name yields no key for the channel; the codes of the walk
of a name that refuses without a journaled closure; `RECENT_BLOCK`,
`RECENT_BLOCK_WINDOW`, `CONFIRMATIONS`, `SEAL_OUTPUT` and `SEAL_SCRIPT`,
where a reorganisation removed what they read; `CLASS_HOLDER` where no
removal mark is the cause; `HOLDER_SEAL_NOT_LIVE`, `HOLDER_SEAL_ALIAS`, `HOLDER_SEAL_REUSED`,
`HOLDER_PIN_INVALID`, `HOLDER_LIST_ROLLBACK`, `HOLDER_LIST_INVALID`,
`HOLDER_LIST_MISMATCH`, `HOLDER_FORM_DOWNGRADE` (LIP-0010 section 10.6 [C]);
`CLASS_LANDLORD`, `CLASS_LANDLORD_CHANGED`, `CLASS_LANDLORD_PENDING`,
`CLASS_CHECKPOINT`, `CLASS_VALUE_UNAUTHORIZED`, `CLASS_WRITER`,
`CLASS_HISTORY_UNAVAILABLE` (LIP-0026 section 9 [D]); `ROW_STOP`, `ROW_COIN`
(LIP-0027 H2.6 [D]; LIP-0026 R3.2 [D]); and `NOTARY_WITHDRAWN` with the
other codes of the attestation steps (LIP-0014 section 8 [C]); and the issuance codes that check C4 and AS5.1 run: the thirteen codes of LIP-0023 section 7 in their order and the codes of the six steps of LIP-0020 W9.4 (section 6, list 3), where a reorganisation removed what they read. A withdrawn attestation is journaled by the verifier and is
cured by a successor attestation, so it ends nothing; the exit is a renew
request that presents the successor.

For a halt, the steps of LIP-0029 section 11 stand first and give their own
codes; step 11 records the identifier of the command when it passes. The
lookup of the session stands after step 12, and step 13, which recomputes
the actual arguments against the fields immediately before the effect,
stands after the lookup and before D writes the end: its code
`FIELDS_MISMATCH` refuses the halt where the looked-up session is not the
one that the fields name, and where the lookup names none, step 13 is not
reached and the code is that of the lookup (cells N19, E19, Q19). A
halt that is sent twice is therefore `REPLAY` of that table, and E19 is
reached only by a second command with another identifier. A halt that
passed steps 1 to 12 while the session journal was lost is kept in the
halt record of AS2.6 and is applied at a restore before any session
leaves `quarantined` (section 5.6); sending it again is `REPLAY` and is
not the way that it is applied. A later
revocation of the device that signed a command is no event of this table:
LIP-0029 O8.4 speaks of envelopes.

**Band 6.**

| State | 21. The operator ends a session of the journal under the host's policy | 22. A closure journal is lost: C's continuity check gives lost, or a record of that journal (a closure, a row closure, a record of the holder journal) fell due and could not be written (AS2.3) | 23. The session journal is lost: D's continuity check gives lost | 24. The session journal is started anew |
| --- | --- | --- | --- | --- |
| `none` | **N21.** Cannot occur: the event names a session of the journal. An operator act that names none is the station contract's and no event here | **N22.** No change. C refuses every request whose path needs the lost journal, by the scope of section 5.6: `JOURNAL_LOST`; the admission for which a closure was due refuses with the code of that closure (AS2.3). A request whose path needs no record of that journal is judged as before. Such a verifier "MUST NOT admit before the journal is recovered or its owner has started it anew" (**R** LIP-0008 J6.9 [C]) | **N23.** `quarantined`. D refuses every act that needs the journal: `JOURNAL_LOST` | **N24.** Cannot occur: only a lost journal is started anew (LIP-0025 M5.3 [D]), and a slot under a lost journal is in the Q row |
| `session held` | **H21.** `ended`. D writes the end with the cause. Ending takes authority away and gives none | **H22.** For a session whose path needs the lost journal, by the scope of section 5.6: `suspended`. C delivers `suspended` with `JOURNAL_LOST` (AS2.6), or is silent and D's bound passes (AS2.5); the height part of AS5.1 may still end it. A session whose path needs no record of that journal does not change state for this event. A journal that is restored with its identity and without its lost-mark gives verdicts again; one that is started anew is event 32 | **H23.** `quarantined`. D writes nothing, because it cannot; it orders no start and answers "no session held". It hands the event to the station contract (section 7.2, row 10). The loss proves nothing about the session: a reader of a lost journal "never takes a missing entry as a sign that nothing happened" (**R** LIP-0025 M5.1 [D]) | **H24.** Cannot occur, as N24 |
| `suspended` | **S21.** `ended` | **S22.** Stays `suspended`, for a session in the scope of H22 as for one outside it | **S23.** `quarantined`, as H23 | **S24.** Cannot occur, as N24 |
| `ended` | **E21.** No change | **E22.** No change | **E23.** `quarantined`, as H23. The record of the end cannot be read; event 33 gives it back | **E24.** Cannot occur, as N24 |
| `quarantined` | **Q21.** Lost: D can write no end and refuses `JOURNAL_LOST`; the operator's attended end attempt is recorded durably under the station contract naming the slot and, where known, the session (a need of that contract, section 7.2), and D applies every such recorded attempt at a restore before any session leaves `quarantined` (section 5.6). An end attempt with no such record was not made durably and the operator issues it again after the restore. Anew: cannot occur, the journal holds no session | **Q22.** No change | **Q23.** No change | **Q24.** Stays `quarantined`. On the operator's attended act D writes the recovery entry and then the boundary entry (LIP-0025 M5.3, M5.4). The recovery entry counts as the end of every session that the lost journal could have held, and the new journal charges by section 5.6. The station contract's stop duty then holds for every process in every slot of the host |

A replica that does not hold the token of a journal is fenced: it writes
nothing and refuses as `JOURNAL_FENCED`, whatever the positions are
(LIP-0025 M4.4, M4.6 [D]). That is a fact of the replica and no event of a
session.

**Band 7.**

| State | 25. The channel key of a recipient by name is replaced under the same owner | 26. The pinned key of `X` no longer equals `executor.key` of `G` | 27. The outcome of a start order is unknown | 28. Clearance of an ended session |
| --- | --- | --- | --- | --- |
| `none` | **N25.** No change | **N26.** No change. A start refuses: `GRANT_EXECUTOR` | **N27.** Cannot occur: D orders a start only after the write that creates the session | **N28.** Cannot occur: no session |
| `session held` | **H25.** Stays `session held`: "Same-owner grantee rotation/renewal keeps a grant by name" (**R** LIP-0008 section 4, step 2 [F]). The next request is authenticated under the new key | **H26.** `suspended`; nothing is written | **H27.** Stays `session held`. D writes "run k: outcome unknown". The debit and the count stay. D orders no other start in the slot, and a restart refuses as `AGENT_SESSION_RUN_OPEN` before any write while any run of the session stands so (AS5.6), releases nothing and does not take the attempt as absent. Every other cell of the row still applies. The outcome is resolved by the station contract's proof: that the run started, which D records, or event 30 | **H28.** Cannot occur: D writes a clearance only for a session that has ended. An account that is found empty while the record has no end is a process that is down, which is the station contract's and no event here |
| `suspended` | **S25.** No change: the replacement is no cause of a suspension and lifts none | **S26.** Stays `suspended` | **S27.** Stays `suspended`; the writes of H27 | **S28.** Cannot occur, as H28 |
| `ended` | **E25.** No change | **E26.** No change | **E27.** Stays `ended`. D writes the entry. No clearance is written until the outcome is resolved | **E28.** Stays `ended`. D writes the clearance with the content of AS1.4, and only where every run has a recorded outcome. The slot is free, and the session no longer counts for the level |
| `quarantined` | **Q25.** No change | **Q26.** No change | **Q27.** D can write nothing (lost) or holds no session (anew). The station contract keeps the unknown outcome in its own row `held:*`, and the census of event 34 covers it | **Q28.** Cannot occur: no clearance of a session can be written (lost), or the journal holds no session (anew). The exit is event 34 |

**Band 8.**

| State | 29. The last check at D11 fails, or is not answered in its bound, after the write of a start or of the admission of a restart | 30. The station contract proves that a start order started nothing and can no longer land | 31. D's continuity check gives pending | 32. A verdict carries a closure journal of another identity: the journal was started anew |
| --- | --- | --- | --- | --- |
| `none` | **N29.** Cannot occur: the write that the check follows created the session (a start) or names one (a restart), so the slot is in another row at D11 | **N30.** Cannot occur, as N27 | **N31.** D completes the outside write first. A pending clearance, recovery or boundary entry stands. No session is touched | **N32.** No change in the session journal. C is a newcomer and admits again after the recorded start anew (LIP-0008 J6.9 [C]); see the known limit S30-K3 |
| `session held` | **H29.** The start or the restart is **refused** with the code of the check; no start order is sent. The failure of the check ends nothing and kills no run. After a start: D writes the compensating entry and the annulment of the start record; the slot is `none`, no start is consumed, and no end is written. After the admission of a restart: D writes the compensating entry; the session and its earlier run are as they were, and no new run was created. Two findings of the check are not a failure of the check but an end that it found: where it found a closure of a link or a height at or above `E` on the pinned chain, the end of H12, H16, H17 or H9 is written first, also after a start, where the clearance of AS1.4 in the form "no start was ordered" may follow in the same entry; the compensating entry stands in that subcase too, because no order was sent. Where one block both moves the tip and reaches `E`, the ended finding is reported and not `OBSERVATION_VOID` (section 5.1). Codes: those of the last check (section 5.1), `AGENT_SESSION_NO_VERDICT` where it was not answered | **H30.** Stays `session held`. D writes "run k: not started" with the reference to the proof. The debit stays. A restart may follow | **H31.** D completes the outside write first, and the entry stands. The act that the entry records does not follow from it (section 5.6), and no start order is sent from a pending entry. A pending start entry (run 1): the compensating entry and the annulment of H29, or the end and the clearance of H29 where a closure or a height is then found. A pending admission entry of a restart (no new run yet): the compensating entry, "restart of run k: not ordered". A pending transition entry of a restart (run k+1 created in it): run k+1 "not ordered", its debit compensated, the end and the fence of run k in that entry stand, and no order is sent for run k+1 ever; a later restart creates run k+2. A pending renew entry stands with its new `E` | **H32.** `ended`, for every session whose path could have had a record in the replaced journal. D writes the end with the cause and both identities before it accepts the verdict |
| `suspended` | **S29.** As H29, in the state that a supervening suspended verdict left between the write and D11; after the compensation the session is `none` (a start) or stays `suspended` (a restart) | **S30.** Stays `suspended`; the write of H30 | **S31.** As H31 | **S32.** `ended`, as H32 |
| `ended` | **E29.** Stays `ended`: this cell is reached only where an end supervened between the write and D11 (a verdict, a halt, an operator end or a height) or the check itself found that end. D orders nothing; it writes the run "not ordered" (run 1 of a start, or the run that the restart had not yet created: "restart of run k: not ordered") with the compensating entry, and the clearance of AS1.4 in the form "no start was ordered" may follow. Code to the caller: `AGENT_SESSION_ENDED`, or the code of the closure that ended it | **E30.** Stays `ended`; the write of H30. A clearance may follow | **E31.** D completes the outside write first. A pending end entry stands, and the station contract's stop duty holds from it. A pending clearance stands | **E32.** No change |
| `quarantined` | **Q29.** D orders nothing. Lost: `JOURNAL_LOST`; the write that the lost journal held is no ground for an order after a restore or a start anew: a restore takes it under event 36, a start anew charges it under section 5.6. Anew: cannot occur in the new identity, which holds no such write | **Q30.** As Q27 | **Q31.** D completes the outside write first. A pending recovery or boundary entry stands | **Q32.** No change. After event 33 the first verdict with the other identity is this event |

**Band 9.**

| State | 33. The lost session journal is restored | 34. The operator's clearance of a slot after a recovery | 35. Inside the transition of a restart (after the last check) the end of the earlier run is unknown, or the proof of an empty account fails | 36. D recovers from a crash or a restart and finds an admitted start, an admission of a restart or a transition whose write was accepted, with no start order recorded as sent and no start-order outcome |
| --- | --- | --- | --- | --- |
| `none` | **N33.** Cannot occur: only a lost journal is restored, and a slot under a lost journal is in the Q row | **N34.** Cannot occur: the slot is not quarantined | **N35.** Cannot occur: no session and no restart | **N36.** Cannot occur: the accepted write created a record (a start), or names a session (a restart), so the slot is in another row |
| `session held` | **H33.** Cannot occur, as N33 | **H34.** Cannot occur, as N34 | **H35.** Stays `session held`. D writes "restart blocked: run k open". The debit stays. The caller gets `AGENT_SESSION_RUN_OPEN`, and so does every later restart, with no write and no debit, until an operator's act lets the station contract give the proof and D records "run k: ended" with the run fence. That record lifts the block and ends the blocked restart: it creates no run and orders no start, and the next restart is a new request with a new debit. No new run is created meanwhile | **H36.** Read where D, after its recovery, first holds a current sound verdict for the session (in the common case, with no verdict yet, the cell is S36). D orders nothing from the recovered entry, in any subcase. It first asks the starter by the pair of identity and position of that entry (check D12): the starter proves that it received no such order and fences that pair, so the order can never land; or it cannot prove it, and the cell is then H27 ("run k: outcome unknown"). On the proof: after a **start**, run 1 "not ordered", the compensating entry and the annulment, and the slot is `none` (or the end and the clearance "no start was ordered" where a closure or a height is then found); after an **admission** of a restart, "restart of run k: not ordered", the compensating entry, and the session and run k are as they were; after a **transition**, run k+1 "not ordered", its debit compensated, the end and the fence of run k stand, and a later restart creates run k+2. A run that is "not ordered" is never ordered afterwards: a retry is a new request with a new identity and, for a restart, a new run number. No start order is sent twice, and none is sent on a recovery |
| `suspended` | **S33.** Cannot occur, as N33 | **S34.** Cannot occur, as N34 | **S35.** Stays `suspended`; the writes of H35, in the state that a supervening suspended verdict left during the transition | **S36.** As H36: D holds no verdict after its own restart (AS2.5), so a recovered admission of a session without an end is read in this row until it asks one |
| `ended` | **E33.** Cannot occur, as N33 | **E34.** Cannot occur, as N34 | **E35.** Stays `ended`: this cell is reached only where an end supervened during the transition (a closure, a height, a halt or an operator end, which the read at D12 finds). D creates no run where the transition write has not stood yet, writes the new run "not ordered" with its compensating entry where it has, and orders nothing. Code: `AGENT_SESSION_ENDED`. The open run is under the station contract's stop duty | **E36.** Stays `ended`. As H36 for the starter's proof: on it, the run is "not ordered", the compensating entry stands, and a clearance may then follow, in the form "no start was ordered" where AS1.4 allows it. Without the proof the cell is E27 and no clearance is written |
| `quarantined` | **Q33.** Lost: the journal is the journal again where the check gives intact or pending against its own outside record (LIP-0025 M5.2 [D]). That alone leaves nothing: D first completes a pending write (event 31), writes the **restore entry** on the operator's recorded act, and then, before any session leaves `quarantined`, before it acts on any verdict and before it admits any request, applies in the replay of section 5.6 every end that fell due during the loss: closures that C wrote, heights at or above `E` that AS5.1 can show, halts in the halt record of AS2.6 (with their halt marks), operator ends recorded under Q21, and the ends of event 32. It writes one end for each session so ended. Only then does a slot leave this row: a record without an end is `suspended` until the next verdict, a record with an end is `ended`, and a slot without a record is `none`. Where D cannot show the halt record, the recorded operator ends or a verdict for a session, the replay for that slot is not complete and the slot stays `quarantined`. Anew: cannot occur; the new identity is the journal | **Q34.** Lost: cannot occur; nothing can be written. Anew: `none`. On the operator's attended act D writes a slot clearance: the slot, its account and generation; the reference to the proof P1 of the station contract for that account; the fenced identity of the lost journal, from the recovery entry; the statement that no start order for the slot is outstanding, which is D's and rests on the starter's proof that it holds and will execute no outstanding order for the slot under any identity and that it has fenced the lost identity; and its own pair of identity and position. The first such clearance after a recovery entry also cites the census (section 5.6, item 4). The charges of section 5.6 still apply | **Q35.** D creates no run. Lost: `JOURNAL_LOST`. Anew: cannot occur; the new journal holds no session and no restart, and a restart of the lost journal is charged under section 5.6 | **Q36.** Lost: D can read no admission and orders nothing: `JOURNAL_LOST`; a restore takes the recovered write under this event in the row that the replay leaves, and a start anew charges it. Anew: cannot occur in the new identity, which holds no such write |

### 5. The rules that hang off single cells

#### 5.1. Cell N1: the checks of a start

C makes the checks C1 to C7 and gives the verdict. D then makes D1 to D12
in this order (**P**).

The order of C1 to C7 is not this profile's. For a path that is a parent
and a child, version 0.1.55 now proposes one order on main, which is not in
the base of this branch: LIP-0014 section 8.4, rows F1 to F19, then A1,
then F20 to F24, then E0 to E3 for a request (its paragraph "The
predicate"), as a proposal of that version (its status paragraph). The
table below cites that order where it decides one of the orders O-1 to
O-6, and says so; where it does not, the order stays open in that table.
For a root grant alone that version has no step table ("A root grant has no
step table in this version", LIP-0020 W11.14 as release 0.1.55 has it), so
for a root each check stands where its own cited text puts it. The column
"Order" says **R** only where an order is the cited text's own.

| # | Check of the grant checker | Order that the cited text states | Code |
| --- | --- | --- | --- |
| C1 | The request and every grant of the path are read as signed objects: the pipeline of LIP-0020 W9.1, with W11.8 to W11.10 for a grant. A child is read under the delegation key of its parent, as W11.8 carries it; a child signed by another key refuses here | For a child, **R** as proposed by version 0.1.55 [D]: the parent as a document (row F1), then the child as a document (F2), then the observation (F3); "a refusal of a document is computed in no observation" (row F3 and pair Q1), so the documents stand before the observation although LIP-0022 B6.1 puts its six codes "before every rule of a grant". For a root, **P** as before: these are rules of the signed object and stand before the observation. Whether a reader judges a whole parent is O-6 | The codes of that pipeline (section 6, list 3). **O** for the invocation (N1) |
| C2 | One healthy observation, on the pinned chain, with a clock that holds and a tip that is not too old | **R** LIP-0022 B6.1 [D]: its six codes in their order | `OBSERVATION_CHAIN`, `OBSERVATION_VOID`, `NODE_UNHEALTHY`, `NODE_DISAGREEMENT`, `OBSERVATION_CLOCK`, `TIP_AGE` |
| C3 | Every fact of the verdict comes from the one observation of C2 | **R** LIP-0022 B1.5 [D] | Those of C2 |
| C4 | For every link, the checks that LIP-0008 section 4 lists in its steps 1, 2 and 4, and section 12: the names and their owners; the request under the recipient mode and its Subject; the closure journals; the window; the recent block; the issuance; the seal, whose kind is `revocable-only` and which the node supplies unspent with the mempool included; the exact leaf in `actions`; the executor and the authenticated pin of the service; `iat <= now < exp` | For a parent and a child, **R** as proposed by version 0.1.55 [D]: the order is that of its rows, and it is neither every check of one link first nor every signed octet first: both documents (F1, F2), the observation (F3), the contract (F5, F6), the parent live in its six parts in their order (F7: recent block, the issuer's name, the recipient's name, the closure journal, the window, the seal and the issuance), then the checks of the child (F8 to F19), the authentication of the request (A1, after the name proof of F19), then the child live, its seal and issuance (F20, F21), and after the predicate the request's own checks (E0) before the reservation (E3). Inside the seal and issuance blocs of F21 the order is unordered there still (its open points O1 and O6), and inside E0 also (its O3): O-1. **R** LIP-0022 B6.2 [D]: `RECENT_BLOCK` stands before every rule that uses the recent block. For a root, and for a path of more than a parent and a child, **P**: this row lists the checks and states no order among them (O-1) | The codes of the walk of a name; `REQUEST_AUTH`, `REQUEST_SUBJECT`; `GRANT_CLOSED`, `ISSUER_NAME_CLOSED`; `GRANT_WINDOW`; `RECENT_BLOCK`; `RECENT_BLOCK_WINDOW`, `CONFIRMATIONS`; the issuance codes of LIP-0023 section 7 and of LIP-0020 W9.4 (section 6, list 3); `SEAL_PROFILE`, `SEAL_OUTPUT`, `SEAL_SCRIPT`, `GRANT_SEAL`; `GRANT_ACTION_ABSENT`; `GRANT_EXECUTOR`; `REQUEST_TIME` |
| C5 | Under a child: the child within its parent (LIP-0008 sections 12.2, 12.5); the row (LIP-0026 R2.1 to R2.4); the class with the list and the entry (LIP-0026 section 9; LIP-0010 section 10.6); the coin (R3.2 to R3.4); the stop coin (LIP-0027 H2); the attestation (LIP-0014 section 8) | **R**: R2.5 [D] puts the four row checks "after the admission of the parent, and before the check of the child's attestation"; R9.9 [D] puts the class checks "before the checks of the coin"; R6.1 [D] orders the three coin checks. Their place beside the attestation, which R6.1 left open, is now proposed by version 0.1.55 [D]: the class checks (its row F19, in the order of R9.9), then the coin (F22, in the order of R6.1), then the attestation (F23), then the stop coin and the withdrawal of the attestation (F24, in the order of LIP-0027 H2.7, which reads its closure journal first within that step, H2.1). The limit kinds are judged inside the row checks, after the keys of the limits and before their amounts (F17 (b)): O-3, O-5 | `CHILD_GENESIS`, `CHILD_ACTIONS_WIDER`, `CHILD_WINDOW_NOT_NESTED`; the four codes of R2; the class and holder codes; the three coin codes; `ROW_CLOSED_FOR_CAUSE`, `ROW_STOP_ALIAS`, `ROW_STOP`; the codes of the attestation (section 6, list 3) |
| C6 | The contract that `contract` binds is presented or resolved (LIP-0008 section 12.2), recomputes to that identifier, and mirrors every limit of `G` by executor, kind, resource, unit and amount | **P**: the mirror is the cited text's (LIP-0008 section 2 [F]); the presentation, the resolution and the recomputation are this draft's, and it states no place for them | `GRANT_CONTRACT`, `CONTRACT_LIMIT_MISMATCH` |
| C7 | For a restart under a restart grant: `G_r` has the form of AS3.4 against the `G` of the session that the request names | **P** | `AGENT_SESSION_RESTART_GRANT` |

**The last check, L.** D asks it twice: immediately before its write (D9),
which is the reservation, and at D11. For a start D11 stands immediately
before the start order, which is the effect. For a restart D11 stands
immediately before the transition write, which is the first part of its
effect that cannot be undone (the end of the earlier run in AS5.7); the
start order then follows the transition write at D12 with no second L,
under the read at D12 that no end stands. C answers at that moment, within
60 seconds (this draft's number, N9; the same bound answers a silence with
`AGENT_SESSION_NO_VERDICT` at every ask of AS2.4), and makes all of the
following. Inside L an ended finding (a closure in a journal that it
reads, or a height at or above `E` that AS5.1 can show on the pinned
chain) is reported before every other finding of L, `OBSERVATION_VOID`
included, where one arriving block both moves the tip and reaches `E`
(**P**):

| Part of L | Mark | Code |
| --- | --- | --- |
| The tip is read again and is the tip of the verdict. "Where the tip is not the tip of the observation, the admission is void" | **R** LIP-0022 B1.6 [D] | `OBSERVATION_VOID` |
| The clock is read again, and LIP-0022 section 3 is applied with the new reading | **R** B1.6 [D] | `OBSERVATION_CLOCK`, `TIP_AGE` |
| `iat <= now < exp` holds at the new reading. "After observation work, the executor MUST recheck both measures before a new reservation/effect" | **R** LIP-0008 section 12.5 [C] | `REQUEST_TIME` |
| `H` is inside every window and below the `E` that stands or was requested | **R** LIP-0008 section 12.5 for the windows; **P** for `E` | `GRANT_WINDOW`; `AGENT_SESSION_ENDED` |
| For a child of a class row: "the pending read of check (b) of the class, the spend state of the seal of the recipient's entry with the mempool included, and its holder journal, with what the deployment's watcher supplies" | **R** B1.6 [D]; LIP-0010 H44 [C] | `CLASS_LANDLORD_PENDING`, `HOLDER_REVOKED`, `HOLDER_SEAL_NOT_LIVE` |
| Every closure journal of the journal mark has the identity of the verdict and no record for the path beyond its position | **P**. Wider than the cited rule, which names the holder journal alone | The code of the closure; `JOURNAL_LOST` |
| The seal of every link and the stop coin of the row are read again, with the mempool included | **P**. Wider than the cited rule | `GRANT_CLOSED`, `GRANT_SEAL`, `ROW_CLOSED_FOR_CAUSE` |
| C answers within the bound | **P** | `AGENT_SESSION_NO_VERDICT` |

L is as wide as LIP-0022 B1.6 and LIP-0008 section 12.5, and wider in the
three parts marked **P**. A failure of L at D9 refuses the request before
its write. **A failure of L at D11, and a silence at D11, is a refusal and
no end:** event 29. It refuses the start or the restart with the code of
the part that failed (or `AGENT_SESSION_NO_VERDICT`), ends no session,
kills no earlier run (the transition of a restart has not begun), orders
no start, and, because no order was sent, the compensating entry of
section 3.3 releases the debit and the count of that admission, so the
start is not consumed. A new block between the verdict and D11, a request
whose `exp` has passed at D11 and a checker that is slower than its bound
are refusals of this kind and no clock ends anything at D11. Two findings
of L are no failure of L: where L finds a closure of a link, or a height
at or above `E` that AS5.1 can show, D writes that end first, at D9 as at
D11 (AS5.3), with its own cause and code, and the compensating entry still
stands for the order that was never sent. A renewal and a stop have no
D11: their write is their effect.

Six orders were open rows. Version 0.1.55, on main and not in the base of
this branch, proposes a step table for a v4 child (LIP-0014 section 8.4)
and the registries behind two of its codes (LIP-0020 W11.14). Where that
text decides an order below, the row is closed by citation, as a proposal
of that version (**R** [D] there) and with no other force; where it does
not, the row stays open and the table says why. Each remaining order
decides only which code comes first where two defects meet.

| Row | The disagreement | What version 0.1.55 decides, and what stays open |
| --- | --- | --- |
| O-1 | Every check of one link before the next link (LIP-0008 section 12.2 has every link of the proof path checked), against a table that judges every signed octet of a child before any read of a node | **Closed for a parent and a child; open beyond it.** The consumer order is F1 to F19, then A1, then F20 to F24, then E0 to E3 (LIP-0014 section 8.4, "The predicate"): both documents first, then the observation, then the parent live whole (F7, in its six parts), then the child. It is neither of the two orders above. What stays open, in that text itself: the order of the three blocs of the seal and the issuance against each other, and the place of the classification of a validated spend against two of them (its open points O1 and O6, row F21 and part 7.6 of F7), and the order inside E0 (its O3). Open in this draft also: a root alone, which has no step table there, and a path longer than a parent and a child. C1, C4 and C5 follow the cited order for a child and state none for a root |
| O-2 | The journal first, against the documents first. A malformed request at a lost journal gets another code under each | **Closed for a child, documents first; the code of an unreadable journal stays open there.** Rows F1 and F2 stand before F3 and before every journal read, so "a malformed document is refused although a read would fail as well" (pair Q1). Inside the predicate the journal of the parent stands after its recent block and its names (part 7.4 of F7), the journal of the child first inside F20, and the journal of rows first inside F24. That a journal of closures of a grant that cannot be read admits nothing is fixed there, and its code is open (its open point O5); this profile's verdict code for it, `JOURNAL_LOST` (AS2.6), is **P** until its editors assign one, and a journal whose lost-mark stands is lost in this profile however it is read (AS2.3). For a root the place stays open with O-1. D reads the session journal at D1, after the verdict, as before |
| O-3 | The place of an undefined action text and of an undefined limit kind, and of the request's own checks (the leaf in `actions`, the Subject, `iat <= now < exp`), relative to the checks of a child | **Closed in part.** An undefined limit kind of a child stands inside the row checks, after the keys and before the amounts, as `LIMIT_KIND_UNDEFINED` (F17 (b)), and for the kinds that a request consumes and that neither grant states, after the predicate as `LIMIT_KIND_UNDEFINED` (E2; LIP-0020 W11.14). A request for an action that no type profile defines stands after the predicate as `ACTION_UNDEFINED` (E1), before E2 and the reservation E3 (pair Q20); this profile, once accepted, is the profile that defines its five leaves, so E1 is met by C for the leaves of section 3.2 and refuses every other text. The request's own checks of E0 (the leaf in `actions` and in `delegate.actions`, the executor, `iat <= now < exp`, the proof path) stand after the last step of the predicate (pair Q26) and before E3, and their order among themselves and against E1 and E2 stays open there, with their codes (its O3), as does the code of an unauthenticated request (its O2, step A1). The Subject of a request is named in no row there: its `SUBJECT_MISMATCH` reports the `genesis` of a child against its parent (LIP-0020 W11.11, rule 4; F8) and is no answer for the Subject of section 3.1, whose place and code (`REQUEST_SUBJECT`, proposed) stay open here. D3 keeps only this profile's own key check |
| O-4 | The inner order of the atomic write | **Closed.** For the debits, the reservation is one atomic write, the own account before the row account for each key (E3, carrying LIP-0026 R5.6 [D]). The rest of the inner order is this profile's own and needs no other text: D10 states it |
| O-5 | The class checks against the coin checks and against the attestation: R9.9 puts the class before the coin, and R6.1 leaves the coin's place beside the attestation open | **Closed.** The class checks stand at F19, the coin at F22 in the order of R6.1, the attestation at F23, and the stop coin with the withdrawal at F24 (pairs Q13, Q15, Q16 and Q19): "The checks of the coin of a row stand before the first step that reads an attestation" (rule T6). C5 states it |
| O-6 | Whether a reader judges a whole parent, with the rows that no presented child selects. The base gives two conforming answers, admitted and `GRANT_DELEGATE`: "This version does not determine that a reader judges them" (LIP-0020 W11.10 [C]) | **Narrowed, and open.** What an admission must judge is fixed there: rules 1 and 3 of W11.10 with the parent (F1) and rules 4 and 5 for the group and the range that the ordinal selects alone (F13 (b), rule T10). What a side does with a finding of the other rules, or of those two in another group, is open (its O7): "Two outcomes conform until the owner decides proposal Q1 of LIP-0026". The decider is therefore no longer the editors of the step table: it is the owner's decision on that proposal, and until then two builders still differ on such a parent. C1 follows F1 and F13 for a child and decides nothing beyond them |

| # | Check of the dispatching service, in this order | Mark | Code |
| --- | --- | --- | --- |
| D1 | The continuity check of the session journal, with its four outcomes in the order of LIP-0025 M4.6. Intact: D goes on. Pending: event 31 first, then D goes on. Fenced and lost refuse | **R** LIP-0025 M4.1 to M4.6 [D]; the codes are those of its section 8 | `JOURNAL_FENCED`, `JOURNAL_LOST` |
| D2 | The identity of the request is not in the journal, and its `iat` is later than the `fenced_at` of every recovery entry. Only an admitted request writes its identity. Identities and ended records are kept as long as the journal lives | **P**, after LIP-0028 T2.6 and T5.8 [D] | `AGENT_SESSION_REPLAY` |
| D3 | The final grant of the cited path states no limit whose `kind` is one of the three texts of section 3.3 and whose full key section 3.3 does not define; the level and the span are stated. A kind that no type profile at C defines was refused by C as `LIMIT_KIND_UNDEFINED` (section 3.3, O-3) and does not reach D | **P** | `AGENT_SESSION_LIMIT_KEY`, `AGENT_SESSION_LIMIT_MISSING` |
| D4 | The slot table maps the recipient to exactly one account at its current generation | **P** | `AGENT_SESSION_SLOT` |
| D5 | The slot holds no session that counts (cells H1, S1, E1) and is not quarantined (Q1); and no session of the same recipient counts at `X` in any other slot, also after a change of the slot table | **P**. The key holder keeps the stronger duty that cannot be checked here: "A slot holds runs of one origin" (LIP-0028 T7.7 [D]) | `AGENT_SESSION_SLOT` |
| D5.1 | No halt mark stands in the session journal for the pair of the final grant of the cited path and its recipient (section 5.8) | **P**, and **O** (Q16) for its lifting | `AGENT_SESSION_HALTED` |
| D6 | The process of the agent will hold no key or right of an effect. A deployment duty | **P**. The cited duty has another subject: "The process of the executor's model MUST NOT hold the right to the effect. Keys, tokens and privileges of an effect sit at a gate under another OS account" (**R** LIP-0029 O1.6 [C]). This draft extends it to every agent that the host starts; the placement under another account is a need of the station contract (section 7.2) | None |
| D7 | `H < lease_end_height <= H + span`, and `lease_end_height` is at most the `not_after_height` of every link | **P** | `AGENT_SESSION_SPAN` |
| D8 | The ceilings of the operator: an operator "never increases a rental ceiling" (**R** LIP-0008 section 2 [F]). The capacity of the host is D's own fact | **P** for the capacity | `AGENT_SESSION_CAPACITY` |
| D9 | The last check L, before the write | See L | Those of L |
| D10 | One atomic write of the store, or nothing, and then `advance` at the outside record. Its reads, in this order: the slot holds no session that counts; no session of the recipient counts; the own level, then the row level; the debit of one start in the own account, then in the row account. It writes the session record: the identifier, which is the identity of the request; the fields (b) to (f) and (h) of the verdict, whose field (d) is from then on the recorded session's path; the channel of the request, for a recipient by name; the slot with its account and generation; the configuration that will be started; `E`; and run 1 with its origin reference. Inside the write D reads the halt mark of D5.1 again, after the slot reads and before the levels, so that a halt that was written between D5.1 and the write still refuses the start | **P**. "An executor reserves all debits of one request in one atomic write of its journal, or none of them ... the own account before the row account" (**R** LIP-0026 R5.6 [D]) | `AGENT_SESSION_SLOT`; `AGENT_SESSION_HALTED`; `AGENT_SESSION_LEVEL_OWN`, `AGENT_SESSION_LEVEL_ROW`; `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| D11 | The last check L, before the effect: for a start before the start order, for a restart before its transition write. Its failure, and a silence, is event 29: a refusal that ends nothing | See L | Those of L |
| D12 | D reads its own journal once more: the session record has no end and the run has no outcome. Where an end stands, D orders nothing (cells E29, E35). Otherwise D orders the start in the slot, at most one order for each run, ever. The order names the session, the run and the pair of the identity of the session journal and the position of the entry that created the run. The starter keeps every order by that pair, so that after a crash it can prove by the pair that it received no such order and fence the pair, or not prove it (event 36); that proof is a need of the station contract (section 7.2). The act "happens only after `advance` was accepted" (**R** LIP-0025 M3.2 [D]) | **P** for the content of the order and for the read | None. An unknown outcome is event 27; a proved failure is event 30 |

#### 5.2. Cell H2: a restart is a new run

By the owner's decision of 2026-11-16 a restart is by a signed request, and
the host must be able to bring a crashed session back. The rules of this
section are **P**.

| Rule | Requirement |
| --- | --- |
| AS5.4 | A restart creates a **new run**: a fresh origin, a fresh bind at the key holder, and a new run record in the session. The session identity spans its runs; the key holder's run does not. A restart never resumes an earlier run and never has the launcher bind an earlier run again. The origin of the new run is the admitted restart request: its identity with the identifier of the grant that it cites. Whether LIP-0013 J7.1 admits that origin is N5 |
| AS5.5 | The slot, the account with its generation and the configuration are those of the session record. A slot table that now maps the recipient to another account, or to the same account at another generation, refuses as `AGENT_SESSION_SLOT`. No restart moves a session, and none changes `E` or the identifier |
| AS5.6 | **A restart passes every check of a start, through the gates of convention 3.** In this order: C1 to C7 for the request, with the restart leaf in `actions` of the grant that it cites, which give a verdict with the cited path and, under a restart grant, the session path (AS2.1 (d), (d2), (g), (h)); D1; D2; the session is in the journal for the executor of the request with a recorded session's path equal to the path of the session path result, where the cited path is that path or a restart grant that passed C7 against it (`AGENT_SESSION_UNKNOWN`). Only now is the session path result applied: `sound` goes on, `ended` writes the end and refuses with its code, `suspended` refuses with its code; and `H` below the `E` that stands is part of it (AS5.1). Then: the request result on the cited path passes (its code where it does not; the session path result applied above stands either way, as the path verdict that AS2.4 owes in any case, and no write, no debit and no transition follow); the session has no end (`AGENT_SESSION_ENDED`); **every run of the session has a recorded start-order outcome, no start order of it is outstanding, no admission of it stands without an outcome under event 36, and no restart of it is blocked** (`AGENT_SESSION_RUN_OPEN`, before any write and any debit; a restart orders run k+1 never while the start outcome of run k is unknown); AS5.5; the cited grant states no limit with a key that D3 refuses (a restart grant needs no level and no span); D8; D9. The starts limit is met in the admission write, in the own account of the **cited** grant and then in its row account (`OWN_LIMIT_OVER`, `ROW_CAP_OVER`) |
| AS5.7 | **The one order of a restart: admit, check, end the earlier run and fence it, create, start.** (1) After D9, D writes the admission entry in one atomic write: the identity of the request, the debit of one start in the own account of the cited grant and then in its row account, and "restart admitted". No new run exists yet. (2) D11, the last check. Its failure is event 29: a refusal, the compensating entry, no transition, and the earlier run untouched. (3) The transition: D has the earlier run ended and asks the station contract's proof P1 that the account holds no process. With the proof D writes the transition entry in one atomic write: "run k: ended" with the reference to P1; the **run fence**, which is this entry's own pair of identity and position and stands for the slot as a clearance stands, so that the starter executes after it no start order for a run up to k and none of a fenced identity or of the same identity at an earlier position; and the creation of run k+1, which the key holder binds. (4) D12, whose read finds no end, orders the start of run k+1. Where, inside step (3), the end of the earlier run is unknown or the proof fails, the cell is H35; where an outcome was already unknown at the checks, AS5.6 refused before any write and the cell is not H35. A delayed order of run k therefore lands never beside run k+1: it is refused by the starter under the fence, and where its outcome is still unknown no transition begins at all |
| AS5.8 | **Two signers.** The key holder of `A` signs under `G`, where `G` lists the restart leaf. The session service of the host signs under a restart grant (AS3.4). Under the first alone, a host cannot bring a session back after a reboot unless the key holder of `A` is up and an origin there still lists the grant. The second is proposed and awaits the owner's yes (Q15) |

**A worked restart under two paths (P).** A session `S` was created by an
admitted start under the path parent `P` to final grant `G`, recipient the
agent `A`; that path is `S`'s recorded session's path, with lease end `E`,
and run 1 has the recorded outcome "ordered and started". After a reboot
the session service of the host signs a restart that cites a restart grant
`G_r` (recipient the session service, a starts limit of 10 in its own
account, of which 3 stand debited) and names `S`. C's verdict carries:
(d) the cited path of `G_r`; (d2) the session path `P` to `G`; (e) the
limits of `G_r`, starts 10; (f) the `E` that stands; (g) for the session
path, `sound` at its tip; (h) on the cited path, passes. D passes the
gates of convention 3 (D1, D2, and `S`'s recorded path is the path of
(d2)), applies (g): `S` is `session held`. It then debits nothing yet:
only in the admission entry of AS5.7 does it debit the own account of
`G_r`, 3 to 4, and then its row account where `G_r` is a child. It debits
no account of `G`. Where the seal of `G_r` was spent instead, (h) is
refused as `GRANT_CLOSED`, (g) as applied above still stands and `S` stays
`session held` on its own path, and D writes nothing, debits nothing and
orders nothing (case S30-28). Where (g) is `ended` instead, D writes the
end of `S` and the restart refuses with the code of that closure, and again
nothing is debited. Later path verdicts for `S` are verdicts on `P` to `G`,
with the octets and the channel of that path (AS5.12); the restart under
`G_r` changed neither, because it presented nothing for the session's path
and was admitted on it in no check.

#### 5.3. Cells H3 and S3: a renewal

| # | Check, in this order (**P**) | Code |
| --- | --- | --- |
| 1 | C1 to C6 for the request, with the renew leaf in `actions`. The request presents the list and the attestation where they changed since they were last taken for the session's path (AS5.12) | The codes of section 5.1 |
| 2 | D1, then D2 (the first two gates of convention 3) | `JOURNAL_FENCED`, `JOURNAL_LOST`, `AGENT_SESSION_REPLAY` |
| 3 | The third gate: the session is in the journal for the executor of the request with a recorded session's path equal to the path of the session path result, which for a renewal is the cited path. Only then is the session path result applied: where it is `ended` D writes the end and the request refuses with its code (for a height, cell H9: the height decides before the request); where it is `suspended` the request refuses with its code. A request whose gates refused moves nothing | `AGENT_SESSION_UNKNOWN`; the code of the session path result |
| 4 | The session has no end, and `H` of the verdict is below the `E` that stands. The new `lease_end_height` is above the `E` that stands, at most `H` plus the span, and at most the `not_after_height` of every link. A renewal never lowers a lease and never leaves it as it is | `AGENT_SESSION_ENDED`; `AGENT_SESSION_SPAN` |
| 5 | D9; then one atomic write with the read that the record has no end | Those of L; `AGENT_SESSION_ENDED` |

The authority stands for the heights `H` with `H < E` inside every window.
The journaled end records the first finding of what the heights already
decided.

#### 5.4. Cells H4 and S4: a stop

The checks are those of section 5.3 with the stop leaf and without the
comparison of a new lease end; the write is the end (**P**). A stop is
admitted like every invocation: "Admission requires two predicates
together" (**R** LIP-0008 section 12.5 [C]), and this profile makes no
exception for a request that only takes authority away. That is a decision
of this draft: a recipient whose session path result is not `sound` cannot end its
own session, and cells 19 and 21 still can. A stop that arrives at a tip
with `H >= E` meets the end of H9 first and refuses as
`AGENT_SESSION_ENDED`.

#### 5.5. Cells 7 to 18: the path verdict

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS5.1 | **The fixed list of a path verdict, in two parts.** **Part H, the height, first and outside the observation:** C compares `E` with every block that it can show: a block that its reading node validated on that node's active chain, where the node gives the pinned genesis hash for the block of height 0 (LIP-0022 B1.3 [D]), at a height at or above `E`. Where C can show such a block, the session path result is `ended` with the cause "height" and that block's hash and height, whether or not Part P can be made: a failed clock, a failed comparison node, a void observation and a lost closure journal are no bar to it. A block from a node that does not give the pinned genesis, or not on its active chain, shows nothing. **Part P, the path, in one observation and no other reads:** where Part H shows no such block, the verdict runs exactly these checks for the session's path, in one observation (C2, C3), and no other: the lease comparison at the tip of that observation (`H < E`, whose failure is the same `ended` by height at that tip); the names and their owners; for a recipient by name, that the name yields a key for the channel that D recorded for the session (check D10, updated only as AS5.12 states); the closure journals; the windows; the recent block and the issuance of every link (the issuance codes of check C4); the seal of every link, supplied unspent with the mempool included; the executor and its pin; and under a child the child within its parent, the row, the class with the list and the entry, the coin, the stop coin and the attestation, each with the octets of AS5.12. It verifies no signature of a request and runs no command, no leaf in `actions`, no `iat` or `exp`, no Subject, no contract mirror and no limit. Its age class is the first of LIP-0022 B3.5, because the profile states none. `suspended` is the answer only for what C cannot show in Part P **and** cannot end in Part H | **P**, after LIP-0028 T4.5 [D], for Part P and for the carve-out of Part H. The pinned chain of Part H is that of the observation: "The observation is on the pinned chain: the node gives the pinned genesis hash for the block of height 0" (**R** LIP-0022 B1.3 [D]). A replaced channel key under the same owner changes no verdict (cell H25) |
| AS5.2 | **A requesting verdict carries the same session path result.** The verdict of a restart, of a renewal and of a stop holds, beside its request result on the cited path, the session path result of AS5.1 for the session's path at the same tip, computed with what a request under that path presents (AS5.12); a restart under a restart grant presents nothing for the session's path, so its result is computed with the octets that C holds for that path. The session path result alone decides `session held` against `suspended` against `ended`, and it is applied only through the gates of convention 3. A failure of the request alone (its signature, its leaf, its `iat` or `exp`, its Subject, its lease end) refuses the request and moves no state of itself, after that application; a replay refuses at gate D2 and reaches no application | **P** |
| AS5.3 | **The fixed effect of each result.** `sound`: `session held`, while the verdict is current. `ended`: D writes the end before it does anything else, when the result reaches it as an event (for a requesting verdict, through convention 3). The result is `ended` only where a closure journal holds a closure of a link of the session's path (events 12, 16, 17), or the height part of AS5.1 shows a block at or above `E` on the pinned chain (event 9). `suspended`: every other result, and no current verdict. A removal mark, a withdrawn attestation and a form mark are durable and close no link: they suspend | **P** |
| AS5.12 | **Whose octets a verdict on the session's path uses.** A path verdict takes no list of a landlord and reads no new attestation. It uses exactly the octets that C holds for the session's path under AS2.6: the list and attestation octets that C last took or held under the pinned hash in a check **on that path** (the start that created the session, and after it any request that C judged on that path and in whose checks a take or a reading under the pin stood, whether or not D then admitted that request), and the channel that D recorded at the start, which D updates only in the write of an admitted renewal, stop or restart **under that path** with the channel of that request. A request under a second document, and a restart under a restart grant, presents nothing for the session's path and changes neither its octets nor its channel, however later it was signed. Event 15 is that C holds no octets under the pinned hash for the session's path in this sense. A fact that only a presentation can supply gives `suspended` (cells H15, H18), and the exit is a renew request under the session's path that presents it | **P**. The take of a list happens in an admission (LIP-0010 H40 [C]) |
| AS5.13 | The node of C watches, with its mempool included, the seal of every link of every such path, the stop coin of the row of a child, and for a child of a class row the seal of the recipient's entry. A conformance claim names the interval of the mempool read; this draft states none | **P**, after LIP-0029 O8.3 [C] |

#### 5.6. Cells 22 to 24 and 31 to 34: journals that are lost, pending, restored or started anew

Each list is **P** except where marked.

**A closure journal.**

| # | Rule |
| --- | --- |
| 1 | It is lost where its continuity check gives lost, and also where a record of it fell due and could not be written, for as long as its lost-mark stands (AS2.3, AS2.6), whatever the check then gives. While it is lost, C gives no sound verdict for a path that could need it, by the scope of item 2 (cell H22); the height part of AS5.1 still answers `ended` where it can show its block. A journal that is restored and passes the check against its own outside record (LIP-0025 M5.2) has its identity and, where its lost-mark is cleared by that recorded act, verdicts resume. A restart of C clears neither a loss nor a lost-mark |
| 2 | A journal that is started anew has another identity. No verdict with that identity lifts a suspension or keeps the state `session held`: D ends every session without an end whose path could have had a record in the replaced journal (cell H32). For the journal of seals and issuers' names that is every session; for the journal of rows, every session under a child; for the holder journal, every session under a child of a class row. This is the charge of LIP-0025 M5.5 for this profile: "it covers everything that the lost journal could have held" (**R** [D]) |
| 3 | A new start at a newcomer is the base's: after the recorded start anew the verifier admits again and reports no closure that it does not hold (LIP-0008 J6.9 [C]; LIP-0027 H3.6 [D]; LIP-0010 H43 [C]). A closure whose spend has left the view is lost with the journal. This profile adds no charge there and states the limit (S30-K3, N8) |
| 4 | Pending: C completes the outside write first, the closure entry stands, and C delivers `ended` for every path that holds the link |

**The session journal.**

| # | Rule |
| --- | --- |
| 1 | While it is lost, every slot of the host is `quarantined` (cells N23 to E23). Restoring it is event 33 |
| 2 | Starting anew is the operator's attended act of LIP-0025 M5.3. The recovery entry counts as the end of every session that the lost journal could have held, with the cause "journal lost". Nothing is recorded for a single session, because none can be named |
| 3 | Every row account of the starts kind that could have had a record counts as full (**R** LIP-0026 section 5 [D]: "every row account that could have had a record counts as full"). So does every own account (**P**). The levels are not charged: item 4 holds every slot. A grant could have had a record unless the height of its recent block, and for a child that of its parent, is at or above the block boundary of the new journal (LIP-0025 M5.4) |
| 4 | Every account that the lost journal could have recorded is quarantined: every slot of the slot table, and every account that was a slot earlier. After a start anew a slot leaves by event 34 alone; while the journal is only lost, a slot also leaves by a restore that completes its replay (item 7, event 33). The first clearance after a recovery cites the **census**: the station contract's proof that no process runs in any account that was ever a slot and is no slot now |
| 5 | Every start, restart, renew and stop request whose `iat` is not later than the `fenced_at` of the recovery entry refuses as `AGENT_SESSION_REPLAY`, because the lost journal could have held its identity (after LIP-0028 T5.8 [D]). A later request that names a session of the lost journal refuses as `AGENT_SESSION_UNKNOWN` |
| 6 | **Pending.** LIP-0025 M4.3 leaves to the rule of each journal "Whether the act that it records may still follow". For the session journal it does not follow. D completes `advance` first and the entry stands. No effect was ordered for it (M3.2), and none is ordered from it after the completion either. A pending start entry gives run 1 "not ordered" with the compensating entry and the annulment, or the end and the clearance "no start was ordered" where a closure or a height is then found. A pending admission entry of a restart gives "restart of run k: not ordered" with the compensating entry. A pending transition entry gives run k+1 "not ordered" with its compensating entry, and the end and the fence of run k in that entry stand. A pending renew entry stands with its new `E`. A pending end (with its halt mark, where the end is a halt), clearance, restore, recovery or boundary entry stands. The caller of a pending request that sends it again meets `AGENT_SESSION_REPLAY` |
| 7 | **Restoring, and the ends of the loss.** The operator puts a store in place, and the journal is the journal again where the check gives intact or pending against its own outside record (**R** LIP-0025 M5.2 [D]). D completes a pending write first (item 6) and then writes the **restore entry**, a recorded entry on the operator's act, before it writes anything else; its form is open with the entries of the journal (N6). From the restore entry until the replay below is complete for a slot, that slot is `quarantined` (AS1.2): D acts on no verdict for it except in the replay, admits no request for it and answers "no session held". The replay, for every session whose record has no end, in this order: (a) D asks C for a verdict on the session's path; a result `ended` by a closure that C wrote during the loss, or by the height part of AS5.1 at or above `E`, or a verdict of event 32, writes the end with that cause (among ends, a closure before a height, convention 5); (b) where (a) wrote no end, a halt for the session in the halt record of AS2.6 writes the end and its halt mark (section 5.8), with step 13 of LIP-0029 section 11 recomputed against the session as restored; (c) where neither wrote an end, a recorded operator end of Q21 for the session or its slot writes the end. One end is written for each session, with the first cause in that order. A halt mark that stood before the loss stands after it, and an admitted entry without an outcome is taken under event 36 after the replay, in the row that the replay leaves, and is never ordered from. Only when (a) to (c) are done for a slot does it leave `quarantined`, to `ended`, to `suspended` until the next verdict, or to `none` where it holds no record. Where C cannot give the verdict of (a), cannot show the halt record, or the recorded operator ends cannot be shown, the replay of that slot is not complete and it stays `quarantined`; D does not guess the ends of the loss away. A restore charges no account and fences no identity |
| 8 | **Fenced identities and halt marks after a start anew.** The recovery entry names the identity of the lost journal as `previous` (**R** LIP-0025 M5.3 [D]); that identity, and every identity so fenced before it that a recovery or a slot clearance names, is a **fenced identity**: the starter executes no start order that carries it, at any position, and D takes no pair with it as a position of its journal (AS1.4). A start order of the lost journal beside a new session is therefore not a matter of comparing 4990 with 3. Halt marks of the lost journal cannot be read; no separate charge is stated for them, because every grant that could have had a halted session in the lost journal is already charged in full under item 3 for the same boundary, so a new start under it refuses on its account before any halt mark could be read, and a grant that could not have had a record, by that boundary, could not have had a halt mark either |

#### 5.7. Cells H9 and H10: the end of a term

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS5.9 | A grant is not extended, and a session does not move to another grant (AS1.1). A new term is a new grant and a new session, opened by a start request, with a new identifier. The cost is one start of the agent in each term | **P**. "Each grant ... ends at `not_after_height`" (LIP-0008 section 2.1 [C]); "A slot serves one grant and lives as long as that grant" (LIP-0017 section 8 [D]) |
| AS5.10 | A row admits one child, ever. Its coin is spent by the anchor of that child (LIP-0026 R3.3 [D]), and the signing service makes one signature, ever, for one place of one parent (LIP-0014 J4.4 (a) [C]). A place whose signing outcome is unknown stays reserved in that ledger and gives no successor: "the row is lost to this parent, and the next child takes another row or another parent" (**R** J4.4 (f)). The party that wants a second term therefore holds a spare row or a second parent before the closing height | **P** for the last sentence |
| AS5.11 | C reads a child through the pipeline of LIP-0020 W11.8, under the delegation key of its parent; that decision awaits the co-author's agreement, and W11.8 carries it for the octets of `swarma-grant/4`. LIP-0008 section 12.6 states the signature by the parent's recipient as the rule in force. A child that is signed by its parent's recipient therefore refuses at C1 as `CHILD_SIGNER`. The disagreement is those two texts' and not this draft's | **P** for the consequence |

#### 5.8. Cells H19, N1 and check D5.1: the halt mark

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS5.14 | Where D writes an end on a halt (cells H19, S19, and a halt applied in the replay of section 5.6, item 7), it writes in the same entry a **halt mark** for the pair of the final grant `G` of the session's path and its recipient `A`, with the identifier of the halt command and of the session. While the mark stands, D refuses every start that cites that grant for that recipient, at check D5.1 and again inside the write (check D10), as `AGENT_SESSION_HALTED`. The mark is what `X` can see: it reads the grant and the recipient of the next start, and it observes no origin (LIP-0013 J7.7 [C]). A start under another grant, under the other document of a row, or for another recipient is no start under the mark. An operator end and a stop by the recipient write no mark | **P** |
| AS5.15 | **Lifting the mark is open for the owners (Q16).** This draft proposes that only a signed owner command lifts it: the same owner whose device signed the halt, admitted by the steps of LIP-0029 section 11 with its replay journal, naming the pair of the mark, after which D writes the lifting entry and no start is admitted before that write. No such command class exists in the registry today, so until the owners answer Q16 and such a class is named, a halt mark cannot be lifted and a new start under the same grant for the same recipient refuses for the life of that grant; a new grant for the agent is not under the mark. Nothing in `X` lifts it: not the operator, not a restart, not a new request, and not the clearance of the halted session. A mark that a restore finds in the restored journal stands; after a start anew item 8 of section 5.6 holds | **P** for the proposal, **O** (Q16) for the act, its class and its level |

What a halt stops beyond what D can see — in particular whether an origin
under which a halted session ran may sign a start under another grant, and
whether a halt should reach further than the one grant — is no longer filed
here as a request to the editors of other texts. It is an owners' question,
Q16, with the lifting of the mark; the answers that would widen the mark
need the owners first and only then the text that carries them.

### 6. Refusal codes

This is the one list. A cell, a check and a verdict spend a code of this
section and no other. It has three lists: the codes of this profile; the
refusals of the base that have no v4 code there, each proposed as **new**;
and the codes that are borrowed with the meaning of their source.

**List 1: the codes of this profile (P).** None of them records a closure
of a grant.

| Code | What it reports | Cells and checks |
| --- | --- | --- |
| `AGENT_SESSION_REPLAY` | The identity of the request is in the session journal, or its `iat` is not later than the fencing of a recovery | Event 5; D2 |
| `AGENT_SESSION_UNKNOWN` | The request or the command names no session of its session's path and executor, at the third gate of convention 3 or at the lookup of a halt | N2, N3, N4, N19, H6, E6, Q2 to Q4, Q19; AS5.6; section 5.3 |
| `AGENT_SESSION_ENDED` | The session that the request names has ended, or the tip has reached its lease end | E2, E3, E4, E19, E29, E35; L; section 5.3 |
| `AGENT_SESSION_SLOT` | The recipient maps to no single account at its current generation; the slot holds a session that counts; another session of the recipient counts; the slot is quarantined; or the slot of a restart is not that of the record | H1, S1, E1, Q1; D4, D5, D10; AS5.5 |
| `AGENT_SESSION_LIMIT_KEY` | The grant states a limit whose `kind` is one of the three texts and whose full key the profile does not define. A kind that no type profile defines is `LIMIT_KIND_UNDEFINED` (list 3) | D3 |
| `AGENT_SESSION_LIMIT_MISSING` | The grant states no limit of the level key or of the span key | D3 |
| `AGENT_SESSION_SPAN` | The lease end is not above `H`, or not above the lease end that stands, or more than the span above `H`, or above the closing height of a link | D7; section 5.3 |
| `AGENT_SESSION_LEVEL_OWN` | A start would put more sessions under the grant than its level | D10 |
| `AGENT_SESSION_LEVEL_ROW` | A start would put more sessions under the row than its level | D10; H6 |
| `AGENT_SESSION_CAPACITY` | A ceiling of the operator or the capacity of the host refuses | D8 |
| `AGENT_SESSION_NO_VERDICT` | C did not answer an ask for a verdict within its bound: the ask for a start, a restart, a renewal or a stop, or the last check at D9 or D11 | AS2.4; N8; L; event 29 |
| `AGENT_SESSION_RUN_OPEN` | A restart cannot go on for an open run: before any write, a run of the session has no recorded start-order outcome, a start order is outstanding, an admission stands under event 36, or a restart is blocked; inside the transition, the end of the earlier run is unknown or the proof of an empty account failed | H27, H35, S35; AS5.6, AS5.7 |
| `AGENT_SESSION_RESTART_GRANT` | The grant of a restart by the host has not the form of AS3.4 against the grant of the session | C7 |
| `AGENT_SESSION_HALTED` | A halt mark stands for the final grant that the start cites and its recipient (section 5.8) | D5.1, D10 |

**List 2: new codes proposed for the base (P).** Each would enter the codes
of the v4 admission in LIP-0020 section 11, beside the rule map of section
11.11. A code with the same meaning that lands first replaces the proposal
(N2). Version 0.1.55 on main now proposes codes for the comparisons of a
child in LIP-0020 W11.11 and for a contract in LIP-0014 section 8.4; this
branch does not carry that text, and this draft imports from it only the
two codes whose place an order below decides (`LIMIT_KIND_UNDEFINED` and
`ACTION_UNDEFINED`, list 3, O-3); its `SUBJECT_MISMATCH` is named in O-3
and in N2 only to tell it apart from `REQUEST_SUBJECT`, and no cell, check
or verdict of this draft spends it. The deciders of N2 reconcile the rest
when this draft lands on a base that carries that version; until then the
proposals below stand as they were, and no cell spends two codes for one
finding.

| New code | What it reports | Check of the base without a v4 code |
| --- | --- | --- |
| `REQUEST_AUTH` | The request does not verify under the recipient mode of the grant, the owner of the recipient's name is not the signed owner key, or the name yields no key for the channel | LIP-0008 section 4, steps 1 and 2; section 3.1 |
| `REQUEST_SUBJECT` | The Subject of the request is not the executor and the recipient of the final grant | LIP-0008 section 12.1 |
| `REQUEST_TIME` | `iat <= now < exp` does not hold | LIP-0008 section 12.5 |
| `GRANT_CLOSED` | A closure journal holds the closure of a link of the path, the final grant or a parent, by its issuer's spend | LIP-0008 sections 4, step 4, and 5.1 |
| `GRANT_WINDOW` | `H` lies outside the window of a link of the path, the final grant or a parent | LIP-0008 sections 7.1, rule 2, and 12.5 |
| `GRANT_SEAL` | The seal of a link is not supplied unspent, with the mempool included, and no validated issuer spend is on record | LIP-0008 sections 4, step 4, and 5.1, last sentence of its first paragraph |
| `GRANT_ACTION_ABSENT` | The command of the request is no entry of `actions` of the grant that it cites | LIP-0008 sections 4, step 4, and 12.3 |
| `GRANT_EXECUTOR` | The executor of the grant, the executor of the request and the authenticated pin of the service do not agree | LIP-0008 section 4, step 4 |
| `GRANT_CONTRACT` | The contract is not presented, or does not recompute to `contract` | LIP-0008 section 12.2 |
| `CONTRACT_LIMIT_MISMATCH` | The contract does not mirror a limit of the grant | LIP-0008 section 2 |
| `CHILD_GENESIS` | The genesis of a child is not that of its parent | LIP-0020 section 11.11, last row |
| `CHILD_ACTIONS_WIDER`, `CHILD_WINDOW_NOT_NESTED` on v4 | A child lists an action outside `delegate.actions`, or its window is not inside its parent's | LIP-0020 section 11.11, last row: LIP-0014 section 4 names the two for v3, and "Whether v4 takes them is an open question" |

This draft does not use `PARENT_NOT_LIVE` for a v4 parent: in the base it is
the code of a parent that fails a check of the earlier grant version
(LIP-0014 section 8, step V5). A parent link that is closed or out of its
window refuses with `GRANT_CLOSED` or `GRANT_WINDOW`, which name any link.

**List 3: borrowed codes, each with the meaning of its source.**

| Source | Codes | Spent in |
| --- | --- | --- |
| LIP-0022 section 6 [D] | `OBSERVATION_CHAIN`, `OBSERVATION_VOID`, `NODE_UNHEALTHY`, `NODE_DISAGREEMENT`, `OBSERVATION_CLOCK`, `TIP_AGE`, `RECENT_BLOCK`, `RECENT_BLOCK_WINDOW`, `CONFIRMATIONS` | C2, C4, L; N8, event 18 |
| LIP-0025 section 8 [D] | `JOURNAL_LOST`, `JOURNAL_FENCED` | D1; AS2.6; events 22, 23; the Q row |
| LIP-0008 SB2 [C], with the code texts as LIP-0024 section 3 names them | `SEAL_PROFILE`, `SEAL_OUTPUT`, `SEAL_SCRIPT` | C4 |
| LIP-0023 section 7 [D] | Its thirteen codes, in the order of C7.1: `W_PROFILE_REQUIRED`, `W_SEAL_OUTPUT`, `W_WITNESS_REQUIRED`, `W_UNCONFIRMED_NON_LINKAGE_PARENT`, `W_NATIVE_P2WPKH_REQUIRED`, `W_WITNESS_SHAPE`, `W_SIGHASH_ALL_REQUIRED`, `W_PUBLIC_KEY`, `W_ISSUANCE_SPENDS_SEAL`, `W_LINKAGE_SCRIPT`, `W_LINKAGE_REQUIRED`, `W_DEPENDENCY_ORDER`, `W_ANCHOR_PENDING` | C4; AS5.1; event 18 |
| LIP-0020 W11.14 and LIP-0014 section 8.4, rows E1, E2 and F17 (b), as release 0.1.55 has them [D] | `ACTION_UNDEFINED`, `LIMIT_KIND_UNDEFINED` | Section 3.3; C5; the paragraph after this list (O-3) |
| LIP-0008 sections 5.2 and 5.3 [C] | `ISSUER_NAME_CLOSED` | C4; event 17 |
| LIP-0026 section 6 [D] | `CHILD_ORDINAL`, `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED`, `CHILD_BUDGET_OVER`; `ROW_COIN_IN_SEAL_TRANSACTION`, `ROW_COIN`, `ROW_COIN_REQUIRED`; `OWN_LIMIT_OVER`, `ROW_CAP_OVER` | C5; D10 |
| LIP-0026 section 9 [D] | `CLASS_LANDLORD`, `CLASS_LANDLORD_CHANGED`, `CLASS_LANDLORD_PENDING`, `CLASS_CHECKPOINT`, `CLASS_VALUE_UNAUTHORIZED`, `CLASS_HOLDER`, `CLASS_WRITER`, `CLASS_HISTORY_UNAVAILABLE` | C5, L; events 14, 18 |
| LIP-0010 section 10.6 [C] | `LIST_UNKNOWN`, `HOLDER_PIN_INVALID`, `HOLDER_LIST_ROLLBACK`, `HOLDER_LIST_INVALID`, `HOLDER_LIST_MISMATCH`, `HOLDER_FORM_DOWNGRADE`, `HOLDER_SEAL_ALIAS`, `HOLDER_REVOKED`, `HOLDER_SEAL_REUSED`, `HOLDER_SEAL_NOT_LIVE` | C5, L; events 15, 17, 18 |
| LIP-0027 section 2 [D] | `ROW_CLOSED_FOR_CAUSE`, `ROW_STOP_ALIAS`, `ROW_STOP` | C5, L; events 16, 18 |
| LIP-0014 section 8 [C] | `NOTARY_WITHDRAWN`, and the other codes of the attestation steps of that section, as its table lists them | C5; event 18 |
| LIP-0020 W9.1, W9.4 and W11.8 to W11.10 [C] | The codes of the pipeline of a signed object and of a grant, and of the six steps of an issuance (W9.4), as that LIP lists them (among them `GRANT_DELEGATE` of W11.10, which O-6 names), with `CHILD_SIGNER`, `CHAIN_DEPTH` and `NOT_DELEGABLE` of LIP-0014 as W11.8 uses them | C1; C4 and AS5.1 for W9.4; event 18 |
| The walk of a name (LIP-0008 section 3; LIP-0021) | The codes of that walk, as those texts list them | C4; event 18 |
| LIP-0029 section 11 [C] | The codes of its steps 1 to 13, as its table lists them: among them `NOT_FOR_ME`, `ACTION_UNKNOWN`, `REPLAY` and `FIELDS_MISMATCH` of step 13, which this draft names in its cells | Events 19 and 20 |

The last four rows name a table of another text and do not print its
codes: this draft could not print them without restating tables that it
does not own, and it adds none to them and changes none.

An action text that no profile defines is refused by W11.4 ("an executor
refuses an action that its profile does not define"); a request with
another command is no request of this profile, and the table of section 4
does not produce it. Its code and its place are now those of version
0.1.55: `ACTION_UNDEFINED`, after the admission of the path and before the
reservation (LIP-0014 section 8.4, row E1; LIP-0020 W11.14). Once this
profile is accepted it is the profile that defines its five leaves, so a
request under one of them passes that step at an executor that runs this
profile. A limit whose kind no type profile at the side defines is
`LIMIT_KIND_UNDEFINED` at the place of O-3; a limit of one of the three
kinds with a key that section 3.3 does not define is
`AGENT_SESSION_LIMIT_KEY`.

### 7. What the profile does not decide

#### 7.1. Matters of other texts

Each is named once, with the unit that owns it.

| Matter | Owner |
| --- | --- |
| **Follow-up work.** The grant of a session authorizes the start and the holding and no instruction. An instruction is admitted under the grant that it cites and enters a run only as LIP-0013 J7.6 says: "An instruction admitted under another grant MUST NOT enter an existing run as an instruction. It creates its own run, with its own channel, or stays data" | LIP-0013 section 3.6 [C] and the gate that admits instructions. This profile adds no rule; the answer of AS2.5 is what such a gate may ask. How a later instruction reaches a running station is **O** for the owners (Q14) |
| **The model lease.** The budget of a model or of a gateway is the limits of a second grant whose executor is the model service, by the owner's decision of 2026-11-16. A failed renewal of a credential there is no event of section 4 and changes no state; the station contract has the station idle (its rule K7) | LIP-0028 [D], for a client that cannot sign, at the model service |
| **Isolation of a slot by origin.** "A slot holds runs of one origin", asked of the key holder | LIP-0028 T7.7 [D]. `X` checks what it can observe: one session for each slot and for each recipient (D5) |
| The mapping of D's own closed set of refusals to the codes of section 6 | The implementation of the dispatching service |

#### 7.2. What the profile hands to the station contract, and what that contract lacks

The first column counts the rows as the owner of the station contract
listed them against this profile. The labels of the third column are those
of that contract's draft, which is in a fix round of its own. This profile
defines none of these rows. Where the last column is not empty, the
profile needs something that the contract does not carry yet; it is listed
as a need of that contract and decided nowhere here.

| # | What the profile hands over | The row of the station contract | Need of that contract |
| --- | --- | --- | --- |
| 1 | The states of a process | `starting`, `running`, `stopping`, `stopped` | A start order has the outcomes that the profile reads apart: started, proved not started (event 30), unknown (event 27), and never received and fenced by its pair, proved after a crash (event 36) |
| 2 | The restart of a service or of its machine | The events "crash of the starter" and "host reboot" | A cell for the restart of another service that a station depends on: the grant checker, the key holder, a gateway |
| 3 | Liveness, heartbeat, backoff | Its rule K4 | The actor on silence, and who looks whether the process of a session in the state `session held` is down |
| 4 | The home and its export | Its section 8 and rule K8 | The sequence of an export |
| 5 | Retirement | `retiring`, `retired` | None |
| 6 | Every bound in clock time for a process | None yet | A named bound from D's journaled end of a session, and from a recovery entry, to the proved absence of its processes, and who acts when it is exceeded. This is the stop duty of every cell that ends |
| 7 | The proof of an empty account | Its proof P1 | That P1 is the proof which a clearance and a run fence cite; that it is a proof for an account; that the starter keys every order by the pair of the journal identity and the position of AS1.4 and executes none of a fenced identity, none below the last clearance or run fence of the slot in the same identity, and none for a run that a fence covers; and that after a crash it proves by that pair that it received no such order and fences the pair, or does not prove it (event 36) |
| 8 | The slot table and how an account is created | Account creation | The slot table as a durable object with its owner: which recipient maps to which account, what a generation is, and which accounts were slots earlier (section 5.6, item 4) |
| 9 | The delivery of the verdict from C to D | Its rule J1 | The authenticated delivery, the retry and the order of the object whose content AS2.1 fixes |
| 10 | The processes after a lost session journal | None yet | An event "the session journal of the dispatching service is lost or fenced", after which every station of the host goes to a `held:*` row and leaves only by P1; the durable record of an operator end attempted while the journal is lost, which the replay at a restore reads (cell Q21); and the census of section 5.6 |
| 11 | The word for a validly occupied session | `held:*` is an unknown outcome there | None: this profile writes `session held` and never "held" alone |
| 12 | Later instructions to a running station | Its rule K5 | The owners' answer to Q14 |
| 13 | The model lease | Its rule K7 | None |

Three more needs follow from rules of this draft: the placement of effect
keys and of credentials that work without a signature outside the slot
account (D6); the end of a run with its proof during a restart, and the
operator's act where that end is unknown (AS5.7, event 35); and the
operator end of event 21: who the operator is and how that act is
authenticated.

### 8. Cases

Each case names its cells and has a control that is admitted. Vectors come
with the members of the invocation.

| Case | Setting | Outcome | Cells |
| --- | --- | --- | --- |
| S30-1 | A valid start; starts 5, level 1, span 144; lease end `H + 144` | Admitted | N1 |
| S30-2 | The same with `H + 145`; with `H`; with one above `not_after_height` | `AGENT_SESSION_SPAN` each. A lease end equal to `not_after_height` inside the span is admitted | D7 |
| S30-3 | A grant without the level limit; without the span limit; without the starts limit | `AGENT_SESSION_LIMIT_MISSING` twice; then `OWN_LIMIT_OVER`. With all three the start is admitted | D3, D10 |
| S30-4 | A limit of the starts kind with a `period`; a limit of a kind that no type profile at the checker defines, beside the three | `AGENT_SESSION_LIMIT_KEY`; then `LIMIT_KIND_UNDEFINED` at the checker. Without either the start is admitted | D3, C5 |
| S30-5 | A second start, with a new identity, for the same slot while the first is `session held`; after its end and before the clearance; after the clearance | `AGENT_SESSION_SLOT` twice; then admitted | H1, E1, E28 |
| S30-6 | The request of S30-1 once more | `AGENT_SESSION_REPLAY`; no second session | H5 |
| S30-7 | The start order of S30-1 gives no answer; the caller sends a start with a new identity; the session is stopped; a clearance is asked while the outcome is unknown; the station proves that nothing started | `AGENT_SESSION_SLOT`; one debit, one record; no clearance is written; after the proof the clearance is written and a new start is admitted | H27, H1, E27, E30, E28 |
| S30-8 | A renew 100 blocks after the start with a lease end 144 above the tip; a renew that states the standing lease end; a renew at a tip that has reached `E` | Admitted; `AGENT_SESSION_SPAN`; `AGENT_SESSION_ENDED` with the end written | H3, H9 |
| S30-9 | The channel key of a recipient by name is replaced under the same owner; then a renew under the new key. Control: the key is removed | The state stays `session held` and the renew is admitted. With the key removed: suspended, `REQUEST_AUTH` | H25, H18 |
| S30-10 | The issuer spends the seal of the parent of `G`; C validates the spend in its mempool while its observation is not healthy. A session under another grant runs | The closure is written, the verdict is delivered at once, the session ends, and a later renew refuses as `GRANT_CLOSED`: the closure is met before the session is looked up. The other session is untouched | H12 |
| S30-11 | The same spend at a non-witness | Suspended, `GRANT_SEAL`; ended at `E` | H13, S9 |
| S30-12 | The tip does not move for 3600 seconds; then a new tip | At the next scheduled verdict C delivers `suspended` with `TIP_AGE`; nothing ends. A sound verdict at the new tip lifts it | H8, S7 |
| S30-13 | A reorganisation lowers `H` below `not_before_height`; later the tip is inside the window again | Suspended; then `session held` | H11, S7 |
| S30-14 | A reorganisation lowers `H` below `E` after the end was written | The session stays ended | E7 |
| S30-15 | The stop coin of row 3 is spent; a session under a child of row 4 runs | The session of row 3 ends; that of row 4 stays | H16 |
| S30-16 | Two documents of one row with a row level of 1 and two recipients: a start under each | The first is admitted; the second refuses as `AGENT_SESSION_LEVEL_ROW` | N6, H6 |
| S30-17 | A stop for a session that is `session held`; for the same session again; for an identifier that the journal lacks; for a suspended session whose session path result is not sound | Ended; `AGENT_SESSION_ENDED`; `AGENT_SESSION_UNKNOWN`; the code of the session path result, and the session stays suspended | H4, E4, N4, S4 |
| S30-18 | The landlord's list changes and C lacks its octets; a renew presents a list without the entry; a renew presents a later list, of a higher `seq`, that holds the same entry again | Suspended; the renew refuses as `CLASS_HOLDER`, the mark is written and the session stays suspended; the mark is lifted, the renew is admitted and the state is `session held` | H15, S14, S3 |
| S30-19 | The session journal is lost while a process runs; it is started anew; a start for a slot before its clearance; the operator's clearance with the census; a start under the old grant; a start under a grant whose recent block is above the boundary | `JOURNAL_LOST`; the recovery entry counts as the end; `AGENT_SESSION_SLOT`; the slot is `none`; `OWN_LIMIT_OVER`; admitted | H23, Q24, Q1, Q34, N1 |
| S30-20 | A second replica of D does not hold the token of the session journal | It admits nothing: `JOURNAL_FENCED` | D1 |
| S30-21 | A child whose `actions` hold the start leaf outside `delegate.actions` of its parent | `CHILD_ACTIONS_WIDER` (proposed for v4). With the leaf in the parent's list it is admitted | C5 |
| S30-22 | A halt command of the owner for a session that is `session held`; the same command again; another halt command for the ended session | Ended; `REPLAY` of LIP-0029; `AGENT_SESSION_ENDED` | H19, E19 |
| S30-23 | A start with a span of 1. A block arrives after the write and before the start order, and does not reach `E`. Control: no block arrives | The last check finds another tip and **refuses**: `OBSERVATION_VOID`; no end is written, the compensating entry annuls the start record and releases its debit and its count, the slot is `none`, and no process starts. A later valid start under the same grant is admitted and debits one start. In the control the process starts and one start stands debited | H29, N1 |
| S30-24 | A child of a class row. The seal of the recipient's entry is spent in the mempool after the verdict and before the start order. Control: no spend appears | The last check reads the seal again: `HOLDER_REVOKED`; the closure is written, the session ends by that closure and not by the check, its never-ordered start is compensated, and the clearance "no start was ordered" frees the slot; no process starts. In the control the process starts | H29, H17 |
| S30-25 | C stops answering while a session is `session held`. Control: C answers | After 120 seconds D holds no current verdict: suspended; D answers "no session held". In the control the state stays `session held` | H8 |
| S30-26 | A restart signed by the key holder of `A` at a tip that has reached `E`, inside every grant window | The end is written; `AGENT_SESSION_ENDED`; no debit | H9, E2 |
| S30-27 | A restart for a session that is `session held` and whose process is down; the station proves the account empty. Control: the proof fails | A new run with a fresh origin; one start debited. In the control: `AGENT_SESSION_RUN_OPEN`, the debit stays, no run is created, and a second restart refuses the same | H2, H35 |
| S30-28 | A restart by the session service under a restart grant after a host reboot; the same after the issuer spent the seal of the restart grant | Admitted, one start debited in the account of the restart grant; then `GRANT_CLOSED`, and the session itself stays `session held` | H2 |
| S30-29 | A restart after the slot table moved the recipient to another generation of the same account | `AGENT_SESSION_SLOT` | AS5.5 |
| S30-30 | D crashes after the store write of a start and before `advance`. Control: no crash | On its restart the check gives pending: D completes the write, writes run 1 "not ordered" with the compensating entry and the annulment, and starts nothing; the slot is `none`. The same request again: `AGENT_SESSION_REPLAY`; a new valid start is admitted. In the control the process starts | H31 |
| S30-31 | A closure journal is lost after C wrote a closure and before D wrote the end; the spend has left the mempool; the journal is started anew | The session is suspended while the journal is lost, and is ended by the first verdict that carries the new identity. It never returns to `session held` | H22, H32 |
| S30-32 | A request whose Subject names another recipient; a child whose genesis differs from its parent's | `REQUEST_SUBJECT`; `CHILD_GENESIS`. With the right values each is admitted | C4, C5 |
| S30-33 | **B1.** A session is `session held`. Its admitted renew request is sent again after the landlord's list changed, and the fresh verdict on the resent request, taken alone, would be `suspended` with `LIST_UNKNOWN`. Then a renew that names the same session under the second document of its row, whose own path is closed, is sent. Control: the original renew sent once, and a new renew under the session's own path presenting the list | The resent renew: `AGENT_SESSION_REPLAY`, and the session stays `session held` on its current verdict; nothing is written. The renew under the second document: `AGENT_SESSION_UNKNOWN` at the third gate, and the session does not end; the closure reaches no session of this path. In the control the renew is admitted once, and the new renew takes the list and moves `E` | H5, H6, S3; convention 3; section 5.3 |
| S30-34 | **B2.** The session journal is started anew; its lost identity held a start order at position 4990 that was never executed. The slot is cleared in the new journal at position 3 and a new session is admitted. The old order then reaches the starter. Control: the new session's own order, carrying the new identity, reaches the starter | The starter refuses the old order: its identity is fenced, at any position, and no process starts beside the new session. In the control the process starts | Q24, Q34, N1; AS1.4; section 5.6, item 8 |
| S30-35 | **B3.** Run 1 was ordered and its outcome is unknown (event 27) after a host reboot. A restart is requested. Control: the station proves run 1 not started (event 30), and the restart is requested again | The restart refuses before any write and any debit: `AGENT_SESSION_RUN_OPEN`; no run 2 is created and no order is sent. In the control the restart is admitted: admission, last check, the transition with "run 1: ended" and its fence, run 2 created and ordered; a late order of run 1 then meets the fence at the starter | H27, H2; AS5.6, AS5.7 |
| S30-36 | **B4.** D crashes after `advance` accepted the write of a start and before it sent any order. The starter proves by the pair of that entry that it received no order and fences the pair. Variants: the same crash after the admission entry of a restart, and after its transition entry. Controls: no crash in each; and the starter cannot prove that it received no order | Recovery sends no order. Start: run 1 "not ordered", compensated and annulled, the slot `none`, and a new valid start is admitted. Restart after its admission: "restart of run k: not ordered", compensated, run k untouched. Restart after its transition: run k+1 "not ordered", compensated, the end and fence of run k stand, and a later admitted restart creates run k+2. Without the starter's proof the run is "outcome unknown" (H27) and nothing is ordered or cleared. In the controls with no crash each process starts once | H36, S36, E36; D12 |
| S30-37 | **B5.** A witness validates the issuer's spend of a link in its mempool; the closure write fails; C crashes and restarts, and its store and outside record agree because nothing was written; the spend is then evicted. Control: the closure write succeeds before the crash | The journal is lost for C although the check gives intact: its lost-mark stands across the restart, the session is `suspended` with `JOURNAL_LOST` and never `session held` again on the evicted spend; the admission for which the closure was due refused with `GRANT_CLOSED`. After a recorded start anew of that journal the session ends under event 32. In the control the closure stands, C delivers `ended` at once, and D writes the end before the restart | H22, H32; AS2.3, AS2.6 |
| S30-38 | **B6.** While the session journal is lost: the owner halts session `S` (its command passes steps 1 to 12 at C and meets `JOURNAL_LOST` at D), the operator records an end attempt for a second session, the tip on the pinned chain reaches `E` of a third, and C writes a closure for a fourth. The same halt command is sent again during the loss. The journal is then restored intact. Control: a fifth session with no due end | The resent halt is `REPLAY` at C during the loss and is not how the halt is applied. At the restore D writes the restore entry and, before any session leaves `quarantined`, the four ends from the replay: the closure and the height from the verdicts, the halt from the halt record (with its halt mark, so a later new start under that grant for that recipient refuses), the operator end from its record; a host restart grant brings none of the four back. In the control the fifth session leaves `quarantined` as `suspended` and is `session held` on its next sound verdict | Q33, Q19, Q21; section 5.6, item 7 |
| S30-39 | **F1.** The worked restart of section 5.2: a reboot, a restart under `G_r` (starts 10, 3 debited in its own account) for a session whose path is `P` to `G`, where `G` is a child of a class row, then the next path verdict for the session after the restart. Variants: the seal of `G_r` spent; the session path closed | Admitted restart: the own account of `G_r` goes 3 to 4, no account of `G` is debited, the state moves only by the session path result of `P` to `G`, and the later verdict uses the octets and the channel of `P` to `G` and nothing that the restart presented. With the seal of `G_r` spent: `GRANT_CLOSED`, no debit, the session stays `session held` on its own path. With the session path closed: the end is written and the restart refuses with the closure's code, no debit. The admitted restart is the control of both variants | H2; AS2.1, AS5.6, AS5.12 |
| S30-40 | **F2.** A session's checker has a failed clock and a lost closure journal, so Part P of AS5.1 gives `suspended`; its reading node, which gives the pinned genesis, then validates a block on its active chain at `E`. Variants: the only block at `E` that any node shows is on another chain; one arriving block both moves the tip at D11 and reaches `E` after the write of a start | The verdict is `ended` by height with that block's hash and height although the observation is not healthy, and D writes the end. On another chain: no end; the session stays `suspended` until a block of the pinned chain at `E` is shown, which then ends it (the control). At D11 the ended finding is reported, the end is written with the cause "height" and not `OBSERVATION_VOID`, and the never-ordered start is compensated | H9, S9, H22; AS5.1 Part H; section 5.1, L |
| S30-41 | *(a)* C gives a `sound` verdict and an `ended` verdict for one path inside one second; a third verdict was computed 119 seconds before D receives it and a fourth 121 seconds before. Control: a verdict received inside both bounds | The `ended` verdict has the greater sequence and is accepted and acted on in the same second; it is never dropped for its second. The third verdict is current on receipt for the remainder of its bound; the fourth is never current. In the control the session is `session held` | AS2.1 (a), AS2.2, AS2.5 |
| S30-42 | *(c)* The owner halts a session; its slot is cleared. A new start under the same grant for the same recipient; a new start under a new grant for the same recipient. Control: a start under the same grant before any halt | Ended, with the halt mark written in the same entry. Under the same grant: `AGENT_SESSION_HALTED` at D5.1 and again inside the write, for as long as the mark stands. Under the new grant: admitted, because the mark is on the pair that D can see; whether a halt should reach it is Q16. In the control the start is admitted | H19, N1; AS5.14 |
| S30-43 | C never answers the ask for the verdict of a start. Control: C answers sound | `AGENT_SESSION_NO_VERDICT` after the answer bound; nothing is written and no state moves. In the control the start is admitted | N8; AS2.4 |
| S30-K1 | A known limit. The issuer spends the seal, and the transaction has not reached the node of C | The state stays `session held` until the node shows the spend. Nothing bounds that time (LIP-0008 section 5.3) | H12 |
| S30-K2 | A known limit. The node receives no block | Suspended after the cutoff, and without an end in time (Q8 (b)) | S8 |
| S30-K3 | A known limit. A closure journal is started anew, and a spend that it had recorded is no longer in the view of the node | The sessions of H32 have ended. A new start under that grant is admitted by the newcomer, as the base has it | N32 |

## Sources

No service, no key holder and no node was run for this draft.

| Statement | Source |
| --- | --- |
| The members of a grant, the limit key, the pools, the pipeline, the rule map | LIP-0020 section 11, W11.2 to W11.4, W11.8 to W11.11 |
| The order of an admission, the executor, the budget, the replicas, the operator's ceilings, the contract mirror | LIP-0008 sections 2 and 4 |
| The closure of a spent seal; a verifier whose closure journal is lost | LIP-0008 section 5.1; J6.9 |
| The window, the invocation with its Subject, the proof path, the leaves, the time terms | LIP-0008 sections 7.1, 12.1, 12.2, 12.3, 12.5 |
| The seal of a v4 grant and its codes | LIP-0008 section 11.4, SB1 to SB3 |
| What a proposal for a leaf and for a limit kind states | LIP-0018 sections 2 and 3 |
| The observation, the recheck before an effect, the classes and their cutoffs, the codes | LIP-0022 sections 1 to 3 and 6 |
| The order of one write, the four outcomes of the continuity check, a lost journal, starting anew, the codes | LIP-0025 sections 3, 4, 5, 7 and 8 |
| Rows, the fit of a child, the coin, the accounts, the class checks | LIP-0026 sections 2, 3, 5, 6 and 9 |
| The stop coin of a row | LIP-0027 sections 2 and 3 |
| The list of a landlord's agents, the entry, the take of a list, the removal mark | LIP-0010 section 10 |
| The gate of the key holder | LIP-0013 section 3.6, J7.1 to J7.8 |
| The signer of a child, the reservation ledger, the attestation | LIP-0014 sections 8 and 11.1, J4.1, J4.4 (a) to (g) |
| The session for a client that cannot sign | LIP-0028 |
| The owner's command and its admission | LIP-0029 sections 1, 2, 6, 8 and 11 |
| The agreed configuration | LIP-0017 section 8 |
| The steps of a v4 child and of a request under it, with their order; the registries of actions and limit kinds. Cited only for the orders O-1 to O-6 | LIP-0014 section 8.4, rows F1 to F24, A1 and E0 to E3 with the pairs Q1 to Q27 and the rules T6 to T10, and LIP-0020 W11.14, as release 0.1.55 has them. They are not in the base of this branch |
| The construction of an issuance anchor and its codes | LIP-0023 sections 2 to 7; LIP-0020 W9.4 |

## Alternatives

- **A grant checker inside the dispatching service.** One service and one
  journal, and the atomic step of LIP-0028 T4.6 as it stands. Rejected: the
  dispatching service would need a chain view, an observation and a closure
  journal of its own, a second copy of what stands behind the message
  origin, and two closure journals on one host can disagree about one seal.
- **The life of a process in this LIP.** Rejected by the narrowing: those
  are facts of one host, and the grant decides none of them.
- **A restart without a request.** The dispatching service starts the
  process again on its own while the state is `session held`. Rejected by the
  owner's decision of 2026-11-16: no debit can be made without a request
  identity (LIP-0026 R5.7), so nothing bounds a loop of restarts.
- **A restart that resumes the earlier run.** Rejected: the key holder's
  record of a run ends with its channel (LIP-0013 J7.4), and a run that is
  bound again after an unknown end leaves two processes for one record.
- **A closure journal that is started anew gives verdicts as a newcomer to
  sessions that it finds.** Rejected: a session whose closure was lost with
  the journal would be `session held` again.
- **A removal mark ends the session.** Rejected: the mark is liftable, and
  the cited text says that a change of the list does not end the child.
- **The lease in seconds,** as LIP-0028 has its window. Excluded by the
  owner's decision.
- **No lease.** A suspended session would then run to the end of its grant.
- **A new member of the grant** for the account, the configuration or the
  model. It would change the octets of `swarma-grant/4`.
- **One leaf for start and restart.** One leaf would have two lists of
  arguments, and a reader of the leaf could not select the list.
- **A level counted as an account.** An account is never lowered (LIP-0026
  R5.1), so it would be a second cap on starts and no level.

## Security consequences

- **A revocation is bounded in blocks and not in time.** An end needs a
  closure of a link at the grant checker, or a height. Every other refusal
  suspends, and a suspended authority ends at `E`, at most one span above
  the tip of its last admitted start or renewal. The height is taken from
  every block that the reading node validated on its active chain where it
  is on the pinned chain (AS5.1, Part H), so a failed clock, a failed
  comparison node or a lost closure journal does not keep a session past
  `E` while such blocks arrive; a block of another chain ends nothing.
  While the node receives no block no height is
  reached; whether a clock then ends a suspended session is Q8 (b). While
  the session journal is lost no end can be written at all: D hands the
  event to the station contract at once and answers "no session held", the
  stop of the processes and its bound are that contract's (section 7.2,
  rows 6 and 10), and the ends that fall due in the loss are written in the
  replay at a restore before any session leaves `quarantined` (section 5.6).
- **"Session held" cannot outlast its verdict.** A verdict is current for
  at most 120 seconds, the checker owes the next one at every tip, at every
  closure and every 60 seconds, and the dispatching service produces the
  suspension itself when none comes (AS2.4, AS2.5).
- **Between a closure and its delivery** the dispatching service may hold
  an older verdict for at most that bound. No process is started on it: the
  last check asks the checker at that moment, before the write and again
  before the effect (L). An answer "session held" is given only after a
  fresh ask (AS2.5).
- **A suspended session still runs.** Suspension takes the answer "session
  held" away and admits no restart. The process keeps its home and every
  credential that works without a signature (LIP-0013 J7.8).
- **An ended session runs until the station contract stops it.** The
  profile writes the end; the bound from that record to a stopped process
  is a need of that contract (section 7.2, row 6) and has no number today.
- **At a non-witness an unvalidated spend only suspends, and the
  suspension can lift** (AS1.6). Where the spend is evicted and the seal is
  shown unspent again before `E`, the session is `session held` again; the
  span bounds only the life that is left to it, because it still ends at
  `E`. A spent stop coin at a non-witness closes its row only where the
  spend is established as LIP-0027 H2.4 and H2.5 state and the closure is
  written, or falls due unwritten (event 22); only shown, it suspends. An
  issuer that grants to such a host chooses a small span.
- **No verifier that never saw a spend is bound by it** (S30-K1), and a
  closure whose spend has left the view is lost with its journal for new
  starts (S30-K3).
- **The executor is trusted for the end.** The set writes the end and has
  the process stopped. A host that does neither keeps an agent running; the
  other executors still make their own checks.
- **A restart grant makes the host a signer.** The session service signs
  restarts with its own key. It can start nothing that the checker would
  not admit: the chain is read for the restart grant and for the session's
  path, each restart debits the restart grant, and a spend of its seal
  stops the host. It cannot start a session, renew one or outlive `E`.
- **After a halt the owner's stop is final for the session, and under the
  same grant it is final at this executor.** The halt mark (section 5.8)
  refuses a new start that cites the halted session's grant for its
  recipient at the same executor while it stands, and nothing in `X` lifts
  it. It reaches no further than that pair, because that is what `X` can
  see: a new start under another grant is an ordinary start that the key
  holder signs for a run with an origin, and no part of `X` can observe
  that origin (LIP-0013 J7.7). Who may lift the mark, and whether a halt
  should reach beyond the one grant or bar the origin itself, is the
  owners' Q16, and this draft claims the halt final for the agent nowhere.
- **The executor is stricter than a fresh verifier in three places.** A
  path verdict takes no presentation (AS5.12); a session journal that was
  started anew charges every older grant as used; and a closure journal
  that was started anew ends the sessions that it could have closed. In
  each the set refuses where another verifier might admit, and never the
  reverse.

## Conformance impact

None on normative v0.1, none on Grant v3, and none on the octets of
`swarma-grant/4`. No conformance class and no vector is added. A
conformance claim under this profile would state whether the executor is a
witness (AS1.6), the interval of its mempool read (AS5.13), and its verdict
interval where it is below 60 seconds (AS2.4).

## Open questions

### Questions for the owners

These seven and no other. Each has its options, what each costs, and a
recommendation that decides nothing. The earlier Q1, Q5 and Q6 are closed
by the owner's decisions of 2026-11-16.

- **Q4. Effect or work.** (a) Effect: `X` is an effect service of LIP-0006
  section 7 and refuses a grant whose terms carry a text, and a run at
  level L0 gets no signature for a start (LIP-0029 O6.7 (a)). Cost: an
  orchestrator at L0 starts no worker. (b) Work. Cost: the start of a
  process on a host is bounded by the three limits alone and by no level.
  Until the answer the profile states no class, and the stricter class of
  LIP-0022 B3.5 holds. Recommendation: (b).
- **Q8 (b). Does a clock ever end a suspended session?** The question is
  left for one cause alone: the reading node receives no block. Every other
  cause ends at `E` by height. (a) No: cell S8 stays, and a session at a
  node without blocks is suspended without an end in time. (b) Yes: the
  dispatching service ends it when the age of the tip reaches a cutoff.
  Cost: the one place where a clock ends an authority, against the decision
  that time is counted in heights. LIP-0022 assigns its cutoffs to an
  action and not to the authority of a session, so the answer would have to state the
  number; at 3600 seconds it would be met without any outage, because in
  the sample that LIP-0022 section 3 cites the tip was older than 60
  minutes for 0.229 percent of the time, and every session of every host
  would then end and cost a start. Under (a) the same gaps only suspend,
  and the next tip lifts them. Recommendation: (a), with the bound stated
  as unbounded in time.
- **Q11. Does a session that an owner starts need a grant?** (a) Yes: cell
  N20. Cost: an owner starts nothing on a host for which no grant exists.
  (b) No. Cost: an authority without a window, a seal or a limit, which
  only a halt command and the operator end; this draft has no rows for it,
  and the table would need them before (b) can be built. Recommendation:
  (a); "The chain rules apply inside one host too" (LIP-0029).
- **Q13. The level of a halt command.** Open in LIP-0029 ("the level of a
  stop and of resumption"). (a) The lowest level that the policy admits.
  Cost: every device of the owner can end every session. (b) The level of
  the command that started the run, or above. Cost: a lost device of that
  level delays a stop. Recommendation: (a): a halt takes authority away.
- **Q14. How does a later instruction reach a running station?** Section
  7.1 keeps LIP-0013 J7.6 as it is, and the station contract has a
  long-lived station receive later instructions in its running process
  (its rule K5). Both cannot hold. (a) An instruction under another grant
  enters the run as an instruction, where that grant names the same
  recipient and an action that the session permits. Cost: an amendment of
  LIP-0013 J7.6, and work in one run under several grants, so that a
  revocation and a debit no longer follow one grant. (b) Every instruction
  opens its own run inside the same station: one account and one home,
  several runs over time, each bound to the grant that it cites. Cost: the
  station contract gains a run level under `running`, with a start, an end
  and an unknown outcome of a run, and the dispatching service and the key
  holder each gain one unit of work. (c) Instructions to a running station
  are data only, and nothing in a message carries authority. Cost: the
  station decides what to do under the authority that it holds, and no
  later work is bound to a grant of its own. Recommendation: (b). This
  draft decides nothing.
- **Q15. May the host restart a session alone under a restart grant?**
  Section 5.2 and AS3.4. (a) Yes, as proposed: a grant gives the restart
  leaf to the session service of the host, with a starts limit over its
  window. Cost: the host holds a signing key of its own, and an issuer
  signs a second grant for each host. (b) No: only the party that started
  signs a restart. Cost: a host cannot recover a session after a reboot or
  a crash while the key holder of the agent is down or an origin there no
  longer lists the grant; the agent stays down until that party acts.
  Recommendation: (a).
- **Q16. Who lifts a halt mark, and how far does a halt reach?** Section
  5.8. Until this is answered a halt mark cannot be lifted at all, so under
  the same grant the halt is final at that executor. (a) Only the owner
  lifts it, by a signed owner command of a class that the registry does
  not have today, at the level of the halt or above (with Q13). Cost: an
  agent that was halted in error gets a new grant from its issuer, or waits
  for that command class. (b) The owner or the issuer of the grant lifts
  it, by a signed request under that grant. Cost: a party other than the
  owner can undo the owner's stop at this executor. (c) The operator lifts
  it by a clearance. Cost: the host can undo the owner's stop, and the mark
  binds nobody that runs the host. Also to decide here, and not in another
  text first: whether a halt reaches beyond the one grant that D can see —
  to a new start under another grant for the same recipient, or to the
  origin at the key holder under which the halted session ran, which no
  part of `X` can observe (LIP-0013 J7.7). (d) No: the mark stays on the
  pair of grant and recipient at one executor, as AS5.14 has it. Cost: the
  same agent under a new grant starts again at once. (e) Yes. Cost: the
  halt must then be carried where those facts live, and an answer here
  names that text; until it is carried, this profile still cannot build
  it. Recommendation: (a) with (d) until a wider stop is built, with the
  cost of (d) stated, as section 5.8 and "Security consequences" do.

### Open, and not the owners'

| Item | The question | Who decides |
| --- | --- | --- |
| P1 | **The configuration.** LIP-0017 section 8 has a contract "under which the platform starts an agent in an agreed configuration" carry the hash of one manifest, as a rule of the contract's profile; no profile has that member today. Two things are open: the preimage of the hash over what a host starts, and how the contract profile requires it. This profile decides neither, gives the start request no configuration argument, and has the record keep what was started (D10). **Consequence:** one hash for each contract, with one contract along a path, makes every worker under one orchestrator run the same configuration. **Remedy:** a mapping in the contract profile from a row or a recipient to a hash, and no member of the grant | The LIP that defines the contract profile of a hosted agent (LIP-0017 section 8; LIP-0018 section 1) |
| O-1 to O-6 | The six orders of section 5.1, as that section now has them: closed for a parent and a child where version 0.1.55 (LIP-0014 section 8.4) orders them, and open where it does not: a root alone and a longer path (O-1, O-2), the blocs of the seal and the issuance and the classification of a validated spend against them (O-1, its open points O1 and O6), the code of a closure journal that cannot be read (O-2, its O5), the order and the codes of the checks of an invocation and of an unauthenticated request and the Subject of a request (O-3, its O2 and O3), and a finding in a part of a parent that the child's ordinal does not select (O-6, its O7) | For O-6, the owner's decision on proposal Q1 of LIP-0026, as version 0.1.55 names it; for the rest, the editors of LIP-0014 section 8.4 and of the texts that rows O-1 to O-3 name. O-4 and O-5 are closed |
| N1 | The members of the invocation and of the receipt; the journal key of a request identity | LIP-0020 |
| N2 | Acceptance of the new codes of section 6, list 2, or their replacement by codes that have landed. Version 0.1.55 on main proposes codes for a child within its parent and for a contract (LIP-0020 W11.11; LIP-0014 section 8.4, F5, F6, F8, F16, F18): its `SUBJECT_MISMATCH` reports the `genesis` of a child and is no replacement for `REQUEST_SUBJECT`, which reports the Subject of a request, so that part of the question is answered by reading it; whether this draft then spends its codes in the place of `CHILD_GENESIS` and of its contract codes is decided when the draft lands on a base that carries that version, and no cell spends both meanwhile | LIP-0020 section 11 |
| N3 | The alphabet of a segment of a leaf and of a kind text | LIP-0008 section 12.3 |
| N4 | The amendment of the row `slot.station` | LIP-0007 section 1 |
| N5 | Whether the readings of AS3.2 and AS5.4 stand: that the key holder's run precedes its process, that an admitted restart request is an origin, and how the origin of the session service is named | LIP-0013 section 3.6 |
| N6 | The entries of the session journal and of the closure journals on the form of LIP-0025, among them the restore entry, the run fence, the compensating entry and the halt mark; the form of the durable lost-mark of AS2.6 and of the sequence counter of AS2.1 (a); the octets of the verdict, of a pair of identity and position and of a start order; and the block boundary of section 5.6 after a reorganisation | LIP-0025 |
| N7 | Withdrawn as an item of this table: whether an origin under which a halted session ran may sign a new start, and how far a halt reaches, is the owners' Q16 above, and is no longer filed as a request to the editors of LIP-0013 or LIP-0029. What those texts would have to carry follows the owners' answer | The owners (Q16) |
| N8 | What a closure journal that is started anew charges for a new admission (S30-K3) | LIP-0008 J6.9; LIP-0025 section 7 |
| N9 | **The three bounds in seconds, as numbers.** The 60 seconds of the delivery duty (AS2.4), the 120 seconds of the currency of a verdict (AS2.5) and the 60 seconds in which C answers the last check and every ask for a verdict (section 5.1, AS2.4) are this draft's own numbers, marked **P** where they stand. No cited text gives any of them: LIP-0022 "fixes no interval between observations" and assigns its clock cutoffs to an action at an admission (LIP-0008 section 6), not to an authority that lasts. Their composition is decided in this draft and is no part of the question: the first two only suspend, the third only refuses (section 5.1), the 120 seconds carry a stated margin of 60 over the duty of 60 (AS2.5), and currency runs from the observation's own time and from D's receipt both. Open is the size of each number: too small, and ordinary computation, transit and clock skew suspend sound sessions; too large, and "session held" outlives the fact that ended it by that much, and a start waits that long for a silent checker | Both owners, on accepting this profile; LIP-0022 only if it were to fix an interval of its own, which it does not |
