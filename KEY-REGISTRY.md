# Key registry

- **Status:** Draft. Recorded on 2026-11-14 at Ivan Oparin's direction; the
  co-author's agreement is pending.
- **Covers:** every key that this specification names

A key that is listed nowhere has no stated owner, no stated holder and no
stated stop, and a reader cannot tell what its leak costs. The parts of
this specification name each key where they first need it. The table of the
[key map](KEY-MAP.md) covers the rental and wallet profiles and says itself
that the notary's two keys are not in it, and the keys that the v4 drafts
add appear only in the LIP that needs each.

This registry is that list. For every key it states whose key it is, where
its public half is published, who holds the secret, what it signs, how
dangerous a leak is, what a thief can do with it, and how its owner
recovers.

## Rules

1. **One entry for every key.** Every key that a part of this specification
   names has exactly one entry here. A revision that introduces a key MUST
   add its entry in the same revision. A key without an entry has no role in
   the protocol.
2. **A closed list of uses.** The line "Signs" of an entry lists every
   object that a part of this specification defines for the key, and it
   marks an object that a Draft only proposes. The holder MUST NOT use the
   key for an object that no part of this specification defines for it.
   Where a part defines a use that an entry omits, the part holds, and the
   entry is a defect to be corrected.
3. **The messaging key never grants authority.** A key that carries messages
   signs no grant, on Grant v3 and on v4. Ivan Oparin decided this on
   2026-11-14, together with a separate delegation key for child grants on
   v4; the co-author's agreement is pending. LIP-0014 section 11.1
   holds the rule. Until the co-author agrees, LIP-0008 section 12.6 states
   the rule in force, under which the parent's recipient key signs a child.
4. **An entry has the status of its source.** Each entry names the part
   that defines its key and has the status of that part: the normative v0.1
   profile, an implemented profile that a Draft LIP describes, a Draft
   proposal, or a decision that waits for the co-author. The registry makes
   no Draft rule normative. Once the co-author agrees, rules 1 to 3 bind
   every later revision.

The words of an entry:

| Line | Meaning |
| --- | --- |
| Owner | The party whose key it is. The owner decides when the key is created and replaced. |
| Published | Where a verifier finds the public half or a pin of it. |
| Holder | The service, device or person that keeps the secret and makes the signatures. A holder may differ from the owner. |
| Signs | Every object the key signs. Rule 2 makes the list complete. |
| Danger | The level of the table below. |
| Leak | What a party that obtains the secret can do, and what it cannot. |
| Recovery | What the owner does after a leak, and what is lost for good. |
| Source | The part that defines the key, and its status. |

## Danger levels

A level says what a leak lets another party do and what stops it. It
belongs to a key with all its uses: a key that several grants name is
exposed in all of them, and nothing in Grant v3 gives a recipient a key of
its own for each grant. Where two descriptions fit a key, the higher level
holds, and where a level depends on a condition the entry and the index
name it. The coin of a seal or of a row is a marker, and its amount raises
no level. Like the rest of the registry the levels are the draft's proposal
and wait for the owners' confirmation.

| Level | A leak lets another party | Stop |
| --- | --- | --- |
| critical | Take over an identity, or sign in its name without a bound: move a name, issue any grant of an issuer. | None that reaches everything the thief signed or moved. The owner rebuilds the identity or reissues every grant. |
| high | Use authority, or pass it on, inside signed bounds, under every grant or parent that names the key; or spend a balance that the key holds as money. | A stop exists that every verifier sees on its own node, such as a seal spend or a name update. For money the balance bounds the loss. |
| medium | End authority early, or forge a record that gives no authority by itself: a withdrawal, a receipt, a verdict, an offer. It uses no authority and creates none. | What can be ended or disputed bounds the damage, and the key is replaced. |
| low | Impersonate an endpoint or a device, or read traffic or stored data. The key carries no authority and controls no money. | New keys and new pins. |

## Index

| Key | Danger | Source and status |
| --- | --- | --- |
| Name-owner key | critical | LIP-0004, in use on v3; pinned by the v4 draft (LIP-0008) |
| Grant key | critical | LIP-0004, in use on v3; v4 draft (LIP-0008) |
| Funding key | high | LIP-0004, in use on v3 |
| Seal keys, v4 | medium | LIP-0008 sections 11 and 11.1, Draft |
| Single-use seal key, issuer branch | medium | LIP-0002 and LIP-0006; the v4 profile is open |
| Single-use seal key, grantee branch | high | LIP-0002 and LIP-0006; the v4 profile is open |
| Provider key | medium | Key map, in use in the rental profile |
| Principal's Nostr key | low; high where a grant names it as grantee | LIP-0004 and LIP-0010, in use on v3 |
| Authority key of a person | high | Key map, K6; decision of 2026-11-14, agreement pending |
| Agent's Nostr key | high | LIP-0004 and LIP-0010, in use on v3 |
| Renter key | high | LIP-0004, in use in the rental profile |
| Wallet client action key | high | LIP-0006 sections 1 and 2, implemented in the wallet service v1 profile |
| Delegation key, v4 | high | LIP-0014 section 11.1; decision of 2026-11-14, agreement pending |
| Row coin key, v4 | medium | LIP-0014 section 9.1; decision of 2026-11-14, agreement pending |
| Child-seal key, v4, optional | medium | LIP-0014 section 11.1; decision of 2026-11-14: a profile option, not in the first version |
| Notary attestation key | high | LIP-0012 and LIP-0014, Draft |
| Notary seal key | medium | LIP-0012 and LIP-0014, Draft |
| Row stop key, v4 | medium | LIP-0014 section 10.1; decision of 2026-11-14, agreement pending |
| Receipt key | medium | LIP-0006, implemented in the wallet service v1 profile |
| Wallet money keys | high | LIP-0006 and the key map, in use |
| Agent-controlled wallet key | high | LIP-0006, security consequences; its provisioning is open |
| Moderator key | medium | LIP-0011, Draft |
| Transport keys | low | Key map, in use in the rental profile |
| Model bearer of a slot | high | Key map, in use in the rental profile |
| Upstream API secret of the model proxy | high | Key map and LIP-0008 section 2, in use in the rental profile |
| Keys bound by a certificate statement | low | LIP-0015 section 6, a proposal |
| Holder's blob decryption keys | low | LIP-0009, a proposal; custody is open |
| Owner key, v0.1 | medium | Normative v0.1 profile, frozen as historical |
| Requester key, v0.1 | high | Normative v0.1 profile, frozen as historical |

## Names and issuance

**Name-owner key**

- Owner: the party that owns the name. For a landlord name that is the
  principal, for an agent's name the agent's operator (key map, K2), for a
  notary's name the notary.
- Published: not in the name's value. It is the key of the name's output
  script, which the chain shows. A v4 grant pins it for its issuer and for
  a recipient by name (LIP-0008 sections 3 and 3.1).
- Holder: the owner alone, in cold custody (LIP-0008 section 11.1). The key
  map proposes a seed of its own for it and never an agent host.
- Signs: name operations, which are updates, renewals and transfers of the
  name. In the v0.1 profile the seal pays the address that holds the owner
  name, so there the same key also spends the seal.
- Danger: critical.
- Leak: the thief moves the name or rewrites its value, and with the value
  the grant key, the agent key or the attestation key that the name
  publishes. A v3 landlord name can be transferred without closing a grant.
  On v4 a changed owner or a changed `swarma` refuses every grant of that
  issuer.
- Recovery: none for a name that was moved; losing the owner key loses the
  name (LIP-0008 section 3.1). The owner registers a new name, issues its
  grants again and replaces the pins that name the old one.
- Source: LIP-0004 section 1, in use on v3; LIP-0008 section 3, Draft.

**Grant key**

- Owner: the principal whose landlord name publishes it.
- Published: `swarma.landlord.grant` in the landlord name (LIP-0004 section
  1, LIP-0010).
- Holder: a key service of the principal that asks for the holder's
  presence at each signature and shows every signed field first (key map,
  requirements on a key service). By decision K5 the interim holder on a
  Mac is the macOS Keychain, read under Touch ID. An operator's signer that
  issues rental grants without a person is bounded by its operator
  ceilings instead.
- Signs: grants, on v3 under `swarma-grant-v3` and on v4 under the typed
  digest that LIP-0008 section 8 plans; `landlord_sig`, the raw contract
  hash of the consent; on v3 the spend of every seal, because a v3 seal
  pays this key; on v4 the endorsement of each seal key (LIP-0008 section
  11) and no transaction. Proposed by LIP-0015 and LIP-0016: configuration
  statements, root rotation statements, certificate statements and
  certificate set heads, each under its own signing domain. No message and
  no name operation.
- Danger: critical.
- Leak: the thief issues grants in the principal's name and, on v3, spends
  the seals of that key. Under LIP-0015 it would also sign configuration
  and bind other keys to the name.
- Recovery: the name-owner key publishes a new grant key by a name update.
  On v3 that ends every grant the old key signed, and the old key is kept
  until it has spent the seals of those grants. On v4 every grant of the
  issuer refuses. All of them are issued again. The stop is slower and
  less final than a seal spend, which LIP-0008 records as an open
  question.
- Source: LIP-0004 sections 1 to 3, in use on v3; LIP-0008, Draft. The
  detached grants of LIP-0003 kept this key in the agent's name; LIP-0004
  moved it to the landlord name.

**Funding key**

- Owner: the issuer.
- Published: nowhere by the protocol. The issuer pins the funding script in
  its own configuration (LIP-0004 section 6).
- Holder: the issuer's signer.
- Signs: the inputs that pay fees and refill the seal pool. It never signs
  an input at the seal script.
- Danger: high.
- Leak: the thief takes the funding outputs. It cannot spend a seal and
  cannot sign a grant.
- Recovery: a new script, the remaining funds moved to it, and the
  accounting reconciled.
- Source: LIP-0004 section 6, in use on v3.

**Seal keys, v4**

- Owner: the issuer of the sealed grant.
- Published: in no name. The issuer's typed endorsement, signed by the
  grant key, binds the public key and the exact script to the seal's
  outpoint (LIP-0008 section 11).
- Holder: the issuer's signer. The keys are derived under BIP-32 in an
  account that holds only seal keys, one key for each seal. The account's
  extended public key is a secret of the operator.
- Signs: the spend of its one seal, which revokes that grant. The entry
  covers the revocable-only seal.
- Danger: medium.
- Leak: the thief spends that seal, which closes the grant early and takes
  the seal amount. With the account's extended public key and one seal's
  private key it computes every seal key of the account. It cannot sign a
  grant or an endorsement, move a name or spend funding outputs.
- Recovery: the closed grants are issued again with new seals. After a
  leak of the extended public key the issuer moves to a new seal account
  or to hardened indices.
- Source: LIP-0008 sections 11 and 11.1, Draft; the derivation is Ivan
  Oparin's decision of 2026-11-11. On v3 no separate seal key exists: the
  seal pays the grant key.

**Single-use seal key, issuer branch**

- Owner: the issuer of the single-use grant.
- Published: in no name. The operator pins the chain keys of the seal
  (LIP-0002).
- Holder: the issuer's signer.
- Signs: the revocation spend of the single-use seal.
- Danger: medium.
- Leak: the thief revokes the single-use grants whose seals name the key.
  It cannot use them.
- Recovery: new grants with seals under a new key.
- Source: LIP-0002, a working design on regtest; LIP-0006 for the wallet
  service. The v4 output profile of this seal, and the source of this key
  on v4, are open (LIP-0008 section 11.1).

**Single-use seal key, grantee branch**

- Owner: the grantee of the single-use grant.
- Published: in no name. The operator pins the chain keys of the seal
  (LIP-0002).
- Holder: the grantee's client.
- Signs: the use spend of the seal, which commits to the hash of one
  request.
- Danger: high.
- Leak: the thief takes the seal value and uses, once each, every
  single-use grant whose seal names the key, inside each grant's limits,
  its window and the service's peer admission.
- Recovery: the issuer revokes those grants by the issuer branch and
  issues new ones with seals under a new key.
- Source: LIP-0002, a working design on regtest; LIP-0006 for the wallet
  service. LIP-0006 does not say whether this is the secret of the wallet
  client's action key. The v4 output profile of this seal is open.

**Provider key**

- Owner: the provider that offers a booking.
- Published: as a pin at the parties that check the package.
- Holder: the booking service.
- Signs: the contract hash and the kind-8182 package of a booking.
- Danger: medium.
- Leak: the thief forges offers. Consent and issuance are checked
  separately, so a forged offer alone issues no grant.
- Recovery: a new key and a new pin; packages under the old pin refuse.
- Source: key map, in use in the rental profile.

## Recipients

A grantee key is whichever key a grant names as its recipient: `grantee_key`
on v3, and on v4 the request key of a recipient by key or the channel key
that a recipient's name yields (LIP-0008 section 3.1). The five entries
below are the keys that play that part.

On v4 a recipient also signs its assent to the contract of a grant
(LIP-0008 sections 1 and 8); the bytes of that object are open.

LIP-0009 proposes two further signed objects for a key that holds an
account at a replaceable service: the consent to a migration, and a BUD-11
endpoint token of kind 24242 for a blob store. Both are proposals whose
signing domains are open, and a key signs them only where that profile
names it as the holder or as the channel key.

**Principal's Nostr key**

- Owner: the principal.
- Published: `nostr.names._` in the principal's name; `nostr` once LIP-0010
  readers are deployed.
- Holder: the principal's own client or key service.
- Signs: the principal's messages. It signs no grant (rule 3). The key
  map's proposed layout also uses it as the grantee key of Goal 1; where a
  grant names it so, it signs what the authority key below signs, and its
  level is that key's.
- Danger: low; high where a grant names it as grantee.
- Leak: the thief reads the principal's messages and writes in the
  principal's name. No authority follows: a peer message is data until a
  signed envelope under a grant is admitted (LIP-0013 section 3.4).
- Recovery: a name update with a new key, and new pins at the contacts. No
  grant closes by that update. Where a grant names the old key as grantee,
  the recovery of the authority key applies as well: the issuer revokes
  that grant before it issues a new one.
- Source: LIP-0004 section 1 and LIP-0010, in use on v3.

**Authority key of a person**

- Owner: a person who receives grants.
- Published: in no name. Each grant to the person names the key directly,
  as `grantee_key` on v3 and as the request key of a recipient by key on
  v4. The person's name keeps the Nostr key for messages.
- Holder: the person's key service, with presence at each signature and
  the signed fields shown first. For the interim the key is a software
  secp256k1 item in the macOS Keychain, read under Touch ID, like the grant
  key under K5. A signer that shows the fields of a kind-8181 consent and
  of a kind-8185 envelope is needed for it.
- Signs: what a grantee signs: the kind-8181 consent to a grant, kind-8185
  instruction envelopes, a kind-8186 delegation request, and v4
  invocations. No message and no grant.
- Danger: high.
- Leak: the thief acts under every grant issued to the key, inside each
  grant's limits, at every executor that admits it.
- Recovery: the issuer of each such grant revokes it by spending its seal
  and checks that the spend is seen. Only then is the leak stopped, and a
  new grant goes to a new key. A new grant alone closes nothing: the old
  one admits the old key until its seal is spent or its window ends.
- Source: key map, decision K6: Ivan Oparin's decision of 2026-11-14 for
  grants issued to him; the co-author's agreement is pending. The decision
  rejects the other reading, an authority key written into the name in
  place of the Nostr key.

**Agent's Nostr key**

- Owner: the agent's operator, who owns the agent's name (key map, K2).
- Published: `swarma.agent.nostr` and `nostr.names._` in the agent's name,
  which must be equal on v3; `nostr` alone once LIP-0010 readers are
  deployed.
- Holder: the gateway of the agent's host, under its own OS user. The key
  map proposes that the key is generated on that host and never leaves it;
  that flow is not decided. No person is present at its signatures. Ivan
  Oparin decided on 2026-11-14 that for an agent's key a gate at the key
  holder, which checks each run, takes the place of presence (LIP-0013
  section 3.6).
- Signs: the agent's messages; and, where a grant names the key as grantee
  or names the agent as a recipient by name: the kind-8181 consent,
  kind-8185 instruction envelopes, a kind-8186 delegation request, and v4
  invocations. It signs no grant (rule 3).
- Danger: high.
- Leak: the thief reads and writes the agent's messages and acts under
  every grant issued to the key or to the agent's name, inside each
  grant's limits.
- Recovery: the operator updates the name with a new key. For a grant that
  names the old key directly, on v3 and for a v4 recipient by key, that
  update closes nothing: the issuer of each such grant revokes it by
  spending its seal, checks that the spend is seen, and then issues a new
  grant to the new key. For a v4 recipient by name the update is enough,
  because the request key is read from the name at every admission. Grants
  whose executor is the agent are not affected by a change of its
  messaging key.
- Source: LIP-0004 section 1 and LIP-0010, in use on v3.

**Renter key**

- Owner: the renter.
- Published: in the grant, as `grantee_key`. No name is required.
- Holder: the renter's device, for example a browser signer.
- Signs: the kind-8181 consent to the rental and the renter's messages to
  the rented agent.
- Danger: high.
- Leak: the thief acts as the renter under every grant that names the key,
  inside each grant's limits and window. Grant v3 does not give a renter a
  key of its own for each rental.
- Recovery: the renter tells its contacts. The issuer of each grant that
  names the key revokes it by spending its seal, and then issues it again
  to a new key.
- Source: LIP-0004 section 3 and the key map, in use in the rental profile.

**Wallet client action key**

- Owner: the party that the wallet grants are issued to, which is an agent
  or its operator.
- Published: in no name. One instance of the wallet service pins it as its
  one grantee key, and each request names it (LIP-0006 sections 1 and 2).
- Holder: the client of the wallet service, which is the agent's own
  process.
- Signs: the action requests of the wallet service v1 profile, under the
  domain `swarma-action-v1`: `spend` and `budget` under a grant, and the
  actions `balance`, `history` and `receive`, which need no grant.
- Danger: high.
- Leak: the thief asks for spends inside the budgets of the wallet grants
  that name the key. The service also checks the kernel peer of the
  connection, so the key alone, used by another OS user, is refused.
- Recovery: the issuer revokes the wallet grants that name the key. The
  service instance gets a new grantee key in its configuration, and new
  grants name that key.
- Source: LIP-0006 sections 1 to 4, implemented in the wallet service v1
  profile.

## Re-delegation and the notary

Four of these keys follow Ivan Oparin's decisions of 2026-11-14 for v4, and
the co-author's agreement on them is pending. LIP-0014 holds their rules:
section 9.1 for rows and the coin of a row, section 10.1 for the stop coin,
and section 11.1 for the delegation key and the child-seal key.

These entries speak of rows. A parent grant signs one row for each child it
permits, and a row fixes the executor, the grantee, the cap and the notary
of that child.

**Delegation key, v4**

- Owner: the re-delegating side, which is the party that consented to the
  parent grant as its recipient.
- Published: in the parent grant, which names one delegation key. It is in
  no name.
- Holder: a signing service of that party's operator, apart from the
  service that holds the messaging key. It signs without a person. What it
  can sign is bounded by the rows of the parent, by the notary and by the
  coins of each row.
- Signs: the child grants of that one parent and nothing else. It differs
  from every other key on the path.
- Danger: high.
- Leak: the thief signs children under that parent, inside the rows that
  the principal signed. A child still needs its attestation.
- Recovery: a new parent grant with a new key. Until then the principal
  can spend the parent's seal, and the notary can refuse or withdraw.
- Source: LIP-0014 section 11.1; decision of 2026-11-14, agreement
  pending. A sketch that is not decided derives the key for each parent
  from the seed of the operator's signer, as seal keys are derived.

**Row coin key, v4**

- Owner: the re-delegating side.
- Published: in the parent grant. Each row of the parent pins one confirmed
  coin, and the issuance of the row's child must spend it.
- Holder: the signer of the re-delegating side. Which key of that side the
  coin pays is fixed with the v4 bytes.
- Signs: the input that spends the row's coin in the issuance of that row's
  child.
- Danger: medium.
- Leak: the thief spends the coin outside an issuance, after which no child
  can be issued for that row. It issues nothing: a child also needs the
  delegation key.
- Recovery: a new parent grant; rows are fixed when a parent is issued.
- Source: LIP-0014 section 9.1, rule J1.9; decision of 2026-11-14,
  agreement pending. One child for each row then holds on the active chain
  and not across forks, which the decision accepts.

**Child-seal key, v4, optional**

- Owner: the re-delegating side.
- Published: in the parent grant, which would name the key that every
  child's seal pays.
- Holder: the operator of the re-delegating side, apart from the
  delegation signer.
- Signs: the spend of a child's seal, which revokes that child.
- Danger: medium.
- Leak: the thief revokes children of that parent early. It creates no
  authority.
- Recovery: a new parent grant.
- Source: LIP-0014 section 11.1; decision of 2026-11-14: a profile option,
  not part of the first v4 version. Without it the operator has no seal to
  spend for a child that a thief of the delegation key signed.

**Notary attestation key**

- Owner: the notary, an agent or a person.
- Published: `swarma.notary.attest` in the notary's own `id/` name
  (LIP-0010 section 9, proposed).
- Holder: a key service that signs on request and does not export the key.
  On a host without one, a file under a separate OS user is an exception
  that each owner approves (LIP-0014 section 6.3).
- Signs: attestations of profile `swarma-notary-attestation/1`, under the
  domain `swarma-notary-v1`. No grant.
- Danger: high.
- Leak: the thief certifies children. It cannot widen an action set, a
  repository list, a window or a child's own budget, because every
  verifier checks those itself. Under the text in force it can certify a
  child that exceeds its parent in words, and its attestations carry the
  sum of the siblings' budgets, which no verifier sees. Under LIP-0014
  sections 3.4 and 9.1 a child of profile `/2` has no text of its own, and
  rows replace that sum.
- Recovery: the notary's name-owner key publishes a new attestation key.
  Every attestation under the old key then refuses, and the notary signs
  again under the new one. No grant is reissued.
- Source: LIP-0012 and LIP-0014 sections 6 and 7, Draft; the designation is
  the owners' decision D3 of 2026-11-12.

**Notary seal key**

- Owner: the notary.
- Published: in no name. Each attestation names the outpoint and the script
  of the seal it depends on.
- Holder: the notary. The key is distinct from the attestation key
  (LIP-0014 section 6.3).
- Signs: the spend of a notary seal, which withdraws every attestation that
  names it; with an action `0x05` frame the withdrawal is for cause.
- Danger: medium.
- Leak: the thief withdraws attestations, and the children they certify
  refuse. It certifies nothing. A withdrawal that carries the frame for
  cause is worse than a plain one: after it the same child may not be
  certified again (LIP-0014 section 10).
- Recovery: after a plain withdrawal the notary certifies the same child
  again with a new seal. After a withdrawal for cause the delegator asks
  for a new child.
- Source: LIP-0012 and LIP-0014 sections 6.4 and 10, Draft.

**Row stop key, v4**

- Owner: the notary of the row.
- Published: in the parent grant. Each row names one confirmed coin of its
  notary, the row's stop coin.
- Holder: the notary, for the life of the parent. The key is not the
  attestation key.
- Signs: the spend of the row's stop coin. That spend ends the row for
  cause for every verifier whose node shows it.
- Danger: medium.
- Leak: the thief ends rows, and an ended row stays ended. It creates no
  authority.
- Recovery: a new parent grant for the rows that were ended. A notary that
  loses the key, without a leak, can no longer end the row for cause.
- Source: LIP-0014 section 10.1, rule J2.7; decision of 2026-11-14 for v4
  from its first version, agreement pending.

## Services

**Receipt key**

- Owner: the operator of the service.
- Published: as a pin that the client holds independently of the service
  (LIP-0006 section 1). LIP-0007 proposes a declaration in the service's
  name, which alone is no trusted pin. On v4 the grant's executor binding
  names the service's name and public key (LIP-0008 section 4).
- Holder: the service, under its dedicated OS user. The service refuses a
  receipt key equal to the grantee key.
- Signs: the service's receipts, under the domain
  `swarma-action-receipt-v1`. Proposed by LIP-0009, with open domains:
  the closing statement of a provider when an account moves to another
  provider, and the acceptance of the provider that takes it over.
- Danger: medium.
- Leak: the thief forges receipts. It cannot spend coins with this key.
- Recovery: a new key, new pins at the clients and a migration of the
  service's state; the old journal refuses.
- Source: LIP-0006 sections 1 and 5, implemented in the wallet service v1
  profile.

**Wallet money keys**

- Owner: the operator of the wallet service.
- Published: nowhere by the protocol.
- Holder: the Namecoin Core wallet behind the service's private RPC,
  outside the client's reach.
- Signs: the coin transactions of the wallet.
- Danger: high.
- Leak: the thief takes the funds. Theft of these keys or of the RPC access
  bypasses the service's limits.
- Recovery: new addresses, the remaining funds moved, and new RPC access.
- Source: LIP-0006 and the key map, in use in the wallet profile.

**Agent-controlled wallet key**

- Owner: not fixed. LIP-0006 leaves the provisioning of this tier open.
- Published: nowhere by the protocol.
- Holder: the agent itself. This is the tier that the wallet service does
  not guard.
- Signs: the coin transactions of a small wallet that the agent controls.
- Danger: high.
- Leak: the thief spends the balance directly, and so can the agent. A
  grant at the wallet service can gate a refill and cannot restrict what
  the key spends afterwards.
- Recovery: no refill, the remaining balance moved, and a new key. The
  refill limits and the revocation of this tier are open.
- Source: LIP-0006, security consequences and open questions.

**Moderator key**

- Owner: the moderator that the contract names: the issuer's own service or
  another party.
- Published: in the contract, which both parties' consent covers.
- Holder: for a model, the service that runs the model and that service's
  operator; the model does not hold the key. For a person, that person.
- Signs: verdict records about violations.
- Danger: medium.
- Leak: the thief forges verdicts. It cannot spend a seal, so no grant
  closes by a forged verdict alone.
- Recovery: open. LIP-0011 leaves the replacement of the key during a
  contract to the contract.
- Source: LIP-0011, Draft.

**Transport keys**

- Owner: the operator of each endpoint.
- Published: as pins of TLS leaf certificates between the endpoints. The
  channel secret of a slot is shared by the two ends of that slot's
  channel and published nowhere.
- Holder: the endpoints. They hold TLS keys, the keys of mutual TLS between
  gateway and manager, and the channel secret of each slot.
- Signs: transport sessions. The channel secret signs nothing; it
  authenticates the messages of one slot's channel.
- Danger: low.
- Leak: the thief impersonates an endpoint to its peer. It gains no model
  access and no effect, because the grant checks stay separate.
- Recovery: new certificates and new pins. A channel secret ends with its
  slot.
- Source: key map, in use in the rental profile.

**Model bearer of a slot**

- Owner: the operator of the model proxy, which mints the bearer.
- Published: nowhere. The proxy gives it to the slot.
- Holder: the slot and the proxy.
- Signs: nothing. It is a shared secret that the proxy accepts as the
  slot's right to model access.
- Danger: high.
- Leak: whoever holds a copy uses the model access of that slot, from
  anywhere, inside the slot's window and its limits. The bearer can be
  passed on, and its bounds do not make its use any less a use of what the
  slot was given.
- Recovery: the proxy revokes the binding, and a new slot gets a new
  bearer. A bearer ends with the window of its slot.
- Source: key map, in use in the rental profile.

**Upstream API secret of the model proxy**

- Owner: the operator of the model proxy, as the holder of the account at
  the upstream model service.
- Published: nowhere.
- Holder: the proxy alone. A slot never receives it; slots get bearers.
- Signs: nothing. It authenticates the proxy to the upstream service.
- Danger: high.
- Leak: the thief uses the upstream service on the operator's account,
  outside the window and the limits of every slot and outside the rental
  accounting. No limit of a grant or of a slot contains it; only the
  limits of the upstream account do.
- Recovery: the operator replaces the secret at the upstream service and
  gives the new one to the proxy. New transport certificates and new
  bearers do not end the old secret. This specification defines no
  procedure for the replacement, and when the old secret stops working is
  a matter of the upstream service.
- Source: key map; LIP-0008 section 2 names the same bypass.

The three entries above differ in what a thief gains, and a deployment
that tests them keeps the three apart:

| Stolen | What the thief can do | What contains it |
| --- | --- | --- |
| A TLS key of one endpoint, and nothing else | Impersonate that endpoint to its peer | The grant checks, which the key does not touch; new certificates and pins |
| The bearer of a live slot | Use that slot's model access from anywhere | The slot's window and limits, and the proxy's revocation of the binding |
| The upstream API secret | Use the upstream service outside every slot | Nothing of this protocol; the upstream account's own limits, and the replacement of the secret there |

## Keys bound to a name

**Keys bound by a certificate statement**

- Owner: the operator of the name that binds them.
- Published: in certificate statements of profile `swarma-cert-statement/1`,
  in the certificate store of LIP-0016, and never in a name value. The
  kinds are `matrix-device`, `matrix-cross-signing`, `git-signing-ssh` and
  `release-key`.
- Holder: the device or the tool that uses the key.
- Signs: what its own system defines, such as transport messages or
  commits. It signs nothing of this protocol.
- Danger: low.
- Leak: the thief acts as that device or signs commits as it until the
  binding is revoked. A certificate is a binding and no authority: a
  message from a certified device stays data until a grant check admits
  it.
- Recovery: a later statement for the same subject that ends the binding.
- Source: LIP-0015 section 6 and LIP-0016, proposals.

## Keys that sign nothing

**Holder's blob decryption keys**

- Owner: the holder of the blobs.
- Published: nowhere.
- Holder: the holder. LIP-0009 says that these keys need not be given to
  either provider when an account moves; where and how the holder keeps
  them is open.
- Signs: nothing. The keys decrypt the holder's private blobs.
- Danger: low.
- Leak: the thief reads the holder's private blobs, once it also has the
  blobs. No authority follows.
- Recovery: the blobs encrypted again under new keys. LIP-0009 leaves the
  encryption of private data and the rotation of its keys open.
- Source: LIP-0009, a proposal.

## The historical v0.1 profile

**Owner key, v0.1**

- Owner: the issuer.
- Published: `swarma.keyvault_owner_spki` in the owner name, a P-256 key
  ([names](protocol/names.md) section 2).
- Holder: the issuer's own custodian. The grant envelope and its signing
  belong to keyvault and are outside this specification.
- Signs: the grant envelope.
- Danger: medium.
- Leak: the thief signs envelopes, and none of them counts until the owner
  name's value carries its hash, which needs the name-owner key.
- Recovery: a name update with a new key, and new grants.
- Source: [names](protocol/names.md) and
  [observation](protocol/observation.md), the normative v0.1 profile,
  frozen as historical.

**Requester key, v0.1**

- Owner: the grantee.
- Published: `swarma.keyvault_requester_spki` in the requester name, a
  P-256 key ([names](protocol/names.md) section 2).
- Holder: the grantee's own custodian.
- Signs: the requests under a grant.
- Danger: high.
- Leak: the thief acts under every grant that an owner name has issued to
  that requester key, until each is revoked. The profile does not limit a
  requester key to one grant.
- Recovery: the issuers revoke those grants by spending their seals. The
  grantee updates its name with a new key and receives new grants.
- Source: [names](protocol/names.md) and
  [observation](protocol/observation.md), the normative v0.1 profile,
  frozen as historical.

## Open points

- Which key of the re-delegating side the coin of a row pays (LIP-0014
  section 9.1). The delegation key signs child grants and nothing else, so
  the coin needs another key of that side, or that rule changes. It is
  fixed with the v4 bytes.
- The key that controls the output of a certificate set head. LIP-0016
  names the output and no key for it.
- The source of the issuer's key of a v4 single-use seal (LIP-0008 section
  11.1).
- The replacement of a moderator key during a contract (LIP-0011).
- Whether the key that signs the use spend of a single-use seal is the
  secret of the wallet client's action key. LIP-0006 does not say.
- The custody of a holder's blob decryption keys (LIP-0009), and the
  provisioning, the refill limits and the revocation of a wallet that an
  agent controls (LIP-0006).
- The signing domains of the two objects that LIP-0009 proposes for a
  holder's key, and of a provider's closing statement.
- The danger levels, which wait for the owners' confirmation.
