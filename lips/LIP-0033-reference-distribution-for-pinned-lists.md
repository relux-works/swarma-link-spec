# LIP-0033: Reference distribution for pinned lists and documents

- **LIP:** 0033
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Affects:** LIP-0005, LIP-0010 sections 10 and 11, LIP-0019,
  LIP-0029 section 3.5; LIP-0032 and LIP-0037
- **Follows:** LIP-0001 and LIP-0018

## Summary

A reference channel helps find bytes; it never restricts the channel over
which a verifier may receive them. The manifest of LIP-0010 section 11
pins the heads of the device, holder, certificate and card sets. Neither
the name value nor the manifest carries `loc`.

Ivan Oparin decided on 2026-11-20 that there is no `loc`, that one Nostr
event kind serves the lists and documents, that location type `0x05`
names that event, and that inline bytes precede retrieval. The co-author's
agreement is pending. These are Draft proposals, not deployed readers.

The words MUST, MUST NOT, SHOULD and MAY have their RFC 2119 and RFC 8174
meanings.

## Motivation and current state

LIP-0010 H17 to H20 and LIP-0029 O3.11 to O3.14 already make list copies
content-addressed, give presentation precedence and refuse `LIST_UNKNOWN`
without a silent fetch. Their secondary Nostr path leaves the event kind
open. LIP-0019 checks fetched bytes as presented bytes. This LIP closes
the event-kind gap and applies non-exclusivity to every object, without
spending name-value bytes on locators.

## 1. Retrieval paths

The primary path is the presentation, request or envelope: inline manifest
bytes first, then the required set bytes. The sender supplies them on change
and first contact; a cache entry is usable only under the exact current pin.
The set's counter is `seq`, not `v`.

A reader without a presenter MAY use the following secondary paths. It
verifies the manifest before using any head obtained from it.

| Object | HTTPS path, relative to the verified NIP-05 domain | Nostr `d` tag |
| --- | --- | --- |
| Manifest | `/.well-known/swarma/manifest/<sha256>` | `swarma-manifest` |
| Device list | `/.well-known/swarma/device-list/<sha256>` | `swarma-device-list` |
| Holders list | `/.well-known/swarma/holders-list/<sha256>` | `swarma-holders-list` |
| Certificate-set head | `/.well-known/swarma/certs/<sha256>` | `swarma-certs` |
| Entity card | `/.well-known/swarma/card/<sha256>` | `swarma-card` |

The device path retains the spelling of LIP-0029 O3.13. `<sha256>` is the
64 lowercase hexadecimal characters of the applicable pin. The response
body is the exact document bytes, without an added newline or wrapper.

A domain is usable only when its NIP-05 identifier is independently bound
to this name under a profile the reader supports. The key-and-relays
`nostr` object of LIP-0010 contains **no domain**. This LIP adds none and
does not derive one from an `id/` label. Until a domain-binding profile
exists or an operator has pinned that binding, that HTTPS path is
unavailable; an arbitrary peer URL supplies no such binding.

An anonymous `id/` name or a pure service with neither a NIP-05 domain nor
a Nostr key works fully when the sender supplies the manifest and every
needed set inline. Secondary paths are optional, never prerequisites.
This records Ivan Oparin's detail of 2026-11-20, event
`$EdwfFTmT7uElQhGWzEq0ykBQXA4pDYrolbWK9FaLWyA`; agreement is pending.

## 2. One Nostr event kind

This profile assigns dedicated **kind 30079** to all Swarma list and
document events, in the parameterized-replaceable (addressable) range of
[NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md). This is
a Draft profile allocation, not a claim of an already accepted upstream NIP
registration or of global exclusivity. Upstream collision/registration
coordination is an implementation gate before interoperable deployment.

Kind 30078 is deliberately not reused: current
[NIP-78](https://github.com/nostr-protocol/nips/blob/master/78.md) describes
private, owner-authenticated app data and directs public inter-application
formats to dedicated kinds. That privacy expectation would be a wrong
retrieval profile for these public list references.

There is exactly one `d` tag, with the value in section 1 for the current
manifest or set. Its event author is the key the owner's confirmed name
yields for Nostr. Its `content`, decoded as a Nostr string and encoded as
UTF-8, is the exact document bytes; the outer event's JSON escaping is not
part of those bytes. The reader checks the event's id and BIP-340 signature,
the author, kind and tag, and then the pinned hash and every document check.
A relay's choice of latest event never overrides a chain pin or a journal.

For other anchored documents the same kind is used, and `d` is the 64
lowercase hexadecimal characters of SHA-256 of the stored document bytes
(the content address, not necessarily the object's identifier or typed
digest). Re-signing may create a new content address. This general form
does not replace the fixed tags for current lists in section 1.

## 3. LIP-0005 location type `0x05`

The pointer is **32 bytes: the NIP-01 event id in binary**, not an author
key, a relay URL, a `nostr:` URI or an address string. A reader requests
that exact id from its operator-configured relays, checks the event id and
signature, requires kind 30079 and the `d` tag of section 2, and takes
`content` as the candidate document bytes. A replaced or unavailable event
is an availability failure only. The anchored object's own commitment
still decides authenticity.

An author key alone would not tell the loader the `d` of an arbitrary
anchored document: its content address cannot be recovered from a typed
commitment. An event-id pointer avoids that missing input and fits the
existing framing: 1 version byte + 32 commitment bytes + 1 location byte
+ 32 event-id bytes = 66 payload bytes, a 72-byte script. The event can be
formed before anchoring; it contains the document, not the anchor's txid.

This allocation does not make an existing action accept a new locator.
Each action's profile must admit it explicitly. In particular the v4
issuance proposal of LIP-0020 W8.5 admits only its stated locators.

## 4. Normative non-exclusive rule and security boundary

1. Every locator and secondary path is reference distribution only. It
   MUST NOT forbid another delivery channel.
2. A reader MUST NOT reject an otherwise valid object merely because it
   arrived inline, through encrypted messaging, HTTPS, a cache, QR or another
   channel. It first bounds size, then checks the object's canonical bytes
   and the value its own profile binds: a list hash, an identifier, a typed
   commitment or a content address. These are not interchangeable
   (LIP-0020 W6.4). All signature, name, window, seal and journal checks
   remain required on the verifier's own node.
3. No source, including a matching hash, grants authority on its own. A
   missing manifest gives no set in the manifest profile. A presentation
   missing required bytes refuses by name; the receiver does not silently
   fetch in place of that refusal.
4. Automatic retrieval MUST stay within the operator's scheme, host,
   address-range, size, time and redirect policy (LIP-0019 sections 2 and 3).
   Neither a peer hint nor a card endpoint can widen it. Inline bytes cause
   no outbound request; they still need size and parser bounds.

## 5. Deterministic refusals

The enclosing profile checks its name pin first. Within a candidate it
checks size before parsing, canonical grammar before hash equality, and
hash equality before semantic and live-state checks; the first failure
wins. Retrieval cannot replace those profiles' existing order.

| Stage | Existing refusal retained |
| --- | --- |
| Invalid manifest pin or manifest | `MANIFEST_PIN_INVALID`, `MANIFEST_INVALID`, `MANIFEST_MISMATCH`, `MANIFEST_ROLLBACK` (LIP-0010 section 11) |
| Oversized or malformed list | `DEVICE_LIST_INVALID` or `HOLDER_LIST_INVALID` |
| List bytes or identity differ from the pin | `DEVICE_LIST_MISMATCH` or `HOLDER_LIST_MISMATCH` |
| Required manifest/list bytes unavailable | `LIST_UNKNOWN` |
| Card grammar, mismatch or unavailable bytes | LIP-0037 section 5 |
| Other signed objects | Their own `WIRE_*` and state-check order |

The distribution layer retains the draft's `LIST_OVERSIZE` diagnostic for
candidate bytes exceeding the requested profile size, and
`LIST_HASH_MISMATCH` for candidate bytes differing from the requested hash.
Check size before hash; do not fetch further bytes after the size bound is
exceeded. These diagnostics do not rename the enclosing set/object profile's
more specific admission codes in the table. A loader may try another allowed
source after a bad candidate. When no usable bytes remain, the enclosing
admission refuses `LIST_UNKNOWN`, **not** the draft's `LIST_UNAVAILABLE`.
A denied outbound request is a loader-policy refusal, never permission to
contact an unconfigured host; matching inline bytes remain acceptable.
A failed transport is not a revocation. No closure is journaled merely
because bytes are unavailable.

## Alternatives

Per-set `loc` fields were rejected: they add no trust, conflict with the
two-member legacy pins, and two 11-byte hints overflow the 500-byte
landlord example. An author-key-only Nostr pointer leaves an anchored
object's lookup tag unknown. A universal raw SHA-256 comparison confuses
the three hashes of a v4 signed object.

## Conformance impact and extension checklist

This is a Draft. Vectors are **not required for Draft LIPs**; adoption under
LIP-0001 requires paired positive and single-defect negative cases and a
checker. Planned cases cover inline-only names, both optional secondary
paths, exact event-id length, kind/tag/author mismatch, stale events,
oversize-before-parse, SSRF and redirect refusal, and non-exclusive delivery.
No installed reader or cross-implementation agreement is claimed.

LIP-0018 checklist: identifiers and locators are sections 2 and 3; bytes and
bounds are sections 1 to 3 and the referenced object profiles; bindings,
refusal order and security are sections 4 and 5; the alternatives and
adoption path are above. No contract profile, limit kind or action leaf is
created, so their specialized checklist items do not apply.

## Open questions

- The co-author's agreement and the reader rollout for the manifest profile.
- The authenticated NIP-05 domain-binding profile; a NIP-05 key object is
  not itself that profile. Missing domain discovery never blocks inline use.
