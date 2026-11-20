# LIP-0020: Wire registry for Grant v4

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** the bytes that every signed object of Grant v4 shares: the
  canonical form, integers, types, signing digests, identifiers, the consent
  of both parties and the issuance commitment; and, since version 0.1.53,
  the members of the grant itself
- **Builds on:** LIP-0008 sections 3.1, 7.1, 8, 8.1 and 9, and LIP-0005;
  for the members of the grant also LIP-0008 sections 3, 4, 11.4 and 12.2,
  LIP-0014 sections 8.3, 9.1, 10.1, 11.1 and 11.2, LIP-0021 section 2,
  LIP-0026 and LIP-0027; relates to LIP-0004, LIP-0013, LIP-0017, LIP-0018
  and LIP-0019

## Summary

LIP-0008 requires that every signed object of Grant v4 carries its type and
version inside canonical bytes, is signed under a digest that belongs to its
type alone, and has one identifier. It assigns none of those bytes. Two
implementations of Grant v4 therefore cannot exchange a single object today,
and no vector can be published for either of them.

This LIP proposes the bytes of that layer, which every v4 object shares:

- one canonical form, RFC 8785 over a restricted set of values (section 1);
- two forms for an integer, so that no amount passes through a binary64
  number (section 2);
- a registry of object types, each with one identifier that stands in the
  signed bytes and also names the signing digest (sections 3 and 4);
- the signature encoding, the signed form and the identifier of an object
  (sections 5 and 6);
- the consent of both parties to a contract, with the rule for a recipient
  that the grant names by name, whose key the name can replace (section 7);
- what an issuance anchor commits to, and its frame (section 8);
- the pipelines of a reader, their order and their refusal codes (section
  9);
- vectors for all of it (section 10);
- since version 0.1.53, the members of a v4 grant, root and child, with the
  right of re-delegation, its groups, templates and ranges, the bounds and
  the refusals (section 11), and their vectors (section 12).

Four objects are complete here: the assent of a party to a contract, the
consent event of a recipient, the issuance preparation and, since version
0.1.53, the grant. The registry reserves an identifier and a digest for four
more types and gives them no member: the invocation, the receipt, the
seal-key endorsement and a successor of the notary attestation. No reader
accepts a payload of those four until the proposal that fixes its meaning
gives it members.

## What is decided and what is proposed

Two points of section 7 are decided. They were decided on 2026-11-14 under
Ivan Oparin's delegation; he may override the decision, and the co-author's
agreement is pending. The first requires authorisation by name at issuance:
the state of a name at the issuance snapshot decides, and a state that held
earlier or later is no substitute. The second makes a consent bound and
single-use, with a largest age of 72 hours at issuance. Section 7 states
both and says what the draft adds to carry them.

Every other rule of sections 1 to 10 is the draft's proposal. Neither owner
has decided a byte of it, and nothing of it is implemented. The owners accept
or change these bytes through this LIP, under LIP-0001.

Section 11, the members of `swarma-grant/4`, is text in force since version
0.1.53. On 2026-11-16 Ivan Oparin ordered, as the lead relayed it, that Grant
v4 does not wait. Its members are therefore written as text in force and not
as a proposal, without waiting for the co-author's agreement, which has not
been given; the co-author's answer is folded in by amendment. The section
opens with what that means for each rule that it carries, and its table
"Where each member comes from" names every form that no decision gives.

Version 0.1.55 adds two things to section 11 and no member: the rule W11.11,
with four comparisons of a child against its parent and their codes, and
the subsection 11.14, with the two registries, both without a defined
entry, and the two refusals of an executor. Both are proposals of version
0.1.55 and are in force by no word of this draft: each binds a reader of
`swarma-grant/4` when the version lands, and the co-author's answer is
folded in by amendment. The owner's order that Grant v4 does not wait
covers the members of the grant, as the paragraph above says, and is not
stretched to these two additions. The steps at which they stand are those
of LIP-0014 section 8.4, which has the same state. No octet of a grant and
no vector of section 12 changes.

Version 0.1.61 adds no member either. It registers in section 11.11 one
further code, `CONTRACT_SEAL_MISSING`, for the check that the contract
which a grant binds has the confirmed seal that it names. The refusal is
decision C12 of LIP-0017 (Ivan Oparin, 2026-11-17; the co-author agrees and leaves the judgement to Ivan, as recorded with the event and quote in LIP-0017,
"Decisions recorded"), at the issuer's signing
service and at every verifier. The code name and its step, part (c) of
row F6 of LIP-0014 section 8.4, are proposals of version 0.1.61 in the
state of W11.11 and of that section. No member of `swarma-grant/4` names
a contract seal; the grant gives the seal's contract through `contract`
alone, and no octet and no vector changes.

The requirements that the proposal meets are Draft text of LIP-0008: a type
and a version inside the signed bytes, one tagged digest for each type, one
identifier for each object, strict BIP-340 verification, and RFC 8785 as the
plan for the canonical form (sections 8 and 8.1).

Section 7 also rests on two parts of LIP-0008 that it does not change.
Section 3.1, a recipient by key or by name, and section 7.1, a window in
block heights, entered LIP-0008 in version 0.1.13; the changelog of that
version dates them to Ivan Oparin's decisions of 2026-11-10, with the
co-author's agreement pending. Section 7.1 itself dates two of its points to
his decision of 2026-11-11: that a window does not open below the committed
recent block, and that an invocation keeps clock time.

The table says which open point of LIP-0008 each section answers.

| Open point of LIP-0008 | Proposed here |
| --- | --- |
| "Exact versioned bytes, signature domain, commitment/consent encoding" | Sections 1, 3, 4, 7 and 8, for the layer that all objects share, and section 11 for the grant. The members of four types stay open |
| "typed-hash registry" and "per-field JCS integer/string schemas" | Sections 2, 3 and 4. The form of each integer member is fixed with its type: for the grant in section 11, and for the four open types it is open with them |
| "Signed metadata envelope, canonical object-ID preimages/signature inclusion, strict signature wire representation" | Sections 3 (W3.7), 5 and 6 |
| "cross-version journal bindings" | Section 6 states what an identifier alone may not do. The journal key of a request comes with the members of the invocation |
| "how the consent event's NIP-01 `created_at`, which stays in seconds, relates to the window" | Section 7.4 |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The reader of canonical bytes, the two integer forms, the typed digest, signatures, the signed form and identifiers (sections 1 to 6) | Yes | The owners' acceptance |
| The assent, the consent event, the issuance preparation and its frame (sections 7 and 8), as octets and as checks on stated inputs | Yes | On the ordinary `/1` path the contract identifier is taken as 32 given octets: its preimage is open in LIP-0017 section 2; W9.4 adds no contract-document input to that path. The reads on a node need the ownership profile of LIP-0008 section 3, which is open |
| A reader of a grant: its members, its signature, and the rules that need its octets alone (section 11) | Yes | The co-author's answer. The admission of a grant needs the reads on a node of the profiles that section 11.11 names |
| A parser of an invocation, a receipt, an endorsement or the successor attestation | No | The members of each, as the next table says |

| Type | Its members wait for |
| --- | --- |
| `swarma-grant/4` | Nothing: section 11 gives the members. Open beside them are the registries of action names and of limit kinds (LIP-0007, LIP-0018), the seal of a single-use grant (LIP-0008 section 11.1) and the key that assents to a child's contract (section 7.1) |
| `swarma-invocation/1` | The action table and the types of its arguments (LIP-0007, LIP-0008 sections 12.1 and 12.3), the encoding of the proof path (section 12.2) and the journal key of a request |
| `swarma-receipt/1` | What a receipt states about an effect, for each action (LIP-0018 section 3) |
| `swarma-seal-endorsement/1` | The seal profile and the form of a seal key and of its script (LIP-0008 sections 11.1 and 11.2) |
| `swarma-notary-attestation/2` | The Draft changes of LIP-0014 sections 3.4 and 10.1 (J5, J2), which await the co-author. The changes of its sections 7.1 and 9.1 (J3, J1) are decided by both owners |

Until a type has members, no reader supports it, and a payload of that
type refuses as `WIRE_TYPE` (W3.1). Nothing in this LIP, and no vector,
makes a payload that holds only `type` a valid object: for the grant such a
payload refuses as `WIRE_MEMBER` since version 0.1.53.

## Motivation

Three defects follow from leaving this layer open, and each is silent.

An amount of 9007199254740993 atoms, read through a parser that holds JSON
numbers as binary64, becomes 9007199254740992. The reader signs or admits
the rounded amount and reports nothing. RFC 8785 does not prevent this: it
serializes a number that the parser already rounded. LIP-0008 section 8
therefore asks each amount to choose an exact form, and names none.

A grant, an invocation and a receipt are all JSON objects signed by BIP-340
keys. Without a digest that belongs to one type, a signature made over one
of them is a signature over the same octets wherever those octets are
accepted as another type. LIP-0008 section 8 requires distinct digests and
assigns no tag.

A recipient that the grant names by name consents with the key that its
name lists for a channel, and the owner of the name can replace that key at
any time (LIP-0008 section 3.1). A verifier that checks the consent later
against the name's current value refuses a consent that was given
correctly, and a verifier that checks it against no name at all accepts a
consent by any key. LIP-0008 lists the point as open.

## Current state

- A v3 grant is compact JSON in a fixed member order, signed over
  `SHA-256("swarma-grant-v3" || bytes)`. Its `grant_id` is the SHA-256 of
  the signed grant, signature included. Its consent is a Nostr event of
  kind 8181 and an untyped signature of the issuer over the contract hash,
  and its issuance commitment is a hash under the prefix `swarma-issue-v1`
  (LIP-0004 sections 2 to 4). The frame of the commitment has payload
  version `0x01` (LIP-0005).
- The signed Draft objects of LIP-0014, LIP-0015 and LIP-0016 use the same
  fixed-prefix style and the encoding rules of LIP-0013 section 2.1.
  LIP-0014 section 6.1 says of its attestation that the typed-hash plan of
  LIP-0008 may replace the prefix before adoption.
- LIP-0008 section 8 plans RFC 8785 and tagged hashes for the next format
  and section 8.1 states the requirements on identifiers and signatures.
  Both leave the bytes open.
- `tools/trustcheck` recomputes the vectors of LIP-0013 and nothing of
  Grant v4. When this LIP was written the reference laboratory held no v4
  code. Since then it holds experiments for the layer of sections 1 to 9 on
  stated facts, and no reader of a grant. `tools/grantv4` reads a grant of
  section 11 and recomputes the vectors of section 12.

## Proposal

### 1. Canonical bytes

The canonical bytes of an object are the RFC 8785 serialization (JSON
Canonicalization Scheme) of one JSON object, over a set of values that is
smaller than JSON's. A document meets all six rules or refuses. Which
refusal a reader reports for a document that breaks more than one of them
is fixed by W9.2.

| Rule | What the reader requires | Refusal |
| --- | --- | --- |
| W1.1 | The document is no larger than the largest size of the type that its place requires (section 3). Its objects and arrays nest at most 16 deep, the document itself being the first level. | `WIRE_SIZE` |
| W1.2 | The octets are UTF-8 without a byte order mark, and they are one JSON object under RFC 8259. | `WIRE_JSON` |
| W1.3 | No object has two members of one name. Names are compared after their escapes are resolved. | `WIRE_DUPLICATE` |
| W1.4 | A value is an object, an array, a string, an integer in the number form of section 2, or `true` or `false`. `null` is no value: a member is present with a value, or it is absent. | `WIRE_VALUE` for a `null`; `WIRE_NUMBER` for a number in any other form |
| W1.5 | A string, a member name included, is a sequence of Unicode scalar values from U+0020 upward. An escape that yields a code point below U+0020, or an unpaired surrogate, refuses. Nothing is normalized: two strings are equal when their code points are equal. | `WIRE_STRING` |
| W1.6 | The octets equal the RFC 8785 serialization of the parsed value. | `WIRE_NOT_CANONICAL` |

For the values that W1.4 and W1.5 admit, the serialization of RFC 8785 is
this:

- no whitespace anywhere outside a string, and nothing before the opening
  brace or after the closing one;
- the members of an object in the order of their names, compared as
  sequences of UTF-16 code units; an array keeps its order;
- a string written literally in UTF-8, with `\"` and `\\` as its only
  escapes. A slash, an ampersand, an angle bracket, U+007F and U+2028 are
  written literally;
- an integer in decimal digits, without a sign, a leading zero, a fraction
  or an exponent.

A reader does not repair. It parses the octets, serializes the parsed value
with its own serializer, and refuses unless the result is identical to what
it received. A reordered member, a space, an escape for a character that is
written literally and a trailing line feed all refuse under W1.6.

Three properties of common JSON libraries make W1.6 a rule that needs its
own code and its own vectors. Order by UTF-16 code units differs from order
by code points for a name outside the Basic Multilingual Plane: U+1F600
stands before U+FB33, because its first code unit is D83D. Go's
`encoding/json` writes U+2028 as an escape in every mode, and writes `<`,
`>` and `&` as escapes unless it is told otherwise. And a parser that
holds numbers as binary64 cannot apply W1.4 at all, which section 2 takes
up.

The restrictions of W1.4 and W1.5 are choices of this draft. Excluding the
code points below U+0020 leaves two escapes in place of seven and one
spelling for every string. Excluding `null` removes the question whether an
absent member and a `null` member mean the same.

### 2. Integers

An integer has one of two forms, and the schema of a type says which form
each integer member has.

| Form | Octets | Range | Use |
| --- | --- | --- | --- |
| Number form | A JSON number: `0`, or a digit from 1 to 9 followed by digits | 0 to 9007199254740991, which is 2^53 - 1, or to the smaller bound that the member states | Values that what they count keeps far below 2^53: a block height, an output index, a position in a list, Unix seconds |
| String form | A JSON string that holds the same grammar | 0 to the bound that the member states | An amount in atomic units, a price, a cost, a count of tokens or of octets, and every cumulative counter |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| W2.1 | Every integer member has exactly one form, stated by the schema of its type. The other form refuses: the number `1` where the string `"1"` is required, and the reverse. No reader converts one into the other. | `WIRE_MEMBER` |
| W2.2 | The number form. The token has no sign, no fraction and no exponent, and its value is at most 9007199254740991. The reader decides this on the digits of the token. Where the schema states a smaller bound for the member, the value is at most that bound. | `WIRE_NUMBER` for the token; `WIRE_INTEGER` for a value above the bound of its member |
| W2.3 | The string form. The string is `0`, or a digit from 1 to 9 followed by digits `0` to `9`, and nothing else: no sign, no leading zero, no fraction, no exponent, no space, no separator, no digit outside ASCII. Its value is at most the bound of the member. | `WIRE_INTEGER` |
| W2.4 | A reader parses an integer from its digits into an exact integer and checks the bound before it computes with the value. No binary64 number takes part, at a reader or at a signer. An addition or a multiplication whose result would pass the bound of its member refuses and does not wrap. | The code of the rule that computes |

No member of the first profile has a bound above 18446744073709551615,
which is 2^64 - 1, so a reader can hold every integer of the profile in 64
unsigned bits. A type that needs more states its own bound.

Which members take the string form is decided with each type. The rule of
thumb in the table is the draft's: whatever can be summed without a natural
ceiling takes the string form, so that no later asset or price forces a
change of form. The assent, the consent event and preparation `/1` hold one integer
member, an output index, in the number form. Preparation `/2` has no
integer member; the new credential types state each integer form explicitly. The grant holds both
forms (section 11), and its rule W11.10 is the one rule of this LIP that
computes with integers.

### 3. Types and the registry

| Rule | Requirement | Refusal |
| --- | --- | --- |
| W3.1 | Every payload has a member `type`, a string: the name of the object type and its version, joined by a slash, exactly as the registry below writes it. A reader compares the whole string and never parses a version out of it. A payload without `type`, with a `type` that is no string, with a `type` that the reader does not support, or with another type than the one that its place requires refuses. A reader supports no type without members. | `WIRE_TYPE` |
| W3.2 | The members of a payload, and of every object inside it, are exactly those that the schema of its type lists for that object, each in the form that the schema states. A member that the schema does not list, a required member that is missing and a value in another form refuse, at every depth. | `WIRE_MEMBER` |
| W3.3 | A change of octets or of meaning takes a new version, as LIP-0018 requires of a profile. A reader that supports one version reads no other version as that one, and no reader falls back from a type that it does not support to one that it does. | `WIRE_TYPE` |
| W3.4 | The registry applies to no object of an earlier format. A v3 grant, the contracts `swarma-trust-contract/1` and `/2`, the attestation `swarma-notary-attestation/1` and the statements of LIP-0015 and LIP-0016 keep their own bytes, prefixes and identifiers. Under this registry such an object has no `type` and refuses. | `WIRE_TYPE` |
| W3.5 | A member that holds a hash, an identifier, a transaction id or a signature is lowercase hexadecimal of the exact length that the schema states. A transaction id and a block hash are written in the byte order in which a node prints them. The `signature` of a signed form has its own rule and code (W5.2). | `WIRE_MEMBER` |
| W3.6 | A signing key, a key under which a BIP-340 signature of this profile verifies, is an x-only key: 64 lowercase hexadecimal characters that are the x coordinate of a point of the curve. The rule covers signing keys and no other key. | `WIRE_MEMBER` for the form; `WIRE_KEY` for a value that is no such coordinate |
| W3.7 | Descriptive members, where the schema of a type admits them, are members of the payload like any other. They are inside the canonical bytes, the digest and the identifier, and a change of one is a change of the object. A signed form carries nothing beside the payload and the signature. Such a member gives no authority (LIP-0008 section 12.3). | `WIRE_SIGNATURE` for a member that was changed after signing |

A key that controls an output is another kind of value than a signing key.
The owner key of a name, a seal key and the key of a coin are known through
the script that they pay, and for a script that hashes a compressed key the
parity of that key decides which script it is. The form of such a key comes
with the ownership and seal profiles of LIP-0008 sections 3 and 11. W3.6
says nothing about it, and no reader of this LIP turns such a key into an
x-only key. In a grant every such key has the compressed form of LIP-0021
O2.1, which W11.1 calls an output key.

The registry:

| Type | Object | Use of its digest | Signed by | Members |
| --- | --- | --- | --- | --- |
| `swarma-grant/4` | A v4 grant, root or child (LIP-0008 section 1) | Signature | For a root grant the issuer's grant key. For a child the delegation key of the parent (W11.8; LIP-0014 J4, awaiting the co-author's agreement) | Section 11, complete |
| `swarma-invocation/1` | A signed invocation (LIP-0008 section 12.1) | Signature | The request key of the final grant, or the key that its recipient's name yields for the channel | None yet |
| `swarma-receipt/1` | The receipt of an executor for an effect | Signature | The executor's key | None yet |
| `swarma-seal-endorsement/1` | The endorsement of a seal key (LIP-0008 section 11.2) | Signature | The issuer's grant key | Named by meaning in LIP-0008 section 11.2; none here |
| `swarma-contract-assent/1` | The assent of one party to a contract | Signature | The key of that party | Section 7.1, complete |
| `swarma-issuance/1` | The issuance preparation | Commitment | Nobody; the anchor transaction authenticates it | Section 8, complete |
| `swarma-notary-attestation/2` | Typed notary attestations: only `child-within-parent` and `contract-notarization` | Signature | The notary's attestation key, never its credential issuer key | LIP-0032 section 1: contract-notarization schema specified; child mapping remains open, v1 semantics unchanged |
| `swarma-credential/1` | Third-party `subject-claim` and `agent-audit` credentials, plus explicitly supported application kinds | Signature | The separately registered credential issuer key | LIP-0032 section 2; signed form at most 65536 bytes |
| `swarma-credential-withdrawal/1` | Cause for a credential-seal spend, never the LIP-0014 notary withdrawal | Commitment | No detached signature; validated seal spend authenticates the withdrawal | LIP-0032 section 3; payload at most 512 bytes |
| `swarma-credential-break/1` | Name-owner-authenticated issuer compromise height | Commitment | No detached signature; name input authorization commits to the break frame | LIP-0032 section 3; payload at most 1024 bytes |
| `swarma-issuance/2` | Scoped unilateral root EFFECT issuance, with or without the optional mandate | Commitment | No detached signature; binds the checked grant signature and, when present, mandate signature | LIP-0035 section 2; payload at most 1024 bytes |
| `swarma-auth-challenge/1` | Foreign-service auth challenge signed as response | Signature: W4 tagged hash with tag `swarma-auth-challenge/1` | Dedicated BIP-340 auth key, never a device/grant/name-owner key | LIP-0034 section 2; signed form at most 4096 bytes |
| `swarma-auth-upgrade/1` | Atomic provisional-to-name upgrade | Signature: W4 tagged hash with tag `swarma-auth-upgrade/1` | Same dedicated auth key as the provisional cell | LIP-0034 section 2; signed form at most 4096 bytes |
| `swarma-unilateral-mandate/1` | Optional unilateral contract, never mandatory for the scoped contract-free branch | Signature: W4 tag `swarma-unilateral-mandate/1` | Issuer's BIP-340 grant key only | LIP-0035 section 2.1; signed form at most 65536 bytes |
| `swarma-broker-invoke/1` | Private broker invocation and single-use challenge | Signature: W4 tag `swarma-broker-invoke/1` | Exact recipient key or verified named BIP-340 channel/request key | LIP-0035 section 2.2; signed form at most 1048576 bytes |

Auth types retain W9 ordering and signature-form errors, but LIP-0034
reports a well-formed invalid BIP-340 signature as `AUTH_SIGNATURE`; this
is the explicit auth-profile exception to the final `WIRE_SIGNATURE`
verdict, not a second alternative code for the same input.

The largest size is 1024 octets for the signed form of an assent, 2048
octets for issuance preparation `/1` and 65536 octets for the signed form
of a grant (W11.6). The new types state their own bounds in the registry
and defining LIP; preparation `/2` is at most 1024 bytes. A type without
members states its largest size with them.

Draft [LIP-0024](LIP-0024-seal-endorsement.md) proposes the members of
`swarma-seal-endorsement/1`, with its largest size, its codes and its
vectors. The entry above stands until both owners accept them.

Draft text of 2026-11-16 in LIP-0008 section 11.4 (SB4), which awaits the
spec review and the co-author's agreement, puts the seal key into
`swarma-grant/4` and removes `swarma-seal-endorsement/1` from this registry
once agreed. Until then the entry stands. Section 11 carries the seal key in
the grant, as that text asks (the member `seal`, W11.2), and no rule of
section 11 reads an endorsement.

W11.8 says who signs a child's grant, and W11.2 with LIP-0014 CS2 whose key
the seal of a child pays. Who assents to a child's contract is a question of
LIP-0014 section 11.1 that stays open (section 7.1).

One object of this profile is a Nostr event and no entry of the registry:
the consent event of section 7.2. It keeps the wire form and the identifier
of NIP-01, and sections 1 to 6 do not apply to it.

The attestation needs a successor for two reasons. Its identifier and its
signature follow the fixed-prefix style, which sections 4 to 6 replace for the
objects of this profile, and new octets take a new version (W3.3). And its
members are not settled for v4: Draft text of LIP-0014 section 3.4 leaves
`none` and `identical` as the values of `textual` (J5), under a decision that
awaits the co-author's agreement. The members `budget` and
`prev_attestation_id` are gone from the attestation since both owners agreed on
rows (J1; LIP-0014 sections 6.1 and 9.1). This LIP gives the successor its
identifier and its digest and no member; its members, and the commitment of its
anchor (LIP-0014 section 6.4), come with the proposal that settles them.
`swarma-notary-attestation/1` keeps the octets and the prefix that LIP-0014
gives it, under W3.4.

A type enters the registry, and a registered type gets a new version,
through a LIP that states its identifier, the key that signs it, its
members with their forms and bounds, its largest size, its refusal codes
and its vectors.

### 4. The typed digest

| Rule | Requirement |
| --- | --- |
| W4.1 | The typed digest of a payload is the SHA-256 of three parts in sequence: the SHA-256 of the tag, the SHA-256 of the tag once more, and the canonical bytes of the payload. This is the tagged hash of BIP-340 with an application tag. |
| W4.2 | The tag is the octets of the payload's own `type` string. No other tag exists for the type, and a reader takes the tag from no other place than the payload. |

```text
typed_digest = SHA-256( SHA-256(tag) || SHA-256(tag) || canonical bytes of the payload )
```

Each type uses its digest for one thing, which the registry states: as the
message of a signature, or as a commitment. A signer computes the digest
itself from the complete object; LIP-0008 section 8 already forbids a key
service to sign a digest that a caller supplies.

With W4.2 the two requirements of LIP-0008 section 8 cannot disagree: the
type is inside the signed bytes, and the same string selects the digest. A
signature made under the tag of one type verifies under no other type,
because the payload that it covers states its type. The tags of BIP-340
itself, `BIP0340/challenge` among them, are internal to the signature and
are not these tags.

For the octets `{"type":"swarma-grant/4"}` the SHA-256 of the tag is
`eb2b9dc1647237e0e0d7e024a19f4ee95379c20ff01f4ccb7cf1168840fef67a` and the
typed digest is
`f1e62e34f6b79cd5c28a4b1edbb50b737bb3f4d2bd26805764b64eb5e7372f75`. The
example is arithmetic: those octets are no valid grant.

### 5. Signatures and the signed form

| Rule | Requirement | Refusal |
| --- | --- | --- |
| W5.1 | A signature is a BIP-340 signature over the 32 octets of the typed digest of the payload. | `WIRE_SIGNATURE` |
| W5.2 | A signature is 64 octets, written as 128 lowercase hexadecimal characters. No other encoding is read. Verification is the verification algorithm of BIP-340 without any relaxation: it fails when the first half is no field element, when the second half is no scalar below the group order, and when the recomputed point is at infinity, has an odd y coordinate or has another x coordinate. | `WIRE_SIGNATURE_FORM` for the encoding; `WIRE_SIGNATURE` for a failed verification |
| W5.3 | The signed form of an object is the canonical bytes of an object with exactly two members: `payload`, the payload, and `signature`. A third member refuses, a stated identifier included. | `WIRE_MEMBER` |
| W5.4 | Two valid signatures over one payload belong to one object. BIP-340 allows a signer to choose other auxiliary randomness, and the result is another valid signature. A reader accepts both, and no state is keyed by a signature (section 6). | none |
| W5.5 | A reader verifies a signature under the key that the rules of the object name for the place: a pin, a member of another object that it already verified, or a member of the payload where the type says so. It verifies no signature under a key that the presenter chose. A key that is no point of the curve refuses before any verification. | `WIRE_KEY`; `WIRE_SIGNATURE` for a signature by another key |

An object that nobody signs, the issuance preparation, has no signed form.

### 6. Identifiers

| Rule | Requirement | Refusal |
| --- | --- | --- |
| W6.1 | The identifier of an object is the SHA-256 of the canonical bytes of its payload, written as 64 lowercase hexadecimal characters. | none |
| W6.2 | The signature and the signed form are outside the identifier. One payload has one identifier, under whichever valid signature and in whichever bundle it travels. | none |
| W6.3 | A reader recomputes an identifier from the payload. It trusts no identifier that is stated beside an object, and it compares every reference to an object with the identifier that it recomputed. | `WIRE_ID` |
| W6.4 | Three hashes of one object have three uses and are never exchanged. The identifier names the object in references: a parent in a child, a grant in an endorsement, a link of a proof path. The typed digest is what a signature covers; nothing is signed by signing an identifier. The content address, the SHA-256 of the signed form, is what a store holds the signed object under (LIP-0019); two signed forms of one payload have two addresses and one identifier. | `WIRE_ID` for a reference that states another of the three |

An identifier names octets. An identifier or a signature alone must not
reset state: LIP-0008 section 8.1 requires that neither re-signing nor
another object identifier restores a seal, a nonce claim, a consumed budget
or a reservation. Under W6.2 re-signing changes no identifier. A request
that is signed again with another `iat` has another identifier and is still
the same request, and the journal knows it by a key that the profile of the
invocation builds from the members that such a change leaves alone, the
executor and the nonce among them. That key comes with the members of the
invocation and is not fixed here.

This restricts no rule that keys state by an identifier together with other
members. LIP-0014 section 9.1 keys the ledger of a row by the identifier of
its parent and an ordinal, and that key stays what its rule says. A new
grant with a new seal is new authority, and nothing here makes it share
state with another grant.

One consequence of W6.4 concerns retrieval. On v3 the `grant_id` is also
the hash under which a store holds the signed grant, so a reader fetches a
parent by the identifier that a child states (LIP-0019 section 5). On v4
the identifier and the content address differ, and a store that is
addressed by the SHA-256 of stored octets cannot serve a signed object
under the identifier of its payload. A reader that holds only an identifier
needs the content address beside it, or a store that also indexes signed
objects by their identifiers. Which of the two a presentation of a v4 grant
uses is open; the rules of LIP-0019 for a parent are rules for v3.

### 7. Consent

Under the Draft text of LIP-0017 section 1 a contract is concluded when
every party that it names has signed its identifier, each with its own key
and under a domain that belongs to contracts alone. The v3 consent is that
rule for two parties: a Nostr event of the recipient and an untyped
signature of the issuer over the contract hash (LIP-0004 section 3). This
section gives both their v4 form. The issuer signs a typed assent. The
recipient signs a Nostr event, as on v3, because a signer in a browser
signs events and nothing else.

Both bind the contract by its identifier, 32 octets that the profile of the
contract defines (LIP-0017 section 2). Both also bind the chain, by the
hash of its genesis block. The pin of the construction profile, which
LIP-0008 section 1.1 leaves open, is not part of either.

Two points of this section are decided. They were decided on 2026-11-14
under Ivan Oparin's delegation; he may override the decision, and the
co-author's agreement is pending.

| Point | Decision |
| --- | --- |
| Authorisation by name at issuance | It is required. At the issuance snapshot, the consistent state of its own node that the issuer signs against, the issuer's name is live, is held by the pinned owner under the first ownership profile (for the Witness profile on Namecoin: a closed list of single-key scripts, read on a node with a transaction index), and its value names the grant key that signs. The recipient identity snapshot is also required when the grant names a recipient by name. For an ordinary bilateral, framework or rental grant, its current value names the channel key that signed the consent; for either narrowly scoped unilateral branch of LIP-0035 no consent signature is required, but the identity snapshot is not waived. A state that held earlier or later is no substitute. |
| Age and reuse of a consent | For grants that bind a contract (bilateral, framework, rental), a consent is bound and is used once. Ivan Oparin decided on 2026-11-20 (source: `$HZ30GFE5jwhKwwz9eDacfUnKf6nTRh2h-uF4OHylwD4`) to scope this rule accordingly; co-author agreement pending. Under LIP-0035's editor proposal, neither scoped unilateral branch has a consent to consume. The consent names the exact contract, the issuer and the recipient. Exactly one issuance consumes it. It is never presented again for another grant, for a re-issue or for a successor; each of those needs a fresh consent, and the issuer records the identifier of the consent as consumed. At most 72 hours pass between the `created_at` of the consent event and the issuer's first transaction of the issuance, measured on the issuer's clock, and an older consent refuses. `created_at` is never compared with a block height. The 72 hours cover an issuance of two transactions with a person's confirmation between them. They are a policy number, not a measured tolerance, and a later profile may change them. |

The rest of the section is the draft's proposal for carrying the two points
in octets and in checks. It adds four things that the decision does not
state: the tags `issuer` and `name` of the consent event (W7.3); the recent
block of the grant as the block of the snapshot, with the evidence output
and the verifier's read of it (W7.6); which transaction counts as the
first of an issuance (W7.8); and what a verifier can and cannot see of the
single use (W7.9).

Ivan Oparin decided on 2026-11-20 (source: `$HZ30GFE5jwhKwwz9eDacfUnKf6nTRh2h-uF4OHylwD4`) to scope this section's contract assent
and recipient consent requirements to **grants that bind a contract
(bilateral, framework, rental)**. The co-author's agreement on this amendment
is pending. Only the LIP-0035 root EFFECT case without `delegate`, never hire
or rental, may omit `contract` and the associated assents/consent. Its
recipient is one key or one name. Issuer authorization and recipient
name/owner binding at the issuance snapshot remain required; the exception
does not manufacture a channel-key consent signature that never occurred.
All consent age/reuse rules remain unchanged where consent is required.

For both scoped unilateral branches, including the optional issuer-signed
mandate, preparation `/2` requires no separate W7 issuer assent or recipient
consent; this is the Swarma Link editor's resolution in LIP-0035, not an
additional owner decision. The signed grant's `recent_block` commits to the
recipient identity snapshot: resolve that name's owner at that block with
the verifier's indexed history and compare `recipient.owner` (LIP-0035 U3).
No `name_output` or consent channel-key evidence is fabricated. Missing
snapshot evidence refuses `ISSUANCE_MODE` at W9.4 step 2.

#### 7.1. The assent of a party

W7.1. An assent is a payload of type `swarma-contract-assent/1` with
exactly these members:

| Member | Form | Meaning |
| --- | --- | --- |
| `type` | string | `swarma-contract-assent/1` |
| `genesis` | 64 hexadecimal characters | The hash of the genesis block of the chain that holds the names of the parties |
| `contract` | 64 hexadecimal characters | The identifier of the contract |
| `party` | signing key (W3.6) | The key that assents. The signature of the signed form verifies under it |

W7.2. A verifier of a grant takes the issuer's assent through the pipeline
of a signed object (section 9) and then checks, in this order:

| Check | Refusal |
| --- | --- |
| `genesis` is the chain of the grant, and `contract` is the contract hash that the grant binds | `ASSENT_BINDING` |
| `party` is the key that the profile of the contract names for the party that issues the grant | `ASSENT_PARTY` |

Until a v4 contract profile says otherwise, the key of the issuing party of
a root grant is the issuer's grant key, the member `issuer.grant_key` of the
grant (W11.2), as in the v3 profiles (LIP-0017 section 1). For a child grant
the point is open: Draft text of LIP-0014 section 11.1 lets the delegation
key sign child grants and nothing else, so that key cannot sign an assent.

An assent gives no authority and opens no window. It says that a key agreed
to a contract.

#### 7.2. The consent event of the recipient

W7.3. The recipient consents with a NIP-01 event of kind **8181** with
empty `content`, in the wire form of LIP-0013 section 3.1 and at most 2048
octets, with exactly these tags in this order:

| # | Tag | Value |
| --- | --- | --- |
| 1 | `t` | `swarma-contract-consent/1` |
| 2 | `genesis` | the hash of the genesis block, as in the assent |
| 3 | `contract` | the identifier of the contract |
| 4 | `issuer` | the issuer's grant key, a signing key (W3.6): the key that signs the grant and the issuer's assent |
| 5 | `name` | for a recipient by name only: the name, exactly as the grant signs it |

The event names the recipient in one of two ways. For a recipient by key it
has four tags, and its `pubkey` is the recipient: the request key. For a
recipient by name it has the fifth tag. The wire form admits printable
ASCII and nothing else (LIP-0013 section 2.1), so a name that holds another
octet has no consent in this profile.

Kind 8181 is the kind of the v3 consent. The two cannot be confused: a v3
verifier requires the v3 value of `t`, and a v4 verifier requires this one.
What a v3 consent carried in its tags `booking` and `privacy` is part of
the contract on v4, which the identifier binds.

W7.4. A verifier checks a consent event in five steps and reports the
first that fails:

| Step | Check | Refusal |
| --- | --- | --- |
| 1. Shape | The size, the wire form, the kind and the empty content are as W7.3 states. The tags are the four, or the five, of W7.3 in their order. `pubkey` and the value of `issuer` are signing keys (W3.6). `id` is the NIP-01 id of the event | `CONSENT_SHAPE` |
| 2. Binding | `genesis` and `contract` are the chain and the contract hash of the grant. `issuer` is the key under which the signature of the grant verifies. For a grant by key the event has four tags; for a grant by name it has five, and `name` is the name that the grant signs | `CONSENT_BINDING` |
| 3. Key | `pubkey` is the consenting key: W7.5 for a grant by key, W7.6 for a grant by name | `CONSENT_KEY`, `CONSENT_EVIDENCE` |
| 4. Signature | `sig` verifies over `id` under `pubkey`, as W5.2 verifies | `CONSENT_SIGNATURE` |
| 5. Time | `created_at` is not later than the verifier's clock (W7.8) | `CONSENT_TIME` |

#### 7.3. Which key consents

| | Recipient by key | Recipient by name |
| --- | --- | --- |
| Consenting key | The request key that the grant signs | The key that the current value of the recipient's name yields for the Nostr channel at the issuance snapshot |
| What the issuer checks before it signs the grant | `pubkey` equals the request key | The five conditions of W7.6, at the snapshot |
| What a verifier establishes | `pubkey` equals the request key of the grant | The five conditions of W7.6 for the evidence output |
| What authenticates a request afterwards | The same request key | The key that the name yields at that admission |

W7.5. For a recipient by key, the `pubkey` of the consent event equals the
request key that the grant signs. Any other key refuses as `CONSENT_KEY`.

W7.6. For a recipient by name, the decision asks for the state at the
issuance snapshot. This draft takes the recent block that the grant
commits (LIP-0008 section 7) as the block of the snapshot: the snapshot is
the state of the active chain at that block, without anything that is
pending and without anything that is confirmed above it. The issuer
commits, as the recent block, the tip of one consistent observation of its
own node, and it makes the checks of this rule in that observation.

The issuer signs the grant only if, at the snapshot:

1. the newest operation of the recipient's name is confirmed, at a height
   that is not above the recent block. Where a newer operation is pending,
   or is confirmed above that block, the issuer takes a later snapshot or
   signs nothing;
2. the name is live: it is not expired at the height of the recent block;
3. the output of that operation is controlled by the owner key that the
   grant signs, under the ownership profile;
4. the value of that output yields a key for the Nostr channel, by the
   member that LIP-0008 section 3.1 names;
5. the `pubkey` of the consent event equals that key.

Where one of the first three fails the issuer refuses the consent as
`CONSENT_EVIDENCE`, and where the fourth or the fifth fails as
`CONSENT_KEY`. The issuer records the output of condition 1, by its
transaction id and its output index, as the evidence output. It puts the
two values into the issuance preparation (section 8), hands them on with
the grant, and keeps the consent event and the transaction of the evidence
output with its record of the grant.

A verifier reads the evidence output on its own node and requires all of:

1. the transaction is confirmed on the active chain, at a height that is
   not above the height of the grant's recent block;
2. the output is an operation of the name that the grant signs, and the
   name was live at the height of the recent block;
3. the output is controlled by the owner key that the grant signs, under
   the ownership profile of LIP-0008 section 3, which is open;
4. the output was the name's current output at the recent block: it is
   unspent, or the transaction that spends it is confirmed above the recent
   block. The verifier finds that transaction by following the outputs of
   the name back from the current one, as LIP-0008 section 3 follows an
   issuer's name; the walk ends at the evidence output;
5. the value of the output yields the `pubkey` of the consent event for the
   Nostr channel.

Where one of the first four fails, or the node cannot establish it, the
consent refuses as `CONSENT_EVIDENCE`, and nothing is recorded as closed.
Where the fifth fails the consent refuses as `CONSENT_KEY`.
[LIP-0021](LIP-0021-name-ownership-and-history.md) proposes the ownership
profile and the readings for the first four conditions; they are that
draft's proposals.

Condition 4 is the last sentence of the decision at a verifier. An output
that the owner had replaced by the snapshot held earlier, and condition 4
refuses it. An output that was confirmed after the snapshot held later, and
condition 1 refuses it.

The read costs a walk that LIP-0008 does not otherwise ask for. A request
needs no history of the recipient's name, because it is authenticated under
the name's current value. The consent needs the operations of the name
since the grant was issued and none before the evidence output. A node
without a transaction index cannot make the read and refuses.

The evidence output is no pin of the recipient. Admission of a request
never compares the name's current output with it, and LIP-0008 section 3.1
stays as it is: a grant by name carries no request key and no pin of a name
output.

For the issuer's own name the decision states the same at the same
snapshot. LIP-0008 section 3 already requires it of a verifier: the output
of the issuer's name that was current at the recent block is controlled by
the bound owner key and carries the grant key that signs. That section
notes that its choice of the recent block needs confirmation; the decision
names the issuance snapshot, and this draft reads the two as one block.
This LIP adds no rule for the issuer's name.

W7.7. A later update of the name by the same owner, which lists another
channel key, leaves the consent as it is. The evidence output is then
spent above the recent block, which condition 4 admits, and it still yields
the key that consented. Requests are authenticated under the key that the
name yields at admission, never under the key that consented. A change of
the name's owner refuses the grant itself (LIP-0008 section 3), and the
consent plays no part in that.

#### 7.4. Time, age and single use

W7.8. The `created_at` of a consent event is a claim in Unix seconds. No
rule compares it with a block height, and it is no input of the grant's
window (LIP-0008 section 7.1).

| Who checks, and when | Rule | Refusal |
| --- | --- | --- |
| The issuer, when it signs the first transaction of the issuance: the seal transaction, or the anchor where the seal exists already | Its clock is not earlier than `created_at` | `CONSENT_TIME` |
| The issuer, at the same moment | Its clock is at most 259200 seconds, which is 72 hours, later than `created_at` | `CONSENT_AGE` |
| A verifier, at every check | Its clock is not earlier than `created_at` | `CONSENT_TIME` |

A verifier applies no largest age. The 72 hours bound the issuance and not
the life of the grant: a grant that was issued under a fresh consent is
verified for as long as its window is open, also after the name of its
recipient lists another channel key. The half of the v3 rule that compared
`created_at` with the end of the grant in seconds has no successor, because
a v4 grant has no end in seconds.

W7.9. The issuer records the `id` of the consent event as consumed,
durably and before it signs the grant. It refuses a consent whose `id` it
has recorded, as `CONSENT_CONSUMED`. A second grant under the same
contract, a re-issue after an issuance that failed and a successor of a
grant each need a fresh consent, which differs from the consumed one at
least in its `created_at`. A crash between the record and the signature
leaves a consent that is consumed and unused, and the recipient consents
again.
[LIP-0025](LIP-0025-journal-continuity.md) proposes the journal that holds
this record and what the issuer does after a loss of it; they are that
draft's proposals.

The tags of W7.3 bind the consent to one contract, one issuer and one
recipient, and a verifier checks that binding. It cannot check the single
use: a verifier sees one issuance, and nothing in that issuance shows
whether the issuer used the same consent for another. Two issuances whose
preparations hold one consent `id` are evidence that the issuer broke
W7.9. The rule is a duty of the issuer, and the open questions name a
change that would let every verifier check it.

#### 7.5. Cases

The vectors of section 10 hold the decisions of this section as tables: for
a verifier in the group `consent_events`, for an issuer in the group
`issuer_checks`. They state the facts that a node would supply and test
what follows from them. These cases need the node itself, and no
implementation exists that could run them.

| Valid control | Refusal or invariant |
| --- | --- |
| A recipient by name; the evidence output is the name's current output at the recent block, under the signed owner key, and yields the consent key | The same grant where the evidence transaction is unconfirmed, is confirmed above the recent block, or is no operation of the signed name: `CONSENT_EVIDENCE`, and the journal holds no closure |
| The same | The key was replaced before the snapshot: the name was updated to another channel key below the recent block, and the preparation names the earlier output. The walk finds its spender at or below the recent block: `CONSENT_EVIDENCE`. A verifier that reads the evidence output alone and admits it is wrong |
| The same | The evidence output is controlled by another key than the signed owner key, or the name was expired at the recent block: `CONSENT_EVIDENCE` |
| The same | The value of the evidence output yields another key than the event's `pubkey`, or lists the key only in another entry of `nostr.names`: `CONSENT_KEY` |
| After issuance the owner updates the name to another channel key; the grant is presented again | The consent still passes, and a request signed by the former channel key refuses under LIP-0008 section 3.1. Refusing the consent because the name lists another key today is wrong |
| At the issuer: tip at height 200, and the newest operation of the name is confirmed at 190. The issuer commits the block at 200 and signs | The issuer would commit the block at 195 as recent while the newest operation of the name is confirmed at 199: it signs nothing, because a verifier would refuse the evidence. The same where that operation is pending |
| At the issuer: a consent that is 71 hours old when the seal transaction is signed | A consent that is 73 hours old: `CONSENT_AGE`. The same consent offered for a second grant: `CONSENT_CONSUMED`, also after a restart of the issuer |
| A node that cannot read the evidence transaction, or has no transaction index | The admission refuses, and nothing is recorded as closed |

### 8. The issuance preparation and its anchor

LIP-0008 section 9 has the issuer fix the seal transaction, the parties
sign, and an anchor carry the commitment to "that signed preparation". This
section fixes what the preparation is and what the anchor carries. How the
anchor transaction is built, which inputs it spends and when it counts as
confirmed stays with LIP-0008 sections 1.1 and 9, where it is open.

W8.1. For an ordinary bilateral, framework or rental grant, the issuance preparation is a payload
of type `swarma-issuance/1`.
Each of its objects has exactly the members that this table lists for it
(W3.2), and the largest size is 2048 octets.

| Member | Form | Meaning |
| --- | --- | --- |
| `type` | string | `swarma-issuance/1` |
| `genesis` | 64 hexadecimal characters | The chain of the grant |
| `contract` | 64 hexadecimal characters | The contract hash that the grant binds |
| `grant_id` | 64 hexadecimal characters | The identifier of the grant |
| `grant_signature` | 128 hexadecimal characters | The signature of the signed grant |
| `issuer_assent` | object with exactly `party` and `signature` | The issuer's assent. With `genesis` and `contract` the two members determine it |
| `issuer_assent.party` | signing key (W3.6) | The `party` of the assent |
| `issuer_assent.signature` | 128 hexadecimal characters | The signature of its signed form |
| `recipient_consent` | object with exactly `event_id` and `signature`, and for a recipient by name also `name_output` | The consent event |
| `recipient_consent.event_id` | 64 hexadecimal characters | The `id` of the event |
| `recipient_consent.signature` | 128 hexadecimal characters | The `sig` of the event |
| `recipient_consent.name_output` | object with exactly `txid` and `vout` | The evidence output of W7.6 |
| `name_output.txid` | 64 hexadecimal characters | Its transaction id |
| `name_output.vout` | integer in the number form, from 0 to 4294967295 | Its output index. The bound, 2^32 - 1, is that of an output index in a transaction |

The scoped unilateral preparation is `swarma-issuance/2`, defined by
LIP-0035 section 2: exactly `type`, `genesis`, `grant_id`, `grant_signature`,
and, **if and only if** the grant binds `swarma-unilateral-mandate/1`,
`mandate_signature` (128 lowercase hex characters, the checked W5 signature
of that mandate). It uses W1–W4 and at most 1024 bytes. The grant identifier
already binds the mandate identifier through `contract`; the additional
signature fixes the exact signed mandate as W8.3 requires. There is no
separate issuer assent, recipient consent or detached preparation signature.
These are different versioned schemas, not optional omissions from `/1`. Ivan Oparin decided on 2026-11-20 (source: `$HZ30GFE5jwhKwwz9eDacfUnKf6nTRh2h-uF4OHylwD4`) to permit that scoped
contract-free path; co-author agreement is pending.

W8.2. The `/1` preparation is rebuilt from four inputs: the signed grant, the
signed form of the issuer's assent, the consent event and, for a recipient
by name, the evidence outpoint. The first three are objects that a reader
checks through their own pipelines. The fourth is two values that nothing
signs. The issuer records them when it reads the name (W7.6) and hands them
on with the grant, and a presenter supplies them with the presentation. The
anchor binds them, because a preparation with another outpoint has another
commitment. Nobody signs the preparation, and nobody needs to transport it:
whoever holds the four inputs builds the same octets. From the signed grant
come its identifier and its signature; its chain, its contract hash and the
mode of its recipient are the members `genesis`, `contract` and `recipient`
of the grant (section 11). The request key of W7.5 is `recipient.key`, the
name and the owner key of W7.6 are `recipient.name` and `recipient.owner`,
and the recent block of W7.6 is the block of `recent_block`.

For `/2`, rebuild the preparation from the checked signed grant and, for
the optional mandate branch, the checked signed mandate supplied with it.
Do not include `contract`, `issuer_assent`, `recipient_consent` or
`name_output` in `/2`. An unrequested consent event is not read or checked.
The mandate adds issuer-signed terms and a confirmed issuer-only seal that
MAY be the grant seal; it adds no recipient assent or obligation.

W8.3. The preparation states the signature of each signed part beside what
identifies the part, and each of those signatures is the signature of the
part that the reader checked. The anchor therefore fixes the exact signed
preparation. A part that is presented under another valid signature is the
same object (W5.4) and is still not what was published: the recomputed
commitment differs.

W8.4. A `/1` preparation for a recipient by name carries `name_output`. A
preparation for a recipient by key carries none. The mode is the grant's.
A presentation that offers an evidence outpoint for a grant by key, or none
for a grant by name, refuses as `ISSUANCE_MODE`. A verifier makes this
check on the inputs before it reads the consent event (W9.4). For either
unilateral branch, `/2` is required and the identity/snapshot inputs of
LIP-0035 U3 are required instead of consent evidence. For a supplied
preparation, the wrong version, or the presence/absence of
`mandate_signature` inconsistent with the selected branch, is
`ISSUANCE_MODE` at step 2; the reader never trusts a preparation to select
the branch. Without a supplied preparation it rebuilds the same schema.

W8.5. The issuance commitment is the typed digest of the preparation
(section 4). The anchor carries it in one zero-value `OP_RETURN` output, in
the frame of LIP-0005 with action `0x01`, payload version `0x02` and
location type `0x01`. The pointer is the content address of the signed
grant (W6.4):

```text
6a 03 53 4c 01 42 02 <commitment:32> 01 <content address of the signed grant:32>
```

The script is 72 octets, the length of a v3 issuance script. Payload
version `0x01` stays the commitment of LIP-0004 for a v3 grant. A reader of
an ordinary contract-binding v4 grant accepts version `0x02` alone, with
this action, this location type and this pointer. Both scoped unilateral
root paths (contract-free or optional mandate) use
preparation `/2`, action `0x01`, payload `0x03`, and location `0x00` with no
pointer or `0x01` with the signed grant's content address (LIP-0035 section 2).
A reader never interprets either version as the other. After the preparation
mode passed step 2, a mismatched anchor frame version, location or pointer
refuses as `ISSUANCE_FRAME` at step 5. The rule of LIP-0005
section 3 that an issuance transaction has exactly one `OP_RETURN` output
holds unchanged.

W8.6. A verifier checks the parts in the order of W9.4, builds the
preparation from the parts that passed, takes its typed digest and compares
it with the commitment of the frame. A difference refuses as
`ISSUANCE_COMMITMENT`. The frame is checked before the commitment, so a
grant that is presented under another signature than the anchored one
already refuses at the pointer.

For the vector `issuance-v-01` the commitment is
`285f5db96180e689bc9745e62c780242032d23aa6322b3049cf35a1cabdb4b63`, and the
script is:

```text
6a03534c014202285f5db96180e689bc9745e62c780242032d23aa6322b3049cf35a1cabdb4b63
01e55b1893e8f41bd23d5f306696a728844721388e15e246abb049a9c88b8c59a0
```

The line break is for display; the script has none. The grant of that
vector is a stand-in of three given values, and the example is arithmetic.

### 9. Pipelines, order and refusal codes

W9.1. A place expects one class of object, and the class selects the
pipeline. The class comes from the place and never from the octets: a
reader that expects a consent event looks for no `type`, and a reader that
expects a signed object accepts no event. A reader reports one refusal, the
first of its pipeline, and it reports no refusal of a later step for a
document that an earlier step refuses.

| Class | Used for | Steps, in order |
| --- | --- | --- |
| Signed object | An assent, a grant, and every other signed type of the registry once it has members | 1. The document: W1.1 to W1.6 on the signed form, in the order of W9.2. 2. The signed form: exactly `payload` and `signature` (W5.3). 3. The `type` (W3.1, W3.3, W3.4). 4. The members of the payload, in the order of W9.3. 5. The encoding of the signature (W5.2). 6. The key of the place (W5.5). 7. The signature (W5.1, W5.2). 8. References to the object and from it (W6.3). 9. The rules of the object: for an assent, W7.2; for a grant, W11.9 and W11.10. W11.8 states the points of these steps that are a grant's own |
| Unsigned payload | An issuance preparation that is read from stored octets | 1. The document, in the order of W9.2. 2. The `type`. 3. The members, in the order of W9.3. No step concerns a signature |
| Nostr event | A consent event | The five steps of W7.4. Sections 1 to 6 do not apply: the event has its own wire form, no `type` and no signed form, and its size, its spelling and the encoding of its keys and of its signature are all part of step 1 |
| Issuance | A presentation that is held against its anchor | The six steps of W9.4 |

W9.2. The document step has this order. A document that is larger than
its largest size refuses as `WIRE_SIZE` before it is read. Then W1.1 and
W1.2 are decided on the whole document: of a level of nesting beyond the
sixteenth and a failure of W1.2, the one that comes first in the octets
decides, where a document that stops early fails W1.2 at its end. A
document that passed both is held against W1.3, W1.4 and W1.5 in that
order, each over the whole document, with a `null` before a number inside
W1.4. W1.6 comes last. The codes of one document therefore have the order
`WIRE_DUPLICATE`, `WIRE_VALUE`, `WIRE_NUMBER`, `WIRE_STRING`,
`WIRE_NOT_CANONICAL`, wherever in the octets each defect stands.

W9.3. The member step has this order. First the names: every object of the
payload, at every depth, has exactly the names of its list (`WIRE_MEMBER`).
Then the values, in the order in which the canonical bytes hold them: each
has the form of its member (`WIRE_MEMBER`), and an integer is within the
bound of its member (`WIRE_INTEGER`). Then the signing keys among the
members are points of the curve (`WIRE_KEY`), and so are the output keys of
a grant (W11.1).

W9.4. Every issuance follows the same six steps below; the first failure
gives the refusal. Step 1 has the following ordered substeps:

1. Check the signed grant through W9 and W11.8–W11.10. The root wire schema
   permits missing `contract`; a child still requires it (`WIRE_MEMBER`).
2. A root without `contract` selects the contract-free branch and MUST NOT
   supply a mandate. For a root with `contract`, only an anchor carrying
   payload `0x03` or a mandate claim as defined here selects the mandate
   branch, regardless of the offered preparation version.
   Only that branch MUST present the bound
   contract document; missing bytes are `CONTRACT_NOT_PRESENTED`, never a
   reason to fall back or silently fetch it. The **claim read** is defined
   as follows: presented bytes claim the mandate profile only if they pass
   W9.1 steps 1–2 and their payload has a member `type` whose value is
   exactly the string `swarma-unilateral-mandate/1`. Other presented bytes
   on a root whose anchor carries payload `0x02` are ignored at issuance.
   On the branch selected by a payload-`0x03` anchor, check the document and signed
   form first (W9.1 steps 1–2, with their codes, including `WIRE_JSON` for
   non-document bytes). The **type check**, after those two steps, refuses
   as `ISSUANCE_MODE` if the payload's `type` is absent, is not a string,
   or is any string other than `swarma-unilateral-mandate/1`; this replaces
   W3.1's `WIRE_TYPE` at this step. The signed
   mandate then passes its remaining W9 wire/signature pipeline. Profile
   selection is not validation, and a failed mandate never falls back.
   Otherwise the root stays on the ordinary `/1` path: no contract document
   is required or validated at issuance, and its identifier remains 32 given
   octets while the ordinary profile's preimage is open. Incidental bytes
   that claim no mandate do not add an ordinary issuance gate. An ordinary
   `/1` issuance never establishes the unilateral mandate profile; when its
   bound document is later presented, LIP-0014 F6(a) and LIP-0030 C6 reject
   a mandate with `ISSUANCE_MODE` before any contract recomputation.
3. For the mandate branch, compare every bound field and the contract
   identifier under LIP-0035 section 2.1. Any mismatch is
   `UNILAT_MANDATE_MISMATCH`; do not examine any consent event first or
   fall back to another branch after a failed mandate.
4. For **both** unilateral branches, check U1–U6: `UNILAT_SCOPE` for a root
   with `delegate`, hire/rental or non-EFFECT scope, then
   `UNILAT_OBLIGATION_FORBIDDEN` for any remaining grantee obligation.
   An equal mandate does not excuse `delegate` or re-delegation. An
   unexpected mandate on a contract-free grant is `ISSUANCE_MODE` at step 2.

For both unilateral branches, step 2 requires the U3 identity/snapshot
inputs but no consent-key snapshot or evidence outpoint; steps 3–4 are
inapplicable even if an unsolicited consent event is supplied. The issuer's
mandate signature is the issuer's signed terms, not a separate W7 assent
requirement and never recipient assent. Steps 5–6 use `/2` and payload
`0x03`, including the mandate signature when present. No name, signature,
seal, action-profile or state check is waived. The optional mandate is the
editor's resolution of the owner's v0.3 profile, not a new owner decision.

| Step | Check | Refusal |
| --- | --- | --- |
| 1 | Signed grant; unilateral branch selection; mandate document/form/type and remaining W9 if selected; mandate equality; unilateral scope, in the substep order above; no contract-byte gate for ordinary `/1` | The respective W9/W11 codes, mandate-only `CONTRACT_NOT_PRESENTED`, `ISSUANCE_MODE` for a non-mandate type on that branch, `UNILAT_MANDATE_MISMATCH`, `UNILAT_SCOPE`, `UNILAT_OBLIGATION_FORBIDDEN` |
| 2 | Preparation mode and profile-specific inputs (W8.4): ordinary consent evidence, or unilateral U3 identity/snapshot inputs; no unexpected mandate | `ISSUANCE_MODE` |
| 3 | Ordinary `/1` only: the issuer's assent, through the pipeline of a signed object, and then W7.2 | The codes of that pipeline, `ASSENT_BINDING`, `ASSENT_PARTY` |
| 4 | Ordinary `/1` only: the consent event, through the five steps of W7.4, with the evidence outpoint for a grant by name | `CONSENT_SHAPE`, `CONSENT_BINDING`, `CONSENT_KEY`, `CONSENT_EVIDENCE`, `CONSENT_SIGNATURE`, `CONSENT_TIME` |
| 5 | The frame (W8.5) | `ISSUANCE_FRAME` |
| 6 | The commitment (W8.6) | `ISSUANCE_COMMITMENT` |

Step 2 stands before step 4 for a reason. The third step of W7.4 reads the
evidence output of a grant by name, and the consent event does not say
which output that is: it holds the name and no outpoint. A presentation
without the outpoint gives that step nothing to read. Its refusal is that
of the missing input, `ISSUANCE_MODE`, and not `CONSENT_EVIDENCE`, which
reports an output that was read and did not serve.

The codes:

| Code | What it reports |
| --- | --- |
| `WIRE_SIZE` | A document above its largest size, or nested deeper than 16 |
| `WIRE_JSON` | Octets that are not UTF-8, or not one JSON object |
| `WIRE_DUPLICATE` | A name twice in one object |
| `WIRE_VALUE` | A `null` |
| `WIRE_NUMBER` | A number that is not an integer of the number form |
| `WIRE_STRING` | A string with a code point below U+0020 or an unpaired surrogate |
| `WIRE_NOT_CANONICAL` | Octets that differ from the serialization of the parsed value |
| `WIRE_TYPE` | No `type`, a `type` that the reader does not support, or another type than the place requires |
| `WIRE_MEMBER` | A member that the schema does not list, a missing member, or a value in another form, a list outside its count included |
| `WIRE_INTEGER` | A string-form integer outside its grammar, or an integer above the bound of its member or below its smallest value |
| `WIRE_KEY` | A signing key, or an output key of a grant, that is no point of the curve |
| `WIRE_SIGNATURE_FORM` | A signature that is not 128 lowercase hexadecimal characters |
| `WIRE_SIGNATURE` | A signature that does not verify |
| `WIRE_ID` | A reference that differs from the recomputed identifier |
| `ASSENT_BINDING`, `ASSENT_PARTY` | An assent for another chain or contract; an assent by another key than the issuing party's (W7.2) |
| `CONSENT_SHAPE`, `CONSENT_BINDING`, `CONSENT_KEY`, `CONSENT_EVIDENCE`, `CONSENT_SIGNATURE`, `CONSENT_TIME` | The five steps of W7.4, with two codes for its third step |
| `CONSENT_AGE`, `CONSENT_CONSUMED` | At the issuer alone: a consent older than 72 hours (W7.8); a consent that was used (W7.9) |
| `ISSUANCE_MODE`, `ISSUANCE_FRAME`, `ISSUANCE_COMMITMENT` | W8.4, W8.5 and W8.6 |
| `GRANT_SHAPE` | A grant whose window, action set or own limits break a rule of W11.9 |
| `GRANT_DELEGATE` | A parent whose right of re-delegation breaks a rule of W11.10 |

A refusal of this section records no closure. Every code of the table is
new, and none replaces a code of an earlier format. The pipeline of a child
also reports three codes of LIP-0014, with the meaning that they have
there: `CHILD_SIGNER`, `CHAIN_DEPTH` and `NOT_DELEGABLE` (W11.8).

The table holds the codes of the pipelines and no code of an admission.
The codes that version 0.1.55 proposes for the admission of a child and
for a request are registered in section 11.11, in the table "Codes of
version 0.1.55", with the step of LIP-0014 section 8.4 at which each
stands. Only `CONTRACT_NOT_PRESENTED` is also reported by W9.4, solely for
the mandate branch defined there; no other code of that table is reported
by a pipeline of this section.

### 10. Vectors

[`vectors/LIP-0020/wire-vectors.json`](../vectors/LIP-0020/wire-vectors.json)
holds 219 vectors. Each names the rules that it exercises. The list
`rules` of the file names, for each of the 47 rules of sections 1 to 9, its
section, its state and at least one vector. The state of every rule is
`proposed`, also for the rules that carry the two decided points, because
no owner has accepted a byte.

Each group belongs to one stage, and the stage says what a checker does
with a vector and what it does not.

| Stage | Groups and vectors | What a checker does |
| --- | --- | --- |
| Document | `canonical`: 15 valid, 30 refused, 8 compound | W1.1 to W1.6 on octets, in the order of W9.2 |
| Integer | `integers`: 6 valid, 13 refused | W2.3 on the content of a string, for a bound of 2^64 - 1 |
| Primitive | `primitives`: 11 | Arithmetic on given octets under a given type string: the tag and the typed digest for each of the original seven types, a signature over a digest, the two SHA-256 values. No schema is consulted, and the octets are no valid object |
| Signed object | `assents`: 4 valid, 26 refused, 6 compound, 6 bindings; `identifiers`: 4 | The pipeline of a signed object on the signed form of an assent, and W7.2 with a stated context |
| Event | `consent_events`: 2 valid, 33 cases | The pipeline of a Nostr event with a stated context. For a recipient by name the context states what the verifier's node would find about the evidence output |
| Issuer | `issuer_checks`: 12 | What an issuer decides before it signs (W7.6, W7.8, W7.9), from its clock, its record of consumed consents and the facts of its snapshot |
| Issuance | `issuance`: 3 valid, 10 refused, 13 stored, 3 compound; and under `composed` 2 valid, 7 refused, 5 compound | The preparation, the commitment and the frame from the four inputs, with a stand-in of three values for the grant; the pipeline of an unsigned payload on stored octets of a preparation; and, under `composed`, the whole check of W9.4 on a presentation whose grant is given as stated facts |

A refused vector outside a `compound` group holds one defect, states the
expected code and names a valid neighbour of the same stage that differs
from it in that defect, in its octets or in its context. A vector of a
`compound` group holds several defects on purpose, lists them and states
the one that the order of W9.2, W9.3 or W9.4 reports; it has no neighbour.

A vector for a rule does not show the whole rule. Where a property has no
vector, the entry of its rule in `rules` says so under `not_covered`: a
member in the string form with a number in its place (W2.1) and arithmetic
at a bound (W2.4), because no complete type has such a member or computes;
a key of the place that comes from a pin (W5.5) and a reference from one
object to another (W6.3), because the one complete signed type names its
own key and refers to nothing; the largest size of the event (W7.3), which
refuses under the code of its spelling; and every read on a node (W7.6).

Two things about the file are limits and not defects of a reader that
finds them. The keys are the published test keys of BIP-340 and belong to
nobody. And the stand-in for a grant, octets that hold `type` alone, is
used as three given values and never as a grant. When the file was made a
reader of grants refused those octets as `WIRE_TYPE`; since version 0.1.53
a grant has members, and such a reader refuses them as `WIRE_MEMBER`
(section 12, `grant-i-05`). The file itself does not change. Vectors of
whole grants are in section 12; those of invocations and receipts come with
their members. Two properties that the list `rules` of the file marks as
not covered have vectors in section 12: a number where the string form is
required (W2.1), and arithmetic at a bound (W2.4).

No checker for these vectors is in this repository. The values were
computed by one implementation and recomputed, with the expected refusals,
by a second one that shares no code with the first; neither is published
here. LIP-0008 asks for a deterministic runner and for a second
implementation in Swift that consumes the same vectors on its own, and it
says that the agreement of two implementations is not the oracle. That
holds for these vectors: they bind nothing until both owners accept the
rules that they follow.

### 11. The members of `swarma-grant/4`

Until version 0.1.52 the registry gave the grant an identifier, a digest and
no member, so no reader could accept a v4 grant and no vector could hold one.
This section gives the grant its members: every member with its form, the
two member sets of a root grant and of a child, the right of re-delegation
with its groups, templates and ranges, the bounds, and the refusals with
their order. Section 12 holds the vectors.

**In force since version 0.1.53.** On 2026-11-16 Ivan Oparin ordered, as the
lead relayed it, that Grant v4 does not wait; the completion of v4 stands
before its freeze
([Decision 0004](../decisions/0004-reconciliation-closures.md)). The members
of the grant are therefore written here as text in force and not as a
proposal, without waiting for the co-author's agreement, which has not been
given; the co-author's answer is folded in by amendment. The section decides
no meaning. It carries, in octets, what LIP-0008, LIP-0014, LIP-0024, LIP-0026
and LIP-0027 state for a v4 grant, and each of those rules keeps the state
that its own text gives it: decided by both owners, in force on one owner's
decision, or Draft with the co-author's agreement pending. That state says
who has agreed, and it does not say whom the rule binds. Every decision that
this section carries binds a reader of `swarma-grant/4` from version 0.1.53,
under the owner's order that Grant v4 does not wait, and the co-author's
answer is folded in by amendment: J2, J4, CS1 to CS3 and J9 to J12 of
LIP-0014, and LIP-0008 sections 7.1 and 11.4. A draft's own additions bind
no reader until they are accepted: the script form of LIP-0026 R3.1 and
R8.2, LIP-0027 H1.2 and H1.3, and LIP-0023 C2.3. Where a rule that
is still pending needs a member, the member is here, so that the octets of
version `/4` do not change when the answer comes. Where the section had to
choose a name or a form that no decision gives, section 11.12 says so. One
shape that LIP-0008 permits has no octets here: several executors under
signed partitions for the own scope of one grant (LIP-0008 section 4). W11.4
gives a grant one executor, and a second executor takes a second grant.
Neither owner has reviewed the octets member by member, and no verifier
implements them: `tools/grantv4` reads a grant for the vectors of section 12
and admits nothing.

A grant is a signed object of this registry. A root grant is signed by the
grant key of its issuer. A child is signed by the delegation key that its
parent names. A root grant that carries the member `delegate` gives the
right of re-delegation and is called a parent.

#### 11.1. Forms

W11.1. Every member of a grant has one of these forms.

| Form | Octets | Refusal |
| --- | --- | --- |
| Hash | 64 lowercase hexadecimal characters (W3.5). A transaction id and a block hash stand in the byte order in which a node prints them | `WIRE_MEMBER` |
| Signing key | The x-only key of W3.6: a key under which a BIP-340 signature verifies | `WIRE_MEMBER` for the form; `WIRE_KEY` for a value that is no x coordinate of a point |
| Output key | A key that controls an output: 66 lowercase hexadecimal characters, of which the first two are `02` or `03` and the other 64 are the x coordinate of a point of the curve. It is the form of an owner pin (LIP-0021 O2.1) | `WIRE_MEMBER` for the form; `WIRE_KEY` for a value in that form whose coordinate is on no point |
| Text | A string of 1 to 255 characters, each from U+0020 to U+007E | `WIRE_MEMBER` |
| Short text | A text of at most 32 characters | `WIRE_MEMBER` |
| Outpoint | An object with exactly `txid`, a hash, and `vout`, an integer in the number form from 0 to 4294967295 | `WIRE_MEMBER`; `WIRE_INTEGER` for a `vout` above the bound |
| Script | Lowercase hexadecimal, an even number of characters from 2 to 200 | `WIRE_MEMBER` |
| Height | An integer in the number form, from 0 to 9007199254740991 | `WIRE_MEMBER` for a string; a number above the bound already refuses in the document step (`WIRE_NUMBER`) |
| Amount | An integer in the string form, from 0 to 18446744073709551615 | `WIRE_MEMBER` for a number; `WIRE_INTEGER` for the grammar and the bound (W2.3) |
| List | An array. Where the schema states a smallest or a largest count, a list outside it refuses | `WIRE_MEMBER` |

An object has exactly the members that its list states (W3.2). Where this
section gives an object alternative lists, it has exactly the members of one
of them. An integer below the smallest value that its member states refuses
as one above the largest does, as `WIRE_INTEGER`.

A signing key and an output key are two forms, and no reader converts one
into the other. A request key, an executor key, a grant key and a delegation
key sign, and they are signing keys. An owner key, a seal key and a
child-seal key control outputs, and the script that they pay commits to
their parity (LIP-0024 E1.2, LIP-0021 section 3), so they are output keys.
Where a rule compares keys of the two forms, it compares x coordinates
(LIP-0021 O2.3).

A text holds printable ASCII and nothing else. A name with another octet
is outside this profile, including its contract-free branch. A missing
consent is not the reason to reject the LIP-0035 exception.

#### 11.2. The payload

W11.2. The payload of a grant has the members of this table. The column
"In" says whether a member belongs to a root grant, to a child, or to both.
A payload that has the member `parent` is read under the list of a child,
and every other payload under the list of a root grant.

| Member | Form | In | Meaning |
| --- | --- | --- | --- |
| `type` | string | both | `swarma-grant/4` |
| `genesis` | hash | both | The chain of the grant: the hash of its genesis block, as in an assent (W7.1) |
| `contract` | hash | child required; root optional at wire stage | The identifier of the one bound contract. The root wire schema permits omission; W9.4 applies LIP-0035 semantic scope to both contract-free and optional-mandate roots (`UNILAT_SCOPE`, then `UNILAT_OBLIGATION_FORBIDDEN`), never to a child as an omission exception. A child requires it and absence is `WIRE_MEMBER` before scope. No other omission is admitted. `null` is never allowed. |
| `issuer` | object with exactly `name`, `registration`, `owner` and `grant_key` | root | The issuer, as LIP-0008 section 3 binds it |
| `issuer.name` | text | | The exact name of the issuer |
| `issuer.registration` | outpoint | | The transaction and the output that first registered that name |
| `issuer.owner` | output key | | The owner key of that name |
| `issuer.grant_key` | signing key | | The grant key. The signature of the signed form verifies under it (W11.8) |
| `parent` | hash | child | The identifier of the parent (W6.4) |
| `ordinal` | integer in the number form | child | The ordinal of the child's row. The schema states no bound of its own: an ordinal of 0, or one above the number of rows of the parent, is a well-formed member and refuses as `CHILD_ORDINAL` (LIP-0026 R2.1) |
| `recipient` | object | both | The recipient, in one of two modes (W11.3) |
| `executor` | object with exactly `name`, a text, and `key`, a signing key | both | The executor: a service name with its pinned public key (W11.4) |
| `actions` | list of texts | both | The closed action set (W11.4) |
| `limits` | list of limits | both | The own limits of the grant (W11.4) |
| `not_before_height` | height | both | The first height of the window (LIP-0008 section 7.1) |
| `not_after_height` | height | both | The height at which the window has closed: the window is half-open |
| `recent_block` | hash | both | The hash of the committed recent block (LIP-0008 section 7; LIP-0022 section 4) |
| `seal` | object with exactly `construction`, `kind`, `outpoint` and `key` | both | The seal of the grant (LIP-0008 section 11.4, SB1) |
| `seal.construction` | short text | | The construction profile of LIP-0008 section 1.1. The first profile writes `W` |
| `seal.kind` | short text | | The kind of seal. The first profile writes `revocable-only` |
| `seal.outpoint` | outpoint | | The transaction and the output index of the seal |
| `seal.key` | output key | | The seal public key. In a child it is the child-seal key of the parent (LIP-0014 CS2) |
| `delegate` | object (W11.5) | root, optional | The right of re-delegation. A root grant without the member gives none |

Ivan Oparin decided on 2026-11-20 (source: `$HZ30GFE5jwhKwwz9eDacfUnKf6nTRh2h-uF4OHylwD4`) to make `contract` optional for exactly
the scoped LIP-0035 case, amending W11.2. Co-author agreement on this Draft
decision is pending. No `authorization_mode`, `contract_hash`, `window` or
execution-mode member is added. `not_before_height`/`not_after_height` remain
the actual height members. A child still requires `contract`.

A child has no `issuer` and no `delegate`. Its authority comes from its
parent, whose issuer is the root of the path, and a path has two links
(LIP-0014 D7), so a child gives no right of re-delegation. A grant with
`issuer` and `parent`, a child with `delegate` and a child without `ordinal`
all refuse as `WIRE_MEMBER`.

The grant states the hash of its recent block and no height. A verifier
reads the height `R` of that block on its own node (LIP-0022 B4.2), and a
second place for it in the grant could only disagree with the first.

A reader of this section checks the form of `seal.construction` and of
`seal.kind` and not their values. Whether a verifier supports the profile
and the kind that a grant states is the check of LIP-0008 SB2, with the
code `SEAL_PROFILE`, at admission. The profile still comes from the
verifier's own configuration (LIP-0023 C1.1): the member lets a verifier
refuse a grant that was built for another profile, and it selects nothing.

A grant carries nothing beside these members. In particular it has:

- no descriptive member, and no recipient name as metadata (LIP-0008
  sections 3.1 and 12.3). The `grantee_name` of v3 is an unlisted member
  and refuses;
- no text and no hash of a text. Words that govern an agent's work stand
  in the contract, which `contract` binds (LIP-0017 section 1; LIP-0006
  section 7). The v4 octets that carry a scope text along a path are open
  (LIP-0014 section 3.4), and this section gives them no member;
- no typed constraint of an action beyond its limits: no list of targets,
  repositories, refs or payees. LIP-0008 section 2 and LIP-0014 section 3.4
  expect such members from the type profiles, and none defines one yet;
- no member for the owner's devices or for a statement key. The device
  list is pinned in the owner's name outside `swarma` and gives no grant
  authority, and there is no statement key (LIP-0029 O3.7, O10.5);
- no holder of a landlord. A class names landlords (W11.7), and the holders
  of a landlord are read at each admission from the list that the
  landlord's name pins, as LIP-0010 section 10 says;
- no stated identifier of itself, and no height of its recent block.

#### 11.3. The recipient

W11.3. `recipient` has exactly one of two member lists (LIP-0008 section
3.1):

| Mode | Members | Meaning |
| --- | --- | --- |
| By key | exactly `key`, a signing key | The request key |
| By name | exactly `name`, a text, and `owner`, an output key | The exact name and the owner key of that name. The request key is read from the name at every admission and is no member |

An object with `key` and a name, an object with neither, and a name without
its owner key refuse as `WIRE_MEMBER`. That is rule 1 of LIP-0008 section
3.1 as a rule of the schema.

#### 11.4. The executor, the actions and the limits

W11.4. A grant names one executor for its own scope, and its own limits
belong to that executor (LIP-0008 section 4).

`actions` is a list of texts in ascending order of their octets, without a
repeated text, so that one action set has one encoding. The list may be
empty; such a grant authorizes no action. Which texts name an action is for
the action registry (LIP-0007; LIP-0008 section 12.3), which is open. A
reader of this section compares texts and knows no action; an executor
refuses an action that its profile does not define.

A limit is an object with exactly `kind`, `resource` and `unit`, each a
text, and `amount`, an amount; it may also have `period`, a text. The key
of a limit is all of its members but the amount (LIP-0026 R1.2). A limit
without `period` and a limit with one have different keys. No two limits of
one list have the same key. `limits` may be empty: a request that consumes
a key for which the grant states no limit meets a ceiling of 0 (LIP-0026
R5.2).

A list of limits has no required order, and neither have `pools` and the
landlords of a class. Two payloads that differ only in the order of such a
list are both well formed, and they are two payloads with two identifiers.
Only `actions` and `notaries` have one encoding for one set. An issuer's
tool that wants one identifier for one set of limits orders them itself.

The texts of a limit are identifiers. Their registry, the meaning of each
kind, its unit, its period and its arithmetic come with the type profile of
the kind (LIP-0008 section 2; LIP-0018 section 2), and none is in force
yet; the first three profiles stand proposed by version 0.1.58 in
LIP-0031 and in the registry of W11.14, and a proposal defines no kind
at a side that runs none of it. A
verifier refuses the admission that an unknown kind affects; the document
with it is still a well-formed grant. A kind whose amount is a floor, as
the required confirmation depth, takes the same members.

#### 11.5. The right of re-delegation

W11.5. `delegate` has exactly these members; `child_seal_key` may be
absent:

| Member | Form | Meaning |
| --- | --- | --- |
| `key` | signing key | The delegation key: only it signs the children of this parent (LIP-0014 J4.1) |
| `child_seal_key` | output key | The child-seal key: the seal of every child pays it (LIP-0014 CS1, CS2). A parent without the member is a well-formed grant and unusable as a parent: every child of it refuses as `CHILD_SEAL_KEY` at its admission (CS1) |
| `actions` | list of texts, ascending and without a repeated text | The actions that a child may receive |
| `pools` | list of limits | One pool for every limit key that a template limits (LIP-0026 R8.5). The `amount` of an entry is the pool |
| `notaries` | list of at most 4 pins | The notaries that the parent pins (LIP-0014 D3, J3.1), in ascending order of their names and without a repeated name. A pin is an object with exactly `name`, a text, `registration`, an outpoint, and `owner`, an output key |
| `groups` | list of 1 to 16 groups | The rows, as groups (W11.6) |

The member is present or absent, and it has no member `depth`: a root grant
with `delegate` is a parent, and no other grant is. It has no checkpoint
either: on v4 the recent block of the grant takes that place (LIP-0014
section 2).

`notaries` may be empty. A parent none of whose templates names a certifier
pins no notary (LIP-0026 R10.1).

#### 11.6. Groups, ranges and the bounds

W11.6. A group is an object with exactly `template` (W11.7) and `ranges`, a
list of 1 to 16 ranges. A range has these members:

| Member | Form | Meaning |
| --- | --- | --- |
| `txid` | hash | The transaction of the coins of the range |
| `first` | integer in the number form, 0 to 4294967295 | The output index of its first coin |
| `count` | integer in the number form, 1 to 4096 | The number of its coins. Each coin is one row |
| `script` | script | The script of every coin of the range |
| `stop` | object with exactly `txid`, a hash, `first`, an integer from 0 to 4294967295, and `script`, a script. The member may be absent | The stop coins of the range. A range has the member exactly where the template of its group names a certifier; rule 5 of W11.10 judges that, and the member list does not |

The stop coins of a range are the outputs of the transaction `stop.txid`
from the index `stop.first` on, as many as the `count` of the range, each
with the script `stop.script`. The stop coin of the coin at the position
`i` of the range is the stop coin at the position `i`. Each row of a group
with a certifier therefore has a stop coin of its own, as LIP-0014 J2.7 and
LIP-0027 H1.1 ask, and a range states it once, as it states its coins.

The member list of a range is the same in every group: `stop` may be absent
at the member step (step 4), and it may be present there, whatever the
template says. Whether a range has the member is no question of that step.
Rule 5 of W11.10 judges the presence of `stop` in step 9: a range without
it in a group with a certifier, and a range with it in a group without one,
refuse as `GRANT_DELEGATE`, and neither refuses as `WIRE_MEMBER`.

An array keeps its order (section 1). The order of `groups` and of the
`ranges` of a group in the octets is the signed order in which LIP-0026
R8.3 counts the rows, and the coins of a range stand in ascending order of
their output index. A change of that order is another payload with another
identifier.

The bounds of a grant are these:

| Bound | Value | Refusal |
| --- | --- | --- |
| The signed form of a grant | 65536 octets | `WIRE_SIZE` |
| Nesting (W1.1) | 16 levels. The deepest member of a grant, the registration of a landlord of a class, stands at the tenth | `WIRE_SIZE` |
| Groups of a parent | 1 to 16 | `WIRE_MEMBER` |
| Ranges of a group | 1 to 16 | `WIRE_MEMBER` |
| Coins of a range | 1 to 4096 | `WIRE_INTEGER` |
| Notaries of a parent | 0 to 4 | `WIRE_MEMBER` |
| Landlords of a class | at least 1 | `WIRE_MEMBER` |

The actions, the limits, the pools and the landlords of a class have no
largest count of their own; the size of the signed form bounds them. A
parent has at most 256 ranges and 1,048,576 rows.

The largest counts of 16 groups, 16 ranges and 4096 coins and the largest
size of 65536 octets are the four numbers of LIP-0026 R8.4. They are decided
limits of the decision on groups (J12), in force since version 0.1.51. Here
and in LIP-0026 they have one state, bounds of the schema, and a document
outside them is no grant. Proposal Q1 of LIP-0026 would keep the size alone
and drop the three counts. It awaits the owner and changes nothing until the
owner decides: until then the counts bind every reader. If it is accepted,
the counts leave the schema by amendment; whether that amendment takes a new
version of the type under W3.3 is an open question of this LIP.

**On the register alone.** No statement of J12 in this specification names
a number. LIP-0014 ("Decisions of 2026-11-15", row J12) and LIP-0026 (its
table of decisions and the paragraph "The decision says this" of section 8)
state the decision in words, without the four. That J12 fixes 16, 16, 4096
and 65536 is said here and in LIP-0026 section 8 on the strength of the
owners' decision register, a record that this repository does not hold, and
each of the four numbers rests on that register alone. They bind as bounds
of the schema all the same. The mark stands until the statement of J12
carries the numbers and cites the record that they come from.

Three numbers of the table come from no decision on groups. The smallest
count of one group and of one range is **NEW**: J12 does not state it,
LIP-0026 R8.4 marks it NEW as well, and proposal Q1 asks for it. The largest
count of four notaries is LIP-0014 D3, agreed by both owners. The nesting of
16 levels is the proposal of W1.1. The smallest count of one coin is the
count of LIP-0026 R8.2, and the smallest count of one landlord is that of
R9.1.

#### 11.7. The template

W11.7. A template is an object with exactly `executor`, `recipient` and
`limits`, and exactly one of `certifier` and `no_certifier`.

| Member | Form | Meaning |
| --- | --- | --- |
| `executor` | as in W11.2 | The executor of every row of the group (LIP-0026 R8.1) |
| `recipient` | object in one of three lists | The recipient constraint (LIP-0026 R9.1) |
| `limits` | list of limits, as in W11.4 | The limits of each row of the group. The list may be empty |
| `certifier` | text | The `name` of one entry of `notaries`: the certifier of the rows of the group |
| `no_certifier` | the value `true` | The statement that the rows of the group have no certifier (LIP-0014 J9.1) |

The recipient constraint has exactly one of three member lists: `key`, as
in W11.3; `name` and `owner`, as in W11.3; or `class`, a list of at least
one pin in the form of W11.5. A class stands in a template alone: the
`recipient` of a grant itself is a key or a name (W11.3).

A template says in so many octets whether its rows have a certifier. A
template with neither member, and one with both, refuses as `WIRE_MEMBER`.
So do `no_certifier` with any other value than `true` and a `certifier`
that is the empty string, and `null` is no value at all (W1.4). No row is
without a certifier because a member was left out.

The form admits `no_certifier` beside any recipient constraint, and it
decides nothing about it. A template without a certifier is valid only where
its recipient is limited to the issuer's own landlord (LIP-0014 J9.2,
LIP-0026 R10.2), and W11.10 refuses every other one. The encoding widens
nothing of J9.

#### 11.8. Who signs, and the pipeline

W11.8. A grant is read through the pipeline of a signed object (W9.1), with
these points for its steps:

| Step | For a root grant | For a child |
| --- | --- | --- |
| 1. The document | The largest size is 65536 octets | The same |
| 4. The members | The lists of W11.2 to W11.7, in the order of W9.3 | The same |
| 6. The key of the place | `issuer.grant_key` of the payload | The `delegate.key` of the parent that the reader has already read through this pipeline. First `parent` equals the identifier that the reader recomputed from that parent (`WIRE_ID`); a child that is presented without its parent refuses with the same code. Then the parent is no child (`CHAIN_DEPTH`) and carries `delegate` (`NOT_DELEGABLE`) |
| 7. The signature | `WIRE_SIGNATURE` | `CHILD_SIGNER` (LIP-0014 J4.1) |
| 8. References | A reference to the grant from another object equals its identifier (`WIRE_ID`): the `grant_id` of a preparation (W8.1), the `parent` of a child | The same |
| 9. The rules of the object | W11.9, then W11.10 | W11.9 |

For a child the reference to its parent stands in step 6 and not in step 8,
because that reference selects the key. A child that is signed by another
key and presented with another parent refuses as `WIRE_ID`.

The key of a root grant is a member of its payload, as the `party` of an
assent is. The pipeline shows that the holder of that key signed the grant.
That the key is the grant key of the pinned issuer is the issuer rule of
LIP-0008 section 3, which a verifier checks on its node at admission, and no
step of this pipeline replaces it.

`CHILD_SIGNER`, `CHAIN_DEPTH` and `NOT_DELEGABLE` are codes of LIP-0014
(J4.1 and section 4), used here with the meaning that they have there. A
signature of a child that fails under the delegation key refuses as
`CHILD_SIGNER`, whichever key made it: a reader cannot tell a signature by
another key from one that verifies under none.

A child is signed by the delegation key under LIP-0014 J4, a decision that
awaits the co-author's agreement. This section carries it, as the first
paragraphs say, and it binds a reader as every carried decision does: for
the octets of `swarma-grant/4` the rule in force since version 0.1.53 is
this one, W11.8. LIP-0008 section 12.6 and LIP-0014 section 11.1 call the
signature by the parent's recipient "the rule in force", and each of them
points here for the octets of `swarma-grant/4`. The same carriage gives every reader the window rule of LIP-0008 section
7.1 (W11.9 rule 1) and the stop coin of a row of LIP-0014 J2.7 (W11.6 and
W11.10 rule 5).

#### 11.9. The rules of every grant

W11.9. After its signature a grant meets these rules, in this order, or
refuses as `GRANT_SHAPE`:

| # | Rule | From |
| --- | --- | --- |
| 1 | `not_before_height` is lower than `not_after_height` | LIP-0008 section 7.1, rule 1 |
| 2 | `actions` stands in ascending order of its octets and repeats no text | W11.4 |
| 3 | No two entries of `limits` have the same key | LIP-0026 R1.2 |

The rules that need a chain are no part of this list: that the window does
not open below the recent block, that it does not pass the expiry of the
issuer's name, and every rule of sections 3 to 7 of LIP-0008.

#### 11.10. The rules of a right of re-delegation

W11.10. LIP-0026 R1.5 refuses a parent that breaks a rule of its rows and
leaves the code to the members of the grant. The code is `GRANT_DELEGATE`.
These are the rules that a reader judges on the signed octets of a parent
alone. All of them report the one code, so their order shows only where a
reader explains its refusal. The column "Judged" says whether every reader
of this section judges the rule, and which decision or text gives it:

| # | Rule | From | Judged |
| --- | --- | --- | --- |
| 1 | `delegate.actions` stands in ascending order and repeats no text | W11.5 | By every reader. The form of the member in W11.5 |
| 2 | No two entries of `pools` have the same key | LIP-0026 R8.5 | By every reader. W11.4 for a list of limits; J12 gives a limit key one pool |
| 3 | `notaries` stands in ascending order of its names and repeats no name | LIP-0014 section 2 | By every reader. The form of the member in W11.5 |
| 4 | For each group, in the order of the groups: no two limits of the template have the same key (R1.2); no two landlords of a class have the same name (R9.1); a `certifier` is the `name` of an entry of `notaries` (R10.1); a template with `no_certifier` has a recipient that is a name with its owner key, or a class of exactly one landlord whose `name`, `registration` and `owner` equal those of `issuer` (R10.2) | LIP-0026 | By every reader. W11.4 for the limits of a template; J10 for a class (R9.1); W11.7 for the name of the certifier; J9, agreed by both owners, for a template without a certifier (LIP-0014 J9.1 and J9.2) |
| 5 | For each range of that group, in the order of the ranges: `first` plus `count` minus 1 is at most 4294967295, and `script` is a witness key hash, the octets `00 14` and 20 further octets (R8.2, R3.1); the range has `stop` exactly where the template names a certifier (LIP-0027 H1.1, LIP-0014 J9.4); `stop.first` plus `count` minus 1 is at most 4294967295, and `stop.script` is a witness key hash (H1.2) | LIP-0026, LIP-0027, LIP-0014 | By every reader: the index of the last coin, since a coin is an output and no output has a higher index (W11.1; R8.2 under J12); no `stop` where the template has no certifier (LIP-0014 J9.4, which is LIP-0026 R10.5, agreed by both owners and text in force); `stop` where the template names a certifier (LIP-0014 J2.7 as this section carries it, and W11.6); the index of the last stop coin, which is an output as a coin is (W11.1, W11.6). Proposals, see below: the witness key hash form of `script` and of `stop.script` |
| 6 | The keys of `pools` are exactly the keys that a template limits. For each key the sum, over the groups, of the number of rows of the group times the amount of its template is at most the pool. The sum is an exact integer sum (W2.4) | LIP-0026 R8.5 | By every reader. J12: the pool bounds the sum, and a key that no row limits has no pool |
| 7 | No output is a coin of two rows: two ranges with one `txid` have index intervals that do not meet. No coin is the outpoint of `seal` | LIP-0026 R8.6 | By every reader. J12 |
| 8 | No output is a stop coin of two rows: two runs of stop coins with one `stop.txid` have index intervals that do not meet. No stop coin is a coin of a row, the outpoint of `seal`, or the output after it in the same transaction | LIP-0014 J2.7, W11.6; LIP-0027 H1.3, LIP-0023 C2.3 | The first sentence: by every reader. Each row with a certifier has a stop coin of its own (LIP-0014 J2.7 as this section carries it, and W11.6), and one output is not the own coin of two rows. The second sentence, the placement points: proposals, see below |

The sum of rule 6 can pass 2^64 - 1 while every amount is within its bound.
A reader adds exactly and refuses; it never wraps.

A rule that every reader judges is a rule of this section, in force with
it. A reader that reads a parent through the pipeline of W11.8 judges each
of them, and a parent that breaks one refuses as `GRANT_DELEGATE`. The
decision or the text that the column names gives the rule; this section
adds the code, the place of the rule in step 9 and the order of the table.

Three points on `stop` are among those rules, and no reader leaves them
out: a range has no `stop` where its template has no certifier; a range has
`stop` where its template names one; and the last stop coin of a run has an
index of at most 4294967295. The first is a decision of both owners. The
second is a decision that this section carries before the co-author's
agreement, and it binds as the first paragraphs of this section say. The
third follows from the forms of W11.1 and W11.6, as it does for the coins
of a range.

Two points of the table are proposals, additions of drafts that bind no
reader until they are accepted, and this section carries them without
deciding them:

- the witness key hash form of `script` and of `stop.script` in rule 5
  (LIP-0026 R3.1 and R8.2, which that LIP keeps outside its subset in
  force; LIP-0027 H1.2);
- the placement points of rule 8: no stop coin is a coin of a row, the
  outpoint of `seal`, or the output after it (LIP-0027 H1.3; LIP-0023 C2.3
  for the output after the seal).

This version does not determine that a reader judges them. It does fix the
code: a reader that judges a proposal point of W11.10 and finds it broken
reports `GRANT_DELEGATE` in step 9, and no other code and no earlier step.
In particular the Script form of W11.1 is not narrowed to a witness key
hash, and a script that is none passes the member step. A reader that does
not judge these points reads a parent that breaks one of them, and nothing
else, as a well-formed parent. Such a parent therefore passes steps 1 to 8
at every reader and has two conforming outcomes, `ok` and `GRANT_DELEGATE`;
any other code is a defect of the reader. The group `undetermined` of
section 12 holds these parents.

The result of the pipeline is a statement about a document. It does not say
what a verifier must have read before it admits a child or a request of the
parent's own. That is the question of proposal Q1 of LIP-0026, the refusal
of a whole parent at admission, and this section does not decide it: under
the profile in force a verifier checks the group and the range of its child
(LIP-0026, "Owner decision proposals"), and a verifier that has read the
whole parent through this pipeline knows more than that profile asks. The
vectors of section 12 state the result of the pipeline and no admission.

One rule on the octets of a parent has its code elsewhere. The delegation
key and the child-seal key differ from each other and from the other keys
of the parent, compared by x coordinate (LIP-0014 J4.3 (a), CS3): from
`issuer.grant_key`, from `recipient.key` or `recipient.owner`, from
`issuer.owner`, from the `owner` of every entry of `notaries` and from
`seal.key`. A parent that breaks it is unusable as a parent, and every
child of it refuses as `DELEGATE_KEY_REUSE` at its admission. The parent
itself is still read.

#### 11.11. Which rule reads which member

The rules that admit a grant stand in other LIPs and read the members of
this section. No rule of this table is changed here.

| Rule | Members that it reads |
| --- | --- |
| The issuer rule (LIP-0008 section 3; LIP-0021 section 7.1) | `issuer.name`, `issuer.registration`, `issuer.owner`, `issuer.grant_key`, `recent_block` |
| The window (LIP-0008 section 7.1) and the recent block (LIP-0022 section 4) | `not_before_height`, `not_after_height`, `recent_block` |
| The seal (LIP-0008 SB2, SB3; LIP-0024 E1.2) and the linkage output (LIP-0023 C2.3) | `seal` |
| The contract seal (LIP-0017 section 6, rule 6), only when a contract is bound | `contract` alone: its document names its own seal and, where applicable, one framework contract, whose document names its own seal. Both documents are presented or resolved and recompute to their identifiers; each seal's confirmation and script are read on the side's own node. No grant member names either seal or is compared by this check |
| The assent, the consent and the issuance (sections 7 and 8) | Contract-binding path: `genesis`, `contract`, `issuer.grant_key`, `recipient`. The LIP-0035 branch uses preparation `/2` and its existing identity checks, without assent/consent evidence or a `contract` member |
| A recipient by name (LIP-0008 section 3.1; LIP-0021 section 7.2) | `recipient.name`, `recipient.owner` |
| The executor and the action (LIP-0008 section 4) | `executor`, `actions` |
| The accounts of a request (LIP-0026 section 5) | `limits`; for a request under a child also the limits of the template of its row |
| The row of a child (LIP-0026 R2.1 to R2.5, R8.3, R8.8) | `ordinal` of the child; `groups` of the parent with the `count` of each range; `executor`, `recipient` and `limits` of the child and of the template |
| The coin of a row (LIP-0026 R3.2 to R3.4) | `txid`, `first` and `script` of the range; `seal.outpoint` of the child; `recent_block` of the parent |
| The class and a row without a certifier (LIP-0026 sections 9 and 10) | `recipient.class` or `recipient.name` of the template; `issuer`; `recent_block` of the parent |
| The notary of a child (LIP-0014 section 7.1) | `notaries`, `certifier`; `recent_block` of the parent as the checkpoint |
| The signer and the seal of a child (LIP-0014 J4.1, J4.3, CS2, CS3) | `delegate.key`, `delegate.child_seal_key`; `seal.key` of the child |
| The stop coin of a row (LIP-0027 section 2) | `stop` of the range; `seal.outpoint` of the child; `recent_block` of the parent |
| A child within its parent (LIP-0008 sections 12.2 and 12.5) | `genesis`, `actions` and the window of the child; `genesis`, `delegate.actions` and the window of the parent |

Before version 0.1.55 no text named a v4 code for the last row, and no rule
said whether a child binds the contract of its parent. Version 0.1.55
proposes both in W11.11. That version changed no row of the member table;
version 0.1.61 adds the contract-seal row. No member changes.

W11.11 (proposed by version 0.1.55). A child lies within its parent in four
comparisons of signed octets. Each is made by the signing service before
it signs a child and by every verifier at admission, at the step that
LIP-0014 section 8.4 gives it, and with the same code on both sides: the
observation of a side stands before all four at the signing service and at
a verifier alike (LIP-0014 section 8.4, pair Q3; section 8.5, I3 before
I4).

| # | Rule | Refusal | Step of LIP-0014 section 8.4 |
| --- | --- | --- | --- |
| 1 | The member `contract` of the child equals the member `contract` of the parent. The comparison is of the two values as the two payloads hold them, 64 hexadecimal characters each (W11.2), and of no octet of a contract document | `CHILD_CONTRACT_DIFFERS` | F5 |
| 2 | Every text of `actions` of the child is a text of `delegate.actions` of the parent. The texts are compared as octets, and an empty list passes | `CHILD_ACTIONS_WIDER` | F16 |
| 3 | `not_before_height` of the parent is at most `not_before_height` of the child, and `not_after_height` of the child is at most `not_after_height` of the parent. The comparison is of heights and of nothing else | `CHILD_WINDOW_NOT_NESTED` | F18 |
| 4 | `genesis` of the child equals `genesis` of the parent | `SUBJECT_MISMATCH` | F8 |

Rule 1 is a new restriction of this version, and so is its code. A v4
grant carries no text, and the words that govern an agent's work stand in
the contract that `contract` binds (W11.2). Both owners agree that on v4 a
re-delegation narrows only typed fields and appends no text (LIP-0014
section 3.4). That agreement fixes no byte, and it does not by itself
forbid a second contract that carries the same text: a child that bound a
narrower contract of its own would meet every sentence of it. Rule 1 does
not follow from the agreement. It is a choice, and it needs the owners'
decision: until a profile states how the contract of a child narrows the
contract of its parent, this version admits none, so that no words reach a
path that the parent's contract does not hold. A later profile that lets a
child bind a narrower contract of its own replaces the rule by amendment.
The bytes that the rule compares are fixed, the two values of the member
`contract`. One thing behind them is not: the preimage of the identifier is
open (LIP-0017 section 2), so the rule says that two grants name one
identifier and says nothing yet about the octets of a contract. The rule
does not say which key assents to the contract for the delegating side,
which stays open (W7.2). A contract that is not presented and a contract
whose octets do not recompute to the identifier are two further findings,
with the codes `CONTRACT_NOT_PRESENTED` and `CONTRACT_ID`. They are decided
after rule 1, which signed octets alone decide (LIP-0014 section 8.4, rows
F5 and F6, rule T1 and pair Q5).

Rules 2, 3 and 4 are LIP-0008 sections 12.2 and 12.5 on these members. Their
codes are the codes that LIP-0014 section 4 names for the same comparisons
of the v3 contract profile: a set that is no subset, a window that is not
nested, another chain. A v3 code is taken where the v4 comparison is the
same relation on the corresponding members, whether or not v3 compares
further members under it (LIP-0014 section 8.4, rule T4): `SUBJECT_MISMATCH`
reports on v4 the one member `genesis` of the three that step V6 compares.
They are taken as LIP-0026 section 2 takes the four codes of a row. The
rules are landed text; that these codes report them on v4 is the proposal
of this version. The window is a
pair of block heights (LIP-0008 section 7.1; Ivan Oparin's decision of
2026-11-16 that the window of a v4 grant is stated in heights only), and
rule 3 never reads a clock: the clock of an invocation is a rule of the
invocation. That the child's own window is not empty is rule 1 of W11.9.

The four are checks of an admission and no step of the pipeline of W11.8:
a child that breaks one is a well-formed child, a reader of documents
reads it without a refusal, and no vector of section 12 changes. The state
of W11.11 is that of LIP-0014 section 8.4: a proposal of version 0.1.55,
which binds a reader of `swarma-grant/4` when the version lands, with the
co-author's answer folded in by amendment.

**Codes of version 0.1.55.** Six codes are new with version 0.1.55, and
three codes of v3 are taken for v4. This table registers all of them for a
checker; each is proposed with the row of LIP-0014 section 8.4 that reports
it. Only `CONTRACT_NOT_PRESENTED` is also used by the Draft mandate branch
of W9.4; the ordinary `/1` pipeline reports none of these codes. "Again" is
the mark of LIP-0014 section 8.4 for what a refusal leaves behind.

| Code | What it reports | Step | Again | Defined by | State |
| --- | --- | --- | --- | --- | --- |
| `CHILD_CONTRACT_DIFFERS` | The member `contract` of a child differs from that of its parent | F5 | no | W11.11, rule 1 | New code, new rule |
| `CONTRACT_NOT_PRESENTED` | No contract document is presented for the identifier that the grants of a path bind, or, since the proposal of 0.1.61, for the framework identifier that document names; also missing mandate bytes on W9.4's selected mandate branch | Mandate-only issuance W9.4 step 1, before mandate checks; path F6, part (a), unchanged; never ordinary `/1` issuance | input | LIP-0014 section 8.4, rules T1 and T11; Draft W9.4 mandate branch | New code, new rule; framework presentation added by 0.1.61 |
| `CONTRACT_ID` | A presented document does not recompute to its required identifier: the bound contract to the identifier of the grants, and, since the proposal of 0.1.61, the framework contract to the identifier the bound document names (LIP-0017 section 2). Not computable until its v4 contract profile fixes the preimage; a mandate mismatch uses W9.4's `UNILAT_MANDATE_MISMATCH` instead | Path F6, part (b), unchanged; not W9.4 issuance | no | LIP-0014 section 8.4, rules T1 and T11 | New code, new rule; framework recomputation added by 0.1.61 |
| `CHILD_NOT_LIVE` | A child that its own closure or its own window refuses: a journaled closure, a window that opens below its recent block, a window that has not opened, a window that has ended, a spent seal | F20, F21 | closed for a closure and a validated spend; state for the window | LIP-0014 section 8.4, rule T3 | New code for rules of LIP-0008 sections 5.1 and 7.1 |
| `ACTION_UNDEFINED` | A request for an action that no type profile of the executor defines | E1 | no, under one profile | W11.14, rule 1 | New code for the rule of W11.4 |
| `LIMIT_KIND_UNDEFINED` | A limit of a child or of its row whose kind has no type profile at the side; a request that consumes a kind without a profile | F17, part (b); E2 | no, under one set of profiles | W11.14, rule 2; LIP-0014 section 8.4, rule T9 | New code for the rule of W11.4 |
| `SUBJECT_MISMATCH` | `genesis` of a child differs from that of its parent | F8 | no | W11.11, rule 4 | Code of LIP-0014 section 4, taken for v4 |
| `CHILD_ACTIONS_WIDER` | An action of a child is no entry of `delegate.actions` of its parent | F16 | no | W11.11, rule 2 | Code of LIP-0014 section 4, taken for v4 |
| `CHILD_WINDOW_NOT_NESTED` | The window of a child does not lie inside the window of its parent, in heights | F18 | no | W11.11, rule 3 | Code of LIP-0014 section 4, taken for v4 |

Three names are chosen against confusion with a neighbour, and two of them
replace names of the first draft of this version. `CONTRACT_ID`, first
called `CONTRACT_ID_MISMATCH`, is not `CONTRACT_MISMATCH` of LIP-0013
section 2.5, which reports that fields of a v3 contract differ from fields
of its grant, and not `CONTRACT_HASH` of the same section, which reports a
plain hash. The v4 counterpart of `CONTRACT_MISMATCH`, the mirror of the
terms of a grant in its contract, has no code yet; it gets one with the v4
contract profile, as part (d) of row F6, part (c) through version 0.1.60. `CHILD_CONTRACT_DIFFERS`, first
called `CHILD_CONTRACT_MISMATCH`, follows `CHILD_TEXT_DIFFERS` of LIP-0014
section 3.4, which reports the same relation between a child and its
parent for a text hash. `CONTRACT_NOT_PRESENTED` reports a missing input
and no finding about a contract.

**Codes of version 0.1.61.** Two further codes are defined here, for a
checker, proposed with the row that reports them and reported by no
pipeline of section 9. They are no fifth comparison of W11.11: the four
above compare a child with its parent on their signed octets. This check
holds a root or child against the seals of its bound contract and, where
named, its framework contract, in that order. Both documents are presented
or resolved and recomputed before any seal read. Within each seal check,
no seal named refuses first without a node read; otherwise an inconclusive
read is pending, and only a conclusive read judges confirmation, index
and script. At a child this is F6(c), after document recomputation (b)
and before the open profile findings (d) (LIP-0014 section 8.4, rule T11).
For a root, LIP-0017 section 6, rule 6, states the same duty and codes;
their place against other root checks remains open, including in
LIP-0030 C6 (**P**, no root order proposed).

| Code | What it reports | Step | Again | Defined by | State |
| --- | --- | --- | --- | --- | --- |
| `CONTRACT_SEAL_MISSING` | The bound contract or its named framework contract names no seal; or a conclusive own-node read in this observation proves its named transaction not confirmed in the active chain (a held mempool-only transaction included), no output at the named index, or another script. An unknown transaction or inconclusive read never gives this code. A confirmed-as-named seal that is spent is not this code; its spend gets no step or code here. No signature or admission | F6, part (c) for a child; root place open | no where no seal is named; state for a conclusive node finding; no closure | LIP-0017 section 6, rule 6; LIP-0014 section 8.4, rule T11 | The refusal at both sides is decision C12 of LIP-0017 (Ivan Oparin, 2026-11-17); the co-author agrees and leaves the judgement to Ivan. The code name and step are proposals of 0.1.61 |
| `CONTRACT_SEAL_UNAVAILABLE` | A seal is named in the bound contract or its named framework contract, but the own-node read proves nothing about its confirmation, index or script, including a named transaction unknown to that node. It proves neither absence nor a spend, even when another node can read a confirmed-and-spent transaction. No signature or admission | F6, part (c) for a child, before classifying a node finding as missing; root place open | pending; no closure | LIP-0017 section 6, rule 6; LIP-0014 section 8.4, rule T11 | The code name, retry mark and step are proposals of 0.1.61; unavailable data permits no effect under LIP-0008 section 4, step 3 |

The names are chosen against the same neighbours: neither is `SEAL_OUTPUT`,
`SEAL_SCRIPT` or `SEAL_PROFILE`, which report the seal that a grant itself
names in its member `seal` (LIP-0008 SB2), and not `CONTRACT_ID` or
`CONTRACT_NOT_PRESENTED`, which report the document. One name covers the
seal that the document does not name and the seal that it names without
the confirmed output behind it, because decision C12 gives both one
answer: no grant under that contract.

Open beside these codes, and named in LIP-0014 section 8.4 as O2 to O4: the
code of a request that is not authenticated, the codes of the checks of an
invocation, and the two codes that follow the contract identifier, for a
contract that is no valid contract of its profile and for one that does not
mirror the terms of its grant. One further open code is O5 there, the code
of a journal of closures of a grant that cannot be read.

One code of this section is reported at an admission as well, under the
same proposal. `GRANT_DELEGATE` is the code of step 9 for the rules of
W11.10. At the admission of a child LIP-0014 section 8.4 asks for rules 1
and 3 with the parent (row F1) and for rules 4 and 5 for the group and the
range of the child alone (row F13, part (b), rule T10). What a side does
with a finding of rules 2 and 6 to 8, whether or not octets of that group
or range take part in it, and with a finding of rules 4 and 5 in another
group or range, stays where the last paragraphs of W11.10 leave it, with
proposal Q1 of LIP-0026, and is open point O7 of that table. The result of the pipeline
for a document does not change: a reader of a parent as a document judges
every rule of W11.10 that every reader judges, in step 9.

#### 11.12. Where each member comes from

The table names, for each choice of this section, the text that it carries.
"Form chosen here" marks a name or a form that no decision gives; the
owners may change each of them.

| Choice | Carries | State of what it carries |
| --- | --- | --- |
| `genesis`, `contract` | LIP-0008 section 1; the same members of the assent (W7.1) | Draft |
| `issuer` with name, registration and owner key | LIP-0008 section 3, decision of 2026-11-11 | Draft; the member names are those of LIP-0024 E2.1 |
| `issuer.grant_key` in the payload | LIP-0008 section 3, rule 3 and section 5.2: a grant binds its issuer key; W5.5 | Form chosen here |
| Owner keys, seal keys and the child-seal key as compressed keys | LIP-0021 O2.1; LIP-0024 E2.1, E2.3; LIP-0014 CS1 | Proposals of those LIPs |
| `recipient` in two modes | LIP-0008 section 3.1, decision of 2026-11-10 | Draft |
| One `executor` with name and key | LIP-0008 section 4; LIP-0026 R1.1 | Draft. That the own scope has one executor and no list of partitions is chosen here |
| `actions`, sorted | LIP-0008 section 1; the order follows LIP-0014 section 2 | The order is chosen here |
| A limit with kind, resource, unit, amount and period | LIP-0026 R1.2; LIP-0008 section 2 | Proposal of LIP-0026; the member names are chosen here |
| An amount in the string form up to 2^64 - 1 | Section 2 | Proposal of this LIP |
| The window as two heights | LIP-0008 section 7.1, decision of 2026-11-11; the names are its logical names | Draft |
| `recent_block` as a hash without a height | LIP-0008 section 7; LIP-0022 B4.2 | Draft; the name is chosen here |
| `seal` with profile, kind, outpoint and key; no endorsement | LIP-0008 section 11.4 (SB1), decision of 2026-11-16 | Draft, agreement pending. The names follow LIP-0024 E2.1 |
| `parent` and `ordinal` of a child | LIP-0008 section 12.2; LIP-0014 J1.2, agreed by both owners | Decided; the names are chosen here |
| `delegate` present or absent, without `depth` | LIP-0014 D7; W1.4 | Form chosen here |
| `delegate.key` | LIP-0014 J4, decision of 2026-11-14, which names the member | Agreement pending |
| `delegate.child_seal_key`, which may be absent | LIP-0014 CS1 and case S4-10, decision of 2026-11-16: a parent without the key is unusable as a parent | Agreement pending; the name is chosen here |
| `delegate.actions` | LIP-0008 section 12.2; LIP-0014 section 2 | Draft |
| `pools` | LIP-0026 R8.5 (J12) | In force since version 0.1.51 |
| `notaries` as at most four pins, sorted | LIP-0014 D3 and J3.1, both agreed by both owners; LIP-0026 R10.1 | Decided; the order follows LIP-0014 section 2 |
| `groups`, `template`, `ranges` and the members of a range | J12, as LIP-0026 section 8 states it | In force since version 0.1.51; the member names are chosen here |
| The counts 16, 16 and 4096 and the size 65536 | J12, as LIP-0026 R8.4 states it | Decided limits, in force since version 0.1.51; bounds of the schema here and there. **On the register alone:** no statement of J12 in this specification names one of the four numbers, and each rests on the owners' decision register, which this repository does not hold (W11.6). Proposal Q1 of LIP-0026 would drop the three counts and awaits the owner |
| At least one group and one range | LIP-0026 R8.4 | **NEW**, here and there: no decision states the number |
| The three forms of a recipient constraint | J10, LIP-0026 R9.1 | In force since version 0.1.51 |
| `certifier` or `no_certifier`, one of them always | J9, LIP-0014 J9.1 and LIP-0026 R10.1: a row states its certifier or states that it has none | Decided by both owners; the two members are the form chosen here |
| `stop` of a range | LIP-0014 J2.7, LIP-0027 H1.1: one stop coin for each row with a certifier | Agreement pending, and carried: the presence of `stop`, the last index of its run and a stop coin of its own for each row bind every reader (W11.10 rules 5 and 8). That a row without a certifier has none is LIP-0014 J9.4, decided by both owners. No decision places the stop coins of a group; the place is chosen here |
| No member for holders | LIP-0010 section 10 | In force since version 0.1.51; the hash-pinned list since version 0.1.53 |
| `GRANT_SHAPE`, `GRANT_DELEGATE` | LIP-0026 R1.5 leaves the code of a refused parent to the members | Chosen here. For the proposal points of W11.10 the code is fixed as well: a reader that judges one reports `GRANT_DELEGATE` in step 9. Whether a reader judges them is open with the proposals |
| The rules of W11.10 that every reader judges | The decisions and texts that the table of W11.10 names for each | **NEW** as rules of a reader, and marked for the owner: a reader of a document refuses on the rules of W11.10 that a decision gives. That is said here, and it awaits the owner's line. The review of record of these members recommends "yes". What a verifier reads at admission stays with proposal Q1 of LIP-0026 |

#### 11.13. An example

The payload of the vector `grant-v-01`, with line breaks and indentation
for display only:

```json
{
  "actions": [
    "example/instruct",
    "example/review"
  ],
  "contract": "6e01e587b9931de4a32076d48cd9a64460d6fa0aeaac953e19201127a4d7afbf",
  "executor": {
    "key": "fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556",
    "name": "id/lip0020-executor"
  },
  "genesis": "000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770",
  "issuer": {
    "grant_key": "f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",
    "name": "id/lip0020-issuer",
    "owner": "02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13",
    "registration": {
      "txid": "5bc5c54e3b97b2214915d1e83786483a05a2928f0b9990f54bbd83e79170b22f",
      "vout": 0
    }
  },
  "limits": [
    {
      "amount": "1000",
      "kind": "example/requests",
      "period": "example/hour",
      "resource": "example/model-a",
      "unit": "request"
    },
    {
      "amount": "18446744073709551615",
      "kind": "example/tokens",
      "resource": "example/model-a",
      "unit": "token"
    }
  ],
  "not_after_height": 252560,
  "not_before_height": 200000,
  "recent_block": "ec5f2fc0c0b09fa7fd89bbaf58cb99c411164cb6f8dc598dee59c8a5ebe7d195",
  "recipient": {
    "key": "dff1d77f2a671c5f36183726db2341be58feae1da2deced843240f7b502ba659"
  },
  "seal": {
    "construction": "W",
    "key": "022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01",
    "kind": "revocable-only",
    "outpoint": {
      "txid": "13fb02c63c5edf9e5117361990df250714b1ef528afaac4896b273007c9df619",
      "vout": 0
    }
  },
  "type": "swarma-grant/4"
}
```

Its identifier is
`294f4517c58e44cf34b61900254c0d2acdf9801cc69492e322325f09d51c1062`, its
typed digest is
`10e12b7359f296bdc3b0288bb36fe845800bd8446e3652f8ed4e238da6f9b7f4`,
and the signed form with the signature of that vector has 1464 octets. The
names, the actions and the texts of the limits are placeholders, and the
transaction ids and the recent block name no transaction and no block.

#### 11.14. Action identifiers and limit kinds

W11.4 says that the texts of `actions` and the texts of a limit are
identifiers, and that their registries are open. This subsection, a
proposal of version 0.1.55 with the state of W11.11, states the two
registries as they stand and the two rules that follow from them, for an
executor at a request and, for a limit kind, for both sides at the
admission of a child. It adds no member and changes no
octet: a reader of documents still compares texts and knows no action and
no kind.

W11.14. The registry of action identifiers lists the texts that a type
profile of this specification defines as an action, with the profile that
defines each (LIP-0007; LIP-0008 section 12.3; LIP-0018 section 3). The
registry of limit kinds lists the texts that a type profile defines as the
`kind` of a limit, with its units, its periods and its arithmetic (LIP-0008
section 2; LIP-0018 section 2).

| Registry | Entries as they stand in version 0.1.67 |
| --- | --- |
| Action identifiers | PROPOSED in [LIP-0030 section 3](LIP-0030-action-profile-agent-session.md#3-the-actions-and-the-limit-kinds): `swarma/station/agent/start`, `swarma/station/agent/restart`, `swarma/station/agent/renew` and `swarma/station/agent/stop`. Its `swarma/station/agent/halt` is an owner command, not a grant action. PROPOSED in [LIP-0038 section 7](LIP-0038-action-profiles.md#7-the-proposed-registry-rows): `swarma/post-message`, `swarma/spend-coins`, `swarma/name-update` and `swarma/model-call`. Each keeps the state of its defining profile; a side running none still refuses under rule 1. The v3 names of LIP-0014 D12 and the placeholder actions of section 12 define none of these leaves |
| Limit kinds | PROPOSED since version 0.1.58 in [LIP-0031](LIP-0031-limit-kinds-1.md): `swarma/coins`, `swarma/model-cost` and `swarma/model-tokens`, reused without a second definition by LIP-0038 section 6. LIP-0038 P6.1 records the owner-decided settlement choice, not adoption of the other rules. PROPOSED separately in LIP-0030 section 3: `swarma/station/agent/starts`, `swarma/station/agent/level` and `swarma/station/agent/span`; those accounts/checks are not the shared kinds of LIP-0031. A side running no profile of a kind still refuses under rule 2. One text stays reserved and undefined: `policy` (LIP-0008 section 12.4) |

| # | Rule | Refusal |
| --- | --- | --- |
| 1 | An executor MUST refuse a request whose action no type profile under which it runs defines. That the text stands in `actions` of the grant does not define it | `ACTION_UNDEFINED` |
| 2 | A limit of an undefined kind is never read as no limit. At the admission of a child, the signing service and a verifier MUST refuse a child where the kind of a limit of the child or of the template of its row has no type profile at that side (LIP-0014 section 8.4, row F17, part (b)). An executor MUST refuse a request that consumes a limit kind for which it has no type profile (row E2). A request that needs `policy` refuses in this way | `LIMIT_KIND_UNDEFINED` |
| 3 | An entry joins a registry by the LIP that defines its profile. A text under `swarma/` is assigned by this specification alone (LIP-0008 section 12.3) | None: a rule of the registries, which no reader and no executor judges |

Rule 1 is a refusal of a request, after the grant and, for a child, its
path were admitted: step E1 of LIP-0014 section 8.4. Rule 2 has two places.
W11.4 says that a verifier refuses "the admission that an unknown kind
affects", and it names no code and no step. For a child, the kinds of the
limits that the child and its row state are judged at its admission, in
row F17, after the keys of the limits and before their amounts, at the
signing service and at a verifier alike; an executor judges the kinds that
a request consumes and that neither states in step E2. A root grant has no
step table in this version, and rule 2 reaches it at a request alone. The
refusals record no closure, and the grant stays a well-formed grant. Both
codes were introduced by this registry. Two conditional facts remain:
at a side that runs no profile of the requested action, rule 1 refuses
as `ACTION_UNDEFINED`; at a side that runs no profile of a limit kind,
rule 2 refuses the affected child admission or request as
`LIMIT_KIND_UNDEFINED`. The proposed profiles above change neither
fallback. A side that runs a shared-kind profile judges it under
LIP-0031 in row F17 and row E2; LIP-0038 consumes that same profile,
not a replacement. LIP-0030's independent station kinds keep their
own account/check distinctions. A kind whose amount is a floor
takes the same members as a ceiling (W11.4); how a floor is compared is for
its profile, and until that profile exists rule 2 refuses.

### 12. Vectors of the grant

The reference checker and vectors do **not** yet cover the LIP-0035
contract-free root branch, its split wire/scope refusals, optional mandate,
broker invocation or the new auth/credential objects. Passing them proves
only the existing cases, not conformance to these Draft amendments.


[`vectors/LIP-0020/grant-v4.json`](../vectors/LIP-0020/grant-v4.json)
holds 112 vectors for section 11. Each is the signed form of a grant. In
three of its four groups a vector states the result of the pipeline of
W11.8, `ok` or the first refusal. Those results do not depend on the
proposal points of W11.10: every valid vector meets them, and each vector
of `invalid` and `compound` is refused by a step or a rule that stands
apart from them. The checker holds that statement against the file: it
reads every vector with the proposal points and without them, and the two
results of such a vector must agree.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `valid` | 11 | Reads the grant and recomputes its typed digest, its identifier, its content address and the witness key hash script of its seal key |
| `invalid` | 84 | Reads the grant and reports the stated code. Each holds one defect, and each but `grant-i-05` names a valid neighbour |
| `compound` | 13 | Reads a grant with several defects and reports the one that the order of W9.1, W9.2, W9.3 and W11.8 to W11.10 puts first |
| `undetermined` | 4 | Reads a parent that breaks one proposal point of W11.10 and nothing else. The vector passes steps 1 to 8, and the stated outcome is `ok` or `GRANT_DELEGATE`; a checker refuses any other code |

The valid vectors are a root grant by key and one by name, two parents, a
child of the first parent under the delegation key, one payload under two
signatures, a grant without an action and without a limit, a parent without
a child-seal key, a parent of exactly 65536 octets with 16 groups of 16
ranges, a range of 4096 coins and a range that ends at the output index
4294967295, and a parent of ordinary size with four notaries, 16 groups and
a group of 16 ranges. The vectors of `invalid` and `compound` exercise 19
codes: every code that the pipeline of a grant reports. `grant-i-05` holds
the octets that the vectors of section 10 use as a stand-in for a grant, a
payload with `type` alone under a valid signature: a reader of grants now
refuses them as `WIRE_MEMBER`. `grant-i-01` is the largest parent with one
octet more. Two vectors hold a pool that its rows exceed only beyond 64
bits: in `grant-i-63` each product fits and the sum wraps, and in
`grant-i-80` the product of one group wraps by itself. A reader that checks
only its additions, or only its multiplications, admits one of the two.
Four vectors hold the points on `stop` that every reader judges
(W11.10): a range with a certifier and no `stop` (`grant-i-81`), a range
without a certifier and with `stop` (`grant-i-82`), a run of stop coins
whose last index would be 4294967296 (`grant-i-83`) and two runs of stop
coins that share an output (`grant-i-84`). Each refuses as `GRANT_DELEGATE`
beside the neighbour `grant-v-03`.

**One defect and a valid neighbour.** A vector of `invalid` holds one
defect, and its neighbour is a valid vector that differs from it in that
defect and in nothing else: in one member of the payload, which may be an
object or a list entry; in octets outside the payload; or in the context.
Where the defect is a property of the parent that a child names, the child
names another parent, so its member `parent` and the context change
together. A vector that passes a largest count is its neighbour with one
more entry or one more coin, and no further rule fails behind the count:
the pool of the neighbour holds the added row. One vector names no
neighbour, and the file
lists it under `no_neighbour`: `grant-i-05`, which lacks every member but
`type` and is kept because the earlier vectors use its octets. Unless its
claim says otherwise, the signature of a vector of `invalid` is valid for
its octets; where the octets have no canonical payload, or name no key
under which a signature verifies, the claim says so. The statement of one
defect does not cover the group `compound`: its vectors hold several
defects on purpose and have no neighbour. The checker does not hold a vector
against its neighbour. It checks that the neighbour is a valid vector, and
that the two differ in one defect is the generator's statement, which a
reviewer reads in the generator.

**The group `undetermined`.** Its four vectors are the parent of
`grant-v-03` with one change each: a range script that is no witness key
hash (`grant-u-01`), a stop script that is none (`grant-u-02`), stop coins
that are coins of another range (`grant-u-03`) and stop coins that begin at
the output after the seal (`grant-u-04`). Each breaks one proposal point of
W11.10, which the vector names under `judged`, and nothing else. This
version does not determine whether a reader judges that point, and it does
determine everything else about the vector. Each passes steps 1 to 8 at
every reader. In step 9 a reader that judges the point reports
`GRANT_DELEGATE`, and a reader that does not judge it reads `ok`. The file
states `ok or GRANT_DELEGATE` under `expect`, lists the two under
`outcomes`, and a reader that reports another code, at any step, fails the
vector. Two conforming readers therefore differ on these four vectors in
that one way, and on no other vector. The reader of `tools/grantv4` can
judge the proposal points or leave them out; its checker reads each of the
four both ways and requires `GRANT_DELEGATE` from the first read and `ok`
from the second.

The other points on `stop` are no part of this group. The presence of
`stop`, the last index of a run of stop coins and a stop coin of its own
for each row are judged by every reader, and their vectors stand in
`invalid`.

**Codes without a vector.** Section 11 names four refusal codes that the
pipeline of W11.8 never reports. Each is a check of an admission, and the
file states results of the pipeline alone, so no vector of it can exercise
them; the file lists them under `not_exercised`.

| Code | Why no vector of the file exercises it | Where it is exercised |
| --- | --- | --- |
| `CHILD_ORDINAL` | The pipeline reads an `ordinal` of any value of its form. The ordinal is held against the rows of the parent at admission (LIP-0026 R2.1, R8.8) | `vectors/LIP-0026/rows-vectors.json` and `groups-vectors.json`, on stated facts and not on the octets of a grant |
| `CHILD_SEAL_KEY` | A parent without a child-seal key is read (`grant-v-10`), and so is a child of it. The child refuses at its admission (LIP-0014 CS1, CS2, agreement pending) | In no vector of this repository. LIP-0014 section 11.2 states the cases S4-9 and S4-10 |
| `DELEGATE_KEY_REUSE` | A parent whose delegation key or child-seal key repeats another of its keys is read. Every child of it refuses at its admission (LIP-0014 J4.3 (a), CS3, agreement pending) | In no vector of this repository. LIP-0014 sections 11.1 and 11.2 state the cases S4-2a and S4-10 |
| `SEAL_PROFILE` | The pipeline checks the form of `seal.construction` and of `seal.kind` and not their values. Whether a verifier supports them depends on its configuration (LIP-0008 SB2) | `vectors/LIP-0024/endorsement-vectors.json`, for the profile of a seal-key endorsement and not for the member `seal` of a grant |

A vector for one of the four would be a pair of grants that the pipeline
reads, with one check of an admission after it. An admission reads stated
facts of a chain beside the octets of the grants: the rows and the coins of
the parent as a node shows them, the configuration of the verifier. This
file models no such fact, and a vector of it holds octets and a context of
other vectors alone. That is the whole reason. The order of the checks of
an admission is not the obstacle, since a pair with one failing check has
one outcome in any order, and neither is a pending agreement, since the
signer of a child is in the same state and has vectors here. The four come
with the vectors of an admission. Section 11.11 also names `SUBJECT_MISMATCH`,
`CHILD_ACTIONS_WIDER` and `CHILD_WINDOW_NOT_NESTED`. Before version 0.1.55
no text assigned them to v4. Version 0.1.55 proposes that W11.11 does, and
that it adds `CHILD_CONTRACT_DIFFERS`; W11.14 adds `ACTION_UNDEFINED` and
`LIMIT_KIND_UNDEFINED`, and LIP-0014 section 8.4 adds
`CONTRACT_NOT_PRESENTED`, `CONTRACT_ID` and `CHILD_NOT_LIVE` and gives
`CHILD_SEAL_KEY` and `DELEGATE_KEY_REUSE` their place among the steps of an
admission (rows F9 to F12). The table "Codes of version 0.1.55" of section
11.11 registers the six new codes and the three that are taken from v3.
Each of these is a check of an admission or of a request, the pipeline of
W11.8 reports none of them, and none has a vector here. The file and its
list
`not_exercised` stand as they were made for version 0.1.53: not one octet
of the file changes with version 0.1.55, and the list names the four codes
of the table above and not the later ones. LIP-0014 section 8.7 plans the
vectors of the steps. Version 0.1.61 adds `CONTRACT_SEAL_MISSING` and
`CONTRACT_SEAL_UNAVAILABLE` to the later codes that list does not name:
checks of a signing and of an admission, which the pipeline reports not,
with no vector here and their plan in LIP-0014 section 8.7. The file's
`not_exercised` list is unchanged.

The document step has four vectors on the octets of a grant beside those of
section 10: a signed form that stops before its last octet (`WIRE_JSON`), a
member twice (`WIRE_DUPLICATE`), a height with a fraction (`WIRE_NUMBER`)
and a name with the escape of a control character (`WIRE_STRING`). Five
compound vectors hold two such defects each and fix the order of W9.2 on a
grant.

The file rests on primitives that it does not repeat: the document rules,
the integer forms, the typed digest and the signatures of
[`wire-vectors.json`](../vectors/LIP-0020/wire-vectors.json) (section 10),
and the primitive vectors of the reference laboratory
([change 146](https://github.com/relux-works/swarma-chain-lab/pull/146),
`experiments/grant-v4/vectors`), whose cases for the canonical form, for
integers, for keys and for signatures a reader of grants must pass as well.
One case of that laboratory no longer holds as it is written: its
`memberless-type-0` expects `WIRE_TYPE` for a grant that holds `type`
alone. Which step refuses it now depends on how the case presents the
octets, and the laboratory's file was not read for this section. A payload
of `type` alone inside a signed form, as in `grant-i-05`, passed step 3
only when the grant got its members, and it now refuses as `WIRE_MEMBER`
at step 4 (W3.2): that refusal changes with this section. The bare octets
`{"type":"swarma-grant/4"}`, presented as a signed form, have neither
`payload` nor `signature` and refuse as `WIRE_MEMBER` at step 2 (W5.3);
that refusal is older than this section and does not change with it. No
vector of
`wire-vectors.json` changes: where it reads the stand-in, the place requires
an assent, and the refusal stays `WIRE_TYPE`.

The limits of the file are these. Keys are public test scalars: three are
the secret keys of the BIP-340 test vectors 0, 1 and 2, the others are small
integers, and none belongs to anybody. Every transaction id and the recent
block are the SHA-256 of an ASCII label. Action names and the kinds,
resources, units and periods of limits are placeholders, because no registry
assigns them. No vector reads a chain, so none shows that a name, a coin, a
seal or a block exists, and none admits a grant. The file holds no assent,
no consent and no frame for its grants; sections 7 and 8 have their own
vectors on a stand-in. The rules of LIP-0026 for a child against its row
have no vector here.

[`tools/grantv4/grantv4.py`](../tools/grantv4/grantv4.py) is a reader of
section 11 in Python, with the generator and the checker of the file; it
uses the standard library alone. The file was computed by that one
implementation. Its signer and its typed digest are calibrated on three
values of earlier vector files, the expected refusals were stated by hand in
the generator, and the reader decided each of them again. The generator,
the reader and the checker share one code, so a run of the checker shows
that the file is what this reader gives and nothing more. The checker reads
each vector twice, with the proposal points of W11.10 and without them. For
the group `undetermined` it requires `GRANT_DELEGATE` from the first read
and `ok` from the second and refuses any other code; for every other vector
it requires the stated outcome from both. On the path of `check` the tool
is more than a reader:
before it reads the file it runs the calibration of the generator, which
signs three stated values with public test scalars. It reads a bounded
vector file and decodes no vector above twice the largest size of a grant.

No second implementation has recomputed the file, and the text, the reader
and the vectors come from one author, so an error of understanding that
they share is in the vectors. An independent implementation recomputes,
from the octets and the context of each vector alone and with none of this
code:

- for every valid vector, that the pipeline reads it, and its typed digest,
  its identifier, its content address, the verification of its signature
  under the key of the place, and the witness key hash script of its seal
  key;
- for every vector of `invalid` and `compound`, the first refusal as a
  code;
- for every vector of `undetermined`, that it passes steps 1 to 8 and
  that step 9 gives one of two outcomes: `GRANT_DELEGATE` where the
  implementation judges the proposal point, and `ok` where it does not.
  Another code is a defect of the implementation.

Until such an implementation agrees, the stated values rest on one
computation.

## Alternatives

- **An identifier over the signed form**, as the `grant_id` of v3. One hash
  would then serve as identifier and as content address. Two valid
  signatures of one payload would be two objects, an endorsement or a child
  could not name a grant before it is signed, and a reference would change
  when a signer signed again. Section 6 separates the two hashes. The cost
  is that a reader holds two values for one object and cannot fetch a
  signed object from a content-addressed store by its identifier alone.
- **Two members, `type` and `version`.** LIP-0008 speaks of a type and a
  version, and two members would state them apart. One string cannot
  disagree with itself, is compared whole, and is the tag without any
  further rule. The existing Draft objects already carry such a string,
  under the names `profile` and `schema`; `type` is chosen here because
  "profile" already names the construction profile and the type profiles
  of LIP-0008.
- **Decimal strings for every integer.** One form would be simpler to
  state. Heights and indexes would then be strings, and the event of
  section 7.2 keeps JSON numbers in any case. Two forms with a refusal for
  the wrong one (W2.1) keep both exact.
- **A typed assent for the recipient as well.** It would give both parties
  one form. A browser signer signs Nostr events only, which is why v3 chose
  the event, and a second form for the same act doubles the cases.
- **Consent by the owner key of the recipient's name.** The owner key does
  not change while the grant lives, so no evidence output and no walk would
  be needed. The owner key is the key that LIP-0008 section 3.1 keeps
  offline, and a contract would then need it online.
- **A consent that names the seal.** The seal transaction is fixed before
  the grant is signed (LIP-0008 section 9). A consent that named the
  outpoint of the seal could serve one grant only, and every verifier could
  check that from one issuance, where W7.9 rests on the issuer's record.
  The recipient would have to consent after the seal transaction is fixed.
  The decision does not state this, and the draft does not add it; it is an
  open question.
- **A preparation that binds identifiers only.** The commitment would not
  change when a part is signed again. The anchor would then no longer show
  that the signatures existed when it was mined, which the v3 commitment
  shows by binding both signatures.
- **A new action in place of a payload version.** Action `0x01` already
  means a grant issuance, and its payload begins with a version octet for
  this purpose.
- **An order of refusals by position in the octets.** A reader that makes
  one pass could report the defect that it meets first. W9.2 orders by rule
  instead, so that a reader built on a parser that reports a syntax error
  and nothing else reaches the same code.

The remaining alternatives concern section 11.

- **A row without a certifier as an absent member.** A template would name
  a certifier or name none. An issuer's tool that left the member out by
  mistake would then sign a row that nobody certifies, and nothing in the
  octets would show that it was meant. W11.7 asks for one of two members,
  so that the statement of J9.1 is made in octets. A `null` or an empty
  string in the place of the name would be a second spelling of the same
  statement, and W1.4 has no `null`.
- **One stop coin for a group.** A range would need no second run of
  outputs. One spend would then close every row of the group, where
  LIP-0014 J2.4a and LIP-0027 H1 keep a cause to the row that it concerns.
  W11.6 gives each row its own stop coin and states them by range.
- **A stop coin for each row as a list of outpoints.** It would allow stop
  coins in any transactions. A group of 4096 rows would carry 4096
  outpoints, more than 300 kilobytes, against a largest size of 65536
  octets.
- **A member `depth` in the right of re-delegation**, as profile `/2` has
  it. With two links the member has two values, and the presence of
  `delegate` already says which. A right with `depth` 0 would be a second
  spelling of no right.
- **The grant key from the issuer's name alone**, without
  `issuer.grant_key`. The payload would be smaller by one key. A reader
  could then verify no signature of a grant without a node, no vector could
  hold a grant that verifies by itself, and the consent of the recipient,
  which names the key that signs the grant (W7.3), could not be compared
  with the grant on octets.
- **One member list for a root grant and a child**, with members that are
  empty where they do not apply. An absent member and an empty one would
  then mean the same, which section 1 excludes for `null` for the same
  reason.
- **A list of own partitions for several executors.** LIP-0008 section 4
  allows several executors under signed partitions. A row already is such
  a partition for a child, and a second executor for the recipient itself
  takes a second grant, which a hire has in any case (LIP-0008 section
  2.1). One executor keeps the own account of a grant in one ledger.
- **The script of a seal in the grant**, beside its key. LIP-0008 section
  11.4 shows that the profile and the key fix the script, so a stated
  script could only disagree with them.

## Security consequences

- **What the layer gives.** A signature covers a type together with its
  octets, an amount is read from its digits, and one payload has one
  identifier. A reader that follows section 9 never repairs an object and
  never reports a later defect in place of an earlier one.
- **What it does not give.** Canonical bytes say nothing about meaning.
  Invocation, receipt and seal-endorsement schemas remain incomplete, as
  does the child-kind mapping of notary `/2`. No reader may accept an
  unsupported schema merely because its type or digest is registered.
- **A grant that is read is not a grant that is admitted.** The pipeline
  of section 11 shows a well-formed document under a signature by the key
  that the payload itself names. It reads no chain. Whether that key is the
  grant key of the pinned issuer, whether the seal exists and is unspent,
  whether the window is open and whether a row has its coin are decided at
  admission, on the verifier's own node (section 11.11). A reader that
  treats the result of W11.8 as authority admits a grant that anybody can
  write.
- **The identifier of a parent covers its rows.** A child names its parent
  by the identifier of the payload, and the payload holds every group,
  range and pool. A presenter cannot show a child against a parent with
  other rows.
- **No row is without a certifier by omission** (W11.7). The form still
  admits the statement beside any recipient; only W11.10 refuses a row
  without a certifier that reaches beyond the issuer's own landlord. A
  verifier that reads the members and skips that rule widens J9.
- **Bounds before meaning.** The size, the counts and the forms of section
  11 are checked before any signature, on octets that anybody can send. A
  parent of the largest size holds up to 1,048,576 rows in at most 256
  ranges, and no rule of section 11 expands a range into its coins.
- **Sums that pass 64 bits.** Rule 6 of W11.10 multiplies and adds amounts
  that are each within 2^64 - 1. A reader that computes in 64 bits admits
  a parent whose rows exceed its pool.
- **Identifiers without a registry.** The actions and the kinds of limits
  are texts that no registry assigns yet. Two issuers can write one
  meaning in two spellings, and a verifier must refuse what its profile
  does not define and never guess.
- **Identifiers and state.** An identifier that leaves the signature out is
  stable under re-signing, which is what a reference needs. It is no
  defence against replay. A journal that keys a request by an object
  identifier alone admits the same request again under a new `iat`.
- **The exact signed preparation.** The commitment binds signatures, so a
  presenter must hold the signatures that were anchored. An issuer that
  loses them cannot replace them without a new anchor.
- **Consent of a recipient by name.** With condition 4 of W7.6 a verifier
  refuses a consent by a key that the owner had replaced before the
  snapshot, also where the issuer did not. A former channel key that leaked
  therefore gives no consent to a new contract. What remains with the
  issuer is the age and the single use.
- **Single use is the issuer's.** An issuer that ignores W7.9 can anchor
  two grants under one consent, and each passes a verifier that sees it
  alone. The recipient gains authority that it consented to once; the
  contract, which both grants bind, is the same. The two anchors are public
  evidence against the issuer.
- **Size and depth.** W1.1 bounds what a reader parses before it knows
  anything about the sender. The numbers are proposals.
- **Vectors made by their author.** The vectors and both implementations
  that computed them come from the author of this text. An error of
  understanding that both share is in the vectors.

## Conformance impact

None on normative v0.1 and none on Grant v3: W3.4 keeps every earlier
object under its own rules, and payload version `0x01` of an issuance frame
keeps its meaning. No conformance class is added.

For Grant v4 this LIP supplies the first vectors. They cover the rows of
the conformance outline of LIP-0008 that concern typed domains, canonical
bytes, exact integers, identifiers and strict signatures, as far as those
rows need no object without members.

Section 12 supplies the first vectors that hold a whole v4 grant. They
cover the rows of that outline on the recipient modes and on a name carried
as metadata, as far as octets decide them, and nothing that needs a chain,
an executor or a journal. The reference laboratory's reader, which refuses
every grant as `WIRE_TYPE`, no longer conforms; the change is its own.

## Open questions

- **The owners on the two decided points of section 7.** Ivan Oparin may
  override them, and the co-author's agreement is pending.
- **The owners' acceptance of each proposal**, in particular: the
  identifier without the signature (section 6); one `type` string as the
  tag (sections 3 and 4); the string form for amounts and counters with
  2^64 - 1 as the largest bound of the first profile (section 2); the
  exclusion of `null` and of code points below U+0020 (section 1); the
  depth of 16 and the largest sizes; the registered type names, including the new Draft additions; the
  order of W9.2.
- **The members** of the invocation, the receipt, the seal-key endorsement
  and the child-kind successor attestation, with their vectors, and with
  them the journal key of a request. The contract-notarization schema is
  proposed in LIP-0032, not an implementation claim.
- **The co-author's answer on section 11**, and on the three decisions
  whose members it carries before their agreement: the delegation key (J4),
  the stop coin of a row (J2) and the seal in the grant with the child-seal
  key (LIP-0008 section 11.4, LIP-0014 section 11.2).
- **Whom a carried decision binds.** Every decision that section 11
  carries (J2, J4, CS1 to CS3, J9 to J12, LIP-0008 sections 7.1 and 11.4)
  binds a reader of `swarma-grant/4` from version 0.1.53, under the owner's
  order that Grant v4 does not wait, and the co-author's answer is folded
  in by amendment; a draft's own additions bind no reader until they are
  accepted (the script form of LIP-0026 R3.1 and R8.2, LIP-0027 H1.2 and
  H1.3, LIP-0023 C2.3). This is decided. If the owners later reject it, the
  vectors on the signer of a child become as undetermined as those of the
  proposal points, and section 12 must then say so.
- **The owners' review of the forms that section 11 chose**, which its
  table of sources marks: the member names, `issuer.grant_key` in the
  payload, one executor for the own scope, the two members for a certifier,
  the place of the stop coins of a group, and the two codes.
- **The counts of a parent.** The largest counts of 16 groups, 16 ranges
  and 4096 coins and the size of 65536 octets are decided limits (J12) and
  bounds of the schema, in W11.6 and in LIP-0026 R8.4 alike. Open are
  proposal Q1 of LIP-0026, which would keep the size alone, and the
  smallest count of one group and one range, which is marked NEW.
- **The record of the four numbers.** No statement of J12 in this
  specification names 16, 16, 4096 or 65536: each rests on the owners'
  decision register alone, which this repository does not hold (W11.6).
  Open until the statement of J12 in LIP-0014 and in LIP-0026 section 8
  carries the numbers and cites the record that they come from.
- **Dropping a bound against W3.3.** If proposal Q1 is accepted, octets
  that refuse today, a parent of 17 groups for one, become grants under the
  same type string. W3.3 gives a change of octets a new version. Either the
  change takes `swarma-grant/5`, or W3.3 says that dropping a bound of a
  schema is no change of octets. Neither is said yet.
- **The proposal points of W11.10**: the witness key hash form of `script`
  and of `stop.script` (LIP-0026 R3.1 and R8.2; LIP-0027 H1.2), and the
  placement points of rule 8 (LIP-0027 H1.3; LIP-0023 C2.3). Until the
  owners accept them, no version determines that a reader judges them. The
  code is fixed: a reader that judges one reports `GRANT_DELEGATE` in step
  9, and their four vectors state `ok` or `GRANT_DELEGATE` (section 12).
  The owners' line comes down to two acceptances, the script form and the
  placement rules.
- **The owner's line on the rules of W11.10 that every reader judges.**
  Each is given by a decision or by a form of section 11; that a reader of
  a document refuses on them is said in W11.10 and marked NEW in section
  11.12. The review of record of these members recommends "yes". What a
  verifier reads of a parent at admission is proposal Q1.
- **Vectors of an admission** for `CHILD_ORDINAL`, `CHILD_SEAL_KEY`,
  `DELEGATE_KEY_REUSE` and `SEAL_PROFILE` on the octets of grants. The last
  three have no vector on a v4 grant anywhere (section 12). The same holds
  for the codes of W11.11 and W11.14 and for `CONTRACT_NOT_PRESENTED`,
  `CONTRACT_ID`, `CONTRACT_SEAL_MISSING` and `CHILD_NOT_LIVE`; LIP-0014
  section 8.7 plans vectors for them, on stated facts for the contract
  seal, plans none for a result that this version cannot compute, and
  generates none.
- **The registries of action names and of limit kinds**, with the meaning
  of a period (LIP-0007, LIP-0018; LIP-0008 sections 2 and 12.3). Section
  11.14, a proposal of version 0.1.55, states them, and both are without a
  defined entry: the texts of a grant are identifiers without a list, an
  executor refuses a request for an action or a kind that no profile
  defines, and a child that states a limit refuses at its admission. Open
  are the entries, the grammar of an identifier and who assigns one outside
  `swarma/`.
- **A child that is wider than its parent allows.** W11.11, a proposal of
  version 0.1.55, names the codes for a child whose contract, chain,
  actions or window do not lie inside those of its parent. Open are the
  owners' acceptance and the co-author's answer, and above all the owners'
  decision on rule 1: that a child binds the contract identifier of its
  parent is a new restriction that the agreed point on text does not
  entail, and with it whether a later profile lets a child bind a narrower
  contract of its own.
- **The codes that follow the contract identifier.** The code of a contract
  that is no valid contract of its v4 profile and the code of a contract
  that does not mirror the terms of its grant, with the preimage of the
  identifier (LIP-0017 section 2), without which `CONTRACT_ID` cannot be
  computed. They come with a v4 contract profile (LIP-0014 section 8.4,
  open point O4). Since version 0.1.61 one code stands between the
  identifier and those two: `CONTRACT_SEAL_MISSING`, for decision C12 of
  LIP-0017, whose refusal Ivan Oparin decided on 2026-11-17 and whose
  name, step and node read are proposals of that version; the
  co-author agrees and leaves the judgement to Ivan (LIP-0017,
  "Decisions recorded"). No step or code is stated for a contract
  seal that is confirmed as named and spent, and no step table fixes the
  place of the contract-seal check at the admission of a root grant.
  Open with the members of the invocation: the code of a request that is
  not authenticated and the codes of the checks of an invocation (O2, O3).
- **The reading of a payload before it is signed.** LIP-0014 section 8.4,
  rule T7, proposes five steps for the signing service of the delegation
  key. W9.1 has no class for it and gains one by amendment if the rule is
  accepted.
- **A scope text and typed constraints on v4.** The octets that carry a
  text along a path (LIP-0014 section 3.4) and the machine members for a
  ref, a revision, a payee or a list of targets have no source and no
  member in section 11. Each is a new member, and so an amendment of this
  section or a new version of the type.
- **The target of a grant.** LIP-0008 section 1 lists a target beside the
  executor bindings. Section 11 reads it as the executor that the grant
  names and gives it no member of its own. Whether a grant needs a subject,
  as an invocation has (LIP-0008 section 12.1), comes with the invocation.
- **The seal of a single-use grant.** `seal` holds one key. A seal with
  two branches needs two (LIP-0008 section 11.1), and its profile is open.
- **A second implementation for the vectors of section 12**, and the
  reader of the reference laboratory.
- **The snapshot and the recent block.** The draft reads the issuance
  snapshot of the decision as the state at the grant's recent block, and it
  has the issuer commit the tip of its observation as that block (W7.6).
  LIP-0008 section 7 leaves the recency of that block to a profile.
- **Single use at a verifier.** Whether the consent names the seal, so that
  one issuance shows that the consent serves no other grant (see
  Alternatives).
- **The name in a consent.** The tag `name` carries printable ASCII. Which
  names the first name profile admits, and their spelling, are open with
  it.
- **The assent to a child's contract.** Which key signs for the delegating
  party, when the delegation key signs child grants and nothing else
  (section 7.1).
- **Other channels.** The consent event belongs to the Nostr channel. A
  channel with another signature scheme needs its own form of consent.
- **Contracts with more than two parties.** The preparation binds two
  consents. The anchor of LIP-0017 is the place for more, and its
  commitment is open there.
- **The chain.** The objects of this LIP name the chain by its genesis hash
  alone. The pin of the construction profile (LIP-0008 section 1.1) is
  open, and so is whether a `network` label joins it.
- **The presentation.** What a presenter hands to a verifier; how a reader
  that starts from the frame obtains the assent, the consent event and the
  evidence outpoint beside the grant; and how a reader fetches a parent
  that a child names by its identifier (section 6). LIP-0019 leaves the
  presentation of a v4 grant open.
- **A list for object types in LIP-0018**, beside its four lists, and who
  assigns an identifier.
- **A published checker and a second implementation** for the vectors.
