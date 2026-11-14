# LIP-0026: Rows and accounts profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** what a v4 parent states for each row, how a verifier checks
  that a child fits its row and that its issuance spent the coin of the
  row, how the re-delegating side derives, funds and uses the key of that
  coin, and which accounts of an executor's ledger a request debits
- **Builds on:** LIP-0014 section 9.1 (J1), LIP-0008 sections 2, 3.1, 4,
  11.1 and 12.2, LIP-0022 sections 1 and 4, LIP-0023 and LIP-0025

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
  confirmed, and the input of the child's anchor that spends it (section
  3);
- the row account of the signer: its path, its index, its funding, and the
  one kind of input that a row key signs (section 4);
- the accounts of an executor's ledger, and which of them a request debits
  (section 5);
- eight refusal codes, three of them new, and their order (section 6);
- vectors, among them a trace of one parent over three executors and a
  trace of direct requests beside the requests of siblings (section 7).

It defines no octets of a row. The members of a v4 grant do not exist yet,
and the rows come with them.

## What is decided and what is proposed

The rows, the two ledgers and the coin of a row are Ivan Oparin's decision
of 2026-11-14 (J1), recorded as Draft text in LIP-0014 section 9.1; the
co-author's agreement is pending. A further decision of the same day names
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
4. Three codes: `ROW_COIN` and `ROW_COIN_REQUIRED` for the refusal that
   J1.9 leaves without a name, and `OWN_LIMIT_OVER` for the refusal of an
   own account, which J1.3 leaves without one.
5. The script of the coin is a witness key hash, and the coin is no output
   of the seal transaction of the row's child (R3.1, R3.4). Both follow
   from LIP-0023, which is a draft itself.

Nothing of this profile is implemented. The owners accept or change its
rules through this LIP, under LIP-0001.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The checks of sections 1 to 3 and the accounting of section 5, as functions of stated facts | Yes | The owners' acceptance |
| A row as octets of a grant, and a reservation as an entry of a journal | No | The members of the grant and of an invocation (LIP-0020) |
| The reads of the coin and of the anchor on a node | No | A run under LIP-0022 and LIP-0023 |
| The row account in a signer | No | The owners' choice of the account, and the custody of v4 accounts, which is open (LIP-0024 section 5) |
| An executor's ledger on a store | No | A store that is qualified under LIP-0014 J1.4; LIP-0025 proposes its form |
| The arithmetic of one kind of limit | No | The type profile of that kind (LIP-0008 section 2) |

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
| R1.1 | A row states five things: the executor, as a service name with its pinned public key; the recipient of the child, in exactly one of the two modes of LIP-0008 section 3.1; the limits of the row; the certifier, which is one of the notaries that the parent pins; and the coin, as an outpoint and a script. The ordinal of a row is its position among the rows of the parent, counted from 1. |
| R1.2 | A limit has a kind, a resource, a unit and an amount, and a period where its kind has one (LIP-0008 section 2). The key of a limit is all of these but the amount. No two limits of one row have the same key, and no two own limits of one grant have. |
| R1.3 | A parent states one pool amount for every key that one of its rows limits. For each key, the amounts of the rows do not sum to more than the pool, and the sum is an exact integer sum. |
| R1.4 | The coins of the rows of one parent are different outpoints, and none of them is the seal of the parent. |
| R1.5 | A parent that does not meet R1.1 to R1.4 or R3.1 is refused as a whole: it admits no child and no request of its own. The refusal is one of the members of the grant and gets its code with them. |

The five things of R1.1 are the decided content of a v4 row. The outpoint
and the script of the coin are this draft's way to state "the coin"; the
script is what a principal compares before it signs, and the outpoint is
what a verifier reads.

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

### 3. The coin of a row

The coin of a row is one output with a witness key hash script, confirmed
at or below the parent's recent block, and the anchor of the row's child
has an input that spends it.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| R3.1 | The script that a row states for its coin is a witness key hash: the octets `00 14` and 20 further octets. | The parent is refused (R1.5) |
| R3.2 | A verifier establishes on its own node, in the observation of the check (LIP-0022 section 1), that the transaction of the coin's outpoint has an output at the stated index with exactly the stated script, and that this transaction is confirmed on the active chain at a height that is not above the height of the parent's committed recent block (LIP-0022 section 4). | `ROW_COIN` |
| R3.3 | One input of the child's anchor spends the outpoint of the coin of the child's row. | `ROW_COIN_REQUIRED` |
| R3.4 | That input is an ordinary input of the anchor under LIP-0023: it has the form of C3.1, and it spends a confirmed output under C4.2. It is not the linkage input. An issuer does not take, as the seal transaction of a child, the transaction that holds the coin of the child's row: the anchor would have two inputs from its seal transaction and refuse under LIP-0023 C2.3. | The codes of LIP-0023 |
| R3.5 | A verifier, a receipt and a report state that a child is the only child of its row for the active chain of the observation and for nothing wider (LIP-0014 J1.8). | None of its own |

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
| `ROW_COIN` | The coin of the row is not on the active chain as the row states it, or is confirmed above the parent's recent block | R3.2 | New |
| `ROW_COIN_REQUIRED` | No input of the child's anchor spends the coin of its row | R3.3 | New |
| `OWN_LIMIT_OVER` | A reservation would exceed an own account | R5.6 | New |
| `ROW_CAP_OVER` | A reservation would exceed a row account | R5.6 | LIP-0014 J1.3 |

R6.1. At the admission of a child, the four checks of section 2 stand in
their order, at the place that R2.5 names. `ROW_COIN` and then
`ROW_COIN_REQUIRED` stand after the checks of LIP-0023 on the child's
anchor. Where these two stand relative to the checks of the child's
attestation comes with the profile of the attestation.

R6.2. At a reservation, the order is that of R5.6. A request that is
refused reserves nothing.

None of these refusals records a closure.

### 7. Vectors

[`vectors/LIP-0026/rows-vectors.json`](../vectors/LIP-0026/rows-vectors.json)
holds 59 vectors over the 33 rules of this LIP, as decisions on stated
facts. No vector holds a grant, a transaction or an entry of a journal.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `parents` | 4 valid, 9 refused | Section 1 and R3.1 on the stated rows and pools of a parent |
| `fit` | 4 passing, 11 refused, 3 compound | Section 2 on a parent and a child, with the order of R2.5 for a child that has two defects |
| `coins` | 3 passing, 11 refused, 1 compound | Section 3 on a row's coin, on what a node gives for it, and on the inputs of the child's anchor |
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

## Sources

No node, no signer and no store was run for this LIP.

| Statement | Source |
| --- | --- |
| The path of a seal key, the rules of its account and the weakness of its layout | LIP-0008 section 11.1 |
| The funding account `m/84'/7'/0'` and a seal account of 10 or above | The key map, table of paths |
| The row coin key: its owner, what it signs, and that its account and path are not fixed | The key registry, entry "Row coin key, v4" and the open points |
| A transaction that spends an output which is missing or already spent is invalid | Namecoin Core at the tag `nc28.0`, `src/validation.cpp`, the check that reports `bad-txns-inputs-missingorspent` |
| The reference laboratory holds none of the codes of J1.2 and J1.3 | A search of the Go files of `swarma-chain-lab` at `b03c6f10fad1be135e780d8b1f556fc46805eb06` |

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

## Conformance impact

None on normative v0.1 and none on Grant v3: the profile `/2` of LIP-0014
keeps its rows with four members and its codes. No conformance class is
added. The cases S1-1 to S1-4 and S1-10 of LIP-0014 get a reading for v4
from sections 2, 3 and 5; the cases of the store, S1-5, S1-5-ABA and S1-6,
still run on a real store.

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
- **The octets** of a row, of a pool and of a reservation entry, and the
  key that identifies a request (LIP-0020 section 6).
- **Limits with a period, and kinds that are floors.** Each waits for its
  type profile.
- **The place of the coin's checks** relative to the checks of the
  attestation.
- **A run** of the reads of section 3 on nodes, and of section 5 on a store
  that is qualified under LIP-0014 J1.4.
