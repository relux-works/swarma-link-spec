# LIP-0010: Name value

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** name values of the landlord profile, their readers, the
  discovery record and deployment; amends LIP-0004 section 1
- **Relates to:** LIP-0007 and LIP-0008

## Summary

A name value has one member that belongs to Link: `swarma`. Every other member
belongs to the name's owner or to another standard, and a Link reader does not
interpret it. Inside `swarma` parsing stays strict.

An agent's key is written once, in the `nostr` member, in the shape NIP-05
defines for `names` and `relays`. `swarma.agent` keeps only the landlord
pointer. A reader accepts the two published forms of `nostr`, a key string and
a NIP-05 object, and both give the same key.

`d/` stays a discovery record without authority. A deployment registers
`d/<label>` together with `id/<label>`, because the two names are unrelated on
chain and Nostr clients resolve `<label>.bit` through `d/<label>`.

This LIP proposes reading rules and value shapes. It adopts no normative
profile, and no implementation of these rules is claimed.

## Decisions recorded

Ivan Oparin decided D1 to D4 on 2026-11-10 and D5 and D6 on 2026-11-11. The
LIP stays Draft until the
co-author agrees; adoption follows LIP-0001.

| Decision | Direction |
| --- | --- |
| D1. Owner members | The value may carry the owner's own members outside `swarma`. The reader ignores them and does not refuse the value. Parsing inside `swarma` stays strict, with the existing alias and fold rules. |
| D2. Agent key once | The agent key appears once, in `nostr.names._`, following NIP-05. `swarma.agent` keeps only `landlord`. The verifier reads the agent key from `nostr`, so `nostr` becomes mandatory for an agent name. The rule behind it: each entity is self-sufficient, and links exist only where they are needed. |
| D3. Both forms of `nostr` | The reader accepts `"nostr":"<hex>"` and the NIP-05 object `{"names":…,"relays":…}`. Both yield the same key for `_`. A shape the reader does not understand does not invalidate the `swarma` authority. |
| D4. `d/` optional | In the protocol `d/` is discovery only and confers no authority. Deployment registers `d/<label>` and `id/<label>` as a pair. |
| D5. Duplicate or aliased `nostr` | A duplicate or a fold alias of `nostr` at the top level refuses the whole value, like one of `swarma` (section 2 rule 2). The alternative, reading an unambiguous `swarma` and treating such a `nostr` as yielding no key, is not taken. |
| D6. Breadth of the pair rule | The deployment registers `d/<label>` for every `id/` name that has a `d/` counterpart, agents included (section 7). |

The owners decided on 2026-11-12 that a notary publishes its attestation key
in its own `id/` name ([LIP-0014](LIP-0014-notary-certified-redelegation.md),
D3). Section 9 is a Draft amendment that proposes the shape for it. The
shape itself is not decided.

## Motivation

The reference reader of the landlord profile compares the complete value with
the bytes its own builder would write. An owner who adds an e-mail address or
a member of another standard to the name makes the value invalid for Link, so
one name cannot serve as the owner's identity for several systems.

The agent value states the agent's key twice: in `swarma.agent.nostr` and in
`nostr.names._`. The copies must be equal. The second copy costs 75 bytes of a
520-byte value, and the equality rule can only add a refusal.

Deployed Nostr clients read two forms of the `nostr` member in Namecoin
values. A reader that accepts one form refuses names that the other software
treats as valid.

An owner who registers `id/alice` and not `d/alice` leaves the second name
free. Whoever registers it controls what Nostr clients and browsers show for
`alice.bit`. The protocol is not affected, and the deployment needs a rule.

## Current state

LIP-0004 section 1 describes the values of the landlord profile as implemented
in `swarma-chain-lab` at `11084e3a31175907e77644a7596e7802283e7c1e`:

```json
{"nostr":{"names":{"_":"<social key>"}},"swarma":{"landlord":{"grant":"<grant key>"}}}
{"nostr":{"names":{"_":"<agent key>"}},"swarma":{"agent":{"nostr":"<agent key>","landlord":"id/alice"}}}
```

These two lines show the member order with placeholders. The reader requires
the exact bytes of its builder. It refuses an unknown member, a key string in
place of the `nostr` object, a `nostr` object with members other than `names`
and `relays`, and a `names` object with an entry other than `_`. For an agent
it requires `nostr.names._` to equal `swarma.agent.nostr`. The `nostr` member
is optional in both values.

Normative v0.1 already separates the two sides: issuers must not write members
other than the defined ones, and a verifier ignores members it does not define
unless they are aliases or fold conflicts ([names](../protocol/names.md)
§2.3). The landlord profile is stricter than v0.1 on this point.

## Proposal

### 1. Who defines each member

| Top-level member | Defined by | What a Link reader does with it |
| --- | --- | --- |
| `swarma` | This specification | Reads the authority binding under section 3. |
| `nostr` | NIP-05 for the shape of `names` and `relays`; the draft NIP-N0 and NIP-N1 for carrying that shape in a Namecoin value | Reads one key, the entry for `_`, and optional relay hints under section 4. |
| Any other member | The name's owner or another standard | Does not read it. |

The only part of the value that Link defines is `swarma`. Authority comes from
`swarma` alone. A member outside `swarma` that looks like a grant key, a
landlord pointer or a limit gives nothing.

### 2. Reading the top level

1. The value MUST be exactly one JSON object in UTF-8, at most 520 bytes
   long. Bytes after the object MUST cause refusal.
2. A reader MUST match `swarma` and `nostr` by exact name. It MUST refuse the
   value when either name occurs twice at the top level, or when a top-level
   member is equal to `swarma` or `nostr` under Unicode simple case folding
   and is not that exact name. This keeps [names](../protocol/names.md) §3.1
   for the names Link reads.
3. A reader MUST skip every other top-level member without interpreting its
   content. Such a member MUST NOT cause refusal, whatever its JSON type. The
   fold-conflict rule of names §3.1 no longer applies between two members
   that Link does not read.
4. A reader MUST take the value of `swarma` as the exact byte span it
   occupies in the name value and parse that span under section 3.
5. A value without `swarma` carries no Link authority. A Link check that
   needs the binding refuses; the name stays valid for its other uses.

Rule 2 is what makes rule 3 safe. Two readers that differ in how they treat
duplicate members still extract the same `swarma` bytes, because a value with
a second `swarma` is refused before anything is read.

### 3. `swarma` stays strict

`swarma` is a JSON object with exactly one member: `landlord`, `agent` or,
under the amendment of section 9, `notary`:

| Name | Value of `swarma` | Meaning |
| --- | --- | --- |
| Landlord name | `{"landlord":{"grant":"<grant key>"}}` | The key that signs grants issued under this name. |
| Agent name | `{"agent":{"landlord":"<landlord name>"}}` | The landlord name whose grant key issues grants for this agent. |
| Notary name (section 9) | `{"notary":{"attest":"<attestation key>"}}` | The key that signs this notary's attestations. |

A key is a valid secp256k1 x-only public key written as 64 lowercase
hexadecimal characters. Inside `swarma` a reader MUST refuse a missing,
additional, duplicate, reordered, `null` or empty member, a member that is a
fold alias of a defined one, and any two fold-equal members. The byte span of
`swarma` MUST equal the compact encoding of the binding it parses to.

`swarma.agent.nostr` is not a member of this shape. The agent key is read
under section 5.

### 4. `nostr`: two forms, one key

A reader derives at most one key from `nostr`, the key for the local part
`_`. In NIP-05 `_` names the identifier of the domain itself, and the draft
NIP-N1 resolves the identifier `id/<label>` to `nostr.names._` of that name.

| Form | Example | Key for `_` | Relay hints |
| --- | --- | --- | --- |
| Key string | `"nostr":"<key>"` | The string | None |
| NIP-05 object | `"nostr":{"names":{"_":"<key>"},"relays":{"<key>":["wss://relay.example/"]}}` | `names._` | The array under that key in `relays`, when present |

1. Both forms yield the same key. A reader MUST NOT treat one form as
   stronger than the other.
2. The key MUST be a valid x-only public key in 64 lowercase hexadecimal
   characters. An `npub` string, uppercase hexadecimal and a prefixed string
   are not keys.
3. In the object form a reader reads `names._` and, as hints, the entry of
   `relays` whose property is that key. It MUST NOT read other entries of
   `names`, and it MUST ignore other members of `nostr`. It MUST NOT fall
   back to another entry of `names` when `_` is absent.
4. A relay hint is an absolute `ws` or `wss` URL with a host name. A reader
   drops a hint that fails this test and keeps the key. Reading the value
   contacts no relay.
5. The result is a key or no key. There is no key when `nostr` is absent,
   when it has another JSON type, when the string or `names._` is not a valid
   key, or when `names` or `_` occurs twice.
6. The result never changes how `swarma` is read. A `nostr` member that a
   reader does not understand MUST NOT cause refusal of the value.

The key has the same type as a grant key, and it is a different key by role.
It confers no authority, issues no grant and adds no scope, for a landlord
and for an agent alike.

### 5. The agent key and the landlord's social key

The agent key is the key that `nostr` yields in the agent name's value.
Messages to the agent are addressed to it. It is also the key this name
lists for the Nostr channel when LIP-0008 section 3 admits a recipient by
name.

An issuer MUST write `nostr` in an agent value. When an agent value yields no
key, a reader still reads `swarma.agent.landlord`, and the closure rules that
depend on the pointer keep working. Every step that needs the agent key
refuses. This refusal records no closure.

In a landlord value `nostr` is optional and names the landlord's social key.
The social key is independent of the grant key. A reader permits equal keys
and never requires or infers equality. The deployment keeps them apart
([key map](../KEY-MAP.md)).

An update that changes only `nostr` changes the agent's address or the social
key. Whether that update closes a grant is decided by the grant version's own
closure rules: LIP-0004 section 5 for v3 and LIP-0008 section 3 for v4. This
LIP adds no closure and removes none.

### 6. Transition from the LIP-0004 values

The shape of `swarma.agent` selects the rules. An object with `nostr` and
`landlord` is the LIP-0004 value and is read by LIP-0004 section 1,
including its equality rule and its exact bytes. An object with `landlord`
alone is read by this LIP. A landlord value has the same `swarma` in both.

A reader MAY support both during the transition and MUST NOT mix them: a
LIP-0004 agent value with a key string in `nostr`, or with owner members, is
refused as before.

Readers built before this LIP refuse an agent value without
`swarma.agent.nostr` and any value with owner members. Every consumer is
upgraded before a name is rewritten in the new form. This is a compatibility
requirement, not evidence that installed consumers were upgraded.

### 7. `d/` and the pair rule

The protocol rule is unchanged. A `d/` record is discovery data. It grants,
revokes, widens and gates nothing, and a grant check does not read it.

`d/<label>` and `id/<label>` are two names. Namecoin consensus treats a name
as a byte string and assigns the prefixes no meaning. The Namecoin domain
name specification reserves `d/` for domain names and calls keys with another
prefix "wholly unrelated" to it. The owner of one name has no claim on the
other.

The draft NIP-N1 sends the two spellings of an identifier to different names:

| Identifier a Nostr client shows | Name it resolves | Member it reads |
| --- | --- | --- |
| `id/alice` | `id/alice` | `nostr.names._` |
| `alice.bit`, `_@alice.bit` | `d/alice` | `nostr.names._` |
| `cedar@alice.bit` | `d/alice` | `nostr.names.cedar` |

A party that registers `d/alice` while another party owns `id/alice` has
these powers and limits:

| The holder of `d/alice` can | The holder of `d/alice` cannot |
| --- | --- |
| Serve the website `alice.bit` to clients that resolve `.bit` | Change the value of `id/alice` |
| Bind `alice.bit` and `<user>@alice.bit` to keys of its choice in Nostr clients | Issue, widen or revoke a grant under `id/alice` |
| Receive messages that a user addresses to `alice.bit` | Pass a Link check, which reads the pinned `id/` names |

Neither Nostr nor Namecoin is at fault here. Each follows its own rule. The
gap is at the seam: a person reads `id/alice` and `alice.bit` as one
identity, and the chain holds two unrelated names.

**Deployment rule.** For every `id/<label>` it registers, a deployment
registers `d/<label>` in the same operation, owned by the same cold key, and
renews both. The rule applies when `d/<label>` is a valid domain name under
ifa-0001: `<label>` is at most 63 characters long, matches
`^(xn--)?[a-z0-9]+(-[a-z0-9]+)*$` and is not wholly numeric. An `id/` label
outside that set has no `d/` counterpart and nothing to pair:

| `id/` name | `d/` counterpart | Reason |
| --- | --- | --- |
| `id/alice-cedar` | `d/alice-cedar` | Matches the grammar. |
| `id/123four` | `d/123four` | Begins with a digit and is not wholly numeric. |
| `id/xn--bcher-kva` | `d/xn--bcher-kva` | The `xn--` prefix of an internationalized name is permitted. |
| `id/123` | None | Wholly numeric names are not permitted in `d/`. |
| `id/alice_cedar`, `id/alice.cedar` | None | An underscore and a dot are outside the grammar. |

The rule costs a second name: 0.01 NMC locked in the name output, the
registration fees, and one more renewal per period. It is a deployment rule.
A verifier does not check it, and a missing `d/` name does not weaken a
grant.

### 8. Size

The complete value MUST fit 520 bytes with every member counted, including
the owner's. An issuer MUST measure the value before publishing it. The
sizes below are the compact encodings with 64-character keys, the landlord
pointer `id/example`, the relay URLs `wss://relay.example/` and
`wss://relay2.example/`, and the owner members `"email":"cedar@example.org"`
and `"name":"Cedar"`:

| Value | Bytes | Left of 520 |
| --- | ---: | ---: |
| Landlord, no `nostr` | 100 | 420 |
| Landlord, key string | 175 | 345 |
| Landlord, NIP-05 object | 191 | 329 |
| Landlord, NIP-05 object and one relay | 294 | 226 |
| Landlord, NIP-05 object and two relays | 318 | 202 |
| Agent in the LIP-0004 form, for comparison | 212 | 308 |
| Agent, key string | 121 | 399 |
| Agent, NIP-05 object | 137 | 383 |
| Agent, NIP-05 object and one relay | 240 | 280 |
| Agent, NIP-05 object and two relays | 264 | 256 |
| Agent, NIP-05 object, `email` and `name` members of the owner | 180 | 340 |
| Notary (section 9), no `nostr` | 99 | 421 |
| Notary, key string | 174 | 346 |
| Notary, NIP-05 object | 190 | 330 |
| `d/` record, root key only | 92 | 428 |
| `d/` record, root key and one agent label `cedar` | 167 | 353 |

Writing the agent key once shortens the agent value from 212 to 137 bytes.
One more agent in a `d/` record costs 70 bytes plus the length of its label,
so a record holds the root and five agents with labels of up to 15
characters. The typed service declaration of LIP-0007 is not counted here and
needs its own budget inside the same 520 bytes.

### 9. Notary name (Draft amendment of 2026-11-12)

A verifier of a child grant must learn a notary's key from a source that the
notary alone controls and that the parent grant can name. The parent names
the notary by `id/` name ([LIP-0014](LIP-0014-notary-certified-redelegation.md)
section 7), and that name's value carries the key in a third `swarma` shape:

```json
{"swarma":{"notary":{"attest":"<attestation key>"}}}
```

1. `notary` is an object with exactly one member, `attest`, a key under the
   rules of section 3. The strictness of section 3 applies unchanged: a
   missing, additional, duplicate, reordered, `null` or aliased member
   refuses.
2. A name has one shape. A value whose `swarma` holds `notary` together with
   `landlord` or `agent` refuses. A party that is a landlord or an agent and
   also certifies uses a separate name for the notary role.
3. The attestation key signs attestations and nothing else. It issues no
   grant, and a grant signed by it refuses. It is a different key by role
   from a grant key and from the key that `nostr` yields; a reader permits
   equal keys and never requires or infers equality.
4. `nostr` is optional in a notary value and names the key under which the
   notary can be reached. It confers no authority.
5. An update that changes `attest` changes which attestations verify:
   those signed by the old key refuse, and the notary signs them again
   under the new key. The update closes no grant: a child certified under
   the old key refuses until it is certified again, and grants that name
   the notary by name are not reissued.
6. Only the checks of LIP-0014 read this shape. A LIP-0004 reader refuses a
   notary value as an unknown shape, which is harmless: no v3 grant check
   reads a notary's name.

The list of a principal's notaries is not a member of the principal's own
value. It is signed in each parent grant (LIP-0014 section 2). A list in the
value would be read at check time and not at issuance, and a member added
to `swarma` refuses under section 3.

## Alternatives

Keeping the exact-byte comparison of the whole value gives the simplest
reader. It also makes the name unusable for anything except Link, which
contradicts D1.

Keeping the key only in `swarma.agent.nostr` makes the Link part
self-contained, and Nostr clients then cannot resolve an agent by its `id/`
name. Keeping both copies with the equality rule is the current state.

Accepting only the NIP-05 object leaves one shape to test. Names that carry
the key string, which deployed clients accept, would have no agent key.

Requiring `d/` in the protocol would make every check read a second name that
carries no authority, and a missing discovery record would then block a valid
grant. The pair rule puts the cost on registration and keeps checks
unchanged.

## Security consequences

Skipping owner members opens a parser-differential risk: two readers could
disagree on which `swarma` they read. Section 2 closes it for the two names
Link reads by refusing duplicates and fold aliases and by parsing the exact
byte span. Owner members can still be malformed in ways that matter to their
own consumers. That is outside Link.

The agent key now sits in a member that other software also writes. Only the
name's owner key can update the value, so the custody boundary is unchanged.
The operational risk is new: a Nostr tool that rewrites `nostr` changes the
agent's key. An operator updates agent names with tools that preserve
`swarma` and writes the intended key.

A `nostr` member that yields no key removes the agent's address and no
authority. It records no closure, and a later update that restores a valid
key restores the address. The pending, malformed and read-failure rules of
the grant versions are unchanged.

The social key and the relay hints carry no authority. A squatted `d/` name
misleads people and Nostr clients. It does not pass a Link check.

## Conformance impact

No normative conformance class changes. A future vector set pairs these
controls; each rejected case leaves no binding and no closure:

| Valid control | Refusal or invariant |
| --- | --- |
| Value with `swarma` and owner members of every JSON type | A second `swarma`, a fold alias of `swarma` or `nostr`, or bytes after the object refuses the value. |
| Two owner members that are fold-equal | The value is read; refusing it is wrong. |
| Strict `swarma` for a landlord and for an agent | Missing, extra, duplicate, reordered, `null` or alias member inside `swarma` refuses; owner members outside do not relax it. |
| Agent value with the key string and the same key in the NIP-05 object | Both yield the same key; preferring one form is wrong. |
| NIP-05 object with further `names` entries and unknown `nostr` members | Only `_` is read; falling back to another entry when `_` is absent is wrong. |
| Agent value whose `nostr` is absent or not understood | The pointer is read and a pointer change still closes; a step that needs the key refuses without closure. |
| Landlord value with a malformed `nostr` | The grant key is read; the value is not refused. |
| Invalid relay hint beside a valid key | The hint is dropped and the key kept; no relay is contacted. |
| LIP-0004 agent value read by a transition reader | Its equality rule holds; a key string or owner members in that form refuse. |
| Every size in section 8 recomputed from its bytes | A value of 521 bytes refuses. |
| `id/<label>` with and without a registered `d/<label>` | The grant verdict is the same in both cases. |
| Notary value with `attest` alone, with and without `nostr` (section 9) | `notary` beside `landlord` or `agent`, a second member inside `notary`, and an `attest` that is not a valid key refuse. A change of `attest` closes no grant. |
| Pairing applied to `id/alice-cedar`, `id/123four` and `id/xn--bcher-kva` | Requiring a pair for `id/123`, `id/alice_cedar` or `id/alice.cedar` is wrong: `d/` admits no such name. Excluding the `xn--` name from pairing is wrong. |

## Open questions

- Exact canonical bytes of `swarma` once the next format moves to RFC 8785,
  and whether a reader checks member order inside `swarma`.
- The date after which readers stop accepting the LIP-0004 agent value.
- A third `nostr` shape, an object with `pubkey` and a relay array, appears in
  one client's notes for `id/` names and is absent from the draft NIP-N0. It
  yields no key here. It is added if the draft adopts it.
- How the LIP-0007 service declaration shares the 520 bytes with `nostr` and
  owner members.
- Whether a transfer of `id/<label>` requires the transfer of `d/<label>` in
  the same deployment procedure.
- Whether a v4 parent pins a notary name by its registration and owner key
  (LIP-0012 open questions), and whether the notary shape needs a member for
  a second, pending key during a rotation.
- Decision record, normative adoption and public vectors.

## Sources

- [LIP-0004](LIP-0004-landlord-grants.md) section 1 and the reference notes
  [`N1-VALUES.md`](https://github.com/relux-works/swarma-chain-lab/blob/11084e3a31175907e77644a7596e7802283e7c1e/experiments/rental/N1-VALUES.md);
  [names](../protocol/names.md) §2 and §3.
- [NIP-05](https://github.com/nostr-protocol/nips/blob/999f9bfbf5fe00d5c2711fd24badb4e56748c9bc/05.md),
  read 2026-11-10: `names` maps local parts to lowercase hexadecimal keys,
  `relays` maps a key to relay URLs, and `_` is the identifier of the domain
  itself.
- Draft NIPs of the Namecoin track at commit
  `b451c82803f314f6f84065d7123dcab2b5fd8976`, read 2026-11-10:
  [NIP-N0](https://github.com/mstrofnone/nips/blob/b451c82803f314f6f84065d7123dcab2b5fd8976/N0.md),
  the `nostr` item in a Namecoin value, and
  [NIP-N1](https://github.com/mstrofnone/nips/blob/b451c82803f314f6f84065d7123dcab2b5fd8976/N1.md),
  the identifier forms and the names they resolve. Both are drafts outside
  the Nostr NIP repository.
- The key-string form: the design note of a Nostr client at commit
  `4fb29192d502542f714e1526ac229378617922fe`,
  [`namecoin-nip05-design.md`](https://github.com/vitorpamplona/amethyst/blob/4fb29192d502542f714e1526ac229378617922fe/docs/namecoin-nip05-design.md),
  read 2026-11-10.
- Namecoin domain names:
  [ifa-0001](https://github.com/namecoin/proposals/blob/1b0043a98fe8f4cf1a85ec92fdbe98d38b5886b3/ifa-0001.md),
  the `d/` namespace and its relation to other prefixes.
