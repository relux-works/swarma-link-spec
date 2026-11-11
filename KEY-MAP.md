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
key signs no grant.

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
