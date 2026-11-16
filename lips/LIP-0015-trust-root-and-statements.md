# LIP-0015: Trust-root pin and typed statements

- **Status:** Draft. Ivan Oparin accepted its direction as a whole on
  2026-11-14; the co-author's agreement is pending, and no rule of it is
  adopted.
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
format, and nothing is implemented. The pin and the configuration
statements have a first use that needs nothing else of this LIP: signing
the profiles and manifests of Curator.

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

Every statement the grant key signs under BIP-340 is hashed with its own
ASCII prefix before the SHA-256 of its canonical bytes, in the fixed-prefix
style of LIP-0004. Transaction signatures are outside this section: the
grant key's ECDSA spend of a v3 seal follows the chain's transaction rules,
and this LIP changes nothing in it.

| Domain | Object | State |
| --- | --- | --- |
| `swarma-grant-v3` | v3 grant | Existing |
| none, the raw contract hash | `landlord_sig` of the v3 consent | Existing and untyped |
| `swarma-config-v1` | configuration statement (section 3) | Proposed |
| `swarma-root-rotate-v1` | root rotation statement (section 5) | Proposed |
| `swarma-cert-v1` | certificate statement (section 6) | Proposed |
| `swarma-certset-v1` | certificate set head (LIP-0016) | Proposed; not used once the head lives in the name (LIP-0016 section 3.1, Draft of 2026-11-16) |
| `swarma-root-cancel-v1` | cancellation of a pending pin (section 5.1) | Proposed, Draft of 2026-11-16 |
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

A configuration statement is authentic when its six members are in canonical
bytes and this signature verifies under the grant key that `root_name`
yields. Being authentic does not make it accepted: a loader accepts it only
through the steps of section 4. It has no `issuer_key`, no subject kind and
no opening time; the certificate rules of section 6 do not apply to it.

The first use that Ivan Oparin named with his acceptance of 2026-11-14 is
the signing of Curator profiles and manifests. Each profile and each
manifest is one section with a `subject` of its own, and a loader accepts
it only through the steps of section 4.

[LIP-0029](LIP-0029-owner-control.md) holds Draft text, written
optimistically under a decision of 2026-11-15 that awaits the co-author's
agreement, under which an executor's policy is such a section, with an
increasing `seq` that the executor journals, signed by an L2 device of the
owner's device list and not by the grant key (O7.2). The grant key then
grants to others only (O10.2). Until the co-author agrees this section stands
as written.

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

A rotation statement is authenticated against the key it replaces and never
against the name's current key. The first one verifies under the pinned
grant key, and each later one under the `new_grant_key` of the statement
before it, in `seq` order. A statement that does not continue this chain
from the pin is ignored, and step 3 then fails as `ROOT_KEY_CHANGED`.

### 5.1. Overwrite by the administrator after a delay (Draft, 2026-11-16)

Ivan Oparin decided, as recorded by the lead on 2026-11-16, that the
administrator may overwrite the pin after a stated delay, with notification,
and that the old key can cancel the overwrite within that delay. The text is
written optimistically: the co-author's agreement is pending, and until it is
given sections 1 and 5 stand. The Link book, §3.10 «Якорь доверия и
подписанная конфигурация», states the rule in force: the pin changes only by
both acts together. This section adds a path for the administrator alone,
with a delay.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| AO1 | An overwrite of the pin that no rotation statement of section 5 carries is pending first. The administrator writes it, with that account's authentication, as a pending pin: the seven members of section 1 followed by `effective_height`, the height of the root's chain from which it takes effect. Until the active chain of the loader's own node reaches `effective_height`, the loader keeps the current pin. | |
| AO2 | `effective_height` is at least `pinned_at_height` of the pending pin plus the delay `D`. The draft proposes `D` = 1008 blocks, about seven days. A pending pin with a shorter delay is not accepted. The administrator writes `pinned_at_height`, so this rule alone does not bound the window; AO3 does. | `PIN_PENDING_INVALID` |
| AO3 | The loader MUST notify the owner when it finds a pending pin, and again at every load while the pin is pending. The notice names the current and the pending `root_name` and `pinned_grant_key`, the SHA-256 of the pending pin and `effective_height`. It goes over a channel that the deployment names and that the agent's OS user can neither write nor suppress, and the loader records each notice outside the agents' write authority. The loader records the anchor `h_first` at the first load at which it finds the pending pin while its own node is caught up: the node is not in initial block download and knows no header more than `LAG` blocks above its tip (LIP-0022 B2.3, `LAG` = 1 block as proposed there). `h_first` is the greater of the height of that node's tip and the height of the best header it knows. The loader then records the effect height `E` = max(`effective_height`, `h_first` + `D`), and every later notice names `E`. While the node is not caught up, the loader keeps the current pin, sends the notice without `E`, and records no `h_first`; a stale tip is never the anchor. A pending pin takes effect only when the active chain of that node reaches `E`; without a notice, or without a recorded `h_first`, it never takes effect. A backdated `pinned_at_height`, a loader that finds the pin late, or a node that comes back behind the chain therefore shortens nothing: the owner has at least `D` blocks after the first notice that names `E`. | |
| AO4 | Until the pending pin takes effect under AO3, the currently pinned grant key can cancel. That is the key that the loader currently accepts for the root: the pinned key, or the `new_grant_key` of the last rotation statement that continues the chain from the pin (section 5). A cancellation is a statement `swarma-root-cancel/1` with the members `schema`, `root_name` and `pending_sha256`, in this order, signed over `SHA-256("swarma-root-cancel-v1" \|\| statement bytes)`. The loader accepts it from any channel, because its signature authenticates it. It then discards the pending pin and records the cancellation. A cancellation that arrives when the active chain has reached `E` changes nothing, because the pin has taken effect. | |
| AO5 | An overwrite that a rotation statement of section 5, signed by the pinned key, carries takes effect at once, as today. The old key has agreed, and nothing remains to cancel. | |
| AO6 | The pending pin and the record of notices, of `h_first` and `E` and of cancellations live where the agent's OS user cannot write, like the pin itself (section 1). A process of that user can write none of them, nor shorten the delay. The administrator account can still write them (see the limits below). | |

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S51-1 | On Alisa's host the administrator writes a pending pin with a delay of 1008 blocks; the loader finds it at once and sends the notice; nobody cancels: the pin takes effect at `E`, which here equals `effective_height` | The same pin with a delay of 144 blocks: `PIN_PENDING_INVALID`. A pin of which no notice was sent: it never takes effect. Until `E` the loader keeps the current pin. A backdated pin, with `pinned_at_height` at the tip minus 1008 and `effective_height` at the tip, found at the tip: `E` is the tip plus 1008, and the loader keeps the current pin until then. |
| S51-2 | Alisa's pinned grant key signs `swarma-root-cancel/1` for the pending pin one block before `E`: the pin is discarded and the cancellation recorded. For the backdated pin of S51-1, a cancellation one block after the first notice: discarded. For an honest pin that the loader first finds 900 blocks after `pinned_at_height`, on a node that is caught up (the host was off and the node has since left initial block download and synced its headers), a cancellation at `effective_height` plus 2: discarded, because `h_first` is the caught-up tip and `E` is `h_first` plus 1008 | The same cancellation at `E`: nothing changes. A cancellation signed by Karl's key: ignored. An overwrite that a rotation statement of the pinned key carries: in effect at once, with no delay (AO5). |
| S51-3 | Alisa's host was off for 900 blocks. At the first load after it comes back, the node is in initial block download at a tip 900 blocks behind, and the loader finds the pending pin: it keeps the current pin, sends a notice without `E` and records no `h_first`. Two loads later the node has left initial block download and its best header is at most one block above its tip, at height `T`: `h_first` = `T`, `E` = max(`effective_height`, `T` + 1008), and the owner has 1008 blocks from there | A loader that took `h_first` from the stale tip at the first load would give `E` = `effective_height` and a window of 108 blocks; AO3 refuses that anchor. A node that has left initial block download but still knows a header 500 blocks above its tip: not caught up, no `h_first`. A pending pin on a host whose node never catches up: it never takes effect, and the current pin stays. |

What the rules give and what they leave:

- **An overwrite through the loader is seen before it counts.** A pending
  pin cannot be hidden from the loader or take effect early: the owner is
  told for at least `D` blocks after the first notice that names `E`, about
  seven days, and the old key can cancel until the pin takes effect.
- **The administrator account itself is outside this section.** Section 1
  makes that account the owner of the pin, and AO6 puts the records beyond
  the agent's OS user only. An administrator account that rewrites the pin
  directly writes a current pin with no pending state, no notice and no
  delay, and the loader cannot tell it from the installed pin. The same
  account can rewrite `h_first` or the record of notices. Like a replaced
  loader program (Security consequences), this is outside this proposal.
  Section 5.1 gives an honest administrator a path that the owner sees, and
  it bounds a process of the agent's OS user; it does not bound whoever takes
  the administrator account. Where the pin and the records could live beyond
  that account is open.
- **A lost grant key no longer locks a host.** Without the key no rotation
  statement can be signed. The administrator writes a pending pin, and after
  the delay it takes effect, because nobody cancels.
- **A thief of the pinned grant key can cancel every overwrite.** When the
  key is stolen and not lost, the rules give the thief a veto on recovery by
  overwrite. The draft proposes that a cancellation does not count once the
  root name's confirmed value no longer carries the cancelling key after a
  change that the name owner signed (LIP-0008 section 5.2). The cold
  name-owner key then outranks the grant key. Neither owner has decided
  this (open questions).
- **The notice is only as good as its channel.** A deployment whose notice
  channel the attacker controls has no notice. AO3 then still holds the pin
  for the delay, and nothing tells the owner.
- **The anchor is only as good as the node's view of the chain.** AO3 takes
  `h_first` from a node that is caught up by its own account: out of initial
  block download, with no header far above its tip. A node that has no peers
  reports a stale tip and no header above it, and meets that test while it
  is behind. A node whose host was off for less than the tip age at which
  Namecoin Core enters initial block download is in the same position until
  it has synced its headers. The loader cannot tell either case from the node
  alone. A deployment that gives the loader the comparison nodes of LIP-0022
  B2.1 and records `h_first` only in a healthy observation (B2.5) closes
  this; whether the loader requires them is open.

Under Draft [LIP-0029](LIP-0029-owner-control.md), configuration moves to
the owner's L2 devices. Whether an L2 device of the old pin's owner may
cancel, beside or in place of the pinned grant key, is open.

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

A verifier judges a statement in two separate steps.

**Authentic.** The bytes are canonical, `issuer_name` resolves on the
verifier's own node, the name's current grant key equals `issuer_key`, and
the signature verifies. The window is no part of this step: a statement
whose window has ended, or has not begun, is still authentic.

**Current binding.** Statements have the same subject when `issuer_name`,
`subject_kind` and the bytes of `subject` are equal. For one subject the
verifier first takes the authentic statement with the highest `seq` it has
seen, and only then reads that statement's window. The subject is bound
exactly when the window contains the verifier's clock. A statement with a
lower `seq` never binds, even when its own window is still open.

A statement is revoked by a later one for the same subject whose `not_after`
is the time of revocation. The revocation has the highest `seq`, so the
subject is unbound from then on, and the earlier certificate cannot bind
again. A revocation is an authentic statement like any other and concerns
its own subject only. A change of the grant key ends every statement the old
key signed.

A certificate is a binding and not authority. It tells a transport that a
device belongs to the operator of a name. It replaces no grant, and a
message from a certified device stays data until a grant check admits it
(LIP-0013 section 3.4). Statements are published in the store of LIP-0016
and never in a name value.

The three paragraphs that follow record Ivan Oparin's direction of
2026-11-14; the co-author's agreement is pending.

**Which Matrix kind.** Of the two Matrix kinds, `matrix-cross-signing` is
preferred. One statement then binds the cross-signing master key of an
account to the name. It covers a device of that account only when the
device's chain of signatures verifies: the master key signed the account's
self-signing key, and that key signed the device. A receiver verifies the
chain itself. A device that is merely logged in to the account, or that
carries only its own signature, is not covered, whatever the server says
of it. A new device therefore needs no new statement once it is
cross-signed, and no statement makes up for a missing signature. A
`matrix-device` statement binds one device: every new device needs another
statement, and every lost device a revocation.

**Other transports.** A key of another transport gets a kind of its own:
the OMEMO identity keys of an XMPP account, a key that signs email, the
keys of other messengers. Such a kind is proposed in a LIP that states the
items of [LIP-0018](LIP-0018-extension-guide.md) section 4. This LIP
defines none of them.

**What a binding gives.** Without one, a receiver knows the sender of a
transport message only from the transport's server. With one, it verifies
the sending device's chain of signatures up to a key that the operator of
a name certified, and it no longer relies on the server for that. A device
whose chain does not verify stays where it was. The platform book calls
the first level of assurance A0 and the second A1. The binding goes no
further: it gives no authority, and a typed action still needs a grant.

Under Draft [LIP-0029](LIP-0029-owner-control.md), written optimistically
under a decision of 2026-11-15 that awaits the co-author's agreement, an
owner's own devices need no certificate statement: the device list that the
owner's name pins lists their keys (section 3 there). The kinds of this
section stay for the keys of other systems.

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
  control for binaries. An administrator account that rewrites the pin or
  the loader's records directly is outside it too (section 5.1).
- A node that lies to the loader defeats step 2. The node's RPC credentials
  must be unreadable by the agent's OS user.
- A stolen grant key signs policy. A short `not_after` and presence per
  signature bound the damage (key map, requirements on a key service).
- One key now signs several kinds of object. The domains of section 2 keep a
  signature for one kind from verifying as another.

## Conformance impact

None. A future vector set pairs each failure of section 4 with a valid
neighbour, and checks that a signature under one domain of section 2 fails
under every other. For section 6 it pairs a bound subject with the same
subject after its revocation, and checks that the earlier certificate with
an open window does not bind once a higher `seq` exists.

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
- The subject members of each certificate kind beyond `matrix-device`, and
  the kinds for other transports, which arrive under LIP-0018 section 4.
- Whether presence is required for a certificate statement or only for a
  configuration statement and a rotation.
- Adoption, vectors, and the relation of these fixed prefixes to the tagged
  hashes that LIP-0008 section 8 plans for v4.
- **The overwrite of section 5.1.** The delay `D`, proposed as 1008 blocks;
  the channel of the notice; whether a cancellation by a grant key that the
  name owner has since replaced counts (the decision says the old key can
  cancel, and the draft proposes an exception); whether an L2 device of
  LIP-0029 can cancel; the code `PIN_PENDING_INVALID`; where the pin, the
  pending pin and the records of AO6 could live beyond the administrator
  account; whether the loader requires the comparison nodes of LIP-0022 for
  `h_first`, against a node without peers that reports a stale tip; and the
  co-author's agreement.
