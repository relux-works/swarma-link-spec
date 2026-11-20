# LIP-0010: Name value

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** name values of the landlord profile, their readers, the
  discovery record and deployment; amends LIP-0004 section 1
- **Relates to:** LIP-0007 and LIP-0008

## Summary

The grant-binding member of a name value is `swarma`, whose parsing stays
strict. Link also reads `nostr` for its defined key roles and, under the
Draft amendment of section 11, the top-level `swarma-manifest` head for
statement sets. Other owner members are skipped. Legacy set-head members
are read only in the explicit transition profile of section 11.2.

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
amendment. An owner decision of the same day had the holders follow the
method of the device list: the landlord's name value pins the hash and the
version of a holders list in a member outside `swarma`, `swarma-holders`; the
list lives off the value without the cap of five; a change of it ends no v4
grant; and the list has one entry for each agent or station name, with the
key that holds the name and a seal whose spend revokes that one name. Section
10 retains that H8 form, in force since version 0.1.53 on the same terms,
as a readable legacy form under section 11.2, and keeps the
member of version 0.1.51 as the inline form for the transition (section
10.9). Section 3 is read with section 10.9 for a landlord binding in the
inline form.

Ivan Oparin accepted a separate device-list head on 2026-11-15, and a
per-set head mechanism on 2026-11-16. Ivan Oparin decided on 2026-11-20
that one `swarma-manifest` head replaces those separate heads; section 11
supersedes those earlier Draft directions, with the co-author's agreement
pending. The manifest carries all four registered set heads and the
LIP-0007 service declaration. A set defect refuses that set, not grant
authority; an invalid manifest leaves all its sets unverified.

The device list gives no grant authority. Besides the owner's executors
and key holders, a foreign service may use the narrow identity-only login
of LIP-0034; it does not gain EFFECT authority. Exact-value v3 readers
refuse the new member. Section 11's every-verifier implementation gate and
section 11.2's explicit legacy transition apply before production writes.

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
| `swarma-manifest` (section 11, Draft) | This specification | Reads the one manifest head; sets and the service declaration live behind it. It gives no grant authority. |
| `swarma-holders` (legacy H8, in force since version 0.1.53) | This specification | Readable only under the explicit legacy transition in section 11.2; never together with the manifest form. |
| Any other member | The name's owner or another standard | Does not read it. A head member of section 11 is read under that section where it applies. |

The only part of the value that gives grant authority is `swarma`. Grant
authority comes from `swarma` alone. A member outside `swarma` that looks like a grant key, a
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
6. Rule 3 has the manifest-profile exception `swarma-manifest`, read under
   section 11 by readers needing a set or the service declaration. The legacy
   `swarma-holders` exception is retained under section 11.2 and H8/H9.
   A defective head gives no affected set, never grant authority or a grant
   closure. Manifest and direct heads MUST NOT coexist; no fallback is allowed.

Rule 2 is what makes rule 3 safe. Two readers that differ in how they treat
duplicate members still extract the same `swarma` bytes, because a value with
a second `swarma` is refused before anything is read.

### 3. `swarma` stays strict

`swarma` is a JSON object with exactly one member: `landlord`, `agent` or,
under the amendments of sections 9 and 9.1, `notary` or `issuer`:

| Name | Value of `swarma` | Meaning |
| --- | --- | --- |
| Landlord name | `{"landlord":{"grant":"<grant key>"}}` | The key that signs grants issued under this name. |
| Agent name | `{"agent":{"landlord":"<landlord name>"}}` | The landlord name whose grant key issues grants for this agent. |
| Notary name (section 9) | `{"notary":{"attest":"<attestation key>"}}` | The key that signs this notary's attestations. |
| Credential issuer name (section 9.1) | `{"issuer":{"cred":"<credential key>"}}` | The key that signs third-party credentials (LIP-0032, Draft). |

A key is a valid secp256k1 x-only public key written as 64 lowercase
hexadecimal characters. Inside `swarma` a reader MUST refuse a missing,
additional, duplicate, reordered, `null` or empty member, a member that is a
fold alias of a defined one, and any two fold-equal members. The byte span of
`swarma` MUST equal the compact encoding of the binding it parses to.

`swarma.agent.nostr` is not a member of this shape. The agent key is read
under section 5.

Since version 0.1.53 the holders of a landlord (J11) are no member of the
landlord binding. The historical direct `swarma-holders` head remains the
legacy form (section 10); the new manifest profile reaches it through
`sets.swarma-holders` (section 11). The binding of a
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
characters. The manifest profile moves the typed service declaration of LIP-0007
off the name value into the pinned manifest (section 11.1).

**Budget amendment (Draft, 2026-11-20).** Ivan Oparin decided on
2026-11-20 that one manifest replaces per-set heads and carries the LIP-0007
service declaration. The co-author's agreement is pending. The former
150-byte service reserve is released; it is not an extra 150 bytes added to
the 520-byte consensus limit. Keys whose change must close grants remain
in `swarma`; the credential issuer key has its own shape in section 9.1.
Certificate-store statements do not replace authority keys or device-list
records. The card carries transports and the full relay list; operating with
no relay in the name is recommended, not a prohibition on a relay hint.

The following replaces the per-set-head budget for the manifest profile.
The single head adds 104 bytes for one-digit `seq`, 119 at the maximum.
The unchanged base sizes above remain useful for legacy values.

| Value | Base | Manifest, one-digit seq | Left of 520 | Manifest, maximum seq | Left of 520 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Landlord, no `nostr` | 100 | 204 | 316 | 219 | 301 |
| Landlord, key string | 175 | 279 | 241 | 294 | 226 |
| Landlord, NIP-05 object | 191 | 295 | 225 | 310 | 210 |
| Landlord, NIP-05 object and one relay | 294 | 398 | 122 | 413 | 107 |
| Landlord, NIP-05 object and two relays | 318 | 422 | 98 | 437 | 83 |
| Agent, key string | 121 | 225 | 295 | 240 | 280 |
| Agent, NIP-05 object | 137 | 241 | 279 | 256 | 264 |
| Agent, NIP-05 object and one relay | 240 | 344 | 176 | 359 | 161 |
| Agent, NIP-05 object and two relays | 264 | 368 | 152 | 383 | 137 |
| Agent, NIP-05 object plus owner `email` and `name` | 180 | 284 | 236 | 299 | 221 |
| Notary, no `nostr` | 99 | 203 | 317 | 218 | 302 |
| Notary, key string | 174 | 278 | 242 | 293 | 227 |
| Notary, NIP-05 object | 190 | 294 | 226 | 309 | 211 |
| Credential issuer, no `nostr` | 97 | 201 | 319 | 216 | 304 |

The issuer base is `{"swarma":{"issuer":{"cred":"<64 hex>"}}}`.
A manifest does not belong in a `d/` discovery-only record: pin it in the
owner's `id/` name. Neither the set count nor the service declaration adds
another byte to the name's head.

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

### 9.1. Credential issuer name (Draft amendment of 2026-11-20)

Ivan Oparin decided on 2026-11-20 to introduce a separate **credential issuer
key**; the co-author's agreement is pending. [LIP-0032](LIP-0032-generalized-notary-and-credentials.md)
uses the exact shape `{"swarma":{"issuer":{"cred":"<key>"}}}` in the issuer's
own `id/` name. `cred` is a valid secp256k1 x-only public key, 64 lowercase
hex. No additional or alternative member inside this shape is accepted.
A notary or landlord that also issues credentials registers a separate name;
one `swarma` object still has exactly one role. A credential key signs no
grant, owner command, card or notary attestation.

The new shape participates in strict parsing and name-history verification.
A change to this `swarma` span is a name-shape/key change under LIP-0021;
it MUST NOT be hidden in the manifest. It cannot serve as a landlord binding
for existing grants. Eternal credentials have the explicit historical-key
exception of LIP-0032 section 3 and LIP-0021 section 7.6: rotation does not
erase an already anchored fact. An authenticated compromise break with
height `h_c` closes anchors at or above `h_c`, not those below it. That is a
credential rule, not an exemption from grant closure rules.

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
A further owner decision of 2026-11-16 gives the shape of an entry and two
things that follow from it: an entry holds the agent name, the owner pin of
that name and a seal outpoint; a listed name whose current owner is another
key than the pin refuses (H34); and a stolen holder key is answered by the
spend of the seal of every entry that carries that pin (H35). These points
are decided and are no choice of this text, and their rows give "owner
decision of 2026-11-16" as the source.
Every rule below names its source in the last column. A rule or a part of a
rule that neither a decision nor a cited text gives is marked **NEW**: it
is this text's choice, it stands in force with the rest under the order
above, and the owners decide it. The entry by name, the seal of an entry and
the reserve did not exist in this specification before: the rows that state
them name the decision or the rule that they are modelled on, and carry the
mark only for what neither gives. The
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

A review of record of the section as it then stood found eight further
points, and the text closes them. The removal mark is the mark of an entry,
and a verifier whose first list for a landlord was the list that dropped an
entry also holds it after a reorganisation (H40, H41). A binding and a
removal mark are kept for each landlord, and only the closure of a spent
seal is keyed by the bare outpoint (H38, H39). A spender that the node has
no means to name has one code (H45, H48). The height bound of a seal has
one anchor (H46). The owner pin of an entry and the answer to a stolen key
are stated as the owner decisions that they are (H34, H35).

A delta review of record of that text found one further point, and an
independent delta read of an earlier state found eight, of which the text
had closed part. The same pin on another name operation after a
reorganisation is taken (H40, step 5). Three points are closed by ruling:
the step that consults an enforcement closure which a deployment's watcher
supplies, and what such a closure must carry (H28); a reader behind a
gateway makes every step and admits only when the gateway shows the seal's
funding as H46 asks (H50); and the mark of a lost journal (H43). The other
changes are statements and no new rules: an admission that ends at an alias
or a reused seal writes no closure (H48), the cost of binding at the take
(H40), and the facts that the vectors of section 10.11 lacked.

#### 10.1. The holder entry

A holder entry is one JSON object under the encoding rules of LIP-0013
section 2.1, with exactly these members in this order:

| # | Member | Rule | Source |
| --- | --- | --- | --- |
| 1 | `name` | The exact name of one agent or station of the landlord: `id/` followed by 1 to 252 bytes of `a-z`, `0-9`, `-`, `_` and `.`, the v3 name syntax of LIP-0013 section 2.1. | Owner decision of 2026-11-16: one entry for each name, which holds the agent name. The syntax is that of LIP-0013 section 2.1 |
| 2 | `key` | The owner pin of that name, in the form of [LIP-0021](LIP-0021-name-ownership-and-history.md) O2.1: a compressed secp256k1 public key, written as 66 lowercase hexadecimal characters that begin with `02` or `03`, whose other 64 characters are the x coordinate of a point of the curve. | Owner decision of 2026-11-16: the entry holds the owner pin of its name (H34). The pin is that of the member `holders` of version 0.1.51 (section 10.9, rule 2); the member name is that of the device record, LIP-0029 section 3.1 |
| 3 | `seal` | `{"txid":…,"vout":…}`, the outpoint of the entry's revocation seal: 64 lowercase hex in display byte order and a canonical non-negative integer, at most 4294967295. | Owner decision of 2026-11-16: the entry holds a seal outpoint. Its form is LIP-0029 section 3.1, member `seal`, word for word. The bound of `vout` is **NEW**; it is the largest output index of a transaction |

The `seal` is one JSON object with exactly two members in this order: `txid`,
a string, and `vout`, an integer. It has no other member, and a `seal` with
`vout` before `txid`, with a third member, with a member twice or with a
`vout` in another spelling than the canonical decimal one is no seal (H1).
An entry names an `id/` name only: a recipient name outside the `id/` syntax
can stand in no entry, so a class admits no such recipient through the
pinned form. That exclusion is by construction and is **NEW**.

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H1 | An entry has the three members `name`, `key` and `seal`, each once, in that order, and no other. Its `seal` has the two members `txid` and `vout`, each once, in that order, and no other. An entry has no label, no algorithm, no presence flag and no ceiling: a holder signs nothing for the landlord, so the members of a device record that describe a signer have no subject. | `HOLDER_LIST_INVALID` | Owner decision of 2026-11-16 for the three members. That an entry has no other member is **NEW**: the record of LIP-0029 section 3.1, less what describes a signer. The rule sentence for the seal object is **NEW**; its shape is that of LIP-0029 section 3.1 |
| H2 | No two entries of one list have the same `name`, and no two have the same `seal`. Two entries may have the same `key`: one key may hold several names, and each of them has its own entry and its own seal. | `HOLDER_LIST_INVALID` | LIP-0029 O3.3 for `seal`. Uniqueness by `name` and not by `key`: owner decision of 2026-11-16, which has one entry for each name and speaks of every entry that carries one pin |
| H38 | **One seal, one entry, within one landlord.** Within one landlord (its name with its registration, H39) a seal outpoint serves exactly one entry: one `name` and one `key`. It is never named by an entry of another name, or by an entry of the same name with another `key`, in the same list or in any other list of that landlord, whether it is spent or not. A change of the owner pin of a listed name is therefore a new entry with a new seal (H36). A landlord's tool refuses to write a list that breaks this, and it lists only seals that it made under H26, so that it names no outpoint of another landlord. A verifier journals, with every list that it takes (H40), the binding of each seal outpoint of that list, under the landlord of that list, to its `name` and `key`. An entry whose seal the journal binds, under the same landlord, to another `name` or another `key` refuses, and the binding that was journaled first for that landlord stays. **The binding of one landlord says nothing about another.** An entry of another landlord that names the same outpoint is bound under that other landlord, and neither entry refuses because of the other's binding or the other's removal mark. **A landlord that copies the seal of another landlord's entry gains an entry that the other landlord's keepers revoke, and takes nothing from the other landlord's entry: the copy harms only the copier.** Across landlords only the closure of a validated spend holds (H30, H39). | `HOLDER_SEAL_REUSED` at a verifier, within one landlord; the tool refuses at the landlord | **NEW** as a rule; H2 states it inside one list only. Its scope, one landlord, is by ruling after the review of record. The binding across landlords of the earlier text is withdrawn: it let every landlord that a verifier reads make another landlord's entries refuse at that verifier, with no key and no spend. Not taken either: a seal that follows its name through a change of pin, under which a runbook written for one pin revokes a name of another. A closure stays one for an outpoint across landlords (H39), so two verifiers match the closure of a shared outpoint alike and need no shared binding for it |
| H3 | A holder is a key that owns names of the landlord's agents and stations: the output of such a name pays the key hash or the witness key hash of the pin (LIP-0021 O3.3). It is a name-owner key of the key registry, and it is a different key by role from the grant key, from the key that owns the landlord name and from every key that `nostr` yields. A reader permits equal keys and never requires or infers equality. The key that owns the landlord name is a holder only where an entry names it. | | Rule 5 of version 0.1.51, unchanged |
| H4 | An entry confers no authority, and neither does its holder. It issues no grant and signs no request. Only the checks of a landlord class read the list ([LIP-0026](LIP-0026-rows-and-accounts.md) sections 9 and 10), and they read it at each admission (section 10.6). | | Rule 6 of version 0.1.51, unchanged |
| H34 | **The entry carries the owner pin.** An entry admits its name only while the current output of that name reads as controlled by the entry's `key` (LIP-0021 O3.4), and only a value that this key wrote (section 10.6, steps 7 and 9). A listed name whose current owner is another key does not pass, whoever that key is and whatever the value says; a key that holds a name which no entry lists passes nothing with it. When the owner of a listed name changes, the entry stops admitting from the block of the transfer, with no closure; the landlord accepts the new owner only by a new list whose entry for the name carries the new pin (H36), and the new owner then writes the value itself. | `CLASS_HOLDER`, `CLASS_WRITER` | Owner decision of 2026-11-16: an entry holds the agent name, the owner pin and the seal outpoint, and a current owner other than the pin refuses. The decision excludes the form without the pin, under which a listed name would pass for whoever came to hold it, and a name listed before it is registered for whoever registered it first. **NEW**, as what the decision did not give: that the entry stops from the block of the transfer and that no closure is recorded for it. That the writer of step 9 is the key of the same entry is by ruling (section 10.6, step 9) |
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
| H8 | In the manifest profile the landlord's confirmed name value pins `swarma-manifest`, whose `sets.swarma-holders` entry is exactly `{"seq":<seq>,"sha256":"<h(H)>"}` under section 11. The direct top-level two-member `swarma-holders` head remains readable only under the explicit legacy transition of section 11.2, never alongside a manifest. Positive integer and lowercase hash forms are unchanged. | `HOLDER_PIN_INVALID` or `MANIFEST_PIN_INVALID` | Ivan Oparin decided on 2026-11-20; co-author agreement pending; SH1/SH2 |
| H9 | Match the manifest head and entries under SH6, then the holders pin under H8. A duplicate, folded alias, escaped name, noncanonical pin or invalid shape gives no holders list and never grant closure. In legacy mode the written name is exactly `swarma-holders`, without escapes; decode member names to detect aliases but never obtain a pin only by decoding one. A name carrying manifest and direct heads refuses the set path; no preference or fallback is allowed. | `HOLDER_PIN_INVALID` or `MANIFEST_PIN_INVALID` | Ivan Oparin decided on 2026-11-20; co-author agreement pending; section 11.2 |
| H10 | The pinned `seq` equals the `seq` of the list, and `sha256` equals `h(H)`. The `owner` of the list is, octet for octet, the landlord name whose value pins it, and its `network` is the network of the reader's pinned chain. | `HOLDER_LIST_MISMATCH` | LIP-0029 O3.6; section 11, SH4 |
| H11 | A reader takes the pin only from the landlord's name output that is confirmed in the active chain of its own node. A pending name operation gives no pin: it neither adds, replaces nor removes one until it confirms. | | Section 11, SH3; LIP-0029 O9.2. A class check refuses while such an operation is pending (LIP-0026 R9.5, sixth step) |
| H12 | The holders entry gives no grant authority. Grant authority comes from `swarma`; every verifier making landlord-class checks reads the holders set, including another owner's executor. Device-list use is separately scoped by LIP-0029 O3.7, including identity-only login under LIP-0034. | | Section 11 SH7; LIP-0029 O3.7 |

Ivan Oparin decided on 2026-11-20 to put the holders head in the single
manifest. The co-author's agreement on this amendment is pending. The direct
two-member H8 form, in force since 0.1.53, remains readable only in the
explicit legacy mode of section 11.2. It is not silently accepted alongside
a manifest. The old three-head value cost 601 bytes with the NIP-05 object
and one relay; the replacement is 398 bytes (413 at maximum manifest seq),
including all four set heads indirectly and without the former service reserve.

#### 10.4. What a grant's liveness depends on (replaces rule 7 of version 0.1.51)

Rule 7 of version 0.1.51 said that `holders` is part of the `swarma` member,
so that an update which adds or removes a holder refuses every v4 grant that
the landlord issued before it (LIP-0008 section 3) and, under LIP-0008 section
5.2, closes them. For a landlord in the pinned form that rule is replaced by
H13:

| Rule | Requirement | Source |
| --- | --- | --- |
| H13 | The holders of a landlord are no part of its `swarma` member. The current pin is the `swarma-holders` entry of the manifest reached through top-level `swarma-manifest`; the direct top-level `swarma-holders` is legacy only (section 11.2). The list is outside the value. A name update of the landlord that changes either permitted pinning form, and that changes neither the owner of the name nor the octets of `swarma`, ends no v4 grant, refuses none, and is no break under LIP-0008 section 5.2 (J6.1): a verifier records no closure for it, and the landlord issues nothing again. The spend of a holder seal that was made under H26 and that is no other outpoint of the protocol (H49) is no operation of the landlord name and touches no grant. A seal that is, against H49, also the seal of a grant, a linkage output, a coin of a row, a stop coin or a name output performs that other act when it is spent, and this sentence does not cover it; a verifier refuses such an entry where it can see the collision (H49). A v4 grant that the landlord issued depends, in the landlord's name, on exactly the facts that LIP-0008 section 3 binds: the name; its registration; the owner key that controls every output of the name from the one current at the grant's committed recent block to the current one; and the exact octets of the `swarma` member on each of those outputs, which for a landlord in the pinned form are the compact encoding of `{"landlord":{"grant":"<grant key>"}}`, with the grant key equal to the grant's issuer key, and nothing else. No octet of `swarma-manifest`, of its document or set entries, of legacy `swarma-holders`, of a holders list or of a holder seal is among them. Beside the name the grant depends, as before, on its own seal and its own window. | LIP-0029 O3.8 and decision 3; section 11, SH7; LIP-0008 section 3, unchanged |
| H14 | H13 changes nothing in LIP-0008. The rule that a grant lives while the owner and `swarma` do not change stands as written; what changes is that `swarma` no longer holds the holders. A change of the grant key or of the owner still ends every v4 grant of the landlord. | LIP-0008 section 3 |
| H15 | Every change of the list is a name update of the landlord, signed by the name-owner key, that writes a higher manifest `seq` and a higher holders-entry `seq` (or a higher direct H8 `seq` in legacy mode). While it is pending, a class check that reads this landlord refuses without closure (LIP-0026 R9.5, sixth step), and a v3 verifier refuses the grants of the name, without closure, until the update confirms (LIP-0004 section 5). Whether a pending update of `swarma-holders` alone suspends the admission of the landlord's own v4 grants is a question of the observation profile, as it is for `swarma-devices` (LIP-0029 section 3.4). | LIP-0029 O3.10 and O9.1 |
| H36 | **Adding entries.** Adding a name, a reserve included, or changing the owner pin of a listed name needs a new list that holds the entry, a new seal for the entry (H38) with its prepared spend placed under H27, and an update of the landlord's name, signed by the name-owner key, that writes a higher manifest `seq` and a higher holders-entry `seq` (or the direct H8 head only in legacy mode). The funding transaction of every seal of the list is confirmed in the active chain before that update is broadcast, so that the seal exists as H46 asks when the pin confirms; the landlord's tool makes that read and refuses otherwise, and a verifier sees a breach as `HOLDER_SEAL_NOT_LIVE`. A presentation, an attachment or a message never adds an entry. That update ends no v4 grant (H13). Adding is slow and guarded; revoking one name is fast where H51 is met. | LIP-0029 O9.1 to O9.3 and decision 6; **NEW** as a rule for entries by name. That the seals are confirmed before the pin is broadcast is **NEW** |
| H16 | A landlord MUST NOT write the new `swarma-manifest` member to a production name until every verifier of that name has a compatible reader (SH8). The exact-value LIP-0004/v3 reader refuses the whole value, not just holders, and grants refuse without a closure until compatible bytes or a compatible reader are restored. The readable legacy H8 profile is not permission to mix forms or silently downgrade. An operator cannot infer remote reader readiness from chain data; this is an implementation gate, not a verifier check. | Ivan Oparin decided on 2026-11-20; co-author agreement pending; section 11.2 and SH8 |

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
| H19 | Secondary retrieval follows LIP-0033: the authenticated NIP-05 domain, if independently available, serves `https://<domain>/.well-known/swarma/holders-list/<h(H)>`; the name's Nostr key, if present, may publish kind 30079 with `d` tag `swarma-holders-list`. These are optional, non-exclusive channels. Bytes from any source count only under H17 and all profile checks. The SSRF boundary restricts network requests, not acceptance of matching inline bytes. No domain or Nostr key is needed when the presenter supplies the manifest and list inline. | `LIST_UNKNOWN` if needed bytes are absent | Ivan Oparin decided on 2026-11-20; co-author agreement pending; LIP-0033 closes the event-kind question, not a missing NIP-05 domain binding |
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
| 5 | Those octets pass the four checks of H53 in their order. Where the pin is not the journaled head of `L`, the verifier then takes the list (H40) before it goes on; in the branch of H23, point 4, it takes it even where the pin's `seq` and `sha256` equal those of the removed head, and the take replaces the operation and the block of the head | `HOLDER_LIST_INVALID`, `HOLDER_LIST_MISMATCH`, in the order of H53; a take that cannot be written, H43 | LIP-0029 section 11, step 5, and O5.3. The order and the take are **NEW** |
| 6 | The list has an entry whose `name` is, octet for octet, the recipient name, and the journal holds no removal mark of that entry: of this landlord with the `name`, the `key` and the `seal` of the entry as the list writes them (H39, H41). A mark of another entry that names the same seal, and a mark under another landlord, do not refuse here | `CLASS_HOLDER` | Owner decision of 2026-11-16 (the entry by name); LIP-0029 section 11, step 6, "one record"; section 11, SH5, for the mark. That the mark is tested by the identity of the entry and not by the outpoint is **NEW** (H39) |
| 7 | Check (c): the current output of the recipient name reads as controlled (LIP-0021 O3.4) by the `key` of that entry | `CLASS_HOLDER` | LIP-0026 R9.6; H34 |
| 8 | The seal of that entry, in the order of H48: it is no other outpoint of the admission (H49); the journal holds no closure of it, and the deployment's watcher supplies none that counts (H28); the journal binds it, under this landlord, to this entry (H38); it exists on the active chain as H46 asks; and the verifier's own node, with its mempool included, shows it unspent in the seal read of H45 | `HOLDER_SEAL_ALIAS`, `HOLDER_REVOKED`, `HOLDER_SEAL_REUSED`, `HOLDER_SEAL_NOT_LIVE`, `CLASS_HISTORY_UNAVAILABLE`, in the order of H48 | LIP-0029 O8.9 and section 11, step 8, for the unspent seal; the rest is **NEW** (section 10.7) |
| 9 | Check (d): the value of the current output of the recipient name was written by the `key` of that entry (LIP-0021 section 4) | `CLASS_WRITER` | LIP-0026 R9.7. That the writer is the key of the same entry, and no other holder of the landlord, is **NEW** (H34), and the ruling keeps it |
| Before the effect | The reads of H44 are made again immediately before a reservation or an effect | The codes of step 8; a tip that moved voids the admission (LIP-0022 B1.6) | **NEW** (H44); LIP-0022 B1.6 |

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H21 | **What a verifier reads.** For every admission it reads, on its own node and in one observation (H44): the confirmed value of `L` and with it the pin; the name operation of the journaled head (H23); and for the entry of the recipient name, the seal read of H45, with the mempool included. It reads the list from its cache or from the presentation. It takes nothing of this from the presenter except octets that hash to the pin. It reads the seal of no other entry for the admission. | | LIP-0026 R9.10; LIP-0029 O8.9 |
| H44 | **One observation, one named tip, and the read before the effect.** The observation of an admission begins and ends with a read of the tip, its hash and its height (LIP-0022 B1.1), and that pair is the named tip of the admission. Five reads bind to it: the confirmed value of `L` with the pin; the name operation of the journaled head; the pending read of check (b), the sixth step of LIP-0026 R9.5; the current output of the recipient name; and the seal read of H45, in its confirmed part by LIP-0022 B1.4 and in its mempool part by being made between the two reads of the tip. They are facts of one admission in the sense of LIP-0022 B1.5. No rule ties a pending transaction to a tip (LIP-0022 section 1), so the mempool part is bound in a second way: immediately before a reservation or an effect, in the recheck of LIP-0022 B1.6, the verifier reads again the tip, the pending read of check (b), the spend state of the seal with the mempool included, and its journal, with what the deployment's watcher supplies (H28), for a closure of the seal. A tip that moved voids the admission. A spend that it validates at any point before the effect (H47) is journaled, and the admission refuses as `HOLDER_REVOKED`; a seal that is no longer shown unspent without such a spend refuses as `HOLDER_SEAL_NOT_LIVE`; a pending operation of `L` refuses as `CLASS_LANDLORD_PENDING`. A spend that reaches the node after that last read does not undo the effect (section 10.7). A closure that was written during an observation which then turns out void stands, as LIP-0022 B1.2 says of the closures of LIP-0008: it rests on a transaction that the verifier validated and on a seal that was confirmed at a tip which the record names. | The codes named; a void observation gives the code of LIP-0022 | **NEW**. LIP-0022 B1.1, B1.2, B1.4, B1.5 and B1.6. The second read is the strict choice; stating the window between step 8 and the effect as an accepted limit is not taken |
| H22 | **How old a list may be.** A list has no expiry, and its age is no input. The one list that counts at an admission is the list whose hash and `seq` the landlord's confirmed value pins at the tip of that admission's observation. A list that an earlier value pinned, however recent, is no input, whether the verifier holds the current one or not. The freshness of the check is therefore the freshness of the observation: the cutoffs of LIP-0022 section 3 for the age of the tip apply to the class check as to every read of the admission, and this section adds no clock of its own. A cached list is valid for exactly as long as the pin that names it is the confirmed pin. | | LIP-0029 section 3.2 (no expiry), O3.12 (the cache), O9.2 (the pin from the name); LIP-0022 B1.5 and B3.6. That no further age bound is added is **NEW** |
| H39 | **The holder journal and its keys.** A verifier keeps one holder journal, outside the agents' write authority, in the form of LIP-0025. In it a **landlord** is the pair of its name and its registration, the transaction id and the output index that the class pins (LIP-0026 R9.1) or that the parent binds for its issuer (R10.3). A name that expired and was registered again under the same spelling is another landlord, with no state. The journal holds five kinds of record. (1) The **head** of a landlord: the `seq` and the `sha256` of the pin of the list that it last took, the txid of the name operation that carried that pin, and the hash and the height of the block that holds it. (2) The **form mark** of a landlord (H42). (3) The **binding** of a seal outpoint, under one landlord, to a `name` and a `key` (H38). (4) The **removal mark** of an entry, with the `seq` that H40 gives it (H41). (5) The **closure** of a seal outpoint (H28). **Each kind has its own key.** An **entry** is identified by four things: the landlord, the `name`, the `key` and the seal outpoint, the pair of `txid` and `vout`; two entries are the same entry only where all four are the same. The key of a binding is the pair of the landlord and the seal outpoint, so the journal holds at most one binding of an outpoint for each landlord, and one outpoint may be bound under two landlords. The key of a removal mark is the entry, all four, so a mark of one entry is no mark of another entry that names the same seal, under the same landlord or under another. The key of a closure is the seal outpoint alone, so the journal holds at most one closure of an outpoint, across every list, every name and every landlord that the verifier reads, and that one closure refuses every entry that names the outpoint (H30). The octets of these records are open. | | **NEW**. Section 11, SH5, and LIP-0029 O9.2 for the head; LIP-0027 section 3 for a journal in the form of LIP-0025. The keys of each kind are by ruling after the review of record. That a closure is keyed by the outpoint and holds across landlords is the strict choice; a closure for each landlord, under which a seal that two landlords name is revoked for one and admitted for the other, is not taken. A binding and a removal mark keyed by the outpoint alone are not taken: the first gives one landlord a lever over another (H38), and the second makes step 6 and point 3 of H48 answer one trace with two codes |
| H40 | **The take of a list, which is the one point at which the journal advances.** A verifier takes a list when, in an admission, the pin has passed step 3 and its octets have passed step 5, and the pin is not the journaled head of the landlord. In the branch of H23, point 4, the take is made even where the current pin's `seq` and `sha256` equal those of the removed head; it replaces the operation and the block of the head, and since the list is the same, point 5 writes nothing. Before that admission goes on to step 6 it writes, as one atomic step of the store, with every comparison made against the journal as it stood before the take: (1) the new head in the place of the old; (2) the form mark, where the landlord has none; (3) a binding, under this landlord, for every seal of the list that the journal does not bind under this landlord yet; (4) a removal mark, with the `seq` of the taken list, for every entry that the journal binds under this landlord, that the taken list does not hold and that has no mark of a higher `seq`; (5) **in a take whose `seq` is not higher than the `seq` of the head that it replaces**, which only the branch of H23, point 4, reaches: a removal mark, with the `seq` of the replaced head, for every entry of the taken list whose seal the journal did not bind under this landlord before the take; and (6) the lifting of the removal mark of every entry that the taken list holds and whose mark has a lower `seq` than the taken list. A list holds an entry only where it holds the same entry in the sense of H39: the same `name`, `key` and `seal`. **The reason of point 5:** the list of the replaced head was pinned by the landlord's name with a `seq` that is not lower, this verifier took it, and it bound every seal that it held; an entry whose seal was not bound is therefore an entry that that list did not hold, and it is dropped for this verifier whether or not an earlier take had bound it. The removal mark so does not depend on the entry having been bound earlier, and a verifier whose first list for the landlord was the dropping list holds the mark as a verifier that took the older list first does (H41). A mark of point 5 has a `seq` that is not lower than the taken list's, so point 6 of the same take does not lift it. Marks are written and lifted for the landlord of the take alone: no take touches a binding or a mark that stands under another landlord. A seal that the journal binds under this landlord to another entry keeps its binding, and the list is taken all the same (H38). A pin whose list the verifier does not hold, or whose octets fail step 5, advances nothing: the journaled head, and with it the floor of step 3, stays. **The cost of binding at the take:** a take binds every seal of the list, up to 1024, whether or not that seal exists under H46, and no rule removes a binding or a removal mark or bounds their number, so the holder journal of a verifier grows with every seal that a landlord of its classes ever listed, by the acts of that landlord's name-owner key alone. | A write that fails: H43 | **NEW**. Neither H23 of the first text nor its sources say when the journal advances. That the take in the branch of H23, point 4, is made for the same pin on another operation is stated after the delta review of record: without it one reader took and another kept the removed operation as its head. The cost of binding at the take is stated after the independent delta read and is no new rule; binding a seal only when it first passes H46 is not taken, because point 5 and the refusal of H38 both rest on the take having bound every seal of the list, and a bound or a pruning rule is open. Advancing on the read of the pin is not taken: a pin whose list nobody supplies would then raise the floor. Point 5 is by ruling after the review of record, which found that a removed entry returned at a verifier whose first list was the dropping one. That point 5 also covers a take of an equal `seq` with other octets is **NEW** and the strict choice: such a verifier cannot tell an entry that the replaced list dropped from one that the replacing list adds, so both wait for a list of a higher `seq`; marking only under a lower `seq` is not taken, because the entry would then return at this verifier where a verifier that took the older list first refuses it (S10-20) |
| H23 | **Rollback, in this order.** (1) Where the journal holds no head of the landlord, step 3 passes. (2) The verifier reads, against the tip of the observation, whether the name operation of the journaled head is in the active chain (LIP-0022 B1.4). A read that fails proves nothing. (3) While that operation is in the active chain: a pin with a lower `seq` gives no list; a pin with the same `seq` and another `sha256` gives no list; a pin with the same `seq` and the same `sha256` passes and is no take, whichever later operation carries it; a pin with a higher `seq` passes and is taken under H40. (4) Where a reorganisation removed that operation, the verifier takes the pin of the current confirmed value, whatever its `seq` and its hash, under H40, and the new head replaces the removed one; where the `seq` of that pin is not higher than the `seq` of the removed head, the take writes the removal marks of H40, point 5. An equal `seq` with another hash is accepted through this branch alone and never through a later name operation. Every form mark, binding, removal mark and closure stays through every branch. | `HOLDER_LIST_ROLLBACK`; for (2), `CLASS_HISTORY_UNAVAILABLE` | Section 11, SH5. The read of the journaled operation at each admission, and the refusal of an equal `seq` with another hash, are **NEW**; without the second, `seq` alone detects no substitution. The rule defends against a later operation that carries an older pin, and against nothing else: whoever holds the name-owner key writes old contents under a higher `seq`, and H30, H41 and H42 are what then holds at a witness |
| H41 | **A removed entry does not return by a reorganisation.** An entry that a taken list dropped has a removal mark with the `seq` of that list (H40), and step 6 refuses that entry while the mark stands, whatever list the current confirmed value pins. The mark is the mark of the entry (H39): the landlord with the same `name`, `key` and `seal`. It is lifted only by the take of a list with a higher `seq` than the mark's that holds the same entry. A reorganisation that removes the operation of the dropping list lifts nothing: the older list is the list again (H23), and the entry that it holds stays refused at this verifier. **This holds at every verifier that took the dropping list, in whatever order.** A verifier that took the older list first wrote the mark when it took the dropping list (H40, point 4). A verifier whose first list for the landlord was the dropping list had bound nothing of the older list; it writes the mark when the reorganisation makes it take the older list, for every entry of that list which the dropping list did not hold (H40, point 5). A verifier that never took the dropping list holds no mark and admits the name from the older list; a removal is a durable fact at the verifiers that took it and at no other. **Removal alone is therefore no answer to a compromise.** A landlord that must not see a name return spends the seal of its entry, and removes the entry as well (H32). | `CLASS_HOLDER` | Section 11, SH5: "a record that the removed head revoked or removed stays refused". The first text of this section departed from SH5 here and that departure is withdrawn by ruling. That the mark is lifted by a higher `seq` alone, and not by an equal one through the reorganisation branch, is **NEW**. That the rule holds at a verifier whose first list was the dropping one is by ruling after the review of record (H40, point 5) |
| H42 | **No return to the inline form.** The form mark of a landlord is written with the first list that the verifier takes for it (H40) and is never lifted, by no later value and by no reorganisation, also not by one that removes the operation of that first list. For a landlord with the form mark the verifier never reads the inline form of section 10.9 again: a confirmed value of that landlord in the inline form gives no holder, as a value with both forms does (M2), and no name passes check (c) or (d) through it. The sealed-off entries of that landlord, and every other name that an inline key holds, therefore stay refused across such a value. The grant key of the value still reads, and the landlord's own grants are judged as before (section 10.9, rule 7, for what the change of `swarma` does to them). A later value of that landlord in the pinned form is read under the steps of this section, with the journal as it stands. | `HOLDER_FORM_DOWNGRADE` | **NEW**, by ruling. M4 binds the landlord's writer only; whoever holds the name-owner key can write the inline form, and M3 made every verifier read it. Scoping H29 to the pinned form in words, and accepting the downgrade as a landlord act, is not taken |
| H43 | **A journal that cannot be written, a journal that is lost, and replicas.** (1) Where a record of H39 is due and cannot be written, the admission for which it was due refuses, with the code that the record would have given (`HOLDER_REVOKED` for a closure) and otherwise with `JOURNAL_LOST`, and the journal is lost for that verifier (LIP-0025 M5.1): it admits no child through any landlord class until its operator has restored the journal or started it anew, an act that is recorded. A restart does not end that state, also where the store and its outside record still agree because nothing was written (LIP-0027 H3.3). **The mark of a lost journal:** the holder journal is created once, with an identity, and a verifier that finds no journal where its configuration says that one existed refuses every class admission of every landlord with `JOURNAL_LOST` until its operator states a new start, by a recorded act, and it takes no list until then. (2) A verifier whose holder journal is lost is a newcomer for holders (LIP-0008 J6.9). After a start anew it holds no head, no form mark, no binding, no removal mark and no closure. It may claim what its own node shows at the tip of an observation and nothing else; it MUST NOT report a closure, a removal or a form mark that it does not hold, and it says that it is a newcomer and since which recorded act. What is lost with the journal is every closure whose spend is no longer in the view, every removal mark and every form mark: such a verifier admits again what a witness refuses, and reads the inline form of a landlord that returned to it. Deleting a record is no recovery. (3) The replicas of one executor share one authoritative holder journal, as they share the grant journal (LIP-0008 section 4). A replica that does not share it is no replica of that executor: it is a verifier of its own, with witness state of its own, and its operator's conformance claim says so. | `JOURNAL_LOST`, `JOURNAL_FENCED` (LIP-0025); no admission | **NEW**: LIP-0008 section 5.1, last sentence of its second paragraph, and J6.9; LIP-0027 H3.3 and H3.6; LIP-0025 M5.1. The mark of a lost journal, a journal that is created once with an identity and is not found where the configuration says that one existed, is by ruling after the independent delta read. It is the mark of a journal that is not found. How the state after a failed write is carried across a restart while the journal is still found under its identity is not given by that ruling and stays open here as it is in LIP-0027 |
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
| `HOLDER_SEAL_NOT_LIVE` | The seal is not on the active chain as H46 asks, or the node does not show it unspent and the verifier validated no transaction that spends it, also where the node shows the spend and has no means to name the spender (H45). It is no statement that the name was revoked | Nothing | Turns to the landlord: the seal was never funded as listed, is not confirmed, has another script, or was spent where this verifier cannot validate the spend |
| `CLASS_HISTORY_UNAVAILABLE` | A read failed, did not answer or contradicted another read. It is no statement about the seal or the name. A definite spend state with a node that has no means to name the spender is not this code (H45) | Nothing | Retries |

#### 10.7. Revoking one name: the seal of an entry

Each entry carries its own seal. The spend of the seal revokes that one
name, with no name update and no new list. Other names stay, those of the
same key included. The rules follow the device seal of LIP-0029 section 8,
and the seal of an entry did not exist in this specification before:
version 0.1.51 had no seal of a holder, and each row names the rule of
LIP-0029 that it is modelled on. That an entry carries a seal outpoint, and
the answer to a stolen key (H35), are owner decisions of 2026-11-16; what
the rows mark **NEW** is this text's choice.

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
| H45 | **The seal read.** In the observation of the admission, against its named tip (H44), the verifier reads three facts of the seal outpoint on its own node. (a) **The funding transaction:** the octets of the transaction whose id is the `txid` of the seal, with the hash and the height of the block of the active chain that holds it, or the fact that no block of the active chain holds it (LIP-0021 O1.1, third fact; LIP-0022 B1.4). (b) **The spend state** of the output at `vout`, in the node's view with its mempool included: unspent; spent by a transaction in a block of the active chain; or spent by a transaction in the node's mempool. (c) **The spenders:** for an output that is not unspent, the exact octets of every transaction that the node holds which spends the outpoint, the one in a block of the active chain with the hash and the height of that block, and every one in its mempool. LIP-0021 O1.1 supplies fact (a) and neither (b) nor (c): they are further facts of the node that this section needs, and how a node supplies them, the lookup from an outpoint to its confirmed spender above all, is not specified here and no node was run for it. An answer that the node does not give, an error, and two reads that contradict each other prove nothing (H24). A definite answer that the transaction, the output or a spender does not exist is an answer and no failed read. **A spender that the node has no means to name is such a definite answer.** Where fact (b) is a definite spend state that is not unspent, and the node has no lookup from an outpoint to its spender, by its configuration or by a definite answer that it keeps no such record, fact (c) reads "no spender supplied": no spend is validated, point 8 of H48 decides, and the code is `HOLDER_SEAL_NOT_LIVE`, without closure. The reason: the spend state is itself a proved fact of the node, the seal is not live on it, and no retry at this node changes that, so the presenter turns to the landlord; `CLASS_HISTORY_UNAVAILABLE` says "retry" and would promise an answer that this node never gives. A call for the spender that the node supports and that fails, does not answer or contradicts fact (b) is a read that proves nothing (H48, point 6). | `CLASS_HISTORY_UNAVAILABLE` for a read that proves nothing; `HOLDER_SEAL_NOT_LIVE` for a spend whose spender the node has no means to name | **NEW**. The form is that of LIP-0027 H2.3 to H2.5; LIP-0029 O8.9 names `gettxout` and no more. The one code for a spender that the node cannot name is **NEW**, as the review of record proposes; `CLASS_HISTORY_UNAVAILABLE` for it is not taken |
| H46 | **When a seal exists.** A seal counts only when, in that read: its funding transaction is confirmed in the active chain at the named tip, at a height that is not above the height of the anchor block of the pin; that transaction has an output at `vout`; and the script of that output is, octet for octet, a version 0 witness program of 20 bytes, a witness key hash. **The anchor block of the pin** is the block that holds the first name operation of the run of the pin: the unbroken run of confirmed outputs of `L`, ending at the current one, whose values each carry `swarma-holders` with exactly the current `seq` and `sha256`. A later operation that carries the same pin again (H23, point 3) does not move the anchor, and the operation of the journaled head (H39) is not the anchor, because one verifier may have taken the list from a later operation of the run than another. The anchor is read from the active chain at the named tip, with the confirmed value of `L` and in the walk of check (b) (LIP-0026 R9.5; LIP-0021 O6.1), so that two verifiers at one tip find one anchor whenever each of them first took the list; a walk that does not reach the start of the run proves nothing (LIP-0026 R9.8). A funding transaction that is pending, unknown, confirmed above that height or removed by a reorganisation, an index without an output, and another script give no seal. The verifier records no closure for it and states no revocation, and the next observation decides again. **What a verifier knows of the script** is its octets, its form and the 20 bytes of a key hash, and so that exactly one key can spend the output. **What it cannot know**, from these or from any read: whose key that is; whether it is fresh or serves elsewhere; whether it still exists; whether a prepared spend exists, and how many transactions were signed with it. **What follows.** (1) At a verifier a revocation is every validated spend of the seal (H47), whoever signed and broadcast it, and not `tx_revoke_N` alone. A key that was kept against H26 can sign a second spend, and that spend also revokes. (2) A seal that pays a key of another party is revoked when that party moves its coins. (3) A seal that nobody can spend, because no spend was prepared or every copy is lost, makes an entry that no seal revokes, and no verifier can tell it from a sound one. (4) H25 is therefore a promise of the landlord's conduct, and a verifier vouches for it in no report. | `HOLDER_SEAL_NOT_LIVE`, without closure | **NEW**. LIP-0027 H2.3 and H2.6 for the existence on the chain; LIP-0023 for the script form. The height bound is the strict choice of the two that the review names, the other being a depth, which stays open. The anchor of the bound is **NEW** and the strict one of the two that the review of record names: the first operation of the run that carries the current pin, which agrees with the landlord's duty of H36. The block of the current output of `L` is not taken: a landlord could then make a seal that was funded after the pin count by carrying the same pin again. The single script form is chosen so that "validated" has one meaning (H47); admitting both address scripts of LIP-0021 is not taken |
| H47 | **A validated spend.** A transaction `T` is a validated spend of a seal when all of this holds. (1) The verifier has the exact octets of `T`, from its own node or from the record that its deployment keeps of that node's sightings (H28); a txid, a status word, a label of a caller and a flag that says "validated" are no octets. (2) An input of `T` spends exactly the seal outpoint. (3) The verifier's own node accepted `T` under the full rules of the chain, scripts and signatures included: `T` is in the mempool of that node in the observation, or in a block of its active chain at the named tip, or that record holds such a sighting with the tip at which it was made. (4) The verifier itself checks that input against the script of the seal on the octets: the witness of the input holds a signature and a public key, the hash of that key is the 20 bytes of the script, and the signature verifies under the signature digest of a version 0 witness program for the hash type that it carries, with the amount of the funding output. Every hash type counts: a signature of the seal's key over a spend of the seal is the act that revokes, whatever else it commits to. (5) The seal existed under H46 at the tip of the sighting. A spend of a seal whose funding is unconfirmed, or confirmed in no block of the active chain, validates nothing here: it refuses as `HOLDER_SEAL_NOT_LIVE` and records no closure. (6) The verifier read every spender that its node holds (H45, fact (c)). One that meets (1) to (5) is enough; a second, conflicting one changes nothing, because it also spends the seal. | | **NEW**. LIP-0008 section 5.1 defines "validated" for the seal of a grant against the grant's authenticated seal binding; an entry carries no key and no script, so the script of H46 on the chain stands in its place. Closing on the node's state without the spending transaction, as LIP-0027 H2.4 does for a stop coin, is not taken, by ruling |
| H48 | **The order inside step 8.** The first that applies gives the outcome. (1) The seal is another outpoint of the admission (H49): `HOLDER_SEAL_ALIAS`. (2) The journal holds a closure of the seal, or the deployment's watcher supplies one that counts under H28, which the verifier journals first: `HOLDER_REVOKED`, whatever the node shows and whichever entry names the seal, of whichever landlord (H30). (3) The journal binds the seal, under this landlord, to another entry (H38): `HOLDER_SEAL_REUSED`; a binding under another landlord does not count. (4) The read of the funding transaction proves nothing: `CLASS_HISTORY_UNAVAILABLE`. (5) The seal does not exist under H46: `HOLDER_SEAL_NOT_LIVE`. (6) The read of the spend state proves nothing, or a read of a spender that the node supports fails, does not answer or contradicts the spend state: `CLASS_HISTORY_UNAVAILABLE`. A node that has no means to name the spender of a spend that it definitely shows is not this point (H45). (7) The output is not unspent and a spender is a validated spend (H47): the verifier writes the closure (H28) and refuses as `HOLDER_REVOKED`. (8) The output is not unspent and no spender is a validated spend, the case in which the node has no means to name the spender included (H45): `HOLDER_SEAL_NOT_LIVE`, without closure. (9) The output is unspent: the step passes. **Points 1 and 3 refuse before any read of the seal.** An admission that ends at either of them looks for no spend and writes no closure, also while a spend of that outpoint is in the node's mempool, so whether a verifier holds the closure of an outpoint can depend on which admissions it made while the spend was in its view. That divergence is accepted: a verifier that makes no admission while a spend is in its view misses it in the same way (H28), and the broadcast again and the completion of H52 and H32 are what makes the verifiers converge. | As stated | **NEW**. That an admission which ends at point 1 or 3 writes no closure is stated as an accepted divergence after the independent delta read, which names two remedies; the other, the seal read before those two refusals, is not taken, because it adds a read of the node to refusals that need none and removes no divergence that H28 does not already have |
| H49 | **A seal is no other outpoint.** In a class admission the seal of the entry differs from every outpoint that the proof path under verification names or reads: the seal of the child and of every grant above it, and the output after each of them in the same transaction, which is the linkage output of LIP-0023 C2.3; the coin of the child's row (LIP-0026 section 3); the stop coin of that row (LIP-0027); and the current output and the pinned registration of `L` and of the recipient name. The verifier compares on the signed octets and on the outpoints that it read in the same admission. A collision with an outpoint that is not in front of the verifier, a device seal among them, it cannot see, and H26 binds the landlord for those. | `HOLDER_SEAL_ALIAS` | **NEW**. LIP-0027 H2.2 and its code `ROW_STOP_ALIAS`; LIP-0026 section 3 for the coin. Without it the spend of one outpoint performs two acts of the protocol, and H13 would be false for that seal |

**What a closure is.**

| Rule | Requirement | Refusal | Modelled on |
| --- | --- | --- | --- |
| H28 | **The enforcement closure.** A verifier that holds a validated spend (H47) of the seal of an entry of a list that it took journals the closure of that entry durably, before any further admission through a landlord class. It looks at every admission, in step 8 of section 10.6 and again before the effect (H44). Between admissions it MAY watch the seals that its journal binds; the **watcher journal** of its deployment, the record that follows the mempool and the blocks of the verifier's own node and keeps the octets of every transaction that spends a watched seal with the tip of its sighting, is the source of that evidence for a spend that has left the node's view. **Where a closure that the watcher supplies is consulted.** Point 2 of H48, in step 8 of section 10.6, and the read before the effect (H44) consult, beside the closures that the holder journal already holds, an enforcement closure that the watcher of the verifier's deployment supplies for the seal. Such a closure counts only if it carries what H47 requires: the validated spender, which is the exact octets of the spending transaction, checked by the verifier itself under points 2 and 4 of H47; the confirmed funding of the seal, as H46 asks, at the tip of the sighting (H47, point 5); and one named tip, the hash and the height of the tip at which the sighting was made (H47, point 3). The verifier journals a closure that counts, as a record of its own holder journal (H39), and refuses as `HOLDER_REVOKED`; a supplied closure that lacks one of the three counts for nothing: it refuses no admission, and nothing is written for it. The format of such a closure and of the watcher journal, and the transport from the watcher to the verifier, are outside this section and open. The closure is keyed by the seal outpoint alone (H39) and refuses every entry that names it (H30). It holds: the outpoint; the landlord's name and registration, the `name` and the `key` of the entry in whose admission or watch it was written, as a record of the sighting and no limit of its reach; the txid of the validated transaction and the SHA-256 of its octets; whether it was sighted in the mempool or in a block, with that block's hash and height; and the hash and the height of the named tip of the sighting. A verifier that validated no such transaction writes no enforcement closure, whatever a node, a gateway or a caller reports. | A closure that cannot be written: H43 | LIP-0029 O8.3; LIP-0008 section 5.1. The record and the watcher journal are **NEW**. Which step consults a closure that the watcher supplies, and what such a closure must carry to count, is by ruling after the independent delta read, which found that no step read the watcher's evidence; the watcher journal itself is not specified here, by the same ruling |
| H29 | After a closure the verifier admits the name of that entry through no class. Every other entry counts as before, an entry with the same `key` included, and the landlord's v4 grants are untouched (H13). A rollback cannot restore the entry: a list of a lower `seq` refuses (H23), every list that names the entry names the same closed seal, and a journaled closure is not lifted by a later list, a name update, a value in the inline form (H42), eviction, replacement, non-confirmation or a reorganisation, the one that removes the funding of the seal included. This rule holds for a verifier that validated the spending transaction on its own node. It does not hold for a reader of H50, and not for a verifier whose journal is lost (H43). | `HOLDER_REVOKED` | LIP-0029 O8.4 and case S29-18; LIP-0008 section 5.1 |
| H30 | A seal outpoint that was spent is never named again by an entry. An entry that names an outpoint of which the verifier holds a closure refuses, whatever `name` and `key` it carries, in whatever list and of whichever landlord. | `HOLDER_REVOKED` | LIP-0029 O8.5. Across landlords: **NEW** (H39) |
| H31 | A seal that the node does not show as an unspent output, where the verifier holds no validated spend of it, refuses the admission and records no closure: the spend may lie in a block whose transaction the node cannot supply, or the spender did not pass H47. A seal that does not exist as H46 asks refuses in the same way. Neither is reported as a revocation, and a read that failed is reported as neither (H24). The refusal lasts while the node shows the output so; it is a verdict on one observation and no journaled closure, and where a reorganisation makes the output unspent again, this verifier admits the name while a witness refuses it for good. | `HOLDER_SEAL_NOT_LIVE`, without closure | LIP-0008 section 5.1, last paragraph; LIP-0027 H2.6 and its code `ROW_STOP`. The code is **NEW**; the first text gave `HOLDER_REVOKED` here |

**A reader that cannot validate a spend.**

| Rule | Requirement | Refusal | Source |
| --- | --- | --- | --- |
| H50 | **The non-witness.** H28 and H29 stand for a verifier that validates the spending transaction on its own node. A verifier that reads the chain through a gateway which returns only the state of a seal (unspent, which is confirmed and not spent in the mempool; unconfirmed; spend pending; not in the confirmed set) is a **non-witness** for closures that begin in the mempool. (1) It makes every step of section 10.6, steps 0 to 9 and the read before the effect, as every verifier does, and it keeps the holder journal of H39 with its heads, form marks, bindings and removal marks; the one thing that it cannot do is write an enforcement closure. A read of a step that it cannot make proves nothing and refuses as H24 says. It refuses on every state of the seal but unspent, and the state unspent alone admits nothing (point 4). (2) It records no enforcement closure, for no state and no sequence of states: a state is a label, and a label is consistent with a valid spend, with a transaction that a relay kept and no node would confirm, and with an error of the gateway. (3) Where the gateway shows a seal absent from the confirmed set, it MAY keep an **observe-grade closure**. That record is named so wherever it is stored or reported; it is never used for enforcement, so it refuses no admission, is no closure of step 8, is not reported as `HOLDER_REVOKED`, and does not stand against a later unspent state. The reason is twofold: the reader validated no spending transaction, and the absence of a seal also follows a reorganisation that removed its funding. (4) **It admits only when H46 holds through what the gateway shows:** the funding transaction of the seal, confirmed against a named tip, with the script of its output and its height, which the reader checks as H46 asks. Where the gateway cannot show the confirmed funding with its script and its height, the reader refuses as `CLASS_HISTORY_UNAVAILABLE`, as for a read that failed; where the gateway shows them and they do not meet H46, it refuses as `HOLDER_SEAL_NOT_LIVE`. This point is asked on the state unspent; every other state refuses as `HOLDER_SEAL_NOT_LIVE` whatever else the gateway shows, and a gateway that gives no state is a read that failed. (5) Its operator's conformance claim says that it is a non-witness and that it admits a revoked name again after an eviction or a reorganisation that it could not validate. An enforcement closure needs three things that such a gateway does not give: the octets of the spending transaction, validated by the reader against the script of the seal (H47); every spender that the node holds; and one named tip for the read. The watcher journal of H28 is the deployment's source of that evidence. | `HOLDER_SEAL_NOT_LIVE` for every state but unspent and for a funding that does not meet H46; `CLASS_HISTORY_UNAVAILABLE` for a read of the gateway that fails and for a gateway that cannot show the confirmed funding with its script and its height | **NEW**, by ruling. LIP-0008 section 5.1: "a caller's label or a reported transaction ID is not branch proof". That the reader makes every step, admits only when H46 holds through what the gateway shows and refuses as a failed read where the gateway cannot show it is by ruling after the independent delta read; the earlier point 4, which left the checks of H46 to what the gateway happened to supply, is withdrawn. The earlier condition of the observe-grade record, a seal that the reader had journaled as unspent, is dropped: H39 holds no such record, and the smaller of the two remedies that the read names is taken |

**The return of a name, and a stolen key.**

| Rule | Requirement | Refusal | Modelled on |
| --- | --- | --- | --- |
| H33 | A name whose entry was sealed off counts again only by a new entry: a later list, with a higher `seq`, that names it with another seal, which exists under H46 and is unspent, pinned by a name update that the name-owner key signs. The closure of H28 is the closure of the entry with its seal, and not of the name or of the key for ever. | | LIP-0029 O9.1 for the slow path. That the closure is of the entry is **NEW**, and the ruling keeps it: LIP-0029 O8.4 closes the device, and O3.20 has a device return with a new key |
| H35 | **A stolen holder key.** The landlord answers the theft of a key by the spend of the seal of every entry whose `key` is that pin: one prepared spend for each such entry, each broadcast by a keeper of H27. There is no seal of a key: no one spend revokes every entry of a pin. Until the last of the spends is validated at a verifier, the names whose seals are unspent still pass there with whatever value the thief writes. The spends move no name: the names stay with whoever holds the key. The landlord then registers names under another key and lists them, or uses reserve entries of another key (H37), and completes the revocation by a list without the sealed entries (H32). Removing the entries by a list alone is no answer to the theft (H41). | | Owner decision of 2026-11-16: a stolen key is answered by the spend of the seal of every entry that carries that pin. LIP-0029 O8.10 for the broadcast. A master seal for each key is not taken, by ruling: it would bring back the reach of one spend over every name of a key, which the entry by name removed |

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
| What a verifier records | The new head and a removal mark of the entry, keyed by the landlord and the entry's `name`, `key` and `seal`, with the `seq` of the list that dropped it (H39, H40, H41) | A durable closure, keyed by the seal outpoint alone, which refuses every entry that names it (H28, H30) |
| After a reorganisation that removes the act | At a verifier that took the dropping list, after the older list or as its first list for the landlord: the older list is the list again (H23), and the entry stays refused by its mark (H40, points 4 and 5; H41). At a verifier that never took it: the entry of the older list admits its name | At a verifier that validated the spend: the closure stays (H29). At a verifier that did not: the seal is unspent again, and the name is admitted (H31) |
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

A closure is written only by an admission that reaches the read of the
seal, or from a closure that the deployment's watcher supplies (H28). An
admission that ends as `HOLDER_SEAL_ALIAS` or as `HOLDER_SEAL_REUSED` reads
no seal and writes none, also while the spend is in the node's view (H48).
That is an accepted divergence between verifiers, of the kind that a
verifier which made no admission in that time already shows, and H52 and
H32 are what closes it.

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
| M1 | **The form of a landlord value.** The current pinned form uses the `swarma-holders` entry in the manifest of section 11; without that manifest and entry it supplies no holders. Only an explicitly selected legacy reader may use the older inline `landlord.holders` or direct top-level H8 head. Missing manifest bytes MUST NOT trigger legacy fallback. | `CLASS_HOLDER`; the manifest refusals of section 11 | Ivan Oparin decided on 2026-11-20; co-author agreement pending |
| M2 | A value that mixes inline holders with a direct holders head or a manifest has no holder by either form. A manifest together with any direct set head refuses under section 11.2. Its otherwise valid `swarma` authority still reads under rule 1; the mixture creates no grant closure. | `CLASS_HOLDER`; `MANIFEST_PIN_INVALID` for mixed manifest/direct heads | Section 11.2 |
| M3 | **Legacy reads meanwhile.** An explicitly selected legacy reader retains the inline checks of version 0.1.51 and the direct H8 checks of section 10.6. An inline key admits only the names it holds and wrote, has no individual seal, and can be removed only by changing `swarma`, with rule 7 consequences. It MUST NOT be accepted after the journal records a pinned form (H42). A manifest reader uses section 11.2, carries existing counters, removals and closures across migration, and never clears them on a form change. | The codes of LIP-0026 section 9; `HOLDER_FORM_DOWNGRADE` (H42) | Legacy compatibility only; section 11.2 |
| M4 | **Current migration target.** A landlord MUST NOT newly write inline holders or return to inline after a pinned form. It migrates inline holders by one name update removing `landlord.holders` and adding `swarma-manifest` with a holders-set head. The list names every agent or station to keep, with its owner key and an H26/H51 seal confirmed under H36; the prepared spend is placed under H27 before broadcast. A direct H8 head instead migrates atomically under section 11.2, without an intermediate mixed form. | Writer precondition; a verifier refuses downgrade under H42 and section 11.2 | Ivan Oparin decided on 2026-11-20; co-author agreement pending |
| M5 | **Cost of the move.** Removing inline holders changes the octets of `swarma`: every v4 grant issued under those old bytes refuses at the confirming block and must be issued again; an observing verifier records the LIP-0008 J6 closure. M6 still applies. Moving a direct H8 head to the manifest, or adding a first manifest to a grant-only landlord value, changes no `swarma` byte or owner and closes no grant (H13). | | LIP-0008 sections 3 and 5.2; section 11.2 |
| M6 | A landlord that added the inline member to a value which had been `{"landlord":{"grant":"<grant key>"}}` would, by removing it, write a `swarma` value that it replaced, which LIP-0008 J6.7 forbids. Such a landlord moves with a new grant key in the update of M4. A landlord whose first `swarma` value already carried the inline member keeps its grant key. | | LIP-0008 section 5.2, J6.1 and J6.7 (Draft, agreement pending) |
| M8 | The move narrows what passes. Under the inline form every name that a listed key holds and wrote is admitted; under the pinned form only the names that the list names. A landlord lists every name in use before it moves, and a name that it leaves out refuses `CLASS_HOLDER` from the block of the update. | `CLASS_HOLDER` | Follows from H34, an owner decision of 2026-11-16 |
| M7 | A landlord moves only after the every-verifier reader gate of H16/SH8. Legacy inline and H8 readers are not manifest readers. An exact-value LIP-0004 reader refuses all these extended forms; a reader which merely skips an unknown manifest finds no holders and cannot admit a class recipient. | Implementation gate, not an on-chain readiness proof | Section 6; section 11.2 |

No implementation of version 0.1.51 is claimed, and this text knows of no
landlord name that carries the inline member. The date after which a reader
stops honouring the inline form is open; until the owners set it, M3 stands,
and with it the form mark of H42 is mandatory at every verifier: it is the
only thing that keeps a sealed-off name refused while the inline form is
still read.

#### 10.10. Cases

The direct-head and inline fixtures below are preserved as **legacy-profile**
cases under section 11.2. Their list, entry and seal checks also apply after
manifest resolution; direct name-member examples do not authorize a mixed
or direct-head value in the manifest profile. Section 11 adds the new
manifest cases separately.

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
| S10-1 | The confirmed value of `L` pins list 3. A child names `id/acme-worker-7`, whose output pays `K1` and whose value `K1` wrote; the presenter supplies list 3, and `Y`'s node shows the seal of the entry confirmed below the anchor block of the pin (H46), with a witness key hash script, and unspent: admitted, and `Y` takes list 3 (H40) and caches it | The same child with the octets of list 3 and one added space: `HOLDER_LIST_MISMATCH`. The same child with no list, at a verifier with an empty cache: `LIST_UNKNOWN`, and the presenter presents again with the list. `id/acme-worker-9`, which `K1` holds and wrote and which points to `L`, and which no entry names: `CLASS_HOLDER` (step 6). |
| S10-2 | `L` issued the v4 grant `G` at recent block `R`. After `R` the landlord pins list 4, which adds an entry, and later list 5, which drops one: `G` is admitted throughout, because the owner and `swarma` did not change (H13) | An update of `L` that replaces the grant key: `G` refuses, as LIP-0008 section 3 says, whatever the pin. A verifier that records a closure of `G` for the update to list 4 is wrong. |
| S10-3 | `P` broadcasts `tx_revoke_N` for `id/acme-worker-7`. `Y`'s node takes it into its mempool, `Y` validates it under H47 and journals the closure of the entry. `id/acme-worker-8`, which the same `K1` holds, is admitted as before, and `G` and every other v4 grant of `L` stay admissible | A child that names `id/acme-worker-7`, at `Y`, while list 3 still names it: `HOLDER_REVOKED`. After a reorganisation that removes the block with the spend: still `HOLDER_REVOKED`, because the closure is journaled (H29). |
| S10-4 | `id/acme-worker-8` is transferred to `K2`, a key that list 3 names for another entry. The child signs `K2` | A child that names it: `CLASS_HOLDER` (step 7), because the entry's `key` is `K1` (H34). After list 4 names `id/acme-worker-8` with `K2` and a new seal (H38) and confirms, and before `K2` updates the value: `CLASS_WRITER` (step 9). After an update of the value by `K2`: admitted. List 4 with `K2` and the seal of the old entry: steps 6 and 7 pass, because the removal mark that the take of list 4 wrote is the mark of the old entry with `K1` and not of this one (H39), and step 8 refuses as `HOLDER_SEAL_REUSED` (H48, point 3). |
| S10-5 | The reserve `id/acme-reserve-01` is registered to `K2` before list 3 is pinned, with a value that is no agent binding (H37). `K2` writes an agent binding that points to `L`: from the block that confirms that update a child that names it is admitted, with no update of `L` | Before that update: `CLASS_LANDLORD` (LIP-0026 R9.4). A landlord that pinned list 3 before the registration, against H37: another party registers the name first and sends it to the address of `K2`, and a child that signs `K2` refuses as `CLASS_WRITER` (step 9); the same party keeps the name, and a child that signs that party's key refuses as `CLASS_HOLDER` (step 7), for as long as the party keeps it. |
| S10-6 | `K1` is stolen. `P` broadcasts the prepared spends of both entries of `K1`; `Y` validates both and journals two closures, and the reserve of `K2` is not touched (H35) | A child that names either name of `K1`: `HOLDER_REVOKED`. After only the first spend, a child that names `id/acme-worker-8` with a value that the thief wrote: admitted, which is why H35 asks for every entry of the pin. |
| S10-7 | List 4 drops the entry of `id/acme-worker-8` without a spend of its seal; after the update confirms and `Y` takes list 4, the name refuses `CLASS_HOLDER`. List 5 holds the same entry again, with the same unspent seal: admitted again from the take of list 5 (H41) | List 5 names `id/acme-worker-7`, sealed off in S10-3, with the same seal: `HOLDER_REVOKED` (H30). A later name update that pins `seq` 3 while the update of `seq` 5 stays in the active chain: `HOLDER_LIST_ROLLBACK`. List 6 names `id/acme-worker-7` with a new seal that exists and is unspent: admitted (H33). |
| S10-8 | The update that pins list 4 is in the mempool: list 3 is the list (H11) | A class check of `L` in that time: `CLASS_LANDLORD_PENDING` (LIP-0026 R9.5). A verifier that takes list 4 before its update confirms is wrong. |
| S10-9 | A landlord value in the inline form with two holders, and no `swarma-holders`: every name that the first inline holder holds and wrote is admitted as in version 0.1.51 (M3) | The same value with a top-level `swarma-holders`: no holder, `CLASS_HOLDER`; the grant key still reads, and the landlord's grants are judged as before (M2). A value with `swarma-holders` twice: `HOLDER_PIN_INVALID`, and the grant key still reads (H9). |
| S10-10 | A landlord in the inline form moves under M4: its v4 grants of before refuse and are issued again, once (M5) | The same landlord then pins list 2: no grant refuses (H13). |
| S10-11 | The grant of the agent `id/acme-worker-8` is ended by the issuer's spend of that grant's seal | The spend of the seal of the entry of `id/acme-worker-8`, with the grant's own seal unspent: the grant is not closed; where its admission passes through a class of `L` it refuses `HOLDER_REVOKED` at each admission, and elsewhere it is admitted. The name stays with the holder of `K1`. |
| S10-12 | The control of S10-1: the funding transaction of the seal is confirmed at a height that is not above the anchor block of the pin, and its output is a witness key hash (H46). The anchor: the update `U3` pins list 3 at height 100, a seal of list 3 is funded at height 100 or below, and a later update `U4` at height 110 changes `nostr` and carries the same pin: the anchor block is the block of `U3`, before and after `U4`, and the seal exists | The update `U3` pins list 3 at height 100, a seal of list 3 is funded at height 105, and `U4` at height 110 carries the same pin: `HOLDER_SEAL_NOT_LIVE` for the entry of that seal, before `U4` and after it, with no closure; a verifier that anchors on `U4` and admits is wrong, and so is one that anchors on the operation of its journaled head where that is `U4`. The funding transaction is in the mempool only; it is unknown to the node; it is confirmed above the anchor block of the pin; the output has another script; the transaction has no output at `vout`: each `HOLDER_SEAL_NOT_LIVE`, with no closure. The node does not answer the read of the funding transaction: `CLASS_HISTORY_UNAVAILABLE`. A spend, in the mempool, of a seal whose funding is unconfirmed: `HOLDER_SEAL_NOT_LIVE`, with no closure (H47, point 5). |
| S10-13 | The spend of the seal of `id/acme-worker-7` confirmed while `Y` was away. `Y`'s node shows the output spent and supplies the spending transaction from its block; `Y` validates it and journals the closure: `HOLDER_REVOKED`, also after a reorganisation that removes that block | The same, where the node shows the output spent and has no means to name the spender, because it keeps no lookup from an outpoint to its spender: `HOLDER_SEAL_NOT_LIVE`, with no closure, at every admission while the view stands (H31, H45, H48 point 8); a verifier that answers `CLASS_HISTORY_UNAVAILABLE` here is wrong. The same, where the node supports that lookup and the call fails or does not answer: `CLASS_HISTORY_UNAVAILABLE` (H48 point 6), and the presenter retries. The seal exists, and the read of its spend state fails: `CLASS_HISTORY_UNAVAILABLE` (H48 point 6). After a reorganisation that removes the spend: this verifier admits the name, and `W`, which validated the spend, refuses it as `HOLDER_REVOKED`. A spender whose seal input does not verify against the script: no closure, `HOLDER_SEAL_NOT_LIVE`. |
| S10-14 | `W` validated the spend of S10-3 in its mempool and holds the closure. `Y` starts after the spend left every mempool unconfirmed, and its node shows the seal unspent: `Y` admits `id/acme-worker-7`. `P` broadcasts the spend again (H52); `Y` validates it and journals the closure | At `W`, throughout: `HOLDER_REVOKED`. At `Y` after the second broadcast: `HOLDER_REVOKED`. Without H52 and H32 the two never converge. |
| S10-15 | Step 8 of an admission at `Y` reads the seal unspent, and no spend reaches the node before the effect: the read before the effect (H44) passes, and the effect is made | The prepared spend reaches `Y`'s mempool after step 8 and before the effect: the read before the effect validates it, `Y` journals the closure, and the admission refuses as `HOLDER_REVOKED` with no effect. The tip moves between the two reads, and `Y` validated no spend in that observation: the admission is void, with the code of LIP-0022, and nothing is written. The tip moves, and `Y` had validated a spend and written its closure in that observation: the admission is void all the same, and the closure stands (H44; LIP-0022 B1.2). |
| S10-16 | A landlord `L2` of which `Y` never took a pinned list has a value in the inline form: the names of its inline holders are admitted as in version 0.1.51 (M3) | After S10-3 the value of `L` is updated to the inline form with `K1` as a holder. A child that names `id/acme-worker-7`, at `Y`: `HOLDER_FORM_DOWNGRADE`. A child that names `id/acme-worker-9`, which `K1` holds and wrote: `HOLDER_FORM_DOWNGRADE`. The grant key of `L` still reads. `L` then pins list 7, which names `id/acme-worker-7` with its old seal: `HOLDER_REVOKED`. A verifier whose journal was started anew after S10-3 admits both names from the inline value and says that it is a newcomer (H43). |
| S10-17 | List 4 holds the entry of `id/acme-worker-7` with the same `key` and the same seal `S` as list 3: the binding is the same, and the name is admitted | List 4 drops `id/acme-worker-7` and names `id/acme-worker-9` with `S`: for a child that names `id/acme-worker-9`, step 6 passes, because the removal mark that the take wrote is the mark of the entry of `id/acme-worker-7` (H39), and step 8 refuses as `HOLDER_SEAL_REUSED` (H48, point 3): under `L` the journal binds `S` to `id/acme-worker-7`. A child that names `id/acme-worker-7` under list 4: `CLASS_HOLDER` (step 6, no entry). A verifier that refuses `id/acme-worker-9` as `CLASS_HOLDER` because the outpoint `S` has a mark is wrong. After a validated spend of `S`: every entry that names `S` refuses as `HOLDER_REVOKED` (H30, H48 point 2), also after a reorganisation that removes the spend. The same outpoint in the list of another landlord: S10-27. |
| S10-18 | The journaled head of `L` at `Y` is `seq` 5 with the hash `h5`, carried by the update `U5`, which is in the active chain. A later update of `L` changes `nostr` and carries the same pin: step 3 passes, and nothing is taken | A later update pins `seq` 5 with another hash while `U5` is in the active chain: `HOLDER_LIST_ROLLBACK`. The same pin after a reorganisation that removed `U5`: taken through the reorganisation branch (H23, point 4), and every closure and removal mark stays. The pin of `seq` 5 with the hash `h5` itself, carried after a reorganisation that removed `U5` by another operation `U5'`: taken through the same branch although its `seq` and `sha256` equal those of the removed head (H40), so that the head holds `U5'` with its block and no mark is written, and a later update that pins `seq` 3 while `U5'` is in the active chain refuses as `HOLDER_LIST_ROLLBACK`; a verifier that keeps the removed `U5` as its head and then takes list 3 is wrong. The read of whether `U5` is in the active chain fails: `CLASS_HISTORY_UNAVAILABLE`. |
| S10-19 | The value of `L` pins `seq` 6, and nobody supplies list 6 to `Y`: `LIST_UNKNOWN`, and the journaled head of `Y` stays at `seq` 5 (H40). `L` then pins `seq` 7 with a list that `Y` is given: taken | List 6 is supplied with a `schema` of another string: `HOLDER_LIST_INVALID`, and the head stays at `seq` 5. A verifier that raised its floor to 6 on the read of the pin is wrong. |
| S10-20 | `Y` took list 4, which dropped the entry of `id/acme-worker-8`. A reorganisation removes the update of list 4, and the confirmed value pins list 3 again: `Y` takes list 3 through the reorganisation branch, and `id/acme-worker-7` is admitted from it | A child that names `id/acme-worker-8`, at `Y`, under list 3: `CLASS_HOLDER` (step 6, H41). At `W`, which never took list 4: admitted. After list 5 holds the entry again and `Y` takes it: admitted at `Y`. A list of `seq` 4 with other octets that holds the entry, taken through the reorganisation branch: still `CLASS_HOLDER`, because the mark is lifted by a higher `seq` alone. The same trace at a verifier whose first list was list 4: S10-26. |
| S10-21 | `Y` validates a spend and writes the closure; the next child of another landlord's class is judged as before | The write of the closure fails: the child for which it was due refuses as `HOLDER_REVOKED`, and every later child of every landlord class refuses as `JOURNAL_LOST`, also after a restart, until the operator restores the journal or starts it anew by a recorded act (H43). A take of a list that cannot be written: `JOURNAL_LOST` for that admission, and the same state. A verifier that starts and finds no journal where its configuration says that one existed: `JOURNAL_LOST` for every child of every landlord class, and it takes no list, until its operator states a new start (H43); one that starts an empty journal in silence and admits is wrong. A replica of `Y` with a journal of its own that reports `Y`'s closures: wrong. |
| S10-22 | The seal of the entry is an outpoint that the admission names nowhere else: the alias check passes | The seal of the entry is the seal of the child; the output after the seal of the parent; the coin of the child's row; the stop coin of that row; the current output of `L`: each `HOLDER_SEAL_ALIAS` (H49), before any read of the seal, and so with no closure, also where a spend of that outpoint is in the node's mempool (H48). |
| S10-23 | `Z` makes every step of section 10.6 and reads the seal of `id/acme-worker-8` through a gateway that answers unspent and shows the funding transaction of the seal confirmed against a named tip, with a witness key hash script and a height that is not above the anchor block of the pin: admitted | The gateway answers unspent and cannot show the confirmed funding with its script and its height: `CLASS_HISTORY_UNAVAILABLE`; a `Z` that admits on the state unspent alone is wrong. It answers unspent and shows a funding with another script, or confirmed above the anchor block: `HOLDER_SEAL_NOT_LIVE`. The gateway answers spend pending: `HOLDER_SEAL_NOT_LIVE`, and `Z` records no closure. It answers unspent again after the spend was evicted: `Z` admits the name, where `W` refuses it for good. It answers unconfirmed: `HOLDER_SEAL_NOT_LIVE`. After an earlier unspent it answers "not in the confirmed set": `HOLDER_SEAL_NOT_LIVE`, and `Z` may keep an observe-grade closure; after a reorganisation the gateway answers unspent, and `Z` admits the name, the observe-grade record notwithstanding. A `Z` that reports `HOLDER_REVOKED` or refuses by that record is wrong (H50). The gateway does not answer: `CLASS_HISTORY_UNAVAILABLE`. |
| S10-24 | The current value of `L`, which carries the pin, was written by the pinned owner of `L`: check (b) passes and the pin is read | The writer check of that output gives "written by another": `CLASS_VALUE_UNAUTHORIZED`. It gives "unsupported": `CLASS_HISTORY_UNAVAILABLE` (LIP-0026 R9.5 and R9.8). In neither is a pin read. |
| S10-25 | The octets of list 3 under their pin: the four checks of H53 pass | Octets of 262145 bytes that also hash to another value: `HOLDER_LIST_INVALID` (check 1 before check 2). A list whose octets hash to the pin and whose `network` is `test`: `HOLDER_LIST_INVALID` (check 3). A valid list of `regtest` under its pin at a verifier of `main`: `HOLDER_LIST_MISMATCH` (check 4). A list that hashes to another value and also has an unsorted `holders`: `HOLDER_LIST_MISMATCH` (check 2 before check 3). |
| S10-26 | **The dropping list as the first list.** List 3 holds `id/acme-worker-8`, and list 4, with `seq` 4, drops its entry. `W` took list 3 and never took list 4; `V` is a verifier whose first list for `L` is list 4, taken after its update confirmed: `V` binds the seals of list 4 and writes no mark, because it bound nothing before. A reorganisation of one block removes the update of list 4, and the confirmed value pins list 3 again. At `W`: a child that names `id/acme-worker-8` is admitted from list 3, because `W` never took the dropping list. At `V`: `id/acme-worker-7`, which both lists hold, is admitted from list 3 | A child that names `id/acme-worker-8`, at `V`, under list 3: `V` takes list 3 through the reorganisation branch (H23, point 4), its `seq` 3 is not higher than the replaced head's `seq` 4, the seal of that entry was not bound under `L` before the take, and the take writes its removal mark with `seq` 4 (H40, point 5): `CLASS_HOLDER` (step 6, H41). A verifier that binds the entry fresh and admits it is wrong. The narrowing control: at `Y` of S10-20, which took list 3 before list 4, the same child still refuses as `CLASS_HOLDER`, by the mark of H40, point 4. In the place of list 3, a list of `seq` 4 with other octets that holds the entry, taken by `V` through the reorganisation branch: `CLASS_HOLDER`, because an equal `seq` is not higher. After list 5 holds the entry again and `V` takes it: admitted at `V`. |
| S10-27 | **One outpoint in the lists of two landlords.** `S` is the seal of the entry of `id/acme-worker-7` in list 3 of `L`. Another landlord, `L2`, whose class `Y` also reads, pins a list that names `S` for a name of its own, `id/beta-agent`, with the key `KB` that holds that name and wrote its value. `S` is unspent and has no closure. A child that names `id/acme-worker-7`: admitted, whether `Y` took the list of `L` or the list of `L2` first. A child that names `id/beta-agent`, with `S` confirmed not above the anchor block of the pin of `L2`: admitted by the steps of `L2`'s own entry. `L2` then pins a list that drops its copy: `Y` writes a removal mark under `L2` alone, and `id/acme-worker-7` is admitted as before | A verifier that refuses `id/acme-worker-7` as `HOLDER_SEAL_REUSED` because it bound `S` under `L2` first is wrong, and so is one that refuses it as `CLASS_HOLDER` by the removal mark of `L2`'s entry (H38, H39). After a validated spend of `S`, which only a signature of the seal's key makes: the entry of `L` and the entry of `L2` both refuse as `HOLDER_REVOKED` (H30, H48 point 2), also after a reorganisation that removes the spend. `L2` gained an entry that the keepers of `L` revoke, and took nothing from `L`. |
| S10-28 | The control of S10-1: the value of `L` pins list 3, which holds the entry of the recipient name | The value of `L` pins, under a valid pin, a list with an empty `holders` that `Y` holds: every child refuses as `CLASS_HOLDER` (step 6, H7). The value of `L` is in the pinned form without the member `swarma-holders`: every child refuses as `CLASS_HOLDER` (step 1, H7), and the grant key still reads. |

#### 10.11. Vectors

These retained fixtures describe the legacy placement where they name a
direct top-level head. They are not manifest-profile vectors; the latter
remain future conformance work under section 11.

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
| `landlord` | The name and the registration of `L`; the form of its confirmed value: pinned, inline, both, neither; the pin; the name operation that carries the pin, with its block; the first operation of the run that carries the current pin, with its block, which is the anchor block (H46); the writer of the value: the pinned owner, another, unsupported; whether an operation of `L` is pending |
| `list` | The list, by reference to a vector of the group `lists`, and where the verifier has it from: its cache, the presentation, nowhere |
| `seal.funding` | For the seal of the entry: confirmed, with the height and whether that height is above the anchor block of the pin; unconfirmed; absent; the read failed. The script of the output: a witness key hash; another script; no output at the index. For the reader `gateway`: the same values as the gateway shows them against a named tip, or not shown (H50, point 4) |
| `seal.spend` | Unspent; spent in the mempool; spent in a block of the active chain; the read failed |
| `seal.spender` | None; supplied, and its seal input verifies against the script; supplied, and it does not; not supplied, because the node has no means to name a spender (H45); the read of a spender that the node supports failed; supplied by the deployment's watcher as an enforcement closure (H28), with the octets of the spender, the tip of its sighting and the state of the seal's funding at that tip (H47, point 5), or lacking one of the three. For the reader `gateway`: the state that the gateway returns, one of unspent, unconfirmed, spend pending, not in the confirmed set, no answer |
| `seal.at_effect` | The same three facts at the read before the effect (H44), where they differ from those of step 8; whether an operation of `L` is pending at that read; and whether the journal holds, or the watcher supplies, a closure of the seal at that read that it did not at step 8 |
| `journal.state` | Intact; lost; fenced; not found where the verifier's configuration says that one existed (H43); started anew, with the recorded act; whether the next write succeeds |
| `journal.head` | None, or the `seq`, the `sha256` and the name operation of the journaled head, and whether that operation is in the active chain at the tip |
| `journal.form_mark` | Present or absent for `L` |
| `journal.bindings` | For each pair of a landlord and a seal that the vector names: the `name` and the `key` that the seal is bound to under that landlord, or none |
| `journal.removals` | For each entry that the vector names, by its landlord, `name`, `key` and `seal`: the `seq` of its removal mark, or none |
| `journal.closures` | For each seal that the vector names: none; an enforcement closure, with its sighting; an observe-grade record |
| `proof_path` | The outpoints that the alias check compares: the seals of the child and of the grants above it, the outputs after them, the coin and the stop coin of the row, and the current output and the pinned registration of `L` and of the recipient name (H49) |

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
| `admissions` | Step 0, H43 | The control of S10-21 | The refusals of S10-21: a closure that cannot be written; a take that cannot be written; a journal that is lost; a journal that is not found where the configuration says that one existed, `JOURNAL_LOST` with no list taken; a journal that is fenced; a journal that was started anew, which admits what a witness refuses |
| `admissions` | Step 1, H42, M3 | The control of S10-16 | The refusals of S10-16 |
| `admissions` | Step 3, H23, H40 | The controls of S10-18 and S10-19 | The refusals of S10-18 and S10-19; a lower `seq` carried by a later operation (S10-7) |
| `admissions` | Step 3, step 5, H23 point 4, H40: the same pin on a new operation after a reorganisation | `journal.head` at `seq` 5 with `h5` and the operation `U5`, which is in the active chain, and the pin of `seq` 5 with `h5` carried by `U5` or by a later operation: step 3 passes, and nothing is taken. The same head with `U5` not in the active chain, and the same pin carried by another operation `U5'`: admitted, and the take writes the head with `U5'` and its block and no mark | After that take, `journal.head` at `seq` 5 with `h5` and `U5'`, which is in the active chain, and a later operation that pins `seq` 3: `HOLDER_LIST_ROLLBACK` at step 3 (S10-18). It is paired with the control in which the same pin on the same operation `U5` stays in the active chain and the same lower `seq` refuses alike. A vector whose expected records leave the removed `U5` as the head, or that takes list 3, is a defect of the set |
| `admissions` | Step 6, H41 | The control of S10-20 | The refusals of S10-20 |
| `admissions` | Step 6, H40 point 5, H41: the dropping list as the first list | The controls of S10-26: the verifier that never took the dropping list admits the entry; the verifier whose first list was the dropping list admits an entry that both lists hold | The refusals of S10-26: `journal.head` at `seq` 4 with its operation not in the active chain, no binding of the entry's seal, the pin at `seq` 3: `CLASS_HOLDER` at step 6, and the take writes the mark with `seq` 4. The narrowing control, with the binding and the mark of `seq` 4 present before the take: `CLASS_HOLDER`. The pin at `seq` 4 with other octets: `CLASS_HOLDER`. Each is paired with the admitted vector that differs in `journal.head` alone |
| `admissions` | H7 | The control of S10-28 | The refusals of S10-28: a valid list with an empty `holders`, `CLASS_HOLDER` at step 6; a value in the pinned form without the member, `CLASS_HOLDER` at step 1 |
| `admissions` | H38, within one landlord | The control of S10-17 | The refusals of S10-17; the last refusal of S10-4. Each states that step 6 passes and that point 3 of H48 gives the code |
| `admissions` | H38, H39, H30: one outpoint under two landlords | The controls of S10-27: both entries admitted while the outpoint is unspent and has no closure, in both orders of `journal.bindings`; the entry of the first landlord admitted after the second drops its copy | The refusals of S10-27: after a validated spend, both entries `HOLDER_REVOKED`. A vector whose expected outcome is `HOLDER_SEAL_REUSED` or `CLASS_HOLDER` for the rightful entry, on a binding or a mark under the other landlord, is a defect of the set |
| `admissions` | H45, H46 | The control of S10-12, the anchor control included | The refusals of S10-12, one vector for each state of `seal.funding` and of the script, and the anchor pair: one chain and one tip, a seal funded between the first operation of the run and a later operation that carries the same pin, `HOLDER_SEAL_NOT_LIVE`, beside the same seal funded at or below the anchor block, admitted |
| `admissions` | H47, H28, H29, H31 | The controls of S10-13 and S10-14 | The refusals of S10-13 and S10-14: a witness and a newcomer on one trace; a spender that the node has no means to name, `HOLDER_SEAL_NOT_LIVE`; a spender that does not verify; an evicted spend; a spend that a reorganisation removed. A closure that the deployment's watcher supplies (H28): with the octets of a spender that verifies, the seal's funding confirmed at the tip of the sighting and that tip named, while the node shows the seal unspent, `HOLDER_REVOKED` at point 2 of H48, and the closure is journaled; the same without the named tip, and the same with the funding unconfirmed at the tip of the sighting, each counts for nothing, and the admission goes by the read of the node |
| `admissions` | H48 point 6, alone | The control of S10-1 | The seal exists (point 5 passes) and the read of its spend state fails: `CLASS_HISTORY_UNAVAILABLE`. The seal exists, the output is not unspent, and the read of a spender that the node supports fails: `CLASS_HISTORY_UNAVAILABLE`. Each holds one defect, and the second is paired with the vector of point 8 in which the node has no means to name the spender |
| `admissions` | H48, compound | The control of S10-1 | A seal with a journaled closure that is also bound, under the same landlord, to another entry: `HOLDER_REVOKED`. A seal that is an alias and has a closure: `HOLDER_SEAL_ALIAS`. A seal whose funding is unconfirmed and whose spend-state read fails: `HOLDER_SEAL_NOT_LIVE`. A seal whose funding read fails and whose output would have another script: `CLASS_HISTORY_UNAVAILABLE` |
| `admissions` | H49 | The control of S10-22 | The refusals of S10-22 |
| `admissions` | H44 | The control of S10-15 | The refusals of S10-15; an operation of `L` that is pending at the read before the effect and was not at step 8, `CLASS_LANDLORD_PENDING`; a closure of the seal that the journal holds at that read and did not hold at step 8, `HOLDER_REVOKED` |
| `admissions` | H50 | The control of S10-23: the state unspent with the funding shown and meeting H46 | The refusals of S10-23, one vector for each state of the gateway, and for the state unspent one with the funding not shown, `CLASS_HISTORY_UNAVAILABLE`, and one with a funding that does not meet H46, `HOLDER_SEAL_NOT_LIVE` |
| `admissions` | Check (b) before the pin | The control of S10-24 | The refusals of S10-24 |
| `admissions` | H34, H37 | The controls of S10-4 and S10-5 | The refusals of S10-4 and S10-5 |

H16, H26, H27, H36, H51, H52, M4 and the first duty of H37 bind a landlord
and have no refusal at a verifier. They have no vector of these groups; a
vector for a landlord's tool is another set, which this section does not
describe.

Until two implementations that share no code agree on those octets, the
length and the hash of section 10.2 are an illustration.

### 11. Heads of statement sets: the single manifest (Draft amendment of 2026-11-20)

Ivan Oparin decided on 2026-11-20 that **one manifest head replaces the
per-set heads in the name value**. It closes the umbrella-head question
left open by the decision of 2026-11-16. The co-author's agreement is
pending. The new Draft text takes precedence over the older Draft
per-set placement, including LIP-0029 decision 3; section 11.2 explicitly
preserves the in-force H8 form as legacy, not as a manifest fallback.
Sources: events `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s` and
`$EdwfFTmT7uElQhGWzEq0ykBQXA4pDYrolbWK9FaLWyA` of 2026-11-20.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| SH1 | The sole head in the manifest profile is the top-level member `swarma-manifest`, outside `swarma`, with value `{"seq":<seq>,"sha256":"<hex>"}`, exactly these two members in this order, compact. `seq` is a positive canonical JSON integer, at most 9007199254740991; `sha256` is 64 lowercase hex, SHA-256 of the exact manifest document bytes. No `loc` is allowed. | `MANIFEST_PIN_INVALID` |
| SH2 | This section registers `swarma-manifest` and document `swarma-manifest/1`. The manifest's `sets` registers `swarma-devices` (LIP-0029 section 3.2), `swarma-holders` (section 10.2), `swarma-certs` (the unsigned head of LIP-0016 section 3.1) and `swarma-card` (LIP-0037 section 1). These are entries of the manifest, not extra name members. A new set requires a LIP registering it here. The manifest also carries the service declaration of LIP-0007 under section 11.1. | `MANIFEST_INVALID` |
| SH3 | A reader takes a manifest head only from the last name output confirmed in the active chain of its own node. A pending name operation neither adds, replaces nor removes a head. | `LIST_UNKNOWN` when no head exists |
| SH4 | The manifest's `owner`, `network` and `seq` match the name, reader's pinned chain and head; its exact bytes hash to the pin. Each needed set document then matches that entry's `seq` and `sha256`, and its own name and network fields match that same name and network. The naming field is `owner` for device/holder lists, `issuer_name` for a certificate head, and `name` for a card; the card's `owner` describes its operator. | `MANIFEST_MISMATCH`, then the set's mismatch code |
| SH5 | A reader journals both the manifest head and each set head, keyed by name and pinned registration, outside agents' write authority. For every later update while the journaled operation remains in the active chain, manifest `seq` MUST strictly increase (`new > old`); each retained set's `seq` MUST NOT decrease (`new >= old`). An untouched set keeps its `seq` and hash when another changes. Equal set `seq` with another hash refuses. Rereading the same manifest head is not an update. A removed set keeps its highest counter and removal marks, and reintroduction requires a higher counter. A lower manifest or set counter refuses; a missing or unwritable journal supplies no rollback proof and fails closed under LIP-0025. | `MANIFEST_ROLLBACK`, then the set's rollback code; `JOURNAL_LOST` or `JOURNAL_FENCED` |
| SH6 | A reader matches `swarma-manifest` exactly and on its written name, with no escapes. Duplicates, Unicode simple-fold aliases and escaped spellings give no verified manifest or sets. Duplicate, unknown or aliased entries in `sets` are invalid. A defect leaves `swarma`, `nostr` and grants as they read; it never creates a closure. | `MANIFEST_PIN_INVALID` or `MANIFEST_INVALID` |
| SH7 | A manifest and its sets give no grant authority. **Every key or binding whose change must close grants stays in `swarma`, never in the manifest.** A grant reader does not substitute a manifest entry for a grant key, landlord pointer or other authority pin. Changing only the manifest head changes neither `swarma` nor its owner and ends no v4 grant. **Revocation remains a spend of seals and requires no manifest**: a reader processes and journals a validated spend even when the manifest is missing or unreadable. | No new grant closure |
| SH8 | Exact-value v3/LIP-0004 readers refuse `swarma-manifest`. A production name MUST NOT be rewritten until **every verifier of that name** has a reader supporting this profile. This is an implementation/deployment gate, not evidence of installed adoption. Every manifest update is a name update signed by the name-owner key; it does not need a detached manifest signature. | The older reader's existing refusal |

The reorganisation branch of SH5 is kept: when the journaled name operation
leaves the active chain, take the last head confirmed in the active chain,
whatever its counters, journal that head in place of the removed one, and
keep every removal and revocation already journaled. A record added only
by the removed operation waits for a head containing it to confirm again.
This branch does not permit a later operation on an unchanged active chain
to decrease either counter. Equal head and equal hash are a reread, not a
new take; a changed manifest with equal `seq` in a later update refuses.
A renewal or unrelated name edit retaining the identical manifest head is
a reread, not a manifest update; it need not invent another document.

In the manifest profile **no manifest means no set**. A reader refuses by
name (`LIST_UNKNOWN`) and asks the presenter to resend; it never silently
fetches as a substitute for that refusal. In a verified manifest, an absent
set entry means the owner publishes no such set. A present entry with no
matching bytes is unavailable, not absent; it records no removal. A valid
new manifest which omits a formerly present set records that removal under
the set's own rules. A set's signature or cached bytes cannot recreate a
missing pin. An invalid manifest leaves all its sets unverified, without
closing grants.

#### 11.1. Manifest bytes and the service declaration

The manifest is one compact UTF-8 JSON object, at most **16384 bytes**,
without a BOM or trailing bytes. It uses the fixed-member-order encoding
of LIP-0013 section 2.1, **not** RFC 8785 key sorting: strings are printable
ASCII with only `\"` and `\\` escapes. Integers are exact unsigned decimal
JSON numbers, without signs, leading zeros, fractions or exponents, at most
9007199254740991. A reader re-encodes and requires identical bytes. Unknown,
duplicate, reordered, null or escaped member names refuse.

| Order | Member | Rule |
| --- | --- | --- |
| 1 | `schema` | Exact string `swarma-manifest/1` |
| 2 | `network` | `main` or `regtest`, matching the pinned chain |
| 3 | `owner` | The exact `id/` name which pins this manifest, at most 255 ASCII bytes |
| 4 | `seq` | Positive integer, equal to the name head |
| 5 | `sets` | Object of zero to four optional entries, in this order when present: `swarma-devices`, `swarma-holders`, `swarma-certs`, `swarma-card` |
| 6 | `service` | Optional service declaration below; absence advertises no service |

Each entry of `sets` has exactly `seq` and `sha256`, in that order and in
the forms of SH1. No list, key, signature, policy, URL or `loc` occurs in
an entry. The manifest authenticates its set pins; a set's bytes still
have to pass that set's own checks. Absence is permitted, for example a
service with only a card need not publish a device list or holders list.

The optional `service` is the LIP-0007 declaration, with exactly `type`,
`actions`, `receipt_key`, `endpoint`, in that order. `type` is a nonempty
ASCII service-type string of at most 128 bytes. `actions` is an array of
at most 256 distinct nonempty ASCII action strings, each at most 128 bytes,
in increasing byte order. Only actions of the declared type's supported
profile can be used; the wallet-v1 strings remain wallet-v1 strings, and
this declaration invents no v4 leaf. `receipt_key` is a valid BIP-340 x-only
key in 64 lowercase hex. `endpoint` is a nonempty ASCII absolute address
of at most 1024 bytes, interpreted only by a supported transport profile.
All of these bytes count toward the manifest's 16384-byte limit.

This settles the containing path, field spellings, order and single-service
multiplicity that LIP-0007 section 3 left open. Receipt/signature profiles
for non-BIP-340 services, multi-service names, exact non-wallet action
schemas and endpoint-access profiles stay open; unsupported profiles are
not usable declarations. The declaration is discovery only. Its receipt
key is not a replacement for any issuer, recipient or executor authority
pin, and changing it cannot make old receipts, grants or reservations valid.

Retrieval follows LIP-0033: presentation inline first; when there is no
presenter, the optional NIP-05-domain well-known path, then kind 30079 with
`["d","swarma-manifest"]` from the name's Nostr key. The domain is not
invented from the label: LIP-0033 section 1 states the missing-domain case.
An anonymous `id/` name or a pure service with neither a NIP-05 domain nor
a Nostr key works fully when manifest bytes and needed set bytes travel
inline. These secondary paths are optional and never required.

A manifest reader's deterministic order is: (1) name pin grammar and
mixed-form check, `MANIFEST_PIN_INVALID`; (2) required bytes present,
`LIST_UNKNOWN`; (3) size then canonical grammar, `MANIFEST_INVALID`;
(4) hash, owner, network and head counter, `MANIFEST_MISMATCH`;
(5) manifest update journal, `MANIFEST_ROLLBACK`; (6) required set presence,
`LIST_UNKNOWN`, then that set's existing grammar, mismatch and rollback
order. A decrease of a set counter uses that set's rollback code. A failure
records no closure; a failed journal write admits nothing.

#### 11.2. Transition from the per-set heads

The H8 two-member `swarma-holders` form, in force since 0.1.53, remains
**readable as the legacy form**. The analogous Draft direct device and
certificate heads remain legacy descriptions. They are not fallback
sources in the manifest profile. A deployment explicitly selects its
reader profile and upgrades all consumers before publishing a manifest
(SH8); absence of the new member never silently selects a weaker profile.
The date for retiring legacy compatibility altogether is still open.

A manifest-profile reader accepts no direct per-set head from a name. A
name carrying a manifest and a direct `swarma-devices`, `swarma-holders`,
`swarma-certs` or `swarma-card` member is refused as a source of sets with
`MANIFEST_PIN_INVALID`, even if both pins are equal. In particular it MUST
NOT accept both forms for one set. Inline `landlord.holders` together with
a manifest likewise gives no holders (M2). A migration writes the manifest head
and removes the direct heads in **one** name update. A reader carries its
existing per-set counters, removal marks and seal closures into the manifest
journal; changing the placement resets none of them. Once it took the
manifest form it journals that form and refuses a downgrade to direct
heads or an absent manifest. This is no new grant closure.

| Case | Valid control | Forbidden outcome |
| --- | --- | --- |
| Manifest update | Manifest 8 changes devices 4 to 5, keeps holders 7 with identical hash | Manifest 8 to 8 on another update, holders 7 to 6, or holders 7 with another hash refuses |
| Reread | Manifest 8 and the identical bytes are checked twice | The second read is not a new update or a rollback |
| No secondary path | A name with no domain and no Nostr supplies manifest and card inline | Demanding HTTPS or Nostr, or silently fetching missing bytes, is forbidden |
| Migration | A legacy holders pin becomes the same set entry of manifest 1 in one confirmed update | Both forms together refuse; dropping the old holder journal must not restore an entry |
| Revocation | A validated seal spend is observed while the manifest cannot be read | The spend is still journaled; manifest availability cannot postpone closure |

The manifest adds **104 bytes** at a one-digit `seq`, **119** at the largest
`seq`. A landlord with a NIP-05 object and one relay takes 398 bytes (413 at
the largest counter), below 520. The four set heads and the service
declaration are off chain; the old 150-byte in-name service reserve is
released. Section 8 gives the complete budget table. Every head update is
still a cold-key name operation. Fast revocation is the spend of a seal,
not a manifest rewrite.

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
  states is always in the second group; it makes every step all the same,
  and admits only when the gateway shows the seal's confirmed funding with
  its script and its height (H50). A closure that a deployment's watcher
  supplies counts only with the validated spender, the seal's confirmed
  funding and one named tip, and its format and transport are open (H28).
  An admission that ends at an alias or a reused seal reads no seal and
  writes no closure (H48). The split between the two is
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
  nothing that it does not hold (H43). A verifier that finds no journal
  where its configuration says that one existed admits nobody through a
  class and takes no list until its operator states a new start.
- **The journal grows with every seal that was ever listed.** A take binds
  every seal of a list, up to 1024, whether or not it exists on the chain,
  and no rule removes a binding or a removal mark or bounds their number
  (H40). A landlord of a class that a verifier serves, by pinning
  successive lists of fresh outpoints, makes that verifier's journal grow
  at each take; the name-owner key of that landlord is the only key that
  can, and the cost falls on every verifier that reads its class. Within
  that landlord an outpoint that such a list named stays bound to its
  entry (H38). A bound, or a rule that prunes, is open.
- **A copied seal harms only the copier.** A seal outpoint is public once
  its list is presented, and another landlord can name it in a list of its
  own. A binding and a removal mark are kept for each landlord (H38, H39),
  so the copy changes nothing for the rightful entry: it is admitted by its
  own steps 6 to 9, whichever list a verifier took first, and a list that
  drops the copy marks the copy alone. The copier gains an entry that the
  rightful landlord's keepers revoke by their own spend, because a closure
  is keyed by the outpoint alone and refuses every entry that names it
  (H30). No landlord stops a name of another landlord: that takes a
  signature of the seal's key, as the decided shape has it. An earlier text
  of this section bound a seal across landlords, and with it any landlord
  that a verifier reads could make another landlord's entries refuse there,
  with no key and no spend; that binding is withdrawn (S10-27).
- **A removed entry stays removed in whatever order the lists were taken.**
  A verifier whose first list for a landlord dropped an entry marks that
  entry when a reorganisation makes it take the older list (H40, point 5).
  The cost: after such a reorganisation that verifier refuses every entry
  of the older list, or of a list of the same `seq`, that the removed list
  did not hold, until a list of a higher `seq` holds it, an entry that the
  landlord never meant to remove included where the two lists have one
  `seq`. It fails closed and admits nobody.
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
| A landlord value that pins a holders list, the list in exact octets with one entry for each name, and the seal of the entry unspent (section 10) | A list that does not hash to the pin, a pin of a lower `seq` or of an equal `seq` with another hash, a missing list, a name that no entry lists, an entry that a taken list removed, a name whose owner is not the entry's pin, a seal that is not confirmed as stated, a seal that the journal binds under the same landlord to another entry, and a seal with a journaled closure refuse the class check and leave the grant key and every v4 grant of the landlord as they read. An entry that a taken list removed refuses also at a verifier whose first list was the removing one. An entry whose seal another landlord's list also names is admitted while the seal is unspent, and both refuse after a validated spend; refusing the rightful entry for the other landlord's binding is wrong. A spent seal whose spend the verifier did not validate refuses without closure, also where the node has no means to name the spender, and a failed read refuses as a failed read. A change of the pin closes no grant. A value in the inline form of version 0.1.51 is read by section 10.9 only where the verifier never took a pinned list for that landlord, and one with both forms has no holder. A journal that cannot be written admits nobody. |
| Notary value with `attest` alone, with and without `nostr` (section 9) | `notary` beside `landlord` or `agent`, a second member inside `notary`, and an `attest` that is not a valid key refuse. A change of `attest` closes no grant. |
| Pairing applied to `id/alice-cedar`, `id/123four` and `id/xn--bcher-kva` | Requiring a pair for `id/123`, `id/alice_cedar` or `id/alice.cedar` is wrong: `d/` admits no such name. Excluding the `xn--` name from pairing is wrong. |

## Open questions

- Exact canonical bytes of `swarma` once the next format moves to RFC 8785,
  and whether a reader checks member order inside `swarma`.
- The date after which readers stop accepting the LIP-0004 agent value.
- A third `nostr` shape, an object with `pubkey` and a relay array, appears in
  one client's notes for `id/` names and is absent from the draft NIP-N0. It
  yields no key here. It is added if the draft adopts it.
- Co-author agreement on the manifest and service-container amendment of
  2026-11-20. The 520-byte placement question is closed by section 11: only
  the manifest head is on chain, and the former 150-byte reserve is freed.
- An additional naming convention with a single level of registration; the
  authors' own parsers would then handle only that level (the note that
  closes section 7). No prefix, grammar or migration is defined.
- Whether a transfer of `id/<label>` requires the transfer of `d/<label>` in
  the same deployment procedure.
- Whether the notary shape needs a member for a second, pending key during a
  rotation.
- Decision record, normative adoption and public vectors.
- **The holders list (section 10).** The co-author's answer; every point
  that the section marks NEW, and first the bounds of 1024 entries and
  262144 bytes (H6). Decided by the owners on 2026-11-16 and not open: an
  entry of agent name, owner pin and seal outpoint, the refusal of a
  current owner other than the pin (H34), and the answer to a stolen key by
  the spend of the seal of every entry with that pin (H35). Ruled after the
  review of record, and no longer open as questions of this text: a removed
  entry stays refused also at a verifier whose first list was the dropping
  one (H40, point 5); a binding and a removal mark are kept for each
  landlord, and only the closure is keyed by the bare outpoint (H38, H39).
  Ruled after the independent delta read, and no longer open as questions
  of this text: step 8 and the read before the effect consult an
  enforcement closure that a deployment's watcher supplies, which counts
  only with the validated spender, the seal's confirmed funding and one
  named tip (H28); a reader behind a gateway makes every step, admits only
  when H46 holds through what the gateway shows and refuses as a failed
  read where the gateway cannot show it (H50); and the mark of a lost
  journal, a journal created once with an identity and not found where the
  configuration says that one existed (H43). Stated after the delta review
  of record: the take of the same pin on another operation after a
  reorganisation (H40).
  Ruled after the second read of this section, and no longer open
  as questions of this text: the closure of a spent seal is of the entry and not of the
  name or the key (H33); no master seal for a key (H35); the writer of check
  (d) is the entry's own key (H34); both forms in one value give no holder
  (M2); a removed entry does not return after a reorganisation at a
  verifier that took the dropping list (H41); and a reader behind a gateway
  of states is a non-witness (H50). Marked NEW since that read and before
  the owners: the seal read and the single script form of a seal (H45,
  H46); the height bound of a seal's funding and its anchor, the first
  operation of the run that carries the current pin (H46); the one code for
  a spend whose spender the node has no means to name (H45); the definition
  of a validated spend (H47); the outpoint as the key of a closure, across
  landlords, the entry as the key of a removal mark, and one seal for one
  entry within a landlord (H38, H39); the removal marks of a take of an
  equal `seq` through the reorganisation branch (H40); the point at which the
  journal advances and the refusal of an equal `seq` with another hash
  (H40, H23); the form mark (H42); the rules of a journal that fails
  (H43); the read before the effect (H44); the alias check (H49); the
  order of the checks, with the accepted divergence that an admission
  which ends at an alias or a reused seal writes no closure (H48, H53);
  the keepers with `ceiling` 2 and the cold
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
  run on a node (H45); the watcher journal of a deployment, with the
  format and the transport of an enforcement closure that it supplies
  (H28); the octets of the records of the holder journal, and a bound on
  their number or a rule that prunes them (H39, H40); how the state after
  a failed write is carried across a restart while the journal is still
  found under its identity (H43); whether the device seal of LIP-0029
  takes the reading of H45 to H48 (LIP-0029 section 8.1); the member that carries the list in a v4
  request (H18); the domain of the landlord and the kind of the Nostr
  event, without which neither secondary path can be built (H19); the date
  after which readers stop honouring the inline form (section 10.9), which
  should be set, because until then the form mark is what holds; whether a
  pending update of `swarma-holders` alone suspends the admission of the
  landlord's own v4 grants (H15); the first-contact cost of a list at its
  bounds, measured; a vector set for a landlord's tool; and the 520 bytes
  of a landlord value with three heads (section 10.3).
- **Heads of statement sets (section 11).** The single manifest is decided by Ivan Oparin on 2026-11-20;
  the co-author's agreement, the date for retiring legacy per-set readers, and the confirmation depth at which a reader takes
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
