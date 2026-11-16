# LIP-0030: Action profile no. 1, an agent session on a host

- **Status:** Draft. Nothing in this file is in force by its own word. Every
  rule is marked as restating a cited text, as proposed here, or as open.
- **Created:** 2026-11-16
- **Affects:** what a v4 grant lets an executor do when the executor is the
  service set of a host that starts the run of an agent: the action texts,
  the limit kinds, what the executor checks at a start, what it checks while
  the authority is held, and which events end or suspend the authority
- **Builds on:** LIP-0006 section 7, LIP-0007 section 1, LIP-0008 sections 2,
  2.1, 3.1, 4, 5, 5.1, 5.2, 7.1, 11.4 and 12, LIP-0010 section 10, LIP-0013
  section 3.6, LIP-0014 sections 8 and 11.1, LIP-0017 section 8, LIP-0018
  sections 2 and 3, LIP-0020 section 11, LIP-0022 sections 1 to 3 and 6,
  LIP-0025 sections 4, 5 and 7, LIP-0026 sections 2, 3 and 5, LIP-0027
  sections 2 and 3, LIP-0028 and LIP-0029 sections 1, 2, 6, 8 and 11
- **Deciders:** both owners

## Summary

A grant of version 4 names an executor, a recipient, a list of action texts
and a list of limits (LIP-0020 W11.2 to W11.4). No profile defines an action
text or a limit kind yet: "Which texts name an action is for the action
registry (LIP-0007; LIP-0008 section 12.3), which is open" (W11.4). Until a
profile defines an action, a v4 grant has no effect at an executor.

This draft proposes the first such profile. It defines the **authority** of
an agent session and not the life of a process. It states:

1. the executor as a set of three services, and which part writes which
   journal (section 2);
2. four action leaves and three limit kinds, each with its full text and the
   registry section that it would enter (section 3);
3. one table of the four states of the authority against every event. Each
   cell has one outcome: the next state, who acts, the durable record that is
   written before the effect, and the refusal code (section 4);
4. the rules that hang off single cells of that table: the checks of a start,
   of a restart, of a renewal and of a stop, the verdict while the authority
   is held, and a journal that is started anew (section 5);
5. the refusal codes, among them those that the base lacks (section 6).

The states of a process (starting, running, down, the restart of a service
or of its machine, the home, retirement) belong to the station contract of
the host. This draft names that contract once (AS1.4) and restates nothing
of it.

The draft adds no member to the grant, changes no other LIP and defines no
octets: the requests are signed invocations, and the invocation has no
members yet (LIP-0020 section 3, type `swarma-invocation/1`). It has no
vectors. Nothing of it is implemented.

## What is decided and what is proposed

**Direction of one owner.** One owner gave this direction on 2026-11-16, as
it was relayed to the author of this draft; no record in `decisions/` holds
it yet, and the co-author's answer is not known:

1. The default agent is long-lived. Each runs in an OS account of its own,
   with an identity of its own and with keys that services hold. The run for
   one task is a special case.
2. A v4 grant has no clock member. The time of a session and of its renewal
   is counted in block heights.

Point 2 agrees with text that the specification already holds: the window of
a v4 grant is a pair of heights (LIP-0008 section 7.1; LIP-0020 W11.2).
Point 1 is the reason for this profile and decides none of its rules.

**Marks.** Every rule carries one of three marks. A mark that restates also
carries the state of its source.

| Mark | Meaning |
| --- | --- |
| **R** | Restates the cited text and adds nothing. The tag after it is the state of that text: **[F]** in force on its own terms; **[C]** carried or decided by one owner, with the co-author's agreement pending; **[D]** a proposal of a Draft that neither owner has accepted |
| **P** | Proposed here. Neither owner has decided it |
| **O** | Open. The question and who decides it are in the section "Open questions" |

**States of the cited texts,** as each states it of itself in the base of
this draft (version 0.1.54):

| Text | Tag | Its own statement |
| --- | --- | --- |
| LIP-0008 sections 2, 4, 5.1, 7.1, 12.1 to 12.5 | [F] | Decided text of that LIP. Its executor profile, its registry assignments and its proof encoding are open there |
| LIP-0008 section 5.2 (J6); LIP-0013 section 3.6 (J7); LIP-0014 J4 and section 11.1; LIP-0028 (J13); LIP-0029 | [C] | Decisions of one owner that await the co-author's agreement |
| LIP-0020 section 11 | [C] | Its carried decisions bind a reader of `swarma-grant/4` from version 0.1.53 under one owner's order; "Neither owner has reviewed the octets member by member, and no verifier implements them" |
| LIP-0010 section 10; LIP-0026 sections 2 and 3 (J1.2, J10, J12) | [C] | Carried by LIP-0020 section 11 on the same terms |
| LIP-0017 section 8; LIP-0022; LIP-0025; LIP-0026 section 5; LIP-0027 | [D] | Proposals of their drafts |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The authority of a session as a function of stated facts: the table of section 4 | Yes, as a model | The owners' answers to Q4, Q6, Q8 (b) and Q11 |
| The requests as octets | No | The members of the invocation and of the receipt (N1) |
| The limits as members of a grant | Yes for the three keys of section 3.3, as proposed texts | Acceptance of this LIP, which enters them into the registry |
| The grant checker's verdict | No | A run of the observation under LIP-0022, and the step table of the v4 admission that is in review (section 5.1) |
| The session journal | No | The entries of a service journal on the form of LIP-0025 |

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
`X`; section 2 says what `X` is.

### 1. Scope and terms

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS1.1 | An **agent session** is the authority under which `X` runs one agent in one slot on the strength of one admitted start request. It belongs to one final grant with its proof path, to one executor and to one slot, and none of the three changes. Its record is an entry of the session journal (section 2). It has no token and is no session of LIP-0028; this draft always writes "agent session" | **P**, in the words of LIP-0028 T1.2 [C] |
| AS1.2 | The authority of an agent session has one of four **states**. `none`: the session journal holds no record of it. `held`: the record has no end, and the dispatching service holds a sound verdict (section 5.5) for the newest tip that the grant checker reported, with `H < E`. `suspended`: the record has no end, and the dispatching service holds no such verdict; the verdict is unknown or refuses without a durable record. `ended`: the record has an end. An end is final. `suspended` is derived and is not written: a part that restarts holds no verdict, so every authority without an end is suspended until the next verdict | **P**. "An end is final" is LIP-0028 T5.4 [C] |
| AS1.3 | The **slot** of an agent session is one OS account of the host, identified by the user id under which it runs (the first form of LIP-0028 T6.1 [C]). A session **counts** from the write of its start until its **clearance**: the record of the dispatching service that the slot holds no process of that session. The proof behind a clearance is the station contract's | **P** |
| AS1.4 | The **station contract** is the agreement between the operator of a host and the parties that use it, with the host's signed policy. It owns the states of a process: starting, running, down, the restart of a service or of its machine, liveness, the home and its export, retirement, and every bound in clock time. It is out of this specification and is named here once | **P**, as a name only |
| AS1.5 | An executor under this profile reads seals on its own node, as a witness (LIP-0008 section 5.1 [F]), or its conformance claim states that it is a non-witness. At a non-witness every spend of a seal is event 13 of section 4 and never event 12: a revocation there only suspends, and the span of section 3.3 is the delay of every revocation | **P**, after LIP-0010 H50 [C], which has a non-witness record no enforcement closure |

### 2. The executor is a service set

`X` is the service set of one host under one executor name and key
(LIP-0020 W11.4 [C]). It has three parts. (**P**; a grant checker inside the
dispatching service is the rejected alternative, see "Alternatives".)

| Part | Holds | Writes | Does |
| --- | --- | --- | --- |
| The **grant checker**, behind the message origin | The chain view of its own node, the observation, the watch of the mempool, and the executor key | The **closure journal**: the closures of seals and of issuers' names (LIP-0008 sections 5.1, 5.2), rows closed for cause (LIP-0027 section 3), holder closures and removal marks (LIP-0010 section 10) | Reads every signed request and every grant, makes every check that needs a document or the chain, and gives the **verdict** (section 5.5): for a request, and at every new tip for every proof path that the dispatching service names |
| The **dispatching service** | The slot table of the host and the configuration that it started | The **session journal**: the session records, the identities of admitted requests, the accounts of the starts kind, the ends, the clearances | Consumes the verdict, makes the checks that need its own journal, writes, and only then performs the effect. It verifies no grant and reads no chain |
| The **key holder** of the recipient | The request key of `A`, the record of each run and its origin, and the table of permissions (LIP-0013 J7.1, J7.2 [C]) | Its own records under LIP-0013 section 3.6 | Binds the run to its origin and signs the requests of sections 3.1 and 3.2. Neither other part can observe its gate (J7.7 [C]) |

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS2.1 | A verdict states the tip hash and `H` of its observation, the identity, the command and the arguments of the request, the ordered proof identifiers, the mode and the channel under which the request was authenticated, the entry of the recipient for a child of a class row, the limits of `G` and of its row, and the **position** of the closure journal at which it was given. The dispatching service takes no fact about a grant from any other source | **P**. "A gateway can deliver data but cannot substitute its prepared binding for that verification" (LIP-0008 section 5 [F]) holds for the set as a whole: the checker is the part that verifies |
| AS2.2 | The signed invocation is the object that reaches the grant checker. What the checker hands to the dispatching service is an internal form of the set and a matter of the station contract; it carries the content of AS2.1 and replaces nothing of the invocation | **P** |
| AS2.3 | The grant checker writes a closure into the closure journal before it gives any further verdict, and its next verdict for every proof path that holds the closed link is `closed`. For a validated issuer spend it writes the closure from the spending transaction itself, whether or not an observation is healthy at that moment | First sentence **R** LIP-0008 section 5.1 [F]: "MUST persist permanent closure before any further admission". Second sentence **P** |
| AS2.4 | The dispatching service answers that an authority is held only after the grant checker confirms, at that moment, that the closure journal holds no record for the proof path beyond the position of the verdict. After its own restart it asks a verdict for every authority without an end before it admits a request | **P**. With two journals this stands where LIP-0028 T4.6 [C] has one atomic step |
| AS2.5 | Replicas of a part share that part's one journal, and a replica that cannot reach it admits nothing and performs no effect | **R** LIP-0008 section 4 [F]: "Replicas acting as the same executor share one authoritative durable journal"; "If shared state or its serialization mechanism is unavailable, replicas admit no new effect" |

### 3. The actions and the limit kinds

#### 3.1. The grant members

No new member is needed (**R** LIP-0020 W11.2 [C]: "A grant carries nothing
beside these members").

| Member | Meaning under this profile | Mark |
| --- | --- | --- |
| `executor` | The service set `X` of one host. Only `X` holds an authority under `G` | **P** on W11.4 |
| `recipient` | `A`, the agent for which the session runs. A row fixes the recipient of its child (LIP-0026 R2.3 [C]), so a grant that named the asking party could not fix the worker | **P**; decided here by W11.3 and R2.3 |
| `actions` | The leaves of section 3.2 that the issuer allows. A leaf that the list lacks is a right that no issuer gave: commands "match exact leaf identifiers" (LIP-0008 section 12.3 [F]). A grant without the stop leaf has a recipient that cannot end its own session | **R** for the match; **P** for the consequence |
| `limits` | The three keys of section 3.3 | **P** |
| `not_before_height`, `not_after_height` | No authority is held outside the window of any link | **R** LIP-0008 sections 7.1 and 12.5 [F] for an admission; **P** for a held authority |
| `seal` | The stop of every session under the grant by its issuer. This profile admits a grant only where `seal.kind` is `revocable-only`; another kind refuses as `SEAL_PROFILE`, until a profile states what a use-branch spend does to a held authority | The code **R** LIP-0008 SB2 [F]; the restriction **P** |
| `contract` | Open: P1 of "Open questions". This profile reads no member of the contract except to mirror the limits (section 5.1, check C6) | **O** |
| `parent`, `ordinal` | The row fixes the executor, the recipient and the limits of a child (LIP-0026 R2.1 to R2.4 [C]) | **R** |

#### 3.2. The leaves

The leaves have the form that LIP-0018 section 3 requires: "in lowercase
segments separated by slashes" (**R**, with LIP-0008 section 12.3 [F]:
"Command names MUST use lowercase slash-separated segments"). That text
settles the separator. The alphabet of a segment is open there; every
segment here uses the letters `a` to `z` alone. No leaf holds the word
"session", which is the word of LIP-0028. Each leaf has one signer and one
list of arguments. (**P** for the exact texts.)

**Registry section that each would enter:** the action table of a service
type in LIP-0007 section 1, under the `swarma/` namespace of LIP-0008
section 12.3. They are the texts that LIP-0020 W11.4 expects in `actions`.

| Item (LIP-0018 section 3) | `swarma/station/agent/start` | `swarma/station/agent/restart` | `swarma/station/agent/renew` | `swarma/station/agent/stop` | `swarma/station/agent/halt` |
| --- | --- | --- | --- | --- | --- |
| What it asks | Start one agent session | Start the process of a held session again. The leaf exists only under branch (a) of Q6 (**O**) | Move the lease end to a higher height | End the session | End the session, by the owner |
| Signer | The key holder of `A`, under the recipient mode of `G` | The same | The same | The same | A device of the owner, as a signed owner command (LIP-0029 [C]). It is no request under `G`, needs no text in `actions` and is never listed there |
| Arguments, as logical fields | `lease_end_height` | `session` | `session`, `lease_end_height` | `session` | The typed fields of the command class: `session` |
| Subject (LIP-0008 section 12.1) | The executor of `G`, name and key, with the recipient of `G` | The same | The same | The same | Not an invocation |
| Service type | `slot.station`, the candidate of LIP-0007 section 1, whose row would say "recipient" where it says "renter". That is an amendment of LIP-0007 by a change of its own | The same | The same | The same | The class of an owner command is one exact leaf of the registry (LIP-0029 O2.1 [C]) |
| Effect or work | **O** (Q4) | **O** (Q4) | **O** (Q4) | **O** (Q4) | **O** (Q4) |
| Class under LIP-0022 B3.5 | Not stated here. "An action whose profile states no class has the first" (**R** B3.5 [D]) | The same | The same | The same | The level of the command is **O** (Q13) |
| Limits that bound it | All three of section 3.3; it consumes one unit of the starts kind and nothing else | One unit of the starts kind | The span kind | None | None |
| Receipt | **O** (N1) | **O** (N1) | **O** (N1) | **O** (N1) | LIP-0029 |

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS3.1 | The Subject is constant along the path: a child names the executor and the recipient of its row (LIP-0026 R2.2, R2.3 [C]), and a root grant names its own. The comparison of a child with its parent beyond the row has no v4 code in the base (LIP-0020 section 11.11) | **P**; the last sentence **R** |
| AS3.2 | **The signer of a start.** The key holder of `A` signs a start for a run that it has bound to an origin: the admitted instruction for `A`, or the owner's command (LIP-0013 J7.1 [C]). The run is the key holder's record and exists before any process: the launcher, which is the dispatching service, has the key holder create the run for that origin, and the start request is the first object that the key holder signs for it, on the channel of that run (J7.4), and only where every grant of the proof path is in the `use` list of that origin (J7.3 (a)). A resumed run "has the origin of the run it comes from" (J7.1), and "After a restart the launcher binds a run again from the stored origin record" (J7.4): those two sentences carry the signature of a restart and of a renewal while no process runs | **R** for the quoted sentences. **P** for the reading that the run precedes its process; it needs no new sentence in LIP-0013, and if its editors reject the reading the first start needs an amendment there (N5) |
| AS3.3 | Every field of a request is covered by its signature (**R** LIP-0008 section 12.1 [F]). A request states its lease end itself, and `X` shortens none and takes none from a default | **P** |

#### 3.3. The limit kinds

The key of a limit is "all of its members but the amount" (**R** LIP-0020
W11.4 [C]). The table gives each key in full. None has a `period`: a limit
with one of the three `kind` texts and another `resource`, another `unit` or
any `period` has a key that this profile does not define, and a grant that
states it refuses as `AGENT_SESSION_LIMIT_KEY` (**P**, after LIP-0018
section 2: a limit that is "missing, unknown or contradictory refuses").

**Registry section that each would enter:** the registry of limit kinds
that LIP-0020 W11.4 leaves to "the type profile of the kind". The texts are
**P**.

| Item (LIP-0018 section 2) | Starts | Level | Span |
| --- | --- | --- | --- |
| `kind` | `swarma/station/agent/starts` | `swarma/station/agent/level` | `swarma/station/agent/span` |
| `resource` | `swarma/station/agent` | `swarma/station/agent` | `swarma/station/agent` |
| `unit` and scale | `start`; whole starts | `session`; whole sessions | `block`; whole blocks |
| Bounds and rounding | 1 and above; nothing is rounded | 1 and above | 1 and above |
| What it is | An **account** of LIP-0026 R5.1 and R5.2 [D], for the whole window | A **level**: a check of this profile and no account. LIP-0026 section 5 does not apply to it | A **maximum of one request**: a check of this profile and no account |
| What a request consumes | A start, and a restart under Q6 (a), debits 1: the own account of `G`, and under a child also the row account (R5.3, R5.4). This is the only key that a request "consumes" in the sense of R5 | Nothing | Nothing |
| Arithmetic | Never lowered (R5.1, R5.8). The own account before the row account (R5.6) | Own: the number of sessions under `G` that count (AS1.3), after the start, is at most the amount. Row, under a child: the number of sessions that count under every document that is a child of the same parent and ordinal, after the start, is at most the amount that the row states for this key | `H < lease_end_height <= H + amount`, with the `H` of the verdict of that request. Under a child the child's own amount holds; R2.4 already holds it at or below the row's |
| Missing limit | The ceiling is 0 (R5.2): `OWN_LIMIT_OVER`, `ROW_CAP_OVER` | Refuses: "Missing required limits ... refuse the affected admission rather than becoming unlimited access" (LIP-0008 section 2 [F]). `AGENT_SESSION_LIMIT_MISSING` | The same |
| Reservation, uncertainty, denial | Reserved in the atomic write of cell N1. An unknown outcome keeps it (LIP-0008 section 2: "Uncertain effects retain their reservations until reconciled"). A refused request reserves nothing (R6.2) | Counted from the same write. Released by the clearance alone | Nothing is reserved |
| Replicas | One session journal (AS2.5) | The same | No state |
| Child and row (LIP-0026 R2.4 [C]) | A smaller amount is stricter | A smaller amount is stricter | A smaller amount is stricter |
| The pool of a parent (LIP-0020 W11.10, rule 6 [C]) | Bounds the sum of the row accounts | Bounds the sum of the row levels: the most sessions that can count at once under all rows | The rule still asks for the member and its sum. The number bounds nothing under this profile |
| Contract mirror | By executor, kind, resource, unit and amount (LIP-0008 section 2 [F]); check C6 | The same | The same |
| Kind of LIP-0008 section 2 | A new kind | "Runtime and concurrency" | "Runtime and concurrency", counted in blocks (section 2.1) |

One slot holds one session at a time (cell H1), and a recipient maps to one
slot, so under a grant that names one recipient at most one session counts,
whatever the level says. The level bounds a row whose documents name
several recipients.

No kind of this profile bounds a model or gateway budget. "A budget belongs
to that executor" (LIP-0008 section 4 [F]), and a grant has one executor
(LIP-0020 W11.4 [C]); section 7 says which unit owns that budget.

### 4. The table of the authority

Rows are the four states of AS1.2. Columns are the events, 28 of them, in
seven bands of four. A cell is named by the letter of its state and the
number of its event. Each cell gives the next state, who acts (C the grant
checker, D the dispatching service), the durable record that is written
before any effect, and the code. Every rule of this draft hangs off a cell,
and nothing outside this section and section 5 restates one. Each cell is
**P** unless it carries another mark; section 5 holds the marks of the
checks that a cell names.

For a start request, which names no session, the row is the state of the
newest session of the slot that the recipient maps to.

**Band 1: the requests.** A request is refused with the first check that
fails, and a refused request writes nothing and changes no state.

| State | 1. Start request | 2. Restart of the process (**O**, Q6) | 3. Renew request | 4. Stop request |
| --- | --- | --- | --- | --- |
| `none` | **N1.** Admitted where every check of section 5.1 passes: then `held` to the stated `E`. C gives the verdict; D writes one atomic entry (the session record, the debit of one start, the count of the level); only then D starts the process. Codes: section 5.1 | **N2.** Branch (a): `AGENT_SESSION_UNKNOWN`. Branch (b): cannot occur; D restarts only a session of its journal | **N3.** `AGENT_SESSION_UNKNOWN` | **N4.** `AGENT_SESSION_UNKNOWN` |
| `held` | **H1.** Refused: `AGENT_SESSION_SLOT`. A slot holds one session that counts, whoever asks and under whichever grant | **H2.** Stays `held`; `E` and the identifier do not change. Branch (a): a signed restart request, admitted by section 5.2; D writes the identity and the debit of one start. Branch (b): D acts without a request and writes a restart entry; nothing is debited. In both, D first stops the earlier process of the session or records the station contract's proof that none runs, and then starts | **H3.** Admitted where section 5.3 passes: stays `held`, to the new `E`. D writes the identity, the new `E` and the channel of this request in one atomic entry. Nothing is debited | **H4.** Admitted where section 5.4 passes: `ended`. D writes the end and the identity; then the process is stopped |
| `suspended` | **S1.** Refused: `AGENT_SESSION_SLOT` | **S2.** Branch (a): the request runs section 5.2 in full; a verdict that refuses gives its code and changes nothing, and a sound one makes the authority `held` and the cell is H2. Branch (b): D starts no process without a sound verdict; nothing is written | **S3.** The request runs section 5.3 in full. Where it passes: `held` to the new `E`. Where it refuses: its code, and the state stays | **S4.** The request runs section 5.4 in full. Where it passes: `ended`. Where it refuses: its code, and the state stays |
| `ended` | **E1.** Before the clearance (event 28): `AGENT_SESSION_SLOT`. After it: as N1; the new session has a new identifier | **E2.** Branch (a): `AGENT_SESSION_ENDED`. Branch (b): D starts nothing | **E3.** `AGENT_SESSION_ENDED` | **E4.** `AGENT_SESSION_ENDED`; nothing is written |

**Band 2.**

| State | 5. A duplicate or replayed request | 6. A request under a second document of the same row | 7. New tip, sound verdict | 8. No sound verdict: the tip cannot be read, the observation is not healthy, the tip is too old, or no verdict arrived |
| --- | --- | --- | --- | --- |
| `none` | **N5.** `AGENT_SESSION_REPLAY`: the identity is in the session journal, or the `iat` of the request is not later than the `fenced_at` of a recovery entry (section 5.6). Nothing is written | **N6.** A start: as N1. The second document has own accounts of its own and shares the row account and the row level with the first (**R** LIP-0026 section 5 [D]: "Two documents of one row have two own accounts and share the row account") | **N7.** No change: there is no authority | **N8.** No change. A start in this state refuses with the code of LIP-0022 [D] |
| `held` | **H5.** `AGENT_SESSION_REPLAY`. No change | **H6.** A start for the same slot: `AGENT_SESSION_SLOT`; for another slot: N1, where the shared row level decides (`AGENT_SESSION_LEVEL_ROW`). A restart, renew or stop that names this session with the other document: `AGENT_SESSION_UNKNOWN`. The authority does not change and never moves to the other document | **H7.** Stays `held`. D writes nothing | **H8.** `suspended`. Nothing is written; D answers "not held" (AS2.4) |
| `suspended` | **S5.** As H5 | **S6.** As H6 | **S7.** `held`. D writes nothing | **S8.** Stays `suspended`. **O** (Q8): under branch (a) no clock ends it; under branch (b) D writes an end when the age of the tip reaches the cutoff, and the state is `ended` |
| `ended` | **E5.** As H5 | **E6.** A start: as E1. A request that names this session with the other document: `AGENT_SESSION_UNKNOWN` | **E7.** No change. From the record of the end no request and no later chain reopens the session | **E8.** No change |

**Band 3.** A height is taken only from a healthy observation.

| State | 9. Lease end: `H >= E` | 10. Grant window end: `H` at or above the `not_after_height` of a link | 11. Tip below the opening of a window, after a reorganisation | 12. Seal of a link spent, and C validated the issuer's spend |
| --- | --- | --- | --- | --- |
| `none` | **N9.** Cannot occur: no lease exists | **N10.** No change. A start refuses: `GRANT_WINDOW`, and `PARENT_NOT_LIVE` for the parent of a child | **N11.** No change. A start refuses: `GRANT_WINDOW` | **N12.** No change in the session journal. C writes the closure (AS2.3). A later start refuses: `GRANT_CLOSED`, and `PARENT_NOT_LIVE` for the parent |
| `held` | **H9.** `ended`. D writes the end with the tip that showed it | **H10.** Cannot occur apart from H9: `E` is at most the `not_after_height` of every link (D7 of section 5.1), so the same tip has reached `E` | **H11.** `suspended`; nothing is written. `E` stands | **H12.** `ended`, for every session whose proof path holds the closed link, the root included. C writes the closure first; D writes the end before it admits anything |
| `suspended` | **S9.** `ended`, as H9 | **S10.** As H10 | **S11.** Stays `suspended` | **S12.** `ended`, as H12 |
| `ended` | **E9.** No change | **E10.** No change | **E11.** No change. A reorganisation undoes no end | **E12.** No change |

**Band 4.**

| State | 13. Seal of a link shown spent, and C validated no issuer's spend, or C is a non-witness | 14. The list of the landlord's agents changed, and an admission took the list and wrote the removal mark of the recipient's entry | 15. The list changed and C does not hold its octets, or the pin of the entry changed | 16. Row stop: the stop coin of the row is spent, and C wrote the closure |
| --- | --- | --- | --- | --- |
| `none` | **N13.** No change. A start refuses with the code of the seal check (LIP-0008 SB2, SB3; LIP-0024) | **N14.** No change. A start refuses: `CLASS_HOLDER` | **N15.** No change. A start refuses: `LIST_UNKNOWN` | **N16.** No change. A start refuses: `ROW_CLOSED_FOR_CAUSE` |
| `held` | **H13.** `suspended`; nothing is written (**R** LIP-0008 section 5.1 [F]: "refuses admission without asserting that an issuer revocation has been proved") | **H14.** `ended`. C wrote the mark; D writes the end | **H15.** `suspended`. The exit is a renew request that presents the list: its admission takes the list, and the cell is then S3 or event 14 | **H16.** `ended`, for every session whose final grant is a child of that row, under either document. A session under another row is untouched (**R** LIP-0027 H3.5 [D]) |
| `suspended` | **S13.** Stays `suspended` | **S14.** `ended` | **S15.** Stays `suspended` | **S16.** `ended` |
| `ended` | **E13.** No change | **E14.** No change | **E15.** No change | **E16.** No change |

A list that still holds the same entry, which is the same landlord, name,
key and seal (LIP-0010 H39 [C]), is no event (**R** section 10.4: a change
of the list "does not end the child, and it does not end its parent"). The
same name under another key or another seal is another entry, and for the
session it is event 14 or 15. Events 14 and 15 exist only for a child of a
class row.

**Band 5.**

| State | 17. Another durable closure of a link | 18. Another refusal that leaves no durable record | 19. Owner control: a halt command | 20. Owner control: a start by a command without a grant (**O**, Q11) |
| --- | --- | --- | --- | --- |
| `none` | **N17.** No change. A start refuses with the code of the closure | **N18.** No change. A start refuses with the code of the check | **N19.** `AGENT_SESSION_UNKNOWN` | **N20.** Branch (a): cannot occur; a command to `X` starts nothing, the command is the origin of a run at the key holder (LIP-0029 O6.5 [C]), and the start is event 1. Branch (b): an authority that no grant bounds; no column of bands 3 to 5 other than 19 applies to it |
| `held` | **H17.** `ended`. C wrote the closure; D writes the end | **H18.** `suspended`; nothing is written | **H19.** `ended`. C admits the command under LIP-0029 and gives its code where it refuses; D writes the end with the identifier of the command | **H20.** Branch (a): cannot occur. Branch (b): `AGENT_SESSION_SLOT` |
| `suspended` | **S17.** `ended` | **S18.** Stays `suspended` | **S19.** `ended`, as H19 | **S20.** As H20 |
| `ended` | **E17.** No change | **E18.** No change | **E19.** `AGENT_SESSION_ENDED` | **E20.** Branch (a): cannot occur. Branch (b): as E1 |

Event 17 is: the closure of the issuer's name where C holds it
(`ISSUER_NAME_CLOSED`, LIP-0008 sections 5.2 and 5.3 [C]); and the closure
of the recipient's entry after a validated spend of its seal
(`HOLDER_REVOKED`, LIP-0010 section 10.7 [C]). Event 18 is every other
refusal of a check of the path: the owner of the recipient's name is not the
signed owner key, which "refuses admission and records no closure" (LIP-0008
section 3.1 [F]); the channel key of the recipient was removed; the name
rule of the issuer refuses without a journaled closure; `HOLDER_SEAL_NOT_LIVE`
(LIP-0010 section 10.6 [C]); `ROW_STOP` and `ROW_COIN` (LIP-0027 H2.6 [D];
LIP-0026 R3.2 [C]); and a withdrawn attestation (`NOTARY_WITHDRAWN`, LIP-0014
section 8 [C]), which a successor attestation cures and which therefore ends
nothing. A later revocation of the device that signed an owner command is no
event of this table: LIP-0029 O8.4 speaks of envelopes.

**Band 6.**

| State | 21. The operator ends the session under the host's policy | 22. The closure journal is lost | 23. The session journal is lost | 24. The session journal is started anew |
| --- | --- | --- | --- | --- |
| `none` | **N21.** Cannot occur: there is nothing to end | **N22.** No change. C gives no verdict and refuses every request: `JOURNAL_LOST`, `JOURNAL_FENCED` (**R** LIP-0008 J6.9 [C]: it "MUST NOT admit before the journal is recovered or its owner has started it anew") | **N23.** D refuses every act that needs the journal: `JOURNAL_LOST`, `JOURNAL_FENCED` (**R** LIP-0025 M5.1 [D]) | **N24.** The new journal charges by section 5.6. A start for a slot without a clearance refuses: `AGENT_SESSION_SLOT`. After the clearance a start under a grant that the journal charges refuses: `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| `held` | **H21.** `ended`. D writes the end with the cause. Ending takes authority away and gives none | **H22.** `suspended`, as H8. A closure journal that is restored or started anew gives verdicts again, as a newcomer | **H23.** The state cannot be read. D ends nothing, writes nothing, starts and restarts nothing, and answers "not held". The loss proves nothing about the session: "It never takes a missing entry as a sign that nothing happened" (**R** M5.1). A restored journal (M5.2) gives the recorded state back, suspended until the next verdict | **H24.** The new journal holds no record of the session and asserts nothing about it: neither that it is held nor that it ended. A request that names it refuses, `AGENT_SESSION_REPLAY` or `AGENT_SESSION_UNKNOWN` (section 5.6). Its slot is unusable until a clearance |
| `suspended` | **S21.** `ended` | **S22.** Stays `suspended` | **S23.** As H23 | **S24.** As H24 |
| `ended` | **E21.** No change | **E22.** No change | **E23.** As H23 | **E24.** As H24 |

**Band 7.**

| State | 25. The channel key of a recipient by name is replaced under the same owner | 26. The pinned key of `X` no longer equals `executor.key` of `G` | 27. The outcome of a process start is unknown, or the start failed | 28. Clearance: D records that the slot holds no process of the session |
| --- | --- | --- | --- | --- |
| `none` | **N25.** No change | **N26.** No change. A start refuses: `GRANT_EXECUTOR` | **N27.** Cannot occur: a process is started only after the write that makes the authority `held` | **N28.** Cannot occur: no session |
| `held` | **H25.** Stays `held` (**R** LIP-0008 section 4, step 2 [F]: "Same-owner grantee rotation/renewal keeps a grant by name"). The next request is authenticated under the new key | **H26.** `suspended`; nothing is written | **H27.** Stays `held`. D writes an entry "outcome unknown". The debit and the count stay. D does not start another process for the record or in the slot, does not release the slot, and does not take the attempt as absent. The exits are H2, H4, H19 and H21 | **H28.** Cannot occur: D records a clearance only for a session that has ended |
| `suspended` | **S25.** No change: the replacement is no cause of a suspension and lifts none | **S26.** Stays `suspended` | **S27.** As H27 | **S28.** As H28 |
| `ended` | **E25.** No change | **E26.** No change | **E27.** Stays `ended`. The slot stays uncleared until event 28 | **E28.** Stays `ended`. D writes the clearance. The slot is free, and the session no longer counts for the level |

### 5. The rules that hang off single cells

#### 5.1. Cell N1: the checks of a start

The grant checker makes the checks C1 to C8 and gives the verdict. The
dispatching service then makes D1 to D11 in this order (**P**).

The order of C1 to C8 is not this profile's. The profile's checks follow
the child and row checks of the step table of the v4 admission that is in
review on another branch, once it lands. Until then each check stands where
its own cited text puts it, and the table marks **R** only an order that is
the cited text's own.

| # | Check of the grant checker | Order that the cited text states | Code |
| --- | --- | --- | --- |
| C1 | The request and every grant of the path are read as signed objects: the pipeline of LIP-0020 W9.1, with W11.8 to W11.10 for a grant | These are rules of the signed object and stand before the observation (**P**: LIP-0022 B6.1 puts its codes "before every rule of a grant", which this draft reads as every rule that needs a chain) | The code of the pipeline. **O** for the invocation (N1) |
| C2 | `seal.kind` of every link is `revocable-only` | None | `SEAL_PROFILE` |
| C3 | One healthy observation, on the pinned chain, with a clock that holds and a tip that is not too old | **R** LIP-0022 B6.1 [D]: its six codes in their order | `OBSERVATION_CHAIN`, `OBSERVATION_VOID`, `NODE_UNHEALTHY`, `NODE_DISAGREEMENT`, `OBSERVATION_CLOCK`, `TIP_AGE` |
| C4 | Steps 1 to 4 of LIP-0008 section 4 for every link, and section 12: the names; the request under the recipient mode; the closure journal; the window; the issuance; the seal, unspent with the mempool included; the recent block; the exact leaf in `actions`; the executor and the authenticated pin of the service; `iat <= now < exp` | **R** [F]: the steps 1 to 4 in their numbers. Whether they run link by link is open (O-1 below) | Section 6 |
| C5 | Under a child: the child within its parent (LIP-0008 sections 12.2, 12.5); the row (LIP-0026 R2.1 to R2.4); the coin (R3.2 to R3.4); the stop coin (LIP-0027 H2); the attestation (LIP-0014 section 8); the class with the list and the entry (LIP-0026 section 9; LIP-0010 section 10.6) | **R**: R2.5 [C] puts the four row checks in their order "after the admission of the parent, and before the check of the child's attestation"; R6.1 orders the three coin checks and leaves their place beside the attestation open; H2.1 [D] reads the closure journal first | The codes of those sections; section 6 for the child within its parent |
| C6 | The contract that `contract` binds is presented or resolved (LIP-0008 section 12.2), recomputes to that identifier, and mirrors every limit of `G` by executor, kind, resource, unit and amount | None | `GRANT_CONTRACT`, `CONTRACT_LIMIT_MISMATCH` |
| C7 | Every fact of the verdict comes from the one observation of C3 | **R** LIP-0022 B1.5 [D] | Those of C3 |
| C8 | Asked by D immediately before its write (D9): the tip is the tip of the verdict, the clock holds, and the closure journal has no record for the path beyond the position of the verdict | **R** LIP-0022 B1.6 [D] for the tip and the clock | `OBSERVATION_VOID`, `OBSERVATION_CLOCK`, `TIP_AGE`; the code of the closure |

Four orders are open rows. Each decides only which code comes first where
two defects meet, and each is decided by the editors of the step table in
review, not by the owners.

| Row | The disagreement | What this draft does until it is decided |
| --- | --- | --- |
| O-1 | LIP-0008 section 4 "for every link" before the row checks, against a table that judges every signed octet of a child before any read of a node | States no order between C4 for a child and C5 |
| O-2 | The journal first, against the documents first. A malformed request at a lost journal gets another code under each | C reads its closure journal where its cited text puts the read; D reads the session journal at D1, after the verdict |
| O-3 | The place of an undefined action text and of an undefined limit kind, and of the request's own checks (the leaf in `actions`, `iat <= now < exp`), relative to the checks of a child | States no place; D3 is this profile's own check of its keys |
| O-4 | The inner order of the atomic write | States it for its own entries: D10 |

| # | Check of the dispatching service, in this order | Mark | Code |
| --- | --- | --- | --- |
| D1 | The session journal is intact and this replica holds its token | **R** LIP-0025 M4.1 [D] | `JOURNAL_LOST`, `JOURNAL_FENCED` |
| D2 | The identity of the request is not in the journal, and its `iat` is later than the `fenced_at` of every recovery entry. Identities and ended records are kept as long as the journal lives | **P**, after LIP-0028 T2.6 and T5.8 [C] | `AGENT_SESSION_REPLAY` |
| D3 | No limit of `G` has one of the three `kind` texts with a key that section 3.3 does not define; the level and the span are stated | **P** | `AGENT_SESSION_LIMIT_KEY`, `AGENT_SESSION_LIMIT_MISSING` |
| D4 | The slot table maps the recipient to exactly one account at its current generation | **P** | `AGENT_SESSION_SLOT` |
| D5 | The slot holds no session that counts (cells H1, S1, E1), and it is not unusable after a recovery (section 5.6) | **P**. The key holder keeps the stronger duty that it cannot be checked here: "A slot holds runs of one origin" (LIP-0028 T7.7 [C]) | `AGENT_SESSION_SLOT` |
| D6 | The process of the agent will hold no key or right of an effect | **R** LIP-0029 O1.6 [C]. A deployment duty; no code | None |
| D7 | `H < lease_end_height <= H + span`, and `lease_end_height` is at most the `not_after_height` of every link | **P** | `AGENT_SESSION_SPAN` |
| D8 | The ceilings of the operator and the capacity of the host. They lower and never raise | **R** LIP-0008 section 2 [F]: "It never increases a rental ceiling" | `AGENT_SESSION_CAPACITY` |
| D9 | The recheck C8 | **R** | Those of C8 |
| D10 | One atomic write, or nothing, with its reads in this order: the slot holds no session that counts; the own level, then the row level; the debit of one start in the own account, then in the row account. It writes the session record: the identifier, which is the identity of the request; the identifier of `G` and the proof identifiers; the Subject; the mode and the channel of the request; the entry of the recipient for a child of a class row; the slot with its account and generation; the configuration that will be started; `E`; the tip and the position of the verdict | **P**; the two accounts and their order **R** LIP-0026 R5.6 [D] | `AGENT_SESSION_SLOT`; `AGENT_SESSION_LEVEL_OWN`, `AGENT_SESSION_LEVEL_ROW`; `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| D11 | After the write and before the effect, C confirms once more that the closure journal has no record for the path. Where it has one, D writes the end, starts nothing, and the debit stays (R5.8) | **P** (AS2.4) | The code of the closure |

The effect follows D11: D starts the process in the slot (**R** LIP-0025
M3.2 [D] for the order: the effect follows the write). A start whose outcome
is unknown is cell H27.

#### 5.2. Cell H2: a restart (**O**, Q6)

One form holds under both branches (**P**): the slot, the account with its
generation and the configuration are those of the session record. A slot
table that now maps the recipient elsewhere refuses as `AGENT_SESSION_SLOT`,
and no restart moves a session. The restart changes neither `E` nor the
identifier. D first stops the earlier process of the session, or records the
station contract's proof that none runs, and then starts: one session has at
most one process.

| | Branch (a): a signed request | Branch (b): no request |
| --- | --- | --- |
| Who asks | The key holder of `A`, for the resumed run (AS3.2), with the leaf `swarma/station/agent/restart` and the one argument `session`. A request that states a lease end is no request of this leaf | The dispatching service, on its own, in the state `held` alone |
| Checks | C1 to C8 for the request, with that leaf in `actions`; D1, D2; the session is in the journal for the proof path and executor of the request (`AGENT_SESSION_UNKNOWN`) and has no end (`AGENT_SESSION_ENDED`); the record's slot (`AGENT_SESSION_SLOT`); D8, D9; the atomic write with the debit of one start; D11 | D1; the authority is `held` under AS2.4; the record's slot |
| Record | The identity of the request, the debit, a restart entry | A restart entry |
| Cost | The key holder is in the path of every restart: a host cannot bring a crashed session back alone, and a key holder that is down, or an origin that no longer lists the grant, leaves the agent down. The starts kind bounds a loop of restarts | No debit can be made, because "One request identity holds at most one reservation" (LIP-0026 R5.7 [D]) and there is no request. The starts kind then bounds no loop. A host can run again, until `E`, an agent for which its key holder would no longer sign |

#### 5.3. Cells H3 and S3: a renewal

The renew request is admitted on its own verdict; that verdict is the check
of the held authority at that tip, and no other check comes first (**P**).

| # | Check, in this order | Code |
| --- | --- | --- |
| 1 | C1 to C8 for the request, with the renew leaf in `actions`. For a child of a class row the request presents the list where the pin changed | The codes of section 5.1 |
| 2 | D1, D2 | `JOURNAL_LOST`, `JOURNAL_FENCED`, `AGENT_SESSION_REPLAY` |
| 3 | The session is in the journal for the proof path and executor of the request | `AGENT_SESSION_UNKNOWN` |
| 4 | The record has no end, and `H` of the verdict is below the `E` that stands. Where `H >= E`, D writes the end (cell H9) and refuses: the height decides before the request | `AGENT_SESSION_ENDED` |
| 5 | The new `lease_end_height` is above the `E` that stands, at most `H` plus the span, and at most the `not_after_height` of every link. A renewal never lowers a lease and never leaves it as it is | `AGENT_SESSION_SPAN` |
| 6 | D9; then one atomic write with the read that the record has no end; then D11 | Those of C8; `AGENT_SESSION_ENDED` |

The authority is held for the heights `H` with `H < E` inside every window.
The journaled end records the first finding of what the heights already
decided (**P**).

#### 5.4. Cells H4 and S4: a stop

The checks are those of section 5.3 with the stop leaf and without check 5;
the write is the end (**P**). A stop is admitted like every invocation:
"Admission requires two predicates together" (**R** LIP-0008 section 12.5
[F]), and this profile makes no exception for a request that only takes
authority away. Where the verdict refuses, the session can still be ended
by cells 19 and 21. A stop for an ended session refuses (cell E4) and is not
answered as done, so that a caller reads the state from the code.

#### 5.5. Cells 7 to 18: the verdict while the authority is held

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS5.1 | At every new tip of its reading node the grant checker gives, for every proof path of a session without an end, one verdict, with the checks C2 to C5 and C7 for the path. No signature is verified. In the place of step 2 of LIP-0008 section 4 it requires, for a recipient by name, that the owner of the name is the signed owner key and that the name yields a key for the channel of the session's last signed request; for a recipient by key it requires nothing | **P**, after LIP-0028 T4.5 [C]. No request of this profile lacks a signature, so the stored key of T4.5 is not needed, and a replaced key under the same owner changes no verdict (cell H25) |
| AS5.2 | A verdict takes no list of a landlord and reads no new attestation. It uses the octets that the last signed request of the session presented. A fact that only a presentation can supply gives a refusal without a record (cells H15, H18), and the exit is a renew request that presents it | **P**. The take of a list happens in an admission (LIP-0010 H40 [C]) |
| AS5.3 | The mapping is one rule. **Sound:** every check passes: `held`. **Ended:** the closure journal holds a durable record that refuses a link of the path (events 12, 14, 16, 17), or a height of a healthy observation is at or above `E` (event 9). **Suspended:** every other verdict, and no verdict | **P** |
| AS5.4 | The node of the grant checker watches, with its mempool included, the seal of every link of every such path, the stop coin of the row of a child, and for a child of a class row the seal of the recipient's entry. A conformance claim names the interval of the mempool read; this draft states none | **P**, after LIP-0029 O8.3 [C]. LIP-0022 "fixes no interval between observations" |

#### 5.6. Cell 24: a session journal that is started anew

The new journal charges everything that the lost one could have held
(**R** LIP-0025 M5.5 [D]). For this journal that means (**P**, except where
marked):

| # | What is charged |
| --- | --- |
| 1 | Every row account of the starts kind that could have had a record counts as full (**R** LIP-0026 section 5 [D]). So does every own account. The levels are not charged: item 3 holds every slot. A grant could have had a record unless the height of its recent block, and for a child that of its parent, is at or above the block boundary of the new journal (LIP-0025 M5.4) |
| 2 | Every start, restart, renew and stop request whose `iat` is not later than the `fenced_at` of the recovery entry refuses as `AGENT_SESSION_REPLAY`, because the lost journal could have held its identity (after LIP-0028 T5.8 [C]). A later request that names a session of the lost journal refuses as `AGENT_SESSION_UNKNOWN` |
| 3 | Every slot of the slot table as it stood at the fencing is unusable until a clearance of it is recorded in the new journal |
| 4 | Nothing is recorded as ended. What happens to a process that the lost journal started is the station contract's, and the clearance of item 3 is the one record of it here |

#### 5.7. Cells H9 and H10: the end of a term

| Rule | Requirement | Mark |
| --- | --- | --- |
| AS5.5 | A grant is not extended, and a session does not move to another grant (AS1.1). A new term is a new grant and a new session, opened by a start request, with a new identifier. The cost is one start of the agent in each term | **P**. "Each grant ... ends at `not_after_height`" (LIP-0008 section 2.1 [F]); "A slot serves one grant and lives as long as that grant" (LIP-0017 section 8 [D]) |
| AS5.6 | A row admits one child, ever. Its coin is spent by the anchor of that child (LIP-0026 R3.3 [C]), and the signing service makes one signature, ever, for one place of one parent (LIP-0014 J4.4 (a) [C]). A successor child takes another row or another parent. A place whose signing outcome is unknown is held and gives no successor: "the row is lost to this parent, and the next child takes another row or another parent" (J4.4 (f)). The party that wants a second term therefore holds a spare row or a second parent before the closing height | **R** for the three cited sentences; the last sentence **P** |
| AS5.7 | A child is signed by the delegation key of its parent, a decision that awaits the co-author's agreement and that LIP-0020 W11.8 carries for the octets of `swarma-grant/4`; LIP-0008 section 12.6 states the signature by the parent's recipient as the rule in force. This draft takes no side and reads neither signature | **R** [C] |

### 6. Refusal codes

Every refusal that the table can produce has a code. The first table holds
the codes of this profile (**P**). The second holds the refusals of the base
that have no v4 code there, each proposed as **new**, with the section that
it would enter; a code with the same meaning that lands first from the text
in review replaces the proposal.

| Code | What it reports | Cells |
| --- | --- | --- |
| `AGENT_SESSION_REPLAY` | The identity of the request is in the session journal, or its `iat` is not later than the fencing of a recovery | Event 5; D2 |
| `AGENT_SESSION_UNKNOWN` | The request names no session of its proof path and executor | N2, N3, N4, N19, H6, 24 |
| `AGENT_SESSION_ENDED` | The session that the request names has ended | E2, E3, E4, E19 |
| `AGENT_SESSION_SLOT` | The recipient maps to no single account at its current generation; the slot holds a session that counts; the slot is unusable after a recovery; or the slot of a restart is not that of the record | H1, S1, E1; D4, D5, D10; section 5.2 |
| `AGENT_SESSION_LIMIT_KEY` | The grant states a limit with one of the three kind texts and a key that the profile does not define | D3 |
| `AGENT_SESSION_LIMIT_MISSING` | The grant states no limit of the level key or of the span key | D3 |
| `AGENT_SESSION_SPAN` | The lease end is not above `H`, or not above the lease end that stands, or more than the span above `H`, or above the closing height of a link | D7; section 5.3 |
| `AGENT_SESSION_LEVEL_OWN` | A start would put more sessions under the grant than its level | D10 |
| `AGENT_SESSION_LEVEL_ROW` | A start would put more sessions under the row than its level | D10 |
| `AGENT_SESSION_CAPACITY` | A ceiling of the operator or the capacity of the host refuses | D8 |

None of them records a closure of a grant (**P**).

| New code | What it reports | Check of the base without a v4 code | Section that it would enter |
| --- | --- | --- | --- |
| `REQUEST_AUTH` | The request does not verify under the recipient mode of `G` | LIP-0008 section 4, step 2 | The codes of the v4 admission in LIP-0020 section 11, beside the rule map of section 11.11 |
| `REQUEST_TIME` | `iat <= now < exp` does not hold | LIP-0008 section 12.5 | The same |
| `GRANT_CLOSED` | The closure journal holds the closure of a root grant by its issuer's spend | LIP-0008 sections 4, step 4, and 5.1 | The same |
| `GRANT_WINDOW` | `H` lies outside the window of a root grant | LIP-0008 section 7.1, rule 2 | The same |
| `GRANT_ACTION_ABSENT` | The command of the request is no entry of `actions` of `G` | LIP-0008 sections 4, step 4, and 12.3 | The same |
| `GRANT_EXECUTOR` | The executor of the grant, the executor of the request and the authenticated pin of the service do not agree | LIP-0008 section 4 | The same |
| `GRANT_CONTRACT` | The contract is not presented, or does not recompute to `contract` | LIP-0008 section 12.2 | The same |
| `CONTRACT_LIMIT_MISMATCH` | The contract does not mirror a limit of the grant | LIP-0008 section 2 | The same |
| `CHILD_ACTIONS_WIDER`, `CHILD_WINDOW_NOT_NESTED` on v4 | A child lists an action outside `delegate.actions`, or its window is not inside its parent's | LIP-0020 section 11.11, last row: LIP-0014 section 4 names the two for v3, and "Whether v4 takes them is an open question" | LIP-0020 section 11.11 |

An action text that no profile defines and a limit kind that no profile
defines are refused by W11.4 ("an executor refuses an action that its
profile does not define"). The table of section 4 produces neither: a
request with another command is no request of this profile, and a foreign
key of one of the three kinds is `AGENT_SESSION_LIMIT_KEY`. Their codes come
with the registry section that is in review.

### 7. What is outside this profile

Each is named once, with the unit that owns it.

| Matter | Owner |
| --- | --- |
| The states of a process, liveness, heartbeat, backoff, the home and its export, the proof of an empty account, every bound in clock time, among them the time from a journaled end to a stopped process | The station contract (AS1.4) |
| **Follow-up work.** The grant of a session authorizes the start and the holding and no instruction. An instruction is admitted under the grant that it cites and enters a run only as LIP-0013 J7.6 says: "An instruction admitted under another grant MUST NOT enter an existing run as an instruction. It creates its own run, with its own channel, or stays data" | LIP-0013 section 3.6 [C] and the gate that admits instructions. This profile adds no rule; the read of AS2.4 is what such a gate may ask |
| **The model lease.** The budget of a model or of a gateway is the limits of a second grant whose executor is the model service. A failed renewal of a credential there is no event of section 4 and changes no state | LIP-0028 [C], for a client that cannot sign, at the model service |
| **Isolation of a slot by origin.** "A slot holds runs of one origin", asked of the key holder | LIP-0028 T7.7 [C]. `X` checks what it can observe: one session per slot (D5) |
| The slot table and how an account is created | The station contract |
| The mapping of the dispatching service's own closed set of refusals to the codes of section 6 | The implementation of the dispatching service |

### 8. Cases

Each case names its cells and has a control that is admitted. Vectors come
with the members of the invocation.

| Case | Setting | Outcome | Cells |
| --- | --- | --- | --- |
| S30-1 | A valid start; starts 5, level 1, span 144; lease end `H + 144` | Admitted | N1 |
| S30-2 | The same with `H + 145`; with `H`; with one above `not_after_height` | `AGENT_SESSION_SPAN` each. A lease end equal to `not_after_height` inside the span is admitted | D7 |
| S30-3 | A grant without the level limit; without the span limit; without the starts limit | `AGENT_SESSION_LIMIT_MISSING` twice; then `OWN_LIMIT_OVER`. With all three the start is admitted | D3, D10 |
| S30-4 | A limit of the starts kind with a `period` | `AGENT_SESSION_LIMIT_KEY`. Without the period it is admitted | D3 |
| S30-5 | A second start for the same slot while the first session is held; after its end and before the clearance; after the clearance | `AGENT_SESSION_SLOT` twice; then admitted | H1, E1, E28 |
| S30-6 | The request of S30-1 once more | `AGENT_SESSION_REPLAY`; no second session | H5 |
| S30-7 | The process start of S30-1 gives no answer; the caller sends a start with a new identity | `AGENT_SESSION_SLOT`; one debit, one record. After a stop and a clearance a new start is admitted | H27, H1 |
| S30-8 | A renew 100 blocks after the start with a lease end 144 above the tip; a renew that states the standing lease end; a renew at a tip that has reached `E` | Admitted; `AGENT_SESSION_SPAN`; `AGENT_SESSION_ENDED` with the end written | H3 |
| S30-9 | The channel key of a recipient by name is replaced under the same owner; then a renew under the new key. Control: the key is removed | The authority stays held and the renew is admitted. With the key removed: suspended | H25, H18 |
| S30-10 | The issuer spends the seal of the parent of `G`; the checker validates the spend in its mempool while its observation is not healthy. A session under another grant runs | The closure is written, the session ends, a later renew refuses as `AGENT_SESSION_ENDED`. The other session is untouched | H12 |
| S30-11 | The same spend at a non-witness | Suspended; ended at `E` | H13, S9 |
| S30-12 | The tip is too old | Suspended; nothing ends. A sound verdict at a new tip lifts it | H8, S7 |
| S30-13 | A reorganisation lowers `H` below `not_before_height`; later the tip is inside the window again | Suspended; then held | H11, S7 |
| S30-14 | A reorganisation lowers `H` below `E` after the end was written | The session stays ended | E7 |
| S30-15 | The stop coin of row 3 is spent; a session under a child of row 4 runs | The session of row 3 ends; that of row 4 stays | H16 |
| S30-16 | Two documents of one row with a row level of 1 and two recipients: a start under each | The first is admitted; the second refuses as `AGENT_SESSION_LEVEL_ROW` | N6, H6 |
| S30-17 | A stop for a held session; for the same session again; for an identifier that the journal lacks; for a suspended session whose verdict refuses | Ended; `AGENT_SESSION_ENDED`; `AGENT_SESSION_UNKNOWN`; the code of the verdict, and the session stays | H4, E4, N4, S4 |
| S30-18 | The landlord's list changes and keeps the entry; changes and the checker lacks its octets; a renew then presents a list without the entry | No event; suspended; ended with the removal mark | H15, H14 |
| S30-19 | The session journal is lost while a process runs; it is started anew; a start under the old grant for the uncleared slot; the same after a clearance; a start under a grant whose recent block is above the boundary, after the clearance | `JOURNAL_LOST`; then `AGENT_SESSION_SLOT`; `OWN_LIMIT_OVER`; admitted | H23, H24, N24 |
| S30-20 | A second replica of the dispatching service cannot reach the session journal | It admits nothing: `JOURNAL_FENCED` or `JOURNAL_LOST` | D1 |
| S30-21 | A child whose `actions` hold the start leaf outside `delegate.actions` of its parent | `CHILD_ACTIONS_WIDER` (proposed for v4). With the leaf in the parent's list it is admitted | C5 |
| S30-22 | A halt command of the owner for a held session; for an ended one | Ended; `AGENT_SESSION_ENDED` | H19, E19 |
| S30-K1 | A known limit. The issuer spends the seal, and the transaction has not reached the node of the checker | The authority is held until the node shows the spend. Nothing bounds that time (LIP-0008 section 5.3) | H12 |
| S30-K2 | A known limit. The node receives no block | Suspended, and under branch (a) of Q8 without an end in time | S8 |

## Sources

No service, no key holder and no node was run for this draft.

| Statement | Source |
| --- | --- |
| The members of a grant, the limit key, the pools, the rule map | LIP-0020 section 11, W11.2 to W11.4, W11.8 to W11.11 |
| The order of an admission, the executor, the budget, the replicas, the operator's ceilings, the contract mirror | LIP-0008 sections 2 and 4 |
| The closure of a spent seal; a verifier whose closure journal is lost | LIP-0008 section 5.1; J6.9 |
| The window, the invocation with its Subject, the proof path, the leaves, the time terms | LIP-0008 sections 7.1, 12.1, 12.2, 12.3, 12.5 |
| What a proposal for a leaf and for a limit kind states | LIP-0018 sections 2 and 3 |
| The observation and its codes | LIP-0022 sections 1 to 3 and 6 |
| The journal check, a lost journal, starting anew | LIP-0025 sections 4, 5 and 7 |
| Rows, the fit of a child, the coin, the accounts | LIP-0026 sections 2, 3 and 5 |
| The stop coin of a row | LIP-0027 sections 2 and 3 |
| The list of a landlord's agents and the entry | LIP-0010 section 10 |
| The gate of the key holder | LIP-0013 section 3.6, J7.1 to J7.8 |
| The signer of a child and the reservation ledger | LIP-0014 section 11.1, J4.1, J4.4 (a) to (g) |
| The session for a client that cannot sign | LIP-0028 |
| The owner's command | LIP-0029 sections 1, 2, 6, 8 and 11 |
| The agreed configuration | LIP-0017 section 8 |

## Alternatives

- **A grant checker inside the dispatching service.** One service and one
  journal, and the atomic step of LIP-0028 T4.6 as it stands. Rejected: the
  dispatching service would need a chain view, an observation and a closure
  journal of its own, a second copy of what stands behind the message
  origin, and two closure journals on one host can disagree about one seal.
- **The life of a process in this LIP.** States for starting, running and
  down, and a rule for the restart of a machine. Rejected by the narrowing:
  those are facts of one host, and the grant decides none of them.
- **The lease in seconds,** as LIP-0028 has its window. Excluded by the
  owner's direction.
- **No lease.** A suspended session would then run to the end of its grant.
- **A new member of the grant** for the account, the configuration or the
  model. It would change the octets of `swarma-grant/4`.
- **One leaf for start and restart.** One leaf would have two lists of
  arguments, and a reader of the leaf could not select the list.
- **A level counted as an account.** An account is never lowered (LIP-0026
  R5.1), so it would be a second cap on starts and no level.

## Security consequences

- **A revocation is bounded in blocks and not in time.** An end needs a
  durable record at the grant checker or a height. Every other refusal
  suspends, and a suspended authority ends at `E`, at most one span above
  the tip of its last admitted start or renewal. While the node receives no
  block no height is reached. Whether a clock ever ends a suspended session
  is Q8.
- **A suspended session still runs.** Suspension takes the answer "held"
  away and admits no restart under branch (b). The process keeps its home
  and every credential that works without a signature (LIP-0013 J7.8).
- **At a non-witness the span is the delay of every revocation** (AS1.5).
  An issuer that grants to such a host chooses a small span.
- **No verifier that never saw a spend is bound by it** (S30-K1).
- **The executor is trusted for the end.** The set writes the end and stops
  the process. A host that does neither keeps an agent running; the other
  executors still make their own checks.
- **The executor is stricter than a fresh verifier in two places.** A
  verdict takes no presentation (AS5.2), and a journal that was started anew
  charges every older grant as used (section 5.6). In both the set refuses
  where another verifier might admit, and never the reverse.
- **Between a closure and its delivery** the dispatching service may still
  hold an older verdict. AS2.4 and D11 close that gap for an answer and for
  an effect; nothing else is performed on a verdict.

## Conformance impact

None on normative v0.1, none on Grant v3, and none on the octets of
`swarma-grant/4`. No conformance class and no vector is added. A
conformance claim under this profile would state whether the executor is a
witness (AS1.5) and the interval of its mempool read (AS5.4).

## Open questions

### Questions for the owners

These five and no other. Each has its options, what each costs, and a
recommendation that decides nothing.

- **Q4. Effect or work.** (a) Effect: `X` is an effect service of LIP-0006
  section 7 and refuses a grant whose terms carry a text, and a run at
  level L0 gets no signature for a start (LIP-0029 O6.7 (a)). Cost: an
  orchestrator at L0 starts no worker. (b) Work. Cost: the start of a
  process on a host is bounded by the three limits alone and by no level.
  Until the answer the profile states no class, and the stricter class of
  LIP-0022 B3.5 holds. Recommendation: (b).
- **Q6. Does a restart need a signed request?** Section 5.2 has both
  branches and their cost. (a) Signed: a host cannot bring a crashed session
  back alone. (b) Unsigned: the starts kind bounds no restart, and a host
  can run again an agent for which its key holder would no longer sign,
  until `E`. Recommendation: (a).
- **Q8 (b). Does a clock ever end a suspended session?** (a) No: cell S8
  stays, and a stalled node holds a suspended session without an end in
  time. (b) Yes: the dispatching service ends it when the age of the tip
  reaches the cutoff of the class (LIP-0022 B3.6). Cost: the one place
  where a clock ends an authority, against the direction that time is
  counted in heights; and an outage of the node longer than the cutoff ends
  every session of the host, each of which then costs a start.
  Recommendation: (a), with the bound stated as unbounded in time.
- **Q11. Does a session that an owner starts need a grant?** (a) Yes: cell
  N20 (a). Cost: an owner starts nothing on a host for which no grant
  exists. (b) No. Cost: an authority without a window, a seal or a limit,
  which only a halt command and the operator end. Recommendation: (a);
  "The chain rules apply inside one host too" (LIP-0029).
- **Q13. The level of a halt command.** Open in LIP-0029 ("the level of a
  stop and of resumption"). (a) The lowest level that the policy admits.
  Cost: every device of the owner can end every session. (b) The level of
  the command that started the run, or above. Cost: a lost device of that
  level delays a stop. Recommendation: (a): a halt takes authority away.

### Open, and not the owners'

| Item | The question | Who decides |
| --- | --- | --- |
| P1 | **The configuration.** LIP-0017 section 8 has a contract "under which the platform starts an agent in an agreed configuration" carry the hash of one manifest, as a rule of the contract's profile; no profile has that member today. Two things are open: the preimage of the hash over what a host starts, and how the contract profile requires it. This profile decides neither, gives the start request no configuration argument, and has the record keep what was started (D10). **Consequence:** one hash for each contract, with one contract along a path, makes every worker under one orchestrator run the same configuration. **Remedy:** a mapping in the contract profile from a row or a recipient to a hash, and no member of the grant | The LIP that defines the contract profile of a hosted agent (LIP-0017 section 8; LIP-0018 section 1) |
| O-1 to O-4 | The four orders of section 5.1 | The editors of the step table of the v4 admission, in review |
| N1 | The members of the invocation and of the receipt; the journal key of a request identity | LIP-0020 |
| N2 | Acceptance of the new codes of section 6, or their replacement by codes of the text in review | LIP-0020 section 11 |
| N3 | The alphabet of a segment of a leaf and of a kind text | LIP-0008 section 12.3 |
| N4 | The amendment of the row `slot.station` | LIP-0007 section 1 |
| N5 | Whether the reading of AS3.2, that the key holder's run precedes its process, stands | LIP-0013 section 3.6 |
| N6 | The entries of the session journal and of the closure journal on the form of LIP-0025, and the block boundary of section 5.6 after a reorganisation | LIP-0025 |
