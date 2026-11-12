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
signed statement that verifies against its issuer's grant key on chain. The
issuer signs a head over the complete set, and anchors each head in a
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

A record is a signed statement of LIP-0015: a certificate statement, a
configuration statement or a root rotation statement. Each verifies by
itself against the grant key that its issuer's name yields on the reader's
node. The store adds nothing to a record and cannot make an invalid one
valid.

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
revocations included: a statement is revoked by a later statement (LIP-0015
section 6), and both stay in the set.

## 3. The anchor

The issuer anchors each head in one zero-value `OP_RETURN` output, in a
LIP-0005 frame with a new action:

| Action | Name | Payload |
| --- | --- | --- |
| `0x06` | certificate set head | `version(1) || head_commitment(32) || locator` |

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
| 6 | Each statement verifies under LIP-0015 | the code of LIP-0015 |

A missing record never reads as "no certificate". It fails step 3. A host
that serves an older complete set fails step 5, also for a reader that has
never seen this issuer before. A reader that cannot complete the steps has
no verified set and treats the keys it wanted to look up as unbound.

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
  head and statement the old key signed; the issuer publishes a new set
  under the new key, starting again at `seq` 1.
- The set of an issuer is public, and with it the list of devices and keys
  the issuer binds. A statement holds nothing private.
- Each head costs one transaction with one input and the anchor output. No
  size or fee has been measured.

## Conformance impact

None. A future vector set pairs a complete set with one dropped record, one
altered record, a head with a spent output, and a head signed by a key that
is no longer the name's grant key.

## Open questions

- The exact file layout of the Git provider and the bytes of its list.
- Whether a head may cover several issuers, for an organization.
- A batch of heads in one anchor transaction.
- What a reader does between a change of the issuer's grant key and the
  first head under the new key.
- Adoption and vectors.
