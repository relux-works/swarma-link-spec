# LIP-0014: Notary-certified re-delegation

- **Status:** Draft
- **Created:** 2026-11-12
- **Affects:** re-delegation (LIP-0008 section 12.6), the notary (LIP-0012),
  the trust contract and admission of LIP-0013, the action table of LIP-0005,
  the name value shapes of LIP-0010
- **Builds on:** LIP-0004, LIP-0008 section 12, LIP-0012 and LIP-0013
- **Vectors:** [`vectors/LIP-0014/contract-vectors.json`](../vectors/LIP-0014/contract-vectors.json),
  for the contract profile `swarma-trust-contract/2` (section 12); no
  published checker reads them yet

## Summary

Every child grant needs a notary's attestation, and every verifier still
checks each countable condition of the child itself. A child without a valid
attestation refuses as not certified, even when all its numbers are within the
parent's. A child that is wider than its parent in an action, a repository, a
budget or a window refuses with that mechanical reason, even when it carries a
valid attestation.

The parent grant names its notaries and its children. Its signed right of
re-delegation lists one to four notaries, each by its `id/` name, the
registration of that name and its owner key, and each notary publishes its
attestation key in its own name. It also holds one row for each child that the
grant permits, with the executor, the grantee, the cap and the certifier of
that child. A notary is never the party that re-delegates and never the party
that receives the child.

On Grant v3 only the landlord's grant key signs a grant. The child is therefore
a grant that the landlord's signer issues on a signed request of the parent's
grantee. The parent binding lives in the contract, in the profile
`swarma-trust-contract/2`. That profile has one member set, which sections 2
and 3 state and for which section 12 names vectors. No v3 byte changes.

Nothing in this LIP is implemented. It belongs to the second phase of Goal 1:
it follows the first proof, starts in shadow mode, and is no part of the first
proof.

Section 8.3 holds J9, decided and agreed by both owners on 2026-11-15: a v4
row inside one owner may have no certifier, and its child then needs no
attestation. The first paragraph of this summary holds for every v3 child and
for every v4 child of a row that names a certifier. J9 admits the child of a
row without a certifier only through the class of landlords and the list of
holders (J10 and J11). Ivan Oparin put J10 and J11 in force in version 0.1.51
without waiting for the co-author's agreement, so such a child is admitted
where its recipient passes those checks (section 8.3). The co-author's answer
is folded in by amendment.

## Decisions recorded

The owners decided the following on 2026-11-12. The LIP stays Draft; adoption
follows LIP-0001.

| Decision | Direction |
| --- | --- |
| D1. Every child is certified | A child grant is admitted only with a valid notary attestation. The rule does not depend on whether the child's scope is written in words. |
| D2. Root grant | A root grant that carries a right of re-delegation names its notaries. It needs no attestation of its own. |
| D3. Designation | The right of re-delegation, signed in the parent grant, names one to four notaries by `id/` name. Each notary publishes its attestation key in its own `id/` name. |
| D4. Staging | After the first proof and in shadow mode first. Enforcing mode for children needs a separate approval by each owner. |
| D5. Withdrawal | A notary's withdrawal is durable. The same child may be certified again after a plain withdrawal and may not after a withdrawal for cause. |
| D6. Sibling budgets | Children draw on a separate pool that the parent signs, each child with its own partition. |
| D7. Depth | Two links. |
| D8. Whose notary | When issuer and delegator have one owner, the notary is the issuer's. When they have different owners, it is a third party both agree on. It is never a notary that belongs only to the delegator's owner. |
| D9. Quorum | One attestation by any one of the named notaries is enough. |
| D10. Anchor | One LIP-0005 frame per attestation, with action `0x04`. Batching comes later. |
| D11. Cost | Within one owner the issuer pays the notary's seal, anchor and fee. Across owners the contract says who pays. |
| D12. Delegable actions in Goal 1 | `instruct`, `review` and `land`. `spend` is not delegable in Goal 1. |

D1 settles proposal (e) of LIP-0008 section 12.6 more broadly than that
proposal stated it: the attestation is required for every child, not only for
a child with free-text scope. D2, D3, D5, D9 and D10 close open questions of
LIP-0012. J9, decided and agreed by both owners on 2026-11-15, limits D1 on v4
to the children of rows that name a certifier; section 8.3 states how it reads
D1, D2, D3 and D8. The rows of this table do not change.

The twelve directions are the owners'. Everything else in this LIP is the
draft's proposal and is not decided: the field names and bytes of the right of
re-delegation, of the contract profile and of the attestation, the refusal
codes and their order, the event kind 8186, the commitment formula of the
anchor, and the action `0x05`.

### Decisions of 2026-11-13 and 2026-11-14

Five additions to the decisions above were decided by Ivan Oparin: J3 on
2026-11-13 and the others on 2026-11-14. The co-author agreed to J1 and J3 on
2026-11-15, so both owners have decided those two. On J2, J4 and J5 the
co-author's agreement is pending, except for one point of J5 that both owners
agree on: what a v4 child does with its parent's text (section 3.4). The rules
of each decision stand in this LIP, in one subsection that opens with the
decision and carries a label of this table. J2, J4 and J5 are not adopted
before the co-author agrees, and until then the text in force for them stays as
it is.

| Label | Touches | The decision | State |
| --- | --- | --- | --- |
| J1. Rows | D6 | The parent signs one row for each child it permits, with the executor, the grantee, the cap and the certifier of that child. On v3 the limit is a number of compartments. On v4 each row also pins a coin that the issuance of its child must spend, and the coin pays a separate key, derived from the seed of the operator's signer in an account of its own. Section 9.1. | Agreed by both owners: the co-author agreed on 2026-11-15. It replaced a pool that the children share, and lists of the agents and grantees a child may name. |
| J2. Withdrawal for cause | D5 and D9; N6 and N8 of LIP-0012 | Each row names one notary, and only that notary certifies the row. It keeps one succession of seals for the row, and a cause counts only when the notary's signature covers its frame. On v3 D5 is narrowed. On v4 each row also names a stop coin of its notary, whose spend ends the row for every verifier. Section 10.1. | The co-author's agreement is pending. Until then any named notary certifies, and a withdrawal for cause reaches only the parties that observed its frame (section 10). |
| J3. Notary identity | D3 | The parent pins each notary as LIP-0008 section 3 pins an issuer: by name, registration and owner key, with a signed checkpoint, and the attestation key in force must have been written by the pinned owner. Section 7.1. | Agreed by both owners: the co-author agreed on 2026-11-15. It replaced a parent that binds a notary by name only. |
| J4. The key that signs a child on v4 | K2 of the key map; LIP-0008 section 12.6 | The parent names one delegation key. On v4 only that key signs children, and it signs nothing else: the messaging key never grants authority. Section 11.1. v3 does not change. | The co-author's agreement is pending. Until then the parent's recipient key signs the child (LIP-0008 section 12.6). |
| J5. Scope text | R3 of LIP-0008 section 12.6; N2 of LIP-0012 | On v3 a child carries its parent's text unchanged, by hash, and narrows only members that a machine compares. A text governs an agent's work and never an effect: an executor that cannot read refuses a grant with a text, and no executor performs a landing or a payment automatically under one. It refuses such a request, and the owner's confirmation of one operation stays as an exception (J5b). On v4 a re-delegation narrows only typed fields and appends no text; both owners agree on that point. Section 3.4. | The co-author's agreement is pending, except on the point for v4. Until then the notary judges a child's text against the parent's, and no step compares an instruction with the text (section 3.3). |

Four further decisions stand in other LIPs. J7, signing under a grant for
each run (LIP-0013 section 3.6), was decided by Ivan Oparin on 2026-11-14
and awaits the co-author's agreement. J6, a durable closure for an
owner-signed change of an issuer's name (LIP-0008 section 5.2), and J8, the
signed invocation as the request of a verdict (LIP-0011 section 7), were
accepted by Ivan Oparin on 2026-11-13 and await the co-author's agreement
as well. J13, sessions for clients that cannot sign
([LIP-0028](LIP-0028-sessions.md)), was decided by Ivan Oparin on 2026-11-15
and awaits the co-author's agreement.

The three pending decisions are separate from each other. Section 10.1 builds
on the rows of section 9.1, which are decided. Where the Draft text of one
pending decision uses another, it says so. Under section 10.1, sections 7.1 and
11.1 read the notary of the child's row. The delegation signer of section 11.1
identifies its caller through LIP-0013 section 3.6 and reads the closure
journals of section 10.1 and of LIP-0008 section 5.2, where those are adopted.

The cases of these subsections carry identifiers. In S3-1 the number
after S is the number of the decision, so S3-1 is the first case of J3. A
letter after the case number marks a variant, and K marks a known limit: a
case that the text admits, and says so.

With J1 a notary adds up no budget across siblings, and it keeps a record of
one child for each row. If J5 is adopted as well, a notary judges no text for a
child of profile `/2`. An attestation then gives a second signature by a party
that the issuer chose (D8), a seal that this party can spend, and a cause that
its witnesses remember; under J2 the notary also keeps one succession of seals
for each row and its causes. D1 is not reopened.

### Decisions of 2026-11-15 on the rows of a v4 parent

Ivan Oparin decided four further points on 2026-11-15. The co-author agreed to
J9 on the same day: J9 is decided and agreed by both owners on 2026-11-15, and
section 8.3 holds it as text in force. J10, J11 and J12 are in force since
version 0.1.51: on 2026-11-16 Ivan Oparin decided to put them in force without
waiting for the co-author's agreement, which has not been given. The
co-author's answer, when it comes, is folded in by amendment. All four concern
the rows of a v4 parent. The contract profile `swarma-trust-contract/2` of
Grant v3 does not change: its member set is the one of sections 2 and 3, each
of its rows names a notary, and every v3 child is certified.

| Label | Touches | The decision | State |
| --- | --- | --- | --- |
| J9. No certifier inside one owner | D1, D2, D3 and D8; J1.1 on v4 | A child needs an attestation only where its row names a certifier, and the right of re-delegation of the parent decides that for each row. A row without a certifier is valid only where its recipient constraint is limited to the issuer's own landlord. Across owners a certifier stays mandatory, as D8 says. The stop coin of section 10.1 belongs only to rows with a certifier. Section 8.3; LIP-0026 section 10. | Decided and agreed by both owners on 2026-11-15. It limits D1 on v4 to the children of rows that name a certifier. A child of a row without a certifier is admitted only through the class of J10 and the holders of J11, which are in force since version 0.1.51 (section 8.3). |
| J10. Landlord class | J1; LIP-0008 section 3.1 | The recipient constraint of a row gains a third form beside a key and a name: a list of landlords, each pinned like a notary under section 7.1. A child of such a row names its recipient by name, and the executor makes four checks in a fixed order; the fourth asks that a holder of the landlord wrote the value of the recipient name. LIP-0026 section 9. | In force since version 0.1.51, by Ivan Oparin's decision of 2026-11-16 not to wait for the co-author. The co-author's answer is folded in by amendment. |
| J11. Holders | LIP-0010 section 3 | A landlord lists, in its own name value, the owner keys of the names of its agents and stations. An absent or empty list admits no name to a class. LIP-0010 section 10. | In force since version 0.1.51, by Ivan Oparin's decision of 2026-11-16 not to wait for the co-author. The co-author's answer is folded in by amendment. |
| J12. Groups | J1 | A parent states its rows as groups: a template with coin ranges, and one ordinal across groups and ranges. LIP-0026 section 8. | In force since version 0.1.51, by Ivan Oparin's decision of 2026-11-16 not to wait for the co-author. The co-author's answer is folded in by amendment. |

The four belong together in one direction. J10 needs the list of J11, and J9
uses the checks of J10 to say what "one owner" means for a verifier. J12 stands
by itself. Where the text of one of them uses another, it says so. All four
are in force, so a child of a row without a certifier meets rule J9.2 through
the checks of J10 and the list of J11 (section 8.3). Both owners agreed to J9;
J10, J11 and J12 rest on Ivan Oparin's decision alone until the co-author
answers.

### Decision of 2026-11-16 on the reservation ledger of the signing service

Ivan Oparin decided on 2026-11-16, as the lead relayed it, that the issuer's
reservation ledger is part of the v4 specification, as a duty of the signing
service of the delegation key and not as a check of a verifier. For one place
of one parent the service makes one signature, ever, with a durable record
before it signs. The same intent is answered with the same result, another
payload for the same place refuses, and a write that was interrupted or
whose outcome is unknown is not taken as absent: the place is held, with no
automatic retry, no new key and no new place. Section 11.1 holds the duty as
rules J4.4 (a) to J4.4 (g), with two codes of the service and the cases
S4-11 to S4-30, S4-15a among them. It adds no member to a grant, no step for a verifier and no
vector, and it changes no v3 byte. The duty binds wherever a delegation key
of J4 signs, so it has the standing of J4: the co-author's agreement has not
been given, and the co-author's answer is folded in by amendment.

### One member set for profile `/2` (2026-11-15)

Before version 0.1.46 this LIP described the right of re-delegation twice: with
the lists of its first draft, and with the rows and the pins of J1 and J3,
which waited for the co-author. One profile string then stood for two sets of
members, and an implementation of `swarma-trust-contract/2` could not tell
which of them to read. With the co-author's agreement of 2026-11-15 the first
set is gone, and this revision removes its text: the lists `agents` and
`grantees`, the count `max_children`, notaries as bare names, the attestation
members `budget` and `prev_attestation_id`, and the verifier's step for a sum
over siblings.

`swarma-trust-contract/2` now names exactly one member set in one order: the
fifteen members of the contract (section 3), the six of `delegate`, the four of
a row and the three of a notary entry (section 2).
`swarma-notary-attestation/1` has eighteen members (section 6.1).

What the owners decided are the directions of the two tables above. The names
of the members, their order, their bytes and the refusal codes are still this
draft's proposal. This revision fixes them, so that vectors and an
implementation can be built against one text, and it says in place where it had
to choose a form that no decision gives: the form of a notary's owner pin, the
range of an output index and the validity of the key of a row (section 2), and
a largest integer, what each rule of a reader owns and the order in which it
reports (section 3.1). A later change of a member, of its bytes or of its
meaning takes a new profile string, as LIP-0018 section 1 asks of every
profile.

## Motivation

An orchestrator directs an executor, and the executor directs a sub-executor
as part of that work. The executor may also hold its own standing grant over
the sub-executor, with more repositories than the principal gave the
orchestrator. If the executor relays the orchestrator's work under that
standing grant, the orchestrator obtains through the executor what the
principal refused it. A child grant bound to the orchestrator's grant gives
the executor a grant for exactly that work: relayed under the child, the work
is admitted only within the orchestrator's grant. The executor still holds
its standing grant, and no check makes it relay under the child; LIP-0013
lists that as open question T10.

LIP-0008 section 12.6 already decides that a child is never broader than its
parent (R1), that countable conditions are compared mechanically (R2), and
that conditions in words need a separate check (R3), which the notary performs
(LIP-0012, N2). It left open whether the attestation is mandatory. A rule that
applies only to children "with textual scope" needs someone to decide whether
a scope is textual, and that decision is itself a judgement. Requiring the
attestation for every child removes the classification (D1).

## Current state

- LIP-0008 section 12.6 records R1 to R6, and LIP-0012 records N1 to N4. Both
  describe semantics without bytes.
- LIP-0013 defines the one-hop trust grant on v3, profile
  `swarma-trust-contract/1`. It has no parent binding and no right of
  re-delegation. A reader of profile `/1` fails closed on a contract of this
  LIP, in one of two ways. A complete contract of this LIP has fifteen
  members, and that reader refuses it as `CONTRACT_ENCODING`, because its
  rule 1 knows only the eleven-member set. An eleven-member object in which
  only the profile string is `swarma-trust-contract/2` passes rule 1 and
  refuses as `CONTRACT_PROFILE`; vector C-N23 of LIP-0013 is that second
  case.
- The laboratory experiment `notary` of LIP-0012 certifies the exact bytes of
  one grant. It does not compare a child with a parent.
- The v3 reference path has no delegation code. A v3 grant is valid only
  under the landlord's grant key (LIP-0004 section 2).
- No reader of profile `/2` is published. `tools/trustcheck` reads profile
  `/1` alone, and section 12 says how the vectors of profile `/2` were
  computed.

## 1. Terms

| Term | Meaning |
| --- | --- |
| Principal `L` | The `landlord_name` of the root grant. Every grant on one path has the same principal. |
| Parent `P` | A grant whose signed terms carry a right of re-delegation (section 2). |
| Child `C` | A grant whose signed terms bind the `grant_id` of `P` (section 3). |
| Delegator | The grantee of `P`, the holder of `P.grantee_key`. LIP-0008 section 12.2 requires that each link's audience is the next link's issuer. |
| Delegatee | The grantee of `C`, the holder of `C.grantee_key`. |
| Child signer | On v4, the delegator; section 11.1 holds Draft text, under a decision that awaits the co-author's agreement (J4), that names a delegation key instead. On v3, the landlord's grant key, acting on the delegator's signed request (section 5). |
| Notary `N` | A party named by `P`'s right of re-delegation whose attestation key signs the statement "child within parent" (LIP-0012). |
| Row | One entry of `slots` in `P`'s right of re-delegation. It fixes the executor, the grantee, the cap and the certifier of one child (sections 2 and 9.1). A child names its row by its ordinal. |
| Link | One signed grant on the authority path. A root grant is link 1 and its child is link 2. A third link refuses (LIP-0008 section 12.2). |

Under LIP-0013 a trust grant says that a grantee may direct an executor for a
principal. The orchestrator, executor and sub-executor of the motivation map
to two links:

| Link | Signed by, v3 / v4 | Grantee | `agent_name` | Meaning |
| --- | --- | --- | --- | --- |
| 1, root `P` | `L` / `L` | the orchestrator | the executor | The orchestrator may direct the executor within `P`. The right of re-delegation in `P` lets the orchestrator ask for one child for each row of `P`, with the grantee and the executor that the row names. |
| 2, child `C` | `L` on the orchestrator's request / the orchestrator | the executor | the sub-executor | The executor may direct the sub-executor within `C`, which is within `P`. Closing `P` closes `C`. |

The executor of `C` differs from the executor of `P`. LIP-0008 section 12.2
allows that only because the issue capability names the child's grantee and
executor explicitly; the rows of section 2 carry them.

## 2. The right of re-delegation

A right of re-delegation is the signed member `delegate` of a grant's terms. On
v3 it is a member of the contract (section 3) and is bound through
`contract_sha256`. On v4 it belongs to the signed scope; this LIP defines no v4
bytes. Since version 0.1.53 [LIP-0020](LIP-0020-grant-v4-wire-registry.md)
section 11 defines them: the member `delegate` of `swarma-grant/4`, with the
delegation key, the child-seal key, the delegable actions, the pools, the
pinned notaries and the groups of rows. On v3 it is an object with exactly
these six members in this order:

| Member | Type | Rule |
| --- | --- | --- |
| `depth` | integer | `0` or `1`. `0` means the grant carries no right of re-delegation. A child carries `0`. |
| `actions` | array of strings | The actions a child may receive: sorted, without duplicates, a subset of the grant's own `actions`. Non-empty when `depth` is 1. |
| `budget` | integer | The pool: atoms that all children together may receive as `spend_budget`. Greater than 0 exactly when the `actions` of this object include `spend`; at most 2100000000000000. The caps of the rows MUST NOT sum to more than `budget`; the sum is an exact integer sum. It is separate from the grant's own `spend_budget` (section 9). |
| `slots` | array of objects | One row for each child that the grant permits: 1 to 16 rows when `depth` is 1. The ordinal of a row is its 1-based position in the array. Two rows MAY name the same executor and grantee. |
| `notaries` | array of objects | The notaries whose attestation satisfies D1: 1 to 4 entries when `depth` is 1, sorted by `name`, without a repeated name. |
| `checkpoint` | string | The hash of a block of the active chain: 64 lowercase hex, in the byte order in which a node prints it. The history of each notary's name is constrained from this block on (section 7.1). v3 only: on v4 the grant's committed recent block takes its place. |

A row, an entry of `slots`, is an object with exactly these four members in
this order:

| Member | Type | Rule |
| --- | --- | --- |
| `executor` | string | An `id/` name in the v3 name syntax (LIP-0013 section 2.1), different from `landlord_name`. The child of the row carries it as its `agent_name`. |
| `grantee` | string | An x-only key: 64 lowercase hex, valid under BIP-340, as `grantee_key` is in LIP-0013 section 2.1. The child of the row carries it as its `grantee_key`. A row names one key and has no wildcard. |
| `cap` | integer | Atoms, 0 to 2100000000000000: the most that the child of the row may carry as `spend_budget`. |
| `notary` | string | The `name` of one entry of `notaries`: the certifier of the row. |

An entry of `notaries` is an object with exactly these three members in this
order:

| Member | Type | Rule |
| --- | --- | --- |
| `name` | string | The notary's `id/` name in the v3 name syntax. |
| `registration` | object | The transaction and the output that first registered the name: exactly the two members `txid` and `vout`, in this order. `txid` is 64 lowercase hex, in the byte order in which a node prints it. `vout` is an integer from 0 to 4294967295. |
| `owner` | string | The owner pin, the key that controls the outputs of the name: a compressed secp256k1 public key in 66 lowercase hex. The first two characters are `02` or `03`, and the other 64 are the x coordinate of a point of the curve. |

"Sorted" means ascending by byte value, as in LIP-0013 section 2.2. When
`depth` is 0 every array is empty, `budget` is 0 and `checkpoint` is the empty
string, so a right of re-delegation with `depth` 0 has one value. A grant
without the right carries it, and so does every child:

```json
{"depth":0,"actions":[],"budget":0,"slots":[],"notaries":[],"checkpoint":""}
```

A right with one row and one notary, with line breaks for display only:

```json
"delegate":{"depth":1,"actions":["instruct","review"],"budget":0,
"slots":[{"executor":"id/alexey-worker","grantee":"<64 hex>","cap":0,"notary":"id/ivanopcode-notary"}],
"notaries":[{"name":"id/ivanopcode-notary","registration":{"txid":"<64 hex>","vout":0},"owner":"<66 hex>"}],
"checkpoint":"<64 hex>"}
```

A right of re-delegation with `depth` 1 and no notary is malformed and refuses
as `DELEGATE_NO_NOTARY`. Every other violation of these tables refuses as
`CONTRACT_DELEGATE`: a member that is missing, added, repeated or out of order
in `delegate`, in a row, in an entry or in a registration; a value of another
JSON type, such as a bare name in `notaries`; and a value outside its rule.
This is how D1 and D3 become a field check: a grant cannot give the right to
re-delegate without saying who certifies. Section 3.1 gives the order of the
two codes.

Only `depth` 1 gives the right. Ordinary action authority, possession of a
grant, management of an agent and an audience key give none (LIP-0008 sections
12.2 and 12.6).

In Goal 1 a right of re-delegation MUST NOT list `spend` (D12). Profile `/2`
belongs to Goal 1, so a reader of it refuses a right that lists `spend`, as
`CONTRACT_DELEGATE`. The `budget` of a valid right is then 0, and so is every
`cap`. The members `budget` and `cap` and the ledgers of section 9.1 stay in
the format for a later decision of the owners on a delegable `spend`. The
vectors of section 12 hold contracts of that spend profile and mark them; no
reader admits one today.

The rows are the decision J1, and the pins of a notary and the checkpoint are
the decision J3. Sections 9.1 and 7.1 hold their rules, and both owners agree
on both. Three points of form in the tables above are this draft's and belong
to no decision. The first is the form of `owner`. J3 binds an owner key and
left its encoding to the profile that LIP-0008 section 3 will fix. A profile
with fixed bytes needs a form now, and the table of an entry takes the
compressed key, which Draft [LIP-0021](LIP-0021-name-ownership-and-history.md)
proposes for every owner pin (its rule O2.1). The table states that form in
full, so that the bytes of profile `/2` do not move with another draft. The
second is the range of `vout`, which is the range of an output index in a
transaction. The third is that the `grantee` of a row is a valid key and not
only 64 characters: the child of the row carries it as its `grantee_key`, and
LIP-0013 requires that key to be valid.

A row names its certifier (J1.1). The check that the attestation of a child
comes from the notary of its row is rule J2.2 of section 10.1, under a decision
that awaits the co-author's agreement. Until then an attestation by any notary
that the parent names satisfies step V12 (D9).

On v4 a row carries more than these four members (section 9.1). Two decisions
that await the co-author's agreement add members on v4 only: a stop coin for
each row (J2, section 10.1) and a delegation key (J4, section 11.1). None of
them is a member of profile `/2`. J9 (section 8.3) lets a v4 row state that it
has no certifier; it removes no member of profile `/2`, whose every row names
its notary.

The member set of the first draft of this LIP, with `agents`, `grantees` and
`max_children` and with notaries as bare names, is no part of profile `/2`. An
object that carries it refuses as `CONTRACT_DELEGATE`, like every other object
whose members are not the six of this section.

## 3. The contract profile `swarma-trust-contract/2`

Profile `/2` is profile `/1` of LIP-0013 with four more members. Its bytes
follow the encoding rules of LIP-0013 section 2.1. The object has exactly these
fifteen members in this order:

| # | Member | Rule |
| --- | --- | --- |
| 1 | `profile` | exactly `swarma-trust-contract/2` |
| 2 to 10 | `network`, `landlord_name`, `agent_name`, `grantee_key`, `actions`, `repos`, `spend_budget`, `not_before`, `not_after` | as in LIP-0013 section 2.1 |
| 11 | `scope_text_sha256` | `""`, or the SHA-256 of the scope text in 64 lowercase hex |
| 12 | `parent_grant_id` | `""` for a root, or the parent's `grant_id` in 64 lowercase hex |
| 13 | `ordinal` | `0` for a root, `1` to `16` for a child |
| 14 | `delegate` | the object of section 2 |
| 15 | `note` | as in LIP-0013 section 2.1 |

The encoding rules hold at every depth. The objects and arrays inside
`delegate` are compact, their members stand in the order of section 2, an empty
array is written `[]`, and every integer and every string follows the rules of
LIP-0013 section 2.1. A complete root contract, with line breaks for display
only; the real bytes contain none:

```json
{"profile":"swarma-trust-contract/2","network":"main","landlord_name":"id/ivanopcode",
"agent_name":"id/ivanopcode-executor","grantee_key":"<64 hex>","actions":["instruct","review"],
"repos":[],"spend_budget":0,"not_before":1794528000,"not_after":1797120000,
"scope_text_sha256":"","parent_grant_id":"","ordinal":0,
"delegate":{"depth":1,"actions":["instruct","review"],"budget":0,
"slots":[{"executor":"id/alexey-worker","grantee":"<64 hex>","cap":0,"notary":"id/ivanopcode-notary"}],
"notaries":[{"name":"id/ivanopcode-notary","registration":{"txid":"<64 hex>","vout":0},"owner":"<66 hex>"}],
"checkpoint":"<64 hex>"},"note":""}
```

### 3.1. Which rules a reader applies

A reader that supports both profiles selects the rules by the member set of the
object, before it judges any value:

| Member names of the object, in order | Rules |
| --- | --- |
| The eleven of LIP-0013 section 2.1 | Profile `/1`: LIP-0013 section 2.3, unchanged |
| The fifteen of this section | Profile `/2`: the rules below |
| Any other set or order | Refusal as `CONTRACT_ENCODING` |

For the fifteen-member set the rules are those of LIP-0013 section 2.3 with
three differences. Rule 1 judges the canonical bytes against the fifteen
members of this section in their order. Rule 2 requires the profile string of
this section. Rule 3 also judges `scope_text_sha256`. Rules 4 to 7 are
unchanged, and two rules follow them:

| # | Rule | Refusal |
| --- | --- | --- |
| 8 | `ordinal` is 0 to 16. `parent_grant_id` is `""` or 64 lowercase hex, and it is `""` exactly when `ordinal` is 0. A contract with a parent has `delegate.depth` 0 | `CONTRACT_PARENT` |
| 9 | `delegate` follows section 2 | `CONTRACT_DELEGATE`, or `DELEGATE_NO_NOTARY` for `depth` 1 without a notary |

A reader applies the nine rules in this order and reports the first failure.
With nested members that needs three statements which LIP-0013 did not need.
They are this draft's.

**What rule 1 owns.** Rule 1 owns every lexical property of the bytes, as in
LIP-0013, and it owns them at every depth: the size of at most 8192 bytes; the
compact form without whitespace and without a trailing newline; the spelling of
every integer and of every string; and that the document holds nothing but
objects, arrays, strings and integers, so that `null`, `true`, `false` and a
number with a fraction or an exponent refuse here. An integer is at most
9223372036854775807, and a larger one refuses here as well. Rule 1 also owns
the fifteen members: their names, their order and, for each member except
`delegate`, the JSON type that its rule gives it.

**What rule 9 owns.** Rule 9 owns the value of `delegate` as a whole: that it
is an object, its members and their order, the members of a row, of an entry
and of a registration, the JSON type of each value and every rule of section 2.
A row that lacks a member therefore refuses as `CONTRACT_DELEGATE`, while
`"cap":01` inside the same row refuses as `CONTRACT_ENCODING`. Rule 9 reports
in three steps:

1. A `delegate` that is not an object with exactly the six members of section 2
   in their order, with an integer for `depth` and for `budget`, an array for
   `actions`, `slots` and `notaries` and a string for `checkpoint`, refuses as
   `CONTRACT_DELEGATE`.
2. `depth` 1 with an empty `notaries` refuses as `DELEGATE_NO_NOTARY`, whatever
   else the value breaks. The case never comes alone: no row can name a listed
   notary when none is listed.
3. Every other violation of section 2 refuses as `CONTRACT_DELEGATE`.

**What rule 8 reads.** Rule 8 stands before rule 9 and reads one value of
`delegate`. Where `delegate` is an object whose first member is `depth` with an
integer value, a contract with a parent refuses unless that value is 0. Where
rule 8 cannot read `depth` in this way, it leaves `delegate` to rule 9.

A member set and its profile string must agree. Fifteen members with the string
`swarma-trust-contract/1`, and eleven members with the string
`swarma-trust-contract/2`, both refuse as `CONTRACT_PROFILE` under rule 2 of
the selected rules. A reader that implements profile `/1` alone knows one
member set: it refuses every fifteen-member object as `CONTRACT_ENCODING` under
its rule 1.

### 3.2. Binding to the grant

The consent tags and the derived v3 scope are those of LIP-0013 sections 2.2
and 2.4. The binding to the grant is LIP-0013 section 2.5 with one
substitution: its check 2, "the contract passes section 2.3", runs the rules
that the member set selects under section 3.1. Checks 1 and 3 to 6, the
contract hash, the equality of the common fields, the derived scope, the
budget and the consent tags, are the same for both profiles. A grant under
profile `/2` is an ordinary valid v3 grant.

### 3.3. Scope text

A scope text governs an agent's work and never a service's effect. That is
the rule of LIP-0006 section 7, decided on 2026-11-14, with the co-author's
agreement pending. Section 3.4 applies the rule to profile `/2`; the
paragraph below describes the text as the draft proposed it before that
decision.

The scope text is a separate document. Its exact octets hash to
`scope_text_sha256`, and it travels with the bundle. Text narrows only: like
the note of LIP-0013, it can never add an action, a repository, a budget or
time. It is meant to restrict what the structured members already allow. A
wrong judgement about text therefore cannot widen a mechanical limit. No
step of section 8 and no step of LIP-0013 section 3.4 compares an
instruction with the text. Whether an executor honours the text is left to
that executor. Section 3.4 records the decision of 2026-11-14 on this (J5).

### 3.4. One text along the path, and what a text does to an effect

Decided by Ivan Oparin on 2026-11-14 (J5), in four parts and a fifth that
followed on the same day (J5b); the co-author's agreement is pending on
each. On v3 a child carries its parent's text unchanged. A text governs an
agent's work and never a service's effect, and money and landings go into a
grant without a text. An executor refuses a landing or a payment that is
still requested under a grant with a text, and the owner's confirmation of
one operation stays as an exception (J5b). Profile `/2` gains no new member,
and on v4 the ref, the revision and the payee are machine members. And these
rules are in force before an executor enters enforcing mode. One further
point is agreed by both owners: on v4 a re-delegation narrows only typed
fields and appends no text. Until the co-author agrees to the five parts,
section 3.3 stands alone: a text narrows a grant, the notary judges a
child's text against the parent's once, at certification, and no step
compares an instruction with the text. Take a child whose text limits the
work to one component of a repository. An instruction that concerns another
component, within the child's actions and repositories, passes every step of
section 8 and steps 6e to 6g of LIP-0013. The notary's `within` is a
judgement as well: no verifier can recompute it.

The subsection does two things, and they answer different halves of that
case. On v3 a child carries the exact octets of its parent's text, by hash,
and narrows only members that a machine compares (J5.1 to J5.3, J5.6). A
second text then does not occur on v3, and the value `within` has no use
there. And the subsection says what a text does at an executor (J5.4, J5.5,
J5.7, J5.8). It does not make words enforceable: equal bytes are not an
applied restriction.

| Property | Closed? | For whom |
| --- | --- | --- |
| The child's text is not wider than the parent's | On v3: yes, completely, because no second text exists. On v4: agreed for the first version, in which a child appends no text; the rule is written with the v4 bytes | Every verifier of a child of profile `/2`, one that starts later included |
| A grant with a text is never executed by an executor that cannot read | Yes, by J5.4 | Every executor that accepts profile `/2` |
| No record says that a text was checked | Yes, by J5.5 | Every reader of a record |
| No landing and no payment rests on a reading of words | Yes, by J5.5: no executor performs a `land` or a `spend` automatically under a grant with a text | Every executor that accepts profile `/2` |
| An agent's work lies within the words | Not established at admission. This is the half of the case that the instruction for another component shows | Nobody at admission; an owner, a moderator or an arbiter judges it afterwards |

The rules apply to contracts of profile `/2`, whose member set carries
`scope_text_sha256`. A reader MUST NOT synthesize the member
for a contract of profile `/1`, require it there, or treat `note` as a scope
text. Nothing is added to a grant or to an attestation. The executor's
configuration gains the setting `text`, which its owner sets to `none` or
`conduct`; absent means `none`. With `conduct` the executor is an agent. Its
admission gate holds the exact octets and hands them to the agent in the
authority frame of each admitted instruction (LIP-0013 section 3.4), and
the agent treats them as a restriction on its work. The
setting promises that a model considers the text. It does not promise a
qualified evaluator, and none is defined; a setting for one is reserved, as
LIP-0008 section 12.4 reserves its policy form. For a contract that carries
the member, the record of LIP-0013 step 7 gains `scope_text` with the values
`none` and `present`. For a contract of profile `/1` the record is
unchanged.

What a text does to an effect follows one rule, which Ivan Oparin decided
on 2026-11-14 and which LIP-0006 section 7 states for every service:

> Text always governs an agent's work and never a service's effect.

`land` and `spend` are the actions that derive a v3 scope entry and end in
an effect at a resource (LIP-0013 section 2.2). Under a grant that carries
a text no executor performs them automatically (J5.5). `instruct` and `review` are an
agent's work, because their object is itself words: no predicate over
"assign this work" exists to fail closed on, and the agent applies the
text to them. A principal who wants an agent to work under a text, and
also to land or to pay, issues two grants: one with the text, whose
actions are `instruct` and `review`, and one without a text for the
landing or the payment, limited by members such as `repos` and
`spend_budget`. Explanation that should bind nobody goes into `note`,
which carries no authority. That matches what v4 says of constraints:
unknown semantics refuse, and no unimplemented policy evaluator may stand
in for the checks (LIP-0008 section 12.2).

The four parts left one question open: what an executor does with a
`land` or a `spend` that is still requested under a grant with a text.
Ivan Oparin decided it later on 2026-11-14 (J5b), and the co-author's
agreement is pending: the refusal is the default, and the owner's
confirmation stays as an exception, with exact arguments and recorded as
the owner's decision. Three courses were considered:

| Course | The request | State and cost |
| --- | --- | --- |
| Refusal | The executor refuses it. | The default. Under the default a text and a landing never meet in one grant. |
| (c) Confirmation of effects | The executor holds a `land` or a `spend` until its owner confirms that one operation, bound to the exact revision or amount (J5.9). `instruct` and `review` stay the agent's work. | The exception. The owner confirms each landing under a grant that has a text. A review under a text can still feed the gate of a landing under another grant. |
| (b) Confirmation of every action | No predicate over a text exists, so every instruction, review, landing and payment under a grant with a text would wait for the owner's confirmation. | Not taken. Grants meant for unattended work would carry no text. |

Ivan Oparin's decision of 2026-11-14 covers three things: the refusal as
the default, the exception as course (c) with the binding of J5.9, and that
course (b) is not taken. This revision therefore removes what served
course (b) alone and what 0.1.35 carried as pending: rule J5.5 (b), case
S5-4b and the clause of J5.9 that bound a confirmation to the body of an
instruction or a review.

The decision does not say what selects the exception: for which executor,
or for which request, the confirmation takes the place of the refusal. This
draft proposes an answer and marks it as a proposal: the executor's owner,
who also confirms, chooses the exception for an executor. The proposal is
no part of the decision and has no normative effect. No rule, no step and
no case of this subsection requires an outcome that depends on that
choice.

One rule is excluded by the decision of 2026-11-14: that the agent applies
the text to every action, landings and payments included. An effect would
then rest on the agent's reading, which can be wrong and is checked only
after the fact.

| # | Rule | Refusal |
| --- | --- | --- |
| J5.1 | A child of profile `/2` MUST carry its parent's `scope_text_sha256` unchanged: both empty, or both the same value. A child MUST NOT add a text where the parent has none and MUST NOT drop the parent's text. Equality is of octets; a different line ending or Unicode form is a different text. | `CHILD_TEXT_DIFFERS`, at V9, before the attestation is read |
| J5.2 | Every member of a child's contract is handled by exactly one row of the member table below. A member to which a profile assigns no row, and a member whose semantics the verifier does not know, refuses, also when child and parent carry equal bytes (LIP-0008 section 12.2). For each narrowing relation the profile states what the executor compares the member with at the effect. | The code of the member's row |
| J5.3 | For a child of profile `/2` the attestation's `textual` is `none` or `identical`, which is what V14 computes from two equal hashes. D1 is unchanged: a child with equal text still needs its attestation. Whether the value `within` stays in the attestation object is for the later revision that narrows by text. | An attestation that carries `within` beside equal hashes: `ATTESTATION_BINDING`, at V14 |
| J5.4 | An executor whose `text` setting is `none` MUST refuse a grant whose `scope_text_sha256` is not empty, root or child, after step 6d of LIP-0013. An executor whose setting is `conduct` MUST hold the exact octets that hash to that value; its admission gate makes that check before it builds an authority frame (LIP-0013 section 3.4). | `TEXT_UNSUPPORTED`; without the octets `TEXT_UNAVAILABLE` |
| J5.5 | At an executor with `conduct` the agent applies the text to its work, which is `instruct` and `review`, as a restriction on what the structured members allow; a text never adds. The executor MUST NOT perform a `land` or a `spend` automatically under a grant whose text is not empty. On v4 the same holds for every command that the action profile marks as an effect at a resource. An issuer that wants a text and an effect issues two grants, and SHOULD NOT list `land` or `spend` in a contract that carries a text. No admission step establishes that an agent's work lies within a text, and no record, receipt or attestation may report that it did. A confirmation is recorded as the owner's decision and never as a check of the text. The record of step 7 states `scope_text` as `none` or `present`. Then one of two branches applies (J5b). The refusal is the default. The confirmation is an exception. What selects the exception is open, and neither branch fixes it. | By the branch |
| J5.5, refusal | The executor refuses the request, after step 6e of LIP-0013. | `TEXT_UNSUPPORTED` |
| J5.5 (c) | The exception (J5b). For `land` and `spend`, and on v4 for every command that the action profile marks as an effect at a resource, the executor MUST NOT perform the effect automatically under a grant whose text is not empty. It holds the effect until its owner confirms it under J5.9, or it refuses. `instruct` and `review` are conduct. | `TEXT_NEEDS_APPROVAL` |
| J5.6 | An inherited text is the root's. Its words refer to the parties and resources of the root grant, which the bundle carries (V2). A reader MUST NOT resolve them against the child's grantee, executor or run. | none; a rule of reading |
| J5.7 | A restriction that must hold at admission MUST be a structured member. The executor compares that member with the arguments actually passed to the privileged call, resolved immediately before the effect, when step 6 of LIP-0013 runs again. A plan, a title or a description of the arguments is not the arguments. | The code of the member, before the effect |
| J5.8 | Words of the delegator travel only as the body of an instruction (LIP-0013 section 3.3), which is data until admitted. Explanation that should bind nobody belongs in `note`. An operative text MUST NOT be treated as explanation without a new, signed and consented contract. | none of its own |
| J5.9 | The rule serves the exception of J5.5 (c). A confirmation binds one operation and is used once. The owner's command MUST name the `event_id` of the request and the `grant_id` it was admitted under; the action; the resolved target, which is the repository and the ref for `land` and the payee for `spend`; and the content of the effect, which is the exact revision to be landed for `land` and the amount for `spend`. Immediately before the effect the executor resolves the actual arguments again (J5.7) and compares them with the confirmation. If the revision, the target, the amount or the payee differs, the confirmation does not apply, and the effect is held again or refuses. A candidate that was rebased, regenerated or amended is another revision and needs its own confirmation. The executor journals the confirmation as its owner's decision, with the arguments that it names, and records its use durably before the effect; a second effect under it refuses. A retry of the same event is not a second use; it falls under the existing rule of one effect per event. A confirmation widens nothing: every structured check of the grant runs as it does without one. The wire form of the command is the deployment's; what it binds is not. | `TEXT_NEEDS_APPROVAL` |

The owner's command of J5.9 is the verified owner command that a2a already
uses (LIP-0013 section 3.5); the bytes of the confirmation record are open.

The member table of J5.2, for a child of profile `/2`:

| Member of the child | Relation to the parent | Refusal |
| --- | --- | --- |
| `profile` | fixed: `/2` in both | `CONTRACT_PROFILE`, `NOT_DELEGABLE` |
| `network`, `landlord_name`, and the grant's genesis | equal to the parent's | `SUBJECT_MISMATCH` |
| `agent_name`, `grantee_key` | equal to the executor and the grantee of the child's row (sections 4 and 9.1) | `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED` |
| `actions` | subset of `P.delegate.actions` | `CHILD_ACTIONS_WIDER` |
| `repos` | subset of `P.repos`, by exact bytes | `CHILD_REPOS_WIDER` |
| `spend_budget` | at most the `cap` of the child's row (sections 4 and 9.1) | `CHILD_BUDGET_OVER` |
| `not_before`, `not_after` | nested in the parent's window | `CHILD_WINDOW_NOT_NESTED` |
| `scope_text_sha256` | equal to the parent's | `CHILD_TEXT_DIFFERS` |
| `parent_grant_id` | the dedicated check V3 | `PARENT_ID_MISMATCH` |
| `ordinal` | the dedicated check of its range; it selects the row (section 9.1) | `CHILD_ORDINAL` |
| `delegate` | fixed: the one value with `depth` 0 (section 2) | `CONTRACT_PARENT` for another `depth`; `CONTRACT_DELEGATE` for `depth` 0 with a member that is not empty (section 3.1) |
| `note` | none; it carries no authority | none |

The parent's `delegate` members are read by their own steps (V4, V8, V9,
V12) and are not inherited. A child narrows through three relations,
subset, at most and nested, and through nothing else.

The fields that a principal may want to narrow map to members as follows:

| Field | v3 profile `/2` | Relation | v4 |
| --- | --- | --- | --- |
| Repository | `repos` | subset | the typed target of the action profile |
| Ref | none; `land` is the default branch | fixed by the action | a machine member of the action profile from its first version |
| Exact revision to be landed | none | none | a machine member of the action profile from its first version |
| Payee of a payment | none | none | a machine member of the action profile from its first version |
| Path inside a repository | none | none | none; it stays words until a rule exists that compares a diff with a path |
| Action | `actions` within `P.delegate.actions` | subset | exact leaf commands (LIP-0008 section 12.3) |
| Recipients | the grantee and the agent of the child's row | equal to the row (section 9.1) | the permitted targets of a typed limit |
| Amounts | `spend_budget` | at most | typed limits |
| Window | `not_before`, `not_after` | nested | height windows (LIP-0008 section 12.5) |

The steps change as follows. V9 gains one equality, of the two text hashes.
V14 checks `none` and `identical` against the two hashes. The bundle of V2
carries one text. Step 6 of LIP-0013 gains the refusals of J5.4 after 6d
and the refusal of J5.5 after 6e, for contracts that carry the member;
step 7 gains `scope_text`. Under the exception of J5.5 (c) the refusal
after 6e gives way to a hold at step 9 and the confirmation of J5.9.
Profile `/1`, its vectors and kind 8185 do not change.

J5.1 to J5.3 and J5.6 belong to the draft profile `/2` on v3. For roots,
J5.4, J5.5 and J5.7, and J5.9 where the exception is used,
are a precondition of enforcing mode for every executor that accepts
profile `/2`, and the setting `text` is `none` unless the
executor's owner set `conduct`. An executor that accepted `/2` contracts and
entered enforcing mode for one-hop grants would otherwise admit a `/2` root
with a text and act on it with no text rule in force. An executor that
accepts profile `/1` alone cannot meet a scope text: profile `/1` has no
text member, and that reader refuses every fifteen-member object (section
3.1).

What stays open:

- **Whether an agent's work lies within the words.** A text is applied to
  `instruct` and `review` by the agent that reads it, and by nobody else.
  That is behavioural trust in the principal's own executor, checked after
  the fact by an owner, a moderator or an arbiter. No summary of this
  subsection may say that scope text is enforced.
- **A confirmed effect rests on a person's judgement.** Under the
  exception of J5.5 (c) an effect that was requested under a text is
  performed on the word of the executor's owner. That judgement can be
  wrong, and it is independent of the model that proposed the effect. The
  bytes of the confirmation record are not fixed.
- **What selects the exception.** The decision names the refusal as the
  default and the owner's confirmation as an exception. It does not say
  for which executor, or for which request, the confirmation takes the
  place of the refusal. The draft's proposal, that the executor's owner
  chooses the exception for an executor, is not decided and binds nothing.
  Until the owners decide, this subsection says what an executor does
  under each branch and not which branch applies.
- **Reviews feed landing gates.** A review is an agent's work, also a
  review given under a grant with a text, and such a review can let a
  landing under another grant, one without a text, pass its gate. It is
  therefore not true that no effect anywhere follows from a model's
  reading. It is true that under a grant that carries a text no landing
  and no payment is performed, except the one operation that the
  executor's owner confirmed under J5.9.
- **Few narrowing members.** Profile `/2` narrows actions, repositories,
  the budget and the window, and the recipients through the parent's right
  of re-delegation. It has no member for a ref, a revision, a payee or a
  path, and under J5.5 a text cannot carry such a limit for a landing or a
  payment. On v3 that limit does not exist for an effect. On v4 the ref,
  the exact revision and the payee are machine members, and a path stays
  words.
- **Narrowing by text on v4.** The first version of v4 has none: a child
  appends no text. Layers of text that a notary checks, possibly with keys,
  are in the plans for the next revision, and nothing of them is defined.
  The v4 bytes that carry a child's text are not fixed either.
- **J5.6 is a rule of reading** and cannot be tested mechanically.
- **The delegator cannot bind a narrower task in the grant.** It states the
  task in the instruction.

The decision of 2026-11-14 has four parts, and a fifth followed on the same
day. The first is exact inheritance on v3 (J5.1 to J5.3). It reverses no
decision: R3 of LIP-0008 section 12.6, N2 of LIP-0012 and the decision that
the notary performs the textual check stand, and on v3 a different text no
longer occurs. The second is the principle for effects (J5.5): a text
governs an agent's work and never a service's effect, and money and landings
go into a grant without a text. The course for an effect that is still
requested under a text was not among the four. The fifth part decides it
(J5b): the refusal is the default, and the owner's confirmation of one
operation, with its exact arguments and recorded as the owner's decision,
stays as an exception. The third concerns members for a ref, a path and a
payee. Profile `/2` gains none, because each needs an envelope tag and an
effect check that LIP-0013 does not have. The ref, the exact revision and
the payee are machine members of the v4 action profile from its first
version, and a path inside a repository stays words until a rule exists that
compares a diff with a path. The fourth is the staging of the root rule
before enforcing mode, as the paragraph above states it.

For profile `/2` four other designs were set aside. Keeping `within` there
keeps a value that no verifier can recompute, under which a stolen
attestation key certifies children that exceed their parents in words. A
narrowing clause that the child appends needs a judgement of whether the
clause narrows, and it puts the delegator's text into the executor's scope.
A policy language is reserved and not adopted (LIP-0008 section 12.4). A
qualified evaluator for texts does not exist, and "qualified" has no
definition yet.

**The text of a v4 child.** Both owners agree on this point. The co-author
answered the question on 2026-11-14: as a first approximation, a
re-delegation on v4 narrows only typed fields and appends no text, and
narrowing by text with a notary, possibly with keys, goes into the plans
for the next revision. The owner who decided the other parts of J5 had
leaned towards layers of text that a notary checks. On the same day that
owner agreed to the answer, and so to deferring the layers, on one
condition: that the system can be built without them. The lean is deferred
and not rejected. The agreement fixes no byte. This draft reads it as the
inheritance of J5.1 carried over to the first version of v4: a child
carries its parent's text unchanged, and nothing lets it add a text,
change one or drop one. The v4 bytes that carry the text are open, and the
agreement changes no rule or case of this subsection.

Cases (J5):

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S5-1 | Child and parent with the same non-empty text hash, the exact octets present, `textual` `identical` | A child with another text hash and an attestation that says `within` under the rules in force: `CHILD_TEXT_DIFFERS`, never `CHILD_NOT_CERTIFIED`. Variants that differ only in line endings, in Unicode form or in a final newline, each with its hash recomputed and the grant signed again, refuse the same way. In force this child is admitted with `within`. |
| S5-2 | Both without text, `textual` `none`; and both with the same text, `identical`; each with a valid attestation | Three separate negatives: a text added under a parent without one, and the parent's text dropped: `CHILD_TEXT_DIFFERS`; an attestation that carries `within` beside equal hashes: `ATTESTATION_BINDING`. A child with equal text and no attestation still refuses as `CHILD_NOT_CERTIFIED`. In force, adding and dropping are admitted with `within`. |
| S5-3 | An executor with `text` `none` admits a `/2` grant without a text | The same executor refuses a `/2` grant with a text, root or child: `TEXT_UNSUPPORTED`. In force it is admitted. The case covers the executor that cannot read and always runs beside S5-4. |
| S5-4 | An executor with `conduct` and the exact octets: the same `land` under a grant without a text is performed; under the grant with the text an `instruct` is admitted, and the record says `present` | The text says "only changes under docs/", and an envelope asks for a `land` under the grant with the text. Under both branches no landing happens automatically, whatever the diff touches. Under the default the request refuses as `TEXT_UNSUPPORTED`, and a `spend` refuses the same way; under the exception it is held, or refuses as `TEXT_NEEDS_APPROVAL`, until the owner confirms. A record or receipt that reports the text as checked is wrong. In force the landing is performed. The test observes the effect, not the record. |
| S5-4a | Two grants of one principal to one grantee at one executor: one with the text and the actions `instruct` and `review`, one without a text and with `land` for the repository. An instruction under the first is admitted with `scope_text` `present`, and a landing under the second is performed | An executor that refuses the grant without a text because another grant of the same principal carries one fails the control. An executor that performs the landing under the grant with the text, without its owner's confirmation, fails S5-4. |
| S5-4c | The exception (J5b): under the grant with the text, a `land` of revision `X`, whose diff touches only `docs/`, is held; the owner confirms it, naming the event, the grant, the repository, the ref and `X`; the landing is performed, once; the record states the owner's decision and `scope_text` `present`. An executor that always holds fails this control | Each a separate negative, with the effect observed: after the confirmation the candidate is replaced by `X'` with another diff: not performed; a confirmation that names another event, another repository or another ref: not performed; the same confirmation presented for a second landing: refused; the request asked again as a new event after the confirmation: not performed under the old confirmation. A record that says the text was checked is wrong in every variant. |
| S5-5 | The actual resolved arguments of the privileged call lie inside every structured member | Signed arguments that are narrow and a real call with wider arguments, including a target that changes between check and call: refused before the effect. v4 already requires it (LIP-0008 section 12.2); a test of the signed description alone is not this case. |
| S5-6 | A narrower action set, repository list and window, one at a time, with the identical text and a valid attestation | Each made wider, one at a time, refuses with its mechanical code and not with a certification code. Budget variants run in the spend profile only. |
| S5-7 | Members of the member table | Parent and child carry the same member of unknown semantics, not merely an extra JSON key: refused. |
| S5-8 | Before enforcing mode, the root rule. `text` `none`: a `/2` root without a text is admitted, and a `/1` grant with a `note` is admitted with its record unchanged | `text` `none` and a `/2` root with a text: `TEXT_UNSUPPORTED`. `conduct` with the octets missing or with octets of another hash: `TEXT_UNAVAILABLE`. An executor whose setting is absent behaves as `none`. |
| S5-9 | A child with the parent's text at another grantee and executor; the bundle carries the root's contract and text | A reader that resolves "you" or "my repository" against the child's parties breaks J5.6. The vector checks that the root's parties are present; the reading itself is reviewed, not computed. |

## 4. What a child binds

A child's contract binds the parent and stays within it. Each line of the table
is a mechanical comparison against the presented parent `P`:

| Binding | Rule | Refusal |
| --- | --- | --- |
| `parent_grant_id` | Equals the `grant_id` recomputed from `P`'s presented signed bytes (LIP-0004 section 2) | `PARENT_ID_MISMATCH` |
| Depth | `P` has no parent, `P.delegate.depth` is 1, and no `grant_id` repeats on the path | `CHAIN_DEPTH` when `P` has a parent or an id repeats; `NOT_DELEGABLE` when `P.delegate.depth` is 0 |
| `network`, genesis, `landlord_name` | Equal to `P`'s | `SUBJECT_MISMATCH` |
| `ordinal` | `1 <= C.ordinal <=` the number of rows in `P.delegate.slots`. A verifier checks this before it reads any row; the ordinal then selects the row of the child | `CHILD_ORDINAL` |
| `agent_name` | Equals the `executor` of the child's row | `CHILD_AGENT_NOT_ALLOWED` |
| `grantee_key` | Equals the `grantee` of the child's row | `CHILD_GRANTEE_NOT_ALLOWED` |
| `actions` | A subset of `P.delegate.actions` | `CHILD_ACTIONS_WIDER` |
| `repos` | A subset of `P.repos`, compared by exact bytes | `CHILD_REPOS_WIDER` |
| `spend_budget` | At most the `cap` of the child's row | `CHILD_BUDGET_OVER` |
| Window | `P.not_before <= C.not_before < C.not_after <= P.not_after` | `CHILD_WINDOW_NOT_NESTED` |
| `scope_text_sha256` | No mechanical rule beyond identity: equal values mean identical text. Different values need the notary's judgement | none |

The lines of the table stand in the order in which section 8 checks them.
Section 9.1 holds the rules of the rows (J1). A contract that names a parent
with `ordinal` 0, or with an `ordinal` above 16, does not reach this table: it
is no valid contract and refuses as `CONTRACT_PARENT` (section 3.1, rule 8).
Section 3.4 holds Draft text, under a decision that awaits the co-author's
agreement (J5), under which the two text hashes must be equal.

The table is the table of the v3 contract profile. For a v4 child the
comparisons that J4.4 calls "the comparisons of section 4" are those that
version 0.1.55 proposes in section 8.4: the parent reference, the depth and
the right of re-delegation in row F2; the contract identifier in F5; the
chain in F8; the ordinal, the executor and the recipient in F13 to F15; the
actions in F16; the limits in F17; and the window in F18. LIP-0020 section
11.11 registers the v4 codes of these rows in one table. `CHILD_REPOS_WIDER`
and the text hash have no v4 member and no v4 row.

## 5. The delegation request on v3

On v3 the landlord signs the child, so the bundle must show that the parent's
grantee asked for it. The delegator signs a NIP-01 event of kind **8186** with
empty content, under the event rules of LIP-0013 section 3.1, with exactly
these tags in this order:

| # | Tag | Value |
| --- | --- | --- |
| 1 | `t` | `swarma-delegation-request-v1` |
| 2 | `parent` | the `grant_id` of `P` |
| 3 | `contract` | the `contract_sha256` of the child contract |
| 4 | `ordinal` | the child's ordinal, a canonical decimal |
| 5 | `nonce` | 32 fresh random bytes, 64 lowercase hex |

Its `pubkey` is `P.grantee_key`, and its `created_at` lies inside `P`'s
window. Kind 8186 is a draft allocation, like kind 8185 of LIP-0013: unused in
this repository and in the reference laboratory on 2026-11-12, and not
allocated.

The landlord's signer admits the request before it reserves anything. It
checks the signature, that `P` is live, every rule of section 4, that the
ordinal is unused for `P` and that the nonce is unused. It then records the
ordinal and the budget durably, before any signature, as LIP-0004 section 6
already requires for bookings and seals.

Before it signs a child, the signer shows the person or policy that approves
the signature every term of that child: the parent grant, the grantee, the
agent, the actions, the repositories, the budget, the window, the ordinal, the
cap and the certifier of the child's row, and the named notaries. A signature
given over a hash alone does not meet this.

A verifier checks the request mechanically: its shape and signature, that
the signer is `P.grantee_key`, that `created_at` lies inside `P`'s window, and
that `parent`, `contract` and `ordinal` equal the child's. Any failure refuses
as `DELEGATION_REQUEST`. On v4 the delegator signs the child itself, and no
request exists.

## 6. The attestation

### 6.1. Object `swarma-notary-attestation/1`

The attestation is a statement about two grants. It is not a grant format:
it gives no action, limit or lifetime, and grants keep their own formats. It
is one JSON object under the encoding rules of LIP-0013 section 2.1, with
exactly these eighteen members in this order:

| # | Member | Rule |
| --- | --- | --- |
| 1 | `profile` | `swarma-notary-attestation/1` |
| 2 | `kind` | `child-within-parent`. Profile `/1` has no other kind |
| 3 | `network` | equals `P`'s and `C`'s |
| 4 | `genesis` | 64 lowercase hex; equals the grants' `genesis` |
| 5 | `landlord_name` | equals `P`'s and `C`'s |
| 6 | `notary_name` | the `name` of an entry of `P.delegate.notaries` |
| 7 | `notary_key` | 64 lowercase hex, x-only; the attestation key that the notary's name yields (section 7) |
| 8 | `parent_grant_id` | the `grant_id` of `P` |
| 9 | `parent_contract_sha256` | the `contract_sha256` of `P` |
| 10 | `child_grant_id` | the `grant_id` of `C` |
| 11 | `child_contract_sha256` | the `contract_sha256` of `C` |
| 12 | `ordinal` | equals `C.ordinal` |
| 13 | `textual` | `none` when both contracts have an empty `scope_text_sha256`; `identical` when both have the same non-empty value; `within` when the values differ and the notary judged the child's text to be within the parent's |
| 14 | `mechanical` | `pass`: the notary's claim that it ran section 4 |
| 15 | `notary_seal` | `{"txid":…,"vout":…,"script":…}`: the output whose spend withdraws this attestation |
| 16 | `tip_height` | the height of the tip the notary's node validated |
| 17 | `tip_hash` | the block hash at that height |
| 18 | `attested_at` | Unix seconds; a claim of the signer |

`textual` has no negative value: a notary that judges the child's text to be
outside the parent's signs nothing. Of the three values only `within` is a
judgement; a verifier checks `none` and `identical` against the two hashes.

A verifier never relies on `mechanical`. It runs section 4 itself. A `pass`
over a child that fails section 4 is evidence against the notary.

The signature is BIP-340 by `notary_key` over
`SHA-256("swarma-notary-v1" || attestation bytes)`. The 16-byte ASCII prefix
has no terminator or length, in the fixed-prefix style of LIP-0004 section 2.
The typed-hash plan of LIP-0008 section 8 may replace it before adoption.
[LIP-0020](LIP-0020-grant-v4-wire-registry.md) proposes that replacement as
a successor type, `swarma-notary-attestation/2`, and gives it no member yet.
`attestation_id` is the SHA-256 of the compact object
`{"attestation":…,"signature":…}`.

The attestation carries no statement about a sum over siblings (J1.5): the rows
fix what each child may receive. Earlier revisions of this LIP gave the object
two more members, `budget` and `prev_attestation_id`, between `mechanical` and
`notary_seal`. An attestation that carries either refuses as
`ATTESTATION_SHAPE` (case S1-9 of section 9.1). Section 3.4 holds Draft text,
under a decision that awaits the co-author's agreement (J5), under which the
`textual` of a child of profile `/2` is `none` or `identical`.

### 6.2. When the notary signs

The notary signs after the child is issued and its issuance is confirmed:
`child_grant_id` exists only once the landlord has signed, and a v3 grant is
live only after its commitment is confirmed. A notary MAY read the draft child
contract before the landlord signs, to avoid a wasted issuance. That
pre-clearance binds nobody and is no attestation.

Before it signs, the notary runs section 4 like any verifier, checks in its own
durable record that it certified no other child under that parent and ordinal
(J1.6), and reads both scope texts when their hashes differ (LIP-0012 section
6).

### 6.3. Custody of the attestation key

A notary's attestation key is held by a key service that signs on request and
does not export the key. A key file that the notary's own process can read does
not meet this. The rule is the same for a notary that is an agent and for one
that is a person. The seal that `notary_seal` names pays a key distinct from
`notary_key`, for the reason LIP-0008 section 11.1 gives for grant and seal
keys: one secret should not sign under two schemes.

Deployment note. On a host that has no key service, a notary may hold its
attestation key in a file under a separate OS user, with mode 0600, that no
agent's OS user can read. This is an exception and not the target. Each owner
approves it for each notary on such a host, and it ends when a key service is
available there.

### 6.4. Anchor and seal

The notary anchors each attestation in one zero-value `OP_RETURN` output, in a
LIP-0005 frame with a new action (D10):

| Action | Name | Payload |
| --- | --- | --- |
| `0x04` | notary attestation | `version(1)` \|\| `attestation_commitment(32)` \|\| `locator` |

```text
attestation_commitment = SHA-256( "swarma-attest-v1" || attestation_id
                                  || child_grant_id || parent_grant_id )
```

The preimage is raw bytes without lengths or separators: the 16-byte ASCII
prefix and three decoded 32-byte values, 112 bytes in all. The locator has
type `0x01` and its pointer is `attestation_id`. The script is 72 bytes, the
length of an issuance script:

```text
6a 03 53 4c 04 42 01 <attestation_commitment:32> 01 <attestation_id:32>
```

The seal is an output the notary alone can spend. It exists before the
attestation is signed, because the attestation names it; the anchor follows,
as for a grant (LIP-0008 section 9). One seal may be named by one attestation
or by every attestation of one parent. Spending a seal withdraws every
attestation that names it.

Section 10.1 holds Draft text, under a decision that awaits the co-author's
agreement (J2), that puts the seals of one row into one succession.

## 7. Who the notary is

The parent grant says who certifies its children. `P.delegate.notaries` lists
the acceptable notaries, and a verifier accepts no other (D3). Each entry binds
the notary's name, the registration of that name and its owner key (J3, section
7.1). Because the list is signed in the grant, it is fixed at issuance and
agreed by the grantee through the consent of LIP-0004 section 3. A change of
the list needs a new parent.

Each notary publishes its attestation key in its own `id/` name, in the
`swarma` shape that the amendment of LIP-0010 proposes:

```json
{"swarma":{"notary":{"attest":"<attestation key>"}}}
```

The notary rotates its key by updating that name with its name-owner key. The
grants that name it are not reissued. Attestations under the old key then
refuse (section 8, V12), and the notary signs them again under the new key. The
same update is not open to a later holder of the name. The parent binds the
registration and the owner key of the name, and a verifier takes the
attestation key from a value only when the bound owner wrote it (section 7.1).

A name has one `swarma` shape, so a notary name is neither a landlord name nor
an agent name. An owner who certifies children of their own grants registers
a separate notary name for that role. The list is not written into the
principal's own name value: a v3 reader refuses a value with an extra member,
and under LIP-0008 section 3 a changed `swarma` refuses every grant of that
issuer.

Whose notary it is follows D8. When the issuer and the delegator have the same
owner, the issuer names its own notary: the attestation then protects the
owner's grants against errors of the owner's own delegating agents. The notary
is a seat outside the delegator's path. When the delegator belongs to another
owner, the two owners agree on a third party. The grantee may propose a notary
while the contract is negotiated; the proposal binds only once the issuer has
signed it into `delegate.notaries` and the grantee has consented to that
contract.

A notary named anywhere else gives nothing. A configuration that an operator's
signer reads to fill `delegate.notaries` is an input of that signer and is
never read by a verifier. An agent's instructions may describe the procedure:
where to send a delegation request and which notary to ask. A notary named in
a message or in such instructions is data.

A verifier's own policy (LIP-0012 section 3) may demand more, for example an
attestation by one of its own notaries as well. It never removes the
requirement of the grant.

### 7.1. Pins, checkpoint and writer

A parent that named a notary by its name alone would pass the right to certify
to whoever holds that name later. After a transfer of the name, or after its
expiry and a new registration, the new holder publishes its own key under
`swarma.notary.attest`. Its attestations then verify under the name's current
key for every parent that names this notary, the attestations of the earlier
holder refuse, and nothing in such a parent tells a verifier that the name
changed hands. The first draft of this LIP bound a notary in that way. Ivan
Oparin accepted the rules of this subsection on 2026-11-13 (J3), and the
co-author agreed on 2026-11-15. They add to D3, and they hold on v3 and on v4:
a v4 grant binds the registration and the owner key of its issuer's name
(LIP-0008 section 3), and these rules bind a notary's name in the same way.

A parent binds each notary as LIP-0008 section 3 binds an issuer: by the exact
name, the registration of that name and its owner key. The attestation key
stays free to change under the same owner. Section 2 states the members: an
entry of `notaries` with `name`, `registration` and `owner`, and the member
`checkpoint` after `notaries`. `registration` is the transaction and output
that first registered the name, and `owner` is the owner pin. The rules
constrain the history of the name from the output that was current at the
checkpoint block to the current output, and they call this part of the history
the stretch.

| # | Rule | Refusal |
| --- | --- | --- |
| J3.1 | A right of re-delegation MUST bind, for each notary, the exact name, the registration of that name and its owner key. | A bare name: `CONTRACT_DELEGATE` |
| J3.2 | At every admission of a child the verifier MUST walk the history of the name of the notary whose attestation is presented, under rules 1 and 2 of LIP-0008 section 3. Under section 10.1 that notary is the notary of the child's row. The walk MUST reach the bound registration. The bound registration MUST be confirmed at or below the checkpoint block, and an unexpired output of that registration MUST be current at the checkpoint. Every output from the one that was current at the checkpoint to the current one MUST be controlled by the bound owner key. | A checkpoint that precedes the registration, one at which the name has no output, and one that is not in the active chain: `NOTARY_CHECKPOINT`. An expired name, a walk that ends at another registration, and an owner change on the stretch: `NOTARY_NAME_CHANGED` |
| J3.3 | The value of `swarma.notary.attest` MAY change on the stretch. The attestation key is the one the current value yields. The comparison MUST NOT be an equality of the whole `swarma` member. | none |
| J3.4 | The value in force is the value of the operation that created the name's current output. That operation MUST have been authorized by the bound owner: the name input it spends MUST be controlled by the bound owner key, and the signature on that input MUST commit to the output that carries the value. The first owner-proof profile accepts `SIGHASH_ALL` without `ANYONECANPAY` only. For a `name_update` the name input is the previous name output. For a `name_firstupdate` it is the `name_new` output; a fee input is no substitute. The bound registration is no exception. A value that fails this is not eligible until the bound owner makes a name update of its own, which may repeat the value unchanged. The rule looks at one operation; it does not trace a value back through history. | `NOTARY_VALUE_UNAUTHORIZED`. A signature-hash type outside the profile refuses under J3.5 |
| J3.5 | Where nothing is proved, the verifier refuses, and the refusal is not evidence of a transfer: an incomplete walk, a node without the transaction index, an owner proof or a signature-hash type that the profile does not support, a history supplied by the presenter. | `NOTARY_HISTORY_UNAVAILABLE` |
| J3.6 | A presentation MUST NOT move the start of the stretch. A later issuance locator, a new anchor of the same parent and a newer attestation leave the signed checkpoint where it is. | none of its own |
| J3.7 | Only the notary of the presented attestation is walked; under section 10.1 that is the notary of the child's row. The state of another notary of the same parent does not affect this child. | none of its own |
| J3.8 | A cached walk is valid only for its predicate: this name, registration, owner pin and checkpoint, the active chain up to the cached output, and the notary rule "owner unbroken, value written by the owner". A result cached for an issuer's rule, which also requires an unchanged `swarma`, MUST NOT be used for a notary, nor the reverse (LIP-0008 section 3). | none of its own |
| J3.9 | Before it signs a parent, the issuer's signer MUST run J3.2 and J3.4 for every notary it names, so that it does not sign a parent under which every child refuses. | none at a verifier |

In step V12 of section 8 the verifier first finds `notary_name` among the
entries of `P.delegate.notaries`. It then checks the checkpoint and walks the
name, then checks the writer, and only then reads the key. So
`NOTARY_CHECKPOINT`, `NOTARY_NAME_CHANGED`, `NOTARY_VALUE_UNAUTHORIZED` and
`NOTARY_HISTORY_UNAVAILABLE` come before `NOTARY_KEY`. None of the last three
records a closure.

The three parts close different cases. The pins refuse a name whose owner
is no longer the pinned one, and a name that was registered anew after an
expiry, also under the same spelling and the same owner key. The walk over
the stretch refuses a transfer and return, which a comparison of the
current owner alone does not show to a verifier that starts later. The
checkpoint puts the start of the stretch into the signed parent. A start
taken from the presentation would be the presenter's choice, because the
issuance locator is unsigned (LIP-0004 section 2): a presenter could show a
later anchor of the same parent and leave an earlier transfer outside the
stretch. A requirement of the bound owner for every output since the
registration would end the use of a notary's name, and not only the parents
that pin the old owner, whenever the name-owner key is replaced. The writer
rule refuses a value that the pinned owner did not write; a comparison of
owners passes such a value. A parent that pinned the attestation key itself
would have to be issued again at every rotation of that key, against
section 7.

The writer rule J3.4 has no exception for the registration, because
receiving an output is not consent. A party `U` that holds a `name_new`
commitment can sign the `name_firstupdate` with its own attestation key in
the value and pay the name output to the address of an honest owner `O`.
`O` signs nothing. A parent that pins that registration and `O` passes J3.2,
because every output on the stretch is `O`'s, and without J3.4 `U` would
certify. Under J3.4 the operation that created the current output is the
registration, its `name_new` input was `U`'s, and the child refuses until
`O` makes an update of its own. The transaction facts of this case come
from reading the source of Namecoin Core, release nc28.0; no node was run
for them.

One case stays open under these rules. A thief of the notary's name-owner key
writes a new attestation key under the same owner, and the rules pass, because
the bound owner key signed that update. The defence is cold custody of the key,
as for an issuer. Under section 9.1 a notary whose key is taken can widen no
mechanical limit, and under the Draft text of section 3.4 it judges no text. It
can still certify and withdraw, and under section 10.1 close a row; the pins
settle none of that.

The rules have these costs. Each notary entry carries two pins, and the
parent carries one block hash. A notary that replaces its owner key needs
new parents. A notary whose name another party registered for it makes one
name update of its own before a parent can use it. A reorganisation that
drops the checkpoint block refuses every child of that parent, without
closure, until the chain holds the block again or the parent is issued
again; the issuer SHOULD sign a block that is buried under its own risk
policy.

The registration order that the key map proposes is such a case. There the
funding wallet signs the reservation and the first update, and the name's
output goes to the owner's address. The owner has then signed nothing, and
under J3.4 the value is not eligible. A notary's name that was registered
in this order needs one update signed by its owner before a parent may
name it. The update may repeat the value unchanged.

The script coverage of the owner proof is open in LIP-0008 section 3, and so is
the encoding of an owner pin in a v4 grant. Until a profile for them is
accepted, an unsupported proof refuses under J3.5.
[LIP-0021](LIP-0021-name-ownership-and-history.md) proposes that profile, with
the reading of the signature-hash type that J3.4 needs. They are that draft's
proposals, and each stays open until both owners accept it. The bytes of
profile `/2` do not wait for it: section 2 fixes the form of `owner` in a
notary entry, and the vectors of section 12 use it. Those vectors read no node.
What a verifier does with the pin, which scripts it reads and how it walks the
name, is not covered by them.

The alternative that the owners did not take is the name alone, as the first
paragraph describes it: no pin and no walk, and a notary's name that changes
hands passes on the right to certify.

Cases (J3). Each uses a verifier that starts after the events and holds no
journal. A verifier that reads the current value of the name and no history
admits the refusals of S3-1 to S3-5b and of S3-7, and a suite catches such a
verifier with them:

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S3-1 | Renewal of the notary's name by the same owner; the child is admitted | The name transferred to another owner who publishes a key and attests with it refuses as `NOTARY_NAME_CHANGED`, although the attestation verifies under the name's current key. |
| S3-2 | The same unexpired registration, after a renewal | Expiry and a new registration with the same spelling, by another key and also by the same owner key, refuse. A checker that compares only the current owner passes the first and must fail the second. |
| S3-3 | An unchanged history since the checkpoint | A transfer and return on the stretch, with the current owner and key identical to the control, refuses. |
| S3-4 | The checkpoint signed in the parent | A valid later re-anchor of the same parent, presented to skip a transfer: the stretch still starts at the checkpoint, and the child refuses. |
| S3-5a | A value written by the bound owner in an update | An output of the bound owner whose value a previous holder wrote in the transfer refuses as `NOTARY_VALUE_UNAUTHORIZED` until the owner updates. The fixture puts the checkpoint after the transfer; otherwise the ownership walk refuses first. |
| S3-5b | The owner's own registration; a registration by another party paid to the owner, followed by the owner's update that repeats the value; after that an ordinary rotation by the owner | A `name_firstupdate` signed by another party, with that party's key in the value, paid to the pinned owner, without a later update: `NOTARY_VALUE_UNAUTHORIZED`. The same registration with a fee input that the owner signed beside the other party's `name_new` input refuses in the same way: a fee input is no name input. |
| S3-6 | The notary rotates `attest` under the same owner and signs again: admitted | The attestation under the old key refuses as `NOTARY_KEY`; refusing the new one because `attest` changed is wrong. |
| S3-7 | A complete walk on the verifier's node under a supported owner proof | One historical name transaction missing while every other read works; a node without the index; an unsupported script; a signature on the name input of another type than `SIGHASH_ALL` without `ANYONECANPAY`, one that does not commit to the value output included; a history supplied by the presenter: `NOTARY_HISTORY_UNAVAILABLE`, and the journal holds no closure afterwards. |
| S3-8 | The notary of the presented attestation is intact; another notary named by the same parent changed hands or cannot be read | The child is still admitted. A verifier that walks every named notary fails this. Run together with S4-2c of section 11.1. |
| S3-9 | An entry with name, registration and owner; a checkpoint in the active chain at or after the registration | A bare name: `CONTRACT_DELEGATE`. A checkpoint before the registration, and one not in the active chain: `NOTARY_CHECKPOINT`; a check that the hash merely exists is not enough. After a reorganisation that drops the checkpoint the child refuses without closure, and is admitted again when the block is back. |

## 8. The verifier's checks

A verifier runs every mechanical check itself, on its own node, before it
looks at the attestation. It then requires a valid attestation for every
child (D1) except a v4 child of a row without a certifier (J9, section 8.3).

Step 6d of LIP-0013 section 3.4 runs the binding of section 3.2, with the
rules that the contract's member set selects. A valid contract of either
profile therefore passes 6d, and a malformed one refuses there with its
contract code. The steps below follow 6d for a presented grant `C`. The
verifier stops at the first refusal; steps 6e to 6g then run against `C`.

| # | Step | Refusal |
| --- | --- | --- |
| V1 | `C`'s contract passed 6d. A contract of profile `/1`, and a contract of profile `/2` with an empty `parent_grant_id`, is a root: the remaining steps do not apply | none here; a contract that fails section 3.1 refused at 6d with the code of its rule |
| V2 | The bundle holds, as complete objects, `P`'s presentation and contract, the delegation request (v3), and each scope text whose hash is not empty; each object hashes to the value that names it | `DELEGATION_BUNDLE` |
| V3 | The `grant_id` recomputed from `P` equals `C.parent_grant_id` | `PARENT_ID_MISMATCH` |
| V4 | `P` has no parent and no id repeats; `P`'s contract has profile `/2` and `P.delegate.depth` is 1. A parent of profile `/1` carries no right of re-delegation | `CHAIN_DEPTH`, `NOT_DELEGABLE` |
| V5 | `P` passes the v3 check of LIP-0004 section 5 on the verifier's own node, with the pins taken from `P` and `P.grantee_key` as presenter, and then the binding of section 3.2 under the rules that `P`'s member set selects | `PARENT_NOT_LIVE` |
| V6 | Subject | `SUBJECT_MISMATCH` |
| V7 | The delegation request (v3) | `DELEGATION_REQUEST` |
| V8 | The ordinal lies between 1 and the number of rows of `P`; then the agent and the grantee are those of the child's row | `CHILD_ORDINAL`, then `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED` |
| V9 | Actions, repositories, the budget against the cap of the child's row, window | `CHILD_ACTIONS_WIDER`, `CHILD_REPOS_WIDER`, `CHILD_BUDGET_OVER`, `CHILD_WINDOW_NOT_NESTED` |
| V10 | An attestation is present | `CHILD_NOT_CERTIFIED` |
| V11 | The attestation has its canonical bytes; BIP-340 by `notary_key` verifies | `ATTESTATION_SHAPE`, then `ATTESTATION_SIGNATURE` |
| V12 | `notary_name` is the `name` of an entry of `P.delegate.notaries`; the checkpoint, the walk of the name and the writer of its value hold for that entry (section 7.1); the current value of that name on the verifier's node yields `notary_key` | `NOTARY_NOT_DESIGNATED`; then `NOTARY_CHECKPOINT`, `NOTARY_NAME_CHANGED`, `NOTARY_VALUE_UNAUTHORIZED`, `NOTARY_HISTORY_UNAVAILABLE`; then `NOTARY_KEY` |
| V13 | Independence, in this order: `notary_key` differs from `P.grantee_key`; `notary_key` differs from `C.grantee_key`; `notary_name` differs from `P.agent_name` and from `C.agent_name` | `NOTARY_IS_DELEGATOR`, `NOTARY_IS_DELEGATEE`, `NOTARY_IS_EXECUTOR` |
| V14 | Members 2 to 5 and 8 to 12 equal this case; `textual` agrees with the two text hashes | `ATTESTATION_BINDING` |
| V15 | Not used. Earlier revisions of this LIP checked a sum over siblings here, and the attestation carries none (J1.5). The steps after it keep their numbers | none |
| V16 | `tip_hash` is the active-chain block at `tip_height`; `tip_height` is at least the confirmation height of `C`'s issuance; `attested_at` is at most the verifier's clock plus 120 s | `ATTESTATION_TIP` |
| V17 | The anchor of section 6.4 is confirmed in the active chain and commits to this `attestation_id` | `ATTESTATION_ANCHOR` |
| V18 | `notary_seal` exists with the named script and is unspent, the mempool included, and the verifier's journal holds no withdrawal of this attestation (section 10) | `NOTARY_WITHDRAWN` |

V6 to V9 precede V10 on purpose. A child that is wider in an action, a
repository, a budget, a window or an ordinal refuses with that code even when
it carries a perfect attestation, as the control table of LIP-0012 requires.

An unconfirmed anchor and an unavailable node are pending. The executor holds
and retries under step 8 of LIP-0013; it does not refuse the child as not
certified.

Draft text under decisions that await the co-author's agreement changes these
steps, and each subsection says how. Section 3.4 adds the equality of the two
text hashes to V9 and limits `textual` in V14 (J5). Section 10.1 compares
`notary_name` with the row in V12 and adds the row's closure for cause to V18
(J2); until the co-author agrees, V12 accepts an attestation by any notary that
`P` names. Section 11.1 gives V7 its v4 counterpart, the child's signature
under the parent's delegation key (J4). Section 8.3, decided and agreed by both
owners on 2026-11-15 (J9), leaves out V10 to V18 for a v4 child of a row
without a certifier.

The table above is the table of v3. Version 0.1.55 proposes a table of its
own for a v4 child, in section 8.4: the steps F1 to F24 with their codes
and their order, for the signing service before it signs and for a verifier
at admission. Section 8.5 orders the checks of the signing service (J4.4),
section 8.6 holds the cases of the order, and section 8.7 the vectors that
are planned for it. The sentence above on V12, that it accepts an
attestation by any notary that `P` names until the co-author agrees, speaks
of the table of v3. For a reader of `swarma-grant/4` LIP-0020 section 11
carries J2 since version 0.1.53, and row F23 of section 8.4 reads V12 with
the notary of the row.

### 8.1. Why both are required

The verifier always re-checks because the check is deterministic: every input
is in the bundle or on the verifier's node, so two honest verifiers on one
chain reach one verdict. It also keeps the notary's power to the one thing
only a notary can do. If a verifier took the notary's word for subsets and
budgets, a stolen attestation key would widen any limit.

The attestation is required in addition, also when `textual` is `none` or
`identical`, for four reasons. The rule has no branch that a child can use to
skip certification. Every certified child has a seal that a party outside the
path can spend. No single verifier sees the siblings of a child; a notary sees
the children it certified itself and keeps a record of the one child that it
certified for each row (J1.6). With more than one named notary, a notary does
not see a child that another notary certified under the same ordinal; section
10.1 holds Draft text for that case, under a decision that awaits the
co-author's agreement (J2). A named party has recorded both contract hashes and
the tip it saw.

### 8.2. Where "not certified" is visible

1. **At admission.** A refusal is reported as its code only, as LIP-0013
   requires. `CHILD_NOT_CERTIFIED` means that no attestation was presented.
   The `ATTESTATION_` and `NOTARY_` codes mean that one was presented and
   failed.
2. **In the executor's own record.** For a refusal under V13 the record also
   names what collided: the delegator's key, the delegatee's key, the parent's
   agent name or the child's agent name. This detail stays local and is not
   sent to the grantee.
3. **In the receipt.** The record of LIP-0013 step 7 adds, for a child,
   `parent_grant_id`, `attestation_id` and `certification`, which is
   `CERTIFIED`. For a root it is `ROOT`. A refused child reaches no receipt.
4. **In shadow mode.** The executor runs every step and reports `CERTIFIED`,
   `ROOT`, `REFUSED` with the code, or `PENDING` to its owner. No peer message
   gains authority from the report.
5. **At the signer and the notary.** The signer refuses a request that fails
   section 4, with the same codes. A notary that refuses to certify returns
   the code to the delegator.

### 8.3. A row without a certifier (J9)

**Decided and agreed by both owners on 2026-11-15: J9.** Ivan Oparin decided
on 2026-11-15 that a child needs an attestation only where its row names a
certifier, and that a row may be without one only inside one owner. The
co-author agreed on 2026-11-15. The rules J9.1 to J9.4 are text in force for a
v4 parent. On v4 they narrow D1, and with it D2 and D3; they leave D8 and J1
as they stand, and the table below says how each of them is read for a row
without a certifier. Grant v3 and the contract profile
`swarma-trust-contract/2` do not change.

Under D1 alone a principal whose agent hands a review to another agent of the
same principal needs a notary's attestation, an anchor and a seal for that
child, although the notary is the principal's own (D8) and the principal pays
for all three (D11).

| # | Rule | Refusal |
| --- | --- | --- |
| J9.1 | The right of re-delegation of a v4 parent MUST state for each row whether the row names a certifier. A v4 child of a row that names a certifier MUST be admitted only with a valid attestation (D1). A v4 child of a row without a certifier needs no attestation. The principal signs the parent, so a delegator cannot drop a certifier. | A child of a row with a certifier: the codes of V10 to V18 |
| J9.2 | A v4 row without a certifier MUST have a recipient constraint that is limited to the issuer's own landlord: either a class with exactly the issuer's landlord, or an exact name that passes the landlord and holder checks of a class against the issuer's landlord. | Any other row without a certifier: the parent is refused (LIP-0026 R10.2). An exact name that fails a check: the code of that check (LIP-0026 R10.3), a proposal of that LIP |
| J9.3 | Across owners a certifier stays mandatory, as D8 says: a v4 row whose recipient constraint is not limited to the issuer's own landlord MUST name a certifier. | As J9.2 |
| J9.4 | The stop coin of a row (section 10.1, J2.7) belongs only to a row with a certifier. A row without a certifier states none. | |

The owner's practice, which is no rule: a certifier for rows whose children
permit effects, such as payments, the use of a model and landings, and none for
rows whose children permit instructions and reviews.

J9.2 names two recipient constraints, and both rest on J10 and J11. The class
is the third form of the recipient that J10 adds (LIP-0026 section 9). The
landlord and holder checks are the checks of a class under J10, and the holder
checks read the holders list of the landlord (J11; LIP-0010 section 10, since
version 0.1.53 a list of names that the landlord's value pins by hash, each
with its holder key and a seal, and no longer a member of the landlord
binding). A request key never meets J9.2. Until version 0.1.51 neither the
class nor the list was in force, and no child of a row without a certifier was
admitted. Since that version both are in force, by Ivan Oparin's decision of
2026-11-16 not to wait for the co-author: a child of a row without a certifier
is admitted where its recipient passes the checks of LIP-0026 section 9 for a
class, or of R10.3 for an exact name, and it needs no attestation (J9.1). That
admission rests on J9, which both owners agreed, and on J10 and J11, which the
co-author has not yet answered; the co-author's answer is folded in by
amendment. J12 does not bear on J9: a template states for the rows of its group
whether they name a certifier (LIP-0026 R10.1).

LIP-0026 section 10 states J9.1 to J9.4 on the facts of a v4 row, with the
class of landlords in its section 9 and the list of holders in LIP-0010 section
10. What follows is how J9 reads the other texts of this LIP.

| Text of this LIP | Under J9 |
| --- | --- |
| D1, "every child is certified" | A child of a row that names a certifier is admitted only with a valid attestation. A v4 child of a row without one needs none. Every v3 child is certified |
| D2 and D3, a parent names one to four notaries | A v4 parent none of whose rows names a certifier need pin no notary (LIP-0026 R10.1). A v4 parent with a row that names a certifier pins that notary, as D3 and section 7.1 say |
| D8, whose notary | Unchanged for a row with a certifier. D8 compares the owner of the issuer with the owner of the delegator; J9.2 compares the issuer's landlord with the recipient of the child. For a row without a certifier D8 has no notary to choose, and "one owner" is what a verifier establishes for the recipient of the child: its name is an agent of the issuer's landlord, a holder of that landlord holds it, and a holder wrote its value (LIP-0026 R10.2 and R10.3). "Across owners" in J9.3 is read for that recipient. The owner of the delegator is not tested (case S9-K1), and whether it should be is open |
| J1, a row fixes the certifier of its child (J1.1, section 9.1) | On v4 the certifier that J1.1 fixes for an ordinal is one of the pinned notaries or, where J9.2 holds, the statement that the row has none; either is signed in the parent. J1.2 to J1.5 and J1.8 apply to a row without a certifier unchanged, and so does the coin of J1.9, which keeps one child for each row on the active chain. J1.6 and the notary's record of J1.7 have no subject in a row without a certifier |
| Section 8, steps V10 to V18 | Not made for a v4 child of a row without a certifier; an attestation that is presented is not read. The steps before V10 keep their place, and the checks of LIP-0026 sections 9 and 10 are added |
| Section 10.1, the stop coin of a row | A row without a certifier states none (J9.4) |
| The contract profile `swarma-trust-contract/2` and its member `notary` | Unchanged. Each of its rows has the member `notary` (section 2), a right of re-delegation with depth 1 and no notary refuses as `DELEGATE_NO_NOTARY`, and every v3 child is certified. `notary` is a member of profile `/2` alone: a v4 row has no octets yet, and LIP-0026 R1.1 and R10.1 state its certifier, or that it has none, as a fact that the parent signs |

A v3 row without a notary would be another member set, and so another profile
string (LIP-0018 section 1). This draft proposes none.

Three things are lost or left open with a row without a certifier:

- **No second party.** The attestation is a second signature by a party
  that the issuer chose, with a seal that this party can spend. A row
  without a certifier has neither. Its child ends with its own seal, with
  the seal of its parent, or with its window. The mechanical checks of V6 to
  V9 and the coin of the row are unchanged.
- **The independence checks of V13** have no counterpart, because there is
  no notary to compare with the delegator, the recipient and the executor.
- **The owner of the delegator is not tested.** The decision limits the
  recipient of the child. A parent that a principal issues to an agent of
  another owner may hold such a row, and that agent then gives its children
  to agents of the principal alone.

| Case | Setting | Outcome |
| --- | --- | --- |
| S9-1 | A v4 parent with one row without a certifier, whose recipient is the class of the issuer's landlord. The child names a name that a holder of that landlord holds and whose value a holder wrote | Admitted without an attestation |
| S9-2 | The same child, presented with an attestation | Admitted; the attestation is not read |
| S9-3 | A row without a certifier whose recipient is a request key | The parent refuses |
| S9-4 | A row without a certifier whose class holds the issuer's landlord and a second landlord, and one whose class holds another landlord alone | The parent refuses |
| S9-5 | A row without a certifier whose recipient is an exact name, and the value of that name points to another landlord than the issuer | The child refuses, `CLASS_LANDLORD` |
| S9-6 | The same row. The value points to the issuer's landlord and a holder holds the name, and the operation that wrote the value spent an output of a key that is no holder | The child refuses, `CLASS_WRITER` |
| S9-K1 | A known limit. The recipient of the parent belongs to another owner, and the row is the one of S9-1 | Admitted |

The vectors of LIP-0026 section 11 hold these cases as decisions on stated
facts. The codes of S9-5 and S9-6 are proposals of that LIP. The vectors follow
J9 through the checks of J10 and the holders of J11, in force since version
0.1.51.

### 8.4. The steps of a v4 child (version 0.1.55)

Before version 0.1.55 a v4 child had no step table of its own. The table of
section 8 states the steps of v3, and notes in sections 8.3, 10.1, 11.1 and
11.2 and in LIP-0020 and LIP-0026 say how single steps read on v4. Five
questions had no answer in any text: the code of a contract that does not
recompute, whether a child may bind another contract than its parent, the
codes of a child that is wider than its parent in an action or in its
window, the place of the child-seal key, and where the coin of a row stands
relative to the attestation. This subsection proposes one table for a v4
child, and every rule, code and case of sections 8.4 to 8.7 names the row of
that table that it comes from. The table of section 8 stays as it is, for
v3.

**State: proposed by version 0.1.55.** Sections 8.4 to 8.7 are a proposal
of version 0.1.55. No rule, code or order that they add is in force by this
draft's own word: each binds a reader of `swarma-grant/4` when the version
lands, and the co-author's answer is folded in by amendment. The owner's
order of 2026-11-16 that Grant v4 does not wait covers the members of the
grant, as LIP-0020 section 11 says, and this unit does not stretch it to
its own steps, codes or counts.

Version 0.1.61 adds one part to this table and no row: part (c) of row F6,
the confirmed contract seal, with rule T11, pair Q28 and case S8-30. The
refusal that it carries is decision C12 of LIP-0017 (Ivan Oparin,
2026-11-17; the co-author agrees and leaves the judgement to Ivan, as
recorded with the event and quote in LIP-0017, "Decisions recorded"). The code name, the part and its place are proposals
of version 0.1.61, in the state of this section, and bind no reader by
this draft's own word. The part that version 0.1.55 numbered (c), the
valid contract and the mirror of the grant's terms, is part (d) since
this amendment. Because part (c) reads a node, it also stands in the
repeat of step 6 of the order of one request, between I3 and I5; the
enumerations of that step and of row I11 are amended in place for it and
marked there, their principle unchanged (section 8.5, "The repeat").

Each row of the tables below has one of three states, and its column
"Status" names it.

| Status | Meaning |
| --- | --- |
| Carried | The row restates a text that landed in an earlier version. Its order, its codes and what a refusal leaves behind are those of that text. The row has the state of that text and no other: decided by both owners, carried for a reader of `swarma-grant/4` by LIP-0020 section 11, or the proposal of a draft that binds no reader until it is accepted |
| **NEW** | The row decides something that no landed text decides. The cell gives the reason, and the open questions of this LIP name the choice for the owners |
| **Amends** | The row changes what a landed sentence says, and that sentence is amended in place by the same change and marked there. Of version 0.1.55 there are four: the sentence of section 11.1 on the place of the child checks of J4.3 (b) (rows F11 and F23, pair Q18); case S4-9 of section 11.2 on the seal of a child (rows F12 and F21, rule T5); step 3 of the order of one request of section 11.1, which gains one branch (section 8.5, I9 and I10; event 39); and step 6 of that order, which names the checks that it repeats and their observation, with rule J4.4 (c) and event 12 of the table of states beside it, whose words "the checks of J4.4 on the parent and on the row" step 6 reads as naming those checks (section 8.5, I11 and the paragraph "The repeat"). Until the version lands, the reading in force of each is the text as version 0.1.54 has it. Beside step 6, version 0.1.56 amends event 12 and step 6 further by one sentence each, marked there as normative text, on the coin spent by the confirmed issuance anchor of this child; rule J4.4 (c) keeps its words |

A row never states a second reading beside a landed one. Where two landed
texts leave a point undecided between them, the row says so and names the
open point; it does not decide the point under the status "Carried". An
order is called carried only where a cited sentence states that order. A
list of checks in one sentence is no order by itself: where a row or a pair
takes the order of such a list, it is marked **NEW**, and where it takes
none, the cell says "unordered". The order of steps
that no text had fixed was proposed by the consuming side on 2026-11-16,
and the list of pairs says where the table follows that proposal and where
it does not. By Ivan Oparin's decision of 2026-11-16 the window of a v4
grant is stated in block heights only; LIP-0008 section 7.1 holds the rule,
and no step of the table reads a clock for the validity of a grant.

**The predicate.** One predicate serves two moments. `ISSUE` is the moment
before the signing service of the delegation key signs a child (J4.4), and
the side that runs it is called the issuer here; it is not the issuer of
`P`, the party whose grant key signed the parent. `ADMIT` is every admission
of a request under the child at a verifier, which is called the consumer.
The inputs are the parent `P`, the child `C`, the contract that both bind,
the facts that the side reads on its own node in one observation (LIP-0022
section 1), its own journals, and the type profiles under which it runs.
Neither side takes a fact of a chain, a proof, a
policy or a verdict from the party that presents the child. A step marked
"both" is made by the issuer and by the consumer with the same inputs and
the same code. Five rows are marked with a part that one side does not make
or decides otherwise, and the cell "Side" states it: F2 (no signature
exists at `ISSUE`), F20 (a window that has not opened yet), and F21, F22
and F24 (facts that do not exist when a child is signed). For every other
part of every row the two sides give one code, outside two open points
under which they may differ: O7, a defect of the parent outside the group
of the child (F13), and O8, the class of `TIP_AGE` at `ISSUE` (F3). The
first step that refuses
ends the predicate and gives the code; a later step is not made, and its
code is not reported. A step with several parts makes them in the order in
which its row or its table states them, and the first part that refuses
gives the code. Three kinds of parts are excepted, and each row says which
of its parts they are: parts that the row calls unordered, whose order is
an open point (the three blocs of F21 and of part 7.6, open points O1 and
O6); parts that share one code, whose order decides no code; and the codes
of one step that the cited text lists without an order (F23).

Each step that a side makes has one place in the order of that side. The
consumer makes the steps in the order of the rows: F1 to F19, then A1, then
F20 to F24. The issuer makes the rows that are marked for it in the same
order, with the identification of its caller, I0, before F1 and the check
of the caller's list, I2, between F2 and F3; section 8.5 states that order
step by step, as the inner order of step 1 of the order of one request of
section 11.1. The issuer has no place for A1 and for F23, which it does not
make. Two steps authenticate the operation and are no steps of the
predicate: A1 at `ADMIT` and, at `ISSUE`, I0 with I2. They are different checks of
different operations, each has one place in the order of its side, and
neither side makes the other's. At `ISSUE` the check of the caller reads
no node and stands before F3, and at `ADMIT` the authentication of the
request stands after F3 (pair Q21). F3 itself has one place on both sides,
after the documents and before F5 to F24 and A1. That place is the place of
its codes. No row of this table states a rule that asks for a minimum
confirmation depth, and the members of `swarma-grant/4` sign none (LIP-0020
section 11), so `CONFIRMATIONS` of LIP-0022 B5.2 has no row: by B6.2 it
stands where a rule that asks for a depth stands, and it enters the table
with the first such rule. An observation ends with a second read of the tip (LIP-0022
B1.1), so a side can learn that it is void after a later step has refused.
A side therefore ends its observation before it reports a refusal of F5 to
F24 or of A1, and where a code of F3 then applies it reports that code and not the later
one (LIP-0022 B6.1).

**Five kinds of refusal.** The column "Again" says what a refusal leaves
behind. A cell that says "open" belongs to a refusal whose code is open,
and the list of open points after the pairs names it.

| Mark | Meaning |
| --- | --- |
| no | The octets decide. The same documents refuse again at every reader and at every time |
| input | A document that the step needs was not presented. The refusal says nothing about the grants and records no closure. The same grants, presented completely, are decided anew |
| state | The chain or a name as it stands decides. The refusal records no closure, and a later observation decides again |
| pending | A read proved nothing. The side refuses this admission, records no closure, and reports neither a revocation nor a missing parent. It reads again; a signing service does not sign and an executor performs no effect on the strength of a retry that it did not make. There is no result of its own for an unavailable read: the code is that of the read |
| closed | The verifier's journal holds a closure. The refusal repeats at that verifier whatever a later view shows |

The steps are named F1 to F24, and A1 stands between F19 and F20. The row
of a child is the row that its ordinal selects (LIP-0026 R8.3, R8.8).

| # | Step | Reads | Side | On success | Refusal | Again | Not yet observed | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | The parent as a document: the pipeline of a signed object (LIP-0020 W9.1, W11.8), steps 1 to 8, and of step 9 the rules of every grant (W11.9) and then rules 1 and 3 of W11.10, the forms of `delegate.actions` and of `notaries`. The row reads no fact of a chain. Rules 2 and 4 to 8 of W11.10, the rules of the pools, the groups and the ranges, are no part of this row at an admission: F13 judges rules 4 and 5 for the group and the range of the child, and open point O7 holds the rest (rule T10) | The signed form of `P`, octets alone | both | `P` is a signed grant with a right of re-delegation, its identifier is recomputed, and its signature holds under `issuer.grant_key` | The codes of that pipeline, in its order: `WIRE_SIZE` to `WIRE_ID`; then `GRANT_SHAPE`; then `GRANT_DELEGATE` for rules 1 and 3 of W11.10 | no | The child, the contract, every fact of a node; the groups and the ranges of `P` | Carried: LIP-0020 W9.1, W11.8 and W11.9; W11.8, step 6, reads a child under the key of "the parent that the reader has already read through this pipeline". **NEW** (rule T10): which rules of W11.10 the admission of a child asks for, and at which step. LIP-0020 W11.10 says that the result of the pipeline "does not say what a verifier must have read before it admits a child" and leaves that to proposal Q1 of LIP-0026, which is pending; under the profile in force a verifier "checks only the group and the range of its child" (LIP-0026 section 8), and the refusal of a whole parent is unavailable (LIP-0026, "Owner decision proposals"). This row therefore asks of W11.10 for the two forms that F16 and F23 read and for nothing of a group, and it decides nothing of Q1. The earlier drafts of this row refused a child for a defect in a group that its ordinal does not select; that requirement is withdrawn, and the row contradicts no sentence in force |
| F2 | The child as a document. At `ADMIT`: the signed form, through the pipeline of a signed object with the points of W11.8 for a child. At `ISSUE`: the payload, read in the five steps of rule T7 | The octets of `C`; from F1 the identifier of `P` and `delegate.key` | both; steps 2, 5 and 7 of the pipeline at the consumer alone, because the issuer makes the signature only in step 7 of the order of one request (section 11.1), after every check | `C` is a well-formed child that names `P` and, at `ADMIT`, is signed by the delegation key of `P` | Steps 1 to 5: the `WIRE_` codes. Step 6: `WIRE_ID`, also for a child that is presented without its parent; then `CHAIN_DEPTH`; then `NOT_DELEGABLE`. Step 7: `CHILD_SIGNER`. Step 8: no finding in this row on either side; the one reference from a child, to its parent, stands in step 6 (W11.8), and a reference to `C` from another object, the `grant_id` of a preparation (LIP-0020 W8.1), is judged where that object is read, in bloc (i) of F21. Step 9: `GRANT_SHAPE` | no; input for a child that is presented without its parent (`WIRE_ID`): the same child, presented with its parent, is decided anew | The contract, every fact of a node | Carried at `ADMIT`: LIP-0020 W9.1 and W11.8. **NEW** at `ISSUE` (rule T7): no pipeline class of LIP-0020 W9.1 reads a payload that is still to be signed |
| F3 | The observation: the reads of this admission belong to one healthy observation on the pinned chain (LIP-0022 sections 1 to 3). The pinned chain is that of `genesis` of `P`, which F1 read | The side's own node and its comparison nodes; `genesis` of `P` | both | Every later read is a read of this observation | `OBSERVATION_CHAIN`, `OBSERVATION_VOID`, `NODE_UNHEALTHY`, `NODE_DISAGREEMENT`, `OBSERVATION_CLOCK`, `TIP_AGE`, in the order of LIP-0022 B6.1. At `ISSUE` the class under which `TIP_AGE` is judged is open (open point O8) | pending; `OBSERVATION_CHAIN` is state | Every fact of a name, a coin, a seal or an anchor | Carried: LIP-0022 sections 1 to 3 and B6.1, the proposal of that draft, for the six codes, their order and their place before every rule of a grant that is computed in the observation (pair Q3). **NEW**: F1 and F2 stand before F3 (pair Q1), although step 9 of their pipeline judges rules of a grant (LIP-0020 W11.9, W11.10). B6.1 withholds "a refusal of another rule that was computed in an observation which one of the six refuses"; a refusal of a document is computed in no observation, and F3 takes the pinned chain from `genesis` of `P`. The line between the reading of documents, before F3, and the rules of an admission, after it, is this table's reading of B6.1 |
| F4 | Not used. The first draft of this table put the authentication of the operation here. It is A1 at `ADMIT`, after F19, and I0 with I2 of section 8.5 at `ISSUE`. The steps after it keep their numbers | Nothing | none | None: no check is made | None | None | Nothing: the row is no step | Withdrawn inside version 0.1.55; no landed text named the row |
| F5 | The same contract: the member `contract` of `C` equals the member `contract` of `P`. The comparison is of the two values of that member as the two payloads hold them, 64 hexadecimal characters each (LIP-0020 W11.2), and of no octet of a contract document (LIP-0020 W11.11, rule 1) | Signed octets of `P` and `C` | both | The path binds one contract identifier | `CHILD_CONTRACT_DIFFERS` | no | Whether a contract is presented; whether `P` is live; the rows | **NEW** rule, **NEW** code, **NEW** place (LIP-0020 W11.11, rule 1; pair Q5). No landed text says that a child binds the contract of its parent, and the agreed point of section 3.4 fixes no byte |
| F6 | The contract binding, in four parts in this order. (a) The contract document for the identifier F5 found in both grants, and any framework document it names, are presented or resolved. (b) Their complete octets, as presented and without normalisation, recompute to their respective identifiers under LIP-0017 section 2. (c) The bound contract, then its named framework contract, each names a seal that the side's own node shows confirmed as named in this observation, under LIP-0017 section 6, rule 6, and T11 below. (d) The bound document is a valid contract of its profile and mirrors the terms of each grant (LIP-0008 sections 2 and 7.1; LIP-0017 section 5) | Both required documents; `contract` of `C` and `P`; for (c) the side's own node | both | Both grants are held against their bound contract and any framework it names, each with its named seal confirmed as named | (a) `CONTRACT_NOT_PRESENTED`, including a missing named framework document. (b) `CONTRACT_ID`, including a framework identifier mismatch. (c) No seal named: `CONTRACT_SEAL_MISSING`; otherwise an inconclusive read: `CONTRACT_SEAL_UNAVAILABLE`; only a conclusive read may give `CONTRACT_SEAL_MISSING` for a node finding. The definitions are LIP-0020 W11.11; neither records closure. No part of this row judges spend state (T11). (d) Open: no code and no rule text until a v4 contract profile exists (T1). A side unable to compute (b), every side under version 0.1.55, ends the predicate there without a code or closure; it signs and admits nothing (O4) | input for (a); no for (b); for (c), no when no seal is named, state for a conclusive node finding, pending for `CONTRACT_SEAL_UNAVAILABLE`; open for (d). The profile-dependent end without a code is none of these marks and lasts until the profile exists | Whether `P` is live; the rows | **NEW** rule form, codes and place (T1; Q6). Parts (b) and (d) still wait for a v4 contract profile: every result at or after (b) in a case or vector is on stated facts (section 8.6). Part (c) and framework presentation/recomputation in (a)/(b) are proposals of 0.1.61. The refusal at the signing service and every verifier is C12 of LIP-0017 (Ivan Oparin, 2026-11-17; the co-author agrees and leaves the judgement to Ivan); the code names, retry marks and position after (b), before (d), are **NEW** proposals (T11; Q28). Through 0.1.60 the valid-contract part was (c); since this amendment it is (d), and earlier texts citing (c) mean that part |
| F7 | The parent is live: `P` passes, on the side's own node, the rules that admit a v4 grant, in the six parts and in the order of the table "Inside F7" below. The row judges `P` as a grant. It reads no coin, no stop coin and no name of any row (LIP-0026 R8.8) | The node; the journals of the side; `issuer`, `recipient`, `recent_block`, the window and `seal` of `P`; the presentation of `P` | both | `P` is a live grant at the tip `H` | The code of the first part that refuses, as the table "Inside F7" gives it. `PARENT_NOT_LIVE` is the code of four findings and of no other: a recipient name of `P` that its signed owner key does not hold, a journaled closure of `P`, a window of `P` that the tip is outside of or that opens below its recent block, and a spent seal of `P` | As the table "Inside F7" gives it for each part | Anything of `C` beyond F2 and F5 | Carried in each part, with the state of the text that the part cites. **NEW** (rule T8): the order of the six parts as one order, and that a refusal of `P` at the admission of a child keeps the code of the rule that refused it |
| F8 | The subject: `genesis` of `C` equals `genesis` of `P` | Signed octets | both | One chain along the path | `SUBJECT_MISMATCH` (rule T2) | no | The keys, the rows | Carried rule: LIP-0008 section 12.2, "The subject MUST remain constant". **NEW** code assignment and place (LIP-0020 W11.11, rule 4; rules T2 and T4; pair Q8) |
| F9 | The keys of the parent, J4.3 (a): the delegation key differs, by x coordinate, from `issuer.grant_key`, from `recipient.key` or `recipient.owner`, from `issuer.owner`, from the `owner` of every entry of `notaries` and from `seal.key` of `P` | Signed octets of `P` | both | `P` is usable as a parent under J4.3 (a) | `DELEGATE_KEY_REUSE` | no | The child-seal key; the rows | Carried: J4.3 (a), which LIP-0020 section 11 carries for a reader of `swarma-grant/4`; the place is that of V7 (section 11.1) |
| F10 | The child-seal key of the parent: first `delegate.child_seal_key` is present (CS1); then it differs, by x coordinate, from the delegation key and from the keys of F9 (CS3) | Signed octets of `P` | both | `P` names a child-seal key that no other role holds | CS1: `CHILD_SEAL_KEY`. CS3: `DELEGATE_KEY_REUSE` | no | The seal of `C`; the rows | Carried rules: CS1 and CS3, which LIP-0020 section 11 carries. **NEW**: the place and the inner order, the key present before it is compared (pairs Q9 and Q10) |
| F11 | The keys of the child, J4.3 (b), as far as no attestation is read: the delegation key differs, by x coordinate, from `seal.key` of `C`, from `recipient.key` or `recipient.owner` of `C`, and then, where `P` names its recipient by name, from every channel key that the value of that name yields. That value is the one that part 7.3 of F7 read in this observation, and F11 makes no read of its own. The comparison with the attestation key of the row's notary stands in F23 | Signed octets of `P` and `C`; the value of the name of `P`'s recipient as part 7.3 read it | both | The delegation key holds no second role at this admission | `DELEGATE_KEY_REUSE`, without closure | no for the octets; state for a channel key | The rows; the attestation | Carried: J4.3 (b) at the place of V7. **Amends** section 11.1 for the one comparison that moves to F23 (pair Q18) |
| F12 | The seal key of the child, CS2 as far as octets decide it: `seal.key` of `C` equals `delegate.child_seal_key` of `P`, octet for octet, the parity octet included | Signed octets | both | The seal key that `C` states is the child-seal key of `P` | `CHILD_SEAL_KEY` | no | The rows; the script of the seal on a node (F21) | Carried: CS2 and LIP-0008 SB1, "for a child the seal public key is the child-seal key of its parent". **NEW** in two points (rule T5): CS2 is split between this row and F21, and the equality includes the parity octet. **Amends** case S4-9 of section 11.2, whose first refusal now names the key that the child states (rule T5) |
| F13 | The row of the child, in two parts in this order. (a) The ordinal lies between 1 and the number of rows of `P`, the sum of the counts of all its ranges. No template is read before this. The ordinal then selects the group, the range and the coin (LIP-0026 R2.1, R8.3, R8.8). (b) The selected group and the selected range meet rules 4 and 5 of LIP-0020 W11.10: the template of that group, and that range with its `stop` | `ordinal` of `C`; the `count` of every range of `P`; for (b) the template of the selected group and the selected range | both | The row of `C` is known, and its group and its range are well-formed | (a) `CHILD_ORDINAL`. (b) `GRANT_DELEGATE`; a proposal point of rule 5 of W11.10 keeps its two outcomes. A finding of rules 2 and 6 to 8 of W11.10, whether or not octets of the selected group or range take part in it, and a finding of rules 4 and 5 in another group or range: open point O7 | no | Whether `C` fits the template (F14 to F18); the coin on a node | Carried for (a): the bound and its code are LIP-0026 R2.1 (J1.2). The order of the count that makes an ordinal name a row is that of R8.3; LIP-0026 section 8 states its state in one place: in force since version 0.1.57, by the owner's decision of 2026-11-17. LIP-0020 W11.6 states the same order for the octets of a parent. The selection of R8.8 is the text of proposal Q2 of LIP-0026, and that a verifier binds the ordinal to the signed template, range and coin as one signed binding is the other pending part of that proposal; the row has that state. For (b) the rules are carried: rules 4 and 5 of W11.10, which "every reader" of LIP-0020 section 11 judges, with the state that section gives them. **NEW** (rule T10): their place here at an admission, for the group and the range of the child alone, which is what the profile in force has a verifier check (LIP-0026 section 8) |
| F14 | The executor of `C` is that of the template of its row: the same name and the same key (R2.2) | Signed octets | both | `C` names the executor of its row | `CHILD_AGENT_NOT_ALLOWED` | no | The recipient, the limits | Carried: LIP-0026 R2.2 and R2.5 (J1.2) |
| F15 | The recipient of `C` is that of the template: the same mode, and in it the same request key or the same name with the same owner key; for a class, a recipient by name (R2.3, R9.3). No name is read here | Signed octets | both | `C` names the recipient of its row, as far as signed octets say it | `CHILD_GRANTEE_NOT_ALLOWED` | no | Whether the name is held, and by whom | Carried: LIP-0026 R2.3 and R2.5 (J1.2); R9.3 for a class (J10) |
| F16 | Every entry of `actions` of `C` is an entry of `delegate.actions` of `P`, compared as texts (LIP-0020 W11.11, rule 2). An empty list passes | Signed octets | both | The actions of `C` are a subset of the delegable actions of `P` | `CHILD_ACTIONS_WIDER` | no | Whether an action is defined (E1) | Carried rule: LIP-0008 section 12.2, "Known action sets and numeric ceilings MUST NOT widen in a child". **NEW** code assignment and place among the checks of a row (rule T4; pair Q12) |
| F17 | The limits of `C` against the template of its row, in three parts in this order. (a) Every limit of `C` has the key of a limit of the template; a limit of `C` whose key the template lacks refuses at any amount, 0 included (R2.4). (b) The kind of every limit of `C` and of the template has a type profile at the side (LIP-0020 W11.4, W11.14). (c) Each amount of `C` stands to the amount of the template under the same key as the profile of its kind says: for a ceiling, it is at most that amount (R2.4); for a floor, the relation of its profile | Signed octets; for (b) and (c) the type profiles of the side | both | Every limit of `C` lies within a limit of its row, under profiles that the side has | (a) `CHILD_BUDGET_OVER`. (b) `LIMIT_KIND_UNDEFINED`. (c) `CHILD_BUDGET_OVER` | no; for (b) and (c), no under one set of profiles | Any account | Carried: R2.4 for (a) and for the ceilings of (c). **NEW** (rule T9): part (b), with its code and its place; that a floor is not compared as a ceiling; and the code of a floor that fails the relation of its profile, `CHILD_BUDGET_OVER`, which R2.4 gives to ceilings alone |
| F18 | The window of `C` lies inside that of `P`, in heights: `P.not_before_height <= C.not_before_height` and `C.not_after_height <= P.not_after_height` (LIP-0020 W11.11, rule 3). F2 already holds `C.not_before_height < C.not_after_height` | Signed octets | both | `C` fits `P` on signed octets | `CHILD_WINDOW_NOT_NESTED` | no | The tip; every fact of a node about `C` | Carried rule: LIP-0008 section 7.1, rule 4, and section 12.5, "A child interval MUST NOT widen its parent's". **NEW** code assignment and place (rule T4; pair Q12) |
| F19 | The recipient of the child on the node, in this order (LIP-0026 R9.9). (a) For a recipient by name, the proof of LIP-0021 O7.2. This is the one place of that proof for `C`. (b) For a row with a class, the checks (a) to (d) of LIP-0026 section 9. (c) For a row without a certifier and with an exact name, the full checks (a) to (d) of that section with the issuer of `P` as the landlord. A recipient by key reads nothing here | The node; the holder journal; the names of the recipient and of the landlord; `recent_block` of `P` | both | The recipient is a party that the row admits | (a) `RECIPIENT_NAME_NOT_HELD`, `RECIPIENT_NAME_UNAVAILABLE`. (b) and (c): the codes of LIP-0026 section 9 and of LIP-0010 section 10.6, in the order of R9.9 | state; closed for `HOLDER_REVOKED`; pending for `RECIPIENT_NAME_UNAVAILABLE`, `CLASS_HISTORY_UNAVAILABLE`, `LIST_UNKNOWN`; for the codes of a journal that is lost or fenced, what LIP-0010 section 10.6 says of them | The request; the seal, the anchor, the coin, the attestation | Carried, each part with the state of its text. The four class checks and their order are J10. The eight class codes and their inner precedence are proposal Q4 of LIP-0026, and the checkpoint of a class is proposal Q3; both are pending, and the row reports the codes as those proposals have them. For (c) the profile in force runs the full class checks; the shortcut of R10.3 is a proposal, and this row does not use it. **NEW**: the row is a duty of the issuer as well (section 8.5, I8) |
| A1 | At `ADMIT` alone, and no step of the predicate: the request is authenticated under the recipient mode of `C` (LIP-0008 section 4, step 2). By key: under the signed request key. By name: under the key that the value read in F19 yields for the channel of the request; for a row with a class that is the value whose writer check (d) judged (LIP-0026 R9.10) | The request; `recipient` of `C`; the value of the recipient name as F19 read it | consumer. The issuer has no request; its own operation is authenticated in I0 and I2 (section 8.5), before F3 | The request comes from the recipient of `C` | The refusal of the request's authentication: a wrong key, an unknown channel, a removed key. Open: the code comes with the members of the invocation (LIP-0020 section 3) and is not assigned here. The refusal is never reported as `CHILD_GRANTEE_NOT_ALLOWED` or as a code of F19 | open, with the code | Whether `C` is live; the seal, the coin, the attestation | Carried place: LIP-0008 section 4, "Admission order", authenticates the request in its numbered step 2, after the names of step 1 and before the checks of step 4. **NEW** against the proposal of the consuming side, which authenticates before the checks of a row (pair Q4). **NEW** as a reading: the place after F3, where the same section numbers "Require healthy observations" as step 3 (pair Q21) |
| F20 | The child is live as a grant, in four parts in this order. (a) The side's journal holds no closure of `C` (LIP-0008 section 5.1). (b) The recent block of `C` is a block of the active chain of the observation, with the height `R` (LIP-0022 B4.2). (c) `R <= C.not_before_height` (LIP-0008 section 7.1, rule 3). (d) The tip `H` against the window (LIP-0008 section 7.1, rule 2; section 12.5). At `ADMIT`: `C.not_before_height <= H < C.not_after_height`. At `ISSUE`: `H < C.not_after_height` alone | The journal; the node; `recent_block` and the window of `C` | both. The sides differ in (d) by design (rule T3): the issuer signs a child whose window has not opened yet, and the consumer refuses that child until the tip reaches `C.not_before_height` | At `ADMIT`: `C` is inside its own window and not closed. At `ISSUE`: `C` is not closed and not backdated, and its window has not ended | (a) `CHILD_NOT_LIVE`. A journal of closures that cannot be read, or that cannot show its continuity, admits nothing (LIP-0008 section 5.1); that refusal has no code (open point O5). (b) `RECENT_BLOCK`. (c) `CHILD_NOT_LIVE`. (d) `CHILD_NOT_LIVE` | closed for (a); open, with the code, for a journal that cannot be read; state for (b), (c) and (d). A refusal of (c) changes only with a reorganisation that moves the recent block | The seal as an output, the anchor, the coin | Carried rules: LIP-0008 sections 5.1, 7.1 and 12.5; LIP-0022 B4.2. Carried place: (b) before (c) and (d) by LIP-0022 B6.2. **NEW** places (pair Q24): (a) before (b), and (c) before (d). Step 4 of LIP-0008 section 4 names the journal and the interval in one list, and that list states no order. **NEW** (rule T3): the code, its use for (c), and the rule of the issuer in (d) |
| F21 | The seal and the issuance of the child, in three blocs. The blocs are unordered against each other: the letters name them and state no order (open point O1). (s) The output at `seal.outpoint` exists with the single-key script of the profile for `seal.key`, and the profile and the kind are supported (LIP-0008 SB2; CS2). (w) The seal transaction and the anchor pass LIP-0023, in the order of its C7.1. (i) A reference to the grant from another object of the presentation, the `grant_id` of a preparation, equals the identifier of `C` (step 8 of the pipeline, LIP-0020 W11.8 and W8.1); then the presentation passes steps 2 to 6 of LIP-0020 W9.4 in their order; and the anchor stands in the window of the recent block (LIP-0022 B4.3). A validated spend of the seal closes `C` (CS5) | The node; the presentation of `C` | consumer for the whole step. The issuer makes bloc (s) alone, as its duty before it signs (section 8.5, I8); no anchor of `C` exists then | `C` is issued on the active chain, and its seal is the one that CS2 asks for | (s) `SEAL_OUTPUT`, then `SEAL_SCRIPT`, then `SEAL_PROFILE`, as LIP-0008 SB2 names them and LIP-0024 E3.1 orders them. (w) The codes of LIP-0023 section 7. (i) `WIRE_ID` for the reference; `ISSUANCE_MODE`; the codes of the pipeline of the assent as a signed object, then `ASSENT_BINDING`, `ASSENT_PARTY`; `CONSENT_SHAPE`, `CONSENT_BINDING`, `CONSENT_KEY`, `CONSENT_EVIDENCE`, `CONSENT_SIGNATURE`, `CONSENT_TIME`; `ISSUANCE_FRAME`; `ISSUANCE_COMMITMENT`; and `RECENT_BLOCK_WINDOW`. A spent seal: `CHILD_NOT_LIVE` | As the text of each code gives it: no where the octets of the presentation decide, state where the node decides; closed for a validated spend of the seal; pending for `W_ANCHOR_PENDING` and for `SEAL_OUTPUT`, which proves nothing about the seal (LIP-0024 section 3) | Which input of the anchor spends the coin | Carried inside each bloc. Four orders across the blocs are carried: a spend is classified only after (s) and the signature (LIP-0008 SB3); `RECENT_BLOCK_WINDOW` stands after the read of the anchor (LIP-0022 B6.2); `ISSUANCE_FRAME` stands where W9.4 puts it (LIP-0023 section 7); and the consent of the child's recipient has this one place at a consumer, step 4 of W9.4. **NEW** as a stated place: the reference of step 8 at the head of bloc (i), where the object that holds it is read. Unordered, and open by name: (s) against (w), (s) against (i), and (w) against (i) (open point O1); and the classification of a validated spend against (w) and against (i), which LIP-0008 SB3 orders after (s) alone (open point O6). Open with LIP-0020 W7.2: which key assents to the contract of a child. Until that is decided, step 3 of W9.4 names no party for a child, and no case holds a defect of it |
| F22 | The coin of the row, in the order of LIP-0026 R6.1: it is no output of the child's seal transaction (R3.4); it is on the active chain as the range states it, at or below the recent block of `P` (R3.2); one input of the confirmed anchor of `C` spends it (R3.3) | Signed octets for R3.4; the node; the anchor of `C` | consumer. At `ISSUE` the issuer makes R3.4 and R3.2 and does not make R3.3: no anchor exists, and a plan of one is no fact. In its place the issuer reads that the output of the coin is unspent in its observation, or that the confirmed issuance anchor of `C` has spent it, which is the case of a replay after publication (section 8.5, I9): a coin that another transaction has spent is a coin that no anchor of `C` can spend | The issuance of `C` is the one issuance of its row on the active chain. At `ISSUE`: the coin is there and can still be spent | `ROW_COIN_IN_SEAL_TRANSACTION`, then `ROW_COIN`, then `ROW_COIN_REQUIRED`. At `ISSUE` the last code reports a coin that another transaction than the confirmed anchor of `C` has spent | no for R3.4; state for the others | The attestation | Carried: LIP-0026 R6.1, the proposal of that draft, for the inner order and for the place after the checks of LIP-0023 (pair Q15). Carried as a duty of the issuer: section 11.1, "that the coin of a row is unspent is read on a node, by the service under J4.4 and by every verifier at use". **NEW**: the place before the attestation (rule T6); the part of the issuer (section 8.5, I9); and the code of a spent coin at `ISSUE`, `ROW_COIN_REQUIRED`, the code that a consumer reports for the same coin once an anchor exists (case S8-18). How a node is read for an unspent output against one tip is open in LIP-0022 and LIP-0027 |
| F23 | The certifier. A row without a certifier ends the predicate here: F23 and F24 are not made, and an attestation that is presented is not read (J9.1; LIP-0026 R10.4). For a row with a certifier, steps V10 to V17 of section 8 in their order, with the notary of the row in V12 (J2.2, section 10.1), and after V12 the last comparison of J4.3 (b): the delegation key differs from the attestation key that this notary yields | The attestation; the node; `notaries` and `certifier` of `P` | consumer | The child is certified by the notary of its row | `CHILD_NOT_CERTIFIED`; then the codes of V11 and V12; then `DELEGATE_KEY_REUSE`; then the codes of V13 to V17 | no for the shape, the signature and the binding; state for the name, the tip and the anchor; pending for `NOTARY_HISTORY_UNAVAILABLE` and an unconfirmed anchor | The stop coin and the seal of the attestation | Carried: steps V10 to V17; J9.1 for a row without a certifier, where the sentence of R10.4 that a presented attestation is not read is a proposal of LIP-0026. The notary of the row in V12 is J2.2, which LIP-0020 section 11 carries for a reader of `swarma-grant/4` since version 0.1.53; the note under the table of section 8, which lets V12 accept any pinned notary until the co-author agrees, speaks of v3. The order of the codes inside V11 and V13 is stated by the table of section 8 ("then", "in this order"). The four middle codes of V12, `NOTARY_CHECKPOINT`, `NOTARY_NAME_CHANGED`, `NOTARY_VALUE_UNAUTHORIZED` and `NOTARY_HISTORY_UNAVAILABLE`, are listed there without an order among themselves: they are unordered here as well, and no case holds two of them. **Amends** section 11.1 for the place of the last comparison of J4.3 (b) (pair Q18) |
| F24 | The end of the row and of the attestation: the checks of the stop coin in the order of LIP-0027 H2.7, and then step V18 | The journal of closures; signed octets for H2.2; the node | consumer for the whole step. The issuer makes the checks of the stop coin and not V18 | The row is not ended, and the attestation is not withdrawn | `JOURNAL_LOST`, `JOURNAL_FENCED`, then `ROW_CLOSED_FOR_CAUSE` from the journal; `ROW_STOP_ALIAS`; `ROW_STOP`; `ROW_CLOSED_FOR_CAUSE` for a spent coin; then `NOTARY_WITHDRAWN` | closed for `ROW_CLOSED_FOR_CAUSE`; no for `ROW_STOP_ALIAS`; state for the others | Whether the request fits an account | Carried: LIP-0027 H2.7 and H5.1, the proposal of that draft, and step V18. **NEW**: the part of the issuer beyond the closure for cause that J4.4 names, that is the checks H2.2 to H2.4 (section 8.5, I9) |

**Inside F7.** The six parts of F7 stand in this order. A part that refuses
ends F7 and gives the code of the child's admission.

| Part | Check | Refusal | Again | Source of the place |
| --- | --- | --- | --- | --- |
| 7.1 | The recent block of `P` is a block of the active chain of the observation; its height is `R` (LIP-0022 B4.2) | `RECENT_BLOCK` | state | Carried: LIP-0022 B6.2, `RECENT_BLOCK` stands before every rule that uses `R`, the window and the walk of the issuer's name among them |
| 7.2 | The issuer rule: the findings of LIP-0021 O7.1 in the order of its rows (LIP-0008 section 3). The Draft text of LIP-0008 section 5.2 (J6) is no part of this row, on either side: neither its journal of closures of an issuer's name, nor its read of the pending operations of the name (J6.4), nor its code `ISSUER_NAME_CLOSED`. That section says of itself that until the co-author agrees the text in force stands. When it is accepted, it enters this part whole and by amendment: J6.1, J6.4 and J6.9 together | `ISSUER_NAME_CHANGED`, `ISSUER_SNAPSHOT`, `ISSUER_HISTORY_UNAVAILABLE`, as O7.1 orders them | state for the first two; pending for `ISSUER_HISTORY_UNAVAILABLE` | Carried: LIP-0008 section 4, numbered step 1, and B6.2 for the place after 7.1; the inner order is LIP-0021 O7.1, the proposal of that draft. J4.4 names, for the signing service, the closures of an issuer's name "under LIP-0008 section 5.2"; that journal exists at a side once that section is in force, and until then J4.4 finds none there |
| 7.3 | Where `P` names its recipient by name: the current output of that name reads as controlled by the signed owner key (LIP-0021 O7.2) | Rows 1 and 2 of O7.2: `PARENT_NOT_LIVE` (J4.5, case S4-4). Row 3: `RECIPIENT_NAME_UNAVAILABLE` | state; pending for row 3 | Carried: LIP-0008 section 4, numbered step 1, holds both names. **NEW**: the order inside that step, the name of the issuer before that of the recipient; the step names them in that sequence and states no order. The reason is that the issuer rule decides whether `P` is a grant of its issuer at all. The code of rows 1 and 2 is that of J4.5, which LIP-0020 section 11 carries and which names the code for a child; `RECIPIENT_NAME_NOT_HELD`, which LIP-0021 proposes, is the code of the recipient of the grant that is being admitted (F19). **NEW**: J4.5 speaks of a change of the owner, and a name without a live output, row 1, takes the same code |
| 7.4 | The side's journal holds no closure of `P` (LIP-0008 section 5.1). A journal that cannot be read, or that cannot show its continuity, admits nothing | `PARENT_NOT_LIVE`. For a journal that cannot be read: no code (open point O5) | closed; open, with the code, for a journal that cannot be read | Carried: the names of numbered step 1 of LIP-0008 section 4 stand before the checks of its step 4, of which the journal is one. **NEW** (rule T8): the code |
| 7.5 | The window of `P`: `R <= P.not_before_height <= H < P.not_after_height` (LIP-0008 section 7.1, rules 2 and 3) | `PARENT_NOT_LIVE` | state | **NEW** place (pair Q22): the journal before the window. Step 4 of LIP-0008 section 4 names both in one list, and that list states no order; a closure in the journal is reported before a finding that a later tip or a reorganisation may change. **NEW** (rule T8): the code. No landed text names a v4 code for a grant outside its window; the code is that of step V5 for a parent that does not pass |
| 7.6 | The seal and the issuance of `P`, in the three blocs of F21, unordered against each other as they are there: LIP-0008 SB2; LIP-0023; the reference of step 8 and steps 2 to 6 of LIP-0020 W9.4 with LIP-0022 B4.3. A validated spend of the seal closes `P` (LIP-0008 SB3 and section 5.1) | The codes of F21 for the three blocs. A spent seal: `PARENT_NOT_LIVE` (case S4-6) | As F21 gives it for each code; closed for a validated spend; pending for `W_ANCHOR_PENDING` and `SEAL_OUTPUT` | **NEW** place (pair Q22): the window before the seal and the issuance, which the list of step 4 does not order; the window reads the tip alone, and a grant outside its window is refused whatever its seal shows. The orders inside this part are those of F21, with the same four carried orders and the same open points O1 and O6 |

A side that passes its last step holds "the child is admitted" for this
observation and for nothing wider. At `ISSUE` that result is the pass of
step 1 of the order of one request (section 11.1), and by itself it permits
no signature: whether the service signs, answers from its record or refuses
is decided by steps 2 to 9 of that order, on the reservation ledger
(section 8.5, I10 and I11). No octet of the payload changes between the
last check and the intent that the service computes. At `ADMIT` the result
permits no effect yet: the request itself follows.

**After the predicate: a request under an admitted child.** These four
steps belong to the executor alone. What an invocation states and how it is
read comes with its members (LIP-0020 section 3). E0 names the checks of
the invocation that landed texts require and that have no code yet, so that
no reader takes the silence of the table for a decision.

| # | Step | Reads | Side | On success | Refusal | Again | Not yet observed | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E0 | The checks of the invocation itself, beside A1: the requested action is an entry of `actions` of `C` and of `delegate.actions` of `P` (LIP-0008 section 12.2); the executor of the invocation, the executor of `C` and the authenticated service agree (LIP-0008 section 4); `iat <= now < exp` on the executor's clock (LIP-0008 section 12.5); the proof path names `P` and `C` (LIP-0008 section 12.2) | The request; `C` and `P`; the clock and the pin of the executor | consumer | The request is one that `C` and `P` permit, at this executor, now | Open: none of these refusals has a code. Each comes with the members of the invocation (LIP-0020 section 3) | open, with the codes | The accounts | Carried rules, without codes. Open, by name: the order of these checks among themselves and against E1 and E2. Carried: all of them stand before E3 (LIP-0008 section 4, "before any new reservation or effect") |
| E1 | The action of the request is defined by the type profile of the executor (LIP-0020 W11.14) | The request; the executor's profile | consumer | The executor knows what the action does | `ACTION_UNDEFINED` | no, under one profile | The limits | Carried rule: LIP-0020 W11.4, "an executor refuses an action that its profile does not define". **NEW** code and place (LIP-0020 W11.14; pair Q20) |
| E2 | Every limit kind that the action consumes has a type profile at the executor. F17 judged the kinds of the limits that `C` and its row state; this step adds the kinds that the action consumes and that neither states (LIP-0020 W11.14) | The request; `limits` of `C` and of the template; the executor's profiles | consumer | The executor knows the arithmetic of every account that it will debit | `LIMIT_KIND_UNDEFINED` | no, under one profile | The amounts in the ledger | Carried rule: LIP-0020 W11.4; LIP-0008 section 12.4 for `policy`. **NEW** code and place (LIP-0020 W11.14; rule T9; pair Q20) |
| E3 | The reservation: one atomic write for all debits, the own account of `C` before the row account for each key, a key without a stated limit with the ceiling 0 (LIP-0026 R5.2, R5.4, R5.6). A request whose identity already holds a reservation is not charged again (R5.7) | The executor's ledger | consumer | The effect may follow the write | `OWN_LIMIT_OVER`, `ROW_CAP_OVER` | no; an account is never lowered (R5.8) | Nothing | Carried: LIP-0026 R5.2, R5.4, R5.6, R5.7 and R6.2, proposals of that draft. **NEW**: the place after E1 and E2 (pair Q20) |

**Rules that this subsection adds.** Each is a rule of the row that it
names. Rules T1 to T10 are proposals of version 0.1.55; rule T11 is added
by version 0.1.61 and states its own state there.

| # | Rule | Row | Refusal |
| --- | --- | --- | --- |
| T1 | A side MUST hold the grants of the path against the complete contract that they bind, before it reads whether the parent is live. A contract that is not presented and a contract that does not recompute are two findings with two codes: the first says nothing about the grants and is decided anew on a complete presentation, the second is decided by the octets. Both codes are new. The codes `CONTRACT_HASH` and `CONTRACT_MISMATCH` of LIP-0013 section 2.5 are not used on v4. `CONTRACT_HASH` reports that the SHA-256 of the contract octets differs from `contract_sha256`, and on v4 the member `contract` is an identifier that is no plain hash of the octets (LIP-0017 section 2; LIP-0020 W6.4). `CONTRACT_MISMATCH` reports that fields of the contract differ from fields of the grant, which on v4 is part (d) of F6, part (c) through version 0.1.60. The name `CONTRACT_ID` is chosen so that it is read as neither; the first draft of this version called it `CONTRACT_ID_MISMATCH`. What cannot be computed: part (b) waits for the exact preimages of the identifier, their prefixes and the length of a salt, which "come with the bytes" (LIP-0017 section 2) and which no landed text fixes. Until a v4 contract profile fixes them, no side can make part (b), no side completes the predicate, and no case and no vector states a result of part (b) on octets. Part (d) waits for the same profile: the rules of a v4 contract and the mirror of the terms of a grant in its contract have no rule text and no code; they stand after (b) and after the contract seal of part (c), and the open points below name them | F6 | `CONTRACT_NOT_PRESENTED`, `CONTRACT_ID` |
| T2 | A child MUST state the `genesis` of its parent (LIP-0008 section 12.2). The code is that of step V6, used for the one member that a v4 child has of the three that V6 compares. No v4 member corresponds to the two others, and nothing of them is checked | F8 | `SUBJECT_MISMATCH` |
| T3 | A child that its own closure or its own window refuses is reported with one code: a journaled closure, a window that opens below the recent block of the child, a window that has not opened, a window that has ended, and a spent seal. **NEW:** no landed text names a v4 code for a grant outside its window or with a journaled closure, and LIP-0008 section 7.1 refuses a backdated window without a code. This subsection names one code for a child alone; a root grant in the same state has no code from it. The two sides are stated apart. The issuer MUST NOT sign a child that is closed in its journal, whose window opens below its recent block, or whose window has ended at the tip of the service's observation. It MAY sign a child whose window has not opened yet: a window that lies ahead is what a delegator prepares, and every consumer decides it again at its own tip. That the window of the child lies inside the window of its parent is F18, on both sides. The consumer MUST refuse a child at every tip outside `[C.not_before_height, C.not_after_height)`. Before the window opens that refusal is state, and the same child is admitted when the tip reaches the opening height | F20, F21 | `CHILD_NOT_LIVE` |
| T4 | A code of v3 is used on v4 where the v4 comparison is the same relation on the corresponding members, whether or not v3 compares further members under that code, and whether or not the place among the steps is that of v3: `SUBJECT_MISMATCH`, `CHILD_ACTIONS_WIDER` and `CHILD_WINDOW_NOT_NESTED` (LIP-0020 W11.11), as LIP-0026 section 2 takes the four codes of J1.2. A code is new where the relation differs: `CHILD_CONTRACT_DIFFERS`, `CONTRACT_NOT_PRESENTED`, `CONTRACT_ID`. `CHILD_REPOS_WIDER` has no v4 member to report and is not used. The first code of some children changes with this version, and the changelog of version 0.1.55 names them | F5, F6, F8, F16, F18 | The codes of those rows; the rule adds none |
| T5 | An absent child-seal key and a wrong one are judged before any row is read. **NEW**, in two readings. First, CS2 is split. A child that states another key than the child-seal key of its parent as its `seal.key` refuses in F12 as `CHILD_SEAL_KEY`. An output on the node whose script is not the single-key script of the profile for the stated key refuses in F21 as `SEAL_SCRIPT`. A child that states the right key over an output that pays another key therefore refuses as `SEAL_SCRIPT`. **Amends** case S4-9 of section 11.2. Through version 0.1.54 its first refusal read "whose seal pays another key", which could be taken for the output on the node; the case is amended in place and now names the key that the child states for the first refusal and the script of the output for the second, so that the case and this rule decide one seal shape in one way. Second, the parity octet. J4.3 compares keys that must differ, by x coordinate and under either parity. F12 compares two output keys that must be equal, and an output key with the other parity octet has another script under the profile, so F12 compares every octet of the member | F10, F12, F21 | `CHILD_SEAL_KEY`; `SEAL_SCRIPT` |
| T6 | The checks of the coin of a row stand before the first step that reads an attestation | F22, F23 | The codes of F22 |
| T7 | At `ISSUE` the service reads the payload of `C` in five steps, in this order, and reports the first refusal. (1) The document step of LIP-0020 W9.2 on the octets of the payload; `WIRE_SIZE` is judged on the length of the signed form that the signature completes, which the payload fixes. (2) The `type` (W3.1). (3) The members, in the order of W9.3. (4) The reference to the parent, as step 6 of W11.8 states it for a child: `WIRE_ID`, then `CHAIN_DEPTH`, then `NOT_DELEGABLE`. (5) The rules of W11.9. These are the three steps of the class "unsigned payload" of W9.1, followed by steps 6 and 9 of the class "signed object". Steps 2, 5 and 7 of that class have no subject before a signature exists, and step 8 has none for a child, whose one reference stands in step 6. **NEW:** LIP-0020 W9.1 defines no such class and gains one by amendment when this rule is accepted | F2 | The codes of F2 without `WIRE_SIGNATURE_FORM` and `CHILD_SIGNER` |
| T8 | A refusal of the parent at the admission of a child keeps the code of the rule that refused the parent. **NEW:** on v3 step V5 reports every such refusal as `PARENT_NOT_LIVE`, and no landed v4 text says which code the admission of a child reports for a parent that LIP-0021, LIP-0022, LIP-0023 or LIP-0020 W9.4 refuses. The reason is that those codes tell a caller what to do, and one code for all of them does not: a changed issuer name, a seal with another script and an anchor that is still pending call for three different acts. The codes of those drafts are proposals and keep that state here. `PARENT_NOT_LIVE` keeps the findings that landed texts give it, J4.5 with the cases S4-4 and S4-6, and takes the two for which no v4 code exists: a journaled closure and the window. The order of the six parts is one order for both sides, and each part names its source in the table "Inside F7": B6.2 and the numbered steps of LIP-0008 section 4 fix 7.1 before 7.2 and the names before the checks of step 4, and the three other boundaries, 7.2 before 7.3, 7.4 before 7.5 and 7.5 before 7.6, are **NEW**, because the texts that name those checks list them and state no order. The Draft text of LIP-0008 section 5.2 is no part of F7 (part 7.2) | F7 | The codes of the table "Inside F7" |
| T9 | LIP-0020 W11.4 says that "a verifier refuses the admission that an unknown kind affects", and LIP-0026 R2.4 says that a kind whose amount is a floor "is no limit in the sense of this rule" and leaves its comparison to the type profile of the kind. Neither names a code or a place. **NEW:** F17 gives both. A side cannot compare an amount whose kind it does not know, so the kind is judged after the keys, which octets decide, and before the amounts. The code is `LIMIT_KIND_UNDEFINED` of LIP-0020 W11.14. No kind is defined in version 0.1.55, so a child or a template that states a limit refuses in F17 at every side until a profile defines its kind, and a pair that states no limit passes. E2 repeats the check for the kinds that a request consumes and that neither the child nor its row limits. A floor that fails the relation of its profile is reported as `CHILD_BUDGET_OVER`; R2.4 gives that code to ceilings, and its use for a floor is **NEW** | F17, E2 | `LIMIT_KIND_UNDEFINED` |
| T10 | At the admission of a child a side judges the rules of LIP-0020 W11.10 in two places and no other. In F1: rules 1 and 3, the forms of `delegate.actions` and of `notaries`, which F16 and F23 read. In F13, part (b): rules 4 and 5 for the group and the range that the ordinal of the child selects. **NEW:** the places, and the limit to the group and the range of the child. LIP-0020 W11.10 states that the result of its pipeline is a statement about a document and "does not say what a verifier must have read before it admits a child"; the profile in force has a verifier check "only the group and the range of its child" (LIP-0026 section 8); and the refusal of a whole parent is proposal Q1 of LIP-0026, which is pending and takes effect by no text before the owner decides it. This rule decides nothing of Q1: what a side does with a finding of rules 2 and 6 to 8, whether or not octets of the selected group or range take part in the finding, and with a finding of rules 4 and 5 in another group or range, is open point O7. The findings of rules 2 and 6 to 8 are not all caused by octets outside the selection: the sum of a pool is taken over every group, the selected one included, and the coin of the selected range can itself be the outpoint of the seal, meet another range or share its stop coin. Such a finding goes to O7 like the others, and to no row of this table. LIP-0020 W11.10 leaves that question to the pending proposal and states two outcomes only for its two proposal points. A reader of documents that judged all eight rules in step 9, as LIP-0020 W11.8 has a reader do, knows more than this rule asks, and at the admission of a child it reports a finding of rules 4 and 5 for the selected group and range in F13 and not in F1 | F1, F13 | `GRANT_DELEGATE` |
| T11 | Added by version 0.1.61. A side MUST hold the path against the confirmed-as-named seal of its bound contract and, where named, its framework contract. Both complete documents must be presented or resolved in F6(a) and recompute to their respective identifiers in (b); their transport, resolution and canonical bytes stay open in LIP-0017. Part (c) checks the bound contract first and its framework second, on the side's own node in F3's observation, before the open profile findings of (d). For each contract it first checks whether a seal is named, then whether the node read is conclusive, and only then judges confirmation, index and script. The refusal codes and retry marks are defined only in LIP-0020 W11.11: `CONTRACT_SEAL_MISSING` for no seal named or a conclusive finding, `CONTRACT_SEAL_UNAVAILABLE`, pending, for an unknown transaction or a read that proves nothing. The same documents against the same confirmed chain give the same answer and code where both nodes can read the required facts; equal chain tips alone do not imply equal availability. Neither code creates a closure, signature or admission. Decided: refusal at both sides under C12 of LIP-0017 (2026-11-17; the co-author agrees and leaves the judgement to Ivan). **NEW** proposals: the code names and retry marks, framework presentation/recomputation, and (c)'s place after (b), before (d); a missing seal is not hidden under (d)'s open code. This check judges no spend state: a seal confirmed as named and spent is not either seal-check refusal, and its step, code and closure stay open. An unavailable read of that transaction is pending, not evidence of absence or spend. `CHILD_NOT_LIVE` and `PARENT_NOT_LIVE` keep their grant-seal findings under T3 and T8. How a node is read against one tip remains open. Both required seal reads repeat after reservation in I4(c), between I3 and I5; refusal there is event 12 with the place held (I11; section 11.1, step 6). No side can compute (b) until a v4 contract profile fixes the identifier preimage: every result at or after (b), including (c), is on stated facts (T1) | F6, part (c) | `CONTRACT_SEAL_MISSING`, `CONTRACT_SEAL_UNAVAILABLE` |

T6 closes the point that LIP-0026 R6.1 left to the profile of the
attestation. The order is **NEW**, and no landed text gives it. Its reason
is an analogy: section 8 opens with the rule that a verifier runs every
mechanical check itself, on its own node, before it looks at the
attestation, and the three checks of the coin are mechanical. A child whose
anchor does not spend the coin of its row therefore refuses as
`ROW_COIN_REQUIRED` also when it carries a perfect attestation, as a child
that is wider than its row does (the paragraph after the table of section
8). One consequence is carried and not chosen. R3.4 compares two signed
transaction ids, and R6.1 still puts it after the checks of LIP-0023, so a
child whose coin is an output of its own seal transaction and whose anchor
is pending is reported as pending at a consumer. To judge R3.4 with the
rows that octets decide would amend R6.1, and this version does not.

**The order, pair by pair.** The rows stand in one sequence at each side.
The list below gives a source for every boundary between two neighbouring
steps of that sequence and for the order inside every step that has more
than one code. "Carried" names the landed text that fixes the order, and
the order has the state of that text. "**NEW**" marks an order that this
subsection chooses and gives the reason; where the choice follows or leaves
the order that the consuming side proposed on 2026-11-16, the cell says so.
"**Amends**" marks the one order that changes a landed sentence.

| Pair | Order | Status, source and reason | Case |
| --- | --- | --- | --- |
| Q1 | F1 before F2, and both before every other step | Carried: LIP-0020 W11.8, step 6, a child is read under the key of "the parent that the reader has already read through this pipeline", so of two malformed documents the parent gives the code; W9.1, a reader reports the first refusal of its pipeline, and the pipeline reads no node. **NEW** as a reading of LIP-0022 B6.1: both stand before F3, although their step 9 judges rules of a grant; a refusal of a document is computed in no observation, and F3 takes its chain from `genesis` of `P` (row F3). A malformed document is refused although a read would fail as well | S8-1 |
| Q2 | Inside F2: the parent reference, then the depth, then the right of re-delegation, then the signature | Carried at `ADMIT`: LIP-0020 W11.8, the reference selects the key. **NEW** at `ISSUE`: the five steps of rule T7, in which the members stand before the reference as steps 4 and 6 of the pipeline do | S8-2 |
| Q3 | F3 before F5 to F24 and before A1, at the issuer and at the consumer alike | Carried: LIP-0022 B6.1, the six codes of the observation stand before every rule of a grant, and a refusal of another rule that was computed in an observation which one of the six refuses is not reported. The issuer establishes the observation in I3, before it holds the contract in I4 (section 8.5), so that F3, F5 and F6, which are marked "both", give one code on both sides. Against the numbering of LIP-0008 section 4, which has the healthy observation as its step 3, the place of F3 before the names (parts 7.2 and 7.3, F19) is the reading of pair Q21, marked **NEW** there | S8-3 |
| Q4 | F19 before A1, and A1 before F20 | Carried: LIP-0008 section 4, the names in step 1, the authentication in step 2, the journal and the interval in step 4; LIP-0026 R9.10, the key of a request under a class comes from the value whose writer was checked. **NEW** against the proposal of the consuming side, which authenticates before the checks of a row. The key of a recipient by name comes from the proof of the name, that proof has one place, and that place is F19, after the checks that octets decide (pair Q13). A request with a wrong signature under a child that does not fit its row is therefore refused for the row. The first draft said that a party which is not authenticated "learns nothing about the path"; that did not hold there either, because both documents were read before the authentication | S8-4 |
| Q5 | F5 before F6 | **NEW**. F5 is decided by the signed octets of the two grants, and F6 by what the presenter shows. What the grants say is decided first, so that a contract which is missing or changed never hides a child that binds another contract than its parent, and F6 then holds one identifier and one document | S8-5 |
| Q6 | F5 and F6 before F7 | **NEW**, for the child and for the parent alike. No landed text holds a contract against a grant before it reads whether the grant is live, and v3 runs the other way: the binding of LIP-0013 section 2.5 follows the live check of the presented grant, and the binding of the parent is the second half of step V5. The reason here is that F5 and F6 are decided by documents. Their refusal is final for those documents, and a side reports it before a refusal that the chain as it stands decides and that a later observation may reverse; a party that must change its documents is not told to wait. The consequence is stated and chosen: a child under another contract, or without a presented contract, is refused for that also where its parent is closed | S8-6 |
| Q28 | Inside F6: (a), then (b), then (c), then (d) | Added by version 0.1.61. Required bound/framework documents are presented in (a), recompute in (b), and only then have their seals read in (c), bound contract first, framework second. Each seal is tested for a name before a node read, then for conclusive evidence before a node finding. C12 fixes the refusal; the code names and this order are proposals. Part (c) precedes (d)'s open profile findings, so a seal refusal does not hide behind an open code. Q6 still places all of F6 before F7 | S8-30 to S8-32 |
| Q7 | F7 before F8 to F24 | Carried: step V5 before V6 to V9; LIP-0026 R2.5, the checks of a row stand after the admission of the parent | S8-7 |
| Q22 | Inside F7: the parts 7.1 to 7.6 in that order. Inside part 7.6 the blocs are unordered (pair Q25) | Carried for two boundaries: LIP-0022 B6.2 for 7.1 before 7.2 and before 7.5; the numbered steps of LIP-0008 section 4, "Admission order", for the names of step 1 (7.2, 7.3) before the checks of step 4 (7.4, 7.5, 7.6). **NEW** for three boundaries, which no sentence orders: 7.2 before 7.3, inside step 1; 7.4 before 7.5 and 7.5 before 7.6, inside step 4, whose list is no order (the paragraph after this table). The reasons stand in the table "Inside F7" (rule T8) | S8-26 |
| Q8 | F8 before F9 | Carried: step V6 before the place of V7 (section 11.1) | S8-8 |
| Q9 | F9, then F10, then F11, then F12 | **NEW** inside the place of V7. The checks on the parent stand before those on the child; J4.3 (a), which section 11.1 puts at that place, stands before the rules of the child-seal key, which section 11.2 adds beside it; in F10 the key must be present before it is compared. Inside F11 the comparisons on octets stand before the comparison with a channel key, so that a refusal which octets decide is not reported as state | S8-9, S8-10 |
| Q10 | F9 to F12 before F13 | Carried for J4.3: the place of V7 stands before V8 (section 11.1). **NEW** for CS1 and CS2, which had no stated place; the order follows the proposal of the consuming side | S8-11 |
| Q11 | F13, then F14, then F15, then F17 | Carried: LIP-0026 R2.5; J1.2 | S8-12 |
| Q27 | Inside F13: (a), then (b) | **NEW** (rule T10). Nothing is selected before the ordinal lies within the rows, so the bound stands first; the group and the range are judged as documents before the child is held against the template in F14 to F18 | S8-29 |
| Q12 | F16 after F15 and before F17; F18 after F17 | **NEW** as the v4 reading. It follows the order of step V9 and of section 4: actions, budget, window. LIP-0026 R2.5 fixes the four checks of a row and does not place the two others | S8-13, S8-14 |
| Q23 | Inside F17: (a), then (b), then (c) | **NEW** (rule T9). The keys are decided by octets and stand first; an amount cannot be compared before its kind is known | S8-27 |
| Q13 | F13 to F18 before F19 | Carried: LIP-0026 section 2 makes the checks of a row on signed octets alone, and R9.9 puts the checks of a class after the proof of the name and before the coin. The consuming side's proposal reads the evidence of the recipient with the comparison of the recipient, before the limits; the table does not follow it, because a refusal for a limit would then depend on a node. Inside F19 the order is that of R9.9 | S8-15 |
| Q14 | F19 and A1, then F20, then F21 | Carried for F19 and A1 before F20 and F21: the numbered steps of LIP-0008 section 4, the names in step 1 and the authentication in step 2 before the checks of step 4. **NEW** for F20 before F21: the journal and the window of the child before its seal and its issuance. The list of step 4 names them and states no order; the window reads the tip alone, and a grant that is closed or outside its window is refused whatever its seal shows | S8-16 |
| Q24 | Inside F20: (a), then (b), then (c), then (d) | Carried: (b) before (c) and (d), `RECENT_BLOCK` before the rules that use `R` (LIP-0022 B6.2). **NEW**: (a) before (b). No sentence orders the journal of a grant against its recent block; a closure is reported before a finding of the chain as it stands, which a later observation may change. For the parent the same two checks stand the other way, 7.1 before 7.4, because there B6.2 puts the recent block before the walk of the issuer's name and the numbered steps put the names before the journal; a child has no issuer's name to walk. (c) and (d) share one code and one mark, so their order decides nothing: any order, the same verdict, and the row states (c) first | S8-28 |
| Q25 | Inside F21, and inside part 7.6 for the parent: four orders across the blocs (s), (w) and (i); otherwise the blocs are unordered | Carried, as the row of F21 names them: LIP-0008 SB3; LIP-0022 B6.2; LIP-0023 section 7 for `ISSUANCE_FRAME`; the order inside each bloc from its own text. Unordered and open: the three pairs of blocs (O1), and a validated spend of the seal against (w) and (i) (O6). The verdict of a grant with defects in two blocs is the same in any order, a refusal; its first code is not determined | None: no case and no vector may hold two defects of two blocs |
| Q15 | F21 before F22 | Carried: LIP-0026 R6.1, the coin after the checks of LIP-0023 | S8-17 |
| Q16 | F22 before F23 | **NEW** (rule T6). The consuming side's table lists the certifier before the coin and leaves the inner order open | S8-18 |
| Q17 | F13 to F18 before F23 | Carried: V6 to V9 precede V10 on purpose (section 8) | S8-19 |
| Q18 | Inside F23: after V12, `DELEGATE_KEY_REUSE`, then V13 | **Amends** section 11.1. Its sentence put every comparison of J4.3 (b) at the place of V7. The comparison with the attestation key of the row's notary cannot stand there: the row is known after F13 alone, and no step before V10 looks at an attestation. It stands at the first step that holds that key, and the sentence of section 11.1 now says so | S8-20 |
| Q19 | F23 before F24; inside F24 the order of LIP-0027 H2.7, then V18 | Carried: LIP-0027 H2.7 and H5.1; steps V10 to V18 | S8-21 |
| Q20 | E0 before E3; E1, then E2, then E3 | Carried for E0 before E3: LIP-0008 section 4, the invocation satisfies section 12 "before any new reservation or effect". **NEW** for E1, E2, E3: an executor reserves nothing for an action or a kind that it cannot account for (LIP-0008 section 2; LIP-0026 R6.2). Open: E0 against E1 and E2 | S8-22 |
| Q21 | F3 before F19 and before A1 at `ADMIT`; I0 and I2 before F3 at `ISSUE` | **NEW** as a reading, in both recipient modes. Two landed texts speak, and neither is amended here. LIP-0008 section 4 numbers "Require healthy observations" as its step 3, after the names of step 1 and the authentication of step 2; its opening sentence has the verifier use "one consistent observation" for every step, and it names no code. LIP-0022 B6.1, the proposal of that draft, puts the six codes of an observation before every rule of a grant and withholds a refusal that was computed in an observation which one of the six refuses. The table takes B6.1 for the order of the refusals: step 1 cannot resolve a name outside an observation, A1 by name uses the value that F19 read at the tip of the observation (LIP-0021 O7.2), and the request by key is authenticated by the recipient mode that the grant signs, so the step has one place in both modes. If the owners read step 3 of LIP-0008 section 4 as the place of the refusals of an observation, F3 moves after A1 by amendment. At `ISSUE` the pair has another subject: the checks of the caller are computed in no observation and stand before F3 (section 8.5, I0 and I2 before I3) | S8-25; S8-24 for `ISSUE` |
| Q26 | The last step of the predicate, F24 or, for a row without a certifier, F22, before E0 to E3 | **NEW**. No sentence orders the checks of an invocation against the admission of the child: LIP-0008 section 4 names the "exact requested action" in the list of its step 4, which states no order, and requires only that the invocation satisfies section 12 "before any new reservation or effect". The reason here is that E0 reads members of the request against `C` and `P`, which bound a request only once both are admitted, and that the predicate stays the same at an issuer, which has no request. A1 is the one check of the request inside the predicate (pair Q4) | None: the codes of E0 are open (O3) |

The pairs keep their numbers: Q21 stands, by its steps, between Q3 and Q4,
Q27 after Q11, Q28 after Q6, and Q22 to Q26 where the list has them. The order of the
signing service's steps is section 8.5, which is the inner order of step 1
of the order of one request of section 11.1 and has its own sources.

**The list of step 4 of LIP-0008 section 4.** That step reads: "Check the
durable closure journal, grant interval, issuer/target, confirmed issuance,
separate seal, recent-block reference and exact requested action." This
subsection reads the numbered steps 1 to 5 of that section as an order,
because the section is headed "Admission order" and numbers them, with the
one reading of pair Q21 for step 3. It does not read the list inside step 4
as an order. Read as one it would put the recent-block reference after the
grant interval, and LIP-0008 section 7.1, rule 3, and LIP-0022 B6.2 need
the recent block before the window; it would also put the issuance before
the seal, which no text asks. Of the pairs of that list, landed sentences
order four: the recent block before the window (B6.2); the anchor before
`RECENT_BLOCK_WINDOW` (B6.2); the output and the signature of a seal before
the classification of its spend (LIP-0008 SB3); and `ISSUANCE_FRAME` at its
place in W9.4 (LIP-0023 section 7). Four orders are proposed here and
marked **NEW**: the journal before the recent block and the window of a
child (Q24) and before the window of a parent (Q22); the window before the
seal and the issuance (Q14, Q22); and the requested action after the whole
predicate (Q26). Every other pair of the list is unordered: the seal
against the issuance and each against the checks of LIP-0023 (O1, O6). No
row and no pair cites the list for an order.

**What the list claims.** The claim is stated in three parts, and no part
says more than its rows.

- **Between the rows the order is total.** At a consumer the rows stand in
  one sequence, F1 to F19, A1, F20 to F24, then E0 to E3, and every
  boundary between two neighbours has a pair with its status. For two steps
  that are not neighbours the order follows from the boundaries between
  them. One boundary is not ordered: E0 against E1 and E2 (O3); E1, E2 and
  E3 are ordered among themselves. At an issuer the sequence is that of
  section 8.5.
- **Inside a row the order is total where the row says "in this order"**
  and its parts report different codes: F2, F3, F6 (a) before (b) before
  (c), F7 with
  its parts 7.1 to 7.6, F10, F13, F17, F19, F20 (a) before (b) before (c)
  and (d), each bloc of F21 by itself, F22, F24, and E1 to E3. Where parts
  share one code their order decides no code; it is stated where it decides
  what the refusal leaves behind (F11) and is otherwise free (F20, (c) and
  (d)).
- **Unordered, and said so in the row:** the three blocs of F21 and of
  part 7.6 against each other, and a validated spend of a seal against two
  of them (O1, O6); the four middle codes of V12 inside F23; the checks of
  E0 among themselves (O3); and the two findings of part (d) of F6 (O4).

A pair is called carried only where the cited sentence states the order.
Every order that this subsection takes from the sequence of a list, or
chooses, is marked **NEW** in its row and its pair.

**Open points.** Eight points stay open. No case of section 8.6 and no
vector of section 8.7 may hold a defect, or a pair of defects, whose first
code or whose verdict depends on one of them. For O1, O2, O3, O5 and O6
the verdict is fixed, a refusal, and its code or its first code is not;
for O4 no side completes the predicate; for O7 two outcomes conform; and
for O8 the cutoff that a signing service applies is not determined.

| # | Open | Where | Waits for |
| --- | --- | --- | --- |
| O1 | The order of the three blocs of the seal and the issuance against each other: LIP-0008 SB2 against LIP-0023, SB2 against the reference of step 8 and steps 2 to 6 of LIP-0020 W9.4, and LIP-0023 against those steps. The four orders that landed texts fix across the blocs are carried and not open (pair Q25) | F21; part 7.6 of F7 | The profile of the seal and the issuance |
| O2 | The code of a request that is not authenticated | A1 | The members of the invocation (LIP-0020 section 3) |
| O3 | The codes of the checks of the invocation itself, the order of those checks among themselves, and their place against E1 and E2. They stand before E3 | E0 | The members of the invocation |
| O4 | The code of a contract that is no valid contract of its v4 profile, the code of a contract that does not mirror the terms of its grant, and the order of the two after the identifier. With them: the preimage of the identifier, without which part (b) of F6 cannot be computed. Since version 0.1.61 these two findings are part (d), after the required contract seals of part (c), whose codes are defined in LIP-0020 W11.11; they are parts (b) and (c) in texts of versions 0.1.55 to 0.1.60 | F6, parts (b) and (d) | A v4 contract profile (LIP-0017 section 2; LIP-0018) |
| O5 | The code, and what the refusal leaves behind, of a journal of closures of a grant that cannot be read or cannot show its continuity. The verdict is fixed: such a side admits nothing and signs nothing (LIP-0008 section 5.1, "Failure to persist closure permits no effect and requires journal recovery"; J4.4, "its closure journals included"). The codes `JOURNAL_LOST` and `JOURNAL_FENCED` of F24 belong to the journal of rows and are not assigned to this one | Part 7.4 of F7; F20, part (a) | The entries of a closure journal on the form of LIP-0025, or an owner's line on the code |
| O6 | The place of the classification of a validated spend of a seal (`CHILD_NOT_LIVE`, `PARENT_NOT_LIVE`; closed) against the blocs (w) and (i). LIP-0008 SB3 orders it after bloc (s) and the signature and against nothing else | F21; part 7.6 of F7 | The profile of the seal and the issuance, with O1 |
| O7 | What a side does, at the admission of a child, with a finding of rules 2 and 6 to 8 of LIP-0020 W11.10, whether or not octets of the group or the range of the child take part in the finding, and with a finding of rules 4 and 5 in another group or range. A finding of rules 2 and 6 to 8 can be caused by the coin of the selected range itself, which is the outpoint of the seal, meets another range or shares its stop coin, and by the pool sum, which is taken over the selected group as well; it is held here all the same, and no row of this table judges it. Two outcomes conform until the owner decides proposal Q1 of LIP-0026: a side that judged the rule refuses in F13, part (b), as `GRANT_DELEGATE`, and a side that judges rules 4 and 5 for the group and the range of its child alone goes on. The two sides of one path may therefore differ on such a parent, a parent whose defect is the child's own coin included. LIP-0020 W11.10 leaves that question to the pending proposal and states two outcomes only for its two proposal points | F13, part (b); rule T10 | The owner's decision on proposal Q1 of LIP-0026 |
| O8 | The class of action under which the signing service judges `TIP_AGE`. LIP-0022 B3.6 measures the age of the tip against the class of the action of a request, and at `ISSUE` there is no request | F3 at `ISSUE`; section 8.5, I3 | A line of LIP-0022 or of the owners on the class of signing a child |

What the table does not decide: whether the key that signs children may run
under the OS user of the delegating agent; which product holds the
delegation key on a given host; who funds the coin of a row and holds the
path of its spend; where a key slot comes from; and which party of the
delegating side makes, for a child, the checks that LIP-0020 W7.5 to W7.9 ask of an issuer
before a grant is signed, the age and the single use of the consent of the
child's recipient among them. The last point is open with the key that
assents to a child's contract (LIP-0020 W7.2). The delegation key signs
child grants and nothing else (J4.2), J4.4 lists no consent among the
checks of the signing service, and this table gives the service none; a
consumer reads the consent in F21. None of these points is a step of the
predicate, and a verifier sees none of them. The refusals of the signing
service's own record of places are decided, and not by this table: they
are the reservation ledger of section 11.1 (J4.4 (a) to J4.4 (g)), to which
section 8.5 points.

The [Source-contract companion](LIP-0014-source-contract-proposals.md)
collects proposed resolutions of these eight points, T1/profile inputs,
identity latching and the enrollment boundary (section 2.4). For the state
of the R8.3 count order, see LIP-0026
section 8. The remaining LIP-0026 proposal Q2 stays **PROPOSED**. The
companion changes no status or outcome in this section.

### 8.5. The order of the issuer's checks (J4.4)

One signing request has one order. It is the order of one request of
section 11.1, in nine steps, which landed with the reservation ledger in
version 0.1.54. Version 0.1.55 amends two steps of it, in place and marked
there: step 3, which gains one branch (I9 and I10 below), and step 6, which
names the checks that it repeats (I11 and the paragraph "The repeat"
below). This subsection changes no other step and no other word of it.
Step 1 of that order reads: the service "identifies the caller and makes
the checks of J4.4". J4.4 lists those checks, and step 1 names them in one
sentence; neither gives them an order among themselves or names the rows
of section 8.4 that make them. This subsection gives that: the steps I0 to
I9 below are the inner order of step 1. Step 6 of the order of one request
repeated, through version 0.1.54, "the checks of J4.4 on the parent and on
the row"; as amended it repeats I3 and I5 to I9 on a fresh observation —
since version 0.1.61 also part (c) of I4, the confirmed contract seal,
which reads a node since that version — and the paragraph "The repeat"
below states it. I10 and I11
are no checks and make no signature of their own: they are steps 2 to 5
and steps 6 to 9 of the order of one request, named here so that the table
shows the whole order in one place, and their cells point into section
11.1 and restate no rule of it.

The state of I0 to I9 is that of section 8.4: a proposal of version
0.1.55. The order of these checks was proposed by the consuming side on
2026-11-16. The table marks **NEW**, in its column "Source and status",
each duty that J4.4 does not name and each place that no sentence states,
and it departs from the proposed order in the place of the observation:
the observation is a step of its own, I3, and stands before the contract
in I4, for the reason that the paragraphs after the table give. When the
version lands, the duties marked **NEW** are checks of step 1 like the
others: a request that any of I0 to I9 refuses is event 1 of the table of
states, it reserves nothing, reads nothing of the ledger and learns nothing
of it (J4.4 (a)), and that holds for a replay as for a first request
(J4.4 (d)).

| # | The service | Source and status | Rows | A refusal |
| --- | --- | --- | --- | --- |
| I0 | identifies its caller. It reads no document of the request for this and no node | Carried: step 1 of the order of one request, "It identifies the caller"; J4.4, "MUST identify the caller"; "Possession of the messaging key is not the authority to ask". **NEW**: the place before I1. Neither text orders the identification against the reading of the documents; this step takes the order in which step 1 names them, so that a caller that is not identified learns no code of a document | None: I0 is no step of the predicate | No signature exists, and the service returns no code (event 1). How the service learns the run and its origin is outside this subsection |
| I1 | takes the complete child as a payload and the complete parent as a signed form, and reads both as documents. It takes no digest, no part of a child and no batch | Carried: "take the complete child"; "MUST NOT sign a digest that a caller supplies" | F1, F2 | The code of the row; for a digest, no signature exists (event 1) |
| I2 | finds `P` on the list for delegation of the caller that I0 identified | Carried: "sign only for a caller that its operator listed for delegation under `P`"; step 1, "that the caller is listed for delegation under the parent". **NEW**: the place after I1 and before I3. The list is read under the identifier of `P`, which I1 recomputes, and the check reads no node | None: I2 is no step of the predicate, as A1 is none at a consumer (section 8.4) | No signature exists, and the service returns no code (event 1) |
| I3 | establishes on its own node the one observation to which every read of part (c) of I4 and of I5 to I9 belongs | Carried: "on its own node". **NEW** as a step of its own: J4.4 names no observation, and LIP-0022 sections 1 to 3 state one | F3 | The code of the row, which is pending, or state for `OBSERVATION_CHAIN`; no signature exists. The class under which the service judges `TIP_AGE` is open (section 8.4, open point O8). A code of F3 stands before the code of every step from I4 on, also where the service learns of it at the last read of the observation (LIP-0022 B6.1) |
| I4 | holds `C` against the contract identifier of `P`, then both against the presented bound contract and any named framework; their identifiers recompute before their seals are read on the service's own node, bound contract first, framework second | **NEW** duty: J4.4 names no contract. Refusal without the required confirmed seals is C12 of LIP-0017 (2026-11-17; the co-author agrees and leaves the judgement to Ivan), carried by 0.1.61; code names, retry marks and place in F6 are proposals (T11). Both seal reads repeat in I11 | F5, then F6 | `CHILD_CONTRACT_DIFFERS`; then `CONTRACT_NOT_PRESENTED`, `CONTRACT_ID`, `CONTRACT_SEAL_MISSING`, `CONTRACT_SEAL_UNAVAILABLE`. Part (b) of F6 cannot be computed yet and (d) is open (T1): until a v4 contract profile exists the service ends here with no code and signs nothing. A result of (c) is on stated facts for (b); a pending read never signs |
| I5 | establishes, in the observation of I3, that `P` is live under every admission rule, its closure journals included | Carried: "on its own node, check that `P` is live under every admission rule, its closure journals included". The closures of an issuer's name "under LIP-0008 section 5.2" are no part of F7 while that section awaits agreement (part 7.2) | F7 | The code of the row. A read that proves nothing is pending, and no signature exists |
| I6 | makes the comparisons of the subject and of the keys | Carried: "the comparisons of section 4"; the sentence after the table of J4, that a verifier repeats the checks of J4.4 on the parent and on the child; for the child-seal key **NEW** as a duty of the service | F8 to F12 | The code of the row |
| I7 | finds the row of the ordinal and holds the child against it and against the parent | Carried: "that the child's row exists and that the child fits it"; "the comparisons of section 4". **NEW** as duties of the service where the rows are new: part (b) of F13 (rule T10) and part (b) of F17 (rule T9) | F13 to F18 | The code of the row |
| I8 | establishes on its own node that the recipient of the child is one that the row admits; then holds the child against its journal, its recent block and its window; then reads the output that `seal.outpoint` of `C` names, in the seal transaction as the delegating side fixed it. It finds there the single-key script of the parent's profile for the child-seal key of `P`. It holds no private child-seal key and needs none for this (CS4) | **NEW**, all three: J4.4 lists no check of the child's recipient on a node, none of the child's own window and none of its seal | F19; then F20, with the issuer's reading of part (d); then F21, bloc (s) alone | The code of the row: for F19 its codes; `CHILD_NOT_LIVE`, `RECENT_BLOCK`; `SEAL_OUTPUT`, `SEAL_SCRIPT`, `SEAL_PROFILE`. No signature exists |
| I9 | establishes that the coin of the row is there, and then that it is unspent, so that the child's anchor can still spend it, or that it is spent by the confirmed issuance anchor of the child in this request; a spend by anything else refuses as before. It then establishes that the row is not ended. The anchor of the child in this request is read from the payload and the chain alone: a transaction that the observation of I3 shows confirmed on the active chain, of which one input spends the coin of the row and one input spends the linkage output of the seal transaction that `seal.outpoint` of the payload names (LIP-0023). The service reads nothing of its ledger for this (J4.4 (a)). Where the check passes by that anchor and not by an unspent coin, step 1 hands step 3 that one fact, "I9 passed by the anchor exception", and nothing else | Carried: "that under section 10.1 the row is not closed for cause"; section 11.1, "that the coin of a row is unspent is read on a node, by the service under J4.4". **NEW** as duties of the service: for the coin LIP-0026 R3.4 and R3.2, and for the stop coin LIP-0027 H2.2 to H2.4. **NEW**: the code of a spent coin (section 8.4, row F22). **NEW**: the anchor exception, so that a replay after publication reaches its record; the landed sentence has the service read the coin as unspent and names no exception. **NEW**: that the anchor is recognised by the two inputs alone, without the issuance commitment, which the service is not presented with | F22 in the issuer's part: R3.4, then R3.2, then the output unspent or spent by the anchor of this child; then F24 without V18. For a row without a certifier F24 is not made | The code of the row; where both rows refuse, that of F22. A coin that another transaction than the confirmed anchor of this child has spent: `ROW_COIN_REQUIRED` |
| I10 | takes steps 2 to 5 of the order of one request, as section 11.1 states them and in its order: the continuity check of the ledger, the read of the place, the room, the reservation. It computes the intent itself from the payload that passed I0 to I9 (J4.4 (b)). A request for a place that has a record or an open mark, a replay included, ends in step 3 and reaches no later step. So does a request that I9 passed by the anchor exception, for a place with no record and no open mark: step 3 refuses it and reserves nothing | Carried: section 11.1, the order of one request and J4.4 (a) to J4.4 (g), decided on 2026-11-16 and landed in version 0.1.54. **Amends** step 3 of that order by one branch, event 39, which is stated there and marked there; this row states no other rule of them and adds none | None: no row of section 8.4, and no check that a verifier can repeat | As section 11.1 gives it: `PLACE_HELD`; `PLACE_CONFLICT`; for a replay of a place that is `signed`, the stored octets and no new signature; for want of room, behind an open mark of another place and for a mark that did not land, a refusal with no code (events 2 to 11); and where I9 passed by the anchor exception and the place has no record and no open mark, a refusal with no code, an entry of the operational audit and a notice to the operator that a signature exists outside this ledger (event 39) |
| I11 | takes steps 6 to 9 of the order of one request, as section 11.1 states them and in its order: the repeat of I3, part (c) of I4 and I5 to I9 on a fresh observation; the entry of the use of the key and one call of the signer; the verification of the signature; the entry of the result, and only then the release | Carried: section 11.1, as for I10; J4.4, "It computes the digest itself". **Amends** step 6 of that order, which through version 0.1.54 repeated "the checks of J4.4 on the parent and on the row": it now repeats I3 and I5 to I9 on a fresh observation, and since version 0.1.61 also part (c) of I4, whose read of a node that version adds, so the enumeration in the step is amended again in place and marked there (the paragraph "The repeat") | For the repeat: F3, part (c) of F6, and F7 to F24 as far as I5 to I9 make them: F7; F8 to F12; F13 to F18; F19, F20 and bloc (s) of F21; F22 and F24 in the issuer's part. For steps 7 to 9: none; the signature is what step 7 of F2 reads at `ADMIT` | As section 11.1 gives it. A repeat that refuses is event 12: the refusal of J4.4, here the code of the row that refused, no code of section 11.1, no signature, and the place is held. After it: `PLACE_HELD` (events 13, 15, 17, 19 and 21 to 23) or the 64 octets of the signature (event 20) |

The service stops at the first step that refuses, and then no signature
exists. Where the step is a row of section 8.4, the service returns the
code of that row to its caller, as section 8.2 says of a signer. That code
is "the refusal of J4.4" of events 1 and 12, and this is **NEW** as a
reading: section 11.1 says of that refusal "no code of this section", and
the code of a row is a code of section 8.4 or of another LIP, not one of
the two codes of the ledger; it states a finding about the documents, the
chain or a journal of closures and discloses nothing of the ledger. I0 and I2 are no
such rows: a caller that is not identified or not listed gets no signature
and no code. The order puts the identification before the documents, as
step 1 of the order of one request names it first, so that a caller that
is not identified learns nothing, not even whether its documents are well
formed; it puts the documents before the caller's list, because the list
is read under the identifier of the parent; it puts both before every read
of a node, so that a caller without authority causes no read; it puts the
observation before every later row of the predicate, the contract
included, as the consumer has it (section 8.4, pair Q3); and it puts every
check on the parent before the first check that reads a row.

**One order, in three sequences.** The order of one request decides each
of these, and I0 to I9 decide none of them alone.

- A replay: a listed caller sends again the payload of a place that is
  `signed`. I0 to I9 are made as for a first request and pass, also after
  the confirmed anchor of that child has spent the coin of its row, by the
  anchor exception of I9 (case S4-30a). I10 reads
  the place in step 3 and answers with the stored octets; no later step is
  reached, and the service does not sign again (J4.4 (d), event 5, case
  S4-12). Where one of I0 to I9 now refuses, the answer is that refusal and
  nothing of the record (event 1).
- A parent that is closed after the reservation: the request passed I0 to
  I9 and I10 wrote the reservation; the repeat of I11 makes F7 again, in
  its fresh observation, and part 7.4 refuses as `PARENT_NOT_LIVE`. That is event 12: no use of the
  key, no signature, and the place is held (case S4-30).
- A place that is taken, and a lost ledger: a request that passes I0 to I9
  with another intent than the record or the open mark of its place is
  refused in step 3 as `PLACE_CONFLICT` (J4.4 (e), event 6, case S4-13);
  under a lost ledger every request that passes I0 to I9 is answered in
  step 2 as `PLACE_HELD` (event 4 in the last column, case S4-24). In
  neither does a signature exist.

**The repeat.** Through version 0.1.54 step 6 of the order of one request
read: "It repeats the checks of J4.4 on the parent and on the row (event
12)." Version 0.1.55 **amends** that step, in place and marked there: the
service repeats I3 and I5 to I9, in that order, on a fresh observation that
it establishes for the step as in I3, because the observation of step 1
ended before the reservation was written. Version 0.1.61 adds part (c)
of I4 to the repeat, between I3 and I5, in the order of step 1: since
that version part (c) reads the contract seal on a node, so the
principle of step 6 — every check of step 1 that reads a node or a
journal — reaches it without a new rule, and the enumerations in step 6
and in row I11 are amended in place for it, as proposals of that version.
No child is therefore signed when either required contract seal fails the
fresh read. That refusal is event 12, with the place held:
`CONTRACT_SEAL_MISSING` for no seal named or a conclusive finding, and
`CONTRACT_SEAL_UNAVAILABLE`, pending, when the read proves nothing.
No check of the repeat is made
on a value that step 1 read: the name of the parent's recipient, which I6
compares, the evidence of the child's recipient, the journal and the
window of the child and the seal output, which I8 reads, and the coin and
the stop coin of I9 are all read again. No child is therefore signed whose
window ended, whose recipient's evidence changed or whose parent or row
closed between step 1 and step 6. I7 is repeated with the others; signed
octets alone decide it, and on the payload of the recorded intent it gives
the verdict of step 1. I0, I1, I2 and I4, apart from its part (c), are not
repeated: the caller, the documents, the caller's list and, apart from
the seal that part (c) reads, the contract are read on no node, and the
payload of the recorded intent is the payload that step 1 read. In the
repeat I9 has no anchor exception: the place is `reserved`, no signature of
this ledger exists for it, and a coin that the fresh observation shows
spent, by the anchor of this child or by anything else, refuses as
`ROW_COIN_REQUIRED`. Where the transaction that spent the coin is the
confirmed issuance anchor of this child, the service also writes the entry
of the operational audit and gives its operator the notice of event 39,
that a signature exists outside this ledger; the place stays held, as event
12 states, and no signature of this ledger exists for it (sentence added
with version 0.1.56, as normative text). The cost of the amendment is one
more read of the node for every signature: where the landed step read
the parent and the row again, the service now also reads again the
names, the journal of the child, the seal output and the tip for the
child's window. Marked for the owners: the amendment of step 6 itself
(**Amends**); that the repeat has an observation of its own, whose
codes are those of F3 (**NEW**); and that the anchor exception of I9
does not hold in the repeat (**NEW**). A refusal of
the repeat is event 12
whatever its code and whatever its mark, a pending read included: the
place is held, and the exit is that of case S4-18. A service may read again
inside the request, while the claim lives, before it ends the request on a
read that proved nothing; a request that it ends there is event 12 or
event 13, and both hold the place.

**A replay after publication.** J4.4 (d) has a replay answered only after
all checks of step 1, "as for a first request". With I9 among them and
with the coin read as unspent alone, a replay that is asked after the
anchor of the child has spent the coin of its row would be refused as
`ROW_COIN_REQUIRED`, and the stored signature would be reached by no
request. I9 therefore passes a coin that the confirmed issuance anchor of
the child in this request has spent (**NEW**). The service tells that spend
from another on the payload and the chain, and reads nothing of its ledger
in step 1 (J4.4 (a)). The pass carries one fact into step 3, that I9 passed
by the anchor exception, and step 3 decides what it is worth. A place with
a record `signed` of this intent answers with the stored octets (event 5,
case S4-30a). A place with no record and no open mark is refused there with
no code, and the operator is told that a signature exists outside this
ledger (event 39): an anchor of the child is confirmed, this ledger shows
no signature for the place, and a service that signed now would make a
signature that it cannot show to be the first. In every other state of
the place and under a lost ledger the answer is the one that section 11.1
gives without the exception. A coin that anything else has spent refuses
in I9 as before.

The observation has one place on both sides. F3, F5 and F6 are marked
"both" in section 8.4, and LIP-0022 B6.1 puts the codes of an observation
before every rule of a grant. A service that held the contract before it
established its observation would return `CHILD_CONTRACT_DIFFERS` where a
consumer with the same inputs returns `OBSERVATION_VOID`, a refusal that
the octets decide where the other side reports a read that proved nothing
(case S8-3). I3 therefore stands before I4. The caller of I2 is not such a
case: the service finds it in its own record, no observation computes it,
and a consumer has no caller of J4.4 to check; a caller that is not listed
learns no code of an observation, of a contract or of a row (case S8-24).

F19, the recipient of the child on the node, is a duty of the service and
the first part of I8. No landed text makes it optional, and a service that
left it out would sign a child that every consumer refuses for its
recipient, after the coin of the row is spent and the row is used up. The
service makes it in the observation of I3 and returns the codes of that
row. Among the rows that both sides make in full the two differ in F20
alone: the service signs a child whose window has not opened yet, and it
signs none that is closed in its journal, that is backdated, or whose
window has ended (section 8.4, rule T3). In F21, F22 and F24 the service
makes the part that its row states, and in F22 it reads the coin as
unspent, or as spent by the confirmed anchor of this child (I9), where a
consumer reads the input of the anchor.

I8 is also the pre-sign duty for the seal of a child. Without it a signing
service signs a child whose seal pays another key, and every verifier
refuses that child as `CHILD_SEAL_KEY` or as `SEAL_SCRIPT` after its coin is
spent and its row is used up. The service does not require the seal
transaction to be confirmed where the construction profile lets the anchor
follow in the same block (LIP-0008 section 9): it reads the transaction that
its own node holds. A seal transaction that its node does not hold gives
`SEAL_OUTPUT`, and that refusal is pending: nothing is proved about the
seal (LIP-0024 section 3), the service signs nothing, and it reads again.
Two services at different distances from the delegating side therefore
differ only in when they sign, and neither reports a fact that it has not
read.

A step that the consumer makes and the issuer does not, in section 8.4, is
no duty of the service: the anchor, the input that spends the coin, the
attestation and the withdrawal are facts that do not exist when a child is
signed. One read of such a fact is made all the same, for a replay alone:
the anchor exception of I9.

### 8.6. Cases of the step order

All are v4 cases. No v4 verifier exists, and no result is claimed. Each
refusal holds the two stated defects and nothing else, and its control is
the same pair of grants without them. A checker that reports the second
code of a case makes the later step first.

Four facts are stated for every case and are not computed, because this
version cannot compute them. The contract of the pair is presented and
recomputes to its identifier, unless the case says otherwise (section 8.4,
rule T1). The bound contract and any framework it names each name a seal
that the side's own node conclusively shows confirmed as named and unspent,
unless the case says otherwise (T11); any named framework document is
presented and stated to recompute to its own identifier as well. A case
that states a limit states a stand-in profile that defines
its kinds as ceilings, because no kind is defined (rule T9). And a case of
a request states a stand-in profile that defines one action, because no
action is defined (LIP-0020 W11.14). A control that needs such a stand-in
has no instance under the registries of version 0.1.55 themselves, and the
case says so. No case holds a pair of defects whose first code depends on
an open point of section 8.4.

| Case | Pair | Valid control | Refusal or invariant |
| --- | --- | --- | --- |
| S8-0 | None: the control of every pair | A parent and a child that pass, at a consumer, every row that the kind of the child's row makes: F1 to F24 for a row with a certifier, F1 to F22 for a row without one. The same pair as a payload at an issuer, from a listed caller, passes I0 to I9 and, for a place with no record under a usable ledger, is signed once through steps 2 to 9 of the order of one request (section 11.1, case S4-11). Both are admitted. A verifier that refuses every child passes each refusal below and fails this case | Invariant: no code. A side that refuses this pair fails the case, whatever it reports for the cases below |
| S8-1 | Q1 | A well-formed child whose parent's history cannot be read: pending under F7, `ISSUER_HISTORY_UNAVAILABLE` | A child with a member that its list does not have, while the history of the parent's issuer cannot be read: `WIRE_MEMBER`, and no read is made. A parent with a member that its list does not have, presented with a child that has one too: `WIRE_MEMBER`, reported for the parent |
| S8-2 | Q2 | A child that names its parent and is signed by the delegation key. At an issuer: a payload that names its parent | A child signed by another key and presented with another parent: `WIRE_ID`, not `CHILD_SIGNER` (LIP-0020 W11.8). At an issuer: a payload with a member that its list does not have and a `parent` that is not the identifier of the presented parent: `WIRE_MEMBER`, not `WIRE_ID` (rule T7) |
| S8-3 | Q3 | The pair of S8-0 at a healthy node. With another `contract` in the child and nothing else: `CHILD_CONTRACT_DIFFERS` | The child with another `contract`, at a node whose tip moved during the observation: `OBSERVATION_VOID`, pending, at the consumer and at the issuer alike (section 8.5, I3 before I4). Neither side reports `CHILD_CONTRACT_DIFFERS`, and the issuer signs nothing |
| S8-4 | Q4 | A request under a child that fits its row and whose recipient name the signed owner key holds, signed by the key that the name lists for the channel: authenticated | The same request signed by another key, under a child whose recipient is not the recipient of its row: `CHILD_GRANTEE_NOT_ALLOWED`, by F15 before A1. Under a child that fits its row and whose recipient name another key holds: `RECIPIENT_NAME_NOT_HELD`, by F19 before A1. Under the child of the control: refused at A1. That last verdict is fixed and its code is open, so it is a note and no code case |
| S8-5 | Q5 | A child with the contract of its parent, presented with that contract | A child whose `contract` differs from the parent's, presented with no contract: `CHILD_CONTRACT_DIFFERS`, not `CONTRACT_NOT_PRESENTED`. A child with the contract of its parent, presented with no contract: `CONTRACT_NOT_PRESENTED`; the same pair presented again with the contract is the control. Stated as a fact and not computed: a presented document that does not recompute to the identifier: `CONTRACT_ID` |
| S8-6 | Q6 | A child of a live parent under one contract | A child with another `contract` under a parent whose seal is spent: `CHILD_CONTRACT_DIFFERS`. A child with the contract of its parent, presented with no contract, under that parent: `CONTRACT_NOT_PRESENTED`. Neither is `PARENT_NOT_LIVE` |
| S8-7 | Q7 | A child that fits its row under a live parent | A child with a limit above its row, under a parent whose window closed at the tip: `PARENT_NOT_LIVE`, not `CHILD_BUDGET_OVER`. The same with the history of the parent's issuer unreadable: `ISSUER_HISTORY_UNAVAILABLE`, pending, and no closure |
| S8-8 | Q8 | The same chain in parent and child | A child with another `genesis`, under a parent whose delegation key equals its grant key: `SUBJECT_MISMATCH` |
| S8-9 | Q9 | A parent with distinct keys and a child-seal key | A parent whose delegation key equals its grant key and which names no child-seal key: `DELEGATE_KEY_REUSE`. A parent without a child-seal key whose other keys are distinct: `CHILD_SEAL_KEY` for every child |
| S8-10 | Q9 | A child whose `seal.key` is the child-seal key of its parent | A child whose `seal.key` has the x coordinate of the delegation key: `DELEGATE_KEY_REUSE`, by F11 before F12. A child whose `seal.key` is a third key: `CHILD_SEAL_KEY`. A child whose `seal.key` has the x coordinate of the child-seal key and the other parity octet: `CHILD_SEAL_KEY` |
| S8-11 | Q10 | A child with the ordinal of the last row | A child with the ordinal 0 under a parent without a child-seal key: `CHILD_SEAL_KEY`. The same ordinal with a wrong `seal.key`: `CHILD_SEAL_KEY`. Neither is `CHILD_ORDINAL` |
| S8-12 | Q11 | A child that names the executor, the recipient and the limits of its row | Another executor and a limit above the row: `CHILD_AGENT_NOT_ALLOWED`. An ordinal above the number of rows and another executor than every template: `CHILD_ORDINAL`, and no template is read |
| S8-13 | Q12 | A child whose actions are a subset of `delegate.actions`, the empty set included, and one whose set equals it | An action outside `delegate.actions` and a limit above the row: `CHILD_ACTIONS_WIDER`. Another recipient and an action outside: `CHILD_GRANTEE_NOT_ALLOWED` |
| S8-14 | Q12 | A child whose window equals the window of its parent | A child whose `not_after_height` is one above the parent's, with a limit above its row: `CHILD_BUDGET_OVER`. The same child within its limits: `CHILD_WINDOW_NOT_NESTED`. One whose `not_before_height` is one below the parent's: the same code |
| S8-15 | Q13 | A row with a class; the child names a name that a holder of the landlord holds and wrote, within the limits of the row | The same child with a limit above the row, while a key that is no holder holds the name, and the child states that key as the owner key of its recipient name: `CHILD_BUDGET_OVER`, and no check of the class is made. Within the limits: `CLASS_HOLDER`, a code that LIP-0026 proposes. Within the limits, where the child states another owner key than the key that holds the name: `RECIPIENT_NAME_NOT_HELD`, by the proof of the name before the class (R9.9) |
| S8-16 | Q14 | A child inside its window whose recipient name is held by the signed owner key | A child whose window has closed at the tip and whose recipient name is held by another key: `RECIPIENT_NAME_NOT_HELD`. With the name held: `CHILD_NOT_LIVE`. A child whose window has closed and whose seal output has another script: `CHILD_NOT_LIVE` |
| S8-17 | Q15 | A child whose anchor is confirmed and spends the coin of its row | A child whose anchor is pending and spends another output than the coin: `W_ANCHOR_PENDING`, pending. Once that anchor is confirmed: `ROW_COIN_REQUIRED` |
| S8-18 | Q16 | A row with a certifier; the anchor of the child spends the coin, and a valid attestation is presented | The coin spent by another transaction, with no attestation presented: `ROW_COIN_REQUIRED`, not `CHILD_NOT_CERTIFIED`. The same with a perfect attestation: `ROW_COIN_REQUIRED` |
| S8-19 | Q17 | A child within its row, with a valid attestation | A child with an action outside `delegate.actions` and a perfect attestation: `CHILD_ACTIONS_WIDER`. A child with a window outside its parent's and no attestation: `CHILD_WINDOW_NOT_NESTED` |
| S8-20 | Q18 | The notary of the row publishes an attestation key that differs from the delegation key | The notary of the row publishes the delegation key as its attestation key, and the attestation is signed with it: `DELEGATE_KEY_REUSE`, at F23 and not at F11, without closure. With no attestation presented: `CHILD_NOT_CERTIFIED`. Another notary of the parent that publishes that key changes nothing (S4-2c) |
| S8-21 | Q19 | A row whose stop coin is unspent, with a valid attestation | The stop coin spent and the attestation signed by another notary than the row's: `NOTARY_NOT_DESIGNATED`, by F23. With the row's notary: `ROW_CLOSED_FOR_CAUSE`, also where the seal of the attestation is spent |
| S8-22 | Q20 | Under a stand-in profile that defines one action and its kinds: a request for that action, within both accounts, is reserved. Under the registries of version 0.1.55 themselves the control has no instance, because no action is defined | A request for an action that no profile of the executor defines, above the row's ceiling: `ACTION_UNDEFINED`, and nothing is reserved. A defined action that consumes a kind without a profile: `LIMIT_KIND_UNDEFINED` |
| S8-23 | F17, E3 | A row with a limit of 5 under one key; a child that states that key with 5, and one that states it with 0 | A row without that key and a child that states it with the amount 0: `CHILD_BUDGET_OVER` (LIP-0026 R2.4): the child would add a resource. A row and a child that both state no limit under the key, and a request that consumes it: the ceiling is 0, and the reservation refuses as `OWN_LIMIT_OVER` (R5.2, R5.6) |
| S8-24 | I0 to I11 | At the signing service: a listed caller, a complete child that passes every row marked for the issuer, a seal output that the service's node holds with the script of the child-seal key, and a place with no record under a usable ledger: signed once, through steps 2 to 9 of the order of one request (case S4-11) | The answers of the ledger are the cases of section 11.1 and are not restated: a replay (S4-12), another intent for a taken place (S4-13), a held place (S4-14), a lost ledger (S4-24) and a parent that is closed after the reservation (S4-30). A service that signs in any of them because I0 to I9 passed fails this case. A caller that is not identified, with a child that has a member which its list does not have: no signature exists, and the service reports no code, not `WIRE_MEMBER` (I0 before I1). A coin of the row that another transaction has spent: `ROW_COIN_REQUIRED` (F22 in I9). Further, one at a time: a seal output with the script of another key: `SEAL_SCRIPT`; a child whose `seal.key` is another key: `CHILD_SEAL_KEY`; a seal transaction that the service's node does not hold: `SEAL_OUTPUT`, pending, and signed once the node holds it; a child whose recipient name another key than the stated owner key holds: `RECIPIENT_NAME_NOT_HELD` (F19 in I8); a caller that is not listed, with a child that also names another contract: no signature exists, and the service reports no code at all; a caller that is not listed, at a node that is not healthy: no signature exists, the service makes no read and reports no code (I2 before I3); a listed caller with a child that names another contract, at a node that is not healthy: `NODE_UNHEALTHY`, not `CHILD_CONTRACT_DIFFERS` (I3 before I4); a parent that is closed in the service's journal while its node still shows the seal unspent: `PARENT_NOT_LIVE`; a child whose coin is an output of its own seal transaction, under a row that the service's journal holds as closed for cause: `ROW_COIN_IN_SEAL_TRANSACTION` (F22 before F24 in I9). In each, no signature exists |
| S8-25 | Q21 | A request under a child that fits its row and whose recipient is a name, at a healthy node on which the signed owner key holds the name, signed by the channel key that the name lists: authenticated. The same at a healthy node on which another key holds the name: `RECIPIENT_NAME_NOT_HELD` | The same request at a node that is not healthy, on which another key holds the name: `NODE_UNHEALTHY`, pending, and not `RECIPIENT_NAME_NOT_HELD`. A request under a child whose recipient is a key, signed by another key, at that node: `NODE_UNHEALTHY`, and not the refusal of A1 |
| S8-26 | Q22 | A live parent, and a child that fits it | One compound each, under a child with a limit above its row. The issuer's name of the parent changed in view, and the recent block of the parent is not on the active chain: `RECENT_BLOCK` (7.1 before 7.2). The history of the parent's issuer cannot be read, and the window of the parent has ended: `ISSUER_HISTORY_UNAVAILABLE`, pending (7.2 before 7.5). One finding each: the issuer's name changed: `ISSUER_NAME_CHANGED`; the bound registration confirmed above the recent block: `ISSUER_SNAPSHOT`; the recipient name of the parent held by another key: `PARENT_NOT_LIVE` (J4.5); the parent closed in the journal: `PARENT_NOT_LIVE`, closed; the window of the parent ended: `PARENT_NOT_LIVE`; the seal of the parent spent: `PARENT_NOT_LIVE` (S4-6). None is `CHILD_BUDGET_OVER` |
| S8-27 | Q23 | A row with a limit of 5 under a key whose kind the stand-in profile defines as a ceiling, and a child that states that key with 5 | A child that states a limit under a key that the template lacks, of a kind that no profile defines: `CHILD_BUDGET_OVER`, by (a) before (b). A child that states 6 under the key of the row, of a kind that no profile of the side defines: `LIMIT_KIND_UNDEFINED`, by (b) before (c). A row and a child that both state a limit of the kind `policy` with equal amounts: `LIMIT_KIND_UNDEFINED`, at an issuer and at a consumer alike |
| S8-28 | Q24; rule T3 | A child with `C.not_before_height <= H < C.not_after_height`, whose recent block is on the active chain at a height that is at most `C.not_before_height`: signed at an issuer, and admitted at a consumer | A child with `C.not_before_height = H + 10`: signed at an issuer; refused at a consumer at the same tip as `CHILD_NOT_LIVE`, state, and admitted there when the tip reaches that height. A child with `H = C.not_after_height`: `CHILD_NOT_LIVE` at both sides, and the issuer signs nothing. A child whose recent block is on the active chain at a height above `C.not_before_height`: `CHILD_NOT_LIVE` at both sides. A closure of the child in the journal, and a recent block that is not on the active chain: `CHILD_NOT_LIVE`, closed, by (a) before (b). A recent block that is not on the active chain, and a window that has ended: `RECENT_BLOCK`, by (b) before (d) |
| S8-29 | Q27; rule T10 | A parent of two groups whose templates and ranges meet rules 4 and 5 of LIP-0020 W11.10, and a child of the first group | A child with the ordinal 0 under a parent whose first group names a `certifier` that is no entry of `notaries`: `CHILD_ORDINAL`, by (a) before (b). A child of that first group with another executor than its template: `GRANT_DELEGATE`, by F13 before F14. A child of that first group that is signed by another key than the delegation key: `CHILD_SIGNER`, by F2 before F13. A parent whose second group has that defect, with a valid child of the first group: no code is stated, because two outcomes conform (open point O7), and this is a note and no code case |
| S8-30 | Q28; rule T11 | Stated facts, not computed (T1): both required documents are presented and recompute; each names a seal conclusively shown confirmed as named and unspent by the side's node. F6(c) passes at issuer and consumer | One defect at a time in the bound contract: no seal named, held transaction only in the mempool, no output at the named index, another script: `CONTRACT_SEAL_MISSING`, no signature, admission or closure. Non-recomputing document plus no seal: `CONTRACT_ID` before (c). No document plus no seal in what it would present: `CONTRACT_NOT_PRESENTED` before (c). No seal plus wrong terms: `CONTRACT_SEAL_MISSING` before (d). A conclusively read seal confirmed as named and spent is never this code; its spend step and closure stay open, so that is a limit and no code case here |
| S8-31 | Q28; rule T11 | For each side, the S8-30 control with conclusive own-node evidence; the same confirmation, index and script pass (c) | The named transaction is unknown to the node, including a pruned confirmed-and-spent transaction, or the read proves nothing: `CONTRACT_SEAL_UNAVAILABLE`, pending, no signature, admission or closure. It is never `CONTRACT_SEAL_MISSING`. Combine with wrong terms: still the pending code before (d). With a non-recomputing document instead: `CONTRACT_ID` before any node read. Mutant: collapse unknown into missing; this named case rejects that classification |
| S8-32 | Q28; framework scope | The bound contract names one presented framework document; both recompute and each seal is conclusively confirmed as named and unspent: issuer and consumer pass (c) | Keep the bound contract valid. Framework no seal, held mempool-only transaction, no output at index, or another script: `CONTRACT_SEAL_MISSING`; framework unknown transaction: `CONTRACT_SEAL_UNAVAILABLE`, pending. Framework document missing: `CONTRACT_NOT_PRESENTED`; wrong framework identifier: `CONTRACT_ID`, before any seal read. For precedence, bound seal absent plus framework read unavailable gives missing; bound read unavailable plus framework seal absent gives pending: bound contract first. No negative signs, admits or records closure. Mutant: check only the bound contract; this named case rejects the bypass |
| S8-33 | I4(c), I11; section 11.1, step 6 | Both seals pass the initial check and the fresh repeat after reservation: the issuer can continue toward the signer, all other gates valid | Keep the bound seal valid; the framework's fresh read becomes unavailable: event 12, `CONTRACT_SEAL_UNAVAILABLE`, pending, the place held, no signature or release. Separately the fresh read conclusively shows the transaction no longer confirmed: event 12, `CONTRACT_SEAL_MISSING`, place held, no signature. The unchanged fresh-read control continues. Mutant: retain only the bound read or reuse step 1's evidence; this named trace rejects signing on either negative |

### 8.7. Vectors planned for the step order

No vector of this repository holds a step of section 8.4 beyond F1 and F2,
which are the pipeline of LIP-0020 section 12. The tool `tools/grantv4`
reads a grant as a document and models no admission; its file and its
output do not change with version 0.1.55. The vectors below are a plan.
They are not generated, and no result is claimed for them.

Two kinds are planned. A vector "on octets" holds the signed forms of a
parent and of a child, which the pipeline reads without a refusal, and
states the first refusal of F5 and F8 to F18, the steps that signed octets
alone decide. Parts (b) and (c) of F17 also read the profiles of the side:
a vector that holds a limit states, as its context, a stand-in profile that
defines the placeholder kinds of the file as ceilings, and a vector for
`LIMIT_KIND_UNDEFINED` states a context without that profile. A vector "on
stated facts" adds what a node, a journal or a presentation would give, as
the vectors of LIP-0026 do. The planned file is
`vectors/LIP-0014/v4-steps.json`, with one valid neighbour for every
refusal and a group `compound` for the pairs. Unless a vector says otherwise,
its bound contract and any named framework document are presented and
stated to recompute, and each names a seal that the side's own node
conclusively shows confirmed as named and unspent (the four default facts
of section 8.6). Every vector past F6 inherits those facts; this does not
claim executable contract-profile or node-read coverage.

| Vector | Kind | Holds | Expected | Row or pair |
| --- | --- | --- | --- | --- |
| `step-v-01` | octets | A parent and a child that pass F5 and F8 to F18 | `ok` | S8-0 |
| `step-v-02` | octets | The child's actions empty; the child's window equal to the parent's; the child's limit equal to the row's | `ok` | F16, F17, F18 |
| `step-i-01` | octets | Another `contract` in the child | `CHILD_CONTRACT_DIFFERS` | F5 |
| `step-i-02` | octets | Another `genesis` in the child | `SUBJECT_MISMATCH` | F8 |
| `step-i-03` to `step-i-08` | octets | A delegation key equal to each key of J4.3 (a), one at a time, under either parity where the other key is an output key | `DELEGATE_KEY_REUSE` | F9 |
| `step-i-09` | octets | A parent without `child_seal_key` | `CHILD_SEAL_KEY` | F10 |
| `step-i-10` to `step-i-16` | octets | A child-seal key equal to each key of CS3, one at a time: the six keys of F9 and the delegation key | `DELEGATE_KEY_REUSE` | F10 |
| `step-i-17` | octets | A row whose recipient key is the delegation key, and the child of that row, which names it | `DELEGATE_KEY_REUSE` | F11 |
| `step-i-18`, `step-i-19` | octets | A third key as the child's `seal.key`; the child-seal key with the other parity octet | `CHILD_SEAL_KEY` | F12 |
| `step-i-20`, `step-i-21` | octets | The ordinal 0; the ordinal one above the number of rows | `CHILD_ORDINAL` | F13 |
| `step-i-22` | octets | The executor of another group | `CHILD_AGENT_NOT_ALLOWED` | F14 |
| `step-i-23`, `step-i-24` | octets | Another recipient key; a recipient by key under a class | `CHILD_GRANTEE_NOT_ALLOWED` | F15 |
| `step-i-25` | octets | One action outside `delegate.actions` | `CHILD_ACTIONS_WIDER` | F16 |
| `step-i-26`, `step-i-27` | octets | A limit one above the row's; a limit of amount 0 under a key that the row lacks | `CHILD_BUDGET_OVER` | F17; S8-23 |
| `step-i-28`, `step-i-29` | octets | `not_after_height` one above the parent's; `not_before_height` one below the parent's | `CHILD_WINDOW_NOT_NESTED` | F18 |
| `step-i-30`, `step-i-31` | octets | Under a context without a profile: a limit of 6 over a row of 5; a limit of the kind `policy` in the row and in the child | `LIMIT_KIND_UNDEFINED` | F17 (b); S8-27 |
| `step-c-01` | octets | Another contract and another `genesis` | `CHILD_CONTRACT_DIFFERS` | F5 before F8 |
| `step-c-02` | octets | Another `genesis` and a reused delegation key | `SUBJECT_MISMATCH` | Q8 |
| `step-c-03` | octets | A reused delegation key and no child-seal key | `DELEGATE_KEY_REUSE` | Q9 |
| `step-c-04` | octets | A child's `seal.key` with the x coordinate of the delegation key, which is also not the child-seal key | `DELEGATE_KEY_REUSE` | Q9, S8-10 |
| `step-c-05` | octets | No child-seal key and the ordinal 0 | `CHILD_SEAL_KEY` | Q10 |
| `step-c-06` | octets | A wrong `seal.key` and the ordinal 0 | `CHILD_SEAL_KEY` | Q10 |
| `step-c-07` | octets | An ordinal above the rows and an executor of no template | `CHILD_ORDINAL` | Q11 |
| `step-c-08` | octets | Another executor and a limit above the row | `CHILD_AGENT_NOT_ALLOWED` | Q11 |
| `step-c-09` | octets | Another recipient and an action outside | `CHILD_GRANTEE_NOT_ALLOWED` | Q12 |
| `step-c-10` | octets | An action outside and a limit above the row | `CHILD_ACTIONS_WIDER` | Q12 |
| `step-c-11` | octets | A limit above the row and a window outside | `CHILD_BUDGET_OVER` | Q12 |
| `step-c-12` | octets | A limit under a key that the template lacks, of a kind without a profile | `CHILD_BUDGET_OVER` | Q23; S8-27 |
| `step-f-01` | stated facts | A member outside the list and an unreadable history | `WIRE_MEMBER` | Q1 |
| `step-f-02` | stated facts | Another `contract` in the child at a void observation, stated once for a consumer and once for an issuer | `OBSERVATION_VOID` on both sides | Q3; S8-3; section 8.5, I3 before I4 |
| `step-f-03`, `step-f-04` | stated facts | Another `contract` in the child, with no contract presented; the contract of the parent in the child, with no contract presented | `CHILD_CONTRACT_DIFFERS`; `CONTRACT_NOT_PRESENTED` | Q5; S8-5 |
| `step-f-05`, `step-f-06` | stated facts | Another `contract` in the child under a closed parent; no contract presented under a closed parent | `CHILD_CONTRACT_DIFFERS`; `CONTRACT_NOT_PRESENTED` | Q6; S8-6 |
| `step-f-07`, `step-f-08` | stated facts | A limit above the row under a parent outside its window; under a parent whose issuer history is unreadable | `PARENT_NOT_LIVE`; `ISSUER_HISTORY_UNAVAILABLE` | Q7 |
| `step-f-09` | stated facts | A limit above the row and a recipient name that no holder holds | `CHILD_BUDGET_OVER` | Q13 |
| `step-f-10`, `step-f-11` | stated facts | A closed window with a name held by another key; with a seal of another script | `RECIPIENT_NAME_NOT_HELD`; `CHILD_NOT_LIVE` | Q14 |
| `step-f-12` | stated facts | A pending anchor that spends another output | `W_ANCHOR_PENDING` | Q15 |
| `step-f-13`, `step-f-14` | stated facts | A coin spent elsewhere without an attestation; with a perfect one | `ROW_COIN_REQUIRED` | Q16 |
| `step-f-15` | stated facts | An action outside with a perfect attestation | `CHILD_ACTIONS_WIDER` | Q17 |
| `step-f-16` | stated facts | The row's notary publishes the delegation key | `DELEGATE_KEY_REUSE` | Q18 |
| `step-f-17` | stated facts | A spent stop coin and an attestation by the row's notary | `ROW_CLOSED_FOR_CAUSE` | Q19 |
| `step-f-18`, `step-f-19` | stated facts | An undefined action above the ceiling; a kind without a profile | `ACTION_UNDEFINED`; `LIMIT_KIND_UNDEFINED` | Q20 |
| `step-f-20` | stated facts | No limit under a key in the row and in the child, and a request that consumes it | `OWN_LIMIT_OVER` | E3; S8-23 |
| `step-f-21` | stated facts | A request under a child by name, at an unhealthy node on which another key holds the name | `NODE_UNHEALTHY` | Q21; S8-25 |
| `step-f-22` | stated facts | At an issuer: a listed caller and another `contract` in the child at an unhealthy node | `NODE_UNHEALTHY` | Section 8.5, I3 before I4; S8-24 |
| `step-f-23`, `step-f-24` | stated facts | Under a child with a limit above its row: a changed issuer name of the parent with a recent block off the active chain; an unreadable issuer history with an ended window of the parent | `RECENT_BLOCK`; `ISSUER_HISTORY_UNAVAILABLE` | Q22; S8-26 |
| `step-f-25` to `step-f-30` | stated facts | One finding about the parent each: its issuer's name changed; its registration above the recent block; its recipient name held by another key; a closure in the journal; an ended window; a spent seal | `ISSUER_NAME_CHANGED`; `ISSUER_SNAPSHOT`; then `PARENT_NOT_LIVE` four times | F7; rule T8; S8-26 |
| `step-f-31`, `step-f-32` | stated facts | A child whose window opens ten blocks above the tip, stated once for an issuer and once for a consumer | `ok` at the issuer; `CHILD_NOT_LIVE` at the consumer | F20 (d); rule T3; S8-28 |
| `step-f-33`, `step-f-34` | stated facts | A child whose window has ended at the tip; a child whose recent block stands above its opening height. Each stated for both sides | `CHILD_NOT_LIVE` on both sides | F20 (c), (d); S8-28 |
| `step-f-35`, `step-f-36` | stated facts | A journaled closure of the child with a recent block off the active chain; that recent block with an ended window | `CHILD_NOT_LIVE`; `RECENT_BLOCK` | Q24; S8-28 |
| `step-f-37` | stated facts | A request signed by another key under a child whose recipient is not that of its row | `CHILD_GRANTEE_NOT_ALLOWED` | Q4; S8-4 |
| `step-f-38` | stated facts | At an issuer: a seal transaction that the node does not hold | `SEAL_OUTPUT`, pending | Section 8.5, I8; S8-24 |
| `step-f-39`, `step-f-40` | stated facts | A contract stated to recompute that names no contract seal, stated once for a consumer and once for an issuer; beside it, as its controls, the same facts with a seal that the node shows confirmed as named, once for each side | `CONTRACT_SEAL_MISSING` on both sides; the controls pass part (c) | F6 (c); rule T11; Q28; S8-30 |
| `step-f-41` | stated facts | A contract stated not to recompute, with no seal named; no contract presented, under a parent whose contract would name no seal; a contract with no confirmed seal whose terms are stated not to mirror the grant. Beside each, the S8-30 control with complete, recomputing documents, confirmed-as-named seals and matching terms | `CONTRACT_ID`; `CONTRACT_NOT_PRESENTED`; `CONTRACT_SEAL_MISSING`; each control passes F6 | Q28; S8-30 |
| `step-f-42` | stated facts | A named held seal transaction only in the mempool, once per side; control beside each: the same transaction confirmed as named | `CONTRACT_SEAL_MISSING`; controls pass (c) | F6(c); S8-30 |
| `step-f-43` | stated facts | A confirmed transaction without the named output index, once per side; control beside each: that output exists with the named script | `CONTRACT_SEAL_MISSING`; controls pass (c) | F6(c); S8-30 |
| `step-f-44` | stated facts | A confirmed output with another script, once per side; control beside each: the output has the exact named script | `CONTRACT_SEAL_MISSING`; controls pass (c) | F6(c); S8-30 |
| `step-f-45` | stated facts | An unknown transaction or inconclusive read, once per side, including a pruned confirmed-and-spent transaction and a pending read plus wrong terms; controls beside each: conclusive confirmed-as-named unspent reads and matching terms | `CONTRACT_SEAL_UNAVAILABLE`, pending, no closure; controls pass F6. No missing-seal or spend inference from an unavailable read | F6(c); S8-31 |
| `step-f-46` | stated facts | Bound contract valid; its presented identifier-valid framework has no seal, held mempool-only transaction, no output at index, or another script, one at a time for each side; controls beside each: both seals confirmed as named | `CONTRACT_SEAL_MISSING`; controls pass (c) | F6(c); S8-32 |
| `step-f-47` | stated facts | Bound contract valid; the named framework's seal transaction is unknown, once per side; control beside each: that node conclusively reads both seals confirmed as named | `CONTRACT_SEAL_UNAVAILABLE`, pending; controls pass (c) | F6(c); S8-32 |
| `step-f-48` | stated facts | Framework document not presented, then presented with a non-recomputing identifier; controls beside each: both documents presented and recomputing with confirmed-as-named seals | `CONTRACT_NOT_PRESENTED`; `CONTRACT_ID`; controls pass F6 | F6(a), (b); S8-32 |
| `step-f-49` | stated facts | Bound seal absent plus unavailable framework read; bound read unavailable plus framework seal absent. Controls beside each: both seals confirmed as named | `CONTRACT_SEAL_MISSING`; `CONTRACT_SEAL_UNAVAILABLE`, pending; controls pass (c) | F6(c); bound contract before framework; S8-32 |

The vectors on octets need a second reader in the tool, after the pipeline:
the steps F5 and F8 to F18 as functions of two grants that were read and,
for F17, of a stated set of profiles. It adds a file and a subcommand and
leaves the generator of `vectors/LIP-0020/grant-v4.json` and its octets as
they are. The vectors on stated facts wait for the forms of an observation
and of a presentation, as the admission vectors of LIP-0020 section 12 do.

No vector is planned for a defect or a pair that depends on one of the
eight open points of section 8.4 (O1 to O8). None is planned for part (b)
of F13 either: a parent that breaks rule 4 or 5 of LIP-0020 W11.10 is
refused as a document by the pipeline of LIP-0020 section 12, whose
vectors hold such parents, and the vectors on octets of this plan hold
parents that the pipeline reads without a refusal; a vector of an
admission for it waits with O7. The answers of the reservation ledger
(section 8.5, I10 and I11) have their own plan in section 11.1. And none
is planned on computed octets for part (b) or part (d) of F6 — part (c) in
texts of versions 0.1.55 to 0.1.60: the first draft planned four vectors
on changed contract octets, and they are withdrawn until a v4 contract
profile fixes the preimage of the identifier. The vectors of part (c)
since version 0.1.61, `step-f-39` to `step-f-49`, state the result of (b)
as a fact, as every vector of a result at or after (b) does (rule T1),
and none is planned for a spent contract seal, whose step and closure
are open (rule T11). The vector of Q21 holds a recipient by name, whose refusal has
a code; the second refusal of case S8-25 and the last of case S8-4, a
request with a wrong signature that nothing else refuses, have no vector
while the code of a request that is not authenticated is open. Rule T7, the
reading of a payload at an issuer, has its case in S8-2 and gets its
vectors with the class that LIP-0020 W9.1 gains for it.

## 9. Sibling budgets

The children of one parent together receive at most `P.delegate.budget` (D6).
LIP-0008 section 12.2 forbids that siblings each inherit another full copy of a
parent's budget, and it requires explicit signed partitions when the executors
keep independent journals. Children run at different agents, so the parent
signs the partitions itself, one row for each child (J1, section 9.1):

- `P.spend_budget` is what `P`'s own executor may spend. `P.delegate.budget` is
  a separate pool for children. The principal signs both, and its exposure is
  their sum.
- Each row has a `cap`, and the caps do not sum to more than the pool. A
  child's `spend_budget` is at most the cap of its row and is enforced by its
  own executor's cumulative ledger (LIP-0013 step 9). The same executor charges
  what is spent under the row to a ledger of the row as well, which every
  document of that row shares (J1.3).
- No party adds up a sum over siblings: the bound is in the signed rows. The
  signer still reserves the ordinal and the amount durably before it signs
  (section 5), and a notary keeps a record of the one child that it certified
  for each row (J1.6). Section 5 describes v3, where that signer is the
  landlord's. On v4 the delegator signs the children, and each row also pins a
  coin that the issuance of its child must spend (J1.9).

From one bundle a verifier cannot see a fork: two attestations with one parent
and one ordinal for different children. Such a pair, both signed by one notary,
is complete evidence of that notary's equivocation for anyone who holds both. A
pair signed by two different named notaries shows no fault of either notary. It
shows that the child signer used one ordinal twice, and no rule in force brings
the two attestations before one party; section 10.1 holds Draft text under
which one notary certifies a row (J2). Both children of such a pair fit the
same row, so the pair adds no party, no executor and no budget beyond that row
(section 9.1). A pair for the same child after a withdrawal is a new
certification of that child (section 10) and no fork.

A consumed ordinal and its budget stay consumed when the child is revoked or
its attestation withdrawn. LIP-0008 section 12.2 requires that reissuance does
not reset an ancestor's consumed allowance.

### 9.1. Rows: one compartment for each child

A pool that the children of a parent share has a bound only if one party sees
every child, and no such party exists. Take a parent with a pool of 100 that
names the notaries N1 and N2, where any one notary is enough (D3, D9) and each
certifies against its own record of the parent's children. Child A takes 60 and
is certified by N1, and child B takes 60 and is certified by N2, both under
ordinal 1. Each child passes every check on its own bundle, and the two hold
120 together. Neither notary signed two attestations for one ordinal, so the
pair shows no equivocation of a notary. The case needs a child signer that uses
one ordinal twice. On v3 that is the landlord's signer, which admits an ordinal
once for a parent and reserves the amount before it signs (section 5), so the
case needs an error or a compromise of that signer. On v4 the delegator signs
the children and reaches the case alone. With a pool of 0, as in Goal 1 (D12),
no amount is at stake, and the same pair still gives two children to a parent
that meant to permit one.

The first draft of this LIP had such a pool, with lists of the agents and the
grantees that a child may name. Ivan Oparin decided on 2026-11-14 to replace it
by rows (J1), and the co-author agreed on 2026-11-15. The decision changes how
D6 is read. The parent signs one row for each child it permits, and on v4 each
row also pins a coin. A row fixes the executor, the grantee, the cap and the
certifier, and a child must fit the row of its ordinal. A total needs a party
that sees every sibling; a row needs none.

| Property | Closed? | For whom |
| --- | --- | --- |
| The number of compartments of authority under a parent, and the executor, grantee, cap and certifier of each | Yes | Every verifier, one that starts later included; it is a function of signed bytes |
| Consumption under one row never exceeds its cap, whatever documents exist | Yes, when `spend` is delegable | The row's executor, while the continuity of its ledger store is proved under J1.4; no deployment profile qualifies a store for that yet. A third party cannot read it from a bundle |
| At most one child object, one `grant_id`, is ever admitted for a row | On v3: no. On v4: yes on the active chain, by the coin of the row (J1.9) | On v3 it rests on the landlord's signer (section 5) and on the notaries: each certifies one child for a row (J1.6), and only under section 10.1 is the row's certifier the one notary that can certify it. On v4 every verifier reads the spend of the coin on its own node; the property does not hold across forks |

A second document for a row names the same grantee at the same executor and
draws on the same row ledger, and every member of it must fit the parent's
delegable set; under section 10.1 it is also certified by the same notary. It
cannot add a party, an executor, an action, a repository, time or budget beyond
what the principal signed for that row. It can carry terms that the delegator
did not choose for that grantee, up to the envelope of the row. A row has
exactly one executor, and a grant is admitted only at the agent it names
(LIP-0013 step 6b), so the verifier that matters for an effect under a row is
that executor.

Section 2 states the members: the rows in `slots`, each with `executor`,
`grantee`, `cap` and `notary`, and the pool in `budget`.

The member of a row is named `executor` because the party that performs the
action can be a service as well as an agent. In the v3 grant and in the
contract the same name stays in the member `agent_name`, whose bytes do not
change.

A v4 row is not the v3 row. On v4 a row is one of the explicit signed
partitions that name each service or key and its allowance (LIP-0008
sections 4 and 12.2). It MUST carry the executor as a service name with its
pinned public key; the child's recipient in exactly one of the two modes of
LIP-0008 section 3.1, a request key, or a name with its owner key; the
limits of the row; the certifier; and the coin of the row (J1.9). The `cap`
of a row of profile `/2` is one number of coin atoms. A v4 row carries
typed limits in its place (LIP-0008 section 2). An `id/` name alone is not
a v4 executor, and the v3 `grantee` key is a recipient by key only. The
bytes come with v4.

Under J9, decided and agreed by both owners on 2026-11-15 (section 8.3), the
certifier of a v4 row is one of the notaries that the parent pins or, where
rule J9.2 holds, the statement that the row has none. LIP-0026 sections 8 and 9
state two decisions of 2026-11-15 that are in force since version 0.1.51: a v4
parent states its rows in groups (J12), and the recipient of a v4 row has a
third form, a class of landlords (J10). Under them the paragraph above is read
as LIP-0026 R8.1 and R9.1 say: a template states the executor, the recipient,
the limits and the certifier once for the rows of its group, and the recipient
is a request key, a name with its owner key, or a class.

| # | Rule | Refusal |
| --- | --- | --- |
| J1.1 | A right of re-delegation MUST fix, for every ordinal a child may carry, the executor, the grantee, the cap and the certifier. The caps MUST NOT sum to more than `delegate.budget`. | `CONTRACT_DELEGATE` |
| J1.2 | A verifier MUST first check that the child's ordinal lies between 1 and the number of rows, before it reads any row. It then requires the child to name the executor of that row as its `agent_name`, the grantee of that row, and a `spend_budget` of at most that row's `cap`. | `CHILD_ORDINAL`; then `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED`, `CHILD_BUDGET_OVER` |
| J1.3 | Before an effect that consumes a countable resource under a child, the executor MUST reserve the amount atomically in two cumulative ledgers: the child's, bounded by the child's limit, and the row's, keyed by `parent_grant_id` and ordinal and bounded by `cap`. If either reservation fails, the executor MUST refuse and MUST reserve nothing. These reservations are added to every other check and reservation that applies, and replace none: the check of one request in step 6g of LIP-0013, the child's v3 budget, and on v4 every ancestor link (LIP-0008 section 12.2). One request identity, the event id or the invocation's nonce, is charged once, also when it is retried. The row ledger draws on `delegate.budget` only; `P.spend_budget` stays the separate account of `P`'s own executor (section 9). | A failure of the row's reservation: `ROW_CAP_OVER` |
| J1.4 | The row ledger lives in a ledger store whose continuity is proved against a record outside the store. The contract of that store follows this table. | A lost store refuses every consuming effect under every row |
| J1.5 | A verifier MUST NOT rely on a statement of a notary or of a signer about a sum over siblings. The attestation carries no such statement. | none of its own |
| J1.6 | A notary MUST NOT certify two different children, two `child_grant_id` values, under one parent and ordinal, ever, also after a revocation or a withdrawal. It MAY sign again for the same child. Two attestations by one notary for different children of one parent and ordinal are complete evidence against it, as section 9 says. The notary keeps a durable record for this. On v3 the landlord's signer still admits an ordinal once (section 5). | none at a verifier that holds one bundle |
| J1.7 | "Used" names three different facts, and on v3 none of them is public state about how many child objects exist: the reservation of the ordinal at the v3 landlord's signer; the notary's record of the child it certified for the row; and consumption in the row ledger, which is state of the row's executor, the verifier that consumes. Each is permanent: a revoked child, a withdrawn attestation and a reissue free none of them. A new child takes another row. | none of its own |
| J1.8 | A verifier, a receipt and a report MUST NOT state that a child is the only child of its row. On v4 they may state it for the active chain and for nothing wider (J1.9). | none of its own |
| J1.9 | v4 only. Each row pins one coin: an output that is confirmed before the parent is signed and that pays a key of the re-delegating side. That key is a separate key: the signer of that side's operator derives it from its seed, in an account of its own, as seal keys are derived (LIP-0008 section 11.1), and it is neither the delegation key nor the messaging key. The issuance of a child MUST spend the coin of the child's row in the transaction that carries the child's commitment, and a verifier checks that input on its own node. A row whose coin another transaction spent admits no child. The exclusivity holds on the active chain and not across forks: after a reorganisation that removes an issuance, another child can spend the coin on the new chain. | A v4 child whose issuance does not spend the coin of its row refuses. The code is fixed with the v4 bytes |

The ledger store of J1.4 has an identity, given once by the executor's
operator, and a position that only moves forward. Where a restore of the
store cannot move it back, the executor keeps the outside record. The
outside record MUST bind three things: the identity of the store, its
position, and the exact committed history of the ledger, which includes
consumption and the state that charges a request identity once. A row's
record is created with consumption 0 by the first reservation under that
row, in the same atomic write, and only in a store whose continuity check
passes. That is the first use.

- **Order of one reservation.** First the reservation and the store's next
  position are written in one atomic write. Then the commitment to the
  resulting history is made durable in the outside record. The outside
  record takes it only as the successor of the exact history it holds, and
  only from the current fenced writer. Only then is the effect performed or
  success acknowledged: no consuming effect and no acknowledgement of
  success occurs before the exact resulting commitment is durable outside
  the domain that a restore reaches. The other order, outside record first
  with a reservation that is never used again, is safe and turns every
  crash in that window into a lost store. It is another profile and MUST
  NOT be mixed with this one.
- **The continuity check** runs at start, when a replica joins, and before
  every reservation. Equal positions alone establish nothing. A store is
  intact only if the identity of its committed history matches the outside
  record. A store that is one transition ahead of the outside record may
  complete that transition only if the transition extends the exact history
  that the outside record holds and the condition of the fenced writer
  still holds; no effect was performed for it, the reservation stays
  charged, and the executor completes the outside write before it does
  anything else. Every other state is a lost store: a history that is
  inconsistent with the outside record, also at an equal position; a
  history that cannot be proved; a store behind the outside record, which
  is what a restore to an earlier position looks like; a store ahead by
  more than one transition; an outside record that is absent or unreadable;
  another identity; a store that is absent or was created anew.
- **Replicas.** All replicas reserve in the one store; a replica holds no
  ledger of its own that it may write. Writes are fenced: the store accepts
  a reservation only from the writer that holds its current write token, a
  number that only increases, so a replica that was cut off and returns
  with an older token reserves nothing and publishes nothing to the outside
  record. A replica that cannot reach the store or the outside record
  refuses. A replica joins by receiving the store; it never starts empty.
- **A lost store.** An executor, or a replica of it, with a lost store MUST
  refuse every consuming effect under every row and MUST NOT treat a
  missing record as a first use. Recovery is one of two acts of the
  operator: restoring the complete store with its continuity proven against
  the outside record; or charging as fully consumed every row that could
  have had a record in the lost store, whether or not any list of those
  rows survived the loss. After a recovery by charging, a row has a first
  use only where the executor can show that its parent did not exist when
  the store was lost. One way that needs no list: the new store records a
  boundary block that is known to have been mined after the loss, and only
  a parent whose signed checkpoint (section 7.1) lies above that block on
  the active chain can have a first use; such a parent was signed after the
  loss. How the profile knows that the boundary is later than the loss,
  with a node that may lag, is part of the open profile. A recovery that
  cannot show this charges every row. Recovery MUST NOT turn an old row
  whose record is unknown into a new row.
- **What the record survives.** The record survives revocation, withdrawal,
  a new attestation, reissue, restart and reorganisation. A changed owner
  of the executor's name does not start a new ledger: the key is the parent
  and the ordinal, and a new holder without the store has a lost store.

A position alone cannot serve as the test, because two different histories
can stand at one position. Rows A and B each have a cap of 60. A
reservation of 40 for A is written at position 1, and the process stops
before the outside write; that image of the store is kept. The store is
restored to position 0. A reservation of 40 for B takes position 1, the
outside record follows, and the effect is performed. Then the first image
is restored. Its position equals the outside position, yet it holds no
record of B, and under a test of positions a further 40 under B would pass
as a first use: 80 against a cap of 60. No outside record went backwards in this history, no old
writer was used, and every effect followed its outside write. The history
is a trace against the rule; no store was run for it. An outside record
that binds the committed history tells the two images apart.

This is the contract that a deployment profile must meet, not a qualified
mechanism. How the outside record commits to the history, and how
continuity is proved, is an open deployment profile; a log whose entries
are bound by hashes is one possible form. Nothing of it was built or run,
and no executor qualifies for `spend` without that profile and before the
cases S1-5, S1-5-ABA and S1-6 pass on its real store. The closure journals of section
10.1 and of LIP-0008 section 5.2 and the denials of LIP-0013 section 3.6
also have to tell an empty store from a lost one; a profile that compares
positions only does not serve them either.

[LIP-0025](LIP-0025-journal-continuity.md) proposes one form of that
profile: a history bound by hashes, an outside record that takes only the
successor of the state it holds, and a block boundary for a recovery, with
vectors. They are that draft's proposals; it selects no store, and each
point stays open until both owners accept it.

[LIP-0026](LIP-0026-rows-and-accounts.md) proposes a first profile for rows
on v4: what a row states, the checks of a child against its row, the coin
of a row with the account of its key, and the accounts that a request
debits, with vectors. They are that draft's proposals, and each point stays
open until both owners accept it.

The decision replaced these parts of the first draft, and this LIP no longer
holds them: the members `agents`, `grantees` and `max_children` of the right of
re-delegation; two members of the attestation, `budget` and
`prev_attestation_id`, so that the attestation has eighteen members; step V15
with the code `ATTESTATION_ARITHMETIC`; the predecessor attestations in the
bundle of V2; the statement that a chain of attestations makes the pool
arithmetic checkable; and the notary's ledger of the sum. The notary's own
record stays and is relied on: one child for each row (J1.6).

In the steps of section 8, V8 checks the range of the ordinal first and then
`agent_name` and `grantee_key` against the row, and V9 compares `spend_budget`
with the row's `cap`. Step 9 of LIP-0013 makes the reservations of J1.3. The
signer's display of section 5 includes the row's cap and certifier. On v3 the
rows are members of the draft profile `/2`. No v3 grant byte, consent rule or
`rental.Check` rule changes; a `/2` contract has other bytes and another hash
than a `/1` contract, as every new contract does. Under D12 every cap is 0 and
`spend` is not listed, so J1.3 and J1.4 are dormant in Goal 1.

What stays open:

- **One child object for each row, on v3.** A second document for a row exists
  if the row's certifier breaks J1.6 or the landlord's signer fails. Until the
  co-author agrees to J2, another notary that the parent names can certify it
  as well (section 10.1). A verifier that starts later admits it. It stays
  inside the envelope of the row.
- **One child object for each row, on v4, across forks.** The coin of J1.9
  admits one issuance for a row on the active chain. After a reorganisation
  that removes that issuance, a thief of the delegation key (section 11.1)
  who can also have the coin spent can issue another child that spends the
  coin on the new chain. Spending the coin takes the key of the coin, or
  the operator's signer, which holds that key; the delegation key alone
  spends nothing. The decision accepts this boundary.
- **Who funds the coin of a row.** The key that the coin pays is decided:
  a separate key, derived from the seed of the operator's signer in an
  account of its own. The delegation key of section 11.1 signs child grants
  and no transaction, and that rule stands. Who funds the coin, and the
  account and the path of its key, are not fixed.
- **The split is fixed when the parent is issued.** Moving budget between
  rows, or adding a row, needs a new parent, which is an ordinary issuance
  with its chain cost. The delegator cannot choose later which worker gets
  which row.
- **J1.4 names a contract, not a format.** The form of the outside record,
  the way it commits to the ledger's history and the place where it lives
  are a deployment profile, the same open item as the recovery and
  anti-rollback profile of LIP-0008 section 5.1. Without something outside
  the store, no store can notice that it was replaced as a whole. An
  outside record that is written after the effect cannot notice a rollback
  across a crash, and one that is restored together with the store notices
  nothing either: where it lives decides what the check is worth, and that
  is open. No spend qualification is claimed.
- **An executor that ignores the contract profile** enforces only the v3
  `budget` of each child (LIP-0013, security consequences). D12 keeps
  `spend` undelegable while such executors exist.
- **Size.** Sixteen rows with the longest names that the syntax allows do not
  fit 8192 bytes; the contract then refuses under rule 1 of LIP-0013 section
  2.3. In the vectors of section 12 a root with sixteen rows and four notaries
  takes 3691 bytes when its names have 17 bytes, and a root of exactly 8192
  bytes holds sixteen rows whose executors have names of 213 bytes.

What the limit is was a choice among four options:

| Option | What it gives | Cost |
| --- | --- | --- |
| (a) The limit is a number of compartments | The first two properties of the table above. Two attestation members and one verifier step go away, and the notary adds up no budget. | A new parent to move budget or to add a child. One child means one compartment; one grant for each row rests on the notary and, on v3, on the signer. |
| (b) (a) with an occupancy record at the row's executor: the executor binds a row to the first child id it admits, also when every amount is 0 | One child grant for each row at the only place where the row has an effect, for what that executor itself admitted and while its store was continuous. It is no statement that no other document exists. | The store of J1.4 is needed already in Goal 1. A lost record ends the row. The first document presented wins, so a wrong first document costs a row. |
| (c) (a) with a pinned coin for each row that the child's issuance must spend | One child grant for each row on the current chain, for every reader, auditors included. It is exclusivity on the current chain, not across forks. | One reserved, confirmed output for each row before the parent is signed; a check of issuance inputs that no v3 verifier makes today (LIP-0004 section 4); and the holder of the coin's key can void an unissued row by spending its coin. |
| (d) The free pool of the first draft | The delegator chooses freely. | The case of the first paragraph stays. |

Ivan Oparin decided on 2026-11-14: option (a) for profile `/2` on v3, with
the limit named a compartment limit, and option (c) for v4, where the
delegator signs children alone. On v4 the coin of a row pays a key of the
re-delegating side (J1.9). A further decision of the same day names that
key: a separate key, derived from the seed of the operator's signer in an
account of its own, as seal keys are derived. The decision on rows accepts
the boundary of (c): one
child for each row holds on the active chain only. Options (b) and (d) are
not taken. D7, D10 and D12 are unchanged, and the landlord's reservation on
v3 is kept. The co-author agreed to J1 on 2026-11-15.

Three further designs were set aside. Shares for each executor, in which
each executor sums what the children presented to it spend, by the parent's
id, bound consumption and leave the number of compartments open; moving
budget between shares would need an agreed state of its own. A chain of
spends through the attestation anchors, in which the anchor of each
attestation spends an output of the anchor of the previous one, gives an
order of allocations at the price of an input and an output for each anchor,
and the executor must still account consumption. One ledger notary, or all
notaries together, would give one child for each row by trust in one party;
it changes D9 and adds a party that must always be reachable.

Cases (J1). Each refusal stands beside a valid control: a suite that feeds a
malformed contract to a parser and counts the rejection proves nothing. Cases
of the spend profile are no part of the Goal 1 suite (D12). The vectors of
section 12 hold the cases that two contracts decide, which are S1-1, S1-1m,
S1-2b, S1-4 and S1-8.

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S1-1 | Rows 1 (`id/x`, `G1`) and 2 (`id/y`, `G2`), caps 0; a child of each row, certified by its row's notary, is admitted | One binding changed at a time: a child with ordinal 1 that names `id/y`, and one that names `G2`: `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED`, each with a valid attestation and never `CHILD_NOT_CERTIFIED`. A reader that only looks for the agent and the grantee somewhere in the rows admits both. |
| S1-1m | Spend profile: caps 60 and 40, pool 100; children of 60 and 40 | A child of 60 under row 2: `CHILD_BUDGET_OVER`. A reader that compares the child with the pool admits it, because 60 is at most 100. |
| S1-2a | One row, pool 0; one child with ordinal 1 | A second child with ordinal 1 for another grantee or executor refuses at V8. For the same grantee and executor with another named notary it refuses as `NOTARY_NOT_DESIGNATED` under section 10.1; until the co-author agrees to J2 it is admitted on its own bundle. |
| S1-2b | A child with ordinal 1 | An ordinal above the number of rows refuses as `CHILD_ORDINAL`, before any row is read, without a crash and without a code that names the agent. A contract that names a parent with ordinal 0, or with an ordinal above 16, never reaches that step: it refuses at 6d as `CONTRACT_PARENT` (section 3.1, rule 8). |
| S1-K1 | One row with cap 0; child `C1` certified by the row's notary | A known limit on v3: a second child `C2` of the same row, with another id, also certified by that notary in breach of J1.6, shown to a verifier that never saw `C1`, is admitted, and the vector records this verdict. On v4 the issuance of `C2` cannot spend the coin of the row (S1-10). |
| S1-3 | Spend profile: two documents of row 1, cap 60; 30 spent under the first; exactly 30 more under the second succeeds | One atom more refuses as `ROW_CAP_OVER`; both ledgers are read afterwards, and the child's ledger holds no partial reservation. The second document carries a valid attestation, so the refusal is the ledger's. A ledger for each child admits 60 under each. |
| S1-4 | Caps that sum to exactly `budget`, and caps below it; each row with its four members and a listed notary. Two rows that name the same executor and the same grantee, each with its own ordinal and cap, are a valid parent, and a child of each row is admitted under its own ordinal; a reader that refuses the repeat fails this control | Four separate negatives: a larger sum; a row with a missing member; a row with an extra member; a row whose `notary` is not in `notaries`: each `CONTRACT_DELEGATE`. The sum is checked at the largest allowed values without overflow. |
| S1-5 | Spend profile, at the store: first use of a row in a store whose continuity check passes; after 40 is spent and the child revoked, a restart with the store intact leaves 20. A crash after the store write and before the outside write: no effect was performed, and after the restart the reservation is charged once and the same request identity completes | The same row after the store was lost, created anew or rolled back: no `spend`, no first use. An unreadable store refuses and reserves nothing. Each a separate negative: a reservation of 40, the effect, a crash, and a restore of the backup taken before the reservation: lost store, no further `spend`; a rollback of the ledger alone; a rollback of the ledger together with every file beside it on the store's host; a missing or unreadable outside record; a replica with an older write token; a recovery by charging in which the list of rows was lost with the store: a row of a parent that existed before the loss gets no first use. |
| S1-5-ABA | Spend profile, at the store: a restart with the image that was actually committed at position 1 spends only the true remainder of 20; and a transition that is pending on the history that the outside record still holds completes once, without a second charge and without an effect before the outside write | Two histories at one position. An image is kept from the window between the store write and the outside write; the store is restored to the image before it; a different reservation commits at the same position; the first image is restored: the executor refuses before any further consuming reservation or effect, although the positions are equal. The planted defect `continuity-counter-only` keeps the presence of the outside record, its identity, the order of writes and the fencing, and drops the comparison with the exact committed history; a suite must catch it with this negative. An implementation that always refuses must fail the two controls. |
| S1-6 | Spend profile, at the store: 40 and then 20 against a cap of 60, from two real callers | Two replicas race 40 and 40 through their public entry points: the committed total is at most 60, and the refused caller holds no reservation. With the shared store unavailable neither succeeds. |
| S1-7 | The same child with a new valid attestation after a plain withdrawal spends the true remainder | The consumption before the new attestation is still charged; a new attestation id, signature or run does not reset it. Section 9 already forbids the reset. |
| S1-8 | Goal 1: every cap 0 and no `spend` | A positive cap or a listed `spend` refuses as `CONTRACT_DELEGATE`. D12 already forbids it; the case shows no new closure. |
| S1-9 | An attestation of exactly eighteen members, with a valid signature and bindings, admitted | An attestation that carries `budget` or `prev_attestation_id` refuses as `ATTESTATION_SHAPE`. Earlier revisions of this LIP described that form of twenty members; the case fixes the shape and shows no protection. |
| S1-10 | v4: a child whose issuance spends the coin of its row and is confirmed | Each a separate negative: a child whose issuance spends another output and leaves the coin of its row unspent; a second child of the row after the first issuance spent the coin; a child of a row whose coin another transaction spent before any issuance. Each refuses. |
| S1-K2 | v4: the same control | A known boundary of the coin: a reorganisation removes the first issuance, and a second child whose issuance spends the coin on the new chain is admitted there. The vector records this verdict as the accepted boundary. |

## 10. Revocation and closure

| Event | Effect |
| --- | --- |
| The landlord spends `P`'s seal | `P` closes durably. Every child refuses at V5 for every verifier that runs section 8. |
| The same, seen by a v3 reader that ignores the contract | That reader would keep a child with `land` alive. On v3 the signer therefore revokes a parent in one transaction that spends the seal of `P` and the seal of every child. All of them pay the landlord's grant key, so one transaction can spend them, and every v3 verifier closes every child. |
| The landlord's grant key or an agent's landlord pointer changes | The grants it covers close under LIP-0004 section 5, parent and children alike. |
| `C`'s seal is spent | Only `C` closes. `P` and the siblings stay live. |
| The notary spends the seal an attestation names | That attestation is withdrawn (D5). The child refuses at V18. Its own seal stays unspent, and siblings are unaffected unless their attestations name the same seal. An executor that observed the spend, in the mempool or in a block, journals the withdrawal durably and keeps refusing that attestation after a reorganisation. |
| `P` is replaced by a grant under a new contract | The new grant has a new `grant_id`. Children of the old one name the old id and close with it. An attestation is not renewed; the delegator requests new children. |

After a plain withdrawal the same child may be certified again by a notary that
`P` names, with the same ordinal (D5). A withdrawal for cause blocks that. The
notary marks it in the transaction that spends the seal, with one LIP-0005
frame:

| Action | Name | Payload |
| --- | --- | --- |
| `0x05` | notary withdrawal for cause | `version(1)` \|\| `withdrawal_commitment(32)` \|\| `locator` |

```text
withdrawal_commitment = SHA-256( "swarma-attest-cause-v1" || attestation_id
                                 || child_grant_id )
```

The locator has type `0x01` and its pointer is `attestation_id`. The frame
states that the withdrawal is for cause and for which attestation. The record
that states the cause, its bytes and its signing domain are open, as the
verdict record of LIP-0011 is.

After a withdrawal for cause a named notary MUST NOT certify that child again,
the landlord's signer revokes the child when it observes the frame, and an
executor that observed it journals the child as closed. The delegator requests
a new child with a new ordinal. These duties reach only a party that
observed the frame. Another named notary and a verifier that starts later
have no step that looks for it. Section 10.1 states the case and holds
Draft text for it, under a decision that awaits the co-author's agreement (J2).

### 10.1. One certifier for each row, and the withdrawal for cause

Decided by Ivan Oparin on 2026-11-14 (J2); the co-author's agreement is
pending. The decision touches D5 and D9 and builds on the rows of section 9.1.
On v3 each row has one certifier, and D5 is narrowed. On v4 each row also names
a stop coin of its notary, from the first version. Until the co-author agrees
the text in force stands: any notary that the parent names certifies a child,
whatever notary the child's row names, and a withdrawal for cause reaches only
the parties that observed its frame.
The frame of section 10 is addressed by the attestation id: its commitment
covers that id and the child's grant id, and its locator points at the
attestation. No step of section 8 looks for it. Notary N1 withdraws its
attestation of child C for cause. N2, which the parent also names, did not
observe the frame and certifies C again when it is asked. A verifier that
starts afterwards receives C with N2's attestation, and every step from V10
to V18 passes: V18 reads N2's seal and the verifier's own journal. The case
holds while C's own seal is unspent: until the landlord's signer has
revoked C, or for as long as that signer has not observed the frame. To
find the frame from the child's id, a verifier would have to test every
`0x05` frame on the chain against that id. No rule asks for that, and none
says when such a search is complete.

Under this subsection each row names exactly one notary, and only that
notary certifies the row. The notary keeps one succession of seals for the
row, so that one spend for cause withdraws every attestation of the row,
and a cause counts only when the notary's own signature covers its frame.
Two words are used below. A witness is a verifier that itself validated an
event, in its mempool or in a block, and journalled it. A view is the
active chain of a node together with its mempool.

| Property | Closed? | For whom |
| --- | --- | --- |
| After a cause, another named notary cannot certify the row | Yes | Every verifier, one that starts later included: the row names its one certifier |
| A verifier that saw the cause refuses every later attestation of the row, also for a child signed again under the same ordinal | Yes | Witnesses of an authenticated cause (J2.4) |
| An attestation of the row that was signed before the cause does not survive it | In a bounded form, for a notary that follows J2.3 (a) and (b): in every view that holds the cause transaction, every seal of the row's succession is spent or absent | A verifier whose chain or mempool holds the cause. Not a view from which the cause is gone, and not an attestation whose seal lies outside the succession |
| The row's own notary cannot certify the row again after its cause | On v3: no. On v4: yes, by the stop coin of the row (J2.7) | On v3 a verifier that starts later admits a new attestation by that notary; this is D5 as the owners wrote it, and the v3 form does not give it. On v4 every verifier whose node shows the spend of the stop coin refuses the row |

**D5 is narrowed on v3.** D5 says that a child may not be certified again
after a withdrawal for cause. With one certifier for each row and nothing
more, D5 becomes narrower: the notary is forbidden to certify the row
again, its witnesses enforce that, the landlord's signer revokes the child,
and a verifier that starts later relies on the notary's conduct. By the
decision of 2026-11-14 profile `/2` on v3 takes this narrower form
knowingly. v4 takes the stronger form of J2.7, under which D5 holds as the
owners wrote it.

On v3 the row gains nothing beyond its member `notary` (section 9.1), and
the child and the attestation gain nothing. On v4 the row gains one member,
the stop coin (J2.7). Three states are kept apart; they have different triggers,
a different reach and different codes:

| State | Trigger | Effect | Code |
| --- | --- | --- | --- |
| Attestation withdrawn | The seal it names is spent, in the mempool or in a block, or does not exist on the verifier's node (V18, as in force), or the verifier journalled that spend | That attestation refuses. A new attestation by the row's notary that names another seal is admissible; a verifier does not check the succession of J2.3 (a) from one bundle | `NOTARY_WITHDRAWN` |
| Row closed for cause | The verifier authenticated a cause for the row (J2.4); on v4 also: the stop coin of the row is spent (J2.7) | Every child of that parent and ordinal refuses, whatever attestation is presented | `ROW_CLOSED_FOR_CAUSE` |
| Child revoked | The child's own seal is spent | That child refuses for every verifier under the existing v3 or v4 rule | the existing seal code |

A seal spend without an authenticated cause produces the first state only.
A missing or unreadable frame never forbids a later plain certification.

| # | Rule | Refusal |
| --- | --- | --- |
| J2.1 | Each row MUST name exactly one notary, listed in `notaries`. Rows of one parent MAY name different notaries, also for the same executor and grantee. | `CONTRACT_DELEGATE` |
| J2.2 | A verifier MUST refuse an attestation whose `notary_name` is not the notary of the child's row, also when the parent names that notary for another row. | `NOTARY_NOT_DESIGNATED` |
| J2.3 | The duties of the row's notary, (a) to (d). A verifier cannot check them from one bundle. | none at a verifier |
| J2.3 (a) | One succession of seals for each row. The first attestation that the notary signs for a parent and ordinal names the row's first seal. Every later attestation for that parent and ordinal names a seal of the same succession: a seal already named for the row, or a successor, which is an output of the transaction that spends a seal of the succession. One spending transaction creates at most one successor for a row. The notary names for the row no output that is not reached from the first seal in this way, also not after a withdrawal, an eviction, a reorganisation or a restart. A transaction that creates a successor is a seal creation: its inputs are signed with `SIGHASH_ALL` without `ANYONECANPAY`, and it takes its funding from confirmed outputs (after LIP-0008 section 1.1). The notary signs with the seal of the succession that exists unspent on its own node, and SHOULD wait until the transaction that creates a seal, the first seal included, is confirmed before it names that seal: a transaction that is replaced leaves an attestation naming an output that never exists, and for a first seal it leaves a row that the notary can no longer certify. The notary keeps a durable record of the succession: every seal it named for the row, the transaction that spent it and the successor that transaction created. A notary that cannot produce that record for a row MUST NOT sign for that row again. | none at a verifier |
| J2.3 (b) | To withdraw for cause the notary spends the seal of the succession that exists unspent on its node, in a transaction that meets J2.4 and creates no successor for that row. It keeps that transaction and every unconfirmed transaction it depends on, and broadcasts them again for as long as they can still confirm. If its node later shows the cause gone and unable to confirm, it withdraws for cause again, with the seal of the succession that is then unspent on its node. | none at a verifier |
| J2.3 (c) | After a withdrawal for cause the notary MUST NOT sign another attestation for any child of that parent and ordinal. | none at a verifier that starts later; `ROW_CLOSED_FOR_CAUSE` at a witness |
| J2.3 (d) | After a plain withdrawal the notary MAY attest the same child again (D5), naming the successor that the withdrawing transaction created. A plain withdrawal that creates no successor leaves the row without a seal that the notary may name, for as long as that transaction stands. | none |
| J2.4 | A cause is authenticated for a verifier only when all of this holds on its own node. (1) The verifier holds an attestation `A` that is authentic and bound. Its bytes are canonical and its signature verifies (V11). Its kind, network, genesis, principal, both grant ids, both contract hashes and its ordinal equal those of the `P` and `C` that the verifier holds (V14). Its `notary_name` is the notary of that row (J2.2) and passes the walk of section 7.1. The signing key is one that this name yielded under the bound owner, either at this verifier's own earlier admission of `A`, whose record names the `attestation_id` (section 8.2), or in the block that confirms `A`'s anchor (V17). The key in force today is not required. (2) The transaction spends exactly the outpoint `A.notary_seal` under the script that member names, and the signature that authorizes that input is `SIGHASH_ALL` without `ANYONECANPAY`, so that it commits to every output. (3) The transaction has exactly one `OP_RETURN` output, the action `0x05` frame, and its commitment recomputes from the pointer of its locator and the `child_grant_id` of `A` (section 10). The pointer need not be the id of `A` itself: under J2.3 (a) several attestations of one child name one seal, and the notary's signature over a frame for that child is what is authenticated. | Purported attestation bytes, a reported transaction id, a frame in another transaction and a frame that the seal signature does not cover authenticate nothing |
| J2.4a | A verifier that authenticated a cause, in its mempool, in a block, or in a transaction that was shown to it and that it found on its own node, MUST journal the pair of `parent_grant_id` and ordinal as closed for cause before any further admission. The record survives restart, eviction, non-confirmation, reorganisation and a later rotation of the notary's key. A shared seal is no exception to locality: the spend withdraws every attestation that names the seal, and it closes for cause only the row of the attestation that the frame commits to. | `ROW_CLOSED_FOR_CAUSE` for every child of that parent and ordinal |
| J2.5 | An unauthenticated frame is neither a closure nor proof of misconduct. A misconduct claim MUST include evidence that establishes the alleged violation of J2.3; a matching commitment alone is insufficient. A claim that the notary's key certified a row again after its cause, a breach of J2.3 (c), MUST include an authenticated cause under J2.4 and evidence of the order: the later attestation's `tip_hash` is the block that confirms the cause or a descendant of it, so that it cannot have been signed before. An attestation with an older attested tip shows no order, and the height of an anchor does not date a signature. A claim of a breach of J2.3 (a) needs the transactions named below and no cause. Where the order or the transactions cannot be shown, the report says "not established". | none; a rule for a reader of evidence |
| J2.6 | On v3 the landlord's signer MUST spend the child's seal once it authenticated a cause for the child's row, observed or shown, and it admits no further request for that ordinal (sections 5 and 10). | none at a verifier; the signer refuses the request |
| J2.7 | v4 only: the stop coin of a row. The row gains a member `stop`, an outpoint. The output exists and is confirmed before the parent is signed, so the row's notary takes part in the parent's issuance. It is an output that the notary alone can spend, given like a notary seal by transaction, index and script (section 6.1, member `notary_seal`); it needs no new spending condition, and it pays a key of the notary that is not its attestation key (section 6.3). A verifier requires `stop` to exist with the named script and to be unspent, the mempool included, and journals a validated spend as it journals a seal spend. The notary ends a row for cause by spending `stop`; the `0x05` frame in that transaction is evidence and no longer the trigger. A plain withdrawal leaves `stop` alone. With the stop coin the third property of the table above does not depend on the succession of J2.3 (a). The output is bound by outpoint, so a rotation of `attest` does not touch it, and the notary must keep its spending key for the life of the parent. If the notary loses that key, the row can no longer be ended for cause, and the stops of the v3 form are what remains. After a reorganisation that removes the output the row refuses until the output is confirmed again. The fee of that spend is the notary's own and must not hang on a coin that somebody else can spend first, for the reason LIP-0008 section 5.2 gives for an issuer's break. A profile in which more than one notary may certify a row, or in which a verifier that starts later must refuse after a cause, MUST have such a state; without it a profile MUST NOT offer either. | A spent `stop`: `ROW_CLOSED_FOR_CAUSE` for every child of the row, whatever seal an attestation names, in every view that holds that spend |

What follows from J2.3 (a), and what does not. In one view a transaction is
present only together with the transactions it spends from, and two
transactions that spend one output are never both present. So a successor
is present only where its predecessor is spent, and two successors of one
seal are never both present. At most one seal of a row's succession exists
unspent in a view; and in a view that holds the cause transaction every
seal of the succession is spent or absent, so every attestation that names
one refuses at V18. This says nothing about a view that does not hold the
cause, and nothing about a seal outside the succession. Nothing that the
notary observed enters the argument: "unspent" belongs to a view and can be
undone, and an order written into the transactions cannot.

Evidence of a breach of J2.3 (a) is a fact about transactions and never
about a moment. Two authentic attestations of one parent and ordinal show a
breach only if all of this holds: their seals are different outputs; the
two creating transactions can stand in one chain, which means that no
output is spent by two different transactions among them and their
ancestors; and neither creating transaction is, or descends from, a
transaction that spends the other seal. Whoever asserts a breach produces
those transactions and the ancestry between them; where they are not
available, the breach is not established. That two seals are unspent at
one block, or that an earlier seal is unspent again after an eviction or a
reorganisation, shows nothing about what the notary did and MUST NOT be
reported as a breach.

The steps change as follows. V12 compares `notary_name` with the row before
it reads the name. V18 keeps the seal check and adds that the journal holds
no closure for cause of this parent and ordinal. On v3 no new read is added;
on v4 the verifier also reads the stop coin of the row. One seal may still
serve every attestation of a parent (section 6.4): a successor may serve the
rows that its predecessor served, and a spend for cause of a shared seal
creates no successor for the row it closes and may create one for the
others.

[LIP-0027](LIP-0027-row-stop.md) proposes a first profile for the stop coin
of a row on v4: what a row states for it, the reads of a verifier, the
record of a row closed for cause and the notary's side, with vectors. They
are that draft's proposals, and each point stays open until both owners
accept it.

With these rules D9 reads: one attestation is enough, by the notary that
the parent names for the child's row. D5 reads on v3: a
withdrawal is durable at its witnesses and on a chain that holds it; after
a plain withdrawal the row's notary may certify the same child again; after
a withdrawal for cause the notary must not, its witnesses refuse the row,
and the landlord's signer revokes the child. On v4 the last clause reads:
and every verifier whose node shows the spend of the row's stop coin
refuses the row. A spend that never reached a verifier's chain or mempool
is unknown to it in both forms.

What stays open:

- **The row's own notary after its cause**, on v3. If the row's notary
  signs again after its own cause, through a restored state, a stolen
  attestation key or a deliberate breach, a verifier that did not witness
  the cause admits the new attestation until one of three things happens:
  the child's seal is spent by the landlord's signer under J2.6; the notary
  replaces its attestation key in its name; or the parent is closed. The
  pins of section 7.1, the caps of section 9.1 and the issuer closure of
  LIP-0008 section 5.2 do not help here. On v4 the child's seal is the
  delegator's, and the stop coin is what closes the row for a verifier
  that starts later.
- **A thief of the attestation key can also close.** It signs an
  attestation for a real child, with its own seal, and spends it with a
  signed frame. Every witness closes the row. That is the notary's own
  power in a thief's hands; the row is lost, and nothing is widened.
- **Availability.** Only the row's notary can sign again after it rotated
  its key, after a reorganisation dropped the attested tip (V16) or after
  its own plain withdrawal. If that notary is gone, the row is unusable. A
  second row with another notary is a new delegation under another ordinal
  and not a second way to certify the old child.
- **A cause that left the view.** A cause seen only in a mempool and then
  evicted is refused by its witnesses and not by a verifier that starts
  later, in both forms, as for every seal (LIP-0008 section 5.1). If
  the cause is evicted before it confirms, or a reorganisation removes it,
  the seal it spent is unspent again in that view, and a verifier without
  a journal admits the attestation that names it until the cause is
  confirmed again. J2.3 (b) makes the notary broadcast it again; if the
  notary is gone, nothing does. On v4 the same holds for the spend of the
  stop coin.
- **A seal outside the succession.** A notary that names one, by a fault or
  after losing its record, leaves an attestation that the cause does not
  touch.
- **The succession itself.** Its argument rests on two properties of a
  view: a transaction is present only with what it spends from, and one
  output has one spender. Its costs: the successor is created in the
  withdrawing transaction, sometimes without ever being used; and a row
  whose succession the notary cannot continue, because its record is lost
  or a creating transaction can never confirm again, is unusable, and a
  new parent or another row is the way out. Without this duty the v3 form does
  not give the third property of the table at all; on v4 the stop coin
  gives it.

The choice began with a requirement: must a verifier that starts later,
and saw nothing of the cause, refuse a row after it?

| Option | What it gives | Cost |
| --- | --- | --- |
| (a) No. One certifier for each row and one succession of seals | The first three properties of the table above. Nothing on chain at issuance; the successor seal of a plain withdrawal is created in the withdrawing transaction | D5 in the narrower form, and D9 becomes "the notary named for that row". After a plain withdrawal only the same notary can certify again, and an absent notary blocks its rows. The notary's tool keeps the record of each succession |
| (b) Yes. (a) with the stop coin of J2.7 | D5 as the owners wrote it: every verifier that reads its node refuses the row after a cause, whatever attestation or seal is shown | One confirmed coin of the notary for each row before the parent is signed, paid under D11. The notary takes part in issuance and keeps one more key for the life of the parent. A spend by mistake is final |
| (c) Yes, and any named notary may certify any row: each row pins an output that any named notary can spend | D9 as written, certification by another notary after a plain withdrawal, and D5 for every verifier | One coin for each row, a spending condition for one of several keys that has no profile, a second member in every notary's name where LIP-0010 section 9 allows exactly one, a key that can never be retired, and a final word for every named notary over every row |

Ivan Oparin decided on 2026-11-14: option (a) for profile `/2` on v3,
recorded as a narrowed D5 and with the known limits S2-K1 to S2-K3 in the
vector set; and option (b), a stop coin for each row, for v4 from its
first version. On v3 the principal has a stop for one child: its signer
spends the child's seal. On v4 the delegator owns the child's seal, and
without the stop coin the principal could stop one child only by closing
the whole parent. Option (c) is not taken. D1 is unchanged.

A coarser form of the stop coin is recorded as a future option and is no
part of the first v4 version: one coin for each notary and parent, whose
spend ends every row of that notary under the parent at once. It could
serve as an emergency brake when a notary is compromised. Its cost and its
limits are not worked out (Alternatives and Other open questions).

Two further designs were set aside. A state for each child that a verifier
finds on its own node, such as a marker it can index, would give the
stronger form without an output in principle, as a complete, authenticated
index of cause frames. A frame can be found from a child id, but
authenticating it needs the withdrawn attestation, which the presenter
withholds; treating an unauthenticated match as a hold lets anyone who
knows a child id stop that child; and it misses a child signed again under
the same ordinal. It is not designed, and it would need rules for
completeness, availability, reorganisations and competing attestations of
one child. A child that names its own notary gives a choice at
issuance; on v4 the delegator then signs the child again and names the
other notary.

Cases (J2). S2-K1 to S2-K3 are known limits, and the vector set records
their verdicts as limits:

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S2-1 | A child of row 1, notary `N1`, with `N1`'s attestation and an unspent seal | The same child with a valid, anchored attestation by `N2`, which the parent names for row 2: `NOTARY_NOT_DESIGNATED`. `N2` stays listed, and every other check passes. In force the child is admitted. |
| S2-2 | After a plain withdrawal by `N1`, a new attestation by `N1` is admitted by a verifier that starts later and by a witness | After a cause by `N1`, an attestation by `N2` shown to a verifier that starts later while the child's seal is unspent: refused. The case tests designation only; it is never reported as closing the fourth property of the table and always runs beside S2-K1. |
| S2-3 | A new child under another row, certified by that row's notary | v4: a child signed again with the terms and the ordinal of the withdrawn one and certified by `N2`: `NOTARY_NOT_DESIGNATED`. The child signed again passes every step before V12. In force it is admitted. |
| S2-4a | A witness of a plain withdrawal admits `N1`'s new attestation of the same child | A witness of an authenticated cause refuses `N1`'s new attestation of the same child, as section 10 requires in force. |
| S2-4b | The same | The same witness refuses a child signed again under the same ordinal with another id: `ROW_CLOSED_FOR_CAUSE`, after restart, eviction and reorganisation. A journal keyed by child id admits that child in force. |
| S2-5 | An authentic attestation of the row's notary and its seal spent with `SIGHASH_ALL` and the one frame: the row closes at that verifier | No row closure and no misconduct verdict for: the frame bytes in an unrelated transaction; a frame for another child; a commitment that does not recompute; a fabricated attestation that names the victim row and an attacker's seal, with that seal genuinely spent; an authentic attestation of another parent, ordinal or contract hash; a frame output appended to a plain withdrawal whose seal signature is `SIGHASH_SINGLE`, where the attestation is withdrawn and `N1`'s next attestation is admitted. After each negative a valid neighbour is still admitted. The text in force closes on an observed frame with no rule of authentication. |
| S2-5r | A cause authenticated before the notary rotated `attest`. A verifier that holds only the newer attestation of the child, where the frame points at the older one that names the same seal: the row closes as well | The closure stays after the rotation; a reader of evidence authenticates the old attestation by the key that the name yielded in the block of its anchor. The same frame does not close another row whose attestation named that seal. |
| S2-6 | Another row of the live parent, with its own unspent seal and a valid attestation, stays admissible after row 1 closed for cause | Closing the parent or another row is wrong. With a shared seal: the other row's attestation named the spent seal, so it refuses as `NOTARY_WITHDRAWN`; a fresh attestation that names the successor created in that spending transaction is admitted, and that row is not closed for cause. |
| S2-7 | A seal spent without a readable frame: the old attestation refuses as `NOTARY_WITHDRAWN`, and a new attestation by the row's notary that names the successor seal is admitted, by a verifier that starts later and by the witness | Admitting the withdrawn attestation because no frame was found is wrong. Closing the row or the child for cause without an authenticated frame is wrong as well; an implementation that closes on every spend breaks the control. |
| S2-8 | v3: the signer, shown an authenticated cause, spends the child's seal, and the spend is observed on chain; a request for another unused ordinal succeeds | A request for the same ordinal after the cause is refused by the signer, from its durable reservation. Both duties exist in force. |
| S2-9 | At the notary's tool: a second attestation for the same child while the row's seal is unspent names that same seal; the spend for cause then refuses both at a verifier that starts later as `NOTARY_WITHDRAWN`. After a confirmed plain withdrawal whose transaction created the successor, a new attestation of the same child that names the successor is admitted | The tool refuses to name for a row any output outside the row's succession, whatever its node shows of the earlier seal: spent in the mempool, spent in a block, or absent. |
| S2-9b | At the notary's tool, on regtest: a plain withdrawal `W` of `A1` creates the successor; the tool signs `A2` naming it; `W` confirms; the cause spends the successor and confirms; a verifier that starts later refuses `A1` and `A2` | `W` is broadcast and evicted before it confirms. At a verifier that starts later `A2` refuses at V18, because its seal does not exist, and `A1` is admitted again: that is the limit of a spend that left the view, not a breach, and a plain withdrawal that vanished closed nothing. The tool then withdraws for cause by spending the first seal, the one unspent on its node; once that confirms, `A1` and `A2` both refuse. Beside it, the forbidden shape, built by hand: a second seal unrelated to `W`, named after the pending `W`; `W` evicted; the cause spends the second seal and confirms; `A1` is admitted after the confirmed cause. The tool must refuse to build this; a verifier cannot refuse it on v3. |
| S2-9c | At a reader of evidence: `A1` names the first seal and `A2` its successor; the reader, given both creating transactions, reports no breach | The withdrawal that created the successor is removed by a reorganisation, and the first seal is unspent again while `A2` exists: still no breach, at any block. Two attestations whose seals have unrelated creating transactions that both stand in one chain: a breach of J2.3 (a), also when one of the seals has been spent since. A reader that decides from the seals unspent at a block fails both; so does one that reports a breach without the transactions. |
| S2-K1 | Known limit of the v3 form. `N1` certifies again after a plain withdrawal: admitted | `N1` signs `A2` with a fresh seal after its own cause; a verifier that starts later and receives `P`, `C` and `A2` admits. On v4, once the stop coin of the row is spent, it refuses as `ROW_CLOSED_FOR_CAUSE` (S2-10). |
| S2-K2 | Known limit of the v3 form. The same control | `A2`, signed before the cause and naming a seal outside the row's succession, in breach of J2.3 (a), and left unspent: a verifier that starts later admits. On v4 it refuses once the stop coin of the row is spent. |
| S2-K3 | Known limit of both forms. A cause that is confirmed in the verifier's chain: every attestation that names a seal of the succession refuses | The cause is evicted before it confirms, or removed by a reorganisation and not confirmed again; the seal it spent is unspent in the verifier's view. A verifier without a journal admits the attestation that names it; a witness of the cause refuses. On v4 it is the spend of the stop coin that left the view. |
| S2-10 | v4: a row whose stop coin exists with the named script and is unspent; a child of the row with a valid attestation is admitted, and another row of the same parent with its own unspent stop coin stays admissible after this row is ended | The stop coin of the row spent, in the mempool or in a block: every child of the row refuses as `ROW_CLOSED_FOR_CAUSE`, whatever attestation and seal are shown, also at a verifier that starts after the spend. A stop coin that does not exist with the named script refuses as well. |

## 11. Staging and the mapping to v3 and v4

Re-delegation is no part of the first proof of LIP-0013 (D4). Until that proof
passes, grants are one-hop grants signed by the owner's signer. Every executor
runs in shadow mode, so the relaying problem of the motivation cannot yet
cause an effect.

After the first proof the pieces of this LIP run in shadow mode first:
executors report the result of section 8 for every envelope that arrives under
a child, and no child confers authority. Enforcing mode for children is a
separate switch. It needs an approval by each owner for that owner's
executors, recorded like the approvals of LIP-0013 section 3.4. Enforcing mode
for one-hop grants does not include it.

| Piece | On v3 | On v4 |
| --- | --- | --- |
| Signer of the child | The landlord's grant key, on a kind-8186 request of the delegator | The delegator |
| Right of re-delegation and parent binding | Contract members of profile `/2`, bound by `contract_sha256` | Signed scope and the issue capability of LIP-0008 section 12.2 |
| Attestation, anchor and notary seal | This LIP | The same object |
| Revocation of a parent | One transaction spends the parent's and every child's seal | A closed ancestor refuses its descendants |
| Agents that sign grants | None | The delegator signs the child with the parent's recipient key (LIP-0008 section 12.6). For a parent issued by name that is the key the name lists at admission, so a child signed with an earlier key refuses (LIP-0008 sections 3.1 and 12.2). Section 11.1 holds Draft text, under a decision that awaits the co-author's agreement (J4), that replaces this rule with a delegation key named in the parent |

Depth stays at two links (D7). Work below a child's executor is covered by a
new root grant from the principal.

Each party pays for its own effects under D11. A payment for a notary's seal,
anchor or fee from an owner's funds follows that owner's spending rule; where
the owner approves each spend, the payment is approved per spend.

### 11.1. The delegation key on v4

Decided by Ivan Oparin on 2026-11-14 (J4); the co-author's agreement is
pending. The decision replaces the rule in force for the link below an
issue capability. Under that rule an agent that its parent names by name
signs child grants with the key that also signs its messages. The decision
states the opposite as a hard rule: the messaging key never grants
authority. v3 does not change, and until the co-author agrees the rule in
force stands. For the octets of `swarma-grant/4` the rule in force since
version 0.1.53 is LIP-0020 W11.8.

By the rule in force the parent's recipient signs the child (LIP-0008
section 12.6): the grantee key, or for a parent issued by name the key that
the name yields at admission. An agent's name yields one key, its Nostr key
(LIP-0010). As the agent's request key it is held, under LIP-0013 section
3.6, by the key holder that the agent's owner names: Keymaker in the
deployment of the owner who took that decision. In the implemented rental
profile the gateway holds the key (key map).
One key then signs both messages and grants, which the key map keeps apart
for a principal, and when another operator runs the host, a key that signs
grants is in that operator's hands. A change of the key is a name update by
the agent's operator (K2 of the key map), for example when the agent moves
to another host under the registration flow that the key map proposes. The
parent survives the change, because its request key is read from the name's
current value at every admission (LIP-0008 section 3.1). A child signed
with the earlier key refuses at use for as long as the name lists another
key, because its issuer does not equal the parent's recipient (LIP-0008
section 12.2); nothing records a closure, and a child signed with the new
key passes that comparison. Every change of the agent's Nostr key therefore
stops the children it signed. On v3 the landlord signs the child, and the
delegator's request of section 5 is signed with `P.grantee_key`, which for
an agent is that same Nostr key.

Under this subsection the v4 issue capability carries one more member, the
delegation key (`delegate.key`), an x-only key. The principal signs it with
the parent, and the grantee's consent covers it. No name is read for it.
Each parent has a delegation key of its own, which signs the children of
that parent and of no other. Its bytes are fixed with the v4 bytes: the
member `delegate.key` of LIP-0020 section 11 (W11.5), where a child that
another key signed refuses as `CHILD_SIGNER` in the reader's pipeline
(W11.8).

| # | Rule | Refusal |
| --- | --- | --- |
| J4.1 | An issue capability MUST name one delegation key. A v4 child MUST be signed by the delegation key of the capability it commits to. | A child signed by any other key, the parent's request key and a key that the grantee's name lists for a channel included: `CHILD_SIGNER` |
| J4.2 | For LIP-0008 section 12.2 the authenticated issuer of the link after an issue capability is that capability's delegation key. The delegation key signs child grants and nothing else: no invocation, no envelope, no consent, no name operation, no transaction. The request key of the same grant MUST NOT sign a child grant; under LIP-0013 section 3.6 what it may sign is the closed list of J7.5. | A child signed by the request key: `CHILD_SIGNER` (J4.1) |
| J4.3 | Keys are compared as secret authorities, by their 32-byte x coordinate: an x-only key equals a compressed key with that coordinate under either parity byte. | none of its own |
| J4.3 (a) | Parent checks, on the bytes and pins of `P`, when `P` is validated. The delegation key MUST differ from the issuer's grant key; from `P`'s request key, when `P` names its recipient by key, or from the owner key of the recipient's name, when `P` names its recipient by name; from the owner key bound for the issuer's name; from the owner key pinned for each notary (section 7.1); and from the key of `P`'s own seal, taken from its endorsement (LIP-0008 section 11.1). | `P` is unusable as a parent, and every child refuses as `DELEGATE_KEY_REUSE` |
| J4.3 (b) | Child checks, at every admission of a child `C`. The delegation key MUST differ from every channel key that the name of `P`'s recipient yields at that admission, when `P` names its recipient by name; from the attestation key that the notary of `C`'s attestation, under section 10.1 the notary of `C`'s row, yields at that admission; from the key of `C`'s seal; and from `C`'s own recipient key, or from the owner key of `C`'s recipient name. Another notary of the parent is not read (J3.7). | That admission refuses as `DELEGATE_KEY_REUSE` and records no closure |
| J4.3 (c) | Where an owner pin is not one key, and for keys that no verifier sees, such as funding and fee keys, the separation is a custody duty of J4.4. It is not checked on the wire. | none at a verifier |
| J4.4 | The delegation key is held by a signing service of the party that consented to the parent as its recipient: for a recipient by name, the operator who holds that name's owner key; for a recipient by key, the operator of that key's key holder. In both modes the service runs outside the delegating agent's OS user and outside the service that holds the request or channel key, and it holds no name-owner key, seal key or funding key. Before it signs, the service MUST take the complete child and, on its own node, check that `P` is live under every admission rule, its closure journals included, which under LIP-0008 section 5.2 and section 10.1 hold the closures of an issuer's name and of a row; that the child's row exists and that the child fits it (section 9.1), and that under section 10.1 the row is not closed for cause; and the comparisons of section 4. It computes the digest itself (LIP-0008 section 8) and MUST NOT sign a digest that a caller supplies. It MUST identify the caller and sign only for a caller that its operator listed for delegation under `P`; under LIP-0013 section 3.6 the caller is a run, and the list is the `delegate` list of that run's origin. Possession of the messaging key is not the authority to ask. | No signature exists |
| J4.4 (a) | The reservation key. The signing service of J4.4 keeps a reservation ledger. A record of the ledger is keyed by the pair of the parent's identifier (LIP-0020 W6.1) and the place. The place is the ordinal of a row of that parent in the count of LIP-0026 R8.3 and R8.8 (J12), which LIP-0020 section 11 carries as the signed order of `groups` and `ranges` (W11.6) and as the member `ordinal` of a child (W11.2). For one place of one parent the service MUST make one signature, ever. A place number names nothing without its parent: the same ordinal under another parent, and another ordinal under the same parent, are other keys with records of their own. One ledger holds the records of every delegation key that the service holds; a delegation key stands in one ledger, and that ledger has one writer (J4.4 (f)). The service identifies the caller and makes the checks of J4.4 before it reads the ledger for a request, in the order of one request that follows the table of states. A request that those checks refuse reserves nothing, reads nothing and learns nothing of the ledger. A verifier cannot observe this duty; it proves nothing to a consumer. | none at a verifier |
| J4.4 (b) | The intent. The intent of a request is the SHA-256 of the exact signing preimage of the complete child. That preimage is the octets of LIP-0020 W4.1: the SHA-256 of the tag `swarma-grant/4`, the same 32 octets once more, and the canonical bytes of the child's payload. The intent is therefore the typed digest that the signature covers (LIP-0020 W5.1), and the service computes it itself from the complete child, as J4.4 requires of the digest. It is neither the identifier of the child (LIP-0020 W6.1) nor a hash of a signed form (W6.4). One payload has one intent, and another payload has another, for as long as SHA-256 keeps two payloads apart. The intent binds the payload alone and nothing of the caller or of the request: two requests with one payload, from two listed callers, are one intent and take one result. A verifier cannot observe this duty; it proves nothing to a consumer. | none at a verifier |
| J4.4 (c) | The record and its states. A place has one of four states: no record; `reserved`; `signed`; and `held`, the state of an outcome that the service does not know. The ledger as a whole is usable or lost (J4.4 (f)). The table of states that follows these rules gives, for every state and every event, the next state, the use of the key, the answer and the code. The service MUST follow it, and where a rule of J4.4 (a) to J4.4 (g) and that table differ, the table governs. Before any use of the delegation key for a child the service MUST make durable a record under the reservation key. The record holds the intent, the identity of the request for the audit, which is the origin of the calling run and the identifier of the request, and the state `reserved`. The reservation is one atomic test and set at the one writer of the ledger: of two requests that arrive together for one reservation key exactly one creates the record, and the other is answered from it. The test reads the records and the open marks at the writer, and the request that loses it writes no mark. The request that created a record holds its claim, which is the right to take the record from `reserved` to `signed`. A claim lives in one run of the service: it ends when its request ends or the service stops, and it is never passed on and never renewed. Between the reservation and the use of the key the service repeats the checks of J4.4 on the parent and on the row, and a request that they now refuse ends with the key unused. It then makes the entry of the use of the key durable (J4.4 (g)), and under one record it calls the signer once. It verifies the signature under the delegation key over the recorded intent, takes the identifier of the child from the payload of that intent, and makes the result durable: the state `signed`, with the exact 64 octets of the signature and the identifier of the child. A place is `signed` only when every write of the result is durable: its mark, its entry and the kept head over that entry (J4.4 (f)). Only then does the service release the signature. A signing call that returns no signature or whose outcome the service does not know, and a signature that fails that verification, are unknown outcomes and the place is `held` (J4.4 (f)): the service MUST NOT release such octets and MUST NOT sign again for the place, in that request or in any later one, because a second signature would be a second use of the key for the place. `reserved` passes to `signed` or to `held`. `signed` is final. `held` ends only as J4.4 (f) says. No entry of the ledger is deleted. A place for which the key was used never takes another signature, also after the parent is closed or the child is revoked. A verifier cannot observe this duty; it proves nothing to a consumer. | No signature exists before the reservation is durable, and none is released before the result is |
| J4.4 (d) | Replay. A request whose parent, place and intent equal those of a record or of an open mark, whose intent is read in the same way, is a replay, whichever listed caller asks. A replay is answered only after the service has identified the caller and made the checks of J4.4, all of them and not the caller check alone, as for a first request. A replay that they refuse is answered with the refusal of J4.4 and nothing else: under a parent that the service holds closed or whose window has ended, and for a caller that is no longer on the list, it discloses no stored octets, no state and not that a record exists. A replay that passes them is answered from the record or the open mark: in the state `signed` with the stored octets of the signature, read from a result that the kept head covers, and in the states `reserved` and `held` as J4.4 (f) says. The service MUST NOT sign again. BIP-340 takes auxiliary randomness, so a second signature over the same digest has other octets (LIP-0020 W5.4), and it would be a second use of the key for the place. The answer writes no reservation, changes no record and appends nothing to the ledger. A verifier cannot observe this duty; it proves nothing to a consumer. | none at a verifier; at the service the stored octets, `PLACE_HELD` or the refusal of J4.4 |
| J4.4 (e) | Conflict. A request that passes the checks of J4.4 and whose intent differs from the intent in the record or in the open mark of its parent and place MUST be refused, in every state of that place: `reserved`, `signed` and `held`, a place under an open reconciliation included. An open mark holds an intent as a record does, and it is read in the same way. No signature exists for the refused payload, and neither the record nor the mark changes. The refusal is closed and is not retryable: while the place has a record or an open mark with another intent no request with the refused intent is signed for it, and once the place is `signed` that is for good. Only a place that a reconciliation returned to "no record" (J4.4 (f)) takes a first request again. Under a lost ledger no record can be read, no conflict can be established, and the answer is `PLACE_HELD` for every intent (J4.4 (f)); so it is for a place that is held with no intent recorded, which is every place of a delegation key whose whole life the ledger does not show. The service answers with no other place, no other key and no other parent. A verifier cannot observe this duty; it proves nothing to a consumer. | `PLACE_CONFLICT`, at the service alone |
| J4.4 (f) | An unknown outcome holds the place. A write that was interrupted, or whose outcome the service does not know, is never taken as "no record", and a stop of the service between the reservation and the durable result, the moment between the signature and the record of the result included, is never taken as "no signature". So that a failed or torn write still leaves a trace, every write to the ledger is one entry and is made in one order: a mark, which names the reservation key, the intent and the kind of the entry, is made durable outside the ledger, beside the kept head; then the entry is appended; then the kept head moves over the entry, which closes the mark. Each partial outcome of a write has one state. A mark that is shown not to have landed leaves nothing. A write that ends after its mark and before the kept head covers its entry leaves an open mark: the place is held, and an entry that stands whole beyond the kept head is evidence only, which the service never completes by itself. A mark or a kept head that cannot be read, and a mark whose writing has an outcome that the service does not know, lose the ledger. A place is held in four forms: under an open mark; under a record `held`; under a record `reserved` that has no live claim, which is every record `reserved` after a stop of the service; and as a place of a delegation key whose whole life, from its making, the ledger does not show. Wherever a hold is derived from a record, an open mark stands beside the record and holds as it does. For a held place the service MUST NOT sign; MUST NOT release a signature, one that was made before the stop included; MUST NOT repeat the signing by itself; and MUST NOT answer with a new delegation key or with another place. The service appends nothing beyond an open mark: before any other write it records the hold of that place as an entry of the chain, with what stands beyond the kept head as the evidence of the hold, and moves the kept head over that entry; only then does it write for another place. A held place has two exits and no other, and each is a reconciliation by the operator of the service. A reconciliation never uses the delegation key and accepts no octets from outside the service. It may confirm a signature that the service itself wrote into the ledger at its making, and the place is then `signed`. It may prove, from the proof-bearing entries of the ledger (J4.4 (g)), that the key was never used for the place, and the place then returns to "no record". That proof covers the whole life of the key, from its making and not from its entry into this ledger: absence of an entry is evidence only inside a chain that is continuous from the making of the key. A key that was not made under the ledger, and a key that the service held when a new ledger was started, has every place of every parent held, and no reconciliation frees a place of such a key. Where neither is proved the place stays held for ever: the row is lost to this parent, and the next child takes another row or another parent. A reconciliation opens only on a held place, and from its opening no claim exists or arises for the place, so the request that created the record cannot complete while a reconciliation is open, and a reconciliation cannot open while that request can complete. The ledger as a whole follows the contract that stands below the table of states: one fenced writer, one chain that holds the records and the proof-bearing audit together under one head, which the service keeps outside the ledger, and a start by an act of the operator alone. A ledger that is absent, that was put back to an earlier state, that forked or that does not continue the kept head is lost. Under a lost ledger every place of every parent whose delegation key the service holds is held, a parent that the service first sees after the loss included, until the complete ledger is restored or the genesis of that contract is made. A restore of the whole host that puts back the ledger and the kept head together is such a loss, and the service cannot find it by itself. That the kept head stands where no restore of the host reaches it is a duty of the operator, and so, beside J4.6, is the single custody of the delegation key: one key under one service and one ledger, with no copy elsewhere. A verifier cannot observe this duty; it proves nothing to a consumer. | `PLACE_HELD` for a request with the recorded intent, for every request for a place that is held with no intent recorded, and for every request under a lost ledger; `PLACE_CONFLICT` for a request with another intent than a record or an open mark that can be read (J4.4 (e)) |
| J4.4 (g) | Audit and capacity. The service keeps two audits, both outside the write authority of the delegating agent, and one of them alone is proof. The proof-bearing audit stands in the chain of the ledger, under the kept head, and has the whole contract of the ledger (J4.4 (f)): an entry of the chain carries a record and its audit entry together, as one entry. The chain holds these entries and no other: the entry of a delegation key; a reservation; a use of the key, in an entry that is durable before the signer is called; a result, which is `signed` or `held`, a failed verification, a signing call of unknown outcome and the hold of a write that did not complete included (J4.4 (c), J4.4 (f)); a reconciliation, with its opening, its evidence and its outcome; and a genesis, which names the loss that it ends. An entry holds the reservation key, the intent, the identity of the request and the outcome. Only these entries are read as proof: of a key that was never used for a place, of a signature that the service made, and of the start of a ledger. The operational audit stands apart from the chain. It holds every refusal by the checks of J4.4, with what the request stated and what the service established of the caller, and every finding that the ledger is lost; the service writes its other answers there as well, which are `PLACE_CONFLICT`, `PLACE_HELD`, a refusal for want of room and a replay that is answered from the stored octets. It is bounded, it proves nothing and is never read as proof, and absence of an entry in it is never evidence. A write to it that fails changes no state of a place and holds back no answer. Two reasons keep it apart: a lost ledger takes no entry except a genesis, so the finding of a loss cannot be written into the ledger; and refusals written into the chain would let a caller that is not on the list grow the ledger. A signature is released for the first time only after the entry of its result is durable under the kept head, and a replay is answered only from such an entry. Before it writes a mark for a reservation, the service secures the room that the three writes of a request need, which are the reservation, the use of the key and the result, each with its mark, and the room of an entry that records a hold, so that none of those writes fails for want of room. A service that cannot secure it refuses before any mark, before any record and before any use of the key, and that refusal holds no place. A write that fails after its mark is durable is no such refusal: it holds the place (J4.4 (f)). A verifier cannot observe this duty; it proves nothing to a consumer. | No mark, no record and no signature exist |
| J4.5 | What a name update does to children. A rotation of the delegating agent's channel key under the same owner, a renewal and a change of host stop no child. An update that makes a channel key equal to the delegation key refuses children for as long as it holds (J4.3 (b)). A change of the name's owner refuses a parent by name and with it every child (LIP-0008 section 3). A parent by key is not portable through any name. | `DELEGATE_KEY_REUSE` while a channel key equals the delegation key; `PARENT_NOT_LIVE` for every child after a change of the name's owner |
| J4.6 | Replacing the delegation key requires a new parent. A move of custody that cannot keep exclusive control of the key MUST NOT begin before the old parent is closed. | none at a verifier |
| J4.7 | v3 is unchanged: the landlord's grant key signs the child on a kind-8186 request signed by `P.grantee_key` (section 5). A delegation key gives nothing on v3. | none new |

A verifier repeats the checks of J4.4 on the parent and on the child at use.
The checks of the signing service spare a wasted child and bound a thief of
the caller's channel. The ledger of J4.4 (a) to J4.4 (g) is no such check: a
verifier cannot repeat it.

**The reservation ledger (J4.4 (a) to J4.4 (g)).** Ivan Oparin decided on
2026-11-16, as the lead relayed it, that the issuer's reservation ledger
belongs to the v4 specification as a duty of the signing service. The rows
state it as duties that can be observed at the service and as names of
states. They fix no storage schema, no record octets and no interface. The
duty binds wherever a delegation key of J4 signs and has the standing of J4:
the co-author's agreement has not been given, and the co-author's answer is
folded in by amendment.

The core of the duty is one sentence: for one place of one parent the
service makes one signature, ever, and the durable record comes before the
signature. A child states its parent and its ordinal in its payload
(LIP-0020 W11.2), so every payload belongs to exactly one reservation key,
and the first intent under which the delegation key is used for a place is
the only one that the service ever signs for it. Without the ledger nothing at the service stops
a caller, or an error of the caller, from obtaining two different children
for one row; section 9.1 states that case for a child signer that uses one
ordinal twice.

The reservation is on v4 what the first of the three facts of J1.7 is on
v3, the reservation of the ordinal at the signer: beside the record of the
notary and the consumption in the row ledger, a place at the signing service
for which the key was used is used for good. A revoked child, a withdrawn
attestation, a closed parent and a reissue free none of them. A delegator
that wants another child takes another row, and where no row is left,
another parent. The one place that becomes free again is a held place for
which a reconciliation proved that the key was never used (event 30 of the
table).

**The table of states.** The rules J4.4 (b) to J4.4 (g), the cases and the
vector plan are read from this table. A place has one of four states, and
the state is read from the last entry of the place that the kept head
covers and from the marks. "No record" is a place of a key that the ledger
shows from its making, with no entry and no open mark, and also a place
that a reconciliation returned to that state. `reserved` is a record
`reserved`, with or without the entry of the use of the key after it, whose
creating request holds a live claim (J4.4 (c)). `signed` is a result
`signed` of which every write is durable, its mark, its entry and the kept
head over that entry, and after which the place has no later entry. Where
`signed` is reached after event 31, by a reconciliation that confirmed a
signature of a held place, the entry that the reconciliation writes for
that outcome is a result `signed`, an entry of the kind of a result and of
no other kind: it holds the octets and the identifier that the
reconciliation confirmed, it records that it came by a reconciliation and
which hold it closes, it is written as every entry is, by its mark, the
entry and the kept head over it, and it is the last entry of its place. The
place is `signed` by that result as by the result of event 20, and the
definition before this sentence, the release rule of the contract of the ledger,
step 3 of the order of one request and event 5 read for it as they stand:
a replay is answered with the stored octets, read from that result
(sentence added with version 0.1.55). `held` is a place under an open
mark, under a record `held`, under a record `reserved` with no live
claim, or a place of a delegation key whose whole life the ledger does
not show. The kinds of entry are those of J4.4 (g), carried here
unchanged: the entry of a delegation key; a reservation; a use of the
key, in an entry that is durable before the signer is called; a result,
which is `signed` or `held`, a failed verification, a signing call of
unknown outcome and the hold of a write that did not complete included
(J4.4 (c), J4.4 (f)); a reconciliation, with its opening, its evidence
and its outcome; and a genesis, which names the loss that it ends (list
carried with version 0.1.56). A mark is pending while the one writer makes
its write in the live run. It is open once that write has ended without the
kept head over its entry, and every mark that a start of the service finds
is open. The first four columns suppose a usable ledger; the fifth is a
lost ledger, under which no state of a place can be read. Each cell states
three things in one order: the next state of the place; what the service
does with the delegation key; and the answer to the caller with its code.
"Unchanged" says that the state stays, and "key idle" that the event makes
no use of the delegation key. A pair that cannot occur says why.

A request makes three writes, of the reservation, of the use of the key and
of the result, and each write has three components in one order: the mark,
the entry, the kept head. Events 8 to 11, 13 to 15 and 20 to 23 take each
write apart by the last component that is durable, so that no event gives
one next state to outcomes that differ. An entry is written when its octets
stand whole in the chain, and it counts, for the state of a place, for the
use of the key and for a release, only when the kept head covers it. Where
the service does not know how the write of an entry or of the kept head
ended, it reads the mark and the kept head, and the event is the one that
they show; where it cannot read them, the event is 24. Before its entry a
delegation key has no place in the ledger, so the entry of a key (events 37
and 38) is read in the column of the state in which it leaves the places of
that key.

| # | Event | No record | `reserved` | `signed` | `held` | Ledger lost |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A request that the checks of J4.4 refuse: a caller that is not identified or not listed, a parent that is closed or whose window has ended, a child that does not fit | Unchanged. Key idle. The refusal of J4.4: no code of this section, no stored octets, no state, and not whether a record exists. The refusal goes to the operational audit, and a failure of that write changes nothing | As in the first column | As in the first column, also for a replay (J4.4 (d)) | As in the first column | As in the first column: the request does not learn that the ledger is lost |
| 2 | A first request that passes the checks and for which the service cannot secure the room of J4.4 (g) | Unchanged. Key idle. Refused with no code; no mark and no record exist, and the same request may be asked again | Impossible, because room is sought only for a place with no record and no open mark: the request is a replay (event 5) or has another intent (event 6), and neither needs room | Impossible, for the same reason | Impossible, for the same reason; a place that is held with no intent is event 7 | Impossible, because under a lost ledger the request is answered at the continuity check, before room is sought (event 4) |
| 3 | A first request that passes the checks while the mark of another place is open and the service cannot complete the resolution of that mark (event 28) | Unchanged. Key idle. Refused with no code: nothing is appended beyond an open mark, no mark and no record exist for this place, and the same request may be asked again | Impossible, as in event 2: a replay and a request with another intent append nothing, and are answered as in events 5 and 6 while that mark is open | Impossible, as in event 2 | Impossible, as in event 2 | Impossible, as in event 2 |
| 4 | A first request: it passes the checks, no open mark stands, room is secured, and the place has no record and no open mark | The service begins the write of the reservation, and the next state is that of events 8 to 11. Key idle. No answer yet | Impossible, because a record exists: the request is a replay (event 5) or has another intent (event 6) | Impossible, for the same reason | Impossible, because a record or an open mark holds an intent (events 5 and 6), or the place is held with no intent (event 7) | Unchanged. Key idle. `PLACE_HELD`, for every intent and for every parent, a parent that the service first sees after the loss included |
| 5 | A replay: a request that passes the checks and whose parent, place and intent equal those of the record or of the open mark | Impossible, because neither a record nor an open mark holds an intent to equal: the request is a first request (event 4) | Unchanged; the creating request goes on. Key idle for this request. `PLACE_HELD` | Unchanged. Key idle: the service never signs again. The stored 64 octets, read from the result that the kept head covers; no code. The answer appends nothing; it goes to the operational audit and does not wait for that write | Unchanged. Key idle. `PLACE_HELD` | Unchanged. Key idle. `PLACE_HELD`, because no record can be read |
| 6 | A request that passes the checks and whose intent differs from that of the record or of the open mark | Impossible, because neither a record nor an open mark holds an intent to differ from: the request is a first request (event 4) | Unchanged. Key idle. `PLACE_CONFLICT` | Unchanged. Key idle. `PLACE_CONFLICT` | Unchanged, also while a reconciliation is open. Key idle. `PLACE_CONFLICT` | Unchanged. Key idle. `PLACE_HELD`, because no conflict can be established |
| 7 | A request that passes the checks, for a place of a delegation key whose whole life the ledger does not show (events 36 and 38), a place that is held with no intent recorded | Impossible, because every place of such a key is held | Impossible, because such a key is never used, so no place of it is reserved | Impossible, for the same reason | Unchanged, and no reconciliation frees the place. Key idle. `PLACE_HELD` for every intent, because no intent is recorded and no conflict can be established | Unchanged. Key idle. `PLACE_HELD` |
| 8 | The write of the reservation succeeds: the mark, the entry `reserved` and the kept head over it are durable, in that order | `reserved`, with the claim at the request that made it. Key idle so far. No answer yet | Impossible, because the one writer reserves by a test and set that reads records and open marks, and only for a place with neither | Impossible, for the same reason | Impossible, for the same reason | Impossible, because a lost ledger takes no entry except its genesis |
| 9 | The write of the mark of a reservation fails, and the service shows that no mark landed | Unchanged. Key idle. Refused with no code, as in event 2; the same request may be asked again | Impossible, as in event 8 | Impossible, as in event 8 | Impossible, as in event 8 | Impossible, as in event 8 |
| 10 | The mark of a reservation is durable, and no whole entry stands beyond the kept head: the write of the entry failed or was torn | `held`, under the open mark. Key idle. `PLACE_HELD`. The resolution follows (event 27). The key was not used, and exit 30 is open | Impossible, as in event 8 | Impossible, as in event 8 | Impossible, as in event 8 | Impossible, as in event 8 |
| 11 | The mark of a reservation is durable and its entry is written whole, and the kept head, which can be read, has not moved over the entry | `held`, under the open mark: the one marked entry beyond the kept head. The service does not complete the write by itself, and the entry is evidence only. Key idle. `PLACE_HELD`. The resolution follows (event 27). The key was not used, and exit 30 is open | Impossible, as in event 8 | Impossible, as in event 8 | Impossible, as in event 8 | Impossible, as in event 8 |
| 12 | Between the reservation and the use of the key the service repeats the checks of J4.4 on the parent and on the row, and they refuse | Impossible, because no request holds a claim where no record is | `held`; the claim ends. Key idle: no mark and no entry of a use exists, and exit 30 is open. The refusal of J4.4, as in event 1, and no code of this section. Where the refusal is the coin of the row spent by the confirmed issuance anchor of this child, the refusal is `ROW_COIN_REQUIRED`, and the service writes an entry of the operational audit and notifies its operator that a signature exists outside this ledger, as in event 39; the place stays held (sentence added with version 0.1.56, as normative text) | Impossible, because the claim ended when the result became durable | Impossible, because a held place has no claim | Impossible, because a lost ledger takes no reservation, so no request holds a claim; a request that was under way when the loss was found is event 34 |
| 13 | The creating request ends with no mark of a use of the key durable: the caller is gone, the service ends the request, the write of that mark fails and the service shows that none landed, or the write cannot begin behind an open mark of another place (event 28) | Impossible, as in event 12 | `held`; the claim ends. Key idle: the signer was not called, no mark and no entry of a use exists, and exit 30 is open. `PLACE_HELD` | Impossible, as in event 12 | Impossible, as in event 12 | Impossible, as in event 12 |
| 14 | The write of the use of the key succeeds: the mark, the entry of the use and the kept head over it are durable, in that order | Impossible, as in event 12 | Unchanged. The key counts as used for the place from this entry on, whether or not the signer is then called. The signer is called next, once. No answer yet | Impossible, as in event 12 | Impossible, as in event 12 | Impossible, as in event 12 |
| 15 | The mark of a use of the key is durable, and the write ends before the kept head covers its entry, whichever component was the last that is durable, the mark or the entry | Impossible, as in event 12 | `held`, under the open mark; the claim ends. Key idle: the signer is not called, because it is called only under an entry of the use that the kept head covers. `PLACE_HELD`. The resolution follows (event 27). Exit 30 is closed, because the chain holds a mark of a use, and no signature was made: a reconciliation ends as event 32 | Impossible, as in event 12 | Impossible, as in event 12 | Impossible, as in event 12 |
| 16 | The signing call returns a signature | Impossible, because the signer is called only under a durable entry of the use of the key, by the holder of the live claim | Unchanged. The key was used, once, and is never used again for the place. No answer yet: the octets are not released | Impossible, because the claim ended and no request may call the signer for the place | Impossible, because for a held place the service does not sign | Impossible, as in event 12 |
| 17 | The signing call returns no signature, or the service does not know its outcome | Impossible, as in event 16 | `held`; the claim ends. The key counts as used and the signer is not called again. `PLACE_HELD`. The service writes the result `held` (event 25). No exit can be proved for this place (event 32) | Impossible, as in event 16 | Impossible, as in event 16 | Impossible, as in event 12 |
| 18 | The service's own verification of the fresh signature passes | Impossible, because only the holder of a live claim verifies a signature | Unchanged. Key idle. No answer yet: the write of the result follows | Impossible, for the same reason | Impossible, for the same reason | Impossible, as in event 12 |
| 19 | The service's own verification of the fresh signature fails | Impossible, as in event 18 | `held`; the claim ends. Key idle: the service does not sign again. The octets are released to nobody. `PLACE_HELD`. The service writes the result `held` (event 25). No exit can be proved for this place (event 32): no signature that verifies was recorded, and the key was used | Impossible, as in event 18 | Impossible, as in event 18 | Impossible, as in event 12 |
| 20 | The write of the result succeeds: the mark, the entry `signed` with the 64 octets and the identifier of the child, and the kept head over that entry are all durable, in that order | Impossible, because only the holder of a live claim writes a result | `signed`; the claim ends. Key idle. The 64 octets of the signature; no code | Impossible, for the same reason | Impossible, for the same reason | Impossible, as in event 12 |
| 21 | The write of the mark of a result fails, and the service shows that no mark landed | Impossible, as in event 20 | `held`; the claim ends. Key idle: the service does not sign again and does not repeat the write by itself. The signature is not released. `PLACE_HELD`. The octets stand nowhere in the chain and the chain holds the use of the key, so no exit can be proved (event 32) | Impossible, as in event 20 | Impossible, as in event 20 | Impossible, as in event 12 |
| 22 | The mark of a result is durable, and no whole entry stands beyond the kept head: the write of the entry failed or was torn | Impossible, as in event 20 | `held`, under the open mark; the claim ends. Key idle. The signature is not released. `PLACE_HELD`. The resolution follows (event 27). No whole octets stand in the chain, so no exit can be proved (event 32) | Impossible, as in event 20 | Impossible, as in event 20 | Impossible, as in event 12 |
| 23 | The mark of a result is durable and its entry is written whole, and the kept head, which can be read, has not moved over the entry | Impossible, as in event 20 | `held`, under the open mark: the one marked entry beyond the kept head; the claim ends. Key idle: the service does not sign again and does not complete the write by itself. The signature is not released, whatever a later kept head covers. `PLACE_HELD`. The resolution follows (event 27) and binds the entry as evidence, on which alone exit 31 rests | Impossible, as in event 20 | Impossible, as in event 20 | Impossible, as in event 12 |
| 24 | In any write of this table the writing of a mark has an outcome that the service does not know, or a mark or the kept head cannot be read | Ledger lost (event 34), because the mark could name any place and the head any history. Key idle. `PLACE_HELD` | Ledger lost. The request under way ends as in event 34. `PLACE_HELD` | Ledger lost. Key idle. `PLACE_HELD` | Ledger lost. Key idle. `PLACE_HELD` | Unchanged. Key idle. `PLACE_HELD` |
| 25 | The service writes the entry `held` of a place whose claim ended without a result `signed` (after events 12, 13, 17, 19 and 21) | Impossible, because such a place has a record | Impossible, because the claim has ended, and the place is held and no longer reserved | Impossible, because `signed` is final | Unchanged: the place is held whether or not the write succeeds. Where it succeeds, the place is under a record `held` that states what the service knows. Where no mark landed, the place stays held by rule. Where the write ends after its mark, the place is under the open mark and the resolution follows (event 27). Key idle. No answer of its own | Impossible, because a lost ledger takes no entry except its genesis |
| 26 | The service stops and starts again | Unchanged where the start finds no mark for the place. Key idle. No answer. A mark of a reservation that the stop left is open, and the place is held as events 10 and 11 say | `held`: no claim outlives a stop. Key idle: at the start the service signs nothing, repeats nothing and releases nothing by itself. A mark of the use or of the result that the stop left is open, and the place is held as events 15, 22 and 23 say. Later requests are answered as in events 5 and 6 | Unchanged. Key idle. A replay is answered as in event 5 | Unchanged. Key idle. A mark that the start finds is open, and the resolution follows (event 27). A reconciliation that was open and reached no outcome is closed by the stop and leaves the place held | Unchanged: the check at the start finds the ledger lost again. Key idle |
| 27 | The resolution of an open mark: before any other write the service appends, under that mark, the entry that records the hold of its place, with what stands beyond the kept head as the evidence, and moves the kept head over it | Impossible, because a place under an open mark is held | Impossible, because the mark of a write under a live claim is pending and not open; once that write ends without the kept head over its entry, the claim has ended and the place is held | Impossible, because no write is made for a place that is `signed` | Unchanged in state: `held`, now under a record `held` in the chain, and the mark is closed. An entry that the evidence holds takes no part in the state of the place, although the kept head now covers it. Key idle. No answer; requests for the place are answered as in events 5 and 6, and the service may now write for other places | Impossible, because a lost ledger takes no entry except its genesis |
| 28 | The resolution does not complete: the entry of the hold is not written whole, or the kept head does not move over it | Impossible, as in event 27 | Impossible, as in event 27 | Impossible, as in event 27 | Unchanged: the mark stays open and the place held. Key idle. The service appends nothing for any place and attempts the resolution again at the next continuity check; what an attempt left beyond the kept head is evidence for the next. A first request for another place is event 3, and a write that waits behind the mark begins when a later attempt succeeds. A mark or a kept head that cannot be read is event 24 | Impossible, as in event 27 |
| 29 | The operator opens a reconciliation for the place | Impossible, because a reconciliation opens only on a held place | Impossible, because the claim is live: the opening is refused. The operator first lets the request end (events 12 to 23) or stops the service (event 26) | Impossible, because `signed` is final | Unchanged, and from the opening no claim exists or arises for the place. At most one reconciliation is open for a place. Key idle. Requests are answered as in events 5 and 6 | Impossible, because no record can be read; a lost ledger ends only by a restore of the complete ledger (event 35) or by the genesis (event 36) |
| 30 | A reconciliation proves that the key was never used for the place, over the whole life of the key | Impossible, as in event 29 | Impossible, as in event 29 | Impossible, as in event 29 | No record; the ledger keeps the earlier entries and the entry of the act. Key idle. No answer to a caller: the next request for the place is a first request (event 4), with whatever intent. The proof exists only for a place of a key that the chain shows from its making (event 37), and only where the chain holds for the place no mark and no entry of a use of the key, and no evidence of either. A record `held` that the service wrote after events 12 and 13, and the entry of a hold after events 10 and 11, state no use and leave the proof standing. For a place of event 7 the proof never exists | Impossible, as in event 29 |
| 31 | A reconciliation confirms a signature that the service itself wrote into the chain at its making: a whole entry of the result that an entry of a hold binds as evidence (events 23 and 27) | Impossible, as in event 29 | Impossible, as in event 29 | Impossible, as in event 29 | `signed`, with those octets and the identifier written with them, by the entry of the outcome and the kept head over it. Key idle: the verification takes the public key alone. No answer to a caller: the next replay is answered as in event 5 | Impossible, as in event 29 |
| 32 | A reconciliation proves neither | Impossible, as in event 29 | Impossible, as in event 29 | Impossible, as in event 29 | Unchanged, and held for ever unless a later reconciliation proves event 30 or 31. Key idle. Requests are answered as in events 5 and 6, or as in event 7 | Impossible, as in event 29 |
| 33 | A write of the operator's act for a place, the opening or the outcome of a reconciliation, does not complete | Impossible, as in event 29 | Impossible, as in event 29 | Impossible, as in event 29 | Unchanged: the place is held, and the opening or the outcome is not taken. Where no mark landed, nothing is left. Where the write ended after its mark, the place is under the open mark and the resolution follows (event 27), which records the hold and never the outcome. Key idle. The operator may act again | Impossible, as in event 29 |
| 34 | The ledger is found lost: it is absent, put back to an earlier state, forked, or not continuing the kept head; more than one mark is open, or the chain stands beyond the kept head by more than the open mark accounts for; event 24; or the operator declares that a restore of the host put back the ledger and the kept head together | Ledger lost. Key idle from that moment. `PLACE_HELD` for every request that passes the checks. The finding goes to the operational audit | Ledger lost. The request under way ends with no release, also where its signature was made, and the signer is not called where it was not. `PLACE_HELD` | Ledger lost. Key idle. No stored octets are released from a ledger that is lost. `PLACE_HELD` | Ledger lost. Key idle. `PLACE_HELD` | Unchanged. Key idle. `PLACE_HELD` |
| 35 | The restore: the complete ledger is put back and continues the kept head exactly | Impossible, because a usable ledger is not restored; another ledger put in its place is event 34 | Impossible, for the same reason | Impossible, for the same reason | Impossible, for the same reason | A usable ledger, the same one and no new one. Every place has the state that its entries and the marks give: a record `reserved` is held, because no claim outlived the loss, and an open mark takes the resolution (event 27). Key idle. No answer to a caller |
| 36 | The genesis: the operator starts a new ledger by an act that is its first entry | Impossible, because a genesis is taken only for a lost ledger or where no ledger ever was; a second ledger beside a usable one is a fork (event 34) | Impossible, for the same reason | Impossible, for the same reason | Impossible, for the same reason | A usable new ledger, whose first entry names the loss that it ends. Every place of every parent whose delegation key the service holds at that moment is `held`, and no reconciliation frees one (event 7), because the new chain does not reach back to the making of those keys. Key idle. No answer to a caller. A genesis whose write does not complete leaves the ledger lost, and the operator makes it again |
| 37 | The entry of a key that the service makes under this ledger: the entry records the making and is durable before the public key leaves the service | Every place of the key has no record and is served from its first request (event 4). Key idle. No answer | Impossible, because a key enters once, and before its entry no place of it has a record | Impossible, for the same reason | Impossible, because a key that the chain shows from its making enters with no place held | Impossible, because a lost ledger takes no entry except its genesis, and under it the service makes no key |
| 38 | The entry of any other key: one that signed before this duty bound its service, one that comes from another custody or another ledger, and one whose entry as in event 37 did not complete after its mark | Impossible, because such a key enters with every place held | Impossible, because such a key is never used | Impossible, for the same reason | Every place of every parent of the key is `held`, with no intent recorded, and no reconciliation frees one. Key idle. `PLACE_HELD` for every request (event 7) | Impossible, as in event 37; under a lost ledger every such parent is held as well (event 4) |
| 39 | A request that passes the checks, and passes the check of the coin of its row only because the confirmed issuance anchor of its own child has spent that coin (step 3 of the order of one request; section 8.5, I9), for a place with no record and no open mark. The request is judged in step 3, before room is sought, so it is none of events 2, 3 and 4 (row added with version 0.1.55, as a proposal of that version) | Unchanged. Key idle. Refused with no code, as in events 2 and 3: the service reserves nothing, seeks no room and writes no mark, and no record and no signature of this ledger exist for the place. The service writes an entry of the operational audit (J4.4 (g)) and notifies its operator that a signature exists outside this ledger; a failure of that write changes nothing. The same request asked again is refused in the same way for as long as the place has no record and the coin is so spent | Impossible, because a record exists: the request is a replay (event 5) or has another intent (event 6), and how it passed the check of the coin changes neither answer | Impossible, for the same reason: a replay takes the stored octets (event 5), and another intent `PLACE_CONFLICT` (event 6) | Impossible, for the same reason: a record or an open mark holds an intent (events 5 and 6), or the place is held with no intent (event 7), and the answer is the one of that event | Impossible, because under a lost ledger the request is answered at the continuity check, before the place is read (event 4): `PLACE_HELD`, and no notice of this event |

Four notes go with the table. The service records `held` where it can
(event 25), but a place is held whether or not that write succeeds: an open
mark and a record `reserved` with no live claim are held by rule. A request
that finds a record `reserved` cannot tell, and need not tell, whether the
creating request is still served or its outcome is unknown: both are
answered with `PLACE_HELD`, and in both the same request asked again reads
the record. In the last column the answer is `PLACE_HELD` also where the
place had a record `signed` before the loss: the stored signature is not
released on the strength of a ledger whose history the service cannot show.
And an event on one place moves no other place: the one thing that a held
place asks of the others is that the service first records its hold in the
chain (event 27), which is a write of the service itself and waits for no
operator.

**The order of one request.** The service takes the steps in this order,
and a later step is not reached where an earlier one refuses.

1. It identifies the caller and makes the checks of J4.4: that the caller
   is listed for delegation under the parent, that the parent is live, that
   the row exists and the child fits it, and the comparisons of section 4,
   on a digest that it computes itself. A refusal here is event 1. Nothing
   of the ledger is read for it or disclosed by it, and a replay is treated
   as a first request is (J4.4 (d)).
2. It makes the continuity check of the ledger. Under a lost ledger the
   answer is `PLACE_HELD` for every intent. Where the check finds an open
   mark, the resolution comes before any other write (events 27 and 28).
3. It reads the place. A record or an open mark with another intent:
   `PLACE_CONFLICT` (event 6). A record or an open mark with this intent:
   the stored octets in the state `signed`, read from the result that the
   kept head covers, and `PLACE_HELD` in the states `reserved` and `held`
   (event 5). A place that is held with no intent recorded: `PLACE_HELD`
   (event 7). A place with no record and no open mark, for a request that
   passed the check of the coin of its row in step 1 only because the
   confirmed issuance anchor of its own child has spent that coin: the
   service refuses with no code, as in events 2 and 3, reserves nothing
   and writes no mark; it writes an entry of the operational audit
   (J4.4 (g)) and notifies its operator that a signature exists outside
   this ledger (event 39). Step 1 hands this step that one fact, which it
   read on the node and on the payload, and nothing else; in every other
   branch of this step the fact changes nothing. (Amended with version
   0.1.55, as a proposal of that version: the branch of event 39 is added.
   Through version 0.1.54 the step ended with the sentence on event 7.)
4. For a place with no record and no open mark it secures the room of
   J4.4 (g); without it the request is refused with no code (event 2), and
   so it is while an open mark of another place is not resolved (event 3).
5. It writes the reservation: the mark, the entry, the kept head (events 8
   to 11).
6. It repeats, on a fresh observation of its own node that it establishes
   for this step, every check of step 1 that reads a node or a journal or
   that is made on what such a read gave: the observation itself, the
   confirmed contract seal, the parent, the keys, the row, the
   recipient, the window and the seal of the child, and the coin and the
   end of the row. In section 8.5 these are the steps I3, part (c) of I4,
   and I5 to I9, in their order. A refusal of any of them
   is event 12, and for this step the words "the checks of J4.4 on the
   parent and on the row" of J4.4 (c) and of event 12 name these checks. A
   coin of the row that the fresh observation shows spent refuses here by
   whatever transaction it was spent: the place is `reserved`, and no
   signature of this ledger exists for it. Where that transaction is the
   confirmed issuance anchor of this child, the service writes an entry of
   the operational audit (J4.4 (g)) and notifies its operator that a
   signature exists outside this ledger, as in event 39; the refusal is
   event 12 and the place is held (sentence added with version 0.1.56, as
   normative text). (Amended with version 0.1.55,
   as a proposal of that version. Through version 0.1.54 the step read:
   "It repeats the checks of J4.4 on the parent and on the row (event
   12)." The confirmed contract seal stands in both lists since version
   0.1.61, as a proposal of that version: part (c) of I4 reads a node
   since that version, so the principle of this step, which does not
   change, already reaches it, and only its enumeration is amended here.)
7. It writes the use of the key, as the mark, the entry and the kept head
   (events 13 to 15), and calls the signer, once (events 16 and 17).
8. It verifies the signature under the delegation key over the recorded
   intent (events 18 and 19).
9. It writes the result, as the mark, the entry and the kept head (events
   20 to 23), and only then releases the signature.

A request that carries another intent for a taken place and that also fails
a check of J4.4 is therefore refused at step 1, as any request that fails
that check is, and learns nothing of the place. The second check of step 6
narrows a window and does not close it: a parent that closes after step 6
still costs its place, because the child that is then signed refuses at
every verifier.

Section 8.5 proposes, with version 0.1.55, the inner order of the checks of
step 1, as its steps I0 to I9, and names the checks that step 6 repeats.
The same version amends two steps of this order in place, each marked at
its place: step 3, which gains the branch of event 39, and step 6, which
names its checks and their observation. No other step of this order
changes, and no rule of J4.4 (a) to J4.4 (g) changes its words; rule
J4.4 (c) keeps its words, and for step 6 its words "the checks of J4.4 on
the parent and on the row" name the checks that step 6 lists, as the
Amends list of section 8.4 states beside step 6. Event 12 keeps those
words; event 12 and step 6 each gain one sentence, marked there and
introduced with version 0.1.56 as normative text, on the coin spent by
the confirmed issuance anchor of this child. Until the version lands,
steps 1, 3 and 6 and event 12 read as version 0.1.54 has them (sentence
added with version 0.1.55, as a pointer; amended with version 0.1.56).

**The contract of the ledger.** The contract is that of the ledger store of
J1.4 (section 9.1), taken for this ledger; like that one it states duties
and no schema.

- **One writer.** Every use of a delegation key passes through the ledger
  that holds that key, and the ledger has one writer. Writes are fenced as
  in J1.4: the ledger takes an entry only from the writer that holds its
  current write token, a number that only increases. Two instances of the
  service, or a replica, never keep a ledger each for one key: a replica
  holds no ledger of its own that it may write, joins by receiving the one
  ledger and never starts empty, and an instance that was cut off and
  returns with an older token writes nothing and therefore releases
  nothing. A run of the service begins with a new token, which is why no
  claim outlives a stop. The writer makes one write at a time: it begins no
  write while another is pending or while a mark is open, so at most one
  mark is ever open. The ledger sees one custody of a key and no more. That
  a delegation key exists under one service and one ledger, with no copy
  under another service, in another ledger or outside any, is a duty of
  the operator beside J4.6: two services that each keep a conforming
  ledger for one key sign twice, and neither ledger shows it.
- **The chain and the kept head.** The ledger is one chain: it has an
  identity, given once by the operator at its genesis, a position that only
  moves forward, and entries of which each binds the exact history before
  it. The chain holds the records and the proof-bearing audit together: an
  entry carries a record and its audit entry as one entry, and no second
  store of proof stands beside the chain. Its entries are of six kinds and
  no other: the entry of a key, a reservation, a use of the key, a result,
  a reconciliation and a genesis. The service keeps the head of the chain,
  which is the identity, the position and a commitment to the exact
  history, outside the ledger, where a restore of the ledger does not reach
  it. An entry counts only when the kept head covers it. The key is used
  only under an entry of the use of the key that the kept head covers, and
  a signature is released only under a result `signed` that the kept head
  covers and that is the last entry of its place. A restore of the whole
  host that puts back the ledger, the marks and the kept head together
  shows the service a chain that continues its head, and the service cannot
  find that restore by itself. To keep the kept head and the marks where no
  restore of the host reaches them is the duty of the operator; where they
  stand within that reach, a restore of the host is a lost ledger that the
  operator declares (event 34).
- **Marks.** No entry is written without a mark, and the order of a write
  is fixed: the mark is made durable, then the entry is appended, then the
  kept head moves over the entry. The mark names the reservation key, the
  intent and the kind of entry, and it is durable beside the kept head
  before the write of the entry begins; the mark of an entry that belongs
  to no place, which is the entry of a key, names that key. A mark is
  closed in the write that moves the kept head over its entry. A mark that
  is open holds its place (events 10, 11, 15, 22 and 23), and it holds an
  intent as a record does. Each partial outcome of a write has one state. A
  write that fails after the mark and before the entry leaves the place
  held under the open mark. An entry that is written whole while the kept
  head has not moved is the one marked entry beyond the kept head: the
  place is held, the entry is evidence only, and the service never
  completes that write by itself. A mark or a kept head that cannot be
  read, and a mark whose writing has an outcome that the service does not
  know, lose the ledger (event 24). This is the stricter of two ways to
  keep a trace of a failed write, and the text takes it for that reason:
  the other way, a rule that an incomplete tail of the ledger holds every
  place that it could have named, holds nothing where the write left no
  octet in the ledger. That rule is kept for what the mark does not cover:
  a mark that cannot be read, and octets beyond the kept head for which no
  open mark accounts, could have named any place, and the ledger is lost.
- **The resolution of an open mark.** The service does not append past an
  open mark. Before any other write it appends, under that mark and with no
  new mark, the entry that records the hold of the place: a result `held`
  that binds, as its evidence and exactly as found, what stands beyond the
  kept head, which is nothing, octets that are no whole entry, the entry
  that the mark announced, or an earlier attempt at this entry. The entry
  that records a hold names what the mark that it closes names: the
  reservation key, the intent and the kind of the entry that the mark
  announced (sentence added with version 0.1.55). It then
  moves the kept head over that entry, which closes the mark (event 27).
  For the mark of an entry of a key the entry records that key as held
  (event 38). The resolution completes nothing: an entry that it binds as
  evidence takes no part in the state of its place, also now that the kept
  head covers it, and the place is `held` by the entry of the hold, which
  is its last entry. Until the resolution completes, the mark stays open,
  the place stays held, and the service attempts it again at every
  continuity check (event 28); it serves requests that only read, and it
  refuses a first request for another place with no code (event 3). A hold
  of one place therefore never becomes a hold of the ledger: it delays the
  other places by one write of the service itself. Another way was set
  aside, in which later writes move the kept head past the marked entry
  and its mark closes only in a reconciliation. Under it the kept head
  covers an entry that must not count, so the state of a place can no
  longer be read from its last entry under the head; open marks gather
  without bound until an operator acts; and the test for a lost ledger has
  to exempt as many entries beyond a mark as there are marks. With the
  hold recorded as an entry none of the three arises, and no hold is lost,
  because the mark stays open until the entry of the hold is under the
  kept head.
- **The continuity check** runs at every start, when a replica joins,
  before every answer that reads the ledger and before every write. A
  ledger is usable only if its identity and its exact history match the
  kept head; equal positions alone establish nothing. One difference is
  not a loss: what stands beyond the kept head under the one open mark,
  which is the entry that the mark names, whole or torn, and attempts at
  the entry of its hold. The service does not complete that write by
  itself. The place of the mark is held, and the entry, where it is whole,
  is evidence for a reconciliation and for nothing else. Every other state
  is a lost ledger: a history that does not match the kept head, also at
  an equal position; a history that cannot be proved; a ledger behind the
  kept head, which is what a restore to an earlier state looks like; a
  ledger beyond the kept head by more than the one open mark accounts for;
  more than one open mark; a mark that cannot be read; a second history
  beside the first; a kept head that is absent or cannot be read; another
  identity; a ledger that is absent or was created anew without a genesis.
  An empty ledger beside a delegation key is therefore never read as
  "every place free".
- **A lost ledger.** Under a lost ledger the service uses no delegation key
  and releases no signature. It answers `PLACE_HELD` to every request that
  passes the checks of J4.4, for every place of every parent whose
  delegation key it holds, and it takes no new delegation key into its
  care as a key that it may use: a parent that it first sees after the loss
  is held like the others, and it makes no key. The finding of the loss
  goes to the operational audit, because a lost ledger takes no entry
  except a genesis. The state ends in one of two ways. The complete ledger
  is put back and continues the kept head exactly; the check then passes,
  and that is a restore and no new ledger (event 35): every place has the
  state that its entries and the marks give, and a record `reserved` is
  held, because no claim outlived the loss. Or the operator makes the
  genesis.
- **The genesis.** A ledger starts only by an act of the operator of the
  service, which is the first entry of the new chain and holds the new
  identity and the first kept head: the first ledger of a service, and a
  new ledger after a loss (event 36). The entry names the loss that it
  ends: the kind of the finding, and the identity and the head of the old
  ledger where they can be read; for the first ledger of a service it says
  that none was before. A new ledger starts with every place of every
  parent whose delegation key the service holds at that moment in the
  state `held`, and with no exception: the new chain does not reach back
  to the making of those keys, a lost ledger is no chain whose continuity
  can be shown, and so no proof exists that such a key was never used for
  a place. Starting a ledger anew thus lifts no hold, at the genesis or
  later. For such a parent the way forward is a new parent with a new
  delegation key (J4.6), which the service makes under the new ledger. A
  genesis whose write does not complete leaves the ledger lost, and the
  operator makes it again.
- **The entry of a key and the life of a key.** A delegation key comes
  under a usable ledger once, by an entry of the chain. A key that the
  service itself makes under this ledger, for a parent that had no key
  before, enters by the entry that records its making, and that entry is
  durable under the kept head before the public key leaves the service, so
  that no parent names a key of the service that the chain does not hold
  from its making (event 37). Such a key enters with no record at any
  place. Every other key enters with every place of every parent held, and
  no reconciliation frees one (events 7 and 38): a key that signed, or
  could have signed, before this duty bound its service; a key that
  arrives from another custody or from another ledger, with or without the
  records that served it there; a key that the service held when a new
  ledger was started; and a key whose entry did not complete. The life of
  a key is thus read in one chain or not at all. A move of custody that
  keeps a key usable moves the whole ledger with its kept head and its one
  writer, which is the same ledger and no entry of a key; any other move
  costs the key its places, and the way forward is a new parent (J4.6).
- **The reconciliation.** It is an act of the operator of the service of
  J4.4, never of a caller, of the delegating agent or of a request on the
  interface of the service, and the chain records its opening, its evidence
  and its outcome as entries. It opens only on a held place of a usable
  ledger, by an entry after which the writer takes no `signed` from a claim
  for that place; a place whose record `reserved` has a live claim is not
  held, and the opening is refused. At most one reconciliation is open for
  a place; its outcome is judged on the state and the evidence at the
  write of the outcome, and an opening with no outcome is closed by a stop
  of the service. It never calls the signer. It takes no octets from a
  caller, from the operator's hand, from a copy, from the operational
  audit or from any record outside the chain. It has three outcomes. It
  confirms a signature (event 31) only on octets that the service itself
  wrote into the chain at the making, in a whole entry of the result that
  an entry of a hold binds as evidence, together with the reservation key
  and the intent, and that verify under the delegation key over the
  recorded intent; the identifier of the child is the one written with
  them. It returns the place to "no record" (event 30) only on proof that
  the key was never used for it, and the proof covers the whole life of
  the key: the chain shows the key from its making (event 37), and it
  holds for the place no mark and no entry of a use of the key, and no
  evidence of either; a result is written only after a use, so a place
  without a use has no result `signed`. The entry of a use is durable before the
  signer is called (J4.4 (g)), so its absence in a chain that is
  continuous from the making of the key is proof and not a guess; absence
  is evidence nowhere else, and absence from the operational audit is
  never evidence. A mark of a use that stayed open counts against the
  proof although the signer was not called under it (event 15): the text
  takes the stricter reading, and the price is that place. Where the key
  is not shown from its making, where the chain holds a mark or an entry
  of a use, and where the octets of a signature that was made stand
  nowhere in the chain, neither is proved (event 32): the place stays held
  for ever, the row is lost to that parent, and the next child takes
  another row or another parent. A write of the opening or of an outcome
  that does not complete leaves the place held and the act not taken, and
  the operator may act again (event 33).
- **The operational audit.** It stands apart from the chain, outside the
  write authority of the delegating agent, and holds what an operator
  reads: every refusal by the checks of J4.4, every finding that the
  ledger is lost, and the other answers of the service. It is bounded. It
  proves nothing, no rule of this section reads it, and no state of a
  place depends on a write to it.

**The two holds.** The hold of a place and the hold of a lost ledger differ
in reach. The hold of a place touches one pair of parent and place: every
other place of that parent and every place of every other parent is served
as before, once the service has recorded the hold in the chain (event 27).
The hold of a key whose life the ledger does not show is a hold of each of
its places, one by one, and reaches no other key. The hold of a lost ledger
touches every place of every parent whose delegation key the service
holds, a parent first seen after the loss included, and it lasts until the
ledger is restored whole or the genesis is made. After the genesis the
places of the parents that the service held stay held for ever, and a
parent whose key the service makes under the new ledger is served from it.

The ledger writes journal first, as the key holder of LIP-0013 section 3.6
does for a consent (J7.3 (d)): the record is durable, and only then is the
signature released. A service that cannot tell an empty ledger from a lost
one treats it as lost, as LIP-0027 H3.3 has it for a journal of closures
and as J7.3 (e) has it for the denials of a key holder.

The service has two codes for its caller. They are answers of the signing
service on its own interface and stand in this section alone. No verifier
reports them, no pipeline of LIP-0020 section 9 holds them, and no object on
the wire carries them. The codes of a verifier have other meanings
(`CHILD_SIGNER`, `DELEGATE_KEY_REUSE`, `PARENT_NOT_LIVE`, `CHILD_ORDINAL`),
the codes of a key holder judge the caller's run and not the place
(`GRANT_NOT_FOR_RUN`), and J4.4 itself names no code, so none of the
existing sets states a place that is taken or held.

| Code | Rule | Meaning | Retryable |
| --- | --- | --- | --- |
| `PLACE_CONFLICT` | J4.4 (e); event 6 | The request passed the checks of J4.4, the ledger is usable, and the place of the parent has a record or an open mark, in the state `reserved`, `signed` or `held`, with another intent. No signature exists for the refused payload | No. The same request is refused in the same way for as long as the record or the mark stands, and for good once the place is `signed`. It is served only if a reconciliation returned the place to "no record" (event 30), which no request brings about |
| `PLACE_HELD` | J4.4 (f); event 5 under `reserved`, under `held` and under a lost ledger; events 4 and 6 under a lost ledger; event 7; events 10, 11, 13, 15, 17, 19 and 21 to 23; events 24 and 34 | The request passed the checks of J4.4 and no signature can be released for it now. Either the place has a record or an open mark with this intent and no released result, because its first request is still served or its outcome is unknown; or the place is held with no intent recorded, as a place of a key whose whole life the ledger does not show, and then the code is given for every intent; or the ledger is lost, and then also for every intent | Not as a request to sign: no request makes the service sign for a held place. The same request asked again reads the record or the mark. It is answered with `PLACE_HELD` while the place is held or the ledger is lost, and with the stored signature once the place is `signed` (J4.4 (d)) |

The code follows from the table in every state that a request can meet.
A request that the checks of J4.4 refuse takes neither code in any state
(event 1), and so does the creating request whose second check refuses
(event 12). A first request that finds no room, that waits behind an open
mark of another place which the service cannot resolve, or whose mark is
shown not to have landed, takes neither code and may be asked again
(events 2, 3 and 9); no mark, no record and no signature exist for it.
A request that step 3 refuses because the anchor of its own child has
spent the coin of its row, at a place with no record, takes neither code
either (event 39; sentence added with version 0.1.55).
Every other request that passes the checks is answered with the stored
octets, with `PLACE_CONFLICT` or with `PLACE_HELD`. One code serves the
request that is still served, the unknown outcome, the key whose life is
not shown and the lost ledger, because the caller's part is the same in
all four: it cannot make the service sign, and it asks again or takes
another row or another parent.

What the ledger does not give is stated with each row: a verifier cannot
observe it. A child shows its signature and not the ledger behind it, and
two children of one row with different payloads, each validly signed, are
what a missing ledger, a broken one and a stolen key all produce. A
consumer therefore concludes nothing from the duty. What a verifier has for
a row is what it reads itself: on v4 the coin of the row, which admits one
issuance on the active chain (J1.9), the one child that the notary of the
row certifies (J1.6), and the row ledger of the executor (J1.3). The ledger
of the signing service keeps an honest service from signing twice, and that
is all it does.

Three things are no part of the duty. The ledger reads no clock and adds
no time member: the window of a child is a pair of heights, and LIP-0008
section 7.1 says where a clock check of an issuer stands. The ledger charges
no budget and no quota: consumption stays with the executor (J1.3). And the
reservation states nothing about a chain: that the coin of a row is unspent
is read on a node, by the service under J4.4 and by every verifier at use.

**The messaging key never grants authority.** That is the hard rule of this
decision, and J4.1 and J4.2 are its form on v4: a key that signs or
authenticates messages, as a channel key or as a request key, signs no
grant. On v3 no agent signs a grant at all (J4.7). A delegation key belongs
to one parent. The party that provides it provides a new key for each
parent; that is a duty of custody, because a verifier that holds one parent
cannot see another.

Where V7 checks the delegation request on v3, a v4 verifier checks the
child's signature under the parent's delegation key, the parent checks of
J4.3 (a) with `P`, and the child checks of J4.3 (b) with `C`, except the
comparison with the attestation key of the notary of the child's row. That
comparison stands in the certifier step, after V12, because the row is
known only from the ordinal and no step before V10 reads an attestation
(section 8.4, row F23 and pair Q18; amended with version 0.1.55, as a
proposal of that version).

A thief of the delegation key endorses a seal of its own, so the delegating
operator has no seal of such a child to spend, as the owner of a leaked grant
key has none (LIP-0008 section 5.2). Three things stop such a child: the
principal spends the parent's seal; a named notary refuses to certify it, or
withdraws its attestation; and, for a parent by name, the delegating operator
changes the owner of the agent's name. A notary certifies one child for a row
(J1.6), and under section 10.1 that notary is the row's. On v4 two coins add to
these stops: the coin of a row admits one issuance for the row on the active
chain (J1.9), and under section 10.1 the notary of the row ends it by spending
its stop coin (J2.7). The right of re-delegation bounds what the thief can sign
to the rows that the principal signed (sections 2 and 9.1). A closure that a
verifier never observed is not known to it.

The rules leave four limits. Different keys do not prove different
custodians: whether the delegation key and the messaging key are in
different hands is established by the owner's approval of a deployment, not
by a verifier. The signing service of J4.4 is a hot service, and a second
OS user on a host whose administrator is not the operator is no separation
from that administrator. The signing service cannot tell what the agent's
model intends from what the agent's host does; it can bound what it signs.
And the delegating operator loses the stop it has under the rule in force,
a rotation of the channel key; it keeps the change of the name's owner.

Four alternatives were set aside. Keeping the rule
in force keeps what the second paragraph lists: one key for messages and
grants, a host operator who can re-delegate, and children that stop with
every change of the key. Signing by the landlord only, on v4 as on v3, needs
no new key and stays the baseline (R5 of LIP-0008 section 12.6), but it is
not re-delegation by an agent, which the owners decided as R1. Checking a
child against the key that the name listed at the child's issuance needs the
name's value at a past height for every child and a rule against backdating,
and a key that was replaced because it leaked keeps every child it signed
before. A delegation key published in the agent's name is a new shape of the
name value that every reader must learn (LIP-0010), and every rotation of it
is a name update.

Two further points were decided with it. The first: the delegation signer
signs without a person. The rows of the parent, the notary of each row, the
coin of each row (J1.9) and its stop coin (J2.7) bound what the signer can
sign, and presence stays at the principal's grant key (K5 of the key map).
The presence rule of LIP-0013 section 3.6 gives the same answer for an
agent's key. The second: a key that every child's seal pays, named in the
parent and held by the delegating operator apart from the signer, is a
profile option and no part of the first v4 version. With it the operator
could spend the seal of a child that a thief of the delegation key signed.
It costs one more key, and under Draft LIP-0008 section 11.4 the child's
grant states that key in place of an endorsement. Section 11.2 holds Draft text, under a decision of
2026-11-16 that awaits the co-author's agreement, that puts this key into the
first v4 version.

A sketch that is not decided derives the delegation key of each parent
from the seed of the operator's signer, as seal keys are derived (LIP-0008
section 11.1).

Cases (J4). All are v4 cases; no v4 implementation
exists, and no result is claimed. "Today" is the rule in force, under which
the channel key signs children:

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S4-1 | A child signed by the parent's delegation key, with a full valid path | The same child, otherwise valid and bound to the parent, signed by the key the grantee's name lists, or by the parent's request key: `CHILD_SIGNER`. That child is the valid one today. The syntax of the new member must not be what refuses. |
| S4-2a | Owner, issuer, request, channel, delegation, attestation and seal keys all distinct | A parent whose delegation key equals, one at a time: the issuer's grant key; the owner key bound for the issuer's name; the request key, for a recipient by key; the owner key of the recipient's name, for a recipient by name; a pinned notary owner key; the parent's seal key, given as a compressed key with either parity: `DELEGATE_KEY_REUSE` for every child. A verifier that drops any one comparison fails the variant that names it. No rule today forbids a key in two roles. |
| S4-2b | The same | Per child, one at a time: a delegation key equal to a channel key that the recipient's name yields at admission; to the current attestation key of the notary of the child's attestation; to the child's seal key; to the child's own recipient key, for a child by key; to the owner key of the child's recipient name, for a child by name: that admission refuses, and the journal holds no closure. A verifier that drops any one comparison fails the variant that names it. |
| S4-2c | Another notary named by the parent publishes an attestation key equal to the delegation key | A child certified by a different named notary is still admitted. Run together with S3-8 of section 7.1. |
| S4-3 | The delegator's channel key is rotated under the same owner, with no alias; children signed before keep verifying | A child signed by the new channel key refuses as `CHILD_SIGNER`. Refusing the earlier children is wrong; today the rotation refuses them. Run together with S4-4 and S4-6, so that a verifier that ignores the parent does not pass. |
| S4-4 | A parent by name whose name stays with its owner; a parent by key whose holder's unrelated name changes owner: still live | A parent by name whose name changes owner: the parent refuses, and every child refuses as `PARENT_NOT_LIVE`, as the name mode requires today. No revocation rule is invented for the key mode. |
| S4-5 | At the signing service: an authenticated caller that the operator listed for delegation under a live parent, under LIP-0013 section 3.6 a run whose origin lists that parent, asks for a complete child, and it is signed | Through the service's public entry point: a supplied digest; a child outside the parent; a parent that is closed in the service's journal; a caller that shows only a signature of the messaging key; a generic or batch route: no signature exists. A test that hands the service a trusted caller identity shows nothing. |
| S4-6 | A new live parent with a new delegation key, after the old parent's seal was spent | A fresh child signed with the old key under the closed parent: `PARENT_NOT_LIVE`, at a verifier whose node shows the spend. |
| S4-7 | v3: a child issued by the landlord's grant key on a valid kind-8186 request, with a complete bundle | v3: a child signed by any other key refuses; a v4 delegation key gives nothing on v3. |
| S4-8 | A recipient by key with no name: the operator of its key holder runs the delegation signer, and its children verify | Treating that parent as portable through a name, and refusing it for lack of a name, are both wrong. |

Cases (reservation ledger, J4.4 (a) to J4.4 (g)). Their identifiers go on
from S4-11, because section 11.2 holds S4-9 and S4-10. All are cases at the
signing service and none is a case of a verifier: every signed child that
they name would verify. Each case names the events of the table of states
that it exercises. They run against the real entry point of the service with
its real store, as S4-5 does; a test that hands the service a ledger state
which the test itself wrote shows the answers and not the durability. In
every case all parents are held by the same signing service, in one ledger,
unless the case says otherwise. No such service exists, and no result is
claimed:

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S4-11 | First signature. For a parent and a place without a record, a listed caller asks for a complete child that passes J4.4 (events 4, 8, 14, 16, 18 and 20). The record `reserved` with the intent is durable, under the kept head, before the key is used; the checks of J4.4 on the parent and the row pass a second time; the entry of the use of the key is durable, under the kept head, before the signer is called; the result `signed` with the 64 octets and the child's identifier is durable, with its mark, its entry and the kept head over it, before the answer; and the signature verifies under the delegation key over the recorded intent. The chain then holds three entries for the place, and each carries its record and its audit entry as one | A service that signs first and writes its record afterwards, that calls the signer before the chain holds the entry of the use under the kept head, or that releases the signature before every write of the result is durable, fails the case, although the child that it returns is valid. So does one that keeps the proof of these steps in a store beside the chain. A request that J4.4 refuses leaves no mark and no record (event 1). |
| S4-12 | Exact replay. The request of S4-11, with the same parent, place and intent, is asked again, also after a restart of the service: the answer holds the stored 64 octets, byte for byte (event 5) | A second valid signature over the same digest, made with other auxiliary randomness, fails the case, although a verifier accepts it (LIP-0020 W5.4). The ledger holds one record for the place, and the replay writes no reservation. The same request asked after the service's journal holds the parent closed, after the window of the parent has ended, or by a caller that was taken off the list after the result became durable, is refused by the checks of J4.4, as a first request would be (event 1): the answer holds no stored octets, neither code of this section, and nothing that shows a record. The same payload asked by another listed caller is the same intent and takes the same stored octets (J4.4 (b)). An answered replay appends nothing to the chain; its line in the operational audit proves nothing, and the answer does not wait for it (J4.4 (g)). |
| S4-13 | Another payload for the same place. After S4-11 the replay of S4-12 is still answered | A child of the same parent and ordinal that differs in one member and still passes the checks of J4.4, such as a lower amount of a limit or another height of its window: `PLACE_CONFLICT`, no signature exists, and the record is unchanged (event 6). Asked again, it refuses in the same way; so it does while the record is `reserved`, while the place is held and while a reconciliation is open. A variant that also fails a check of J4.4, such as a recipient that the row does not name, or the same variant from a caller that is not listed, takes the refusal of J4.4 and not `PLACE_CONFLICT` (event 1): a service that answers it from the ledger fails. A service that signs the second payload, that moves the request to a free ordinal or that answers with another key fails. |
| S4-14 | A stop after the reservation and before the signature. The service is stopped when the record `reserved` is durable and no mark of a use of the key is, and is started again. The record is still there with its intent | The same request asked again: `PLACE_HELD`, and no signature (event 5). A request with another intent: `PLACE_CONFLICT` (event 6). The service signs nothing by itself after the start. A service that treats the place as free, or that signs on the repeated request, fails (event 26). No request and no act of the service ends the state; its one exit here, since the chain holds no mark and no entry of a use, is the reconciliation of S4-18. Where the stop comes after the mark of the use is durable, that exit is closed and the place stays held for ever (events 15 and 32), although the signer was not called. |
| S4-15 | A stop after the signature and before the record of the result. The signature was made, the result `signed` is not durable in every write, and the service is stopped and started again | The same request asked again: `PLACE_HELD`. The signature that was made before the stop is not released, whether or not the service still holds its octets, and the service does not sign again (event 26). What follows depends on the last component of the result that was durable before the stop, and S4-28 and S4-19 hold the branches: where the entry of the result stands whole in the chain beyond the kept head, the service records the hold with that entry as evidence, and a reconciliation may confirm the octets (events 23, 27 and 31); where the octets stand nowhere in the chain, the place stays held for ever (events 21, 22 and 32), because the chain holds the entry of the use of the key and no proof of an unused key exists. |
| S4-15a | A signature that fails the service's own verification. The service is not stopped: it signed, and its verification of the fresh signature over the recorded intent fails, as with a faulty signer or wrong key material. The place is held, and the failure is a result `held` in the chain (event 25, J4.4 (g)). Run together with S4-11, where the verification passes and the signature is released | The octets that failed are not released, to the request that created the record or to any other. The same request asked again: `PLACE_HELD`, and the service does not sign again. A request with another intent: `PLACE_CONFLICT`. A service that signs a second time for the place, in the same request or in a later one, until a signature verifies, fails the case, although the child that it then returns is valid: that is a second use of the key for the place (J4.4 (a)). So does one that puts the record back to `reserved` or treats the place as free. No reconciliation ends this hold (events 19 and 32): no signature that verifies was recorded, and the key was used. The same holds for a signing call that returns nothing or whose outcome the service does not know (event 17). |
| S4-16 | A second parent with the same place number. Parent `P2`, with a delegation key of its own, has a row with the ordinal that S4-11 used under `P1`. A child of `P2` at that ordinal is served as a first signature, with a record of its own (events 4 and 8) | An answer of `PLACE_CONFLICT` or `PLACE_HELD` on the strength of the record of `P1`, also while the place of `P1` is held, is wrong; so is the stored signature of `P1`. A ledger that is keyed by the ordinal alone fails. |
| S4-17 | A second place of the same parent. Another ordinal of `P1` is served as a first signature (events 4 and 8) while the place of S4-11 is `signed`, and while it is held in each form: under a record `held`, under a record `reserved` with no live claim, and under an open mark, which the service first resolves (S4-27) | A service that refuses every place of a parent because one of them is held or in conflict fails; so does one that answers from the record of the first place. Run together with S4-13, so that a service that signs every request does not pass. The hold of a place reaches one pair of parent and place and no other. The hold of a lost ledger is another hold: under it the same request for the other ordinal is answered with `PLACE_HELD` (event 4 in the last column, S4-24), and a service that serves it there fails. |
| S4-18 | A held place for which the key was never used. The state of S4-14, or a mark of a reservation whose entry never landed (S4-21), under a key that the service made under this ledger. The operator opens a reconciliation (event 29); the chain shows the key from its making, and it holds for the place no mark and no entry of a use of the key, and no evidence of either. The place returns to "no record" (event 30), the chain holds the act with its evidence, and the next request is a first request, also with another intent than the one first reserved | The same reconciliation where the chain holds a mark or an entry of a use of the key, or where the key is not shown from its making (S4-29): nothing is proved, and the place stays held (event 32). An operational audit that shows no use proves nothing, and a reconciliation that frees a place on it fails. A service that frees a held place by itself, at a start, after a time or on a request, fails. So does one that deletes the entries of the place, and one that frees the place of S4-15 or of S4-15a. Without a reconciliation the place of S4-14 is held for ever, and that is no failure of the service. |
| S4-19 | A held place for which a signature was made. The state of S4-15, in the branch where the service wrote the octets into the chain itself before the stop: a whole entry `signed` beyond the kept head under its open mark, which the service bound as evidence when it recorded the hold (events 23 and 27). The reconciliation confirms those octets, which verify under the delegation key over the recorded intent (event 31); the place is `signed`, and the request is then answered as in S4-12, with those octets | Octets that the operator brings from outside, from a caller, from a copy, from the operational audit or from a log that the service did not write into the chain, are not taken, also where they verify over the recorded intent: nothing is recorded, and the place stays held. A reconciliation that calls the signer fails the case, although the child that results is valid: that is a second use of the key. In the branch where the octets stand nowhere in the chain, the place stays held for ever (event 32). A write of the outcome that does not complete leaves the place held and the outcome not taken (event 33). |
| S4-20 | The fence between the creating request and a reconciliation. A request reserves and is slow inside the signing call; it then completes, the record is `signed`, and the signature is released. A reconciliation that the operator tries to open meanwhile is refused, because the claim is live (event 29) | After a stop of the service (event 26) the operator opens a reconciliation for the place. An instance of the earlier run that returns with its signature writes nothing, because its token is older and the place has no claim, and releases nothing. A service in which the octets of the returning request and the outcome of the reconciliation can both be recorded, in either order, fails: two signatures for one place would then be released. |
| S4-21 | A reservation write that fails. The store refuses the first write of a reservation before any mark landed, and the service shows that none did: the request is refused with no code, no mark and no record exist, and the same request asked again is served as S4-11 (event 9) | By the last component that is durable. The mark is durable and the write of the entry is cut, by a stop or by an error of the store (event 10); and the mark and the whole entry are durable while the kept head has not moved (event 11). In both the place is held after a restart, the same request takes `PLACE_HELD` and another intent `PLACE_CONFLICT`, each read from the mark, and the service records the hold in the chain before it writes for any other place (event 27). A service that finds no record after the restart and reserves another intent for the place fails; so does one that moves the kept head over the entry of event 11 and treats the place as `reserved`. A mark or a kept head that cannot be read, and a mark whose writing has an unknown outcome, lose the ledger (event 24, S4-24). |
| S4-22 | Two requests together for one reservation key. With one intent: one record is created, one request signs, and the other takes `PLACE_HELD` and, asked again, the stored octets of the first (events 5 and 8) | With two intents: one creates the record, and the other takes `PLACE_CONFLICT` (event 6). The request that loses the test writes no mark. A service that creates two records, that signs both intents, or that signs twice for one intent fails; a service that checks for a record and writes it in two steps fails under load although each step is right. |
| S4-23 | Two writers. A second instance of the service, or a replica, serves requests for the delegation key of `P1` through the one ledger and its one writer, and the answers are those of S4-11 to S4-13 (events 4 to 6 and 8; the fence is the contract's and has no event of its own) | A second instance with a ledger of its own for the same key, and an instance that returns with an older write token, sign nothing and release nothing. A service in which two instances each keep a conforming ledger and each sign another intent for one place fails. |
| S4-24 | A lost ledger. Control: on the continuous ledger the replay of S4-12 is answered. The ledger is then put back to an earlier state that is consistent in itself, taken before S4-11, while the kept head stays | The check finds a ledger behind the kept head, and the ledger is lost (event 34); the finding is in the operational audit and in no entry of the ledger. Every request that passes the checks of J4.4 takes `PLACE_HELD`: the replay of S4-12, although its record was `signed`; a request with another intent, which takes no `PLACE_CONFLICT`; another place of `P1`; a place of `P2`; and a place of a parent `P3` that the service first sees after the loss. A request that fails J4.4 takes the refusal of J4.4 and does not learn of the loss. A service that reads the restored ledger and signs another intent for the place of S4-11 fails; so does one that serves `P3`, one that treats an absent or empty ledger as "every place free", and one in which a kept head that cannot be read counts as a new start. Putting the complete ledger back, so that it continues the kept head exactly, ends the state (event 35), and S4-12 is answered again; a record that was `reserved` at the loss is held after it. A restore of the whole host that puts back the ledger and the kept head together is outside what this case can show at the service: the service cannot find it, and the duty is the operator's (J4.4 (f)). |
| S4-25 | The genesis after a loss. The operator starts a new ledger by an act that is its first entry and that names the loss it ends: the kind of the finding, and the old identity and head where they can be read (event 36). Every place of `P1` and of `P2` starts held and stays held. A parent `P4` whose delegation key the service makes under the new ledger, by an entry that is durable before the public key leaves the service, enters with no record and is served as S4-11 (event 37) | A new ledger that starts empty, with the places of `P1` and `P2` free, fails. So does a ledger whose first entry is no genesis or names no loss; a place of `P1` or `P2` that is freed at the genesis or by a later reconciliation, on whatever evidence, the old ledger and the operational audit included; and a genesis that is recorded only in a store beside the chain. For a held parent the way forward is a new parent with a new key (J4.6). |
| S4-26 | Room and the two audits. With room secured the first signature of S4-11 leaves three entries in the chain: the reservation, the use of the key, the result. A request for which the service cannot secure the room is refused with no code; no mark and no record exist, no key is used, and the same request asked later, with room, is served (event 2) | A service that reserves and then fails for want of room, leaving a held place where a refusal was due, fails the capacity duty. The operational audit holds a line for each refusal by the checks of J4.4 and for the finding of a lost ledger, where its store can take one; the chain holds none of them, and a service in which a caller that is not listed can make the chain grow fails. With the operational audit made unwritable, every answer and every state of S4-11 to S4-13 is unchanged, and a service that holds back an answer or holds a place for want of that write fails. An entry of either audit that the delegating agent could write or remove fails the case. |
| S4-27 | Across places. An entry beyond the kept head, and another place. The result of place 1 of `P1` is left as in S4-15, a whole entry `signed` beyond the kept head under its open mark (event 23). A first request then comes for place 2 of `P1`. The service first appends the entry that records the hold of place 1, with the marked entry as evidence, and moves the kept head (event 27); it then serves place 2 as a first signature (events 4 and 8). Place 1 is `held` under a record `held`, and the replay of its request takes `PLACE_HELD` | A service that appends the reservation of place 2 past the marked entry fails. So does one in which the kept head, once it covers the marked entry, lets a replay of place 1 take the octets without a reconciliation; one that completes the write of place 1 by itself; one that sets the marked entry aside or deletes it; and one that answers place 2 with `PLACE_HELD` on the strength of the hold of place 1. Where the store refuses the entry of the hold, the mark stays open, place 2 is refused with no code and may be asked again, and replays of other places that are `signed` are still answered (events 28, 3 and 5). The same is run with the place of S4-21 in the place of place 1, and with a second parent in the place of place 2. |
| S4-28 | By partial outcome. The write of the result, by the last component that is durable. Control: all three are durable, the mark, the entry and the kept head, and the signature is released (event 20) | The store is cut after each component in turn. No mark landed: the place is held, nothing of the result stands in the chain, and the place stays held for ever (events 21 and 32). The mark alone: held under the open mark, with no whole octets, and held for ever after the hold is recorded (events 22, 27 and 32). The mark and the whole entry, the kept head not moved: held under the open mark, and the entry is evidence for S4-19 alone (events 23, 27 and 31). A mark or a kept head that cannot be read: the ledger is lost (event 24). In none of them is the signature released, and a service that releases it because the entry stands whole, or because a later kept head covers it, fails. The same cuts are run on the write of the use of the key: with no mark of the use the place can be freed as in S4-18 (event 13), and with the mark durable it cannot (event 15), and in neither is the signer called. |
| S4-29 | Over the whole life of a key. Control: a key that the service made under this ledger, whose place is held as in S4-14, is freed as in S4-18 (events 37 and 30) | A key that signed one child for a place before it came under this ledger enters it (event 38). Every place of its parent is held; a request for the signed place and a request for any other place take `PLACE_HELD`, with whatever intent (event 7). The operator opens a reconciliation for the signed place: the chain of this ledger holds no use of the key for it, and nothing is proved (event 32). A service that frees the place because its own chain shows no use from the entry of the key onward fails: it would sign a second child for the place. So does one that enters as unused a key that arrives with a statement, a log or a copy of another ledger, and one that frees such a place at a genesis (S4-25). |
| S4-30 | The second check. Control: S4-11, in which the checks pass both times | The parent is closed in the service's journal after the reservation is durable and before the write of the use of the key. The request ends with the refusal of J4.4 and no code of this section; the signer is not called, no mark and no entry of a use exists, and the place is held (event 12). A service that signs the child, which every verifier would refuse, fails. The place can be freed as in S4-18. A closure that comes after the second check still costs the place. |
| S4-30a | A replay after publication (case added with version 0.1.55, as a proposal of that version). The request of S4-11 is asked again on the continuous ledger, after the confirmed issuance anchor of its child has spent the coin of its row. Step 1 passes, the check of the coin by that anchor alone (section 8.5, I9); the place has its record `signed`, and the answer holds the stored 64 octets, byte for byte, as in S4-12 (event 5). The service does not sign, appends nothing and sends no notice | The same request on a continuous ledger that holds no record and no open mark for the place, the coin of the row spent by the confirmed issuance anchor of this child: refused with no code; no signature exists, nothing is reserved, no mark is written, the chain is unchanged, and the operational audit holds the entry and the operator the notice that a signature exists outside this ledger (event 39). A service that takes the request for a first request and signs fails the case, although the child that it returns would verify: it would make a second signature for a place whose first one this ledger does not show. So does one that answers `PLACE_HELD` or `PLACE_CONFLICT`, or that reserves the place. With the same coin spent by any other transaction the request is refused in step 1 as before, with the code of that check and no notice (event 1). Under a lost ledger the same request takes `PLACE_HELD` in step 2 and no notice (event 4 in the last column, S4-24); for a place that is held with no intent recorded, after a genesis included, `PLACE_HELD` (event 7, S4-25); for a place with a record `reserved` or `held` of this intent, `PLACE_HELD` (event 5); and with another intent than the record, `PLACE_CONFLICT` (event 6). |
| S4-30b | The coin spent by the child's own anchor between the two checks (case added with version 0.1.56, as normative text). Control: S4-11, in which the coin of the row is unspent at step 1 and at step 6 and the signature is released | After the reservation is durable and before step 6, the confirmed issuance anchor of this child spends the coin of its row. The repeat refuses as `ROW_COIN_REQUIRED` (event 12); the signer is not called, no signature of this ledger exists, and the place is held. The service writes an entry of the operational audit and notifies its operator that a signature exists outside this ledger, as in event 39, where its store can take the entry. A service that signs, that answers with stored octets, or that gives no such entry and notice, fails the case. Run together with S4-30, where the second check refuses for another reason and no notice of event 39 is given, and with S4-30a, where the same spend is met at step 1 on a replay. |

A vector plan goes with these cases. It is a plan and holds no vector; no
file of it exists, and `tools/grantv4` and `vectors/LIP-0020/` do not change.

| Cases | Kind | What a vector would state |
| --- | --- | --- |
| The intent (J4.4 (b)) | Deterministic | The canonical payload of a child and its intent, beside its identifier, so that an implementation that reserves under the identifier or under a hash of the signed form is reported. The child payloads of `vectors/LIP-0020/grant-v4.json` serve as inputs by reference |
| S4-12, the replay | Deterministic, on a stated ledger state | A record `signed` with its reservation key, its intent and its 64 stored octets, and a request with the same three values: the answer is the stored octets, compared byte for byte. Beside it a second signature that verifies over the same digest, which the answer must not be |
| S4-13, the conflict | Deterministic, on a stated ledger state | A record in each of the three states and a request with another intent: `PLACE_CONFLICT`, no signature, and the state after equal to the state before |
| S4-16 and S4-17, the independence of keys | Deterministic, on a stated ledger state | Records under (`P1`, 1), and requests under (`P2`, 1) and (`P1`, 2): each is a first signature. A vector states the record that the request creates and not the octets of the new signature, which auxiliary randomness leaves free |
| A held place answered (J4.4 (f); events 5 to 7) | Deterministic for the answer alone | A record `held`, a record `reserved` that the request did not create, or an open mark: `PLACE_HELD` for the recorded intent and `PLACE_CONFLICT` for another. A place of a key that entered as held, with no intent recorded: `PLACE_HELD` for every intent |
| The partial outcomes of a write (events 9 to 11, 13 to 15, 20 to 24, 27 and 28; S4-21, S4-27, S4-28) | Deterministic, on a stated chain, kept head and marks | For each of the three writes of a request, the chain, the kept head and the marks as each cut leaves them: the state of the place, the answer to its request and to a request for another place, the entry that the resolution appends, and the state after it. A vector states what is read and not that a store reaches it |
| The order of the checks (events 1, 5 and 6; S4-12, S4-13) | Deterministic, on a stated ledger state and a stated outcome of the checks of J4.4 | A record `signed` or `held`, and a request that fails a check of J4.4, with the recorded intent and with another: the refusal of J4.4, no code of the ledger, no octets, and the state after equal to the state before |
| A lost ledger answered (event 34; S4-24) | Deterministic for the answer alone | A ledger stated as lost, and requests that pass the checks: for the recorded intent, for another intent, for another place, for another parent and for a parent with no record at all, the answer is `PLACE_HELD` |
| The outcomes of a reconciliation (events 30 to 32; S4-18, S4-19, S4-29) | Deterministic, on a stated chain and stated evidence | A held place with the entries of the chain from the entry of its key: a key that the chain shows from its making and no mark or entry of a use give "no record"; octets in a whole entry of the result that an entry of a hold binds, and that verify, give `signed`; octets marked as brought from outside or from the operational audit, a chain with a mark or an entry of a use, and a key that the chain does not show from its making give the state before. A vector states the transition and not how the evidence is gathered |
| The start of a new ledger and the entry of a key (events 36 to 38; S4-25, S4-29) | Deterministic, on a stated list of keys | The keys that the service holds at a genesis: every place of each is held after it, and stays held under every stated reconciliation. The state of the places of a key that the service makes afterwards, and of a key that enters from elsewhere |
| S4-11, S4-30 and S4-30b, the order of record, second check, entry of the use and signature | Behavioural only | No vector shows that a record was durable before the key was used. It takes the real service and its store |
| S4-14, S4-15, S4-15a, S4-21, S4-27 and S4-28, the stops, the failed verification and the failed writes | Behavioural only | A stop, a store that refuses or cuts a write after each of its components, or for S4-15a a signer whose output does not verify, is injected between two steps of a running service. A vector can state the answer on the state that is left, which is the rows "a held place answered" and "the partial outcomes of a write", and not that the service reaches that state |
| S4-20, S4-22 and S4-23, the fence, two requests together and two writers | Behavioural only | They take concurrent requests, a second instance and a returning instance on the real store. A vector states neither the atomic step nor the token |
| S4-24 to S4-26, the continuity check, the genesis as an act, the room and the two audits | Behavioural only | They are qualified on a real store, as the stores of J1.4 and of LIP-0025 are: that a restore of the ledger is found, that no ledger starts without the act, that a refusal for want of room comes before any mark, that both audits are outside the reach of the delegating agent, and that no answer and no state depends on the operational audit. A restore of the whole host is no case of the service: nothing at the service shows it |

The deterministic vectors would stand in a file of their own,
`vectors/LIP-0014/ledger-vectors.json`, as vectors of a transition: a ledger
state before, a request, the answer and the ledger state after. They are
vectors of a service and belong to no conformance class of a verifier. The
behavioural cases belong to the qualification of a signing service on its
real store, with the stops injected in an isolated fixture, and to no vector
file.

### 11.2. The child-seal key (Draft, 2026-11-16)

Ivan Oparin decided, as recorded by the lead on 2026-11-16, that v4 has a
separate child-seal key from its first version: it is neither the grant key
nor the delegation key. This replaces the point of J4, decided on
2026-11-14, that made the key a profile option outside the first version.
The text is written optimistically; the co-author's agreement is pending,
and until it is given section 11.1 stands.

The key closes the case of section 11.1 in which a thief of the delegation
key signs a child with a seal of its own, so that the delegating operator
has no seal of that child to spend. Under CS2 every child's seal pays a key
that the parent names and the thief does not hold. LIP-0008 section 11.4 uses
the same key to drop the seal-key endorsement for children: the parent, which
the grant key signs, fixes the key, and the child names its seal's outpoint
and states the child-seal key as its seal key (LIP-0008 SB1), which a
verifier compares with the parent's (CS2).

| # | Rule | Refusal |
| --- | --- | --- |
| CS1 | An issue capability MUST name one child-seal key, beside its delegation key (J4.1). The principal signs it with the parent, and the grantee's consent covers it. Each parent has a child-seal key of its own. Its form is the form of a seal key (LIP-0020 section 3), and its bytes are fixed with the v4 bytes. | A parent without one is unusable as a parent: every child refuses as `CHILD_SEAL_KEY` |
| CS2 | Every child of the parent has a revocable-only seal whose script is the single-key script of the parent's construction profile for the child-seal key, and the child names that seal's outpoint (LIP-0008 SB1). The verifier reads the script on its own node (LIP-0008 SB2). | A child whose seal key is another key: `CHILD_SEAL_KEY`; a script that does not match: `SEAL_SCRIPT` |
| CS3 | Parent checks, as in J4.3 (a), by the 32-byte x coordinate. The child-seal key MUST differ from the issuer's grant key; from the delegation key of the same parent; from `P`'s request key, or the owner key of the recipient's name; from the owner key bound for the issuer's name; from the owner key pinned for each notary; and from the key of `P`'s own seal. | `P` is unusable as a parent, and every child refuses as `DELEGATE_KEY_REUSE` |
| CS4 | The child-seal key is held by the delegating operator apart from the signing service of J4.4: not by that service and not under the delegating agent's OS user. The signing service holds no private child-seal key. | none at a verifier |
| CS5 | A validated spend of a child's seal is the delegating side's revocation of that child, and closes it under LIP-0008 section 5.1 (SB3). One transaction may spend the seals of several children of one parent. | The child refuses under the closure of LIP-0008 section 5.1 |
| CS6 | Replacing the child-seal key requires a new parent, as J4.6 has it for the delegation key. | none at a verifier |

What it leaves:

- **One address for the children of a parent.** Every child's seal pays the
  same script, so a chain observer links the children of one parent through
  their seals. A party that sees the grants learns nothing new, because each
  child names its parent. A per-child key derived from a key named in the
  parent would remove the link; it is not proposed (open questions).
- **A thief of the child-seal key** spends the seals of the children of that
  parent early, which closes them, and takes the seal amounts. It signs no
  child and no grant.
- **A thief of the delegation key** still signs children within the rows of
  the parent, and each of them can now be revoked by the delegating side.
  The stops of section 11.1 stay.

The Link book still lists the key as a profile option outside the first
edition of v4 (§3.8, the row «Ключ печатей дочерних доверенностей, версия 4»;
§10.3), and §4.9.9 «Подтверждение ключа печати» describes the endorsement
that LIP-0008 section 11.4 drops. Both are updates for the book once agreed;
the shape of the key in §3.8, held apart from the delegation service, is the
one written here.

Cases (child-seal key):

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S4-9 | A child whose seal pays the parent's child-seal key under the parent's profile, with an outpoint that the child names: admitted; a spend of it by the delegating operator closes the child | A child signed by the delegation key whose `seal.key` is another key than the child-seal key of its parent: `CHILD_SEAL_KEY`. A child that states the child-seal key and whose named outpoint holds another script, the script of another key included: `SEAL_SCRIPT`. (Amended with version 0.1.55, as a proposal of that version: section 8.4, rows F12 and F21, rule T5. Through version 0.1.54 the first refusal read "whose seal pays another key".) |
| S4-10 | A parent whose grant, delegation, request, notary owner, own seal and child-seal keys are all distinct | A parent whose child-seal key equals, one at a time, each of those keys, under either parity: `DELEGATE_KEY_REUSE` for every child. A parent with no child-seal key: `CHILD_SEAL_KEY` for every child. |

## 12. Vectors for the contract profile

[`vectors/LIP-0014/contract-vectors.json`](../vectors/LIP-0014/contract-vectors.json)
holds 190 vectors for the contract profile `/2`: 151 contracts and 39 pairs
of a parent and a child.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `contracts` | 15 valid, 3 valid in the spend profile alone, 133 refused, of which 12 hold two defects | Section 3.1 on the bytes of one document: the rules that its member set selects, and the first code in their order |
| `pairs` | 10 passing, 1 root, 28 refused, of which 10 hold two defects | The steps V1, V3, V4, V6, V8 and V9 of section 8 on two valid contracts and on the grant id of the parent, which the vector states |

A contract is a string whose UTF-8 octets are the octets of the document. A
valid contract states its SHA-256, the v3 scope and budget that LIP-0013
section 2.2 derives from it and the booking tag of LIP-0013 section 2.4, so
that the binding of section 3.2 can be recomputed. A refused contract holds one
defect, states the expected code and names a valid neighbour that differs from
it in that defect. A vector marked compound holds two defects, states the one
that the order reports and names no neighbour. Each vector names the rules that
it exercises, by labels that the file lists with their place in this LIP.

| Rule of section 3.1 | Refused contracts | Among them |
| --- | --- | --- |
| 1 | 26 | A document of 8193 bytes beside a valid one of 8192; a member that is missing, added, repeated, renamed or out of order among the fifteen; a space, a tab, a sign, a leading zero, a fraction, an exponent, `null` and `true` inside `delegate`; an integer of 9223372036854775808; a member of another JSON type |
| 2 | 3 | Fifteen members with the string of profile `/1`, and eleven members with the string of profile `/2` |
| 3 to 7 | 10 | `scope_text_sha256` with 63 characters and in uppercase; four further defects of rule 3 and one of each of the rules 4 to 7, which profile `/1` already has |
| 8 | 8 | Ordinal 17; a parent id with ordinal 0, and ordinal 1 without one; a parent id that is short, in uppercase or no hexadecimal string; a child with `depth` 1 and with `depth` 2 |
| 9 | 77 | Each member of the three tables of section 2 with its violations; the member set of the first draft; `depth` 1 without a notary; a bare name in `notaries`; names in the order of their numbers where the order of their bytes differs |
| The order of the rules | 9 | Pairs of defects of two rules, and a child whose `delegate` holds `depth` 1 and nothing else |

Eight contracts touch the spend profile and state a second outcome,
`expected_spend_profile`: the outcome of the same rules with D12 lifted. Three
of them are valid there and refuse for a reader of this revision as
`CONTRACT_DELEGATE`, which is case S1-8. Five refuse in both, for a sum of caps
above the pool, a pool of 0 beside a delegable `spend`, and a pool or a cap
above its largest value. Six of the pairs belong to the spend profile and are
judged with D12 lifted, among them case S1-1m: a child of 60 under a row with a
cap of 40 refuses as `CHILD_BUDGET_OVER`, although 60 is at most the pool of
100. No reader admits a contract of the spend profile before the owners decide
that `spend` is delegable.

The pairs hold the cases of section 9.1 that two contracts decide. A child of
ordinal 1 that names the executor or the grantee of row 2 refuses (S1-1). An
ordinal above the number of rows refuses before any row is read (S1-2b). Two
rows with the same executor and grantee are a valid parent, and each has its
child (S1-4). Ten pairs hold two defects and show the order of the steps.

The limits of the file are these. It holds no grant, no delegation request and
no attestation: no vector recomputes a `grant_id`, verifies a signature, reads
a node or walks a notary's name, so the steps V2, V5, V7 and V10 to V18 have no
vector here. Of step V4 the pairs hold no repeated id, and of step V6 they
compare the network and the principal; the genesis is a field of the grant and
stands in no contract. The parent of a pair is always a valid contract; what a
verifier reports for a parent that is none is an open question. The keys are
published test keys of BIP-340 and never real keys; grant ids, transaction ids
and the checkpoint are placeholder digests. One rule is not separated by any
vector, because no contract can separate it: a `cap` above its largest value
also exceeds every valid pool.

No checker for these vectors is in this repository; `tools/trustcheck` reads
profile `/1` alone. The expected outcomes were stated by hand, computed by one
implementation and decided again by a second one that shares no code with the
first, with 0 mismatches over the 190 vectors. Both implementations also give
the 36 published contracts of profile `/1` in `vectors/LIP-0013/` their
published outcomes. Two controls were run on the second implementation. In 397
copies of the file one thing was changed each time, an outcome, a byte of a
contract or a derived value, and each change was reported at the vector that
held it. And 64 copies of the implementation, each reading one rule in another
way, were each reported by the unchanged vectors at the cases written for that
rule; one of them showed that a vector had been filed under the wrong rule, and
that vector was removed. Neither implementation is published. Both come from
the author of this text, so an error of understanding that they share is in the
vectors.

## Alternatives

- **Attestation only for children with textual scope** (proposal (e) of
  LIP-0008 section 12.6 as first stated): rejected by D1. It needs a rule that
  says when a scope is textual.
- **The notary list in the principal's name value:** rejected. The list a
  verifier reads would be the value at check time, so adding a notary later
  would widen trust in grants already issued. On v3 an extra member makes the
  value unreadable, and on v4 a changed `swarma` refuses every grant of the
  issuer.
- **The notary named by configuration or instructions alone:** rejected. Such
  a source is not an input every verifier shares.
- **Trusting the notary for the countable conditions:** rejected. It turns a
  stolen attestation key into a way to widen any limit.
- **Anchoring in an update of the notary's name:** rejected by D10. It adds
  one name operation per child to the notary's name history.
- **A third link for deeper trees:** not taken (D7).
- **One stop coin for each notary and parent,** whose spend ends every row
  of that notary under the parent at once: recorded on 2026-11-14 as a
  future option, for example as an emergency brake for a compromised
  notary. It is no part of the first v4 version, and its cost and its
  limits are not worked out (section 10.1).

## Security consequences

- **A stolen or careless attestation key** certifies children that exceed their
  parents in words. It cannot widen an action set, a repository list, a window
  or a child's own budget, because every verifier enforces those itself. The
  sum over siblings does not rest on it either: the signed rows bound it
  (section 9.1). What the key can add is a second document for a row, inside
  the envelope of that row. The notary's name-owner key rotates the attestation
  key, which makes every attestation under the old key refuse at once.
- **An unavailable notary** stops new children and new certifications.
  Certified children keep working: admission reads the seal and the anchor, not
  the notary's service. Naming up to four notaries bounds the outage. It also
  means that two notaries can each certify a child under one ordinal, because
  each keeps its own record (section 6.2). Both children fit the same row.
  Section 10.1 holds Draft text for this case, under a decision that awaits the
  co-author's agreement (J2).
- **A withdrawal for cause does not reach everyone.** It binds the parties that
  observed its frame. Another named notary can certify the child again, and a
  verifier that starts later admits it. Section 10.1 holds Draft text for this
  case, under a decision that awaits the co-author's agreement (J2).
- **The notary's name can change hands, and the right to certify does not go
  with it.** After a transfer, or after an expiry and a new registration, the
  holder of a notary's name publishes its own attestation key; the pins, the
  checkpoint and the writer rule refuse its attestations under every parent
  that bound the earlier owner (section 7.1). A thief of the notary's
  name-owner key is not stopped by them.
- **Scope text binds nobody at admission.** The notary judges the text once. No
  admission step compares an instruction with it. Section 3.4 holds Draft text
  for this case, under a decision that awaits the co-author's agreement (J5).
- **On v4 an agent's messaging key signs its children**, by the rule in force.
  Section 11.1 states what follows from that and holds Draft text, under a
  decision that awaits the co-author's agreement (J4), that replaces the rule.
- **Self-certification.** V13 refuses a notary key equal to the delegator's or
  the delegatee's key and a notary name equal to an executor's. Different keys
  do not prove different parties; the control is that the issuer, not the
  delegator, names the notary.
- **Replay onto another child.** The attestation binds both grant ids, both
  contract hashes, the ordinal, the network, the genesis and the principal. Two
  children with identical contracts still have different ids, because each
  grant has its own seal.
- **A v3 reader that ignores the contract** does not see a closed parent. The
  joint revocation transaction of section 10 closes the children for it.
- **A reorganisation that drops the attested tip** makes V16 refuse until the
  notary signs again against the new chain.
- **The notary learns both contracts and both scope texts.** The anchor carries
  hashes only. A deployment that cannot disclose them uses issuance by the
  operator's signer without a child (LIP-0008 section 12.6, R5).
- **Cost.** A certified child adds one anchor transaction and one seal output
  on the notary's side to the child's own issuance. No size or fee of it has
  been measured.
- **Disputes.** The attestation is a signed statement and no proof (LIP-0012
  section 6). Evidence open to any holder: both contracts and texts, the
  attestations, the anchor, an equivocating pair, a `mechanical` `pass` over a
  child that fails section 4, and a withdrawal for cause. Judging a dispute
  stays with the arbiter of a contract.

## Conformance impact

None while this LIP is a Draft. The vectors of section 12 cover the contract
profile `/2` and the checks of a child against its parent that two contracts
decide; they are draft vectors and no conformance class. A future vector set
for the rest pairs each refusal with a valid neighbour:

| Valid control | Refusal or invariant |
| --- | --- |
| A valid contract of profile `/1`, and a valid root and a valid child of profile `/2`, each read by a reader of both profiles | Fifteen members with the `/1` string and eleven members with the `/2` string refuse as `CONTRACT_PROFILE`. A `/2` object with a missing, additional, reordered or duplicated member among the four new ones refuses as `CONTRACT_ENCODING`. A reader of profile `/1` alone refuses every fifteen-member object as `CONTRACT_ENCODING`. |
| A valid child whose parent is a valid contract of profile `/2`, admitted through 6d and V5 | The same child presented with a parent of profile `/1` refuses as `NOT_DELEGABLE`. |
| A root under profile `/2` with a well-formed right of re-delegation | `depth` 1 without a notary refuses as `DELEGATE_NO_NOTARY`; each other malformed member refuses as `CONTRACT_DELEGATE`. |
| A certified child with `textual` `none`, `identical` and `within` | The same child without an attestation refuses as `CHILD_NOT_CERTIFIED`. |
| A certified child within its parent | One widening at a time, each with a valid attestation: actions, repositories, budget, window start, window end, agent, grantee, and an ordinal above the number of rows. Each refuses with its mechanical code and never as `CHILD_NOT_CERTIFIED`. Budget variants run in the spend profile only. |
| An attestation bound to this child and this parent | The attestation of a sibling, of another parent, of other contract hashes, or of another network or genesis refuses as `ATTESTATION_BINDING`. |
| A designated notary whose name yields the signing key | An undesignated notary, and a key that is not the name's current key, refuse. A notary key equal to the delegator's key, one equal to the delegatee's key, and a notary name equal to an executor's each refuse with their own code. |
| An attestation of exactly eighteen members | One that carries `budget` or `prev_attestation_id` refuses as `ATTESTATION_SHAPE` (case S1-9). |
| `textual` consistent with the hashes | `identical` over different hashes and `none` over a present text refuse as `ATTESTATION_BINDING`. |
| A request signed by the parent's grantee for this contract and ordinal | A request by another key, or for another contract or ordinal, refuses as `DELEGATION_REQUEST`. |
| Two links | A third link and a repeated id refuse as `CHAIN_DEPTH`. |
| On a node: a live parent, a confirmed anchor, an unspent notary seal | A spent parent seal refuses as `PARENT_NOT_LIVE` while the child's seal is unspent. A notary seal spent in the mempool refuses as `NOTARY_WITHDRAWN` while the child's seal is unspent. An unconfirmed anchor is pending and not refused. A reorganised tip refuses as `ATTESTATION_TIP`. |
| The same child certified again after a plain withdrawal | Certified again after a withdrawal for cause refuses at an executor that journalled the frame. For a verifier that did not observe it, see the second planned case below. |
| A verifier that journalled the notary's spend, after the spend is reorganised out of the chain | The withdrawn attestation still refuses as `NOTARY_WITHDRAWN`; admitting it again because the seal looks unspent is wrong. A fresh attestation of the same child by a named notary after that plain withdrawal is admitted. |
| An agent and a person as notary with the same attestation shape | Refusing because the notary is an agent, or because it is a person, is wrong. |

Sections 7.1 and 9.1 carry the cases of the pins and of the rows. Sections 3.4,
10.1 and 11.1 carry the cases of their Draft text, which is under decisions
that await the co-author's agreement.

Two further cases are planned as negative cases of a v4 vector set. Under the
rules in force both are admitted in the form that the table states. The verdict
that a vector must require follows the decision of section 10.1 once the
co-author agrees:

| Case | Today | Depends on |
| --- | --- | --- |
| Two children of one parent, both with ordinal 1, each certified by a different named notary | A second child for another grantee or executor refuses at V8 (section 9.1). Two children that fit the row are each admitted on its own bundle; what they spend together stays under the cap of the row at its executor (J1.3) | J2. Under section 10.1 the child whose notary is not the row's refuses as `NOTARY_NOT_DESIGNATED`. For the same row, the same notary and two different ids, each child is admitted on its own bundle, which is the known limit S1-K1 of section 9.1 |
| A child whose attestation was withdrawn for cause, presented with a fresh attestation by another named notary while the child's own seal is unspent, to a verifier that observed neither the frame nor a revocation | Admitted | J2. Under section 10.1 the child refuses as `NOTARY_NOT_DESIGNATED`. The case is S2-2; it tests designation only and runs beside the known limit S2-K1 |

## Open questions

### Gaps found in review

Two independent reviews of the design found five gaps in this LIP: the pool
across several notaries, a withdrawal for cause that does not reach a new
verifier, the notary bound by name only, the key an agent signs a child with on
v4, and scope text that is not enforced. Each has text under a decision of Ivan
Oparin, in the subsection that the table of decisions of 2026-11-13 and
2026-11-14 names. The co-author agreed to two of them on 2026-11-15: the rows,
which replace the pool (J1), and the pins of a notary's name (J3). The first
paragraph of each subsection states the gap with the case that shows it, and
each subsection says what its text closes and what stays open. The other three
gaps are not closed before the co-author agrees, and no gap is called closed
for a property that its subsection lists as open.

### Other open questions

- The child-seal key of section 11.2: its member name, its form among the v4
  bytes, whether a per-child key derived from a key named in the parent
  should replace one key for all children, and the co-author's agreement.
- The reservation ledger of section 11.1 (J4.4 (a) to J4.4 (g)): the
  co-author's answer, and with it the standing that the text gives the duty,
  that of J4. Earlier items are closed by the table of states and are no
  longer open: a held place for which the key was never used has one exit,
  the reconciliation of event 30, and without that proof stays held for
  ever; a request that ends with the key unused leaves the place held
  (events 12 and 13); a replay is answered only after the checks of J4.4
  (J4.4 (d)); the audit that is proof stands in the chain of the ledger
  and has its contract, and the audit beside it proves nothing
  (J4.4 (g)); an entry beyond the kept head is recorded as a hold before
  any other place is written (event 27); the proof of an unused key covers
  the whole life of the key (event 30); and each write is taken apart by
  its last durable component (events 8 to 11, 13 to 15 and 20 to 24).
  Open, each with its clause:
  - J4.4 (c): the second check between the reservation and the use of the
    key is in the text (event 12) and is no longer open. What stays is the
    window after it: a parent that closes between that check and the
    release costs its place, and the text gives no third check.
  - J4.4 (c) and J4.4 (f): whether the record should hold the canonical
    payload beside the intent. It holds the intent alone, so the ledger
    cannot show which child a held place reserved unless the payload is
    presented again.
  - J4.4 (d): what the service does with a record `signed` whose stored
    octets do not verify when they are read. The text gives a replay no
    verification on reading and gives `signed` no way back.
  - J4.4 (f), the reconciliation: how the operator is authenticated for the
    act, and whether the evidence standard of events 30 and 31 needs a
    second party. The text says who may act and on what evidence, and no
    more.
  - J4.4 (f), the marks: the form of a mark, of the kept head and of the
    place outside the ledger that holds them, which is the deployment
    profile for stores that must tell an empty store from a lost one, open
    for J1.4 as well. With it: where the kept head has to stand so that a
    restore of the whole host does not reach it. The text makes that the
    operator's duty and says that the service cannot find such a restore
    by itself; it names no place and no check.
  - J4.4 (f), the life of a key: the text holds for ever every place of a
    key that the ledger does not show from its making, a key from another
    custody and a key held at a genesis included, and takes no proof from
    outside the chain. Whether a later revision admits such a proof, for
    example a second ledger whose continuity a third party can show, is
    not decided; none is admitted now.
  - J4.4 (f), single custody: that a delegation key exists under one
    service and one ledger is a duty of the operator beside J4.6, and
    nothing at the service shows a second copy.
  - J4.4 (f), a mark of a use that stayed open: the text counts it against
    the proof of an unused key although the signer was not called under
    it. The looser reading would free that place.
  - J4.4 (g): which answers the operational audit holds beyond the two
    that the text names, its bound, and what an operator does when it
    cannot be written. No answer and no state of a place depends on it.
  - The codes: whether a request that is still served and a lost ledger
    should each have a code of their own beside `PLACE_HELD`; the interface
    of the service and the octets of its codes.
  - The entries of the ledger on the form of LIP-0025, and the vectors of
    the plan in section 11.1, of which none exists.
- Canonical vectors for the request and for the attestation, whose values have
  no fixed form yet, and a published checker for the vectors of profile `/2`
  (section 12).
- Whether a later decision that makes `spend` delegable keeps the profile
  string. A reader of this revision refuses a right of re-delegation that lists
  `spend` (D12), a reader after that decision would admit the same bytes, and
  LIP-0018 section 1 gives a change of meaning a new version.
- The code for a parent whose contract is no valid contract of either profile.
  Step V4 reads members of the parent's contract, and step V5, which comes
  after it, is the step that judges that contract.
- Kind 8186 is a draft allocation, with the same limits as kind 8185.
- The carriage of the request and of the bundle between agents, which follows
  the open carriage question of LIP-0013.
- The record that states the cause of a withdrawal. How a verifier that
  observed neither the withdrawal nor the revocation of the child learns of a
  withdrawal for cause is the subject of section 10.1.
- A quorum of notaries for sensitive resources; D9 fixes one of the set.
- A batched anchor and one seal per parent; D10 fixes one frame per
  attestation now.
- The coarse form of the stop coin, one coin for each notary and parent,
  as a future option (section 10.1): its cost and its limits.
- Narrowing the scope of a v4 child by text that a notary checks, possibly
  with keys. Both owners agreed on 2026-11-14 to leave it to the next
  revision (section 3.4); it is no part of the first version of v4, and
  nothing of it is defined.
- The v4 bytes of the right of re-delegation, the delegation key of section
  11.1 among them, are LIP-0020 section 11 since version 0.1.53. The v4
  bytes that carry a text (section 3.4) stay open. Version 0.1.55 proposes
  the v4 codes for a child whose chain, actions or window are wider than
  its parent allows (section 8.4, rows F8, F16 and F18).
- Eight points that section 8.4 leaves open, O1 to O8 of its table of open
  points: the order of the three blocs of the seal and the issuance against
  each other (row F21 and part 7.6 of F7); the code of a request that is
  not authenticated (A1); the codes, the inner order and the place of the
  checks of an invocation (E0); after the contract identifier, the
  code of a contract that is no valid contract of its v4 profile and the
  code of a contract that does not mirror the terms of its grant, with the
  preimage of the identifier, without which part (b) of F6 cannot be
  computed; the code of a journal of closures of a grant that cannot be
  read (part 7.4, F20); the place of a validated spend of a seal against
  the checks of the anchor and of the issuance (F21, part 7.6); what a
  side does with a finding of rules 2 and 6 to 8 of LIP-0020 W11.10, and
  with a finding of rules 4 and 5 outside the group and the range of the
  child, which waits for proposal Q1 of LIP-0026 (F13, rule T10); and the class under which a signing service
  judges `TIP_AGE` (F3). The vectors of section 8.7 are a plan, and none
  is generated.
- The owners' acceptance of sections 8.4 to 8.7, which are a proposal of
  version 0.1.55 and in force by no word of this draft, and the co-author's
  answer on them. The owners' line is asked on each choice that a row or a
  pair marks NEW. The codes: `CHILD_CONTRACT_DIFFERS` with the rule that a
  child binds the contract identifier of its parent (F5);
  `CONTRACT_NOT_PRESENTED` and `CONTRACT_ID` (F6, rule T1);
  `CONTRACT_SEAL_MISSING` and `CONTRACT_SEAL_UNAVAILABLE`, proposed by
  version 0.1.61 with the refusal required by decision C12 of
  LIP-0017 (2026-11-17; the co-author agrees and leaves the judgement to Ivan): open for the
  owners are the code names and retry marks, their place as part (c) of
  F6 (rule T11, pair Q28),
  and how a node is read for the confirmation and the script; no step,
  code or closure is stated for a contract seal that is confirmed as
  named and spent;
  `CHILD_NOT_LIVE`, with its use for a backdated window and the rule that
  an issuer signs a child whose window has not opened yet (F20, rule T3);
  `LIMIT_KIND_UNDEFINED` at the admission of a child (F17, rule T9). The
  readings: that the admission of a child judges rules 1 and 3 of LIP-0020
  W11.10 with the parent and rules 4 and 5 for the group and the range of
  the child alone, and nothing of another group (F1, F13, rule T10; the
  earlier requirement that a defect in a group which the child does not
  select refuses the child is withdrawn, and proposal Q1 of LIP-0026 is
  not decided here); the
  reading of a payload at an issuer (rule T7); that a refusal of the parent
  keeps the code of the rule that refused it, with `PARENT_NOT_LIVE` for
  four findings alone, and the order of the six parts of F7 (rule T8),
  without the Draft text of LIP-0008 section 5.2 (part 7.2); the
  split of CS2 between F12 and F21 and the parity octet (rule T5); the
  code `CHILD_BUDGET_OVER` for a floor that fails its profile (rule T9);
  that the documents stand before the observation (Q1, row F3); and the
  code `ROW_COIN_REQUIRED` for a coin that is spent when a child is to be
  signed (F22). The
  orders: the contract steps before the parent (Q5, Q6); the authentication
  of a request after the recipient of the child and not before the checks
  of a row (Q4); the keys (Q9, Q10); the actions and the window among the
  checks of a row (Q12); the coin before the attestation (Q16, rule T6);
  the steps of a request (Q20); the orders that the list of step 4 of
  LIP-0008 section 4 does not state: the issuer's name before the
  recipient's, the journal before the window and the window before the seal
  and the issuance, for the parent (Q22) and for the child (Q14, Q24); the
  predicate before the checks of an invocation (Q26); the bound of the
  ordinal before the rules of its group (Q27); the contract seal after
  the recomputed identifier and before the open part (Q28); and Q21,
  which puts the
  observation before the names and before the authentication of a request,
  a reading of LIP-0022 B6.1 against the numbering of step 3 of LIP-0008
  section 4, marked NEW in both recipient modes. The duties that section
  8.5 adds to the signing service inside step 1 of the order of one
  request: the observation as a step of its own (I3), the contract (I4),
  the recipient, the window and the seal of the child (I8), and the coin
  and the stop coin (I9); the places of I0 and I2; the anchor exception of
  I9, under which a coin that the confirmed issuance anchor of the child in
  the request has spent passes, so that a replay after publication reaches
  its record, with the anchor recognised by its two inputs; and that the
  repeat of step 6 has an observation of its own, in which that exception
  does not hold. And the four amendments of landed text: the sentence of
  section 11.1 (Q18); case S4-9 of section 11.2 (rule T5); step 3 of the
  order of one request, which refuses, with no code and a notice to the
  operator, a request that passed I9 by the anchor exception for a place
  with no record (event 39, case S4-30a); and step 6 of that order, which
  repeats I3 and I5 to I9 on a fresh observation, at the cost of one more
  read of the node for every signature. Since version 0.1.61 the repeat
  also makes part (c) of I4, the confirmed contract seal, between I3 and
  I5, and the enumerations of that step and of row I11 are amended in
  place for it, its principle unchanged (rule T11).
- Which party of the delegating side makes, for a child, the checks that
  LIP-0020 W7.5 to W7.9 ask of an issuer before a grant is signed. Section
  8.4 gives the signing service none of them.
- Whether "across owners" in rule J9.3 also covers the owner of the
  delegator. J9.2 tests the recipient of the child, and case S9-K1 admits a
  row without a certifier in a parent whose recipient belongs to another
  owner (section 8.3). LIP-0026 lists the same question.
- D4 places the pieces of this LIP after the first proof, as tools around v3
  that change no v3 byte. Question T1 of LIP-0013, whether such tools count
  as "v3 as is", has no explicit answer yet.
