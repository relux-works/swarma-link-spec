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
| `swarma-holders` (section 10.3, in force since version 0.1.53) | This specification | Reads the pin of a landlord's holders list under H8 and H9. It gives no authority (H12). |
| Any other member | The name's owner or another standard | Does not read it. A head member of section 11 is read under that section where it applies. |

The only part of the value that gives authority is `swarma`. Authority comes from
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
6. Rule 3 has one exception in force: the member `swarma-holders`. A reader
   that makes the checks of a landlord class reads it under section 10.3,
   matches it under H9, and takes its value as the exact byte span that it
   occupies. A defect of that member gives no holders list and never
   refuses the value (H9). Every other reader skips it under rule 3. The
   head members of section 11 are a further exception where that section
   applies.

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

An independent second read of this section found the shape sound and its
seal layer, its journal rules and its transition under-specified. The rules
H38 to H53, and the changed rows of the older rules, close its findings.
Where a point was ruled after that read, the row says "by ruling";
every other addition is marked **NEW** with the alternative that it does
not take, and where a choice was open the strict one, which refuses, was
taken. The rules are numbered in the order in which they were written and
stand in the subsection of their subject.

#### 10.1. The holder entry

A holder entry is one JSON object under the encoding rules of LIP-0013
section 2.1, with exactly these members in this order:

| # | Member | Rule | Source |
| --- | --- | --- | --- |
| 1 | `name` | The exact name of one agent or station of the landlord: `id/` followed by 1 to 252 bytes of `a-z`, `0-9`, `-`, `_` and `.`, the v3 name syntax of LIP-0013 section 2.1. | **NEW**: the decision makes the entry one per name; the syntax is that of LIP-0013 section 2.1 |
| 2 | `key` | The owner pin of that name, in the form of [LIP-0021](LIP-0021-name-ownership-and-history.md) O2.1: a compressed secp256k1 public key, written as 66 lowercase hexadecimal characters that begin with `02` or `03`, whose other 64 characters are the x coordinate of a point of the curve. | **NEW** as a member of an entry by name (H34). The pin is that of the member `holders` of version 0.1.51 (section 10.9, rule 2); the member name is that of the device record, LIP-0029 section 3.1 |
| 3 | `seal` | `{"txid":…,"vout":…}`, the outpoint of the entry's revocation seal: 64 lowercase hex in display byte order and a canonical non-negative integer, at most 4294967295. | LIP-0029 section 3.1, member `seal`, word for word. The bound of `vout` is **NEW**; it is the largest output index of a transaction |

The `seal` is one JSON object with exactly two members in this order: `txid`,
a string, and `vout`, an integer. It has no other member, and a `seal` with
`vout` before `txid`, with a third member, with a member twice or with a
`vout` in another spelling than the canonical decimal one is no seal (H1).
An entry names an `id/` name only: a recipient name outside the `id/` syntax
can stand in no entry, so a class admits no such recipient through the
pinned form. That exclusion is by construction and is **NEW**.

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H1 | An entry has the three members `name`, `key` and `seal`, each once, in that order, and no other. Its `seal` has the two members `txid` and `vout`, each once, in that order, and no other. An entry has no label, no algorithm, no presence flag and no ceiling: a holder signs nothing for the landlord, so the members of a device record that describe a signer have no subject. | `HOLDER_LIST_INVALID` | **NEW**; the record of LIP-0029 section 3.1, less what describes a signer, with the name. The rule sentence for the seal object is **NEW**; its shape is that of LIP-0029 section 3.1 |
| H2 | No two entries of one list have the same `name`, and no two have the same `seal`. Two entries may have the same `key`: one key may hold several names, and each of them has its own entry and its own seal. | `HOLDER_LIST_INVALID` | LIP-0029 O3.3 for `seal`. Uniqueness by `name` and not by `key` is **NEW** |
| H38 | **One seal, one entry.** A seal outpoint serves exactly one entry: one landlord (its name with its registration, H39), one `name` and one `key`. It is never named by an entry of another name, by an entry of the same name with another `key`, or by an entry of another landlord, in the same list or in any other, whether it is spent or not. A change of the owner pin of a listed name is therefore a new entry with a new seal (H36). A landlord's tool refuses to write a list that breaks this. A verifier journals, with every list that it takes (H40), the binding of each seal outpoint of that list to its landlord, `name` and `key`. An entry whose seal the journal binds to another landlord, another `name` or another `key` refuses, and the binding that was journaled first stays. | `HOLDER_SEAL_REUSED` at a verifier; the tool refuses at the landlord | **NEW**. H2 states it inside one list only. The alternatives are not taken: a seal that follows its name through a change of pin, under which a runbook written for one pin revokes a name of another; and a rule for one landlord only, under which two verifiers match a closure of a shared outpoint differently. The limit of the rule is stated in the security consequences: the binding journaled first wins at each verifier |
| H3 | A holder is a key that owns names of the landlord's agents and stations: the output of such a name pays the key hash or the witness key hash of the pin (LIP-0021 O3.3). It is a name-owner key of the key registry, and it is a different key by role from the grant key, from the key that owns the landlord name and from every key that `nostr` yields. A reader permits equal keys and never requires or infers equality. The key that owns the landlord name is a holder only where an entry names it. | | Rule 5 of version 0.1.51, unchanged |
| H4 | An entry confers no authority, and neither does its holder. It issues no grant and signs no request. Only the checks of a landlord class read the list ([LIP-0026](LIP-0026-rows-and-accounts.md) sections 9 and 10), and they read it at each admission (section 10.6). | | Rule 6 of version 0.1.51, unchanged |
| H34 | **The entry carries the owner pin.** An entry admits its name only while the current output of that name reads as controlled by the entry's `key` (LIP-0021 O3.4), and only a value that this key wrote (section 10.6, steps 7 and 9). A listed name whose current owner is another key does not pass, whoever that key is and whatever the value says; a key that holds a name which no entry lists passes nothing with it. When the owner of a listed name changes, the entry stops admitting from the block of the transfer, with no closure; the landlord accepts the new owner only by a new list whose entry for the name carries the new pin (H36), and the new owner then writes the value itself. | `CLASS_HOLDER`, `CLASS_WRITER` | **NEW**: the strong form of the decision's default, an entry of name, owner pin and seal. The form without the pin is not taken: a listed name would then pass for whoever came to hold it, and a name listed before it is registered would pass for whoever registered it first |
| H37 | **Reserve entries.** A landlord may list names ahead of their use and keep them in reserve: an entry is valid whether or not its name is registered, points to the landlord or has ever been presented. A reserve entry admits nothing until the name is live, its value is an agent binding that points to `L`, the entry's `key` holds it and that key wrote the value (LIP-0026 R9.4 to R9.7); from that block it admits, with no update of the landlord's name and no new list. A reserve entry costs its seal, with the prepared spend of H26 and H27, and its octets in the list within H6; it costs no byte of the name value and no name update beyond the one that pins the list that holds it. A reserve entry is revoked like any other, by the spend of its seal. **Register first, then list.** A landlord MUST NOT broadcast the name update that pins a list before every reserve name of that list is registered to the `key` of its entry: the registration is confirmed in the active chain, and the current output of the name reads as controlled by that key. The landlord's tool makes that read on its own node and refuses to write the pin otherwise. What is lost otherwise: the list makes the name public before it exists, whoever registers it first owns it, the name never passes steps 7 and 9 of section 10.6 for that party, and where that party keeps the name the entry is dead for good, its seal and its prepared spend are spent for nothing, and only a name update of the landlord removes the entry. A prepared spend of a reserve entry that leaks ends the entry before its first use, with the same recovery (H33). | None at a verifier: it reads an entry of an unregistered name as a reserve and refuses the name at check (a). The tool refuses at the landlord | **NEW**; the decision allows listing ahead. That registration comes first was this text's advice to the holder key and is now a rule for the landlord, whose pin creates the exposure. That the registration is confirmed, and not only reserved by a pending or a first-stage name operation, is the strict choice; the weaker one is not taken. LIP-0026 check (d) is what keeps a name that was registered by another party from passing |

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
| H5 | A list that is no JSON object of exactly the five members in their order, that is not in the encoding of LIP-0013 section 2.1, whose re-encoding differs from its octets, whose `schema` is another string, whose `network` is neither `main` nor `regtest`, whose `seq` is no canonical positive integer within its bound, whose entries are not sorted or break H1 or H2, or that holds a `name` outside the syntax of section 10.1 or a `key` that is no owner pin, is no list. A member that occurs twice in one object refuses at every level: in the list, in an entry and in a seal object. A reader MUST refuse it in those words and not only because the re-encoding differs. | `HOLDER_LIST_INVALID` | LIP-0029 section 3.2 and `DEVICE_LIST_INVALID`; the refusals of rule 3 of section 10.9. The duplicate member in words is **NEW** here; LIP-0013 section 2.1 gives it through the re-encoding |
| H6 | A list holds at most 1024 entries and at most 262144 bytes. A list above either bound is no list. A reader MUST compare the length of the octets with the byte bound before it hashes or parses them, and it reads no octet beyond the bound. The cap of five holders of version 0.1.51 does not apply to a list: it followed from the 520 bytes of a name value (section 10.9, rule 8), and the list is outside the value. | `HOLDER_LIST_INVALID` | **NEW**. LIP-0029 section 3.2 bounds a device list at 16 records and 4096 bytes; those numbers are not taken, because 16 is the order of the cap that the decision removes and an entry is now one for each name. An entry with a name of 16 bytes takes 194 bytes, so 1024 such entries take about 200000 bytes; with the longest names the byte bound is reached first |
| H7 | A list with an empty `holders` is valid and says that the landlord lists no name. A landlord value without the pin of section 10.3 says the same. No name passes check (c) or (d) of a class against such a landlord. | `CLASS_HOLDER` (LIP-0026 section 9) | Rule 4 of version 0.1.51. LIP-0029 section 3.2 asks at least one record of a device list; that floor is not taken |
| H53 | **The order of the checks of a list.** Step 5 of section 10.6 makes four checks in this order, and the first that fails gives the refusal. (1) The octets are at most 262144 bytes long (H6): `HOLDER_LIST_INVALID`. (2) Their SHA-256 equals the pinned `sha256` (H17): `HOLDER_LIST_MISMATCH`. (3) They are a list under H5 and H6, the encoding, the members, the values of `schema` and `network`, the count and the entries included: `HOLDER_LIST_INVALID`. (4) The `seq`, the `owner` and the `network` meet H10: `HOLDER_LIST_MISMATCH`. So octets that are too long and also hash to another value refuse as invalid; a list whose `network` is a third string refuses as invalid; and a valid list of the other network of the two refuses as a mismatch. | The first that applies | **NEW**. The order is the cheapest check first and the bound before the hash, so that no reader hashes or parses what it must not read |

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
| H9 | A reader MUST match `swarma-holders` by exact name. A duplicate of it, or a member equal to it under Unicode simple case folding that is not that exact name, gives no holders list, and so no listed name. It leaves `swarma`, `nostr`, every other member and every grant as they read. A member of another shape than H8 gives no holders list in the same way. The name is matched on the bytes of the member name as the value writes them: the 14 bytes `swarma-holders` between two quotation marks, with no escape. A top-level member whose written name holds an escape and decodes to `swarma-holders`, or to a string that is equal to it under the fold, is such an alias and gives no holders list; a reader therefore decodes the names of the top-level members to find it and never takes a pin from a member that it found only by decoding. The value of the member is the exact byte span that it occupies in the name value, from the opening brace to the closing one, and that span MUST equal the compact encoding of the pin that it parses to (H8); the content of the other members is not interpreted to find it, beyond the JSON structure that delimits them. | `HOLDER_PIN_INVALID` | Section 11, SH6. LIP-0029 O3.5, which refuses the whole value, is not taken: a defect of the pin would then refuse every grant of the landlord, against H13. The rule for an escaped spelling and the byte span of the pin are **NEW**, in the form of section 2, rules 2 and 4; reading an escaped name as the member is not taken, because two readers would then find a pin in different values |
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
| H13 | The holders of a landlord are no part of its `swarma` member. The pin `swarma-holders` is a top-level member outside `swarma`, and the list is outside the value. A name update of the landlord that adds, replaces or removes `swarma-holders`, and that changes neither the owner of the name nor the octets of `swarma`, ends no v4 grant, refuses none, and is no break under LIP-0008 section 5.2 (J6.1): a verifier records no closure for it, and the landlord issues nothing again. The spend of a holder seal that was made under H26 and that is no other outpoint of the protocol (H49) is no operation of the landlord name and touches no grant. A seal that is, against H49, also the seal of a grant, a linkage output, a coin of a row, a stop coin or a name output performs that other act when it is spent, and this sentence does not cover it; a verifier refuses such an entry where it can see the collision (H49). A v4 grant that the landlord issued depends, in the landlord's name, on exactly the facts that LIP-0008 section 3 binds: the name; its registration; the owner key that controls every output of the name from the one current at the grant's committed recent block to the current one; and the exact octets of the `swarma` member on each of those outputs, which for a landlord in the pinned form are the compact encoding of `{"landlord":{"grant":"<grant key>"}}`, with the grant key equal to the grant's issuer key, and nothing else. No octet of `swarma-holders`, of a holders list or of a holder seal is among them. Beside the name the grant depends, as before, on its own seal and its own window. | LIP-0029 O3.8 and decision 3; section 11, SH7; LIP-0008 section 3, unchanged |
| H14 | H13 changes nothing in LIP-0008. The rule that a grant lives while the owner and `swarma` do not change stands as written; what changes is that `swarma` no longer holds the holders. A change of the grant key or of the owner still ends every v4 grant of the landlord. | LIP-0008 section 3 |
| H15 | Every change of the list is a name update of the landlord, signed by the name-owner key, that writes a pin with a higher `seq`. While it is pending, a class check that reads this landlord refuses without closure (LIP-0026 R9.5, sixth step), and a v3 verifier refuses the grants of the name, without closure, until the update confirms (LIP-0004 section 5). Whether a pending update of `swarma-holders` alone suspends the admission of the landlord's own v4 grants is a question of the observation profile, as it is for `swarma-devices` (LIP-0029 section 3.4). | LIP-0029 O3.10 and O9.1 |
| H36 | **Adding entries.** Adding a name, a reserve included, or changing the owner pin of a listed name needs a new list that holds the entry, a new seal for the entry (H38) with its prepared spend placed under H27, and an update of the landlord's name, signed by the name-owner key, that writes `swarma-holders` with a higher `seq`. The funding transaction of every seal of the list is confirmed in the active chain before that update is broadcast, so that the seal exists as H46 asks when the pin confirms; the landlord's tool makes that read and refuses otherwise, and a verifier sees a breach as `HOLDER_SEAL_NOT_LIVE`. A presentation, an attachment or a message never adds an entry. That update ends no v4 grant (H13). Adding is slow and guarded; revoking one name is fast where H51 is met. | LIP-0029 O9.1 to O9.3 and decision 6; **NEW** as a rule for entries by name. That the seals are confirmed before the pin is broadcast is **NEW** |
| H16 | A landlord MUST NOT write `swarma-holders` into a name while a verifier that its own deployment configures or knows of reads that name with a reader older than this LIP. No landlord can list every present and future verifier of another party, so for those the sentence is a statement of cost and no rule: a LIP-0004 reader refuses the whole value, and every v3 grant under that name then refuses at that verifier, without closure, until the exact value is restored (section 6). A reader of this LIP before this amendment skips the member as one of the owner's and finds no holder, so it refuses every recipient of a class of that landlord and admits none wrongly. | LIP-0029 O3.9; section 2, rule 3. None at a verifier: no verifier can observe the order of a landlord's deployment. The narrowing to the verifiers that the deployment knows is **NEW** |

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
| H18 | The primary path is the presentation. The party that presents a child of a row whose recipient is a class, or a request under such a child, supplies the exact octets of the list that the landlord's value pins: when the list has changed since the last presentation that this verifier admitted from it, and at first contact, which is every presentation to a verifier of which the presenter holds no record that it admitted one under this `h(H)`. Otherwise the presentation carries nothing of the list. A verifier caches every list that it verified under H10 and H17, keyed by the landlord (its name with its registration, H39) and `h(H)`, and makes a later check from the cache. The member that carries the octets comes with the octets of a v4 request ([LIP-0020](LIP-0020-grant-v4-wire-registry.md)); until then the list travels beside the presentation. | | LIP-0029 O3.12. That the presenter stands in the sender's place is **NEW** |
| H19 | Two secondary paths serve a reader that has no presenter to ask, such as the signer of an issuer under LIP-0026 R9.12 or a verifier that starts with an empty cache. (a) The landlord's domain: `https://<domain>/.well-known/swarma/holders-list/<h(H)>`, where `<domain>` is the domain of the NIP-05 identifier in the landlord's name value, and the body of the response is the exact octets of the list. (b) A parameterized replaceable Nostr event signed by the key that the landlord's name value yields for the Nostr channel, with the tag `["d","swarma-holders-list"]`, whose `content` is the exact octets of the current list. Both places are named by the landlord's name value, and a reader fetches from no other: not from a URL in a request, not from a relay's or a peer's hint. A copy from either counts only under H17. **Neither path can be built between two independent readers yet.** The name value of this document holds a key and relay hints and no domain, so path (a) has no `<domain>` that a reader can derive from the value alone; the kind of the event of path (b) is open. Until both are closed, the readers that this rule names have no working secondary path: they stay at `LIST_UNKNOWN` (H20), which fails closed, and no implementation claims either path. | | LIP-0029 O3.13. The path segment and the `d` tag value are **NEW**, in the form of those of the device list; the kind of the event is open as it is there. That the paths are not yet implementable is stated here and is **NEW** as a statement |
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
| 0 | The verifier's holder journal (H39) is intact and can be written (H43) | `JOURNAL_LOST`, `JOURNAL_FENCED` (LIP-0025) | **NEW** in this place; LIP-0027 H2.1 |
| 1 | Read the current confirmed value of `L` on the verifier's own node, in the observation of the admission (H44): the output that check (b) judged. Decide its form under section 10.9. A value with neither form, or with both (M2), lists no name. A value in the inline form of a landlord for which the journal holds the form mark gives no holder (H42) | `CLASS_HOLDER`; for the inline form after a pinned list, `HOLDER_FORM_DOWNGRADE` | LIP-0026 R9.6 and R9.10; H7, H11. The downgrade refusal is **NEW** (H42) |
| 2 | The member `swarma-holders` is valid under H8 and H9 | `HOLDER_PIN_INVALID` | LIP-0029 section 11, step 4 |
| 3 | The pin is no rollback against the journaled head of `L`, in the order of H23: the name operation of the journaled head is read against the tip; while it stays in the active chain, a lower `seq` refuses, and so does an equal `seq` with another `sha256` | `HOLDER_LIST_ROLLBACK`; a read that fails, `CLASS_HISTORY_UNAVAILABLE` | Section 11, SH5. LIP-0029 O9.2 is no longer cited for this step: read to the letter, "only with a `seq` higher" refuses the same list at the next admission |
| 4 | The verifier holds octets under the pinned hash, from its cache or from the presentation | `LIST_UNKNOWN` (H20) | LIP-0029 section 11, step 5 |
| 5 | Those octets pass the four checks of H53 in their order. Where the pin is not the journaled head of `L`, the verifier then takes the list (H40) before it goes on | `HOLDER_LIST_INVALID`, `HOLDER_LIST_MISMATCH`, in the order of H53; a take that cannot be written, H43 | LIP-0029 section 11, step 5, and O5.3. The order and the take are **NEW** |
| 6 | The list has an entry whose `name` is, octet for octet, the recipient name, and the journal holds no removal mark of that entry (H41) | `CLASS_HOLDER` | **NEW** (the entry by name); LIP-0029 section 11, step 6, "one record"; section 11, SH5, for the mark |
| 7 | Check (c): the current output of the recipient name reads as controlled (LIP-0021 O3.4) by the `key` of that entry | `CLASS_HOLDER` | LIP-0026 R9.6; H34 |
| 8 | The seal of that entry, in the order of H48: it is no other outpoint of the admission (H49); the journal holds no closure of it (H28); the journal binds it to this entry (H38); it exists on the active chain as H46 asks; and the verifier's own node, with its mempool included, shows it unspent in the seal read of H45 | `HOLDER_SEAL_ALIAS`, `HOLDER_REVOKED`, `HOLDER_SEAL_REUSED`, `HOLDER_SEAL_NOT_LIVE`, `CLASS_HISTORY_UNAVAILABLE`, in the order of H48 | LIP-0029 O8.9 and section 11, step 8, for the unspent seal; the rest is **NEW** (section 10.7) |
| 9 | Check (d): the value of the current output of the recipient name was written by the `key` of that entry (LIP-0021 section 4) | `CLASS_WRITER` | LIP-0026 R9.7. That the writer is the key of the same entry, and no other holder of the landlord, is **NEW** (H34), and the ruling keeps it |
| Before the effect | The reads of H44 are made again immediately before a reservation or an effect | The codes of step 8; a tip that moved voids the admission (LIP-0022 B1.6) | **NEW** (H44); LIP-0022 B1.6 |

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H21 | **What a verifier reads.** For every admission it reads, on its own node and in one observation (H44): the confirmed value of `L` and with it the pin; the name operation of the journaled head (H23); and for the entry of the recipient name, the seal read of H45, with the mempool included. It reads the list from its cache or from the presentation. It takes nothing of this from the presenter except octets that hash to the pin. It reads the seal of no other entry for the admission. | | LIP-0026 R9.10; LIP-0029 O8.9 |
| H44 | **One observation, one named tip, and the read before the effect.** The observation of an admission begins and ends with a read of the tip, its hash and its height (LIP-0022 B1.1), and that pair is the named tip of the admission. Five reads bind to it: the confirmed value of `L` with the pin; the name operation of the journaled head; the pending read of check (b), the sixth step of LIP-0026 R9.5; the current output of the recipient name; and the seal read of H45, in its confirmed part by LIP-0022 B1.4 and in its mempool part by being made between the two reads of the tip. They are facts of one admission in the sense of LIP-0022 B1.5. No rule ties a pending transaction to a tip (LIP-0022 section 1), so the mempool part is bound in a second way: immediately before a reservation or an effect, in the recheck of LIP-0022 B1.6, the verifier reads again the tip, the pending read of check (b), the spend state of the seal with the mempool included, and its journal for a closure of the seal. A tip that moved voids the admission. A spend that it validates at any point before the effect (H47) is journaled, and the admission refuses as `HOLDER_REVOKED`; a seal that is no longer shown unspent without such a spend refuses as `HOLDER_SEAL_NOT_LIVE`; a pending operation of `L` refuses as `CLASS_LANDLORD_PENDING`. A spend that reaches the node after that last read does not undo the effect (section 10.7). A closure that was written during an observation which then turns out void stands, as LIP-0022 B1.2 says of the closures of LIP-0008: it rests on a transaction that the verifier validated and on a seal that was confirmed at a tip which the record names. | The codes named; a void observation gives the code of LIP-0022 | **NEW**. LIP-0022 B1.1, B1.2, B1.4, B1.5 and B1.6. The second read is the strict choice; stating the window between step 8 and the effect as an accepted limit is not taken |
| H22 | **How old a list may be.** A list has no expiry, and its age is no input. The one list that counts at an admission is the list whose hash and `seq` the landlord's confirmed value pins at the tip of that admission's observation. A list that an earlier value pinned, however recent, is no input, whether the verifier holds the current one or not. The freshness of the check is therefore the freshness of the observation: the cutoffs of LIP-0022 section 3 for the age of the tip apply to the class check as to every read of the admission, and this section adds no clock of its own. A cached list is valid for exactly as long as the pin that names it is the confirmed pin. | | LIP-0029 section 3.2 (no expiry), O3.12 (the cache), O9.2 (the pin from the name); LIP-0022 B1.5 and B3.6. That no further age bound is added is **NEW** |
| H39 | **The holder journal and its keys.** A verifier keeps one holder journal, outside the agents' write authority, in the form of LIP-0025. In it a **landlord** is the pair of its name and its registration, the transaction id and the output index that the class pins (LIP-0026 R9.1) or that the parent binds for its issuer (R10.3). A name that expired and was registered again under the same spelling is another landlord, with no state. The journal holds five kinds of record. (1) The **head** of a landlord: the `seq` and the `sha256` of the pin of the list that it last took, the txid of the name operation that carried that pin, and the hash and the height of the block that holds it. (2) The **form mark** of a landlord (H42). (3) The **binding** of a seal outpoint to its landlord, `name` and `key` (H38). (4) The **removal mark** of an entry, keyed by its seal outpoint, with the `seq` of the list that dropped it (H41). (5) The **closure** of an entry, keyed by its seal outpoint (H28). The key of a binding, of a removal mark and of a closure is the seal outpoint alone, the pair of `txid` and `vout`: by H38 an outpoint is one entry, so the journal holds at most one of each for an outpoint, across every list, every name and every landlord that the verifier reads. The octets of these records are open. | | **NEW**. Section 11, SH5, and LIP-0029 O9.2 for the head; LIP-0027 section 3 for a journal in the form of LIP-0025. That a closure is keyed by the outpoint and holds across landlords is the strict choice; a closure for each landlord, under which a seal that two landlords name is revoked for one and admitted for the other, is not taken |
| H40 | **The take of a list, which is the one point at which the journal advances.** A verifier takes a list when, in an admission, the pin has passed step 3 and its octets have passed step 5, and the pin is not the journaled head of the landlord. Before that admission goes on to step 6 it writes, as one atomic step of the store: the new head in the place of the old; the form mark, where the landlord has none; a binding for every seal of the list that the journal does not bind yet; a removal mark, with the `seq` of the taken list, for every entry that the journal binds to this landlord, that the taken list does not hold and that has no mark of a higher `seq`; and the lifting of the removal mark of every entry that the taken list holds and whose mark has a lower `seq` than the taken list. A seal that the journal binds to another entry keeps its binding, and the list is taken all the same (H38). A pin whose list the verifier does not hold, or whose octets fail step 5, advances nothing: the journaled head, and with it the floor of step 3, stays. | A write that fails: H43 | **NEW**. Neither H23 of the first text nor its sources say when the journal advances. Advancing on the read of the pin is not taken: a pin whose list nobody supplies would then raise the floor |
| H23 | **Rollback, in this order.** (1) Where the journal holds no head of the landlord, step 3 passes. (2) The verifier reads, against the tip of the observation, whether the name operation of the journaled head is in the active chain (LIP-0022 B1.4). A read that fails proves nothing. (3) While that operation is in the active chain: a pin with a lower `seq` gives no list; a pin with the same `seq` and another `sha256` gives no list; a pin with the same `seq` and the same `sha256` passes and is no take, whichever later operation carries it; a pin with a higher `seq` passes and is taken under H40. (4) Where a reorganisation removed that operation, the verifier takes the pin of the current confirmed value, whatever its `seq` and its hash, under H40, and the new head replaces the removed one. An equal `seq` with another hash is accepted through this branch alone and never through a later name operation. Every form mark, binding, removal mark and closure stays through every branch. | `HOLDER_LIST_ROLLBACK`; for (2), `CLASS_HISTORY_UNAVAILABLE` | Section 11, SH5. The read of the journaled operation at each admission, and the refusal of an equal `seq` with another hash, are **NEW**; without the second, `seq` alone detects no substitution. The rule defends against a later operation that carries an older pin, and against nothing else: whoever holds the name-owner key writes old contents under a higher `seq`, and H30, H41 and H42 are what then holds at a witness |
| H41 | **A removed entry does not return by a reorganisation.** An entry that a taken list dropped has a removal mark with the `seq` of that list (H40), and step 6 refuses its name while the mark stands, whatever list the current confirmed value pins. The mark is lifted only by the take of a list with a higher `seq` than the mark's that holds the same entry: the same `name`, `key` and `seal`. A reorganisation that removes the operation of the dropping list lifts nothing: the older list is the list again (H23), and the entry that it holds stays refused at this verifier. A verifier that never took the dropping list holds no mark and admits the name from the older list; a removal is a durable fact at the verifiers that took it and at no other. **Removal alone is therefore no answer to a compromise.** A landlord that must not see a name return spends the seal of its entry, and removes the entry as well (H32). | `CLASS_HOLDER` | Section 11, SH5: "a record that the removed head revoked or removed stays refused". The first text of this section departed from SH5 here and that departure is withdrawn by ruling. That the mark is lifted by a higher `seq` alone, and not by an equal one through the reorganisation branch, is **NEW** |
| H42 | **No return to the inline form.** The form mark of a landlord is written with the first list that the verifier takes for it (H40) and is never lifted, by no later value and by no reorganisation, also not by one that removes the operation of that first list. For a landlord with the form mark the verifier never reads the inline form of section 10.9 again: a confirmed value of that landlord in the inline form gives no holder, as a value with both forms does (M2), and no name passes check (c) or (d) through it. The sealed-off entries of that landlord, and every other name that an inline key holds, therefore stay refused across such a value. The grant key of the value still reads, and the landlord's own grants are judged as before (section 10.9, rule 7, for what the change of `swarma` does to them). A later value of that landlord in the pinned form is read under the steps of this section, with the journal as it stands. | `HOLDER_FORM_DOWNGRADE` | **NEW**, by ruling. M4 binds the landlord's writer only; whoever holds the name-owner key can write the inline form, and M3 made every verifier read it. Scoping H29 to the pinned form in words, and accepting the downgrade as a landlord act, is not taken |
| H43 | **A journal that cannot be written, a journal that is lost, and replicas.** (1) Where a record of H39 is due and cannot be written, the admission for which it was due refuses, with the code that the record would have given (`HOLDER_REVOKED` for a closure) and otherwise with `JOURNAL_LOST`, and the journal is lost for that verifier (LIP-0025 M5.1): it admits no child through any landlord class until its operator has restored the journal or started it anew, an act that is recorded. A restart does not end that state, also where the store and its outside record still agree because nothing was written (LIP-0027 H3.3). (2) A verifier whose holder journal is lost is a newcomer for holders (LIP-0008 J6.9). After a start anew it holds no head, no form mark, no binding, no removal mark and no closure. It may claim what its own node shows at the tip of an observation and nothing else; it MUST NOT report a closure, a removal or a form mark that it does not hold, and it says that it is a newcomer and since which recorded act. What is lost with the journal is every closure whose spend is no longer in the view, every removal mark and every form mark: such a verifier admits again what a witness refuses, and reads the inline form of a landlord that returned to it. Deleting a record is no recovery. (3) The replicas of one executor share one authoritative holder journal, as they share the grant journal (LIP-0008 section 4). A replica that does not share it is no replica of that executor: it is a verifier of its own, with witness state of its own, and its operator's conformance claim says so. | `JOURNAL_LOST`, `JOURNAL_FENCED` (LIP-0025); no admission | **NEW**: LIP-0008 section 5.1, last sentence of its second paragraph, and J6.9; LIP-0027 H3.3 and H3.6; LIP-0025 M5.1. The durable mark of a journal that is lost after a write failed is open here as it is in LIP-0027 |
| H24 | **What a verifier refuses when it cannot get the pinned list.** It refuses the admission of that child, `LIST_UNKNOWN`, and nothing else: the parent, the landlord's own grants and every other row are judged as before. It MUST NOT fall back to a list of a lower `seq`, to a list that it cached under another hash, to the inline form of section 10.9, or to the claim of the presenter. A failed or ambiguous read of the node, of the landlord's value, of the journaled operation or of a seal, proves nothing and refuses as `CLASS_HISTORY_UNAVAILABLE` (LIP-0026 R9.8); it is never reported as a revocation or as a missing seal. None of these refusals records a closure, and each ends when the verifier holds the list or the read succeeds. | `LIST_UNKNOWN`; `CLASS_HISTORY_UNAVAILABLE` for a read of the node | LIP-0029 O3.14; LIP-0026 R9.8; LIP-0008 section 5.1, last paragraph |

The steps stand inside the order of LIP-0026 R9.9: steps 0 to 8 are check (c)
and step 9 is check (d), after checks (a) and (b). In the pinned form the
sentence of R9.7 that the writer need not be the holder of R9.6 has no
subject: one entry answers both.

The codes of this section are these. Nine are **NEW** and are proposals:
`HOLDER_PIN_INVALID`, `HOLDER_LIST_INVALID`, `HOLDER_LIST_MISMATCH`,
`HOLDER_LIST_ROLLBACK` and `HOLDER_REVOKED`, each in the form of the
device-list code that its source row gives, and `HOLDER_SEAL_NOT_LIVE`,
`HOLDER_SEAL_REUSED`, `HOLDER_SEAL_ALIAS` and `HOLDER_FORM_DOWNGRADE`, which
have no device-list model. Four are reused with the meaning that their
source gives them: `LIST_UNKNOWN` (LIP-0029 decision 17),
`CLASS_HISTORY_UNAVAILABLE` (LIP-0026 R9.8), and `JOURNAL_LOST` and
`JOURNAL_FENCED` (LIP-0025). The eight codes of a class keep their meaning.

Three of them are kept apart because a presenter, an operator and a retry
policy act differently on each:

| Code | What it says | What it leaves behind | What the presenter does |
| --- | --- | --- | --- |
| `HOLDER_REVOKED` | The verifier holds a journaled closure of the seal of this entry: it validated a transaction that spends the seal (H47), now or earlier | A durable closure (H28) | Does not retry. The name returns only by a new entry with a new seal (H33) |
| `HOLDER_SEAL_NOT_LIVE` | The seal is not on the active chain as H46 asks, or the node does not show it unspent and the verifier validated no transaction that spends it. It is no statement that the name was revoked | Nothing | Turns to the landlord: the seal was never funded as listed, is not confirmed, has another script, or was spent where this verifier cannot validate the spend |
| `CLASS_HISTORY_UNAVAILABLE` | A read failed, did not answer or contradicted another read. It is no statement about the seal or the name | Nothing | Retries |

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

The figure is the decision's, in its words. Three of its lines are narrowed
by the rules below. "`gettxout(S_N)` unspent" is the seal read of H45 and
H46: a seal counts only when its funding output is confirmed in the active
chain, and an output that only a pending transaction creates is no unspent
seal. "The devices of the landlord's owner" are the keepers of H27. And "a
rollback cannot restore the entry" holds at a verifier that validated the
spending transaction on its own node (H28, H29), and at no other (H50).

The rules stand in four groups: how a landlord makes and keeps a seal, which
no verifier observes; what a verifier reads of a seal; what a closure is;
and what a reader does that cannot validate a spend.

**How a landlord makes and keeps a seal.** No verifier observes a rule of
this group, and none refuses anything for it; the landlord's tool does.

| Rule | Requirement | Refusal | Modelled on |
| --- | --- | --- | --- |
| H25 | Revocation of one name is the spend of the seal of its entry. | | LIP-0029 O8.1 |
| H26 | The seal `S_N` of an entry is an output that pays a fresh key `k_N`, which is neither the holder key nor any other key. Before the entry is listed, a transaction `tx_revoke_N` that spends `S_N` is signed with `k_N`, and `k_N` is then destroyed, so that no spend of `S_N` other than `tx_revoke_N` can be signed afterwards. A seal is created for this purpose alone: its outpoint is no seal of a grant, no output after such a seal, no coin of a row, no stop coin, no device seal and no name output (H49). | None at a verifier. **No verifier can check that `k_N` is fresh, that it is no other key, that it was destroyed, or that `tx_revoke_N` exists.** H46 says what follows | LIP-0029 O8.8. The last sentence is **NEW** (H49) |
| H51 | **The construction of the seal and of its prepared spend.** `S_N` pays the witness key hash of `k_N` (H46). `tx_revoke_N` has exactly one input, the seal; it takes its fee from the amount of the seal, and no second input exists that another party, or a service that signs without an act of the landlord, could spend first. Its signature has the hash type `01`, so that it commits to every input and every output, and its outputs are fixed when it is signed. Three points stay **open**: the amount of a seal; the fee of `tx_revoke_N`, which is fixed for good when `k_N` is destroyed and must still relay and confirm at a broadcast that may come years later; and whether an output of `tx_revoke_N` pays a key of the landlord's cold custody, so that a child transaction can raise the fee. **Until the owners close those three points, no landlord and no implementation claims the fast path of this section**: a prepared spend whose fee no longer relays reaches no verifier's mempool, and with `k_N` destroyed no second one can be signed. The slow path of H32 does not depend on them. | None at a verifier, except the script form (H46). The tool refuses at the landlord | **NEW**. LIP-0027 H4.5 for the inputs and the hash type; LIP-0008 J6.6. A second input for the fee is not taken: its spend by anyone who reaches it displaces the revocation for good. With another hash type a copy of the spend could redirect the amount or graft inputs, and "gives nothing else" (H27) would be false |
| H27 | **Who keeps the prepared spends.** Nobody holds a key of the seal. Two custodies keep `tx_revoke_N`, and the holder of the name is in neither. (1) **The devices.** Where the landlord name's own confirmed value pins a device list in `swarma-devices` (LIP-0029 section 3.3), every device of that list whose record has `ceiling` 2 (LIP-0029 section 3.1) holds `tx_revoke_N` of every entry and can broadcast it without the holder and without the name-owner key. A device with a lower `ceiling`, a messenger device above all (LIP-0029 section 4.1), holds none. A device list that another name pins is no device list of this landlord, and no rule maps a landlord to one. (2) **The cold floor.** Every landlord keeps one copy of every prepared spend in a custody that is no weaker than the custody of its name-owner key: offline, and on no host that runs an agent, a service, a holder key or a messenger. A landlord whose name pins no device list has this custody alone. (3) **A landlord that has neither custody has the slow path only**, the name update of H32, and MUST NOT claim fast revocation, in a conformance claim or to a party that relies on its class. (4) `tx_revoke_N` MUST reach its keepers before the list that names the entry is pinned. (5) The prepared spend is a bearer of revocation: whoever copies it can revoke that entry, which under H51 denies the landlord one name and gives nothing else. **The copies that one keeper holds cover the whole list.** One keeper that is compromised can revoke every name of the landlord, up to 1024, at every witness and for good; the recovery is a new seal for every name and a name update by the cold key. | None at a verifier | LIP-0029 O8.2, O8.10 and O9.3, and its security consequences, "a prepared spend is a bearer of revocation". That the keepers of the spend are the devices of the landlord's owner is the decision's. **NEW**: which device list it is; the floor of `ceiling` 2 for a keeping device, where keeping by every device is not taken, because a key in a messenger's client storage would then hold the revocation of the fleet; the cold floor; and point (3), by ruling |
| H52 | **Broadcasting again, and completing.** A keeper that broadcast `tx_revoke_N` broadcasts it again for as long as it can still confirm and its node shows it gone and the seal unspent. A landlord that revoked by a seal completes the revocation under H32. Without one of the two, a verifier that starts after the spend left every mempool admits the name, and nothing makes it converge with the witnesses. | None at a verifier | **NEW**. LIP-0027 H4.6; LIP-0008 section 5.3, EB5 |
| H32 | A name update completes the revocation: a new list without the entry, with a higher `seq` (H15). The landlord MUST make it, and makes it as soon as the cold key is at hand. Until it confirms, the entry stays in the list and refuses at every verifier that validated the spend. From its confirmation every verifier that takes the new list refuses the name by H41 as well. | None at a verifier | LIP-0029 O8.7. That the completion is a duty is **NEW**: O8.7 states what completes and obliges nobody |

**What a verifier reads of a seal.**

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H45 | **The seal read.** In the observation of the admission, against its named tip (H44), the verifier reads three facts of the seal outpoint on its own node. (a) **The funding transaction:** the octets of the transaction whose id is the `txid` of the seal, with the hash and the height of the block of the active chain that holds it, or the fact that no block of the active chain holds it (LIP-0021 O1.1, third fact; LIP-0022 B1.4). (b) **The spend state** of the output at `vout`, in the node's view with its mempool included: unspent; spent by a transaction in a block of the active chain; or spent by a transaction in the node's mempool. (c) **The spenders:** for an output that is not unspent, the exact octets of every transaction that the node holds which spends the outpoint, the one in a block of the active chain with the hash and the height of that block, and every one in its mempool. LIP-0021 O1.1 supplies fact (a) and neither (b) nor (c): they are further facts of the node that this section needs, and how a node supplies them, the lookup from an outpoint to its confirmed spender above all, is not specified here and no node was run for it. An answer that the node does not give, an error, and two reads that contradict each other prove nothing (H24). A definite answer that the transaction, the output or a spender does not exist is an answer and no failed read. | `CLASS_HISTORY_UNAVAILABLE` for a read that proves nothing | **NEW**. The form is that of LIP-0027 H2.3 to H2.5; LIP-0029 O8.9 names `gettxout` and no more |
| H46 | **When a seal exists.** A seal counts only when, in that read: its funding transaction is confirmed in the active chain at the named tip, at a height that is not above the height of the block that holds the name operation which carries the current pin; that transaction has an output at `vout`; and the script of that output is, octet for octet, a version 0 witness program of 20 bytes, a witness key hash. A funding transaction that is pending, unknown, confirmed above that height or removed by a reorganisation, an index without an output, and another script give no seal. The verifier records no closure for it and states no revocation, and the next observation decides again. **What a verifier knows of the script** is its octets, its form and the 20 bytes of a key hash, and so that exactly one key can spend the output. **What it cannot know**, from these or from any read: whose key that is; whether it is fresh or serves elsewhere; whether it still exists; whether a prepared spend exists, and how many transactions were signed with it. **What follows.** (1) At a verifier a revocation is every validated spend of the seal (H47), whoever signed and broadcast it, and not `tx_revoke_N` alone. A key that was kept against H26 can sign a second spend, and that spend also revokes. (2) A seal that pays a key of another party is revoked when that party moves its coins. (3) A seal that nobody can spend, because no spend was prepared or every copy is lost, makes an entry that no seal revokes, and no verifier can tell it from a sound one. (4) H25 is therefore a promise of the landlord's conduct, and a verifier vouches for it in no report. | `HOLDER_SEAL_NOT_LIVE`, without closure | **NEW**. LIP-0027 H2.3 and H2.6 for the existence on the chain; LIP-0023 for the script form. The height bound is the strict choice of the two that the review names, the other being a depth, which stays open. The single script form is chosen so that "validated" has one meaning (H47); admitting both address scripts of LIP-0021 is not taken |
| H47 | **A validated spend.** A transaction `T` is a validated spend of a seal when all of this holds. (1) The verifier has the exact octets of `T`, from its own node or from the record that its deployment keeps of that node's sightings (H28); a txid, a status word, a label of a caller and a flag that says "validated" are no octets. (2) An input of `T` spends exactly the seal outpoint. (3) The verifier's own node accepted `T` under the full rules of the chain, scripts and signatures included: `T` is in the mempool of that node in the observation, or in a block of its active chain at the named tip, or that record holds such a sighting with the tip at which it was made. (4) The verifier itself checks that input against the script of the seal on the octets: the witness of the input holds a signature and a public key, the hash of that key is the 20 bytes of the script, and the signature verifies under the signature digest of a version 0 witness program for the hash type that it carries, with the amount of the funding output. Every hash type counts: a signature of the seal's key over a spend of the seal is the act that revokes, whatever else it commits to. (5) The seal existed under H46 at the tip of the sighting. A spend of a seal whose funding is unconfirmed, or confirmed in no block of the active chain, validates nothing here: it refuses as `HOLDER_SEAL_NOT_LIVE` and records no closure. (6) The verifier read every spender that its node holds (H45, fact (c)). One that meets (1) to (5) is enough; a second, conflicting one changes nothing, because it also spends the seal. | | **NEW**. LIP-0008 section 5.1 defines "validated" for the seal of a grant against the grant's authenticated seal binding; an entry carries no key and no script, so the script of H46 on the chain stands in its place. Closing on the node's state without the spending transaction, as LIP-0027 H2.4 does for a stop coin, is not taken, by ruling |
| H48 | **The order inside step 8.** The first that applies gives the outcome. (1) The seal is another outpoint of the admission (H49): `HOLDER_SEAL_ALIAS`. (2) The journal holds a closure of the seal: `HOLDER_REVOKED`, whatever the node shows and whichever entry names the seal (H30). (3) The journal binds the seal to another entry (H38): `HOLDER_SEAL_REUSED`. (4) The read of the funding transaction proves nothing: `CLASS_HISTORY_UNAVAILABLE`. (5) The seal does not exist under H46: `HOLDER_SEAL_NOT_LIVE`. (6) The read of the spend state or of a spender proves nothing: `CLASS_HISTORY_UNAVAILABLE`. (7) The output is not unspent and a spender is a validated spend (H47): the verifier writes the closure (H28) and refuses as `HOLDER_REVOKED`. (8) The output is not unspent and no spender is a validated spend, among them a spender that the node cannot supply: `HOLDER_SEAL_NOT_LIVE`, without closure. (9) The output is unspent: the step passes. | As stated | **NEW** |
| H49 | **A seal is no other outpoint.** In a class admission the seal of the entry differs from every outpoint that the proof path under verification names or reads: the seal of the child and of every grant above it, and the output after each of them in the same transaction, which is the linkage output of LIP-0023 C2.3; the coin of the child's row (LIP-0026 section 3); the stop coin of that row (LIP-0027); and the current output and the pinned registration of `L` and of the recipient name. The verifier compares on the signed octets and on the outpoints that it read in the same admission. A collision with an outpoint that is not in front of the verifier, a device seal among them, it cannot see, and H26 binds the landlord for those. | `HOLDER_SEAL_ALIAS` | **NEW**. LIP-0027 H2.2 and its code `ROW_STOP_ALIAS`; LIP-0026 section 3 for the coin. Without it the spend of one outpoint performs two acts of the protocol, and H13 would be false for that seal |

**What a closure is.**

| Rule | Requirement | Refusal | Modelled on |
| --- | --- | --- | --- |
| H28 | **The enforcement closure.** A verifier that holds a validated spend (H47) of the seal of an entry of a list that it took journals the closure of that entry durably, before any further admission through a landlord class. It looks at every admission, in step 8 of section 10.6 and again before the effect (H44). Between admissions it MAY watch the seals that its journal binds; the **watcher journal** of its deployment, the record that follows the mempool and the blocks of the verifier's own node and keeps the octets of every transaction that spends a watched seal with the tip of its sighting, is the source of that evidence for a spend that has left the node's view. This text names it and does not specify it. The closure is keyed by the seal outpoint (H39) and holds: the outpoint; the landlord's name and registration, the `name` and the `key` of the entry; the txid of the validated transaction and the SHA-256 of its octets; whether it was sighted in the mempool or in a block, with that block's hash and height; and the hash and the height of the named tip of the sighting. A verifier that validated no such transaction writes no enforcement closure, whatever a node, a gateway or a caller reports. | A closure that cannot be written: H43 | LIP-0029 O8.3; LIP-0008 section 5.1. The record and the watcher journal are **NEW** |
| H29 | After a closure the verifier admits the name of that entry through no class. Every other entry counts as before, an entry with the same `key` included, and the landlord's v4 grants are untouched (H13). A rollback cannot restore the entry: a list of a lower `seq` refuses (H23), every list that names the entry names the same closed seal, and a journaled closure is not lifted by a later list, a name update, a value in the inline form (H42), eviction, replacement, non-confirmation or a reorganisation, the one that removes the funding of the seal included. This rule holds for a verifier that validated the spending transaction on its own node. It does not hold for a reader of H50, and not for a verifier whose journal is lost (H43). | `HOLDER_REVOKED` | LIP-0029 O8.4 and case S29-18; LIP-0008 section 5.1 |
| H30 | A seal outpoint that was spent is never named again by an entry. An entry that names an outpoint of which the verifier holds a closure refuses, whatever `name` and `key` it carries, in whatever list and of whichever landlord. | `HOLDER_REVOKED` | LIP-0029 O8.5. Across landlords: **NEW** (H39) |
| H31 | A seal that the node does not show as an unspent output, where the verifier holds no validated spend of it, refuses the admission and records no closure: the spend may lie in a block whose transaction the node cannot supply, or the spender did not pass H47. A seal that does not exist as H46 asks refuses in the same way. Neither is reported as a revocation, and a read that failed is reported as neither (H24). The refusal lasts while the node shows the output so; it is a verdict on one observation and no journaled closure, and where a reorganisation makes the output unspent again, this verifier admits the name while a witness refuses it for good. | `HOLDER_SEAL_NOT_LIVE`, without closure | LIP-0008 section 5.1, last paragraph; LIP-0027 H2.6 and its code `ROW_STOP`. The code is **NEW**; the first text gave `HOLDER_REVOKED` here |

**A reader that cannot validate a spend.**

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H50 | **The non-witness.** H28 and H29 stand for a verifier that validates the spending transaction on its own node. A verifier that reads the chain through a gateway which returns only the state of a seal (unspent, which is confirmed and not spent in the mempool; unconfirmed; spend pending; not in the confirmed set) is a **non-witness** for closures that begin in the mempool. (1) It admits on unspent alone and refuses on every other state. (2) It records no enforcement closure, for no state and no sequence of states: a state is a label, and a label is consistent with a valid spend, with a transaction that a relay kept and no node would confirm, and with an error of the gateway. (3) Where it journaled the seal as unspent earlier and later sees it absent from the confirmed set, it MAY keep an **observe-grade closure**. That record is named so wherever it is stored or reported; it is never used for enforcement, so it refuses no admission, is no closure of step 8, is not reported as `HOLDER_REVOKED`, and does not stand against a later unspent state. The reason is twofold: the reader validated no spending transaction, and the absence of a seal also follows a reorganisation that removed its funding. (4) It checks the script and the height of H46 where the gateway supplies the funding transaction against a named tip, and otherwise does not check them. (5) Its operator's conformance claim says that it is a non-witness, that it admits a revoked name again after an eviction or a reorganisation that it could not validate, and which conditions of H46 it does not check. An enforcement closure needs three things that such a gateway does not give: the octets of the spending transaction, validated by the reader against the script of the seal (H47); every spender that the node holds; and one named tip for the read. The watcher journal of H28 is the deployment's source of that evidence. | `HOLDER_SEAL_NOT_LIVE` for every state but unspent; `CLASS_HISTORY_UNAVAILABLE` for a read of the gateway that fails | **NEW**, by ruling. LIP-0008 section 5.1: "a caller's label or a reported transaction ID is not branch proof" |

**The return of a name, and a stolen key.**

| Rule | Requirement | Refusal | Modelled on |
| --- | --- | --- | --- |
| H33 | A name whose entry was sealed off counts again only by a new entry: a later list, with a higher `seq`, that names it with another seal, which exists under H46 and is unspent, pinned by a name update that the name-owner key signs. The closure of H28 is the closure of the entry with its seal, and not of the name or of the key for ever. | | LIP-0029 O9.1 for the slow path. That the closure is of the entry is **NEW**, and the ruling keeps it: LIP-0029 O8.4 closes the device, and O3.20 has a device return with a new key |
| H35 | **A stolen holder key.** The landlord answers the theft of a key by the spend of the seal of every entry whose `key` is that pin: one prepared spend for each such entry, each broadcast by a keeper of H27. There is no seal of a key: no one spend revokes every entry of a pin. Until the last of the spends is validated at a verifier, the names whose seals are unspent still pass there with whatever value the thief writes. The spends move no name: the names stay with whoever holds the key. The landlord then registers names under another key and lists them, or uses reserve entries of another key (H37), and completes the revocation by a list without the sealed entries (H32). Removing the entries by a list alone is no answer to the theft (H41). | | **NEW**; follows from H2 and H25. LIP-0029 O8.10 for the broadcast. A master seal for each key is not taken, by ruling: it would bring back the reach of one spend over every name of a key, which the entry by name removed |

**What happens to grants.** An entry and its holder issue no grant (H4), so
the spend of a seal revokes no grant that either issued: there is none. What
the spend ends is the admission of that one name through a landlord class,
from the moment at which a verifier validates it. Three things stay as they were:

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
from the moment at which a verifier validates the spend on its own node, in
its mempool, that name passes no class at that verifier, and the agents
beside it are not touched. The cold name-owner key is not needed for that,
and it completes the revocation later with a list that drops the entry
(H32). A thief of a holder key owns the names that pay it and rewrites their
values, and with them the keys under which those names sign requests; H35 is
the answer.

`k_N` is a holder seal key. H46 and H51 fix the form of its script, the one
input of `tx_revoke_N` and its hash type. The amount of the seal, the fee of
`tx_revoke_N` and whether an output of it lets a child transaction raise the
fee are open, as they are for a device seal (LIP-0029 section 8.3), and the
fast path is not claimed until they are closed (H51). If every copy of
`tx_revoke_N` is lost, `S_N` can no longer be spent, and only the name update
of H32 removes the entry; that removal holds at the verifiers that take the
new list, and a verifier that never took it admits the name from an older
list after a reorganisation (H41).

**The limits of this section, in one place.** A seal revokes fast only where
the landlord made it as H26 and H51 say, kept its spend as H27 says and
broadcasts it as H52 says; no verifier checks one of these. A closure is
durable only at a verifier that validated the spending transaction on its
own node and still holds its journal. A verifier that could not validate
the spend refuses while its view shows the seal not unspent and records
nothing. A reader behind a gateway of states is a non-witness. And until the
amount, the fee and the fee-raising output are closed, nobody claims the
fast path at all.

#### 10.8. A removed entry and a sealed-off entry

| | Removed entry | Sealed-off entry |
| --- | --- | --- |
| The act | A name update of the landlord that pins a new list, with a higher `seq`, without the entry (H15) | The broadcast of `tx_revoke_N` (H25) |
| Who acts | The name-owner key of the landlord name, which is cold | Any keeper of the prepared spend; no key is used at that moment (H27) |
| A new list | Needed | Not needed; the entry stays in the list until H32 |
| From when | From the block that confirms the update, at a verifier that takes the new list (H40). While the update is pending, the old list is the list, and class checks of the landlord refuse without closure (H11, H15) | From the first validated sight of the spend, in the mempool of each verifier's own node (H28, H47) |
| What a verifier records | The new head and a removal mark of the entry, with the `seq` of the list that dropped it (H40, H41) | A durable closure of the entry, keyed by its seal outpoint (H28) |
| After a reorganisation that removes the act | At a verifier that took the dropping list: the older list is the list again (H23), and the entry stays refused by its mark (H41). At a verifier that never took it: the entry of the older list admits its name | At a verifier that validated the spend: the closure stays (H29). At a verifier that did not: the seal is unspent again, and the name is admitted (H31) |
| Return | A later list with a higher `seq` than the dropping one may hold the same entry again, with the same `name`, `key` and `seal`, while that seal is unspent and not closed (H41) | Never for that entry; the name returns only in a new entry with a new seal (H33) |
| Refusal | `CLASS_HOLDER` | `HOLDER_REVOKED` |
| An answer to a stolen key | No. It holds only where the dropping list was taken, and it needs the cold key and a confirmation | Yes, entry by entry (H35) |
| Other names of the same key | Not touched | Not touched |
| The landlord's v4 grants | Untouched (H13) | Untouched (H13) |
| The name | Stays with its key holder | Stays with its key holder |

The row "after a reorganisation" follows section 11 SH5 for the removed
entry: a record that a removed head dropped stays refused at the reader that
took that head. The first text of this section had the entry return, as a
fact of a history that the reorganisation replaced; that reading is
withdrawn by ruling, because a removal is an act that the owner
of the name signed and that the verifier validated, like the acts that
LIP-0008 section 5.2 and SH5 journal. The two columns still differ in who
holds the record: a removal binds the verifiers that took the dropping list,
and no depth of confirmation at which a verifier takes a new pin is stated
yet, so one block makes the mark and a verifier that was away for that block
has none. Removal alone is therefore no answer to a compromise. A landlord
that must not see a name return spends its seal.

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
| M3 | **What a verifier does with each form meanwhile.** A reader of this LIP MUST parse both forms, so that a landlord value in the inline form keeps its grant key and its grants. For a class check against a landlord in the inline form it takes the holders from the inline member under rules 1 to 4 and makes checks (c) and (d) on them as version 0.1.51 did: every name that an inline holder holds passes check (c), and a value that any inline holder wrote passes check (d). Steps 0 and 1 of section 10.6 are made for every landlord, and steps 2 to 6 and 8 have no subject for a value in the inline form. **The inline form is read only for a landlord of which the verifier's journal holds no form mark.** Once the verifier took a pinned list for a landlord, a value of that landlord in the inline form gives no holder (H42), so that a return to the inline form lifts no closure and no removal, and admits no name. An inline holder is a key and has no seal: it is removed only by a name update, with the consequence of rule 7, and one name of it cannot be revoked alone. For a landlord in the pinned form the verifier follows section 10.6. | The codes of LIP-0026 section 9; `HOLDER_FORM_DOWNGRADE` (H42) | **NEW** |
| M4 | **What a landlord does.** From this version a landlord MUST NOT write the inline member into a value that did not carry it, MUST NOT add a pin to an inline list, and MUST NOT write the inline member into a value of a name that ever carried `swarma-holders`. It moves to the pinned form by one name update that removes `holders` from `landlord` and writes `swarma-holders` with the pin of a list that holds one entry for each agent and station name that it means to keep, each with the key that holds the name and with a seal made under H26 and H51, confirmed (H36), and its prepared spend placed under H27 before the update is broadcast. | None at a verifier for the writer's duties: the landlord's tool refuses. A verifier answers a return to the inline form by H42 | **NEW** |
| M5 | **The cost of the move.** The update of M4 changes the octets of `swarma`. It is the last update of that landlord to which rule 7 applies: every v4 grant that the landlord issued under the inline form refuses from the block that confirms it and is issued again, and a verifier that observes it under LIP-0008 section 5.2 records the closure. From then on H13 holds. A landlord whose value never carried the inline member moves at no cost to its grants: it adds `swarma-holders`, and `swarma` stays. | | LIP-0008 sections 3 and 5.2 |
| M6 | A landlord that added the inline member to a value which had been `{"landlord":{"grant":"<grant key>"}}` would, by removing it, write a `swarma` value that it replaced, which LIP-0008 J6.7 forbids. Such a landlord moves with a new grant key in the update of M4. A landlord whose first `swarma` value already carried the inline member keeps its grant key. | | LIP-0008 section 5.2, J6.1 and J6.7 (Draft, agreement pending) |
| M8 | The move narrows what passes. Under the inline form every name that a listed key holds and wrote is admitted; under the pinned form only the names that the list names. A landlord lists every name in use before it moves, and a name that it leaves out refuses `CLASS_HOLDER` from the block of the update. | `CLASS_HOLDER` | **NEW**; follows from H34 |
| M7 | A landlord with live v3 grants moves only after every verifier of those grants reads this section, as H16 says. A reader of version 0.1.51 reads the inline form and skips `swarma-holders`; a reader before version 0.1.51 refuses the inline form and skips `swarma-holders`; a LIP-0004 reader refuses both. | | Section 6; the closing text of section 10 in version 0.1.51 |

No implementation of version 0.1.51 is claimed, and this text knows of no
landlord name that carries the inline member. The date after which a reader
stops honouring the inline form is open; until the owners set it, M3 stands,
and with it the form mark of H42 is mandatory at every verifier: it is the
only thing that keeps a sealed-off name refused while the inline form is
still read.

#### 10.10. Cases

Each case pairs a valid control with its refusal. The landlord `id/acme` is
`L`, and the keepers of its prepared spends are the devices `P` and `M`.
List 3 is the example of section 10.2: `K1` holds `id/acme-worker-7` and
`id/acme-worker-8`, and `K2` holds the reserve `id/acme-reserve-01`. `Y` is
the executor of another owner that admits children of a row whose class
holds `L`; it reads its own node, validates spends under H47 and keeps the
journal of H39. `W` is a second such verifier where a case sets a witness
beside a newcomer, and `Z` reads the chain through a gateway of states
(H50). Unless a case says otherwise, the journal of the verifier is intact,
every seal exists under H46, and the child signs the owner key that holds
the recipient name at that moment, so that the proof of the recipient by
name passes (LIP-0026 R9.9) and the class checks are reached.

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S10-1 | The confirmed value of `L` pins list 3. A child names `id/acme-worker-7`, whose output pays `K1` and whose value `K1` wrote; the presenter supplies list 3, and `Y`'s node shows the seal of the entry confirmed below the block of the pin, with a witness key hash script, and unspent: admitted, and `Y` takes list 3 (H40) and caches it | The same child with the octets of list 3 and one added space: `HOLDER_LIST_MISMATCH`. The same child with no list, at a verifier with an empty cache: `LIST_UNKNOWN`, and the presenter presents again with the list. `id/acme-worker-9`, which `K1` holds and wrote and which points to `L`, and which no entry names: `CLASS_HOLDER` (step 6). |
| S10-2 | `L` issued the v4 grant `G` at recent block `R`. After `R` the landlord pins list 4, which adds an entry, and later list 5, which drops one: `G` is admitted throughout, because the owner and `swarma` did not change (H13) | An update of `L` that replaces the grant key: `G` refuses, as LIP-0008 section 3 says, whatever the pin. A verifier that records a closure of `G` for the update to list 4 is wrong. |
| S10-3 | `P` broadcasts `tx_revoke_N` for `id/acme-worker-7`. `Y`'s node takes it into its mempool, `Y` validates it under H47 and journals the closure of the entry. `id/acme-worker-8`, which the same `K1` holds, is admitted as before, and `G` and every other v4 grant of `L` stay admissible | A child that names `id/acme-worker-7`, at `Y`, while list 3 still names it: `HOLDER_REVOKED`. After a reorganisation that removes the block with the spend: still `HOLDER_REVOKED`, because the closure is journaled (H29). |
| S10-4 | `id/acme-worker-8` is transferred to `K2`, a key that list 3 names for another entry. The child signs `K2` | A child that names it: `CLASS_HOLDER` (step 7), because the entry's `key` is `K1` (H34). After list 4 names `id/acme-worker-8` with `K2` and a new seal (H38) and confirms, and before `K2` updates the value: `CLASS_WRITER` (step 9). After an update of the value by `K2`: admitted. List 4 with `K2` and the seal of the old entry: `HOLDER_SEAL_REUSED`. |
| S10-5 | The reserve `id/acme-reserve-01` is registered to `K2` before list 3 is pinned, with a value that is no agent binding (H37). `K2` writes an agent binding that points to `L`: from the block that confirms that update a child that names it is admitted, with no update of `L` | Before that update: `CLASS_LANDLORD` (LIP-0026 R9.4). A landlord that pinned list 3 before the registration, against H37: another party registers the name first and sends it to the address of `K2`, and a child that signs `K2` refuses as `CLASS_WRITER` (step 9); the same party keeps the name, and a child that signs that party's key refuses as `CLASS_HOLDER` (step 7), for as long as the party keeps it. |
| S10-6 | `K1` is stolen. `P` broadcasts the prepared spends of both entries of `K1`; `Y` validates both and journals two closures, and the reserve of `K2` is not touched (H35) | A child that names either name of `K1`: `HOLDER_REVOKED`. After only the first spend, a child that names `id/acme-worker-8` with a value that the thief wrote: admitted, which is why H35 asks for every entry of the pin. |
| S10-7 | List 4 drops the entry of `id/acme-worker-8` without a spend of its seal; after the update confirms and `Y` takes list 4, the name refuses `CLASS_HOLDER`. List 5 holds the same entry again, with the same unspent seal: admitted again from the take of list 5 (H41) | List 5 names `id/acme-worker-7`, sealed off in S10-3, with the same seal: `HOLDER_REVOKED` (H30). A later name update that pins `seq` 3 while the update of `seq` 5 stays in the active chain: `HOLDER_LIST_ROLLBACK`. List 6 names `id/acme-worker-7` with a new seal that exists and is unspent: admitted (H33). |
| S10-8 | The update that pins list 4 is in the mempool: list 3 is the list (H11) | A class check of `L` in that time: `CLASS_LANDLORD_PENDING` (LIP-0026 R9.5). A verifier that takes list 4 before its update confirms is wrong. |
| S10-9 | A landlord value in the inline form with two holders, and no `swarma-holders`: every name that the first inline holder holds and wrote is admitted as in version 0.1.51 (M3) | The same value with a top-level `swarma-holders`: no holder, `CLASS_HOLDER`; the grant key still reads, and the landlord's grants are judged as before (M2). A value with `swarma-holders` twice: `HOLDER_PIN_INVALID`, and the grant key still reads (H9). |
| S10-10 | A landlord in the inline form moves under M4: its v4 grants of before refuse and are issued again, once (M5) | The same landlord then pins list 2: no grant refuses (H13). |
| S10-11 | The grant of the agent `id/acme-worker-8` is ended by the issuer's spend of that grant's seal | The spend of the seal of the entry of `id/acme-worker-8`, with the grant's own seal unspent: the grant is not closed; where its admission passes through a class of `L` it refuses `HOLDER_REVOKED` at each admission, and elsewhere it is admitted. The name stays with the holder of `K1`. |
| S10-12 | The control of S10-1: the funding transaction of the seal is confirmed at a height that is not above the block of the pin, and its output is a witness key hash (H46) | The funding transaction is in the mempool only; it is unknown to the node; it is confirmed above the block of the pin; the output has another script; the transaction has no output at `vout`: each `HOLDER_SEAL_NOT_LIVE`, with no closure. The node does not answer the read of the funding transaction: `CLASS_HISTORY_UNAVAILABLE`. A spend, in the mempool, of a seal whose funding is unconfirmed: `HOLDER_SEAL_NOT_LIVE`, with no closure (H47, point 5). |
| S10-13 | The spend of the seal of `id/acme-worker-7` confirmed while `Y` was away. `Y`'s node shows the output spent and supplies the spending transaction from its block; `Y` validates it and journals the closure: `HOLDER_REVOKED`, also after a reorganisation that removes that block | The same, where the node shows the output spent and cannot supply the spender: `HOLDER_SEAL_NOT_LIVE`, with no closure, at every admission while the view stands (H31, H48 point 8). After a reorganisation that removes the spend: this verifier admits the name, and `W`, which validated the spend, refuses it as `HOLDER_REVOKED`. A spender whose seal input does not verify against the script: no closure, `HOLDER_SEAL_NOT_LIVE`. |
| S10-14 | `W` validated the spend of S10-3 in its mempool and holds the closure. `Y` starts after the spend left every mempool unconfirmed, and its node shows the seal unspent: `Y` admits `id/acme-worker-7`. `P` broadcasts the spend again (H52); `Y` validates it and journals the closure | At `W`, throughout: `HOLDER_REVOKED`. At `Y` after the second broadcast: `HOLDER_REVOKED`. Without H52 and H32 the two never converge. |
| S10-15 | Step 8 of an admission at `Y` reads the seal unspent, and no spend reaches the node before the effect: the read before the effect (H44) passes, and the effect is made | The prepared spend reaches `Y`'s mempool after step 8 and before the effect: the read before the effect validates it, `Y` journals the closure, and the admission refuses as `HOLDER_REVOKED` with no effect. The tip moves between the two reads: the admission is void, with the code of LIP-0022 and no closure. A closure that `Y` wrote during an observation which then turned out void: it stands (H44). |
| S10-16 | A landlord `L2` of which `Y` never took a pinned list has a value in the inline form: the names of its inline holders are admitted as in version 0.1.51 (M3) | After S10-3 the value of `L` is updated to the inline form with `K1` as a holder. A child that names `id/acme-worker-7`, at `Y`: `HOLDER_FORM_DOWNGRADE`. A child that names `id/acme-worker-9`, which `K1` holds and wrote: `HOLDER_FORM_DOWNGRADE`. The grant key of `L` still reads. `L` then pins list 7, which names `id/acme-worker-7` with its old seal: `HOLDER_REVOKED`. A verifier whose journal was started anew after S10-3 admits both names from the inline value and says that it is a newcomer (H43). |
| S10-17 | List 4 holds the entry of `id/acme-worker-7` with the same `key` and the same seal `S` as list 3: the binding is the same, and the name is admitted | List 4 drops `id/acme-worker-7` and names `id/acme-worker-9` with `S`: `HOLDER_SEAL_REUSED` for `id/acme-worker-9`. The list of another landlord, `L2`, names `S` for a name of its own, at a verifier that bound `S` to `L` first: `HOLDER_SEAL_REUSED`. After a validated spend of `S`: every entry that names `S`, of `L` or of `L2`, refuses as `HOLDER_REVOKED` (H30, H48 point 2), also after a reorganisation that removes the spend. |
| S10-18 | The journaled head of `L` at `Y` is `seq` 5 with the hash `h5`, carried by the update `U5`, which is in the active chain. A later update of `L` changes `nostr` and carries the same pin: step 3 passes, and nothing is taken | A later update pins `seq` 5 with another hash while `U5` is in the active chain: `HOLDER_LIST_ROLLBACK`. The same pin after a reorganisation that removed `U5`: taken through the reorganisation branch (H23, point 4), and every closure and removal mark stays. The read of whether `U5` is in the active chain fails: `CLASS_HISTORY_UNAVAILABLE`. |
| S10-19 | The value of `L` pins `seq` 6, and nobody supplies list 6 to `Y`: `LIST_UNKNOWN`, and the journaled head of `Y` stays at `seq` 5 (H40). `L` then pins `seq` 7 with a list that `Y` is given: taken | List 6 is supplied with a `schema` of another string: `HOLDER_LIST_INVALID`, and the head stays at `seq` 5. A verifier that raised its floor to 6 on the read of the pin is wrong. |
| S10-20 | `Y` took list 4, which dropped the entry of `id/acme-worker-8`. A reorganisation removes the update of list 4, and the confirmed value pins list 3 again: `Y` takes list 3 through the reorganisation branch, and `id/acme-worker-7` is admitted from it | A child that names `id/acme-worker-8`, at `Y`, under list 3: `CLASS_HOLDER` (step 6, H41). At `W`, which never took list 4: admitted. After list 5 holds the entry again and `Y` takes it: admitted at `Y`. A list of `seq` 4 with other octets that holds the entry, taken through the reorganisation branch: still `CLASS_HOLDER`, because the mark is lifted by a higher `seq` alone. |
| S10-21 | `Y` validates a spend and writes the closure; the next child of another landlord's class is judged as before | The write of the closure fails: the child for which it was due refuses as `HOLDER_REVOKED`, and every later child of every landlord class refuses as `JOURNAL_LOST`, also after a restart, until the operator restores the journal or starts it anew by a recorded act (H43). A take of a list that cannot be written: `JOURNAL_LOST` for that admission, and the same state. A replica of `Y` with a journal of its own that reports `Y`'s closures: wrong. |
| S10-22 | The seal of the entry is an outpoint that the admission names nowhere else: the alias check passes | The seal of the entry is the seal of the child; the output after the seal of the parent; the coin of the child's row; the stop coin of that row; the current output of `L`: each `HOLDER_SEAL_ALIAS` (H49), before any read of the seal. |
| S10-23 | `Z` reads the seal of `id/acme-worker-8` through a gateway that answers unspent: admitted | The gateway answers spend pending: `HOLDER_SEAL_NOT_LIVE`, and `Z` records no closure. It answers unspent again after the spend was evicted: `Z` admits the name, where `W` refuses it for good. It answers unconfirmed: `HOLDER_SEAL_NOT_LIVE`. After an earlier unspent it answers "not in the confirmed set": `HOLDER_SEAL_NOT_LIVE`, and `Z` may keep an observe-grade closure; after a reorganisation the gateway answers unspent, and `Z` admits the name, the observe-grade record notwithstanding. A `Z` that reports `HOLDER_REVOKED` or refuses by that record is wrong (H50). The gateway does not answer: `CLASS_HISTORY_UNAVAILABLE`. |
| S10-24 | The current value of `L`, which carries the pin, was written by the pinned owner of `L`: check (b) passes and the pin is read | The writer check of that output gives "written by another": `CLASS_VALUE_UNAUTHORIZED`. It gives "unsupported": `CLASS_HISTORY_UNAVAILABLE` (LIP-0026 R9.5 and R9.8). In neither is a pin read. |
| S10-25 | The octets of list 3 under their pin: the four checks of H53 pass | Octets of 262145 bytes that also hash to another value: `HOLDER_LIST_INVALID` (check 1 before check 2). A list whose octets hash to the pin and whose `network` is `test`: `HOLDER_LIST_INVALID` (check 3). A valid list of `regtest` under its pin at a verifier of `main`: `HOLDER_LIST_MISMATCH` (check 4). A list that hashes to another value and also has an unsorted `holders`: `HOLDER_LIST_MISMATCH` (check 2 before check 3). |

#### 10.11. Vectors

[`vectors/LIP-0010/holders-vectors.json`](../vectors/LIP-0010/holders-vectors.json)
holds 28 landlord values of the inline form, 9 valid and 19 refused, and
five rows of capacity with the value of each. They follow rules 1 to 8 of
section 10.9, which the file cites as 10.1 to 10.8, and no byte and no
outcome of the file changes. A refused value holds one defect, states the
rule that refuses it and names a valid neighbour. The expected outcomes were
stated by hand, computed by one implementation and decided again by a second
one that shares no code with the first; neither is published here, and both
come from the author of that text. The claim that no outcome of that file
and of the class file changes rests on a reading of the inline rules against
their form of version 0.1.51. Nobody ran the existing checkers for it, and
until somebody does, it is a claim and no evidence.

The pinned form has no published vector yet, and this section fixes no
octet of one. It states what a vector set holds, so that the rules of
sections 10.6 to 10.9 can be tested: three groups, the facts that an
admission states, and the vectors by rule. A refused vector holds one
defect, states the rule, the step or the point of an order, and the code
that refuse it, and names the valid neighbour from which it differs in that
defect. A compound vector holds two defects on purpose and is marked so: it
fixes which of two codes comes first. **Every rule of section 10 that has a
refusal, every step of section 10.6 and every point of H23, H48 and H53
names at least one vector below**; a rule that the table leaves out is a
defect of the table.

**The facts of an admission.** A vector of the group `admissions` is a
decision on stated facts, in the manner of the admissions of
`vectors/LIP-0026/class-vectors.json`. It reads no chain. It states these
facts, each with a closed set of values, and its expected outcome: admitted,
or a code with the step and the point that gives it, and the records that
the verifier writes.

| Fact | Values |
| --- | --- |
| `reader` | `own-node`, which validates spends (H47); `gateway`, the non-witness of H50 |
| `tip` | The hash and the height of the named tip, and whether the second read of the tip equals the first |
| `child` | The recipient name and the owner key that the child signs |
| `recipient` | The key that controls the current output of the recipient name; who wrote its value: that key, another key, unsupported; whether the value is an agent binding that points to `L` |
| `landlord` | The name and the registration of `L`; the form of its confirmed value: pinned, inline, both, neither; the pin; the name operation that carries the pin, with its block; the writer of the value: the pinned owner, another, unsupported; whether an operation of `L` is pending |
| `list` | The list, by reference to a vector of the group `lists`, and where the verifier has it from: its cache, the presentation, nowhere |
| `seal.funding` | For the seal of the entry: confirmed, with the height and whether that height is above the block of the pin; unconfirmed; absent; the read failed. The script of the output: a witness key hash; another script; no output at the index |
| `seal.spend` | Unspent; spent in the mempool; spent in a block of the active chain; the read failed |
| `seal.spender` | None; supplied, and its seal input verifies against the script; supplied, and it does not; not supplied by the node; supplied by the watcher journal with its sighting. For the reader `gateway`: the state that the gateway returns, one of unspent, unconfirmed, spend pending, not in the confirmed set, no answer |
| `seal.at_effect` | The same three facts at the read before the effect (H44), where they differ from those of step 8 |
| `journal.state` | Intact; lost; fenced; started anew, with the recorded act; whether the next write succeeds |
| `journal.head` | None, or the `seq`, the `sha256` and the name operation of the journaled head, and whether that operation is in the active chain at the tip |
| `journal.form_mark` | Present or absent for `L` |
| `journal.bindings` | For each seal that the vector names: the landlord, the `name` and the `key` that it is bound to, or none |
| `journal.removals` | For each entry that the vector names: the `seq` of its removal mark, or none |
| `journal.closures` | For each seal that the vector names: none; an enforcement closure, with its sighting; an observe-grade record |
| `proof_path` | The outpoints that the alias check compares: the seals of the child and of the grants above it, the outputs after them, the coin and the stop coin of the row |

**The vectors by rule.**

| Group | Rule | Valid | Refused, each paired with a valid neighbour |
| --- | --- | --- | --- |
| `lists`: the exact octets of a list, with their length and SHA-256 | H1 | The example of section 10.2; a list with one entry | A fourth member in an entry; a missing `seal`; `key` before `name`; `name` twice in one entry. In the seal object: a third member; `vout` before `txid`; `txid` twice; a missing `vout` |
| `lists` | H2 | A list in which two entries have one `key` | Two entries with one `name`; two with one `seal` |
| `lists` | H5, the encoding | A list with an empty `holders` | Entries not in ascending order of `name`; a `name` that is a prefix of the one before it and stands after it; a space after a comma; a trailing newline; a string with the escape `A`; a string with a non-ASCII character; a sixth top-level member; a top-level member twice; `owner` before `network` |
| `lists` | H5, the values | The valid lists above | A `schema` of `swarma-device-list/1`; a `network` of `test`; a `name` with an uppercase letter; a `name` without `id/`; a `name` of 253 bytes after `id/`; a `key` of 64 characters; a `key` that begins with `04`; a `key` whose x coordinate is on no point of the curve; a `txid` in uppercase; a `txid` of 63 characters |
| `lists` | H5, the numbers | `seq` 1; `seq` 9007199254740991; `vout` 0; `vout` 4294967295 | `seq` 0; `seq` 9007199254740992; `seq` `-1`; `seq` `1.0`; `seq` `1e2`; `seq` `01`; `seq` as a string; `vout` 4294967296; `vout` `-1`; `vout` with a leading zero; `vout` `1.0` |
| `lists` | H6 | A list of 1024 entries; a valid list of exactly 262144 bytes | 1025 entries; a list of 262145 bytes |
| `pins`: the exact text of a landlord value, with the list that it pins | H8 | The value of section 10.2 with `seq` 3; the same beside `nostr` and `swarma-devices`; a value without the member (no name listed) | `sha256` before `seq`; a third member; `sha256` in uppercase or of 63 characters; `seq` as a string; `seq` 0; a space inside the member |
| `pins` | H9 | The valid values above | The member twice; a member `Swarma-Holders` beside it; a member whose name is written with an escape and decodes to `swarma-holders`, alone and beside the exact member. Each leaves the grant key readable |
| `pins` | H10 | The valid values above | A pin whose `seq` differs from the list's; a pin whose hash is of other octets; a list whose `owner` is another name; a list of the other network |
| `pins` | H53, compound | The valid values above | The four compound vectors of case S10-25 |
| `pins` | M1, M2 | A value in the inline form; a value in the pinned form | A value with the inline member and the pin: no holder, and the grant key reads |
| `admissions` | Steps 1 to 9 as first stated | The valid controls of S10-1 to S10-11 | The refusals of S10-1 to S10-11, each with its code and the step that gives it, and each with the owner key that the child signs |
| `admissions` | Step 0, H43 | The control of S10-21 | The refusals of S10-21: a closure that cannot be written; a take that cannot be written; a journal that is lost; a journal that is fenced; a journal that was started anew, which admits what a witness refuses |
| `admissions` | Step 1, H42, M3 | The control of S10-16 | The refusals of S10-16 |
| `admissions` | Step 3, H23, H40 | The controls of S10-18 and S10-19 | The refusals of S10-18 and S10-19; a lower `seq` carried by a later operation (S10-7) |
| `admissions` | Step 6, H41 | The control of S10-20 | The refusals of S10-20 |
| `admissions` | H38 | The control of S10-17 | The refusals of S10-17; the last refusal of S10-4 |
| `admissions` | H45, H46 | The control of S10-12 | The refusals of S10-12, one vector for each state of `seal.funding` and of the script |
| `admissions` | H47, H28, H29, H31 | The controls of S10-13 and S10-14 | The refusals of S10-13 and S10-14: a witness and a newcomer on one trace; a spender that is not supplied; a spender that does not verify; an evicted spend; a spend that a reorganisation removed |
| `admissions` | H48, compound | The control of S10-1 | A seal with a journaled closure that is also bound to another entry: `HOLDER_REVOKED`. A seal that is an alias and has a closure: `HOLDER_SEAL_ALIAS`. A seal whose funding is unconfirmed and whose spend-state read fails: `HOLDER_SEAL_NOT_LIVE`. A seal whose funding read fails and whose output would have another script: `CLASS_HISTORY_UNAVAILABLE` |
| `admissions` | H49 | The control of S10-22 | The refusals of S10-22 |
| `admissions` | H44 | The control of S10-15 | The refusals of S10-15 |
| `admissions` | H50 | The control of S10-23 | The refusals of S10-23, one vector for each state of the gateway |
| `admissions` | Check (b) before the pin | The control of S10-24 | The refusals of S10-24 |
| `admissions` | H34, H37 | The controls of S10-4 and S10-5 | The refusals of S10-4 and S10-5 |

H16, H26, H27, H36, H51, H52, M4 and the first duty of H37 bind a landlord
and have no refusal at a verifier. They have no vector of these groups; a
vector for a landlord's tool is another set, which this section does not
describe.

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
| SH2 | The member names are registered here, each with the LIP that defines its head document: `swarma-devices`, whose head document is the device list (LIP-0029 section 3.2), `swarma-certs`, whose head document is the head of LIP-0016 section 2, and `swarma-holders`, whose head document is the holders list of a landlord (section 10.2). A new set is a section of a LIP that registers its member here. `swarma-holders` is in force since version 0.1.53 by rules of its own (section 10.3, H8 to H11), which state for it what SH1, SH3, SH4 and SH6 state; it does not wait for this section. Its rollback rule and its removal mark (section 10.6, H23 and H41) follow SH5 and state its points of time. | |
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
copy of a prepared spend revokes one name and gives nothing else, where the
spend was made under H51 (H27). A
verifier whose node has not yet seen a spend admits that name until it
does, and LIP-0022 bounds how long its view may stand still. A
verifier that starts after a spend was confirmed and later reorganised away
holds no closure and decides by its node's view, where a verifier that
validated the spend refuses for good (H29, H31). A host that withholds the list delays
the readers that rely on it and admits nobody (H20, H24).

Further consequences of the seal, the journal and the transition:

- **No verifier checks how a seal was made.** That its key is fresh and
  destroyed and that a prepared spend exists are the landlord's conduct
  (H26, H46). A verifier checks that the seal is confirmed, has one key's
  script and is unspent. A seal that nobody can spend is an entry that only
  a name update removes, and no verifier sees the difference.
- **A durable closure exists only where the spend was validated.** A
  verifier that validated the spending transaction on its own node refuses
  for good. A verifier that could not obtain or validate it refuses while
  its view shows the seal not unspent, records nothing, and admits the name
  again after a reorganisation or an eviction. A reader behind a gateway of
  states is always in the second group (H50). The split between the two is
  permanent unless the spend is broadcast again or the landlord completes
  by a list (H52, H32).
- **One keeper holds the revocation of the whole list.** A device with
  `ceiling` 2 or a cold copy that is compromised can revoke every name of
  the landlord at every witness, for good; the recovery is a new seal for
  every name and a cold-key update (H27). It ends no grant and moves no
  name.
- **The fast path is not claimed yet.** The fee of a prepared spend is fixed
  when it is signed and cannot be raised by a second signature. Until the
  amount, the fee and the fee-raising output are closed, a landlord has the
  name update for certain and the seal on a hope (H51).
- **Removal is weaker than a seal.** A removed entry stays refused at the
  verifiers that took the dropping list and at no other, and it needs the
  cold key and a confirmation (H41). Against a stolen key the landlord
  spends the seals.
- **The journal carries the guarantees.** Closures, removal marks and the
  form mark live in the verifier's journal. A verifier that lost it and
  started anew is a newcomer: it admits what a witness refuses, and it reads
  the inline form of a landlord that returned to it. It says so and reports
  nothing that it does not hold (H43).
- **The binding that was journaled first wins.** H38 refuses the second
  entry that names a seal. A landlord whose list a verifier reads can name
  the seal of another landlord's entry, which the other landlord's list
  makes public; at a verifier that takes the hostile list first, the
  rightful entry then refuses as `HOLDER_SEAL_REUSED` until its landlord
  lists the name with a new seal. The lever reaches only the verifiers that
  read both landlords, it admits nobody, and it is the price of one meaning
  for a closure of one outpoint.
- **A reserve that is listed before it is registered can be lost for good**
  to whoever registers the name first (H37).
- **A return to the inline form admits nobody** at a verifier that took a
  pinned list for that landlord (H42). At a verifier that never did, it
  admits every name of the inline keys, as version 0.1.51 does.

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
| A landlord value that pins a holders list, the list in exact octets with one entry for each name, and the seal of the entry unspent (section 10) | A list that does not hash to the pin, a pin of a lower `seq` or of an equal `seq` with another hash, a missing list, a name that no entry lists, an entry that a taken list removed, a name whose owner is not the entry's pin, a seal that is not confirmed as stated, a seal that another entry is bound to, and a seal with a journaled closure refuse the class check and leave the grant key and every v4 grant of the landlord as they read. A spent seal whose spend the verifier did not validate refuses without closure, and a failed read refuses as a failed read. A change of the pin closes no grant. A value in the inline form of version 0.1.51 is read by section 10.9 only where the verifier never took a pinned list for that landlord, and one with both forms has no holder. A journal that cannot be written admits nobody. |
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
  that the section marks NEW, and first the owner pin in an entry (H34) and
  the bounds of 1024 entries and 262144 bytes (H6). Ruled after the second read of this section, and no longer open
  as questions of this text: the closure of a spent seal is of the entry and not of the
  name or the key (H33); no master seal for a key (H35); the writer of check
  (d) is the entry's own key (H34); both forms in one value give no holder
  (M2); a removed entry does not return after a reorganisation at a
  verifier that took the dropping list (H41); and a reader behind a gateway
  of states is a non-witness (H50). Marked NEW since that read and before
  the owners: the seal read and the single script form of a seal (H45,
  H46); the height bound of a seal's funding (H46); the definition of a
  validated spend (H47); the outpoint as the key of a closure, across
  landlords, and one seal for one entry (H38, H39); the point at which the
  journal advances and the refusal of an equal `seq` with another hash
  (H40, H23); the form mark (H42); the rules of a journal that fails
  (H43); the read before the effect (H44); the alias check (H49); the
  order of the checks (H48, H53); the keepers with `ceiling` 2 and the cold
  floor (H27); the one input and the hash type of the prepared spend, and
  the duties to broadcast again and to complete (H51, H52, H32); a reserve
  registered before it is listed (H37); and the codes
  `HOLDER_SEAL_NOT_LIVE`, `HOLDER_SEAL_REUSED`, `HOLDER_SEAL_ALIAS` and
  `HOLDER_FORM_DOWNGRADE`. Open, and blocking for the fast path (H51): the
  amount of a holder seal, the fee of its prepared spend, and an output
  that lets a child transaction raise it. Open beside them: the
  confirmation depth at which a verifier takes a new pin and, beyond the
  bound of H46, counts a seal as existing; how a node supplies the spend
  state of an outpoint and its spenders, the confirmed one above all, and a
  run on a node (H45); the watcher journal of a deployment (H28); the
  octets of the records of the holder journal and the durable mark of a
  journal that is lost (H39, H43); the member that carries the list in a v4
  request (H18); the domain of the landlord and the kind of the Nostr
  event, without which neither secondary path can be built (H19); the date
  after which readers stop honouring the inline form (section 10.9), which
  should be set, because until then the form mark is what holds; whether a
  pending update of `swarma-holders` alone suspends the admission of the
  landlord's own v4 grants (H15); the first-contact cost of a list at its
  bounds, measured; a vector set for a landlord's tool; and the 520 bytes
  of a landlord value with three heads (section 10.3).
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
