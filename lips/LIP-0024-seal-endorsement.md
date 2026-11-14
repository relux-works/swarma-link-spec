# LIP-0024: Seal and endorsement profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** the octets of the seal-key endorsement of a v4 grant, the
  script of its seal on Namecoin, and the checks by which a verifier accepts
  a seal and attributes a spend of it to the issuer
- **Builds on:** LIP-0008 sections 5.1 and 11 to 11.3, LIP-0020 sections 1
  to 6 and 9, LIP-0021 section 2 and LIP-0023 sections 1 and 2

## Summary

A v4 grant has a seal with a key of its own, and a verifier accepts that
seal, and calls a spend of it the issuer's, only under an endorsement that
the issuer's grant key signed. LIP-0008 section 11.2 fixes what the
endorsement states and the order in which a verifier checks it, and it
leaves the octets and the refusal codes open. LIP-0020 registers the type
`swarma-seal-endorsement/1` and gives it no member. Until the members
exist, no reader accepts an endorsement, and so no reader accepts a seal.

This LIP proposes the octets:

- the seal of the first profile: a revocable-only seal whose script is the
  witness key hash of the seal key (section 1);
- the members of `swarma-seal-endorsement/1`, their forms and the largest
  size (section 2);
- the checks in the order that LIP-0008 fixes, with the parsing steps of
  LIP-0020 before them and with refusal codes (section 3);
- what a verifier may do with a seal after the checks (section 4);
- five points about the provisioning and custody of the seal account, as a
  proposal that awaits an owner's choice (section 5);
- vectors (section 6).

Where the seal key is kept is not decided, and this LIP does not decide it.
Beyond the five points of section 5 the provisioning and custody of the
seal account stay open, and so do the seal of a child grant and the
single-use seal. The section "Open questions" says what each waits for.

## What is decided and what is proposed

The meaning of the endorsement is decided, and its octets are not. LIP-0008
section 11.2 records Ivan Oparin's decision of 2026-11-14, with the
co-author's agreement pending: the eight members by their meaning, and the
order of the verifier's five steps. Section 11.1 records his decision of
2026-11-11 that the revocable-only seal has the single-key script of its
construction profile, which under the Witness profile is a native witness
key hash, and that its indices are not hardened by default. Section 11.3
records his decision of 2026-11-14, with the co-author's agreement pending,
that the signer shows before issuance that it can spend the seal. This LIP
changes none of the three.

Every rule of sections 1 to 4 is the draft's proposal for carrying those
decisions in octets: the names and forms of the members, the two members
that write the profile, the choice of the grant's identifier as the
reference, the largest size, the place of the parsing steps before the five
decided steps, the bindings that step 4 gains, and the five new codes.
Neither owner has decided them, and nothing of them is implemented. The
owners accept or change them through this LIP, under LIP-0001.

The provisioning and custody of the seal account are open, and the question
is before an owner. Section 5 states five points as the draft's proposal
and proposes nothing else about custody. No rule of sections 1 to 4 and no
vector depends on them: a verifier cannot see how an issuer keeps its
keys.

| Decided in LIP-0008 section 11.2 | Proposed here |
| --- | --- |
| The members "are named by meaning, and their bytes stay open" | Section 2 |
| The order of the five steps | Section 3 keeps the order and says where the parsing of the object stands |
| "The refusal codes come with the bytes" | Section 3 |
| The reference is "the grant, or the signed preparation" | The identifier of the grant (E2.1) |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The reader of an endorsement: its octets, its members, its signature (sections 2 and 3) | Yes, on the common layer of LIP-0020 | The owners' acceptance |
| The checks against a grant: the same outpoint, the same issuer pin, the grant's identifier | Only on stated facts | The members of the grant (LIP-0020) |
| The read of the seal output on a node | No | The observation (LIP-0022) and a run on a node |
| The issuer's side: deriving the seal key, recording its index, the recorded revocation | No | The provisioning and custody of the seal account, which is open |
| The endorsement of a child's seal and of a single-use seal | No | LIP-0014 sections 9.1 and 11.1 for the child; the output profile of the single-use seal (LIP-0008 section 11.1) |

## Motivation

A grant names its seal by an outpoint, and an outpoint says nothing about
who can spend it. In v3 the seal pays the grant key, so a verifier that
knows the issuer knows the script. In v4 every seal has a key of its own,
and nothing on the chain connects that key with the issuer. Without a
statement of the issuer a verifier cannot tell whether the output is a seal
of the profile at all, and it cannot call a spend of it the issuer's
revocation (LIP-0008 sections 5.1 and 11).

The decision of LIP-0008 says which statements close that gap. The octets
decide whether two implementations read one endorsement alike, and in one
point they decide more: the order. The decided order has a verifier read
the output on its own node before it verifies the signature. The pipeline
of a signed object in LIP-0020 verifies the signature before any rule of
the object. An implementation that followed the pipeline would report a bad
signature where the decision asks for a report about the script.

## Current state

- LIP-0008 section 11.2 names the members by meaning and fixes the order
  of the checks.
- LIP-0020 registers `swarma-seal-endorsement/1`, signed by the issuer's
  grant key, with no member, and a reader refuses a payload of that type as
  `WIRE_TYPE`.
- LIP-0021 fixes the form of a key that controls an output, and LIP-0023
  names the value `W` of the construction profile.
- In Grant v3 the seal pays the grant key (LIP-0004 section 5), and v3 has
  no endorsement. The reference laboratory pins that seal for its issuer
  (`swarma-chain-lab` at `b03c6f10fad1be135e780d8b1f556fc46805eb06`,
  `experiments/WITNESS-PROFILE.md`).
- The key map proposes, as a layout that each owner decides, the funding
  account at `m/84'/7'/0'` and seal keys in an account of 10 or above
  (`KEY-MAP.md`, "Proposed key layout").

## Proposal

### 1. The seal of the first profile

The seal of this profile is a revocable-only seal under the Witness
profile: an output that pays the witness key hash of its own seal key.

| Rule | Requirement |
| --- | --- |
| E1.1 | The seal is revocable-only: only its issuer spends it, and every spend of it is a revocation (LIP-0008 section 11.1). |
| E1.2 | The script of the seal is a witness key hash: the octets `00 14`, then the RIPEMD-160 of the SHA-256 of the 33 octets of the compressed seal key. |
| E1.3 | The seal is an output of the seal transaction of LIP-0023, at the outpoint that the grant names. |

E1.2 writes out, for Namecoin under the Witness profile, the decision of
LIP-0008 section 11.1. Where the seal key comes from, that its index is
used once, and that the signer records a signed spend of the seal before it
signs the grant are rules of LIP-0008 sections 11.1 and 11.3 for the
issuer. A verifier sees none of them and refuses for none of them.

### 2. The endorsement

An endorsement is a signed object of LIP-0020 whose payload has nine
members, signed by the issuer's grant key.

E2.1. The payload of type `swarma-seal-endorsement/1` has exactly these
members:

| Member | Form | Meaning in LIP-0008 section 11.2 |
| --- | --- | --- |
| `type` | string | `swarma-seal-endorsement/1` |
| `genesis` | 64 hexadecimal characters | Network and genesis: the hash of the genesis block of the chain on which the seal exists |
| `issuer` | object with exactly `name`, `registration` and `owner` | Issuer pin |
| `issuer.name` | string of 1 to 255 characters of printable ASCII | The name of the issuer, exactly as the grant binds it |
| `issuer.registration` | object with exactly `txid`, 64 hexadecimal characters, and `vout`, a number from 0 to 4294967295 | The registration of that name |
| `issuer.owner` | owner pin (LIP-0021 O2.1) | The owner key of that name |
| `construction` | string of 1 to 32 characters of printable ASCII | Profile: the construction profile, `W` |
| `seal` | string of 1 to 32 characters of printable ASCII | Profile: the kind of seal, `revocable-only` |
| `outpoint` | object with exactly `txid` and `vout`, as in `issuer.registration` | Outpoint: the transaction and the output index of the seal |
| `seal_public_key` | compressed public key in the form of LIP-0021 O2.1 | Seal public key |
| `script` | lowercase hexadecimal, an even number of characters from 2 to 200 | Script: the exact octets of the seal's script |
| `grant` | 64 hexadecimal characters | Reference: the identifier of the grant (LIP-0020 section 6) |

E2.2. The signed form has exactly `payload` and `signature` (LIP-0020
section 5) and at most 2048 octets. The signature is by the issuer's grant
key over the typed digest of the payload, whose tag is the type string
(LIP-0020 section 4): the domain that LIP-0008 asks for.

E2.3. `issuer.owner` and `seal_public_key` are keys that control an output
and no signing keys. Their form is the form of an owner pin, and a value in
that form that is no point of the curve refuses in the member step, in the
place where LIP-0020 W9.3 checks signing keys.

The decision lets the reference be the grant or the signed preparation.
This draft takes the identifier of the grant. It exists as soon as the
payload of the grant is fixed, before any signature, so the issuer can sign
the endorsement and the grant in one sitting. The preparation exists only
after the consent, and an endorsement that named it could not be made
before the recipient had answered.

The two profile members are written apart so that each has one value today
and each can gain values on its own: another construction profile, and
another kind of seal.

A name that holds an octet outside printable ASCII has no endorsement in
this profile, as it has no consent under LIP-0020 W7.3.

An endorsement holds no secret and gives no authority. It says which key
and which script the issuer's grant key stands behind for one outpoint and
one grant.

### 3. The checks and their order

A verifier parses the endorsement, then makes the five steps of LIP-0008
section 11.2 in their order, and reports the first refusal.

E3.1. The order is:

| # | Step | Check | Refusal |
| --- | --- | --- | --- |
| 1 | Parsing | The document, the signed form, the `type` and the members of the payload, as steps 1 to 4 of the pipeline of a signed object (LIP-0020 W9.1), with E2.3 | The codes of LIP-0020: `WIRE_SIZE` to `WIRE_NOT_CANONICAL`, `WIRE_TYPE`, `WIRE_MEMBER`, `WIRE_INTEGER`, `WIRE_KEY` |
| 2 | Decided step 1 | The verifier's own node supplies the output at `outpoint` | `SEAL_OUTPUT` |
| 3 | Decided step 1 | The script of that output equals `script`, octet for octet | `SEAL_SCRIPT` |
| 4 | Decided step 2 | `construction` is the construction profile of the verifier's configuration (LIP-0023 C1.1), and `seal` is a kind that the verifier supports | `SEAL_PROFILE` |
| 5 | Decided step 2 | `script` is the script of E1.2 for `seal_public_key` | `SEAL_SCRIPT_KEY` |
| 6 | Decided step 3 | The encoding of the signature, the key of the place and the signature, as steps 5 to 7 of the pipeline of a signed object. The key of the place is the grant key of the pinned issuer | `WIRE_SIGNATURE_FORM`, `WIRE_KEY`, `WIRE_SIGNATURE` |
| 7 | Decided step 4 | The grant names `outpoint` as its seal. `grant` is the identifier of that grant, and `genesis` and `issuer` are the chain and the issuer pin that the grant binds | `SEAL_BINDING` |
| 8 | Decided step 5 | The seal is accepted (section 4) | |

The parsing stands first because nothing can be compared before the object
is read. It verifies no signature. From row 2 on the order is the decided
one, and it differs from the pipeline of a signed object in LIP-0020 W9.1
in one point that this rule states: the read of the output and the check of
the script stand before the signature. An endorsement with a wrong script
and a wrong signature refuses as `SEAL_SCRIPT`.

Row 7 adds three bindings to the one that the decision names. The decision
has the verifier check that the grant names the same outpoint. Without the
other three an endorsement of another grant of the same issuer, of the same
issuer on another chain, or of an issuer under another registration of the
same name would pass for an output that happens to match. They are this
draft's addition, and they stand in the decided step because they concern
the same question: whether the endorsement speaks of this grant.

| Code | Meaning |
| --- | --- |
| `SEAL_OUTPUT` | The verifier's node supplies no output at the endorsed outpoint. Nothing is proved about the seal |
| `SEAL_SCRIPT` | The output exists and has another script than the endorsed one |
| `SEAL_PROFILE` | The endorsement is for another construction profile than the verifier's, or for a kind of seal that the verifier does not support |
| `SEAL_SCRIPT_KEY` | The endorsed script is not the script of this profile for the endorsed key |
| `SEAL_BINDING` | The endorsement speaks of another grant, another chain, another issuer pin or another outpoint than the grant's |

None of the five records a closure. A grant whose endorsement refuses is
not admitted, and nothing is said about its seal.

### 4. What a verifier does with an accepted seal

Only an endorsement that passed all checks lets a verifier treat the output
as the seal of the grant.

| Rule | Requirement |
| --- | --- |
| E4.1 | A verifier admits a v4 grant only with an endorsement of its seal that passed E3.1 in the same observation (LIP-0022). |
| E4.2 | After the checks, a spend of the endorsed output that the verifier validated is the issuer's spend. For a revocable-only seal it is a revocation, and it closes the grant under LIP-0008 section 5.1. |
| E4.3 | An output that no accepted endorsement covers is no seal of the grant. A spend of it closes nothing, and the absence of a spend admits nothing. |

E4.2 is the fifth step of the decision. For the revocable-only seal there
is one branch: whoever spends the output holds the seal key, and the issuer
stood behind that key. The seal of a single-use grant has two branches, and
this profile does not cover it.

### 5. Provisioning and custody of the seal account

How a seal account is created, kept and recovered is open, and the question
is before an owner. The draft proposes five points about it and nothing
beyond them.

| Rule | Proposal |
| --- | --- |
| E5.1 | The seal account and the funding account are separate accounts. No key pays a seal and also funds a transaction. |
| E5.2 | The grant key signs no transaction and pays no fee: no input of a seal transaction, of an anchor or of a revocation spends an output that the grant key controls. |
| E5.3 | The seal account is not the account `m/84'/7'/0'`, and no key of that account is a seal key. |
| E5.4 | No seal account is derived from a grant key. The private key that a v3 installation stores for its grant key is no seed of a v4 account. |
| E5.5 | A seal account is created in a provisioning sitting of its own, which its owner attends, and its key material is wrapped by itself, so that unwrapping one account yields no other. |

E5.1 and E5.2 repeat, as rules of this profile, what LIP-0008 section 11.1
states in its first rule: the seal account is separate from the funding
account, and the grant key signs no transaction. The second is why v4
leaves the seal of v3, which pays the grant key: one secret would sign
grants under BIP-340 and spends under ECDSA.

E5.3 keeps seal keys out of the account that the key map proposes for
funding. An extended public key together with one private key below it
reveals the other private keys of an account (LIP-0008 section 11.1), so a
seal key in the funding account would tie the two custodies together.

E5.4 keeps a v4 account from inheriting the exposure of a key that already
signs. A grant key is one private key and no seed. An account derived from
it would be only as safe as that key, and one leak would give away the
right to sign grants and the right to revoke them together.

E5.5 costs a sitting for each account. In return a signer can be given the
seal account without the funding account, and a recovery of one account
does not open another.

Everything else about custody stays open: the steps of the sitting and what
the owner confirms in it; the recovery of an account; which account indices
may hold seal keys; what the signer records for an index and what keeps
that record from being rolled back; what happens when an index gives no
valid key or the indices run out; the import of the account's public
descriptor into a watch-only wallet; and the fee of the recorded revocation
of LIP-0008 section 11.3, with its replacement. A verifier sees none of
this and refuses for none of it.

### 6. Vectors

[`vectors/LIP-0024/endorsement-vectors.json`](../vectors/LIP-0024/endorsement-vectors.json)
holds 47 vectors over the 15 rules of this LIP.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `scripts` | 1 seal script, 5 others | E1.2 on a compressed key and a script |
| `endorsements` | 2 passing, 31 refused, 8 compound | E3.1 on the octets of a signed endorsement and a stated context: the grant key of the pinned issuer, the output that the node supplies, the verifier's construction profile, and the facts of the grant |

A vector whose outcome is not the passing one holds one defect, states the
expected code and names a neighbour with the passing outcome that differs
from it in that defect. A vector marked compound holds two defects, states
the one that the order of E3.1 reports and names no neighbour. The list
`rules` of the file names for each rule its section, its state, which is
`proposed` for all, its vectors and what no vector covers.

The five rules of section 5 have no vector: they are about the issuer's
custody, which a verifier cannot see.

The limits of the file are these. The signatures are real BIP-340
signatures under published test keys, which belong to nobody. The grant is
given as stated facts, because a grant has no members yet: its identifier,
its seal outpoint, its chain and its issuer pin are values of the context,
and the identifier is a placeholder. Names, transaction ids and the octets
of the registration are placeholders. The vectors for the first row of E3.1
hold defects of the members of this type; the defects of a document as such
are in the vectors of LIP-0020. No vector reads a node.

No checker for these vectors is in this repository. The expected outcomes
were stated by hand, computed by one implementation and decided again by a
second one that shares no code with the first; neither is published here.
Both come from the author of this text, so an error of understanding that
they share is in the vectors. The vectors bind nothing until both owners
accept the rules that they follow.

## Alternatives

- **The signed preparation as the reference.** It would bind the
  endorsement to the consent as well. It exists only after the recipient
  answered, so the issuer would need a second sitting for the endorsement.
- **One member for the profile**, for example `W/revocable-only`. It is one
  string to compare. A new kind of seal under the same construction profile
  would then be a new value that has to repeat the first half.
- **The pipeline of a signed object unchanged**, with the signature before
  every other check. It is the order that every other type of LIP-0020 has.
  It is not the order that LIP-0008 section 11.2 fixes.
- **The seal key as an x-only key**, like a signing key. The script hashes
  the compressed key, so the parity is part of what the endorsement states
  (LIP-0021 section 2).
- **No script member**, since this profile's script follows from the key.
  The decision lists the script as a member, and a later kind of seal has a
  script that does not follow from one key.

## Security consequences

- **The endorsement is what makes a seal the issuer's.** A verifier that
  accepts a seal without it accepts an output that its issuer may be unable
  to spend, and then a grant that nobody can revoke.
- **The grant key signs endorsements.** A thief of the grant key can
  endorse a seal key of its own for a grant that it signs, as LIP-0008
  section 5.2 says of such grants. The endorsement does not limit a stolen
  grant key; the rules about the issuer's name do.
- **A valid endorsement does not show that the issuer can spend the seal.**
  It shows that the grant key stood behind a key and a script. That the
  signer holds the key is the duty of LIP-0008 section 11.3, which a
  verifier cannot see.
- **The read of the output comes before the signature.** A verifier makes a
  read on its node for an endorsement whose signature it has not verified.
  The read is of one transaction, and the parsing bounds the size of what
  was presented.
- **The bindings of row 7 rest on the grant.** Until a grant has members, a
  verifier has no octets to take them from, and an implementation that
  takes them from a presenter has not made the check.

## Conformance impact

None on normative v0.1 and none on Grant v3, whose seal pays the grant key
and has no endorsement. No conformance class is added. The pair of LIP-0008
on a typed endorsement for the exact key, script and outpoint of a seal
gets its octets and its codes from sections 2 and 3.

## Open questions

- **The owners' acceptance** of the members and their forms, of the grant's
  identifier as the reference, of the place of the parsing before the
  decided steps, of the three added bindings and of the five codes; and an
  owner's choice on the five points of section 5.
- **The provisioning and custody of the seal account.** The question is
  before an owner. Section 5 proposes five points and lists what stays open
  beyond them.
- **The linkage key of LIP-0023.** LIP-0008 section 11.1 has the seal
  account hold seal keys alone, so the linkage key is outside it. Which
  account holds it belongs to the same question of custody.
- **The seal of a child grant.** Who endorses it, and who records that it
  can be spent, do not yet fit together: under the Draft text of LIP-0014
  section 11.1 the delegation key signs child grants and nothing else. One
  option is that the grant-key service of the root endorses the exact child
  preparation while a seal service of the delegating operator holds the
  child's seal key and its recorded revocation; that costs one exchange
  with the root's service for each child. Another is a separately trusted
  authority for the endorsements of children. In neither does the service
  that holds the delegation key hold a seal key or a funding key. The
  owners have not chosen.
- **The single-use seal**, whose output profile LIP-0008 section 11.1
  leaves open, and with it the second value of `seal`.
- **A spend proof that a verifier can see**, which LIP-0008 section 11.3
  calls optional and does not define.
- **A second implementation in Swift**, which LIP-0008 asks for before any
  claim of interoperability.
