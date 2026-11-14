# LIP-0016: Certificate store

- **Status:** Draft. A proposal; nothing in it is decided.
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

## 4. Providers

A provider gives a reader two operations: list the head and the statement
ids of an issuer, and get one statement by its id. It is addressed by
configuration. The first provider is a Git hosting repository with one file
per statement and one file for the current head. The location types of
LIP-0005, a content-addressed blob store and BitTorrent, are later
providers. A provider is not trusted for anything but availability.

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

Commit-signing keys are records too: a `git-signing-ssh` statement binds a
commit-signing key to the name. The signatures on a provider repository's
commits then lead back to the grant key, though a reader does not need them.

## Alternatives

- **The head in the issuer's name value,** as an owner member outside
  `swarma`. The name then always shows the current head without a chain of
  spends. It is possible only after LIP-0010 readers are deployed on every
  verifier, and it costs value bytes on every change.
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

## Open questions

- The exact file layout of the Git provider and the bytes of its list.
- Whether a head may cover several issuers, for an organization.
- A batch of heads in one anchor transaction.
- What a reader does between a change of the issuer's grant key and the
  first head under the new key.
- Adoption and vectors.
