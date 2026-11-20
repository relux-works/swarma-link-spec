# LIP-0016: Certificate store

- **Status:** Draft. Ivan Oparin accepted its direction as a whole on
  2026-11-14; the co-author's agreement is pending, and no rule of it is
  adopted. The answers that this revision gives to the open questions of
  the first draft are the draft's proposals.
- **Created:** 2026-11-12
- **Affects:** publication of the statements of LIP-0015, the action table
  of LIP-0005
- **Builds on:** LIP-0005 and LIP-0015
- **Deciders:** both owners

## Summary

A host that stores signed statements can drop one, or serve last month's
set, and a reader who trusts the host does not notice. This LIP proposes a
store in which the host provides availability only. Every record is a
signed statement, and each type of record is checked under its own rules.
The issuer signs a head over the complete set, and anchors each head in a
transaction that spends an output of the previous head's transaction. A
reader recomputes the head, checks its anchor on its own node, and checks
that the head's output is unspent. A dropped record changes the head, and an
old head has a spent output.

The first provider is a Git hosting repository with one file per statement.
Nothing is implemented.

Under Draft [LIP-0029](LIP-0029-owner-control.md), written optimistically
under a decision of 2026-11-15 that awaits the co-author's agreement, the
store holds no statement for an owner's own devices: the device list pinned in
the owner's name replaces it for them.

Ivan Oparin decided on 2026-11-20 (source: `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`) that section 3.1 uses the
`swarma-certs` entry of the single manifest pinned by the issuer's name
(LIP-0010 section 11), superseding the separate-head Draft of 2026-11-16.
The co-author's agreement is pending. In this profile the set has no head
anchor or chain of spends, and only the confirmed name pins it. The older
anchor-based profile below remains a separately identified legacy profile,
not a fallback when a manifest or its set is absent.

## Motivation

Key bindings and configuration statements (LIP-0015) do not fit a name
value: it holds 520 bytes, and on Grant v3 any member beyond the exact
LIP-0004 shapes makes every grant under the name refuse (key map). They
need a place outside the chain. Putting them on a hosting service is
convenient and makes that service a party that can hide a revocation. The
store must make omission and rollback visible to a reader who has only its
own node and the fetched files.

## 1. Records

A record is a signed statement of LIP-0015, of one of three types. The
first member of the object names the type, and a reader selects the rules by
it:

| Type | First member | What the store reader checks | Who decides its effect |
| --- | --- | --- | --- |
| Certificate statement | `profile` = `swarma-cert-statement/1` | Authentic under LIP-0015 section 6: the eleven members in canonical bytes, `issuer_name` equal to the head's, `issuer_key` equal to the name's current grant key, the signature under `swarma-cert-v1` | The store reader, in step 7 of section 5 |
| Configuration statement | `schema` = `swarma-config-statement/1` | Authentic under LIP-0015 section 3: the six members in canonical bytes, `root_name` equal to the head's `issuer_name`, the signature by that name's current grant key under `swarma-config-v1` | A loader with a pin, under LIP-0015 section 4 |
| Root rotation statement | `schema` = `swarma-root-rotate/1` | Inclusion only: its id is one the head lists. Its signature is not verified here, because the key it replaces signed it and not the current key | A loader with a pin, along the chain of LIP-0015 section 5 |

The id of a record of any type is the SHA-256 of the compact object
`{"statement":…,"signature":…}`, as LIP-0015 section 6 defines it for a
certificate. An object with any other first member is no record of this
store.

Three facts are kept apart. A record is included when the signed head lists
its id. A certificate or a configuration statement is authentic when it
passes its row above. A subject is currently bound when step 7 says so. The
store adds nothing to a record and cannot make an invalid one valid.

## 2. The head

This section describes the older **signed, anchored-head profile**. The
current Draft manifest profile of section 3.1 replaces its head signature
and anchor chain; its missing bytes never trigger fallback to this profile.

The issuer signs one head per version of its set. The head is one JSON
object under the encoding rules of LIP-0013 section 2.1, with exactly these
members in this order:

| # | Member | Meaning |
| --- | --- | --- |
| 1 | `profile` | `swarma-certset-head/1` |
| 2 | `network` | `main` or `regtest` |
| 3 | `issuer_name` | the `id/` name whose statements the set holds |
| 4 | `issuer_key` | that name's current grant key |
| 5 | `seq` | 1 for the first head, then one higher each time |
| 6 | `count` | the number of statements in the set |
| 7 | `set_sha256` | SHA-256 of the statement ids of the set, each as 32 raw bytes, in ascending order |
| 8 | `prev_head_id` | `""` for `seq` 1; otherwise the `head_id` of the previous head |
| 9 | `head_outpoint` | `{"txid":…,"vout":…}`, the output that the next head's anchor spends |

The signature is BIP-340 by `issuer_key` over
`SHA-256("swarma-certset-v1" || head bytes)`. `head_id` is the SHA-256 of
the compact object `{"head":…,"signature":…}`.

A head covers one issuer. An operator with several issuing names publishes
one head for each. A head over several issuers would need a rule for the
key that signs it, which belongs to the organization identity that LIP-0015
sketches, and it is not proposed.

The set of a head holds every statement the issuer still publishes,
revocations and ended statements included: a statement is revoked by a later
statement (LIP-0015 section 6), and both stay in the set. A set published
after a change of the grant key also holds the root rotation statements that
lead to the new key, so that a loader pinned to an earlier key can follow
them.

## 3. The anchor

The issuer anchors each head in one zero-value `OP_RETURN` output, in a
LIP-0005 frame with a new action:

| Action | Name | Payload |
| --- | --- | --- |
| `0x06` | certificate set head | `version(1)` \|\| `head_commitment(32)` \|\| `locator` |

```text
head_commitment = SHA-256( "swarma-certset-anchor-v1" || head_id )
```

The locator has type `0x01` and its pointer is `head_id`. The script is 72
bytes. Actions `0x04` and `0x05` are proposed by LIP-0014.

The anchor transaction of a head with `seq` above 1 spends the
`head_outpoint` of the previous head. The output named by a head's own
`head_outpoint` exists before the head is signed, as a seal exists before
its grant (LIP-0008 section 9). The heads of one issuer thus form a chain
of spends, and only the newest head has an unspent output.

One anchor transaction anchors one head. A batch of heads in one
transaction would save fees for an operator of many issuers. It needs one
commitment over several heads and one input for each issuer's chain of
spends, and it is left to a later proposal.

### 3.1. The head in the name (Draft, 2026-11-16)

Under the decision of LIP-0010 section 11 the store has one mechanism with
every other statement set: its head is the `swarma-certs` entry in the
issuer's name-pinned `swarma-manifest/1`, and the last confirmed manifest
counts. Ivan Oparin decided on 2026-11-20 (source: `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`) to replace the former direct
name member this way; co-author agreement on this amendment is pending.
The 2026-11-20 direction
supersedes the conflicting older Draft placement now; it does not claim
implementation or adoption. Sections 2, 3 and 5 describe the explicitly
separate legacy anchored-head profile except where CH1–CH4 replace them.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| CH1 | The head document is the head of section 2 with members 1 to 7 only, in that order, and without a signature. `sets.swarma-certs` in the pinned manifest pins its `seq` and the SHA-256 of its exact octets (LIP-0010 SH1–SH5). The name-owner key, which signs the name update, authenticates it. | |
| CH2 | No anchor of section 3 is made, and action `0x06` is not used. | |
| CH3 | In section 5, steps 2, 4 and 5 are replaced by two steps. 2: the confirmed value of `issuer_name` on the reader's own node pins the manifest, which carries `sets.swarma-certs` (LIP-0010 SH1–SH6); the fetched head hashes to its `sha256`, its `seq` equals the pinned `seq`, its `issuer_name` and `network` are the name's and the reader's, and `issuer_key` equals the grant key that the name yields. 4: the head passes LIP-0010 SH5: its `seq` is not lower than the highest that the reader journaled for this issuer, unless a reorganisation removed the name operation that carried that head, and a certificate that the reader journaled as revoked stays revoked. Steps 1, 3, 6 and 7 stay. | 2: `HEAD_PIN`; 4: `HEAD_ROLLBACK` |
| CH4 | A pending name update gives no head. A record that a new head adds or revokes takes effect at that head's confirmation, at every reader alike. | |

The two consequences that change:

- **The gap after a change of the grant key closes.** One name update can
  carry the new grant key and the new head together, so no height exists at
  which the name's grant key and the head disagree. That update changes
  `swarma`, and on v4 it is a break (LIP-0008 section 5.2).
- **A revocation waits for a block.** Under section 5, step 5, a newer head
  in the mempool made the old one fail at once. Under CH4 a revocation by a
  later statement takes effect at the confirmation of the head that lists it.
  A stop that must act from the mempool is a seal spend (LIP-0008 sections
  5.1 to 5.3).

The Link book, §3.12 «Хранилище заявлений», describes the anchor of section
3 and counts a spend in the mempool at step 5 («ни в блоке, ни в мемпуле»),
and says that statements do not go into the name value. The statements still
do not: only the head does. Its §9.2 puts the head of an organization's state
into the organization's name value, and its §9.4 says that after a
reorganisation the state is recomputed and that an urgent revocation goes by
a separate name update or a seal spend. Section 3.1 follows §9.2, and
through LIP-0010 SH5 it follows §9.4: after a reorganisation the last
confirmed head counts again and a revocation that a reader journaled stays.
§3.12 is an update for the book once agreed.

The Draft form decided by Ivan Oparin on 2026-11-20 (source:
`$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`; co-author agreement
pending) now puts the head behind the single manifest, not in a separate
name member. Every changed set still requires a name update
signed by the cold key, with the v3 outage of LIP-0029 O3.10. The one shared
manifest head costs 104 bytes at a one-digit sequence or 119 at the maximum
(LIP-0010 section 8); the certificate entry itself costs no extra name
bytes. Legacy direct-head sizes are not this profile's budget.

## 4. Providers

A provider gives a reader two operations: list the head and the statement
ids of an issuer, and get one statement by its id. It is addressed by
configuration. The first provider is a Git hosting repository with one file
per statement and one file for the current head. The location types of
LIP-0005, a content-addressed blob store and BitTorrent, are later
providers. A provider is not trusted for anything but availability.

### 4.1. The Git provider

The proposal for the first provider adds no format of its own. A file
holds the exact bytes of one object of this LIP:

| Path | Content |
| --- | --- |
| `head.json` | The current head: the compact object `{"head":…,"signature":…}`, with no trailing newline. Its SHA-256 is the `head_id`. |
| `statements/<id>.json` | One record of the set: the compact object `{"statement":…,"signature":…}`, with no trailing newline. `<id>` is the record id in 64 lowercase hex. |

One repository, or one directory of a repository, holds the store of one
issuer. The list of the provider is the set of files under `statements/`.
It has no bytes of its own: the head commits to the set through `count` and
`set_sha256`, so a file that is missing or added fails step 3 of section 5.
A reader computes each id from the bytes of the file and does not trust
the file's name. It takes the files from any commit that it fetched; the
history of the repository, its branches and the signatures on its commits
are no evidence for it.

An issuer may keep earlier heads beside the current one. A reader does not
read them.

## 5. Reading the store

A reader, for one issuer:

| # | Step | Failure |
| --- | --- | --- |
| 1 | Fetch the head and every statement it lists | `STORE_UNAVAILABLE` |
| 2 | The head's signature verifies under the grant key that `issuer_name` yields on the reader's node, and that key equals `issuer_key` | `HEAD_SIGNATURE` |
| 3 | The number of fetched statements equals `count`, and their ids give `set_sha256` | `STORE_INCOMPLETE` |
| 4 | The anchor of section 3 is confirmed in the active chain and commits to this `head_id` | `HEAD_ANCHOR` |
| 5 | `head_outpoint` is unspent, the mempool included | `HEAD_SUPERSEDED` |
| 6 | Each record is checked by its type, under its row of section 1. A certificate statement is authentic under LIP-0015 section 6, and its window is not judged here. A configuration statement is authentic under LIP-0015 section 3, and its expiry is not judged here. A root rotation statement is included and nothing more. A listed object of no known type fails | `STORE_RECORD_INVALID` |
| 7 | Certificates only: for each certificate subject, take the authentic certificate statement with the highest `seq`, and only then read its window. The subject is bound when the window contains the reader's clock | none; an unbound subject is a result and no failure of the set |

Steps 1 to 6 establish that the set is complete, that its certificate and
configuration statements are authentic, and that its rotation statements
are included. They do not establish that a rotation statement is validly
signed. Step 7 reads the current certificate bindings. A retained
revocation, or a certificate whose window has ended, passes step 6 and
leaves its own subject unbound in step 7. Every other subject of the set
keeps its binding. An earlier certificate of a revoked subject does not
bind again, because step 7 never selects a statement below the highest
`seq`.

Step 7 gives a configuration statement no effect. A loader takes an
authentic configuration statement from the set and accepts it only under
LIP-0015 section 4: its pin, the expiry, the rollback mark and the hash of
the section. The same loader evaluates a rotation statement from the set
under LIP-0015 section 5. A valid configuration or rotation statement in a
set therefore never affects whether a certificate subject is bound.

A missing record never reads as "no certificate". It fails step 3. A host
that serves an older complete set fails step 5, also for a reader that has
never seen this issuer before. A host that replaces a record by one with a
forged signature changes that record's id and fails step 3. A reader that
cannot complete steps 1 to 6 has no verified set and treats the keys it
wanted to look up as unbound.

**After a change of the grant key.** Between the name update that changes
an issuer's grant key and the first head under the new key, step 2 fails
for the old head, because its key is no longer the name's grant key. The
reader then has no verified set, and every subject of that issuer is
unbound. It MUST NOT fall back to the old set. The issuer keeps the gap
short: it prepares the complete set under the new key before the update
and anchors its first head as soon as the update is confirmed.

Commit-signing keys are records too: a `git-signing-ssh` statement binds a
commit-signing key to the name. The signatures on a provider repository's
commits then lead back to the grant key, though a reader does not need them.

## Alternatives

- **A separate head in the issuer's name value.** Superseded by the
  single manifest on 2026-11-20. The explicit legacy transition of
  LIP-0010 section 11.2 does not permit mixing this form with the manifest.
- **No anchor, signatures only.** A reader then detects an altered record
  and not a dropped one.
- **An anchor without the chain of spends.** A reader that kept the highest
  `seq` it saw detects a rollback; a first reader does not.

## Security consequences

- A host that drops, adds or alters a record is detected by steps 3 and 6.
  A host that withholds a newer head is detected by step 5.
- A stolen grant key signs a new head. A change of the grant key ends every
  head and every certificate and configuration statement the old key signed.
  The issuer publishes a new set under the new key, starting again at `seq`
  1; it carries the root rotation statement, which the old key signed.
- The set of an issuer is public, and with it the list of devices and keys
  the issuer binds. A statement holds nothing private.
- Each head costs one transaction with one input and the anchor output. No
  size or fee has been measured.

## Conformance impact

None. A future vector set pairs these controls:

| Valid control | Refusal or invariant |
| --- | --- |
| A complete set with certificates of subjects A and B, both bound | The same set with one record dropped fails as `STORE_INCOMPLETE`. |
| The set after A is revoked: A's certificate, A's revocation and B's certificate | The set is still complete and authentic. A is unbound and B stays bound; discarding the set because the revocation's window has ended is wrong. A's earlier certificate, whose own window is still open, does not bind. |
| Every record with its issuer's signature | A record replaced by one with a forged signature fails as `STORE_INCOMPLETE`, because its id changes. A head that lists a certificate whose signature does not verify fails as `STORE_RECORD_INVALID`. |
| A mixed set: a live certificate, a valid unexpired configuration statement and a root rotation statement | The set passes steps 1 to 6 and the certificate's subject is bound. Judging the configuration statement by the certificate members, and discarding the set because it lacks them, is wrong. |
| The same mixed set with each record of its own type | A configuration statement whose signature does not verify under `swarma-config-v1`, one whose `root_name` differs from the head's `issuer_name`, a configuration statement signed under the certificate domain, and a listed object with an unknown first member each fail as `STORE_RECORD_INVALID`. |
| A rotation statement in the set that continues the chain from a loader's pin | A rotation statement with a bad signature leaves the set readable, because the store checks its inclusion only; the loader refuses it under LIP-0015 section 5. Reporting it as verified by the store is wrong. |
| The newest head | A head whose output is spent fails as `HEAD_SUPERSEDED`; a head signed by a key that is no longer the name's grant key fails as `HEAD_SIGNATURE`. |
| A reader after the first head under a new grant key: the subjects of the new set are bound | The same reader between the name update and that head: `HEAD_SIGNATURE` for the old head, and every subject unbound. Reading the old set as still valid is wrong. |
| A Git store whose files hold the exact bytes of the head and of each record | A record file with a trailing newline, and a file whose bytes hash to an id that the set does not hold: `STORE_INCOMPLETE`. A file under a name that its bytes do not hash to is read by its bytes. |

The vector set of this LIP is described here and not built. It holds the
controls of this table as exact bytes: records of the three types, heads
with their signatures and ids, the anchor scripts, and for each refusal the
one change that produces it. The reference checker of LIP-0013 is the place
for it.

## Open questions

- The key that controls the output of a head. This LIP names the output
  and no key for it. Under section 3.1 no such output exists.
- Under section 3.1: whether the head keeps a signature by the grant key
  beside the pin of the name, which the draft drops; and the co-author's
  agreement.
- How a reader learns where the store of an issuer is. Today a provider is
  addressed by configuration.
- A head for several issuers, with the organization identity.
- A batch of heads in one anchor transaction.
- Adoption, and the building of the vector set.
