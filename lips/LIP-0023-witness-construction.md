# LIP-0023: Witness construction profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** how an issuer builds the seal transaction and the anchor of a
  v4 grant on Namecoin, and how a verifier checks their inputs, their
  funding and their order
- **Builds on:** LIP-0008 sections 1.1 and 9, LIP-0005, LIP-0020 section 8
  and LIP-0022 sections 1 and 4

## Summary

Under the Witness profile of LIP-0008 an issuance may rest on two
unconfirmed parents: the linkage output that the seal transaction creates,
and a same-chain payment output that the anchor spends. LIP-0008 says that
the exact dependency and payment checks still need versioned fixtures. A
verifier that cannot tell a permitted parent from arbitrary unconfirmed
funding has to refuse both or to admit both.

This LIP proposes the first construction profile for Grant v4, the Witness
profile on Namecoin, in its narrowest useful form:

- the profile is selected by the verifier's authenticated configuration and
  by nothing in a presentation (section 1);
- the anchor always spends the linkage output, which is the output that
  follows the seal in the seal transaction; that makes the anchor an act of
  the holder of the key that this one output pays (section 2);
- every input of the two transactions spends a witness key hash with a
  signature of hash type `01` (section 3);
- the linkage is the only parent that may be unconfirmed; every other input
  spends an output that is confirmed below its spender (section 4);
- an effect needs a confirmed anchor (section 5);
- a replaced seal transaction needs a new grant, and a replaced anchor
  changes nothing that was signed (section 6);
- thirteen refusal codes and their order (section 7);
- vectors (section 8).

The unconfirmed payment parent of LIP-0008 is refused under this profile
until a proposal of its own says how a verifier authenticates it. The
Legacy profile is not proposed.

## What is decided and what is proposed

The two construction profiles, Witness and Legacy, are Draft text of
LIP-0008 sections 1.1 and 9, which calls the Witness profile for Namecoin
the first implementation direction. This LIP changes none of it. It
proposes a first profile inside that text, and where it is narrower than
the text, it says so:

| LIP-0008 | This profile |
| --- | --- |
| The seal transaction creates the seal and an additional output, the linkage output, and the anchor spends it (section 9) | The same, as a rule that a verifier checks for every grant, with the linkage output fixed as the output that follows the seal (C2.3) |
| Two unconfirmed dependencies are permitted: the linkage output and a same-chain payment output (section 1.1) | The linkage output alone. An unconfirmed payment output refuses (C4.4) |
| "The exact dependency and payment checks still need versioned fixtures" | Sections 3 and 4, with vectors, for the linkage |
| The selected profile belongs to the authenticated chain context; "exact pin encoding and fixtures remain open" | A value of the verifier's authenticated configuration (C1.1). Its place in the octets of a grant stays open |

Every rule of this LIP is the draft's proposal. Neither owner has decided
one. The reference laboratory implements a subset of the Witness profile
for Grant v3, which the section "Current state" describes; that subset is
the laboratory's and no decision of the owners either. The owners accept or
change the rules through this LIP, under LIP-0001.

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The form of an input on its octets, and the checks of funding, linkage and order on stated facts (sections 2 to 4, 7) | Yes | The owners' acceptance |
| The reads of the two transactions and of their parents on a node, in one observation | The reference laboratory has them for its own subset | LIP-0022 for the observation; a run under the rules of this profile |
| The seal output: its script, its key and its endorsement | No | The seal profile (LIP-0008 sections 11 to 11.3) |
| The seal outpoint as a member of a grant | No | The members of the grant (LIP-0020) |
| An unconfirmed payment parent | No | A proposal of its own |

## Motivation

The anchor of a v4 grant commits to the signed preparation (LIP-0020
section 8), and a preparation is data: whoever holds a copy can compute the
commitment. If the anchor could be funded by any confirmed coin, any such
holder could publish it, for example a recipient that was handed the signed
grant early, a transport or a store. The issuer would have signed and would
no longer decide whether the grant is issued. The linkage output answers
that. It is the output that follows the seal in the seal transaction. The
grant names the seal, the transaction is fixed before the grant is signed,
and only the holder of the key of that one output can spend it into an
anchor.

The second question is which parents may be unconfirmed. A seal transaction
and its anchor in one block make an issuance fast, and the anchor then
spends an output that is not yet confirmed. LIP-0008 permits that for the
linkage and for a payment output and for nothing else. A verifier needs a
rule that it can apply to the inputs it sees: an input that spends the
linkage output of the named seal transaction may have a pending parent, and
no other input may.

## Current state

- LIP-0008 sections 1.1 and 9 state the Witness profile: every input of the
  seal transaction and of the anchor is a native witness key hash with
  `SIGHASH_ALL`, ordinary funding is confirmed, and two unconfirmed
  dependencies are permitted.
- The reference laboratory implements a linkage-only subset of that profile
  for Grant v3 (`swarma-chain-lab` at
  `b03c6f10fad1be135e780d8b1f556fc46805eb06`: `experiments/WITNESS-PROFILE.md`,
  `experiments/single-use/witness.go`,
  `experiments/single-use/witness_observation.go`). Its configuration pins
  the profile, and a missing value, an unknown value and the Legacy profile
  refuse. It checks every input of both transactions on their octets and
  verifies each signature itself. It requires confirmed funding below the
  spender's block and refuses an unconfirmed payment parent. It reports
  stable reasons, whose names begin with `W_`.
- That subset requires the linkage only where the seal transaction is
  pending or shares the anchor's block. Where the seal transaction is
  confirmed in an earlier block, it admits an anchor that is funded
  independently. It takes as the linkage output whichever output of the
  seal transaction the anchor spends, the seal excepted, and admits at most
  one such input.
- The laboratory's document names cases that run on regression test nodes:
  a seal transaction and an anchor in one block, refusals, and the
  confirmation of funding. They were not run for this LIP.
- LIP-0020 fixes the one `OP_RETURN` output of a v4 anchor, with the
  commitment and the pointer (W8.5).

## Proposal

The seal transaction is called `T` and the anchor `A`, as in LIP-0008
section 9. The linkage output is an output of `T` and has no letter here,
because `L` also names the Legacy profile.

### 1. The profile

A verifier takes the construction profile from its own authenticated
configuration, and nothing that a presenter sends selects it.

| Rule | Requirement |
| --- | --- |
| C1.1 | The verifier's authenticated configuration states the construction profile of the pinned chain, and for this profile the value is `W`. A missing value, any other value and the Legacy profile refuse. There is no fallback from one profile to another (LIP-0008 section 1.1). |
| C1.2 | A witness in a transaction, a field of a presentation and the script of an output select no profile. |

Where a grant will carry the pin of its construction profile is open
(LIP-0008 section 1.1). Until that member exists, the verifier's
configuration is the only place.

### 2. The two transactions

The linkage output of a grant is the output that follows its seal in the
seal transaction. The anchor spends that output, no other output of the
seal transaction, and never the seal.

| Rule | Requirement |
| --- | --- |
| C2.1 | `T` is the transaction that holds the output which the grant names as its seal. The named output index exists in `T`. |
| C2.2 | `A` is the transaction that carries the frame of LIP-0020 W8.5 in its one `OP_RETURN` output. |
| C2.3 | The linkage output of the grant is the output of `T` whose index is the index of the seal plus one. It exists, and its script is a witness key hash, the octets `00 14` and 20 further octets. Exactly one input of `A` spends an output of `T`, and it spends the linkage output; that input is the linkage input. |
| C2.4 | No input of `A` spends the seal. |
| C2.5 | An issuer signs a grant only where the linkage output of its seal pays a key that the issuer's own signer holds. A verifier cannot check this rule: it sees a script and not the holder of its key. |

For a grant whose seal is output 2 of `T`, the linkage output is output 3
of `T`, and an anchor of that grant has exactly one input from `T`, which
spends output 3.

C2.3 holds for every grant, also where `T` was confirmed long before `A`.
The reference subset asks for the linkage only while `T` is pending or in
the block of `A`, and it takes as the linkage whichever output of `T` the
anchor spends. This profile is stricter on both points, for one purpose.
The grant names its seal as an output of `T`, and `T` is fixed before the
grant is signed. The issuer's signature over the seal outpoint therefore
fixes the output after the seal as well, and with it the key that this
output pays. An anchor that spends that output comes from the holder of
that key. An anchor that is funded by any other coin could come from
anybody who holds the preparation. So could an anchor that spends another
output of `T`: a seal transaction can pay change, or pay a third party, and
the holder of such an output can sign an input that spends it. Under C2.3
such an anchor refuses. The cost is one more output in every seal
transaction, a fixed place for it, and a key that the issuer's signer keeps
until the anchor is built.

C2.5 is the issuer's half of the rule. A verifier takes the output after
the seal as the linkage output, whoever holds its key. An issuer that
signed a grant whose seal is followed by an output of another party would
have given that party the anchor.

`T` may hold more than these two outputs: change, payments, and the seals
of other grants, each followed by its own linkage output. This profile
reads the seal that the grant names and the output after it. The output
that follows the seal of one grant is the linkage output of that grant
alone.

### 3. The inputs

Every input of `T` and of `A` spends a witness key hash and carries a
signature of hash type `01` and the key in its witness.

| Rule | Requirement |
| --- | --- |
| C3.1 | For every input of `T` and of `A`: the script of the spent output is a witness key hash, exactly `00 14` and 20 octets; the unlocking script is empty; the witness has exactly two items. The first is a signature with its hash-type octet, 9 to 73 octets, and its last octet is `01`. The second is a compressed public key of 33 octets, and the RIPEMD-160 of its SHA-256 is the 20 octets of the spent output. |
| C3.2 | The verifier checks C3.1 itself, on the octets of the transaction and of the spent outputs that its node supplied in one observation (LIP-0022 section 1). That a signature is valid is established by the node that validated the transaction; a verifier MAY verify it again. |

A key hash without a witness, a script hash that wraps a witness key hash,
a witness script hash and a Taproot output all fail C3.1, and so does a
name output: its script begins with a name prefix and is no witness key
hash, in whatever script the name is held (LIP-0021 section 3). The
historical anchor of v0.1 spends a name output and is no anchor of this
profile.

The hash type `01` is `SIGHASH_ALL` without `ANYONECANPAY`. For a witness
key hash it commits to every input and every output of the transaction and
to the amount of the spent output. Because every input is such a witness
input, nobody but the signers can change the transaction id of `T` or of
`A`: the id does not cover the witness, and nothing outside the witness can
be changed without a new signature. That is what lets a grant name `T`
before `T` is confirmed.

The reference laboratory verifies every signature itself and requires a
strictly encoded signature. This profile leaves that to an implementation,
because the node has validated every transaction that it supplies, a
pending one included.

### 4. Funding and order

The input that spends the linkage output may have a pending parent, and no
other input may.

| Rule | Requirement |
| --- | --- |
| C4.1 | Every input of `T` spends an output of a transaction that is confirmed. Where `T` is confirmed, that transaction is in a block below the block of `T`. |
| C4.2 | Every input of `A` other than the linkage input spends an output of a transaction that is confirmed. Where `A` is confirmed, that transaction is in a block below the block of `A`. |
| C4.3 | Where `A` is confirmed, `T` is confirmed in a lower block, or in the same block at an earlier position. |
| C4.4 | A payment output is no exception. An input of `A` that spends an unconfirmed payment output of the same chain fails C4.2. |

A parent in the spender's own block counts as unconfirmed, because it was
not confirmed when the spender entered the block. A confirmed parent ends
the check: this profile does not read the parents of a confirmed parent,
and a coinbase output may fund either transaction once consensus lets it be
spent.

C4.3 follows from consensus once C2.3 holds, since `A` spends an output of
`T`. A verifier checks it all the same on the facts of its observation; a
violation shows that those facts are inconsistent.

C4.4 is narrower than LIP-0008 section 1.1, which permits the unconfirmed
payment output. A verifier can recognise the linkage output without help:
it is the output after the seal in the named `T`. It cannot recognise a
payment output: nothing that a grant signs today says which output pays for
it. Until a proposal fixes that, an unconfirmed payment is indistinguishable
from arbitrary unconfirmed funding, and this profile refuses it. The cost
is that a payment has to be confirmed before the anchor that spends it is
built.

### 5. When an effect may rest on the construction

A verifier admits no effect while the anchor is pending.

| Rule | Requirement |
| --- | --- |
| C5.1 | Admission requires that `A` is confirmed on the active chain of the observation. A pending `A` passes the checks of sections 2 to 4 and gives no authority. |
| C5.2 | `T` and `A` may be confirmed in one block. The depth that a rule asks of the anchor is counted under LIP-0022 section 5. |

LIP-0008 section 1.1 says it in general: no observation of pending
transactions alone authorizes an effect. A profile that lets an effect rest
on a pending anchor is the separate profile without a block wait that
LIP-0008 section 10 names, and it is not proposed here.

### 6. Replacement

A grant names `T` by its transaction id, so another `T` needs another
grant, and another `A` for the same grant needs nothing new.

| Rule | Requirement |
| --- | --- |
| C6.1 | An issuer fixes `T` before it signs the grant and does not build it again. Where `T` cannot be confirmed and the issuer builds another seal transaction, that transaction has another id, the grant does not name it, and the issuer signs a new grant. The parties sign again what changed, and under LIP-0020 W7.9 the recipient consents again. |
| C6.2 | An issuer MAY replace a pending `A` by another anchor that spends the same linkage output and carries the same frame, for example at a higher fee. Nothing that was signed changes. A verifier reads the anchor that is confirmed, and a presentation names that one. |

Both anchors of C6.2 spend one output, so at most one is confirmed. A
reference to the id of an anchor that was replaced is void, as LIP-0008
section 1.1 says of pending references.

### 7. Refusals and their order

A verifier reports the first refusal of the order below. None of them
records a closure.

| Code | What it reports | Rule |
| --- | --- | --- |
| `W_PROFILE_REQUIRED` | The configuration states no profile, another one, or the Legacy profile | C1.1 |
| `W_SEAL_OUTPUT` | The named seal is no output of `T` | C2.1 |
| `W_WITNESS_REQUIRED` | The transaction carries no witness for any of its inputs | C3.1 |
| `W_UNCONFIRMED_NON_LINKAGE_PARENT` | An input other than the linkage input spends an output that is pending or lies in the spender's own block or above it | C4.1, C4.2, C4.4 |
| `W_NATIVE_P2WPKH_REQUIRED` | A spent output is no witness key hash, or an unlocking script is not empty | C3.1 |
| `W_WITNESS_SHAPE` | The witness of an input does not have exactly its two items in their sizes | C3.1 |
| `W_SIGHASH_ALL_REQUIRED` | The last octet of a signature is not `01` | C3.1 |
| `W_PUBLIC_KEY` | The second item is no compressed public key, or it does not hash to the 20 octets of the spent output | C3.1 |
| `W_ISSUANCE_SPENDS_SEAL` | `A` spends the seal | C2.4 |
| `W_LINKAGE_SCRIPT` | `T` has no output after the seal, or that output is no witness key hash | C2.3 |
| `W_LINKAGE_REQUIRED` | No input of `A` spends the linkage output, or an input of `A` spends another output of `T` | C2.3 |
| `W_DEPENDENCY_ORDER` | `A` is confirmed and `T` is pending, in a higher block, or later in the same block | C4.3 |
| `W_ANCHOR_PENDING` | `A` is not confirmed | C5.1 |

Twelve of these names are stable reasons of the reference laboratory. Ten
have the meaning that it gives them. `W_LINKAGE_REQUIRED` is wider here,
because this profile asks for the linkage always and for one fixed output.
`W_LINKAGE_SCRIPT` reports the script of that fixed output, where the
laboratory reports the script of whichever output of `T` the anchor spends.
`W_ANCHOR_PENDING` is new. The laboratory reports further reasons for reads
of its own, such as a transaction that does not match its id; under this
specification those are matters of the observation (LIP-0022).

C7.1. The order is: the profile; for `T`, the seal output, then the
presence of a witness, then the funding of all its inputs, then the form of
each input in the order of the inputs; for `A`, the spend of the seal, then
the linkage output of `T`, then the inputs of `A` that spend outputs of
`T`, then the order of `T` and `A`, then the presence of a witness, then
the funding of its other inputs, then the form of each input in the order
of the inputs; last, the confirmation of `A`. For one input the form is
checked in this order: the spent output and the unlocking script, the shape
of the witness, the hash type, the key.

The frame of the anchor is checked under LIP-0020 (`ISSUANCE_FRAME`), and
that check stands where LIP-0020 W9.4 puts it.

### 8. Vectors

[`vectors/LIP-0023/construction-vectors.json`](../vectors/LIP-0023/construction-vectors.json)
holds 63 vectors over the 18 rules of this LIP.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `inputs` | 1 passing, 18 refused, 3 compound | C3.1 on the octets of a spent script, of an unlocking script and of the items of a witness, with the order of C7.1 for an input that has two defects |
| `graphs` | 7 passing, 25 refused, 9 compound | Sections 1, 2, 4 and 5 and the order of C7.1 on a stated pair of transactions: their blocks and positions, their outputs, and for each input its parent and the result of C3.1. Nine of them test the fixed place of the linkage output, among them a seal transaction with an output of another party, one with the seals of two grants, and one whose seal is its last output |

A vector whose outcome is not the passing one holds one defect, states the
expected code and names a neighbour with the passing outcome that differs
from it in that defect. A vector marked compound holds two defects, states
the one that the order reports and names no neighbour. The list `rules` of
the file names for each rule its section, its state, which is `proposed`
for all, its vectors and what no vector covers.

The limits of the file are these. The keys are the compressed forms of the
published test keys of BIP-340 and belong to nobody. The octets of
signatures are placeholders, and no signature in the file verifies. The
group `graphs` states facts and holds no transaction: no vector there has a
transaction id, an amount or a fee. Who holds the key of an output is said
in the claim of a vector and is no fact that a checker reads. No vector
reads a node.

No checker for these vectors is in this repository. The expected outcomes
were stated by hand, computed by one implementation and decided again by a
second one that shares no code with the first; neither is published here.
Both come from the author of this text, so an error of understanding that
they share is in the vectors. The vectors bind nothing until both owners
accept the rules that they follow.

## Sources

No node was run for this LIP.

| Statement | Source |
| --- | --- |
| The reference subset: the pinned profile, the form of every input, confirmed funding below the spender, the linkage where the seal transaction is pending or shares the anchor's block, the linkage output as whichever output of the seal transaction the anchor spends, no unconfirmed payment parent, and the reasons that it reports | `swarma-chain-lab` at `b03c6f10fad1be135e780d8b1f556fc46805eb06`: `experiments/WITNESS-PROFILE.md`; `experiments/single-use/witness.go`, `VerifyWitnessInputs`; `experiments/single-use/witness_observation.go`, `WitnessCreation` and `WitnessIssuance` |
| A transaction id does not cover the witness, and a signature of hash type `01` over a witness key hash commits to every input, every output and the spent amount | BIP141 and BIP143, which LIP-0008 section 1.1 cites |
| A witness key hash is spent by a witness of exactly two items | Namecoin Core at the tag `nc28.0`, `src/script/interpreter.cpp`, `VerifyWitnessProgram` |
| The main chain enforces the witness rules from height 475000 | The same tag, `src/kernel/chainparams.cpp` |

## Alternatives

- **The linkage only where the seal transaction is pending or in the
  anchor's block**, as the reference subset has it. A seal from a pool that
  was confirmed earlier would need no linkage output. Any holder of the
  preparation could then publish the anchor of such a grant.
- **Any output of the seal transaction as the linkage**, as the reference
  subset has it: the verifier takes the output that the anchor spends. A
  seal transaction could order its outputs freely. Whoever holds another
  witness output of that transaction, for example its change or a payment
  to a third party, could then publish the anchor with a copy of the
  preparation.
- **A member of the grant that names the linkage outpoint.** The linkage
  output could stand anywhere in the seal transaction. Every grant would
  carry one more outpoint in a member that does not exist yet, and a
  verifier would have one more value to compare. The fixed place after the
  seal needs no octet, because the signature over the seal outpoint covers
  it.
- **The unconfirmed payment parent now.** An issuance could wait for one
  block and not for two. The verifier would have to trust an unsigned
  statement about which output is the payment, or to guess it from a
  script.
- **Verification of every signature by the verifier**, as the reference
  subset does. It would not rest on the node for that one fact. The node
  that supplied the transaction has validated it, and a verifier already
  rests on its node for the chain.
- **A profile that also covers name outputs as inputs**, so that an anchor
  could update a name as the anchor of v0.1 does. A name output is no
  witness key hash as section 3 requires, and an update of the issuer's
  name on every issuance would lengthen every walk of that name (LIP-0021
  section 6).

## Security consequences

- **The anchor is an act of the holder of the linkage key.** That key is
  as sensitive as the decision to issue: a party that obtains it and holds
  the preparation can publish the anchor of that grant. Which account holds
  the key is a matter of the seal profile.
- **The output after the seal decides who can publish.** A verifier reads
  its script and cannot see who holds its key. The rule shows that the
  holder of that key published the anchor; that this holder is the issuer's
  signer is the issuer's own care (C2.5).
- **The grant is signed before the anchor exists.** Between the two the
  issuer can still withhold the anchor. After the anchor is broadcast it
  cannot: anybody can broadcast a signed transaction again.
- **A parent in the same block is treated as pending.** A funding
  transaction that is confirmed together with its spender was not confirmed
  when the spender was built, and the rule does not let block inclusion
  hide that.
- **The profile reads no further than one parent.** A confirmed parent is
  taken as it is. What funded it is not read, since nothing about a
  confirmed transaction can change without a reorganisation, and a
  reorganisation voids the observation (LIP-0022).
- **A verifier that takes the profile from a presentation has none.** C1.2
  is what keeps a presenter from choosing the rules.

## Conformance impact

None on normative v0.1 and none on Grant v3: the reference subset and its
reasons stay as the laboratory has them. No conformance class is added. The
pairs of LIP-0008 on the Witness profile get their meaning for a first
profile from sections 2 to 5, with one difference that this LIP states: the
pair with a permitted unconfirmed parent holds here for the linkage output
alone.

## Open questions

- **The owners' acceptance** of the linkage as a rule for every grant, of
  its fixed place after the seal, of the refusal of an unconfirmed payment
  parent, of the form of an input and of the thirteen codes with their
  order.
- **The unconfirmed payment parent.** What a grant has to sign so that a
  verifier can tell a payment output from other funding.
- **The pin of the profile in a grant**, and the form of the verifier's
  configuration that holds it today.
- **The linkage key.** Which account derives it, and who may sign with it;
  both belong to the seal profile.
- **The place of the linkage output.** This draft fixes it as the output
  after the seal, also in a seal transaction that holds the seals of
  several grants. A member of the grant that names the outpoint is the
  alternative, and the owners choose.
- **The Legacy profile**, which LIP-0008 keeps as specification only until
  a chain without the witness rules is pinned.
- **A run on nodes** of the cases that the laboratory names, under the
  rules of this profile.
