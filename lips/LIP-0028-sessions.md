# LIP-0028: Sessions for clients that cannot sign

- **Status:** Draft
- **Created:** 2026-11-15
- **Affects:** how a service by grant admits a client that cannot sign its
  requests: the signed request that opens a session, the bearer token of the
  session, its binding to a slot, its window, its accounts and its end
- **Builds on:** LIP-0008 sections 2, 4, 5, 5.1 and 12, LIP-0013 section 3.6
  (J7), LIP-0006 sections 1 and 4, LIP-0007 section 1, LIP-0020, LIP-0022
  sections 1 to 3, LIP-0025 sections 3 to 5 and LIP-0026 section 5

## Summary

A model proxy is a service by grant whose client signs nothing. The client is a
third-party program, the harness of an agent. It reads a base URL and an API
key once, when it starts, and sends that key with every request. LIP-0008 has a
v4 service authenticate every request under the key of the recipient (section
4, step 2), as a signed invocation (section 12.1), and such a client cannot
make one. The model proxy of today accepts a binding of slot, grant, window and
caps that a gateway prepared, and it does not observe the chain itself
(LIP-0008, "Current state"); the bearer that it mints for the slot rests on
that binding. LIP-0008 section 5 excludes this for a v4 service: a gateway
cannot put its prepared binding in the place of the service's own verification.

This LIP proposes the session:

- which services admit sessions, and what a session belongs to (section 1);
- the session-open request, a signed invocation of the recipient's key
  holder (section 2);
- the token and the record of a session in the journal of the service
  (section 3);
- a request in a session, and what the service checks before each
  reservation (section 4);
- the window of a session, its extension and its end (section 5);
- the slot binding (section 6);
- the rules for the key holder, which no service sees (section 7);
- ten refusal codes and their order (section 8), and cases (section 9).

A session has a price, and the text states it where it arises. The token is a
bearer that every process of the slot's user can use. The requests in a session
are unsigned, so neither party can show the other which requests were made. And
a token works until the last end that the key holder signed, which lies up to
an hour after its last signature. A session is for a client that cannot sign; a
client that can sign sends signed invocations.

The LIP defines no octets. The three signed requests of a session are
invocations, and the invocation has no members yet (LIP-0020).

## What is decided and what is proposed

**Owner decision pending: J13.** Ivan Oparin decided on 2026-11-15 that a
service whose client cannot sign admits sessions. The co-author's agreement is
pending, and until then a v4 service admits signed invocations and nothing else
(LIP-0008 sections 4 and 12.1).

The decision says this, in eight parts.

1. A service whose client is a third-party program admits a session. The first
   case is the model proxy with the harness of a vendor.
2. The key holder of the recipient checks the origin of the run against its
   table. It then signs one session-open request under the grant. The request
   states the authority path, the executor, which is this service by name and
   key, the slot binding, a window of at most one hour, and requested limits
   within the grant.
3. The service verifies that request like any request under LIP-0008 section 4,
   the observation of LIP-0022 with a comparison node included. It returns a
   bearer token of 32 random octets, bound in its journal to the grant, the
   session, the slot binding, the end of the window and the limits.
4. The slot binding is, on one host, the user id of the caller that the kernel
   reports through `SO_PEERCRED` or `LOCAL_PEERCRED`, as LIP-0006 has it for
   the wallet service. Over a network it is the address of the slot.
5. The token stays the same for the run, because a harness reads its key once,
   at start. The key holder extends the window by further signed requests, each
   for at most one hour. Without an extension the token expires.
6. The service ends every session of a grant as soon as it observes the seal of
   that grant spent.
7. The harness gets a base URL and the token, and nothing else.
8. Against a captured agent with a shell in its slot a session equals a
   signature on every request: the agent gets only what the grant allows. A
   profile that signs every request stays possible later, for billing disputes.

The decision leaves the place of the text to this draft. The draft gives the
session a LIP of its own, because a session is no property of one service type:
every type whose profile says so can admit one (T1.1).

This draft adds the following to the decision. Each point is a proposal,
and neither owner has decided one.

1. The session-open request is a signed invocation of LIP-0008 section 12.1,
   and so are two further requests, which extend and close a session (T2.1,
   T5.2, T5.5). One consequence is that the proof path has to allow these
   commands, as it has to allow any command, so the issuer of a grant decides
   whether its authority may be used through a bearer (T2.5). A request with a
   token never asks for one of the three (T1.3).
2. The hour of part 5 is read as an end of the window at most 3600 seconds
   after the clock of the service at the admission of the request, and not as
   an hour added to the end that stands (T2.3, T5.2). Under the other reading,
   requests sent in a row would build a window of many hours.
3. The requested limits lie also within the ceilings of the operator, and name
   each key once. A session has accounts of its own beside those of the grant,
   and a limit key that the session-open request does not state has the ceiling
   0 (T2.4, T4.6).
4. A repeated request opens no session and returns no token (T2.6), and the
   identifier of a session is the identity of the request that opened it
   (T3.2).
5. The journal holds the SHA-256 of the token and need not hold the token. The
   service returns the token once and does not repeat an answer that was lost
   (T3.2 to T3.5).
6. Before every reservation in a session the service makes the checks of the
   proof path again, in an observation of its own, and requires that the key of
   the last signed request of the session is still the key of the recipient
   (T4.5).
7. An extend request never moves an end back, an end is final, and a close
   request exists (T5.2, T5.4, T5.5).
8. A closure of any grant on the proof path ends the session, where the
   decision names the seal of the grant (T5.6). A refusal without a closure
   ends no session, and a journal that is started anew holds none (T5.7, T5.8).
9. The rules of section 7 for the key holder, and the ten refusal codes of
   section 8 with their order.

Nothing of this profile is implemented.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The life of a session as a function of stated facts: admission, token, binding, window, extension, accounts, end | Yes | The co-author's agreement and the owners' acceptance |
| The open, extend and close requests as octets | No | The members of the invocation (LIP-0020) and the three commands in the profile of `model.proxy` (LIP-0007) |
| The record of a session as an entry of a journal | No | The entries of a service journal on the form of LIP-0025 |
| The checks of the proof path before a reservation | No | A run of the observation under LIP-0022 and of the name reads under LIP-0021 |
| The binding of a slot on one host | No | A way for a harness that is configured with a URL to reach a local socket (section 6) |
| A model proxy with sessions | No | All of the above, and the interface of the proxy to the harness |

## Motivation

The harness of an agent is configured with a base URL and an API key. It reads
both once, when it starts, and it signs nothing. A rule that asks for a signed
invocation on every request to the model has no client that can follow it.

The model proxy of today answers this with a bearer that it mints for a slot
(key map). It takes the slot, the grant, the window and the caps from a binding
that the gateway prepared, and it does not observe the chain (LIP-0008,
"Current state"). A gateway that errs or is taken over then extends the access
to the model, while the upstream API secret, and with it the account at the
upstream model service, lies with the proxy (key registry). LIP-0008 section 5
therefore asks that a model proxy verifies the presentation, the signed limits,
the validity and the seal against its own view of the chain.

The key holder has the same gap from its side. Under LIP-0013 section 3.6 it
signs for a run only under the grants that its table lists for the origin of
that run, and J7.8 names the credential that acts without a signature of the
key: such a credential must be out of the run's reach or behind the same
binding. A bearer for the model is such a credential, and the harness of the
run has to hold it.

## Current state

- LIP-0008 section 12.1 states the logical fields of a signed invocation,
  and section 4 the order of an admission. LIP-0020 reserves the type
  `swarma-invocation/1` and gives it no member.
- LIP-0008 section 5 names the model proxy that verifies for itself as a
  follow-on direction, and calls the proxy of today gateway-bound.
- LIP-0013 section 3.6 (J7, agreement pending) has the key holder offer a v4
  invocation as one of its typed operations (J7.5).
- LIP-0006 section 1 has the wallet service take the user id of its peer
  from the kernel before it reads a frame, on a Unix connection.
- The key registry holds the entry "Model bearer of a slot", in use in the
  rental profile: the proxy mints the bearer, the slot holds it, and whoever
  has a copy uses the model access of that slot inside its window and its
  limits.
- LIP-0007 section 1 lists `model.proxy` as a semantic candidate: to invoke
  a selected model and to account for requests, tokens, cost and the output
  of a request. The type has no accepted action strings.

## Proposal

A session is an activity at run time: for a bounded time a service admits the
requests of one client on the strength of one signed request. Its record is an
entry in the journal of the service, and the token is the credential that
stands for the session.

The final grant of a proof path is called `G`, and the service `X`. `now` is
the reading of the clock of `X` in whole seconds (LIP-0022 B3.1). Where a rule
compares a time with `now` for an admission, the reading is the one that `X`
takes immediately before the write (LIP-0022 B1.6).

### 1. Sessions and their service

| Rule | Requirement | Refusal |
| --- | --- | --- |
| T1.1 | A service admits sessions only where the profile of its type says so (LIP-0007). The action table of such a type holds three commands for them: to open, to extend and to close a session. The first such type is `model.proxy`. A service of a type without these commands admits signed invocations alone. | |
| T1.2 | A session belongs to one final grant with its proof path, to one executor, which is the service, and to one slot binding. None of the three changes while the session lives. | |
| T1.3 | A request in a session asks for one action of the action table of the type other than the three commands of T1.1, with the arguments that a signed invocation would state, and it carries no signature. `X` takes the three commands from signed invocations alone. A session adds no action and no allowance to what the proof path allows. | A command of T1.1 in a request with a token: `SESSION_COMMAND` |

### 2. The session-open request

| Rule | Requirement | Refusal |
| --- | --- | --- |
| T2.1 | The session-open request is a signed invocation (LIP-0008 section 12.1) whose command is the open command of T1.1. `X` authenticates it under the recipient mode of `G`, as step 2 of LIP-0008 section 4 says. | The refusal of that step |
| T2.2 | Its arguments state three things: the slot binding (section 6), the end of the window as a time in whole seconds, and the requested limits. Its ordered proof identifiers are the authority path, and its executor is `X` by name and key. | |
| T2.3 | The end of the window is later than `now`, and at most 3600 seconds later. | `SESSION_WINDOW` |
| T2.4 | Each requested limit names the key of a limit that `G` states for `X`, and no key is named twice. Its amount is at most the amount of that limit, and at most the ceiling of the operator of `X` for that key where the operator set one (LIP-0008 section 2). | `SESSION_LIMITS` |
| T2.5 | `X` admits the request as it admits any invocation: with every check of LIP-0008 sections 4 and 12, in one healthy observation (LIP-0022 sections 1 to 3). | The refusal of the check that fails |
| T2.6 | `X` records the identity of a signed request of a session when it admits the request, and it admits no request whose identity its journal holds. One request identity therefore opens at most one session, and a repeated session-open request opens none and gets no token. | `SESSION_REPLAY` |
| T2.7 | The slot binding has one of the forms of section 6, and `X` checks that form for its callers. | `SESSION_BINDING` |

T2.5 has a consequence that the decision does not name. Step 4 of LIP-0008
section 4 asks for the exact requested action, so the proof path has to allow
the open command for `X`. A grant that allows the model action alone admits no
session, and the issuer of a grant decides in this way whether its authority
may be used through a bearer.

T2.6 differs on purpose from the wallet profile, in which a repeated request
receives its stored receipt once more (LIP-0006 section 4). The answer to a
session-open request carries a bearer, and whoever repeats a request that it
saw on its way would receive the token of a session that it did not open. A
request that `X` refused left no record and can be sent again.

T2.4 treats the limits that have an account: a cumulative amount with a key and
a ceiling (LIP-0026 section 5). LIP-0008 section 2 names further kinds, among
them a maximum for one request, a rate, and the required confirmation depth,
which is a minimum. For such a kind the type profile says when a requested
limit lies within the grant, under one bound that holds for every kind: a
session never loosens a limit of the path.

A session has three times, and none is converted into another. The window of
T2.3 is a time on the clock of `X`. The `iat` and `exp` of the invocation bound
the admission of the request itself (LIP-0008 section 12.5). The height window
of each grant of the path is checked at every request (T4.5). A key holder
whose clock is ahead of the clock of `X` asks for less than an hour, because
`X` refuses under T2.3 an end that lies more than 3600 seconds ahead of its own
clock.

### 3. The token and the record of a session

| Rule | Requirement | Refusal |
| --- | --- | --- |
| T3.1 | When `X` admits the request it draws 32 octets from a cryptographically secure random source. They are the token of the session. | |
| T3.2 | `X` writes the session into its journal: the identifier of the session, which is the identity of the request that opened it; `G` and the proof path; the slot binding; the end of the window; the limits; the key under which `X` authenticated the request; and the SHA-256 of the token. The journal need not hold the token. | A write that fails opens no session and returns no token |
| T3.3 | `X` returns the token once: in its answer to the request that opened the session, on the connection that carried the request, and only after the write of T3.2 is complete (LIP-0025 M3.2). No later answer carries it. | |
| T3.4 | A token is the token of a session when its SHA-256 is the one that the record of that session holds. | |
| T3.5 | Where the answer of T3.3 did not reach the key holder, or `X` stopped between the write and the answer, the session stands in the journal and nobody holds its token. `X` does not send the token later. The key holder closes that session (T5.5), or lets its window end, and opens another session with a new request. | |

The decision asks that the token is bound in the journal. The hash of T3.2 is
this draft's way to bind it: a copy of the journal gives no token that works.
T3.5 is the rule that LIP-0025 M4.3 leaves to each kind of entry: where a
restart finds the entry of a session whose answer may not have been sent, the
answer does not follow.

### 4. A request in a session

| Rule | Requirement | Refusal |
| --- | --- | --- |
| T4.1 | A request in a session carries the token and no signature. `X` finds the session of the token (T3.4). | `SESSION_TOKEN` |
| T4.2 | The caller meets the slot binding of the session (section 6). | `SESSION_PEER` |
| T4.3 | The session is live: it has not ended (T5.4), and `now` is earlier than the end of its window. | `SESSION_ENDED` |
| T4.4 | The request asks for none of the three commands of T1.1 (T1.3). | `SESSION_COMMAND` |
| T4.5 | Before every reservation `X` makes the checks of LIP-0008 sections 4 and 12 for the proof path of the session and for the action of the request, in a healthy observation of its own (LIP-0022 sections 1 to 3). Step 2 of section 4 has no signature to verify. In its place `X` requires that the key under which it authenticated the last signed request of the session is still the key of step 2: the signed request key of `G`, or, for a recipient by name, the key that the name yields at that moment for the channel of that signed request. `X` reads the tip and its clock again as LIP-0022 B1.6 says, and applies T4.3 with that reading. | The refusal of the check that fails |
| T4.6 | `X` gives the request an identity of its own, and charges the request as it charges a signed invocation under `G` (LIP-0008 section 12.2; LIP-0026 section 5 proposes the accounts). For each limit key that the request consumes, `X` also debits an account of the session: a cumulative amount with the key `session`, the identifier of the session and that limit key. The ceiling of that account is the limit that the session states for the key, and 0 where the session states none. All debits of one request are reserved in one atomic write of the journal, or none, and of the accounts of one limit key the account of the session comes last. | `SESSION_LIMIT_OVER` for an account of the session; for another account the refusal of that account |
| T4.7 | The checks stand in the order T4.1 to T4.6, and the first that fails gives the refusal. A request that is refused reserves nothing. | |

The six checks serve one property, which is part 8 of the decision written as a
rule. `X` admits a request in a session only where it would admit, at that
moment, the same request as an invocation signed under the key of the session's
last signed request. Three things differ from a signed request. A request in a
session has no identity that its sender signed, so a request that is sent twice
is two requests and is charged twice. The window of the session stands where
the `iat` and `exp` of an invocation stand. And the caller is the slot, which
`X` checks against the slot binding.

The decision speaks of the request that opens a session, and T4.5 is this
draft's rule for the requests that follow it. LIP-0008 section 12.5 asks that
every link is valid at execution and not only when it was parsed or first
observed, and a seal that was spent after the opening has to stop the next
request. So `X` observes again before each reservation, and the token replaces
one thing, the signature. The key of T4.5 covers a recipient by name whose
owner removes or replaces the channel key: a signed request under the old key
then refuses at once, and so does the next request of a session that was opened
under it.

The price of T4.5 is one observation for every request: the reads of the
reading node and of each comparison node. A signed invocation pays the same,
because LIP-0022 B1.5 takes every fact of one admission from one observation.
For a model request, which takes seconds, that is little. A type with many
short requests would feel it, and this LIP gives such a type no cheaper check.

The limits of a session reserve nothing. They are ceilings beside the accounts
of `G`: two sessions of one grant may each state the full limit of `G`, and the
account of `G` bounds what both consume together. A limit key that the session
does not state has the ceiling 0, as LIP-0008 section 2 has it for a grant,
where a missing limit refuses and never becomes unlimited access.

### 5. The window, its extension and the end of a session

| Rule | Requirement | Refusal |
| --- | --- | --- |
| T5.1 | The token is the same from the opening of a session to its end. | |
| T5.2 | The extend request is a signed invocation with the extend command of T1.1. It names a session by its identifier and states a new end of the window. `X` authenticates it as T2.1 says, admits it as T2.5 and T2.6 say, and applies T2.3 to the new end. The end of the window becomes the later of the end that stands and the new end, and the key of T4.5 becomes the key under which `X` authenticated this request. `X` writes both into its journal before it answers. Nothing else of the session changes. | The refusals of those rules, and of T5.3 |
| T5.3 | An extend and a close request name a session that the journal holds for their own proof path and executor. An extend request names a live session (T4.3). | No such session: `SESSION_UNKNOWN`. An extend request for a session that is not live: `SESSION_ENDED` |
| T5.4 | A session ends with the first of three events: `now` reaches the end of its window; `X` admits a close request for it (T5.5); or `X` records a closure for a grant of its proof path (T5.6). `X` writes the end into its journal when it first finds it. An end is final: from that record on no request reopens the session, and `X` never accepts its token again, whatever its clock reads. | |
| T5.5 | The close request is a signed invocation with the close command of T1.1 that names a session by its identifier. `X` authenticates it as T2.1 says and admits it as T2.5 and T2.6 say. For a session that has already ended it changes nothing. | The refusals of those rules, and of T5.3 |
| T5.6 | When `X` records a closure for a grant, it ends every session whose proof path holds that grant, before it admits anything further. The first such closure is that of a validated issuer spend of the seal of the grant, in a block or, as LIP-0008 section 5.1 adds, in the mempool of `X` alone. | |
| T5.7 | A refusal that records no closure ends no session. A tip that is too old, an observation that is not healthy and a name that cannot be read refuse the request, and the session stays as it is until one of the events of T5.4. | The refusal of the check |
| T5.8 | A session lives in the journal of `X`, and a restart with an intact journal keeps it: `X` accepts the token as before. While the journal is lost, `X` refuses every act that needs it (LIP-0025 M5.1). A journal that is started anew holds no session of the lost one, and a recovery charges nothing for sessions. | After a new start: `SESSION_TOKEN` |

No request in a session is admitted 3600 seconds or more, on the clock of `X`,
after `X` admitted the last request that opened or extended that session. Three
rules give this bound. A request that opens or extends a session and that `X`
admits at the reading `a` leaves an end of at most `a + 3600`: T2.3 bounds the
end that the request states, and T5.2 keeps the end that stands only where it
is the later one, which an earlier request set under the same bound at a
reading that was not above `a`. The journal holds the end. A request in the
session is admitted at a reading that is earlier than the end (T4.3) and not
below `a`, because LIP-0022 B3.2 refuses a reading below the largest that `X`
has used.

For the key holder the bound reads otherwise, because a signed request can
reach `X` late. `X` admits no request in a session at or after the latest end
that the key holder signed for that session, whenever the signed requests
arrive. T7.5 keeps each end within 3600 seconds of the key holder's clock at
the signature. A key holder that stops, because its run ended or because its
table no longer lists the grant, therefore leaves the harness its access until
an end that lies at most one hour after its last signature, and for a shorter
time where a grant of the path ends earlier. The end is read on the clock of
`X` and the signature on the clock of the key holder, so a difference between
the two clocks adds to that hour or takes from it. A clock of `X` that runs
slow lengthens it in real time, and no rule of this LIP detects that.

An end is final in this draft, which the decision does not say. An extend
request that `X` receives after the end of the window finds no live session,
and the harness, which cannot read a new key, has lost its access to the model:
its run has to be started again with a new session. A key holder therefore
extends well before the end (T7.6). The other way, a session that a late extend
request reopens, would let a token return that the service has already refused;
it stands under the alternatives. A close request that `X` refuses, for an
observation that is not healthy for example, ends nothing. The key holder sends
it again, and until then the window bounds the session.

T5.6 goes beyond the words of the decision in one point. The decision names the
seal of the grant. A session under a child also ends when the parent of that
child is closed, because LIP-0008 section 12.2 has a closed ancestor refuse the
dependent request. `X` need not watch a seal between two requests for this.
T4.5 puts an observation before every reservation, so `X` admits no request
once one of its observations shows the spend. The request that meets the spend
refuses with the refusal of the closed grant, and every later request with a
token of that path refuses as `SESSION_ENDED`.

### 6. The slot binding

| Rule | Requirement | Refusal |
| --- | --- | --- |
| T6.1 | A slot binding has one of two forms. On one host it is the user id of the operating system under which the slot runs. Over a network it is the address of the slot. | A third form: `SESSION_BINDING` (T2.7) |
| T6.2 | For the first form `X` takes the user id of its caller from the kernel, for the local socket of the connection and before it reads the request: `SO_PEERCRED` on Linux and `LOCAL_PEERCRED` on Darwin, as LIP-0006 section 1 has it. A user id that the caller states is no input. | `SESSION_PEER` |
| T6.3 | For the second form `X` takes the address of its caller from the connection. An address that the caller states inside a request is no input. | `SESSION_PEER` |

The binding says from where a token is accepted. On one host it is as strong as
the separation of users by the operating system: every process of the slot's
user meets it. Over a network it is an address and no identity, and it holds as
far as the network between the slot and the service lets nobody else send from
that address. The binding concerns the requests that carry the token. A signed
request of the key holder is authenticated by its signature and comes from the
key holder, which is another caller than the slot.

T6.2 needs a local socket. On Linux `SO_PEERCRED` works only for a connected
stream socket of the Unix domain and for socket pairs, and it returns the
credentials that were in effect when the peer connected (`unix(7)`, Linux
man-pages 6.19). The wallet service of LIP-0006 section 1 has such a socket.
The decision gives the harness a base URL, and it does not say how a harness
that is configured with a URL reaches a local socket. This draft proposes no
way. A relay inside the slot, which runs under the slot's user, would meet
T6.2. Until the point is settled the first form of the binding cannot be built.

### 7. The key holder

These are rules for the service that holds the recipient's key. A service
that admits sessions cannot observe them and refuses nothing for them
(LIP-0013 J7.7).

| Rule | Requirement |
| --- | --- |
| T7.1 | The key holder signs an open, an extend and a close request for a run under LIP-0013 J7.3 (a): every grant of the proof path is in the `use` list of the origin of that run. |
| T7.2 | The key holder builds each of the three requests itself, and it signs no invocation with one of the three commands that a caller built. The slot binding that it states is the slot of that run by its own record of the run (LIP-0013 J7.4), and no value that a caller supplies. |
| T7.3 | It hands the token to the harness of that run and to nobody else, and it writes the token into no log. |
| T7.4 | One session serves one run. Another run gets a session of its own, also where it has the same origin. |
| T7.5 | The end of the window that the key holder states lies at most 3600 seconds after its own clock at the signature. |
| T7.6 | The key holder extends a session only while its run lives, and each time well before the end of the window. When the run ends it sends a close request and extends no further. |

T7.1 to T7.4 are how a session meets J7.8 of LIP-0013. The token acts without a
signature of the key and lies within the run's reach. It stays behind the
binding of that run all the same: the key holder asked for it under the grants
of the run's origin, the service accepts it from the slot of that run alone,
and it stops working at the last end that the key holder signed, at most an
hour after its last signature (section 5).

T7.2 closes a way out of the slot. LIP-0013 J7.5 lets a run ask the key holder
for a v4 invocation. A captured agent that could choose the slot binding of a
session-open request would name an address outside its host and receive a
bearer that works from there. So the binding comes from the key holder's record
of the run and from no caller.

T7.1 has a consequence that stays open. When the operator removes a grant from
the `use` list of an origin (LIP-0013 J7.3 (e)), the key holder signs nothing
under that grant any more, and a close request is an invocation under it. The
session of a run under that grant then ends with its window, at most an hour
after the key holder's last signature, and not at once.

### 8. Refusals and their order

| Code | What it reports | Rule |
| --- | --- | --- |
| `SESSION_REPLAY` | The identity of an open, an extend or a close request is already in the journal | T2.6 |
| `SESSION_BINDING` | The slot binding of a session-open request has a form that the service does not check | T2.7, T6.1 |
| `SESSION_WINDOW` | The end of the window is not later than `now`, or more than 3600 seconds later | T2.3 |
| `SESSION_LIMITS` | A requested limit is above the limit of the grant or the ceiling of the operator, names a key that the grant does not limit, or names a key twice | T2.4 |
| `SESSION_UNKNOWN` | An extend or a close request names no session of its proof path and executor | T5.3 |
| `SESSION_TOKEN` | The token is the token of no session in the journal | T4.1, T5.8 |
| `SESSION_PEER` | The caller does not meet the slot binding of the session | T4.2, T6.2, T6.3 |
| `SESSION_ENDED` | The session has ended, or `now` has reached the end of its window | T4.3, T5.3 |
| `SESSION_COMMAND` | A request with a token asks for a command that opens, extends or closes a session | T1.3, T4.4 |
| `SESSION_LIMIT_OVER` | A reservation would exceed an account of the session | T4.6 |

T8.1. For a session-open request the checks of the invocation and of its proof
path come first, with their own refusals (T2.1, T2.5). Then `SESSION_REPLAY`,
`SESSION_BINDING`, `SESSION_WINDOW` and `SESSION_LIMITS` stand in this order.

T8.2. For an extend request the order is: the checks of the invocation and of
its proof path, `SESSION_REPLAY`, `SESSION_UNKNOWN`, `SESSION_ENDED`,
`SESSION_WINDOW`. For a close request it is the same without the last two.

T8.3. For a request in a session the order is that of T4.7.

T8.4. None of the ten records a closure of a grant. The end of a session is a
record of the service about its session.

### 9. Cases

The cases state outcomes in words. Vectors come with the members of the
invocation.

| Case | Setting | Outcome |
| --- | --- | --- |
| S13-1 | A valid session-open request whose end is `now` plus 3600 seconds | Admitted. The journal holds the session, and the answer carries the token once |
| S13-2 | The request of S13-1 once more; in a variant its answer had been lost | `SESSION_REPLAY`, and no token. In the variant the key holder closes the session and opens another with a new request |
| S13-3 | An end of `now` plus 3601 seconds; an end of `now` | `SESSION_WINDOW` for both |
| S13-4 | A requested limit one above the limit of `G`; a limit with a key that `G` does not limit; one key twice | `SESSION_LIMITS` for each |
| S13-5 | A slot binding of a third form | `SESSION_BINDING` |
| S13-6 | A proof path that allows the model action and not the open command | The refusal of LIP-0008 section 4, step 4. No session |
| S13-7 | A request with the token from another user id than the bound one | `SESSION_PEER`; the same request from the bound user id is admitted |
| S13-8 | A request with 32 octets that are the token of no session | `SESSION_TOKEN` |
| S13-9 | A request at the second of the end of the window | `SESSION_ENDED`; one second earlier it is admitted |
| S13-10 | A request with the token that asks to extend its session | `SESSION_COMMAND` |
| S13-11 | An extend request 1800 seconds after the opening, with an end 3600 seconds ahead | Admitted. The end moves, and the token is the one of S13-1 |
| S13-12 | An extend request that arrives late and states an end before the end that stands | Admitted. The end stays |
| S13-13 | An extend request after the end of the window | `SESSION_ENDED`; a request with the token refuses in the same way |
| S13-14 | An extend request that names a session of another proof path | `SESSION_UNKNOWN` |
| S13-15 | The seal of `G` is spent, and an observation of the service shows the spend in its mempool. A second session at the same service belongs to another grant | The request that meets the spend refuses with the refusal of the closed grant. Every session of `G` ends, and a later request with its token refuses as `SESSION_ENDED`. The second session is untouched |
| S13-16 | The tip of the service's node is too old for the action | The request refuses under LIP-0022. The session stays, and a request after a new block is admitted |
| S13-17 | The account of the session is full while the account of `G` has room; and the reverse | `SESSION_LIMIT_OVER`; the refusal of the account of `G`. Neither request reserves anything |
| S13-18 | A recipient by name whose value lists another channel key since the last signed request of the session | The request refuses with the refusal of step 2. After an extend request under the new key the token is admitted again |
| S13-19 | A close request; then a request with the token | The session ends; `SESSION_ENDED` |
| S13-20 | A restart with an intact journal; a recovery by starting anew | The token is accepted; `SESSION_TOKEN` |
| S13-K1 | A known limit. A captured agent with a shell in its slot reads the token | It uses the session for everything that the path allows, as it would with a signature on every request |
| S13-K2 | A known limit. A copy of the token in another process of the slot's user | Accepted. From another user id it refuses as `SESSION_PEER` |

## Sources

No service, no key holder and no node was run for this LIP.

| Statement | Source |
| --- | --- |
| The logical fields of an invocation, the order of an admission, the limit kinds and the time terms | LIP-0008 sections 2, 4, 12.1, 12.2 and 12.5 |
| The model proxy of today and its bearer | LIP-0008, "Current state" and section 5; the key map; the key registry, entries "Model bearer of a slot" and "Upstream API secret of the model proxy" |
| The peer credentials of a Unix connection at the wallet service, and the stored receipt of a repeated request | LIP-0006 sections 1 and 4 |
| The sockets for which `SO_PEERCRED` works | `unix(7)` of the Linux man-pages project, release 6.19. No Darwin manual page was read; for `LOCAL_PEERCRED` the draft relies on LIP-0006 section 1 |
| What the key holder signs for a run, and the credential without a signature | LIP-0013 section 3.6, J7.3, J7.4, J7.5, J7.7 and J7.8 |
| The observation, the comparison node and the clock | LIP-0022 sections 1 to 3 |
| The order of a write, the pending entry and the lost journal | LIP-0025 M3.2, M4.3 and M5.1 |
| The accounts that a request debits | LIP-0026 section 5 |

## Alternatives

- **A signature on every request**, by a shim between the harness and the proxy
  that asks the key holder each time. Every request would have an identity that
  the recipient signed, which settles a billing dispute. It gives a captured
  agent nothing less, and it adds a round to the key holder for every call of
  the model. The decision keeps it as a possible later profile.
- **A bearer from the gateway's binding**, as the proxy of today has it. The
  proxy would not read the chain, and LIP-0008 section 5 excludes that.
- **The session in LIP-0008 section 5 and in the profile of `model.proxy`**,
  the other place that the decision offers. The session would then be the
  property of one type, and the next type whose client cannot sign would state
  it again.
- **A token that the key holder chooses** and states in the request. The
  service would draw nothing. The token would then stand in a request that
  others may see, and a copy of the request would be a way to learn it.
- **A new token with every extension.** A leaked token would stop working
  within the hour. The harness reads its key once and could not follow.
- **A session that a late extend request reopens.** A key holder that is a
  moment late would not lose its run. A token that the service has refused
  would be accepted again, and the journal could not state that a session has
  ended.
- **A missing limit that means the limit of the grant.** A session-open request
  without limits would open the whole grant to a bearer. With the ceiling 0 the
  key holder states every limit that the harness may use.
- **No slot binding.** The token would be accepted from anywhere, as the
  registry says of the bearer of today.

## Security consequences

- **The token is a bearer.** Whoever holds a copy and meets the slot binding
  uses the session, inside its window and its limits. On one host that is every
  process of the slot's user.
- **An address is no identity.** Over a network the binding holds as far as
  nobody else can send from the address of the slot.
- **Up to one hour after the key holder's last signature.** A token works until
  the latest end that the key holder signed (section 5). A difference between
  the clock of the key holder and the clock of the service adds to that hour,
  and so does a clock of the service that runs slow.
- **A spent seal reaches a session at the next observation.** The service
  observes before every reservation (T4.5), so a request refuses once an
  observation shows the spend. A request that was reserved before is not
  undone.
- **Requests in a session are not signed.** The journal of the service is the
  one record of them. The recipient cannot show that a request was not its own,
  and the service cannot show that it was. A billing dispute has the records of
  the two parties and nothing else.
- **A retry is a second request.** The service cannot tell a retry from a new
  request, and both are charged (T4.6).
- **Whoever delivers a session-open request first receives the token.** A party
  that reads the signed request on its way and delivers it first takes the
  answer, and the key holder's own delivery then refuses as `SESSION_REPLAY`.
  That party holds a token that works from the slot alone. The request and its
  answer need a channel that others cannot read; the slot binding is the second
  guard where the channel fails.
- **A change of the recipient's channel key reaches a session at its next
  request** (T4.5), as it reaches a signed request.
- **A grant that leaves the key holder's table keeps its session for up to an
  hour.** The key holder signs no extension and no close request under it
  (section 7).
- **The gate of the key holder is invisible.** A key holder that gives one
  token to two runs, or states the slot of another run, breaks section 7, and
  the service sees a valid session.
- **A journal that goes back revives a session.** A store that is restored to
  an earlier state holds as live a session that was closed after that state.
  The continuity check of LIP-0025 is what tells such a store from the journal.

## Conformance impact

None on normative v0.1 and none on Grant v3. No conformance class and no vector
is added: the three signed requests are invocations, the invocation has no
members yet (LIP-0020), and the record of a session waits for the entries of a
service journal. The cases of section 9 state the outcomes that vectors will
hold.

## Open questions

- **The co-author's agreement** to J13, and the owners' acceptance of each
  rule, first of the nine points that the section "What is decided and what is
  proposed" lists.
- **The three commands** and the action table of `model.proxy` (LIP-0007),
  whether they are commands of each type or of the reserved protocol namespace,
  the members of the invocation (LIP-0020) and the entries of a service journal
  (LIP-0025).
- **Whether a grant has to name the commands of a session**, as T2.5 has it, or
  whether the right to an action includes the right to a session for it.
- **How a harness with a base URL reaches a local socket**, without which the
  binding by user id cannot be built (section 6), and the form of an address
  binding: which address, and what a service behind a relay compares.
- **Limits of other kinds in a session**: a maximum for one request, a rate, a
  number of concurrent runs, and the required confirmation depth (LIP-0008
  section 2).
- **A close request after a withdrawal at the key holder.** Under LIP-0013 J7.3
  (a) the key holder cannot sign it (section 7).
- **A bound on the live sessions of one grant.** Each session needs a signed
  request, and nothing else bounds their number.
- **The interface between the harness and the proxy**: where the token stands
  in a request, and what a harness is told when the service refuses.
- **An answer that is in progress when a session ends.** The reservation was
  made before the end. Whether the service completes the answer is for the type
  profile.
- **A recipient that is a person.** In the rental profile the grant names the
  renter's key, which lies on the renter's device and signs a consent and
  messages (key map). Who signs the session-open request and its extensions for
  the agent of such a rental is not treated here.
- **Single-use grants.** The session is written for a grant with limits. What a
  session means under a grant whose one request is committed in the spend of
  its seal is not treated; the v4 encoding of single use has no profile yet
  (LIP-0008 section 4).
- **Other service types** that admit sessions.
