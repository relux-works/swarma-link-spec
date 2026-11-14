# LIP-0019: Retrieval by hash

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** how a reader obtains an object that a locator or a bundle
  names by its hash
- **Builds on:** LIP-0005; relates to LIP-0004, LIP-0009, LIP-0014,
  LIP-0016 and LIP-0017

## Summary

A frame on chain can say that an object lies in a content-addressed blob
store and give its hash (LIP-0005, location type `0x01`). Nothing says how a
reader gets from that hash to the bytes. An auditor who finds an issuance
frame cannot fetch the grant behind it, and a verifier that is shown a
child grant without its parent has no rule for obtaining the parent.

This LIP proposes a delivery profile for that step and the loader that
performs it: where the loader looks for a store, how it fetches by hash,
and what it checks before it hands the bytes on. It records Ivan Oparin's
decision of 2026-11-14 that such a profile is specified; the co-author's
agreement is pending. Every rule below is the draft's proposal. Nothing of
it is implemented.

## Motivation

Four uses need bytes that the asking party does not hold:

| Use | Object | Named by |
| --- | --- | --- |
| Audit | The canonical signed grant behind an issuance frame, or the signed contract behind an anchor frame of LIP-0017 | The pointer of the frame's locator: for a grant its `grant_id`, for a contract the hash of its stored bytes |
| Dispute | A verdict, a termination statement, a disclosed clause of a contract | The pointer of a termination frame, or a hash that a party gives |
| Parent grants | The parent's canonical signed grant and its contract, from which a verifier of a child completes the parent's presentation (LIP-0014 section 8, V2) | The `parent_grant_id` of the child, which is the SHA-256 of that signed grant, and the contract hash of the parent |
| Certificate sets | The head of an issuer and the records of its set (LIP-0016) | The `head_id` and the record ids |

In each of them a value that a signature or the chain already binds decides
whether a fetched object is the right one. For most objects that value is
the hash that the loader asks for. For a contract of LIP-0017 it is an
identifier that the reader recomputes from the fetched bytes (section 5).
What is missing is only availability.

A presentation is not among these objects. LIP-0004 section 2 makes a
`grant_id` the SHA-256 of the canonical signed grant alone, and it leaves
the issuance locator of a presentation unsigned and outside the id. No
presentation can therefore hash to a grant id, and section 5 says how a
reader completes one.

## Current state

- LIP-0005 defines the locator and says that endpoint discovery is separate
  configuration or future profile work. Its reference parser fetches
  nothing.
- The delivery profile of the reference implementation takes a complete
  grant presentation from the presenter and does not use the locator.
- LIP-0016 names a content-addressed blob store as a later provider of a
  certificate store.
- LIP-0009 lists the operations of a Blossom store, among them the
  retrieval of a blob by its SHA-256.

## Proposal

### 1. The loader

A loader is the part of a reader that turns a hash into checked bytes. It
is given the hash, the kind of object that is expected, and a largest
size. It returns the bytes, or it reports that it has none. It never
decides what the object means.

### 2. Where the loader looks

The loader takes endpoints from these sources, in this order:

1. Its own configuration: the stores that its operator chose.
2. A hint that travels with the request or the bundle. A hint is unsigned.
   It may point the loader to a store and gives that store no trust.

A hint also names an address that the loader would contact, and a request
is sent before any byte can be checked. A loader therefore takes an
endpoint from a hint only under a policy of its operator that says which
schemes, hosts and address ranges it may contact. This draft does not
define that policy, and a loader without one uses its configured stores
alone. The price of that default is availability: an object that only a
hinted store holds then counts as not presented.

A third source is possible later and is not defined: a member of the
issuer's name value outside `swarma`, which a LIP-0010 reader ignores. The
landlord and agent values of Grant v3 are closed and cannot carry it.

An endpoint is trusted for availability and for nothing else, like a
provider of LIP-0016. The loader sends it no credential and no grant data.

### 3. The fetch

The first transport is the retrieval of a Blossom store, a `GET` of the
SHA-256 in lowercase hexadecimal (LIP-0009 names it as BUD-01). The loader
bounds what it accepts before and while it reads: the largest size for the
expected kind of object, a time limit, and no redirect to another host.
The location types `0x02` to `0x04` of LIP-0005, the BitTorrent networks,
need a profile of their own.

### 4. The check

1. The SHA-256 of the fetched bytes MUST equal the hash that was asked
   for. Bytes that hash to anything else are discarded, and the loader
   tries the next endpoint.
2. The reader then checks the object exactly as if the presenter had
   handed it over: its canonical bytes, its signature, its identifier and
   every state check that its use requires. A fetched grant is no more
   live than a presented one, and LIP-0008 section 12.2 says the same of a
   fetched proof.
3. An object that no endpoint returned counts as not presented. The
   request that needed it refuses or is held under its own rules, and no
   closure is recorded for it.

Retrieval therefore adds availability and no authority. A store that
returns wrong bytes, old bytes or nothing can make a reader refuse; it
cannot make a reader accept.

### 5. What a hash addresses

A grant id is the SHA-256 of the canonical signed grant
`{"grant":…,"signature":…}` and of nothing else. A store can therefore
serve a signed grant under its id, and it can never serve a presentation
under it: the presentation of LIP-0004 section 2 holds the signed grant
and, beside it, the issuance locator, which is unsigned and outside the
id. The loader asks for the SHA-256 of stored octets, as LIP-0005 defines
the pointer of location type `0x01`, and for two objects that hash is not
the whole answer.

**A presentation is completed, not fetched.**

1. The loader fetches the canonical signed grant by its grant id. It MUST
   NOT ask a store for a presentation by a grant id, and a body that holds
   anything beside the canonical signed grant fails rule 1 of section 4.
2. The reader takes the issuance locator from the bundle or the request,
   as an unsigned hint, and puts it beside the fetched signed grant. The
   result is checked as every presentation is. LIP-0004 section 4 requires
   that the transaction which the locator names is confirmed in the active
   chain on the reader's own node, and that its one `OP_RETURN` output
   carries the issuance commitment. The reader recomputes that commitment
   from the fetched signed grant alone, and the commitment binds the grant
   id, so a locator that names another transaction fails.
3. A fetched signed grant without a locator is no presentation. The
   presentation then counts as not presented, as under rule 3 of section
   4.

For the parent of a child grant, the loader only fills what the bundle
lacks before the checks of LIP-0014 section 8 run, and none of those
checks changes. Without a locator the bundle does not hold the parent's
presentation as a complete object, and V2 refuses as `DELEGATION_BUNDLE`.
With a locator, V3 recomputes the grant id from the fetched signed grant,
and V5 runs the v3 check of LIP-0004 section 5, which includes the
issuance of section 4 and refuses a wrong locator as `PARENT_NOT_LIVE`.
Rules 1 to 3 are for Grant v3. The presentation of a v4 grant belongs to
its own profile, which is open.

An auditor works in the other direction. It starts from the issuance
transaction, so it already holds the locator, and it fetches the signed
grant by the pointer of the frame. An issuance in the historical bare form
of LIP-0004 section 4 carries no pointer, and an auditor cannot fetch its
grant from the chain alone.

**A contract of LIP-0017 is fetched by the hash of its stored bytes, not
by its identifier.** The identifier commits to salts and to the
commitments of the clauses (LIP-0017 section 2), so it is not the SHA-256
of any stored document. The loader fetches the contract by the hash of its
stored bytes, which is the pointer of its anchor (LIP-0017 section 3) or a
hash that a party gives. Under rule 2 of section 4 the reader then
recomputes the identifier from the fetched bytes and compares it with the
identifier that it was looking for: the one that the commitment of the
anchor binds, or the one by which another contract names its framework
contract (LIP-0017 section 5). A hash that a party gives is a hint: it
finds bytes and proves nothing about them.

Every other object of this LIP is addressed by its own identifier: the
contract of a v3 grant by `contract_sha256` (LIP-0013), a verdict by its
`verdict_id` (LIP-0011), a termination statement by the hash of its signed
bytes (LIP-0017 section 6), and a head and a record of a certificate set
by the `head_id` and the record id (LIP-0016).

### 6. What is public

An object in a public store is public to whoever knows its hash. A grant
names its parties, and a head lists the keys an issuer binds. A store also
learns which hashes a loader asks for, and from which address.

A contract of LIP-0017 is no exception, because a salt is not encryption.
A stored contract that holds the octets of its clauses is plain text to
everyone who fetches it, with or without the salts. What a party can store
without showing a clause is a disclosure in the sense of LIP-0017 section
2, which holds the commitment of that clause in place of its octets and
its salt. Such a disclosure still shows the parts other than the clauses,
the parties and the window among them, and the number and the positions of
the clauses.

## Alternatives

- **The presenter always supplies everything.** That is the delivery of the
  reference implementation. It serves admission and fails an auditor, who
  has no presenter.
- **A location on chain,** such as a short server identifier in the
  locator. LIP-0005 proposes not to spend bytes on it.
- **A fixed store for all issuers.** It names an operator that every party
  has to trust for availability.

## Security consequences

- A store can withhold. The result is a refusal or a held request, never
  an acceptance.
- A hint can point a loader at a hostile store, or at an address that is
  no store at all, such as a service inside the loader's own network. The
  hash check and the bounds of section 3 govern the bytes that come back:
  wrong bytes are discarded, and an answer that is too large or too slow
  is cut off. They do not govern which address receives the request. That
  is the policy of section 2, which this draft leaves to the operator, and
  without such a policy a hinted endpoint is not contacted.
- Fetching discloses interest in a hash to the store.
- The loader sends no credential, so a redirect cannot carry one away.

## Conformance impact

None while this LIP is a Draft. A future vector set pairs these controls:

| Valid control | Refusal or invariant |
| --- | --- |
| Bytes whose SHA-256 equals the requested hash, from a configured store | Bytes of another hash, an object above the size bound, and a redirect to another host: discarded, and the next endpoint is tried. |
| A parent's canonical signed grant fetched by `parent_grant_id` and completed with an issuance locator from the bundle; the parent then passes V2 to V5 of LIP-0014 section 8 | A fetched body that holds a whole presentation, or anything else beside the canonical signed grant, does not hash to the grant id and is discarded. A fetched parent whose seal is spent refuses as a presented one does; having fetched it changes nothing. |
| The same parent with a locator that names its confirmed issuance transaction | No locator: the parent counts as not presented, and the child refuses as `DELEGATION_BUNDLE`. A locator that names an unconfirmed transaction, or a confirmed one whose commitment is not the one recomputed from the fetched signed grant: the child refuses as `PARENT_NOT_LIVE`. Under LIP-0004 section 5 neither is a closure. |
| A contract of LIP-0017 fetched by the hash of its stored bytes, whose identifier recomputes to the one that the commitment of its anchor binds | Bytes that hash to the pointer and recompute to another identifier: the contract is refused, although rule 1 of section 4 passed. |
| A store named by a hint that the operator's policy allows returns the right bytes | A hinted endpoint outside the policy, and every hinted endpoint when no policy is set, is not contacted. A store named by a hint is sent no credential, and wrong bytes from it are discarded. |
| No endpoint returns the object | The object counts as not presented; the journal holds no closure. |

## Open questions

- The size bounds for each kind of object, and the time limits.
- Whether an issuance locator needs an address of its own, so that a reader
  with nothing but a grant id can find the issuance transaction. Today it
  needs the locator from the presenter, or a search of the chain for the
  frame whose pointer is that id, for which no index is defined.
- The operator's policy for hinted endpoints: which schemes, hosts and
  address ranges a loader may contact, and how it treats a redirect within
  one host.
- Whether a name value may name a store, and in which member.
- A profile for the BitTorrent location types.
- Whether an issuer has a duty to keep its objects retrievable, for how
  long, and who pays the store; LIP-0009 leaves retention to a contract.
