# LIP-0030: Action profile no. 1, an agent session on a host

- **Status:** Draft. Nothing in this file is in force by its own word. Every
  rule is marked as restating a cited text, as proposed here, or as open.
- **Created:** 2026-11-16
- **Affects:** what a v4 grant lets an executor do when the executor is the
  service of a host that starts and keeps the run of an agent: the actions,
  the limit kinds, the order of the checks at a start, the events that end a
  running session, and renewal
- **Builds on:** LIP-0006 sections 1 and 7, LIP-0007 sections 1 and 2,
  LIP-0008 sections 2, 2.1, 4, 5, 5.1 to 5.3, 6, 7.1, 11.4 and 12, LIP-0010
  sections 10 and 11, LIP-0013 section 3.6, LIP-0017 section 8, LIP-0018
  sections 2 and 3, LIP-0020 sections 6 and 11, LIP-0022 sections 1 to 6,
  LIP-0025, LIP-0026 sections 1, 2, 5 and 9, LIP-0027 sections 1 to 3,
  LIP-0028 and LIP-0029 sections 1, 2, 6 to 8 and 11
- **Deciders:** both owners

## Summary

A grant of version 4 names an executor, a recipient, a list of action texts
and a list of limits (LIP-0020 W11.2 to W11.4). No profile defines an action
text or a limit kind yet: "Which texts name an action is for the action
registry (LIP-0007; LIP-0008 section 12.3), which is open", and of the limit
kinds "none exists yet" (LIP-0020 W11.4). Until a profile defines an action,
a v4 grant has no effect at an executor.

This draft proposes the first such profile. Its executor is the service of a
host that starts the run of an agent and keeps it: the agent is long-lived,
and a run for one task is the special case in which the session is stopped
after that task.

The draft has seven parts:

1. the terms, and what the profile adds and what it only references
   (section 1);
2. three actions and four limit kinds, each marked "proposed here" with the
   registry section that it would fill, and the grant members that carry
   them, which are members that LIP-0020 section 11 already has (section 2);
3. one table of every field that an executor needs to start and to keep a
   session, with the place of each: the grant, the host's policy, a derived
   value, the executor's check and its refusal (section 3);
4. the order of the checks at a start, with the observation of LIP-0022
   that each rests on (section 4);
5. the keep check, and the events that end a running session, each with its
   largest delay or with the delay marked open (section 5);
6. renewal and expiry, in block heights alone (section 6);
7. what the profile does not decide (section 7).

The draft adds no member to the grant, changes no other LIP, and defines no
octets: the three requests are signed invocations, and the invocation has no
members yet (LIP-0020 section 3, type `swarma-invocation/1`). It has no
vectors. Nothing of it is implemented.

## What is decided and what is proposed

**Direction of the owner.** Ivan Oparin gave this direction on 2026-11-16, as
it was relayed to the author of this draft; no record in `decisions/` holds
it yet, and the co-author's answer is not known:

1. The default agent is long-lived: an orchestrator, a worker, a reviewer.
   Each runs in an OS account of its own, with an identity of its own and
   with keys that services hold. The run for one task is a special case.
2. A v4 grant has no clock member. The time of a session and of its renewal
   is counted in block heights.

Point 2 agrees with text that the specification already holds: the window of
a v4 grant is a pair of heights (LIP-0008 section 7.1; LIP-0020 W11.2), and
"No clock enters this comparison" (LIP-0008 section 7.1, rule 2). Point 1 is
the reason for this profile and decides none of its rules.

**Marks.** Every rule of this draft carries one of three marks.

| Mark | Meaning |
| --- | --- |
| **Restates** | The rule repeats the cited text and adds nothing. The cited text keeps the state that its own LIP gives it: in force, Draft, or awaiting the co-author. This draft changes no such state. |
| **Proposed here** | The rule is new in this draft. Neither owner has decided it. |
| **Open** | The draft states the need and decides nothing. The question has a number in the section "Open questions". |

**The inputs.** Two lists were weighed for this draft: the list of what the
dispatching side of a host needs to start and to keep a session, and a
proposal from the side that checks grants. The action names and the limit
kinds of section 2 come from that proposal. They are proposals of this draft
and nothing more. Where the draft does not follow the proposal, it says so in
place: the limit kind for a model budget (section 2.3, Q5), the form of the
names (Q3), and the reading of a restart (Q6).

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The life of an agent session as a function of stated facts: start, lease, keep check, renewal, end | Yes, as a model | The owners' answers to Q1, Q4, Q6, Q7 and Q8 |
| The three requests as octets | No | The members of the invocation (LIP-0020), the registry of action texts and a service type (Q2, Q3) |
| The limits as members of a grant | No | The registry of limit kinds (LIP-0018 section 2; LIP-0020 W11.4) and the texts of `resource` and `unit` (N3) |
| The checks of the proof path at a start and at a keep check | No | A run of the observation under LIP-0022 and of the reads of LIP-0021, as LIP-0028 states for its own checks |
| The record of a session as an entry of a journal | No | The entries of a service journal on the form of LIP-0025 |
| A host service that keeps sessions | No | All of the above, and the station contract (section 7) |

## Motivation

The forms that a host has today start one bounded run of an existing worker
account and are finished with it. A long-lived agent needs more: an identity
of the session that survives a restart, a lifetime that follows the grant and
not a local timer, a rule for a restart, a stop when the authority behind the
session ends, and a claim on capacity that lasts as long as the session.

The specification has most of the parts. LIP-0008 section 4 gives the order
of an admission, section 12 the signed invocation and the proof path,
section 5.1 the durable closure of a spent seal. LIP-0022 gives the
observation. LIP-0026 gives rows and accounts, LIP-0027 the stop of a row,
LIP-0010 section 10 the list of a landlord's agents, LIP-0029 the owner's
command. LIP-0028 shows, for a bearer token at a model proxy, how an
admission that happened once is kept honest afterwards: the service makes
the checks of the proof path again before every reservation (T4.5).

What is missing is the profile that says which action a grant names for a
session, which limits bound it, and how those parts apply to a run that
lasts for thousands of blocks. LIP-0018 section 3 lists what a proposal for
an action name has to state, and section 2 what a proposal for a limit kind
has to state. This draft follows both lists and says where it cannot fill an
item.

## Current state

- LIP-0020 section 11 gives `swarma-grant/4` its members, as text in force
  since version 0.1.53 on its own terms. The action registry and the
  registry of limit kinds are open (W11.4). A section with those registries
  is in review on another branch and is no part of the base of this draft.
- LIP-0020 reserves `swarma-invocation/1` and gives it no member. LIP-0008
  section 12.1 states its logical fields.
- LIP-0007 section 1 lists `slot.station` as a semantic candidate: "Admit
  access to a named rental slot/station and end access; bind the renter,
  resources and rental window." It has no accepted action strings.
- LIP-0028 defines a session for a client that cannot sign, with a bearer
  token. Its word "session" means that and nothing else (Draft, J13,
  agreement pending).
- LIP-0029 O2.1 names the action profiles of this specification as the typed
  action registry of an owner command. Its open questions hold "the level of
  a stop and of resumption".
- LIP-0017 section 8 has a contract under which the platform starts an agent
  carry the hash of the agreed configuration manifest, and has the launcher
  start nothing that does not reproduce that hash (a draft's proposal on
  decision C9, agreement pending).

## Proposal

The final grant of a proof path is called `G`, as in LIP-0028. The executor
is `X`: the service of one host that starts and keeps sessions. `H` is the
height of the tip of an observation (LIP-0008 section 7.1, rule 2). The
recipient of `G` is `A`, the agent.

### 1. Scope and terms

| Rule | Requirement | Mark and source |
| --- | --- | --- |
| AS1.1 | An **agent session** is an activity at run time: `X` keeps one run of one agent alive in one slot on the strength of one admitted start request, across restarts of the process, until the session ends. Its record is an entry in the journal of `X`. | **Proposed here.** "An activity at run time" and "its record is an entry in the journal of the service" are the words of LIP-0028, "Proposal". "Run" is the run of LIP-0013 J7.1. |
| AS1.2 | An agent session belongs to one final grant with its proof path, to one executor, which is `X`, and to one slot. None of the three changes while the session lives. | **Proposed here**, in the words of LIP-0028 T1.2, which states the same of its session. Q7 asks whether the grant may change. |
| AS1.3 | The **slot** of an agent session is one OS account of the host of `X`. It is identified by the user id under which the slot runs, the first form of a slot binding in LIP-0028 T6.1. The address form of T6.1 is not used by this profile. | **Proposed here.** The form is LIP-0028 T6.1. |
| AS1.4 | An agent session has no token and is no session of LIP-0028. Each of its three commands is a signed invocation (LIP-0008 section 12.1), and no request with a bearer asks for one of them. | **Proposed here.** LIP-0028 T1.3 has the same for the three commands of its own session. |
| AS1.5 | The **lease** of an agent session is the stretch of heights for which the last admitted start or renew request keeps it. Its end is the **lease end** `E`, a block height. The session is **live** while its record has no end. It is **suspended** while it is live and the last keep check of `X` refused without a durable record (section 5). An end is final. | **Proposed here.** "An end is final" is the rule of LIP-0028 T5.4 for its session. |
| AS1.6 | The **station contract** is the agreement between the operator of a host and the parties that use it, with the host's signed policy. It is named here and is out of this specification. | **Proposed here**, as a name only. |

**What this profile adds:** the three action texts and the four limit kinds
of section 2, as proposals; the logical arguments of the three requests; the
lease in heights; the order of the checks at a start; the keep check; the
list of the events that end or suspend a session; the rule of renewal; and
eight refusal codes (section 8).

**What this profile only references,** and does not change: the members of a
grant and their forms (LIP-0020 section 11); the order of an admission
(LIP-0008 section 4); the signed invocation and the proof path (LIP-0008
section 12); the observation, the clock and the age of the tip (LIP-0022);
the durable closures (LIP-0008 sections 5.1 and 5.2); rows and accounts
(LIP-0026); the stop coin of a row (LIP-0027); the list of a landlord's
agents and the seal of an entry (LIP-0010 section 10); the owner's command
(LIP-0029); the gate of the key holder (LIP-0013 section 3.6); the agreed
configuration (LIP-0017 section 8); and the session of LIP-0028, which the
harness of an agent may hold at a model proxy while its agent session lives.

One word has two meanings from here on. "Session" alone, in LIP-0028, is the
bearer session of a client that cannot sign. This draft always writes "agent
session". Q3 asks whether the names of the actions should carry that
difference.

### 2. The actions and the members that carry them

#### 2.1. The grant members

No new member is needed. The table states what each member of LIP-0020
section 11 means under this profile.

| Member (LIP-0020) | What the cited text says | Its meaning under this profile | Mark |
| --- | --- | --- | --- |
| `executor` {`name`, `key`} | One executor for the own scope of a grant, a service name with its pinned public key (W11.4). The grant's executor, the invocation's executor and the authenticated service's pinned name and key agree (LIP-0008 section 4) | `X`, the session service of one host. It fixes which host acts. Only `X` starts a session under `G` | **Restates** for the member; the meaning is **proposed here** |
| `recipient` | By key, or by name with the owner key; in the name mode the request key is read from the name at every admission (W11.3; LIP-0008 section 3.1) | `A`, the agent for which the session runs. Its request key authenticates every request of the session (LIP-0008 section 4, step 2) | **Proposed here**; Q1 holds the other reading |
| `actions` | A sorted list of texts; a reader compares texts and knows no action; "an executor refuses an action that its profile does not define" (W11.4). Commands match exact leaf identifiers (LIP-0008 section 12.3) | The texts of section 2.2 that the issuer allows. A grant without the start text starts no session, and a grant without the renew text has sessions that end with their first lease | **Restates**; the texts are **proposed here** |
| `limits` | A list of limits, each with `kind`, `resource`, `unit`, `amount` and an optional `period`; a key without a stated limit has the ceiling 0 (W11.4; LIP-0026 R5.2) | The limits of section 2.3 | **Restates**; the kinds are **proposed here** |
| `not_before_height`, `not_after_height` | The half-open window in heights; admission requires `not_before_height <= H < not_after_height` (LIP-0008 section 7.1, rules 1 and 2) | The outer lifetime of every session under `G`. No session starts before the first height, and none is live at or after the second (AS5.4) | **Restates** for an admission; the rule for a running session is **proposed here** |
| `seal` | The seal of the grant; a validated issuer spend closes the grant durably (LIP-0008 SB1 to SB3 and section 5.1) | The stop of every session under `G` by the issuer (section 5) | **Restates** for the closure; the end of a session is **proposed here** |
| `contract` | The identifier of the one contract that the grant binds (W11.2; LIP-0017 section 5) | The contract carries the hash of the agreed configuration, which is what runs (LIP-0017 section 8, rules 1 and 3) | **Restates** LIP-0017 section 8, a draft's proposal there |
| `recent_block` | The committed recent block (LIP-0008 section 7; LIP-0022 section 4) | No meaning of its own here | **Restates** |
| `delegate`; `parent` and `ordinal` of a child | A root grant with `delegate` is a parent; a child names its parent and the ordinal of its row and fits that row in executor, recipient and limits (W11.2, W11.5; LIP-0026 R2.1 to R2.4) | An orchestrator that holds a parent gives each worker a child. The row fixes the host, the worker and the limits of that worker's sessions | **Restates** |

The grant states no clock, no path on a host, no secret, no key for messages
and no interval of liveness. That follows from W11.2: "A grant carries
nothing beside these members."

#### 2.2. The actions

Each row is one proposed leaf with the items of LIP-0018 section 3. The
names are those of the grant-side proposal. **Registry section that each
would fill:** the action table of a service type in LIP-0007 section 1,
under the `swarma/` namespace that LIP-0008 section 12.3 reserves for the
protocol; they are the texts that LIP-0020 W11.4 expects in `actions`. The
registry section of LIP-0020 that is in review would list them; it is no part
of this base, and this draft writes nothing into it.

| Item (LIP-0018 section 3) | `swarma/session.start` | `swarma/session.renew` | `swarma/session.stop` |
| --- | --- | --- | --- |
| State of the name | **Proposed here** | **Proposed here** | **Proposed here** |
| What it asks | Start one agent session, or restart the process of a live one (AS4.6) | Move the lease end of a live session to a later height, never past a window (AS6.1) | End a live session in an orderly way |
| Service type | **Open** (Q2). Smallest proposal: the candidate `slot.station` of LIP-0007 section 1 | The same | The same |
| Arguments, as logical fields without octets | `lease_end_height`; `configuration`, the hash of the agreed configuration (LIP-0017 section 8); for a restart `session`, the identifier of the live session | `session`; `lease_end_height` | `session` |
| Effect or work | **Open** (Q4) | **Open** (Q4) | **Open** (Q4) |
| Limits that bound it | `swarma/session.concurrent`, `swarma/session.starts`, `swarma/session.span` | `swarma/session.span` | None |
| Class under LIP-0022 B3.5 | Other privileged. **Proposed here** | Other privileged. **Proposed here** | Other privileged. **Proposed here**; Q12 holds the other reading |
| Receipt | **Open** (N1): the receipt has no members (LIP-0020). It would state the session identifier, `G`, the slot and the lease end | The same, with the new lease end | The same, with the end |
| Refusal codes | Section 8 | Section 8 | Section 8 |
| Vectors and checker | None. They come with the members of the invocation | None | None |

Every field of the three requests is covered by the request signature, as
LIP-0008 section 12.1 asks of the arguments of an invocation (**restates**).
A request states its lease end and its configuration itself; `X` takes
neither from a default (**proposed here**, after LIP-0029 O1.3: the fields
"define the effect completely").

The names have a point of form. LIP-0008 section 12.3 asks for "lowercase
slash-separated segments" and leaves the exact grammar open; LIP-0029
section 8.2 writes `swarma/device/revoke`. A dot inside a segment is neither
allowed nor excluded by that text. Q3 holds the question.

#### 2.3. The limit kinds

Each row is one proposed kind with the items of LIP-0018 section 2 that this
draft can state. **Registry section that each would fill:** the registry of
limit kinds, which "does not exist yet" (LIP-0018, "What the guide leaves
out"); LIP-0020 W11.4 says that the kinds "come with the type profile of the
kind (LIP-0008 section 2; LIP-0018 section 2)". The last column names the
kind of LIP-0008 section 2 that each belongs to.

| Kind (**proposed here**) | Unit, as a meaning | Period and arithmetic | Reservation, uncertainty, denials | May a child narrow it (LIP-0026 R2.4) | Kind of LIP-0008 section 2 |
| --- | --- | --- | --- | --- | --- |
| `swarma/session.concurrent` | Agent sessions | No period. A level and no cumulative amount: the number of sessions under the grant at `X` whose record has no end | Claimed in the atomic write of a start (AS4.5). Released by the journaled end of the session and by nothing else. A restart claims nothing more. A start whose outcome is unknown keeps its claim until it is reconciled (LIP-0008 section 2: "Uncertain effects retain their reservations until reconciled"). A refused request claims nothing | Yes: a smaller amount is the stricter one. Under a child, a start counts against the limit of the child and against the limit of its row | "Runtime and concurrency": "the number of instances or runs that may be active at once" |
| `swarma/session.starts` | Starts | No period: it holds for the whole window. A cumulative amount with an account of LIP-0026 R5.1 and R5.2; every admitted start request debits 1, a restart included | Reserved in the atomic write of a start. Never lowered (LIP-0026 R5.1, R5.8). One request identity holds one reservation (R5.7). A refused request reserves nothing (R6.2) | Yes. Under a child a start debits the own account of the child and the row account of its parent (R5.4) | None of the named kinds: a new kind, which arrives through a LIP (LIP-0008 section 2) |
| `swarma/session.span` | Blocks | A maximum for one request and no account: the largest `lease_end_height - H` that one start or renew request may state | Nothing is reserved. A request above it refuses and is not shortened (AS4.4) | Yes: a smaller amount is the stricter one. Under a child the smaller of the child's and the row's holds | "Runtime and concurrency", the running time. This profile counts it in blocks, which LIP-0008 section 2.1 leaves to the type profile |
| `swarma/gateway.units` | Units of a model or gateway budget | Not stated here | Not stated here | Not stated here | "Model requests", "Model tokens", "Model cost" or "External service cost" |

Three rules of the cited texts hold for every kind and are **restated**: an
allowance of zero authorizes nothing, a missing limit refuses and never
becomes unlimited access (LIP-0008 section 2), and a limit key for which a
grant or a row states no limit has the ceiling 0 (LIP-0026 R5.2). A grant
that allows `swarma/session.start` and states no limit of the kind
`swarma/session.concurrent` therefore starts nothing.

The kind `swarma/gateway.units` is in the list because the grant-side
proposal names it. This draft gives it no arithmetic and recommends against
it as a limit of this profile (Q5). A budget belongs to its executor
(LIP-0008 section 4: "A budget belongs to that executor"), and W11.4 gives a
grant one executor: "a second executor takes a second grant" (LIP-0020
section 11, opening text). The model
budget of a session is consumed at the model service, which is another
executor than `X`. `X` cannot count it, and a limit that its executor cannot
count bounds nothing.

The texts of `resource` and `unit` of each limit are not proposed. The table
states the unit as a meaning. N3 holds the need.

The contract mirrors every limit of the grant, and a mismatch refuses
(LIP-0008 section 2; **restates**). How a contract writes the three kinds is
open with the contract profile.

### 3. Where each field lives

The rows are the fields of a start (A.1 to A.9) and the nine points of a kept
session (B.1 to B.9), as the dispatching side lists them. No cell is empty: a
cell that does not apply says "none" and why.

| Field | (a) Carried by the grant | (b) Carried by the host's signed policy or the station contract (out of this specification) | (c) Derived | (d) The executor's check and its refusal | (e) Status |
| --- | --- | --- | --- | --- | --- |
| A.1 Receiver: which host acts | `executor`, name and key (W11.4) | The pin of the key of `X` at its callers and the transport of `X`: the executor profile: "Exact key/transport encoding remains open" (LIP-0008 section 4) | None: the value is read from the grant and compared | The service name and public key of `X` equal the executor of the grant and of the request (LIP-0008 section 4, step 4). Refusal: that of the step, for which the base assigns no v4 code (N2); under a child `CHILD_AGENT_NOT_ALLOWED` (LIP-0026 R2.2) | Defined by LIP-0020 W11.4 and LIP-0008 section 4; the v4 code is open (N2) |
| A.2 Agent account and its generation | `recipient` names the agent (W11.3). None for the account or its generation: a grant has no path on a host and no member for one (W11.2) | The table of the host that maps a recipient to one managed account at its current generation. The account exists before the start and is not created by it | The account and the generation, from the recipient through that table | The table holds exactly one account for the recipient that step 2 authenticated, at its current generation. Refusal: `AGENT_SESSION_ACCOUNT` | Proposed here (AS4.4); the table is out of this specification |
| A.3 Who may ask | None: a grant names a recipient and no caller (W11.2) | The table of the key holder with the `use` list of each origin (LIP-0013 J7.2, J7.3 (a)), and the host's rule for local callers | The origin of the run (LIP-0013 J7.1; LIP-0029 O6.5) | `X` authenticates the request under the recipient mode of `G` (LIP-0008 section 4, step 2) and its peer (step 5). It cannot verify the gate of the key holder and treats no flag or label as evidence of it (LIP-0013 J7.7). Refusal: that of step 2 | Restates LIP-0008 section 4 and LIP-0013 J7 (Draft, agreement pending); the reading is open (Q1) |
| A.4 What runs: the pins of the plan | `contract`: the contract carries the hash of the agreed configuration manifest (LIP-0017 section 8, rule 1). None for a pin in the grant itself: a grant has "no typed constraint of an action beyond its limits" (W11.2) | The catalog of the configurations that the host admits, addressed by content; no path, URL or wildcard | The hash that the launcher recomputes "from what it is about to start" (LIP-0017 section 8, rule 3) | The `configuration` of the request equals the hash that the contract of `G` carries, and the launcher reproduces it; otherwise nothing starts. Refusal: `AGENT_SESSION_PLAN` | Proposed here, on LIP-0017 section 8, which is a draft's proposal. Open: how `X` obtains the contract (N4) |
| A.5 Local policy, window and bounds | `not_before_height`, `not_after_height` (W11.2). `limits` of the kind `swarma/session.span`. None for a policy identifier or its revision: no member exists (W11.2) | The identifier and revision of the host's policy; the bounds to detect an end and to stop a process; a local ceiling on the lease. A local ceiling lowers and never raises (LIP-0008 section 2: operator configuration "never increases a rental ceiling") | The usable window, which is the intersection of the windows of the links (LIP-0008 section 7.1, rule 4); the lease end `E` from the request | `not_before_height <= H < not_after_height` for every link (section 7.1, rule 2; section 12.5); `H < E`, `E - H` within the span, and `E` at most every `not_after_height`. Refusal: for the window that of LIP-0008 section 4, step 4, with no v4 code in the base (N2); for the lease `AGENT_SESSION_SPAN` | The window is defined by LIP-0008 section 7.1 and LIP-0020 W11.9; the lease and the span are proposed here |
| A.6 Entry: model, reasoning effort, prompt, timeout | None: a grant has "no text and no hash of a text" and no typed constraint (W11.2) | The strings of the model catalog, the largest size of a prompt and the timeout of an entry | The model selection where the agreed configuration fixes it (A.4); none otherwise | None on the text: `X` decides nothing from a prompt and passes it to the agent unchanged ("Text always governs an agent's work and never a service's effect", LIP-0006 section 7, with its rule 2; LIP-0029 O1.2). Refusal: none of this profile | Restates LIP-0006 section 7 and LIP-0029 O1.2. Open: whether the start request binds a hash of the first text (Q10) |
| A.7 Identity of the run | None: a grant has "no stated identifier of itself" (W11.2); its identifier is recomputed (LIP-0020 W6.1, W6.3) | The local identifiers of an effect, of an execution and of a controller epoch in the journal of `X` | The session identifier, which is the identity of the request that opened the session (AS4.5); the request identity, which is the nonce field of the invocation (LIP-0008 section 12.1) | The identity of the request is not in the journal of `X`. Refusal: `AGENT_SESSION_REPLAY`. One request identity holds at most one reservation (LIP-0026 R5.7) | Proposed here, on the model of LIP-0028 T2.6 and T3.2. Open: the journal key of a request (LIP-0020, "What can be built") |
| A.8 Origin of the admission | The proof path: `G`, and for a child its `parent` and `ordinal` (W11.2); `recipient` | The key holder's record of a run and its origin, outside the agent's write authority (LIP-0013 J7.1) | The ordered proof identifiers of the invocation (LIP-0008 section 12.1) | Every link passes its own checks at use (LIP-0008 section 12.2). `X` verifies the grant against its own view of the chain and puts no prepared binding in the place of that verification (LIP-0008 section 5). Refusal: that of the check that fails | Restates LIP-0008 sections 5 and 12 |
| A.9 Isolation | None: a grant has no member for a slot or an account (W11.2) | One live session for one account; the proof that an account holds no process before it is used again | The slot binding, which is the user id of the account (AS1.3) | The account holds no live session of another recipient, and the process of the agent holds no key or right of an effect (LIP-0029 O1.6). Refusal: `AGENT_SESSION_ACCOUNT` | Proposed here, after LIP-0028 T7.7 and LIP-0029 O1.6; the proof of an empty account is out of this specification |
| B.1 Session identity | None as a member. The record of the session binds the identifier of `G`, the proof path and the recipient | How the identifier is shown to local tools | The session identifier of A.7. It is the same from the first start to the end, across restarts | A renew, a stop and a restart name a session that the journal holds for their own proof path and executor. Refusal: `AGENT_SESSION_UNKNOWN`. A restart consumes one start of `swarma/session.starts`, no further claim of `swarma/session.concurrent` and no lease | Proposed here, on the model of LIP-0028 T5.3 |
| B.2 Lifetime | The two heights of the window; `swarma/session.span`; the text `swarma/session.renew` in `actions` | The procedure of a renewal and how many blocks before `E` it is asked | The lease end `E` | At every keep check `H < E` and `H` lies in the window of every link; otherwise the session ends (AS5.4). Refusal of a later request: `AGENT_SESSION_ENDED` | The comparison of heights restates LIP-0008 sections 7.1 and 12.5; the lease and the end are proposed here (section 6) |
| B.3 Restart | `swarma/session.starts` caps the starts; the text `swarma/session.start` in `actions` | When a restart is asked, how many times, with what backoff, and whether the same account and home are used again | The count of starts, from the accounts of `X` | A restart is a signed start request that names a live session, and `X` makes every check of a start again (AS4.6). Refusal: `OWN_LIMIT_OVER`, `ROW_CAP_OVER` (LIP-0026 R5.6), or that of the check that fails | Proposed here; Q6 holds the restart without a signed request |
| B.4 Liveness | None: a grant has no interval of liveness and no member for one (W11.2) | What "alive" means, the interval of a heartbeat, and who acts on silence | None: nothing of it follows from the chain or from a grant | None of this profile: silence is no event of section 5. `X` may end a session that it finds dead, as it may end any session (AS5.7), and it journals that end. Refusal: none | Not decided here (section 7) |
| B.5 Follow-up work | None: the grant of a session authorizes the start and the keeping, and no later instruction. A grant has no key for messages (W11.2) | The channel on which later instructions reach the agent, and its binding to the session | The origin of the run, which never changes (LIP-0013 J7.1) | An instruction is admitted under the grant that it cites, at the gate that admits instructions, and one that was admitted under another grant does not enter the run (LIP-0013 J7.6). The gate hands an instruction to a session only while `X` reports it live and not suspended (AS5.6). Refusal: that of the instruction's own admission | J7.6 restates LIP-0013 (Draft, agreement pending); AS5.6 is proposed here |
| B.6 Revocation while running | `seal` (LIP-0008 SB1); for a child the stop coin of its row, the `stop` of its range (W11.6). None for the seal of the recipient's entry at its landlord: a grant has "no holder of a landlord" (W11.2) | The bound within which a process is stopped after an end is journaled; whether the deployment reads its node itself or through a gateway that shows only the state of a seal | The outpoints that `X` watches for a live session (AS5.3) | The events of section 5. A durable record that refuses the path ends the session. Refusals: `ROW_CLOSED_FOR_CAUSE` (LIP-0027), `HOLDER_REVOKED` (LIP-0010), the refusal of a closed grant (LIP-0008 section 5.1), `ISSUER_NAME_CLOSED` (section 5.3, EB6) | The closures restate the cited texts; that they end a running session is proposed here |
| B.7 Lease of a credential and of a gateway | None in this grant. The grant-side proposal names `swarma/gateway.units`; this draft does not adopt it (section 2.3) | How the lease of a model credential and of a gateway token is taken and renewed | None | None: a refusal at another executor is no event of section 5. A harness that lost its bearer cannot read a new one (LIP-0028 section 5), so its process is started again by a restart (B.3) | Open (Q5) |
| B.8 Home and state | None: a grant has no path on a host (W11.2) | Where the state of a session lives across restarts; the export of the work before a home is removed; the quarantine of an account until it is shown empty | None | None | Not decided here (section 7) |
| B.9 Capacity | `swarma/session.concurrent` | The ceilings of the operator and how a host claims capacity. An operator's ceiling lowers and never raises (LIP-0008 section 2) | The number of live sessions, from the journal of `X` | The claim is part of the atomic write of a start and lasts until the journaled end. Refusals: `AGENT_SESSION_CONCURRENT` for the limit of the grant or of a row, `AGENT_SESSION_CAPACITY` for a ceiling of the operator. Every end of section 5 releases the claim, and `X` may end a session to take its capacity back (AS5.7) | Proposed here |

### 4. The start

`X` runs the steps in this order and stops at the first refusal. A refused
request reserves nothing, claims nothing and starts nothing.

| # | Step | Which observation | Refusal | Mark and source |
| --- | --- | --- | --- | --- |
| 1 | The journal of `X` is intact and can be written | None: before any read of the chain | `JOURNAL_LOST`, `JOURNAL_FENCED` (LIP-0025) | **Proposed here** as a first step, as LIP-0027 H2.1 and LIP-0010 section 10.6, step 0, have it |
| 2 | The request and every grant of its proof path are read as signed objects: the pipeline of LIP-0020 W9.1, with W11.8 to W11.10 for a grant | None | The code of the pipeline | **Restates** for a grant. **Open** for the invocation, which has no members (N1) |
| 3 | `X` opens one observation: its reads begin and end with a read of the tip, it asks every comparison node, and it reads its clock after the last read. The observation is on the pinned chain and healthy, the clock holds, and the tip is not too old for the class of the action | The observation of the start, which this step opens (LIP-0022 B1.1, B1.3, B2.5, B3.1 to B3.3, B3.6) | `OBSERVATION_CHAIN`, `OBSERVATION_VOID`, `NODE_UNHEALTHY`, `NODE_DISAGREEMENT`, `OBSERVATION_CLOCK`, `TIP_AGE`, in this order and before every rule of a grant (LIP-0022 B6.1) | **Restates** LIP-0022 (a draft's proposal); the class is that of section 2.2 |
| 4 | Steps 1 to 4 of LIP-0008 section 4 for every link of the path, the root first, and the checks of section 12: the names and the walk of the issuer's name; the request under the recipient mode; the closure journal; the window against `H`; the committed recent block, before every rule that uses its height (LIP-0022 B6.2); the confirmed issuance; the seal, unspent with the mempool included; the exact action in `actions`; the executor. Then `iat <= now < exp` (section 12.5) | The same observation: every fact of one admission comes from one observation (LIP-0022 B1.5) | The refusal of the check that fails | **Restates** LIP-0008 sections 4, 7.1 and 12 and LIP-0022 B1.5 |
| 5 | Under a child: the row of its ordinal (LIP-0026 R2.1 to R2.4), the coin of the row (R3.2 to R3.4), the stop coin of the row (LIP-0027 H2.1 to H2.6), the attestation where the row names a certifier (LIP-0014 section 8), and, where the row names its recipient by a class, the checks of the class with the read of the landlord's list and of the seal of the recipient's entry (LIP-0026 section 9; LIP-0010 section 10.6) | The same observation (LIP-0022 B1.5; LIP-0010 H44) | The codes of those sections, in their order | **Restates** |
| 6 | The request is new, the session that a restart names is live, the account is the recipient's and holds no session of another recipient, the configuration is the one of the contract, and the lease lies within the span and the windows (AS4.2 to AS4.4, AS4.6) | None: the journal and the policy of `X`, and `H` of the observation | `AGENT_SESSION_REPLAY`, `AGENT_SESSION_UNKNOWN`, `AGENT_SESSION_ENDED`, `AGENT_SESSION_ACCOUNT`, `AGENT_SESSION_PLAN`, `AGENT_SESSION_SPAN`, in this order | **Proposed here** |
| 7 | The ceilings of the operator and the capacity of the host | None | `AGENT_SESSION_CAPACITY` | **Restates** LIP-0008 section 4, step 5, for the ceilings; the code is **proposed here** |
| 8 | Immediately before the write, `X` reads the tip and its clock again. A tip that is not the tip of the observation voids the admission. With the new reading it applies LIP-0022 section 3 and the window again; for a child of a class row it also makes the reads of LIP-0010 H44 again | The recheck of LIP-0022 B1.6 | `OBSERVATION_VOID`, `OBSERVATION_CLOCK`, `TIP_AGE`; the codes of LIP-0010 H44 | **Restates** LIP-0022 B1.6 and LIP-0008 section 12.5 |
| 9 | One atomic write of the journal (AS4.5) | None | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` (LIP-0026 R5.6); `AGENT_SESSION_CONCURRENT`; `AGENT_SESSION_ENDED` where a restart finds an end; the refusal of the closed grant where a closure stands | **Proposed here**, on the model of LIP-0028 T4.6 and LIP-0026 R5.6 |
| 10 | The effect: `X` starts the process in the slot, after the write is complete | None | None: a start that fails or whose outcome is unknown keeps its record and its reservations until it is reconciled | **Restates** LIP-0025 M3.2 for the order and LIP-0008 section 2 for the uncertain effect |

| Rule | Requirement | Mark and source |
| --- | --- | --- |
| AS4.1 | The start request is a signed invocation (LIP-0008 section 12.1) whose command is the start text. `X` admits it as it admits any invocation, with every check of LIP-0008 sections 4 and 12, in one healthy observation. | **Proposed here**, in the words of LIP-0028 T2.1 and T2.5 for its own request |
| AS4.2 | `X` records the identity of a start, a renew and a stop request when it admits the request, and it admits no request whose identity its journal holds. | **Proposed here**, after LIP-0028 T2.6. `AGENT_SESSION_REPLAY` |
| AS4.3 | The `configuration` of a start request equals the hash of the agreed configuration that the contract of `G` carries. `X` starts exactly that configuration. | **Proposed here**; the second sentence restates LIP-0017 section 8, rule 3. `AGENT_SESSION_PLAN` |
| AS4.4 | The `lease_end_height` of a start request is higher than `H`, at most `H` plus the amount of `swarma/session.span`, and at most the `not_after_height` of every link. Under a child the smaller span of the child and of its row holds. `X` shortens no request: a lease end outside these bounds refuses. | **Proposed here**. `AGENT_SESSION_SPAN` |
| AS4.5 | The write of step 9 is one atomic step of the journal, or nothing: the reservation of one start in the accounts of `swarma/session.starts`, the own account before the row account (LIP-0026 R5.6); the claim of `swarma/session.concurrent`; and the record of the session with its identifier, `G` and the proof path, the key under which `X` authenticated the request, the account, the configuration and the lease end. The identifier of a session is the identity of the request that opened it. The same step reads that no grant of the proof path has a closure. | **Proposed here**, after LIP-0028 T3.2 and T4.6 |
| AS4.6 | A restart is a start request that states `session`. The session is live and belongs to the proof path and the executor of the request. `X` makes steps 1 to 10. The write reserves one start, claims nothing further, and changes neither the identifier nor the lease end of the session; the same step reads that the session has no end. | **Proposed here**; Q6 |
| AS4.7 | A session starts in an account that holds no live session of another recipient, and while it lives `X` starts no session of another recipient there. | **Proposed here**, after LIP-0028 T7.7, which states the same for the key holder and a slot |

The key holder of the recipient signs the three requests. Under LIP-0013
J7.3 (a) it signs an invocation for a run only where every grant of the proof
path is in the `use` list of the origin of that run, and a run that is
resumed has the origin of the run that it comes from (J7.1). A restart
therefore needs no new origin. `X` cannot observe that gate (J7.7). The start
of a first run raises a question that J7 does not answer: the key holder
binds a run to its origin "when the run is created", and here it signs the
request that creates the run. The draft reads the record of the run as made
by the key holder before it signs; that reading belongs to LIP-0013 and is
listed as N5.

### 5. The kept session

A start is admitted once. What keeps the admission honest afterwards is the
keep check, which is the check of LIP-0028 T4.5 applied to a session that
makes no reservation of its own.

| Rule | Requirement | Mark and source |
| --- | --- | --- |
| AS5.1 | In a **keep check** `X` makes the checks of LIP-0008 sections 4 and 12 for the proof path of a live session, and of step 5 of section 4 of this draft where they apply, in a healthy observation of its own. No signature is verified. In its place `X` requires that the key under which it authenticated the last signed request of the session is still the key of step 2 of LIP-0008 section 4: the signed request key of `G`, or, for a recipient by name, the key that the name yields at that moment. | **Proposed here**, in the words of LIP-0028 T4.5 |
| AS5.2 | `X` makes a keep check for a live session at three points: before it admits a renew, a restart or a stop request for it; before it reports the session live to a gate that asks (AS5.6); and at every new tip that its reading node shows. | **Proposed here**. LIP-0022 "fixes no interval between observations, and the question is open" (its section 3) |
| AS5.3 | While a session is live, the node of `X` watches, with its mempool included, the seal of every grant of the proof path, the stop coin of the row of a child, and, for a child of a class row, the seal of the recipient's entry. When it shows one of them spent, `X` makes a keep check at once. How often the mempool is read is open (Q9). | **Proposed here**, after LIP-0029 O8.3, which has an own executor's node watch the seal of every device of its list |
| AS5.4 | A session ends with the first of these: a keep check finds `H` at or above the lease end `E`, or outside the window of a link; `X` records a closure or another durable refusal for its proof path (the rows of the table below); `X` admits a stop request for it; `X` admits an owner's command that stops it; or `X` ends it under AS5.7. `X` writes the end into its journal when it first finds it. From that record on no request reopens the session, whatever a later chain shows. | **Proposed here**, after LIP-0028 T5.4 and T5.6. "An effect that was already performed is not undone" by a reorganisation that lowers `H` (LIP-0008 section 7.1), and neither is an end |
| AS5.5 | A refusal that leaves no durable record ends no session. The session is suspended: `X` admits no renew and no restart for it and reports it as not live to a gate. The next keep check that passes lifts the suspension. | **Proposed here**, after LIP-0028 T5.7. Q8 holds the alternative |
| AS5.6 | A gate that hands instructions to an agent hands one to a session only while `X` reports that session live and not suspended. | **Proposed here**. The admission of the instruction itself is not changed (LIP-0013 section 3; LIP-0029 section 11) |
| AS5.7 | `X` may end a session at any time under the policy of its operator, and it journals that end. It never keeps a session beyond an end of AS5.4, and it never moves a lease end without an admitted request. | **Proposed here**. An operator may "refuse service" and never raises a ceiling (LIP-0008 section 2) |
| AS5.8 | After the end is journaled, `X` stops the process of the session. The time that this takes is a bound of the station contract. It is no grace of authority: from the record of the end on, nothing is admitted for the session. | **Proposed here**. No grace is added to a window, in blocks or in clock time (LIP-0008 sections 7.1 and 12.5) |

**The largest delay.** Four quantities make up every delay of the table.

| Name | What it is | Bound |
| --- | --- | --- |
| `D_node` | The time until the transaction or the block that carries the event reaches the node of `X` | None. "Each act takes effect at a verifier that has validated its transaction, and not at one that has not" (LIP-0008 section 5.3). For a confirmed fact it is the time until the node of `X` has the block |
| `D_watch` | The time from the node of `X` showing the event to the keep check that reads it | For a fact in a block: none beyond the block itself, because a keep check follows every new tip (AS5.2). For a fact in the mempool alone: **open** (Q9) |
| `D_stop` | The time from the journaled end to the stopped process | A bound of the station contract, out of this specification (AS5.8) |
| The lease bound | The blocks from an event that only suspends a session to its end | At most the amount of `swarma/session.span`: a suspended session admits no renew (AS5.5), so it ends at its lease end `E`, which lies at most one span above the height of its last admitted start or renew (AS4.4, AS6.1) |

The lease bound counts blocks of the node of `X`. While that node receives
no block, `H` does not advance and no lease end is reached: "While no block
arrives, `H` does not advance and the window does not close" (LIP-0008
section 7.1). Q8 holds what a session does in that state.

| Event | The cited rule | What `X` does to a running session (**proposed here**) | Largest delay |
| --- | --- | --- | --- |
| The grant expired: `H` reached the `not_after_height` of a link | LIP-0008 section 7.1, rule 2; section 12.5: at `H == not_after_height` "new admission MUST refuse; an expired middle link is sufficient" | Ends the session (AS5.4) | 0 blocks at `X`: the keep check at the first tip of that height. In time, `D_stop` |
| The lease ran out: `H` reached `E` | AS4.4, AS6.1 (**proposed here**) | Ends the session | The same |
| The grant was revoked: a validated issuer spend of the seal of `G` or of its parent | LIP-0008 section 5.1: the executor "MUST persist permanent closure before any further admission"; section 12.2: "an invalid or closed ancestor MUST refuse the dependent request" | Records the closure and ends every session whose proof path holds that grant, before it admits anything further, as LIP-0028 T5.6 has it for its sessions | `D_node` + `D_watch` + `D_stop`. `D_node` has no bound |
| A spend of that seal that `X` cannot validate as the issuer's | LIP-0008 section 5.1: "refuses admission without asserting that an issuer revocation has been proved" | Suspends the session (AS5.5) | The lease bound |
| The issuer's name was broken by its owner | LIP-0008 section 5.2 (J6, Draft, agreement pending); section 5.3, EB6, `ISSUER_NAME_CLOSED` | Where `X` holds that closure: ends every session under a grant of that issuer. Until J6 is agreed: the name rule refuses without a journaled closure, and the session is suspended | With the closure: `D_node` + `D_watch` + `D_stop`. Without it: the lease bound |
| The seal of the recipient's entry at its landlord was spent, for a child of a class row | LIP-0010 section 10.6, step 8, and section 10.7: `HOLDER_REVOKED` with a durable closure at a verifier that validated the spend | Ends the session | `D_node` + `D_watch` + `D_stop` |
| The same seal is not shown unspent and `X` validated no spend, or `X` reads seal states through a gateway | LIP-0010 section 10.6: `HOLDER_SEAL_NOT_LIVE` leaves nothing behind; H50, the non-witness, which "records no enforcement closure" (in the words of LIP-0029 section 8.1, which points to H50) | Suspends the session | The lease bound |
| The list of the landlord's agents changed and no longer holds the recipient's entry | LIP-0010 H40, point 4, and H41: the take of the list writes a removal mark of the entry, and step 6 then refuses as `CLASS_HOLDER`. Only a confirmed pin counts (section 11, SH3) | Where the keep check took the list and wrote the mark: ends the session. Where `X` does not hold the octets of the pinned list (`LIST_UNKNOWN`): suspends it | With the mark: 0 blocks after the name update confirms at `X`, plus `D_stop`. Without the list: the lease bound |
| The list changed and still holds the entry | LIP-0010 section 10.4: a change of the list "does not end the child, and it does not end its parent" | Nothing | None: no event |
| The owner of the recipient's name changed, or another key wrote its value | LIP-0010 H34: the entry "stops admitting from the block of the transfer, with no closure"; LIP-0008 section 4, steps 1 and 2 | Suspends the session | The lease bound |
| The row was stopped: the stop coin of the row of a child is spent | LIP-0027 H2.4 and H3.4: `ROW_CLOSED_FOR_CAUSE`, written "before any further admission", permanent at that verifier | Ends every session whose final grant is a child of that row. A session under another row of the same parent is untouched (H3.5) | `D_node` + `D_watch` + `D_stop` |
| The stop coin is not on the active chain as the row states it | LIP-0027 H2.6: `ROW_STOP`; the verifier "writes no closure for it" | Suspends the session | The lease bound |
| The attestation of a child was withdrawn | LIP-0014 section 8, step V18: `NOTARY_WITHDRAWN` where the notary's seal is spent or the journal holds a withdrawal | Where the journal of `X` holds the withdrawal: ends the session. Otherwise suspends it | With the record: `D_node` + `D_watch` + `D_stop`. Otherwise the lease bound |
| The owner stops the session by a command | LIP-0029 section 11: an owner command to an own executor, whose class is a leaf of the action registry (O2.1) and whose level the policy assigns (O6.4) | Ends the session named in the fields of the command. The class is the stop text; its level is open in LIP-0029 ("the level of a stop and of resumption") and here (Q11) | From the delivery of the command: `D_stop`. The command depends on no block |
| A device of the owner was revoked | LIP-0029 O8.4: `X` "refuses every envelope signed by the key of that device". No cited rule speaks of a run that such a device started | **Open** (Q11) | **Open** |
| The recipient asks for a stop | The stop request of section 2.2 | Ends the session. A stop request that `X` refuses ends nothing | `D_stop` after the admission |
| The observation of `X` is not healthy, or its tip is too old | LIP-0022 B2.5, B3.6: the verifier refuses, "and nothing is recorded as closed" | Suspends the session (AS5.5) | The lease bound, in blocks that the node of `X` does not receive: **open** (Q8) |
| The journal of `X` is lost | LIP-0025 M5.1; LIP-0008 J6.9: a verifier whose closure journal is lost "is a newcomer" and "MUST NOT admit before the journal is recovered or its owner has started it anew" | A journal that is started anew holds no session. Every session of the lost journal has ended for `X`, and its process is stopped | `D_stop` after the loss is found |

One principle orders the table. A session ends when the journal of `X` gains
a durable record that refuses its path, or when the heights run out. A
refusal that leaves nothing behind suspends the session, and the lease bound
then ends it. `X` is a witness in the sense of LIP-0008 section 5.3 for what
its node validated, and for nothing else.

### 6. Renewal and expiry

Every quantity of this section is a block height. No rule compares a height
with a clock (LIP-0008 section 12.5: "Heights and clock times are never
compared with each other"). The `iat` and `exp` of each signed request stay
in clock time, as LIP-0008 section 7.1 has it for every invocation; they
bound the admission of that one request and no part of a lease.

| Rule | Requirement | Mark and source |
| --- | --- | --- |
| AS6.1 | The renew request is a signed invocation with the renew text. It names a live session of its own proof path and executor and states a new `lease_end_height`. `X` admits it as AS4.1 and AS4.2 say, after a keep check, and applies AS4.4 to the new lease end with the `H` of that observation. The lease end becomes the higher of the one that stands and the new one, and the key of AS5.1 becomes the key under which `X` authenticated this request. `X` writes both before it answers, in one atomic step with the read that the session has no end. Nothing else of the session changes. | **Proposed here**, in the words of LIP-0028 T5.2 |
| AS6.2 | A lease end never lies above the `not_after_height` of a link. A session is therefore never live at the closing height of its grant, however often it is renewed. | **Proposed here**; the bound restates LIP-0008 section 7.1, rules 2 and 4 |
| AS6.3 | Who may renew a lease: the recipient, through its key holder, under a grant whose `actions` hold the renew text. The key holder renews only while the run lives and its origin still lists every grant of the path. | **Proposed here**; the second sentence restates LIP-0013 J7.3 (a) |
| AS6.4 | A grant is not extended. A new term is a new grant, with a new seal and a new issuance. Who may issue it: the issuer of a root grant, with the consent that LIP-0020 section 7 asks of the recipient; for a child, the holder of the delegation key of a parent, under a row that admits a new child (LIP-0026 section 2). | **Restates** LIP-0008 section 2.1 ("Each grant ... ends at `not_after_height`") and section 5.3, EB6 ("a stopped grant comes back only as a new grant with a new seal") |
| AS6.5 | At the closing height of its grant a session ends (AS5.4). A session under a successor grant is a new session, opened by a start request under that grant, with a new identifier. | **Proposed here**, from AS1.2; Q7 holds the alternative |
| AS6.6 | When the lease end, or the closing height of the grant, comes near, the session's side acts in blocks: the key holder sends the renew request a number of blocks before `E` that the station contract states, and the successor grant is issued so that its anchor is confirmed before the closing height. This draft proposes no number. | **Proposed here** as a duty without a number, as LIP-0028 T7.6 has "well before the end" |
| AS6.7 | A renew request that reaches `X` at or after the lease end finds no live session and refuses. The process is started again by a new start request, which opens a new session. | **Proposed here**, after LIP-0028 section 5. `AGENT_SESSION_ENDED` |

Three facts of the cited texts bound the lead of AS6.6. A renew request needs
a healthy observation at `X` (AS5.1), so an outage of `X` or of its nodes
that lasts longer than what is left of a lease ends the session. A successor
grant may open its window before the old one closes, but not below the
height of its own recent block (LIP-0008 section 7.1, rule 3). And its
issuance anchor is confirmed above that recent block within `K` blocks,
proposed as 432 (LIP-0022 B4.3). A window has no exact length in clock time
(LIP-0008 section 7.1), so a lead that is stated in blocks is the only lead
that a verifier can check.

The cost of AS6.5 is one restart of a long-lived agent at each term of its
grant. LIP-0008 section 2.1 gives about 13,000 blocks as the term of three
months.

### 7. What this profile does not decide

These belong to the station contract, out of this specification. They are
named here once.

- How many times a process is restarted and with what backoff. The grant
  caps the starts (`swarma/session.starts`) and decides nothing else of it.
- What "alive" means, the interval of a heartbeat, and who acts on silence.
- The layout of a home, where the state of a session lives, the export of
  the work before a home is removed, and the quarantine of an account.
- The bounds within which an end is detected and a process is stopped
  (`D_stop`), and how often the mempool is read (Q9).
- The table that maps a recipient to an account and its generation, and how
  an account is created.
- The channel on which instructions reach an agent, and its binding to a
  session.
- The lease of a model credential and of a gateway token.
- The catalog of models, the largest size of a prompt and the timeout of an
  entry.
- How a host claims capacity, and the ceilings of its operator.

### 8. Refusals and their order

All eight codes are **proposed here**. Their prefix differs from the
`SESSION_` codes of LIP-0028 on purpose.

| Code | What it reports | Rule |
| --- | --- | --- |
| `AGENT_SESSION_REPLAY` | The identity of a start, a renew or a stop request is already in the journal | AS4.2 |
| `AGENT_SESSION_UNKNOWN` | A renew, a stop or a restart names no session of its proof path and executor | AS4.6, AS6.1 |
| `AGENT_SESSION_ENDED` | The session that a request names has ended | AS4.6, AS5.4, AS6.7 |
| `AGENT_SESSION_ACCOUNT` | The host maps the recipient to no account at its current generation, or the account holds a live session of another recipient | AS4.7; table rows A.2 and A.9 |
| `AGENT_SESSION_PLAN` | The configuration of the request is not the one that the contract of the grant carries, or the launcher cannot reproduce it | AS4.3 |
| `AGENT_SESSION_SPAN` | The lease end is not above `H`, is more than the span above it, or lies above the closing height of a link | AS4.4, AS6.1 |
| `AGENT_SESSION_CONCURRENT` | A start would exceed the limit `swarma/session.concurrent` of the grant or of its row | AS4.5 |
| `AGENT_SESSION_CAPACITY` | A ceiling of the operator or the capacity of the host refuses the start | Section 4, step 7 |

AS8.1. For a start request the order is that of the table of section 4. For
a renew request it is: steps 1 to 5 of that table; `AGENT_SESSION_REPLAY`,
`AGENT_SESSION_UNKNOWN`, `AGENT_SESSION_ENDED`, `AGENT_SESSION_SPAN`; step 8.
For a stop request it is the same without `AGENT_SESSION_SPAN`. (**Proposed
here.**)

AS8.2. None of the eight records a closure of a grant. The end of a session
is a record of `X` about its session, as LIP-0028 T8.4 says of its own
codes. (**Proposed here.**)

The refusals of LIP-0008 section 4, steps 2 and 4, have no v4 code in the
base of this draft: an action text that the profile does not define, a
window that `H` lies outside, an executor that is not `X`. This draft
assigns none and writes "the refusal of that step" (N2).

### 9. Cases

The cases state outcomes in words, each with a control that is admitted.
Vectors come with the members of the invocation.

| Case | Setting | Outcome |
| --- | --- | --- |
| S30-1 | A valid start request under a grant with `swarma/session.concurrent` 1, `swarma/session.starts` 5 and `swarma/session.span` 144; the lease end is `H` plus 144 | Admitted. The journal holds the session, one start is reserved and one session is claimed |
| S30-2 | The same with a lease end of `H` plus 145; with a lease end of `H`; with a lease end one above `not_after_height` | `AGENT_SESSION_SPAN` for each. A lease end equal to `not_after_height` within the span is admitted, and the session ends at that height |
| S30-3 | A grant that allows the start text and states no limit of the kind `swarma/session.concurrent` | `AGENT_SESSION_CONCURRENT`: the ceiling is 0 (LIP-0026 R5.2). With the limit at 1 the start is admitted |
| S30-4 | A second start under the grant of S30-1 while the first session lives | `AGENT_SESSION_CONCURRENT`. After the first session ended, the second start is admitted |
| S30-5 | A restart of the session of S30-1, five times | The first four are admitted; the fifth refuses as `OWN_LIMIT_OVER`, because the first start and four restarts filled the account. The session identifier and the lease end are those of S30-1 throughout |
| S30-6 | A start request whose `configuration` differs from the hash in the contract by one profile | `AGENT_SESSION_PLAN`, and nothing starts. With the hash of the contract the start is admitted |
| S30-7 | The request of S30-1 once more | `AGENT_SESSION_REPLAY`; no second session |
| S30-8 | A renew request 100 blocks after the start, with a lease end 144 above the tip | Admitted; the lease end moves. A renew request at the lease end: `AGENT_SESSION_ENDED` |
| S30-9 | The seal of `G` is spent, and the node of `X` shows the issuer's spend in its mempool. A second session at `X` belongs to another grant | `X` records the closure and ends the session of `G`. A later renew request refuses as `AGENT_SESSION_ENDED`. The second session is untouched |
| S30-10 | The tip of the node of `X` is too old | The keep check refuses under LIP-0022, and the session is suspended. It ends nothing. A keep check after a new block lifts the suspension |
| S30-11 | A session under a child of row 3. The stop coin of row 3 is spent; a session under a child of row 4 runs at the same host | The session of row 3 ends (`ROW_CLOSED_FOR_CAUSE`). The session of row 4 stays |
| S30-12 | A reorganisation lowers `H` below the lease end after `X` journaled the end at `E` | The session stays ended. A new start request under the same grant, while its window is open, is admitted and opens a new session |
| S30-K1 | A known limit. The issuer spends the seal, and the transaction has not reached the node of `X` | The session runs until the node shows the spend. Nothing bounds that time (LIP-0008 section 5.3) |
| S30-K2 | A known limit. The node of `X` receives no block | `H` does not advance, and no lease end is reached. The session is suspended and does not end (Q8) |

## Sources

No service, no key holder and no node was run for this draft.

| Statement | Source |
| --- | --- |
| The members of a grant, the open registries, the forms of a limit | LIP-0020 section 11, W11.2 to W11.4, W11.6, W11.8 to W11.10 |
| The order of an admission, the executor, the budget of an executor, the operator's ceilings | LIP-0008 sections 2 and 4 |
| The closure of a spent seal, the break of an issuer's name, the window of a stop | LIP-0008 sections 5.1, 5.2 and 5.3 |
| The window in heights, the invocation, the proof path, the time terms, the namespace | LIP-0008 sections 7.1, 12.1, 12.2, 12.3 and 12.5 |
| The observation, the comparison nodes, the clock, the classes and the order of refusals | LIP-0022 sections 1 to 3 and 6 |
| Rows, the fit of a child, the accounts | LIP-0026 sections 1, 2 and 5 |
| The stop coin of a row and its closure | LIP-0027 sections 1 to 3 and 5 |
| The list of a landlord's agents, the seal of an entry, the take of a list | LIP-0010 sections 10.4, 10.6 and 10.7, and section 11 |
| The session for a client that cannot sign, whose rules are the model of several rules here | LIP-0028 sections 1 to 8 |
| The owner's command, the registry, the levels, the device seal | LIP-0029 sections 1, 2, 6, 8 and 11 |
| The gate of the key holder | LIP-0013 section 3.6, J7.1 to J7.8 |
| The agreed configuration | LIP-0017 section 8 |
| What a proposal for an action name and for a limit kind states | LIP-0018 sections 2 and 3 |
| The candidate service types | LIP-0007 section 1 |
| The fields of a start and the nine points of a kept session; the proposed action names and limit kinds | Two working inputs to this draft, from the dispatching side of a host and from the side that checks grants. Neither is part of this repository |

## Alternatives

- **The lease in seconds on the clock of the executor,** as LIP-0028 has its
  window. A lease would have an exact length, and a node without blocks could
  not hold a session open. The owner's direction excludes a clock for a
  session and its renewal.
- **No lease: a session lives for the whole window of its grant.** No renew
  request would be needed. A session whose keep check is refused without a
  record would then run to the end of the grant, which is thousands of
  blocks, and the lease bound of section 5 would not exist.
- **A bearer for the session,** on the model of LIP-0028. The key holder of
  an agent can sign, so the price of a bearer buys nothing here.
- **A new member of the grant for the account, the plan or the model.** It
  would change the octets of `swarma-grant/4`. The contract already binds the
  configuration (LIP-0017 section 8), and the account is a fact of one host.
- **One action for start and restart, and a second count for restarts.** The
  grant-side proposal has one action and one count, and this draft keeps it:
  a restart is a start that names a session.
- **A stop that needs no grant text.** The recipient could then always end
  its own session. Under LIP-0008 section 12.3 a command matches an exact
  leaf, and a right that no text names is a right that no issuer gave.

## Security consequences

- **A session outlives the facts of its start by up to one span.** A refusal
  that leaves no record suspends a session and does not end it. The issuer
  chooses the span, and with it the largest stretch for which a process runs
  on an admission that can no longer be repeated.
- **A suspended session still runs.** Its process keeps what it holds: its
  home, and every credential that works without a signature of its key. It
  receives no new instruction through a gate that asks `X` (AS5.6), and its
  key holder is asked for no renewal. What the process does with what it
  holds is bounded by the other executors and their own checks, and by
  LIP-0013 J7.8.
- **No verifier that never saw a spend is bound by it.** A stop by a seal
  reaches `X` when the transaction reaches its node (S30-K1). The reserve and
  the rebroadcast of LIP-0008 section 5.3 shorten that time, and nothing
  closes it.
- **A node without blocks holds every lease open** (S30-K2). The cutoffs of
  LIP-0022 refuse new admissions in that state. Whether they also stop a
  running process is Q8.
- **The executor is trusted for the end.** `X` journals the end and stops
  the process. A host that does neither keeps an agent running, and no other
  party sees it; the other executors still make their own checks at each
  request of that agent.
- **A restart is signed, so the key holder is in the path of every restart.**
  A key holder that is down leaves a crashed agent down. The count of starts
  bounds a loop of restarts that a faulty or a hostile host asks for.
- **The requests are replayable only inside their `iat` and `exp`.** AS4.2
  refuses a repeated identity while the journal holds it. A journal that is
  started anew forgets them; LIP-0028 T5.8 states the rule that refuses
  older requests there, and this draft has no such rule yet (N6).
- **Two words.** A reader who takes an agent session for a session of
  LIP-0028 expects a token and a window in seconds. The draft writes "agent
  session" throughout, and the action names do not (Q3).

## Conformance impact

None on normative v0.1, none on Grant v3, and none on the octets of
`swarma-grant/4`. No conformance class and no vector is added. The three
requests are invocations, the invocation has no members yet, and the record
of a session waits for the entries of a service journal. The cases of
section 9 state the outcomes that vectors will hold.

## Open questions

### Questions for the owners

Each has its options and a recommendation of this draft. A recommendation
decides nothing.

- **Q1. Whom does `recipient` name?** (a) The agent for which the session
  runs; who may ask is the gate of the key holder (LIP-0013 J7) and no
  member. (b) The party that asks for the start, with the agent as an
  argument of the request. Recommendation: (a). Under (b) the grant would
  bind no agent, and a row could not fix the worker (LIP-0026 R2.3).
- **Q2. The service type.** LIP-0018 section 3 asks every leaf for its type.
  (a) The candidate `slot.station` of LIP-0007 section 1 takes the three
  actions, and its row says "recipient" where it says "renter". (b) A new
  type with its own row. Recommendation: (a), as the smaller change; it is an
  amendment of LIP-0007 and no part of this draft.
- **Q3. The form of the names.** (a) The names of the grant-side proposal,
  with a dot: `swarma/session.start`. (b) Slashes alone, as LIP-0029 section
  8.2 writes `swarma/device/revoke`: `swarma/session/start`. (c) As (b), with
  a segment that tells the agent session from the session of LIP-0028.
  Recommendation: (c), decided together with the grammar that LIP-0008
  section 12.3 leaves open. The same choice holds for the limit kinds.
- **Q4. Effect or work.** LIP-0018 section 3 asks whether a leaf "ends in an
  effect at a resource or is an agent's work". (a) Effect: `X` is an effect
  service of LIP-0006 section 7 and refuses a grant whose terms carry a
  text, and a run at level L0 gets no signature for a start (LIP-0029 O6.7
  (a)), so an orchestrator at L0 starts no worker. (b) Work: the three
  commands move no money, land nothing and release no secret; `X` decides
  from machine members alone and hands a text of the contract to the agent
  unchanged, as LIP-0017 section 8, rule 4, has the launcher do.
  Recommendation: (b), with the limits of section 2.3 as the bound.
- **Q5. The model budget.** (a) A limit `swarma/gateway.units` in the grant
  of the session, as the grant-side proposal has it. (b) No such limit here:
  the budget is the limits of a second grant whose executor is the model
  service (LIP-0008 section 4; LIP-0020 W11.4), and a failed renewal of a
  credential there is no end of the session. Recommendation: (b).
- **Q6. The restart.** (a) A signed start request that names the session
  (AS4.6). (b) `X` restarts a crashed process itself, inside the lease, and
  debits a start without a request. Recommendation: (a). Under (b) a debit
  has no request identity, against LIP-0026 R5.7, and a host could run an
  agent that its key holder no longer signs for.
- **Q7. A session across two grants.** (a) A session ends with its grant, and
  the successor grant gets a new session (AS6.5). (b) A renew request under
  a successor grant with the same executor, recipient and contract rebinds a
  live session. Recommendation: (a) for the first version: it needs no new
  check, and it costs one restart in a term.
- **Q8. A session whose keep check is refused without a record,** a node
  without blocks included. (a) It is suspended and ends at its lease end
  (AS5.5). (b) `X` also stops the process when the age of the tip reaches
  the cutoff of the class, 5400 seconds for a privileged action (LIP-0022
  B3.6). (c) `X` ends it at the first such refusal. Recommendation: (a), and
  the owners say whether (b) is added for a node that receives no block,
  where the lease bound does not run. (b) uses the clock of LIP-0022, which
  is decided design for an admission (LIP-0008 section 6), and it is the one
  place where a clock would end a session.
- **Q9. The delay of the watch.** (a) The specification asks for a keep check
  at every new tip and leaves the read of the mempool to the station
  contract, and a conformance claim names its interval. (b) The
  specification states a largest interval. Recommendation: (a) until a run
  on a host has measured the read; LIP-0022 leaves the interval between
  observations open for the same reason.
- **Q10. The first text.** (a) The start request binds nothing of a prompt.
  (b) It binds the SHA-256 of the text, as `text_sha256` does in LIP-0029
  section 5.2, and `X` decides nothing from it. Recommendation: (b): the
  record of the session then names what the agent was first told.
- **Q11. The owner and a session.** Three points. Does a session that an
  owner starts at an own executor need a grant? (a) Yes: the owner's command
  is the origin of the run at the key holder (LIP-0029 O6.5), the key holder
  signs the start under a grant, and a command to `X` itself only stops.
  (b) No: an owner command to `X` starts a session without a grant.
  Recommendation: (a), with the one-host rule of LIP-0029 ("The chain rules
  apply inside one host too"). The level of a stop is open in LIP-0029; this
  draft recommends the lowest level that the policy admits, because a stop
  takes authority away. And a session whose origin is a command of a device
  that was later revoked: recommendation, the key holder signs no renew and
  no restart for such a run, so the session ends at its lease end; `X`
  cannot see the origin (LIP-0013 J7.7).
- **Q12. A stop while the observation is refused.** (a) A stop request is
  admitted like any invocation, and one that is refused ends nothing
  (LIP-0028 T5.5). (b) A stop request needs its signature alone.
  Recommendation: (a): for a recipient by name the key of the signature is
  itself a read of the chain, and the operator may end a session in any case
  (AS5.7).

### Needs without a member or a value

Each states a need and the smallest proposal. This draft writes no octets
for any of them.

- **N1. The members of the invocation and of the receipt** (LIP-0020). The
  arguments of section 2.2 are logical fields. Smallest proposal: three
  argument lists, as that section names them.
- **N2. A v4 code for the refusals of LIP-0008 section 4, steps 2 and 4,**
  among them an action text that no profile defines and a limit of a kind
  that no profile defines. The registry section that is in review is
  reported to name such codes; they are not in the base. Smallest proposal:
  this draft uses the codes of that section once it lands.
- **N3. The texts of `resource` and `unit`** of the three limit kinds
  (LIP-0020 W11.4). Smallest proposal: one fixed `resource` text for the
  profile, and the units "session", "start" and "block" as texts.
- **N4. How `X` obtains the contract** that `G` binds, to read the hash of
  the agreed configuration: in the proof bundle (LIP-0008 section 12.2) or by
  retrieval (LIP-0019). And a contract profile that requires that hash
  (LIP-0018 section 1; LIP-0017 section 8).
- **N5. The record of a run that does not exist yet.** LIP-0013 J7.1 binds a
  run to its origin "when the run is created"; here the key holder signs the
  request that creates it. Smallest proposal: a sentence in LIP-0013 that the
  key holder makes the record before it signs a start.
- **N6. A journal of `X` that is started anew.** Which older requests it
  refuses (LIP-0028 T5.8 has the rule for its sessions), and what it charges
  for the accounts of `swarma/session.starts` (LIP-0025 section 7).
- **N7. Single-use grants.** The profile is written for a grant with limits,
  as LIP-0028 is.
- **N8. Limits with a period,** for example starts in a stretch of blocks.
  The profile has none.
