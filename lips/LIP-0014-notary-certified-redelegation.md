# LIP-0014: Notary-certified re-delegation

- **Status:** Draft
- **Created:** 2026-11-12
- **Affects:** re-delegation (LIP-0008 section 12.6), the notary (LIP-0012),
  the trust contract and admission of LIP-0013, the action table of LIP-0005,
  the name value shapes of LIP-0010
- **Builds on:** LIP-0004, LIP-0008 section 12, LIP-0012 and LIP-0013

## Summary

Every child grant needs a notary's attestation, and every verifier still
checks each countable condition of the child itself. A child without a valid
attestation refuses as not certified, even when all its numbers are within the
parent's. A child that is wider than its parent in an action, a repository, a
budget or a window refuses with that mechanical reason, even when it carries a
valid attestation.

The parent grant names its notaries. Its signed right of re-delegation lists
one to four notaries by `id/` name, and each notary publishes its attestation
key in its own name. A notary is never the party that re-delegates and never
the party that receives the child.

On Grant v3 only the landlord's grant key signs a grant. The child is
therefore a grant that the landlord's signer issues on a signed request of the
parent's grantee. The parent binding lives in the contract, in the profile
`swarma-trust-contract/2`. No v3 byte changes.

Nothing in this LIP is implemented. It belongs to the second phase of Goal 1:
it follows the first proof, starts in shadow mode, and is no part of the first
proof.

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
LIP-0012.

The twelve directions are the owners'. Everything else in this LIP is the
draft's proposal and is not decided: the field names and bytes of the right of
re-delegation, of the contract profile and of the attestation, the refusal
codes and their order, the event kind 8186, the commitment formula of the
anchor, and the action `0x05`.

### Decisions pending

Five additions to the decisions above wait for the owners' decision. Their
rules stand in this LIP as Draft text, each in one subsection that is
marked "owner decision pending" with a label of this table. None of them is
adopted before the decision, and until then the text in force stays as it
is.

| Label | Touches | Direction of the Draft text | Until the decision |
| --- | --- | --- | --- |
| J1. Rows | D6 | The parent signs one row for each child it permits, with the executor, the grantee, the cap and the certifier of that child. The limit is a number of compartments. Section 9.1. | A pool that the children share, and lists of the agents and grantees a child may name (sections 2 and 9). |
| J2. Withdrawal for cause | D5 and D9; N6 and N8 of LIP-0012 | Each row names one notary, and only that notary certifies the row. It keeps one succession of seals for the row, and a cause counts only when the notary's signature covers its frame. Section 10.1. | Any named notary certifies, and a withdrawal for cause reaches only the parties that observed its frame (section 10). |
| J3. Notary identity | D3 | The parent pins each notary as LIP-0008 section 3 pins an issuer: by name, registration and owner key, with a signed checkpoint, and the attestation key in force must have been written by the pinned owner. Section 7.1. | A parent binds a notary by name only (section 7). |
| J4. The key that signs a child on v4 | K2 of the key map; LIP-0008 section 12.6 | The parent names one delegation key. On v4 only that key signs children, and it signs nothing else. Section 11.1. v3 does not change. | The parent's recipient key signs the child (LIP-0008 section 12.6). |
| J5. Scope text | R3 of LIP-0008 section 12.6; N2 of LIP-0012 | A child carries its parent's text unchanged, by hash, and narrows only members that a machine compares. An executor that cannot read refuses a grant with a text, and the owners choose what a text does to an effect. Section 3.4. | The notary judges a child's text against the parent's, and no step compares an instruction with the text (section 3.3). |

Three further decisions are pending in other LIPs: J6, a durable closure for
an owner-signed change of an issuer's name (LIP-0008 section 5.2); J7,
signing under a grant for each run (LIP-0013 section 3.6); and J8, the
signed invocation as the request of a verdict (LIP-0011 section 7).

The decisions are separate, with one dependency: section 10.1 needs the
rows of section 9.1. Where the Draft text of one decision uses another, it
says so. Sections 7.1 and 11.1 read the notary of the child's row where
rows exist. The delegation signer of section 11.1 identifies its caller
through LIP-0013 section 3.6 and reads the closure journals of section 10.1
and of LIP-0008 section 5.2, where those are adopted.

The cases of the pending subsections carry identifiers. In S3-1 the number
after S is the number of the decision, so S3-1 is the first case of J3. A
letter after the case number marks a variant, and K marks a known limit: a
case that the Draft text admits, and says so.

If J1 and J5 are adopted, a notary adds up no budget across siblings and
judges no text. It still keeps a record: one child for each row and, under
J2, one succession of seals for each row and its causes. An attestation
then gives a second signature by a party that the issuer chose (D8), a seal
that this party can spend, and a cause that its witnesses remember. D1 is
not reopened.

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

## 1. Terms

| Term | Meaning |
| --- | --- |
| Principal `L` | The `landlord_name` of the root grant. Every grant on one path has the same principal. |
| Parent `P` | A grant whose signed terms carry a right of re-delegation (section 2). |
| Child `C` | A grant whose signed terms bind the `grant_id` of `P` (section 3). |
| Delegator | The grantee of `P`, the holder of `P.grantee_key`. LIP-0008 section 12.2 requires that each link's audience is the next link's issuer. |
| Delegatee | The grantee of `C`, the holder of `C.grantee_key`. |
| Child signer | On v4, the delegator; section 11.1 holds Draft text, under a pending owner decision (J4), that names a delegation key instead. On v3, the landlord's grant key, acting on the delegator's signed request (section 5). |
| Notary `N` | A party named by `P`'s right of re-delegation whose attestation key signs the statement "child within parent" (LIP-0012). |
| Link | One signed grant on the authority path. A root grant is link 1 and its child is link 2. A third link refuses (LIP-0008 section 12.2). |

Under LIP-0013 a trust grant says that a grantee may direct an executor for a
principal. The orchestrator, executor and sub-executor of the motivation map
to two links:

| Link | Signed by, v3 / v4 | Grantee | `agent_name` | Meaning |
| --- | --- | --- | --- | --- |
| 1, root `P` | `L` / `L` | the orchestrator | the executor | The orchestrator may direct the executor within `P`. The right of re-delegation in `P` lets the orchestrator ask for children whose grantees and agents `P` lists. |
| 2, child `C` | `L` on the orchestrator's request / the orchestrator | the executor | the sub-executor | The executor may direct the sub-executor within `C`, which is within `P`. Closing `P` closes `C`. |

The executor of `C` differs from the executor of `P`. LIP-0008 section 12.2
allows that only because the issue capability names the child's grantee and
executor explicitly; section 2 carries those lists.

## 2. The right of re-delegation

A right of re-delegation is the signed member `delegate` of a grant's terms.
On v3 it is a member of the contract (section 3) and is bound through
`contract_sha256`. On v4 it belongs to the signed scope; this LIP defines no
v4 bytes. It has exactly these seven members in this order:

| Member | Type | Rule |
| --- | --- | --- |
| `depth` | integer | `0` or `1`. `0` means the grant carries no right of re-delegation. A child carries `0`. |
| `actions` | array of strings | The actions a child may receive: sorted, without duplicates, a subset of the grant's own `actions`. Non-empty when `depth` is 1. |
| `agents` | array of strings | The `id/` names a child may name as `agent_name`: sorted, without duplicates, each different from `landlord_name`. 1 to 16 entries when `depth` is 1. |
| `grantees` | array of strings | The x-only keys a child may name as `grantee_key`: sorted, without duplicates, 64 lowercase hex each. 1 to 16 entries when `depth` is 1. No wildcard. |
| `budget` | integer | Atoms that all children together may receive as `spend_budget`. Greater than 0 exactly when `actions` includes `spend`; at most 2100000000000000. It is separate from the grant's own `spend_budget` (section 9). |
| `max_children` | integer | 1 to 16 when `depth` is 1. The largest ordinal a child may carry. |
| `notaries` | array of strings | The `id/` names of the notaries whose attestation satisfies D1: sorted, without duplicates, 1 to 4 entries when `depth` is 1. |

When `depth` is 0 every array is empty and `budget` and `max_children` are 0.

A right of re-delegation with `depth` 1 and no notary is malformed and
refuses as `DELEGATE_NO_NOTARY`. Every other violation of this table refuses
as `CONTRACT_DELEGATE`. This is how D1 and D3 become a field check: a grant
cannot give the right to re-delegate without saying who certifies.

Only `depth` 1 gives the right. Ordinary action authority, possession of a
grant, management of an agent and an audience key give none (LIP-0008 sections
12.2 and 12.6).

In Goal 1 a right of re-delegation MUST NOT list `spend`, and its `budget` is
0 (D12). The budget members and the arithmetic of sections 6 and 9 stay in the
format for a later decision.

Two subsections hold Draft text, under pending owner decisions, that
changes members of this table. Section 7.1 changes `notaries` and adds
`checkpoint` (J3). Section 9.1 replaces `agents`, `grantees` and
`max_children` by rows (J1).

## 3. The contract profile `swarma-trust-contract/2`

Profile `/2` is profile `/1` of LIP-0013 with four more members. Its bytes
follow the encoding rules of LIP-0013 section 2.1. The object has exactly
these fifteen members in this order:

| # | Member | Rule |
| --- | --- | --- |
| 1 | `profile` | exactly `swarma-trust-contract/2` |
| 2 to 10 | `network`, `landlord_name`, `agent_name`, `grantee_key`, `actions`, `repos`, `spend_budget`, `not_before`, `not_after` | as in LIP-0013 section 2.1 |
| 11 | `scope_text_sha256` | `""`, or the SHA-256 of the scope text in 64 lowercase hex |
| 12 | `parent_grant_id` | `""` for a root, or the parent's `grant_id` in 64 lowercase hex |
| 13 | `ordinal` | `0` for a root, `1` to `16` for a child |
| 14 | `delegate` | the object of section 2 |
| 15 | `note` | as in LIP-0013 section 2.1 |

### 3.1. Which rules a reader applies

A reader that supports both profiles selects the rules by the member set of
the object, before it judges any value:

| Member names of the object, in order | Rules |
| --- | --- |
| The eleven of LIP-0013 section 2.1 | Profile `/1`: LIP-0013 section 2.3, unchanged |
| The fifteen of this section | Profile `/2`: the rules below |
| Any other set or order | Refusal as `CONTRACT_ENCODING` |

For the fifteen-member set the rules are those of LIP-0013 section 2.3 with
three differences. Rule 1 judges the canonical bytes against the fifteen
members of this section in their order. Rule 2 requires the profile string
of this section. Rule 3 also judges `scope_text_sha256`. Rules 4 to 7 are
unchanged, and two rules follow them:

| # | Rule | Refusal |
| --- | --- | --- |
| 8 | `ordinal` is 0 to 16, and `parent_grant_id` is `""` exactly when `ordinal` is 0. A contract with a parent has `delegate.depth` 0 | `CONTRACT_PARENT` |
| 9 | `delegate` follows section 2 | `CONTRACT_DELEGATE`, or `DELEGATE_NO_NOTARY` for `depth` 1 without a notary |

A member set and its profile string must agree. Fifteen members with the
string `swarma-trust-contract/1`, and eleven members with the string
`swarma-trust-contract/2`, both refuse as `CONTRACT_PROFILE` under rule 2 of
the selected rules. A reader that implements profile `/1` alone knows one
member set: it refuses every fifteen-member object as `CONTRACT_ENCODING`
under its rule 1.

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
agreement pending. This LIP does not yet say how profile `/2` applies the
rule; the paragraph below describes the text as the draft proposed it
before that decision.

The scope text is a separate document. Its exact octets hash to
`scope_text_sha256`, and it travels with the bundle. Text narrows only: like
the note of LIP-0013, it can never add an action, a repository, a budget or
time. It is meant to restrict what the structured members already allow. A
wrong judgement about text therefore cannot widen a mechanical limit. No
step of section 8 and no step of LIP-0013 section 3.4 compares an
instruction with the text. Whether an executor honours the text is left to
that executor. Section 3.4 holds Draft text for this, under a pending owner
decision (J5).

### 3.4. One text along the path, and what a text does to an effect

Owner decision pending: J5. Every rule of this subsection is Draft text.
Until the decision section 3.3 stands alone: a text narrows a grant, the
notary judges a child's text against the parent's once, at certification,
and no step compares an instruction with the text. Take a child whose text
limits the work to one component of a repository. An instruction that
concerns another component, within the child's actions and repositories,
passes every step of section 8 and steps 6e to 6g of LIP-0013. The notary's
`within` is a judgement as well: no verifier can recompute it.

The subsection does two things, and they answer different halves of that
case. A child carries the exact octets of its parent's text, by hash, and
narrows only members that a machine compares (J5.1 to J5.3, J5.6). A second
text then does not occur, and the value `within` is deleted. And the
subsection says what a text does at an executor (J5.4, J5.5, J5.7 to J5.9).
It does not make words enforceable: equal bytes are not an applied
restriction.

| Property | Closed? | For whom |
| --- | --- | --- |
| The child's text is not wider than the parent's | Yes, completely: no second text exists | Every verifier, one that starts later included |
| A grant with a text is never executed by an executor that cannot read | Yes, by J5.4 | Every executor that accepts profile `/2` |
| No record says that a text was checked | Yes, by J5.5 | Every reader of a record |
| An effect that lies outside the words is refused | No. This is the half of the case that the instruction for another component shows | Nobody; the owners choose what a text does to an effect |

The rules apply to contracts whose member set carries `scope_text_sha256`:
profile `/2` and its v4 counterpart. A reader MUST NOT synthesize the member
for a contract of profile `/1`, require it there, or treat `note` as a scope
text. Nothing is added to a grant or to an attestation. The executor's
configuration gains the setting `text`, which its owner sets to `none` or
`conduct`; absent means `none`. With `conduct` the executor is an agent, it
holds the exact octets, and it is told to treat them as a restriction. The
setting promises that a model considers the text. It does not promise a
qualified evaluator, and none is defined; a setting for one is reserved, as
LIP-0008 section 12.4 reserves its policy form. For a contract that carries
the member, the record of LIP-0013 step 7 gains `scope_text` with the values
`none` and `present`. For a contract of profile `/1` the record is
unchanged.

What a text does to an effect is the owners' choice among three rules, and
J5.5 has one branch for each:

| Option | May an automatic effect rest on a model's reading of words? | Cost |
| --- | --- | --- |
| (a) | Yes, for every action. An executor that is an agent applies the text. | The effect rests on the agent's reading, which can be wrong and is checked after the fact. The half of the case that concerns enforcement stays open and is reported as open. |
| (b) | No, for every action. | No predicate over a text exists, so every instruction, review, landing and payment under a grant with a text waits for the owner's confirmation. Grants meant for unattended work carry no text. |
| (c) | No for `land` and `spend`; yes for `instruct` and `review`. | The owner confirms each landing under a grant that has a text, bound to the exact revision (J5.9). Grants meant for automatic landing carry no text. A review under a text can still feed the gate of a landing under another grant. |

The proposal is (c). It follows exact inheritance to its end: authority that
a machine acts on sits in members that a machine compares. `land` and
`spend` are the actions that derive a v3 scope entry and act on a resource
(LIP-0013 section 2.2). `instruct` and `review` stay conduct, because their
object is itself words: no predicate over "assign this work" exists to fail
closed on. Under (c) a principal who wants automatic landings writes the
limit into `repos` and leaves the text empty, or puts explanation into
`note`, which carries no authority. A principal who wants words to limit a
landing gets a person's confirmation and not a model's reading. That matches
what v4 says of constraints: unknown semantics refuse, and no unimplemented
policy evaluator may stand in for the checks (LIP-0008 section 12.2).

| # | Rule | Refusal |
| --- | --- | --- |
| J5.1 | A child MUST carry its parent's `scope_text_sha256` unchanged: both empty, or both the same value. A child MUST NOT add a text where the parent has none and MUST NOT drop the parent's text. Equality is of octets; a different line ending or Unicode form is a different text. | `CHILD_TEXT_DIFFERS`, at V9, before the attestation is read |
| J5.2 | Every member of a child's contract is handled by exactly one row of the member table below. A member to which a profile assigns no row, and a member whose semantics the verifier does not know, refuses, also when child and parent carry equal bytes (LIP-0008 section 12.2). For each narrowing relation the profile states what the executor compares the member with at the effect. | The code of the member's row |
| J5.3 | The attestation's `textual` has the values `none` and `identical` only. D1 is unchanged: a child with equal text still needs its attestation. | An attestation that carries `within`: `ATTESTATION_SHAPE` |
| J5.4 | An executor whose `text` setting is `none` MUST refuse a grant whose `scope_text_sha256` is not empty, root or child, after step 6d of LIP-0013. An executor whose setting is `conduct` MUST hold the exact octets that hash to that value. | `TEXT_UNSUPPORTED`; without the octets `TEXT_UNAVAILABLE` |
| J5.5 | Common to every option: at an executor with `conduct` the agent applies the text, at step 9 of LIP-0013, as a restriction on what the structured members allow, and a text never adds. No admission step establishes that an effect lies within a text, and no record, receipt or attestation may report that it did. A confirmation is recorded as the owner's decision and never as a check of the text. The record of step 7 states `scope_text` as `none` or `present`. Then exactly one branch applies, by the owners' choice. | By the branch |
| J5.5 (a) | Nothing more. Every action under a grant with a text is conduct. | none |
| J5.5 (c) | For `land` and `spend`, and on v4 for every command that the action profile marks as an effect at a resource, the executor MUST NOT perform the effect automatically under a grant whose text is not empty. It holds the effect until its owner confirms it under J5.9, or it refuses. `instruct` and `review` are conduct. | `TEXT_NEEDS_APPROVAL` |
| J5.5 (b) | For every action, `instruct` and `review` included, a request under a grant whose text is not empty MUST NOT take effect automatically. An instruction is not given to a run as an instruction, a review verdict is not counted by a landing gate, and an effect at a resource is not performed, until one of two things has happened: the executor evaluated a predicate that a profile defines for that text, and it holds; or the executor's owner confirmed that request under J5.9. Otherwise the request is held or refuses. No predicate is defined in the first version, so under (b) every such request waits for the owner. Parsing, storing and certifying the grant are not blocked. | `TEXT_NEEDS_APPROVAL` |
| J5.6 | An inherited text is the root's. Its words refer to the parties and resources of the root grant, which the bundle carries (V2). A reader MUST NOT resolve them against the child's grantee, executor or run. | none; a rule of reading |
| J5.7 | A restriction that must hold at admission MUST be a structured member. The executor compares that member with the arguments actually passed to the privileged call, resolved immediately before the effect, when step 6 of LIP-0013 runs again. A plan, a title or a description of the arguments is not the arguments. | The code of the member, before the effect |
| J5.8 | Words of the delegator travel only as the body of an instruction (LIP-0013 section 3.3), which is data until admitted. Explanation that should bind nobody belongs in `note`. An operative text MUST NOT be treated as explanation without a new, signed and consented contract. | none of its own |
| J5.9 | A confirmation binds one operation and is used once. The owner's command MUST name the `event_id` of the request and the `grant_id` it was admitted under; the action; the resolved target, which is the repository and the ref for `land` and the payee for `spend`; and the content of the effect, which is the exact revision to be landed for `land` and the amount for `spend`. For `instruct` and `review` under (b) the event id fixes the body. Immediately before the effect the executor resolves the actual arguments again (J5.7) and compares them with the confirmation. If the revision, the target, the amount or the payee differs, the confirmation does not apply, and the effect is held again or refuses. A candidate that was rebased, regenerated or amended is another revision and needs its own confirmation. The executor records the use of a confirmation durably before the effect, and a second effect under it refuses. A retry of the same event is not a second use; it falls under the existing rule of one effect per event. A confirmation widens nothing: every structured check of the grant runs as it does without one. The wire form of the command is the deployment's; what it binds is not. | `TEXT_NEEDS_APPROVAL` |

The owner's command of J5.9 is the verified owner command that a2a already
uses (LIP-0013 section 3.5); the bytes of the confirmation record are open.

The member table of J5.2, for a child of profile `/2`:

| Member of the child | Relation to the parent | Refusal |
| --- | --- | --- |
| `profile` | fixed: `/2` in both | `CONTRACT_PROFILE`, `NOT_DELEGABLE` |
| `network`, `landlord_name`, and the grant's genesis | equal to the parent's | `SUBJECT_MISMATCH` |
| `agent_name`, `grantee_key` | allowed by the parent's right of re-delegation: listed (section 4), or under section 9.1 equal to those of the child's row | `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED` |
| `actions` | subset of `P.delegate.actions` | `CHILD_ACTIONS_WIDER` |
| `repos` | subset of `P.repos`, by exact bytes | `CHILD_REPOS_WIDER` |
| `spend_budget` | at most the parent's allowance: `P.delegate.budget` (section 4), or under section 9.1 the `cap` of the child's row | `CHILD_BUDGET_OVER` |
| `not_before`, `not_after` | nested in the parent's window | `CHILD_WINDOW_NOT_NESTED` |
| `scope_text_sha256` | equal to the parent's | `CHILD_TEXT_DIFFERS` |
| `parent_grant_id` | the dedicated check V3 | `PARENT_ID_MISMATCH` |
| `ordinal` | the dedicated check of its range; under section 9.1 it selects the row | `CHILD_ORDINAL` |
| `delegate` | fixed: `depth` 0 and every member empty | `CONTRACT_PARENT` |
| `note` | none; it carries no authority | none |

The parent's `delegate` members are read by their own steps (V4, V8, V9,
V12) and are not inherited. A child narrows through three relations,
subset, at most and nested, and through nothing else.

The fields that a principal may want to narrow map to members as follows:

| Field | v3 profile `/2` | Relation | v4 |
| --- | --- | --- | --- |
| Repository | `repos` | subset | the typed target of the action profile |
| Branch | none; `land` is the default branch | fixed by the action | a typed argument when a profile defines one |
| Action | `actions` within `P.delegate.actions` | subset | exact leaf commands (LIP-0008 section 12.3) |
| Recipients | the grantee and the agent that the parent allows | listed, or under section 9.1 equal to the row | the permitted targets of a typed limit |
| Amounts | `spend_budget` | at most | typed limits |
| Window | `not_before`, `not_after` | nested | height windows (LIP-0008 section 12.5) |

The steps change as follows. V9 gains one equality, of the two text hashes.
V14 checks `none` and `identical` against the two hashes. The bundle of V2
carries one text. Step 6 of LIP-0013 gains the refusals of J5.4 after 6d,
for contracts that carry the member; step 7 gains `scope_text`; step 9
gains the branch of J5.5 that the owners choose and the confirmation of
J5.9. Profile `/1`, its vectors and kind 8185 do not change.

J5.1 to J5.3 and J5.6 belong to the draft profile `/2` on v3 and to the
verbal terms of a child's contract on v4. For roots, J5.4, J5.5, J5.7 and
J5.9 are a precondition of enforcing mode for every executor that accepts
profile `/2`. An executor that accepted `/2` contracts and entered
enforcing mode for one-hop grants would otherwise admit a `/2` root with a
text and act on it with no text rule in force. An executor that accepts
profile `/1` alone cannot meet a scope text: profile `/1` has no text
member, and that reader refuses every fifteen-member object (section 3.1).

What stays open:

- **Whether an effect lies within the words.** Under (a) and (c) a text is
  applied to `instruct` and `review` by the agent that reads it, and by
  nobody else; under (a) that holds for every action. That is behavioural
  trust in the principal's own executor, checked after the fact by an
  owner, a moderator or an arbiter. Under (b) nothing takes effect on a
  model's reading alone; whether a confirmed request lies within the words
  is then the judgement of the person who confirmed, which is not a check
  either. No summary of this subsection may say that scope text is
  enforced.
- **A confirmation is a person's judgement.** It can be wrong. It is
  independent of the model that proposed the effect.
- **Reviews feed landing gates.** Under (c) a review stays conduct, also a
  review given under a grant with a text that lets a landing under another
  grant, one without a text, pass its gate. Under (c) it is therefore not
  true that no automatic effect anywhere rests on a model's reading. It is
  true of the landing and of the payment made under the grant that carries
  the text. An owner who wants more adds `review` to the confirmed actions.
- **Few narrowing members.** Profile `/2` narrows actions, repositories,
  the budget and the window, and the recipients through the parent's right
  of re-delegation. A limit on a branch, a path or a payee can be stated
  only in the root's text until v4 has a typed member for it.
- **J5.6 is a rule of reading** and cannot be tested mechanically.
- **The delegator cannot bind a narrower task in the grant.** It states the
  task in the instruction.

The owners decide four things with this text. The first is exact
inheritance itself (J5.1 to J5.3). It reverses no decision: R3 of LIP-0008
section 12.6, N2 of LIP-0012 and the decision that the notary performs the
textual check stand, and a different text no longer occurs. The second is
the choice among (a), (b) and (c) above. The third is whether profile `/2`
gains members for a branch, a path or a payee before it is fixed; the
proposal is to leave them to the typed arguments of v4, because each needs
an envelope tag and an effect check that LIP-0013 does not have. The fourth
is the staging of the root rule before enforcing mode, as the paragraph
above states it.

Four other designs were set aside. Keeping `within` keeps a value that no
verifier can recompute, under which a stolen attestation key certifies
children that exceed their parents in words. A narrowing clause that the
child appends needs a judgement of whether the clause narrows, and it puts
the delegator's text into the executor's scope. A policy language is
reserved and not adopted (LIP-0008 section 12.4). A qualified evaluator for
texts does not exist, and "qualified" has no definition yet.

Cases (owner decision pending: J5):

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S5-1 | Child and parent with the same non-empty text hash, the exact octets present, `textual` `identical` | A child with another text hash and an attestation that says `within` under the rules in force: `CHILD_TEXT_DIFFERS`, never `CHILD_NOT_CERTIFIED`. Variants that differ only in line endings, in Unicode form or in a final newline, each with its hash recomputed and the grant signed again, refuse the same way. In force this child is admitted with `within`. |
| S5-2 | Both without text, `textual` `none`; and both with the same text, `identical`; each with a valid attestation | Three separate negatives: a text added under a parent without one, and the parent's text dropped: `CHILD_TEXT_DIFFERS`; an attestation that carries `within`: `ATTESTATION_SHAPE`. A child with equal text and no attestation still refuses as `CHILD_NOT_CERTIFIED`. In force, adding and dropping are admitted with `within`. |
| S5-3 | An executor with `text` `none` admits a `/2` grant without a text | The same executor refuses a `/2` grant with a text, root or child: `TEXT_UNSUPPORTED`. In force it is admitted. The case covers the executor that cannot read and always runs beside S5-4. |
| S5-4 | An executor with `conduct` and the exact octets: the same `land` under a grant without a text is performed; under the grant with the text an `instruct` is admitted, under (b) after the owner's confirmation, and the record says `present` | The text says "only changes under docs/"; the instruction asks for a permitted `land` whose actual diff changes `src/auth.c`. Under (c), and under (b), no landing happens without the owner's confirmation: it is held, or refuses as `TEXT_NEEDS_APPROVAL`. Under (a) admission passes, and the vector records that verdict as the open half of the case. Under every option a record or receipt that reports the text as checked is wrong. In force the landing is performed. The test observes the effect, not the record. |
| S5-4c | Under (c) and (b): under the grant with the text, a `land` of revision `X`, whose diff touches only `docs/`, is held; the owner confirms it, naming the event, the grant, the repository, the ref and `X`; the landing is performed, once; the record states the owner's decision and `scope_text` `present`. An executor that always holds fails this control | Each a separate negative, with the effect observed: after the confirmation the candidate is replaced by `X'` with another diff: not performed; a confirmation that names another event, another repository or another ref: not performed; the same confirmation presented for a second landing: refused; the request asked again as a new event after the confirmation: not performed under the old confirmation. A record that says the text was checked is wrong in every variant. |
| S5-4b | Under (b) only: a text-bearing `instruct` that the owner confirmed under J5.9 is given to a run as an instruction; a review that the owner confirmed is counted by the gate | The same `instruct` with no predicate and no confirmation: held, or `TEXT_NEEDS_APPROVAL`, and no run receives it as an instruction. The same for a review verdict: the landing gate does not count it. Under (a) and (c) both are admitted as conduct, and the vector records that verdict. |
| S5-5 | The actual resolved arguments of the privileged call lie inside every structured member | Signed arguments that are narrow and a real call with wider arguments, including a target that changes between check and call: refused before the effect. v4 already requires it (LIP-0008 section 12.2); a test of the signed description alone is not this case. |
| S5-6 | A narrower action set, repository list and window, one at a time, with the identical text and a valid attestation | Each made wider, one at a time, refuses with its mechanical code and not with a certification code. Budget variants run in the spend profile only. |
| S5-7 | Members of the member table | Parent and child carry the same member of unknown semantics, not merely an extra JSON key: refused. |
| S5-8 | Before enforcing mode, the root rule. `text` `none`: a `/2` root without a text is admitted, and a `/1` grant with a `note` is admitted with its record unchanged | `text` `none` and a `/2` root with a text: `TEXT_UNSUPPORTED`. `conduct` with the octets missing or with octets of another hash: `TEXT_UNAVAILABLE`. |
| S5-9 | A child with the parent's text at another grantee and executor; the bundle carries the root's contract and text | A reader that resolves "you" or "my repository" against the child's parties breaks J5.6. The vector checks that the root's parties are present; the reading itself is reviewed, not computed. |

## 4. What a child binds

A child's contract binds the parent and stays within it. Each row is a
mechanical comparison against the presented parent `P`:

| Binding | Rule | Refusal |
| --- | --- | --- |
| `parent_grant_id` | Equals the `grant_id` recomputed from `P`'s presented signed bytes (LIP-0004 section 2) | `PARENT_ID_MISMATCH` |
| Depth | `P` has no parent, `P.delegate.depth` is 1, and no `grant_id` repeats on the path | `CHAIN_DEPTH` when `P` has a parent or an id repeats; `NOT_DELEGABLE` when `P.delegate.depth` is 0 |
| `network`, genesis, `landlord_name` | Equal to `P`'s | `SUBJECT_MISMATCH` |
| `agent_name` | Listed in `P.delegate.agents` | `CHILD_AGENT_NOT_ALLOWED` |
| `grantee_key` | Listed in `P.delegate.grantees` | `CHILD_GRANTEE_NOT_ALLOWED` |
| `actions` | A subset of `P.delegate.actions` | `CHILD_ACTIONS_WIDER` |
| `repos` | A subset of `P.repos`, compared by exact bytes | `CHILD_REPOS_WIDER` |
| `spend_budget` | At most `P.delegate.budget` | `CHILD_BUDGET_OVER` |
| Window | `P.not_before <= C.not_before < C.not_after <= P.not_after` | `CHILD_WINDOW_NOT_NESTED` |
| `ordinal` | `1 <= C.ordinal <= P.delegate.max_children` | `CHILD_ORDINAL` |
| `scope_text_sha256` | No mechanical rule beyond identity: equal values mean identical text. Different values need the notary's judgement | none |

Two subsections hold Draft text, under pending owner decisions, that
changes rows of this table. Under section 3.4 the two text hashes must be
equal (J5). Under section 9.1 a child must fit the row of its ordinal (J1).

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
agent, the actions, the repositories, the budget, the window, the ordinal and
the named notaries. A signature given over a hash alone does not meet this.

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
exactly these twenty members in this order:

| # | Member | Rule |
| --- | --- | --- |
| 1 | `profile` | `swarma-notary-attestation/1` |
| 2 | `kind` | `child-within-parent`. Profile `/1` has no other kind |
| 3 | `network` | equals `P`'s and `C`'s |
| 4 | `genesis` | 64 lowercase hex; equals the grants' `genesis` |
| 5 | `landlord_name` | equals `P`'s and `C`'s |
| 6 | `notary_name` | an `id/` name listed in `P.delegate.notaries` |
| 7 | `notary_key` | 64 lowercase hex, x-only; the attestation key that the notary's name yields (section 7) |
| 8 | `parent_grant_id` | the `grant_id` of `P` |
| 9 | `parent_contract_sha256` | the `contract_sha256` of `P` |
| 10 | `child_grant_id` | the `grant_id` of `C` |
| 11 | `child_contract_sha256` | the `contract_sha256` of `C` |
| 12 | `ordinal` | equals `C.ordinal` |
| 13 | `textual` | `none` when both contracts have an empty `scope_text_sha256`; `identical` when both have the same non-empty value; `within` when the values differ and the notary judged the child's text to be within the parent's |
| 14 | `mechanical` | `pass`: the notary's claim that it ran section 4 and the arithmetic of member 15 |
| 15 | `budget` | `{"pool":p,"before":b,"child":c,"after":a}`: `P.delegate.budget`, the total certified for lower ordinals, `C.spend_budget`, and `b + c` |
| 16 | `prev_attestation_id` | `""` when `ordinal` is 1; otherwise the id of the attestation for the ordinal one lower under the same parent |
| 17 | `notary_seal` | `{"txid":…,"vout":…,"script":…}`: the output whose spend withdraws this attestation |
| 18 | `tip_height` | the height of the tip the notary's node validated |
| 19 | `tip_hash` | the block hash at that height |
| 20 | `attested_at` | Unix seconds; a claim of the signer |

`textual` has no negative value: a notary that judges the child's text to be
outside the parent's signs nothing. Of the three values only `within` is a
judgement; a verifier checks `none` and `identical` against the two hashes.

A verifier never relies on `mechanical`. It runs section 4 itself. A `pass`
over a child that fails section 4 is evidence against the notary.

The signature is BIP-340 by `notary_key` over
`SHA-256("swarma-notary-v1" || attestation bytes)`. The 16-byte ASCII prefix
has no terminator or length, in the fixed-prefix style of LIP-0004 section 2.
The typed-hash plan of LIP-0008 section 8 may replace it before adoption.
`attestation_id` is the SHA-256 of the compact object
`{"attestation":…,"signature":…}`.

Two subsections hold Draft text, under pending owner decisions, that
changes this object. Section 3.4 removes the value `within` of `textual`
(J5). Section 9.1 removes the members 15 and 16 (J1).

### 6.2. When the notary signs

The notary signs after the child is issued and its issuance is confirmed:
`child_grant_id` exists only once the landlord has signed, and a v3 grant is
live only after its commitment is confirmed. A notary MAY read the draft child
contract before the landlord signs, to avoid a wasted issuance. That
pre-clearance binds nobody and is no attestation.

Before it signs, the notary runs section 4 like any verifier, checks the
arithmetic against its own record of the parent's earlier children, and reads
both scope texts when their hashes differ (LIP-0012 section 6).

### 6.3. Custody of the attestation key

A notary's attestation key is held by a key service that signs on request and
does not export the key. A key file that the notary's own process can read
does not meet this. The rule is the same for a notary that is an agent and
for one that is a person. The seal named by member 17 pays a key distinct from
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

Section 10.1 holds Draft text, under a pending owner decision (J2), that
puts the seals of one row into one succession.

## 7. Who the notary is

The parent grant says who certifies its children. `P.delegate.notaries` lists
the acceptable notaries by name, and a verifier accepts no other (D3). Because
the list is signed in the grant, it is fixed at issuance and agreed by the
grantee through the consent of LIP-0004 section 3. A change of the list needs
a new parent.

Each notary publishes its attestation key in its own `id/` name, in the
`swarma` shape that the amendment of LIP-0010 proposes:

```json
{"swarma":{"notary":{"attest":"<attestation key>"}}}
```

The notary rotates its key by updating that name with its name-owner key. The
grants that name it are not reissued. Attestations under the old key then
refuse (section 8, V12), and the notary signs them again under the new key.
The parent binds the notary by name only. It binds neither the registration
nor the owner of that name, so the same update is open to whoever holds the
name later. Section 7.1 holds Draft text that binds both (owner decision
pending: J3).

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

Accepted by Ivan Oparin on 2026-11-13 (J3); the co-author's agreement is
pending. The rules of this subsection add to D3. Until the co-author agrees
the text in force stands, under which a parent binds a notary by name only:
V12 accepts the key that the notary's name yields at check time. After a
transfer of the name, or after its expiry and a new registration, the new
holder publishes its own key under `swarma.notary.attest`. Its attestations
then pass V12 for every parent that names this notary, the attestations of
the earlier holder refuse, and nothing in the parent tells a verifier that
the name changed hands. This holds on v3 and on v4: a v4 grant binds the
registration and the owner key of its issuer's name (LIP-0008 section 3),
and nothing binds a notary's name.

Under this subsection a parent binds each notary as LIP-0008 section 3 binds
an issuer: by the exact name, the registration of that name and its owner
key. The attestation key stays free to change under the same owner. Two
members of the right of re-delegation (section 2) change. Each entry of
`notaries` becomes an object, and a member `checkpoint` is appended after
`notaries`:

| Member | Type | Rule |
| --- | --- | --- |
| `notaries` | array of objects | 1 to 4 objects when `depth` is 1, sorted by `name`, without a repeated name. Each object has exactly the three members `name`, `registration` and `owner`, as in the example below. |
| `checkpoint` | string | The hash of a block of the active chain, 64 lowercase hex; `""` when `depth` is 0. v3 only: on v4 the grant's committed recent block takes its place. |

```json
{"name":"id/acme-notary","registration":{"txid":"<64 hex>","vout":0},"owner":"<owner pin>"}
```

`registration` is the transaction and output that first registered the name.
`owner` is the owner pin, in the encoding that LIP-0008 section 3 will fix.
The rules constrain the history of the name from the output that was
current at the checkpoint block to the current output, and they call this
part of the history the stretch.

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

Step V12 of section 8 changes. After it found `notary_name` in
`P.delegate.notaries`, the verifier checks the checkpoint and walks the
name, then checks the writer, and only then reads the key. So
`NOTARY_CHECKPOINT`, `NOTARY_NAME_CHANGED`, `NOTARY_VALUE_UNAUTHORIZED` and
`NOTARY_HISTORY_UNAVAILABLE` come before `NOTARY_KEY`. None of the last
three records a closure.

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

One case stays open under these rules. A thief of the notary's name-owner
key writes a new attestation key under the same owner, and the rules pass,
because the bound owner key signed that update. The defence is cold custody
of the key, as for an issuer. Under sections 3.4 and 9.1 a notary whose key
is taken can widen no mechanical limit and judges no text. It can still
certify, withdraw and close a row; the pins settle none of that.

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

The owner-pin encoding and the script coverage of the owner proof are open
in LIP-0008 section 3. Until they exist an unsupported proof refuses under
J3.5, and byte vectors of profile `/2` wait for them.

The alternative before the owners is the name alone, as the first paragraph
describes it: no pin and no walk, and a notary's name that changes hands
passes on the right to certify.

Cases (J3). Each uses a verifier that starts after
the events and holds no journal. Under the name-only rule in force a
verifier reads no history, so it admits the refusals of S3-1 to S3-5b and of
S3-7:

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
child (D1).

Step 6d of LIP-0013 section 3.4 runs the binding of section 3.2, with the
rules that the contract's member set selects. A valid contract of either
profile therefore passes 6d, and a malformed one refuses there with its
contract code. The steps below follow 6d for a presented grant `C`. The
verifier stops at the first refusal; steps 6e to 6g then run against `C`.

| # | Step | Refusal |
| --- | --- | --- |
| V1 | `C`'s contract passed 6d. A contract of profile `/1`, and a contract of profile `/2` with an empty `parent_grant_id`, is a root: the remaining steps do not apply | none here; a contract that fails section 3 refused at 6d as `CONTRACT_ENCODING`, `CONTRACT_PROFILE`, `CONTRACT_FIELD`, `CONTRACT_PARENT`, `CONTRACT_DELEGATE` or `DELEGATE_NO_NOTARY` |
| V2 | The bundle holds, as complete objects, `P`'s presentation and contract, the delegation request (v3), the predecessors of a presented attestation, and each scope text whose hash is not empty; each object hashes to the value that names it | `DELEGATION_BUNDLE` |
| V3 | The `grant_id` recomputed from `P` equals `C.parent_grant_id` | `PARENT_ID_MISMATCH` |
| V4 | `P` has no parent and no id repeats; `P`'s contract has profile `/2` and `P.delegate.depth` is 1. A parent of profile `/1` carries no right of re-delegation | `CHAIN_DEPTH`, `NOT_DELEGABLE` |
| V5 | `P` passes the v3 check of LIP-0004 section 5 on the verifier's own node, with the pins taken from `P` and `P.grantee_key` as presenter, and then the binding of section 3.2 under the rules that `P`'s member set selects | `PARENT_NOT_LIVE` |
| V6 | Subject | `SUBJECT_MISMATCH` |
| V7 | The delegation request (v3) | `DELEGATION_REQUEST` |
| V8 | Agent and grantee are listed | `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED` |
| V9 | Actions, repositories, budget, window, ordinal | `CHILD_ACTIONS_WIDER`, `CHILD_REPOS_WIDER`, `CHILD_BUDGET_OVER`, `CHILD_WINDOW_NOT_NESTED`, `CHILD_ORDINAL` |
| V10 | An attestation is present | `CHILD_NOT_CERTIFIED` |
| V11 | The attestation has its canonical bytes; BIP-340 by `notary_key` verifies | `ATTESTATION_SHAPE`, then `ATTESTATION_SIGNATURE` |
| V12 | `notary_name` is listed in `P.delegate.notaries`; the current value of that name on the verifier's node yields `notary_key` | `NOTARY_NOT_DESIGNATED`, then `NOTARY_KEY` |
| V13 | Independence, in this order: `notary_key` differs from `P.grantee_key`; `notary_key` differs from `C.grantee_key`; `notary_name` differs from `P.agent_name` and from `C.agent_name` | `NOTARY_IS_DELEGATOR`, `NOTARY_IS_DELEGATEE`, `NOTARY_IS_EXECUTOR` |
| V14 | Members 2 to 5 and 8 to 12 equal this case; `textual` agrees with the two text hashes | `ATTESTATION_BINDING` |
| V15 | `budget.pool` equals `P.delegate.budget`; `budget.child` equals `C.spend_budget`; `after` equals `before` plus `child` and is at most `pool`. For ordinal 1, `before` is 0 and `prev_attestation_id` is empty. Otherwise each predecessor back to ordinal 1 has the same parent, an ordinal one lower, a designated notary and a valid signature, and its `after` equals the next one's `before` | `ATTESTATION_ARITHMETIC` |
| V16 | `tip_hash` is the active-chain block at `tip_height`; `tip_height` is at least the confirmation height of `C`'s issuance; `attested_at` is at most the verifier's clock plus 120 s | `ATTESTATION_TIP` |
| V17 | The anchor of section 6.4 is confirmed in the active chain and commits to this `attestation_id` | `ATTESTATION_ANCHOR` |
| V18 | `notary_seal` exists with the named script and is unspent, the mempool included, and the verifier's journal holds no withdrawal of this attestation (section 10) | `NOTARY_WITHDRAWN` |

V6 to V9 precede V10 on purpose. A child that is wider in an action, a
repository, a budget, a window or an ordinal refuses with that code even when
it carries a perfect attestation, as the control table of LIP-0012 requires.

In V15 a predecessor's seal is not checked. A withdrawn predecessor still
counts in the arithmetic, because a withdrawal does not return budget.

An unconfirmed anchor and an unavailable node are pending. The executor holds
and retries under step 8 of LIP-0013; it does not refuse the child as not
certified.

Draft text under pending owner decisions changes these steps, and each
subsection says how. Section 3.4 adds the equality of the two text hashes
to V9 and limits `textual` in V14 (J5). Section 7.1 adds the pins, the
checkpoint, the walk and the writer to V12 (J3). Section 9.1 puts the range
of the ordinal first in V8, compares the budget with the row's cap in V9
and removes V15 with the predecessors of V2 (J1). Section 10.1 compares
`notary_name` with the row in V12 and adds the row's closure for cause to
V18 (J2). Section 11.1 gives V7 its v4 counterpart, the child's signature
under the parent's delegation key (J4).

### 8.1. Why both are required

The verifier always re-checks because the check is deterministic: every input
is in the bundle or on the verifier's node, so two honest verifiers on one
chain reach one verdict. It also keeps the notary's power to the one thing
only a notary can do. If a verifier took the notary's word for subsets and
budgets, a stolen attestation key would widen any limit.

The attestation is required in addition, also when `textual` is `none` or
`identical`, for four reasons. The rule has no branch that a child can use to
skip certification. Every certified child has a seal that a party outside the
path can spend. No single verifier sees the siblings of a child; a notary
sees the children it certified itself and the chain it is shown, and its
attestations make the pool arithmetic checkable along that chain (section
9). With more than one named notary, a notary does not see a sibling that
another notary certified under the same ordinal; section 9.1 states the
case and holds Draft text for it, under a pending owner decision (J1). A
named party has recorded both contract hashes, the arithmetic and the tip
it saw.

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

## 9. Sibling budgets

The children of one parent together receive at most `P.delegate.budget` (D6).
LIP-0008 section 12.2 forbids that siblings each inherit another full copy of
a parent's budget, and it requires explicit signed partitions when the
executors keep independent journals. Children run at different agents, so:

- `P.spend_budget` is what `P`'s own executor may spend. `P.delegate.budget`
  is a separate pool for children. The principal signs both, and its exposure
  is their sum.
- Each child's `spend_budget` is its own partition, enforced by its own
  executor's cumulative ledger (LIP-0013 step 9).
- The sum over children is serialized at issuance: the signer reserves the
  ordinal and the amount durably before it signs (section 5). The notary keeps
  the same ledger per parent and certifies only when `after` is at most
  `pool`. Section 5 describes v3, where that signer is the landlord's. On v4
  the delegator signs the children, and the only ledger of the sum outside
  the delegator is a notary's.

A verifier checks the arithmetic of the chain it receives (V15). From one
bundle it cannot see a fork: two attestations with one parent and one ordinal
for different children. Such a pair, both signed by the notary, is complete
evidence of the notary's equivocation for anyone who holds both. A pair
signed by two different named notaries shows no fault of either notary. It
shows that the child signer used one ordinal twice, and no rule of this
draft brings the two attestations before one party (section 9.1). A pair
for the same child after a withdrawal is a new certification of that child
(section 10) and no fork.

A consumed ordinal and its budget stay consumed when the child is revoked or
its attestation withdrawn. LIP-0008 section 12.2 requires that reissuance
does not reset an ancestor's consumed allowance.

### 9.1. Rows: one compartment for each child

Decided by Ivan Oparin on 2026-11-14 (J1); the co-author's agreement is
pending. The decision changes how D6 and the member `max_children` are
read: the parent signs rows, and on v4 each row also pins a coin. Until the
co-author agrees the text in force stands, under which the pool is free and
no party sees every child of a parent. A
parent names up to four notaries, and any one of them is enough (D3, D9).
Each certifies against its own record of the parent's children (section
6.2). A parent has a pool of 100 and names notaries N1 and N2. Child A
takes 60 and is certified by N1; child B takes 60 and is certified by N2.
Both children carry ordinal 1, and both attestations carry `before` 0 and
`after` 60. Each child passes V9 and V15 on its own bundle, and the two
hold 120 together. Neither notary signed two attestations for one ordinal,
so the pair shows no equivocation of a notary. The case needs a child
signer that uses one ordinal twice. On v3 that is the landlord's signer,
which admits an ordinal once for a parent and reserves the amount before it
signs (section 5), so the case needs an error or a compromise of that
signer. On v4 the delegator signs the children and reaches the case alone.
In Goal 1 the pool is 0 (D12) and no amount is at stake; the same pair
still gives a parent with `max_children` 1 two children.

Under this subsection the parent signs one row for each child it permits.
A row fixes the executor, the grantee, the cap and the certifier, and a
child must fit the row of its ordinal. A total needs a party that sees
every sibling; a row needs none.

| Property | Closed? | For whom |
| --- | --- | --- |
| The number of compartments of authority under a parent, and the executor, grantee, cap and certifier of each | Yes | Every verifier, one that starts later included; it is a function of signed bytes |
| Consumption under one row never exceeds its cap, whatever documents exist | Yes, when `spend` is delegable | The row's executor, while the continuity of its ledger store is proved under J1.4; no deployment profile qualifies a store for that yet. A third party cannot read it from a bundle |
| At most one child object, one `grant_id`, is ever admitted for a row | On v3: no. On v4: yes on the active chain, by the coin of the row (J1.9) | On v3 it rests on the row's certifier (J1.6) and on the landlord's signer (section 5). On v4 every verifier reads the spend of the coin on its own node; the property does not hold across forks |

A second document for a row names the same grantee at the same executor,
is certified by the same notary and draws on the same row ledger, and every
member of it must fit the parent's delegable set. It cannot add a party, an
executor, an action, a repository, time or budget beyond what the principal
signed for that row. It can carry terms that the delegator did not choose
for that grantee, up to the envelope of the row. A row has exactly one
executor, and a grant is admitted only at the agent it names (LIP-0013 step
6b), so the verifier that matters for an effect under a row is that
executor.

The right of re-delegation (section 2) loses `agents`, `grantees` and
`max_children` and gains `slots`. Its members, in order, are `depth`,
`actions`, `budget`, `slots` and `notaries`, followed by `checkpoint` under
section 7.1.

| Member | Type | Rule |
| --- | --- | --- |
| `slots` | array of objects | One row for each child the grant permits: 1 to 16 rows when `depth` is 1, empty when it is 0. The ordinal of a row is its 1-based position. On v3 each row has exactly four members in this order: `executor`, an `id/` name different from `landlord_name`, which the child carries as its `agent_name`; `grantee`, an x-only key in 64 lowercase hex; `cap`, an integer of atoms from 0 to 2100000000000000; `notary`, the name of one entry of `notaries`. Two rows MAY name the same executor and grantee. |
| `budget` | integer | The pool. The caps MUST NOT sum to more than `budget`; the sum is an exact integer sum. Greater than 0 exactly when `actions` includes `spend`. |

```json
"delegate":{"depth":1,"actions":["instruct","review"],"budget":0,
"slots":[{"executor":"id/alexey-worker","grantee":"<64 hex>","cap":0,"notary":"id/ivanopcode-notary"}],
"notaries":[{"name":"id/ivanopcode-notary","registration":{"txid":"<64 hex>","vout":0},"owner":"<owner pin>"}],
"checkpoint":"<64 hex>"}
```

Line breaks are for display. A child carries
`{"depth":0,"actions":[],"budget":0,"slots":[],"notaries":[],"checkpoint":""}`.
Both values show `notaries` and `checkpoint` as section 7.1 defines them;
without that section the entries of `notaries` are names, and `checkpoint`
is absent.

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

| # | Rule | Refusal |
| --- | --- | --- |
| J1.1 | A right of re-delegation MUST fix, for every ordinal a child may carry, the executor, the grantee, the cap and the certifier. The caps MUST NOT sum to more than `delegate.budget`. | `CONTRACT_DELEGATE` |
| J1.2 | A verifier MUST first check that the child's ordinal lies between 1 and the number of rows, before it reads any row. It then requires the child to name the executor of that row as its `agent_name`, the grantee of that row, and a `spend_budget` of at most that row's `cap`. | `CHILD_ORDINAL`; then `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED`, `CHILD_BUDGET_OVER` |
| J1.3 | Before an effect that consumes a countable resource under a child, the executor MUST reserve the amount atomically in two cumulative ledgers: the child's, bounded by the child's limit, and the row's, keyed by `parent_grant_id` and ordinal and bounded by `cap`. If either reservation fails, the executor MUST refuse and MUST reserve nothing. These reservations are added to every other check and reservation that applies, and replace none: the check of one request in step 6g of LIP-0013, the child's v3 budget, and on v4 every ancestor link (LIP-0008 section 12.2). One request identity, the event id or the invocation's nonce, is charged once, also when it is retried. The row ledger draws on `delegate.budget` only; `P.spend_budget` stays the separate account of `P`'s own executor (section 9). | A failure of the row's reservation: `ROW_CAP_OVER` |
| J1.4 | The row ledger lives in a ledger store whose continuity is proved against a record outside the store. The contract of that store follows this table. | A lost store refuses every consuming effect under every row |
| J1.5 | A verifier MUST NOT rely on a statement of a notary or of a signer about a sum over siblings. The attestation carries no such statement. | none of its own |
| J1.6 | A notary MUST NOT certify two different children, two `child_grant_id` values, under one parent and ordinal, ever, also after a revocation or a withdrawal. It MAY sign again for the same child. Two attestations by one notary for different children of one parent and ordinal are complete evidence against it, as section 9 says today. The notary keeps a durable record for this. On v3 the landlord's signer still admits an ordinal once (section 5). | none at a verifier that holds one bundle |
| J1.7 | "Used" names three different facts, and on v3 none of them is public state about how many child objects exist: the reservation of the ordinal at the v3 landlord's signer; the notary's record of the child it certified for the row; and consumption in the row ledger, which is state of the row's executor, the verifier that consumes. Each is permanent: a revoked child, a withdrawn attestation and a reissue free none of them. A new child takes another row. | none of its own |
| J1.8 | A verifier, a receipt and a report MUST NOT state that a child is the only child of its row. On v4 they may state it for the active chain and for nothing wider (J1.9). | none of its own |
| J1.9 | v4 only. Each row pins one coin: an output that is confirmed before the parent is signed and that pays a key of the re-delegating side. The issuance of a child MUST spend the coin of the child's row in the transaction that carries the child's commitment, and a verifier checks that input on its own node. A row whose coin another transaction spent admits no child. The exclusivity holds on the active chain and not across forks: after a reorganisation that removes an issuance, another child can spend the coin on the new chain. | A v4 child whose issuance does not spend the coin of its row refuses. The code is fixed with the v4 bytes |

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

The subsection replaces these parts of the text in force: the members
`agents`, `grantees` and `max_children` of section 2; the attestation
members 15, `budget`, and 16, `prev_attestation_id`, of section 6.1, so
that the attestation has eighteen members; step V15 and the code
`ATTESTATION_ARITHMETIC`; the predecessor attestations in V2; the sentence
of section 8.1 that the chain of attestations makes the pool arithmetic
checkable; and the notary's ledger of the sum in section 9. The notary's
own record stays and is relied on: one child for each row (J1.6).

The steps change as follows. V8 checks the range of the ordinal first and
then `agent_name` and `grantee_key` against the row. V9 compares
`spend_budget` with the row's `cap`. Step 9 of LIP-0013 makes the
reservations of J1.3. The signer's display of section 5 adds the row's cap
and certifier. On v3 these are members of the draft profile `/2`. No v3
grant byte, consent rule or `rental.Check` rule changes; a `/2` contract
has other bytes and another hash than a `/1` contract, as every new
contract does. Under D12 every cap is 0 and `spend` is not listed, so J1.3
and J1.4 are dormant in Goal 1.

What stays open:

- **One child object for each row, on v3.** A second document for a row
  exists if the row's certifier breaks J1.6 or the landlord's signer fails.
  A verifier that starts later admits it. It stays inside the envelope of
  the row.
- **One child object for each row, on v4, across forks.** The coin of J1.9
  admits one issuance for a row on the active chain. After a reorganisation
  that removes that issuance, a thief of the delegation key (section 11.1)
  can issue another child that spends the coin on the new chain. The
  decision accepts this boundary.
- **The key of a row's coin.** The decision has the coin pay a key of the
  re-delegating side. The delegation key of section 11.1 signs child grants
  and no transaction, so the coin needs another key of that side, or that
  rule changes. Which key it is, and who funds the coin, is open and is
  fixed with the v4 bytes.
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
- **Size.** Sixteen rows with the longest names that the syntax allows do
  not fit 8192 bytes; the contract then refuses under rule 1 of LIP-0013
  section 2.3. Real serialized fixtures decide the sizes.

What the limit is was a choice among four options:

| Option | What it gives | Cost |
| --- | --- | --- |
| (a) The limit is a number of compartments | The first two properties of the table above. Two attestation members and one verifier step go away, and the notary adds up no budget. | A new parent to move budget or to add a child. One child means one compartment; one grant for each row rests on the notary and, on v3, on the signer. |
| (b) (a) with an occupancy record at the row's executor: the executor binds a row to the first child id it admits, also when every amount is 0 | One child grant for each row at the only place where the row has an effect, for what that executor itself admitted and while its store was continuous. It is no statement that no other document exists. | The store of J1.4 is needed already in Goal 1. A lost record ends the row. The first document presented wins, so a wrong first document costs a row. |
| (c) (a) with a pinned coin for each row that the child's issuance must spend | One child grant for each row on the current chain, for every reader, auditors included. It is exclusivity on the current chain, not across forks. | One reserved, confirmed output for each row before the parent is signed; a check of issuance inputs that no v3 verifier makes today (LIP-0004 section 4); and the holder of the coin's key can void an unissued row by spending its coin. |
| (d) The free pool of the text in force | The delegator chooses freely. | The case of the first paragraph stays. |

Ivan Oparin decided on 2026-11-14: option (a) for profile `/2` on v3, with
the limit named a compartment limit, and option (c) for v4, where the
delegator signs children alone. On v4 the coin of a row pays a key of the
re-delegating side (J1.9). The decision accepts the boundary of (c): one
child for each row holds on the active chain only. Options (b) and (d) are
not taken. D7, D10 and D12 are unchanged, and the landlord's reservation on
v3 is kept.

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

Cases (J1). A suite that feeds a contract with rows
to a parser of the text in force and counts the rejection proves nothing;
each case names the fixture of the old shape that is its equivalent. Cases
of the spend profile are no part of the Goal 1 suite (D12).

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S1-1 | Rows 1 (`id/x`, `G1`) and 2 (`id/y`, `G2`), caps 0; a child of each row, certified by its row's notary, is admitted | One binding changed at a time: a child with ordinal 1 that names `id/y`, and one that names `G2`: `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED`, each with a valid attestation and never `CHILD_NOT_CERTIFIED`. In force both are admitted: with `agents` [`id/x`,`id/y`] and `grantees` [`G1`,`G2`] every combination is listed. |
| S1-1m | Spend profile: caps 60 and 40, pool 100; children of 60 and 40 | A child of 60 under row 2: `CHILD_BUDGET_OVER`. In force it is admitted: 60 is at most the pool, and the arithmetic of one bundle closes. The case is not 60 and 60 against 100 in one chain of attestations, which V15 refuses in force. |
| S1-2a | One row, pool 0; one child with ordinal 1 | A second child with ordinal 1 for another grantee or executor refuses at V8. For the same grantee and executor with another named notary it refuses as `NOTARY_NOT_DESIGNATED` under section 10.1. In force both are admitted. |
| S1-2b | A child with ordinal 1 | Ordinal 0 and an ordinal above the number of rows refuse as `CHILD_ORDINAL`, before any row is read, without a crash and without a code that names the agent. In force `max_children` refuses them. |
| S1-K1 | One row with cap 0; child `C1` certified by the row's notary | A known limit on v3: a second child `C2` of the same row, with another id, also certified by that notary in breach of J1.6, shown to a verifier that never saw `C1`, is admitted, and the vector records this verdict. On v4 the issuance of `C2` cannot spend the coin of the row (S1-10). |
| S1-3 | Spend profile: two documents of row 1, cap 60; 30 spent under the first; exactly 30 more under the second succeeds | One atom more refuses as `ROW_CAP_OVER`; both ledgers are read afterwards, and the child's ledger holds no partial reservation. The second document carries a valid attestation, so the refusal is the ledger's. A ledger for each child admits 60 under each. |
| S1-4 | Caps that sum to exactly `budget`, and caps below it; each row with its four members and a listed notary. Two rows that name the same executor and the same grantee, each with its own ordinal and cap, are a valid parent, and a child of each row is admitted under its own ordinal; a reader that refuses the repeat fails this control | Four separate negatives: a larger sum; a row with a missing member; a row with an extra member; a row whose `notary` is not in `notaries`: each `CONTRACT_DELEGATE`. The sum is checked at the largest allowed values without overflow. |
| S1-5 | Spend profile, at the store: first use of a row in a store whose continuity check passes; after 40 is spent and the child revoked, a restart with the store intact leaves 20. A crash after the store write and before the outside write: no effect was performed, and after the restart the reservation is charged once and the same request identity completes | The same row after the store was lost, created anew or rolled back: no `spend`, no first use. An unreadable store refuses and reserves nothing. Each a separate negative: a reservation of 40, the effect, a crash, and a restore of the backup taken before the reservation: lost store, no further `spend`; a rollback of the ledger alone; a rollback of the ledger together with every file beside it on the store's host; a missing or unreadable outside record; a replica with an older write token; a recovery by charging in which the list of rows was lost with the store: a row of a parent that existed before the loss gets no first use. |
| S1-5-ABA | Spend profile, at the store: a restart with the image that was actually committed at position 1 spends only the true remainder of 20; and a transition that is pending on the history that the outside record still holds completes once, without a second charge and without an effect before the outside write | Two histories at one position. An image is kept from the window between the store write and the outside write; the store is restored to the image before it; a different reservation commits at the same position; the first image is restored: the executor refuses before any further consuming reservation or effect, although the positions are equal. The planted defect `continuity-counter-only` keeps the presence of the outside record, its identity, the order of writes and the fencing, and drops the comparison with the exact committed history; a suite must catch it with this negative. An implementation that always refuses must fail the two controls. |
| S1-6 | Spend profile, at the store: 40 and then 20 against a cap of 60, from two real callers | Two replicas race 40 and 40 through their public entry points: the committed total is at most 60, and the refused caller holds no reservation. With the shared store unavailable neither succeeds. |
| S1-7 | The same child with a new valid attestation after a plain withdrawal spends the true remainder | The consumption before the new attestation is still charged; a new attestation id, signature or run does not reset it. Section 9 already forbids the reset. |
| S1-8 | Goal 1: every cap 0 and no `spend` | A positive cap or a listed `spend` refuses as `CONTRACT_DELEGATE`. D12 already forbids it; the case shows no new closure. |
| S1-9 | An attestation of exactly eighteen members, with a valid signature and bindings, admitted | An attestation that carries `budget` or `prev_attestation_id` refuses as `ATTESTATION_SHAPE`. The form of twenty members is valid in force and invalid after; the case proves the change of shape, not a protection. |
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

After a plain withdrawal the same child may be certified again by a notary
that `P` names, with the same ordinal and the same arithmetic (D5). A
withdrawal for cause blocks that. The notary marks it in the transaction that
spends the seal, with one LIP-0005 frame:

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
Draft text for it, under a pending owner decision (J2).

### 10.1. One certifier for each row, and the withdrawal for cause

Decided by Ivan Oparin on 2026-11-14 (J2); the co-author's agreement is
pending. The decision touches D5 and D9 and uses the rows of section 9.1.
On v3 each row has one certifier, and D5 is narrowed. On v4 each row also
names a stop coin of its notary, from the first version. Until the
co-author agrees the text in force stands, under which a withdrawal for
cause reaches only the parties that observed its frame.
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
| J2.7 | v4 only: the stop coin of a row. The row gains a member `stop`, an outpoint. The output exists and is confirmed before the parent is signed, so the row's notary takes part in the parent's issuance. It is an output that the notary alone can spend, given like a notary seal by transaction, index and script (section 6.1, member 17); it needs no new spending condition, and it pays a key of the notary that is not its attestation key (section 6.3). A verifier requires `stop` to exist with the named script and to be unspent, the mempool included, and journals a validated spend as it journals a seal spend. The notary ends a row for cause by spending `stop`; the `0x05` frame in that transaction is evidence and no longer the trigger. A plain withdrawal leaves `stop` alone. With the stop coin the third property of the table above does not depend on the succession of J2.3 (a). The output is bound by outpoint, so a rotation of `attest` does not touch it, and the notary must keep its spending key for the life of the parent. If the notary loses that key, the row can no longer be ended for cause, and the stops of the v3 form are what remains. After a reorganisation that removes the output the row refuses until the output is confirmed again. The fee of that spend is the notary's own and must not hang on a coin that somebody else can spend first, for the reason LIP-0008 section 5.2 gives for an issuer's break. A profile in which more than one notary may certify a row, or in which a verifier that starts later must refuse after a cause, MUST have such a state; without it a profile MUST NOT offer either. | A spent `stop`: `ROW_CLOSED_FOR_CAUSE` for every child of the row, whatever seal an attestation names, in every view that holds that spend |

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
no closure for cause of this parent and ordinal. On v3 no new read is added; on v4 the verifier also reads the stop coin of
the row. One seal may still serve every attestation of a parent
(section 6.4): a successor may serve the rows that its predecessor served,
and a spend for cause of a shared seal creates no successor for the row it
closes and may create one for the others.

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
| Agents that sign grants | None | The delegator signs the child with the parent's recipient key (LIP-0008 section 12.6). For a parent issued by name that is the key the name lists at admission, so a child signed with an earlier key refuses (LIP-0008 sections 3.1 and 12.2). Section 11.1 holds Draft text, under a pending owner decision (J4), that replaces this rule with a delegation key named in the parent |

Depth stays at two links (D7). Work below a child's executor is covered by a
new root grant from the principal.

Each party pays for its own effects under D11. A payment for a notary's seal,
anchor or fee from an owner's funds follows that owner's spending rule; where
the owner approves each spend, the payment is approved per spend.

### 11.1. The delegation key on v4

Owner decision pending: J4. Every rule of this subsection is Draft text. It
replaces the rule in force for the link below an issue capability. Under
that rule an agent that its parent names by name signs child grants with
the key that also signs its messages. v3 does not change.

By the rule in force the parent's recipient signs the child (LIP-0008
section 12.6): the grantee key, or for a parent issued by name the key that
the name yields at admission. An agent's name yields one key, its Nostr key
(LIP-0010), and the gateway of the agent's host holds that key (key map).
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
Its bytes are fixed with the v4 bytes.

| # | Rule | Refusal |
| --- | --- | --- |
| J4.1 | An issue capability MUST name one delegation key. A v4 child MUST be signed by the delegation key of the capability it commits to. | A child signed by any other key, the parent's request key and a key that the grantee's name lists for a channel included: `CHILD_SIGNER` |
| J4.2 | For LIP-0008 section 12.2 the authenticated issuer of the link after an issue capability is that capability's delegation key. The delegation key signs child grants and nothing else: no invocation, no envelope, no consent, no name operation, no transaction. The request key of the same grant MUST NOT sign a child grant; under LIP-0013 section 3.6 what it may sign is the closed list of J7.5. | A child signed by the request key: `CHILD_SIGNER` (J4.1) |
| J4.3 | Keys are compared as secret authorities, by their 32-byte x coordinate: an x-only key equals a compressed key with that coordinate under either parity byte. | none of its own |
| J4.3 (a) | Parent checks, on the bytes and pins of `P`, when `P` is validated. The delegation key MUST differ from the issuer's grant key; from `P`'s request key, when `P` names its recipient by key, or from the owner key of the recipient's name, when `P` names its recipient by name; from the owner key bound for the issuer's name; from the owner key pinned for each notary (section 7.1, under J3); and from the key of `P`'s own seal, taken from its endorsement (LIP-0008 section 11.1). | `P` is unusable as a parent, and every child refuses as `DELEGATE_KEY_REUSE` |
| J4.3 (b) | Child checks, at every admission of a child `C`. The delegation key MUST differ from every channel key that the name of `P`'s recipient yields at that admission, when `P` names its recipient by name; from the attestation key that the notary of `C`'s attestation, under section 10.1 the notary of `C`'s row, yields at that admission; from the key of `C`'s seal; and from `C`'s own recipient key, or from the owner key of `C`'s recipient name. Another notary of the parent is not read (J3.7). | That admission refuses as `DELEGATE_KEY_REUSE` and records no closure |
| J4.3 (c) | Where an owner pin is not one key, and for keys that no verifier sees, such as funding and fee keys, the separation is a custody duty of J4.4. It is not checked on the wire. | none at a verifier |
| J4.4 | The delegation key is held by a signing service of the party that consented to the parent as its recipient: for a recipient by name, the operator who holds that name's owner key; for a recipient by key, the operator of that key's key holder. In both modes the service runs outside the delegating agent's OS user and outside the service that holds the request or channel key, and it holds no name-owner key, seal key or funding key. Before it signs, the service MUST take the complete child and, on its own node, check that `P` is live under every admission rule, its closure journals included, which under LIP-0008 section 5.2 and section 10.1 hold the closures of an issuer's name and of a row; that under section 9.1 the child's row exists, that the child fits it and that the row is not closed for cause; and the comparisons of section 4. It computes the digest itself (LIP-0008 section 8) and MUST NOT sign a digest that a caller supplies. It MUST identify the caller and sign only for a caller that its operator listed for delegation under `P`; under LIP-0013 section 3.6 the caller is a run, and the list is the `delegate` list of that run's origin. Possession of the messaging key is not the authority to ask. | No signature exists |
| J4.5 | What a name update does to children. A rotation of the delegating agent's channel key under the same owner, a renewal and a change of host stop no child. An update that makes a channel key equal to the delegation key refuses children for as long as it holds (J4.3 (b)). A change of the name's owner refuses a parent by name and with it every child (LIP-0008 section 3). A parent by key is not portable through any name. | `DELEGATE_KEY_REUSE` while a channel key equals the delegation key; `PARENT_NOT_LIVE` for every child after a change of the name's owner |
| J4.6 | Replacing the delegation key requires a new parent. A move of custody that cannot keep exclusive control of the key MUST NOT begin before the old parent is closed. | none at a verifier |
| J4.7 | v3 is unchanged: the landlord's grant key signs the child on a kind-8186 request signed by `P.grantee_key` (section 5). A delegation key gives nothing on v3. | none new |

A verifier repeats the checks of J4.4 on the parent and on the child at use.
The checks of the signing service spare a wasted child and bound a thief of
the caller's channel.

Where V7 checks the delegation request on v3, a v4 verifier checks the
child's signature under the parent's delegation key, the parent checks of
J4.3 (a) with `P`, and the child checks of J4.3 (b) with `C`.

A thief of the delegation key endorses a seal of its own, so the delegating
operator has no seal of such a child to spend, as the owner of a leaked
grant key has none (LIP-0008 section 5.2). Three things stop such a child:
the principal spends the parent's seal; a named notary refuses to certify
it, or withdraws its attestation; and, for a parent by name, the delegating
operator changes the owner of the agent's name. Under sections 9.1 and 10.1
the notary is the row's, and it certifies one child for the row. The right
of re-delegation bounds what the thief can sign to the grantees and
executors that the principal signed (section 2), under section 9.1 to the
rows. A closure that a verifier never observed is not known to it.

The rules leave four limits. Different keys do not prove different
custodians: whether the delegation key and the messaging key are in
different hands is established by the owner's approval of a deployment, not
by a verifier. The signing service of J4.4 is a hot service, and a second
OS user on a host whose administrator is not the operator is no separation
from that administrator. The signing service cannot tell what the agent's
model intends from what the agent's host does; it can bound what it signs.
And the delegating operator loses the stop it has under the rule in force,
a rotation of the channel key; it keeps the change of the name's owner.

The owners choose between this text and four alternatives. Keeping the rule
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

Two further choices of the owners come with this decision. The first is
whether the delegation signer needs a person for each signature, as the key
map requires of a grant key, or signs unattended inside the parent's right
of re-delegation. The proposal is unattended signing, because the right of
re-delegation and the notary bound what the signer can sign; presence stays
at the principal's grant key (K5 of the key map). It is the same question as
the presence rule under LIP-0013 section 3.6 and should get the same answer.
The second is whether the parent also names the key that every child's seal
pays, held by the delegating operator apart from the signer, so that the
operator can spend the seal of a child that a thief of the delegation key
signed. That costs one more key and a change of the endorsement rule of
LIP-0008 section 11.1 for children; the proposal is to decide it with the v4
bytes, together with the row-ending output of section 10.1 (J2.7).

Cases (owner decision pending: J4). All are v4 cases; no v4 implementation
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

- **A stolen or careless attestation key** certifies children that exceed
  their parents in words. It cannot widen an action set, a repository list, a
  window or a child's own budget, because every verifier enforces those
  itself. The sum over siblings is different: no verifier sees it, and it
  rests on the child signer's reservation and on the attestation chain
  (section 9). The notary's name-owner key rotates the attestation key, which
  makes every attestation under the old key refuse at once.
- **An unavailable notary** stops new children and new certifications.
  Certified children keep working: admission reads the seal and the anchor,
  not the notary's service. Naming up to four notaries bounds the outage. It
  also gives the pool more than one ledger: each notary certifies against its
  own record (section 6.2), and two notaries can each certify a child under
  one ordinal. Section 9.1 holds Draft text for this case, under a pending
  owner decision (J1).
- **A withdrawal for cause does not reach everyone.** It binds the parties
  that observed its frame. Another named notary can certify the child again,
  and a verifier that starts later admits it. Section 10.1 holds Draft text
  for this case, under a pending owner decision (J2).
- **The notary's name can change hands.** After a transfer, or after an
  expiry and a new registration, the holder of a notary's name publishes its
  own attestation key and can certify under every parent that names it.
  Section 7.1 holds Draft text for this case, under a pending owner decision
  (J3).
- **Scope text binds nobody at admission.** The notary judges the text once.
  No admission step compares an instruction with it. Section 3.4 holds
  Draft text for this case, under a pending owner decision (J5).
- **On v4 an agent's messaging key signs its children**, by the rule in
  force. Section 11.1 states what follows from that and holds Draft text,
  under a pending owner decision (J4), that replaces the rule.
- **Self-certification.** V13 refuses a notary key equal to the delegator's
  or the delegatee's key and a notary name equal to an executor's. Different
  keys do not prove different parties; the control is that the issuer, not the
  delegator, names the notary.
- **Replay onto another child.** The attestation binds both grant ids, both
  contract hashes, the ordinal, the network, the genesis and the principal.
  Two children with identical contracts still have different ids, because each
  grant has its own seal.
- **A v3 reader that ignores the contract** does not see a closed parent. The
  joint revocation transaction of section 10 closes the children for it.
- **A reorganisation that drops the attested tip** makes V16 refuse until the
  notary signs again against the new chain.
- **The notary learns both contracts and both scope texts.** The anchor
  carries hashes only. A deployment that cannot disclose them uses issuance by
  the operator's signer without a child (LIP-0008 section 12.6, R5).
- **Cost.** A certified child adds one anchor transaction and one seal output
  on the notary's side to the child's own issuance. No size or fee of it has
  been measured.
- **Disputes.** The attestation is a signed statement and no proof (LIP-0012
  section 6). Evidence open to any holder: both contracts and texts, the
  chain of attestations, the anchor, an equivocating pair, a `mechanical`
  `pass` over a child that fails section 4, and a withdrawal for cause.
  Judging a dispute stays with the arbiter of a contract.

## Conformance impact

None while this LIP is a Draft. A future vector set pairs each refusal with a
valid neighbour:

| Valid control | Refusal or invariant |
| --- | --- |
| A valid contract of profile `/1`, and a valid root and a valid child of profile `/2`, each read by a reader of both profiles | Fifteen members with the `/1` string and eleven members with the `/2` string refuse as `CONTRACT_PROFILE`. A `/2` object with a missing, additional, reordered or duplicated member among the four new ones refuses as `CONTRACT_ENCODING`. A reader of profile `/1` alone refuses every fifteen-member object as `CONTRACT_ENCODING`. |
| A valid child whose parent is a valid contract of profile `/2`, admitted through 6d and V5 | The same child presented with a parent of profile `/1` refuses as `NOT_DELEGABLE`. |
| A root under profile `/2` with a well-formed right of re-delegation | `depth` 1 without a notary refuses as `DELEGATE_NO_NOTARY`; each other malformed member refuses as `CONTRACT_DELEGATE`. |
| A certified child with `textual` `none`, `identical` and `within` | The same child without an attestation refuses as `CHILD_NOT_CERTIFIED`. |
| A certified child within its parent | One widening at a time, each with a valid attestation: actions, repositories, budget, window start, window end, agent, grantee, ordinal 0 and an ordinal above `max_children`. Each refuses with its mechanical code and never as `CHILD_NOT_CERTIFIED`. |
| An attestation bound to this child and this parent | The attestation of a sibling, of another parent, of other contract hashes, or of another network or genesis refuses as `ATTESTATION_BINDING`. |
| A designated notary whose name yields the signing key | An undesignated notary, and a key that is not the name's current key, refuse. A notary key equal to the delegator's key, one equal to the delegatee's key, and a notary name equal to an executor's each refuse with their own code. |
| Arithmetic that closes at or below the pool | `after` unequal to `before` plus `child`, `after` above `pool`, and a broken chain of predecessors refuse as `ATTESTATION_ARITHMETIC`. |
| `textual` consistent with the hashes | `identical` over different hashes and `none` over a present text refuse as `ATTESTATION_BINDING`. |
| A request signed by the parent's grantee for this contract and ordinal | A request by another key, or for another contract or ordinal, refuses as `DELEGATION_REQUEST`. |
| Two links | A third link and a repeated id refuse as `CHAIN_DEPTH`. |
| On a node: a live parent, a confirmed anchor, an unspent notary seal | A spent parent seal refuses as `PARENT_NOT_LIVE` while the child's seal is unspent. A notary seal spent in the mempool refuses as `NOTARY_WITHDRAWN` while the child's seal is unspent. An unconfirmed anchor is pending and not refused. A reorganised tip refuses as `ATTESTATION_TIP`. |
| The same child certified again after a plain withdrawal | Certified again after a withdrawal for cause refuses at an executor that journalled the frame. For a verifier that did not observe it, see the second planned case below. |
| A verifier that journalled the notary's spend, after the spend is reorganised out of the chain | The withdrawn attestation still refuses as `NOTARY_WITHDRAWN`; admitting it again because the seal looks unspent is wrong. A fresh attestation of the same child by a named notary after that plain withdrawal is admitted. |
| An agent and a person as notary with the same attestation shape | Refusing because the notary is an agent, or because it is a person, is wrong. |

Sections 3.4, 7.1, 9.1, 10.1 and 11.1 carry the cases of their Draft text,
which is under pending owner decisions.

Two further cases are planned as negative cases of a v4 vector set. Under the
rules in force both are admitted, and the verdict a vector must require
depends on a pending owner decision:

| Case | Today | Depends on |
| --- | --- | --- |
| Two children of one parent, both with ordinal 1, each certified by a different named notary | Each is admitted on its own bundle, also when their budgets together exceed the pool or `max_children` is 1 | J1 and J2. Under sections 9.1 and 10.1 the case has three verdicts. The child whose notary is not the row's refuses as `NOTARY_NOT_DESIGNATED`. A second child for another grantee or executor refuses at V8. For the same row, the same notary and two different ids, each child is admitted on its own bundle, which is the known limit S1-K1 of section 9.1 |
| A child whose attestation was withdrawn for cause, presented with a fresh attestation by another named notary while the child's own seal is unspent, to a verifier that observed neither the frame nor a revocation | Admitted | J2. Under section 10.1 the child refuses as `NOTARY_NOT_DESIGNATED`. The case is S2-2; it tests designation only and runs beside the known limit S2-K1 |

## Open questions

### Gaps found in review

Two independent reviews of the design found five gaps in this LIP: the pool
across several notaries, a withdrawal for cause that does not reach a new
verifier, the notary bound by name only, the key an agent signs a child
with on v4, and scope text that is not enforced. Each now has Draft text
under a pending owner decision, in the subsection that the table of pending
decisions names. The first paragraph of each subsection states the gap with
the case that shows it, and each subsection says what its text closes and
what stays open. No gap is closed before the owners decide, and none is
called closed for a property that its subsection lists as open.

### Other open questions

- Canonical vectors for profile `/2`, the request and the attestation, and an
  extension of the reference checker.
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
- The v4 bytes of the right of re-delegation, the delegation key of section
  11.1 among them.
- D4 places the pieces of this LIP after the first proof, as tools around v3
  that change no v3 byte. Question T1 of LIP-0013, whether such tools count
  as "v3 as is", has no explicit answer yet.
