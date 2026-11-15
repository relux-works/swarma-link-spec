# LIP-0029: Owner control by signed envelopes and a pinned device list

- **Status:** Draft, written optimistically. Ivan Oparin accepted the
  thirteen decisions of this LIP on 2026-11-15 and asked that the text be
  written without waiting for the co-author: where the co-author objects, the
  point is fixed separately. The co-author's agreement is pending, no rule of
  this LIP is adopted, and until the co-author agrees every text that this LIP
  revises stands as written.
- **Created:** 2026-11-15
- **Affects:** how an owner directs and bounds its own executors and the key
  holders of its agents: the signed envelope and its typed body kinds, the
  device list and its pin in the owner's name value, device keys, levels and
  the level of a launch, executor policy, revocation and addition of a device
- **Builds on:** LIP-0004 sections 1 and 5, LIP-0006 sections 2, 3 and 7,
  LIP-0008 sections 3, 4, 5.1, 12.1, 12.3 and 12.4, LIP-0010 sections 1, 2, 6
  and 8, LIP-0013 sections 2.1, 2.2, 3.2, 3.4, 3.6 and 3.7, LIP-0015
  sections 1 to 4 and 6, LIP-0016 and LIP-0018 section 3; the platform
  envelope `swarm-envelope/2` of Swarma Envelope
- **Revises, once agreed:** the owner's devices in LIP-0015 section 6 and
  LIP-0016; the owner's command as an origin in LIP-0013 section 3.6 (J7.1,
  J7.2) and section 3.7 (point 2); the signer of the configuration statement
  of LIP-0015 section 3; decision K6 of the key map
- **Deciders:** both owners

## Summary

An owner directs its agents today over the owner channel, and the channel
carries no signature (LIP-0013 section 3.7, point 2). Whatever can write into
that channel speaks as the owner. A run that the owner's command starts signs
under the row that the operator writes for the owner's own work (LIP-0013
J7.2), so a command that only starts work can end in a payment or a landing
through the agent's own grants. And every statement of LIP-0015 is signed by the grant key, the key
that issues grants to others.

This LIP gives the owner a voice that the receivers check:

1. Only a signed envelope counts. Free text directs work; an effect happens
   only through typed fields that define it completely, and the executor's
   gate compares them with the arguments it is about to use (section 1).
2. The owner's name value pins the hash of a **device list**, with a version
   number, in a member outside `swarma`. The list holds a record for each of
   the owner's devices: its key, the algorithm, a claimed presence flag, a
   level ceiling and a revocation seal (section 3).
3. A device key is BIP-340 or P-256. P-256 is admitted because the Secure
   Enclave holds no other curve. The envelope identifier and the replay journal
   exclude the signature (section 4).
4. One envelope format, `swarm-envelope/2`, with three typed body kinds: the
   owner command, the LIP-0013 instruction and the wallet request (section 5).
5. Three levels, L0 work, L1 effects within limits and L2, and a launch that
   inherits the level of the envelope that started it. At every level the
   inherited level bounds what the run's key holder signs (section 6).
6. Policy lives in signed executor configuration sections with an increasing
   number, signed by an L2 device, and never in the pinned document
   (section 7).
7. A device is revoked by the spend of its seal, fast, and added by a new list
   and a name update, slowly (sections 8 and 9).
8. The grant key grants to others only. The owner's devices
   speak for the owner at its own executors, and there is no statement key
   (section 10). This is where R5 closes.

The text states its limits in place: a key without presence serves any code
on its device, the presence flag is a claim, and a console that agents can
reach is no L2 console (section "Honest limits").

Nothing of this LIP is implemented. Its body kinds and tags need a reviewed
change of `swarm-envelope/2`, which this repository does not own.

## What is decided and what is proposed

**Owner decision, written optimistically.** Ivan Oparin accepted the
reviewer's recommendations on question R4 as a whole on 2026-11-15, in the
thirteen decisions below, and asked that the draft be written without waiting
for the co-author. The co-author's agreement is pending. The brief of the
decision calls this text R4 v4. The decisions are the normative content of
this LIP; each is written out in the section that the last column names.

| # | Decision | Section |
| --- | --- | --- |
| 1 | All communication counts only when signed, and an unsigned message is ignored. Free text inside a signed envelope directs work only. An effect happens only through typed fields that define it completely: repository, ref and exact revision; payee and amount. The executor's gate recomputes the actual arguments and compares them with the fields before any effect. The owner's client forms the fields and shows them; the executor's model does not. | 1 |
| 2 | The typed action registry is the action profiles of this specification: LIP-0006 and the v4 action profile of LIP-0008. A new action is a LIP section plus executor code. An unknown action class requires L2 or is refused. LIP-0008 section 12.4 stays reserved. | 2 |
| 3 | The owner's name value pins the hash of the device list only, with a version number. The member sits outside `swarma`, so v4 grants are not ended by its changes. It is added only after every verifier runs the LIP-0010 reader, because the LIP-0004 reader refuses extra members. The v3 outage while a name update is pending is a known cost; v3 is the internal alpha. | 3.3, 3.4 |
| 4 | A device record holds a label, the public key, the algorithm (BIP-340 or P-256; the verifier takes it from the record, never from the envelope), a presence flag (claimed, not proven), the level ceiling, and the outpoint of the revocation seal. | 3.1 |
| 5 | Revocation of a device is the spend of its seal. The other devices hold a prepared spend, and the executors' nodes see it in the mempool and journal the closure. A rollback cannot restore a revoked device. An L2-signed revocation, journaled forever by the executors that receive it, is an extra fast path. A name update completes the revocation. | 8 |
| 6 | Adding a device needs a new device list, its new seal, and a name update signed by the name-owner key. Adding is slow and guarded by design; removing is fast. | 9 |
| 7 | Policy, from action class to level and limits, does not live in the pinned document. It lives in signed executor configuration sections (LIP-0015) with an increasing number, signed by an L2 device. Each executor journals the number and refuses a lower one. Every limit belongs to a named executor. | 7 |
| 8 | There is no separate BIP-340 statement key. Statements are pinned in the name or signed by L2 devices. The authority key of a person leaves the key map in favour of device keys. | 10, 10.1 |
| 9 | P-256 is admitted for device keys: SEC1 33-byte keys, 64-byte r‖s signatures, a domain tag. The envelope identifier and the replay journal are computed over the body without the signature, because ECDSA is malleable. P-256 is for envelopes only; Nostr events, the v3 `grantee_key` and seal spends stay BIP-340 (open questions, on seal spends). | 4 |
| 10 | One envelope format, `swarm-envelope/2`, with typed body kinds: owner command, LIP-0013 instruction and wallet request. Every envelope names the executor, an anti-replay number, an expiry and the device-list hash; the list may be attached. | 5 |
| 11 | Levels: L0 work; L1 effects within limits; L2 only by a key with the presence flag or by a separated human console. A launch inherits the envelope's level: an agent started under L0 cannot reach effects beyond L0 through its own grants. The key holder's table includes the level. | 6 |
| 12 | Key boundaries. The name-owner key decides who speaks for the owner. The grant key grants to others only. Device keys are the owner itself at its own executors and at its agents' key holders. At a foreign executor nothing changes: the owner remains a grantee. | 10 |
| 13 | Honest limits: a key without presence is available to any code on its device; the presence flag is claimed (a passcode instead of biometry, one touch for several signatures, an untrusted screen); a host console is not L2 when agents have shells there. | Honest limits |

The reviewer's answer adds one condition that the decision takes over with
the rest: the model's process does not hold the right. Keys, tokens and
privileges of an effect sit at a gate under another OS account (rule O1.6).

This draft adds the following. Each point is a proposal, and neither owner
has decided one.

1. The member names and the order of the device record and of the device
   list, the bound of 16 devices and 4096 bytes, and the encoding of LIP-0013
   section 2.1 for both (section 3).
2. The name of the name-value member, `swarma-devices`, and its value
   `{"seq":…,"sha256":…}` (section 3.3).
3. The type names `owner-command/1`, `instruction/1` and `wallet-request/1`,
   their tags, their members, the attachment of the list as base64url and
   the lifetimes (section 5).
4. The rows of the key holder's table for each level; that the key holder
   receives each executor's policy section from the owner's L2 device and
   checks every object of a run against it at the run's level, a total limit
   counted at the key holder, and no device key at a key holder; and the
   refusal `LEVEL_NOT_FOR_RUN` (section 6, O6.6 and O6.9 to O6.12). That the
   inherited level bounds a run at L1 and L2 as at L0 (O6.7) is decision 11,
   "a launch inherits the envelope's level", applied at every level; the
   decision's example names L0 only.
5. That a policy section reaches an executor as an L2 owner command, so that
   a P-256 device signs envelopes only (section 7).
6. The action `swarma/device/revoke` of the fast path (section 8.2).
7. The order of admission and its refusal codes (section 11).

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The device list, its hash and the name-value member as bytes | Yes | The co-author's agreement; vectors |
| The rule set of an executor as a function of stated facts: list, seals, levels, policy, journal | Yes | The same |
| The rows by level in the key holder's table, its copy of each executor's policy and its checks at every level | Yes, beside J7 | The same, J7 itself, and the members of a policy section (open questions) |
| The three body kinds as `swarm-envelope/2` records | No | A reviewed change of `swarm-envelope/2` sections 2.1 and 2.4 (section 5.4) |
| The member in a live name | No | Every verifier of that name on a LIP-0010 reader (section 3.4) |
| Revocation by seal | No | The script and custody of a device seal (open questions) |
| L2 by presence | No | A qualified signer provider; no provider is qualified (Honest limits) |

## Motivation

**R4: the owner has no voice that a receiver checks.** Under LIP-0013
section 3.7 an owner instructs its own agent "over the owner channel, as for
any other work", without an envelope, and in shadow mode "only the owner
directs" (section 3.4). Every process that can post into that channel, and
every operator of the transport, speaks with the owner's authority. The key
holder then binds the run to "the owner's own command" (J7.1) and signs under
the owner's row of its table (J7.2), which lists the grants of the owner's own
work; the reviewer calls it the widest row. A command that
asks an agent to look at a repository starts a run that can land into it or
pay from it under the agent's own grants. The reviewer named this the main
gap.

**R5: the grant key signs more than grants.** LIP-0015 section 2 gives the
grant key four statement domains beside the grant: configuration, root
rotation, certificates and certificate-set heads. One key then both hands
authority to others and configures the owner's own machines, and a leak of it
does both. The earlier proposal answered with a separate statement key. That
adds a key and still makes the cold name-owner key sign every change.

**One owner, several devices.** The owner signs on a phone, a laptop and
perhaps a hardware key. The Secure Enclave of an Apple device holds P-256 keys
only, so a BIP-340 key on a Mac is a software key (key map, K5). A design that
admits BIP-340 only puts the owner's strongest key outside the Enclave.

## Current state

- LIP-0013 section 3.7, point 2: "An owner directs its own agent without an
  envelope." J7.1 binds a run to "the owner's own command"; J7.2 gives the
  owner's commands a row of their own. No level exists.
- Key map, K6 (2026-11-14, agreement pending): an authority key of a person,
  named in each grant to the person, signs with presence per signature. The
  key registry has its entry, "Authority key of a person".
- LIP-0015 section 3: a configuration statement is signed by the root's grant
  key under `swarma-config-v1`; section 4 step 6 refuses a lower `seq` as
  `CONFIG_ROLLBACK`. Section 6 binds keys of other systems, Matrix devices
  among them, by certificate statements that LIP-0016 stores.
- LIP-0010 section 1: "Authority comes from `swarma` alone." Section 2 rule 3
  skips every other top-level member. The LIP-0004 reader refuses every
  member it does not build (LIP-0010 section 6; key map, "Only the exact
  LIP-0004 values").
- LIP-0008 section 3: a v4 grant lives while the issuer name's updates change
  neither the owner nor `swarma`; an update of another member closes nothing.
- `swarm-envelope/2` (Swarma Envelope, `spec/swarm-envelope-2.md` at
  `065e25f`): a closed envelope `{version, body, id, signatures}`; the
  identifier over the domain tag and the canonical body only (section 2.2);
  P-256 keys as 33-byte compressed SEC1 points with 64-byte low-S r‖s
  signatures, and BIP-340 keys for agent authors (section 2.3); a closed table
  of tags and signature profiles (section 2.4); `operator-act/1`, signed by a
  P-256 operator device that the pinned operator root attests (section 4).
- LIP-0014 J5.9: the owner confirms one operation by a command that names the
  request, the grant, the action, the target and the content, and the executor
  resolves the actual arguments again before the effect (J5.7). The wire form
  of that command is left to the deployment.
- The platform book (chapter 6, section 6.6) has the operator sign each act
  on a phone against a key pinned at the machine, and curator-spec CIP-0011
  revision 6 (R-OPERATOR) has the same presence-gated operator device key. The
  Link book, section 3.13, describes devices and recovery and names no format
  for a device attestation. The section "Reconciliation" cites each of them.

## Proposal

The owner is `O`, with the name `id/alisa`; Alisa is the person. Her devices
are a phone `P`, a laptop `M` and a hardware key `K`. An executor of hers is
`X`; Bob is another owner, with an executor `Y`. A device list is `D`, its
version `seq`, and its hash `h(D)`.

An executor or key holder is **own** to an owner when its trust-root pin
(LIP-0015 section 1) names that owner's name. It reads the owner's device list
from that name. Every other executor is **foreign** to that owner.

### 1. Signed communication and typed effects

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O1.1 | An own executor and an own key holder MUST give effect to a message from or for the owner only when it carries a signed envelope of section 5 that passes section 11. A message without an envelope, or whose envelope fails, MUST be ignored: it directs no work, starts no run, changes no configuration and counts as no approval. | The code of the failed step; nothing for a message without an envelope |
| O1.2 | Free text inside a signed envelope directs work only. It MUST NOT define, select or widen an effect (LIP-0006 section 7). | |
| O1.3 | An effect happens only through the typed fields of its action class, and the fields MUST define the effect completely. A landing names the repository, the ref and the exact revision, which is a full commit identifier. A payment names the payee and the amount. A class whose fields leave a part of the effect to the executor is not admitted for an effect. | `FIELDS_INCOMPLETE` |
| O1.4 | Before any effect the executor's gate MUST recompute the actual arguments of the operation it is about to perform, from the operation itself and not from the envelope, and compare them with the signed fields. Any difference refuses, and no effect follows. LIP-0014 J5.7 and J5.9 have this step for the owner's confirmation of one operation; O1.4 makes it the step of every effect. | `FIELDS_MISMATCH` |
| O1.5 | The owner's client MUST form the typed fields and show them to the owner before a device signs. The executor's model MUST NOT form them. | |
| O1.6 | The process of the executor's model MUST NOT hold the right to the effect. Keys, tokens and privileges of an effect sit at a gate under another OS account, as the wallet service does (LIP-0006 section 1; LIP-0013 J7.8). | A deployment that leaves one within the model's reach does not meet this LIP |

O1.4 is the step that turns a signature into a bound. A gate that compared the
fields with what the model told it would compare two things that the model
wrote. For a landing the gate reads the commit that it is about to make the
head of the ref and compares its full identifier; for a payment it reads the
output that the transaction pays and its amount.

### 2. The action registry

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O2.1 | The typed action registry is the set of action profiles of this specification: LIP-0006 and the v4 action profile of LIP-0008 (sections 12.1 and 12.3, with the type tables of LIP-0007). A class is one exact leaf name of that registry. | |
| O2.2 | A new action class is a section of a LIP, stating the items of LIP-0018 section 3, plus the code of the executor that performs it. No envelope, configuration section or policy adds a class. | |
| O2.3 | An executor MUST refuse an envelope whose class is not in the registry unless the envelope has level L2. | `ACTION_UNKNOWN` |
| O2.4 | LIP-0008 section 12.4 stays reserved. The policy of section 7 is no `policy` form of a grant and no stateless predicate; a request that requires `policy` still refuses there. | |

LIP-0018 section 3 already asks every leaf to state whether it ends in an
effect or in an agent's work. Section 6 uses that line.

### 3. The device list

#### 3.1. The device record

A device record is one JSON object under the encoding rules of LIP-0013
section 2.1, with exactly these members in this order:

| # | Member | Rule |
| --- | --- | --- |
| 1 | `label` | Printable ASCII, 1 to 64 bytes. Names the device for people; carries no authority. |
| 2 | `alg` | `bip340` or `p256` |
| 3 | `key` | For `bip340`: 64 lowercase hex, a valid x-only secp256k1 key under BIP-340 `lift_x`. For `p256`: 66 lowercase hex, the 33-byte compressed SEC1 point: prefix `02` or `03`, `x` below the field prime, on the curve, not the identity. |
| 4 | `presence` | `true` or `false`. The owner's claim, made when the device is enrolled, that the key signs only with a person present. It is not proven (Honest limits). |
| 5 | `ceiling` | `0`, `1` or `2`: the highest level the device may sign. |
| 6 | `seal` | `{"txid":…,"vout":…}`, the outpoint of the device's revocation seal: 64 lowercase hex in display byte order and a canonical non-negative integer. |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O3.1 | A verifier MUST take the algorithm of a device from `alg` of its record, never from an envelope. A key identifier in an envelope whose algorithm differs from the record's refuses. | `DEVICE_ALG_MISMATCH` |
| O3.2 | A record with `ceiling` 2 MUST have `presence` `true`. | `DEVICE_LIST_INVALID` |
| O3.3 | No two records of one list have the same `key` bytes or the same `seal`. | `DEVICE_LIST_INVALID` |

#### 3.2. The device list

A device list is one JSON object under the encoding rules of LIP-0013 section
2.1, at most 4096 bytes, with exactly these members in this order:

| # | Member | Rule |
| --- | --- | --- |
| 1 | `schema` | `swarma-device-list/1` |
| 2 | `network` | `main` or `regtest` |
| 3 | `owner` | the owner's `id/` name |
| 4 | `seq` | the version: a canonical positive integer, at most 9007199254740991 |
| 5 | `devices` | an array of 1 to 16 device records, sorted ascending by the bytes of `key` |

`h(D)` is the SHA-256 of the exact octets of `D`, in 64 lowercase hex. A
reader MUST refuse a list unless re-encoding the parsed value gives the
identical octets. The list has no expiry and holds no policy: the reviewer's
answer removed both from the pinned document, and section 7 holds the policy.

#### 3.3. The pin in the owner's name value

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O3.4 | The owner's name value pins the hash of the device list only, with its version, in the top-level member `swarma-devices`, outside `swarma`: `{"seq":<seq>,"sha256":"<h(D)>"}`, exactly these two members in this order, compact. Nothing else of the list, and no policy, enters the name. | `DEVICE_PIN_INVALID` |
| O3.5 | A reader MUST match `swarma-devices` by exact name. A duplicate of it, or a member equal to it under Unicode simple case folding that is not that exact name, refuses the whole value, as LIP-0010 section 2 rule 2 has it for `swarma` and `nostr`. A member of another shape gives no device list and leaves `swarma` as it reads. | `DEVICE_PIN_INVALID` |
| O3.6 | The pinned `seq` equals the `seq` of the list, and `sha256` equals `h(D)`. | `DEVICE_LIST_MISMATCH` |
| O3.7 | `swarma-devices` gives no grant authority. A Link reader of grants does not read it, and LIP-0010 section 1 holds for grants as written. Only an own executor and an own key holder read it, for owner control. | |
| O3.8 | An update that changes only `swarma-devices` changes neither the owner nor `swarma`, and ends no v4 grant (LIP-0008 section 3). | |

O3.7 amends LIP-0010 in one point: section 1 names `swarma` and `nostr` as the
members that Link reads, and section 8 says that a further entry has "a shape
of its own in this LIP". `swarma-devices` is a third member that Link reads,
for owner control and not for grants.

The member adds 103 bytes while `seq` has one digit, 118 bytes at the largest
`seq`. The sizes count as in LIP-0010 section 8:

| Value | Bytes without | With `swarma-devices`, `seq` < 10 | Left of 520 |
| --- | ---: | ---: | ---: |
| Landlord, no `nostr` | 100 | 203 | 317 |
| Landlord, key string | 175 | 278 | 242 |
| Landlord, NIP-05 object | 191 | 294 | 226 |
| Landlord, NIP-05 object and one relay | 294 | 397 | 123 |

The last row leaves less than the 150 bytes that the budget plan of LIP-0010
section 8 keeps for the service declaration of LIP-0007 (open questions).

#### 3.4. Deployment order and the cost on v3

| Rule | Requirement |
| --- | --- |
| O3.9 | An owner MUST NOT write `swarma-devices` into a name before every verifier of that name runs a LIP-0010 reader. A LIP-0004 reader refuses the whole value, and every v3 grant under that name then refuses at that verifier, without closure, until the exact value is restored (LIP-0010 section 6; key map, "Only the exact LIP-0004 values"). |
| O3.10 | Every change of the device list is a name update. While it is pending, a v3 verifier refuses the grants of that name, without closure, until the update confirms (LIP-0004 section 5: "Pending changes … refuse without closure"). This outage is a known cost. v3 is the internal alpha, and the cost is accepted. |

On v4 a pending name spend can suspend admission under the selected
observation profile (LIP-0008 section 3), and the J6 text of LIP-0008 section
5.2 reads every pending operation of the issuer's name. Whether an update of
`swarma-devices` alone suspends v4 admission is a question of that profile.

### 4. Device keys and signatures

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O4.1 | A device key is a P-256 key or a BIP-340 key, as its record says. | |
| O4.2 | A P-256 public key is the 33-byte compressed SEC1 point of section 3.1. A P-256 signature is exactly 64 bytes: `r` then `s`, each 32 bytes big-endian, `1 ≤ r, s < n`, and `s ≤ ⌊n/2⌋`, over SHA-256 of the signing preimage. DER, an uncompressed point, a high `s` and every wrapper refuse. These are the rules of `swarm-envelope/2` section 2.3 for `p256:` keys. | `ENVELOPE_SIGNATURE` |
| O4.3 | A BIP-340 device key is 32 x-only bytes, and its signature 64 bytes over SHA-256 of the signing preimage, under `swarm-envelope/2` section 2.3 for `bip340:` keys, without a low-`s` rule. | `ENVELOPE_SIGNATURE` |
| O4.4 | Every body kind has a domain tag of its own (section 5.1). The signing preimage is the tag, one byte `0x0a`, and the CCJ-1 bytes of the signed record `{body, key, role, version}` (`swarm-envelope/2` section 2.2). A signature under one tag never verifies under another. | `ENVELOPE_SIGNATURE` |
| O4.5 | The envelope identifier is `"sha256:"` and the lowercase hex of SHA-256 over the tag, `0x0a` and the CCJ-1 bytes of the body. It is computed over the body without the signatures. The replay journal is keyed by this identifier: an envelope whose identifier is in the journal refuses as a replay, whatever its signature bytes. No identity of an envelope is taken from a signature. | `REPLAY` |
| O4.6 | P-256 signs envelopes only. Nostr events, the v3 `grantee_key` and seal spends stay on secp256k1 as they are: BIP-340 for events and grantee keys, the chain's transaction rules for a seal spend. | |

O4.5 is the answer to malleability. ECDSA admits more than one valid signature
over one body: `(r, n − s)` beside `(r, s)`, and a fresh signature with another
nonce. The low-`s` rule of O4.2 removes the first and not the second. An
identifier or a journal key that included the signature would give one body
several identities: from `(r, n − s)` for anyone who saw the envelope, wherever
a verifier does not enforce low `s`, and from a second signature for the device
itself or a client that retries.

### 5. One envelope format with typed body kinds

The envelope is the `swarm-envelope/2` envelope of Swarma Envelope, section
2.1: `{version, body, id, signatures}`, `version` equal to
`swarm-envelope/2`, one `author` signature, the body in CCJ-1 (section 2.2),
times as `YYYY-MM-DDTHH:MM:SSZ`, and the limits of that section. This LIP adds
no second format.

#### 5.1. Members of every body kind

| Member | Rule | Source |
| --- | --- | --- |
| `type` | `owner-command/1`, `instruction/1` or `wallet-request/1` | Proposed here |
| `aud` | The executor, by its `id/` name. The executor compares it with its own name byte for byte. | `swarm-envelope/2` section 2.1 |
| `nonce` | The anti-replay number: 16 random bytes, canonical unpadded base64url | The same |
| `iat`, `exp` | Signing time as claimed, and the expiry; `iat < exp` | The same |
| `devices` | `{"seq":…,"sha256":…}`, the pin of the device list that the envelope relies on (section 5.3) | Proposed here |
| `device_list` | Optional: the exact octets of that list, canonical unpadded base64url | Proposed here |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O5.1 | There is one envelope format, `swarm-envelope/2`, and it has three typed body kinds: the owner command, the LIP-0013 instruction and the wallet request. | `ENVELOPE_SHAPE` |
| O5.2 | Every envelope names the executor, an anti-replay number, an expiry and the device-list hash. | `ENVELOPE_SHAPE` |
| O5.3 | An attached list MUST hash to `devices.sha256`, and it is never a source of the pin: the executor reads the pin from the name (section 9). | `DEVICE_LIST_MISMATCH` |

The proposed tags and lifetimes:

| Type | Tag | Signer | Largest `exp − iat` |
| --- | --- | --- | --- |
| `owner-command/1` | `swarma-link owner-command/1` | One device of the owner's current list | 120 seconds, as `operator-act/1` |
| `instruction/1` | `swarma-link instruction/1` | The grantee key of the grant it cites | 900 seconds, the window of LIP-0013 step 4e |
| `wallet-request/1` | `swarma-link wallet-request/1` | The grantee key of the grant it cites | 900 seconds |

#### 5.2. The three body kinds

**Owner command.** The owner's word to an own executor or an own key holder.

| Member | Rule |
| --- | --- |
| `level` | `0`, `1` or `2` (section 6) |
| `action` | One class of the registry (section 2) |
| `fields` | The typed fields of the class, complete under O1.3. `{}` for a class that is work. |
| `text_sha256` | SHA-256 of the exact UTF-8 octets of the free text, 64 lowercase hex; the hash of the empty string when there is none. The text travels beside the envelope, as the text of `message/1` does. |

The fields of the two effects that decision 1 names:

| Class | `fields`, in CCJ-1 |
| --- | --- |
| A landing (`land`) | `repository`, in the grammar of LIP-0013 section 2.3; `ref`, a full ref name such as `refs/heads/main`; `revision`, the full commit identifier in lowercase hex |
| A payment (`spend`) | `to`, `amount_sat` and `fee_limit_sat`, as the `spend` parameters of LIP-0006 section 3 |

Under decisions 1 and 10 the confirmation of one operation of LIP-0014 J5.9
is an owner command. Its
fields are the members that J5.9 names: the `event_id` of the request, the
`grant_id`, the action, the resolved target and the content of the effect. J5.9
leaves the wire form to the deployment; this kind is that form.

**LIP-0013 instruction.** The instruction of LIP-0013 section 3, moved from a
kind-8185 event into this format. Its members are the tags 2 to 9 of LIP-0013
section 3.2 under the same rules: `aud` in place of `to`, `nonce` in the
common form, and `grant`, `action`, `text_sha256` in place of `body`, `room`
and `mxid`. For `spend` it adds `amount`. For `land` it adds `repository`,
`ref` and `revision` in place of `repo`, because O1.3 needs the ref and the
revision.

**Wallet request.** The request of LIP-0006 section 2 in this format: `aud` in
place of `service`, `iat` in place of `created_at`, the common `nonce`, the
author's key in place of `grantee`, and `action`, `params` and `grant` as
LIP-0006 section 3 has them. The implemented wallet service v1 profile keeps its
own bytes; this kind is for its successor.

#### 5.3. The device-list pin of each kind

An owner command carries the pin of the list that holds its signing device.
An instruction and a wallet request are signed by a grantee key and not by a
device. For them the draft proposes the pin of the list of the owner whose
name the signing agent's landlord pointer names. The other reading is in the
open questions.

#### 5.4. Registration in `swarm-envelope/2`

`swarm-envelope/2` admits only the types of its section 2.1 and the tags and
signature profiles of its section 2.4, and both tables are closed. The three
types, their tags and their signature profiles enter it only through a
reviewed change of that specification, which Swarma Envelope owns. Until then
no verifier admits them, and this LIP is a request to that change. The
conflicts with its section 2.4 are listed under "Reconciliation".

### 6. Levels and the level of a launch

| Level | What it admits | Who signs it | What a run started at it may sign (O6.7) |
| --- | --- | --- | --- |
| L0 | Work: a run is started or directed; no effect | A device of the current list with `ceiling` 0 or more | No object whose action ends in an effect |
| L1 | Effects within the limits of the executor's policy (section 7) | A device with `ceiling` 1 or more | Effects of the classes that the policy for the executor assigns to L0 or L1, within its L1 limits |
| L2 | What the policy assigns to L2; a class outside the registry (O2.3); the policy itself (section 7); the fast revocation (section 8.2) | A device with `presence` `true` and `ceiling` 2, or a separated human console | Effects of every class that the policy for the executor admits, within its L2 limits, and a class outside the registry; never the policy or a revocation (O6.12) |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O6.1 | The `level` of an owner command MUST NOT exceed the `ceiling` of its device. | `LEVEL_ABOVE_DEVICE` |
| O6.2 | L2 is signed only by a key whose record has the presence flag, or given at a separated human console. | `LEVEL_ABOVE_DEVICE` |
| O6.3 | A separated human console is a console of the executor's host under an OS account of a person, in which no agent has a shell and to whose input no agent's process can write. A console of a host where agents have shells is not L2, and an executor MUST NOT admit L2 from it. | `LEVEL_ABOVE_DEVICE` |
| O6.4 | An action whose class the executor's policy assigns to a level above the command's `level` refuses. | `LEVEL_TOO_LOW` |
| O6.5 | A launch inherits the level of the envelope that started it. The origin of a run that an owner command starts is that command's identifier and its `level` (extends LIP-0013 J7.1). A run that a run creates, and a run that is resumed, has the level of the run it comes from. | |
| O6.6 | The key holder's table has a row for the owner's commands at each level, L0, L1 and L2, in place of the one owner row of J7.2. A run signs only under the grants of the row of its origin's level. A row selects the grants a run may use; it does not bound what is signed under them, which O6.7 does. | `GRANT_NOT_FOR_RUN` |
| O6.7 | For a run whose origin has level N, at every level L0, L1 and L2, the key holder MUST refuse to sign an object for the run when an action that the object authorizes (a) ends in an effect (LIP-0018 section 3, LIP-0006 section 7) and N is L0; (b) has a class that the policy for the executor at which the action takes effect assigns to a level above N, or a class outside the registry while N is below L2 (O2.3); or (c) states an amount, a count or another limited quantity above the limit that this policy sets for its class at level N. The rule holds under every grant of the identity, whatever the run's row lists. The objects are those of J7.5: an envelope, a v4 invocation, a consent to a contract, a delegation request and a request to a delegation signer; for a consent and for a request, the actions and the quantities are those that the contract or the parent allows. An agent started at level N cannot reach, through its own grants, an effect that the policy reserves for a level above N or that exceeds its limits at N. | (a), (b) `LEVEL_NOT_FOR_RUN`; (c) `LIMIT_OVER` |
| O6.8 | The level of a run, like its origin, is kept outside the agent's write authority and never changes. A caller cannot state it. | Nothing is signed |
| O6.9 | The key holder takes the policy from the owner's devices and from nothing else. An L2 device of the current list sends it each policy section as the owner command of section 7, with `aud` the key holder; the section names the executor that it bounds (O7.4). The key holder runs steps 1 to 12 of section 11 on it, keeps the latest section that it accepted for each named executor, journals that section's `seq` per executor outside the agents' write authority, and refuses a lower one, and an equal `seq` with other octets (O7.3). It never takes policy from an executor, an agent, a run or a caller. | `CONFIG_ROLLBACK` and the refusals of section 11 |
| O6.10 | Where the key holder holds no accepted section for the executor at which an action takes effect, or the object does not name that executor, it signs no object whose action ends in an effect for a run at any level, as an executor without a section admits none (O7.5). This holds at a foreign executor too: the owner bounds its agents' runs there by a section that names that executor, which only the owner's key holders read and the foreign executor never does (O10.4). | `LEVEL_NOT_FOR_RUN` |
| O6.11 | Where the policy states a limit as a total over a period, the key holder counts every object that it signed under that limit for runs of that level, for that executor, within the period. It journals the count outside the agents' write authority before it releases the signature. A key holder that cannot show the count signs nothing more under that limit within the period. | `LIMIT_OVER` |
| O6.12 | No level lets a run sign as the owner. A key holder MUST NOT hold a device key of the owner, so no run, an L2 run included, signs an owner command, and with it no policy section (O7.2) and no revocation (section 8.2). | Nothing is signed |

O6.5 to O6.12 close the gap that the reviewer named, at every level. A command
at level N starts a run that keeps N for its whole life and for its children.
Its key holder signs, under the agent's own grants, no effect when N is L0;
when N is L1 or L2 it signs only the classes that the policy for the named
executor admits at N, within the limits that the policy sets at N. The
executor does not see a run's level: a v4 invocation carries none, and section
11 admits owner commands only. The bound is therefore held at the key holder,
and O6.9 gives the key holder the policy for that. The LIP-0013 actions `land`
and `spend` and the wallet `spend` are effects; `instruct` and `review` are
work.

### 7. Executor policy

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O7.1 | Policy maps each action class to the level it requires and to its limits. It MUST NOT be in the device list or in a name value. | |
| O7.2 | Policy lives in signed executor configuration sections, the configuration statements of LIP-0015 section 3, with an increasing `seq`. A section is signed by an L2 device of the current list, and not by the grant key. | `STATEMENT_SIGNATURE` |
| O7.3 | Each executor journals the highest `seq` that it accepted for its policy, outside the agents' write authority, and refuses a lower one. | `CONFIG_ROLLBACK` |
| O7.4 | Every limit belongs to a named executor. A section names exactly one executor, by its `id/` name and pinned key (LIP-0008 section 4), and an executor accepts only a section that names it. A limit that names no executor, or one total for several executors, refuses. | `POLICY_INVALID` |
| O7.5 | Without an accepted section an executor admits no effect: it runs at its most restrictive level, as LIP-0015 section 4 has it for a failed load. | `LEVEL_TOO_LOW` |

The draft proposes that a section reaches the executor as an owner command at
L2 whose action is `swarma/config` and whose fields are the six members of the
configuration statement of LIP-0015 section 3, with the section's octets
attached. The device then signs an envelope, and P-256 stays for envelopes
only (O4.6). The same section reaches each key holder of the owner's agents
in a second command whose `aud` is that key holder (O6.9). The other reading is in the open questions. Equal `seq` with
other octets refuses as `CONFIG_ROLLBACK`.

### 8. Revocation of a device

#### 8.1. By the spend of the seal

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O8.1 | Revocation of a device is the spend of its seal. | |
| O8.2 | When a device is added, a spend of its seal is prepared and given to the other devices of the list. Each of them holds it and can broadcast it without the revoked device. | |
| O8.3 | An own executor's node watches the seal of every device of the list that the executor holds. When it sees a spend of a seal, in its mempool or in a block, the executor journals the closure of that device durably, before it admits another envelope. | |
| O8.4 | After a closure the executor refuses every envelope signed by the key of that device. A rollback cannot restore it: a list of lower `seq` refuses (section 9), a list that names the device names the same spent seal, and a journaled closure is not lifted by a later list, a name update or a reorganisation. | `DEVICE_REVOKED` |
| O8.5 | A seal outpoint that was spent is never named again by a device record. | `DEVICE_REVOKED` |

#### 8.2. The fast path and its completion

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O8.6 | An L2-signed revocation is an extra fast path: an owner command at L2 whose action is `swarma/device/revoke` and whose fields are the `key` and the `seal` of the device. Every executor that receives it journals the closure of that device forever, and from then refuses the device as O8.4 does. | `DEVICE_REVOKED` |
| O8.7 | A name update completes the revocation: a new list without the device, with a higher `seq`, under section 9. | |

The seal is the fast path that does not depend on reaching each executor: a
node sees the spend in its mempool within the time a transaction takes to
propagate, at every executor at once. The L2 command reaches only the
executors to which it is delivered, and none of them depends on the chain for
it. The name update makes the removal visible to an executor that saw neither.

### 9. Adding a device

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O9.1 | Adding a device needs a new device list that holds its record, the device's new seal, and an update of the owner's name signed by the name-owner key that writes the new `swarma-devices` with a higher `seq`. | |
| O9.2 | An executor takes a list only through the pin in the owner's name value on its own node, in its validated active chain, and only with a `seq` higher than the highest it journaled. An envelope, an attachment or a message never adds a device. | `DEVICE_LIST_ROLLBACK` |
| O9.3 | The prepared spend of the new seal MUST reach the other devices under O8.2 before the new device signs anything. | |

Adding is slow and guarded by design; removing is fast. The reviewer's figures
for the wait are a median of about seven minutes for a confirmation and more
than thirty minutes in five cases of a hundred, plus the time to fetch the cold
name-owner key. A thief of one device cannot add a second one, and every
device can remove a stolen one at once.

### 10. Key boundaries

| Rule | Requirement |
| --- | --- |
| O10.1 | The name-owner key decides who speaks for the owner. It does so by the device-list pin in the name and by nothing else of this LIP. |
| O10.2 | The grant key grants to others only. It signs grants and what a grant needs: the contract hash of `landlord_sig`, on v3 the spend of a seal that pays it, and on v4 the endorsement of a seal key (LIP-0004 sections 2, 3 and 5; LIP-0008 section 11). It signs no statement, no configuration, no device list and no envelope. |
| O10.3 | Device keys are the owner at the owner's own executors and at the key holders of the owner's agents. |
| O10.4 | At a foreign executor nothing changes: the owner remains a grantee there, and a device key gives nothing. |
| O10.5 | There is no separate BIP-340 statement key. A statement is pinned in the name or signed by an L2 device. |

| Key | Decides or signs | Never |
| --- | --- | --- |
| Name-owner key | Updates of the name; with them the device-list pin | Directs work; signs an envelope |
| Grant key | Grants to others | Statements, configuration, envelopes |
| Device key, L0 or L1 | Owner commands up to its ceiling, at own executors and own key holders | L2; anything at a foreign executor |
| Device key, L2 with presence | The same at L2, policy sections and fast revocations | Anything at a foreign executor |

#### 10.1. Where R5 closes

R5 closes in O10.2 and O10.5. Policy sections leave the grant key for L2
devices (O7.2), the owner's devices need no certificate statement because the
list in the name binds them, and no statement key is added. The authority key
of a person (key map, K6) leaves the key map in favour of device keys: where
K6 had the person sign with presence at each signature, the person's device
signs, with the claimed presence of its record. Until the co-author agrees, K6
stands as written. How far O10.2 reaches into the other statement domains of
LIP-0015 section 2 is an open question.

### 11. Admission of an owner command

The executor `X` runs these steps in order and stops at the first refusal. The
order and the codes are the draft's proposal.

| # | Step | Refusal |
| --- | --- | --- |
| 1 | The envelope parses as `swarm-envelope/2` with the expected type from the channel, and its identifier recomputes | `ENVELOPE_SHAPE` |
| 2 | `aud` equals the name of `X` | `NOT_FOR_ME` |
| 3 | `iat` is not in the future beyond the skew of `X`, `exp` has not passed, and `exp − iat` is within the lifetime of section 5.1 | `STALE` |
| 4 | `X` reads the owner's name on its own node: a valid `swarma-devices`, with a `seq` not lower than its journaled highest | `DEVICE_PIN_INVALID`, `DEVICE_LIST_ROLLBACK` |
| 5 | `devices` equals the pin; the list that `X` holds, or the attached one, hashes to it | `DEVICE_LIST_MISMATCH` |
| 6 | Exactly one signature, whose key equals the `key` of one record, under that record's `alg` | `DEVICE_UNKNOWN`, `DEVICE_ALG_MISMATCH` |
| 7 | The signature verifies | `ENVELOPE_SIGNATURE` |
| 8 | No closure of the device is journaled, and its seal is unspent in the view of the node | `DEVICE_REVOKED` |
| 9 | `level` within the device's ceiling and presence (O6.1 to O6.3) | `LEVEL_ABOVE_DEVICE` |
| 10 | The class is in the registry, or the level is L2 (O2.3); the policy's level for the class is at most `level` (O6.4, O7.5) | `ACTION_UNKNOWN`, `LEVEL_TOO_LOW` |
| 11 | The identifier is not in the replay journal; on success it is recorded with the exact bytes | `REPLAY` |
| 12 | The fields are complete for the class, and the limits of the policy section hold | `FIELDS_INCOMPLETE`, `LIMIT_OVER` |
| 13 | Immediately before the effect, the gate recomputes the actual arguments and compares them with the fields (O1.4) | `FIELDS_MISMATCH` |

A refusal at any step leaves no effect and no reservation. A key holder runs
steps 1 to 11 for an owner command that starts or directs a run, and records
the command's identifier and level as the run's origin (O6.5). It runs steps
1 to 12 for a policy section addressed to it (O6.9).

### 12. Cases

Each case pairs a valid control with its refusal. Their identifiers begin
with S29.

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S29-1 | Alisa's phone `P` (`p256`, presence, ceiling 2) signs an L1 landing at `X` with repository, ref and revision; the gate finds the same commit: admitted | The same message without an envelope, in the owner channel: ignored, no run. The model of `X` rewrites `revision` before the gate: `FIELDS_MISMATCH`. |
| S29-2 | An L1 payment with `to`, `amount_sat` and `fee_limit_sat` | The text says "pay Karl 5000", the fields name no payee: `FIELDS_INCOMPLETE`; the text never fills a field. |
| S29-3 | Laptop `M` (`bip340`, no presence, ceiling 1) signs L1 | `M` signs L2: `LEVEL_ABOVE_DEVICE`. A list that gives `M` ceiling 2 without presence: `DEVICE_LIST_INVALID`. |
| S29-4 | The record of `P` says `p256`; `P`'s envelope verifies under P-256 | A `bip340:` identifier whose 32 bytes equal the `x` of `P`'s key: no record has those key bytes, `DEVICE_UNKNOWN`; the verifier never tries BIP-340 on a record that says `p256`. |
| S29-5 | An L0 command starts a run; the run signs an `instruct` envelope under grant `G` | The same run asks its key holder to sign a `land` envelope or a `spend` invocation under `G`, which lists both: `LEVEL_NOT_FOR_RUN`. A child run of it: the same. A caller that states L1 for it: nothing is signed. |
| S29-6 | `P` re-signs an envelope with a fresh nonce: a new identifier, admitted | The same body with a second valid P-256 signature: the same identifier, `REPLAY`. |
| S29-7 | `K` broadcasts the prepared spend of `M`'s seal; `X` journals the closure | `M` signs after the spend is in the mempool: `DEVICE_REVOKED`. A name update back to a list of lower `seq` that names `M`: `DEVICE_LIST_ROLLBACK`; a new list that names `M` with the same seal: `DEVICE_REVOKED`. |
| S29-8 | `P` signs `swarma/device/revoke` for `M` at L2; `X` journals it | `M` signs at `X` after that, even before the seal is spent: `DEVICE_REVOKED`. |
| S29-9 | A confirmed name update with a higher `seq` adds `K`; `X` admits `K` | An envelope with `K`'s record attached and a pin that the name does not carry: `DEVICE_LIST_MISMATCH`. The update still in the mempool: `K` is unknown to `X`. |
| S29-10 | A policy section with `seq` 7 for `X`, signed by `P` at L2 | A section with `seq` 6 after 7: `CONFIG_ROLLBACK`. One signed by `M`: `LEVEL_ABOVE_DEVICE`. One signed by the grant key: `DEVICE_UNKNOWN` as an owner command, `STATEMENT_SIGNATURE` as a LIP-0015 statement. A section with a total for `X` and `Y`: `POLICY_INVALID`. |
| S29-11 | An L2 command for a class outside the registry reaches step 12 | The same class at L1: `ACTION_UNKNOWN`. |
| S29-12 | Bob's executor `Y` admits Alisa's agent under a grant from Bob | An owner command of Alisa's device at `Y`: `NOT_FOR_ME` for an `aud` of `X`; for an `aud` of `Y`, `DEVICE_LIST_MISMATCH`, because `Y` reads the pin of Bob's name. |
| S29-13 | An L2 command from a console of a human OS account without agent shells | The same command typed at a console of a host where agents have shells: `LEVEL_ABOVE_DEVICE`. |
| S29-14 | Laptop `M` (no presence, ceiling 1) signs an L1 `instruct` that starts run `R` of agent `A`. The section for `X` that `A`'s key holder accepted assigns `land` to L2 and caps an L1 `spend` at 10000 sat a day. `R` asks for a v4 `spend` invocation of 4000 sat at `X` under `G`, which lists `land` and `spend`: signed | `R` asks for a `land` invocation at `X` under `G`, which its L1 row lists: `LEVEL_NOT_FOR_RUN`. A `spend` of 12000 sat: `LIMIT_OVER`. A third `spend` of 4000 sat on the same day: `LIMIT_OVER` (O6.11). A child run of `R`, or a caller that states L2 for `R`: the same refusals. |
| S29-15 | Phone `P` (presence, ceiling 2) signs an L2 `instruct`; its run asks for a `land` invocation at `X` under `G`, within the L2 limits of `X`'s section: signed | The same run asks for a `spend` above the L2 limit: `LIMIT_OVER`. A `land` at executor `Z`, for which the key holder holds no section: `LEVEL_NOT_FOR_RUN` (O6.10). A policy section or a `swarma/device/revoke` for the run: nothing is signed (O6.12). A section for `X` with `seq` 6, after 7, sent to the key holder by `P`: `CONFIG_ROLLBACK`. The envelope of `X`'s own section, relayed by `X`: `NOT_FOR_ME`, because its `aud` is `X` (O6.9). |

## Honest limits

The decision asks that these limits stand in the text and not be hidden.

- **A key without presence is available to any code on its device.** An
  orchestrator that runs as the owner on the owner's laptop can make the
  laptop's key sign. L1 on such a device means "any code on this laptop", and
  the owner sets L1 limits for that. A device key without presence belongs
  under an OS account other than the one where agents run.
- **The presence flag is claimed, not proven.** The verifier reads the
  owner's claim in the record. On Apple platforms `.userPresence` accepts the
  passcode in place of biometry. One touch can cover several signatures when
  the authentication context is reused. The screen of the device that shows
  the fields is not trusted: what it shows may differ from what the key
  signs. No signer provider is qualified for exact-content presence
  (`swarm-envelope/2` section 4: "no signer provider is qualified for A3"),
  and L2 by presence rests on the owner's enrollment until one is.
- **A host console is not L2 when agents have shells there.** An agent with a
  shell on the host can write into a console of the same account, or into
  what that console reads. O6.3 admits only a console of a separate human
  account.
- **The gate is local.** O1.4 and O6.7 hold at an honest executor and an
  honest key holder. The level of a run is checked at its key holder alone:
  a v4 invocation carries no level, so the executor cannot refuse an effect
  that a dishonest key holder signed beyond it. No receiver sees that the key
  holder refused, as LIP-0013 section 3.6 already says of J7.
- **One presence act covers an L2 run.** Presence is given once, for the
  command that starts the run. Every effect that the run then signs within
  its L2 row and the L2 limits rests on that act, and no person sees each
  effect. The owner bounds this by the L2 row and the L2 limits only (open
  questions).
- **A run of any level can still instruct.** O6.7 bounds what a run signs
  under its own grants. An `instruct` envelope that it sends to another agent
  starts a run whose origin is that instruction's grant (J7.6), and that
  origin's row decides what the second run may sign. The level does not
  travel with the instruction (open questions).

## Rationale

- **Only the hash of the device list in the name.** The name-owner key is
  cold. A pinned document that held the policy would make that key sign every
  change of a limit, and grow the value from about 175 to about 340 of 520
  bytes (the reviewer's figures). The hash with a version costs 103 bytes and
  changes only when a device is added or removed.
- **The member outside `swarma`.** A v4 grant lives while the owner and
  `swarma` stay unchanged (LIP-0008 section 3). A device change inside
  `swarma` would end every v4 grant of the owner.
- **Policy in configuration sections.** Limits change more often than
  devices. LIP-0015 already has a signed, numbered section and a loader that
  refuses a lower number; an L2 device signs it without the cold key.
- **Revocation by seal.** A spend is seen by every node at once, from the
  mempool, without delivering anything to each executor, and a seal once spent
  stays spent: an older list cannot bring the device back. LIP-0008 section
  5.1 already treats a validated mempool spend as a durable closure.
- **Slow to add, fast to remove.** A stolen device must not be able to add a
  second one; every honest device must be able to remove a stolen one.
- **P-256.** The Secure Enclave holds P-256 keys only. Without P-256 the
  owner's best custody is unavailable for the keys that speak for the owner.
  `swarm-envelope/2` already verifies P-256 for operator devices.
- **The identifier without the signature.** ECDSA signatures are malleable
  and not unique, so an identity derived from them can be multiplied.
- **One envelope format.** Three formats for one owner's three kinds of word
  need three parsers and three replay journals at one executor. The platform
  already has `swarm-envelope/2`.
- **The level inherited by the launch.** A level that bounded only the first
  envelope would bound nothing: the run it starts holds the agent's grants.
  A level that bounded only L0 would leave an L1 run every class and every
  amount of its grants, L2 classes included.
- **The policy at the key holder.** The executor does not see the run's
  level, so only the key holder can compare an object with the policy at that
  level. It takes the section from the owner's L2 device, as the executor
  does, and not from the executor, which an agent may share a host with.
- **The grant key grants only.** A key that grants to others and configures
  the owner's own machines makes one leak do both. A separate statement key
  would add a key and keep the cold key on every change.

## Reconciliation

This LIP cites the platform book, the Link book, the curator specification and
Swarma Envelope instead of restating them. The revisions read are:
`relux-works/swarma-docs` at `34abef2`, `relux-works/curator-spec` at
`ab6b1b0` and `relux-works/swarma-envelope` at `065e25f`.

| Source and section | What it says | Relation to this LIP |
| --- | --- | --- |
| Platform book, ch. 6 "Keys and the key holder", §6.6 "The operator signs one act" (`book/ru/06-klyuchi.md`, lines 106–113) | A widening act needs a human boundary. The phone signs the exact content it shows, with a non-exportable Secure Enclave or StrongBox key under biometry, over SSH into a narrow operator command; the machine verifies against the pinned phone key. Revocation takes one touch. | The same principle as O1.5 and the L2 of section 6. The anchor differs: a key pinned at the machine there, the device list in the name here (conflict X3). |
| Same chapter, §6.6.1 "Registration, the second device and a lost phone" (lines 114–121) | Pairing by QR at installation; a second device, a FIDO2 key or a second phone, is mandatory; the second device replaces or revokes a lost key; the fallback is password `sudo` into the operator account. | Section 9 makes adding a name update and section 8 makes removal a seal spend (X4, X5). The fallback meets O6.3 (X11). |
| Same chapter, §6.6.2 "General stop" (lines 122–135), and ch. 7 §7.12 "General stop" (`07-zapusk-i-host-sessiy.md`, lines 179–183) | One operator command signed by the phone stops every service; only the operator's signature resumes; the keeper may hold a grant to stop. | No decision of this LIP gives the stop a level (X13). |
| Same chapter, §6.7 "The owner's registry on the trust node" (lines 136–175) and §6.8 "Roles of the roots" (lines 176–191) | The owner's registry on a trust node stores keys, attestations and revocations; an operator root attests operator devices; revocations are root-signed snapshots. | A second anchor for the owner's devices (X3) and a second way to revoke them (X4). |
| Ch. 22 §22.5 "Stop by one signature" (`22-effekty-ostanovka-federaciya.md`, lines 73–84) | A stop of the protocol by the key of one core node; resumption by a quorum. | A different mechanism, not changed here (X13). |
| Ch. 24 §24.4 and §24.8 (`24-soobscheniya-i-most.md`, lines 56–78 and 109–126) | Assurance levels A0 to A3 for people's messages; an unsigned body is untrusted data; a transitional mode admits A0 and A1 commands within zones. | Decision 1 ignores an unsigned message; L0 to L2 have no stated mapping to A0 to A3 (X1, X11). |
| Ch. 13 §13.4 (`13-doverennosti.md`, lines 68–70) | Actions are added at run time by signed `handler-manifest/1` and `action-namespace/1` records. | Decision 2 makes a new action a LIP section plus code (X2). |
| curator-spec CIP-0011 revision 6, R-OPERATOR (`cips/CIP-0011-credential-broker-and-agent-users.md`, lines 24–26; §5, lines 126–153; §5.2, lines 136–141) | A presence-gated operator device key in the phone's secure element signs each exact act; the machine verifies against the pinned phone key; password `sudo` from a terminal is the fallback, widening included, with content confirmation; signature domain and bytes are unpublished. | The device class of this LIP. Conflicts: the pin at the machine (X3), the fallback for widening (X11), and the unstated relation between operator acts on one machine and owner commands to executors (X14). |
| Link book §3.4 "Three keys of a participant and the agent's identity" (`link-book/ru/03-klyuchi.md`, lines 87–115) | Three keys of a participant; the LIP-0004 reader refuses an extra member. | O3.9. Device keys stand beside the three keys (X15). |
| Link book §3.7 "The agent's key holder" (lines 140–157) | The owner's command is an origin at the key holder, and its row lists the operator's grants. | Revised by O6.5 to O6.12: the origin carries a level, and the level bounds what the run signs. |
| Link book §3.10 to §3.12 (lines 236–311) | Signed configuration, key statements and their store, signed by the grant key. | Revised by O7.2 and O10.2 (X6, X7). |
| Link book §3.13 "Devices and recovery" (lines 312–318) | Devices and recovery; no format for a device attestation. | The device record of section 3.1 is that format for the owner's devices. |
| Link book §4.9.2 "The executor" (`04-doverennost.md`, lines 310–319) | A limit of a grant belongs to a named executor. | O7.4 applies it to the limits of a policy section. |
| Link book §4.9.3 "The issuer's name: registration and owner key" (lines 320–342) | A v4 grant lives while the owner and `swarma` stay. | O3.8. |
| Link book §4.9.4 "Re-delegation and child grants" (line 375) | The owner's confirmation of one effect, which the executor compares with the actual arguments. | O1.4 generalizes it to every effect; LIP-0014 J5.7 and J5.9 are its text in this repository. |
| Link book §4.9.10 "Checking the seal spend before issuance" (lines 511–522) | A seal spend signed in advance and kept in the signer's journal; its fee is fixed when it is signed. | O8.2 follows the pattern; the holders are the other devices, which is new (X4). |
| Link book §5.2 "Two profiles" (`05-otzyv.md`, lines 17–51) | On v3 a pending change refuses without closure. | O3.10. |
| Link book §8.9 "Delivery between agents" (`08-arenda.md`, lines 253–268) | The owner tasks its agent over its own channel; no envelope is needed for that. | Revised by O1.1 (X1). |
| `swarm-envelope/2` §§2.1 to 2.4, 4 and 5 (Swarma Envelope, `spec/swarm-envelope-2.md`) | The envelope, its identifier over the body, P-256 and BIP-340 key identifiers, the closed tables of types, tags and signature profiles, `operator-act/1`, and A3 inactive in v0. | Sections 4 and 5 adopt its envelope and cryptography; X8 to X11 list the conflicts. |

The brief places the four sections of the platform book in "ch. 05". In the
book at `34abef2` they are §6.6, §6.6.1, §6.6.2 and §6.7 of chapter 6;
chapter 5 is "An OS user per agent and the agent's network".

**Conflicts for the owners.** The decisions and these sources disagree in the
following points. This LIP writes the decisions and chooses none of the
conflicts.

| # | Decision | Conflict |
| --- | --- | --- |
| X1 | 1 | The book keeps an unsigned body as untrusted data and admits A0 and A1 commands in a transitional mode (§24.4, §24.8); the Link book lets the owner task its agent without an envelope (§8.9); LIP-0013 section 3.7 point 2 says the same. Decision 1 ignores every unsigned message. |
| X2 | 2 | The book registers actions at run time by signed records (§13.4). `swarm-envelope/2` section 4.1 refuses an unknown operation outright and has no branch for L2. |
| X3 | 3, 4, 6 | Three anchors for the owner's devices: a phone key pinned at the machine (book §6.6; CIP-0011 §5.2), an operator root that attests devices in the owner's registry (book §6.7, §6.8), and the device list in the name. `swarm-envelope/2` section 2.1 says that device trust comes from the operator root "not a second device-key pin list". |
| X4 | 5 | The book revokes in the registry by root-signed snapshots (§6.7). A P-256 device cannot sign a Namecoin spend, so a prepared spend is signed in advance by a secp256k1 key, with its fee fixed at signing (Link book §4.9.10). |
| X5 | 6 | The book pairs the second device by QR at installation and has it replace a key (§6.6.1); CIP-0011 proposes re-enrolment at a terminal. The book's FIDO2 backup key cannot sign `swarm-envelope/2` (section 2.4 there refuses WebAuthn assertions). |
| X6 | 7 | LIP-0015 section 3 and Link book §3.10 have the grant key sign configuration, with a `not_after`; decision 7 has an L2 device sign it. The rule of the increasing number matches LIP-0015 step 6. |
| X7 | 8, 12 | Link book §3.4 and §3.8, key map K6 and the key registry define the authority key of a person; LIP-0015, LIP-0016 and Link book §3.10 to §3.12 put statements on the grant key. Removing K6 leaves no BIP-340 key of the person for a v3 grant at a foreign executor (open questions). |
| X8 | 4, 9 | `swarm-envelope/2` section 2.4: an operator device key MUST be P-256, and BIP-340 is admitted only as the author of `message/1`. Decision 4 admits BIP-340 device keys. |
| X9 | 4 | In `swarm-envelope/2` the algorithm is the prefix of the key identifier in the signature entry. O3.1 reconciles the two: the identifier must agree with the record, and the record decides. |
| X10 | 10 | `swarm-envelope/2` is the name of the platform's signed-records format, whose types are closed and already include `operator-act/1`, close to the owner command. The LIP-0013 instruction is a Nostr event and the wallet request has bytes of its own. Decision 10 needs a change in Swarma Envelope or another version name. |
| X11 | 11, 13 | The existing ladders are A0 to A3 (book §24.4; `swarm-envelope/2` section 5), and A3 is inactive in v0 because no signer provider is qualified. CIP-0011 §5.2 and book §6.6.1 accept password `sudo` at a terminal for widening; `swarm-envelope/2` section 4.1 refuses an unsigned fallback for widening; decision 13 says that a host console is not L2 where agents have shells. |
| X12 | 11 | The Link book §3.7 and LIP-0013 J7 key the table by origin only, and a receiver cannot verify an origin (LIP-0013 section 3.6). The level holds at an honest key holder only. |
| X13 | — | No decision gives the general stop a level. The book has the phone sign it while the keeper may hold a grant to stop (§6.6.2, §7.12); `swarm-envelope/2` and CIP-0011 let narrowing go without presence; the stop of ch. 22 is another mechanism. Decision 5 puts the fast revocation of a device at L2. |
| X14 | — | Several operators with M of N confirmations (book ch. 12) are not addressed, nor the relation between CIP-0011 operator acts on one machine and the owner commands of this LIP. |
| X15 | 8 | Key map K1 gives a principal three keys and no administrative key; device keys are further keys of the principal. |

## Alternatives

- **The whole control document pinned in the name**, policy included: the
  cold name-owner key signs every change of a limit, and the value nearly
  doubles. Rejected by decisions 3 and 7.
- **A separate statement key under BIP-340**: one more key, and the name-owner
  key still signs every change. Rejected by decision 8.
- **Device keys bound by Matrix certificate statements and stored under
  LIP-0016**: a binding gives no authority (LIP-0015 section 6), and the store
  adds a host and a chain of heads. The reviewer's answer removed them for
  owner devices.
- **The head of a store in the name value**, as LIP-0016 lists among its
  alternatives: the name would pin a set of statements and not a list of keys.
  This LIP pins the list itself.
- **Device trust from an operator root and signed attestations**, as
  `swarm-envelope/2` section 2.4 has it: a root key and a registry on a trust
  node. The decision puts the list under the name-owner key instead; the
  conflict is listed under "Reconciliation".
- **BIP-340 only**: the Secure Enclave cannot hold such a key.
- **A second envelope format for owner commands** beside the instruction and
  the wallet request: rejected by decision 10.
- **A level that bounds only the first envelope**: the reviewer's main gap.
- **An L1 bound in the rows alone**: the operator writes the L1 row so that
  its grants stay within the L1 limits. Not taken: one grant may allow both an
  L1 and an L2 class, and a row has no limit of its own, so O6.7 checks each
  object against the policy.
- **A level in the v4 invocation, checked by the executor**: the invocation
  has no member for it, and a foreign executor does not hold the owner's
  policy. Not written; open questions.

## Security consequences

- **A stolen device signs up to its ceiling until it is revoked.** The spend
  of its seal stops it at every executor whose node has seen the spend; the
  L2 command stops it where it is delivered. Effects admitted before the
  closure are not undone.
- **A stolen L2 device can revoke the other devices.** It holds their
  prepared spends and can sign `swarma/device/revoke` for each. It cannot add
  a device. Recovery goes through the name-owner key: a new list, new seals
  and a name update.
- **A prepared spend is a bearer of revocation.** Whoever copies it can
  revoke that device. That denies the owner one device and gives nothing else.
- **A stolen name-owner key decides who speaks for the owner.** It writes a
  list of its own devices. A v4 grant does not end, because `swarma` and the
  owner stay; the owner's own executors follow the new list. Custody of the
  cold key is the defence, as for the name itself (key map).
- **A lying node defeats the pin and the seals.** An executor reads both on
  its own node; the node's credentials must be out of the agents' reach
  (LIP-0015, security consequences).
- **An executor that has not seen a spend admits the device.** Until its node
  receives the transaction the seal looks unspent. LIP-0022 bounds how long a
  view may stand still for an action that moves money.
- **The replay journal must not go back.** A restored journal admits an
  identifier again inside its window; the windows of section 5.1 bound that,
  and LIP-0025 states how a journal shows its continuity.
- **A level does not cross an instruction to another agent** (Honest limits).
- **A run's level holds at its key holder.** A compromised key holder signs
  beyond the level, and the executor cannot see it (Honest limits). A key
  holder that lacks or loses an executor's section signs no effect for that
  executor (O6.10), so a lost section fails closed.
- **The key holder's policy comes from the owner's devices only.** A section
  that an executor or an agent relays is not accepted, and an older one
  refuses as `CONFIG_ROLLBACK` (O6.9). A stolen L2 device can still widen the
  limits, as it can at the executor.
- **The grant key can no longer configure.** A leak of it issues grants and
  spends v3 seals, and changes no policy and no device list.

## Conformance impact

None on normative v0.1 and none on Grant v3 bytes. No vector is added. A
future vector set holds: a device record and a list in exact bytes with their
hashes, and each neighbour that one defect makes invalid; the name value with
`swarma-devices` beside the LIP-0010 values, and a LIP-0004 reader that
refuses it; P-256 signatures with a high `s`, in DER and over another tag; an
identifier that stays the same under a second signature; and the cases of
section 12, each with its valid control. The types of section 5 need vectors in
Swarma Envelope once registered there.

## Open questions

- **The co-author's agreement** to the thirteen decisions, written here
  optimistically, and the owners' acceptance of each point that the section
  "What is decided and what is proposed" lists as the draft's.
- **The conflicts X1 to X15** of the section "Reconciliation", which the
  owners decide; above all X3, the anchor of the owner's devices, and X10,
  the registration of the body kinds in Swarma Envelope or a new version name.
- **An unknown action class (decision 2).** Reading (a), written in O2.3: the
  class requires L2, and below L2 it is refused. Reading (b): the executor
  refuses it, or admits it at L2 only where its policy says so. Under either
  reading a class without executor code has no gate that can run O1.4, so an
  L2 command for it still refuses at step 13; whether "unknown" means unknown
  to the registry or only to the policy is open.
- **The registry and LIP-0013.** Decision 2 names LIP-0006 and LIP-0008. The
  four actions of LIP-0013 section 2.2, which the instruction kind carries,
  are not named. Reading (a): they belong to the registry through the trust
  contract profile. Reading (b): they need a section in LIP-0006 or LIP-0008
  first.
- **"Seal spends stay BIP-340" (decision 9).** A seal spend is a secp256k1
  ECDSA signature under the chain's transaction rules (LIP-0004 section 5;
  key map, K5; Link book §4.9.8), and no seal profile uses BIP-340. Reading
  (a), written in O4.6: seal spends stay as they are, on secp256k1 and not on
  P-256. Reading (b): a literal BIP-340, which no Namecoin seal of this
  specification can meet.
- **P-256 "for envelopes only" and statements signed by L2 devices
  (decisions 7, 8 and 9).** Reading (a), proposed in section 7: a policy
  section, and any other statement of an L2 device, travels as an L2 owner
  command, so a P-256 key signs envelopes only. Reading (b): an L2 device
  signs a LIP-0015 statement directly under its domain, and decision 9 admits
  P-256 there too.
- **The device-list pin in an instruction and a wallet request (decision
  10).** They are signed by a grantee key. Reading (a), proposed in section
  5.3: the pin of the owner whose name the agent's landlord pointer names.
  Reading (b): only an envelope signed by a device carries the member, against
  "every envelope".
- **The anti-replay number.** Reading (a), written: the random `nonce` of
  `swarm-envelope/2`, and a journal by identifier for the lifetime of section
  5.1. Reading (b): a number that grows for each device, which needs no
  journal of identifiers and fails when a device's counter is lost.
- **The key of a grant to the owner at a foreign executor (decisions 8, 9
  and 12).** The owner remains a grantee there, and K6 leaves the key map.
  Reading (a): a BIP-340 device key of the list is the v3 `grantee_key`, and
  any device key is the request key of a v4 recipient by key; a P-256 key
  cannot be a v3 grantee. Reading (b): the owner has no personal grantee key,
  and the grantee across owners is the owner's agent (LIP-0013 section 3.7).
- **How far the grant key withdraws (decisions 8 and 12 against the brief's
  "device parts").** Reading (a): every statement of LIP-0015 section 2 leaves
  the grant key: configuration, root rotation, certificates and the heads of
  LIP-0016, and with them the member `pinned_grant_key` of the trust-root pin
  loses its use for statements. Reading (b): only the owner's devices and the
  policy section leave it, as the brief's reconcile list says ("LIP-0015 and
  LIP-0016 in their device parts"), and the other domains stay.
- **The separated human console (decision 11).** Reading (a): input at that
  console is a local act of the executor and carries no signature, an
  exception to decision 1. Reading (b): the console holds a device key of the
  list under the person's account and signs owner commands like any device.
- **The level of a stop and of resumption** (X13).
- **The levels and A0 to A3.** No mapping is decided (X11).
- **Presence for each L2 effect of a run (decision 11).** Reading (a),
  written in O6.7: a run started at L2 signs L2 classes within the L2 limits
  on the presence of its launch. Reading (b): an L2 class is signed only in
  an owner command, so a run started at L2 signs at most what L1 admits.
- **A level in the v4 invocation.** Whether the invocation should carry the
  run's level, so that an own executor checks it as well as the key holder;
  LIP-0008 has no member for it.
- **Two counters for one limit.** A total of the policy is counted by the
  executor for owner commands (section 11, step 12) and by the key holder for
  runs (O6.11). Whether one total covers both, and how the two counts meet,
  is open.
- **A level across an instruction.** An L0 run can send an `instruct`
  envelope to another agent, whose run then has the origin of that grant and
  that origin's row (Honest limits). Whether the level travels with the
  instruction is not decided.
- **The device seal.** Its script, its amount, the key that controls it and
  who holds that key once the prepared spend exists; and the fee of a prepared
  spend, fixed when it is signed, at a later fee level.
- **Accepting a new list.** The confirmation depth at which an executor takes
  a new list (O9.2), and whether a pending update of `swarma-devices` alone
  suspends v4 admission (LIP-0008 sections 3 and 5.2).
- **The size of the name value.** A landlord value with a NIP-05 object, one
  relay and the member leaves 123 bytes, less than the 150 that LIP-0010
  section 8 keeps for the service declaration of LIP-0007.
- **The policy section.** The members that state classes, levels and limits,
  the `subject` of LIP-0015 that names an executor's policy, and its largest
  size within the 8192 bytes of an operator envelope.
- **Existing bytes.** The kind-8185 envelope of LIP-0013, its vectors and
  `tools/trustcheck`, and the request bytes of the wallet service v1 stay as
  they are; how their successors in `instruction/1` and `wallet-request/1` are
  introduced, and when the old forms stop being admitted, is open. The `land`
  instruction of LIP-0013 names a repository and no ref or revision.
- **Own and foreign.** This draft reads "own" as named by the trust-root pin
  of LIP-0015 section 1. An executor that serves several owners is not
  treated.
- **The question texts.** R4 and R5 are named as the brief and the reviewer's
  answer name them. The text of the question that went to the reviewer was
  not available to this draft.
