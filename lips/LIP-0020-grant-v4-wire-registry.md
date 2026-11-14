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
- the refusal codes of this layer and their order (section 9);
- vectors for all of it (section 10).

It does not fix the members of a grant, of an invocation, of a receipt, of
a seal-key endorsement or of a notary attestation. Each of those comes with
the proposal that fixes its meaning; the registry gives each its identifier
and its digest now, so that those proposals share one layer.

## What is decided and what is proposed

Every rule of this LIP is the draft's proposal. Neither owner has decided a
byte of it, and nothing of it is implemented. The owners accept or change
these bytes through this LIP, under LIP-0001.

The requirements that the proposal meets are Draft text of LIP-0008: a type
and a version inside the signed bytes, one tagged digest for each type, one
identifier for each object, strict BIP-340 verification, and RFC 8785 as the
plan for the canonical form (sections 8 and 8.1). Two amendments of
LIP-0008 bound section 7 of this LIP. They follow Ivan Oparin's decisions
of 2026-11-10, and the co-author's agreement on them is pending: a grant
names its recipient in exactly one way, by key or by name (LIP-0008 section
3.1), and the window of a grant is a pair of block heights (LIP-0008
section 7.1). An invocation keeps clock time, by his decision of
2026-11-11.

The table says which open point of LIP-0008 each section answers.

| Open point of LIP-0008 | Proposed here |
| --- | --- |
| "Exact versioned bytes, signature domain, commitment/consent encoding" | Sections 1, 3, 4, 7 and 8, for the layer that all objects share. The members of each object stay open |
| "typed-hash registry" and "per-field JCS integer/string schemas" | Sections 2, 3 and 4 |
| "Signed metadata envelope, canonical object-ID preimages/signature inclusion, strict signature wire representation" | Sections 3 (W3.7), 5 and 6 |
| "cross-version journal bindings" | Section 6 states what an identifier may not be used for. The journal key of a request comes with the members of the invocation |
| "how the consent event's NIP-01 `created_at`, which stays in seconds, relates to the window" | Section 7.4 |

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
  LIP-0014 section 6.1 says
  of its attestation that the typed-hash plan of LIP-0008 may replace the
  prefix before adoption.
- LIP-0008 section 8 plans RFC 8785 and tagged hashes for the next format
  and section 8.1 states the requirements on identifiers and signatures.
  Both leave the bytes open.
- `tools/trustcheck` recomputes the vectors of LIP-0013 and nothing of
  Grant v4. The reference laboratory holds no v4 code.

## Proposal

### 1. Canonical bytes

The canonical bytes of an object are the RFC 8785 serialization (JSON
Canonicalization Scheme) of one JSON object, over a set of values that is
smaller than JSON's. A reader takes the octets through these steps in this
order and refuses at the first that fails.

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
| Number form | A JSON number: `0`, or a digit from 1 to 9 followed by digits | 0 to 9007199254740991, which is 2^53 - 1 | Values that what they count keeps far below 2^53: a block height, an output index, a position in a list, Unix seconds |
| String form | A JSON string that holds the same grammar | 0 to the bound that the member states | An amount in atomic units, a price, a cost, a count of tokens or of octets, and every cumulative counter |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| W2.1 | Every integer member has exactly one form, stated by the schema of its type. The other form refuses: the number `1` where the string `"1"` is required, and the reverse. No reader converts one into the other. | `WIRE_MEMBER` |
| W2.2 | The number form. The token has no sign, no fraction and no exponent, and its value is at most 9007199254740991. The reader decides this on the digits of the token. | `WIRE_NUMBER` |
| W2.3 | The string form. The string is `0`, or a digit from 1 to 9 followed by digits `0` to `9`, and nothing else: no sign, no leading zero, no fraction, no exponent, no space, no separator, no digit outside ASCII. Its value is at most the bound of the member. | `WIRE_INTEGER` |
| W2.4 | A reader parses an integer from its digits into an exact integer and checks the bound before it computes with the value. No binary64 number takes part, at a reader or at a signer. An addition or a multiplication whose result would pass the bound of its member refuses and does not wrap. | The code of the rule that computes |

No member of the first profile has a bound above 18446744073709551615,
which is 2^64 - 1, so a reader can hold every integer of the profile in 64
unsigned bits. A type that needs more states its own bound.

Which members take the string form is decided with each type. The rule of
thumb in the table is the draft's: whatever can be summed without a natural
ceiling takes the string form, so that no later asset or price forces a
change of form.

### 3. Types and the registry

| Rule | Requirement | Refusal |
| --- | --- | --- |
| W3.1 | Every payload has a member `type`, a string: the name of the object type and its version, joined by a slash, exactly as the registry below writes it. A reader compares the whole string and never parses a version out of it. A payload without `type`, with a `type` that is no string, with a `type` that the reader does not support, or with another type than the one that its place requires refuses. | `WIRE_TYPE` |
| W3.2 | The members of a payload are those that the schema of its type lists, each in the form that the schema states. A member that the schema does not list, a required member that is missing and a value in another form refuse. | `WIRE_MEMBER` |
| W3.3 | A change of octets or of meaning takes a new version, as LIP-0018 requires of a profile. A reader that supports one version reads no other version as that one, and no reader falls back from a type that it does not support to one that it does. | `WIRE_TYPE` |
| W3.4 | The registry applies to no object of an earlier format. A v3 grant, the contracts `swarma-trust-contract/1` and `/2`, the attestation `swarma-notary-attestation/1` and the statements of LIP-0015 and LIP-0016 keep their own bytes, prefixes and identifiers. Under this registry such an object has no `type` and refuses. | `WIRE_TYPE` |
| W3.5 | A member that holds a hash, an identifier, a transaction id or a signature is lowercase hexadecimal of the exact length that the schema states. A transaction id and a block hash are written in the byte order in which a node prints them. The `signature` of a signed form has its own rule and code (W5.2). | `WIRE_MEMBER` |
| W3.6 | A public key is an x-only key of BIP-340: 64 lowercase hexadecimal characters that are the x coordinate of a point of the curve. | `WIRE_MEMBER` for the form; `WIRE_KEY` for a value that is no such coordinate |
| W3.7 | Descriptive members, where the schema of a type admits them, are members of the payload like any other. They are inside the canonical bytes, the digest and the identifier, and a change of one is a change of the object. A signed form carries nothing beside the payload and the signature. Such a member gives no authority (LIP-0008 section 12.3). | `WIRE_SIGNATURE` for a member that was changed after signing |

The registry:

| Type | Object | Use of its digest | Signed by | Members |
| --- | --- | --- | --- | --- |
| `swarma-grant/4` | A v4 grant, root or child (LIP-0008 section 1) | Signature | For a root grant the issuer's grant key. For a child the rule in force names the parent's recipient key, and Draft text of LIP-0014 section 11.1 names the delegation key of the parent (J4, awaiting the co-author's agreement) | Open |
| `swarma-invocation/1` | A signed invocation (LIP-0008 section 12.1) | Signature | The request key of the final grant, or the key that its recipient's name yields for the channel | Open |
| `swarma-receipt/1` | The receipt of an executor for an effect | Signature | The executor's key | Open |
| `swarma-seal-endorsement/1` | The endorsement of a seal key (LIP-0008 section 11.2) | Signature | The issuer's grant key | Named by meaning in LIP-0008 section 11.2; octets open |
| `swarma-contract-assent/1` | The assent of one party to a contract | Signature | The key of that party | Section 7.1, complete |
| `swarma-issuance/1` | The issuance preparation | Commitment | Nobody; the anchor transaction authenticates it | Section 8, complete |
| `swarma-notary-attestation/2` | The successor of the attestation of LIP-0014 section 6.1 | Signature | The notary's attestation key | Open |

The largest size is 1024 octets for the signed form of an assent and 2048
octets for an issuance preparation. A type whose members are open states
its largest size with them.

One object of this profile is a Nostr event and no entry of the registry:
the consent event of section 7.2. It keeps the wire form and the identifier
of NIP-01, and section 1 does not apply to it.

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

For the payload `{"type":"swarma-grant/4"}`, which stands in for a grant in
the vectors, the SHA-256 of the tag is
`eb2b9dc1647237e0e0d7e024a19f4ee95379c20ff01f4ccb7cf1168840fef67a` and the
typed digest is
`f1e62e34f6b79cd5c28a4b1edbb50b737bb3f4d2bd26805764b64eb5e7372f75`.

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

An identifier names octets. It is no key of state. LIP-0008 section 8.1
requires that re-signing, and another object identifier, restore neither a
seal nor a nonce claim nor a consumed budget. Under W6.2 re-signing changes
no identifier. A payload that was changed and signed again has another
identifier, and it must reach the same state as the first: a closure is
keyed by the seal's outpoint, and a request by a key that the profile of the
invocation builds from the members that a new signature or a new `iat`
does not change, the executor and the nonce among them. That key comes
with the members of the invocation and is not fixed here.

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

#### 7.1. The assent of a party

W7.1. An assent is a payload of type `swarma-contract-assent/1` with
exactly these members:

| Member | Form | Meaning |
| --- | --- | --- |
| `type` | string | `swarma-contract-assent/1` |
| `genesis` | 64 hexadecimal characters | The hash of the genesis block of the chain that holds the names of the parties |
| `contract` | 64 hexadecimal characters | The identifier of the contract |
| `party` | public key (W3.6) | The key that assents. The signature of the signed form verifies under it |

W7.2. A verifier of a grant takes the issuer's assent through the steps of
section 9 and then checks, in this order:

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
octets, with exactly these three tags in this order:

| # | Tag | Value |
| --- | --- | --- |
| 1 | `t` | `swarma-contract-consent/1` |
| 2 | `genesis` | the hash of the genesis block, as in the assent |
| 3 | `contract` | the identifier of the contract |

Kind 8181 is the kind of the v3 consent. The two cannot be confused: a v3
verifier requires the v3 value of `t` and four tags, and a v4 verifier
requires this value and these three. What a v3 consent carried in its tags
`booking` and `privacy` is part of the contract on v4, which the identifier
binds.

W7.4. A verifier checks a consent event in this order:

| Check | Refusal |
| --- | --- |
| The wire form, the kind, the empty content and the three tags are as W7.3 states, and `id` is the NIP-01 id of the event | `CONSENT_SHAPE` |
| The tags `genesis` and `contract` equal the chain and the contract hash of the grant | `CONSENT_BINDING` |
| `pubkey` is the consenting key of section 7.3 | `CONSENT_KEY`; `CONSENT_EVIDENCE` where the read of W7.6 establishes nothing |
| `sig` verifies over `id` under `pubkey`, under W5.2 | `CONSENT_SIGNATURE` |
| `created_at` is not later than the verifier's clock (section 7.4) | `CONSENT_TIME` |

#### 7.3. Which key consents

| | Recipient by key | Recipient by name |
| --- | --- | --- |
| Consenting key | The request key that the grant signs | The key that the recipient's name yielded for the Nostr channel when the grant was issued |
| What the issuer checks before it signs the grant | `pubkey` equals the request key | The three conditions of W7.6, in one observation |
| What a verifier compares `pubkey` with | The request key of the grant | The key that the evidence output yields |
| What authenticates a request afterwards | The same request key | The key that the name yields at that admission |

W7.5. For a recipient by key, the `pubkey` of the consent event equals the
request key that the grant signs.

W7.6. For a recipient by name, the issuer reads the recipient's name in
the same consistent observation from which it takes the recent block that
the grant commits (LIP-0008 section 7). In that observation:

1. the current output of the name is controlled by the owner key that the
   grant signs;
2. the value of that output yields a key for the Nostr channel, by the
   member that LIP-0008 section 3.1 names;
3. the `pubkey` of the consent event equals that key.

The issuer signs nothing unless all three hold. It records that output, by
transaction id and output index, as the evidence output of the issuance
preparation (section 8), and it keeps the consent event and the
transaction of the evidence output with its record of the grant.

A verifier reads the evidence output on its own node. The transaction is
confirmed on the active chain at a height that is not above the height of
the grant's recent block. The output is an operation of the signed name. It
is controlled by the signed owner key, under the ownership-proof profile of
LIP-0008 section 3, which is open. Where the read cannot establish these,
the consent refuses as `CONSENT_EVIDENCE` and no closure is recorded. Where
the value of the output yields another key than the event's `pubkey`, or
no key, the consent refuses as `CONSENT_KEY`.

The evidence output is no pin of the recipient. Admission of a request
never compares the name's current output with it, and LIP-0008 section 3.1
stays as it is: a grant by name carries no request key and no pin of a name
output.

W7.7. A later update of the name by the same owner, which lists another
channel key, leaves the consent as it is. The evidence output stays
confirmed, and it still yields the key that consented. Requests are
authenticated under the key that the name yields at admission, never under
the key that consented. A change of the name's owner refuses the grant
itself (LIP-0008 section 3), and the consent plays no part in that.

The verifier's read has a limit. It shows that the consenting key was a
channel key of the name under the signed owner, in an output that existed
when the grant was built. It does not show that this output was still the
name's current output at the recent block: an issuer that names an earlier
output, whose key the owner had replaced by then, passes. The issuer's own
check under W7.6 excludes that case, and an auditor can refute it from the
name's history. What a false statement would gain is small: the key was a
key of the same owner, and it authenticates no request. Whether a verifier
must prove the point at admission is an open question.

#### 7.4. Time

W7.8. The `created_at` of a consent event is a claim in Unix seconds. No
rule compares it with a block height, and it is no input of the grant's
window (LIP-0008 section 7.1). One rule of v3 carries over unchanged
because it needs no height: a consent whose `created_at` is later than the
checker's clock refuses, at the issuer and at a verifier. The other half
of the v3 rule compared `created_at` with the end of the grant in seconds,
and a v4 grant has no end in seconds; it has no successor here.

How old a consent may be when the issuer signs, and whether a verifier
bounds that age, is open.

#### 7.5. Cases that need a node

The vectors of section 10 cover every check that needs no chain. These
cases need one, and no implementation exists that could run them.

| Valid control | Refusal or invariant |
| --- | --- |
| A recipient by name; the evidence output is the name's current output at the recent block, under the signed owner key, and yields the consent key | The same grant where the evidence transaction is unconfirmed, is confirmed above the height of the recent block, or is no operation of the signed name: `CONSENT_EVIDENCE`, and the journal holds no closure |
| The same | The evidence output is controlled by another key than the signed owner key: `CONSENT_EVIDENCE` |
| The same | The value of the evidence output yields another key than the event's `pubkey`, or lists the key only in another entry of `nostr.names`: `CONSENT_KEY` |
| After issuance the owner updates the name to another channel key; the grant is presented again | The consent still passes, and a request signed by the former channel key refuses under LIP-0008 section 3.1. Refusing the consent because the name lists another key today is wrong |
| At the issuer: the name lists the consent key in the observation that supplies the recent block | The name was updated to another key before that observation and the consent is by the former key: the issuer signs nothing |
| A node that cannot read the evidence transaction | The admission refuses, and nothing is recorded as closed |

### 8. The issuance preparation and its anchor

LIP-0008 section 9 has the issuer fix the seal transaction, the parties
sign, and an anchor carry the commitment to "that signed preparation". This
section fixes what the preparation is and what the anchor carries. How the
anchor transaction is built, which inputs it spends and when it counts as
confirmed stays with LIP-0008 sections 1.1 and 9, where it is open.

W8.1. The issuance preparation is a payload of type `swarma-issuance/1`
with exactly these members:

| Member | Form | Meaning |
| --- | --- | --- |
| `type` | string | `swarma-issuance/1` |
| `genesis` | 64 hexadecimal characters | The chain of the grant |
| `contract` | 64 hexadecimal characters | The contract hash that the grant binds |
| `grant_id` | 64 hexadecimal characters | The identifier of the grant |
| `grant_signature` | 128 hexadecimal characters | The signature of the signed grant |
| `issuer_assent` | object | `party`, the key of the issuer's assent, and `signature`, its signature. With `genesis` and `contract` they determine the assent |
| `recipient_consent` | object | `event_id` and `signature`, the `id` and the `sig` of the consent event; for a recipient by name also `name_output` |
| `name_output` | object, inside `recipient_consent` | `txid`, 64 hexadecimal characters, and `vout`, an integer in the number form: the evidence output of W7.6 |

Nobody signs the preparation, and nobody needs to transport it. Whoever
holds the signed grant, the issuer's assent and the consent event builds
the same octets.

W8.2. The preparation states the signature of each signed part beside what
identifies the part. The anchor therefore fixes the exact signed
preparation. A part that is presented under another valid signature is the
same object (W5.4) and is still not what was published: the recomputed
commitment differs.

W8.3. A preparation for a recipient by name carries `name_output`. A
preparation for a recipient by key carries none. The mode is the grant's.
A presentation that offers an evidence output for a grant by key, or none
for a grant by name, refuses as `ISSUANCE_MODE`.

W8.4. The issuance commitment is the typed digest of the preparation
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

W8.5. A verifier recomputes the preparation from the parts that were
presented, takes its typed digest and compares it with the commitment of
the frame. A difference refuses as `ISSUANCE_COMMITMENT`. The frame is
checked first, so a grant that is presented under another signature than
the anchored one already refuses at the pointer.

For the vector `issuance-v-01` the commitment is
`08a0d8033a1eb887a1bb9c7965c92130fa2b133f5d908f435123d660eccf2a93`, and the
script is:

```text
6a03534c01420208a0d8033a1eb887a1bb9c7965c92130fa2b133f5d908f435123d660eccf2a93
01e55b1893e8f41bd23d5f306696a728844721388e15e246abb049a9c88b8c59a0
```

The line break is for display; the script has none.

### 9. Order of checks and refusal codes

A reader reports one refusal, the first in this order. The order matters
where one defect could be reported in two ways: a name that is spelled with
an escape and repeats another name is a duplicate, and a number with a
fraction is refused as a number before any schema is consulted.

| Step | What is checked | Codes |
| --- | --- | --- |
| 1 | The document: W1.1 to W1.6, in that order | `WIRE_SIZE`, `WIRE_JSON`, `WIRE_DUPLICATE`, `WIRE_VALUE`, `WIRE_NUMBER`, `WIRE_STRING`, `WIRE_NOT_CANONICAL` |
| 2 | For a signed form: exactly the members `payload` and `signature` (W5.3) | `WIRE_MEMBER` |
| 3 | The `type` of the payload (W3.1, W3.3, W3.4) | `WIRE_TYPE` |
| 4 | The members of the payload under the schema of its type (W3.2, W2.1, W2.3, W3.5), and then the keys among them (W3.6) | `WIRE_MEMBER`, `WIRE_INTEGER`, `WIRE_KEY` |
| 5 | The encoding of the signature (W5.2) | `WIRE_SIGNATURE_FORM` |
| 6 | The key of the place (W5.5) | `WIRE_KEY` |
| 7 | The signature (W5.1, W5.2) | `WIRE_SIGNATURE` |
| 8 | References to the object and from it (W6.3) | `WIRE_ID` |
| 9 | The rules of the object: for an assent W7.2; for a consent event W7.4; for an issuance W8.3, then W8.4, then W8.5 | `ASSENT_BINDING`, `ASSENT_PARTY`, `CONSENT_SHAPE`, `CONSENT_BINDING`, `CONSENT_KEY`, `CONSENT_EVIDENCE`, `CONSENT_SIGNATURE`, `CONSENT_TIME`, `ISSUANCE_MODE`, `ISSUANCE_FRAME`, `ISSUANCE_COMMITMENT` |

A refusal of this section records no closure. Every code is new, and none
replaces a code of an earlier format.

### 10. Vectors

[`vectors/LIP-0020/wire-vectors.json`](../vectors/LIP-0020/wire-vectors.json)
holds 137 vectors. Each names the rules that it exercises. The list
`rules` of the file names, for each of the 41 rules of sections 1 to 8, its
section, its state and at least one vector; the state of every rule is
`proposed`. A refused vector holds one defect, states the expected code and
names a valid neighbour that differs from it in that defect alone.

| Group | Vectors | What it holds |
| --- | --- | --- |
| `canonical` | 11 valid, 30 refused | Section 1 on octets: order by UTF-16 code units, the two escapes, literal U+007F and U+2028, a URL, the depth; every step of W1.1 to W1.6 with its code |
| `integers` | 4 valid, 13 refused | The string form of W2.3 for a bound of 2^64 - 1 |
| `digests` | 7, and 1 across types | For each type of the registry the tag, its SHA-256 and the typed digest of a payload that holds the type alone |
| `signed` | 3 valid, 17 refused | Sections 4 to 6 on a signed form: a second valid signature of one payload; signatures without the tag, under the prefix style and under another type's tag; the three ways in which strict verification fails; a stated identifier; an unknown version |
| `identifiers` | 4 | The identifier, the typed digest and the content address of one object, and references that state the wrong one |
| `assents` | 3 valid, 8 refused, 6 bindings | Section 7.1 |
| `consent_events` | 1 valid, 15 cases | Sections 7.2 to 7.4, with the mode of the recipient as context |
| `issuance` | 3 valid, 11 refused | Section 8: preparations for both modes, the commitment, the frame |

Three things about the file are limits and not defects of a reader that
finds them. The keys are the published test keys of BIP-340 and belong to
nobody. A payload that holds only `type`, or `type` and `note`, stands in
for a grant, whose members are open: it shows the digest, the signature and
the identifier and is no valid grant. And the cases of section 7.5 are
absent, because they need a node.

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
- **Consent by the owner key of the recipient's name.** The owner key never
  changes while the grant lives, so no evidence output would be needed. The
  owner key is the key that LIP-0008 section 3.1 keeps offline, and a
  contract would then need it online.
- **A preparation that binds identifiers only.** The commitment would not
  change when a part is signed again. The anchor would then no longer show
  that the signatures existed when it was mined, which the v3 commitment
  shows by binding both signatures.
- **A new action in place of a payload version.** Action `0x01` already
  means a grant issuance, and its payload begins with a version octet for
  this purpose.

## Security consequences

- **What the layer gives.** A signature covers a type together with its
  octets, an amount is read from its digits, and one payload has one
  identifier. A reader that follows section 9 never repairs an object and
  never reports a later defect in place of an earlier one.
- **What it does not give.** Canonical bytes say nothing about meaning. A
  payload that passes sections 1 to 6 can still hold members that no rule
  admits; the schema of its type decides that, and for five of the seven
  types it does not exist yet.
- **Identifiers and state.** An identifier that leaves the signature out is
  stable under re-signing, which is what a reference needs. It is no
  defence against replay. State is keyed as section 6 says, and a journal
  that keys a request by an object identifier alone admits the same request
  again under a new `iat`.
- **The exact signed preparation.** The commitment binds signatures, so a
  presenter must hold the signatures that were anchored. An issuer that
  loses them cannot replace them without a new anchor.
- **Consent of a recipient by name.** Section 7.3 states the limit of the
  verifier's read. A stolen former channel key cannot consent to a new
  contract at an honest issuer, because the issuer reads the name's current
  value; it can at an issuer that skips that read, and such an issuer can
  also sign a grant that nobody asked for.
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
rows need no object whose members are open.

## Open questions

- **The owners' acceptance of each proposal**, in particular: the
  identifier without the signature (section 6); one `type` string as the
  tag (sections 3 and 4); the string form for amounts and counters with
  2^64 - 1 as the largest bound of the first profile (section 2); the
  exclusion of `null` and of code points below U+0020 (section 1); the
  depth of 16 and the largest sizes; the names of the seven types.
- **The members** of the grant, the invocation, the receipt, the seal-key
  endorsement and the successor attestation, with their vectors, and with
  them the journal key of a request.
- **The assent to a child's contract.** Which key signs for the delegating
  party, when the delegation key signs child grants and nothing else
  (section 7.1).
- **Consent by name at admission.** Whether a verifier must prove that the
  evidence output was the name's current output at the recent block, which
  takes a walk of the recipient name's history that LIP-0008 does not
  otherwise require (section 7.3).
- **The age of a consent**, at the issuer and at a verifier (section 7.4).
- **Other channels.** The consent event belongs to the Nostr channel. A
  channel with another signature scheme needs its own form of consent.
- **Contracts with more than two parties.** The preparation binds two
  consents. The anchor of LIP-0017 is the place for more, and its
  commitment is open there.
- **The chain.** The objects of this LIP name the chain by its genesis hash
  alone. The pin of the construction profile (LIP-0008 section 1.1) is
  open, and so is whether a `network` label joins it.
- **The presentation.** What a presenter hands to a verifier; how a reader
  that starts from the frame obtains the assent and the consent event
  beside the grant; and how a reader fetches a parent that a child names
  by its identifier (section 6). LIP-0019 leaves the presentation of a v4
  grant open.
- **A list for object types in LIP-0018**, beside its four lists, and who
  assigns an identifier.
- **A published checker and a second implementation** for the vectors.
