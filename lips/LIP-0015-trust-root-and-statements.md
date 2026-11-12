# LIP-0015: Trust-root pin and typed statements

- **Status:** Draft. A proposal; nothing in it is decided.
- **Created:** 2026-11-12
- **Affects:** verification of an agent host's configuration, the signing
  domains of the grant key, bindings of other keys to a name
- **Builds on:** LIP-0004, LIP-0008 section 3 and LIP-0013 section 2.1;
  relates to LIP-0016
- **Deciders:** both owners

## Summary

A configuration section that is signed by a key named in the same file
proves nothing: a process that can rewrite the section can rewrite the key
and sign again. A key compiled into the program is the same for every
installation and names no owner. The owners therefore decided on 2026-11-12
to sign no configuration sections until a trust anchor exists (key map, K4).

This LIP proposes that anchor and what is signed under it:

1. a **trust-root pin** that a person writes once, at installation, in a
   place the agent's OS user cannot write. It names the root `id/` name with
   its registration, its owner script and its grant key;
2. resolution of that name on the verifier's **own node** at every load, so a
   moved or re-registered name refuses;
3. **typed statements** signed by the root's grant key, each kind under its
   own signing domain, so that a statement can never be read as a grant;
4. a **rotation statement** by which the pinned key hands over to a new root;
5. **certificate statements** that bind other keys, such as a messaging
   device key or a commit-signing key, to the name.

A statement binds; it gives no authority. Nothing here changes a grant
format, and nothing is implemented.

## Motivation

An agent host loads policy from a configuration file: which peers it
accepts, which level of checks it runs. An agent that runs as the same OS
user as the loader can edit that file. Signing the file helps only if the
verifying key comes from somewhere that agent cannot reach, and if an old,
weaker file cannot be put back.

The grant key is the natural signer: the owners gave a principal three keys
and no administrative key (key map, K1), and the grant key is the one whose
public half every verifier already resolves on chain. Using one key for
grants, policy, key bindings and later releases is safe only when each kind
of object has its own domain and the key service shows what it signs.

## Current state

- Grants and their contract are the only objects the grant key signs. The v3
  grant uses the fixed prefix `swarma-grant-v3`; `landlord_sig` signs the raw
  contract hash without a prefix (LIP-0004 sections 2 and 3).
- LIP-0008 section 8 plans a distinct tagged hash per object type for v4 and
  requires that a signer validates and hashes the object itself. No tag is
  assigned.
- No configuration statement, key binding or root pin exists in this
  specification. The key service requirements of the key map are open work.

## 1. The trust-root pin

The pin answers the question "who is root" outside the agent's reach. It is
one JSON object under the encoding rules of LIP-0013 section 2.1:

| # | Member | Meaning |
| --- | --- | --- |
| 1 | `schema` | `swarma-trust-root/1` |
| 2 | `network` | `main` or `regtest` |
| 3 | `root_name` | the `id/` name of the root principal |
| 4 | `registration` | `{"txid":…,"vout":…}`, the output that first registered the name |
| 5 | `owner_script_sha256` | SHA-256 of the script that controls the name's output, 64 lowercase hex |
| 6 | `pinned_grant_key` | the root's grant key, 64 lowercase hex |
| 7 | `pinned_at_height` | the height of the tip when the pin was written |

The installer fills the pin from the installing person's own node and shows
the key. The person compares it with a copy received on another channel
before confirming. The file is owned by the administrator account, in a
directory the agent's OS user cannot write; writing or replacing it takes
that account's authentication. The pin is not secret.

## 2. Signing domains of the grant key

Every object the grant key signs is hashed with its own ASCII prefix before
the SHA-256 of its canonical bytes, in the fixed-prefix style of LIP-0004:

| Domain | Object | State |
| --- | --- | --- |
| `swarma-grant-v3` | v3 grant | Existing |
| none, the raw contract hash | `landlord_sig` of the v3 consent | Existing and untyped |
| `swarma-config-v1` | configuration statement (section 3) | Proposed |
| `swarma-root-rotate-v1` | root rotation statement (section 5) | Proposed |
| `swarma-cert-v1` | certificate statement (section 6) | Proposed |
| `swarma-certset-v1` | certificate set head (LIP-0016) | Proposed |
| `swarma-release-v1` | release statement | Reserved for a later proposal |

A key service that holds the grant key signs none of these from a digest
that a caller supplies. It parses the typed object, shows it, and hashes it
itself (key map, requirements on a key service). The one untyped signature,
`landlord_sig`, is produced only from a contract that the service parsed and
showed.

The notary attestation of LIP-0014 is signed by a different key, under
`swarma-notary-v1`, and is not in this table.

## 3. The configuration statement

A signed section is a statement about the hash of that section. It is one
JSON object under the encoding rules of LIP-0013 section 2.1, with exactly
these members in this order:

| # | Member | Meaning |
| --- | --- | --- |
| 1 | `schema` | `swarma-config-statement/1` |
| 2 | `root_name` | equals the pin's `root_name` |
| 3 | `subject` | which section this is, for example `curator.policy` |
| 4 | `seq` | a positive integer that grows with every statement for this subject |
| 5 | `not_after` | Unix seconds after which the statement is not accepted |
| 6 | `body_sha256` | SHA-256 of the exact octets of the section |

The signature is BIP-340 by the root's grant key over
`SHA-256("swarma-config-v1" || statement bytes)`. The 16-byte prefix has no
terminator or length.

## 4. Verification at load

The loader runs these steps each time it loads a signed section and stops at
the first failure:

| # | Step | Failure |
| --- | --- | --- |
| 1 | Read the pin | `PIN_UNREADABLE` |
| 2 | Resolve `root_name` on the loader's own node. The name's history reaches the pinned registration, as in the walk of LIP-0008 section 3, and its current output is controlled by the pinned owner script | `ROOT_MOVED` |
| 3 | The name's current grant key equals `pinned_grant_key`, or is reached from it through rotation statements (section 5) | `ROOT_KEY_CHANGED` |
| 4 | `root_name` and `subject` match; the signature verifies under that key | `STATEMENT_SIGNATURE` |
| 5 | The loader's clock is at most `not_after` | `STATEMENT_EXPIRED` |
| 6 | `seq` is at least the highest value this loader accepted for the subject. The high-water mark is kept where the agent's OS user cannot write | `CONFIG_ROLLBACK` |
| 7 | SHA-256 of the section equals `body_sha256` | `BODY_MISMATCH` |

Step 2 applies the owner-key binding of the v4 draft locally. It works for a
name used by v3 grants, because it reads only the name's history and current
output and no grant.

**Fail closed.** On any failure, and when the node is unreachable or the name
is missing or expired, the loader runs at its most restrictive level. It
never falls back to running without checks.

## 5. Changing the root

The pin changes only with both of these: a statement `swarma-root-rotate/1`
signed by the currently pinned grant key, and the administrator account's
authentication to rewrite the pin. The statement has the members `schema`,
`old_root`, `new_root`, `new_registration`, `new_owner_script_sha256`,
`new_grant_key` and `seq`, in this order, and is signed over
`SHA-256("swarma-root-rotate-v1" || statement bytes)`.

A change of the grant key on chain is accepted by step 3 only together with
such a statement signed by the old key, or after a person writes a new pin.
A process of the agent's OS user can do neither.

## 6. Certificate statements

A certificate statement says that a key of another system belongs to the
operator of a name. It is one JSON object under the encoding rules of
LIP-0013 section 2.1, with exactly these members in this order:

| # | Member | Meaning |
| --- | --- | --- |
| 1 | `profile` | `swarma-cert-statement/1` |
| 2 | `network` | `main` or `regtest` |
| 3 | `issuer_name` | the `id/` name whose grant key signs |
| 4 | `issuer_key` | that name's current grant key |
| 5 | `subject_kind` | `matrix-device`, `matrix-cross-signing`, `git-signing-ssh` or `release-key` |
| 6 | `subject` | an object whose members depend on the kind; for `matrix-device`: `{"mxid":…,"device_id":…,"ed25519":…}` |
| 7 | `purpose` | what the key is used for, for example `a2a-transport` |
| 8 | `seq` | a positive integer that grows with every statement for this subject |
| 9 | `not_before` | Unix seconds |
| 10 | `not_after` | Unix seconds, at most one year after `not_before` |
| 11 | `note` | at most 280 bytes; carries no authority |

The signature is BIP-340 by `issuer_key` over
`SHA-256("swarma-cert-v1" || statement bytes)`. `statement_id` is the SHA-256
of the compact object `{"statement":…,"signature":…}`.

A verifier resolves `issuer_name` on its own node, requires the name's
current grant key to equal `issuer_key`, checks the window, and for one
subject takes the statement with the highest `seq` it has seen. A statement
is revoked by a later one for the same subject whose `not_after` is the
time of revocation, or by a change of the grant key, which ends every
statement the old key signed.

A certificate is a binding and not authority. It tells a transport that a
device belongs to the operator of a name. It replaces no grant, and a
message from a certified device stays data until a grant check admits it
(LIP-0013 section 3.4). Statements are published in the store of LIP-0016
and never in a name value.

## Alternatives

- **A key compiled into the program:** the same for every installation, and
  it names no owner.
- **A platform key of the installing person,** outside the chain: works on
  one platform and cannot be resolved by another verifier.
- **A key named in the configuration file:** rejected by the owners'
  decision K4.
- **An organization as root** (see the sketches below): possible later, once
  an organization identity exists.

## Security consequences

- A rewritten section fails step 4 or step 7. A section signed by a new key
  that the same file names fails step 3, because the key comes from the pin
  and the chain.
- An old section with a valid signature fails step 6. This needs the
  high-water mark to be out of the agent's reach, like the pin.
- A replaced loader program is outside this proposal. Signing configuration
  does not protect the program that checks it; that needs programs the
  agent's OS user cannot replace, and platform notarization stays the
  control for binaries.
- A node that lies to the loader defeats step 2. The node's RPC credentials
  must be unreadable by the agent's OS user.
- A stolen grant key signs policy. A short `not_after` and presence per
  signature bound the damage (key map, requirements on a key service).
- One key now signs several kinds of object. The domains of section 2 keep a
  signature for one kind from verifying as another.

## Conformance impact

None. A future vector set pairs each failure of section 4 with a valid
neighbour, and checks that a signature under one domain of section 2 fails
under every other.

## Related sketches, not proposed here

**Organization identity.** An organization could be a principal like any
other: an `id/` name whose owner script needs the name-owner keys of its
founders together, and whose grant key certifies the founders' grant keys
through certificate statements of a further kind. A name output with a
multi-key script has not been verified on regtest. This follows Goal 1 and
the first v4 work; it is not needed for the migration to trust grants.
Deciders: both owners.

**Release statements.** A release of a program could be a statement
`swarma-release-v1` over a name, a version, the hash of the artifact and the
platform, signed by the grant key or by a certified release key and
published through the store of LIP-0016. Verification before launch,
revocation and the comparison with existing transparency systems belong to a
separate paper. Platform notarization stays in force meanwhile. Decider:
Ivan Oparin, as the author of that paper.

## Open questions

- Where the high-water mark of step 6 is kept on each platform.
- The subject members of each certificate kind beyond `matrix-device`.
- Whether presence is required for a certificate statement or only for a
  configuration statement and a rotation.
- Adoption, vectors, and the relation of these fixed prefixes to the tagged
  hashes that LIP-0008 section 8 plans for v4.
