# LIP-0031: Limit-kind profiles 1 — coins, model cost, model tokens

- **Status:** Draft. The paragraph of section 5 that states the four
  rules is decided by the owner on 2026-11-17 and is in force in this
  version; the co-author's answer is folded in by amendment. Every
  other rule of this LIP remains proposed except the actual-settlement
  and release choice recorded in point 5 below, decided on 2026-11-20
  with the co-author's agreement pending. No other rule is adopted. The
  owner's requirement of 2026-11-17 that a period be expressible in
  clock time and, for chain coins, in blocks is recorded under "What
  is decided and what is proposed"; the rules that carry it are
  proposed like the rest.
- **Created:** 2026-11-17
- **Affects:** the first three entries of the registry of limit kinds
  (LIP-0020 W11.14): what a limit of each kind counts, in which unit and
  over which period, how an executor reserves and settles it, what a
  verifier compares at the admission of a child against the template and
  the pool of its parent, and what follows when a counter reaches its
  ceiling
- **Builds on:** LIP-0008 sections 2, 2.1, 4, 7.1 and 12.2, LIP-0018
  section 2, LIP-0020 sections 2 and 11 (W11.1, W11.4, W11.10, W11.14),
  LIP-0022 sections 1 to 5, LIP-0026 sections 1, 2, 5, 6 and 8,
  LIP-0014 sections 8.4 and 11.1 (J4.4 (a)) and LIP-0025
- **Deciders:** both owners

## Summary

No limit kind is defined. LIP-0020 W11.14 lists no defined kind —
version 0.1.58 proposes its first three entries in this LIP, and a
proposal defines none yet — and its rule 2 follows from that: a child
that states a limit, and
a child of a row whose template states one, refuses as
`LIMIT_KIND_UNDEFINED` at every side, and only a pair without limits
passes row F17 of LIP-0014 section 8.4. LIP-0008 section 2 names the
kinds by their meaning and leaves each of them to a type profile with
the items that LIP-0018 section 2 lists. No such profile exists, so no
signed limit of Grant v4 bounds anything yet: a grant can state one in
well-formed octets, and every side that follows the texts refuses the
child that carries it.

This LIP proposes the first three type profiles:

- the rules that the three kinds share: the existing members of a
  limit, the reading of `period`, the comparison of a child against the
  template of its row and against the pool, the accounts of a period,
  and the reservation (section 1);
- `swarma/coins`: an asset and payment-system identifier, an atomic
  unit, a maximum for one spend, a maximum for a period, and a total
  over the term of the grant including fees (section 2);
- `swarma/model-cost`: a cumulative cost ceiling per period in an exact
  currency and scale, reserved at the maximum before a request and
  settled at the actual cost (section 3);
- `swarma/model-tokens`: separate cumulative input and output token
  ceilings per period, under a named model and token-accounting profile
  (section 4);
- exhaustion and continuation, in the paragraph of section 5 that
  states the four rules, to which every other text points (decided
  by the owner on 2026-11-17 and in force in this version; the rest
  of this list is proposed except point 5's actual-settlement and
  release choice below);
- the refusal codes and their order (section 6), and the vector set
  that the profiles need, described and not built (section 7).

The LIP defines no member and no octet. A limit stands in a grant as
LIP-0020 W11.4 already states it, with `kind`, `resource` and `unit`,
each a text, `amount` in the string form, and `period` where the kind
has one. What this LIP assigns is texts: three values of `kind` under
`swarma/`, the values of `resource`, `unit` and `period` that each kind
recognises, and the arithmetic of their amounts. Where a profile needs
a member that `swarma-grant/4` does not have, the need stands as an
open question and no member is invented.

## What is decided and what is proposed

LIP-0008 section 2 holds the meanings that a profile of each kind must
bind, as initial semantic kinds. It also records that Ivan Oparin
decided on 2026-11-14 that further kinds join the list, with the
co-author's agreement pending; for coins that decision adds a maximum
for one spend, a maximum for a period, and an explicit identifier of
the asset and of the payment system, and it says for every kind that
an allowance of zero authorizes nothing. The list of what a proposal
for a kind states is LIP-0018 section 2, which records a decision of
the same day with the co-author's agreement pending. This LIP changes
none of those texts and restates none of them; it cites them.

| Decided, or text in force | Where | This profile |
| --- | --- | --- |
| The meaning that the profile of coins, of model tokens and of model cost must bind | LIP-0008 section 2, first table | Adopts each meaning and binds it to texts and arithmetic (sections 2 to 4) |
| For coins: a maximum for one spend, a maximum for a period, and an explicit identifier of the asset and of the payment system, a chain with its asset or a rail outside a chain | LIP-0008 section 2, decision of 2026-11-14, agreement pending | Three ceilings of one kind, told apart by `period` (L3, L12) |
| What a proposal for a limit kind states | LIP-0018 section 2 | One table for each kind (sections 2 to 4) |
| A limit has `kind`, `resource`, `unit`, `amount` and, where its kind has one, `period`; the key of a limit is all of these but the amount | LIP-0020 W11.4; LIP-0026 R1.2 | The same members, with the texts of this LIP (L1) |
| The pool bounds, for each key, the sum over the groups of the number of rows of the group times the amount of its template | LIP-0026 section 8 (J12); LIP-0020 W11.10 rule 6 | The same sum for the three kinds, which are ceilings (L2, L6) |
| For one place of one parent the signing service MUST make one signature, ever | LIP-0014 J4.4 (a) | The PROPOSED reading relates continuation to it; section 5 states only the four decided rules |
| Every period and term of a limit is expressible in clock time and, for chain coins, in blocks of that chain ("at most N coins per M blocks") | Owner requirement of 2026-11-17, recorded here | Two period families, counted in blocks and in clock seconds, with their instance arithmetic (L3, L7); states the item for every kind (sections 2 to 4). The requirement is decided; the texts and arithmetic that carry it are this draft's proposal |
| Exhaustion and continuation | The decision record is the paragraph of section 5 that states the four rules | That paragraph contains nothing beyond them. The separate PROPOSED reading has no interim force |

Every rule of this LIP except the paragraph of section 5 that states
the four rules and the limited decision in point 5 below remains the
draft's proposal. Points 1 to 4 are choices of this draft where no text
gives an answer, and the owners should look at them first; point 5
records the subsequent settlement decision:

1. The reading of `period` in L3: an absent `period` is the total over
   the whole window, a present one is a ceiling per period instance,
   and one reserved text, `swarma/per-request`, is the ceiling of a
   single request. Present beside the reserved text are two families
   that this LIP assigns as the type profile, counted in blocks and in
   clock seconds, carrying the owner's requirement in the table
   above. W11.4 gives a limit with and without `period` different keys
   and gives neither a meaning; LIP-0018 section 2 asks a proposal to
   state whether a limit holds for one request, for a period or for
   the whole window, and whether a period is counted in blocks or in
   clock time. LIP-0008 section 2.1 gives that choice to the limit's
   type profile and to the contract; L3 takes the type profile's part
   and leaves the contract's mirror open (L10).
2. A request always consumes the key without `period` for its kind,
   resource and unit, so a grant that states only a ceiling per period
   authorizes nothing (L5). The alternative, a grant per period with
   no total, stands under Alternatives.
3. One account for each period instance (L7). LIP-0026 section 5 keys
   an account by grant or row and limit key and holds no vector with a
   period; which instance a debit belongs to has no answer there.
4. Three new codes, `LIMIT_UNSUPPORTED`, `SPEND_OVER` and
   `LIMIT_CLOCK_REGRESSION` (section 6).
   Every other refusal of this LIP takes a code that a landed text
   already names.
5. **DECIDED settlement choice only:** charge actual consumption and
   release the difference from the reservation for each of the three
   shared kinds, by L9. Ivan Oparin selected option A for LIP-0038 on
   2026-11-20, "charge actual, return the rest, as LIP-0031", event
   `$VY_Ow-Yi4YWA695VYxcLlg0EdizZ6p8UzPkpr37ZyGU`.
   The co-author's agreement is pending. LIP-0026 R5.8 leaves release
   to the type profile; the other mechanics and per-kind rules remain
   PROPOSED. [LIP-0038 P6.1](LIP-0038-action-profiles.md#6-the-three-shared-limit-kinds)
   states that settlement choice once for the consuming action leaves.

The paragraph of section 5 that states the four rules is no choice
of this draft: it is decided by the owner on 2026-11-17 and in force
in this version. The separate PROPOSED reading needs acceptance and
has no interim force.

Nothing of this profile is implemented. The owners accept or change
its proposed rules through this LIP, under LIP-0001.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The comparison of a child against its template and the pool for the three kinds, as a function of signed octets | Yes | The owners' acceptance |
| The accounts and the reservation of sections 1 to 4 as functions of stated facts | Yes | The owners' acceptance |
| A spend, a priced request or a token count at a real executor | No | An action profile that consumes the kind (LIP-0020 W11.14 rule 1); the members of the invocation and of the receipt (LIP-0020) |
| A period of the two families of L3, as a function of a stated tip height or clock reading | Yes | The owners' acceptance; at a real executor, a healthy observation and a clock under LIP-0022 sections 1 to 3 |
| The admission of a child that carries a limit, end to end | No | Even at a side that runs this LIP, parts (b) and (d) of row F6 of LIP-0014 section 8.4 end every child admission before F17 until a v4 contract profile exists (rule T1). No reader should expect children with limits to be admitted now |
| The vectors of section 7 | No | The owners' acceptance; no file exists |
| The report required by section 5 | No | Report recipients, carrier and form (open questions) |

## Motivation

Take a parent with a pool of 100 and two rows of 60 and 40, the
example of LIP-0026. The pool holds because a checker can add the
rows. It holds for no kind in particular: the texts compare amounts
under a key, and until a profile says what one unit of a key is, two
executors can both keep the sum and count different things. One counts
a spend without its fee, the other with it, and both journals agree
with their own reading while the principal's 100 is either kept or
passed. LIP-0018 section 2 opens with the same gap from the other
side: a proposal that leaves out what happens to a reservation after
an uncertain outcome cannot be implemented the same way by two
parties, and nobody notices until their journals disagree.

The three kinds of this LIP are the ones that bound money and model
use, which is where a disagreement costs something outside the
protocol. Coins need the fee inside the total, or the signed total is
not the most that leaves the payer. Model cost needs the reservation
before the request, because the price of an answer is known only
after it, and an executor that reserved nothing has already spent
against a ceiling it never checked. Model tokens need the accounting
named, because two tokenizers count one text differently and a
ceiling without its counting is two ceilings.

## Current state

- LIP-0008 section 2 lists six semantic kinds — coins, model
  requests, model tokens, model cost, maximum answer length and
  required confirmation depth — and, under the decision of
  2026-11-14, nine further kinds by name. Each needs a type profile.
  This LIP profiles three of the six; the rest stay as that section
  leaves them, and the open questions name them.
- LIP-0020 W11.4 states the members of a limit and says of their
  texts that the registry, the meaning of each kind, its unit, its
  period and its arithmetic come with the type profile of the kind,
  and that none exists yet. W11.14 states the registry of limit kinds
  as it stands: none is defined, and the one text `policy` is
  reserved and undefined (LIP-0008 section 12.4). Version 0.1.58
  enters the three kinds of this LIP in that registry, each proposed
  by version 0.1.58, LIP-0031; the registry of action identifiers is
  not touched.
- LIP-0026 gives a limit its key (R1.2), the pool over the rows
  (R1.3), for groups the sum of the count times the amount of the
  template (R8.5), the check of a child against its row (R2.4), and
  the accounts that a request debits (section 5). R2.4 compares
  ceilings and leaves a kind whose amount is a floor to its type
  profile; R5.8 leaves the release of a reservation after a
  reconciled outcome to the type profile. No vector of that LIP holds
  a limit with a period.
- LIP-0014 section 8.4 puts the kind of a limit in row F17 between
  the keys and the amounts, with the code `LIMIT_KIND_UNDEFINED`, and
  repeats the check for a request in row E2. Both stand as proposals
  of version 0.1.55 with the state of that section.
- No executor reserves against a v4 limit today. The model proxy of
  the rental profile enforces caps of a binding that a gateway
  prepared and does not observe the chain (LIP-0008, "Current
  state"); no v4 implementation or conformance result is claimed
  there or here.

## Proposal

A root grant is called `G`, a parent `P` and a child `C`, as in
LIP-0026 and LIP-0014 section 8.4. The executor that a grant names is
the side that meters under it (LIP-0020 W11.4).

### 1. What the three kinds share

The three kinds stand in a grant in the same members, are compared at
the admission of a child in the same step, draw on a pool by the same
sum, and are reserved in the same accounts. Sections 2 to 4 state
only what differs: the resource, the unit, the debit of one request,
and the settlement.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| L1 | A limit of one of the three kinds is a limit of LIP-0020 W11.4: exactly `kind`, `resource` and `unit`, each a text, and `amount`, an integer in the string form from 0 to 18446744073709551615 (W11.1), with `period`, a text, where the kind has one. `kind` is `swarma/coins`, `swarma/model-cost` or `swarma/model-tokens`. This LIP assigns no other member, and a side reads no member beside these for a limit of the three kinds. The key of a limit is all of its members but the amount (LIP-0026 R1.2). | The codes of the member step (LIP-0020 W11.8) |
| L2 | The amount of each of the three kinds is a ceiling. R2.4 of LIP-0026 therefore applies to them as it stands: the amount of a child under a key is at most the amount of its row under the same key. No kind of this LIP is a floor, and the sentence of R2.4 that leaves a floor to its type profile has no case here. | `CHILD_BUDGET_OVER` |
| L3 | `period` has three readings, and no other. Absent: the amount bounds the sum of all debits of the key over the whole window of the grant. Present with the text `swarma/per-request`: the amount bounds the debit of one request. Present with a text of one of the two families below: the amount bounds the sum of the debits of the key inside one instance of the period that the text names. A period divides the one window for accounting (LIP-0008 section 2.1). Whether a period is counted in blocks or in clock time belongs to the limit's type profile and to the contract, as that section has it; this LIP, as the type profile, assigns the counting, the length and the boundaries of each family, and the contract's mirror of them stays open (L10). The block-counted family is `swarma/blocks-<N>` and the clock-counted family is `swarma/seconds-<S>`, where `<N>` and `<S>` are decimal integers with no sign and no leading zero, from 1 to 9007199254740991 (the bound of a height and of the number form, LIP-0020 W11.1 and section 2). `<N>` is a count of blocks and `<S>` a count of seconds. A text of neither form, and a count of 0, has no definition under this profile. Which family each kind accepts is stated in sections 2 to 4: every kind accepts the clock-counted family, and chain coins accept the block-counted family as well, under the owner's requirement of 2026-11-17 recorded above. No side converts a period text or its accounts between blocks and seconds to make two keys match; conversion of calendar time to window heights at issuance remains LIP-0008 section 7.1. A seconds period has fixed length and epoch alignment, not calendar months, calendar years or local-time days; those periods remain open. The instance arithmetic of the two families stands in the paragraphs after this table and in L7. | L4 for a text with no definition at the side, or of a family that the kind does not accept |
| L4 | A side that has the profile of a kind and meets a limit of that kind whose `resource`, `unit` or `period` it does not recognise under sections 2 to 4 — an asset system it does not serve, a currency and scale it has no price in, an accounting it does not count by, a period text that L3 does not define, a block-counted text for a kind or a resource that accepts no block counting there, or a block count on a chain that the side does not read — refuses as `LIMIT_UNSUPPORTED`. The refusal stands where the kind is judged: at the admission of a child inside row F17 with its part (b), after the kind and before the amounts, and at a request inside row E2. A kind with no profile at the side is not this refusal; it stays `LIMIT_KIND_UNDEFINED` (LIP-0020 W11.14 rule 2). No unrecognised text is read as no limit, and none is read in the other counting. No refusal code beside `LIMIT_UNSUPPORTED` is needed for a period family: a counting that the child and the template do not share is two keys and refuses in part (a) under L6. | `LIMIT_UNSUPPORTED` |
| L5 | A request consumes keys as follows. For the kind, resource and unit that the request draws on it always consumes the key without `period`. It also consumes every key with a `period` other than the reserved text that the grant — for a request under a child, the child and the template of its row together — states for the same kind, resource and unit, each in the instance that holds the request. The key with the reserved text, where stated, is checked per kind in sections 2 to 4 and is no cumulative account. A key that a request consumes and that the grant does not state has the ceiling 0 (LIP-0020 W11.4; LIP-0026 R5.2), so the first debit against it refuses. Which resource and unit a request draws on is fixed by the action that it asks for and by the executor that serves it, under the profile of that action; this LIP defines no action. | At the reservation, L8 |
| L6 | At the admission of a child the three kinds are compared in row F17 of LIP-0014 section 8.4, in its three parts: every limit of the child has the key of a limit of the template of its row (part (a)); the kind of every limit of the child and of the template has a profile at the side, and its texts are recognised there (part (b) with L4); each amount of the child is at most the amount of the template under the same key (part (c), by L2). The key of part (a) holds `period` among its members (LIP-0020 W11.4; LIP-0026 R1.2), so a child's period counting matches its template's exactly where part (a) passes at all: a child that states a block-counted text where the template states a clock-counted one, a clock-counted text where the template states a block-counted one, the reserved text where the template states an instance text, or any other count of blocks or seconds than the template's, states a key that the template lacks and refuses in part (a) as `CHILD_BUDGET_OVER`, however near the two lengths stand in time; no side converts one counting into the other to make them match (L3). A child need not restate a key of its template to pass this step; a key that it omits then has the ceiling 0 in its own account under R5.2 and authorizes no consumption under the child, whatever the row states. The child is compared against no pool at an admission: the pool is judged on the signed octets of the parent — in step 9 on the parent's octets, as LIP-0020 W11.10 has it — one pool for every key that a template limits, by the sum over the groups of the number of rows of the group times the amount of its template for that key, an exact integer sum that never wraps (LIP-0026 R8.5; LIP-0020 W11.10 rule 6). That rule takes the keys that a template limits exactly, the key with `swarma/per-request` included: a template that states the reserved text therefore has a pool of count times amount for that key as well, or the parent refuses as `GRANT_DELEGATE`, although no account sums that key (L5). The chosen reading of L3 has the pool consequence that the fourth kind of the Alternatives would have had, and this profile states it instead of leaving it to be found. The pool is no account, and what one row leaves unused is available to no other row (LIP-0026 R5.5). | `CHILD_BUDGET_OVER`; `LIMIT_KIND_UNDEFINED`; `LIMIT_UNSUPPORTED`; for the pool, `GRANT_DELEGATE` |
| L7 | A request under a grant that is no child debits the own accounts of that grant, and a request under a child the own account of the child and the row account of its parent and its ordinal, and no own account of the parent (LIP-0026 R5.3, R5.4). For a key without `period` the account is the account of R5.2. For a key with a `period` other than the reserved text the executor keeps one such account for each instance of the period, keyed beside R5.2 by the instance that holds the debit. The instance is the one that holds the reading taken immediately before the reservation (LIP-0022 B1.6): for a block-counted text, the instance that holds the tip height `H` of that reading on the chain of L12, read from the executor's node in the one observation of the admission (LIP-0022 B1.1, B1.5); for a clock-counted text, the instance that holds `now`, the executor's clock in whole seconds of UTC read in the same recheck (LIP-0022 B3.1). Which heights and which seconds an instance holds is stated after this table. An account of an instance begins at 0. A debit belongs to the instance of its reservation and is never moved to another instance afterwards: not by a later block, not by a later second, and not by a reorganisation, which lowers no account (L9; LIP-0026 R5.8). A request whose reading falls in a later instance debits that instance and never back into an ended one, except where a reorganisation has lowered `H` into an earlier block instance that the chain as then validated holds open; a new reservation then debits that earlier instance's account as it stands, reservations already charged to a later instance included where they stand. A session debits its own account beside these, as LIP-0028 T4.6 proposes, and that account takes the instance of its key in the same way. | L8 |
| L8 | Before the effect of a request the executor reserves the debits of every key that the request consumes, durably and in one atomic write of its journal, or none of them, taking the keys in the order in which the request consumes them and for each key the own account before the row account, and it reports the first account whose ceiling the reservation would exceed (LIP-0026 R5.6). What is made durable is the reservation entry of the journal; its octets and the key that identifies a request come with the members of the invocation (LIP-0026 section 5) and are open here as there. A request that is refused reserves nothing (LIP-0026 R6.2). Parallel requests and the replicas of one executor share one allowance through that one journal, in the form that LIP-0025 proposes; no replica keeps a remainder of its own (LIP-0008 section 4; LIP-0026 R5.5). | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| L9 | One request identity holds at most one reservation, and a repeated request is charged once (LIP-0026 R5.7). A reservation whose effect has an outcome that is not known is retained until it is reconciled, and no account is lowered by a revocation, a restart or an unknown outcome (LIP-0026 R5.8; LIP-0008 section 2). Where sections 2 to 4 settle a reservation at an actual consumption below the reserved amount, the difference is released in the same accounts that the reservation debited, in one write with the entry that records the outcome, and only where that outcome is known: the effect happened at the settled consumption, or it did not happen. A settlement never raises an account above the reserved amount of its request, and a consumption above the reservation is not charged to the grant after the effect; each kind states what its reservation must cover so that this case cannot arise inside the profile. After a recovery by starting anew, what an account counts as is the rule of LIP-0025 section 7 for row accounts; what it charges for an instance account of L7 is an open question. | None of its own |
| L10 | The contract mirrors the limits of the grant as LIP-0008 section 2 states it, and a mismatch refuses admission there; the code of that refusal comes with the v4 contract profile and is open (LIP-0014 section 8.4, row F6 part (d)). A default selects an allowance only within the signed limit and never supplies a limit that the grant lacks (LIP-0008 section 2; LIP-0018 section 2). Operator ceilings of the executor may be lower and never higher, as that section has it. The two rules that LIP-0018 section 2 holds for every kind without restating them hold here in the same way and are cited here, not repeated; the tables below cite this rule. Whether the contract also mirrors `period` — its text, its counting and its count — besides the executor, kind, resource, unit and amount of that section is open with the code, as the open questions state; until a v4 contract profile mirrors it, two contracts that differ only in a period cannot be told apart by that mirror, while the signed keys of L6 tell them apart at every side. | None of its own |

**Exact arithmetic (L8, L9, L13 to L21).** Every debit, sum of
debits, product in the declared integer unit, account value and
released difference is an exact integer, computed before any
comparison. No side wraps, saturates, truncates or rounds that
arithmetic. L17 and L18 first convert the exact rational cost of a
whole request upward once to integer subunits; those integers are
the reservation and settlement debits, with no further rounding of
either debit or any account. No binary64 calculation takes part in
either the rational cost or the integer arithmetic. A result above
18446744073709551615 is above
every ceiling and refuses at the applicable check: `SPEND_OVER` at
a stated ceiling for one request, otherwise `OWN_LIMIT_OVER` or
`ROW_CAP_OVER` at the first account that the reservation would
exceed, in L8's order. A refusal performs no effect and writes no
reservation or changed account. The pool's existing exact, no-wrap
sum and its refusal remain L6 and LIP-0020 W11.10 rule 6 (W2.4);
this paragraph does not replace them with fixed-width arithmetic.

**The instances of a block-counted period (L3, L7).** Let `A` be
`not_before_height` and `E` be `not_after_height` of the grant that
owns the account: for an own account that grant itself, for a row
account the parent. The window is half-open, `[A, E)`, and admission
requires `A <= H < E` for the tip height `H` of the validated active
chain, with no clock and no grace (LIP-0008 section 7.1 rules 1
and 2). For the text `swarma/blocks-<N>` the instances are numbered
`n = 0, 1, 2, ...` and instance `n` holds the heights
`[A + n·N, A + (n+1)·N)`, cut at the window: its last instance ends
at `E` where the count would pass it. The height that opens an
instance, `A + n·N`, belongs to it; the height that opens the next
one belongs to the next one and to no other. A reservation at tip
height `H` belongs to instance `(H - A)` divided by `N`, the whole
quotient, computed exactly; heights on different chains are not
compared, added or converted, in the manner of LIP-0022 B5.3 for
depths, which is why L12
bounds the chain of a block count. Take `A = 200000` and
`swarma/blocks-144`: instance 0 holds heights 200000 to 200143,
instance 1 opens at 200144, and a spend reserved while the tip
stands at 200144 debits instance 1, never instance 0. A grant of
`swarma/coins` that states at most so many atomic units under
`swarma/blocks-144` states the owner's "at most N coins per M
blocks" with `M = 144`, in the members that exist.

**The instances of a clock-counted period (L3, L7).** A v4 grant has
no clock member, and an interval that the parties state in calendar
time is converted to heights at issuance for the window (LIP-0008
section 7.1, decision of 2026-11-16 recorded there); a clock-counted
period therefore takes no anchor from the grant. For the text
`swarma/seconds-<S>` the instances are numbered by whole seconds of
UTC from the Unix epoch, the seconds that `now` counts (LIP-0022
B3.1; Unix seconds as in LIP-0013 section 2.1): instance `m` holds
the seconds `[m·S, (m+1)·S)`, the first second included and the
first second of the next instance excluded, and a reservation at
`now` belongs to instance `now` divided by `S`, the whole quotient.
So `swarma/seconds-3600` holds the clock hours and
`swarma/seconds-86400` the UTC days; `swarma/seconds-604800` starts
its weeks on Thursday 00:00 UTC, not on a contract's chosen weekday.
Calendar months, years and local-time days have no assigned text.
An instance may begin before
the window opens in heights or end after it closes; a debit still
needs the window open at `H`, and the instance gives the account,
never the admission. The guards on that clock — a reading below the
kept mark, a header too far ahead, the age of the tip — are those
of LIP-0022 section 3 where that profile runs, with its codes and
its order. The separate per-key ledger check of section 6 applies
even at a side that does not run that profile; it can refuse
`LIMIT_CLOCK_REGRESSION`, with no reservation or changed account,
rather than debiting an ended instance (L7). A reading in the same
or a later instance passes this instance check. The epoch alignment, the
two text forms and their common bound are choices of this draft,
marked in point 1 above; that a period is expressible in both
countings is the owner's requirement, and no rate between a block
and a second is stated or used anywhere in this profile.

**A reorganisation and a block instance (L7).** Every fact of one
admission comes from one observation between two reads of the same
tip, and immediately before a reservation the tip is read again;
where it is not the tip of the observation the admission is void
and nothing is recorded as closed (LIP-0022 B1.1, B1.5, B1.6). The
verdicts are relative to the active chain: after a reorganisation
the side decides again on the chain that it then validates
(LIP-0022 B4.4), and a reorganisation can lower `H`, on which the
window comparison is repeated at the effect boundary while an
effect already performed is not undone (LIP-0008 section 7.1). For
an instance account that gives three cases. A reorganisation that
leaves `H` inside the instance of a standing reservation changes
nothing for that account. One that lowers `H` into an earlier
instance reopens that instance for new reservations, which debit
its account as it stands; debits already charged to a later
instance stay there, because no account is lowered by a restart, a
revocation or an unknown outcome (L9; LIP-0026 R5.8), so a side
never gains room in an earlier instance by moving a debit out of a
later one, and never loses the later debit either. One that lowers
`H` below `A` admits nothing until the window opens again on the
chain as validated. Two tips at one height with different hashes
conflict and no healthy observation admits on either (LIP-0022
B2.4, B2.5), so no reservation takes an instance from a contested
tip. What a displaced spend itself charges is L15; the instance of
its reservation does not follow the block that confirms it.

Thus this draft's reading of "at most N coins per M blocks" is per
instance at the reservation's validated tip, not per M blocks of a
chain that is finally validated. This is proposed, not a further
owner decision.

Own and row instances can have different anchors. Where the child
and parent starts differ modulo `N`, a fresh own instance can meet
a row instance that already holds debits and refuse `ROW_CAP_OVER`.
Both ceilings still hold; the effective allowance may be below a
full template amount in each own instance.

Two consequences of L5 are stated in place. A parent whose template
states only a ceiling per period gives its children nothing to spend:
the key without `period` has the ceiling 0, and the first request
refuses at its reservation, against the own account first, however
much room the period has. And a template that states two periods
for one resource, an hour
and a day, bounds a request by both, each in its own instance; neither
period needs the other, and the pool holds a key and a sum for each.

The order inside F17 in L6 keeps the order of that row: the keys,
which octets decide, stand before the recognition of the texts, which
needs the profiles of the side, and both stand before the amounts. A
child that states a limit under a key that its template lacks, of a
kind without a profile, therefore refuses as `CHILD_BUDGET_OVER`, and
a child that states an amount above its row under a text that the
side does not recognise refuses as `LIMIT_UNSUPPORTED`. That is the
reading of parts (a) to (c) that pair Q23 of that section states for
the kind, extended to the texts by L4; the extension is this draft's.

### 2. `swarma/coins`

Coins is the kind of LIP-0008 section 2 whose meaning a profile must
bind to an asset and network, an atomic unit, permitted targets and a
total spending including the applicable fees; the decision of
2026-11-14 in that section adds a maximum for one spend, a maximum
for a period, and an explicit identifier of the asset and of the
payment system. This profile adopts that meaning. Permitted targets
are no part of it: a grant carries no list of targets or payees
(LIP-0020 W11.2), no profile defines one, and this LIP invents no
member for them; the need stands in the open questions. Rental price
and authority to spend funds stay separate terms, as that meaning has
it: a limit of this kind bounds spending and prices nothing.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| L11 | `resource` is the identifier of the asset and of the payment system, in the form `<system>:<asset>`. The system is a chain with its asset, or a rail outside a chain, in the words of the decision. This LIP assigns one value, `namecoin:NMC`, for Namecoin and its coin. Every further value is assigned as L4 and the open questions have it, by a text that names the system, the asset and its atomic unit; a value that no such text assigns is unrecognised at every side. `unit` names the atomic unit of the asset, the smallest unit that the payment system itself counts, and `amount` counts atomic units. For `namecoin:NMC` this LIP assigns the unit text `atomic` and states the scale that the tree already carries: one whole NMC holds 100000000 atomic units, as the bound of `amount_sat`, at most `21000000 * 100000000` atomic NMC units (LIP-0006), and the spend budget in atoms, 0 to 2100000000000000 (LIP-0013 section 2.1), each give it. No side converts an amount through a number of whole coins. The text `namecoin:NMC` does not by itself tell the main chain from a regtest chain: the grant names its chain by the hash of its genesis block alone (LIP-0020 W11.2; LIP-0020, open questions, "The chain"), and that genesis governs. A side serves `namecoin:NMC` under a grant only on the chain of that grant's `genesis`; on a grant of another chain the resource is unrecognised there. | L4 |
| L12 | The three maxima of the decision are three limits of one kind with one `resource` and one `unit`, told apart by `period` under L3: without `period`, the total over the term of the grant; with a period text of L3, the maximum inside one instance of that period; with `swarma/per-request`, the maximum for one spend. A grant states any of them, and each stated one bounds every spend under L5; the total is the key that every spend consumes, stated or not. The maximum for a period of this kind is expressible in both countings: in clock time, by `swarma/seconds-<S>` for every resource of the kind; and in blocks, by `swarma/blocks-<N>` where the system of the resource is a chain. A block count holds heights of that chain, and of no other: it is defined in this profile only where that chain is the chain of the grant's `genesis` under L11, so that the heights of the count and the heights of the window are heights of one chain and section 1's instance anchor applies. A block-counted text for a rail outside a chain, which has no blocks, and for a chain other than the grant's, whose heights no signed member anchors, is unrecognised (L4); the second case is open with the further payment systems. A template that states the key with `swarma/per-request` has a pool for that key under L6, as for every key it limits. | L5, L8; L4 |
| L13 | The debit of one spend is the value that the spend pays away from the payer together with the applicable fees of that spend in the same asset, in atomic units. Change that the spend pays back to the payer is no part of the debit, at whichever address of the payer it lands; a payment to the payer itself with no value leaving it debits its fee alone. A fee in another asset than the spent one has no debit under this profile and is an open question. The executor computes the debit from the spend that it is asked to make, before it makes it, and reserves it in full under L8; a spend whose fee the executor cannot bound before the effect is not made under this kind. Where the confirmed spend shows a smaller fee than the reserved one, the difference is settled under L9; a larger one cannot arise, because the reservation covered the fee that the executor itself set. | L8 |
| L14 | The maximum for one spend is checked before any reservation. All spends that one request asks for are one spend for this check: their debits under L13 are summed, and a sum above the amount of the key with `swarma/per-request` refuses as `SPEND_OVER` and reserves nothing. Splitting one payment into several outputs, transactions or requests of one identity does not pass the check; two requests with two identities are two spends, and what identifies a request is open with the invocation (L8). Where neither a grant nor, for a child, the child and its row state the key, no check is made. Where it is stated, the check at a request under a child follows the accounts: the sum is held first against the child's amount for the key, which is 0 where the child omits it (L6), and then against the row's amount, under which the child's already lies by L2. | `SPEND_OVER` |
| L15 | The executor that a grant of this kind names is the service that makes the spend, and it alone meters: it debits its ledger under L7 and L8 and no other side keeps the counter. The evidence of a debit is the spend on the named payment system together with the reservation entry that precedes it; what a receipt states about the spend comes with the members of the receipt, which no reader accepts yet (LIP-0020), and is open. A verifier at the admission of a child compares signed limits under L6 and reads no balance: that the payer holds enough of the asset is no part of this profile, and a spend that the payer cannot fund refuses at the executor without a code of this LIP and reserves nothing. An outcome that is not known — a spend broadcast and neither confirmed nor seen spent otherwise — retains its reservation under L9; when the spend is confirmed the debit stands, and when the same coins are seen spent by a different transaction the reservation is settled at a consumption of 0 for the value and at the fee that was actually paid to make the attempt, if any. What a displaced or replaced spend charges beyond this is an open question. | L8 |

A spend of 60 with a fee of 1 under a total of 100, an hour of 70 and
a maximum for one spend of 50 refuses as `SPEND_OVER` and moves no
account, although both cumulative ceilings have room. The same spend
without the third limit debits 61 against the total and against the
hour that holds it. A second spend of 40 with a fee of 1 in the same
hour then refuses at the reservation: the total would reach 102, and
the hour would reach it as well, and the own account of the total is
reported first under L8 where the request consumes that key first.

| Item of LIP-0018 section 2 | `swarma/coins` states |
| --- | --- |
| Identifier and resource | Kind `swarma/coins`; the resource is one asset on one payment system (L11). |
| Unit and integer scale | Atomic units of the asset; for `namecoin:NMC`, 100000000 to one whole coin, as the tree carries it; `amount` in the string form (L1, L11). No amount is a floating-point number, as the item requires and LIP-0020 section 2 has it. |
| Bounds and rounding | 0 to 18446744073709551615 (L1). No rounding: a debit is a whole number of atomic units or it is not made (L13). Sums and accounts are exact, never wrap, and overflow refuses (section 1, Exact arithmetic). |
| Period and aggregation | Whole window, per period instance, and one spend, by `period` (L3, L12). An instance is counted in clock time (`swarma/seconds-<S>`, for every resource) or, for a chain resource on the grant's chain, in blocks of that chain (`swarma/blocks-<N>`); the heights and seconds of each instance, half-open, and the reorganisation cases stand in section 1. Debits add inside an instance (L7). |
| Reservation | The full debit, fee included, durably before the spend (L8, L13). |
| Concurrency | One journal for parallel requests and replicas (L8). |
| Uncertain outcomes | Retained until reconciled; confirmed stands, displaced settles as L15 states (L9, L15). |
| Replay | One identity, one reservation (L9, L14). |
| Denials | A refused request reserves nothing and consumes nothing (L8); a spend the payer cannot fund likewise (L15). |
| Contract mirror | As L10 states it. |
| Defaults | None supply authority; an unstated total is a ceiling of 0 (L5, L10). |
| Refusal codes | Section 6. |
| Vectors and checker | Section 7, described and not built. |
| Path | This LIP, adopted under LIP-0001. |
| Who meters, and the evidence | The executor that makes the spend; the spend on its payment system and the reservation entry (L15). |
| At the admission of a child | Keys — the `period` text among them, so the counting in blocks or in seconds and its count must be the template's — then kind and texts, then amounts against the template; the pool by count times amount on the parent (L6). |

### 3. `swarma/model-cost`

Model cost is the kind of LIP-0008 section 2 whose meaning a profile
must bind to a cumulative cost ceiling, an exact currency and scale
and the price or conservative reservation policy used to account for
it. This profile adopts that meaning and takes the conservative
reservation: the maximum is reserved before a request and the actual
cost is settled after it. In the second table of that section the
kind is the first case of external service cost; this LIP profiles
the model case alone and assigns no identifier for the wider kind.
Its periods are counted in clock time alone, by
`swarma/seconds-<S>` (L3). Clock-only periods are this draft's choice,
not a claim that a block-counted model limit is impossible. The
owner's requirement asks for blocks for chain coins; this draft
assigns no block-counted period to model cost. A
`swarma/blocks-<N>` text under this kind is unrecognised (L4).

| Rule | Requirement | Refusal |
| --- | --- | --- |
| L16 | `resource` names the priced model at the executor that serves it, in the form that the executor's own profile states for its models; this LIP assigns no model name, and a resource that names no model of the executor is unrecognised there. `unit` states the currency and its scale in one text of the form `<currency>/<scale>`, where `<currency>` is the code of the currency as the executor's price table states it and `<scale>` is the name of the smallest subdivision that the table accounts in. `amount` counts that subdivision. Two limits that differ in currency or in scale are two keys and are never added together, and no side converts between currencies or scales inside this profile. Which codes and subdivisions a deployment uses is stated by its price table under L17; a unit that the table does not state is unrecognised. | L4 |
| L17 | Before a request the executor reserves the maximum cost of that request under its price table: the highest cost that the table gives the request as asked, over every part that the table prices, the input that it carries and the longest output that it permits included. The cost is computed exactly as a rational number from the values the table states, with no binary64 calculation; every product and the sum over all parts are exact, and no unit price or part is rounded. The reservation under L8 is the least integer in the limit's subdivision not below that exact maximum: round upward once, after summing the whole request, so that the reservation never falls short of the table. A request whose maximum the table cannot give — an output without a permitted length, a part with no price — is not served under this kind. The price table is the executor's: who sets it, how it is signed or pinned, and how a change of it meets a live grant have no member and no text, and stand in the open questions. A change of the table changes no signed ceiling; it changes what one request reserves against it. | L8; for no finite maximum, L18 |
| L18 | When the outcome of a request is known, the executor computes the actual cost under the same table by L17's exact rational products and sum over all parts, and settles at the least integer subdivision not below that sum, with the same single upward conversion and no binary64 calculation. That integer is the settlement debit; the integer difference from the reservation is released under L9. Upward conversion is monotone, so an actual cost no greater than the table's exact maximum never settles above the reserved integer. A request that the upstream refused before any priced work settles at 0; priced work that was done settles at its table cost converted in this way whether or not the answer was used. An outcome that is not known retains the full reserved maximum until it is reconciled (L9). A charge above the reserved maximum is outside this profile: the reservation was the highest cost of the table, so a higher charge means the table did not govern the request, and the executor charges nothing above the reservation to the accounts of the grant. What it does with such a charge is an open question. A request with no finite maximum under L17 reserves nothing and refuses as `SPEND_OVER` at the per-request check if that key is stated; otherwise it refuses at the reservation step against the first account that it consumes, as a reservation above every ceiling does. | `SPEND_OVER`; otherwise `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| L18A | The reserved text of L3 gives a maximum cost for one request. It is checked against the reserved maximum of L17 before any reservation, as L14 checks one spend: a reserved maximum above the amount of the key with `swarma/per-request` refuses and reserves nothing. Where neither a grant nor, for a child, the child and its row state the key, no check is made; where it is stated, the check at a request under a child holds the maximum first against the child's amount for the key, which is 0 where the child omits it (L6), and then against the row's amount, as L14 has it. | `SPEND_OVER` |

The ceilings of this kind are the whole-window total and, for each
stated clock-counted period, the ceiling of its instance (L3, L5),
with the maximum for one request of L18A beside them. A grant that
wants only a ceiling per period states the total as well or
authorizes nothing (L5).

| Item of LIP-0018 section 2 | `swarma/model-cost` states |
| --- | --- |
| Identifier and resource | Kind `swarma/model-cost`; the resource is one priced model at its executor (L16). |
| Unit and integer scale | One currency in its smallest accounted subdivision; `amount` in the string form (L1, L16). |
| Bounds and rounding | 0 to 18446744073709551615 (L1). Maximum and actual costs use exact rational products and sums over the whole request, then one upward conversion each to integer subunits (L17, L18). No unit price or part is rounded and no binary64 calculation takes part; subsequent integer arithmetic is exact, with no rounding or wrap, and overflow refuses (section 1, Exact arithmetic). |
| Period and aggregation | Whole window and per period instance (L3, L5), and one request (L18A). An instance is counted in clock time alone, by `swarma/seconds-<S>`, as this draft's choice; a block-counted text is unrecognised (L4). Settled costs add inside an instance (L7, L18). |
| Reservation | The maximum under the price table, durably before the request; the reservation entry is what is made durable (L8, L17). |
| Concurrency | One journal for parallel requests and replicas (L8). |
| Uncertain outcomes | The reserved maximum is retained until reconciled (L9, L18). |
| Replay | One identity, one reservation, settled once (L9). |
| Denials | A refused request reserves nothing (L8); a request refused upstream before priced work settles at 0 (L18). |
| Contract mirror | As L10 states it. |
| Defaults | None supply authority, and no default price exists: a part with no price is not served (L10, L17). |
| Refusal codes | Section 6. |
| Vectors and checker | Section 7, described and not built. |
| Path | This LIP, adopted under LIP-0001. |
| Who meters, and the evidence | The executor that serves the model, by its price table; the reservation and settlement entries of its journal, with the upstream charge where it has one (L17, L18). |
| At the admission of a child | Keys — the `period` text among them, so a child's clock count must be the template's and no block count passes for it — then kind and texts, then amounts against the template; the pool by count times amount on the parent (L6). |

### 4. `swarma/model-tokens`

Model tokens is the kind of LIP-0008 section 2 whose meaning a
profile must bind to separate cumulative input and output token
ceilings, with the model and token-accounting profile. This profile
adopts that meaning. It does not profile maximum answer length, which
that section lists as a kind of its own, and it gives the signed
default output allowance of that kind no member, because
`swarma-grant/4` has none; both stand in the open questions. Its
periods are counted in clock time alone, by `swarma/seconds-<S>`
(L3), as this draft's choice, like model cost in section 3. A
`swarma/blocks-<N>` text under this kind is unrecognised (L4).

| Rule | Requirement | Refusal |
| --- | --- | --- |
| L19 | `resource` names one model together with the token accounting that counts for it, in the form `<model>/<accounting>`, where `<model>` is the model as the executor's profile states it — the same text that L16 prices — and `<accounting>` is the identifier of the counting under which the executor reports input and output. This LIP assigns neither part; a pair that the executor does not serve is unrecognised there. `unit` is `input-token` for the ceiling of tokens sent to the model and `output-token` for the ceiling of tokens received from it, so the two ceilings of the meaning are two keys for one resource. `amount` counts tokens. Input and output are never added together, and a count under one accounting is never compared with a ceiling of another. | L4 |
| L20 | The executor counts. The input of a request is counted under the named accounting before the request is sent and is reserved at that count. The output is reserved before the request at the longest output that the request permits under the same accounting, and a request that permits no longest output reserves nothing and refuses as `SPEND_OVER` if a per-request output ceiling is stated, or at the reservation step otherwise, as L18 has it for cost. When the outcome is known the output reservation settles at the counted output under L9; the input, counted exactly, settles at its reservation where the request was sent and at 0 where it was not. A count that the upstream reports beside the executor's own does not govern: where the two differ the account keeps the executor's count under the named accounting, and the difference is evidence for the parties and no debit. An outcome that is not known retains both reservations until it is reconciled (L9); output received before the outcome became unknown is counted where the executor holds it, and the rest of the reserved output stays reserved. | L8; `SPEND_OVER`, `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| L21 | The reserved text of L3 gives a ceiling for one request for each unit. For input it is checked against the count of L20 before any reservation, and for output against the longest output that the request permits; either above its amount refuses as `SPEND_OVER` by the proposal of section 6 and reserves nothing. Such a ceiling is per request and no cumulative account, and it takes the place of no signed maximum answer length, which stays a kind of its own as the head of this section says. | `SPEND_OVER` |

The ceilings of this kind are, for each unit, the whole-window total
and the ceiling of each stated period instance (L3, L5, L7): four
accounts at least for one resource under one grant, of which a
request debits the two of its window and the two of its instance,
each once, in one write (L8). A request that fits the window and
fails the instance reserves nothing, as every refused request does.

| Item of LIP-0018 section 2 | `swarma/model-tokens` states |
| --- | --- |
| Identifier and resource | Kind `swarma/model-tokens`; the resource is one model under one named token accounting (L19). |
| Unit and integer scale | `input-token` and `output-token`, one token each; `amount` in the string form (L1, L19). |
| Bounds and rounding | 0 to 18446744073709551615 (L1). No rounding: a count is a whole number of tokens under its accounting (L20). Sums and accounts are exact, never wrap, and overflow refuses (section 1, Exact arithmetic). |
| Period and aggregation | Whole window and per period instance, separately for input and output (L3, L5, L7), and one request for each unit (L21). An instance is counted in clock time alone, by `swarma/seconds-<S>`, as this draft's choice; a block-counted text is unrecognised (L4). |
| Reservation | Input at its count, output at the longest permitted, durably before the request (L8, L20). |
| Concurrency | One journal for parallel requests and replicas (L8). |
| Uncertain outcomes | Both reservations retained until reconciled; output already held is counted (L9, L20). |
| Replay | One identity, one reservation, settled once (L9). |
| Denials | A refused request reserves nothing (L8); a request never sent settles its input at 0 (L20). |
| Contract mirror | As L10 states it. |
| Defaults | None supply authority; no default output allowance is stated, for want of a member (head of this section; L10). |
| Refusal codes | Section 6. |
| Vectors and checker | Section 7, described and not built. |
| Path | This LIP, adopted under LIP-0001. |
| Who meters, and the evidence | The executor, by the named accounting; its reservation and settlement entries, with the count that the upstream reports kept beside its own (L20). |
| At the admission of a child | Keys — the `period` text among them, so a child's clock count must be the template's and no block count passes for it — then kind and texts, then amounts against the template; the pool by count times amount on the parent (L6). |

### 5. Exhaustion and continuation

The owner, Ivan Oparin, decided the four rules below on 2026-11-17;
the co-author's answer is folded in by amendment. Only the quoted
paragraph is decided and in force in this version. It is the
decision record to which the README, changelog and unresolved
questions point, with the four rules' wording unchanged:

> stop and report, without revocation; no top-up of an existing grant;
> continuation by a new grant on a new place; long-lived agents get
> limits per period, with a new grant per period.

### PROPOSED reading of exhaustion and continuation

This separate subsection is entirely PROPOSED. It needs the owners'
acceptance, has no interim force and adds nothing to the decided
paragraph of section 5.

The draft reads an exhausted counter as an account at its ceiling:
the whole-window account of a key, or the account of the instance
that holds the request (L3, L5, L7). A refused reservation does not
exhaust an account that still has room. The extended trigger "a
reservation under it refuses because its debit would pass that
ceiling" is not adopted: at 10 of 100, refusing a debit of 95 would
otherwise strand 90 units and stop a later debit of 5 that L8
admits. Any proposed extension needs the owner's confirmation and
must not fire while a smaller request fits, or on the no-finite-
maximum refusals of L18 and L20. No such extension is in force.

The draft would stop requests consuming the exhausted key while
that ceiling stands, without a seal spend or a recorded closure.
It would report to the delegating side of the parent for a child,
and to the issuer for a root grant; these recipients, the carrier
and the form of the report are proposed, not part of the decision.
Whether a later instance can admit again under the same grant is
also a proposed reading, subject to the fourth rule and the open
relation to LIP-0008 section 2.1 below.

The draft relates a new place for a child to the ordinal of an
unused row, with its own seal and accounts, and not a second
signature or a larger amount for the old place: LIP-0014 J4.4 (a)
says the signing service MUST make one signature, ever, for one
place of one parent. Continuation of a root by a new grant from
its issuer is the draft's proposal, not a decided recipient or
issuance rule.

The relation of the fourth rule to both sentences of LIP-0008
section 2.1 remains open: "Each grant covers the whole agreed term"
and "A new period needs no new grant, no new seal and no new issuance
record". One possible reading distinguishes accounting periods
inside a grant from authority issued period by period to a
long-lived agent. That reading, including a whole-window total per
such grant, its window in heights under LIP-0008 section 7.1, and
a new parent place for each child so issued, is PROPOSED only.
This LIP neither resolves the relation nor amends LIP-0008; the
owners must decide whether and how to amend that section. No
reconciliation acquires force pending their answer.

### 6. Refusals and their order

| Code | What it reports | Rule | Name |
| --- | --- | --- | --- |
| `CHILD_BUDGET_OVER` | A limit of the child is above the limit of its row under the same key, or has a key that the row does not have | L2, L6 | LIP-0026 R2.4; LIP-0014 J1.2 |
| `LIMIT_KIND_UNDEFINED` | The kind of a limit has no type profile at the side | L4, L6 | LIP-0020 W11.14 rule 2 |
| `LIMIT_UNSUPPORTED` | The kind has a profile at the side and the `resource`, `unit` or `period` of the limit is not recognised there | L4 | New |
| `SPEND_OVER` | One request is above the ceiling for one request of its kind: one spend, one reserved maximum, one input count or one longest output | L14; L18A; L21 | New |
| `OWN_LIMIT_OVER` | A reservation would exceed an own account, of the window or of an instance | L7, L8 | LIP-0026 R5.6 |
| `ROW_CAP_OVER` | A reservation would exceed a row account, of the window or of an instance | L7, L8 | LIP-0026 R5.6; LIP-0014 J1.3 |
| `GRANT_DELEGATE` | The pools of a parent do not bound the sums of its templates for a key of the three kinds | L6 | LIP-0020 W11.10 rule 6 |
| `LIMIT_CLOCK_REGRESSION` | A clock reading falls in an instance earlier than the latest one already debited for the key | L7; section 1, clock instances | New |

The form of a limit refuses in the member step with the codes of that
step, and no code of this LIP changes their meaning (L1). The refusal
of a contract that does not mirror a limit has no code yet (L10).

At the admission of a child the order is that of row F17: the keys
(`CHILD_BUDGET_OVER` — a `period` text of another counting or count
than the template's is another key and refuses here, under L6),
then the kind (`LIMIT_KIND_UNDEFINED`) and the texts
(`LIMIT_UNSUPPORTED` — a period text that L3 does not define, or of
a family that the kind does not accept, refuses here), then the
amounts (`CHILD_BUDGET_OVER`). At a request the order is: the action and the
kinds it consumes, with their texts (rows E1 and E2;
`LIMIT_KIND_UNDEFINED`, then `LIMIT_UNSUPPORTED`); then the ceiling
for one request (`SPEND_OVER`); then the reservation, taking keys in
L8's order. For each key, check its clock instance first
(`LIMIT_CLOCK_REGRESSION`, for clock-counted keys only), then its
own account (`OWN_LIMIT_OVER`), then its row account (`ROW_CAP_OVER`),
before moving to the next key. No account or reservation is written
unless all these checks pass. Where LIP-0022 runs, its observation
guards and B6.1 withholding still precede these request checks;
the new ledger refusal is not an observation refusal and does not
invoke B6.1 withholding on its own.
The place of `LIMIT_UNSUPPORTED` beside the kind and of `SPEND_OVER`
before the reservation are proposals of this LIP, marked NEW against
the table of LIP-0014 section 8.4, which has neither code. The place
of `LIMIT_CLOCK_REGRESSION` at the reservation is also NEW against
that table; it changes no definition or order of LIP-0022. The checks
of the invocation itself (row E0) have no codes and no order against
E1 and E2 in that table, and this LIP orders nothing against them.

None of these refusals records a closure. Exhaustion is no refusal
of this table and has no code. The four decided rules stand only
in the paragraph of section 5; the separate PROPOSED reading and
the open questions hold the draft's details. This section restates
none of them.

### 7. Vectors

No vector file of this LIP exists, and no checker for it is in this
repository. The set that the profiles need, paired valid and refused
cases with a checker that recomputes them as LIP-0018 section 2
asks, is described here so that its absence is stated and not
discovered: for each kind, admissions of a child against a template
and a pool on stated octets (a key the row lacks, a `period` text of
the other counting or of another count than the row's, a
block-counted text under a model kind, an unrecognised text, an
amount one above the row, a pool one short of the sum and a pool
missing for the key with `swarma/per-request`); the instance
arithmetic on stated heights and seconds (the last height of a
block instance and the height that opens the next one, the last
second of a clock instance and the next one, a window that cuts the
last block instance short, a tip lowered by a reorganisation into
an earlier instance with its debits standing where they were
charged); ledger traces on stated facts in the manner of LIP-0026
section 7 (a spend with its fee against a total, an hour and a
maximum for one spend; the same spend against a count of blocks; a
reservation at a maximum settled below it; input and output against
a window and an instance; a debit that falls into the next instance;
a replay charged once; an uncertain outcome retained and then
reconciled; a counter filled exactly and the next request refused;
at 95 of 100 a debit of 6 refused without exhausting the account,
beside a debit of 5 admitted and filling it exactly). Identifiers,
models, currencies and accountings in such a file would be
placeholders, as they are in the vectors of LIP-0026.
The vectors bind nothing until both owners accept the rules that
they follow, and no octet of an existing vector file changes for
this LIP.

These paired text fixtures narrow the exhaustion and exactness
requirements. They are not an executable vector set or conformance
evidence. All unrelated checks pass; no per-request ceiling is
stated unless the case names one. A refusal leaves every account
and reservation unchanged and performs no effect.

| Case | Refused trace | Valid control |
| --- | --- | --- |
| `overshoot-room` | Own account 10 of 100, debit 95: `OWN_LIMIT_OVER`, account stays 10 and is not exhausted | A following debit of 5 is admitted at 15 of 100 |
| `overshoot-remainder` | Own account 95 of 100, debit 6: `OWN_LIMIT_OVER`, account stays 95 and is not exhausted | A following debit of 5 is admitted at 100, exactly exhausted; a further debit of 1 refuses `OWN_LIMIT_OVER` |
| `unbounded-cost` | Cost account 0 of 1000, no finite maximum under L18: `OWN_LIMIT_OVER`, no exhaustion | A following finite maximum of 5 is admitted at 5 of 1000 |
| `unbounded-output` | Output account 0 of 1000, no longest output under L20: `OWN_LIMIT_OVER`, no exhaustion and no input reservation either | A following output maximum of 5, with input within its own ceiling, is admitted |
| `clock-instance-regression` | After debiting 10 to clock instance 2 of length 3600, `now = 7199` selects instance 1: `LIMIT_CLOCK_REGRESSION`, no account changes | `now = 7200` selects instance 2 and passes the instance check; a debit of 1 against its account at 10 of 100 is admitted at 11 |
| `clock-per-request-order` | Without LIP-0022, coins total 10 of 100, instance 2 of length 3600 at 10 of 70, per-request ceiling 50; at `now = 7199` a debit of 60 refuses `SPEND_OVER`, before the instance check; a debit of 5 instead refuses `LIMIT_CLOCK_REGRESSION` | At `now = 7200` a debit of 5 is admitted at total 15 of 100 and instance 2 at 15 of 70 |
| `clock-before-own` | Clock instances have length 3600; latest debit in instance 2, instance 1 at 70 of 70, instance 2 at 10 of 70. At `now = 7199` a debit of 1 refuses `LIMIT_CLOCK_REGRESSION`, not `OWN_LIMIT_OVER` on instance 1 | At `now = 7200` the debit of 1 is admitted in instance 2 at 11 of 70 |
| `clock-key-order` | The request consumes the total before its clock-period key of length 3600; total 100 of 100, latest instance 2, `now = 7199`, debit 1: `OWN_LIMIT_OVER` on the total before the later key's instance check | With total 99 of 100 and `now = 7200`, instance 2 at 10 of 70, debit 1 is admitted at total 100 and instance 2 at 11 of 70 |
| `unbounded-cost-per-request` | Cost account 0 of 1000, per-request ceiling 50, no finite maximum: `SPEND_OVER`, not `OWN_LIMIT_OVER`; no reservation | With the same ceilings, a finite maximum of 5 is admitted at 5 of 1000 |
| `unbounded-output-per-request` | Output account 0 of 1000, per-request output ceiling 50, no longest output: `SPEND_OVER`, no output or input reservation | With the same ceilings, a longest output of 5 and input within its own ceilings are admitted |
| `exact-room` | Own account 9000 of 10000, maximum 1001: `OWN_LIMIT_OVER`, account stays 9000 | Maximum 1000 is admitted at 10000 |
| `maximum-no-wrap` | Own account 9000 of 10000, maximum 18446744073709551616: `OWN_LIMIT_OVER`, never a debit of 0 | Maximum 1000 is admitted at 10000 |
| `maximum-offset-no-wrap` | Own account 9000 of 10000, maximum 18446744073709552116: `OWN_LIMIT_OVER`, never a debit of 500 | Maximum 500 is admitted at 9500 |
| `sum-no-wrap` | L14 spends with debits 18446744073709551615 and 1 sum to 18446744073709551616: `OWN_LIMIT_OVER` against an empty account with ceiling 18446744073709551615 | Debits 18446744073709551614 and 1 sum to 18446744073709551615 and are admitted at that ceiling |
| `product-no-wrap` | A finite L17 maximum in integer subunits of 9223372036854775808 times 2 is 18446744073709551616: `OWN_LIMIT_OVER` against an empty account with ceiling 18446744073709551615 | 9223372036854775807 times 2 is 18446744073709551614 and is admitted |
| `account-no-wrap` | Own account 18446744073709551615 at that ceiling, debit 1: `OWN_LIMIT_OVER`, never an account of 0 | At account 18446744073709551614, debit 1 is admitted at the ceiling |
| `row-no-wrap` | Own account 0, row account 18446744073709551615, both ceilings 18446744073709551615, debit 1: `ROW_CAP_OVER`, neither account changes | With row account 18446744073709551614, debit 1 is admitted in both accounts |
| `per-request-no-wrap` | Stated per-request ceiling 10000, maximum 18446744073709551616: `SPEND_OVER` before any reservation | Maximum 10000 passes that check and, with an empty own account of ceiling 10000, is admitted |
| `no-binary64-rounding` | Own account 9007199254740992 at that ceiling, debit 1: `OWN_LIMIT_OVER`, not a rounded account at the ceiling | At account 9007199254740991, debit 1 is admitted at 9007199254740992 |
| `fractional-binary64-over` | Own account 9993 of 10000, maximum 8: `OWN_LIMIT_OVER`, unchanged; forming price 0.07 times 100 in binary64 gives 7.000000000000001 and then 8, the forbidden `binary64-cost` mutant | Exact price 0.07 subunit times 100 tokens is 7; reserve 7 and admit at 10000, not 10001; 100 actual tokens settle at 7 and release 0 |
| `fractional-no-shortfall` | Exact price 0.10000000000000001 subunit times 1000000000 tokens is 100000000.00000001; reserve 100000001, so an empty account with ceiling 100000000 refuses `OWN_LIMIT_OVER`; binary64's 100000000 is short of the table and forbidden | With ceiling 100000001 the same request is admitted at 100000001; that actual count settles at the same integer and releases 0 |
| `fractional-sum-once` | Empty account, ceiling 1: reservation 2 refuses `OWN_LIMIT_OVER`; converting input cost 0.5 and output cost 0.5 separately to 1 each is the forbidden `round-parts` mutant | Sum the two parts exactly to 1, reserve 1 and admit at the ceiling; those actual parts settle at 1 and release 0 |
| `fractional-unit-price` | Own account 700 of 1000: reservation 1000 refuses `OWN_LIMIT_OVER`; rounding a unit price of 0.25 to 1 before multiplying by 1000 is forbidden | Exact price 0.25 subunit times 1000 tokens is 250, reserved once and admitted at 950 of 1000; those actual tokens settle at 250 |
| `fractional-settlement` | At price 0.05 subunit per token, 100 permitted tokens reserve 5. For 50 actual tokens, settling at 2 or refusing the fractional cost is forbidden; 2 is the `truncate-settlement` mutant | Actual cost 2.5 converts upward once to settlement 3; release exactly 2 of the reserved 5; 100 actual tokens instead settle at 5 with no release |
| `fractional-overflow` | Exact maximum 18446744073709551615.1 converts upward to 18446744073709551616: `OWN_LIMIT_OVER` against an empty account with ceiling 18446744073709551615, with no wrap or truncation | Exact maximum 18446744073709551614.1 converts to 18446744073709551615 and is admitted at that ceiling |

The named `fractional-binary64-over` regression fixture narrows the
repeated exactness finding to the fractional path: its valid control
must admit at 10000, while the `binary64-cost` mutant refuses it.
`fractional-no-shortfall` catches that mutant in the other direction:
it admits a request whose exact reservation exceeds the ceiling.
`round-parts` fails `fractional-sum-once`; `truncate-settlement` fails
`fractional-settlement`. These are text-level mutation witnesses,
not a claim that an executor or the planned vector checker was run.

## Sources

- LIP-0008 section 2: the meanings of the three kinds and the
  decision of 2026-11-14 for coins; section 2.1: a grant for the
  whole term and the period as a term of a limit, counted in blocks
  or in clock time as its type profile and the contract have it;
  section 7.1: the window as two heights, half-open, no clock
  member and a reorganisation that can lower `H`; section 4 and
  section 12.2: the concrete executor and the charging of every link.
- LIP-0022 sections 1 to 5: one observation between two reads of the
  same tip and the recheck before a reservation (B1.1, B1.5, B1.6),
  a tip that conflicts (B2.4, B2.5), the clock in whole seconds of
  UTC (B3.1), verdicts relative to the active chain after a
  reorganisation (B4.4), and no comparison of depths across chains
  (B5.3), applied to heights in the same manner by this LIP.
- LIP-0006 (`amount_sat`, atomic NMC units at most
  `21000000 * 100000000`) and LIP-0013 section 2.1 (`spend_budget` in
  atoms, 0 to 2100000000000000): the scale of NMC that L11 states.
- LIP-0018 section 2: the fourteen items of a limit kind, and the
  two rules that hold for every kind without restating them.
- LIP-0020 section 2 and W11.1: the string form and its bound;
  W11.4: the members of a limit and the ceiling of an unstated key;
  W11.10 rule 6 and W11.14: the pool sum and the registries.
- LIP-0026 R1.2, R2.4, R5.2 to R5.8, R6.2 and R8.5: the key, the
  comparison of ceilings, the accounts, and count times amount.
- LIP-0014 section 8.4, rows F6, F17, E1 to E3 and rules T1 and T9:
  the place of the kind, and the contract profile that every child
  admission still waits for; J4.4 (a): for one place of one parent
  the service MUST make one signature, ever, a place being the
  ordinal of a row.
- LIP-0025: the form of the journal behind the accounts, and what a
  recovery charges for a row account.

## Alternatives

**One cumulative kind with the resource doing all the work.** Coins,
cost and tokens could share one kind whose resource names what is
counted. Not taken: LIP-0008 section 2 names them as kinds with
meanings of their own, their settlements differ (a fee inside a
debit, a reserved maximum, two directions of one count), and a side
that serves one resource of a shared kind and not another could not
say so in F17, which judges kinds.

**A ceiling per period without a total.** L5 could consume only the
keys that a grant states, so that a grant for one period needs no
whole-window limit. Not taken as the rule, and left to the owners in
the open questions: the meaning of coins binds a total, a missing
total under the other reading is an unlimited term behind a bounded
hour, and under the PROPOSED reading of section 5 a long-lived
agent that wants period-sized authority gets a new grant per period,
whose total is its window.

**The maximum for one spend as a fourth kind.** LIP-0008 section 2
lists maximum answer length beside model tokens, so a per-request
ceiling as a kind of its own has a precedent in the list. Not taken
for coins: the decision adds the maximum to the kind coins, and the
reserved text of L3 carries it in the members that exist. A fourth
kind would need its own pool key for a bound that no account sums;
the chosen reading needs the same pool key, because rule 6 of
W11.10 takes exactly the keys that a template limits, and L6 and
L12 state that cost instead of counting it only against the
alternative. For the output of a model the precedent stands as that section
leaves it, and L21 does not take its place.

**Settling nothing: the reservation is the charge.** An executor
could keep every reserved maximum as spent. Not taken: R5.8 leaves
the release to the type profile because kinds differ, and for cost
and output the maximum is a bound that most requests stay far below,
so keeping it would price a ceiling by the longest answer that a
grant ever permitted and not by any answer that it got. For coins
and for input, which are known before the effect, reservation and
charge already coincide.

## Security consequences

A ceiling binds only at the executor that meters it, under an intact
journal and credentials; LIP-0008 section 2 states the boundary for
an upstream key, and it holds here unchanged. Inside that boundary
the profiles close three ways past a signed amount. The fee is
inside the debit of coins, so a payer cannot be charged a signed
total and then its fees on top. The maximum is reserved before the
effect for cost and output, so parallel requests cannot each fit a
ceiling that only one of them fits, and an uncertain outcome keeps
its reservation instead of freeing room for a second spend of the
same allowance. And no unrecognised text passes as no limit: a grant
written against a currency, an accounting or a period that the
executor does not serve refuses instead of being served unbounded
under a key that nobody debits.

The price is stated where it falls. The reserved maximum is held for
as long as an outcome is unknown, so a slow upstream holds allowance
that a settled request would have freed. The total that L5 always
consumes makes a template without one useless by refusal, loudly,
at the first request of its first child. And the executor's own
count and price govern (L17, L20): a recipient who disputes a bill
has the journal entries and the upstream count as evidence, and no
rule of this LIP makes a third side recount a request.

## Conformance impact

The paragraph of section 5 that states the four rules is decided
by the owner on 2026-11-17 and in force in this version. The separate
PROPOSED reading, including its accounts and triggers, has no
interim force. The relation of the fourth rule to LIP-0008
section 2.1 is open, not a claim that no rule of a text in force is
affected. No member of `swarma-grant/4` changes, no octet of a
tool or of a vector file changes, and Grant v3 is untouched. A side
that adopts no profile of this LIP refuses the three kinds as
`LIMIT_KIND_UNDEFINED`, exactly as version 0.1.57 has it; a side
that adopts one judges its limits under F17 and E2 instead — and
even at such a side parts (b) and (d) of row F6 still end every
child admission before F17 until a v4 contract profile exists
(LIP-0014 rule T1), so no child with limits is admitted end to end
by this LIP. The registry entry in LIP-0020 W11.14 records the
proposal and decides nothing. Nothing of this LIP is implemented,
and its vectors are described and not built (section 7).

## Open questions

- **The owners' acceptance** of each proposed rule, and first of the
  five points that "What is decided and what is proposed" lists.
  The paragraph of section 5 that states the four rules needs no
  acceptance: it is decided. Every interpretation outside that
  paragraph, including the separate PROPOSED reading, needs it.
  The co-author's
  agreement is pending on the decisions that sections 2 to 4 build
  on, as LIP-0008 section 2 and LIP-0018 section 2 record them, and
  the co-author's answer on section 5 is folded in by amendment.
- **Exhaustion details beyond the four rules.** Only the paragraph
  of section 5 that states the four rules is decided and in force.
  The separate PROPOSED reading has no interim force. Open: the
  trigger beyond an account at its ceiling; the report recipients,
  carrier and form; how a delegating side learns of it without
  polling the executor; continuation of a root; and what code, if
  any, a request takes after the stop that L8 would admit, including
  both zero and positive debits. The relation to LIP-0008
  section 2.1 must address both "Each grant covers the whole agreed
  term" and "A new period needs no new grant, no new seal and no new
  issuance record". The draft's reconciliation decides nothing;
  whether and how that section is amended is for the owners.
- **Period texts beyond the two families.** L3 assigns the
  block-counted and clock-counted families, their counts and the
  boundaries of their instances; every other text refuses under L4.
  Open: calendar months, calendar years, local-time days and a
  contract's chosen week alignment; who assigns a further text and
  in what registry; a block
  count on a chain other than the grant's, whose instance anchor no
  signed member states (L12); what a recovery by starting anew
  charges for an instance account (L7, L9), and whether an instance
  that ended before a loss can be told from one that did not —
  block instances answer that from `H` where the journal names the
  instance's heights, clock instances only as far as the kept clock
  mark of LIP-0022 B3.2 reaches, and neither answer is written here.
- **Permitted targets for coins.** The meaning in LIP-0008
  section 2 binds them, a grant has no member for a list of targets
  or payees (LIP-0020 W11.2), and this LIP invents none. A target
  list needs a member, and with it a comparison at admission and a
  refusal; until then a limit of this kind bounds how much, never
  to whom.
- **Further payment systems, and their atomic scales.** This LIP
  assigns `namecoin:NMC`, the unit text `atomic` and, for that one
  system, the scale that the tree carries (L11). Each further
  system — a chain with its asset, or a rail outside a chain —
  needs a text that assigns its resource and its scale, and a
  decision on who assigns values under no namespace of this
  specification.
- **Fees and displaced spends.** A fee paid in another asset than
  the one spent; a fee raised after the reservation by replacing
  the spend; a spend displaced by a reorganisation and confirmed
  again, or dropped without a conflicting spend in view. L15
  settles the conflicting spend and retains the rest; the charges
  of the other cases are open.
- **Price tables.** Who sets the table of L17, how a grant or a
  contract pins it, what a change of it does to requests already
  reserved, and what an executor does with a charge above the
  reserved maximum (L18). With it: the currency codes and
  subdivisions that a unit of L16 may state.
- **Token accountings and model names.** The identifiers of L19 and
  the model texts of L16 are assigned by no text here. Open with
  them: a request whose input the executor cannot count before
  sending under the named accounting, and how a recipient disputes
  a count that the upstream reports differently (L20).
- **The kinds not profiled here.** Model requests, maximum answer
  length with its signed default output allowance, and required
  confirmation depth from the first table of LIP-0008 section 2 —
  the last a floor, whose comparison R2.4 leaves to its profile —
  and the nine kinds of its second table. Each still needs a type
  profile, and the default output allowance needs a member that
  `swarma-grant/4` does not have. Until maximum answer length is
  profiled, the longest output that a request permits in L20 comes
  from the request alone, under members of the invocation that do
  not exist yet.
- **The total that L5 always consumes.** Whether a grant that
  states only a ceiling per period should authorize inside that
  period instead of refusing at a total of 0. Alternatives states
  why this draft refuses; the owners may read the meanings of
  section 2 otherwise for cost and tokens, whose table entries name
  no total.
- **The mirror of `period` in a contract.** LIP-0008 section 2
  states the mirror by executor, kind, resource, unit and amount;
  whether the contract also mirrors `period`, which key and
  instance both depend on, comes with the v4 contract profile and
  the code of L10.
- **Evidence and identity.** The members of the invocation and of
  the receipt, the octets of a reservation entry, and the key that
  identifies a request (L8, L15). L9, L14 and every settlement rest
  on that identity and state it as a fact until then.
- **Vectors and a checker** for the set of section 7, and a second
  implementation that shares no code with the first, as the other
  profiles ask of theirs.



