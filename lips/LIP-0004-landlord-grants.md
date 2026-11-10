# LIP-0004: Landlord grants with an on-chain consent commitment

- **Status:** Draft
- **Created:** 2026-11-08
- **Affects:** names, issuance, observation, revocation; builds on LIP-0003
- **Motivation:** an agent holds no grant key; the party that rents the agent out (its **landlord**) signs grants; both
  sides' consent is a signature, and what goes on chain is fixed and known to both in advance.
- **Terms:** *grant* (the signed document), *contract* (the terms both sides sign), *seal* (the output whose spend ends
  the grant early). The word "certificate" is not used.

## Current state and profile boundary

This draft describes the landlord implementation profile in
[`swarma-chain-lab` at `11084e3a31175907e77644a7596e7802283e7c1e`](https://github.com/relux-works/swarma-chain-lab/tree/11084e3a31175907e77644a7596e7802283e7c1e/experiments/rental),
including its strict name parser and framed issuance writer. It does not replace
the normative v0.1 name/envelope/anchor profile or adopt these draft requirements.
Implementation statements below are informative; adoption follows LIP-0001.

## 1. Names

Historical authority values remain accepted with identical builder bytes:

```json
{"swarma":{"landlord":{"grant":"<x-only grant key>"}}}
{"swarma":{"agent":{"nostr":"<x-only messaging key>","landlord":"<landlord name>"}}}
```

- The landlord name holds the **grant key**; it is owned by a cold key. The agent name holds only its messaging key
  and a pointer to its landlord name. A landlord may be the operator who owns the agent or a company.
- Authority comes from the pinned `id/` names, their bindings and the grant checks below.

### Optional social descriptor

The upgraded parser also accepts a typed root `nostr` member, before `swarma`:

```json
{"nostr":{"names":{"_":"<social key>"}},"swarma":{"landlord":{"grant":"<grant key>"}}}
{"nostr":{"names":{"_":"<agent key>"}},"swarma":{"agent":{"nostr":"<agent key>","landlord":"id/alice"}}}
```

These examples show field order with placeholders, not valid signable values.
Keys are lowercase 64-hex valid secp256k1 x-only public keys. The descriptor has
`names`, then optional `relays`. Here `names` has exactly one member, `_`.
When present, `relays` has exactly that social key as its map key and a nonempty
array of distinct absolute `ws` or `wss` URLs with hostnames. Userinfo and nonempty
fragments refuse; spelling is preserved and duplicates use exact string equality.
No relay is inferred, fetched or contacted by parsing this value.

For an agent, `nostr.names._` equals `swarma.agent.nostr`. A landlord's social key
is independent of its grant key: equality is permitted, never required or inferred.
An absent descriptor supplies no social identity. The social key and relay hints
do not issue grants, add scope or replace the authority binding. A valid social-only
update does not close a grant; observed authority changes still follow section 5.

Both historical and combined values require exact compact UTF-8 JSON bytes, with
the implementation's field/map order and escaping, no newline, and at most 520
bytes for the complete value. Missing required, aliased, extra, duplicate, null,
reordered or malformed fields refuse, including case-folded or escaped duplicate
names. Empty descriptors, scalar shorthand, delegated/imported maps and arbitrary
local-parts inside this `id/` descriptor are not accepted.

Upgrade all consumers before publishing combined values: older binaries reject
the new root member. This is a parser compatibility requirement, not evidence that
installed consumers were upgraded.

### Separate discovery record

The optional `d/` mirror is a separate local discovery profile, for example:

```json
{"nostr":{"names":{"_":"<landlord social key>","sonya":"<agent social key>"}}}
```

It contains exactly `nostr.names`, with sorted map keys; no `swarma`, relays,
wildcards, imports or delegation. `_` is the landlord root. Other labels use
1–63 lowercase ASCII letters/digits/hyphens, with no leading, trailing or repeated
hyphen. The landlord `id/<label>` determines `d/<label>`; agent `id/` names are
explicit inventory entries, not derived from their social labels. Agent labels
and names are unique, and their landlord pointers agree with that inventory.

The reference tool admits at most 32 agent entries before the final 520-byte
mirror limit and reports sorted missing, extra and mismatched labels. It neither
publishes names nor proves the inventory complete or fresh. A stale inventory
can produce a misleading match. A discovery record cannot replace an `id/`
authority value, and a combined authority value is not a discovery mirror.
Missing or stale discovery never grants, revokes, widens or gates authority.

## 2. Grant v3

Canonical compact JSON in this field order: `version` (3), `network`, `genesis`, `agent_name`, `landlord_name`,
`issuer_key`, `grantee_key`, optional `grantee_name`, `contract_sha256`, `scope`, `not_before`, `not_after`,
`seal {txid, vout}`, optional `budget`, `consent`.

- Signature: BIP-340 by the landlord's grant key over
  `SHA-256("swarma-grant-v3" || canonical grant bytes)`. The 15-byte ASCII prefix
  has no terminator, length or separator; this is a fixed protocol prefix,
  not the BIP-340 tagged-hash construction. A signature over the unprefixed
  grant hash is rejected.
- `grant_id` = SHA-256 of the canonical signed grant `{"grant":…,"signature":…}`.
- Presentation: `{"signed_grant": …, "issuance": {"txid": …}}`. The issuance locator is unsigned and outside the id.
- Scope: a sorted set from `deliver`, `names.register`, `pay`, `publish`, `repository.push`, `secret.release`; no
  wildcards. A grant with no budget has budget zero.

## 3. Consent

`consent` = {`contract_sha256`, `consent_event`, `landlord_sig`}.

- `consent_event` is the renter's signed Nostr event (kind 8181, empty content) with exactly the tags
  `["t","swarma-rental-consent-v1"]`, `["contract",<contract_sha256>]`, `["booking",<hash>]`,
  `["privacy",<hash>]`; its pubkey is the grantee key. A verifier recomputes the NIP-01 id and checks BIP-340 over it.
  This is how a browser renter signs (NIP-07 can only sign events).
- `landlord_sig`: BIP-340 by the grant key over the raw 32-byte contract hash.
- Consent may not come from the future at checking time nor at or after the grant's end.

## 4. On-chain commitment (mandatory, one per grant)

```
commitment = SHA-256( "swarma-issue-v1" || contract_sha256 || consent_event.id || consent_event.sig
                      || landlord_sig || grant_id )
```

Raw bytes, no lengths or separators: the 15-byte ASCII prefix is followed by
decoded fields of 32, 32, 64, 64 and 32 bytes respectively. ASCII hex spelling
does not replace the decoded bytes. The issuance transaction has exactly one
zero-value `OP_RETURN` output carrying the commitment. Fresh plans use the
72-byte LIP-0005 frame, action `0x01`, location `0x01`, pointer equal to `grant_id`:

```text
6a 03 53 4c 01 42 01 <commitment:32> 01 <grant_id:32>
```

The verifier also accepts the exact historical 34-byte
`6a20<commitment:32>` landlord form. Those 32 bytes are this section's issuance
commitment, which already binds `grant_id`; they are not silently reinterpreted
as the normative v0.1 envelope hash. Bare syntax alone does not identify a profile.
Malformed framing never falls back to the bare path. For framed landlord issuance,
generic parsing is insufficient: the action, blob location and exact grant ID
must match. A batch, torrent, no-locator or Memo output cannot substitute for it.
The verifier counts all `OP_RETURN` outputs; an additional one also refuses.

The seal is not an input of the issuance transaction. The verifier fetches the
transaction named by the unsigned issuance locator on its own node and requires
it to be confirmed in the active chain. Before the renter signs, they know the
formula and their own inputs; the final commitment depends on the landlord's
countersignature and the grant id and is checkable after issuance.

## 5. Checking

Live only if, on the verifier's own node: both names have the exact shapes, the agent points to the landlord named in
the grant, the landlord's grant key signed it; the commitment transaction is confirmed; the seal pays P2PKH to the
even-y compressed grant key, is confirmed and unspent (mempool included); the window is open; the presenter is the
grantee. The verifier pins network, genesis, agent name, landlord name and the seal script.

**Closures** (durable): a seal spend (mempool or block); a confirmed change of the landlord's grant key or of the
agent's landlord pointer, observed against a generation this verifier had seen. Pending changes, malformed values and
read failures refuse without closure. A return to the old key or pointer never reopens a closure. A first observer
cannot prove a change-and-return history it never saw.

## 6. Issuance and funding

- The issuer reserves the booking and the pool seal durably before any signature; a crash leaves an uncertain refusal,
  never a re-signed grant; one pool seal per grant, ever.
- **Funding never uses the seal script.** All funding inputs and change use a separate pinned funding script; any
  input at the seal script is refused, known or not. Pool refills and revocations return change to the funding script.
- Fresh funding projections include the 72-byte script before any reservation
  or signature; funds sufficient only for the old 34-byte output do not qualify.
- Completed-record replay preserves the whole stored plan, including fee,
  change and signed-size bound. The reference comparator accepts exact old
  regtest plans and exact framed plans, not mixed shapes or a migration to a new
  transaction. Its legacy projection is regtest-only; completed main records
  accept only exact framed plans. The fresh writer always uses framing.
- The V2 payment route, `IssueGrantWithNodes`, supports fresh main issuance
  preparation with explicitly pinned identity/payment network and genesis and
  a positive explicit fee rate. Shared funding-input checks precede replay
  lookup; fresh issuance then checks the framed fee projection before any
  reservation or signature. The result is a signed grant and an unsigned
  issuance plan, not a broadcast or a live grant. Separate transaction signing,
  broadcast and confirmed observation are still required.
- The v1 payment route, `IssueGrant`, remains regtest-only: main payment-package
  admission refuses with `ISSUER_POLICY`. Its shared funding preflight reaching
  an observation does not establish successful v1 main issuance.

## 7. Relation to LIP-0003

LIP-0003's detached grant moves its signing key from the agent name to the landlord name, gains the consent object and
the mandatory per-grant commitment. LIP-0003's batch anchor stays optional and never replaces the per-grant commitment.

## 8. Evidence

The pinned reference laboratory publishes genuine Namecoin Core 28 regtest
suites for lifecycle, landlord rotation, issuer crash boundaries, funding
separation and legacy replay, plus pure locator/name fixtures. See
`LIP-0004-PROFILE.md`, `N1-VALUES.md`, `grant_locator_test.go`,
`grant_locator_core_test.go`, `nostr_value_test.go` and `nostr_value_core_test.go`
there. Implementation support for explicit mainnet pins does not itself qualify
a deployment or extend the historical v0.1 mainnet conformance record.

Main-route regression coverage is defined in
[`main_issuance_test.go`](https://github.com/relux-works/swarma-chain-lab/blob/11084e3a31175907e77644a7596e7802283e7c1e/experiments/rental/main_issuance_test.go)
and
[`main_issuance_core_test.go`](https://github.com/relux-works/swarma-chain-lab/blob/11084e3a31175907e77644a7596e7802283e7c1e/experiments/rental/main_issuance_core_test.go).
The pure public-entry test checks funding refusals without burns beside a
funded control that reaches an offline observation boundary. The Core V2
witness uses isolated regtest identity and payment nodes, changes only their
chain/genesis replies, and re-signs the V2 terms for main. It checks a signed
framed grant, explicit fees, payment evidence and exact offline replay, with
wrong-chain refusals that leave no burns. A separate witness pairs v1 main
refusal with valid regtest preparation. These tests neither contact mainnet nor
broadcast the main-labelled plan, prove mainnet consensus or qualify a deployment.

## 9. Proposed successor

[LIP-0008](LIP-0008-grant-v4.md) proposes Grant v4 with directly signed rental
limits and a distinct name-bound recipient mode. V3's optional `grantee_name`
remains syntax-checked metadata; this cross-reference does not resolve it to
authority or change any v3 bytes, domains or acceptance rule.
