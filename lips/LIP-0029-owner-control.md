# LIP-0029: Owner control by signed envelopes and a pinned device list

- **Status:** Draft, written optimistically. Ivan Oparin accepted the
  thirteen decisions of this LIP on 2026-11-15, and six more on 2026-11-16,
  and asked that the text be written without waiting for the co-author: where
  the co-author objects, the point is fixed separately. On 2026-11-16 he
  also corrected decision 1, decided the one-host rule and staged the M6
  switch. Those three decisions are in force in this version; the
  co-author's answer to them is folded in later by amendment and gates
  nothing ([Decision 0004](../decisions/0004-reconciliation-closures.md),
  status). For everything else the co-author's agreement is pending, no
  other rule of this LIP is adopted, and until the co-author agrees every
  other text that this LIP revises stands as written. This Draft incorporates
  LIP-0032 to LIP-0037 amendments and the binding decisions individually
  cited there; editorial proposals do not acquire owner-decision status. Agreement on each amendment remains pending;
  the precedence direction is not an implementation or adoption claim.
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
  J7.2) and the device-signed owner command of its section 3.7; the signer
  of the configuration statement
  of LIP-0015 section 3; decision K6 of the key map
- **Deciders:** both owners

## Summary

The chain rules apply inside one host too. The host is one node; a registry
simplification inside a host remains an open question (Ivan Oparin's
decision of 2026-11-16, in force in this version:
[Decision 0004](../decisions/0004-reconciliation-closures.md), one host).

The owner channel carries work under the transition of section 1:
unsigned work is delivered but labelled, and the unsigned message itself
is given no effect. J7.2 gives the owner's work a row at the key holder.
Section 6 adds the level bound to that row and to the objects signed under
the agent's own grants. LIP-0015 still puts statements on the grant key;
section 10 moves the owner's statements to its devices.

This LIP gives the owner a voice that the receivers check:

1. Communication is signed at minimum and encrypted at maximum. During M0,
   unsigned work is delivered but labelled, and the unsigned message
   itself is given no effect. After M6, unsigned input is ignored. Section
   1 defines M0 and M6. Free text directs work; an effect happens only
   through typed fields that the executor's gate compares with the actual
   arguments (section 1).
2. The owner's name value pins a **manifest** outside `swarma`; its
   `swarma-devices` entry pins the device-list hash and sequence. The list
   holds a record for each of
   the owner's devices: its key, the algorithm, a claimed presence flag, a
   level ceiling and a revocation seal (section 3).
3. A device key is BIP-340 or P-256, or an entry of the registry of section
   3.6 (Draft of 2026-11-16). P-256 is admitted because the Secure Enclave
   holds no other curve. The envelope identifier and the replay journal
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
   and a name update, slowly (sections 8 and 9). Figure 1 shows the seal: a
   fresh key, a revocation signed in advance, the key destroyed (section 8.3,
   Draft of 2026-11-16).
8. The grant key grants to others only. The owner's devices
   speak for the owner at its own executors, and there is no statement key
   (section 10). This is where R5 closes.
9. Draft text of 2026-11-16: the sender attaches the list when it changes
   and at first contact with a receiver, otherwise the envelope carries the
   hash and the receiver reads its cache; an unknown hash refuses by name and
   the sender re-sends; the owner's domain and a Nostr replaceable event are
   secondary paths (section 3.5). A Matrix device is an ordinary record at L1
   without presence, and only an end-to-end encrypted event bound to its
   session counts (section 4.1).
10. Draft text of 2026-11-16: an algorithm registry gives every `alg` of a
    device record its key encoding, its signature encoding, its presence
    semantics and its highest level; only the Matrix entry has a verifier in
    M5n. L2 is strengthened: a Secure Enclave key under `biometryCurrentSet`
    without passcode fallback, a fresh authentication for each signature, and
    a signer that shows the fields first (section 3.6).

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
| 1 | Signed at minimum, encrypted at maximum: use native encryption where possible. Transitional (M0): unsigned work is delivered but labelled; effects only on a signature, which section 1 carries for the unsigned message itself. After M6, unsigned input is ignored. Free text directs work only. An effect happens only through typed fields that define it completely: repository, ref and exact revision; payee and amount. The executor's gate recomputes the actual arguments and compares them with the fields before any effect. The owner's client forms the fields and shows them; the executor's model does not. | 1 |
| 2 | The typed action registry is the action profiles of this specification: LIP-0006 and the v4 action profile of LIP-0008. A new action is a LIP section plus executor code. An unknown action class requires L2 or is refused. LIP-0008 section 12.4 stays reserved. | 2 |
| 3 | Ivan Oparin decided on 2026-11-20 (source: `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`) that the name pins one `swarma-manifest` head, outside `swarma`, whose manifest carries device and other set heads plus the service declaration. This supersedes the direct-device-only decision; co-author agreement on the amendment is pending. Changes do not close v4 grants; every verifier needs the compatible reader before production writing. Exact v3 readers still refuse extras. | 3.3, 3.4; LIP-0010 section 11 |
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

**Decisions of 2026-11-16.** Ivan Oparin decided three more points, which
the lead relayed at about 00:40Z. They are written optimistically: the
co-author's agreement is pending.

| # | Decision | Section |
| --- | --- | --- |
| 14 | The device-seal diagram goes into this LIP and the book in the same words: adding a device makes a seal `S_D` on a fresh `k_D`, a pre-signed `tx_revoke_D`, destroys `k_D`, hands the spend to the other devices and puts the list hash in the name by the cold key; each command needs the device signature, the list hash from the name and `gettxout(S_D)` unspent; on loss any device broadcasts `tx_revoke_D`, and a rollback cannot restore `D`. | 8.3, Figure 1 |
| 15 | Ivan Oparin decided on 2026-11-20 (source: `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`) to reach the device pin through the single manifest, superseding direct name placement; co-author agreement is pending. Matching checked bytes from any source count. Inline manifest/list delivery is primary; authenticated-domain HTTPS and Nostr kind 30079 are optional, non-exclusive secondary paths. No domain or Nostr key is required for inline operation. | 3.5; LIP-0033 |
| 16 | A messenger device key (a Matrix device's Ed25519 key, an XMPP OMEMO key) is an ordinary device record with the messenger's algorithm, an L1 ceiling and no presence. An end-to-end encrypted event authenticated by that device's session counts as an L1 command. Forwarded or backup-restored session keys are refused as unauthenticated, and plaintext never counts. | 4.1 |

**Decisions of 2026-11-16, later.** Ivan Oparin decided three more points,
which the lead relayed at about 01:15Z (17 and 18) and, with the keeper, at
about 01:40Z (19). They are written optimistically: the co-author's agreement
is pending. Decision 17 refines decision 15 and stands where the two differ.

| # | Decision | Section |
| --- | --- | --- |
| 17 | The sender attaches the full list on change and on first contact with a peer; otherwise the envelope carries only the list hash. The receiver caches by hash. An unknown hash is refused with a named `LIST_UNKNOWN`, and the sender re-sends; the list is never silently fetched from an untrusted place. A Nostr replaceable event, parameterized, with a `d` tag for the device list and signed by the Nostr key in the name, is a real secondary channel. A storage service by grant comes later. | 3.5 |
| 18 | An algorithm registry for device records. Each entry gives the key encoding, the signature encoding, the presence semantics and the highest level. The entries: Apple Secure Enclave P-256; FIDO2/WebAuthn (ES256 or EdDSA, with the UP and UV flags as signed presence, L2-capable); YubiKey PIV P-256 and P-384; TPM 2.0 P-256; Android Keystore/StrongBox P-256; Matrix device Ed25519 (L1, Olm-direct sessions only); XMPP OMEMO (XEdDSA Curve25519, L1); Signal identity (XEdDSA, L1, through a client API); Nostr BIP-340; OpenPGP Ed25519; SSH Ed25519 and sk-ecdsa (FIDO). Telegram secret chats and WhatsApp are not supported: no per-device signing identity that a verifier can use, or no client API. Only Matrix has a verifier in M5n; the other entries are reserved. | 3.6 |
| 19 | The D2 signer threat model is accepted, with limits: a key without per-signature presence can be used by any code on that machine, so it is L1 at most, within limits. The presence flag is a claim, not proof. A host console is not L2 when agents have shells on that host. L2 is strengthened: the key's access control is Secure Enclave `biometryCurrentSet` with no passcode fallback, so the key is invalidated when the enrolled fingers change; every signature needs a fresh authentication, with no `LAContext` reuse; the signer itself shows the fields before Touch ID; this must be verified on a real Mac, as a qualification requirement. Several L2 devices are allowed, each with its own record; a finger change invalidates that device's key, and the device is re-added by the slow, guarded add path. At least two L2 devices are recommended. | 3.6, 6, Honest limits |

Decision 1 includes Ivan Oparin's correction of 2026-11-16 at 03:15Z
([Decision 0004](../decisions/0004-reconciliation-closures.md), signed
communication). Section 1 defines M0, the current transitional stage, and
M6, the refuse-unsigned switch. His decision of 2026-11-16 at 01:45Z allows
that switch only after the live messenger-device check, the owner's own
test and break-glass; observe-only verification continues until then. This
text supplies no deployment date. The one-host rule of the Summary is his
decision of 2026-11-16 at 03:08Z.

These three decisions are in force in this version. The co-author's answer
to them is folded in later by amendment and gates nothing (Decision 0004,
status). The envelope, the device list and the levels by which a message is
signed and admitted (sections 3 to 6 and 11) keep their Draft status and
their agreement boundary.

The correction says "effects only on a signature". Section 1 carries that
for the unsigned message itself (O1.1). It does not carry it for the run
that such work starts; that gap is listed under "Open questions".

The device list of sections 3, 4 and 8 stays in its existing format.
The external replacement of that format was not accepted (Decision 0004,
completion before freeze).

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
8. Under decisions 15 and 17: the well-known path, the `d` tag value
   `swarma-device-list` of the Nostr event, the sender's record of what each
   receiver admitted, and that the secondary paths serve only a reader that
   has no sender to ask (section 3.5). The kind of the Nostr event is open
   within the parameterized replaceable range of NIP-01, 30000 to 39999.
   The code `LIST_UNKNOWN` is decision 17's; it replaces the draft's
   `DEVICE_LIST_UNAVAILABLE` of the earlier text of this date.
9. Under decision 16: the value `matrix-ed25519` and the hex form of its key,
   `ceiling` exactly 1, the chain of OM2, the replay key of OM5, the member
   `swarma.owner_command`, the reading of a plain encrypted text as an L1
   `instruct`, which event and which part of it count (`m.room.message`
   with `m.text`, `body` without the reply fallback; an edit and every other
   event ignored), and the code `MESSENGER_UNAUTHENTICATED` (section 4.1).
10. Under decision 14: that `k_D` is neither the device key nor any other
    key, and rules O8.8 to O8.10 (section 8.3).
11. Under decision 18: the `alg` values and the encodings of the reserved
    entries, and the code `DEVICE_ALG_UNSUPPORTED`; the highest levels that
    the decision does not state: 1 for PIV, TPM, Android, Nostr `bip340`,
    OpenPGP and SSH Ed25519, and 2 for `ssh-sk-ecdsa`; UV, not UP, as the
    flag that level 2 needs on a FIDO2 or sk-ecdsa signature (O6.2), where
    the decision names "UP and UV flags as signed presence"; that a verifier
    enforces the highest level per `alg` value and the lower per-entry levels
    bind the owner's client (O3.16); and that `bip340` at 1 narrows decisions
    4 and 11 for a BIP-340 key with claimed presence (section 3.6).
12. Under decision 19: that the three properties of O3.19 are a qualification
    of the owner's signer on a real Mac, which a verifier cannot check; that
    an invalidated key leaves the list by section 8 and returns by section 9
    as a new device (O3.20).

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The device list, its hash and the name-value member as bytes | Yes | The co-author's agreement; vectors |
| The rule set of an executor as a function of stated facts: list, seals, levels, policy, journal | Yes | The same |
| The rows by level in the key holder's table, its copy of each executor's policy and its checks at every level | Yes, beside J7 | The same, J7 itself, and the members of a policy section (open questions) |
| The three body kinds as `swarm-envelope/2` records | No | A reviewed change of `swarm-envelope/2` sections 2.1 and 2.4 (section 5.4) |
| The member in a live name | No | Every verifier of that name on a LIP-0010 reader (section 3.4) |
| Revocation by seal | No | The script of a device seal and the fee of `tx_revoke_D`; custody is decided by Figure 1 (open questions) |
| The device-list check of a Matrix device: list bytes, the record of OM1 and the L1 ceiling | Yes | The co-author's agreement; a receiver that decrypts Megolm and makes the chain of OM2 itself |
| A verifier for an entry of section 3.6 other than `matrix-ed25519`, `p256` and `bip340` | No | The entry leaves the reserved state: its encoding agreed, a verifier and vectors |
| L2 by presence | No | A signer qualified on a real Mac for the three properties of O3.19; no signer is qualified yet (Honest limits) |

## Motivation

**R4: the owner has no voice that a receiver checks.** LIP-0013
section 3.7 formerly let the owner instruct its agent without an envelope;
point 2 now cites the labelled transition of section 1. In shadow mode
"only the owner directs" (section 3.4). Every process that can post into an
unsigned owner channel, and every operator of the transport, speaks with
the owner's authority. The key
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

- LIP-0013 section 3.7, point 2 cites section 1's labelled transition.
  J7.1 binds a run to "the owner's own command"; J7.2 gives the owner's
  commands a row of their own. Section 6 supplies the Draft level rules.
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
| O1.1 | Communication is signed at minimum and encrypted at maximum, using native encryption where possible. During M0, unsigned work is delivered but MUST be labelled as unsigned. The unsigned message itself gives no authority for an effect: an own executor and an own key holder MUST give effect only to a signed message admitted under this LIP. After M6, unsigned input MUST be ignored: it directs no work, starts no run, changes no configuration and counts as no approval. An envelope that fails section 11 gives no authority. | The code of the failed step; nothing for unsigned input |
| O1.2 | Free text inside a signed envelope directs work only. It MUST NOT define, select or widen an effect (LIP-0006 section 7). | |
| O1.3 | An effect happens only through the typed fields of its action class, and the fields MUST define the effect completely. A landing names the repository, the ref and the exact revision, which is a full commit identifier. A payment names the payee and the amount. A class whose fields leave a part of the effect to the executor is not admitted for an effect. | `FIELDS_INCOMPLETE` |
| O1.4 | Before any effect the executor's gate MUST recompute the actual arguments of the operation it is about to perform, from the operation itself and not from the envelope, and compare them with the signed fields. Any difference refuses, and no effect follows. LIP-0014 J5.7 and J5.9 have this step for the owner's confirmation of one operation; O1.4 makes it the step of every effect. | `FIELDS_MISMATCH` |
| O1.5 | The owner's client MUST form the typed fields and show them to the owner before a device signs. The executor's model MUST NOT form them. | |
| O1.6 | The process of the executor's model MUST NOT hold the right to the effect. Keys, tokens and privileges of an effect sit at a gate under another OS account, as the wallet service does (LIP-0006 section 1; LIP-0013 J7.8). | A deployment that leaves one within the model's reach does not meet this LIP |

M0 and M6 name two points of the transition to signed owner communication,
and this LIP uses them in this sense only. **M0** is the current stage:
unsigned owner input is delivered and labelled as unsigned. **M6** is the
switch after which unsigned owner input is ignored. The switch is allowed
only under the conditions that "What is decided and what is proposed"
records, and this LIP gives it no date.

O1.1 covers the unsigned message. It does not cover the run that labelled
unsigned work starts during M0. That run still gets the owner row of the
key holder's table (LIP-0013 J7.1 and J7.2), and section 6 gives a level
only to a run that a signed owner command starts (O6.5). Binding of effects
to the key holder signature is not specified for it ("Open questions").

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
| 2 | `alg` | An `alg` value of the registry of section 3.6 (Draft of 2026-11-16): `bip340` or `p256`; for a messenger device `matrix-ed25519` (section 4.1); a reserved value of the registry otherwise. |
| 3 | `key` | For `bip340`: 64 lowercase hex, a valid x-only secp256k1 key under BIP-340 `lift_x`. For `p256`: 66 lowercase hex, the 33-byte compressed SEC1 point: prefix `02` or `03`, `x` below the field prime, on the curve, not the identity. For `matrix-ed25519`: 64 lowercase hex, the 32-byte Ed25519 public key of a Matrix device, a canonical encoding of a point that is not of small order (section 4.1). For every other `alg`: the key encoding of its registry entry (section 3.6). |
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

`devices` is sorted by the bytes of `key`, which for lowercase hex is the
order of the `key` strings as ASCII, a shorter string first where one is a
prefix of the other. An example with three devices, one of each `alg`, with
line breaks for display only; the real bytes contain none. Its keys are the
P-256 and secp256k1 generator points and the Ed25519 public key of RFC 8032
test 1, so it is an illustration and no device may use them:

```json
{"schema":"swarma-device-list/1","network":"main","owner":"id/alisa","seq":5,"devices":[
{"label":"phone P","alg":"p256","key":"036b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296","presence":true,"ceiling":2,"seal":{"txid":"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1","vout":0}},
{"label":"laptop M","alg":"bip340","key":"79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798","presence":false,"ceiling":1,"seal":{"txid":"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1","vout":1}},
{"label":"Element on P","alg":"matrix-ed25519","key":"d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a","presence":false,"ceiling":1,"seal":{"txid":"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1","vout":2}}]}
```

Without the line breaks it is 789 bytes, and `h(D)` is
`b726e9dd98d9ff7fa6cb98541f4473dcb521d6c872ac17b9ebdcc0c52372ae79`. The name
value then carries
`"swarma-devices":{"seq":5,"sha256":"b726e9dd98d9ff7fa6cb98541f4473dcb521d6c872ac17b9ebdcc0c52372ae79"}`.

For all manifest-backed list reads below, first run LIP-0010 section
11.1's manifest order (`MANIFEST_*`, missing bytes `LIST_UNKNOWN`), then
the list's own order. Equal set seq with a different hash refuses, not
just lower seq; SH5's active-chain/reorg branch applies before comparison.
The logical direct-pin examples below do not bypass this stage.

#### 3.3. The pin reached through the owner's manifest

Ivan Oparin decided on 2026-11-20 (source: `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`) to replace the direct device-list head
with the single top-level `swarma-manifest` head of LIP-0010 section 11.
The co-author's agreement is pending. That confirmed manifest supplies
`sets.swarma-devices`; no `loc`, policy, device keys or list enters the
name. The manifest seq strictly increases on updates; set seq never decreases,
and an untouched device set keeps its seq and hash. The older direct-pin
examples and diagrams below describe the logical device pin reached through
this manifest, not permission to write an additional name member. Legacy
compatibility is explicit under LIP-0010 section 11.2, never a silent fallback.

The Swarma Link editor's resolution keeps device keys internal to owner
control. Foreign-service login uses LIP-0034's separate auth key, not an
owner envelope or any amendment to O3.7/O4.6.


| Rule | Requirement | Refusal |
| --- | --- | --- |
| O3.4 | The name has one `swarma-manifest` head under LIP-0010 SH1. Its verified manifest carries `sets.swarma-devices` as `{"seq":<seq>,"sha256":"<h(D)>"}`. No device-list bytes or policy enters the name. A direct device head remains only a Draft legacy description; legacy holders pins remain readable per name under LIP-0010 section 11.2; manifest-plus-direct forms refuse. | `MANIFEST_PIN_INVALID` or `DEVICE_PIN_INVALID` |
| O3.5 | Match manifest head and entries under LIP-0010 SH6: exact written names, no duplicate, escaped or folded aliases, and canonical shapes. A defective manifest gives no device set and no grant authority or closure. It leaves unrelated `swarma`-based grant checks unchanged. | `MANIFEST_PIN_INVALID`, `MANIFEST_INVALID` or `DEVICE_PIN_INVALID` |
| O3.6 | The pinned `seq` equals the `seq` of the list, and `sha256` equals `h(D)`. | `DEVICE_LIST_MISMATCH` |
| O3.7 | `swarma-devices` gives no grant authority. A Link reader of grants does not read it, and LIP-0010 section 1 holds for grants as written. Only an own executor and an own key holder read it, for owner control. | |
| O3.8 | An update changing only `swarma-manifest`, including its device entry, changes neither owner nor `swarma` and ends no v4 grant. Revoking a device by spending its seal needs no manifest update. | |

Ivan Oparin decided on 2026-11-20 (source: `$qthK9PE_qJlXchm3O9Cdy9Lvz24EmiqwzN8CFhh1n_s`) that the single manifest of
[LIP-0010](LIP-0010-name-value.md) section 11 replaces the Draft separate
heads; the co-author's agreement is pending. A confirmed manifest pins the
device list and the other registered sets. Its sequence strictly increases
on each update, while each set sequence never decreases; an untouched set
retains its head. SH4/SH5 retain the active-chain reorganisation branch and
all journaled removals, revocations and closures. A lower sequence on a
later active-chain update is still a rollback, not a reorganisation.

The holders set and device set share the manifest container, not authority.
Every class verifier reads the former; own executors and key holders read
the latter, for owner control only (O3.7). A holder
names one agent or station, its name-owner key and an individual seal; it
signs nothing for the landlord. L2 devices of that landlord hold prepared
holder-seal spends under LIP-0010 H27.

The one manifest head adds 104 bytes at a one-digit sequence, 119 at the
maximum. LIP-0010 section 8 gives the full budget, including the maximum:

| Value | Bytes without | With `swarma-manifest`, `seq` < 10 | Left of 520 |
| --- | ---: | ---: | ---: |
| Landlord, no `nostr` | 100 | 204 | 316 |
| Landlord, key string | 175 | 279 | 241 |
| Landlord, NIP-05 object | 191 | 295 | 225 |
| Landlord, NIP-05 object and one relay | 294 | 398 | 122 |

The service declaration now travels in the manifest, so the old 150-byte
reserve in the name is released. LIP-0037 recommends keeping the full relay
list in the card and no relay in the name. Legacy direct-head byte counts
are not the manifest budget; the transition is explicit in LIP-0010 section
11.2, and writing the new member is gated on every verifier's reader.

#### 3.4. Deployment order and the cost on v3

| Rule | Requirement |
| --- | --- |
| O3.9 | An owner MUST NOT write the manifest profile before every verifier of that name supports it. Exact-value LIP-0004/v3 readers refuse its extra member without closure. Legacy migration and downgrade protection follow LIP-0010 section 11.2. |
| O3.10 | Every change of the device list is a name update. While it is pending, a v3 verifier refuses the grants of that name, without closure, until the update confirms (LIP-0004 section 5: "Pending changes … refuse without closure"). This outage is a known cost. v3 is the internal alpha, and the cost is accepted. |

On v4 a pending name spend can suspend admission under the selected
observation profile (LIP-0008 section 3), and the J6 text of LIP-0008 section
5.2 reads every pending operation of the issuer's name. Whether an update of
`swarma-devices` alone suspends v4 admission is a question of that profile.

#### 3.5. Distribution of the device list (Draft, 2026-11-16)

Ivan Oparin decided on 2026-11-16, as the lead relayed at about 00:40Z, how
the list reaches its readers (decision 15), and refined it at about 01:15Z
(decision 17). The text is written optimistically: the co-author's agreement
is pending.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O3.11 | The name pins the manifest, and the verified manifest pins device-list seq/hash. Every copy whose exact octets match that entry and all list checks is the list, whoever serves it. | `DEVICE_LIST_MISMATCH` |
| O3.12 | The primary path is the envelope. Every envelope carries the list hash in `devices` (section 5.1). A sender MUST attach the full list in `device_list` when the list has changed since the last envelope that this receiver admitted from it, and at first contact, which is every envelope to a receiver of which the sender holds no record that it admitted an envelope under this `h(D)`. Otherwise the envelope carries the hash alone. An executor and a key holder cache every list that they verified under O3.11, keyed by `h(D)`, and verify a later envelope from the cache. | |
| O3.13 | Optional secondary paths are `https://<authenticated-NIP-05-domain>/.well-known/swarma/device-list/<h(D)>` and a name-channel-key-signed Nostr kind 30079 event with `d` tag `swarma-device-list`, under LIP-0033. The key/relays object supplies no domain by itself. These paths never forbid another source of matching checked bytes. The SSRF boundary restricts network requests; inline manifest/list bytes work without either path. | |
| O3.14 | A receiver that holds no list with the hash that an envelope names refuses by name, and the sender re-sends the envelope with the list attached. The refusal is never replaced by a silent fetch. A reader of a messenger event that holds no list with the pinned hash and finds none on the secondary paths refuses with the same code. The unavailability of a secondary path never blocks an envelope that carries the list. | `LIST_UNKNOWN` |

No path adds a device. The pin comes from the name on the reader's own node
(O5.3, O9.2), and a copy only supplies octets that hash to it. A domain that
drops the file, or a relay that withholds the event, delays the readers that
rely on it and does nothing else. An event of a messenger device (section
4.1) carries neither the list nor its hash, so its readers rely on their cache
and the secondary paths. LIP-0033 assigns dedicated Draft kind 30079 within the NIP-01
parameterized-replaceable range, with `d` tag `swarma-device-list`. A relay
keeps the latest event for that author/kind/tag, and a reader takes the
decoded UTF-8 `content` bytes only where they hash to the manifest entry.
The older unknown-kind question is closed. The NIP-05 key/relays object
does not itself encode a domain: HTTPS is optional and needs an independently
authenticated domain binding. Inline manifest/list bytes work without any
domain or Nostr key. The owner therefore publishes the event after
the name update that pins the list confirms; the domain path, keyed by
`h(D)`, keeps older lists.

#### 3.6. Algorithm registry and presence semantics (Draft, 2026-11-16)

Ivan Oparin decided on 2026-11-16, as the lead relayed at about 01:15Z, that
device records have an algorithm registry (decision 18), and at about 01:40Z,
as the lead and the keeper relayed, what presence means and how L2 is
strengthened (decision 19). The text is written optimistically: the
co-author's agreement is pending.

Each row is one entry. The `alg` value is the draft's; the entry is the
decision's. The signature encoding is over the signing preimage of O4.4,
unless the row says otherwise. "Signed presence" means that the signature
itself covers a flag that the authenticator sets only with a person present;
"claimed presence" means that the owner claims it in the record and the
signature shows nothing. The highest level is the ceiling that a record of
this entry may carry. A verifier enforces it per `alg` value, as the highest
over the entries that share the value (O3.16); the lower level of an entry
that shares its value binds the owner's client at enrolment, because a
verifier cannot tell the entries apart. O3.2 and O3.19 still apply.

| Entry | `alg` | Key encoding | Signature encoding | Presence semantics | Highest level |
| --- | --- | --- | --- | --- | --- |
| Apple Secure Enclave P-256 | `p256` | 33-byte compressed SEC1 point, 66 lowercase hex (section 3.1) | 64 bytes `r‖s`, low `s`, over SHA-256 (O4.2) | Claimed: the access control of O3.19 makes each signature need a fresh biometric authentication, which the verifier cannot see | 2, under O3.19 |
| FIDO2/WebAuthn, ES256 or EdDSA | `fido2-es256`, `fido2-eddsa` | The COSE key of the credential: P-256 as the 33-byte compressed point, Ed25519 as 32 bytes; lowercase hex | The assertion: `authenticatorData` and `clientDataJSON` beside the signature, which is ES256 as 64 bytes `r‖s`, low `s`, or EdDSA as 64 bytes, each over `authenticatorData ‖ SHA-256(clientDataJSON)`; the `challenge` of `clientDataJSON` is the SHA-256 of the signing preimage | Signed: the flags byte of `authenticatorData`; UP (bit 0) is a touch, UV (bit 2) is a verified person. A record with `presence` `true` needs UV on every signature | 2, with UV |
| YubiKey PIV P-256 and P-384 | `p256`, `p384` | P-256 as above; P-384 as the 49-byte compressed SEC1 point, 98 lowercase hex | P-256 as O4.2; P-384 as 96 bytes `r‖s`, low `s`, over SHA-384 of the signing preimage | Claimed: a touch policy of the slot is set at enrolment and the PIN is cached; the signature shows neither | 1 |
| TPM 2.0 P-256 | `p256` | As above | As O4.2 | None: a TPM key signs for any process with the authorization value | 1 |
| Android Keystore and StrongBox P-256 | `p256` | As above | As O4.2 | Claimed: user authentication per use with invalidation on biometric enrolment is the counterpart of O3.19 and is not verified on a device | 1 until that check is done on a real device (open questions) |
| Matrix device Ed25519 | `matrix-ed25519` | 32-byte Ed25519 key, 64 lowercase hex (OM1) | No envelope signature: the Megolm message signature of a session bound to the device over Olm (OM2); forwarded, restored and imported sessions never count (OM3) | None | 1 |
| XMPP OMEMO | `omemo-xeddsa` | The 32-byte Curve25519 identity key of the OMEMO device, 64 lowercase hex | XEdDSA, 64 bytes, over the signing preimage, as OMEMO signs its signed pre-key; the session binding is open | None | 1 |
| Signal identity | `signal-xeddsa` | The 32-byte Curve25519 identity key, 64 lowercase hex, read through a client API | XEdDSA, 64 bytes; the binding of a message to the identity key through a client API is open | None | 1 |
| Nostr BIP-340 | `bip340` | 32-byte x-only key, 64 lowercase hex (section 3.1) | BIP-340, 64 bytes (O4.3) | None: a browser or client signer may ask the person, and the signature shows nothing | 1 |
| OpenPGP Ed25519 | `openpgp-ed25519` | The 32-byte Ed25519 key of the key packet, 64 lowercase hex | The raw 64-byte Ed25519 signature over the signing preimage; an OpenPGP signature packet is not admitted until a profile reads it | Claimed where a hardware token holds the key; none otherwise | 1 |
| SSH Ed25519 and sk-ecdsa (FIDO) | `ssh-ed25519`, `ssh-sk-ecdsa` | Ed25519 as 32 bytes; sk-ecdsa as the 33-byte compressed P-256 point; lowercase hex, from the OpenSSH key blob. The application string of an sk key, whose SHA-256 opens the signed data, is not in the record; where it goes is open | Ed25519 as the raw 64-byte signature; sk-ecdsa as the OpenSSH signature with its flags byte and counter beside `r‖s` | Ed25519: none. sk-ecdsa: signed, the flags byte of the signature, as FIDO2 | Ed25519: 1. sk-ecdsa: 2, with UV |

Not supported:

| System | Reason |
| --- | --- |
| Telegram secret chats | No per-device signing identity that a verifier can use: a secret chat is keyed by a Diffie-Hellman exchange and signs nothing, and no client API exposes its keys. |
| WhatsApp | No client API: the identity keys exist in the client and no interface exposes them or binds a message to one. |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O3.15 | Every `alg` of a device record is an `alg` value of this registry, and `key` has the key encoding of its entry. A value outside the registry refuses the list. | `DEVICE_LIST_INVALID` |
| O3.16 | A verifier verifies the signatures of a record under the signature encoding of its `alg` value and admits a `ceiling` up to the highest level of that value, which is the highest over the entries that share it: 2 for `p256`, and for `fido2-es256`, `fido2-eddsa` and `ssh-sk-ecdsa` with UV on every L2 signature (O6.2); 1 for every other value. A record whose `ceiling` exceeds the highest level of its `alg` value refuses the list. The lower highest levels of the PIV, TPM and Android entries, which share `p256`, and the cap of O3.18 on a key without per-signature presence are rules for the owner's client: it enrols no record above the highest level of the entry that holds the key. A verifier cannot tell those entries apart and does not try. | `DEVICE_LIST_INVALID`; none at the verifier for the per-entry level |
| O3.17 | Of the entries, only `matrix-ed25519` has a verifier in M5n (section 4.1). `p256` and `bip340` have the rules of section 4 and wait for the registration of section 5.4. Every other entry is reserved: it is registered so that a list may name it, and it has no verifier and no vector. A receiver without a verifier for the `alg` of a record admits the list and refuses every command of that device. | `DEVICE_ALG_UNSUPPORTED` |
| O3.18 | The D2 signer threat model is accepted, with limits. A key without per-signature presence can be used by any code on that machine, so a record of such a key has `ceiling` at most 1 and acts within the L1 limits of the executor's policy. The presence flag is a claim, not proof (section 3.1, `presence`; Honest limits). A host console is not L2 when agents have shells on that host (O6.3). | `DEVICE_LIST_INVALID` for a ceiling above the highest level of the `alg` value (O3.16); none at the verifier for the cap on a key without presence, which the owner's client applies at enrolment |
| O3.19 | A record with `presence` `true` and `ceiling` 2 of the Secure Enclave entry is enrolled only for a key whose access control is `biometryCurrentSet` with no passcode fallback, so that the key is invalidated when the enrolled fingers change; whose every signature needs a fresh authentication, with no reuse of an `LAContext`; and whose signer shows the fields of the envelope itself before Touch ID (O1.5). A record of this kind is enrolled only through a signer that has been qualified on a real Mac for these three properties; the qualification is of the signer build, once, and not an act of the client at each enrolment. A verifier reads only the record and cannot check them. | None at the verifier |
| O3.20 | An owner may hold several L2 devices, each with its own record and its own seal. When the enrolled fingers of a device change, its key is invalidated and signs nothing more; the device leaves the list by section 8 and returns, with a new key and a new seal, by the slow add path of section 9. At least two L2 devices are RECOMMENDED, so that one invalidated key leaves the owner an L2 device. | |

A `p256` record says nothing about which of its four entries holds the key.
The owner knows at enrolment and claims `presence` and `ceiling` from the
entry; the verifier reads the claim and enforces only the highest level of
the value, 2 (O3.16). A PIV, TPM or Android key enrolled as `p256` with
`presence` `true` and `ceiling` 2 passes every verifier; only the owner's
client, at enrolment, refuses it. The FIDO2 and sk-ecdsa entries are the
two whose presence a verifier sees in the signature, and they conflict with
`swarm-envelope/2` section 2.4 until the reviewed change of section 5.4
(Reconciliation, X16).

### 4. Device keys and signatures

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O4.1 | A device key is a P-256 key or a BIP-340 key, as its record says. Under section 4.1 it may also be the Ed25519 key of a messenger device. Every other `alg` is a reserved entry of section 3.6. | |
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

#### 4.1. Messenger devices (Draft, 2026-11-16)

Ivan Oparin decided on 2026-11-16, as the lead relayed at about 00:40Z, that
the device key of a messenger is an ordinary device record (decision 16). The
text is written optimistically: the co-author's agreement is pending. It pins
the Matrix device. An XMPP OMEMO device follows the same rules under the
reserved entry `omemo-xeddsa` of section 3.6; how its message binds to the
identity key is open.

| Rule | Requirement | Refusal |
| --- | --- | --- |
| OM1 | A messenger device is an ordinary record of section 3.1, with its own seal. Its `alg` names the messenger's algorithm: `matrix-ed25519` for a Matrix device. Its `key` is the Ed25519 key that the device's signed device-keys object publishes as `ed25519:<device_id>`, in 64 lowercase hex; a reader decodes the unpadded base64 of the Matrix wire to compare bytes. Its `presence` is `false`, and its `ceiling` is `1`. | `DEVICE_LIST_INVALID` |
| OM2 | An end-to-end encrypted Matrix room event counts as an owner command at level 1 when, and only when, the receiver binds it to the record's key through this chain: the event is `m.room.encrypted` with algorithm `m.megolm.v1.aes-sha2`; its Megolm message signature verifies under the Ed25519 key of its Megolm session; the receiver received that session as `m.room_key` in an Olm message from the Curve25519 identity key of the sending device; and that Curve25519 key is the one in the device-keys object that the record's Ed25519 key signs. The `room_id` of the decrypted payload equals the room that the deployment names as the owner's channel to this executor or key holder. | `MESSENGER_UNAUTHENTICATED` |
| OM3 | A session that the receiver did not receive as OM2 says gives no command: a session from `m.forwarded_room_key`, one restored from server-side key backup, one imported from a file, and one whose Olm sender the receiver cannot bind. The receiver never takes the device from the event's `sender`, from its `sender_key` or `device_id` fields, or from the homeserver. | `MESSENGER_UNAUTHENTICATED` |
| OM4 | A plaintext event never counts as an authenticated messenger command. O1.1 governs unsigned input: labelled work during M0, ignored after M6. It authorizes no effect. | Nothing |
| OM5 | The replay journal of O4.5 keys the event by its Megolm session identifier and message index, which the session's signature covers. A pair already in the journal refuses. | `REPLAY` |
| OM6 | The decrypted content gives the command. A member `swarma.owner_command` that holds the members of section 5.1 other than `type` and `device_list`, and those of section 5.2 with `level` `0` or `1`, gives that command. Without that member, only a decrypted event of type `m.room.message` with `msgtype` `m.text` counts: it is an owner command with `level` 1, `action` `instruct` and `fields` `{}`, whose free text is `body` with the reply fallback removed, which is every leading line that begins with `> ` up to the first empty line; `formatted_body` is not read. It starts or directs a run at L1 (O6.5) and defines no effect (O1.2, O1.3). An edit (`m.relates_to` with `rel_type` `m.replace`), every other `msgtype` and every other event type give no command and are ignored. | The codes of section 11; nothing for an ignored event |
| OM7 | Section 11 applies with four changes. OM2, OM3 and OM5 take the place of steps 1, 7 and 11. Step 6 finds the record whose `key` equals the Ed25519 key of OM2 and whose `alg` is `matrix-ed25519`. Steps 2 and 3 apply only where OM6 gives `aud`, `iat` and `exp`; the room of OM2 stands in for `aud` otherwise. Step 5 compares `devices` only where OM6 gives it; otherwise the list that the receiver holds in its cache, or fetches under O3.13, hashes to the pin of step 4, and a receiver that holds and finds none refuses `LIST_UNKNOWN` (O3.14). A messenger event never carries `device_list`. | The codes of section 11 |

Megolm signs every message with the session key of its originator, so a
homeserver cannot forge or alter an event inside a session. Two risks remain:
the binding of the session to a device, which OM2 makes through the Olm
channel, and the `sender` that the homeserver asserts, which OM3 never reads.
The receiver has to decrypt and make the chain of OM2 itself. A client that
hands it decrypted text does not meet the rule.

A certificate statement of LIP-0015 section 6 of kind `matrix-device` binds a
Matrix device to a name and gives no authority. A record of OM1 makes the same
device the owner at level 1 at the owner's own executors and key holders. One
device can have both, and neither implies the other.

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
| `device_list` | The exact octets of that list, canonical unpadded base64url. The sender attaches it on change and at first contact (O3.12, Draft of 2026-11-16) and leaves it out otherwise; a verifier that holds the list under `devices.sha256` does not refuse an envelope for the lack of it, and one that does not refuses `LIST_UNKNOWN` (O3.14) | Proposed here |

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

The authority frame travels on the separate channel of
[LIP-0013](LIP-0013-trust-contract.md) section 3.4. A signature on the frame
is NOT established; no fourth signed body kind follows from that decision.

### 6. Levels and the level of a launch

| Level | What it admits | Who signs it | What a run started at it may sign (O6.7) |
| --- | --- | --- | --- |
| L0 | Work: a run is started or directed; no effect | A device of the current list with `ceiling` 0 or more | No object whose action ends in an effect |
| L1 | Effects within the limits of the executor's policy (section 7) | A device with `ceiling` 1 or more | Effects of the classes that the policy for the executor assigns to L0 or L1, within its L1 limits |
| L2 | What the policy assigns to L2; a class outside the registry (O2.3); the policy itself (section 7); the fast revocation (section 8.2) | A device with `presence` `true` and `ceiling` 2, or a separated human console | Effects of every class that the policy for the executor admits, within its L2 limits, and a class outside the registry; never the policy or a revocation (O6.12) |

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O6.1 | The `level` of an owner command MUST NOT exceed the `ceiling` of its device. | `LEVEL_ABOVE_DEVICE` |
| O6.2 | L2 is signed only by a key whose record has the presence flag and whose `alg` value admits level 2 (section 3.6, O3.16, O3.19), or given at a separated human console. Where the entry carries presence in the signature, the flag of a verified person (UV) is on every L2 signature. | `LEVEL_ABOVE_DEVICE` |
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

O8.3 and O8.4 are the model of the seal of a holder entry (LIP-0010 section
10.7), and that section states for the holder seal what a durable closure
needs. By pointer, and with no change to a rule of this LIP: a closure that
no rollback lifts stands for a verifier that validates the spending
transaction on its own node (LIP-0010 H28, H29, H47). A verifier that reads
the chain through a gateway which returns only the state of a seal
(unspent, unconfirmed, spend pending, not in the confirmed set) is a
non-witness for closures that begin in the mempool: it makes every step of
the admission, refuses on every state but unspent, admits on unspent only
when the gateway shows the seal's confirmed funding with its script and its
height, refuses as a failed read where the gateway cannot show it, and
records no enforcement closure. Where the gateway shows the seal absent
from the confirmed set, it may keep an observe-grade closure, named so and
never used for
enforcement, because it validated no spending transaction and the absence
can also follow a reorganisation that removed the funding of the seal. An
enforcement closure needs the octets of the spending transaction, validated
by the reader against the script of the seal, every spender that the node
holds, and one named tip; the watcher journal of a deployment is the source
of that evidence, and neither LIP specifies it (LIP-0010 H50). A closure
that such a watcher supplies is consulted in the seal step of the
admission and before the effect, and counts only with the validated
spender, the seal's confirmed funding and one named tip; its format and
its transport are open (LIP-0010 H28).

**The device seal of this section keeps its own reading.** O8.3 and O8.9
stand as they are written, and the conditions of LIP-0010 H45 to H48 do not
bind a device seal. The two readings differ, and the difference is stated
here so that nobody takes one for the other. O8.3 journals a closure for a
spend that the executor's node sees, with no definition of a validated
spend and no condition that the funding of the seal is confirmed; for a
holder seal the spend of an unconfirmed seal refuses without closure
(LIP-0010 H47, point 5). O8.9 refuses as `DEVICE_REVOKED` whenever
`gettxout` does not show the seal unspent, so a device seal that is
unconfirmed, has another script or was never funded reads as revoked, and
the code does not tell a defect of the listing from a revocation; for a
holder seal those are `HOLDER_SEAL_NOT_LIVE` and a failed read is
`CLASS_HISTORY_UNAVAILABLE`. An executor that is also a verifier of a
landlord class watches both kinds of seal on one node and keeps two
meanings of a closure, one for each kind. The reason is one of scope and
no judgement that the older reading is sound: the amendment that hardened
the holder seal changes no rule of this LIP, only an owner's own executors
read a device seal (O3.7), and splitting the device codes to match is a
change of this LIP that its owners have not decided. That the divergence
stands until then is this text's choice; whether the device seal takes the
reading of LIP-0010 H45 to H48, with its codes split to match, is open.

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

#### 8.3. The device seal (Draft, 2026-11-16)

Ivan Oparin decided on 2026-11-16, as the lead relayed at about 00:40Z, that
the device seal works as Figure 1 shows, and that the figure stands in this
LIP and in the book in the same words (decision 14). The text is written
optimistically: the co-author's agreement is pending.

Figure 1. The device seal.

```text
Adding a device D:

    seal S_D on a fresh k_D
              |
              v
    a pre-signed tx_revoke_D
              |
              v
    k_D destroyed
              |
              v
    the spend handed to the other devices
              |
              v
    the list hash in the name by the cold key

Per command:

    device signature
      + list hash from the name
      + gettxout(S_D) unspent

On loss:

    any device broadcasts tx_revoke_D
    a rollback cannot restore D
```

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O8.8 | The seal `S_D` of a device `D` is an output that pays a fresh CSPRNG key `k_D`, never derived from a BIP-39 seed and neither the device key nor any other key (the Swarma Link editor's resolution, owner's v0.3 draft, 2026-11-20). Before `D` is added, a transaction `tx_revoke_D` that spends `S_D` is signed with `k_D`, and `k_D` is then destroyed, so that no spend of `S_D` other than `tx_revoke_D` can be signed afterwards. `tx_revoke_D` is the prepared spend of O8.2, and it reaches the other devices under O9.3. | |
| O8.9 | For every command an own executor checks three things: the device's signature (section 11, steps 6 and 7), the list hash from the name (steps 4 and 5), and that `gettxout` on its own node, with the mempool included, shows `S_D` unspent (step 8). | `DEVICE_REVOKED` for the third |
| O8.10 | When `D` is lost, any other device of the list broadcasts `tx_revoke_D`. A rollback cannot restore `D` (O8.4). | |

O8.8 answers the custody of a device seal: nobody holds its key. It also
fixes the fee of `tx_revoke_D` when it is signed. How that fee is set and
raised, the script of `S_D`, and what `tx_revoke_D` pays are open. If every
other device loses `tx_revoke_D`, `S_D` can no longer be spent, and only the
fast path of section 8.2 and a name update remain.

### 9. Adding a device

| Rule | Requirement | Refusal |
| --- | --- | --- |
| O9.1 | Adding a device needs a new device list that holds its record, the device's new seal, and an update of the owner's name signed by the name-owner key that writes a higher-seq manifest with the new `sets.swarma-devices` head and its higher set `seq`, under LIP-0010 SH5. | |
| O9.2 | An executor takes a list only through the pin in the owner's name value on its own node, in its validated active chain, and only with a `seq` higher than the highest it journaled. "Higher" is the condition of a take alone: a pin that equals the journaled one, in `seq` and in hash, is the list that the executor holds, and it is read at every command with no new take and no refusal. An envelope, an attachment or a message never adds a device. | `DEVICE_LIST_ROLLBACK` |
| O9.3 | The prepared spend of the new seal MUST reach the other devices under O8.2 before the new device signs anything. | |

Adding is slow and guarded by design; removing is fast. The reviewer's figures
for the wait are a median of about seven minutes for a confirmation and more
than thirty minutes in five cases of a hundred, plus the time to fetch the cold
name-owner key. A thief of one device cannot add a second one, and every
device can remove a stolen one at once.

### 10. Key boundaries

| Rule | Requirement |
| --- | --- |
| O10.1 | The name-owner key decides who speaks for the owner by updating the manifest head and pinned device entry. It never logs in or signs an envelope. |
| O10.2 | The grant key grants to others only. It signs grants and what a grant needs: the contract hash of `landlord_sig`, on v3 the spend of a seal that pays it, and on v4 the endorsement of a seal key (LIP-0004 sections 2, 3 and 5; LIP-0008 section 11). Under Draft LIP-0008 section 11.4 of 2026-11-16 the v4 grant carries its seal key, and the grant key signs no endorsement. It signs no statement, no configuration, no device list and no envelope. |
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
| 4 | `X` reads the owner's confirmed name and first runs LIP-0010 section 11.1 steps 1–6 for its manifest and device entry. Then check the device pin/list journal under SH5: a lower set seq, or equal seq with a different hash, refuses, subject to its active-chain/reorg rule | The ordered `MANIFEST_*` and `LIST_UNKNOWN` refusals of section 11.1, then `DEVICE_PIN_INVALID`, `DEVICE_LIST_ROLLBACK` |
| 5 | `devices` equals the pin; the list that `X` holds under that hash, cached or attached, hashes to it | `DEVICE_LIST_MISMATCH`; with no list under that hash, `LIST_UNKNOWN` (O3.14), and the sender re-sends with the list attached |
| 6 | Exactly one signature, whose key equals the `key` of one record, under that record's `alg`, for which `X` has a verifier (O3.17) | `DEVICE_UNKNOWN`, `DEVICE_ALG_MISMATCH`, `DEVICE_ALG_UNSUPPORTED` |
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
| S29-1 | Alisa's phone `P` (`p256`, presence, ceiling 2) signs an L1 landing at `X` with repository, ref and revision; the gate finds the same commit: admitted | The same message without an envelope, in the owner channel: during M0, delivered as labelled work with no landing; after M6, ignored with no run. The model of `X` rewrites `revision` before the gate: `FIELDS_MISMATCH`. |
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
| S29-16 | `P`'s first command to `X` carries list 5 attached; `X` has no list cached, and Alisa's domain is down: admitted, and `X` caches list 5 (O3.12, O3.14). `P`'s next commands to `X` carry the hash alone: admitted from the cache. Alisa adds `K`, and `P`'s first command under list 6 to `X` carries list 6 attached: admitted | The attached octets with one added space: `DEVICE_LIST_MISMATCH`. A command under list 6 with the hash alone to `V`, a second own executor of Alisa's that `P` never addressed, or to `X` before it saw list 6: `LIST_UNKNOWN`; `P` re-sends it with list 6 attached: admitted. The same command to Bob's executor `Y`: `DEVICE_LIST_MISMATCH` before any question of the cache, as S29-12 has it (O10.4). A Nostr event with a list that the name does not pin: not taken (O3.11). A list fetched from a URL that the command names: not taken (O3.13). |
| S29-17 | Alisa's Matrix device `E` (`matrix-ed25519`, no presence, ceiling 1) sends an encrypted "review branch fix-7" to her owner room of `X`. The harness of `X` received the session from `E` over Olm, and `X` holds list 5, cached from `P`'s envelope of S29-16, which hashes to the pin (OM7, step 5): an L1 `instruct`, and the run it starts has level L1 | The same text as a plaintext event: labelled unsigned work during M0, ignored after M6, and never an authenticated messenger command. The same event, decrypted with a session from `m.forwarded_room_key` or from key backup: `MESSENGER_UNAUTHENTICATED`. The same event at an executor with an empty cache, Alisa's domain down and no Nostr event for the `d` tag: `LIST_UNKNOWN`, and nothing to re-send, because the event carries no list. A list that gives `E` ceiling 2 or presence: `DEVICE_LIST_INVALID`. A `swarma.owner_command` of `E` with `level` 2: `LEVEL_ABOVE_DEVICE`. The same text sent as a reply to the agent's proposal: the quoted lines of the fallback are not Alisa's words, and the instruction is "review branch fix-7" alone (OM6). An edit of that event, an `m.notice`, or a file event whose `body` is a file name: ignored, and the first instruction stands. The same session and message index again: `REPLAY`. An event that the homeserver labels as Alisa's but whose session binds to a device in no record: `DEVICE_UNKNOWN`. |
| S29-18 | `M`'s seal `S_M` pays a fresh `k_M`; `tx_revoke_M` is signed, `k_M` destroyed, and `P` and `K` hold the spend; `X`'s `gettxout` shows `S_M` unspent, and `M`'s command is admitted | `P` broadcasts `tx_revoke_M`; `M`'s next command: `DEVICE_REVOKED`. After a reorganisation that removes the block with `tx_revoke_M`: still `DEVICE_REVOKED`, because the closure is journaled (O8.4). |
| S29-19 | Alisa's phone `P` and her laptop `M2` are both Secure Enclave records with presence and ceiling 2, each with its own seal, enrolled under O3.19. Alisa enrols a new finger on `P`: `P`'s key is invalidated and signs nothing more; `K` broadcasts `tx_revoke_P`, and Alisa adds `P` again with a new key and a new seal by section 9. Meanwhile `M2` signs her L2 commands (O3.20) | Alisa's client refuses to enrol a YubiKey PIV slot (`p256`, touch policy) at ceiling 2, because the highest level of the PIV entry is 1 (O3.16); a verifier cannot tell that record from `P`'s and would admit it, which is why the rule binds the client. A `p384` record with ceiling 2: `DEVICE_LIST_INVALID`, because the highest level of `p384` is 1 (O3.16). A record with `alg` `fido2-es256` at `X`, which has no verifier for it in M5n: the list is admitted and its command refuses `DEVICE_ALG_UNSUPPORTED` (O3.17). A record with `alg` `telegram`: `DEVICE_LIST_INVALID` (O3.15). An assertion of a `fido2-es256` record with presence whose flags byte has UP without UV, at an executor that has a FIDO2 verifier: `LEVEL_ABOVE_DEVICE` at L2 (O6.2); at `X` the same assertion refuses `DEVICE_ALG_UNSUPPORTED` at step 6. |

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
  signs. O3.19 closes the first two at the signer, with `biometryCurrentSet`
  and no passcode fallback and with a fresh authentication for each
  signature, and asks the signer itself to show the fields; the verifier
  still sees none of it. No signer is qualified on a real Mac for the three
  properties of O3.19, and none for exact-content presence
  (`swarm-envelope/2` section 4: "no signer provider is qualified for A3");
  L2 by presence rests on that qualification and on the owner's enrolment
  until one is.
  Only the FIDO2 and sk-ecdsa entries of section 3.6 put a presence flag into
  the signature, and no verifier admits them yet.
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

- **A messenger device is as safe as its client.** The key of a Matrix
  device lives in the client's storage, with no presence, and any code that
  reads that storage can send as the device. The L1 ceiling and the L1
  limits bound what it reaches. A plain encrypted text carries no signed
  time, so a homeserver can hold it back and deliver it later; OM5 still
  refuses a second delivery. A messenger event carries no list and no hash,
  so a reader with an empty cache depends on the secondary paths, and a
  refusal `LIST_UNKNOWN` there has no sender that re-sends.
- **An invalidated L2 key is a lost device.** Under O3.19 a change of the
  enrolled fingers destroys the key. The owner removes the device and adds it
  again by the slow path, and with one L2 device only, no L2 command can be
  signed in between (O3.20).
- **A device seal can be lost.** Nobody holds `k_D`. If every other device
  loses `tx_revoke_D`, the seal can no longer be spent, and only the fast
  path of section 8.2 and a name update remain for that device.

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
| Ch. 24 §24.4 and §24.8 (`24-soobscheniya-i-most.md`, lines 56–78 and 109–126) | Assurance levels A0 to A3 for people's messages; an unsigned body is untrusted data; a transitional mode admits A0 and A1 commands within zones. | Decision 1 carries the labelled M0 transition (X1); L0 to L2 still have no stated mapping to A0 to A3 (X11). |
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
following points. X1 records the correction of 2026-11-16. The remaining
conflicts retain their existing open or proposed status.

| # | Decision | Conflict |
| --- | --- | --- |
| X1 | 1 | Decided on 2026-11-16: signed at minimum, encrypted at maximum. Transitional (M0): unsigned work is delivered but labelled; effects only on a signature; after M6, unsigned input is ignored. Section 1 and LIP-0013 section 3.7 point 2 carry this rule for the unsigned message itself; the run that such work starts is an open question. The Link book section 8.9 requires the same correction. The transitional mode of the platform book (§24.4), which admits A0 and A1 commands within zones, is wider than this rule; it stays a platform-book item on hold. The level mapping of X11 remains open. |
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
| X16 | 18 | `swarm-envelope/2` section 2.4 refuses WebAuthn assertions, and its signature profiles name P-256 and BIP-340 only. Decision 18 registers FIDO2, P-384, XEdDSA, Ed25519 and the OpenSSH forms as entries; each needs the reviewed change of section 5.4 before a verifier admits it. |

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

- **Decisions 14 to 19 (Draft, 2026-11-16).** The script of `S_D`, how the
  fee of `tx_revoke_D` is set and raised, and what it pays; the kind of the
  Nostr event of O3.13, within 30000 to 39999, and the case of an owner
  without a NIP-05 domain; the storage service under a grant as a third
  path; whether OMEMO 0.3 Curve25519 identity keys are admitted at all, and
  how an OMEMO or Signal message is bound to the identity key; whether a
  messenger device may have `ceiling` 0; the `alg` values and encodings of
  the reserved entries of section 3.6, the hash of the P-384 preimage and
  the place of an sk key's application string among them; whether a PIV slot
  with a touch policy can reach L2, which only the owner's client could
  enforce (O3.16); whether a BIP-340 key in a hardware signer with claimed
  presence may reach L2, which `bip340` at 1 denies; the Android counterpart
  of O3.19 on a real device; a signal to a messenger sender whose list the
  reader lacks; and the book's copy of Figure 1, which seat B writes in the
  same words. "Olm-direct sessions only" of decision 18 is read as OM2 and
  OM3 read it: a Megolm session received directly over Olm from the
  originating device, not commands by Olm to-device messages alone.
- **The co-author's agreement** to the nineteen decisions, written here
  optimistically, and the owners' acceptance of each point that the section
  "What is decided and what is proposed" lists as the draft's.
- **A run that unsigned work starts (decision 1, stage M0).** A run started
  by labelled unsigned work still gets the owner row; binding of effects to
  the key holder signature is not specified.
- **The remaining conflicts X2 to X16** of the section "Reconciliation",
  which the owners decide; X1 is corrected above. Above all X3, the anchor
  of the owner's devices, and X10,
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
  section 8 keeps for the service declaration of LIP-0007. With the member
  `swarma-holders` of LIP-0010 section 10.3 beside it, the same value leaves
  20 bytes.
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
