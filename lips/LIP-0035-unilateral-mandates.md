# LIP-0035: Unilateral mandates and contract-free EFFECT grants

- **LIP:** 0035
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Requires:** [LIP-0008](LIP-0008-grant-v4.md), [LIP-0020](LIP-0020-grant-v4-wire-registry.md)
- **Amends:** [LIP-0017](LIP-0017-contracts.md), [LIP-0020](LIP-0020-grant-v4-wire-registry.md)
- **Follows:** [LIP-0001](LIP-0001-link-improvement-proposals.md), [LIP-0018](LIP-0018-extension-guide.md)

## Summary and decision

A root EFFECT grant may confer permission without imposing a contract on its
recipient. Ivan Oparin decided on 2026-11-20 (source: `$HZ30GFE5jwhKwwz9eDacfUnKf6nTRh2h-uF4OHylwD4`) to take **Option B, scoped**:
only a root grant without `delegate`, never a hire or rental grant, may omit
`contract`; the recipient is one key or one name. The co-author's agreement
is pending. Source: `$HZ30GFE5jwhKwwz9eDacfUnKf6nTRh2h-uF4OHylwD4`.

This supersedes the universal wording of LIP-0017 C5 and C12 and the universal
consent wording in LIP-0020. Their requirements still apply to grants that
bind a contract (bilateral, framework, rental). It does not remove contract
or consent requirements from hiring, rental, or re-delegation.

The terms MUST, MUST NOT, SHOULD and MAY are normative. A proposal in this
Draft is not evidence of implemented or admitted execution profiles.

## 1. Wire and scope

U1. Use `swarma-grant/4` and LIP-0020 W1–W6 and W11. Omission of its optional
`contract` member selects the contract-free branch of this profile. A
root satisfying U2–U6 MAY instead bind the optional mandate in section 2.1;
that branch retains contract-bound issuance, assent and consent checks. Do not add `authorization_mode`,
`contract_hash`, `consent`, `scope`, or `kind` members to the grant. In
particular `contract: null` is invalid under W1. All other required W11
members remain required, including `recent_block`, `not_before_height`,
`not_after_height`, and `seal`.

U2. The grant MUST be a root, have no `parent` and no `delegate`, and contain
only actions whose accepted profile classifies their effect as EFFECT.
The grant MUST NOT be a hire or rental grant. A verifier lacking the action
profile refuses; examples such as `secret.release`, `calendar-broker` and
asset withdrawal are not registrations of those profiles here. Actions use
lowercase slash segments as in LIP-0007 section 1, for example
`contact/release`. Hire/rental has no grant discriminator: the verifier
enforces EFFECT-only supported profiles and U5's prohibition of obligations;
the issuer MUST NOT use either branch to disguise hire or rental.

U3. The recipient is exactly one W11.3 form: `{"key":"<x-only key>"}` or
`{"name":"id/...","owner":"<compressed owner key>"}`. The executor is
exactly one W11 executor. No wildcard, list of recipients, or trust-policy
substitute is allowed. Name-mode authority and ownership checks, including
the issuance snapshot and live-name checks, remain required. At issuance,
resolve the recipient name at the signed grant's `recent_block` using the
verifier's own indexed name history, and compare its live owner to
`recipient.owner`. No consent-key snapshot or `name_output` evidence is
fabricated for the contract-free branch. Missing historical evidence refuses
`ISSUANCE_MODE` in W9.4 step 2; invocation repeats the live name/owner check.
Omitted consent
does not mean omitted issuer or recipient identity checks.

U4. Typed limits MUST explicitly bound each permitted action. The height
members define the existing half-open interval with a finite upper bound. The dedicated
grant seal MUST be confirmed before admission and remain unspent. It is not
a shared bilateral contract seal; the optional issuer-only mandate MAY
share exactly that grant seal under section 2.1. Undefined action/limit kinds fail closed under W11;
LIP-0031 is itself a Draft, not a blanket implementation permission.

U5. This grant imposes no payment, penalty, work, or other obligation on its
grantee. Acceptance by use authorizes the requested effect only; it is not
consent to an unstated contract. A profile which debits the grantee or binds
such an obligation MUST NOT use this exception.

U6. There is **no re-delegation**, including a notary-certified exception.
A child under a root without `delegate` is `NOT_DELEGABLE`. To delegate, issue
a different, contract-binding grant through the existing contract and
LIP-0014 rules; do not convert this grant by adding a child.

## 2. Issuance preparation and anchor

For this case only, the unsigned preparation is `swarma-issuance/2`, with
exactly `type`, `genesis`, `grant_id`, and `grant_signature`. The last three
have the same forms and meanings as in `swarma-issuance/1`. Its canonical
payload is at most 1024 bytes, follows W1–W4, and has no detached signature.
The grant signature, not a signature on the preparation, proves the issuer's
grant-key authorization. No issuer assent, recipient consent event, or
contract seal is fabricated.

The issuance anchor uses LIP-0005 action `0x01`, payload version `0x03`, and
the 32-byte typed digest of that preparation. Location `0x00` has zero pointer
bytes; location `0x01` has the 32-byte SHA-256 content address of the **signed
grant**, not of the preparation. These frames are 40 and 72 bytes respectively.
Version `0x02` and preparation `/1` remain the contract-binding path; neither
version may be substituted for the other. Existing v3 framing is unchanged.

Apply W9's frame, wire, signature, binding and commitment checks in order.
In its issuance pipeline, choose `/2` only after the signed grant satisfies
U1–U6. Skip only the contract-assent/consent evidence steps, not signature,
name, seal, snapshot, or action-profile checks. The recipient snapshot is
reconstructed at the signed `recent_block` as U3 specifies, not read from
a nonexistent `/2` member. A `/2` preparation carrying
a contract-binding grant, or `/1` carrying a contract-free grant, refuses.

### 2.1. Optional signed mandate contract

The Swarma Link editor's resolution proposes `swarma-unilateral-mandate/1`
from the owner's v0.3 draft, 2026-11-20. It is signed **only by the issuer's
BIP-340 grant key**, in the LIP-0020 W5 `{payload,signature}` wrapper;
tag = `swarma-unilateral-mandate/1`. The signed form is at most 65536 bytes.
All bytes follow W1–W6: RFC 8785 restricted form, no null, exact listed
members, W2 integer forms. Its contract identifier is W6.1's SHA-256 of
canonical payload bytes, stored in `swarma-grant/4.contract`.

The exact payload members are `type`, `network`, `genesis`, `issuer`,
`recipient`, `executor`, `mode`, `actions`, `limits`, `seal`, `seal_type`,
`not_before_height`, `not_after_height`, `issued_at`. `type` is the exact
registered type; `network` is `main` or `regtest` matching `genesis`.
`issuer`, `recipient`, `executor`, `actions`, `limits`, `seal` and the two
height members have **exactly the root grant's W11 forms and values**.
This preserves key/name owner pins rather than using bare name strings.
`mode` is `single-use` or `standing`; it selects the supported execution
profile, never an extra grant member. `seal_type` is exactly `issuer-only`.
`issued_at` is W2 number-form Unix seconds, at most 9007199254740991.
`limits` is W11.4's array (`kind`, `resource`, `unit`, decimal-string
`amount`, optional `period`), not an object map; actions are lowercase
slash segments. An unsupported action/limit/seal construction refuses.

Only the issuer is a contractual party. No grantee payment, penalty or
other obligation is permitted. C5 and C12 hold: the contract is named and
has a confirmed live seal. The mandate MAY use the **same issuer-only seal**
as its grant; both close on its spend. The mandate's issuer, recipient,
executor, actions, limits, seal, genesis and window MUST equal the grant's,
and the grant's `contract` MUST equal its identifier. After both objects'
wire/signature checks, any inequality is **`UNILAT_MANDATE_MISMATCH`**.
This includes a different issuer key or recipient owner pin. No fallback
to the contract-free branch is allowed when a supplied contract fails.
The contract-bound `/1` issuance path still checks W7 issuer assent and
recipient consent; the issuer-only mandate signature does not fabricate
either document. Its single-party contract signature imposes no grantee
obligation. Re-delegation stays forbidden under U6.

### 2.2. Signed broker invocation

`swarma-broker-invoke/1` is the LIP-0020 W5 signed invocation wrapper, tag
`swarma-broker-invoke/1`, at most 1048576 bytes including the signature.
Its exact payload members are `type`, `genesis`, `grant`, optional
`mandate`, `issuance_txid`, `manifest_bundle`, `nonce`, `expires_at`.
`type` is the exact type; `genesis` and `issuance_txid` are 64-lowercase-hex
hashes. `grant` is lowercase even-length hex of the canonical **signed grant
bytes**; `mandate`, when present, is the same encoding of the signed mandate.
It is required iff this invocation uses the optional mandate profile, and
MUST be omitted for the contract-free branch. This wrapper cannot carry an
unrelated bilateral contract as a unilateral mandate.

`manifest_bundle` is an array of objects exactly `name`, `manifest`, `sets`.
`name` is the exact `id/` name, at most 255 ASCII bytes; names are distinct
and in increasing ASCII order. `manifest` is lowercase even-length hex of
its exact canonical bytes. `sets` is an object of zero to four optional
registered set names, each with lowercase even-length hex of its document
bytes. W1 sorting applies to this container, not to the decoded fixed-order
documents. All decoded documents keep their own size and grammar limits.
The bundle supplies octets only: resolve every pin on the verifier's own
node and follow LIP-0010/LIP-0033; no bundled URL authorizes an outbound fetch.

`nonce` is 32 CSPRNG bytes, 64 lowercase hex, issued by the executor as an
outstanding single-use challenge. `expires_at` is W2 number-form Unix
seconds, at most 9007199254740991, equal to the executor's challenge expiry.
The executor binds the challenge to this grant, audience and grantee;
`now >= expires_at` refuses. The wrapper is signed by the grant's exact
recipient key, or for name mode the current named BIP-340 channel/request
key verified by the accepted Link recipient proof, never a device key.
Unsupported name-mode proof refuses; no signature alone supplies authority.
`issuance_txid` must resolve to the verified grant issuance, not just any
transaction. A fresh nonce does not reopen an already single-used grant.

After wire, mandate equality and grant/issuance/state checks, a missing,
expired, mismatched or consumed challenge is `UNILAT_INVOCATION`. The
executor atomically reserves the nonce and single-use grant (or standing
budget) in its fenced LIP-0025 journal before any effect. Section 3 applies
to retries, backup rollback, concurrency and uncertain outcomes.

## 3. Single-use and bounded standing operation

**Single-use** permits one effect. A lightweight grantee may use an
issuer-revocable seal and a durable one-time consumption record in the
executor's LIP-0025 journal, with an **external append-only fencing
witness outside the database backup domain**. Before admission the executor
checks the journal position against that witness; a restored stale database
is `JOURNAL_ROLLBACK`, never a fresh use. Reserve in the journal and witness
before performing the effect; interrupted/uncertain reservations stay
consumed or pending, never reopen. Unavailable fencing fails closed with
LIP-0025's `JOURNAL_FENCED`. Admission MUST reserve the one permitted use
durably before the external effect. Retries with the same invocation identity
return the journaled outcome; uncertainty MUST NOT reopen the use. All
replicas of that one executor share the authoritative journal. Independent
executors require independently targeted grants (LIP-0026).

The original LIP-0002 one-of-two P2SH spend is another single-use construction,
but its exact Grant-v4 `seal.construction` profile is not defined here.
It MUST NOT be encoded by inventing `seal.kind: "single-use"`. That mapping
is open; a verifier without an accepted construction refuses it.

**Bounded standing** permits repeated effects only within the signed action
limits and finite window, with durable LIP-0025/LIP-0026 accounting. Mode is
an action/limit-profile property, not a new grant member. A standing permission
never authorizes unbounded calls, an unregistered `Rate` or `Model requests`
limit, or a second executor's independent consumption of the same budget.

Delivery SHOULD be private off chain. The issuer MAY use anchor location
`0x00` and deliver the bytes directly by an authenticated encrypted channel,
including Matrix E2EE, appropriately encrypted Nostr delivery, or HTTPS.
[LIP-0033](LIP-0033-reference-distribution-for-pinned-lists.md) makes reference
channels non-exclusive; a public Nostr event is not private delivery.

A seal spend closes admission **upon observation** in the mempool or a block,
durably under `protocol/revocation.md`. No manifest update or grantee consent
is needed. This is immediate at a witnessing verifier, not a claim of zero
network propagation time. Already disclosed bytes cannot be recalled.

## 4. Deterministic refusal order

Use existing pipeline codes rather than aliases for malformed wire or closure:

1. LIP-0005 frame errors, then W9 canonical/type/size/signature errors
   for each object. Null is `WIRE_VALUE`; a contract-free child is
   `WIRE_MEMBER` before any scope check.
2. For the optional contract profile, `UNILAT_MANDATE_MISMATCH` for any
   inequality of the section 2.1 bound fields or contract identifier.
3. `UNILAT_SCOPE` for an otherwise well-formed contract-free root with
   `delegate`, a hire/rental action profile or non-EFFECT scope; then
   `UNILAT_OBLIGATION_FORBIDDEN` for any other obligation-bearing profile.
   Optional mandates must satisfy the same U2/U5/U6 semantic restrictions.
   An attempted child under a non-delegable parent remains `NOT_DELEGABLE`
   at its ordinary delegation stage, never a new alias.
4. W11 binding, unsupported action/limit, name and issuance-anchor errors
   in their existing order. Existing `ISSUER_NAME_CLOSED`, seal-spend and
   window refusals retain their existing stages and precede consumption.
5. `UNILAT_INVOCATION` for a failed broker challenge/binding/expiry check.
6. `JOURNAL_ROLLBACK` for a database position behind the external witness;
   LIP-0025 `JOURNAL_LOST`/`JOURNAL_FENCED` for missing/unavailable journal
   or fencing evidence. No effect is allowed.
7. `UNILAT_ALREADY_CONSUMED` when a single-use grant was consumed; the
   existing limit code for exhausted standing budget. A retry of the same
   accepted invocation returns its recorded outcome, never a second effect.

The draft aliases `UNILAT_ENCODING`, `UNILAT_REDELEGATION_FORBIDDEN` and
`UNILAT_SEAL_SPENT` are not new wire codes. Preserve W9, delegation and seal
codes above. A stage failure creates neither a partial effect nor authority.

## 5. Rejected alternative and security

Mandatory Option A was rejected in favor of the owner's scoped B.
The Swarma Link editor's resolution nevertheless accepts the owner's v0.3
signed mandate as an **optional** contract profile, not a replacement for B.
Whether it becomes mandatory later remains an open owner question.

The exception cannot be used to disguise hiring, rental, contractual liability,
an unknown action profile, or delegated authority. Executor compromise and
post-disclosure irreversibility remain outside the grant's cryptographic
guarantees. Private delivery does not remove ledger visibility of an anchor.

## 6. LIP-0018 checklist and conformance

- Identifier and byte rules: W11 grant `/4`, registered preparation `/2`,
  action `0x01` payload `0x03`, optional mandate and broker types registered
  in LIP-0020, W1–W6 canonical and digest rules above.
- Bounds and binding: U1–U6, dedicated seal, one recipient/executor, finite
  window, and accepted action/limit profiles; unknown profiles refuse.
- Refusal order, negative cases, revocation, replay and rollout: sections 2–5.
- Contract-profile checklist: identifier, exact parties/signature, payload,
  finite window, equal limits, issuer-only seal and spend semantics are in
  section 2.1; no machine field imposes grantee obligations. This is not an
  agent-launch/rental contract, so C9 configuration does not apply. General
  C2 per-clause salt/selective-disclosure proof mapping remains open before
  adoption; this whole-document profile MUST NOT claim partial-clause proof.
- Specialized certificate-subject checklist: not applicable. No certificate
  subject or general new limit kind is registered by this LIP.
- Adoption: W11, issuance preparation and executor-journal readers must be
  updated before production issuance. Existing contract-binding grants keep
  their consent and confirmed-contract-seal requirements.

Vectors are **not required for Draft LIPs** and are not supplied. Admission
still requires implementation tests for a valid root/key and root/name pair,
contract-bearing positive controls, forbidden `delegate`/child/hire/rental,
null versus omitted contract, obligation-bearing actions, wrong preparation
version, absent seal, replay/concurrent single use, and durable revocation.
No single-use P2SH-v4 bytes are claimed while their construction is open.

The conformance plan also requires named regression pairs for contract-free child `WIRE_MEMBER` versus root
scope `UNILAT_SCOPE`, each mandate equality field, null `WIRE_VALUE`, nonce
replay/expiry, and restored database versus external fencing witness
(`JOURNAL_ROLLBACK`). A witness outside the backup domain is not optional.

## Open questions

The co-author's agreement on the scoped C5/C12 and consent amendments is
pending. The single-use P2SH-v4 construction and application action/limit
profiles and general C2 per-clause salt/proof mapping remain open before
adoption. The Option A/B choice itself is closed by the owner's
decision, not awaiting another preference poll. Whether the optional
mandate profile becomes mandatory later is an open owner item.
