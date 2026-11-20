# LIP-0036: Federated trust and progressive disclosure

- **LIP:** 0036
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Requires:** [LIP-0008](LIP-0008-grant-v4.md), [LIP-0029](LIP-0029-owner-control.md), [LIP-0032](LIP-0032-generalized-notary-and-credentials.md), [LIP-0033](LIP-0033-reference-distribution-for-pinned-lists.md), [LIP-0035](LIP-0035-unilateral-mandates.md)
- **Related:** [Revocation](../protocol/revocation.md), [LIP-0034](LIP-0034-provisional-onboarding-and-name-auth.md), external [curator-trust](https://github.com/relux-works/curator-trust)
- **Follows:** [LIP-0001](LIP-0001-link-improvement-proposals.md), [LIP-0018](LIP-0018-extension-guide.md)

## Summary and decision

Unknown peers may screen each other under bounded, low-risk policy before
an owner authorizes a specific disclosure. Ivan Oparin decided on 2026-11-20
that this proposal uses the LIP-0032 **credential** kinds, the non-exclusive
LIP-0033 distribution rule, and the scoped LIP-0035 contract-free exception.
The co-author's agreement on the amended Draft decisions is pending.

MUST, MUST NOT, SHOULD and MAY are normative. Neither federation membership,
a credential nor a policy signature creates grant authority.

## 1. Two phases

| Phase | Admission | Data boundary | Human gate |
| --- | --- | --- | --- |
| Screening | Pinned landlord trust policy, an independently valid screening grant and optionally a `subject-claim` credential | Zero PII and no external tools in the screening context | No per-message confirmation, within accepted signed limits |
| Disclosure | Exactly targeted EFFECT grant to one recipient and one executor | Sensitive bytes held by the isolated executor, not the screening agent | Explicit human-gated issuance request, followed by grant-key signing |

F1. A verifier MUST NOT accept wildcard Grantee fields. It checks separately
the peer's landlord against its active trust policy, the peer-to-landlord
binding, and the screening grant's authority, limits and unspent seals.
The agent's `swarma.agent.landlord` pointer alone is not ownership or grant
authority. Use the issuer/name/owner pins and applicable holder/J10 proofs.
A policy may narrow admission; it never replaces any of those checks.

`curator-trust` is an **external repository**, not a module, file or accepted
wire profile in this repository. A deployment MUST pin the exact policy
version/digest, signing authority and supported schema. If it cannot verify
that policy or cannot establish the landlord binding, it refuses admission.
This LIP does not invent the external project's canonical policy bytes.

F2. A `subject-claim` or `agent-audit` is a kind of `swarma-credential/1`,
not of `swarma-notary-attestation/2`. When required by the local policy,
verify its issuer credential-key role, named subject binding, anchored bytes,
lifecycle, compromise-height and revocation rules in LIP-0032. A claim such
as `human_verified` is accepted only under an explicit claim/issuer policy;
an arbitrary signed string is not proof that a human exists.

F3. The screening context MUST contain no PII and have no external tools.
Every screening session MUST enforce explicit per-peer caps for model
requests, model tokens, outbound messages and rate, using supported action
and limit profiles. Missing, undefined, unmeasurable or exhausted limits
refuse, never mean infinity. Registering these application profiles remains
a prerequisite; their names here do not extend LIP-0031 automatically.
Accounting is durable and follows LIP-0025/LIP-0026. One grant has one
executor; independent executors require independent grants, not cloned caps.

Screening TEXT hiring remains contract-binding. It MUST NOT use the
contract-free exception reserved for root, non-hire, non-rental EFFECT
grants. Federation membership does not remove recipient consent to hiring.

F4. The screening agent MUST NOT autonomously issue the disclosure grant.
An owner must explicitly approve the precise recipient, effect, executor,
limits and expiry. When using LIP-0029 owner control, require an L2 owner
command from a presence-capable ceiling-2 device, or its separately admitted
human-console path. That command requests the operation; the **grant key**
still signs the resulting root grant. A ceiling-2 device does not acquire
grant-key signing authority. The cold name-owner key does not log in or sign
routine envelopes. The `Owner-confirmation threshold` is an effect-policy
limit, not the name for issuance authority or an alternative signing key.

F5. The resulting unilateral grant follows all LIP-0035 rules: one recipient
key or name, one executor, no `delegate`, no hire/rental, no obligations on
the grantee, a dedicated seal and finite limits/window. Examples include
single-use contact handoff or narrowly capped calendar access. An undefined
`secret.release` or calendar profile MUST refuse until separately specified.

F6. Matrix E2EE, Nostr and a2a-swarm can carry the private conversation and
grant bytes. Reference bytes from any source count only after their pin and
all profile checks pass (LIP-0033). No `loc` enters the name or manifest,
and a reference channel never forbids another channel. Public event delivery
does not satisfy a requirement for private disclosure.

F7. Spending a disclosure seal closes its admission durably on observation,
without a manifest update. Issuer emergency closure uses its applicable
LIP-0008/LIP-0021 rules. A landlord's brake closes grants issued by that
landlord; it does not magically revoke a different owner's disclosure grant.
Loss of federation-policy admission may independently stop further screening.
Network propagation is not instantaneous at every verifier.

## 2. Deterministic refusal order

1. Existing frame, object wire, signature and identity errors for each
   submitted object, in that object's profile order.
2. `FED_POLICY_UNKNOWN` for missing, stale, unsupported or unverifiable trust
   policy, then `FED_LANDLORD` for a failed policy or peer/landlord binding.
3. Credential-profile refusals when a credential is required; grant-profile
   refusals for screening authority, seals and closure, in their own order.
4. `FED_LIMITS` for missing or unsupported required screening caps; the
   existing limit-overrun code when a defined cap is exhausted.
5. `FED_HUMAN_GATE` for an attempted disclosure transition without the
   human-authorized issuance request. No grant or disclosure is produced.
6. The ordinary LIP-0035/Link invocation pipeline for the resulting disclosure
   grant. A policy verdict never overrides its refusal.

## 3. Security boundaries

Keeping PII and external tools out of the screening context reduces the
available prompt-injection impact; it is not a universal guarantee against
exfiltration of other context, covert channels, or implementation compromise.
Untrusted peer text never supplies policy or human authorization. The
executor must independently verify every authority and requested effect.

Revocation stops future admissions but cannot erase a copied contact or an
already executed external effect. Prefer revocable handles and ephemeral
rooms over permanent phone numbers. A credential claim and a policy pin may
be privacy-sensitive even when their delivery transport is encrypted.

## 4. LIP-0018 checklist and conformance

- This is a composition profile: no new grant wire member, anchor, certificate
  subject or limit kind. Specialized registration checklists are inapplicable;
  the depended-on profiles must themselves be accepted and implemented.
- Binding and bounds: F1–F7; no wildcard, separate policy/grant checks,
  explicit screening caps and human-gated targeted disclosure.
- Refusal order and security limits: sections 2–3. Unknown policy/profile,
  absent limits or a failed human gate leave no disclosure or grant behind.
- Rollout requires the external policy format, the action/limit profiles and
  the LIP-0032/0035 implementations; this Draft does not certify those systems.

Vectors are **not required for Draft LIPs** and are not supplied. Future
conformance must pair valid two-phase cases with wildcard recipients, false
landlord pointers, expired policy, wrong credential subject/key role, missing
caps, unknown profiles, multi-executor budget duplication, ceiling-1 issuance,
ceiling-2 grant-signature substitution, contract-free TEXT hiring, and seal
revocation without forbidden partial disclosure.

## Open questions

Co-author agreement on the amended Draft decisions remains pending. External
policy schema/admission, application action/limit profiles and a privacy-safe
claim policy are prerequisites, not canonical bytes asserted by this LIP.
