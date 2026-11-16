# LIP-0026: Rows and accounts profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** what a v4 parent states for each row, how a verifier checks
  that a child fits its row and that its issuance spent the coin of the
  row, how the re-delegating side derives, funds and uses the key of that
  coin, and which accounts of an executor's ledger a request debits
- **Builds on:** LIP-0014 section 9.1 (J1), LIP-0008 sections 2, 3.1, 4,
  11.1 and 12.2, LIP-0022 sections 1 and 4, LIP-0023 and LIP-0025; for
  sections 8 to 10 also LIP-0010 section 10, LIP-0014 section 8.3 and
  LIP-0021

## Summary

A parent grant of v4 signs one row for each child that it permits, and each
row pins a coin that the issuance of its child must spend (LIP-0014 section
9.1, J1.9). The decision names the key of that coin. It leaves open who
funds the coin and which account and path the key has, and it names no code
for a child whose issuance does not spend the coin. The same section has an
executor reserve every request under a child in two ledgers, the child's
and the row's, in addition to every ancestor link of LIP-0008 section 12.2.
LIP-0014 section 9 keeps the parent's own budget apart from the pool of its
children. An executor that charged a child's request against the parent's
own budget would follow one reading of LIP-0008 and break LIP-0014.

This LIP proposes the first profile for rows on v4, on Namecoin:

- what a parent states for a row, and the bound of a pool over its rows
  (section 1);
- the checks of a child against its row, on signed octets alone (section
  2);
- the coin of a row: its script, the block at or below which it is
  confirmed, that it lies outside the child's seal transaction, and the
  input of the child's anchor that spends it (section 3);
- the row account of the signer: its path, its index, its funding, and the
  one kind of input that a row key signs (section 4);
- the accounts of an executor's ledger, and which of them a request debits
  (section 5);
- nine refusal codes, four of them new, and their order (section 6);
- vectors, among them a trace of one parent over three executors and a
  trace of direct requests beside the requests of siblings (section 7).

It defines no octets of a row. Since version 0.1.53
[LIP-0020](LIP-0020-grant-v4-wire-registry.md) section 11 defines them, with
the members of a v4 grant: the right of re-delegation with its pools, its
groups, their templates and their ranges. That section states which member
each rule of this LIP reads and changes no rule of it.

Sections 8 and 9 state two decisions of Ivan Oparin of 2026-11-15, in force
since version 0.1.51: a parent states its rows in groups (J12), and a row may
name the recipient of its child by a class of landlords (J10). On 2026-11-16
Ivan Oparin put them in force without waiting for the co-author's agreement,
which has not been given; the co-author's answer is folded in by amendment.
Sections 1 to 7 are read as sections 8 and 9 say for groups and the recipient.
Section 10 holds J9, decided and agreed by both owners on 2026-11-15: a row
inside one owner may have no certifier, so the certifier of R1.1 may be absent.
J9 admits a child of such a row only through the class of section 9 and the
holders of LIP-0010 section 10 (J11), and since version 0.1.51 such a child is
admitted where it passes those checks.

## What is decided and what is proposed

The rows, the two ledgers and the coin of a row are Ivan Oparin's decision
of 2026-11-14 (J1), recorded in LIP-0014 section 9.1; the co-author agreed
to it on 2026-11-15. A further decision of the same day names
the key of the coin: a separate key, derived from the seed of the
operator's signer in an account of its own, as seal keys are derived. The
partitions for several executors and the charging of every link are text of
LIP-0008 sections 4 and 12.2. This LIP changes none of them.

| Decided, or text in force | Where | This profile |
| --- | --- | --- |
| A v4 row carries the executor as a service name with its pinned public key, the child's recipient in one of two modes, the limits of the row, the certifier and the coin. "The bytes come with v4" | LIP-0014 section 9.1 | States the same as facts that a parent signs, and adds that the coin is stated as an outpoint and a script (R1.1). No octets |
| The caps of the rows do not sum to more than the pool (J1.1) | The same | The same bound for each typed limit (R1.3) |
| The ordinal first, then the executor, the grantee and the budget of the child against its row, with four codes (J1.2) | The same | The same order and the same codes on the facts of v4 (section 2) |
| Two cumulative ledgers, the child's and the row's; one request identity is charged once; the row ledger draws on the pool only (J1.3) | The same | Section 5 names the accounts and says which of them a request debits |
| The coin is confirmed before the parent is signed and pays a separate key of the re-delegating side; the issuance of a child spends it in the transaction that carries the child's commitment; "the code is fixed with the v4 bytes" (J1.9) | The same | Section 3, with two codes |
| "Who funds the coin, and the account and the path of its key, are not fixed" | LIP-0014 section 9.1; the key registry, open points | Section 4, as a proposal that awaits the owners |
| A parent states its rows as groups: a template with coin ranges, and one ordinal across groups and ranges (J12, decided by Ivan Oparin, in force since version 0.1.51) | LIP-0014, "Decisions of 2026-11-15" | Section 8 |
| The recipient constraint of a row has a third form, a class of landlords each pinned like a notary, with four checks in a fixed order (J10, decided by Ivan Oparin, in force since version 0.1.51) | The same | Section 9 |
| A landlord lists the owner keys of the names of its agents and stations (J11, decided by Ivan Oparin, in force since version 0.1.51). Since version 0.1.53 the landlord's value pins by hash a holders list with one entry for each agent or station name: the name, the key that holds it and a revocation seal; the member `holders` of version 0.1.51 is the inline form of the transition | LIP-0010 section 10 | Section 9, checks (c) and (d) |
| A child needs an attestation only where its row names a certifier; a row without one is valid only where its recipient constraint is limited to the issuer's own landlord; across owners a certifier stays mandatory; a row without a certifier has no stop coin (J9, decided and agreed by both owners on 2026-11-15) | LIP-0014 section 8.3, rules J9.1 to J9.4 | Section 10 |
| Every applicable link is charged once for a request; independent executors need signed partitions and share no remainder | LIP-0008 sections 4 and 12.2 | Section 5 takes the row as the parent's link for a request under a child |

Every rule of this LIP is the draft's proposal, and neither owner has
decided one. Five points are more than a restatement of the decided text,
and the owners should look at them first:

1. "Confirmed before the parent is signed" becomes "confirmed at or below
   the parent's committed recent block" (R3.2). That is the one mark of the
   moment of signing that a verifier can read, and it is a little stricter
   than the decision.
2. For a request under a child, the link of the parent is the row. The
   parent's own limits are not charged (R5.4). This is the draft's reading
   where LIP-0008 section 12.2 and LIP-0014 section 9 meet.
3. The path of a row key, the account that holds it and the party that
   funds the coin (section 4).
4. Four codes: `ROW_COIN` and `ROW_COIN_REQUIRED` for the refusal that
   J1.9 leaves without a name, `ROW_COIN_IN_SEAL_TRANSACTION` for the rule
   of point 5, and `OWN_LIMIT_OVER` for the refusal of an own account,
   which J1.3 leaves without one.
5. The coin is no output of the seal transaction of the row's child
   (R3.4). The decision does not treat the case. LIP-0023 admits an anchor
   whose one input from the seal transaction is at once the linkage input
   and the input of the coin, and this profile refuses it, so that the two
   roles have two inputs. The script of the coin is a witness key hash
   (R3.1), which follows from LIP-0023, a draft itself.

Three further decisions are Ivan Oparin's of 2026-11-15. The co-author agreed
to J9 on the same day, so J9 is decided and agreed by both owners on
2026-11-15. J10 and J12 are in force since version 0.1.51, by Ivan Oparin's
decision of 2026-11-16 not to wait for the co-author; the co-author's answer is
folded in by amendment. They are recorded in LIP-0014, "Decisions of
2026-11-15", and each has one section of this LIP that opens with what the
decision says and marks what this draft adds.

| Decision | What it says | Section |
| --- | --- | --- |
| J12. Groups | A parent states its rows as groups. A group is a template with coin ranges. The template holds the executor, the recipient constraint, the limits of each child, and a certifier or none. A range is a transaction id, a first output index, a count and a script, and each coin of a range is one row. One ordinal runs across groups and ranges. In force since version 0.1.51 | 8 |
| J10. Landlord class | The recipient constraint of a row has a third form beside a key and a name: a list of landlords, each pinned like a notary. A child of such a row names its recipient by name, and the executor makes four checks in a fixed order, the last of which asks who wrote the value of that name. In force since version 0.1.51 | 9 |
| J9. No certifier inside one owner | A child needs an attestation only where its row names a certifier. A row without one is valid only where its recipient is limited to the issuer's own landlord. Across owners a certifier stays mandatory. Decided and agreed by both owners on 2026-11-15 | 10 |

The bounds of section 8, the refusal codes of sections 9 and 10, and every rule
that those sections mark as this draft's are proposals.

Nothing of this profile is implemented. The owners accept or change its
rules through this LIP, under LIP-0001.

### Owner decision proposals

**The in-force profile stays at version 0.1.51.** J9 to J12 and their decided
dependencies keep the classification in the public
[decision map](https://github.com/relux-works/swarma-chain-lab/blob/0f50d9151cfdb9d46cebacec0fa229788d73fc4f/experiments/grant-v4/identity/R1-DECISIONS-051.md).
The lead's relay of 2026-11-16 at 05:30Z requests the following proposals
([Decision 0004](../decisions/0004-reconciliation-closures.md)). None takes
effect before the owner's decision.

Under the in-force profile, whole-parent atomic refusal (R1.5, R8.7) and
whole-child composition remain unavailable. The profile checks fit only on
independently established selected facts and does not establish their signed
binding. One global ordinal is decided; its concrete traversal is proposed.
Each landlord requires an independently established checkpoint. The four
class checks keep their decided order, while the eight class strings remain
local diagnostics with no normative taxonomy or inner-step precedence.

The proposed bounds and witness range script, the landlord-value writer
check, holder ordering, the exact-name shortcut, the guarantee of not reading
an optional attestation, and the additional signer rules remain outside that
in-force subset. In-force exact-name recipients without a certifier run the
full decided class checks. These exclusions are unchanged by the proposals.

#### Q1. Whole-parent atomic refusal

**proposed, owner decision pending**

For whole-parent admission, the verifier MUST check the complete signed
parent against R8.1 to R8.3, R8.5, R8.6, R9.1, R10.1 and R10.2 before it
admits an own request or any child. The parent MUST contain at least one
group, each group at least one range, and the parent's encoded size MUST NOT
exceed 65536 octets. This byte bound replaces the group, range and coin count
caps proposed in R8.4. A failure anywhere refuses the whole parent under
R8.7, with no partial admission or reservation. The selected row's chain
reads remain those of R8.8; whole-parent refusal adds no chain read for an
unselected row. A landlord-class recipient remains valid under R9.1, and a
certifier remains optional only under R10.2. This text assigns no new code.

#### Q2. Ordinal-to-row mapping

**proposed, owner decision pending**

The verifier MUST use the traversal of R8.3 and the selection of R8.8 to
bind a child's ordinal to the signed group template, range and coin. It MUST
check the ordinal bounds before reading a row, then count groups and ranges
in their signed order and outputs in ascending index order, with the first
row at ordinal 1. The selection changes neither the template's recipient
constraint nor its certifier requirement. An out-of-range ordinal retains
`CHILD_ORDINAL`.

#### Q3. Class checkpoint derivation

**proposed, owner decision pending**

On v4 the verifier MUST derive every landlord-class checkpoint from the
parent's committed recent block, as R9.2 proposes, and use that block in the
history checks of R9.5. Neither the child nor its presenter may substitute
another checkpoint. This rule also supplies the checkpoint for the full
class checks of an exact-name recipient without a certifier under J9. It
adds no separately signed checkpoint member and leaves the other proposed
checks of section 9 at their existing status.

#### Q4. Normative class refusal codes

**proposed, owner decision pending**

The verifier MUST report the eight class refusal codes already assigned by
R9.4 to R9.9 and the finding-to-code table after R9.12, with the order of
R9.9. The recipient-name proof still precedes the class checks. This adopts
the class code taxonomy and its inner-step precedence only; the fifth step
of R9.5, the exact-name shortcut and the other explicitly proposed checks
remain outside the in-force subset until separately decided. A verifier
reports no code for a check that its profile does not perform. None of the
codes records a closure. The same taxonomy applies to decided class checks
for a row without a certifier; it adds no attestation requirement.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The checks of sections 1 to 3 and the accounting of section 5, as functions of stated facts | Yes | The owners' acceptance |
| A row as octets of a grant | Yes, since version 0.1.53 | LIP-0020 section 11 gives the members; the co-author's answer on it is pending |
| A reservation as an entry of a journal | No | The members of an invocation (LIP-0020) |
| The reads of the coin and of the anchor on a node | No | A run under LIP-0022 and LIP-0023 |
| The row account in a signer | No | The owners' choice of the account, and the custody of v4 accounts, which is open (LIP-0024 section 5) |
| An executor's ledger on a store | No | A store that is qualified under LIP-0014 J1.4; LIP-0025 proposes its form |
| The arithmetic of one kind of limit | No | The type profile of that kind (LIP-0008 section 2) |
| The checks of sections 8 to 10 as functions of stated facts and of the octets of name scripts and name values | Yes | The owners' acceptance of the rules that sections 8 to 10 mark as this draft's. J9 to J12 are in force: J9 agreed by both owners, J10 to J12 since version 0.1.51 on Ivan Oparin's decision, with the co-author's answer folded in by amendment |

## Motivation

A principal gives an agent a grant with an own budget of 50 and a pool of
100 for two workers: 60 at one service and 40 at another. Each worker
spends its share in full, and the agent spends its own 50 at a third
service. The principal signed 150, and that is what was spent. Two other
readings of the texts give other totals. LIP-0008 section 12.2 has all
direct and descendant consumption fit each ancestor's budget. If the
service of a worker reads that budget as the agent's own 50 and charges the
worker's request against it, the first worker stops at 50, and what the
agent itself spent elsewhere is invisible to that service anyway. If each
service keeps the pool of 100 as a counter of its own, each admits up to
100 across the documents of its row, and the two together admit 200.
LIP-0008 section 4 forbids the second, and LIP-0014 section 9 excludes the
first by keeping the own budget apart. Neither says which counter a service
keeps under which key.

The coin of a row has the same kind of gap. It makes one child for each row
visible to every verifier, on one condition: the key of the coin signs
nothing but the issuance of that row's child. Where the coin sits in an
account whose outputs a wallet may take as funding, an ordinary payment
spends it, and the row is void before any child exists. The decision gives
the key an account of its own and does not say which, or what the signer
checks before it signs.

## Current state

- LIP-0014 section 9.1 holds the decided rules J1.1 to J1.9 and lists as
  open who funds the coin and the account and the path of its key.
- LIP-0008 section 4 requires signed partitions for several executors and
  forbids one executor to borrow the remainder of another. Section 12.2
  charges a request once against every applicable link and limits a path
  to two links.
- The key registry describes the row coin key and says that its account and
  path are not fixed. The key map gives the funding account as
  `m/84'/7'/0'` and proposes a seal account of 10 or above.
- Draft LIP-0023 proposes the inputs of an anchor: exactly one input from
  the seal transaction, the linkage input, and every other input on a
  confirmed witness key hash. Draft LIP-0025 proposes the form of a journal
  that cannot go back unnoticed and leaves the entries of a row ledger to
  the rules that write them.
- The reference laboratory has no rows on v4. No Go file of
  `swarma-chain-lab` at `b03c6f10fad1be135e780d8b1f556fc46805eb06` holds
  one of the codes of J1.2 and J1.3.

## Proposal

The parent is called `P`, a child `C`, and the ordinal of the child's row
`k`. The anchor of a child is the transaction that carries its frame
(LIP-0023 C2.2).

### 1. The row of a v4 parent

A parent states for each row who may act under it, at which service, up to
which limits, who certifies the child, and which coin its issuance spends.

| Rule | Requirement |
| --- | --- |
| R1.1 | A row states five things: the executor, as a service name with its pinned public key; the recipient of the child, in exactly one of the two modes of LIP-0008 section 3.1; the limits of the row; the certifier, which is one of the notaries that the parent pins, or, under section 10 (J9), the statement that the row has none; and the coin, as an outpoint and a script. The ordinal of a row is its position among the rows of the parent, counted from 1. |
| R1.2 | A limit has a kind, a resource, a unit and an amount, and a period where its kind has one (LIP-0008 section 2). The key of a limit is all of these but the amount. No two limits of one row have the same key, and no two own limits of one grant have. |
| R1.3 | A parent states one pool amount for every key that one of its rows limits. For each key, the amounts of the rows do not sum to more than the pool, and the sum is an exact integer sum. |
| R1.4 | The coins of the rows of one parent are different outpoints, and none of them is the seal of the parent. |
| R1.5 | A parent that does not meet R1.1 to R1.4 or R3.1 is refused as a whole: it admits no child and no request of its own. The refusal is one of the members of the grant and gets its code with them. |

The code that R1.5 leaves to the members of the grant is `GRANT_DELEGATE`
(LIP-0020 W11.10), which also fixes the order in which a reader reports the
rules that it judges on the signed octets of a parent. That section does
not change R1.5 or its state.

The five things of R1.1 are the content that LIP-0014 section 9.1 decides
for a v4 row. The outpoint and the script of the coin are this draft's way
to state "the coin"; the script is what a principal compares before it
signs, and the outpoint is what a verifier reads.

Section 10.1 of LIP-0014 adds a sixth thing to a v4 row, the stop coin of
the row's notary (J2.7). This LIP does not treat it;
[LIP-0027](LIP-0027-row-stop.md) proposes its profile.

Sections 8 and 9 state J12 and J10, in force since version 0.1.51. Under
section 8 (J12) a parent states its rows in groups, and R1.1, R1.3 and R1.4 are
read as that section says. Under section 9 (J10) the recipient of R1.1 has a
third form. Section 10 holds J9, which both owners decided: the certifier of
R1.1 may be absent where R10.2 holds, and a child of such a row is admitted
only through the checks of section 9 (R10.2, R10.3).

A parent with a pool of 100 and rows of 60 and 40 is valid, and so is one
with rows of 60 and 30. Rows of 60 and 60 are not. Two rows may name the
same executor and the same recipient: each has its own ordinal, its own
limits and its own coin (LIP-0014 section 9.1, case S1-4).

### 2. A child fits its row

A verifier checks a child against the row of its ordinal on signed octets
alone, before it looks at the child's attestation.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| R2.1 | The ordinal that the child states lies between 1 and the number of rows of its parent. A verifier reads no row before it has checked this. | `CHILD_ORDINAL` |
| R2.2 | The child names the executor of its row: the same service name and the same pinned public key. | `CHILD_AGENT_NOT_ALLOWED` |
| R2.3 | The child names the recipient of its row: the same mode, and in that mode the same request key, or the same name with the same owner key. | `CHILD_GRANTEE_NOT_ALLOWED` |
| R2.4 | Every own limit of the child has the key of a limit of its row, and its amount is at most the amount of that limit. A child with a limit whose key the row does not have refuses with the same code, because it would add a resource. | `CHILD_BUDGET_OVER` |
| R2.5 | The checks stand in this order. They stand where LIP-0014 section 8 puts its steps V8 and V9: after the admission of the parent, and before the check of the child's attestation. | The first of the four |

These are the checks of J1.2 with its four codes, and R2.5 keeps the place
that LIP-0014 gives them: a child that widens its row refuses for the
widening, also when it carries a valid attestation. The names of the codes
say "agent", "grantee" and "budget", as the members of v3 do; on v4 they
report the executor, the recipient and a limit.

R2.4 compares ceilings. A kind whose amount is a floor and no ceiling, as
the required confirmation depth of LIP-0008 section 2, is no limit in the
sense of this rule. How the floor of a child stands to the floor of its row
is for the type profile of that kind.

A child that names the executor of another row of its parent refuses under
R2.2, also when every other member fits that other row. The ordinal selects
the row, and nothing in the child selects another one.

Under section 9 (J10, in force since version 0.1.51) R2.3 has a third
case: a child of a row whose recipient is a class names its recipient by name,
and four further checks on the verifier's node follow.

### 3. The coin of a row

The coin of a row is one output with a witness key hash script, confirmed
at or below the parent's recent block and outside the seal transaction of
the row's child, and the anchor of that child has an input that spends it.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| R3.1 | The script that a row states for its coin is a witness key hash: the octets `00 14` and 20 further octets. | The parent is refused (R1.5) |
| R3.2 | A verifier establishes on its own node, in the observation of the check (LIP-0022 section 1), that the transaction of the coin's outpoint has an output at the stated index with exactly the stated script, and that this transaction is confirmed on the active chain at a height that is not above the height of the parent's committed recent block (LIP-0022 section 4). | `ROW_COIN` |
| R3.3 | One input of the child's anchor spends the outpoint of the coin of the child's row. | `ROW_COIN_REQUIRED` |
| R3.4 | The coin of a child's row is no output of the child's seal transaction: the transaction id of the coin's outpoint differs from the transaction id of the seal outpoint that the child names. A verifier compares the two on the signed octets of the parent and of the child. | `ROW_COIN_IN_SEAL_TRANSACTION` |
| R3.5 | A verifier, a receipt and a report state that a child is the only child of its row for the active chain of the observation and for nothing wider (LIP-0014 J1.8). | None of its own |
| R3.6 | The input that spends the coin is an ordinary input of the anchor under LIP-0023: it has the form of C3.1, and it spends a confirmed output under C4.2. Under R3.4 it is another input than the linkage input. | The codes of LIP-0023 |

The decision asks for a coin that is confirmed before the parent is signed.
A verifier cannot read the moment of a signature. It can read the recent
block that the parent commits, which is the tip of the observation in which
the issuer made the checks of the issuance (LIP-0022 B4.1); on v4 it takes
the place of the checkpoint of LIP-0014 section 7.1. A coin at or below
that block was confirmed when the parent was signed, whichever block the
issuer committed: a grant cannot commit a block that did not exist yet.
R3.2 is a little stricter than the decision: a coin that was confirmed
after the committed block and before the signature refuses, and the parties
issue the parent again with a later recent block.

R3.3 needs no index of spent outputs. Two confirmed transactions of one
chain cannot spend one output, so a confirmed anchor that spends the coin
is its only spender. A second child of the row cannot show a confirmed
anchor with that input: its anchor spends something else and refuses under
R3.3. The same holds for a child of a row whose coin another transaction
spent before any issuance. That an anchor is confirmed is a rule of
LIP-0023 (C5.1).

R3.4 refuses a case that LIP-0023 admits. Take a transaction whose output 0
is the seal of the child and whose output 1 is a witness key hash. Output 1
is the linkage output of that seal (LIP-0023 C2.3). If the parent names the
same output as the coin of the row, one input of the anchor spends it and
fills both roles. LIP-0023 finds its one linkage input, R3.2 finds the
coin, and R3.3 finds it spent. Nothing then shows that the key of the row
took part beside the linkage key, because one signature stands for both.

The other places of a coin in the child's seal transaction lead nowhere
under LIP-0023, and its codes keep their meaning. Where the coin is a third
output, an anchor that spends it has two inputs from its seal transaction
and refuses there as `W_LINKAGE_REQUIRED`. Where the coin is the seal
itself, an anchor that spends it refuses there as `W_ISSUANCE_SPENDS_SEAL`.
So R3.4 refuses nothing that could have been issued except the one input
with two roles, and it does so by one comparison of two signed transaction
ids. With it the linkage input and the input of the coin are two inputs.
That the two outputs pay two keys is a rule for the signer (R4.1), and a
verifier does not see it. The cost falls on a re-delegating side that
prepares seals and coins ahead: it uses two transactions.

The exclusivity is that of the active chain. After a reorganisation that
removes an issuance, another child whose anchor spends the coin on the new
chain is admitted there. LIP-0014 accepts this boundary with the decision,
and the vectors record it (case S1-K2).

The coin shows that the holder of its key took part in the issuance. It
does not show who that holder is: a verifier reads a script.

### 4. The row account of the signer

The key of a row's coin comes from an account of the signer that holds row
keys and nothing else, and the signer signs one kind of input with it: the
input that spends the coin in the anchor of that row's child.

These are rules for the re-delegating side. A verifier cannot observe them
and refuses nothing for them, as it refuses nothing for the path of a seal
key (LIP-0008 section 11.1, rule 4).

| Rule | Requirement |
| --- | --- |
| R4.1 | Under the Witness profile on Namecoin a row key has the path `m/84'/7'/<row-account>'/0/<i>`, the layout of a seal key (LIP-0008 section 11.1). `<row-account>` is a hardened account index of 10 or above that is no seal account of the same seed. The account holds row keys alone: no seal key, no linkage key, no funding key and no key of a name. |
| R4.2 | The public descriptor of the row account is the witness key hash descriptor of its extended public key at `/0/*`. The signer alone holds the extended private key. The operator's watch-only node MAY hold the descriptor, and it is not published. |
| R4.3 | One index `<i>` serves one row. The signer records the index durably before it gives out the address, and it records the outpoint of the coin, the parent and the ordinal as each becomes known. An index is not used for a second coin. |
| R4.4 | The operator of the re-delegating side funds the coin from its funding account, in a transaction of its own, before the parent is signed. The amount of the coin carries no meaning. |
| R4.5 | The signer signs with a row key one kind of input: the input that spends the recorded coin of a row, in a transaction whose one `OP_RETURN` output carries the frame of a child of that row. The signer computes the commitment of the frame itself, from the signed preparation of the child, and it checks that the child names the recorded parent and the recorded ordinal. The signature has the hash type `01`. The signer signs no digest that it did not compute from the whole transaction. |
| R4.6 | A row key signs no other input, and no other key signs the input that spends a row's coin. The key of a coin is neither the delegation key nor the messaging key (J1.9), and the delegation key signs child grants and no transaction (LIP-0014 section 9.1). |
| R4.7 | The signer signs an input of an anchor only after it has checked the whole transaction under R4.5, and it releases a signature for that exact transaction and no other. |

The path follows the words of the decision, "as seal keys are derived". The
floor of 10 is the floor that the key map proposes for seal accounts; it
keeps the account away from the funding account `m/84'/7'/0'` and from the
low indices of a wallet. Which index a deployment takes is for its signer's
configuration, and the owners may fix one.

The layout has the weakness that LIP-0008 section 11.1 names for the seal
account. The indices below the account are not hardened, so the extended
public key together with one row private key gives every row key of the
account. That is why R4.2 keeps the descriptor out of publication. A party
with every row key can spend the coins and so void rows that have no child
yet. It can issue nothing: a child needs the delegation key and an
attestation.

R4.5 is the rule that keeps a coin for its row. The hash type `01` commits
to every input and every output of the anchor (LIP-0023 section 3), so the
signature of the row key covers the frame, and with it the one child that
the anchor issues. A signer that signed the coin's input in any other
transaction would spend the coin without an issuance.

An anchor of a child has inputs of up to three kinds: the linkage input of
LIP-0023, the input that spends the row's coin, and funding inputs. Each is
signed by the key of its own account. Which party holds the linkage key of
a child's seal transaction follows from who creates the seal of a child,
and that is open (LIP-0014 section 11.1). Where two parties sign inputs of
one anchor, R4.7 holds for each of them, and the hash type `01` makes a
change of the transaction void every signature.

How a v4 account is created, wrapped and recovered is open for the seal
account (LIP-0024 section 5). The same question holds for the row account,
and this LIP proposes nothing for it.

Under section 8 (J12, in force since version 0.1.51) every coin of a
range has one script, so one index of the row account serves one range, and
R4.3 is read as R8.9 says.

### 5. The accounts of an executor's ledger

A request under a child debits two accounts at the child's executor, the
child's own and the row's, and it debits no account of the parent's own
limits.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| R5.1 | An account is a cumulative amount in the ledger of one executor, with a key and a ceiling. It begins at 0 with its first reservation, and nothing in this profile lowers it. | |
| R5.2 | An own account has the key: `own`, the identifier of a grant, and the key of one own limit of that grant. Its ceiling is the amount of that limit. A row account has the key: `row`, the identifier of a parent, an ordinal, and the key of one limit of that row. Its ceiling is the amount of that limit. The identifier of a grant is that of LIP-0020 section 6. Keys that differ in any part are different accounts. A limit key for which a grant or a row states no limit has the ceiling 0. | |
| R5.3 | A request under a grant that is no child debits, for each limit key that its action consumes, the own account of that grant. | |
| R5.4 | A request under a child debits, for each limit key that its action consumes, two accounts: the own account of the child, and the row account of its parent and its ordinal. It debits no own account of the parent. | |
| R5.5 | The pool of a parent is no account. No executor holds a remainder of a pool, and what one row leaves unused is available to no other row. | |
| R5.6 | An executor reserves all debits of one request in one atomic write of its journal, or none of them. It takes the limit keys in the order in which the request consumes them, and for each key the own account before the row account, and it reports the first account whose ceiling the reservation would exceed. | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` |
| R5.7 | One request identity holds at most one reservation in a ledger. A request whose identity already holds one is not charged again, with whichever document of the row, proof path or attestation it is presented. | |
| R5.8 | A revocation of the child, a withdrawn attestation, a second document of the row, a reissue, a restart and an effect whose outcome is unknown lower no account. Whether a reservation is released after a reconciled outcome is a rule of the type profile of its limit. | |
| R5.9 | The exposure that a principal signs with a parent is, for each limit key, the amount of the parent's own limit plus the pool. Executors can admit at most the own limit plus the sum of the rows. | |

R5.4 is the draft's reading of two texts. LIP-0008 section 12.2 has the
executor reserve a request "against every applicable link" and says in the
same place that one chain uses one executor and that independent executors
need the signed partitions of section 4. A row is such a partition: it is
what the parent's link assigns to the executor of the child. The parent's
own limit is another partition, that of the parent's own executor. The
executor of a child cannot read the journal of the parent's executor, so it
could not charge the parent's own account if a rule asked for it, and
LIP-0014 section 9 says that the row ledger draws on the pool only.

The rule holds also where the parent and a child name the same service.
That service keeps the own account of the parent and the row account under
different keys, and a request of the child moves the second.

Two documents of one row have two own accounts and share the row account.
Under a row of 60, 30 spent under the first document and 30 under the
second fill the row, and one atom more under either refuses as
`ROW_CAP_OVER` and leaves both own accounts as they were (LIP-0014, case
S1-3).

An account lives in a journal of the form that LIP-0025 proposes, and the
effect follows the write to the outside record (LIP-0025 M3.2). After a
recovery by starting anew, every row account that could have had a record
counts as full (LIP-0025 section 7). The octets of a reservation entry and
the key that identifies a request come with the members of the grant and of
the invocation (LIP-0020 section 6); the vectors state both as facts.

### 6. Refusals and their order

| Code | What it reports | Rule | Name |
| --- | --- | --- | --- |
| `CHILD_ORDINAL` | The ordinal of the child is 0 or above the number of rows | R2.1 | LIP-0014 J1.2 |
| `CHILD_AGENT_NOT_ALLOWED` | The child names another executor than its row | R2.2 | LIP-0014 J1.2 |
| `CHILD_GRANTEE_NOT_ALLOWED` | The child names another recipient than its row | R2.3 | LIP-0014 J1.2 |
| `CHILD_BUDGET_OVER` | A limit of the child is above the limit of its row, or has a key that the row does not have | R2.4 | LIP-0014 J1.2 |
| `ROW_COIN_IN_SEAL_TRANSACTION` | The coin of the child's row is an output of the child's seal transaction | R3.4 | New |
| `ROW_COIN` | The coin of the row is not on the active chain as the row states it, or is confirmed above the parent's recent block | R3.2 | New |
| `ROW_COIN_REQUIRED` | No input of the child's anchor spends the coin of its row | R3.3 | New |
| `OWN_LIMIT_OVER` | A reservation would exceed an own account | R5.6 | New |
| `ROW_CAP_OVER` | A reservation would exceed a row account | R5.6 | LIP-0014 J1.3 |

R6.1. At the admission of a child, the four checks of section 2 stand in
their order, at the place that R2.5 names. The three checks of the coin
stand after the checks of LIP-0023 on the child's seal transaction and
anchor, in this order: `ROW_COIN_IN_SEAL_TRANSACTION`, then `ROW_COIN`,
then `ROW_COIN_REQUIRED`. A child that LIP-0023 refuses gets the code of
LIP-0023, and no code of that LIP changes its meaning. Where the three
stand relative to the checks of the child's attestation comes with the
profile of the attestation.

R6.2. At a reservation, the order is that of R5.6. A request that is
refused reserves nothing.

None of these refusals records a closure.

Sections 9 and 10 propose eight further codes for the checks of a landlord
class, with their order (R9.9). They belong to Draft text that awaits the
co-author's agreement.

### 7. Vectors

[`vectors/LIP-0026/rows-vectors.json`](../vectors/LIP-0026/rows-vectors.json)
holds 64 vectors over the 34 rules of this LIP, as decisions on stated
facts. No vector holds a grant, a transaction or an entry of a journal.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `parents` | 4 valid, 9 refused | Section 1 and R3.1 on the stated rows and pools of a parent |
| `fit` | 4 passing, 11 refused, 3 compound | Section 2 on a parent and a child, with the order of R2.5 for a child that has two defects |
| `coins` | 4 passing, 11 refused, 5 compound | Section 3 in the order of R6.1, on a row's coin, on the seal that the child names, on what a node gives for the coin, and on the inputs of the child's anchor. Two outcomes are codes of LIP-0023, for an anchor that it refuses before this profile is asked |
| `ledgers` | 13 traces | Section 5 as a state machine: grants, executors, and a list of requests with the expected outcome of each and the accounts at the end |

A vector of the first three groups whose outcome is not the passing one
holds one defect, states the expected outcome and names a neighbour with
the passing outcome that differs from it in that defect. A vector marked
compound holds two defects, states the one that the order reports and names
no neighbour. A trace states the outcome of each of its requests and names
no neighbour.

Two traces show the accounting across executors and inside one ledger.
`ledger-01` runs one parent with an own limit of 50 and rows of 60 and 40
over three executors, and ends with 150 reserved and nothing above a
ceiling. `ledger-02` runs direct requests of the parent beside the requests
of two siblings in one ledger, each up to its ceiling.

`coin-16` is the one input with two roles: the output after the child's
seal is also the coin of the row, and the anchor spends it once. LIP-0023
admits that anchor, and R3.4 refuses the child. Its control is `coin-18`,
with the coin in another transaction and two inputs for the two roles.

The limits of the file are these. Identifiers, keys, transaction ids and
scripts are placeholders. A trace runs its requests one after another: no
vector holds two writers at one moment. Where two requests compete for the
last amount of an account, two traces state the two orders. No vector holds
a limit with a period. The refusal of a parent has no code, because R1.5
names none.

No checker for these vectors is in this repository. The expected outcomes
were stated by hand, computed by one implementation and decided again by a
second one that shares no code with the first; neither is published here.
Both come from the author of this text, so an error of understanding that
they share is in the vectors. The vectors bind nothing until both owners
accept the rules that they follow.

### 8. Groups of rows (J12)

**In force since version 0.1.51: J12.** Ivan Oparin decided on 2026-11-15 that
a parent states its rows as groups. On 2026-11-16 Ivan Oparin put the decision
in force without waiting for the co-author's agreement, which has not been
given; the co-author's answer is folded in by amendment. Section 1 is read as
R8.1 to R8.3 say.

A parent that permits 10,000 children states, under section 1, 10,000 rows, and
most of them differ in nothing but their coin. The owner named 10,000 agents as
the scale to reach. Under the decision the parent states what such rows share
once, and states their coins as ranges.

The decision says this. A group is a template with coin ranges. The template
holds the executor, the recipient constraint, the limits of each child, and a
certifier or none. A range is a transaction id, a first output index, a count
and a script. Each coin of a range is one row, and one ordinal runs across
groups and ranges, so that the ordinal of a child keeps its meaning. For each
limit key the pool bounds the sum, over the groups, of the count times the
amount of the template, and a key that no row limits has no pool. Coins are
distinct, ranges do not overlap, no coin is the seal of the parent, and every
coin is confirmed at or below the recent block of the parent. A verifier checks
only the group and the range of its child, on signed octets.

The decision names the numbers of R8.4 as proposed bounds. This draft adds the
order of the count in R8.3, the witness key hash of R8.2, which follows R3.1,
and the rules R8.9 and R8.10 for the two signers.

| Rule | Requirement |
| --- | --- |
| R8.1 | A parent states its rows as a list of groups. A group has one template and a list of ranges. The template states four things: the executor, as R1.1 states it; the recipient constraint (section 9); the limits of each row of the group, under R1.2; and the certifier of the rows of the group, or that they have none (section 10). |
| R8.2 | A range states a transaction id, a first output index, a count of at least 1 and a script. Its coins are the outputs of that transaction from the first index on, as many as the count, and the script of each of them is the script of the range. The index of the last coin is at most 4294967295. The script is a witness key hash, as R3.1 asks of a coin. |
| R8.3 | Each coin of a range is one row, with the template of its group. The rows of a parent are counted group by group in the order of the groups, inside a group range by range in the order of the ranges, and inside a range by ascending output index. The ordinal of a row is its position in that count, from 1. The number of rows of a parent is the sum of the counts of all its ranges. |
| R8.4 | Proposed bounds: a parent has at least one and at most 16 groups, a group at least one and at most 16 ranges, and a range at most 4096 coins. The largest size of a parent is 65536 octets. |
| R8.5 | A parent states one pool amount for every limit key that a template limits. For each key, the sum over the groups of the number of rows of the group times the amount of its template for that key is at most the pool, and the sum is an exact integer sum. A key that no template limits has no pool. |
| R8.6 | No coin belongs to two rows: two ranges of one parent that state the same transaction id have index intervals that do not meet. No coin is the seal of the parent. |
| R8.7 | A parent that does not meet R8.1 to R8.6, R9.1, R10.1 or R10.2 is refused as a whole, as R1.5 says: it admits no child and no request of its own. |
| R8.8 | A verifier of a child checks the ordinal of the child against the number of rows (R2.1) and finds the group, the range and the coin of that ordinal from the counts that the parent signs. It reads no fact of a chain for another row. Sections 2 and 3 then apply to the template of that group and to that coin: R3.2 reads the transaction of the range and its output at the index of the coin, with the script of the range. |
| R8.9 | One index of the row account (R4.1) serves one range: every coin of the range pays the key of that index. The signer records the range durably before it gives out the address, and for each coin its outpoint, the parent and the ordinal as each becomes known. It signs the input of each coin once, under R4.5. An index is not used for a second range. |
| R8.10 | Before it signs a parent, the signer of the issuer establishes for every coin of every range what R3.2 asks, so that it signs no parent with a row that can never have a child. A verifier does not see this. |

Take a parent with two groups. The first has ranges of three and of two coins,
the second one range of four. The parent has nine rows. The ordinals 1 to 3 are
the coins of the first range in the order of their output indices, 4 and 5
those of the second, and 6 to 9 those of the second group. A child with the
ordinal 5 is checked against the template of the first group and against the
second coin of its second range, and a child with the ordinal 10 refuses as
`CHILD_ORDINAL` before any row is read.

The pool of R8.5 is the pool of R1.3 with the rows of a group counted together.
Two groups whose templates limit one key to 60 and to 40, with two rows and one
row, need a pool of at least 160 for that key. A template may state no limit at
all. Its rows then draw on no pool, and a request under their children that
consumes a countable resource meets a ceiling of 0 (R5.2).

Under the bounds of R8.4 a parent has at most 256 ranges and at most 1,048,576
rows, and a verifier finds a row by adding at most 256 counts. The largest size
of 65536 octets is a number for LIP-0020, which gets it when the grant gets its
members. No octets of a group are defined here; since version 0.1.53 LIP-0020
section 11 defines them.

The number of coins that one transaction creates has a bound outside this
profile. Namecoin Core relays a transaction of at most 400,000 weight units. A
transaction with one witness key hash input and `n` witness key hash outputs
weighs `322 + 124 n` units from 253 outputs on, so it holds at most 3223
outputs. One funding transaction of the standard size therefore gives a range
of at most 3223 coins, or 3222 beside an output for change, and 10,000 rows
need four such transactions and at least four ranges. The bound of 4096 is
above what one standard transaction holds.

The rows of a parent are fixed when it is signed. A further coin is a further
row and needs a new parent, which is an ordinary issuance with its cost on the
chain. A re-delegating side therefore reserves coins with headroom. A row that
is never used costs its coin and nothing else.

R8.9 gives up a separation that R4.3 has. With one key for each row, a leaked
row key can void one row. With one key for a range, the holder of that key can
spend every coin of the range that no child has spent yet, and void all those
rows. It still issues nothing: a child needs the delegation key and, where the
row has a certifier, an attestation.

Three points were open under this section until version 0.1.53. LIP-0020
section 11 answers them in the octets of the grant, and one of them stays
open as a question of this LIP:

- **The bounds.** The four numbers of R8.4 are proposals of this LIP, and
  neither owner has fixed one here. LIP-0020 W11.6 takes them as bounds of
  the member schema of `swarma-grant/4`: a document with more than 16
  groups, with more than 16 ranges in a group, with more than 4096 coins in
  a range or with more than 65536 octets is no well-formed grant. Proposal
  Q1 of this LIP, which would keep the size alone, is not decided by that.
  If the owner accepts it, the three counts leave the schema by amendment.
- **The stop coins of a group.** LIP-0014 section 10.1 (J2.7) and LIP-0027
  give each row with a certifier a stop coin of its own. The decision on
  groups names no place for them. LIP-0020 W11.6 places them: a range of a
  group whose template names a certifier states a run of stop coins beside
  its coins, one for each coin, as a transaction id, a first index and a
  script. No owner has decided that place.
- **The octets** of a group, of a template and of a range are LIP-0020
  W11.5 to W11.7. A template states its certifier by one of two members,
  `certifier` or `no_certifier`, and never by leaving a member out
  (W11.7).

### 9. The landlord class (J10)

**In force since version 0.1.51: J10.** Ivan Oparin decided on 2026-11-15
that the recipient constraint of a row gains a third form beside a key and a
name: a class of landlords. On 2026-11-16 Ivan Oparin put the decision in force
without waiting for the co-author's agreement, which has not been given; the
co-author's answer is folded in by amendment.

A row that names a key or a name fixes one party at the moment at which the
parent is signed. A principal that runs a swarm starts agents after that
moment, and their names do not exist yet when the parent is signed. A class
says instead whose agent the recipient must be.

The decision says this. A class is a list of landlords, each pinned like a
notary under LIP-0014 section 7.1: by name, registration and owner key, with a
checkpoint. A child of such a row names its recipient by name and never by key.
The executor then checks four things in this order. (a) The current value of
the recipient name is an agent binding whose landlord is in the list of the
row. (b) That landlord is live, its registration and its owner are the pinned
ones, its history from the checkpoint shows no change of owner, a transfer and
a return included, and it has no pending name operation. (c) The current owner
of the recipient name is one of the holders that the landlord's current value
lists (LIP-0010 section 10; since version 0.1.53 the value pins by hash a
list that names the recipient name with that holder, and the seal of that
entry is confirmed, unspent and not closed in the verifier's journal). (d) The name operation that wrote the current
value of the recipient name spent a name output that a holder owned. The
decision asks that the refusal codes be proposed in this draft and named as
proposals.

Check (d) answers an attack on the first three. Anybody can send the output of
a name to any address, and the receiver signs nothing. An attacker registers a
name, writes into its value an agent binding that points to the landlord
together with a channel key of its own, and sends the output to the address of
a holder. The value points to the landlord, the landlord is untouched, and the
current owner of the name is a holder: (a), (b) and (c) pass, and the
attacker's channel key would sign requests as an agent of that landlord. The
operation that wrote the value spent an output of the attacker, so (d) refuses.
A value passes only where a holder wrote it.

This draft adds four things to the decision: that the checkpoint of a class on
v4 is the recent block of the parent (R9.2); that the current value of the
landlord, which carries the holders, was written by the pinned owner (the
fifth step of R9.5), as LIP-0014 J3.4 asks of a notary's value; the eight
codes and their order; and the rules R9.11 and R9.12 for the two signers.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| R9.1 | The recipient constraint of a template has exactly one of three forms: a request key; a name with its owner key; or a class. A class is a list of at least one landlord. For each landlord it states the exact name, the registration of that name as a transaction id and an output index, and the owner key as an owner pin (LIP-0021 O2.1). No two entries of one class state the same name. | The parent is refused (R8.7) |
| R9.2 | The checkpoint of a class is the committed recent block of the parent (LIP-0022 section 4). | |
| R9.3 | A child of a row whose recipient is a class names its recipient in the mode "by name" of LIP-0008 section 3.1: an exact name and the owner key of that name. | A child that names a request key: `CHILD_GRANTEE_NOT_ALLOWED` |
| R9.4 | Check (a). The current value of the recipient name parses under LIP-0010 as an agent binding, and its `landlord` is, octet for octet, the name of one landlord of the class. That landlord is called `L`. | `CLASS_LANDLORD` |
| R9.5 | Check (b), in six steps. `L` is live at the tip of the observation (LIP-0021 O5.1). The walk of `L` ends at the pinned registration (O6.1). That registration is confirmed at or below the checkpoint. Every output of `L` from the one that was current at the checkpoint to the current one reads as controlled by the pinned owner key (O3.4, O6.2). The value of the current output of `L` was written by the pinned owner (O4.4). The reading node holds no pending transaction that spends the current output of `L`. | The table below |
| R9.6 | Check (c). The current output of the recipient name reads as controlled (O3.4) by a holder of `L`. For a value of `L` that pins a holders list, the verifier makes steps 0 to 8 of LIP-0010 section 10.6: its holder journal, the pin, the rollback check against the journaled head, the list under its hash, the entry that names the recipient name and that no taken list removed, the control of the current output by the key of that entry, and the seal of that entry, which is confirmed on the active chain as LIP-0010 H46 asks, is bound to that entry alone, has no journaled closure and is unspent with the mempool included. The verifier makes the read of the seal again before the effect (LIP-0010 H44). A name that no entry names does not pass, whoever holds it. For a value of `L` in the inline form of version 0.1.51 the holders are the pins of its member `holders`, and every name that one of them controls passes (LIP-0010 section 10.9), unless the verifier ever took a pinned list for `L`: it then reads the inline form of `L` no more (LIP-0010 H42). | `CLASS_HOLDER`; for the journal, the pin, the list, the seal and the form, the codes of LIP-0010 section 10.6. A seal read that proves nothing refuses under R9.8 and is never reported as a revocation |
| R9.7 | Check (d). The value of the current output of the recipient name was written by a holder of `L`: the check of LIP-0021 section 4 gives "written by the owner" for the key of the entry of R9.6 (LIP-0010 section 10.6, step 9). In the inline form of version 0.1.51 it gives it for one pin of the member `holders`, and that holder need not be the holder of R9.6. | `CLASS_WRITER` |
| R9.8 | Where a read of R9.4 to R9.7 proves nothing, the verifier refuses, and the refusal is no evidence about either name. That is so for a node that does not supply a fact (O1.3), an unsupported script (O3.5), an unsupported writer check (O4.4), and a walk that is incomplete or bounded (O6.3). | `CLASS_HISTORY_UNAVAILABLE` |
| R9.9 | The four checks stand in the order (a), (b), (c), (d), and the six steps of (b) in the order of R9.5. The first step that fails, or that proves nothing, gives the refusal. The checks stand after the proof of the child's recipient by name (LIP-0021 section 7.2) and before the checks of the coin (R6.1). | The first that applies |
| R9.10 | Every read of the four checks belongs to the observation of the admission (LIP-0022 section 1). The request key of the child is the key that the value of R9.7 yields for the channel (LIP-0008 section 3.1), so that the key which signs a request comes from the value whose writer was checked. | |
| R9.11 | A holder key signs a name operation only for a name that its signer registered itself, or that its operator accepted by a decision of its own. It does not update or renew a name for the one reason that the output of the name pays its address. | None at a verifier |
| R9.12 | Before it signs a parent, the signer of the issuer makes the steps of R9.5 for every landlord of every class, so that it signs no parent under which every child of a row refuses. | None at a verifier |

The six steps of check (b) give these refusals:

| Finding | Refusal |
| --- | --- |
| `L` has no live output at the tip; the walk ended at another registration; an output of the stretch from the checkpoint reads as another key | `CLASS_LANDLORD_CHANGED` |
| The pinned registration is confirmed above the checkpoint, so that `L` had no output of that registration at the checkpoint | `CLASS_CHECKPOINT` |
| The writer check of the current output of `L` gives "written by another" | `CLASS_VALUE_UNAUTHORIZED` |
| A pending transaction spends the current output of `L` | `CLASS_LANDLORD_PENDING` |
| Nothing was proved at a step | `CLASS_HISTORY_UNAVAILABLE` |

Check (b) is the rule of a notary's name with two differences. It asks nothing
about the octets of the `swarma` member, because the list of holders changes
while the class stands, as a notary's attestation key does (LIP-0014 J3.3);
since version 0.1.53 the list is outside that member altogether (LIP-0010
section 10.4). And
it refuses while a name operation of `L` is pending, because that operation may
remove the very holder that checks (c) and (d) are about to accept. A transfer
of `L` to another key and back leaves an output of the stretch that reads as
another key, and the class refuses `L` from then on.

By the proof of LIP-0021 section 7.2 the current output of the recipient name
is controlled by the owner key that the child signs. Check (c) therefore asks
whether that key is a holder. A recipient whose name is held by a key that the
landlord does not list refuses, also when its value points to the landlord.
That proof has refusals of its own, and they come first (R9.9). A current
output that reads as another key than the one that the child signs refuses as
`RECIPIENT_NAME_NOT_HELD`, and one whose script is unsupported as
`RECIPIENT_NAME_UNAVAILABLE` (LIP-0021 O7.2). No check of the class is reached
for such a child, and the two codes keep the meaning that LIP-0021 gives them.

Checks (c) and (d) read one list: the holders of `L`, the landlord that the
value of the recipient name points to. Since version 0.1.53 they read one
entry of it, the entry that names the recipient name (LIP-0010 section
10.6). In a class of several landlords a holder
of another landlord of the class is no holder for this name. It can neither
hold the name nor have written its value, so a holder of one listed landlord
cannot make an agent of another.

Check (d) looks at one operation, the one that created the current output of
the recipient name. For an update, the name input is the previous output of the
name; for a registration, it is the output of the reservation (O4.1). The check
does not trace a value back through the history of the name. A holder that
registers a name and writes its value passes. A holder that received a name
passes only after an operation of its own, which may repeat the value
unchanged.

That last case is the limit of check (d), and R9.11 is the rule for it. A
holder that updates or renews a name which an attacker sent to it writes the
attacker's value under its own signature, and (d) then passes. A wallet that
renews every name whose output pays its addresses does exactly this. No
verifier can tell such an update from a deliberate one, so the rule binds the
holder's signer, as R4.5 binds the signer of a row key.

Four further limits hold:

- **A stolen holder key** passes all four checks for every listed name that
  it holds, with whatever channel key the thief writes. A keeper of the
  landlord's prepared spends broadcasts the spend of the seal of every entry
  with that key (LIP-0010 section 10.7, H35), and from the moment at which
  a verifier validates a spend on its own node the name of that entry
  refuses there as `HOLDER_REVOKED`, with no name update. A verifier that
  cannot validate the spend refuses as `HOLDER_SEAL_NOT_LIVE` while its
  view shows the seal not unspent, and records nothing (LIP-0010 H31, H50).
  The owner of the landlord name
  completes it with a list that drops the entries, and from the block that
  confirms that update the names refuse as `CLASS_HOLDER` at every verifier
  that takes that list. Dropping the entries alone is no answer to the
  theft (LIP-0010 H41). A landlord in the inline
  form of version 0.1.51 has the update alone. Neither act ends a grant,
  and the names stay with the thief; one agent's own grant is ended by that
  grant's seal.
- **The class says whose agent a recipient is.** It does not say which
  agent: every name that the holders list of a listed landlord names, and
  that the key of its entry holds and wrote, fits the row (in the inline
  form of version 0.1.51, every name that a holder holds and wrote). Which of them receives the child is the delegator's choice, and a
  second child of the row is excluded by the coin (section 3) and not by the
  class.
- **A pending operation of the recipient name** is not read. The value in
  force is the confirmed one, and a pending change of the channel key takes
  effect with its block.
- **The number of landlords of a class** has no bound here. The decision
  names none, and the largest size of the parent (R8.4) is the only limit.

### 10. Rows without a certifier (J9)

**Decided and agreed by both owners on 2026-11-15: J9.** Ivan Oparin decided
on 2026-11-15 that a child needs an attestation only where its row names a
certifier, and that a row may be without one only inside one owner. The
co-author agreed on 2026-11-15. The decision is text in force; LIP-0014
section 8.3 states it as the rules J9.1 to J9.4.

A principal whose own agents hand work to each other pays, under D1, a notary's
attestation, anchor and seal for every child, although the notary is its own
and the recipient is its own agent.

The decision says this. The right of re-delegation of the parent MUST state
for each row whether a child of it needs an attestation: it does where the row
names a certifier. The principal signs the parent, so a delegator cannot drop a
certifier. A row without a certifier MUST have a recipient constraint that is
limited to the issuer's own landlord: either a class with exactly the issuer's
landlord, or an exact name that passes the landlord and holder checks of
section 9 against the issuer's landlord. Across owners a certifier stays
mandatory, as D8 of LIP-0014 says. The stop coin of LIP-0027 belongs only to
rows with a certifier.

Both recipient constraints of the decision rest on J10 and J11. The class is
the form of section 9 (J10), and the landlord and holder checks of an exact
name are checks of section 9 that read the holders list of LIP-0010 section
10 (J11). Until version 0.1.51 neither was in force, and no child of a row
without a certifier was admitted. Since that version both are in force, by
Ivan Oparin's decision of 2026-11-16 not to wait for the co-author: a child of
a row without a certifier is admitted where its recipient passes the checks of
section 9 for a class, or of R10.3 for an exact name, and it needs no
attestation. That admission rests on J9, which both owners agreed, and on J10
and J11, which the co-author has not yet answered; the co-author's answer is
folded in by amendment. Section 8 (J12) does not bear on the decision: R10.1
and R10.2 apply to the template of each group, and so to each of its rows.

The owner's practice, which is no rule of this profile: a certifier for rows
whose children permit effects, such as payments, the use of a model and
landings, and none for rows whose children permit instructions and reviews.

This draft adds two things to the decision. The first is the split of check (b)
in R10.3. The four steps that the admission of the parent has made for the
issuer's name are not made again; the fifth and the sixth are made, so that the
class of the issuer's landlord and an exact name decide alike on the same
facts. The fifth is no repetition, because the issuer rule in force does not
ask who wrote the issuer's value (LIP-0021 section 4.1). Its cost is the one
that LIP-0021 states there: a landlord whose name another party registered for
it or transferred to it signs one update before its holders count. The second
addition is that a verifier does not read an attestation that is presented for
a child of a row without a certifier (R10.4).

| Rule | Requirement | Refusal |
| --- | --- | --- |
| R10.1 | A row states its certifier, which is one of the notaries that the parent pins, or states that it has none. Under section 8 (J12) a template states this for the rows of its group. A parent none of whose rows names a certifier need pin no notary. | A certifier that the parent does not pin: the parent is refused (R1.5; under section 8, R8.7) |
| R10.2 | A row without a certifier has one of two recipient constraints. The first is a class with exactly one landlord, whose name, registration and owner key are those that the parent binds for its issuer (LIP-0008 section 3). The second is a name with its owner key. A row without a certifier whose recipient is a request key, a class with two or more landlords, or a class whose one landlord is not the issuer makes the parent refused. Under section 8 the same holds for a template without a certifier. | The parent is refused as a whole, as R1.5 says (under section 8, R8.7) |
| R10.3 | For a child of a row without a certifier whose recipient is a name, the verifier makes the checks (a), (c) and (d) of section 9 for that name with the issuer of the parent as the landlord `L`, and the fifth and the sixth step of check (b): the writer of the current value of `L`, and the pending read. The first four steps of (b) are met by the admission of the parent, which judged the issuer's name under LIP-0008 section 3 with the same registration, owner key and recent block (LIP-0021 section 7.1). | The codes of section 9, in the order of R9.9 |
| R10.4 | A child of a row without a certifier needs no attestation. The verifier makes no check of an attestation for it and reads none that is presented. A child of a row with a certifier is certified as LIP-0014 says. | |
| R10.5 | A row without a certifier states no stop coin, and no rule of LIP-0027 applies to it. | |

R10.1, R10.2, the first sentence of R10.4 and R10.5 state the decision on the
facts of a row. R10.3 and the second sentence of R10.4 are the two additions
of this draft named above and stay proposals, and so do the codes of section 9
that R10.3 gives.

D8 of LIP-0014 speaks of an issuer and a delegator that have one owner and does
not say how a verifier tells. R10.2 and R10.3 give the recipient of the child a
test that a verifier makes on its own node: the name is an agent of the
issuer's landlord, a holder of that landlord holds it, and a holder wrote its
value. A class with the one landlord of the issuer admits every such name. An
exact name admits one, and it is checked in the same way, so that a name of
another owner cannot stand in a row without a certifier.

The issuer's own rule is stricter than check (b). It asks that the `swarma`
member of the issuer's name is unchanged from the recent block of the parent on
(LIP-0008 section 3). Since version 0.1.53 the holders are no part of that
member: the issuer's value pins its holders list outside `swarma` (LIP-0010
section 10.4, H13). For a row whose landlord is the issuer the list of holders
is therefore the list that the issuer's current value pins at each admission,
as for every other landlord of a class, and an update that changes it refuses
neither the parent nor a child of it. Only for an issuer in the inline form of
version 0.1.51, whose `swarma` carries the holders, is the list still the one
at the recent block of the parent, and an update that changes it refuses the
parent and every child of it (LIP-0010 section 10.9, rule 7).

Three limits hold:

- **The test is on the recipient of the child.** It does not look at the
  owner of the delegator, the recipient of the parent. A parent that a
  principal issues to an agent of another owner may hold a row without a
  certifier, and that agent then gives children of that row to agents of the
  principal alone.
- **Nobody but the issuer ends such a row early.** A row without a certifier
  has no withdrawal for cause and no stop coin. A child of it ends with its
  own seal, with the seal of its parent, or with its window.
- **Grant v3 does not change.** A row of the contract profile
  `swarma-trust-contract/2` always names its notary (LIP-0014 section 2),
  and every v3 child is certified.

### 11. Vectors of sections 8 to 10

Two files hold 103 vectors over the 27 rules of sections 8 to 10. They follow
J12 and J10, in force since version 0.1.51, and the vectors of rows without a
certifier follow section 10, which both owners decided, through the checks of
section 9 and the holders of LIP-0010 section 10 (J11, in force since the same
version).

| File | Group | Vectors | What a checker does |
| --- | --- | --- | --- |
| [`groups-vectors.json`](../vectors/LIP-0026/groups-vectors.json) | `parents` | 10 valid, 16 refused | Section 8 on the stated groups, ranges, limits and pools of a parent; a refused parent states the rule that it breaks |
| | `ordinals` | 12 | R8.3 and R8.8: the group, the range and the coin of an ordinal, or `CHILD_ORDINAL` |
| [`class-vectors.json`](../vectors/LIP-0026/class-vectors.json) | `templates` | 6 valid, 9 refused | R9.1, R10.1 and R10.2 on a stated template and the issuer that the parent binds |
| | `admissions` | 13 passing, 33 refused, 4 compound | Sections 9 and 10 for one child, in the order of R9.9 |

The groups file holds no octets, because a parent has none yet. `group-10` and
`group-22` hold amounts whose sum is 2 to the power 64: a checker that adds in
64 bits gets 0 and takes the second for a parent within its pool. `group-07`,
`group-25` and `group-26` put a range into the transaction of the parent's
seal, beside the seal, over it and up to it.

An admission of the class file holds octets where they exist: the script of the
current output of the recipient name with the value inside it, and for each
input of the operation that created that output the script that it spends and
its unlocking script or witness. The value of a landlord is the text of a name
value. The history of a landlord is stated, output by output, as the walks of
the LIP-0021 vectors are. The writer of each output is the one that the output
before it implies, because the name input of an update spends that output
(LIP-0021 O4.1); no history of the file is one that cannot occur.

`class-25` is the gift. The recipient name points to the landlord, the landlord
is untouched, a holder holds the name, and the name input of the update that
wrote the value spends an output of another key. It refuses as `CLASS_WRITER`,
and its control is `class-01`, where the holder spent its own previous output.
`class-26` is the same gift by a registration, with `class-03` as its control.
`class-27` is the limit of R9.11: the holder made an update of its own on the
gifted name, and the check passes.

Four refused admissions hold a class of two landlords and bind the holders to
the landlord that the value names, in both positions of the class. In
`class-36` and `class-37` the value names the first landlord, and their control
is `class-35`. In `class-36` a holder of the second landlord wrote the value
and sent the name to a holder of the first; it refuses as `CLASS_WRITER`. In
`class-37` a holder of the second landlord holds the name; it refuses as
`CLASS_HOLDER`. `class-38` and `class-39` are the mirror: the value names the
second landlord, and their control is `class-05`. In `class-38` a holder of the
first landlord wrote the value (`CLASS_WRITER`), and in `class-39` a holder of
the first landlord holds the name (`CLASS_HOLDER`). A checker that takes the
holders of every landlord of a class together admits all four. One that adds to
the holders of the named landlord those of the landlords listed before it, or
those of the issuer's landlord, admits the two mirrors and decides every other
admission of the file as it stands.

Two admissions end with a code of LIP-0021. In `class-29` the current output of
the recipient name has an unsupported script. The proof of the recipient by
name refuses it as `RECIPIENT_NAME_UNAVAILABLE`, where a checker that made the
checks of the class first would report a code of the class: this vector shows
the place that R9.9 gives the checks. In `class-34` the child signs another
owner key than the one that holds the name, while every check of the class
would pass. The proof refuses it as `RECIPIENT_NAME_NOT_HELD`, which shows that
the proof is made and not where it stands. The file lists these two codes apart
from its own, in `codes_of_lip_0021`.

`certifier-01` to `certifier-09` are the cases S9-1 to S9-K1 of LIP-0014
section 8.3 and their neighbours. `certifier-08` is the same exact name in a
row with a certifier: the checks of a class are not made for it. `certifier-10`
and `certifier-11` hold one history of the issuer's name, which came to its
owner by a transfer below the recent block, under the two forms of a row
without a certifier. Both refuse as `CLASS_VALUE_UNAUTHORIZED`.

Every landlord value of the class file is in the inline form of version
0.1.51 (LIP-0010 section 10.9), which a verifier still reads, so no byte and
no outcome of the file changes with version 0.1.53. No admission of the file
holds a holders list, a pin or a seal; the vectors of the pinned form are
those that LIP-0010 section 10.11 describes, and none is published yet.

The limits of the two files are these. Transaction ids are placeholders, and
the octets of signatures are placeholders that verify nothing. No vector reads
a chain or holds an observation, a pending transaction as octets, a request or
an attestation. The largest size of a parent has no vector. The refusal of a
parent has no code, so a refused parent states a rule. Both files stand as
they were made. Since version 0.1.53 the vectors of LIP-0020 section 12 hold
parents as octets, the largest size among them, and the code
`GRANT_DELEGATE`.

No checker for these vectors is in this repository. The expected outcomes were
stated by hand, computed by one implementation and decided again by a second
one that shares no code with the first; neither is published here. Both come
from the author of this text, so an error of understanding that they share is
in the vectors. The vectors bind nothing until both owners accept the rules
that they follow.

## Sources

No node, no signer and no store was run for this LIP.

| Statement | Source |
| --- | --- |
| The path of a seal key, the rules of its account and the weakness of its layout | LIP-0008 section 11.1 |
| The funding account `m/84'/7'/0'` and a seal account of 10 or above | The key map, table of paths |
| The row coin key: its owner, what it signs, and that its account and path are not fixed | The key registry, entry "Row coin key, v4" and the open points |
| A transaction that spends an output which is missing or already spent is invalid | Namecoin Core at the tag `nc28.0`, `src/validation.cpp`, the check that reports `bad-txns-inputs-missingorspent` |
| The reference laboratory holds none of the codes of J1.2 and J1.3 | A search of the Go files of `swarma-chain-lab` at `b03c6f10fad1be135e780d8b1f556fc46805eb06` |
| A node relays a transaction of at most 400,000 weight units (section 8) | Namecoin Core at the tag `nc28.0`, `src/policy/policy.h`, the constant `MAX_STANDARD_TX_WEIGHT`. The count of 3223 outputs is computed from the sizes of a witness key hash input and output; no transaction of that size was built |
| The owner pin, the three readings of a script, the writer check, a live name and the walk (section 9) | LIP-0021 sections 2 to 6 |
| The holders list of a landlord, its pin in the landlord value and the seal of each entry (sections 9 and 10) | LIP-0010 section 10; the inline form of version 0.1.51 in its section 10.9 |

## Alternatives

- **The parent's own limit as the ceiling of its descendants**, as LIP-0008
  section 12.2 can be read. A principal would sign one number. The executor
  of a child would have to read the journal of the parent's executor, which
  section 4 excludes, and LIP-0014 section 9 says the opposite.
- **One ledger of the pool** that every executor of a row draws on. A row
  could use what another left. It is the shared remainder that LIP-0008
  section 4 forbids, and it needs a party that every executor reaches.
- **The principal funds the coin.** The principal would see the coin before
  it signs. The coin pays a key of the re-delegating side, so that side
  gives out the address either way, and the principal would pay for a
  marker that it cannot spend.
- **Row keys in the seal account.** One account would be enough. A signer
  could then no longer tell from the account what an input is, and the
  weakness of the layout would join seals and rows: one leaked key of
  either kind with the extended public key opens both.
- **Hardened indices for row keys.** The extended public key would give no
  row key. A watch-only node would import each script one by one, as
  LIP-0008 section 11.1 says of seals, and the choice is the same as there.
- **Refusing only a coin that is the linkage output**, and no other output
  of the child's seal transaction. The rule would be narrower in words. A
  coin elsewhere in that transaction can have no child under LIP-0023, as
  section 3 shows, so the narrower rule would admit parents with a row that
  can never be used.
- **A member of the child that names the coin.** A verifier would read the
  coin from the child. The row already names it, and a second place could
  disagree with the first.
- **A coin that is an output of the parent's seal transaction.** One
  transaction would create the seal and the coins. Under the Witness
  profile the seal transaction may be pending when the parent is signed,
  and the decision asks for a coin that is confirmed by then.

## Security consequences

- **The holder of a row key can void its row.** Spending the coin outside
  an issuance leaves the row without a child for good. R4.5 is the signer's
  rule against it, and a thief of the key is not bound by it. Such a thief
  issues nothing.
- **Two inputs are not two keys.** R3.4 keeps one input from standing for
  the linkage and for the coin. A signer that pays both outputs to one key
  breaks R4.1, and no verifier sees it.
- **One child for each row holds on the active chain.** A reorganisation
  that removes an issuance frees the coin on the new chain. The decision
  accepts it, and R3.5 keeps a report from saying more.
- **The recent block of the parent dates the coin.** A parent whose issuer
  commits an older block than its tip refuses coins that were confirmed in
  between. That harms only the delegation of that parent.
- **A child's executor does not see what the parent itself spent.** The own
  account of the parent lives in another ledger. The principal's exposure
  is the sum of R5.9 and not the larger of its two parts.
- **Accounts are worth what their journal is worth.** An executor whose
  store went back unnoticed has accounts that are too low. LIP-0014 J1.4
  and LIP-0025 treat that, and no rule of this profile replaces them.
- **A missing limit is no unlimited limit.** A request that consumes a key
  for which its grant states no limit meets a ceiling of 0 (R5.2).
- **The codes of section 2 do not say that an attestation is missing.** A
  child that widens its row refuses for the widening, also when a notary
  certified it.

The following consequences belong to sections 8 to 10: to sections 8 and 9,
in force since version 0.1.51, and to section 10, which both owners decided,
where its rows meet the checks of section 9.

- **A class is as strong as the custody of its holder keys.** A holder key
  admits whatever value it writes into a name that it holds (R9.7). It is a
  name-owner key, which the key registry asks to keep cold, and a key that
  registers the names of agents every day is not cold.
- **A holder that renews a gifted name adopts it.** Check (d) refuses a
  value that another key wrote, until a holder writes over it. R9.11 is the
  rule for the holder's signer, and no verifier sees its breach.
- **A change of the holders no longer ends the landlord's own v4 grants.**
  Since version 0.1.53 the list is outside the `swarma` member that LIP-0008
  section 3 binds for an issuer: the landlord's value pins it by hash
  (LIP-0010 section 10.4, H13). A landlord that adds a holder for a new
  station pins a new list, and its grants stay. Only a landlord in the
  inline form of version 0.1.51 still refuses every v4 grant that it issued
  before such a change, and it does so once more when it moves to the list
  (LIP-0010 section 10.9, M5).
- **A class reads a list that is not on the chain.** The landlord's value
  pins the hash, and the octets come from the presenter or from the
  verifier's cache. A verifier that cannot get them refuses the child,
  `LIST_UNKNOWN`, and admits nobody on an older list (LIP-0010 H24).
- **A spent holder seal is seen by each verifier on its own node.** A
  verifier whose node has not seen the spend admits the name of that entry
  until it does (LIP-0010 section 10.7; LIP-0022). Only a verifier that
  validated the spending transaction itself keeps a closure that no
  rollback lifts; one that reads seal states through a gateway is a
  non-witness and admits the name again after an eviction or a
  reorganisation (LIP-0010 H47, H50). A seal counts only while its funding
  output is confirmed in the active chain (LIP-0010 H46), and no verifier
  checks how the landlord made the seal or kept its spend.
- **The guarantees of a class against a revoked or removed name live in
  the verifier's holder journal.** A verifier that cannot write it admits
  nobody through a class, and one that lost it is a newcomer (LIP-0010
  H43).
- **A class admits only listed names.** Since version 0.1.53 a name that a
  holder key registers passes a class only once the landlord's list names
  it. Names listed ahead, in reserve, need no update of the landlord's name
  when they come into use (LIP-0010 H37).
- **One key holds a whole range.** Under R8.9 a leaked row key voids every
  unused row of its range, where under R4.3 it voids one row.
- **A row without a certifier has one signer of children.** The delegation
  key signs the child, the row's coin shows that the signer of the
  re-delegating side took part, and nobody else does. Whoever holds both
  issues one child for each such row, to any agent of the issuer's landlord.

## Conformance impact

None on normative v0.1 and none on Grant v3: the profile `/2` of LIP-0014
keeps its rows with four members and its codes. No conformance class is
added. The cases S1-1 to S1-4 and S1-10 of LIP-0014 get a reading for v4
from sections 2, 3 and 5; the cases of the store, S1-5, S1-5-ABA and S1-6,
still run on a real store.

Sections 8 to 10 add nothing to Grant v3 either: a row of profile `/2` names
its grantee by key and always names its notary. Their two vector files are
Draft vectors: they follow J10, J11 and J12, in force since version 0.1.51
without the co-author's answer, and the vectors of section 10 follow J9, which
both owners decided, through the checks of J10. The codes they name stay
proposals.
They change no vector of section 7.

## Open questions

- **The owners' acceptance** of each rule, and first of the five points
  that the section "What is decided and what is proposed" lists.
- **The index of the row account.** R4.1 gives a floor and a separation.
  Whether the specification fixes one index is the owners' choice.
- **The custody of the row account**: how it is created, wrapped and
  recovered. The same question is open for the seal account (LIP-0024
  section 5).
- **Who funds the coin.** R4.4 proposes the operator of the re-delegating
  side.
- **The seal of a child and its linkage key.** Who creates the seal of a
  child, and so who signs which input of a child's anchor (LIP-0014
  section 11.1).
- **The octets** of a reservation entry, and the key that identifies a
  request (LIP-0020 section 6). The octets of a row and of a pool are
  LIP-0020 section 11 since version 0.1.53.
- **Limits with a period, and kinds that are floors.** Each waits for its
  type profile.
- **The place of the coin's checks** relative to the checks of the
  attestation.
- **A run** of the reads of section 3 on nodes, and of section 5 on a store
  that is qualified under LIP-0014 J1.4.
- **The co-author's answer** on J10 and J12, on which sections 8 and 9
  rest, and on J11 in LIP-0010. All three are in force since version 0.1.51
  without it, and it is folded in by amendment. The admission of a child of a
  row without a certifier (section 10) rests on J9, which both owners agreed,
  and on J10 and J11, which only Ivan Oparin has decided.
- **The four bounds of R8.4** and a bound on the landlords of a class.
  LIP-0020 W11.6 takes the four numbers as bounds of the grant's schema and
  states no bound on the landlords of a class; proposal Q1 is still before
  the owner.
- **The stop coins of a group** whose template names a certifier (section
  8). LIP-0020 W11.6 gives them a place in a range, which no owner has
  decided.
- **Whether a change of `holders` should end an issuer's grants.** Closed
  in version 0.1.53 by an owner decision of 2026-11-16: it does not.
  The list is outside the member, pinned by hash (LIP-0010 section 10). The
  co-author's answer and the points that section marks NEW are open there.
- **The owner of the delegator** in a row without a certifier (section 10).
- **A pending operation of a recipient name** (section 9).
- **The eight codes of section 9.**
