# LIP-0031: Limit-kind profiles 1 — coins, model cost, model tokens

- **Status:** Draft. Everything in this LIP except section 5 is proposed;
  nothing else in it is in force by this text.
  Section 5 is decided: the owner approved it on 2026-11-17, as that
  section says.
- **Created:** 2026-11-17
- **Affects:** the first three entries of the registry of limit kinds
  (LIP-0020 W11.14): what a limit of each kind counts, in which unit and
  over which period, how an executor reserves and settles it, what a
  verifier compares at the admission of a child against the template and
  the pool of its parent, and what follows when a counter reaches its
  ceiling
- **Builds on:** LIP-0008 sections 2, 2.1, 4 and 12.2, LIP-0018
  section 2, LIP-0020 sections 2 and 11 (W11.1, W11.4, W11.10, W11.14),
  LIP-0026 sections 1, 2, 5, 6 and 8, LIP-0014 sections 8.4 and 11.1
  (J4.4 (a)) and LIP-0025
- **Deciders:** both owners

## Summary

The registry of limit kinds is empty. LIP-0020 W11.14 lists no defined
kind, and its rule 2 follows from that: a child that states a limit, and
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
- exhaustion and continuation, in one paragraph to which every other
  text points (section 5);
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
| For one place of one parent the signing service makes one signature, ever | LIP-0014 J4.4 (a) | Section 5 builds continuation on it |

Every rule of this LIP is the draft's proposal, and neither owner has
decided one. Six points are choices of this draft where no text gives
an answer, and the owners should look at them first:

1. The reading of `period` in L3: an absent `period` is the total over
   the whole window, a present one is a ceiling per period instance,
   and one reserved text, `swarma/per-request`, is the ceiling of a
   single request. W11.4 gives a limit with and without `period`
   different keys and gives neither a meaning; LIP-0018 section 2 asks
   a proposal to state whether a limit holds for one request, for a
   period or for the whole window.
2. A request always consumes the key without `period` for its kind,
   resource and unit, so a grant that states only a ceiling per period
   authorizes nothing (L5). The alternative, a grant per period with
   no total, stands under Alternatives.
3. One account for each period instance (L7). LIP-0026 section 5 keys
   an account by grant or row and limit key and holds no vector with a
   period; which instance a debit belongs to has no answer there.
4. Two new codes, `LIMIT_UNSUPPORTED` and `SPEND_OVER` (section 6).
   Every other refusal of this LIP takes a code that a landed text
   already names.
5. The settlement of sections 3 and 4 releases the difference between
   the reserved maximum and the actual consumption once the outcome is
   known. LIP-0026 R5.8 leaves that release to the type profile.
6. Section 5 whole is decided: Ivan Oparin approved it on 2026-11-17.

Nothing of this profile is implemented. The owners accept or change
its rules through this LIP, under LIP-0001.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The comparison of a child against its template and the pool for the three kinds, as a function of signed octets | Yes | The owners' acceptance |
| The accounts and the reservation of sections 1 to 4 as functions of stated facts | Yes | The owners' acceptance |
| A spend, a priced request or a token count at a real executor | No | An action profile that consumes the kind (LIP-0020 W11.14 rule 1); the members of the invocation and of the receipt (LIP-0020) |
| A period other than the reserved text of L3 | No | A definition of its length and counting (open questions) |
| The vectors of section 7 | No | The owners' acceptance; no file exists |
| The report of section 5 to a parent | No | A carrier for the report (open questions) |

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
| L3 | `period` has three readings, and no other. Absent: the amount bounds the sum of all debits of the key over the whole window of the grant. Present with the text `swarma/per-request`: the amount bounds the debit of one request. Present with any other text: the amount bounds the sum of the debits of the key inside one instance of the period that the text names. A period divides the one window for accounting (LIP-0008 section 2.1); whether an instance is counted in blocks or in clock time, how long it is, and where its boundaries fall are fixed by the definition of its text in the contract that mirrors the limit, as section 2.1 has it. This LIP assigns the one reserved text and no length. | L4 for a text with no definition at the side |
| L4 | A side that has the profile of a kind and meets a limit of that kind whose `resource`, `unit` or `period` it does not recognise under sections 2 to 4 — an asset system it does not serve, a currency and scale it has no price in, an accounting it does not count by, a period text with no definition in the presented contract — refuses as `LIMIT_UNSUPPORTED`. The refusal stands where the kind is judged: at the admission of a child inside row F17 with its part (b), after the kind and before the amounts, and at a request inside row E2. A kind with no profile at the side is not this refusal; it stays `LIMIT_KIND_UNDEFINED` (LIP-0020 W11.14 rule 2). No unrecognised text is read as no limit. | `LIMIT_UNSUPPORTED` |
| L5 | A request consumes keys as follows. For the kind, resource and unit that the request draws on it always consumes the key without `period`. It also consumes every key with a `period` other than the reserved text that the grant — for a request under a child, the child and the template of its row together — states for the same kind, resource and unit, each in the instance that holds the request. The key with the reserved text, where stated, is checked per kind in sections 2 to 4 and is no cumulative account. A key that a request consumes and that the grant does not state has the ceiling 0 (LIP-0020 W11.4; LIP-0026 R5.2), so the first debit against it refuses. Which resource and unit a request draws on is fixed by the action that it asks for and by the executor that serves it, under the profile of that action; this LIP defines no action. | At the reservation, L8 |
| L6 | At the admission of a child the three kinds are compared in row F17 of LIP-0014 section 8.4, in its three parts: every limit of the child has the key of a limit of the template of its row (part (a)); the kind of every limit of the child and of the template has a profile at the side, and its texts are recognised there (part (b) with L4); each amount of the child is at most the amount of the template under the same key (part (c), by L2). A child need not restate a key of its template to pass this step; a key that it omits then has the ceiling 0 in its own account under R5.2 and authorizes no consumption under the child, whatever the row states. Against the pool nothing is compared at an admission: the pool is judged on the signed octets of the parent, one pool for every key that a template limits, by the sum over the groups of the number of rows of the group times the amount of its template for that key, an exact integer sum that never wraps (LIP-0026 R8.5; LIP-0020 W11.10 rule 6). The pool is no account, and what one row leaves unused is available to no other row (LIP-0026 R5.5). | `CHILD_BUDGET_OVER`; `LIMIT_KIND_UNDEFINED`; `LIMIT_UNSUPPORTED`; for the pool, `GRANT_DELEGATE` |
| L7 | A request under a grant that is no child debits the own accounts of that grant, and a request under a child the own account of the child and the row account of its parent and its ordinal, and no own account of the parent (LIP-0026 R5.3, R5.4). For a key without `period` the account is the account of R5.2. For a key with a `period` the executor keeps one such account for each instance of the period, keyed beside R5.2 by the instance that holds the debit; the instance is read from the executor's node where the period counts blocks and from its clock where it counts clock time, under the definition of L3. An account of an instance begins at 0, and a debit that falls after the instance has ended belongs to the next one and never back into the ended one. A session debits its own account beside these, as LIP-0028 T4.6 proposes, and that account takes the instance of its key in the same way. | L8 |
| L8 | Before the effect of a request the executor reserves the debits of every key that the request consumes, durably and in one atomic write of its journal, or none of them, taking the keys in the order in which the request consumes them and for each key the own account before the row account, and it reports the first account whose ceiling the reservation would exceed (LIP-0026 R5.6). What is made durable is the reservation entry of the journal; its octets and the key that identifies a request come with the members of the invocation (LIP-0026 section 5) and are open here as there. A request that is refused reserves nothing (LIP-0026 R6.2). Parallel requests and the replicas of one executor share one allowance through that one journal, in the form that LIP-0025 proposes; no replica keeps a remainder of its own (LIP-0008 section 4; LIP-0026 R5.5). | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| L9 | One request identity holds at most one reservation, and a repeated request is charged once (LIP-0026 R5.7). A reservation whose effect has an outcome that is not known is retained until it is reconciled, and no account is lowered by a revocation, a restart or an unknown outcome (LIP-0026 R5.8; LIP-0008 section 2). Where sections 2 to 4 settle a reservation at an actual consumption below the reserved amount, the difference is released in the same accounts that the reservation debited, in one write with the entry that records the outcome, and only where that outcome is known: the effect happened at the settled consumption, or it did not happen. A settlement never raises an account above the reserved amount of its request, and a consumption above the reservation is not charged to the grant after the effect; each kind states what its reservation must cover so that this case cannot arise inside the profile. After a recovery by starting anew, what an account counts as is the rule of LIP-0025 section 7 for row accounts; what it charges for an instance account of L7 is an open question. | None of its own |
| L10 | The contract mirrors the limits of the grant as LIP-0008 section 2 states it, and a mismatch refuses admission there; the code of that refusal comes with the v4 contract profile and is open (LIP-0014 section 8.4, row F6 part (c)). A default selects an allowance only within the signed limit and never supplies a limit that the grant lacks (LIP-0008 section 2; LIP-0018 section 2). Operator ceilings of the executor may be lower and never higher, as that section has it. The two rules that LIP-0018 section 2 holds for every kind without restating them hold here in the same way and are cited, not repeated, in each table below. | None of its own |

Two consequences of L5 are stated in place. A parent whose template
states only a ceiling per period gives its children nothing to spend:
the key without `period` has the ceiling 0, and the first request
refuses at its reservation, against the own account first, however
much room the period has. And a template that states two periods for one resource, an hour
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
| L11 | `resource` is the identifier of the asset and of the payment system, in the form `<system>:<asset>`. The system is a chain with its asset, or a rail outside a chain, in the words of the decision. This LIP assigns one value, `namecoin:NMC`, for Namecoin and its coin. Every further value is assigned as L4 and the open questions have it, by a text that names the system, the asset and its atomic unit; a value that no such text assigns is unrecognised at every side. `unit` names the atomic unit of the asset, the smallest unit that the payment system itself counts, and `amount` counts atomic units. For `namecoin:NMC` this LIP assigns the unit text `atomic`; how many atomic units one whole coin holds is a fact of the payment system, stated by the text that assigns the resource, and no side converts an amount through a number of whole coins. | L4 |
| L12 | The three maxima of the decision are three limits of one kind with one `resource` and one `unit`, told apart by `period` under L3: without `period`, the total over the term of the grant; with a period text, the maximum inside one instance of that period; with `swarma/per-request`, the maximum for one spend. A grant states any of them, and each stated one bounds every spend under L5; the total is the key that every spend consumes, stated or not. | L5, L8 |
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
| Unit and integer scale | Atomic units of the asset; `amount` in the string form (L1, L11). No amount is a floating-point number, as the item requires and LIP-0020 section 2 has it. |
| Bounds and rounding | 0 to 18446744073709551615 (L1). No rounding: a debit is a whole number of atomic units or it is not made (L13). |
| Period and aggregation | Whole window, per period instance, and one spend, by `period` (L3, L12); instances in blocks or clock time by the definition of the text; debits add inside an instance (L7). |
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
| At the admission of a child | Keys, kind and texts, then amounts against the template; the pool by count times amount on the parent (L6). |

### 3. `swarma/model-cost`

Model cost is the kind of LIP-0008 section 2 whose meaning a profile
must bind to a cumulative cost ceiling, an exact currency and scale
and the price or conservative reservation policy used to account for
it. This profile adopts that meaning and takes the conservative
reservation: the maximum is reserved before a request and the actual
cost is settled after it. In the second table of that section the
kind is the first case of external service cost; this LIP profiles
the model case alone and assigns no identifier for the wider kind.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| L16 | `resource` names the priced model at the executor that serves it, in the form that the executor's own profile states for its models; this LIP assigns no model name, and a resource that names no model of the executor is unrecognised there. `unit` states the currency and its scale in one text of the form `<currency>/<scale>`, where `<currency>` is the code of the currency as the executor's price table states it and `<scale>` is the name of the smallest subdivision that the table accounts in. `amount` counts that subdivision. Two limits that differ in currency or in scale are two keys and are never added together, and no side converts between currencies or scales inside this profile. Which codes and subdivisions a deployment uses is stated by its price table under L17; a unit that the table does not state is unrecognised. | L4 |
| L17 | Before a request the executor reserves the maximum cost of that request under its price table: the highest cost that the table gives the request as asked, over every part that the table prices, the input that it carries and the longest output that it permits included. The reservation is made under L8 in the unit of the limit, and a cost that the table states as a fraction of the subdivision is rounded up to a whole subdivision before it is reserved, so that the reservation never falls short of the table. A request whose maximum the table cannot give — an output without a permitted length, a part with no price — is not served under this kind. The price table is the executor's: who sets it, how it is signed or pinned, and how a change of it meets a live grant have no member and no text, and stand in the open questions. A change of the table changes no signed ceiling; it changes what one request reserves against it. | L8; for no finite maximum, L18 |
| L18 | When the outcome of a request is known, the executor settles the reservation at the actual cost under the same table and releases the difference under L9. A request that the upstream refused before any priced work settles at 0; priced work that was done settles at its table cost whether or not the answer was used. An outcome that is not known retains the full reserved maximum until it is reconciled (L9). A charge above the reserved maximum is outside this profile: the reservation was the highest cost of the table, so a higher charge means the table did not govern the request, and the executor charges nothing above the reservation to the accounts of the grant. What it does with such a charge is an open question. A request with no finite maximum under L17 reserves nothing and refuses at the reservation step against the first account that it consumes, as a reservation above every ceiling does. | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |

The ceilings of this kind are the whole-window total and, for each
stated period, the ceiling of its instance (L3, L5). The reserved
text of L3 gives a third, a maximum cost for one request, checked
against the reserved maximum of L17 before any reservation, as L14
checks one spend; this profile gives that check the same refusal,
`SPEND_OVER`, by the proposal of section 6. A grant that wants only a
ceiling per period states the total as well or authorizes nothing
(L5).

| Item of LIP-0018 section 2 | `swarma/model-cost` states |
| --- | --- |
| Identifier and resource | Kind `swarma/model-cost`; the resource is one priced model at its executor (L16). |
| Unit and integer scale | One currency in its smallest accounted subdivision; `amount` in the string form (L1, L16). |
| Bounds and rounding | 0 to 18446744073709551615 (L1). A fractional cost rounds up to the subdivision (L17). |
| Period and aggregation | Whole window and per period instance (L3, L5); settled costs add inside an instance (L7, L18). |
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
| At the admission of a child | Keys, kind and texts, then amounts against the template; the pool by count times amount on the parent (L6). |

### 4. `swarma/model-tokens`

Model tokens is the kind of LIP-0008 section 2 whose meaning a
profile must bind to separate cumulative input and output token
ceilings, with the model and token-accounting profile. This profile
adopts that meaning. It does not profile maximum answer length, which
that section lists as a kind of its own, and it gives the signed
default output allowance of that kind no member, because
`swarma-grant/4` has none; both stand in the open questions.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| L19 | `resource` names one model together with the token accounting that counts for it, in the form `<model>/<accounting>`, where `<model>` is the model as the executor's profile states it — the same text that L16 prices — and `<accounting>` is the identifier of the counting under which the executor reports input and output. This LIP assigns neither part; a pair that the executor does not serve is unrecognised there. `unit` is `input-token` for the ceiling of tokens sent to the model and `output-token` for the ceiling of tokens received from it, so the two ceilings of the meaning are two keys for one resource. `amount` counts tokens. Input and output are never added together, and a count under one accounting is never compared with a ceiling of another. | L4 |
| L20 | The executor counts. The input of a request is counted under the named accounting before the request is sent and is reserved at that count. The output is reserved before the request at the longest output that the request permits under the same accounting, and a request that permits no longest output reserves nothing and refuses at the reservation step, as L18 has it for cost. When the outcome is known the output reservation settles at the counted output under L9; the input, counted exactly, settles at its reservation where the request was sent and at 0 where it was not. A count that the upstream reports beside the executor's own does not govern: where the two differ the account keeps the executor's count under the named accounting, and the difference is evidence for the parties and no debit. An outcome that is not known retains both reservations until it is reconciled (L9); output received before the outcome became unknown is counted where the executor holds it, and the rest of the reserved output stays reserved. | L8; `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
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
| Bounds and rounding | 0 to 18446744073709551615 (L1). No rounding: a count is a whole number of tokens under its accounting (L20). |
| Period and aggregation | Whole window and per period instance, separately for input and output (L3, L5, L7). |
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
| At the admission of a child | Keys, kind and texts, then amounts against the template; the pool by count times amount on the parent (L6). |

### 5. Exhaustion and continuation

**Decided by the owner on 2026-11-17.** Ivan Oparin approved the rules
of this section on 2026-11-17; the co-author's answer is folded in by
amendment. The paragraph that follows is the one place that states what
exhaustion and continuation are for the kinds of this LIP, and every
other text points here: the README, the changelog and the unresolved
questions. The open points listed under "What is decided and what is
proposed" stay open inside it.

When a counter of a grant reaches its ceiling — the whole-window
account of a key, or the account of the instance that holds the
request — the executor stops the action under that grant: it admits
no further request that consumes that key under that grant while the
ceiling stands, it reports the exhaustion to the parent, for a child
to the delegating side of its parent and for a root grant to its
issuer, and the grant is not revoked, no seal is spent and no closure
is recorded, so a later instance of a period admits again under the
same grant where the ceiling that stopped the action was an instance
account, and a whole-window ceiling stops it for the rest of the
window; an existing grant is never topped up, because for one place
of one parent the signing service makes one signature, ever
(LIP-0014 J4.4 (a)), and a signed amount therefore changes only with
a new grant; continuation is a new child grant on a new place of the
parent's pool, under a row that no child has taken, with its own seal
and its own accounts, and never a second signature for the place of
the exhausted child and never a larger amount written over it; and a
long-lived agent is given its limits per period, as a new grant for
each period where the deployment renews by grant, in the pattern of
a per-period effect grant, or as limits with a period inside one
grant for the whole term where it does not (LIP-0008 section 2.1),
and in neither pattern does a new period by itself enlarge a ceiling
that a grant already signed.

### 6. Refusals and their order

| Code | What it reports | Rule | Name |
| --- | --- | --- | --- |
| `CHILD_BUDGET_OVER` | A limit of the child is above the limit of its row under the same key, or has a key that the row does not have | L2, L6 | LIP-0026 R2.4; LIP-0014 J1.2 |
| `LIMIT_KIND_UNDEFINED` | The kind of a limit has no type profile at the side | L4, L6 | LIP-0020 W11.14 rule 2 |
| `LIMIT_UNSUPPORTED` | The kind has a profile at the side and the `resource`, `unit` or `period` of the limit is not recognised there | L4 | New |
| `SPEND_OVER` | One request is above the ceiling for one request of its kind: one spend, one reserved maximum, one input count or one longest output | L14; section 3; L21 | New |
| `OWN_LIMIT_OVER` | A reservation would exceed an own account, of the window or of an instance | L7, L8 | LIP-0026 R5.6 |
| `ROW_CAP_OVER` | A reservation would exceed a row account, of the window or of an instance | L7, L8 | LIP-0026 R5.6; LIP-0014 J1.3 |
| `GRANT_DELEGATE` | The pools of a parent do not bound the sums of its templates for a key of the three kinds | L6 | LIP-0020 W11.10 rule 6 |

The form of a limit refuses in the member step with the codes of that
step, and no code of this LIP changes their meaning (L1). The refusal
of a contract that does not mirror a limit has no code yet (L10).

At the admission of a child the order is that of row F17: the keys
(`CHILD_BUDGET_OVER`), then the kind (`LIMIT_KIND_UNDEFINED`) and
the texts (`LIMIT_UNSUPPORTED`), then the amounts
(`CHILD_BUDGET_OVER`). At a request the order is: the action and the
kinds it consumes, with their texts (rows E1 and E2;
`LIMIT_KIND_UNDEFINED`, then `LIMIT_UNSUPPORTED`); then the ceiling
for one request (`SPEND_OVER`); then the reservation, own account
before row account for each key (`OWN_LIMIT_OVER`, `ROW_CAP_OVER`).
The place of `LIMIT_UNSUPPORTED` beside the kind and of `SPEND_OVER`
before the reservation are proposals of this LIP, marked NEW against
the table of LIP-0014 section 8.4, which has neither code. The checks
of the invocation itself (row E0) have no codes and no order against
E1 and E2 in that table, and this LIP orders nothing against them.

None of these refusals records a closure. Exhaustion under section 5
is no refusal and has no code: the request that fills a counter is
served, and the next one refuses at its reservation as above.

### 7. Vectors

No vector file of this LIP exists, and no checker for it is in this
repository. The set that the profiles need, paired valid and refused
cases with a checker that recomputes them as LIP-0018 section 2
asks, is described here so that its absence is stated and not
discovered: for each kind, admissions of a child against a template
and a pool on stated octets (a key the row lacks, an unrecognised
text, an amount one above the row, a pool one short of the sum);
ledger traces on stated facts in the manner of LIP-0026 section 7 (a
spend with its fee against a total, an hour and a maximum for one
spend; a reservation at a maximum settled below it; input and output
against a window and an instance; a debit that falls into the next
instance; a replay charged once; an uncertain outcome retained and
then reconciled; a counter filled exactly and the next request
refused). Identifiers, models, currencies and accountings in such a
file would be placeholders, as they are in the vectors of LIP-0026.
The vectors bind nothing until both owners accept the rules that
they follow, and no octet of an existing vector file changes for
this LIP.

## Sources

- LIP-0008 section 2: the meanings of the three kinds and the
  decision of 2026-11-14 for coins; section 2.1: a grant for the
  whole term and the period as a term of a limit; section 4 and
  section 12.2: the concrete executor and the charging of every link.
- LIP-0018 section 2: the fourteen items of a limit kind, and the
  two rules that hold for every kind without restating them.
- LIP-0020 section 2 and W11.1: the string form and its bound;
  W11.4: the members of a limit and the ceiling of an unstated key;
  W11.10 rule 6 and W11.14: the pool sum and the registries.
- LIP-0026 R1.2, R2.4, R5.2 to R5.8, R6.2 and R8.5: the key, the
  comparison of ceilings, the accounts, and count times amount.
- LIP-0014 section 8.4, rows F17, E1 to E3 and rule T9: the place of
  the kind; J4.4 (a): one signature for one place, ever.
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
hour, and section 5 already gives a deployment that wants
period-sized authority a new grant per period, whose total is its
window.

**The maximum for one spend as a fourth kind.** LIP-0008 section 2
lists maximum answer length beside model tokens, so a per-request
ceiling as a kind of its own has a precedent in the list. Not taken
for coins: the decision adds the maximum to the kind coins, the
reserved text of L3 carries it in the members that exist, and a
fourth kind would need its own pool key for a bound that no account
sums. For the output of a model the precedent stands as that section
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

None on any text in force. No member of `swarma-grant/4` changes, no
octet of a tool or of a vector file changes, and Grant v3 is
untouched. A side that adopts no profile of this LIP refuses the
three kinds as `LIMIT_KIND_UNDEFINED`, exactly as version 0.1.57
has it; a side that adopts one judges its limits under F17 and E2
instead. The registry entry in LIP-0020 W11.14 records the proposal
and decides nothing. Nothing of this LIP is implemented, and its
vectors are described and not built (section 7).

## Open questions

- **The owners' acceptance** of each rule, and first of the six
  points that "What is decided and what is proposed" lists. The
  co-author's agreement is pending on the decisions that sections 2
  to 4 build on, as LIP-0008 section 2 and LIP-0018 section 2 record
  them.
- **Section 5, whole.** Exhaustion and continuation are decided by the
  owner (2026-11-17). Still open inside it: the carrier and the
  form of the report to the parent, how a delegating side learns of
  it without polling the executor, and the reading of its last
  clause — this draft states a new grant per period and limits with
  a period inside one grant as two patterns that a deployment
  chooses between; whether the owner means one of them is not
  decided by this text.
- **The definitions of period texts.** Their lengths, their counting
  in blocks or in clock time, where an instance begins against a
  window stated in heights, and who assigns a text. Until a text has
  a definition in the contract, L4 refuses it, so no period but the
  reserved one can be served yet. With it: what a recovery by
  starting anew charges for an instance account (L7, L9), and
  whether an instance that ended before a loss can be told from one
  that did not.
- **Permitted targets for coins.** The meaning in LIP-0008
  section 2 binds them, a grant has no member for a list of targets
  or payees (LIP-0020 W11.2), and this LIP invents none. A target
  list needs a member, and with it a comparison at admission and a
  refusal; until then a limit of this kind bounds how much, never
  to whom.
- **Further payment systems, and their atomic scales.** This LIP
  assigns `namecoin:NMC` and the unit text `atomic` and states no
  number of atomic units in a whole coin for any system. Each
  further system — a chain with its asset, or a rail outside a
  chain — needs a text that assigns its resource and its scale, and
  a decision on who assigns values under no namespace of this
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



