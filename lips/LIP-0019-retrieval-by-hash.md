# LIP-0019: Retrieval by hash

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** how a reader obtains an object that a locator or a bundle
  names by its hash
- **Builds on:** LIP-0005; relates to LIP-0009, LIP-0014, LIP-0016 and
  LIP-0017

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
| Audit | The signed grant behind an issuance frame | Its `grant_id`, the pointer of the frame's locator |
| Dispute | A verdict, a termination statement, a disclosed clause of a contract | The pointer of a termination frame, or a hash that a party gives |
| Parent grants | The parent presentation and its contract, which a verifier of a child needs (LIP-0014 section 8, V2) | The `parent_grant_id` of the child and the contract hash of the parent |
| Certificate sets | The head of an issuer and the records of its set (LIP-0016) | The `head_id` and the record ids |

In each of them the hash is already known and already bound by a signature
or by the chain. What is missing is only availability.

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

### 5. What is public

An object in a public store is public to whoever knows its hash. A grant
names its parties, and a head lists the keys an issuer binds. A contract of
LIP-0017 shows nothing without its salts. A store also learns which hashes
a loader asks for, and from which address.

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
- A hint can point a loader at a hostile store. The hash check and the
  bounds of section 3 limit what that store can do to refusing and to
  wasting the loader's time.
- Fetching discloses interest in a hash to the store.
- The loader sends no credential, so a redirect cannot carry one away.

## Conformance impact

None while this LIP is a Draft. A future vector set pairs these controls:

| Valid control | Refusal or invariant |
| --- | --- |
| Bytes whose SHA-256 equals the requested hash, from a configured store | Bytes of another hash, an object above the size bound, and a redirect to another host: discarded, and the next endpoint is tried. |
| A fetched parent presentation that passes every check of LIP-0014 section 8 | A fetched parent whose seal is spent refuses as a presented one does; having fetched it changes nothing. |
| A store named by a hint returns the right bytes | A store named by a hint is sent no credential, and wrong bytes from it are discarded. |
| No endpoint returns the object | The object counts as not presented; the journal holds no closure. |

## Open questions

- The size bounds for each kind of object, and the time limits.
- Whether a name value may name a store, and in which member.
- A profile for the BitTorrent location types.
- Whether an issuer has a duty to keep its objects retrievable, for how
  long, and who pays the store; LIP-0009 leaves retention to a contract.
