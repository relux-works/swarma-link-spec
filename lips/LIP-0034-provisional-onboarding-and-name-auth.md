# LIP-0034: Provisional onboarding and name authentication

- **LIP:** 0034
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Requires:** [LIP-0010](LIP-0010-name-value.md), [LIP-0020](LIP-0020-grant-v4-wire-registry.md), [LIP-0024](LIP-0024-seal-endorsement.md), [LIP-0029](LIP-0029-owner-control.md), [LIP-0033](LIP-0033-reference-distribution-for-pinned-lists.md)
- **Related:** [Names](../protocol/names.md), [LIP-0009](LIP-0009-replaceable-services.md), [LIP-0035](LIP-0035-unilateral-mandates.md)
- **Follows:** [LIP-0001](LIP-0001-link-improvement-proposals.md), [LIP-0018](LIP-0018-extension-guide.md)

## Summary and editorial resolution

A dedicated **auth key**, not a device, grant or cold name-owner key,
authenticates an owner to a foreign replaceable service. A new user starts
with a restricted key-only account and promotes it after client-owned
name registration. Authentication gives no EFFECT or disclosure authority.

The Swarma Link editor's resolution adopts the owner's v0.3 draft,
2026-11-20: BIP-340 auth objects replace the earlier proposed device-signed
envelope response. It preserves the binding card decision's premise:
"LIP-0029 O3.7/O4.6 stay intact (device keys never face foreign verifiers)"
(`$LGvz_xrefHjg61tvoQgu5D4Dew_A_vZlfo09ay__PbQ`). This is an editorial
resolution, not a new owner decision. The co-author's agreement is pending.

MUST, MUST NOT, SHOULD and MAY are normative. No implementation or installed
reader support is claimed.

## 1. Keys and manifest binding

A1. The auth key is secp256k1 BIP-340, in its own hardened account and
separate custody. Its Draft path is `m/84'/7'/12'/0/0`; see KEY-MAP's
v0.3 reconciliation for existing-path exceptions. A P-256 or BIP-340 device
key stays internal to the owner's control plane and MUST NOT sign external
service challenges or grants. The cold name-owner key signs name operations
only, never a login. The grant key signs grants, never a login.

A2. Named authentication requires the current confirmed LIP-0010 manifest's
paired `auth_key` and `auth_seal` members. `auth_key` is the 64-lowercase-hex
x-only key. `auth_seal` is exactly `{txid,vout,script}`: lowercase 64-hex
txid, number-form output index at most 4294967295, and lowercase script hex.
The seal MUST be a confirmed output under a supported disposable-key
construction, with its spent state checked on the verifier's own node.
Its exact script/fee construction remains open as for LIP-0029 device seals;
unsupported construction refuses, not unspent. The seal is never an auth-key
spend and is never a grant or device seal shared across roles.

A3. `auth_seal` and `device_seal` private keys MUST come from a CSPRNG,
never the BIP-39 seed. Destroy each private key immediately after securely
pre-signing and recording its `tx_revoke`, per LIP-0029 Figure 1; do not
destroy the recorded transaction. Changing the auth key requires a fresh
seal. All verifiers durably journal a validated seal spend under revocation
rules, even without manifest bytes; rollback cannot restore authentication.
Manifest edits alone close no grant and replace no grant authority pin.

## 2. Canonical challenge and upgrade objects

Both types use restricted RFC 8785 (LIP-0020 W1), W2 number-form Unix
seconds, W3 exact schemas, W4 typed digests and W5 BIP-340 signed forms
`{"payload":...,"signature":"<128 lowercase hex>"}`. The signing tag
equals `payload.type`. No `null`, unknown member or algorithm selector is
allowed. Each complete signed form is at most 4096 bytes. There is no
`swarm-envelope/2` body kind for foreign-service authentication.

| Type | Exact payload members |
| --- | --- |
| `swarma-auth-challenge/1` | `type`, `service_id`, `nonce`, `expires_at`, `auth_pubkey`; optional `name`, required in named mode and omitted in provisional mode |
| `swarma-auth-upgrade/1` | `type`, `service_id`, `account_id`, `name`, `auth_pubkey`, `firstupdate_txid`, `nonce`, `expires_at` |

`type` is the exact registered string. `service_id` is a nonempty ASCII
audience identifier pinned in the service's local configuration, not a
peer-supplied retrieval URL. `nonce` is 32 CSPRNG bytes in 64 lowercase hex;
`auth_pubkey` is a valid 64-hex x-only key. `name` is the exact `id/` name,
at most 255 ASCII bytes. `account_id` is a nonempty service-local ASCII
identifier. `firstupdate_txid` is a lowercase 64-hex transaction id.
`expires_at` is a W2 number, at most 9007199254740991.

A4. The service issues and durably records the exact challenge payload,
issuance time, audience, mode, nonce and intended account/key/name binding.
The client signs it with the **auth key**; the signed challenge is the
response. A nonce is valid for at most **120 seconds** from service issuance;
`now >= expires_at`, an expiry not after issuance or a longer TTL refuses.
The service compares every field to its outstanding challenge, verifies the
signature, then atomically consumes the nonce before establishing a session.
A replay or concurrent second consumption creates no second session.
For named mode it resolves the name and registration/owner history, obtains
the verified manifest through LIP-0033, matches `auth_key`, and checks the
auth seal and its durable closure journal. A device list is not needed.
An existing named account MUST retain its exact registration/owner binding;
a different registration or owner cannot silently take over that cell even
with the same name string. Missing bytes never trigger a silent outbound
fetch for a presentation.

A5. `swarma-auth-upgrade/1` uses a fresh nonce, with all A4 lifetime,
audience and single-use requirements, from the service's
upgrade-challenge endpoint (the v0.3 API example is
`POST /v1/onboarding/upgrade-challenge`, not a required HTTP API here).
The service binds it to the existing provisional account and auth key.
The signature proves that same key; a different key MUST NOT take over the
cell. Named checks and the confirmed first-update proof must pass before
one atomic consume-and-bind operation. Failures leave the provisional cell
unchanged. Replaying an upgrade never produces another account or a partial
rebinding. Ordinary challenges cannot be used as upgrade challenges.

## 3. Provisional accounts and client-owned registration

P1. A service MAY admit a key-only challenge without a name. It creates a
restricted local cell, not a named Link identity. No EFFECT, PII release,
wildcard grant recipient, federation membership or verified-human status
follows. Provisional request/rate/storage caps must be explicit, supported
and enforced durably; absent limits refuse. A key-only signature is no
proof that the key belongs to a human or owns a name.

N1. A sponsor MAY fund outputs controlled exclusively by the client. The
client may construct `OP_NAME_NEW` spending an unconfirmed funding output.
Same/next-block inclusion depends on policy, fees and miners, not a protocol
promise. The sponsor never owns the name or signs the client name operation.

N2. `OP_NAME_FIRSTUPDATE` must be mined at least 12 blocks after
`OP_NAME_NEW`, not after `funding_tx`. Waiting for 12 commit confirmations
before broadcast is conservative client policy. There is no promised
wall-clock duration. [Names](../protocol/names.md) defines verification,
not a funding API. The first-update value pins the manifest's auth key/seal;
the client supplies manifest bytes inline when no secondary path exists.
The service checks its required confirmed depth and the exact registration,
not merely a txid, an unconfirmed reveal or a sponsor statement.

### Non-normative implementation note: sponsored recovery

The owner's v0.3 draft, 2026-11-20, suggests a five-output `funding_tx`
to distinct user-controlled `name_new_addr`, `firstupdate_addr`,
`auth_seal_addr`, `seal_pool_addr`, `emergency_reserve_addr`. The auth-seal
address is CSPRNG-only and stays unspent until real auth revocation; the
emergency reserve uses a separate account 14'. See KEY-MAP for exceptions
to v0.3's proposed owner, grant and seal derivations. Persist the
`OP_NAME_NEW` salt in encrypted durable storage **before broadcast**.
A restart-safe client resumes after sleep/restart and automatically submits
FIRSTUPDATE when the commit is mature. This is implementation advice,
not an additional consensus rule, a deployed wallet claim or a timer guarantee.

## 4. Portability and third parties

The account owner is the pinned identity, not the replaceable service.
Services SHOULD support LIP-0009 migration; application export bytes are open.
Another person needs an independently verified, exactly targeted grant.
LIP-0035 permits contract-free scoped roots and an optional signed mandate
contract, never hire/rental, obligations or re-delegation under that profile.
Successful auth is not a grant signature, recipient consent or authority
to disclose data. A service MUST NOT turn its authenticated accounts into
a wildcard recipient.

## 5. Deterministic refusal order

1. LIP-0020 W9 wire pipeline (`WIRE_VALUE` for null, then its ordered
   schema/key/signature failures). A validly encoded but incorrect BIP-340
   signature is `AUTH_SIGNATURE` in this auth profile, not `WIRE_SIGNATURE`;
   WIRE signature form errors retain their codes.
2. `AUTH_CHALLENGE_EXPIRED` for an invalid time interval, TTL above 120 s,
   or expiry; then `AUTH_CHALLENGE` for wrong audience, field mismatch,
   absent/reused/wrong-purpose nonce or provisional-policy rejection.
3. In named mode: `AUTH_NAME_CLOSED` for a validated name closure, then
   existing name/history refusals, then LIP-0010's manifest order including
   `LIST_UNKNOWN` and active-chain `MANIFEST_ROLLBACK`.
4. `AUTH_KEY_UNPINNED` for absent/unpaired/different manifest auth binding
   or unsupported seal construction; `AUTH_SEAL_SPENT` for a validated
   spend/durable closure; `AUTH_SEAL_UNAVAILABLE` for unknown seal state.
5. On upgrade, `UPGRADE_KEY_MISMATCH` for another provisional key. For
   either mode, `AUTH_UPGRADE` for a mismatch with an existing cell's
   registration/owner binding; on upgrade also for invalid first-update/
   account binding or failed atomic consume-and-bind. No session or cell
   change precedes acceptance.

Grant checks belong to the later invocation pipeline. Credential issuer
closure is not a name or auth-key closure.

## 6. LIP-0018 checklist and conformance

- Identifiers, exact schemas, sizes, integers, signers and digests: section 2
  and LIP-0020 registry. New key role and manifest members: section 1.
- Binding/replay/provisional limits/atomic failure: sections 1–3; refusal
  order and forbidden partial outcomes: section 5.
- No new anchor action, limit kind or certificate subject; those specialized
  extension checklists do not apply. Auth seal script/fee and wallet APIs
  remain open, not fabricated canonical bytes.
- Adoption needs compatible readers, supported seal construction and a
  durable service challenge/account journal. Co-author agreement is pending.

Vectors are **not required for Draft LIPs** and are not supplied. Future
conformance pairs valid named/provisional/upgrade cases with device, grant
and cold-key substitution, wrong audience/nonce/purpose, TTL 121 versus 120,
expiry equality, replay/concurrency, unavailable or rolled-back manifest,
spent/unknown seal, immature reveal and an upgrade that changes the key.

## Open questions

Co-author agreement, the exact auth-seal script/fee/revoke construction,
service confirmation depths and application session/export profiles remain
pending. No secret is stored in the public manifest or card.
