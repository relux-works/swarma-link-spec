# LIP-0020: Wire registry for Grant v4

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** the bytes that every signed object of Grant v4 shares: the
  canonical form, integers, types, signing digests, identifiers, the consent
  of both parties and the issuance commitment
- **Builds on:** LIP-0008 sections 3.1, 7.1, 8, 8.1 and 9, and LIP-0005;
  relates to LIP-0004, LIP-0013, LIP-0014, LIP-0017, LIP-0018 and LIP-0019

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
- vectors for all of it (section 10).

Three objects are complete here: the assent of a party to a contract, the
consent event of a recipient and the issuance preparation. The registry
reserves an identifier and a digest for five more types and gives them no
member: the grant, the invocation, the receipt, the seal-key endorsement and
a successor of the notary attestation. No reader accepts a payload of those
five until the proposal that fixes its meaning gives it members.

## What is decided and what is proposed

Two points of section 7 are decided. They were decided on 2026-11-14 under
Ivan Oparin's delegation; he may override the decision, and the co-author's
agreement is pending. The first requires authorisation by name at issuance:
the state of a name at the issuance snapshot decides, and a state that held
earlier or later is no substitute. The second makes a consent bound and
single-use, with a largest age of 72 hours at issuance. Section 7 states
both and says what the draft adds to carry them.

Every other rule of this LIP is the draft's proposal. Neither owner has
decided a byte of it, and nothing of it is implemented. The owners accept or
change these bytes through this LIP, under LIP-0001.

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
| "Exact versioned bytes, signature domain, commitment/consent encoding" | Sections 1, 3, 4, 7 and 8, for the layer that all objects share. The members of five types stay open |
| "typed-hash registry" and "per-field JCS integer/string schemas" | Sections 2, 3 and 4. The form of each integer member is fixed with its type, so for the five open types it is open with them |
| "Signed metadata envelope, canonical object-ID preimages/signature inclusion, strict signature wire representation" | Sections 3 (W3.7), 5 and 6 |
| "cross-version journal bindings" | Section 6 states what an identifier alone may not do. The journal key of a request comes with the members of the invocation |
| "how the consent event's NIP-01 `created_at`, which stays in seconds, relates to the window" | Section 7.4 |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The reader of canonical bytes, the two integer forms, the typed digest, signatures, the signed form and identifiers (sections 1 to 6) | Yes | The owners' acceptance |
| The assent, the consent event, the issuance preparation and its frame (sections 7 and 8), as octets and as checks on stated inputs | Yes | The contract identifier is taken as 32 given octets: its preimage is open in LIP-0017 section 2. The reads on a node need the ownership profile of LIP-0008 section 3, which is open |
| A parser of a grant, an invocation, a receipt, an endorsement or the successor attestation | No | The members of each, as the next table says |

| Type | Its members wait for |
| --- | --- |
| `swarma-grant/4` | The encoding of the issuer pin and of an owner key (LIP-0008 section 3), of the recipient modes (section 3.1), of the executor (section 4), of the limits and their kinds (section 2 and LIP-0018), of the window and the recent block (sections 7 and 7.1) and of the seal with its construction profile (sections 1.1, 9 and 11); for a parent and a child, the rows, the delegation key and the issue capability (LIP-0014 sections 9.1 and 11.1, LIP-0008 section 12.2), whose rules await the co-author |
| `swarma-invocation/1` | The action table and the types of its arguments (LIP-0007, LIP-0008 sections 12.1 and 12.3), the encoding of the proof path (section 12.2) and the journal key of a request |
| `swarma-receipt/1` | What a receipt states about an effect, for each action (LIP-0018 section 3) |
| `swarma-seal-endorsement/1` | The seal profile and the form of a seal key and of its script (LIP-0008 sections 11.1 and 11.2) |
| `swarma-notary-attestation/2` | The Draft changes of LIP-0014 sections 3.4, 7.1, 9.1 and 10.1 (J5, J3, J1, J2), which await the co-author |

Until a type has members, no reader supports it, and a payload of that
type refuses as `WIRE_TYPE` (W3.1). Nothing in this LIP, and no vector,
makes a payload that holds only `type` a valid object.

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
  Grant v4. The reference laboratory holds no v4 code.

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
change of form. The three objects that are complete here hold one integer
member, an output index, in the number form, and no rule of this LIP
computes with an integer.

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
x-only key.

The registry:

| Type | Object | Use of its digest | Signed by | Members |
| --- | --- | --- | --- | --- |
| `swarma-grant/4` | A v4 grant, root or child (LIP-0008 section 1) | Signature | For a root grant the issuer's grant key. For a child the rule in force names the parent's recipient key, and Draft text of LIP-0014 section 11.1 names the delegation key of the parent (J4, awaiting the co-author's agreement) | None yet |
| `swarma-invocation/1` | A signed invocation (LIP-0008 section 12.1) | Signature | The request key of the final grant, or the key that its recipient's name yields for the channel | None yet |
| `swarma-receipt/1` | The receipt of an executor for an effect | Signature | The executor's key | None yet |
| `swarma-seal-endorsement/1` | The endorsement of a seal key (LIP-0008 section 11.2) | Signature | The issuer's grant key | Named by meaning in LIP-0008 section 11.2; none here |
| `swarma-contract-assent/1` | The assent of one party to a contract | Signature | The key of that party | Section 7.1, complete |
| `swarma-issuance/1` | The issuance preparation | Commitment | Nobody; the anchor transaction authenticates it | Section 8, complete |
| `swarma-notary-attestation/2` | The successor of the attestation of LIP-0014 section 6.1 | Signature | The notary's attestation key | None yet |

The largest size is 1024 octets for the signed form of an assent and 2048
octets for an issuance preparation. A type without members states its
largest size with them.

Draft [LIP-0024](LIP-0024-seal-endorsement.md) proposes the members of
`swarma-seal-endorsement/1`, with its largest size, its codes and its
vectors. The entry above stands until both owners accept them.

The entries of the grant and of the endorsement name the root case. Who
signs a child's grant, who endorses the seal of a child and who assents to a
child's contract are questions of LIP-0014 sections 9.1 and 11.1, and the
registry settles none of them.

One object of this profile is a Nostr event and no entry of the registry:
the consent event of section 7.2. It keeps the wire form and the identifier
of NIP-01, and sections 1 to 6 do not apply to it.

The attestation needs a successor for two reasons. Its identifier and its
signature follow the fixed-prefix style, which sections 4 to 6 replace for
the objects of this profile, and new octets take a new version (W3.3). And
Draft text of LIP-0014 changes its members: section 9.1 removes the members
`budget` and `prev_attestation_id` (J1), and section 3.4 leaves `none` and
`identical` as the values of `textual` (J5). Those decisions await the
co-author's agreement. This LIP gives the successor its identifier and its
digest and no member; its members, and the commitment of its anchor
(LIP-0014 section 6.4), come with the proposal that settles those changes.
`swarma-notary-attestation/1` keeps its octets and its prefix under W3.4.

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
| Authorisation by name at issuance | It is required. At the issuance snapshot, the consistent state of its own node that the issuer signs against, the issuer's name is live, is held by the pinned owner under the first ownership profile (for the Witness profile on Namecoin: a closed list of single-key scripts, read on a node with a transaction index), and its value names the grant key that signs. The same holds for a recipient that the grant names by name: the current value of its name at that snapshot names the channel key that signed the consent. A state that held earlier or later is no substitute. |
| Age and reuse of a consent | A consent is bound and is used once. It names the exact contract, the issuer and the recipient. Exactly one issuance consumes it. It is never presented again for another grant, for a re-issue or for a successor; each of those needs a fresh consent, and the issuer records the identifier of the consent as consumed. At most 72 hours pass between the `created_at` of the consent event and the issuer's first transaction of the issuance, measured on the issuer's clock, and an older consent refuses. `created_at` is never compared with a block height. The 72 hours cover an issuance of two transactions with a person's confirmation between them. They are a policy number, not a measured tolerance, and a later profile may change them. |

The rest of the section is the draft's proposal for carrying the two points
in octets and in checks. It adds four things that the decision does not
state: the tags `issuer` and `name` of the consent event (W7.3); the recent
block of the grant as the block of the snapshot, with the evidence output
and the verifier's read of it (W7.6); which transaction counts as the
first of an issuance (W7.8); and what a verifier can and cannot see of the
single use (W7.9).

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
a root grant is the issuer's grant key, as in the v3 profiles (LIP-0017
section 1). For a child grant the point is open: Draft text of LIP-0014
section 11.1 lets the delegation key sign child grants and nothing else, so
that key cannot sign an assent.

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

W8.1. The issuance preparation is a payload of type `swarma-issuance/1`.
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

W8.2. The preparation is rebuilt from four inputs: the signed grant, the
signed form of the issuer's assent, the consent event and, for a recipient
by name, the evidence outpoint. The first three are objects that a reader
checks through their own pipelines. The fourth is two values that nothing
signs. The issuer records them when it reads the name (W7.6) and hands them
on with the grant, and a presenter supplies them with the presentation. The
anchor binds them, because a preparation with another outpoint has another
commitment. Nobody signs the preparation, and nobody needs to transport it:
whoever holds the four inputs builds the same octets. From the signed grant
come its identifier and its signature; its chain, its contract hash and the
mode of its recipient are members of the grant, which has none yet.

W8.3. The preparation states the signature of each signed part beside what
identifies the part, and each of those signatures is the signature of the
part that the reader checked. The anchor therefore fixes the exact signed
preparation. A part that is presented under another valid signature is the
same object (W5.4) and is still not what was published: the recomputed
commitment differs.

W8.4. A preparation for a recipient by name carries `name_output`. A
preparation for a recipient by key carries none. The mode is the grant's.
A presentation that offers an evidence outpoint for a grant by key, or none
for a grant by name, refuses as `ISSUANCE_MODE`. A verifier makes this
check on the inputs before it reads the consent event (W9.4).

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
a v4 grant accepts version `0x02` alone, with this action, this location
type and this pointer, and it never reads a frame of one version as the
other. Any other frame refuses as `ISSUANCE_FRAME`. The rule of LIP-0005
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
| Signed object | An assent, and every signed type of the registry once it has members | 1. The document: W1.1 to W1.6 on the signed form, in the order of W9.2. 2. The signed form: exactly `payload` and `signature` (W5.3). 3. The `type` (W3.1, W3.3, W3.4). 4. The members of the payload, in the order of W9.3. 5. The encoding of the signature (W5.2). 6. The key of the place (W5.5). 7. The signature (W5.1, W5.2). 8. References to the object and from it (W6.3). 9. The rules of the object: for an assent, W7.2 |
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
members are points of the curve (`WIRE_KEY`).

W9.4. An issuance is checked in six steps, and the first that fails gives
the refusal.

| Step | Check | Refusal |
| --- | --- | --- |
| 1 | The signed grant, through the pipeline of a signed object | The codes of that pipeline. The step has no content until the grant has members |
| 2 | The inputs: the mode of the grant and the presence of the evidence outpoint (W8.4) | `ISSUANCE_MODE` |
| 3 | The issuer's assent, through the pipeline of a signed object, and then W7.2 | The codes of that pipeline, `ASSENT_BINDING`, `ASSENT_PARTY` |
| 4 | The consent event, through the five steps of W7.4, with the evidence outpoint for a grant by name | `CONSENT_SHAPE`, `CONSENT_BINDING`, `CONSENT_KEY`, `CONSENT_EVIDENCE`, `CONSENT_SIGNATURE`, `CONSENT_TIME` |
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
| `WIRE_MEMBER` | A member that the schema does not list, a missing member, or a value in another form |
| `WIRE_INTEGER` | A string-form integer outside its grammar, or an integer above the bound of its member |
| `WIRE_KEY` | A signing key that is no point of the curve |
| `WIRE_SIGNATURE_FORM` | A signature that is not 128 lowercase hexadecimal characters |
| `WIRE_SIGNATURE` | A signature that does not verify |
| `WIRE_ID` | A reference that differs from the recomputed identifier |
| `ASSENT_BINDING`, `ASSENT_PARTY` | An assent for another chain or contract; an assent by another key than the issuing party's (W7.2) |
| `CONSENT_SHAPE`, `CONSENT_BINDING`, `CONSENT_KEY`, `CONSENT_EVIDENCE`, `CONSENT_SIGNATURE`, `CONSENT_TIME` | The five steps of W7.4, with two codes for its third step |
| `CONSENT_AGE`, `CONSENT_CONSUMED` | At the issuer alone: a consent older than 72 hours (W7.8); a consent that was used (W7.9) |
| `ISSUANCE_MODE`, `ISSUANCE_FRAME`, `ISSUANCE_COMMITMENT` | W8.4, W8.5 and W8.6 |

A refusal of this section records no closure. Every code is new, and none
replaces a code of an earlier format.

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
| Primitive | `primitives`: 11 | Arithmetic on given octets under a given type string: the tag and the typed digest for each of the seven types, a signature over a digest, the two SHA-256 values. No schema is consulted, and the octets are no valid object |
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
used as three given values and never as a grant: a reader of grants refuses
those octets as `WIRE_TYPE` today, and as `WIRE_MEMBER` once a grant has
members. Vectors of whole grants, invocations and receipts come with their
members.

No checker for these vectors is in this repository. The values were
computed by one implementation and recomputed, with the expected refusals,
by a second one that shares no code with the first; neither is published
here. LIP-0008 asks for a deterministic runner and for a second
implementation in Swift that consumes the same vectors on its own, and it
says that the agreement of two implementations is not the oracle. That
holds for these vectors: they bind nothing until both owners accept the
rules that they follow.

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

## Security consequences

- **What the layer gives.** A signature covers a type together with its
  octets, an amount is read from its digits, and one payload has one
  identifier. A reader that follows section 9 never repairs an object and
  never reports a later defect in place of an earlier one.
- **What it does not give.** Canonical bytes say nothing about meaning.
  Five of the seven types have no members, and until they have, no reader
  can accept one of them.
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

## Open questions

- **The owners on the two decided points of section 7.** Ivan Oparin may
  override them, and the co-author's agreement is pending.
- **The owners' acceptance of each proposal**, in particular: the
  identifier without the signature (section 6); one `type` string as the
  tag (sections 3 and 4); the string form for amounts and counters with
  2^64 - 1 as the largest bound of the first profile (section 2); the
  exclusion of `null` and of code points below U+0020 (section 1); the
  depth of 16 and the largest sizes; the names of the seven types; the
  order of W9.2.
- **The members** of the grant, the invocation, the receipt, the seal-key
  endorsement and the successor attestation, with their vectors, and with
  them the journal key of a request.
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
