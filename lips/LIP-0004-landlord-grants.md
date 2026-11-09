# LIP-0004: Landlord grants with an on-chain consent commitment

- **Status:** Draft
- **Created:** 2026-11-08
- **Affects:** names, issuance, observation, revocation; builds on LIP-0003
- **Motivation:** an agent holds no grant key; the party that rents the agent out (its **landlord**) signs grants; both
  sides' consent is a signature, and what goes on chain is fixed and known to both in advance.
- **Terms:** *grant* (the signed document), *contract* (the terms both sides sign), *seal* (the output whose spend ends
  the grant early). The word "certificate" is not used.

## 1. Names

```json
{"swarma":{"landlord":{"grant":"<x-only grant key>"}}}
{"swarma":{"agent":{"nostr":"<x-only messaging key>","landlord":"<landlord name>"}}}
```

- The landlord name holds the **grant key**; it is owned by a cold key. The agent name holds only its messaging key
  and a pointer to its landlord name. A landlord may be the operator who owns the agent or a company.
- Exact shapes: missing, aliased, extra, duplicate, reordered or malformed fields refuse.

## 2. Grant v3

Canonical compact JSON in this field order: `version` (3), `network`, `genesis`, `agent_name`, `landlord_name`,
`issuer_key`, `grantee_key`, optional `grantee_name`, `contract_sha256`, `scope`, `not_before`, `not_after`,
`seal {txid, vout}`, optional `budget`, `consent`.

- Signature: BIP-340 by the landlord's grant key over `SHA-256("swarma-grant-v3" || canonical grant bytes)`; no
  untagged form is accepted.
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

Raw bytes, no lengths or separators. The issuance transaction has exactly one zero-value `OP_RETURN` output carrying
the commitment (encoding per LIP-0005; the first implementation uses the bare `6a20<commitment>` form). The seal is not
an input of that transaction. The verifier fetches the transaction named by the locator on its own node and requires
it to be confirmed in the active chain. Before the renter signs, they know the formula and their own inputs; the final
commitment depends on the landlord's countersignature and the grant id and is checkable after issuance.

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

## 7. Relation to LIP-0003

LIP-0003's detached grant moves its signing key from the agent name to the landlord name, gains the consent object and
the mandatory per-grant commitment. LIP-0003's batch anchor stays optional and never replaces the per-grant commitment.

## 8. Evidence

A regtest implementation with genuine Namecoin Core 28 suites (lifecycle, landlord rotation, issuer crash boundaries,
funding separation, legacy replay) and independent review exists in the reference laboratory.
