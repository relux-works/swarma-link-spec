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

One addition to the decisions above waits for an owner's decision. Its
rules stand in this LIP as Draft text, each marked "owner decision pending"
with the label of this table. Nothing of it is adopted until the decision.

| Label | Adds to | Direction of the Draft text |
| --- | --- | --- |
| J3. Notary identity | D3 | The parent pins each notary as LIP-0008 section 3 pins an issuer: by name, registration and owner key, with a signed checkpoint, and the attestation key in force must have been written by the pinned owner. Sections 2, 7.1 and 8, step V12. |

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
| Child signer | On v4, the delegator. On v3, the landlord's grant key, acting on the delegator's signed request (section 5). |
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
v4 bytes. On v3 it has exactly these eight members in this order:

| Member | Type | Rule |
| --- | --- | --- |
| `depth` | integer | `0` or `1`. `0` means the grant carries no right of re-delegation. A child carries `0`. |
| `actions` | array of strings | The actions a child may receive: sorted, without duplicates, a subset of the grant's own `actions`. Non-empty when `depth` is 1. |
| `agents` | array of strings | The `id/` names a child may name as `agent_name`: sorted, without duplicates, each different from `landlord_name`. 1 to 16 entries when `depth` is 1. |
| `grantees` | array of strings | The x-only keys a child may name as `grantee_key`: sorted, without duplicates, 64 lowercase hex each. 1 to 16 entries when `depth` is 1. No wildcard. |
| `budget` | integer | Atoms that all children together may receive as `spend_budget`. Greater than 0 exactly when `actions` includes `spend`; at most 2100000000000000. It is separate from the grant's own `spend_budget` (section 9). |
| `max_children` | integer | 1 to 16 when `depth` is 1. The largest ordinal a child may carry. |
| `notaries` | array of objects | The notaries whose attestation satisfies D1: 1 to 4 objects when `depth` is 1, sorted by `name`, without a repeated name. Each object has exactly the members `name`, `registration` and `owner`, in this order (section 7.1). Owner decision pending: J3; until it, each entry is the `id/` name alone. |
| `checkpoint` | string | The hash of a block of the active chain, 64 lowercase hex, from which the ownership of every named notary must be unbroken (section 7.1); `""` when `depth` is 0. v3 only: on v4 the grant's committed recent block takes its place. Owner decision pending: J3; until it, the member does not exist and the object has seven members. |

When `depth` is 0 every array is empty, `budget` and `max_children` are 0 and
`checkpoint` is `""`.

A right of re-delegation with `depth` 1 and no notary is malformed and
refuses as `DELEGATE_NO_NOTARY`. Every other violation of this table refuses
as `CONTRACT_DELEGATE`, a notary entry that is a bare name or lacks one of
its three members included. This is how D1 and D3 become a field check: a
grant cannot give the right to re-delegate without saying who certifies.

Only `depth` 1 gives the right. Ordinary action authority, possession of a
grant, management of an agent and an audience key give none (LIP-0008 sections
12.2 and 12.6).

In Goal 1 a right of re-delegation MUST NOT list `spend`, and its `budget` is
0 (D12). The budget members and the arithmetic of sections 6 and 9 stay in the
format for a later decision.

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

The scope text is a separate document. Its exact octets hash to
`scope_text_sha256`, and it travels with the bundle. Text narrows only: like
the note of LIP-0013, it can never add an action, a repository, a budget or
time. It is meant to restrict what the structured members already allow. A
wrong judgement about text therefore cannot widen a mechanical limit. No
step of section 8 and no step of LIP-0013 section 3.4 compares an
instruction with the text. Whether an executor honours the text is left to
that executor, which is a gap listed under Open questions.

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
| `0x04` | notary attestation | `version(1) || attestation_commitment(32) || locator` |

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
A name alone would leave the same update open to whoever holds the name
later; section 7.1 binds the registration and the owner of the name as well.

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

Owner decision pending: J3. Every rule of this subsection is Draft text that
adds to D3. Until the decision a parent binds a notary by name only, and a
transfer of the notary's name, or its expiry and a new registration, passes
the right to certify to the new holder.

A parent binds each notary as LIP-0008 section 3 binds an issuer: by the
exact name, the registration of that name and its owner key. The attestation
key stays free to change under the same owner. Each entry of
`delegate.notaries` is an object with exactly three members in this order:

```json
{"name":"id/acme-notary","registration":{"txid":"<64 hex>","vout":0},"owner":"<owner pin>"}
```

`registration` is the transaction and output that first registered the name.
`owner` is the owner pin, in the encoding that LIP-0008 section 3 will fix.
`delegate.checkpoint` is the hash of a block of the active chain; the
stretch of the name's history that the rules constrain starts there.

| # | Rule | Refusal |
| --- | --- | --- |
| J3.1 | A right of re-delegation MUST bind, for each notary, the name, the registration and the owner key. | A bare name, or an entry without one of the three members: `CONTRACT_DELEGATE` |
| J3.2 | At every admission of a child the verifier MUST walk the history of the name of the notary whose attestation is presented, under rules 1 and 2 of LIP-0008 section 3. The walk MUST reach the bound registration. The bound registration MUST be confirmed at or below the checkpoint block, and an unexpired output of that registration MUST be current at the checkpoint. Every output from the one that was current at the checkpoint to the current one MUST be controlled by the bound owner key. | A checkpoint that precedes the registration, one at which the name has no output, and one that is not in the active chain: `NOTARY_CHECKPOINT`. An expired name, a walk that ends at another registration, and an owner change on the stretch: `NOTARY_NAME_CHANGED` |
| J3.3 | The value of `swarma.notary.attest` MAY change on that stretch. The attestation key is the one the current value yields. The comparison MUST NOT be an equality of the whole `swarma` member. | none |
| J3.4 | The value in force is the value of the operation that created the name's current output. That operation MUST have been authorized by the bound owner: the name input it spends MUST be controlled by the bound owner key, and the signature on that input MUST commit to the output that carries the value. The first owner-proof profile accepts `SIGHASH_ALL` without `ANYONECANPAY` only. For a `name_update` the name input is the previous name output. For a `name_firstupdate` it is the `name_new` output; a fee input is no substitute. The bound registration is no exception. A value that fails this is not eligible until the bound owner makes a name update of its own, which may repeat the value unchanged. The rule looks at one operation; it does not trace a value back through history. | `NOTARY_VALUE_UNAUTHORIZED` |
| J3.5 | Where nothing is proved, the verifier refuses and holds no evidence of a transfer: an incomplete walk, a node without the transaction index, an owner proof or a signature-hash type that the profile does not support, a history supplied by the presenter. | `NOTARY_HISTORY_UNAVAILABLE` |
| J3.6 | A presentation MUST NOT move the start of the stretch. A later issuance locator, a new anchor of the same parent and a newer attestation leave the signed checkpoint where it is. | none of its own |
| J3.7 | Only the notary of the presented attestation is walked. The state of another notary of the same parent does not affect this child. | none of its own |
| J3.8 | A cached walk is valid only for its predicate: this name, registration, owner pin and checkpoint, the active chain up to the cached output, and the notary rule "owner unbroken, value written by the owner". A result cached for an issuer's rule, which also requires an unchanged `swarma`, MUST NOT be used for a notary, nor the reverse (LIP-0008 section 3). | none of its own |
| J3.9 | Before it signs a parent, the issuer's signer MUST run J3.2 and J3.4 for every notary it names, so that it does not sign a parent under which every child refuses. | none at a verifier |

All of these refusals come before `NOTARY_KEY`, and none records a closure.

The writer rule J3.4 has no exception for the registration, because
receiving an output is not consent. A party `U` that holds a `name_new`
commitment can sign the `name_firstupdate` with its own attestation key in
the value and pay the name output to the address of an honest owner `O`.
`O` signs nothing. A parent that pins that registration and `O` passes J3.2,
because every output on the stretch is `O`'s, and without J3.4 `U` would
certify. Under J3.4 the operation that created the current output is the
registration, its `name_new` input was `U`'s, and the child refuses until
`O` makes an update of its own. These transaction facts were read in the
source of Namecoin Core, release nc28.0; no node was run for them.

The rules do not cover four things. A thief of the notary's name-owner key
writes a new attestation key under the same owner; the defence is cold
custody, as for an issuer. A notary that replaces its owner key needs new
parents. A notary whose name another party registered for it makes one name
update of its own before a parent can use it. And a reorganisation that
drops the checkpoint block refuses every child of that parent, without
closure, until the chain holds the block again or the parent is issued
again; the issuer SHOULD sign a block that is buried under its own risk
policy.

The owner-pin encoding and the script coverage of the owner proof are open
in LIP-0008 section 3. Until they exist an unsupported proof refuses under
J3.5, and byte vectors of profile `/2` wait for them.

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
| V12 | `notary_name` is listed in `P.delegate.notaries`. Then, under section 7.1 (owner decision pending: J3): the pins of that entry and the checkpoint, the walk of the name's history, and the writer of the value in force. Then the current value of that name on the verifier's node yields `notary_key` | `NOTARY_NOT_DESIGNATED`; then `NOTARY_CHECKPOINT`, `NOTARY_NAME_CHANGED`, `NOTARY_VALUE_UNAUTHORIZED` or `NOTARY_HISTORY_UNAVAILABLE`; then `NOTARY_KEY` |
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
another notary certified under the same ordinal, which is a gap listed under
Open questions. A named party has recorded both contract hashes, the
arithmetic and the tip it saw.

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
draft brings the two attestations before one party (Open questions). A pair
for the same child after a withdrawal is a new certification of that child
(section 10) and no fork.

A consumed ordinal and its budget stay consumed when the child is revoked or
its attestation withdrawn. LIP-0008 section 12.2 requires that reissuance
does not reset an ancestor's consumed allowance.

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
| `0x05` | notary withdrawal for cause | `version(1) || withdrawal_commitment(32) || locator` |

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
have no step that looks for it, which is a gap listed under Open questions.

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
| Agents that sign grants | None | The delegator signs the child with the parent's recipient key (LIP-0008 section 12.6). For a parent issued by name that is the key the name lists at admission, so a child signed with an earlier key refuses (LIP-0008 sections 3.1 and 12.2). Whether an agent needs a key of its own for this, and whether that rule stays, is open (Open questions) |

Depth stays at two links (D7). Work below a child's executor is covered by a
new root grant from the principal.

Each party pays for its own effects under D11. A payment for a notary's seal,
anchor or fee from an owner's funds follows that owner's spending rule; where
the owner approves each spend, the payment is approved per spend.

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
  one ordinal (Open questions).
- **A withdrawal for cause does not reach everyone.** It binds the parties
  that observed its frame. Another named notary can certify the child again,
  and a verifier that starts later admits it (Open questions).
- **The notary's name changes hands.** By name alone, the holder of a
  notary's name after a transfer, or after an expiry and a new registration,
  publishes its own attestation key and certifies under every parent that
  names it. Section 7.1 (owner decision pending: J3) refuses these cases for
  every verifier whose node holds the name's history. It does not cover
  theft of the notary's name-owner key.
- **Scope text binds nobody at admission.** The notary judges the text once.
  No admission step compares an instruction with it (Open questions).
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

Cases for section 7.1 (owner decision pending: J3). Each uses a verifier that
starts after the events and holds no journal:

| Valid control | Refusal or invariant |
| --- | --- |
| Renewal of the notary's name by the same owner; the child is admitted | The name transferred to another owner who publishes a key and attests with it refuses as `NOTARY_NAME_CHANGED`, although the attestation verifies under the name's current key. |
| The same unexpired registration, after a renewal | Expiry and a new registration with the same spelling, by another key and also by the same owner key, refuse. A checker that compares only the current owner passes the first and must fail the second. |
| An unchanged history since the checkpoint | A transfer and return on the stretch, with the current owner and key identical to the control, refuses. |
| The checkpoint signed in the parent | A valid later re-anchor of the same parent, presented to skip a transfer: the stretch still starts at the checkpoint, and the child refuses. |
| A value written by the bound owner in an update | An output of the bound owner whose value a previous holder wrote in the transfer refuses as `NOTARY_VALUE_UNAUTHORIZED` until the owner updates. The fixture puts the checkpoint after the transfer; otherwise the ownership walk refuses first. |
| The owner's own registration; a registration by another party paid to the owner, followed by the owner's update that repeats the value; after that an ordinary rotation by the owner | A `name_firstupdate` signed by another party, with that party's key in the value, paid to the pinned owner, without a later update: `NOTARY_VALUE_UNAUTHORIZED`. An owner-signed fee input beside the other party's `name_new` input, and an owner input signature that does not commit to the value output, refuse in the same way. |
| The notary rotates `attest` under the same owner and signs again: admitted | The attestation under the old key refuses as `NOTARY_KEY`; refusing the new one because `attest` changed is wrong. |
| A complete walk on the verifier's node under a supported owner proof | One historical name transaction missing while every other read works; a node without the index; an unsupported script or signature-hash type; a history supplied by the presenter: `NOTARY_HISTORY_UNAVAILABLE`, and the journal holds no closure afterwards. |
| The notary of the presented attestation is intact; another notary named by the same parent changed hands or cannot be read | The child is still admitted. A verifier that walks every named notary fails this. |
| An entry with name, registration and owner; a checkpoint in the active chain at or after the registration | A bare name: `CONTRACT_DELEGATE`. A checkpoint before the registration, and one not in the active chain: `NOTARY_CHECKPOINT`. After a reorganisation that drops the checkpoint the child refuses without closure, and is admitted again when the block is back. |

Two further cases are planned as negative cases of a v4 vector set. Under the
rules of this draft both are admitted, and the verdict a vector must require
depends on an open question below:

| Case | Today | Depends on |
| --- | --- | --- |
| Two children of one parent, both with ordinal 1, each certified by a different named notary | Each is admitted on its own bundle, also when their budgets together exceed the pool or `max_children` is 1 | The pool across several notaries |
| A child whose attestation was withdrawn for cause, presented with a fresh attestation by another named notary while the child's own seal is unspent, to a verifier that observed neither the frame nor a revocation | Admitted | A withdrawal for cause does not reach a new verifier |

## Open questions

### Gaps found in review

Two independent reviews of the design found five gaps in this LIP. For one
of them, the notary bound by name only, section 7.1 now holds Draft text
under the pending owner decision J3. The other four are given with the case
that shows each. The fixes named for them are candidates: proposals that
the owners decide. This LIP chooses none of them.

| Gap | The case that shows it | Candidate fixes (proposals; the owners decide) |
| --- | --- | --- |
| **The pool across several notaries.** A parent names up to four notaries, and any one of them is enough (D3, D9). Each certifies against its own record of the parent's children (section 6.2). | A parent has a pool of 100 and names notaries N1 and N2. Child A takes 60 and is certified by N1; child B takes 60 and is certified by N2. Both children carry ordinal 1, and both attestations carry `before` 0 and `after` 60. Each child passes V9 and V15 on its own bundle, and the two hold 120 together. Neither notary signed two attestations for one ordinal, so the pair shows no equivocation of a notary. The case needs a child signer that uses one ordinal twice. On v3 that is the landlord's signer, which admits an ordinal once for a parent and reserves the amount before it signs (section 5), so the case needs an error or a compromise of that signer. On v4 the delegator signs the children and reaches the case alone. In Goal 1 the pool is 0 (D12) and no amount is at stake; the same pair still gives a parent with `max_children` 1 two children. | (a) The anchor of each attestation spends an output of the anchor of the previous attestation for the same parent, so that consensus orders the attestations of one parent. (b) The parent fixes a share for each executor, and each executor sums what the children presented to it spend, by the parent's id; moving budget between shares then needs an agreed state of its own. |
| **A withdrawal for cause does not reach a new verifier.** The frame of section 10 is addressed by the attestation id: its commitment covers that id and the child's grant id, and its locator points at the attestation. No step of section 8 looks for it. | Notary N1 withdraws its attestation of child C for cause. N2, which the parent also names, did not observe the frame and certifies C again when it is asked. A verifier that starts afterwards receives C with N2's attestation, and every step from V10 to V18 passes: V18 reads N2's seal and the verifier's own journal. The case holds while C's own seal is unspent: until the landlord's signer has revoked C, or for as long as that signer has not observed the frame. To find the frame from the child's id, a verifier would have to test every `0x05` frame on the chain against that id. No rule asks for that, and none says when such a search is complete. | A state per `child_grant_id` that a verifier finds on its own node, such as a marker it can index, with rules for completeness and for competing attestations of one child. |
| **The key an agent signs a child with on v4.** LIP-0008 section 12.6 has the parent's recipient sign the child: the grantee key, or for a parent issued by name the key that the name yields. An agent's name yields one key, its Nostr key (LIP-0010). Whether a re-delegating agent needs a key of its own is open there. | The agent's Nostr key is held by the gateway of the host the agent runs on (key map). When that host is run by an operator other than the agent's own, a key that signs grants is in that operator's hands, and one key signs both messages and grants; for a principal the key map keeps those two apart. A change of that key is a name update by the operator (K2), for example when the agent moves to another host under the registration flow that the key map proposes. For a parent issued by name the current rules already give the result. The parent survives, because its request key is read from the name's current value at every admission (LIP-0008 section 3.1). A child signed with the earlier key refuses at use for as long as the name lists another key, because its issuer does not equal the parent's recipient (LIP-0008 section 12.2); nothing records a closure. A child signed with the new key passes that comparison. Every change of the agent's Nostr key therefore stops the children it signed. On v3 the landlord signs the child; the delegator's request of section 5 is signed with `P.grantee_key`, which for an agent is that same Nostr key. | A separate re-delegation key of the agent, or signing by the landlord only. For the children of an agent whose key changes: keep the current rule, under which they stop with the key, or check a child against the key that the name listed at its issuance. |
| **Scope text is not enforced.** Section 3.3 lets a text narrow a grant. The notary judges the child's text against the parent's once, at certification. | A child's text limits the work to one component of a repository. An instruction that concerns another component, within the child's actions and repositories, passes every step of section 8 and steps 6e to 6g of LIP-0013, because no step compares an instruction with the text. The notary's `within` is a judgement as well: no verifier can recompute it. | A child carries the parent's text unchanged, by hash, and narrows only machine fields, such as repository, branch, action, recipients and amounts. |

### Other open questions

- Canonical vectors for profile `/2`, the request and the attestation, and an
  extension of the reference checker.
- Kind 8186 is a draft allocation, with the same limits as kind 8185.
- The carriage of the request and of the bundle between agents, which follows
  the open carriage question of LIP-0013.
- The record that states the cause of a withdrawal. How a verifier that
  observed neither the withdrawal nor the revocation of the child learns of a
  withdrawal for cause is the second gap above.
- A quorum of notaries for sensitive resources; D9 fixes one of the set.
- A batched anchor and one seal per parent; D10 fixes one frame per
  attestation now.
- The v4 bytes of the right of re-delegation. Whether a re-delegating agent
  on v4 needs a key of its own is the fourth gap above (also LIP-0008
  section 12.6).
- D4 places the pieces of this LIP after the first proof, as tools around v3
  that change no v3 byte. Question T1 of LIP-0013, whether such tools count
  as "v3 as is", has no explicit answer yet.
