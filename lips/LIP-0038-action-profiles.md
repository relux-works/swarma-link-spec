# LIP-0038: Action profiles: post-message, spend-coins, name-update and model-call

- **Status:** Draft
- **Created:** 2026-11-17
- **Re-filed:** 2026-11-20, from the action-profiles draft on version 0.1.57; LIP-0032 now names the credentials proposal
- **Affects:** the proposed entries of the two registries of
  LIP-0020 W11.14: four further action identifiers under `swarma/`, two of which use the three
  shared limit kinds of LIP-0031, with what an executor checks before and during each effect, the
  refusals, and what its receipt states
- **Builds on:** LIP-0006 sections 1, 3, 4, 5, 6 and 7, LIP-0007 section 1,
  LIP-0008 sections 2, 3.1, 4, 5, 5.1, 6, 12.1, 12.2, 12.3 and 12.5,
  LIP-0010, LIP-0013 section 3.6, LIP-0018 sections 2 and 3, LIP-0020
  sections 2, 3 and 11 (W11.2, W11.4 and W11.14), LIP-0022, LIP-0025,
  LIP-0026 section 5, LIP-0028, LIP-0030, LIP-0031, LIP-0034 and LIP-0035

## Summary

The registries of LIP-0020 W11.14 carry proposed profiles, not adopted
actions at every executor. LIP-0030 proposes the agent-session leaves
and their own kinds; LIP-0031 proposes `swarma/coins`,
`swarma/model-cost` and `swarma/model-tokens`. This LIP proposes four
further leaves, two of which use those same three kinds, not competing
definitions of them. A side that runs no profile of an action still refuses it as
`ACTION_UNDEFINED` (W11.14 rule 1), and a consumed kind without a profile
there still refuses as `LIMIT_KIND_UNDEFINED` (rule 2).

This LIP proposes, in the reserved `swarma/` namespace (LIP-0008
section 12.3; LIP-0020 W11.14 rule 3):

- `swarma/post-message`: an agent signs and posts a message as itself
  (section 2);
- `swarma/spend-coins`: a payment under a `swarma/coins` limit
  (section 3);
- `swarma/name-update`: a Namecoin name operation on a named name
  (section 4);
- `swarma/model-call`: a model request through a model service under
  `swarma/model-cost` and `swarma/model-tokens` limits (section 5).

For each action the text states the items that LIP-0018 section 3
requires of an action leaf: the name, the service type, the arguments
and targets that the request signature covers, whether it ends in an
effect, the limit kinds that bound it, what the receipt states, and its
refusals, vectors and path. Section 1 states what the four share: what
an executor checks before it reserves, what it checks again during the
effect, and what it reports. Section 6 states the three limit kinds
with the items of LIP-0018 section 2. Section 7 collects the proposed
registry rows. Section 8 orders the refusals, and section 9 states
cases in words.

The LIP defines no octets. The invocation `swarma-invocation/1` and the
receipt `swarma-receipt/1` have an identifier and no members (LIP-0020
section 3), so the arguments and the receipts below are logical fields
in the sense of LIP-0008 section 12.1: they state what the request
signature covers and what a receipt states, and they assign no member
name, no encoding and no size.

## What is decided and what is proposed

Every rule of this LIP is **PROPOSED**, except the settlement choice
explicitly marked **DECIDED** in P6.1. Nothing here is implemented.
The owners accept or change the remaining profiles through this LIP,
under LIP-0001. Carried rules retain the state of their cited source;
landing a Draft is not adoption of all its rules.

**Recorded decision.** On 2026-11-20 Ivan Oparin selected option A for
LIP-0038 reserve settlement: "charge actual, return the rest, as
LIP-0031". Source event:
`$VY_Ow-Yi4YWA695VYxcLlg0EdizZ6p8UzPkpr37ZyGU`.
P6.1 references LIP-0031 L9 for that choice; the event decides neither
the four leaves nor any other rule or open encoding of this draft.
It supersedes the original section 6 proposal to retain a reconciled
unused reservation.
The co-author's agreement is pending.

| Carried text | State there | Used here |
| --- | --- | --- |
| An executor refuses an action that its profile does not define, and a limit of an undefined kind is never read as no limit (`ACTION_UNDEFINED`, `LIMIT_KIND_UNDEFINED`) | LIP-0020 W11.14, a proposal of version 0.1.55, in force by no word of that draft | P1.4, section 8 |
| The admission order, the concrete executor, signed partitions and one authoritative journal for replicas of one executor | LIP-0008 section 4, Draft | P1.2, P1.3 |
| The signed invocation with its eight logical fields, the proof path with attenuation and ancestor accounting, exact leaf commands under the reserved `swarma/` namespace, and the two time measures with their recheck at execution | LIP-0008 sections 12.1, 12.2, 12.3 and 12.5, Draft | P1.1, P1.5, P1.8 |
| The limit kinds named by meaning: coins, model requests, model tokens, model cost and maximum answer length among the initial kinds; outbound messages and name operations among the further kinds of the decision of 2026-11-14 | LIP-0008 section 2, Draft; the further kinds are Ivan Oparin's decision of 2026-11-14 with the co-author's agreement pending, and the meaning beside each of them is that draft's proposal | Sections 2 to 6 |
| Text governs an agent's work and never a service's effect: an effect service refuses a grant whose terms carry a text | LIP-0006 section 7; Ivan Oparin's decision of 2026-11-14, with the co-author's agreement pending | P1.6 |
| Money or irreversible actions stop at a tip age of 60 minutes and other privileged actions at 90 minutes, with at least two independent nodes; a service determines the risk from its action profile | LIP-0008 section 6, decided design of 2026-11-10; age measure, nodes and classification left to profiles, and LIP-0022 proposes the first three and leaves the classification to action profiles | P1.12 |
| The accounts that a request debits, one atomic reservation write and one charge for one request identity; uncertainty retains the reservation, while known outcomes settle under the shared kind profile | LIP-0026 section 5; LIP-0031 L8, L9, L13, L18 and L20, with the settlement choice confirmed by the decision above | P1.7, P1.9, P1.10, P6.1 |
| A service whose client cannot sign admits sessions, first at the model proxy, and checks the proof path before every reservation | LIP-0028; a decision of Ivan Oparin of 2026-11-15 (J13) with the co-author's agreement pending, and the rules of the session are that draft's proposals | P5.4 |

Five points are more than a restatement of those texts, and the owners
should look at them first. Each is marked where it stands.

1. The four action identifiers are this draft's proposal. LIP-0030
   already proposes other leaves under `swarma/`, and the three shared
   limit-kind identifiers and their arithmetic come from LIP-0031.
   Section 6 references that profile rather than redefining it.
   For the counting kinds that sections 2 and 4 need, outbound messages
   and name operations, this draft assigns no identifier: it states
   them by the meaning of LIP-0008 section 2 and leaves their profiles
   open (sections 2, 4 and 6).
2. Two refusal codes, `ACTION_ARGUMENTS` and `ACTION_TARGET`, with
   their place between the steps E2 and E3 of LIP-0014 section 8.4
   (section 8). LIP-0030 section 6 proposes invocation-check codes,
   and the LIP-0014 companion's section 5 (O3) proposes E0's inner
   order. Neither is an adopted assignment by this LIP; it adds only
   the two codes for the checks that belong to an action alone.
3. All four actions stand in the risk class that stops at a tip age of
   60 minutes (P1.12). The cutoffs are decided; which action stands in
   which class is not, and LIP-0022 leaves it to action profiles.
4. `swarma/name-update` covers an update of a name that is already
   registered, and no registration and no transfer (P4.2). The stages
   of a registration stay outside the leaf, as they stay outside the
   wallet service v1 profile (LIP-0006 section 3).
5. For `swarma/post-message` no service type of LIP-0007 defines the
   leaf. The type `mail.send` is a semantic candidate there, for mail;
   this draft leaves the type that offers a posted message open and
   binds the action to the concrete executor that the grant names, as
   every v4 action is bound (section 2).

This re-filing reconciles the original version 0.1.57 draft with version
0.1.66. It leaves LIP-0030's session authority, lifecycle and independent
starts/level/span kinds unchanged. Its halt leaf is an owner command,
not a grant action. Section 7 keeps those entries separate.

The book's chapters "Grants and authority" (`book/ru/06-granty.md`) and
"Effects, stopping and federation" (`book/ru/22-effekty-ostanovka-federaciya.md`)
in `swarma-docs` supply the same authority-before-effect and unknown-outcome
boundaries. The module sources below remain authoritative for this wire
profile: **same**, cite them without importing the book's separate broker
v0 vocabulary; **refines**, this LIP proposes the four leaves; settlement
follows the explicit owner decision above. No new book-level design is
introduced here.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The checks of sections 1 to 6 and the order of section 8, as functions of stated facts: a grant, an invocation in its logical fields, an observation, a ledger and an effect outcome | Yes | The owners' acceptance |
| A request or a receipt as octets | No | The members of `swarma-invocation/1` and of `swarma-receipt/1` (LIP-0020 section 3), which also fix the journal key of a request (LIP-0020 section 6) |
| An executor for one of the four actions | No | The above, a run of the observation under LIP-0022 and of the name reads under LIP-0021, a journal under LIP-0025, and the custody of the credentials of its effect (the wallet keys, the name-owner key, the upstream model secret, the message signing path), which no rule below assigns |
| Vectors and a checker for these profiles | No | The members of the invocation and of the receipt; section 9 states the cases in words |

## Motivation

A Grant v4 reader compares identifiers; it does not thereby implement
an action (LIP-0020 W11.4). LIP-0030 now proposes session actions and
LIP-0031 supplies proposed money, cost and token accounting, but neither
supplies the four effect leaves below. An executor without the relevant
action profile still refuses at `ACTION_UNDEFINED`. This LIP fills that
action-profile gap without changing the shared kind arithmetic.

Four effects are the ones that the running system already performs
outside Grant v4, each under a narrower contract of its own: an agent
posts a message under its messaging key, a wallet service spends coins
under the closed action set of LIP-0006, an operator updates a
Namecoin name by hand, and a model proxy answers model requests under
a binding that a gateway prepared. Naming the four as exact leaves,
with the checks and the accounting that Grant v4 already requires of
every effect, is what would let a v4 grant authorize these effects.

## Current state

- LIP-0030 proposes the station agent-session leaves and three distinct
  station kinds. LIP-0031 proposes the three shared kinds used here,
  including their resource/unit forms, periods and arithmetic. These
  Draft profiles do not define an action or kind at a side that runs
  none of them (LIP-0020 W11.14). The kind `policy` remains reserved
  and undefined (LIP-0008 section 12.4).
- The wallet service v1 profile of LIP-0006 is implemented with a
  closed set of five actions, `balance`, `history`, `receive`,
  `budget` and `spend`, exact request bytes and signed receipts. Its
  wire action `spend` maps to the executor verb `pay` (LIP-0007
  section 1). It rejects registration, updates and other name actions,
  whose continuations need a separate design (LIP-0006 section 3).
  Nothing below renames a wallet-v1 action or extends its parser.
- The model proxy of today accepts a binding of slot, grant, window
  and caps that a gateway prepared, and it does not observe the chain
  itself (LIP-0008, "Current state" and section 5). LIP-0028 proposes
  sessions for its client, which cannot sign, and names no model
  action: the commands of the profile of `model.proxy` are open there.
- LIP-0007 section 1 lists the service types `wallet.nmc`,
  `model.proxy`, `mail.send` and `names.nmc` with the actions and
  boundaries that their future profiles need to define. Only the
  wallet row records an existing action set; the other rows are
  semantic candidates and no accepted wire action strings.
- A messaging key grants no authority. The key holder of LIP-0013
  section 3.6 signs a run's typed objects only under what its operator
  listed for the origin of that run, it builds the transport operations
  of the messaging profile itself from the message, and those
  operations authorize nothing (J7.5). Whether an agent's NIP-17
  messages use the same key as its requests, and through which holder,
  is not decided (the same section).
- The invocation and the receipt have identifiers and no members
  (LIP-0020 section 3). What a receipt states about an effect, for
  each action, is one of the things their members wait for (LIP-0020,
  "What can be built from this LIP"; LIP-0018 section 3).

- Service discovery now uses the optional `service` declaration of the
  pinned LIP-0010 section 11 manifest: `type`, `actions`, `receipt_key`
  and `endpoint`, not older per-service locators (LIP-0007 section 3).
  It advertises only supported profiles and replaces no authority pin
  of `G`; P1.2 and P1.11 still require their pinned keys. Changing the
  manifest alone closes no grant (LIP-0010 SH7).
- LIP-0034 A1 to A3 separate foreign-service login under `auth_key` and
  its paired `auth_seal` from device, grant and cold name-owner keys.
  A login, a device key or a service declaration authorizes none of
  these effects and substitutes for none of their signing roles.
- LIP-0035's contract-free branch is a root grant without `delegate`,
  never a hire or rental. These leaves add no exception to that scope
  or to its verification. Its optional mandate keeps lowercase slash
  action segments and W11.4 limit arrays, not an object map. A contract
  mirror below applies where a contract is required or supplied; this
  LIP neither invents a contract for that branch nor removes one from
  a hire, rental or delegated path.
  Its section 2.2 `swarma-broker-invoke/1` wrapper has no member for
  action arguments. It therefore cannot request any of these four
  leaves under P1.5 without a new signed argument binding. That binding
  remains open; arguments supplied outside the signature cannot fill it.

## Proposal

In what follows, `G` is the final grant of a proof path and `X` is the
executor: the concrete service by name and key that `G` signs as its
`executor` (LIP-0020 W11.2, W11.4). A request is a signed invocation in
the logical fields of LIP-0008 section 12.1, or, where section 5 says
so, a request in a session under LIP-0028. The rules are numbered with
the prefix `P`. A rule that only carries a landed text names that
text; a rule of this draft says so.

### 1. What the four actions share

| Rule | Requirement | Refusal |
| --- | --- | --- |
| P1.1 | Each of the four identifiers is one exact leaf, in lowercase segments separated by slashes. It matches exactly; a prefix grants nothing, and no other text stands for it (LIP-0008 section 12.3; LIP-0018 section 3; LIP-0035 section 2.1). The leaf is an entry of `actions` of `G` and, for a request under a child, of `delegate.actions` of the parent (LIP-0014 section 8.4, row E0). | `GRANT_ACTION_ABSENT` is proposed in LIP-0030 section 6 and the LIP-0014 companion O3; E0 assignments remain proposed |
| P1.2 | The executor of the grant, the executor of the invocation and the authenticated service's pinned name and key are one service (LIP-0008 section 4). A service of the same type that the grant does not name is no executor for the request, and no budget of `G` is spendable at it (LIP-0008 sections 4 and 12.2). | The refusal of that check |
| P1.3 | Before any reservation or effect, `X` admits the request as it admits any invocation: the checks of LIP-0008 sections 4 and 12 over the whole proof path, in one consistent observation of its own node, healthy and fresh for the class of the action (P1.12). A gateway or a presenter supplies data for those checks and replaces none of them (LIP-0008 section 5). | The refusal of the check that fails |
| P1.4 | `X` knows the leaf and every limit kind that the request consumes, under the type profile it runs. That a text stands in `actions` of `G` does not define it, and a limit of an undefined kind is never read as no limit (LIP-0020 W11.14 rules 1 and 2). For the three shared kinds it also recognises the limit's resource, unit and period under LIP-0031 L4; an unsupported text is not a new kind or unlimited authority. | `ACTION_UNDEFINED`; `LIMIT_KIND_UNDEFINED`; `LIMIT_UNSUPPORTED` (LIP-0031) |
| P1.5 | The arguments are the complete typed parameters and targets of the effect, and the request signature covers them beside the command, the subject, the proof order, the nonce, the times and the executor (LIP-0008 section 12.1). `X` derives the actual arguments of its effect from the signed arguments alone and checks the two equal before the effect. A value that the transport, a model or the caller outside the signature supplies is no argument. (This draft's rule.) | `ACTION_ARGUMENTS` (proposed, section 8) |
| P1.6 | Each of the four ends in an effect at a resource. `X` therefore decides from members that a machine compares and refuses a grant whose terms carry a text, and it leaves no part of that decision to a model (LIP-0006 section 7). The content of a message under section 2 and the content of a model request under section 5 are arguments of the effect, not terms of the grant, and P1.6 says nothing about them. | No code in a landed text; open |
| P1.7 | Before the effect, `X` reserves every debit of the request in one atomic write of its journal, or none of them: for each limit key that the action consumes, the own account of `G` and, for a request under a child, the row account of its parent, the own account first (LIP-0026 R5.2 to R5.6). A key without a stated limit has the ceiling 0, an allowance of zero authorizes nothing, and an operator ceiling may only lower what the grant allows (LIP-0008 section 2). A request that is refused reserves nothing (LIP-0026 R6.2). | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| P1.8 | Every link of the path is valid at execution and not only when the request was parsed. After the observation work, `X` rechecks both time measures before a new reservation and before the effect: the tip height lies in the intersection of the height windows of the links, and `iat <= now < exp` holds on its clock (LIP-0008 section 12.5). A grant whose closure `X` records under a validated spend of its seal admits no further effect (LIP-0008 section 5.1). An effect that was made while its grant was admissible is not undone by a later refusal (LIP-0008 section 3). | The refusal of the check that fails |
| P1.9 | One request identity holds at most one reservation in the ledger of `X` and is charged once, under whichever bundle it is presented (LIP-0026 R5.7). A repeated request performs no second effect. What identifies the request in the journal comes with the members of the invocation (LIP-0020 section 6); whether a repeat is answered with the stored receipt, as the wallet service v1 profile has it (LIP-0006 section 4), or refused, is open for each action, and sections 2 to 5 say what a second effect would cost where the answer matters. | None of its own |
| P1.10 | Where the outcome of an effect is not known, its reservation stands until the outcome is reconciled (LIP-0008 section 2; LIP-0026 R5.8). `X` reports such a request as uncertain and never as executed. Changing the nonce, the key or the journal to repeat an uncertain effect is outside the contract of each of the four, as it is outside the wallet profile (LIP-0006 sections 4 and 6). The shared kinds settle by P6.1; an unknown outcome is not a settlement. | None of its own |
| P1.11 | `X` answers with a receipt signed by the executor's key (LIP-0020 section 3, the registry entry `swarma-receipt/1`), which is the key that `G` pins for `X`. In meaning, beside what sections 2 to 5 state for each action, every receipt states the identity of the request, the action, the outcome, executed, refused or uncertain, and, for each limit key the request consumed, the reserved amount and, once known, the actual settlement debit and released difference under P6.1 for the shared kinds. A caller verifies a receipt under no key that the answer itself supplies, as a wallet client verifies under its pinned receipt key (LIP-0006 section 5). The members of the receipt are open with its type. | None of its own |
| P1.12 | Each of the four actions stands in the class of money or irreversible actions: admission stops when the age of the tip reaches the cutoff of that class, 60 minutes (LIP-0008 section 6; the age measure and the nodes are proposed by LIP-0022). A caller cannot lower the class. (This draft's proposal: a posted message cannot be unposted, a payment and a name operation move chain state, and a model request spends cost at an upstream account.) | The refusals of the observation profile |

Three properties of the common part are worth stating apart from the
table.

**No effect rests on a prepared binding.** P1.3 is the point on which
the model proxy of today differs from an executor of section 5, and it
holds for the other three alike: whoever carries the presentation to
`X`, prepares its slot binding, or mints a bearer for it, `X` reads its
own node and admits the request itself (LIP-0008 section 5; LIP-0028
section 4 for a request in a session).

**The journal is part of the authority.** Replicas that act as one
executor share one authoritative journal for request identity,
reservations and remaining allowance; where the shared state is
unavailable, replicas admit no new effect (LIP-0008 section 4). The
form of such a journal is proposed by LIP-0025, and its entries for a
service journal are open (LIP-0028, "What can be built from this LIP").

**A refusal records no closure.** None of the refusals of this LIP
closes a grant. A closure still comes only from the events that the
landed texts name, first the validated spend of a seal (LIP-0008
section 5.1), and an executor that observes one writes it before any
further admission, under those texts and not under this one.

### 2. `swarma/post-message`: an agent signs and posts a message as itself

The effect of this leaf is that a message goes out signed as the agent
itself: under the agent's own messaging key, to a stated destination,
with a stated content. The grant authorizes the posting at the
executor that the grant names; it does not turn the messaging key into
an authority key, and a message that this leaf posts grants nothing to
whoever receives it.

| Item of LIP-0018 section 3 | This profile |
| --- | --- |
| Name | `swarma/post-message`, one exact leaf (P1.1) |
| Service type | Open. No type of LIP-0007 section 1 defines a posted message; `mail.send` is its semantic neighbour there, with sender identity, allowed recipients and sending limits to bind. Until a type profile adopts the leaf, the only service that offers it is the concrete executor that `G` names and whose profile is this section |
| Arguments and targets | The destination, in the form of the messaging profile that carries the message: the recipient or the place the message is posted to, complete enough that no second reading is possible; and the complete content that will be signed and posted. Both stand under the request signature (P1.5). Where the messaging profile encrypts the content, the arguments bind the content as the profile of that transport commits to it, and the salted binding of LIP-0011 section 7 is the landed pattern for an invocation inside an encrypted message; its form for this leaf is open |
| Effect or work | An effect: the signed message leaves the executor. It is authorized by machine members only (P1.6). Writing the message is the agent's work and no part of the effect |
| Limits | The kind that LIP-0008 section 2 names by the meaning "Outbound messages": the number of messages, and the recipients they may go to. This draft assigns that kind no identifier (section 6). A request therefore consumes one message against a limit of that kind, and its destination is held against the recipients that the limit's resource permits; until a kind profile assigns the identifier and the resource form, a request that needs the count refuses at P1.4 |
| Receipt | Beside P1.11: the destination that the message went to and the identifier under which the messaging profile names the posted message, where that profile has one; otherwise the hash of the exact signed message as posted. A receipt proves the executor's statement that it posted, and not that a recipient read the message |
| Refusal codes, vectors and checker, path | Section 8; cases S38-1 to S38-4 in section 9, with vectors and a checker waiting for the members of the invocation; this LIP, adopted under LIP-0001 |

Checks of the executor, beside section 1:

| Rule | Requirement | Refusal |
| --- | --- | --- |
| P2.1 | The key that signs the message is the messaging key of the agent that `G` names as its recipient, as the profile of the transport binds that agent to that key. `X` signs no message under a key that the caller chose, and no message as another agent or as an owner. Which key that is on each transport, and through which holder it signs, is open in the landed texts and stays open here (LIP-0013 section 3.6). (This draft's rule.) | `ACTION_TARGET` (proposed) |
| P2.2 | The destination is one that the outbound-messages limit of `G` permits for its resource, and the content that `X` will sign is the content of the signed arguments, byte for byte as the messaging profile commits to it. `X` signs no digest that a caller supplies; the signer computes the digest of the message itself (LIP-0020 section 4, for the signed objects of the v4 profile), and it builds the transport operations itself from the message (LIP-0013 J7.5, for the key holder). | `ACTION_TARGET` for the destination; `ACTION_ARGUMENTS` for the content (both proposed) |
| P2.3 | The reservation of P1.7 counts one message. `X` makes it durable before the message is signed and posted. A message that is signed and whose posting then has no known outcome keeps its reservation (P1.10): it may have been posted, and a second posting under a new request identity is a second message that the count has to show. | As in P1.7 |
| P2.4 | A repeated request posts nothing again (P1.9). Whether it is answered with the stored receipt is open; an answer that returned the signed message for the caller to post elsewhere would give the effect a second path with no second count, and this draft proposes no such answer. | None of its own |
| P2.5 | The duties of the key holder of LIP-0013 section 3.6 stand where they are a landed text's: at the holder, which no executor observes (J7.7). Where `X` and the holder are one service, the holder's gate comes before the signature under the messaging key, and the checks of this section come before both. One service in two roles gives neither role the other's evidence. (This draft's statement of their order.) | The refusals of each role |

What this leaf does not give, the text states so that no reader takes
it for more. A posted message is attributable to the agent's key and
to nothing else: it shows neither that a grant authorized the posting
nor under which run the agent wrote it, because neither a grant nor an
origin has a place in a message that a landed messaging profile
defines. A recipient that acts on a message does so under its own
admission rules, as with an instruction under LIP-0013 today.

### 3. `swarma/spend-coins`: a payment under a `swarma/coins` limit

The effect of this leaf is one payment: coins of a stated asset, on a
stated payment system, move to a stated payee, and the whole spend,
the applicable fees included, is charged against a `swarma/coins`
limit of `G` (section 6). The executor holds the spending credentials
outside the client, as a grant-gated service does (LIP-0006); the
agent signs the request and holds no coin key for this leaf.

| Item of LIP-0018 section 3 | This profile |
| --- | --- |
| Name | `swarma/spend-coins`, one exact leaf (P1.1) |
| Service type | A wallet-type service. The existing set is `wallet.nmc` of LIP-0007 section 1, whose implemented v1 action `spend` keeps its own bytes and its own name; this leaf is its v4 counterpart by meaning and renames nothing |
| Arguments and targets | The asset and the payment system, by the explicit identifier that the limit's resource names: a chain with its asset, or a rail outside a chain (LIP-0008 section 2, the decision of 2026-11-14 for coins). The payee, complete as the payment system names a payee. The amount, in atomic units of the asset. A bound for the fees of the spend, in the same atomic units, so that amount and fees together are the charge. All stand under the request signature (P1.5) |
| Effect or work | An effect at the asset: the payment. Authorized by machine members only (P1.6) |
| Limits | `swarma/coins` (section 6): the total spending of the window, and the two further bounds of the decision of 2026-11-14, a maximum for one spend and a maximum for a period, where `G` states limits of those keys. Beside it, where the profile of the asset needs chain evidence, the kind "Required confirmation depth" of LIP-0008 section 2 by its meaning: a floor, whose effective minimum is the maximum of the signed minimum and the operator's risk floor. This draft assigns that kind no identifier; its tiers and depths stay open in LIP-0008 section 2 |
| Receipt | Beside P1.11: the payee and the amount as paid, the fees as paid, and the identifier of the spend on its payment system, on a chain the transaction id. Where confirmation is part of the outcome, the depth that the executor's own node showed when it reported, stated as an observation and not as finality. An outcome that is not known is reported as uncertain (P1.10) |
| Refusal codes, vectors and checker, path | Section 8; cases S38-5 to S38-9; this LIP, under LIP-0001 |

Checks of the executor, beside section 1:

| Rule | Requirement | Refusal |
| --- | --- | --- |
| P3.1 | The asset and payment system of the arguments are the ones that the resource of the `swarma/coins` limit names, and the unit of the amount and of the fee bound is the atomic unit of that asset, as the limit's unit states. An amount on another asset, another rail or another unit is no spend under this limit, at any value. No amount passes through a floating-point number (LIP-0020 section 2). | `ACTION_TARGET` (proposed) for the asset and the rail; `ACTION_ARGUMENTS` (proposed) for the unit |
| P3.2 | The payee is a permitted target of the limit (LIP-0008 section 2, "permitted targets"). The permitted-target encoding remains open: LIP-0031 L11's `<system>:<asset>` resource does not encode a payee list or wildcard, and this leaf adds no ad hoc resource suffix or limit member. A payee not permitted by the applicable target constraint and, where present, the contract mirror refuses before any amount is compared; defining that constraint's form is still a prerequisite of an executable profile. The payee that the payment goes to is the payee of the arguments (P1.5). | `ACTION_TARGET` (proposed) |
| P3.3 | The reservation of P1.7 charges the amount together with the fee bound, before the spend is signed or broadcast. Where `G` states a maximum for one spend, the same sum stands against it, and where it states a maximum for a period, against that period's account; LIP-0031 L3, L5, L7 and L12 define the period families and accounts, and a limit with a period that the executor cannot read refuses at P1.4 and not here. The per-request check is LIP-0031 L14, before reservation. | `SPEND_OVER` (LIP-0031 L14); `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| P3.4 | After the reservation and before the spend leaves `X`, `X` checks the authority and the spend once more on the facts of that moment: the recheck of P1.8, and that the inputs it will spend are still the executor's to spend for this payment and still unspent on its own node where the asset is on a chain. The wallet service v1 profile makes this second check before broadcast (LIP-0006 section 4, step 5); this draft proposes it for the v4 leaf. A refusal after the reservation retains it while the outcome is unknown (P1.10); a known non-effect follows P6.1. | The refusal of the check that fails |
| P3.5 | A spend whose broadcast or confirmation has no known outcome is never repeated under the same request identity and never rebroadcast as a fresh payment (P1.10; the wallet profile's rule of LIP-0006 sections 4 and 6, proposed here for the leaf). Reconciliation reads the executor's own node or the records of its rail, and what it may then report goes in a later answer to the same request identity, never in a new spend. | None of its own |
| P3.6 | Rental price and authority to spend funds are separate terms (LIP-0008 section 2). A payment for a period of a rental is a spend like any other under this leaf and is charged like one; that a contract expects the payment gives it no place outside the limits. A single-use grant binds its spend under its own profile (LIP-0006 section 3, for v1; LIP-0008 section 4, for v4), and this section states no byte of that binding. | None of its own |

Two boundaries of the leaf come from the landed texts and are stated,
not widened. A small wallet whose key an agent holds is a separate
risk tier that no grant restricts after the fact (LIP-0006, security
consequences); this leaf governs spends at the executor and claims
nothing about coins outside it. And observations and effects are not
atomic: a revocation or a reorganisation after the last check can race
a broadcast, and a later reorganisation does not undo a payment that
left (LIP-0006 section 4; LIP-0008 section 3).

### 4. `swarma/name-update`: a Namecoin name operation on a named name

The effect of this leaf is one operation on one Namecoin name, which
the arguments name exactly: the executor writes a new value for that
name, under the key that controls the name's output. Whoever controls
the name output controls the name (`protocol/names.md` section 1), so
the executor of this leaf holds, or signs through a holder of, that
name-owner key; which service that may be, and under what custody, no
landed text states, and this section assigns neither.

| Item of LIP-0018 section 3 | This profile |
| --- | --- |
| Name | `swarma/name-update`, one exact leaf (P1.1) |
| Service type | `names.nmc` of LIP-0007 section 1, a semantic candidate: register and update names, with permitted names, operation stages, fees and ownership policy to bind. This leaf takes the update of that candidate (P4.2) |
| Arguments and targets | The exact name, as the chain writes it. The complete new value that the operation will write, as exact octets. A bound for the fees of the operation, in atomic units of the chain's asset. All stand under the request signature (P1.5) |
| Effect or work | An effect on the chain: the name operation. Authorized by machine members only (P1.6). Composing a value is the agent's work; writing it is the effect |
| Limits | The kind that LIP-0008 section 2 names by the meaning "Name operations": the number of name registrations and updates. This draft assigns that kind no identifier (section 6). The fees of the operation are a spend of the executor's funding and no charge under `swarma/coins`, unless the grant and the contract state the fee bound as such a charge; the draft decides neither reading and states both in P4.5 |
| Receipt | Beside P1.11: the name, the hash of the value that stood before the operation as the executor's node read it, the hash of the value that the operation wrote, the transaction id of the operation, and the state that the executor's own node showed for it when it reported, in the mempool or confirmed at a stated depth. A receipt states no finality: a reorganisation can remove the operation, and the receipt does not claim otherwise |
| Refusal codes, vectors and checker, path | Section 8; cases S38-10 to S38-13; this LIP, under LIP-0001 |

Checks of the executor, beside section 1:

| Rule | Requirement | Refusal |
| --- | --- | --- |
| P4.1 | The name of the arguments is the name that the limit's resource permits and no other. One request operates on one name; a name that the arguments name by a pattern, a prefix or a list is no argument of this leaf. (This draft's rule.) | `ACTION_TARGET` (proposed) |
| P4.2 | The operation is an update of a name that the executor's own node shows as registered and unexpired at the tip of the observation. A registration, with its stages, and a transfer of the name to another owner are no part of this leaf and refuse here; the wallet profile likewise gives name operations no place and leaves their continuations to a separate design (LIP-0006 section 3). An expired name refuses (`protocol/names.md` section 1). (This draft's scope for the leaf.) | `ACTION_TARGET` (proposed); the refusal of the read where the node cannot show the name |
| P4.3 | The new value is complete in the arguments and fits the chain's bound for a name value, 520 bytes (`protocol/names.md` section 2; LIP-0010 section 8). `X` writes those octets and no others (P1.5): it completes no member, carries no member over from the old value, and takes no value from a configuration or a model at operation time. Whether the value is a value that the readers of LIP-0010 accept is a check for those readers at their admissions; this leaf adds the executor's own read of the old value for the receipt and for P4.4, and a value that no reader profile it runs can parse refuses as an argument it cannot check. (This draft's rule.) | `ACTION_ARGUMENTS` (proposed) |
| P4.4 | The operation keeps the owner of the name: its name output pays the same owner key that the current output pays, read under the ownership profile that the executor runs (LIP-0021, every rule a proposal). A new value that changes the owner is a transfer and refuses under P4.2, by whatever member or output the change would come. What a change of the value does to grants that are bound to the name follows the landed texts and is reported, not hidden: an update of an issuer's name that changes the owner or `swarma` ends that issuer's grants on the chain that holds the change, and a renewal ends nothing (LIP-0008 section 3). `X` states in its receipt, where it can read them, whether the new value's `swarma` differs from the old; it refuses no update for that difference alone, because the difference is what the grant that authorized the update may exist to make. (This draft's rule.) | `ACTION_TARGET` (proposed) for an owner change |
| P4.5 | The reservation of P1.7 counts one name operation, durable before the operation is signed. The fee bound of the arguments bounds what the operation may pay in fees; an operation that cannot be built inside it is not broadcast and is reported as refused, with the reservation retained until reconciled where a broadcast may have left (P1.10). Whether the fee is also charged under a `swarma/coins` limit of `G` is open, and an executor that charges it states the charge in its receipt under that limit's key. (This draft's rule, with the open point named.) | As in P1.7 |
| P4.6 | Before the operation is signed, `X` rechecks under P1.8 and reads the name once more in the same observation: the current output is still the one it checked, still controlled by the same owner, and the value still the one whose hash the receipt will state as the old value. A name whose output another operation has spent since the first read, in a block or in the mempool as the executor's node shows it, refuses without a new operation on a stale output. (This draft's rule.) | The refusal of the read |
| P4.7 | An operation whose outcome is not known is not built again on the new output that it may have created (P1.10). A second update of the same name is a second request, against the count again, on the state that the executor's node then shows. | None of its own |

The price of the leaf is the custody it needs. A service that can
write a name can write every value of that name, and with the owner
key of an issuer's name it can end that issuer's grants or take the
name. The landed key layout keeps a name-owner key with the operator
of the agent or the owner, and no text gives an executor of this kind
a place in it (KEY-MAP.md; KEY-REGISTRY.md). Until one does, the leaf
is a profile in search of a deployment, and the checks above bound
what a conforming executor does and not what a holder of the key can
do outside it. Section "Security consequences" states this again with
the other three.

### 5. `swarma/model-call`: a model request through a model service

The effect of this leaf is one model request: the executor, a model
service, sends the stated request to the stated model at its upstream
account and returns the model's answer, charging the request against
`swarma/model-cost` and `swarma/model-tokens` limits of `G`
(section 6). The executor verifies the presentation, the signed
limits, the validity and the seal against its own view of the chain;
a gateway can deliver the request and cannot substitute a prepared
binding for that verification (LIP-0008 section 5). Where a deployment
calls its model service a gateway, the executor of this leaf is that
service only where the service itself makes the checks of section 1;
a gateway that only prepares a slot binding is a carrier here and no
executor (LIP-0028, Motivation).

| Item of LIP-0018 section 3 | This profile |
| --- | --- |
| Name | `swarma/model-call`, one exact leaf (P1.1) |
| Service type | `model.proxy` of LIP-0007 section 1: invoke an explicitly selected model, and account for requests, tokens, cost and the output of a request |
| Arguments and targets | The selected service and model, as the model service names them in its profile. The complete request that will be sent to the model. The largest output that the request asks for, in tokens of the model and token-accounting profile that the tokens limit names. All stand under the request signature where the request is signed (P1.5; for a request in a session, P5.4) |
| Effect or work | An effect at the upstream model account: the upstream call and its cost. The reasoning that the answer feeds is the agent's work |
| Limits | `swarma/model-cost` and `swarma/model-tokens` (section 6). Beside them, by their meanings in LIP-0008 section 2 and with no identifier assigned here: "Model requests", the count of admitted requests in the window, and "Maximum answer length" with its signed default output allowance, which cannot exceed the per-request maximum or the remaining cumulative allowance |
| Receipt | Beside P1.11: the model that answered, the input and output tokens counted under the named accounting profile, the cost charged and its basis under the same price table as the reservation (LIP-0031 L17/L18; section 6). The receipt states no part of the request or the answer beyond what the parties need for a dispute: the hashes that a later verdict under LIP-0011 would bind are open with that profile, whose request hash is defined per service profile and not here |
| Refusal codes, vectors and checker, path | Section 8; cases S38-14 to S38-18; this LIP, under LIP-0001 |

Checks of the executor, beside section 1:

| Rule | Requirement | Refusal |
| --- | --- | --- |
| P5.1 | The model of the arguments is one that the resource of the tokens and cost limits names, together with one model and token-accounting profile for both. A request that names another model, or tokens counted under another profile, is no call under these limits. The largest output of the arguments stands against the per-request maximum of its kind, and against the remaining output allowance at the reservation of P5.2. A default that the arguments omit comes from the signed default of the grant and from nowhere else (LIP-0008 section 2). An absent largest output with no signed default is the no-finite-maximum case of LIP-0031 L18/L20, not malformed arguments. | `ACTION_TARGET` (proposed) for the model; `ACTION_ARGUMENTS` (proposed) for a present but malformed output bound; `SPEND_OVER` for a well-formed bound above a stated per-request ceiling, or an absent bound without a signed default where a per-request cost or output key applies (LIP-0031 L18/L20/L21). Without such a key, the absent bound refuses at P5.2's reservation as `OWN_LIMIT_OVER` or `ROW_CAP_OVER`, in LIP-0031 section 6's order; nothing is reserved |
| P5.2 | The reservation of P1.7 comes before the upstream call and covers, for the cost kind, the price of the request at its largest stated output under LIP-0031 L17's exact price-table maximum and single upward conversion, and, for the tokens kind, the input tokens as counted before the call and that largest output, in separate `input-token` and `output-token` accounts (LIP-0031 L19/L20), never their sum in one token account. Input that cannot be counted under the named accounting profile before the call reserves nothing and refuses. No upstream call is made on an estimate that no reservation covers. (This draft's rule, on the reservation duty of LIP-0008 section 2.) | `OWN_LIMIT_OVER`, `ROW_CAP_OVER`; `ACTION_ARGUMENTS` (proposed) where the input has no count |
| P5.3 | During the call, `X` counts the output as it arrives and delivers no output beyond the smaller of the largest output of the arguments and what the reservation covers. Where the upstream returns more than was reserved, the excess is not delivered as this request's answer, and the cost that the upstream nevertheless charged is reconciled against the reservation and reported in the receipt, never taken silently from a later request's allowance. Known outcomes follow P6.1 and LIP-0031 L18/L20; an upstream charge above the reservation is outside that profile and is charged neither above the reservation to this grant nor to a later request. (This draft's rule.) | None of its own |
| P5.4 | A request may arrive as a signed invocation, or in a session under LIP-0028 where the client cannot sign. In a session the request carries a bearer token and no signature, `X` makes the checks of the proof path before every reservation (LIP-0028 T4.5), the session's accounts stand beside those of `G` (T4.6), and a request sent twice is two requests, because no sender signed its identity (LIP-0028 section 4). The commands that open, extend and close a session are separate leaves of the type's table (LIP-0028 T1.1) and no part of this leaf; until the co-author agrees to sessions, a v4 model service admits signed invocations alone (LIP-0008 section 5). | The refusals of LIP-0028 for a request in a session |
| P5.5 | An upstream call whose outcome is not known, no answer and no certain failure, keeps its reservation until the upstream account or the call's record reconciles it (P1.10), and the request is not sent again upstream under the same identity. Enforcement of every limit of this section needs the upstream secret intact at `X`: whoever steals it calls the model outside the accounting, as LIP-0008 section 2 states for the proxy of today. | None of its own |
| P5.6 | A moderation verdict over a model request, where a contract provides for one, judges the signed invocation as its request (LIP-0011 section 7, Draft text under a decision that awaits the co-author). This leaf neither calls a moderator nor defines a request hash; it leaves the content bound in the signed arguments (P1.5), so that a profile that needs the hash can take it over them. | None of its own |

### 6. The three shared limit kinds

The identifiers below already have one proposed profile,
[LIP-0031](LIP-0031-limit-kinds-1.md). This section uses that profile,
not a second definition. The W11.4 limit remains an object with exactly
`kind`, `resource`, `unit`, decimal-string `amount` and optional `period`;
`limits` remains an array. Its key is every member but `amount`.
LIP-0031 L1 to L10 supply the integer bounds, ceiling comparisons,
period families and instances, child/pool checks, atomic reservation
and uncertainty handling. In particular, L3 defines `swarma/per-request`,
`swarma/blocks-<N>` and `swarma/seconds-<S>` with each kind's supported
families, and L4 refuses unsupported resource, unit or period texts as
`LIMIT_UNSUPPORTED`, not as an undefined kind. No conversion, new limit
member or alternate period arithmetic is introduced here.

Reservation remains durable before any effect, atomic over every own
and applicable row account (P1.7; LIP-0031 L8). Replicas share one
journal; one request is reserved once, and a request refused before
reservation consumes nothing. An unknown outcome, a restart or a
revocation releases nothing (P1.10; LIP-0031 L9). The machine-readable
contract mirror, where required or supplied, retains LIP-0031 L10;
the scoped contract-free root of LIP-0035 is not given a new mirror.

**P6.1 — Settlement (option A).** **DECIDED: actual settlement and
release of the difference only.** Apply LIP-0031 L9:
for each shared kind, settle a known outcome at its actual consumption
as that kind measures it, and release the difference from the reservation.
This is the choice recorded by the owner event above, with the co-author's
agreement pending, not acceptance of the other proposed rules of
LIP-0031 or of this LIP. Each kind below cites this one rule.

**PROPOSED mechanics and per-kind readings.** LIP-0031 L9 releases
in the same accounts, atomically with the journal entry recording the
outcome, once for that request identity and not again on replay.
A known outcome in which the effect did not happen settles at the
consumption its kind states for it (LIP-0031 L13/L15, L18 and L20),
which is zero only where nothing was consumed. An unknown outcome
retains its reservation. No settlement charges above the reservation
to the grant. These carried rules remain PROPOSED.

#### `swarma/coins`

| Item of LIP-0018 section 2 | Shared profile used by this action |
| --- | --- |
| Identifier and resource | `swarma/coins`, LIP-0031 L11: `<system>:<asset>`, with `namecoin:NMC` assigned. Other payment systems require their own assigned texts; permitted-target encoding remains open (P3.2), not an invented suffix to this resource |
| Unit and integer scale | L11: atomic asset units; `namecoin:NMC` uses `atomic`, 100000000 per NMC. Amounts use W11.1 decimal strings and exact integer arithmetic |
| Bounds and rounding | L1 and L13: integer form 0 to 18446744073709551615, no floating-point amounts; charge the value paid away plus applicable fees, excluding change |
| Period and aggregation | L3, L5, L7 and L12: whole-window total, stated period instances and the per-request ceiling of L14. Only coins on the chain of the grant's `genesis` admit block and clock families; other chains and off-chain rails admit clock counting only |
| Reservation, uncertainty and settlement | P3.3 and L13 reserve amount plus fee bound before signing or broadcast. P3.5 retains unknown outcomes. Known amount and fees use L13 and the single settlement rule P6.1 |
| Refusal codes | Section 8; LIP-0031 L4/L14 and L8 retain their codes. `ACTION_TARGET` and `ACTION_ARGUMENTS` check the request against a recognised limit, not the recognisability of that limit |
| Vectors and checker, path | Cases S38-5 to S38-9 and S38-C1/S38-C2; invocation/receipt octets and real-executor vectors remain open. LIP-0031 sections 1 and 2, consumed by this LIP |

#### `swarma/model-tokens`

| Item of LIP-0018 section 2 | Shared profile used by this action |
| --- | --- |
| Identifier and resource | `swarma/model-tokens`, LIP-0031 L19: `<model>/<accounting>`, with the model text also priced by L16; deployment model/accounting identifiers remain open |
| Unit and integer scale | L19: `input-token` and `output-token`, two separate keys for one resource, not two resources distinguished by direction and not one summed input/output account |
| Bounds and rounding | L1 and L19: exact integer counts, with no rounding or conversion between accountings |
| Period and aggregation | L3, L5, L7 and L21: whole-window and clock-period accounts; the stated per-request input/output ceilings are checked before reservation. Block periods are unsupported |
| Reservation, uncertainty and settlement | L20 counts input before the call and reserves longest permitted output separately. Unknown outcomes retain both reservations. The executor's counted outcome, not an upstream substitute count, follows L20 and P6.1 |
| Refusal codes | Section 8; unsupported limit texts use L4, per-request ceilings use L21 and accounts use L8; request model mismatch and uncountable input keep P5.1/P5.2's distinct checks |
| Vectors and checker, path | Cases S38-14 to S38-18 and S38-T1/S38-T2; exact wire vectors remain open. LIP-0031 sections 1 and 4, consumed by this LIP |

#### `swarma/model-cost`

| Item of LIP-0018 section 2 | Shared profile used by this action |
| --- | --- |
| Identifier and resource | `swarma/model-cost`, LIP-0031 L16: the executor's priced model; currency and scale are in `unit`, not a competing resource syntax |
| Unit and integer scale | L16: `<currency>/<scale>`; no currency or scale conversion |
| Bounds and rounding | L17/L18: exact rational products and sum over the whole request, followed by one upward conversion to integer subunits for reservation and one for actual cost; no per-part rounding or binary64 arithmetic |
| Period and aggregation | L3, L5, L7 and L18A: whole-window and clock-period accounts plus a stated per-request cost ceiling; block periods are unsupported. Price-table authority, binding and changes remain open in LIP-0031 |
| Reservation, uncertainty and settlement | L17 reserves the finite table maximum before the call. L18 supplies actual cost under that same table and the outside-profile overrun boundary; settlement follows P6.1 |
| Refusal codes | Section 8; L4 for unsupported texts, L18/L18A for a missing finite maximum or a per-request excess, and L8 for accounts |
| Vectors and checker, path | Cases S38-14 to S38-18 and S38-M1/S38-M2; exact wire vectors remain open. LIP-0031 sections 1 and 3, consumed by this LIP |

**Kinds stated by meaning alone.** Five further kinds stand in the
profiles above by the meanings that LIP-0008 section 2 gives them, and
this draft assigns none of them an identifier: outbound messages and
name operations, of the decision of 2026-11-14 whose meanings in that
text are its draft's proposal, and model requests, maximum answer
length and required confirmation depth, of the initial list. A request
under sections 2 or 4 consumes a count of a kind without an identifier
and therefore refuses at P1.4 until a profile of that kind assigns
one. The two leaves are defined here so that their checks have a place
to stand when the kinds arrive; until then `swarma/spend-coins` and
`swarma/model-call` are the two of the four that a grant can carry to
an effect, and the text says so rather than naming identifiers that
nobody assigned.
Whether `swarma/model-call` also consumes the unnamed model-request
count is open, not decided by that statement. If required, that count
likewise blocks the effect at P1.4 until its kind has a profile and
identifier; this LIP assigns neither by implication.

### 7. The proposed registry rows

An entry joins a registry through its profile (LIP-0020 W11.14 rule 3).
The four action entries below are **PROPOSED**. W11.14 also records
LIP-0030's distinct start/restart/renew/stop grant actions and its three
station kinds; its halt leaf is an owner command and is not in `actions`.
Those proposals and their boundaries remain unchanged. A side that
adopts none of a leaf's profile still refuses it under W11.14 rule 1.
Discovery of a supported service is through the LIP-0010 section 11.1
manifest declaration, never an alternate authority pin.

| Action identifier | Profile | Service type that offers it | State |
| --- | --- | --- | --- |
| `swarma/post-message` | Section 2 of this LIP | Open (section 2) | Proposed |
| `swarma/spend-coins` | Section 3 of this LIP | A wallet-type service (`wallet.nmc`, LIP-0007 section 1) | Proposed |
| `swarma/name-update` | Section 4 of this LIP | `names.nmc` (LIP-0007 section 1) | Proposed |
| `swarma/model-call` | Section 5 of this LIP | `model.proxy` (LIP-0007 section 1) | Proposed |

| Limit kind | Profile | Unit | State |
| --- | --- | --- | --- |
| `swarma/coins` | LIP-0031 sections 1 and 2; section 6 here consumes it | L11: `atomic` for `namecoin:NMC` | Proposed in LIP-0031; P6.1 records the settlement decision |
| `swarma/model-tokens` | LIP-0031 sections 1 and 4; section 6 here consumes it | L19: `input-token` or `output-token` | Proposed in LIP-0031; P6.1 records the settlement decision |
| `swarma/model-cost` | LIP-0031 sections 1 and 3; section 6 here consumes it | L16: `<currency>/<scale>` | Proposed in LIP-0031; P6.1 records the settlement decision |

The reserved kind `policy` stays reserved and undefined (LIP-0008
section 12.4), and a request that needs it refuses at P1.4.

### 8. Refusals and their order

Two codes of this LIP are new. Each is a proposal with this draft, and
neither binds a reader before it.

| Code | What it reports | Rules | State |
| --- | --- | --- | --- |
| `ACTION_ARGUMENTS` | The arguments are not complete for the leaf, are not in the form that its profile states, or differ from the actual arguments of the effect. The request's amount unit differing from a recognised limit, a present but malformed output bound, a name value that no profile of the executor can read, and input with no token count stand here. Exception: an absent largest output with no signed default follows LIP-0031 L18/L20 under P5.1, not this code. A well-formed longest output above a stated shared-kind per-request ceiling instead uses `SPEND_OVER` | P1.5, P2.2, P3.1, P4.3, P5.1, P5.2 | New with this LIP |
| `ACTION_TARGET` | The target of the effect is not the one that the grant and its limits permit: a signing key or a destination of a message, an asset, a rail or a payee of a payment, a name, a registration or a transfer asked of the update leaf, a model or a currency of a model request | P2.1, P2.2, P3.1, P3.2, P4.1, P4.2, P4.4, P5.1 | New with this LIP |
| `ACTION_UNDEFINED` | No type profile of the executor defines the action | P1.4 | LIP-0020 W11.14 |
| `LIMIT_KIND_UNDEFINED` | A limit kind that the request consumes has no type profile at the executor | P1.4 | LIP-0020 W11.14 |
| `LIMIT_UNSUPPORTED` | A shared kind is known but its resource, unit or period is unsupported | P1.4 | LIP-0031 L4 |
| `SPEND_OVER` | A shared kind exceeds a stated per-request ceiling, or has no finite maximum under L18/L20 and the applicable per-request cost or output key is stated. This includes an absent largest output with no signed default. With no such key, a missing finite maximum instead refuses at reservation as `OWN_LIMIT_OVER` or `ROW_CAP_OVER`, in LIP-0031 section 6's order. A present but malformed output bound is `ACTION_ARGUMENTS` | P3.3, P5.1, section 6 | LIP-0031 L14, L18, L18A, L20, L21 |
| `LIMIT_CLOCK_REGRESSION` | A clock-period instance regresses at reservation | P1.7, section 6 | LIP-0031 L7 and section 6 |
| `OWN_LIMIT_OVER` | A reservation would exceed the own account of `G` for its key | P1.7 | LIP-0026 R5.6 |
| `ROW_CAP_OVER` | A reservation would exceed the row account of the parent for its key | P1.7 | LIP-0026 R5.6 |

P8.1. The checks of a request stand in this order. First the admission
of the grant and of its path and the authentication of the request, at
their places in the landed texts (LIP-0008 sections 4 and 12; LIP-0014
section 8.4 for a child). Then the checks of the invocation itself
(row E0 there). LIP-0030 section 6 proposes their base codes, and the
[LIP-0014 companion section 5 (O3)](LIP-0014-source-contract-proposals.md#5-o3-invocation-checks--proposed)
proposes E0.1 to E0.4's order. Both remain PROPOSED; this LIP adopts
none of their assignments. Then the action
is defined (E1), then every kind it consumes is defined (E2), with the
shared-kind texts checked as `LIMIT_UNSUPPORTED` under LIP-0031 L4. Then the
checks of this LIP that need no ledger: `ACTION_TARGET` before
`ACTION_ARGUMENTS`, because whose key, which asset and which name are
questions about the grant and its limits, and the form of the
arguments is a question about the request, and this draft puts the
grant first as F17 of the same table puts the keys of a child's limits
before their amounts. Then the shared-kind per-request checks
(`SPEND_OVER`, LIP-0031 section 6), and only then the reservation (E3),
in the order of P1.7 and LIP-0031 section 6 for the shared kinds. Then
the effect, with the rechecks of P1.8 and of the leaf. An
outcome after a reservation (P3.4, P3.5, P5.3, P5.5) is a statement of
a receipt and no new refusal of admission. The place of the two new
codes between E2 and E3 is this draft's proposal; all of E0 to E3
stand before any reservation or effect (LIP-0008 section 4), and
nothing here moves a check across that line. At each shared-kind key,
LIP-0031 section 6 checks `LIMIT_CLOCK_REGRESSION` first when applicable,
then `OWN_LIMIT_OVER`, then `ROW_CAP_OVER`; all keys pass before any
write. Unsupported limit texts and recognised limits whose request
targets differ are different failures; the former precede the latter.
These two action codes have no other definition in the current refusal
registries; the shared-kind codes are reused, not reassigned.

P8.2. No refusal of this section records a closure of a grant (section
1), and a request refused before its reservation consumes nothing.
Under one set of profiles the two new codes agree at every side, as
the codes of E1 and E2 do; two executors that run other profiles of
the counting kinds of section 6 can still disagree at E2, which is the
state of those kinds and no new divergence of this LIP.

### 9. Cases

The cases state outcomes in words, on stated facts. Vectors come with
the members of the invocation and of the receipt, and each case below
is written so that it becomes a vector then without a new decision: a
valid control, and beside it one defect. No case was run; no node, no
wallet, no name writer and no model upstream was operated for this
draft.

| Case | Setting | Outcome |
| --- | --- | --- |
| S38-1 | A `post-message` request to a permitted destination with stated content, at an executor that runs this profile and a profile of the outbound-messages kind | Admitted. One message is reserved, the message is signed under the agent's messaging key and posted, and the receipt states the destination and the message's identifier |
| S38-2 | The same request to a destination that the limit's resource does not permit; and the same with content that `X` would have to complete outside the signature | `ACTION_TARGET`; `ACTION_ARGUMENTS`. Nothing is signed and nothing is reserved |
| S38-3 | A `post-message` request that asks `X` to sign as another agent, or under a key that the caller supplies | `ACTION_TARGET`. No signature under either key |
| S38-4 | The request of S38-1 once more; and, beside it, a posting whose outcome the transport does not report | No second posting and no second charge (P1.9). The uncertain posting keeps its reservation and is reported as uncertain (P2.3) |
| S38-5 | A `spend-coins` request inside every stated limit, amount and fee bound together | Reserved, rechecked and paid. The receipt states the payee, the amount and fees as paid and the spend's identifier |
| S38-6 | The same request with the amount one atomic unit below the remaining allowance and a fee bound of two units | `OWN_LIMIT_OVER` (or `ROW_CAP_OVER` under a child): the charge is amount and fees together (P3.3). Nothing is signed |
| S38-7 | The same amount on another asset; on the same asset through another rail; in another unit | `ACTION_TARGET` for the asset and the rail; `ACTION_ARGUMENTS` for the unit (P3.1) |
| S38-8 | A payee that the applicable target constraint does not permit (form open, P3.2), at an amount of one atomic unit | `ACTION_TARGET`, before any amount is compared (P3.2) |
| S38-9 | A spend broadcast and then no certain outcome; the same request once more; a new request for the same payment under a new nonce | The reservation stands and the receipt is uncertain. The repeat makes no second spend. The new request is a second payment and is charged as one; it reconciles nothing (P3.5) |
| S38-10 | A `name-update` request for a registered, unexpired name with a complete new value within 520 bytes that keeps the owner | Reserved, re-read and written. The receipt states the name, both value hashes, the transaction id and the observed state |
| S38-11 | A value of 521 bytes; a value that `X` would complete from the old value; a request for a name that the limit does not permit | `ACTION_ARGUMENTS` twice; `ACTION_TARGET` (P4.1, P4.3) |
| S38-12 | A request to register a new name; to write a name that the node shows expired; to move the name to a new owner | `ACTION_TARGET` for all three (P4.2, P4.4), unlike the registered, unexpired control S38-10. No operation is built |
| S38-13 | The request of S38-10, and between its two reads another operation spends the name's output | Refused on the second read, with no operation on the stale output (P4.6) |
| S38-14 | A `model-call` request whose counted input and largest output fit both limits, at the reserved price | Reserved before the call, answered, and the receipt states the model, both token counts and the cost charged with its basis |
| S38-15 | A model that the limits' resource does not name; input that has no count under the named accounting profile | `ACTION_TARGET`; `ACTION_ARGUMENTS`. No upstream call (P5.1, P5.2) |
| S38-16 | A largest output above the per-request maximum; and one above the remaining output allowance but inside the maximum | `SPEND_OVER` for the first (LIP-0031 L21); the refusal of the account for the second (P5.1) |
| S38-16A | S38-14 with the sole change that the signed arguments omit the largest output and there is no signed default; an applicable per-request cost or output key is stated | `SPEND_OVER`, not `ACTION_ARGUMENTS` (P5.1; LIP-0031 L18/L20). No reservation or upstream call |
| S38-16B | S38-16A at a root grant with whole-window cost and output ceilings, but without an applicable per-request cost or output key | `OWN_LIMIT_OVER` at the first consumed own account in LIP-0031 section 6's order. Nothing is reserved and no upstream call is made; not `ACTION_ARGUMENTS` (P5.1) |
| S38-16C | S38-14 with a present output bound that is malformed under the accounting profile rather than absent | `ACTION_ARGUMENTS`, whether or not a per-request key is stated (P5.1). No reservation or upstream call. S38-14's well-formed bound remains the positive control |
| S38-17 | An upstream answer longer than the largest output of the arguments | The answer is cut at the bound and no more is delivered; the excess cost is reconciled and reported, never moved to a later request (P5.3) |
| S38-18 | An upstream call with no certain outcome, and the same request sent twice in a session | The reservation stands and the outcome is uncertain (P5.5). In a session the two sends are two requests and are charged twice (P5.4) |
| S38-19 | Each of the four leaves at an executor that runs no profile of this LIP, under a well-formed grant whose `actions` state the leaf | `ACTION_UNDEFINED` for each (P1.4): that the text stands in the grant defines nothing |
| S38-20 | A `post-message` and a `name-update` request at an executor that runs this LIP and no profile of the counting kinds of section 6 | `LIMIT_KIND_UNDEFINED` for both, until a kind profile assigns those kinds their identifiers. Beside them a `spend-coins` request under `swarma/coins` is admitted |
| S38-21 | A request of S38-5 under a grant whose terms carry a text | Refused at the effect service, with no code from a landed text (P1.6). Under a grant without a text for the same payment it is admitted |
| S38-22 | The tip of `X`'s node older than the cutoff of the class of P1.12, for each leaf in turn | Each refuses under the observation profile. A request below the cutoff after a new block is admitted; no refusal closed the grant |
| S38-K1 | A known limit. The upstream API secret of the model service is stolen and used directly | The calls bypass every limit of section 5 (P5.5). The journal of `X` shows no charge, because there was no request |
| S38-K2 | A known limit. The holder of the name-owner key writes a name outside an executor of section 4 | The write is valid on the chain and no check of this LIP ran. The leaf bounds a conforming executor and not the key |
| S38-K3 | A known limit. A message posted under section 2 is shown to a third party as proof that a grant ordered its content | It proves no such thing: the message binds the agent's key alone (section 2) |

#### Shared settlement controls and one-defect cases

These are semantic contract fixtures, not invocation octets or executed
service tests. Each control assumes the shared-kind profile, valid
authority, recognised keys, sufficient ceilings and a durable reservation
before the effect. Each negative case changes only the settlement step
as stated, retaining unused allowance or zeroing actual consumption; it is nonconforming to
P6.1, not a new request refusal code. The same check covers every own
and applicable row account and its original period instance. Other
requests' debits are unchanged.

| Case | Kind and setting | Required outcome |
| --- | --- | --- |
| S38-C1 | `swarma/coins`: reserve 10 atomic units, payment 3 plus fee bound 7; known actual payment 3 plus fee 1 = 4 | Debit 4, release 6, atomically with the outcome (P6.1; LIP-0031 L9/L13). Replay changes no account and sends no second payment |
| S38-C2 | S38-C1 with the sole defect that settlement retains the reserved 10 and releases 0 | Nonconforming to P6.1: the required debit is 4 and release is 6, not 10 and 0. No repair may create a second payment |
| S38-C3 | `swarma/coins`: reserve 10 atomic units, payment 3 plus fee bound 7; the payment is displaced by a transaction returning the coins to the payer, and the attempt actually paid fee 2 | Debit 2, release 8 (P6.1; LIP-0031 L13/L15): the payment value is 0, not the paid fee |
| S38-C4 | S38-C3 with the sole defect that the known failed payment settles at debit 0 and release 10 | Nonconforming to P6.1 and LIP-0031 L13/L15: the fee debit must be 2 and release 8. A known non-effect does not erase actual consumption |
| S38-C5 | The reservation of S38-C3, but a known refusal before broadcast, with no value or fee consumed | Debit 0, release 10 (P3.4; P6.1; LIP-0031 L13/L15). Zero is correct here because nothing was consumed, unlike S38-C3 |
| S38-T1 | `swarma/model-tokens`: reserve 10 in the `output-token` account; the known actual output is 4 under the executor's accounting. The separate counted input was sent | Debit 4 output tokens, release 6 output tokens (P6.1; LIP-0031 L9/L20). Input settles separately at its counted reservation. Replay releases nothing again |
| S38-T2 | S38-T1 with the sole defect that output settlement retains the reserved 10 and releases 0 | Nonconforming to P6.1: the output debit must be 4 and release 6; neither the input account nor a new model call may absorb the difference |
| S38-T3 | `swarma/model-tokens`: input counted and reserved at 4 was sent; output reserved at 10; the known upstream refusal returned no output | Input debit 4, release 0; output debit 0, release 10 (P6.1; LIP-0031 L20). A refusal does not erase the sent input's consumption |
| S38-T4 | S38-T3 with the sole defect that input settles at debit 0 and release 4 | Nonconforming to P6.1 and LIP-0031 L20: input sent must settle at its reservation of 4, irrespective of the answer |
| S38-M1 | `swarma/model-cost`: finite table maximum reserves 10 integer subunits; the known actual whole-request cost under that same table converts once upward to 4 | Debit 4, release 6 (P6.1; LIP-0031 L9/L18). Replay changes neither debit nor release and makes no new upstream call |
| S38-M2 | S38-M1 with the sole defect that cost settlement retains the reserved 10 and releases 0 | Nonconforming to P6.1: the required debit is 4 and release is 6; the difference cannot be charged to a later request |
| S38-M3 | `swarma/model-cost`: reserve 10 integer subunits; known priced work converts once upward to actual cost 4, but the answer is unusable | Debit 4, release 6 (P6.1; LIP-0031 L18). Priced work is charged whether or not the answer is used |
| S38-M4 | S38-M3 with the sole defect that an unusable answer settles at debit 0 and release 10 | Nonconforming to P6.1 and LIP-0031 L18: actual priced work still debits 4 and releases 6 |
| S38-U1 | S38-C1, S38-T1 and S38-M1 separately, with the sole changed fact that the outcome is still unknown rather than established at 4 | Each keeps its full reservation of 10 and releases 0. A restart, revocation or partial observation is not evidence permitting the control's release (P1.10; LIP-0031 L9) |

## Sources

No service, no node, no wallet, no upstream model account and no
messaging transport was run for this LIP.

| Statement | Source |
| --- | --- |
| The proposed registries, `ACTION_UNDEFINED` and `LIMIT_KIND_UNDEFINED`, and how an entry joins a registry | LIP-0020 W11.4 and W11.14 |
| The members of a grant that these profiles read: one executor, `actions`, and a limit as kind, resource, unit, amount and an optional period, with the amount in the string form | LIP-0020 W11.1, W11.2 and W11.4 |
| The admission order, the concrete executor, the proof path, exact leaves, the `swarma/` reservation, the time measures and the seal closure from the mempool | LIP-0008 sections 4, 5.1, 12.1, 12.2, 12.3 and 12.5 |
| The kinds by their meanings, the further kinds of the decision of 2026-11-14, the contract mirror, operator ceilings, durable reservation before an effect and uncertain effects that retain it | LIP-0008 section 2 |
| The 60 and 90 minute cutoffs and the class of an action | LIP-0008 section 6; LIP-0022, "What is decided and what is proposed" |
| The wallet service v1 profile: its five actions, its admission and reservation order, its receipts and its recovery, and its rejection of name actions | LIP-0006 sections 3 to 6 |
| Text governs work and never an effect | LIP-0006 section 7 |
| The service types and the boundary that each future profile has to define | LIP-0007 section 1 |
| What a proposal for a limit kind and for an action leaf has to state | LIP-0018 sections 2 and 3 |
| The accounts, the atomic reservation, one charge for one identity, and that a refused request reserves nothing | LIP-0026 section 5 and R6.2 |
| The steps E0 to E3 of a request under a child and the place of the action and kind checks | LIP-0014 section 8.4 |
| The key holder's gate, its typed operations and the transport operations that authorize nothing | LIP-0013 section 3.6, J7.5 and J7.7 |
| Sessions for a client that cannot sign, at the model proxy first | LIP-0028 sections 1, 4 and 5 |
| The invocation as the request of a verdict, and its salted binding inside an encrypted message | LIP-0011 section 7 |
| Whoever controls the name output controls the name, an expired name refuses, and the 520 bytes of a value | `protocol/names.md` sections 1 and 2; LIP-0010 section 8 |
| The owner of a name read from its output script | LIP-0021 |
| That a change of an issuer name's owner or `swarma` ends its grants and a renewal ends nothing | LIP-0008 section 3 |
| The gateway-bound model proxy of today and why a v4 executor verifies for itself | LIP-0008, "Current state" and section 5; LIP-0028, Motivation |
| Existing session leaves and independent starts/level/span kinds | LIP-0030 section 3; not redefined here |
| The shared kinds, exact resource/unit/period forms and refusal order | LIP-0031 L1 to L21 and section 6 |
| Settlement choice A for this re-filing | Owner decision of 2026-11-20, event `$VY_Ow-Yi4YWA695VYxcLlg0EdizZ6p8UzPkpr37ZyGU`; P6.1 references LIP-0031 L9 |
| Manifest service discovery, not authority; separate auth-key role | LIP-0010 SH7 and section 11.1; LIP-0034 A1 to A3 |
| Contract-free root scope, action spelling and limit-array form | LIP-0035 sections 1 and 2.1; LIP-0020 W11.4 |

## Alternatives

- **One profile per service type, without `swarma/` leaves.** Each type
  of LIP-0007 would name its own commands, and no cross-type vocabulary
  would exist. Two of the four effects, a posted message and a model
  call, are offered by services of more than one shape in the running
  system, and a grant that should follow the agent across them would
  state a different action for each. The reserved namespace exists for
  protocol-defined capabilities (LIP-0008 section 12.3), and these
  four are protocol effects before they are a provider's.
- **A generic spend leaf for every priced effect**, under which a
  model call and a name operation would be payments of their fees. It
  would charge cost and say nothing about tokens, about a value's
  octets, or about who a message is posted as: the checks that make
  each effect safe are not the checks of a payment, and one leaf would
  hide which of them ran.
- **Limit identifiers for every kind that the four actions touch, in
  this LIP.** Outbound messages, name operations, model requests,
  maximum answer length and required confirmation depth would take
  `swarma/` texts here. This draft names three and leaves five by
  their meanings, because a kind is its arithmetic and not its name
  (LIP-0018 section 2), and five arithmetics in one proposal are five
  that no reviewer counts. The cost is stated in section 6: two
  leaves wait for their kinds.
- **Returning the stored receipt for a repeated request, for every
  leaf**, as the wallet service v1 profile has it. For a message the
  receipt can carry the signed message, and handing it out again hands
  out the effect by a second path (P2.4). The draft leaves the answer
  open per leaf rather than settle it in common.

## Security consequences

Each leaf moves a credential that today sits with an operator into the
reach of a grant, and the grant becomes the bound that a stolen
request key can spend. That is the design of every grant-gated
service (LIP-0006), and it holds per leaf:

- Under `swarma/post-message` a captured request path posts as the
  agent until the grant ends, inside the count and the destinations of
  its limits. The messages are the agent's, and no later proof
  separates a posted message that its run wrote from one that a
  captor had posted (S38-K3).
- Under `swarma/spend-coins` the bound is the money: amount and fees
  against signed partitions at one executor. Coins outside the
  executor, in a wallet whose key an agent holds, are outside the leaf
  (section 3).
- Under `swarma/name-update` the executor needs the name-owner key or
  a signature from its holder, and that key is worth more than any one
  grant under it: it can transfer the name outside the leaf (S38-K2)
  and end every grant bound to the name (LIP-0008 section 3). No
  custody for such an executor is proposed here or landed elsewhere,
  and the leaf should not be adopted for an issuer's name before one
  is.
- Under `swarma/model-call` the upstream secret is the whole
  enforcement (S38-K1), and a bearer in a session is worth the
  session's limits to every process that can read it (LIP-0028).

For all four, a receipt is a signed statement of the executor and no
independent proof of the effect (LIP-0006 section 5, for its profile):
a payment is proved on its chain, a name operation on the chain, and a
posted message and a model answer by what the other side holds. The
draft claims for a receipt only what P1.11 states.

## Conformance impact

This LIP changes no byte of the wallet service v1 profile, no vector
and no reader. The four leaves remain PROPOSED; an executor that runs
none of their profiles behaves as in version 0.1.66. W11.14 records
their proposed entries beside the existing Draft profiles, without
adopting them at every side. P6.1 records only the owner-decided
settlement choice for the shared kinds. Conformance to an adopted
action profile still needs the invocation and receipt members, the
vectors of section 9 built on them, a checker and a run of each effect
against its resource; no such implementation or qualification is claimed.

## Open questions

- The members of `swarma-invocation/1` and of `swarma-receipt/1`, the
  journal key of a request, and with them every argument form and
  receipt member of sections 2 to 5 (LIP-0020 sections 3 and 6).
  LIP-0035 section 2.2's broker wrapper cannot carry these leaves until
  a signed action-argument binding is specified; no unsigned supplement
  is authorized by this LIP.
- Identifiers and profiles for the five kinds that section 6 states by
  meaning alone: outbound messages, name operations, model requests,
  maximum answer length and required confirmation depth. Until the
  first two exist, sections 2 and 4 are defined and unusable.
  Whether `model-call` consumes the unnamed model-request count is
  unresolved; if it does, P1.4 also blocks that leaf until its kind
  profile and identifier exist.
- Permitted-target encoding for coins and the other action constraints:
  LIP-0031 now fixes `<system>:<asset>`, `<model>/<accounting>`, the
  input/output units and `<currency>/<scale>`, but assigns no payee
  constraint, deployment model/accounting names or message destination
  form. No extra member or ad hoc resource extension is defined here.
- The contract's mirror of a period and its accounting after journal
  recovery remain open in LIP-0031 L9/L10. The period families and
  instance arithmetic themselves are no longer open here: L3/L7
  provide them. Calendar periods stay outside that profile.
- Settlement below reservation is resolved by the recorded owner
  decision and P6.1, not an open no-release alternative. Price-table
  binding, disputes and charges outside the reservation remain open
  as LIP-0031 L17/L18 state; this decision supplies no new encoding.
- The price of a model request: who states it, in what form the
  receipt binds it, and how a caller disputes a charged cost when a
  session left the request unsigned (LIP-0028). The token-counting
  profile for a model whose upstream counts in its own way.
- `post-message`: the service type that offers it; which key signs on
  each transport and through which holder (open already in LIP-0013
  section 3.6); the form of a destination; and whether a repeated
  request is answered with the stored receipt (P2.4).
- `name-update`: the custody of the name-owner key at an executor;
  whether registration joins the leaf or takes one of its own, with
  its stages and their fees; whether the fee is charged under
  `swarma/coins` (P4.5); and how an executor reads a pending operation
  of the name against one tip (open already for the reads of LIP-0021
  and LIP-0022).
- The risk class of each leaf (P1.12 proposes one class for the four),
  and, for `spend-coins` on more than one chain, that confirmation
  counts of different chains are no measures of one another
  (LIP-0008 section 2).
- The code for a grant that an effect service refuses under
  LIP-0006 section 7 (P1.6), which no landed text names, and adoption
  of the invocation-check codes proposed in LIP-0030 section 6 and
  the E0 order of the LIP-0014 companion O3, beside which the two
  codes of section 8 stand.
- Confirmation as part of an outcome for `spend-coins` and
  `name-update`: at what depth a receipt may call an effect
  confirmed, per asset and per value, which is the open tier table of
  LIP-0008 section 2 and of LIP-0022 section 5.
- The owners' acceptance of the four action identifiers, of the two codes
  and of their place, and of every rule above that this draft marks
  as its own, except the settlement choice already decided in P6.1.
