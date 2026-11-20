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
recipient. Ivan Oparin decided on 2026-11-20 to take **Option B, scoped**:
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
`contract` member selects this profile. Do not add `authorization_mode`,
`contract_hash`, `consent`, `scope`, or `kind` members to the grant. In
particular `contract: null` is invalid under W1. All other required W11
members remain required, including `recent_block`, `not_before_height`,
`not_after_height`, and `seal`.

U2. The grant MUST be a root, have no `parent` and no `delegate`, and contain
only actions whose accepted profile classifies their effect as EFFECT.
The grant MUST NOT be a hire or rental grant. A verifier lacking the action
profile refuses; examples such as `secret.release`, `calendar-broker` and
asset withdrawal are not registrations of those profiles here.

U3. The recipient is exactly one W11.3 form: `{"key":"<x-only key>"}` or
`{"name":"id/...","owner":"<compressed owner key>"}`. The executor is
exactly one W11 executor. No wildcard, list of recipients, or trust-policy
substitute is allowed. Name-mode authority and ownership checks, including
the issuance snapshot and live-name checks, remain required. Omitted consent
does not mean omitted issuer or recipient identity checks.

U4. Typed limits MUST explicitly bound each permitted action. The height
members define the existing half-open interval with a finite upper bound. The dedicated
grant seal MUST be confirmed before admission and remain unspent. It is not
a shared contract seal. Undefined action/limit kinds fail closed under W11;
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
name, seal, snapshot, or action-profile checks. A `/2` preparation carrying
a contract-binding grant, or `/1` carrying a contract-free grant, refuses.

## 3. Single-use and bounded standing operation

**Single-use** permits one effect. A lightweight grantee may use an
issuer-revocable seal and a durable one-time consumption record in the
executor's LIP-0025 journal. Admission MUST reserve the one permitted use
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

1. LIP-0005 frame errors, then W9 canonical/type/size/signature errors.
2. `UNILAT_SCOPE` for a contract-free non-root, `delegate`, hire/rental, or
   non-EFFECT scope; `UNILAT_OBLIGATION_FORBIDDEN` for an otherwise valid
   action profile imposing obligations on the recipient. Unknown wire members
   fail earlier at W9, not here.
3. W11 binding, unsupported action/limit, name and issuance-anchor errors, in
   their existing order. A presented child fails `NOT_DELEGABLE` at the
   existing delegation stage, not under a new alias.
4. Existing `ISSUER_NAME_CLOSED`, seal-spend and window refusal codes at their
   existing stages. They take precedence over consumption checks.
5. `UNILAT_ALREADY_CONSUMED` when the single use is already consumed, or the
   existing limit refusal for an exhausted standing budget.

The draft aliases `UNILAT_ENCODING`, `UNILAT_REDELEGATION_FORBIDDEN`, and
`UNILAT_SEAL_SPENT` are not new wire codes. Preserve the existing specific
W9, delegation, and seal refusals.

## 5. Rejected alternative and security

Option A, a nominal `swarma-unilateral-mandate/1` contract, was rejected by
the owner. It is not an alternative implementation path or an object-type
registration. In particular sharing a grant seal with an invented issuer-only
contract does not satisfy the existing bilateral contract protocol.

The exception cannot be used to disguise hiring, rental, contractual liability,
an unknown action profile, or delegated authority. Executor compromise and
post-disclosure irreversibility remain outside the grant's cryptographic
guarantees. Private delivery does not remove ledger visibility of an anchor.

## 6. LIP-0018 checklist and conformance

- Identifier and byte rules: W11 grant `/4`, registered preparation `/2`,
  action `0x01` payload `0x03`, W1–W6 canonical and digest rules above.
- Bounds and binding: U1–U6, dedicated seal, one recipient/executor, finite
  window, and accepted action/limit profiles; unknown profiles refuse.
- Refusal order, negative cases, revocation, replay and rollout: sections 2–5.
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

## Open questions

The co-author's agreement on the scoped C5/C12 and consent amendments is
pending. The single-use P2SH-v4 construction and application action/limit
profiles remain open. The Option A/B choice itself is closed by the owner's
decision, not awaiting another preference poll.
