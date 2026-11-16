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

Ivan Oparin decided on 2026-11-15 that a landlord lists, in its own name value,
the owner keys of the names of its agents and stations (J11). Version 0.1.51
put it in force as a member `holders` of the landlord binding: on 2026-11-16
Ivan Oparin put it in force without waiting for the co-author's agreement,
which has not been given, and the co-author's answer is folded in by
amendment. An owner decision of the same day has the holders follow the
method of the device list: the landlord's name value pins the hash and the
version of a holders list in a member outside `swarma`, `swarma-holders`; the
list lives off the value without the cap of five; a change of it ends no v4
grant; and the list has one entry for each agent or station name, with the
key that holds the name and a seal whose spend revokes that one name. Section
10 states this, in force since version 0.1.53 on the same terms, and keeps the
member of version 0.1.51 as the inline form for the transition (section
10.9). Section 3 is read with section 10.9 for a landlord binding in the
inline form.

Ivan Oparin accepted on 2026-11-15 a third member that Link reads, outside
`swarma`: `swarma-devices`, the hash and the version of an owner's device list
([LIP-0029](LIP-0029-owner-control.md) section 3.3). The text was written
optimistically, and the co-author's agreement is pending. The member gives no
grant authority; only the owner's own executors and key holders read it, and a
duplicate or fold alias of it refuses the whole value as for `swarma` and
`nostr`. Until the co-author agrees, sections 1 and 2 stand: a reader skips the
member as one of the owner's.

Section 11 holds Draft text, under a decision of 2026-11-16 that awaits the
co-author's agreement, for one mechanism for every statement set of an owner:
the head of the set in the owner's name value, read from the confirmed active
chain only. `swarma-devices` is its first instance; under section 11 a defect
of a head member refuses that set only, and no longer the whole value.

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

Since version 0.1.53 the holders of a landlord (J11) are no member of the
landlord binding: the landlord's value pins a holders list in the top-level
member `swarma-holders`, outside `swarma` (section 10). The binding of a
landlord is `{"landlord":{"grant":"<grant key>"}}` as the table has it.
Version 0.1.51 gave the binding a second member, `holders`; a reader still
admits that member, for the transition, as section 10.9 says, and refuses
every other additional member.

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

The cost of breaking it is concrete for Grant v3. A LIP-0004 reader that
meets one owner member in a landlord value cannot read the grant key, and
every v3 grant under that name refuses at that verifier until the value is
restored; the refusal records no closure. The [key map](../KEY-MAP.md)
lists where each key may be published before and after the upgrade.

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

**Note, not normative.** Recorded on 2026-11-13 at Ivan Oparin's direction.
The pair of `id/<label>` and `d/<label>` is a convention outside Namecoin
consensus: consensus gives a prefix no meaning and relates no two names. The
convention misleads. A person reads `id/<label>` and `<label>.bit` as one
identity, while the chain holds two unrelated names, and the pair lasts only
as long as one owner registers and renews both. An additional naming
convention with a single level of registration is therefore under
consideration, and the authors' own parsers would handle only that level.
This note defines nothing of that convention and changes no rule: the
protocol rule and the deployment rule of this section stand.

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

**Budget plan (proposal, not decided; deciders: the specification's
authors).** A landlord value with a NIP-05 object and one relay takes 294
bytes and leaves 226. The plan keeps it that way:

1. A name carries only the keys that some reader must resolve on chain: the
   grant key or the notary key in `swarma`, and the Nostr key in `nostr`.
2. Every other key or binding is a signed statement in the certificate store
   of [LIP-0016](LIP-0016-certificate-store.md), anchored by LIP-0005
   frames: messaging device keys, commit-signing keys, release keys and
   organization membership.
3. A further key enters a name only when a verifier must resolve it on
   chain, and then with a shape of its own in this LIP.
4. About 150 bytes stay reserved for the service declaration of LIP-0007.

### 9. Notary name (Draft amendment of 2026-11-12)

A verifier of a child grant must learn a notary's key from a source that the
notary alone controls and that the parent grant can name. The parent names the
notary by `id/` name and binds the registration and the owner key of that name
([LIP-0014](LIP-0014-notary-certified-redelegation.md) sections 7 and 7.1; Ivan
Oparin accepted the binding on 2026-11-13, and the co-author agreed on
2026-11-15). The value of that name carries the key in a third `swarma` shape:

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

### 10. Holders of a landlord: the hash-pinned holders list (amendment of 2026-11-16, in force since 0.1.53)

**In force since version 0.1.53.** An owner decision of 2026-11-15 has a
landlord list, in its own name value, the owner keys of the names of its
agents and stations (J11), and version 0.1.51 put the member `holders` of the
landlord binding in force. An owner decision of 2026-11-16 replaces that
member. Five holders for a landlord name are too few, and the holders follow
the method of the device list of [LIP-0029](LIP-0029-owner-control.md): the
landlord name pins a hash and a version, and the list itself lives off the
value. A change of the list does not end the v4 grants that the landlord
issued. The landlord revokes one agent, not one key: the list has one entry
for each agent or station name, and each entry carries a seal whose spend
revokes that one name with no name update and no new list. The text was
ordered written as text in force, without waiting for the co-author's
agreement, which has not been given; the co-author's answer is folded in by
amendment.

This section replaces the member `holders` of version 0.1.51. Section 10.9
keeps that member, as the inline form, for the transition only.

A verifier that admits a recipient because of whose agent it is must learn that
from the chain. An agent's name says which landlord it points to, and anybody
can register a name that points to any landlord. The landlord therefore says
which names are its agents and stations, and which key holds each. It says so
in a list that its name value pins by hash:

```json
{"swarma":{"landlord":{"grant":"<grant key>"}},"swarma-holders":{"seq":<seq>,"sha256":"<h(H)>"}}
```

A holders list is `H`, its version `seq`, and its hash `h(H)`. The landlord is
`L`, with the name `id/acme`. An entry of the list names one agent or station
name, the key that holds it, and a seal. The **holder** of an entry is that
key, as in version 0.1.51; what is listed, and what a seal revokes, is the
name.

**What is decided and what is this text's choice.** The decision gives the
method (a hash and a version in the name, the list off the value, modelled on
LIP-0029 sections 3.1 to 3.3), that no cap of five remains, that a change of
the list ends no v4 grant, that an entry is one name with its own seal on the
model of LIP-0029 section 8, that entries may be listed ahead and kept in
reserve, and the distribution of the list as LIP-0029 section 3.5 has it.
Every rule below names its source in the last column. A rule or a part of a
rule that neither the decision nor a cited text gives is marked **NEW**: it
is this text's choice, it stands in force with the rest under the order
above, and the owners decide it. The whole of the entry by name, of the seal
of an entry and of the reserve is new in this specification, and the rows
that state them are marked so with the rule they are modelled on. The
refusal codes of this section are proposals, like the codes of a class
([LIP-0026](LIP-0026-rows-and-accounts.md) section 9).

#### 10.1. The holder entry

A holder entry is one JSON object under the encoding rules of LIP-0013
section 2.1, with exactly these members in this order:

| # | Member | Rule | Source |
| --- | --- | --- | --- |
| 1 | `name` | The exact name of one agent or station of the landlord: `id/` followed by 1 to 252 bytes of `a-z`, `0-9`, `-`, `_` and `.`, the v3 name syntax of LIP-0013 section 2.1. | **NEW**: the decision makes the entry one per name; the syntax is that of LIP-0013 section 2.1 |
| 2 | `key` | The owner pin of that name, in the form of [LIP-0021](LIP-0021-name-ownership-and-history.md) O2.1: a compressed secp256k1 public key, written as 66 lowercase hexadecimal characters that begin with `02` or `03`, whose other 64 characters are the x coordinate of a point of the curve. | **NEW** as a member of an entry by name (H34). The pin is that of the member `holders` of version 0.1.51 (section 10.9, rule 2); the member name is that of the device record, LIP-0029 section 3.1 |
| 3 | `seal` | `{"txid":…,"vout":…}`, the outpoint of the entry's revocation seal: 64 lowercase hex in display byte order and a canonical non-negative integer, at most 4294967295. | LIP-0029 section 3.1, member `seal`, word for word. The bound of `vout` is **NEW**; it is the largest output index of a transaction |

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H1 | An entry has the three members `name`, `key` and `seal` and no other. It has no label, no algorithm, no presence flag and no ceiling: a holder signs nothing for the landlord, so the members of a device record that describe a signer have no subject. | `HOLDER_LIST_INVALID` | **NEW**; the record of LIP-0029 section 3.1, less what describes a signer, with the name |
| H2 | No two entries of one list have the same `name`, and no two have the same `seal`. Two entries may have the same `key`: one key may hold several names, and each of them has its own entry and its own seal. | `HOLDER_LIST_INVALID` | LIP-0029 O3.3 for `seal`. Uniqueness by `name` and not by `key` is **NEW** |
| H3 | A holder is a key that owns names of the landlord's agents and stations: the output of such a name pays the key hash or the witness key hash of the pin (LIP-0021 O3.3). It is a name-owner key of the key registry, and it is a different key by role from the grant key, from the key that owns the landlord name and from every key that `nostr` yields. A reader permits equal keys and never requires or infers equality. The key that owns the landlord name is a holder only where an entry names it. | | Rule 5 of version 0.1.51, unchanged |
| H4 | An entry confers no authority, and neither does its holder. It issues no grant and signs no request. Only the checks of a landlord class read the list ([LIP-0026](LIP-0026-rows-and-accounts.md) sections 9 and 10), and they read it at each admission (section 10.6). | | Rule 6 of version 0.1.51, unchanged |
| H34 | **The entry carries the owner pin.** An entry admits its name only while the current output of that name reads as controlled by the entry's `key` (LIP-0021 O3.4), and only a value that this key wrote (section 10.6, steps 7 and 9). A listed name whose current owner is another key does not pass, whoever that key is and whatever the value says; a key that holds a name which no entry lists passes nothing with it. When the owner of a listed name changes, the entry stops admitting from the block of the transfer, with no closure; the landlord accepts the new owner only by a new list whose entry for the name carries the new pin (H36), and the new owner then writes the value itself. | `CLASS_HOLDER`, `CLASS_WRITER` | **NEW**: the strong form of the decision's default, an entry of name, owner pin and seal. The form without the pin is not taken: a listed name would then pass for whoever came to hold it, and a name listed before it is registered would pass for whoever registered it first |
| H37 | **Reserve entries.** A landlord may list names ahead of their use and keep them in reserve: an entry is valid whether or not its name is registered, points to the landlord or has ever been presented. A reserve entry admits nothing until the name is live, its value is an agent binding that points to `L`, the entry's `key` holds it and that key wrote the value (LIP-0026 R9.4 to R9.7); from that block it admits, with no update of the landlord's name and no new list. A reserve entry costs its seal, with the prepared spend of H26 and H27, and its octets in the list within H6; it costs no byte of the name value and no name update beyond the one that pins the list that holds it. A reserve entry is revoked like any other, by the spend of its seal. The holder key SHOULD register a reserve name before the list that names it is published, because the list makes the name public, and a name that another party registers first never passes steps 7 and 9 of section 10.6 for it. | | **NEW**; the decision allows listing ahead. That registration comes first is this text's advice, and LIP-0026 check (d) is what keeps a name that was registered by another party from passing |

#### 10.2. The holders list

A holders list is one JSON object under the encoding rules of LIP-0013 section
2.1, at most 262144 bytes, with exactly these members in this order:

| # | Member | Rule | Source |
| --- | --- | --- | --- |
| 1 | `schema` | `swarma-holders-list/1` | **NEW**; the form of `swarma-device-list/1`, LIP-0029 section 3.2 |
| 2 | `network` | `main` or `regtest` | LIP-0029 section 3.2 |
| 3 | `owner` | the landlord's `id/` name | LIP-0029 section 3.2; section 11, SH4 |
| 4 | `seq` | the version: a canonical positive integer, at most 9007199254740991 | LIP-0029 section 3.2 |
| 5 | `holders` | an array of 0 to 1024 holder entries, sorted ascending by the bytes of `name` | The array and its order follow LIP-0029 section 3.2; that the sort member is `name` is **NEW**. The bounds: H6 |

`h(H)` is the SHA-256 of the exact octets of `H`, in 64 lowercase hex. A
reader MUST refuse a list unless re-encoding the parsed value gives the
identical octets (LIP-0029 section 3.2). The list has no expiry and holds
nothing but the entries (the same section).

`holders` is sorted by the bytes of `name`: the order of the `name` strings
as ASCII, a shorter string first where one is a prefix of the other. The
encoding rules of LIP-0013 section 2.1 apply as they do to a device list:
compact UTF-8, no whitespace outside strings, no trailing newline, canonical
decimal integers, printable ASCII in every string, and no escape other than
`\"` and `\\`.

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H5 | A list that is no JSON object of exactly the five members in their order, that is not in the encoding of LIP-0013 section 2.1, whose re-encoding differs from its octets, whose `schema` is another string, whose entries are not sorted or break H1 or H2, or that holds a `name` outside the syntax of section 10.1 or a `key` that is no owner pin, is no list. | `HOLDER_LIST_INVALID` | LIP-0029 section 3.2 and `DEVICE_LIST_INVALID`; the refusals of rule 3 of section 10.9 |
| H6 | A list holds at most 1024 entries and at most 262144 bytes. A list above either bound is no list, and a reader MAY stop reading at the bound. The cap of five holders of version 0.1.51 does not apply to a list: it followed from the 520 bytes of a name value (section 10.9, rule 8), and the list is outside the value. | `HOLDER_LIST_INVALID` | **NEW**. LIP-0029 section 3.2 bounds a device list at 16 records and 4096 bytes; those numbers are not taken, because 16 is the order of the cap that the decision removes and an entry is now one for each name. An entry with a name of 16 bytes takes 194 bytes, so 1024 such entries take about 200000 bytes; with the longest names the byte bound is reached first |
| H7 | A list with an empty `holders` is valid and says that the landlord lists no name. A landlord value without the pin of section 10.3 says the same. No name passes check (c) or (d) of a class against such a landlord. | `CLASS_HOLDER` (LIP-0026 section 9) | Rule 4 of version 0.1.51. LIP-0029 section 3.2 asks at least one record of a device list; that floor is not taken |

An example with three entries, with line breaks for display only; the real
bytes contain none. Two names are held by one key, and the third, held by
another, is a reserve. The keys are multiples of the generator of secp256k1
and belong to nobody, and the seals are placeholders, so it is an
illustration and no landlord may use it:

```json
{"schema":"swarma-holders-list/1","network":"main","owner":"id/acme","seq":3,"holders":[
{"name":"id/acme-reserve-01","key":"022f8bde4d1a07209355b4a7250a5c5128e88b84bddc619ab7cba8d569b240efe4","seal":{"txid":"b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2","vout":0}},
{"name":"id/acme-worker-7","key":"022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01","seal":{"txid":"b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2","vout":1}},
{"name":"id/acme-worker-8","key":"022f01e5e15cca351daff3843fb70f3c2f0a1bdd05e5af888a67784ef3e10a2a01","seal":{"txid":"b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2b2","vout":2}}]}
```

Without the line breaks it is 676 bytes, and `h(H)` is
`6d7c3e11094aac51cff6901471be500d7689f7d5830794efe57381a29cef7a35`. The name
value then carries
`"swarma-holders":{"seq":3,"sha256":"6d7c3e11094aac51cff6901471be500d7689f7d5830794efe57381a29cef7a35"}`.
The length and the hash were computed by one implementation and by no second
one; section 10.11 says what a vector set fixes.

#### 10.3. The pin in the landlord's name value

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H8 | The landlord's name value pins the hash of the holders list only, with its version, in the top-level member `swarma-holders`, outside `swarma`: `{"seq":<seq>,"sha256":"<h(H)>"}`, exactly these two members in this order, compact. `seq` is a canonical positive integer, at most 9007199254740991, and `sha256` is 64 lowercase hex. Nothing else of the list enters the name. | `HOLDER_PIN_INVALID` | LIP-0029 O3.4; section 11, SH1. The member name is **NEW**, in the form of `swarma-devices` |
| H9 | A reader MUST match `swarma-holders` by exact name. A duplicate of it, or a member equal to it under Unicode simple case folding that is not that exact name, gives no holders list, and so no listed name. It leaves `swarma`, `nostr`, every other member and every grant as they read. A member of another shape than H8 gives no holders list in the same way. | `HOLDER_PIN_INVALID` | Section 11, SH6. LIP-0029 O3.5, which refuses the whole value, is not taken: a defect of the pin would then refuse every grant of the landlord, against H13 |
| H10 | The pinned `seq` equals the `seq` of the list, and `sha256` equals `h(H)`. The `owner` of the list is, octet for octet, the landlord name whose value pins it, and its `network` is the network of the reader's pinned chain. | `HOLDER_LIST_MISMATCH` | LIP-0029 O3.6; section 11, SH4 |
| H11 | A reader takes the pin only from the landlord's name output that is confirmed in the active chain of its own node. A pending name operation gives no pin: it neither adds, replaces nor removes one until it confirms. | | Section 11, SH3; LIP-0029 O9.2. A class check refuses while such an operation is pending (LIP-0026 R9.5, sixth step) |
| H12 | `swarma-holders` gives no grant authority, and section 1 holds as written: authority comes from `swarma` alone. The member is a further one that Link reads, beside `swarma`, `nostr` and the heads of section 11. Unlike `swarma-devices`, which only an owner's own executors read, every verifier that makes the checks of a landlord class reads it, an executor of another owner included. | | LIP-0029 O3.7, with the difference stated; rule 6 of version 0.1.51 |

The member is registered as a head of a statement set in section 11 (SH2),
whose Draft text awaits the co-author's agreement. Rules H8 to H11 state for
this member what SH1, SH3, SH4 and SH6 state for every head, so that the pin
does not depend on the status of section 11.

The member adds 103 bytes while `seq` has one digit, 118 bytes at the largest
`seq`: the same as `swarma-devices`, whose name has the same length. The
sizes count as in section 8:

| Landlord value | Bytes without | With `swarma-holders`, `seq` < 10 | Left of 520 | With `swarma-devices` as well | Left of 520 |
| --- | ---: | ---: | ---: | ---: | ---: |
| No `nostr` | 100 | 203 | 317 | 306 | 214 |
| Key string | 175 | 278 | 242 | 381 | 139 |
| NIP-05 object | 191 | 294 | 226 | 397 | 123 |
| NIP-05 object and one relay | 294 | 397 | 123 | 500 | 20 |
| NIP-05 object and two relays | 318 | 421 | 99 | 524 | does not fit |

The cost of the list to the name value is the same for one entry and for
1024. A landlord value with a NIP-05 object, one relay and the three heads
`swarma-holders`, `swarma-devices` and `swarma-certs` takes 601 bytes and
does not fit; the single member over every set, which section 11 leaves open,
is the way out, and it is open with it.

#### 10.4. What a grant's liveness depends on (replaces rule 7 of version 0.1.51)

Rule 7 of version 0.1.51 said that `holders` is part of the `swarma` member,
so that an update which adds or removes a holder refuses every v4 grant that
the landlord issued before it (LIP-0008 section 3) and, under LIP-0008 section
5.2, closes them. For a landlord in the pinned form that rule is replaced by
H13:

| Rule | Requirement | Source |
| --- | --- | --- |
| H13 | The holders of a landlord are no part of its `swarma` member. The pin `swarma-holders` is a top-level member outside `swarma`, and the list is outside the value. A name update of the landlord that adds, replaces or removes `swarma-holders`, and that changes neither the owner of the name nor the octets of `swarma`, ends no v4 grant, refuses none, and is no break under LIP-0008 section 5.2 (J6.1): a verifier records no closure for it, and the landlord issues nothing again. The spend of a holder seal (section 10.7) is no operation of the landlord name and touches no grant. A v4 grant that the landlord issued depends, in the landlord's name, on exactly the facts that LIP-0008 section 3 binds: the name; its registration; the owner key that controls every output of the name from the one current at the grant's committed recent block to the current one; and the exact octets of the `swarma` member on each of those outputs, which for a landlord in the pinned form are the compact encoding of `{"landlord":{"grant":"<grant key>"}}`, with the grant key equal to the grant's issuer key, and nothing else. No octet of `swarma-holders`, of a holders list or of a holder seal is among them. Beside the name the grant depends, as before, on its own seal and its own window. | LIP-0029 O3.8 and decision 3; section 11, SH7; LIP-0008 section 3, unchanged |
| H14 | H13 changes nothing in LIP-0008. The rule that a grant lives while the owner and `swarma` do not change stands as written; what changes is that `swarma` no longer holds the holders. A change of the grant key or of the owner still ends every v4 grant of the landlord. | LIP-0008 section 3 |
| H15 | Every change of the list is a name update of the landlord, signed by the name-owner key, that writes a pin with a higher `seq`. While it is pending, a class check that reads this landlord refuses without closure (LIP-0026 R9.5, sixth step), and a v3 verifier refuses the grants of the name, without closure, until the update confirms (LIP-0004 section 5). Whether a pending update of `swarma-holders` alone suspends the admission of the landlord's own v4 grants is a question of the observation profile, as it is for `swarma-devices` (LIP-0029 section 3.4). | LIP-0029 O3.10 and O9.1 |
| H36 | **Adding entries.** Adding a name, a reserve included, or changing the owner pin of a listed name needs a new list that holds the entry, the entry's seal with its prepared spend placed under H27, and an update of the landlord's name, signed by the name-owner key, that writes `swarma-holders` with a higher `seq`. A presentation, an attachment or a message never adds an entry. That update ends no v4 grant (H13). Adding is slow and guarded; revoking one name is fast. | LIP-0029 O9.1 to O9.3 and decision 6; **NEW** as a rule for entries by name |
| H16 | A landlord MUST NOT write `swarma-holders` into a name before every verifier of that name runs a reader of this LIP. A LIP-0004 reader refuses the whole value, and every v3 grant under that name then refuses at that verifier, without closure, until the exact value is restored (section 6). A reader of this LIP before this amendment skips the member as one of the owner's and finds no holder, so it refuses every recipient of a class of that landlord and admits none wrongly. | LIP-0029 O3.9; section 2, rule 3 |

A grant to an agent is a different matter from the landlord's own grants, and
H13 does not speak of it. A child of a class row is admitted through the
checks of the class at each admission, and those checks read the list and the
seals (section 10.6). A change of the list or a spent seal therefore decides
whether such a child is admitted from then on; it does not end the child, and
it does not end its parent.

#### 10.5. Distribution of the holders list

The list reaches its readers as LIP-0029 section 3.5 has it for a device
list. The reader of a holders list is the verifier of a class check, and the
party that has the list to give is the one that presents the child.

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H17 | The name pins the hash and nothing else (H8). The list is addressed by its content: every copy whose exact octets hash to the pinned `sha256` is the list, whoever serves it, and no other copy is. | `HOLDER_LIST_MISMATCH` | LIP-0029 O3.11 |
| H18 | The primary path is the presentation. The party that presents a child of a row whose recipient is a class, or a request under such a child, supplies the exact octets of the list that the landlord's value pins: when the list has changed since the last presentation that this verifier admitted from it, and at first contact, which is every presentation to a verifier of which the presenter holds no record that it admitted one under this `h(H)`. Otherwise the presentation carries nothing of the list. A verifier caches every list that it verified under H10 and H17, keyed by the landlord name and `h(H)`, and makes a later check from the cache. The member that carries the octets comes with the octets of a v4 request ([LIP-0020](LIP-0020-grant-v4-wire-registry.md)); until then the list travels beside the presentation. | | LIP-0029 O3.12. That the presenter stands in the sender's place is **NEW** |
| H19 | Two secondary paths serve a reader that has no presenter to ask, such as the signer of an issuer under LIP-0026 R9.12 or a verifier that starts with an empty cache. (a) The landlord's domain: `https://<domain>/.well-known/swarma/holders-list/<h(H)>`, where `<domain>` is the domain of the NIP-05 identifier in the landlord's name value, and the body of the response is the exact octets of the list. (b) A parameterized replaceable Nostr event signed by the key that the landlord's name value yields for the Nostr channel, with the tag `["d","swarma-holders-list"]`, whose `content` is the exact octets of the current list. Both places are named by the landlord's name value, and a reader fetches from no other: not from a URL in a request, not from a relay's or a peer's hint. A copy from either counts only under H17. | | LIP-0029 O3.13. The path segment and the `d` tag value are **NEW**, in the form of those of the device list; the kind of the event is open as it is there |
| H20 | A verifier that holds no list with the pinned hash refuses by name, and the presenter presents again with the list. The refusal is never replaced by a silent fetch. The refusal is no evidence about the landlord, the recipient or any holder, and it records no closure. The unavailability of a secondary path never blocks a presentation that carries the list. | `LIST_UNKNOWN` | LIP-0029 O3.14 and decision 17, with its code |

No path adds an entry. The pin comes from the landlord's name on the reader's
own node (H11), and a copy only supplies octets that hash to it. An agent
learns the current list from its landlord; how the landlord hands it over is
the deployment's.

#### 10.6. The verifier's read and the freshness rule

Check (c) of a landlord class asks whether the recipient name is held by a
holder of `L`, and check (d) whether a holder of `L` wrote the value of its
current output (LIP-0026 R9.6 and R9.7). For a landlord in the pinned form
both are asked of one entry, the entry of the recipient name, and a verifier
answers them from these steps, in this order, at every admission:

| # | Step | Refusal | Source |
| --- | --- | --- | --- |
| 1 | Read the current confirmed value of `L` on the verifier's own node, in the observation of the admission (LIP-0022 B1.5): the output that check (b) judged. Decide its form under section 10.9. A value with neither form lists no name | `CLASS_HOLDER` | LIP-0026 R9.6 and R9.10; H7, H11 |
| 2 | The member `swarma-holders` is valid under H8 and H9 | `HOLDER_PIN_INVALID` | LIP-0029 section 11, step 4 |
| 3 | The pinned `seq` is not lower than the highest that the verifier journaled for `L` (H23) | `HOLDER_LIST_ROLLBACK` | LIP-0029 O9.2 and section 11, step 4, as section 11 SH5 narrows them |
| 4 | The verifier holds octets under the pinned hash, from its cache or from the presentation | `LIST_UNKNOWN` (H20) | LIP-0029 section 11, step 5 |
| 5 | Those octets hash to the pin, are a list under H5 and H6, and meet H10 | `HOLDER_LIST_MISMATCH`, `HOLDER_LIST_INVALID` | The same; LIP-0029 O5.3 |
| 6 | The list has an entry whose `name` is, octet for octet, the recipient name | `CLASS_HOLDER` | **NEW** (the entry by name); LIP-0029 section 11, step 6, "one record" |
| 7 | Check (c): the current output of the recipient name reads as controlled (LIP-0021 O3.4) by the `key` of that entry | `CLASS_HOLDER` | LIP-0026 R9.6; H34 |
| 8 | No closure of that entry is journaled, and the verifier's own node, with its mempool included, shows the entry's `seal` as an unspent output (section 10.7) | `HOLDER_REVOKED` | LIP-0029 O8.9 and section 11, step 8 |
| 9 | Check (d): the value of the current output of the recipient name was written by the `key` of that entry (LIP-0021 section 4) | `CLASS_WRITER` | LIP-0026 R9.7. That the writer is the key of the same entry, and no other holder of the landlord, is **NEW** (H34) |

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H21 | **What a verifier reads.** For every admission it reads, on its own node and in one observation: the confirmed value of `L` and with it the pin; and for the entry of the recipient name, the state of its seal with the mempool included. It reads the list from its cache or from the presentation. It takes nothing of this from the presenter except octets that hash to the pin. It reads the seal of no other entry for the admission. | | LIP-0026 R9.10; LIP-0029 O8.9 |
| H22 | **How old a list may be.** A list has no expiry, and its age is no input. The one list that counts at an admission is the list whose hash and `seq` the landlord's confirmed value pins at the tip of that admission's observation. A list that an earlier value pinned, however recent, is no input, whether the verifier holds the current one or not. The freshness of the check is therefore the freshness of the observation: the cutoffs of LIP-0022 section 3 for the age of the tip apply to the class check as to every read of the admission, and this section adds no clock of its own. A cached list is valid for exactly as long as the pin that names it is the confirmed pin. | | LIP-0029 section 3.2 (no expiry), O3.12 (the cache), O9.2 (the pin from the name); LIP-0022 B1.5 and B3.6. That no further age bound is added is **NEW** |
| H23 | **Rollback.** A verifier journals, outside the agents' write authority, for each landlord whose list it took: the highest `seq`, the txid of the name operation that carried that pin, and every closure of section 10.7. While that operation stays in the active chain, a pin with a lower `seq` that a later name operation carries gives no list. When a reorganisation removes that operation, the verifier takes the last pin confirmed in the active chain, whatever its `seq`, and journals it in place of the removed one; every journaled closure stays. | `HOLDER_LIST_ROLLBACK` | Section 11, SH5; LIP-0029 O9.2 |
| H24 | **What a verifier refuses when it cannot get the pinned list.** It refuses the admission of that child, `LIST_UNKNOWN`, and nothing else: the parent, the landlord's own grants and every other row are judged as before. It MUST NOT fall back to a list of a lower `seq`, to a list that it cached under another hash, to the inline form of section 10.9, or to the claim of the presenter. A failed or ambiguous read of the landlord's value or of a seal refuses in the same way and proves nothing (LIP-0026 R9.8). None of these refusals records a closure, and each ends when the verifier holds the list or the read succeeds. | `LIST_UNKNOWN`; `CLASS_HISTORY_UNAVAILABLE` for a read of the node | LIP-0029 O3.14; LIP-0026 R9.8; LIP-0008 section 5.1, last paragraph |

The steps stand inside the order of LIP-0026 R9.9: steps 1 to 8 are check (c)
and step 9 is check (d), after checks (a) and (b). In the pinned form the
sentence of R9.7 that the writer need not be the holder of R9.6 has no
subject: one entry answers both. The codes `HOLDER_PIN_INVALID`,
`HOLDER_LIST_INVALID`, `HOLDER_LIST_MISMATCH`, `HOLDER_LIST_ROLLBACK` and
`HOLDER_REVOKED` are **NEW**, each in the form of the device-list code that
its source row gives; `LIST_UNKNOWN` is the code of LIP-0029 decision 17.
They are proposals, and the eight codes of a class keep their meaning.

#### 10.7. Revoking one name: the seal of an entry

Each entry carries its own seal. The spend of the seal revokes that one
name, with no name update and no new list. Other names stay, those of the
same key included. The rules follow the device seal of LIP-0029 section 8,
and all of this section is **NEW** in this specification: version 0.1.51 had
no seal of a holder, and each row names the rule of LIP-0029 that it is
modelled on.

Figure 1. The seal of a holder entry, for a name `N`.

```text
Listing a name N:

    seal S_N on a fresh k_N
              |
              v
    a pre-signed tx_revoke_N
              |
              v
    k_N destroyed
              |
              v
    the spend handed to the devices of the landlord's owner
              |
              v
    the list hash in the landlord's name by the cold key

Per admission of a class check:

    list hash and seq from the landlord's value
      + the entry of N present, its key the owner of N
      + gettxout(S_N) unspent

To revoke N:

    any device of the landlord's owner broadcasts tx_revoke_N
    a rollback cannot restore the entry
```

| Rule | Requirement | Refusal | Modelled on |
| --- | --- | --- | --- |
| H25 | Revocation of one name is the spend of the seal of its entry. | | LIP-0029 O8.1 |
| H26 | The seal `S_N` of an entry is an output that pays a fresh key `k_N`, which is neither the holder key nor any other key. Before the entry is listed, a transaction `tx_revoke_N` that spends `S_N` is signed with `k_N`, and `k_N` is then destroyed, so that no spend of `S_N` other than `tx_revoke_N` can be signed afterwards. | | LIP-0029 O8.8 |
| H27 | **Who can spend it.** Nobody holds a key of the seal. `tx_revoke_N` is held by every device of the device list of the landlord name's owner (LIP-0029 section 3), and each of them can broadcast it without the holder and without the name-owner key. A landlord whose name pins no device list keeps `tx_revoke_N` in a custody that its owner chooses. The holder of the name is not given it. The prepared spend is a bearer of revocation: whoever copies it can revoke that entry, which denies the landlord one name and gives nothing else. `tx_revoke_N` MUST reach its keepers before the list that names the entry is pinned. | | LIP-0029 O8.2, O8.10 and O9.3, and its security consequences, "a prepared spend is a bearer of revocation". That the keepers of the spend are the devices of the landlord's owner is the decision's; the custody of a landlord without a device list is this text's |
| H28 | A verifier that sees a validated transaction which spends the seal of an entry of a list that it holds, in its own mempool or in a block of its validated chain, journals the closure of that entry durably, before it admits another child through a class of that landlord. It looks at the latest at every admission, in step 8 of section 10.6, and MAY watch the seals of the lists that it holds. The closure names the landlord's name and registration, the `name`, the `key` and the `seal` of the entry, and the validated transaction. | | LIP-0029 O8.3; LIP-0008 section 5.1 |
| H29 | After a closure the verifier admits that name through no class that reads this landlord. Every other entry counts as before, an entry with the same `key` included, and the landlord's v4 grants are untouched (H13). A rollback cannot restore the entry: a list of a lower `seq` refuses (H23), every list that names the entry names the same spent seal, and a journaled closure is not lifted by a later list, a name update, eviction, replacement, non-confirmation or a reorganisation. | `HOLDER_REVOKED` | LIP-0029 O8.4 and case S29-18; LIP-0008 section 5.1 |
| H30 | A seal outpoint that was spent is never named again by an entry. An entry that names an outpoint of which the verifier holds a closure refuses, whatever `name` and `key` it carries. | `HOLDER_REVOKED` | LIP-0029 O8.5 |
| H31 | A seal that the node does not show as an unspent output, where the verifier has validated no transaction that spends it, refuses the admission and records no closure: the output may not exist yet, the read may have failed, or the spend may lie in a block whose transaction the verifier did not validate itself. The refusal lasts while the node shows the output so, and it is a verdict on the node's view and not a journaled closure. | `HOLDER_REVOKED`, without closure | LIP-0008 section 5.1, last paragraph; **NEW** in this place |
| H32 | A name update completes the revocation: a new list without the entry, with a higher `seq` (H15). Until then the entry stays in the list and refuses at every verifier whose node has seen the spend. | | LIP-0029 O8.7 |
| H33 | A name whose entry was sealed off counts again only by a new entry: a later list, with a higher `seq`, that names it with another seal, which is unspent, pinned by a name update that the name-owner key signs. The closure of H28 is the closure of the entry with its seal, and not of the name or of the key for ever. | | LIP-0029 O9.1 for the slow path. That the closure is of the entry is **NEW**: LIP-0029 O8.4 closes the device, and O3.20 has a device return with a new key |
| H35 | **A stolen holder key.** The landlord answers the theft of a key by the spend of the seal of every entry whose `key` is that pin: one prepared spend for each such entry, each broadcast by a device of the landlord's owner. Until the last of them is seen, the names whose seals are unspent still pass with whatever value the thief writes. The spends move no name: the names stay with whoever holds the key. The landlord then registers names under another key and lists them, or uses reserve entries of another key (H37), and completes the revocation by a list without the sealed entries (H32). | | **NEW**; follows from H2 and H25. LIP-0029 O8.10 for the broadcast |

**What happens to grants.** An entry and its holder issue no grant (H4), so
the spend of a seal revokes no grant that either issued: there is none. What
the spend ends is the admission of that one name through a landlord class,
from the moment at which a verifier sees it. Three things stay as they were:

- **One agent's own grant is still ended by that grant's seal.** A grant
  that names the sealed-off agent, by key or by name, is ended early by the
  issuer's spend of that grant's own seal and by nothing of this section
  (LIP-0008 sections 3 and 5.1). A child that was admitted through a class
  refuses at its next admission, because the class check is made again
  there (H4); the child is not closed, and its own seal still ends it for
  good.
- **The landlord's v4 grants are untouched** (H13).
- **The name stays with its key holder.** The spend moves no name. Whoever
  holds the key of the entry still owns the name, rewrites its value and
  renews it. The name is no longer admitted as an agent of this landlord,
  and that is all the landlord can take from it. An effect that was admitted
  before the closure is not undone.

A landlord that wants one agent out broadcasts `tx_revoke_N` for its name:
from the moment at which a verifier's node sees the spend, in its mempool,
that name passes no class of this landlord at that verifier, and the agents
beside it are not touched. The cold name-owner key is not needed for that,
and it completes the revocation later with a list that drops the entry
(H32). A thief of a holder key owns the names that pay it and rewrites their
values, and with them the keys under which those names sign requests; H35 is
the answer.

`k_N` is a holder seal key. Its script, the amount of the seal, how the fee
of `tx_revoke_N` is set and raised and what the transaction pays are open, as
they are for a device seal (LIP-0029 section 8.3). If every copy of
`tx_revoke_N` is lost, `S_N` can no longer be spent, and only the name update
of H32 removes the entry.

#### 10.8. A removed entry and a sealed-off entry

| | Removed entry | Sealed-off entry |
| --- | --- | --- |
| The act | A name update of the landlord that pins a new list, with a higher `seq`, without the entry (H15) | The broadcast of `tx_revoke_N` (H25) |
| Who acts | The name-owner key of the landlord name, which is cold | Any device of the landlord's owner that holds the prepared spend; no key is used at that moment (H27) |
| A new list | Needed | Not needed; the entry stays in the list until H32 |
| From when | From the block that confirms the update. While the update is pending, the old list is the list, and class checks of the landlord refuse without closure (H11, H15) | From the first sight of the validated spend, in the mempool of each verifier's node (H28) |
| What a verifier records | Nothing but the highest `seq` (H23). The verdict is a property of the active chain, as the name rule of LIP-0008 section 3 is | A durable closure of the entry (H28) |
| After a reorganisation | The last pin confirmed in the active chain counts again (H23); an entry that only the removed pin dropped admits its name again | The closure stays (H29) |
| Return | A later list may name the same entry again, with the same seal, while that seal is unspent | Never for that entry; the name returns only in a new entry with a new seal (H33) |
| Refusal | `CLASS_HOLDER` | `HOLDER_REVOKED` |
| Other names of the same key | Not touched | Not touched |
| The landlord's v4 grants | Untouched (H13) | Untouched (H13) |
| The name | Stays with its key holder | Stays with its key holder |

The row "after a reorganisation" differs from section 11 SH5 for the removed
entry: SH5 keeps a record refused that a removed head dropped. A removal of
an entry is here a fact of the chain's history, and a history that a
reorganisation replaced is no longer the chain's history (LIP-0008 section 3,
rule 5). That difference is **NEW**. A landlord that must not see a name
return spends its seal.

#### 10.9. Migration, and the inline form of version 0.1.51

Version 0.1.51 wrote the holders into the landlord binding. That member is
the inline form, and it stays readable for the transition:

```json
{"swarma":{"landlord":{"grant":"<grant key>","holders":["<owner key>","<owner key>"]}}}
```

Its rules are those of version 0.1.51, unchanged, with their numbers; the
vectors of the inline form cite them as 10.1 to 10.8:

1. `landlord` is an object with the member `grant` and, after it, at most
   one further member, `holders`. The strictness of section 3 applies to
   both: a missing `grant`, an additional, duplicate, reordered, `null` or
   aliased member refuses the value. It has one exception, which rule 4
   states: an empty `holders` is valid, where section 3 refuses an empty
   member.
2. `holders` is an array of strings. Each string is an owner pin in the form
   of [LIP-0021](LIP-0021-name-ownership-and-history.md) O2.1: a compressed
   secp256k1 public key, written as 66 lowercase hexadecimal characters that
   begin with `02` or `03`, whose other 64 characters are the x coordinate
   of a point of the curve.
3. The pins of one list are different, and they stand in the ascending order
   of their characters, so that one set of holders has one encoding. A value
   whose `holders` is no array, holds an element that is no pin, repeats a
   pin or has its pins in another order refuses, as a `swarma` member that is
   not the compact encoding of its binding refuses under section 3.
4. A landlord binding without `holders` and one with an empty array are both
   valid, and they say the same: the binding lists no holder. The two are
   different octets of `swarma`, so a landlord that writes the one in the
   place of the other changes the member, with the consequence of rule 7.
5. A holder of the inline form is what H3 says.
6. The inline `holders` confers no authority, as H4 says.
7. The inline `holders` is part of the `swarma` member. A v4 grant lives
   while the updates of its issuer's name change neither the owner nor the
   `swarma` member (LIP-0008 section 3), so an update that adds, removes or
   changes the inline member refuses every v4 grant that this landlord
   issued before the update, until the landlord issues them again, and
   under LIP-0008 section 5.2 (J6, agreement pending) a verifier that
   observes such an update records a closure for those grants. Rule 7 holds
   for the inline form only; H13 replaces it for the pinned form.
8. The value fits 520 bytes (section 2). A list of `n` inline holders, with
   `n` at least 1, adds `12 + 69 n` bytes to a landlord value, and an empty
   list adds 13. A landlord value without `nostr` holds at most five inline
   holders, four with a key string or a NIP-05 object, three with one relay
   and two with two relays.

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| M1 | **The form of a landlord value.** A value whose `landlord` has the member `holders` and that has no top-level `swarma-holders` is in the inline form. A value whose `landlord` has `grant` alone is in the pinned form: its listed names are the entries of the list that `swarma-holders` pins, and none where the member is absent. | | **NEW**; the shape selects the rules, as in section 6 |
| M2 | A value that has both the inline member and a top-level `swarma-holders` has no holder by either form. Its `swarma` still parses under rule 1, and its grants read as before. | `CLASS_HOLDER` | **NEW**; "MUST NOT mix", section 6 |
| M3 | **What a verifier does with each form meanwhile.** A reader of this LIP MUST parse both forms, so that a landlord value in the inline form keeps its grant key and its grants. For a class check against a landlord in the inline form it takes the holders from the inline member under rules 1 to 4 and makes checks (c) and (d) on them as version 0.1.51 did: every name that an inline holder holds passes check (c), and a value that any inline holder wrote passes check (d). Steps 2 to 6 and 8 of section 10.6 have no subject there. An inline holder is a key and has no seal: it is removed only by a name update, with the consequence of rule 7, and one name of it cannot be revoked alone. For a landlord in the pinned form the verifier follows section 10.6. | The codes of LIP-0026 section 9 | **NEW** |
| M4 | **What a landlord does.** From this version a landlord MUST NOT write the inline member into a value that did not carry it, and MUST NOT add a pin to an inline list. It moves to the pinned form by one name update that removes `holders` from `landlord` and writes `swarma-holders` with the pin of a list that holds one entry for each agent and station name that it means to keep, each with the key that holds the name and with a seal made under H26 and its prepared spend placed under H27 before the update is broadcast. | | **NEW** |
| M5 | **The cost of the move.** The update of M4 changes the octets of `swarma`. It is the last update of that landlord to which rule 7 applies: every v4 grant that the landlord issued under the inline form refuses from the block that confirms it and is issued again, and a verifier that observes it under LIP-0008 section 5.2 records the closure. From then on H13 holds. A landlord whose value never carried the inline member moves at no cost to its grants: it adds `swarma-holders`, and `swarma` stays. | | LIP-0008 sections 3 and 5.2 |
| M6 | A landlord that added the inline member to a value which had been `{"landlord":{"grant":"<grant key>"}}` would, by removing it, write a `swarma` value that it replaced, which LIP-0008 J6.7 forbids. Such a landlord moves with a new grant key in the update of M4. A landlord whose first `swarma` value already carried the inline member keeps its grant key. | | LIP-0008 section 5.2, J6.1 and J6.7 (Draft, agreement pending) |
| M8 | The move narrows what passes. Under the inline form every name that a listed key holds and wrote is admitted; under the pinned form only the names that the list names. A landlord lists every name in use before it moves, and a name that it leaves out refuses `CLASS_HOLDER` from the block of the update. | `CLASS_HOLDER` | **NEW**; follows from H34 |
| M7 | A landlord with live v3 grants moves only after every verifier of those grants reads this section, as H16 says. A reader of version 0.1.51 reads the inline form and skips `swarma-holders`; a reader before version 0.1.51 refuses the inline form and skips `swarma-holders`; a LIP-0004 reader refuses both. | | Section 6; the closing text of section 10 in version 0.1.51 |

No implementation of version 0.1.51 is claimed, and this text knows of no
landlord name that carries the inline member. The date after which a reader
stops honouring the inline form is open; until the owners set it, M3 stands.

#### 10.10. Cases

Each case pairs a valid control with its refusal. The landlord `id/acme` is
`L`, and its owner's devices are `P` and `M`. List 3 is the example of
section 10.2: `K1` holds `id/acme-worker-7` and `id/acme-worker-8`, and `K2`
holds the reserve `id/acme-reserve-01`. `Y` is the executor of another owner
that admits children of a row whose class holds `L`.

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S10-1 | The confirmed value of `L` pins list 3. A child names `id/acme-worker-7`, whose output pays `K1` and whose value `K1` wrote; the presenter supplies list 3, and `Y`'s node shows the seal of the entry unspent: admitted, and `Y` caches list 3 | The same child with the octets of list 3 and one added space: `HOLDER_LIST_MISMATCH`. The same child with no list, at a verifier with an empty cache: `LIST_UNKNOWN`, and the presenter presents again with the list. `id/acme-worker-9`, which `K1` holds and wrote and which points to `L`, and which no entry names: `CLASS_HOLDER` (step 6). |
| S10-2 | `L` issued the v4 grant `G` at recent block `R`. After `R` the landlord pins list 4, which adds an entry, and later list 5, which drops one: `G` is admitted throughout, because the owner and `swarma` did not change (H13) | An update of `L` that replaces the grant key: `G` refuses, as LIP-0008 section 3 says, whatever the pin. A verifier that records a closure of `G` for the update to list 4 is wrong. |
| S10-3 | `P` broadcasts `tx_revoke_N` for `id/acme-worker-7`. `Y` sees it in its mempool and journals the closure of the entry. `id/acme-worker-8`, which the same `K1` holds, is admitted as before, and `G` and every other v4 grant of `L` stay admissible | A child that names `id/acme-worker-7`, at `Y`, while list 3 still names it: `HOLDER_REVOKED`. After a reorganisation that removes the block with the spend: still `HOLDER_REVOKED`, because the closure is journaled (H29). |
| S10-4 | `id/acme-worker-8` is transferred to `K2`, a key that list 3 names for another entry | A child that names it: `CLASS_HOLDER` (step 7), because the entry's `key` is `K1` (H34). After list 4 names `id/acme-worker-8` with `K2` and confirms, and before `K2` updates the value: `CLASS_WRITER` (step 9). After an update of the value by `K2`: admitted. |
| S10-5 | The reserve `id/acme-reserve-01` is not registered while list 3 is pinned. `K2` registers it and writes an agent binding that points to `L`: from the block that confirms the registration a child that names it is admitted, with no update of `L` (H37) | Before the registration: `CLASS_LANDLORD`, because the name has no value (LIP-0026 R9.4). Another party registers the reserve name first and sends it to the address of `K2`: `CLASS_WRITER` (step 9). The same party keeps the name: `CLASS_HOLDER` (step 7). |
| S10-6 | `K1` is stolen. `P` broadcasts the prepared spends of both entries of `K1`; `Y` journals two closures, and the reserve of `K2` is not touched (H35) | A child that names either name of `K1`: `HOLDER_REVOKED`. After only the first spend, a child that names `id/acme-worker-8` with a value that the thief wrote: admitted, which is why H35 asks for every entry of the pin. |
| S10-7 | List 4 drops the entry of `id/acme-worker-8` without a spend of its seal; after the update confirms, the name refuses `CLASS_HOLDER`. List 5 names it again with the same unspent seal: admitted again (section 10.8) | List 5 names `id/acme-worker-7`, sealed off in S10-3, with the same seal: `HOLDER_REVOKED` (H30). A later name update that pins `seq` 3 while the update of `seq` 5 stays in the active chain: `HOLDER_LIST_ROLLBACK`. List 6 names `id/acme-worker-7` with a new, unspent seal: admitted (H33). |
| S10-8 | The update that pins list 4 is in the mempool: list 3 is the list (H11) | A class check of `L` in that time: `CLASS_LANDLORD_PENDING` (LIP-0026 R9.5). A verifier that takes list 4 before its update confirms is wrong. |
| S10-9 | A landlord value in the inline form with two holders, and no `swarma-holders`: every name that the first inline holder holds and wrote is admitted as in version 0.1.51 (M3) | The same value with a top-level `swarma-holders`: no holder, `CLASS_HOLDER`; the grant key still reads, and the landlord's grants are judged as before (M2). A value with `swarma-holders` twice: `HOLDER_PIN_INVALID`, and the grant key still reads (H9). |
| S10-10 | A landlord in the inline form moves under M4: its v4 grants of before refuse and are issued again, once (M5) | The same landlord then pins list 2: no grant refuses (H13). |
| S10-11 | The grant of the agent `id/acme-worker-8` is ended by the issuer's spend of that grant's seal | The spend of the seal of the entry of `id/acme-worker-8`, with the grant's own seal unspent: the grant is not closed; where its admission passes through a class of `L` it refuses `HOLDER_REVOKED` at each admission, and elsewhere it is admitted. The name stays with the holder of `K1`. |

#### 10.11. Vectors

[`vectors/LIP-0010/holders-vectors.json`](../vectors/LIP-0010/holders-vectors.json)
holds 28 landlord values of the inline form, 9 valid and 19 refused, and
five rows of capacity with the value of each. They follow rules 1 to 8 of
section 10.9, which the file cites as 10.1 to 10.8, and no byte and no
outcome of the file changes. A refused value holds one defect, states the
rule that refuses it and names a valid neighbour. The expected outcomes were
stated by hand, computed by one implementation and decided again by a second
one that shares no code with the first; neither is published here, and both
come from the author of that text.

The pinned form has no published vector yet. A vector set for it holds three
groups. A refused vector holds one defect, states the rule and the code that
refuse it, and names the valid neighbour from which it differs in that
defect.

| Group | Valid | Refused, each paired with a valid neighbour |
| --- | --- | --- |
| `lists`: the exact octets of a list, with their length and SHA-256 | The example of section 10.2; a list with an empty `holders`; a list with one entry; a list of 1024 entries; a list in which two entries have one `key` | A fourth member in an entry, a missing `seal`, and `key` before `name` (H1). Two entries with one `name`; two with one `seal` (H2). Entries not in ascending order of `name`; a `name` with an uppercase letter; a `name` without `id/`; a `key` of 64 characters; a `key` that begins with `04`; a `key` whose x coordinate is on no point of the curve; a `txid` in uppercase; a `vout` with a leading zero; a space after a comma; a trailing newline; a `schema` of `swarma-device-list/1`; `seq` 0; a sixth top-level member (H5). 1025 entries; a list of 262145 bytes (H6). |
| `pins`: the exact text of a landlord value, with the list that it pins | The value of section 10.2 with `seq` 3; the same beside `nostr` and `swarma-devices`; a value without the member (no name listed) | `sha256` before `seq`; a third member; `sha256` in uppercase or of 63 characters; `seq` as a string (H8). The member twice; a member `Swarma-Holders` beside it (H9); each leaves the grant key readable. A pin whose `seq` differs from the list's; a pin whose hash is of other octets; a list whose `owner` is another name; a list whose `network` is not the verifier's (H10). A value with the inline member and the pin (M2). |
| `admissions`: a decision on stated facts, in the manner of the admissions of `vectors/LIP-0026/class-vectors.json`, with the state of each seal and the verifier's journal stated | The valid controls of S10-1 to S10-11 | The refusals of S10-1 to S10-11, each with its code and the step of section 10.6 that gives it |

Until two implementations that share no code agree on those octets, the
length and the hash of section 10.2 are an illustration.

### 11. Heads of statement sets (Draft amendment of 2026-11-16)

Ivan Oparin decided, as recorded by the lead on 2026-11-16, that every
statement set of an owner has one mechanism: the head of the set lives in the
owner's name value, and the last head confirmed in the active chain counts;
the mempool does not. The organization head of the Link book, chapter 9,
«Организация из подписанных записей», is read the same way. The text is
written optimistically: the co-author's agreement is pending, and until it is
given sections 1 and 2 stand and LIP-0016 keeps its anchor.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| SH1 | The head of a statement set of an owner is one top-level member of the owner's name value, outside `swarma`: `{"seq":<seq>,"sha256":"<hex>"}`, exactly these two members in this order, compact. `seq` is a canonical positive integer, at most 9007199254740991, and `sha256` is 64 lowercase hex: the SHA-256 of the exact octets of the set's head document. | The set's own code; none for the value |
| SH2 | The member names are registered here, each with the LIP that defines its head document: `swarma-devices`, whose head document is the device list (LIP-0029 section 3.2), `swarma-certs`, whose head document is the head of LIP-0016 section 2, and `swarma-holders`, whose head document is the holders list of a landlord (section 10.2). A new set is a section of a LIP that registers its member here. `swarma-holders` is in force since version 0.1.53 by rules of its own (section 10.3, H8 to H11), which state for it what SH1, SH3, SH4 and SH6 state; it does not wait for this section, and section 10.8 says where it differs from SH5. | |
| SH3 | A reader takes a head only from the owner's name output that is confirmed in the active chain of its own node, after the last confirmed name operation. A pending name operation gives no head: it neither adds, replaces nor removes one until it confirms. | |
| SH4 | The head document names the owner's `id/` name and the network, and its `seq` equals the pinned `seq`. A document that names another owner or another network, or whose octets do not hash to `sha256`, gives no verified set. | The set's mismatch code |
| SH5 | A reader journals, outside the agents' write authority, for each set of each owner: the highest `seq` that it took, the txid of the name operation that carried that head, and every refusal that it took from the set (for `swarma-devices`, a device that a list removed, a spent device seal and a journaled revocation; LIP-0029 section 8). When a reorganisation removes that name operation from the active chain, the reader takes the last head confirmed in the active chain, whatever its `seq`, journals it in place of the removed one, and keeps every journaled refusal: a record that the removed head revoked or removed stays refused, and a record that only the removed head added waits until a head that holds it confirms again. While the operation of the journaled head stays in the active chain, a head with a lower `seq` that a later name operation carries gives no verified set. | The set's rollback code |
| SH6 | A reader matches a head member by exact name. A duplicate of it, or a member equal to it under Unicode simple case folding that is not that exact name, gives no verified set for that set, and leaves `swarma`, `nostr`, every other set and every grant as they read. | The set's own code |
| SH7 | A head member gives no grant authority. A Link reader of grants does not read it, and an update that changes only head members changes neither the owner nor `swarma` and ends no v4 grant (LIP-0008 section 3; LIP-0029 O3.7 and O3.8). | |
| SH8 | The deployment order of LIP-0029 O3.9 and the v3 cost of O3.10 hold for every head member: none is written before every verifier of the name runs a LIP-0010 reader, and every change of a head is a name update. | |

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S11-H1 | Alisa's confirmed value carries `swarma-devices` with `seq` 4, and Bob's executor reads list 4. List 5 adds device `K` and drops device `M`; after it confirmed, a reorganisation removes its update, and Bob's executor reads list 4 again (SH5) | A pending update to `seq` 5: `K` is unknown until the update confirms (SH3). After the reorganisation: `K` is unknown until a head that names it confirms again, and `M`, which list 5 dropped, stays refused (`DEVICE_REVOKED`). A later name update that writes `seq` 3 while the update of `seq` 5 stays in the active chain: no verified list, `DEVICE_LIST_ROLLBACK`. |
| S11-H2 | The same value with `swarma-certs`: Bob's store reader verifies Alisa's set | A value with `swarma-devices` twice: no device list, and Alisa's v4 grants and her certificate set still read (SH6). A list whose `owner` is Karl's name, pinned in Alisa's value: no verified list (SH4). |

A set without a verified head is no set: each LIP says what its readers then
do. Under LIP-0029 an own executor refuses owner commands
(`DEVICE_PIN_INVALID`, `DEVICE_LIST_MISMATCH`, `DEVICE_LIST_ROLLBACK`), and
under LIP-0016 a store reader treats every subject of the issuer as unbound.

What the rules give and what they cost:

- **One reading for every set.** A reader of devices and a reader of
  certificates see the same head at the same height, and neither depends on
  a host that serves the files: a dropped record or an old set does not hash
  to the head (LIP-0016 section 5).
- **A pending head counts for nothing.** A new head counts only from its
  confirmation, and the record that it adds or revokes takes effect then and
  not before. Between broadcast and confirmation readers keep the previous
  head. A stop that must act from the mempool is a seal spend and not a head
  (LIP-0029 section 8; LIP-0008 sections 5.1 to 5.3).
- **After a reorganisation the last confirmed head counts again.** This is
  the reading of the Link book, §9.4 «Спорные случаи» (line 35 at
  swarma-docs 34abef2): the state is recomputed, new records wait to be
  anchored again, and remembered refusals are not forgotten. SH5 states it
  for every set. The txid in the journal is the draft's way for a reader to
  tell a reorganisation from a lower `seq` that the owner writes later; only
  the second refuses. This narrows the version pin of LIP-0029 O9.2, which
  refused every lower `seq`, and it is put to the owners with the rest of
  this section.
- **The name-owner key signs every change of a set.** It is the cold key, and
  each change is a name update with its fee and, on v3, its outage (SH8).
- **The name value fills.** With the sizes of section 8 and `seq` below 10,
  `swarma-devices` adds 103 bytes and `swarma-certs` 101:

| Value | Bytes without | With both heads | Left of 520 |
| --- | ---: | ---: | ---: |
| Landlord, no `nostr` | 100 | 304 | 216 |
| Landlord, key string | 175 | 379 | 141 |
| Landlord, NIP-05 object | 191 | 395 | 125 |
| Landlord, NIP-05 object and one relay | 294 | 498 | 22 |

Every row with `nostr` leaves less than the 150 bytes that section 8 keeps for
the service declaration of LIP-0007. One member whose head document lists
the heads of every set would cost about 103 bytes for any number of sets, and
the name would then pin the device list through that document and not
directly, against LIP-0029 decision 3. Both forms are open. The table counts
two heads. `swarma-holders` (section 10.3) is a third and adds 103 bytes
more: a landlord value with a NIP-05 object and no relay then takes 498
bytes, and one with a relay does not fit.

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

The holders list of section 10 has consequences of its own. A stolen
name-owner key of the landlord pins a list of its own holders; the
landlord's v4 grants do not end by that update, because `swarma` and the
owner stay, and the classes that name the landlord then admit the thief's
names. A stolen holder key is answered entry by entry (H35), and until the
last spend is seen a name of that key still passes. The list publishes the
names of a landlord's agents and its reserves to everyone who is given it. Custody of the cold key is the defence, as for the name itself. A
copy of a prepared spend revokes one name and gives nothing else (H27). A
verifier whose node has not yet seen a spend admits that name until it
does, and LIP-0022 bounds how long its view may stand still. A
verifier that starts after a spend was confirmed and later reorganised away
holds no closure and decides by its node's view, where a verifier that saw
the spend refuses for good (H29, H31). A host that withholds the list delays
the readers that rely on it and admits nobody (H20, H24).

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
| A landlord value that pins a holders list, the list in exact octets with one entry for each name, and the seal of the entry unspent (section 10) | A list that does not hash to the pin, a pin of a lower `seq`, a missing list, a name that no entry lists, a name whose owner is not the entry's pin and a spent seal refuse the class check and leave the grant key and every v4 grant of the landlord as they read. A change of the pin closes no grant. A value in the inline form of version 0.1.51 is read by section 10.9, and one with both forms has no holder. |
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
- An additional naming convention with a single level of registration; the
  authors' own parsers would then handle only that level (the note that
  closes section 7). No prefix, grammar or migration is defined.
- Whether a transfer of `id/<label>` requires the transfer of `d/<label>` in
  the same deployment procedure.
- Whether the notary shape needs a member for a second, pending key during a
  rotation.
- Decision record, normative adoption and public vectors.
- **The holders list (section 10).** The co-author's answer; every point
  that the section marks NEW, and first the owner pin in an entry and the
  writer of check (d) (H34), the bounds of 1024 entries and 262144 bytes
  (H6), that the closure of a spent seal is of the entry and not of the name
  or the key (H33), whether one spend should revoke every entry of a stolen
  key (H35), and that a removed entry returns after a reorganisation
  (section 10.8); the script and the amount of a holder seal, the fee of its
  prepared spend and the custody of that spend at a landlord without a
  device list (H27); the confirmation depth at which a verifier takes a new
  pin and at which it counts a seal as existing; the member that carries the
  list in a v4 request (H18) and the kind of the Nostr event (H19); the date
  after which readers stop honouring the inline form (section 10.9); whether
  a pending update of `swarma-holders` alone suspends the admission of the
  landlord's own v4 grants (H15); and the 520 bytes of a landlord value with
  three heads (section 10.3).
- **Heads of statement sets (section 11).** One member for each set, as
  written, or one member over every set, which fits the budget and pins the
  device list only indirectly; the confirmation depth at which a reader takes
  a new head; how a reader learns that an owner has no head of a set, as
  opposed to a head it cannot read; and the co-author's agreement.

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
