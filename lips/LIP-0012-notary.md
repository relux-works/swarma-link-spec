# LIP-0012: Notary

- **Status:** Draft
- **Created:** 2026-11-11
- **Affects:** grant admission, re-delegation (LIP-0008 section 12.6), the
  key map
- **Builds on:** LIP-0004 and LIP-0008
- **Extended by:** LIP-0014, which proposes the bytes and the checks for a
  child grant

## Summary

A child grant must not be broader than its parent. A verifier can compare
action sets and numbers. It cannot compare conditions written in words. The
notary is the party that does: it reads the child and the parent, and
certifies that the child does not exceed the parent.

A notary is an additional link beside the authority path. It certifies a
grant and can revoke it. It creates no authority: a certified grant carries
exactly the rights its issuer signed. A notary can be an agent or a person.

Nothing in this LIP is implemented in a grant profile. The reference
laboratory compared two ways of attaching a notary to a grant on regtest
with one trusted node. This LIP proposes semantics on that basis, without
canonical bytes. For a child grant,
[LIP-0014](LIP-0014-notary-certified-redelegation.md) proposes the object,
its anchor and the order of the checks.

## Decisions recorded

Ivan Oparin decided the following on 2026-11-11. The LIP stays Draft until
the co-author agrees; adoption follows LIP-0001.

| Decision | Direction |
| --- | --- |
| N1. Role | A notary is an additional link that certifies a grant and can revoke it. |
| N2. Re-delegation | For a re-delegated grant the notary is the party that checks that the child does not exceed the parent's authority, and certifies it. |
| N3. Performer | The notary can be an agent or a human. |
| N4. Sensitive scenarios | Recommended: a grant with the right of re-delegation, plus a notary. |

The owners decided the following on 2026-11-12. LIP-0014 records D1 to D12;
N5 to N9 restate the part of them that concerns the notary, and N10 is a
direction of the same day.

| Decision | Direction |
| --- | --- |
| N5. Every child | Every child grant is admitted only with a valid attestation (D1). A root grant with a right of re-delegation names its notaries and needs none (D2). |
| N6. Designation | The parent's signed right of re-delegation names one to four notaries by `id/` name, and each notary publishes its attestation key in its own name (D3). One attestation by any of them is enough (D9). |
| N7. Whose notary | Within one owner the notary is the issuer's. Across owners it is a third party both agree on, and never a notary that belongs only to the delegator's owner (D8). |
| N8. Withdrawal | A withdrawal is durable. The same child may be certified again after a plain withdrawal and may not after a withdrawal for cause (D5). |
| N9. Anchor | One LIP-0005 frame per attestation (D10). |
| N10. The notary issues nothing | The notary attests and does not issue. An owner may be the notary of their own grants. |

N1 to N10 are the owners' directions. The decisions of 2026-11-12 are stated
in terms of the separate attestation: they fix its anchor and the effect of
its withdrawal. Everything else in this LIP and in LIP-0014 is a draft's
proposal and is not decided: every field and byte of the attestation, the
admission steps and their codes, and the form of the signed requirement.

## Motivation

LIP-0008 section 12.6 makes child grants part of the protocol and requires
that a child is never broader than its parent. Section 12.2 enforces this
for known action sets and numeric ceilings, and refuses unknown constraint
semantics. The contract text and the scope of a task are words. A program
cannot tell whether "work on the project and its dependencies" is wider
than "work on the project".

Without a notary, a verifier of such a child either trusts the agent that
issued it or refuses every child with textual conditions. With a notary, a
named third party has read both documents and signed a statement that can
be withdrawn.

## Current state

The specification has no notary. The laboratory experiment `notary` at
`swarma-chain-lab` `839bdcca41cd17ffd7c4057de2dc88a521745515` compared two
schemes on regtest, with one trusted node and synthetic statements:

| Scheme | How the notary takes part | What withdrawal does |
| --- | --- | --- |
| Separate attestation | The notary signs a statement that names the hash of the grant and the notary's own seal, and anchors the hash of the statement. | The notary spends its seal. A verifier whose policy requires that notary refuses. The grant's own seal stays unspent. |
| Co-signed issuance | The issuance transaction spends an output that needs the issuer's and the notary's signatures. | The notary spends its seal and withdraws the endorsement. The issuance is not reversed and the issuer's seal is not revoked. |

The experiment states its conceptual default as the separate attestation,
"subject to corrected verifier review and an explicitly selected
trusted-notary policy". It is a laboratory comparison. It does not qualify a
production policy, a grant contract or a name lifecycle, and its statements
are not vectors. The notary's verdict in it concerns a fact about the grant;
it does not compare a child with a parent.

## Proposal

### 1. The role

A notary certifies facts that it checked itself. For a child grant the fact
is: this child, issued under that parent, does not exceed the parent's
authority, including the conditions written in words in both contracts.
Other facts are possible, for example that a recipient key belongs to a
named party; each attestation says what was checked.

The performer is an agent or a person (N3). The protocol sees a key. Like
the moderator of LIP-0011, an agent that performs the role does not prove
how it reached its statement; the statement binds the notary's key and
nothing more.

The notary is not on the authority path. It issues no grant, holds no
right of re-delegation by its role, and its attestation adds no action,
limit or lifetime to the grant.

### 2. The attestation

An attestation is a signed object of its own type under LIP-0008 section 8.
It has these logical fields; the table is not a byte fixture:

| Field | Meaning |
| --- | --- |
| Grant | The `grant_id` of the certified grant. |
| Parent | For a child grant, the ID of the parent it was compared with. Absent otherwise. |
| Checked | The statement the notary makes: a kind from a closed set, and the values it is bound to. For re-delegation the kind is "child within parent", bound to the `contract_sha256` of the child and the `contract_sha256` of the parent. |
| Notary | The notary's key and, when it is named, its name with the pins of LIP-0008 section 3. |
| Notary seal | An outpoint that the notary alone can spend. |
| Height | The height of the tip the notary's node validated. It is a claim of the signer. |
| Signature | A signature by the notary key over the object's typed digest. |

The hash of the attestation is anchored on chain. The laboratory anchors it
in an update of the notary's own name. The owners chose the other candidate,
a LIP-0005 frame per attestation (N9); LIP-0014 section 6.4 proposes its
action and commitment.

### 3. A grant that requires a notary

A grant can require an attestation. The requirement is signed: it is part
of the grant, or of the right of re-delegation under which the grant was
issued. It names the notary or the set of notaries that satisfy it, and the
kind of statement it demands. A parent can thus require that every child
issued under it is certified as within the parent.

A verifier can also require a notary by its own policy, for a grant that
does not ask for one. That is the laboratory's arrangement: a list of
trusted notary identities in the verifier's configuration.

For a child grant the requirement is no longer a choice of the parent: every
child needs an attestation (N5), and a right of re-delegation that names no
notary is malformed. LIP-0014 section 2 proposes the member that carries the
names. For a grant that is not a child, field names and encoding of a
requirement stay open.

### 4. Admission

For a grant that requires a notary, admission adds one step to LIP-0008
section 4, after the grant and every ancestor passed their own checks. The
verifier checks, on the same observation of its own node:

1. the attestation's signature under a notary that the requirement names;
2. that the attestation names this grant and, for a child, the parent
   that the child itself commits to;
3. that the Checked statement is of the kind the requirement demands and
   is bound to this case: for "child within parent", its two contract
   hashes equal the `contract_sha256` of this child and of that parent;
4. that the attestation's anchor is in the active chain;
5. that the notary's seal is unspent, with the mempool included.

Step 3 is a check of its own. An attestation by the right notary for the
right grant and parent, with a valid anchor and a live seal, does not
satisfy the requirement if it states something else, for example that a
recipient key belongs to a named party, or if it states "child within
parent" for other contracts. The step verifies what the notary asserted.
It does not verify that the assertion is true: whether the child's words
are within the parent's stays the notary's judgement (section 6).

A missing, unverifiable or withdrawn attestation refuses. An attestation
never substitutes for a check of section 4: a certified grant with a spent
seal, an expired window or a closed ancestor refuses.

For a child grant on v3, LIP-0014 section 8 gives these five checks their
place in an executor's order, as steps V10 to V18, after the mechanical
comparison of the child with its parent.

### 5. Revocation

The notary revokes by spending its seal (N1). For a grant that requires the
attestation, every verifier then refuses at step 5. The grant's own seal is
untouched: only the issuer can spend it, and the notary's spend does not
make the grant's seal spent.

Two points were open until 2026-11-12, and N8 settles both. A verifier that
observed the notary's spend journals the withdrawal durably, like the
issuer's spend in LIP-0008 section 5.1; it does not recompute it from the
active chain. After a plain withdrawal a notary that the requirement names
can certify the same grant again. After a withdrawal for cause it cannot,
and the issuer issues a new grant. LIP-0014 section 10 proposes how a
withdrawal for cause is marked. The laboratory refuses on a spend seen in
the mempool and keeps refusing after the withdrawal is reorganised out while
it stays in the mempool; it implements no journal.

For a grant that requires no notary, a withdrawal removes the endorsement
for verifiers that asked for it by policy and changes nothing else.

### 6. What the notary of a child checks

The notary receives the child, the parent and both contracts. It verifies
the mechanical part like any verifier: the parent carries the right of
re-delegation, the child commits to it, action sets and ceilings do not
widen. It then reads the conditions in words and decides whether the
child's are within the parent's. The attestation records the hashes of what
it read.

The attestation is a statement of the notary, not a proof. A wrong
statement is visible afterwards to anyone who holds both documents, and the
parties' recourse against the notary is outside the protocol.

### 7. Designation and independence

A verifier accepts an attestation only from a notary that the parent grant
names. The names are part of the parent's signed right of re-delegation
(N6), so the issuer chooses them and the grantee consents to them with the
contract. A notary named in a message, in an agent's instructions or in a
configuration file gives nothing to a verifier.

The attestation key is read from the notary's own name. A notary name has
its own `swarma` shape, proposed as an amendment of
[LIP-0010](LIP-0010-name-value.md): it is neither a landlord name nor an
agent name. The notary replaces its key by updating that name, and no grant
that names the notary is reissued.

The notary is independent of the two parties whose authority it compares. It
is not the party that re-delegates and not the party that receives the
child. A verifier checks what keys and names can show: the notary's key
differs from the delegator's key and from the delegatee's key, and the
notary's name differs from the executors' names (LIP-0014 section 8, step
V13). Different keys do not prove different parties. The stronger control is
N7: the issuer, whose authority the child must not exceed, names the notary,
and the delegator does not.

An owner may certify children of their own grants (N10). The attestation
then guards the owner's grants against errors of the owner's delegating
agents, not against the owner.

## Alternatives

Structured scope (LIP-0008 section 12.6, proposal a) removes the need for a
notary wherever the scope fits the structure, because any verifier can then
check the subset relation. It does not cover conditions that stay in prose.
Refusing every child with textual conditions is safe and makes
re-delegation unusable for contracts. Trusting the re-delegating agent
leaves the check to the party whose authority is being limited. Co-signed
issuance makes the notary's consent visible in the issuance transaction;
the laboratory found that a later withdrawal does not reverse that
issuance, and by construction a second notary needs a new joint issuance.

## Security consequences

A notary that signs carelessly, or whose key is stolen, certifies children
that exceed their parents in words. It cannot widen the mechanical limits:
the verifier still enforces action sets, ceilings, budgets and windows of
every link.

A notary can deny service: it can refuse to certify, and it can withdraw.
Two rules bound this: a requirement may name up to four notaries, any one of
which is enough (N6), and after a plain withdrawal another named notary can
certify the same grant (N8).

The notary learns the contents of both contracts. A deployment that cannot
disclose them to a third party uses issuance by the operator's signer
instead (LIP-0008 section 12.6).

The notary, the moderator of LIP-0011 and the arbiter of a contract are
three different third parties: the first certifies a grant before it is
used, the second judges requests while it is used, the third decides a
dispute after it. One party can hold more than one of these roles only if
the contract says so.

## Conformance impact

No normative conformance class changes. A future vector set pairs these
controls:

| Valid control | Refusal or invariant |
| --- | --- |
| A child that requires a notary, with a valid attestation by a named notary whose seal is unspent | The same child without the attestation, with an attestation by a notary the requirement does not name, or with one that names another grant or another parent refuses. |
| The same child with an attestation of the demanded kind, "child within parent", bound to the contract hashes of this child and its parent | An attestation that is valid in signature, IDs, anchor and seal but states another fact, or states "child within parent" for other contract hashes, refuses. |
| The same child after the notary spent its seal, seen in the mempool | Refuses. The child's own seal is still unspent; reporting the grant's seal as spent is wrong. |
| A certified child whose own seal is spent, whose window ended or whose parent is closed | Refuses; the attestation does not override section 4 of LIP-0008. |
| A certified child with a wider action set or a higher ceiling than its parent | Refuses mechanically; an attestation does not waive the checks of section 12.2 of LIP-0008. |
| A grant that is not a child and requires no notary, with and without an attestation | Both are admitted by a verifier without a notary policy; refusing for a missing attestation that nothing requires is wrong. |
| A child grant with a valid attestation by a notary its parent names | The same child without an attestation refuses, whatever its scope and whatever the verifier's own policy (N5). |
| An agent and a person as notary with the same attestation shape | Refusing an attestation because its notary is an agent, or because it is a person, is wrong. |

## Open questions

Closed on 2026-11-12: where the attestation is anchored (N9), how a notary
is named (N6), durable closure and certification after a withdrawal (N8),
and who pays (LIP-0014, D11). An attestation of a child is not renewed when
the parent's contract is replaced; the new parent has new children
(LIP-0014 section 10).

Still open:

- Adoption of the bytes, the signing domain and the statement kinds that
  LIP-0014 proposes for a child grant; statement kinds for other facts.
- The field that carries a requirement in a grant that is not a child.
- Whether a v4 parent pins a notary name by its registration and owner key,
  as it pins an issuer.
- Whether the notary of a child and the moderator of the same contract can
  be one party.
