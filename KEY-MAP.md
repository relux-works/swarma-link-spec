# Key map

The Grant v4 proposal in LIP-0008 separately binds the issuer name's
registration and owner key in the grant, agent pointer and independent
verifier pins; the verifier walks the name's history, and a renewal closes
nothing. It also proposes a derived key per seal with a typed issuer
endorsement of the key/script/outpoint. These are distinct identity and script
pins. LIP-0008 section 11.1 proposes BIP-32 derivation of the keys of
revocable-only seals in an account of their own, so that the grant key no longer spends seals; custody
qualification, recovery and migration remain open. Distinct seal
addresses reduce one linkage source; names/funding/anchors remain observable.
Draft LIP-0012 adds a notary key that signs attestations and a notary seal
that only the notary spends; neither is in the table below, and the notary
key signs no grant. Draft LIP-0014 names where they live: the attestation
key is published in the notary's own `id/` name, in the `swarma.notary`
shape that LIP-0010 section 9 proposes, and is replaced by an update of that
name; the seal pays a different key; and the attestation key is held by a
key service that signs on request and does not export it.

Informative custody map for the rental and wallet profiles, not normative adoption.
Deployment policy keeps the landlord grant key separate from the owner's personal Nostr key.
By design, public keys and pins reach verifiers; hot service keys stay outside the agent's OS user.
Rotation below names required operator work, not an automatic migration protocol.
The table describes existing rental/wallet profiles; the v4 paragraph above is
a separate design proposal.

| Key / custodian | Signs or authorizes | Rotation / breakage | Theft and containment |
| --- | --- | --- | --- |
| Name owner / cold | Updates/transfers `id/`, `d/`. | Transfer name output; old key loses control. | Hijack names/bindings; protect cold custody. |
| Landlord grant key / issuer | Grant, contract hash, P2PKH seal spends. | Confirm grant-key update in name; prior observers close grants. Old seals need old key. | Forge grants/spend seals; binding change stops future admission. |
| Funding key / issuer | Fees and pool refill; separate script. | New script, move funds, reconcile accounting. | Drain funding; cannot spend seals. |
| Provider key / booking | Contract hash and kind-8182 package. | New provider pin rejects old packages. | Forge offers; consent and issuance checked separately. |
| Agent Nostr key / gateway | NIP-17; public key in `id/`, `d/`. | Update value/mirror/pins; messaging address changes. | Read/impersonate messages; grant key stays separate. |
| Renter key / renter device | Kind-8181 consent, NIP-17; grant `grantee_key`. | Update contacts; revoke/reissue old grants. | Impersonate renter; revocation, window and grant limits constrain use. |
| Single-use grantee / client | 1-of-2 P2SH spend committing request hash. | Revoke; issue new grant and seal. | Take seal value; grant/request/window/journal and service peer admission constrain effects. |
| Wallet money keys / Core | Coin signatures via private service RPC. | New addresses, fund/RPC access transfer. | Drain funds; keep secrets outside client. |
| Receipt key / wallet service | Results checked against client pin. | New pins/state migration; old journal refuses. | Forge receipts; cannot spend coins with this key. |
| Model bearer / proxy mints for slot | Model access within slot window. | Revoke binding; new slot gets new secret. | Transferable use bounded by revocation, window and limits. |
| Transport keys / endpoints | TLS leaf pins, gateway/manager mTLS; channel HMAC. | New certificates/pins; old pins refuse. | Impersonate peer; grant checks remain separate. Channel secret expires with slot. |

The authority path and the distinct seal profiles are:

```text
cold key -> landlord id/ -> grant key
         -> agent id/    -> gateway Nostr key
         -> d/           -> discovery only
renter -> consent + contract <- provider
grant key -> grant -> P2PKH seal -> service admission
grant key -> seal spend         -> closure
funding   -> fees + seal pool
grantee   -> request + 1-of-2 P2SH spend -> wallet
wallet    -> receipt (service key)
slot      -> bearer -> model proxy (window and limits)
```

The seals belong to distinct profiles; `d/` is discovery only. In v3, messaging-key
rotation does not revoke grants. The proxy keeps the upstream API secret;
slots receive bearers. Upstream API theft bypasses slot limits.
Raw grant-key/money-key/RPC theft bypasses service quotas.
Preserve journals; deleting state restores no authority and undoes no effects.

Basis: [public implementation at 11084e3a](https://github.com/relux-works/swarma-chain-lab/tree/11084e3a31175907e77644a7596e7802283e7c1e/experiments),
[LIP-0004](lips/LIP-0004-landlord-grants.md), [LIP-0006](lips/LIP-0006-grant-gated-actions.md).
Model caps denote signed contract terms proposed in [PR #60](https://github.com/relux-works/swarma-chain-lab/pull/60),
not landed integration or mainnet qualification. In v3, a first observer cannot
prove unseen grant-key changes; pin/state migration needs coordinated operator work.
The v4 draft instead finds a changed owner or grant key in the issuer name's
history, without local memory; see
[LIP-0008](lips/LIP-0008-grant-v4.md).

## Decisions of 2026-11-12

The owners decided four points about keys and identities on 2026-11-12. They
change no grant format.

| Decision | Direction |
| --- | --- |
| K1. Three keys per principal | A principal has a name-owner key, a Nostr key and a grant key. There is no separate administrative key for now. |
| K2. Agents have their own identities | An agent has its own `id/` name. The person who operates the agent holds that name's owner key. The agent controls only its Nostr key, and a change of that key is a name update by the person. The agent's landlord pointer names its operator's landlord name. |
| K3. Stable roles | Only an owner creates an identity. Project roles are stable, and the owners register them. An agent registers no identity for another agent. |
| K4. No signed configuration sections yet | Sections of an agent host's configuration are not signed until a trust anchor exists. A key named in the same file is no anchor: whoever can rewrite the section can rewrite the key. |

K1 adds no row to the table above. The name-owner key and the landlord grant
key are its first two rows, and the principal's Nostr key is the personal
key that the deployment policy above keeps apart from the grant key. Under
K2 the name-owner key of an agent name is one of its operator's cold keys,
and the agent's Nostr key is the fifth row. How an agent's Nostr key reaches
its gateway is not decided.

## Grant v3: clarifications for names and keys

These four points restate rules of LIP-0004 and LIP-0010 for a deployment
that issues v3 grants. They add no rule.

**Only the exact LIP-0004 values.** Until every verifier of a name runs a
LIP-0010 reader, an issuer MUST write that name only in the exact value
shapes of LIP-0004 section 1. A LIP-0004 reader compares the whole value
with the bytes of its own builder, so any additional member, inside `swarma`
or beside it, makes the value unreadable. Every v3 grant under that name
then refuses at every such verifier until the value is restored. The
refusal records no closure. LIP-0010 section 6 already requires that every
consumer is upgraded before a name is rewritten.

Where each key is published follows from that:

| Key | LIP-0004 value, in use for v3 | After LIP-0010 readers are deployed | Authority |
| --- | --- | --- | --- |
| Name-owner key | Not in the value. It is the key of the name's output script. | The same | Controls updates and transfers of the name |
| Grant key | `swarma.landlord.grant` | The same | Signs grants |
| Principal's Nostr key | `nostr.names._` | `nostr`, as a key string or a NIP-05 object | None |
| Agent's Nostr key | `swarma.agent.nostr` and `nostr.names._`, which must be equal | `nostr` only | The agent's address; a grantee key only where a grant names it |
| Any further key or pointer of the owner | Nowhere: it refuses the whole value | A member outside `swarma`, which a Link reader ignores | None |
| Notary attestation key | Not in a principal's or an agent's name | The notary's own name, `swarma.notary.attest` (LIP-0010 section 9, proposed) | Signs attestations only |

**What a name change does to existing grants.** Grant v3 binds no owner key.
The owner-key binding is a rule of the v4 draft (LIP-0008 section 3).

| Change to a name | Effect on v3 grants (LIP-0004 section 5) | Effect on v4 grants (LIP-0008 section 3, Draft) |
| --- | --- | --- |
| Transfer of a landlord name to a new owner, value unchanged | Nothing closes; the grants stay live | Every grant of that issuer refuses |
| Change of the grant key in `swarma.landlord.grant` | Every grant signed by the old key stops verifying. A verifier that had observed the old key records a durable closure; a verifier that had not refuses because the name's current key did not sign the grant. Old seals can still be spent only by the old key | Every grant of that issuer refuses |
| Change of a principal's Nostr key | No closure | No closure |
| Change of an agent's Nostr key | No closure of grants whose executor is that agent. A grant that names the old key as grantee no longer admits the agent and is issued again | A grantee bound by name keeps its grants |
| Change of an agent's landlord pointer | Every grant whose executor is that agent closes, for a verifier that had observed the old pointer; a verifier that had not refuses because the agent no longer points to the landlord the grant names | The pointer no longer binds the grant's issuer, and the grant refuses |
| Any added member | Every grant under that name refuses, without closure, until the exact value is restored | Outside `swarma`: nothing. Inside `swarma`: every grant of that issuer refuses |
| Renewal, same value and same owner | Nothing | Nothing |

Two consequences follow for a v3 deployment. An issuer that plans to replace
its grant key does so before it issues the grants it wants to keep. And a
party that obtains a name-owner key can transfer a v3 landlord name without
closing a grant: a v3 verifier notices only a later change of the grant key.
On v3 the defence is custody of the name-owner key and verifiers that keep
their journals.

**No agent grant keys on v3.** A v3 grant is valid only under the landlord's
grant key (LIP-0004 section 2), and an agent's value has no grant member. In
Goal 1 no agent therefore holds a grant key. A child grant is issued by the
landlord's signer on the delegator's signed request (LIP-0014 section 5). A
notary holds an attestation key, which signs no grant.

**The landlord pointer is a name on v3.** The agent's value names its
landlord by `id/` name, and a v3 verifier pins the network, the genesis, the
agent name, the landlord name and the seal script. The landlord's key is
what that name's current value says. Binding the pointer to the issuer's
registration and owner key is a rule of the v4 draft. A key fingerprint
cannot be added to a v3 agent value, by the first clarification.

## Requirements on a key service

K1 gives the grant key to a service that signs for its holder. Three
requirements follow from the formats that key signs. They concern a
principal's own key service, as used for the trust grants of LIP-0013. An
operator's signer that issues rental grants without a person is bounded by
its operator ceilings instead (LIP-0006).

1. **A grant-key purpose of its own on secp256k1,** separate from the Nostr
   key and from funding keys. It signs grants under BIP-340. On v3 it also
   spends seals under ECDSA, because a v3 seal pays the grant key (LIP-0004
   section 5). LIP-0008 section 11.1 states the risk of one secret under two
   schemes; until v4 separates them, BIP-340 uses fresh auxiliary randomness
   and ECDSA uses RFC 6979.
2. **Presence per signature.** The holder confirms each signature of the
   grant key. The same holds for any key that a grant names as grantee,
   before the executors that admit it enter enforcing mode (LIP-0013 section
   3.4): a key that signs without its holder can be used by any process of
   the same OS user.
3. **Typed display.** The service parses the object it is asked to sign,
   shows its fields, and computes the hash itself. It signs no digest that a
   caller supplies. LIP-0008 section 8 requires this of a v4 signer; for v3
   it covers the grant, the contract hash that `landlord_sig` signs, and the
   terms of a child grant (LIP-0014 section 5).

The keyvault interface was read on 2026-11-12 at two revisions. At
[`swarma-keyvault` `41e0c71`](https://github.com/relux-works/swarma-keyvault/tree/41e0c71b0ddb2a102ae5dbc0184c60dfc10f3819)
its recovery command derives two purposes from one mnemonic, a Nostr leaf
without presence and a Namecoin account, and its documentation states that
it implements no address registration, transaction signing or broadcasting
(`docs/recovery.md`). Its Nostr signing command takes a 32-byte digest and
does not hash input again (`docs/nostr.md`).

At [`662623f9`](https://github.com/relux-works/swarma-keyvault/tree/662623f94494df9a8c1f14a552da51d248ff4f79)
it prepares a third purpose, the landlord's grant root
(`internal/keyvault/recovery_root_grants.go`): profile
`namecoin-landlord-root/1`, derived by BIP-85 at the fixed path
`m/83696968'/2'/7'`, one secp256k1 key for BIP-340 and ECDSA together with
the P2PKH seal script of that key. The source states that this is public
preparation data only and conveys no storage, owner enrollment, presence or
signing capability. That path governs where the grant key comes from.

So the first requirement has its derivation. Signing a grant, the ECDSA
seal spend, presence per signature and typed display are later stages of
that interface. A name whose owner key the interface holds cannot be updated
until it signs name operations.

The profile fixes one path per recovery group, so a grant key is replaced by
a new recovery group with new words. The name-owner key publishes the new
key by an update of `swarma.landlord.grant`, and the old group keeps the old
key until it has spent the seals of the old grants. The owners accept this
for v3, where a change of the grant key ends every grant of the old key in
any case.
