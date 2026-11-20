# LIP-0037: Entity card — a name-pinned public identity card

- **LIP:** 0037
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Affects:** the public identity subset of agent, person and service cards
- **Builds on:** LIP-0010 sections 10 and 11, LIP-0019, LIP-0029;
  KEY-REGISTRY, Name-owner key
- **Follows:** LIP-0001 and LIP-0018

## Summary

The card is one document, `swarma-card/1`, pinned by the `swarma-card`
entry of the name's `swarma-manifest/1`. It has **no signature inside it**.
Authenticity follows the SHA-256 chain from the confirmed name value to
the manifest and from the manifest to the card. Only the name owner can
write that name update.

Ivan Oparin decided on 2026-11-20 (source: `$LGvz_xrefHjg61tvoQgu5D4Dew_A_vZlfo09ay__PbQ`) on this placement and on option (a),
pin-only authenticity, in event
`$LGvz_xrefHjg61tvoQgu5D4Dew_A_vZlfo09ay__PbQ`. The co-author's agreement
is pending. This is a Draft proposal; no installed adoption is claimed.

The words MUST, MUST NOT, SHOULD and MAY have their RFC 2119 and RFC 8174
meanings.

## Motivation and current state

The a2a-swarm Markdown card is another owner's accepted protocol. It is
maintained under that protocol, including its own `a2a card set` workflow.
It is not demoted, replaced or declared invalid by
this LIP. Only the identity subset defined here can be projected from
the name-pinned card; status, heartbeat, goals, claims, subscriptions,
boards and other coordination fields remain governed by a2a.

A public directory, another transport and a human client need the same
verifiable name-bound identity subset without treating a repository or a
homeserver as the authority over that name. A card describes reachability
and work, not permission. Third-party claims belong to LIP-0032 credentials.

### The size question

The complete name value is at most 520 bytes. With the measurement inputs
of LIP-0010 section 8 and a one-digit manifest `seq`:

| Value | Without manifest | With manifest | Left of 520 |
| --- | ---: | ---: | ---: |
| Landlord, NIP-05 object and one relay | 294 | 398 | 122 |
| Landlord, NIP-05 object and no relay | 191 | 295 | 225 |
| Agent, key string in `nostr` | 121 | 225 | 295 |
| Agent, NIP-05 object and one relay | 240 | 344 | 176 |

The card itself adds **no further name bytes**: its head is inside the
manifest. The old three-head landlord was 601 bytes and did not fit.
There is no direct card-head placement and no certificate-store placement.
The old rule C7 and the two-placement Cases are withdrawn, not precedence
rules in this profile. The full relay list lives in the card; an owner
SHOULD put **no relay hint in the name value** as an operating rule, not
as a new parser refusal.

## 1. The card bytes

The document is one compact UTF-8 JSON object, at most **16384 bytes**,
without a BOM or trailing bytes, with exactly these members in this order:

| Order | Member | Meaning and bound |
| --- | --- | --- |
| 1 | `schema` | Exact string `swarma-card/1` |
| 2 | `network` | `main` or `regtest`, matching the manifest and pinned chain |
| 3 | `name` | The entity's own `id/` name, at most 255 ASCII bytes |
| 4 | `seq` | Positive canonical JSON integer, at most 9007199254740991 |
| 5 | `kind` | `agent`, `person` or `service` |
| 6 | `display` | Short human label, directing no authority |
| 7 | `owner` | Landlord/operator `id/` name, at most 255 ASCII bytes; the same name for a person |
| 8 | `transports` | Array of `{transport,address}` objects, in that member order, each identifying one public reachability hint |
| 9 | `relays` | The full list of absolute ASCII `ws` or `wss` URLs with a host; the empty list is valid |
| 10 | `role` | Short work description, directing no authority |
| 11 | `contact` | Public contact address or empty string |
| 12 | `replaces` | Canonical nonnegative JSON integer, less than `seq`; 0 for the first card, otherwise the previous card's `seq` |

Canonical encoding is fixed-order, **not** RFC 8785 key sorting. Outside
strings there is no whitespace. Member names are literal ASCII. String
values contain Unicode scalar values from U+0020 upward, except U+007F
through U+009F; write them literally in UTF-8 with only `\"` and `\\`
escapes. There is no normalization. Integers use the number form of
LIP-0020 section 2, not strings; they have no leading zero, sign, fraction
or exponent. Arrays keep their order. A reader re-encodes and requires
identical bytes. Duplicate, unknown, reordered or null members refuse.
The 16384-byte bound covers the complete document, not a signed wrapper.

`transport` is a nonempty ASCII string; `address` is a nonempty string
in the card encoding. The complete 16384-byte document cap bounds these
fields and arrays; no additional per-field quota is imposed. This is a reachability vocabulary, not an action registry:
an unknown transport is an opaque hint, never authority or an automatic
connection. Matrix, XMPP, Mattermost, Nostr, email and HTTPS may be listed.
A `nostr` entry is the
64-hex key the name's `nostr` yields; a contradictory Nostr address gives
`CARD_MISMATCH`. A name without a Nostr key has no `nostr` entry.

For `kind` `agent`, the name has the agent `swarma` shape and `owner`
equals `swarma.agent.landlord`. An agent-shaped name cannot claim another
kind. `owner` in this document is an operator description, **not** the
name-owner output key or the manifest's naming field. A consumer derives
landlord authority from `swarma`, never from the card. A person uses its
own name as `owner`; a service's operator is a public claim only.

Free text directs no authority (LIP-0029 O1.2). Empty `transports`,
`relays` and `contact` are valid. A person's private contacts SHOULD stay
out of the public card and be disclosed through LIP-0036 or a separately
governed audience projection. The card is public; a salted hash or private
delivery does not make published contacts private.

## 2. Authenticity and retrieval

EC1. The reader first verifies the name and manifest under LIP-0010
section 11. The `swarma-card` entry pins the card's `seq` and SHA-256 of
its exact bytes; the card's `name` and `network` match that name and chain.
There is no detached signature, signed form, card key or card seal in v1.
The cold name-owner key signs the **name operation**, not the card bytes.

EC2. Distribution follows LIP-0033: inline card and manifest at first
contact or on change, otherwise an exact-pin cache; optional well-known
retrieval by a verified NIP-05 domain, then kind 30079 with
`["d","swarma-card"]` signed by the name's Nostr key. Every candidate
passes the same hash and document checks regardless of its source.
A name without domain and Nostr works fully with inline bytes. A card's
transport or relay hints never replace the loader's SSRF policy.

EC3. A missing or invalid card gives no verified card. It leaves grants
and other sets as they read, unless their common manifest itself is
invalid. Reading a card gives no permission to invoke any action.

## 3. Updates, rollback and removal

EC4. Every changed card increments its set `seq`; the owner publishes a
new manifest with a strictly higher manifest `seq`. Unchanged cards keep
both set counter and hash when another set changes. Readers journal both
heads under the name and registration (SH5). The same set counter and
same hash is a reread; a lower counter, or the same counter with another
hash, is `CARD_ROLLBACK` while the journaled operation stays in the chain.
`replaces < seq` is checked, but a reader need not have seen the prior card.

EC5. A verified new manifest which omits a formerly present card records
its removal at the highest card counter taken. Only a later card of a
higher counter can be taken. Unavailable bytes or an invalid manifest are
not proof of removal and write no removal mark. SH5's reorganisation
branch restores the last confirmed head but keeps removal and revocation
marks; a removed version does not return merely through a reorganisation.
An expired or differently owned name supplies no current card under the
old pinned registration and ownership policy. There is no instant card
revocation apart from ceasing to rely on the name; name updates confirm
slowly. Seal revocations of grants remain independent and fast.

## 4. Projection rule

EC6. A consumer projecting these identity fields carries the source
`name`, card `seq` and card `sha256`, and the manifest head from which it
verified them. Without that mark the copy is an unverified **Link identity
projection**, not a verified `swarma-card/1`. This says nothing against its
status as a valid a2a roster card under that protocol. LIP-0037 governs
only the identity subset; changing the a2a format needs that owner's own
process. It does not put heartbeats or coordination state on chain.

## 5. Deterministic refusals

After the manifest pipeline, the first applicable card failure wins:
(1) no card entry or no bytes, `CARD_UNAVAILABLE`; (2) size, canonical
grammar, fields, bounds or duplicates, `CARD_INVALID`; (3) hash, name,
network, counter-versus-pin, agent/operator or Nostr binding mismatch,
`CARD_MISMATCH`; (4) journal rollback or a counter at or below its removal
mark, `CARD_ROLLBACK`. Journal loss/fencing retains LIP-0025's codes.
No `CARD_BUDGET` reader code exists: the writer measures the entire name
value, and all card data beyond the manifest head is off chain.

Consumers rendering `display`, `role` or other human-facing metadata
SHOULD isolate untrusted text and visibly flag bidi controls U+200E/U+200F,
U+202A–U+202E and U+2066–U+2069. They do not change identity or authority.
This display warning does not silently change the v1 canonical grammar.

## Alternatives and security consequences

Option (a), no internal signature, is chosen because another signature is
redundant under the owner-written hash pin. The owner's stated premise is
"LIP-0029 O3.7/O4.6 stay intact (device keys never face foreign verifiers)"
in `$LGvz_xrefHjg61tvoQgu5D4Dew_A_vZlfo09ay__PbQ`, without a card-reader
qualification. The Swarma Link editor's resolution preserves that premise:
LIP-0034 uses a dedicated auth key instead. The card survives a device's
revocation and prevents an
agent from rewriting its own card without its name owner's operation.

Rejected: signing with the Nostr key would widen a closed messaging-key
role; signing with an owner device plus subject countersignature would
require foreign device-list readers, couple the card to device revocation
and add a redundant signature under the pin. Direct name placement and
certificate-store placement are rejected in favour of the single manifest.
The public card adds no certificate-store record type.

## Conformance impact and extension checklist

This is a Draft. Vectors are **not required for Draft LIPs**. Adoption
needs valid agent/person/service cards and negative neighbours for wrong
pin, owner, network, Nostr key, bounds, duplicate members, equal-counter
hash substitution, missing bytes, removal and reorganisation. A valid
inline-only service and a valid unchanged-card manifest update are controls.
No implementation or cross-reader byte agreement is claimed.

LIP-0018 checklist: identifier, canonical bytes and size are section 1;
binding and retrieval section 2; journal/refusal rules sections 3 and 5;
security, alternatives and adoption are above. This is neither a contract
profile, action leaf, limit kind nor certificate-subject kind; their
specialized checklist items do not apply.

## Open questions

- The co-author's agreement and the manifest reader/legacy transition.
- Future option (d) for fast off-chain updates: a distinct domain
  `swarma-card-v1` on the grant key or a dedicated card key, **not** the
  Nostr key or a device key. Custody, rotation, replay, algorithms and bytes
  remain open. This grants no new signing use to any key in v1.
- A sealed private companion, and a2a's own decision on a projection mark.
- A key-only executor has no card and no holders entry: a holders entry
  names an `id/` name (LIP-0010 section 10.1). Its grant's pinned executor
  key, not a fictitious holders record, describes its authority boundary.
