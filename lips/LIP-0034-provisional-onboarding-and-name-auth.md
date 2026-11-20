# LIP-0034: Provisional onboarding and name authentication

- **LIP:** 0034
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Requires:** [LIP-0010](LIP-0010-name-value.md), [LIP-0029](LIP-0029-owner-control.md), [LIP-0033](LIP-0033-reference-distribution-for-pinned-lists.md)
- **Related:** [Names](../protocol/names.md), [LIP-0009](LIP-0009-replaceable-services.md), [LIP-0035](LIP-0035-unilateral-mandates.md)
- **Follows:** [LIP-0001](LIP-0001-link-improvement-proposals.md), [LIP-0018](LIP-0018-extension-guide.md)

## Summary and decision

An existing owner can authenticate to a replaceable service using an authorized
device, not the cold name-owner key. A new user can start with a restricted
key-only account and promote it after client-owned name registration.

Ivan Oparin decided on 2026-11-20 that challenge-response uses
`swarm-envelope/2` with body kind `auth-response/1`, not a separate
`swarma-auth-challenge/1` signed format. Device-level and third-party rules
remain those of LIP-0029 and the scoped LIP-0035 exception. The co-author's
agreement on the corresponding older Draft amendments is pending.

MUST, MUST NOT, SHOULD and MAY are normative. Authentication establishes
identity only: it is not a grant, owner command, consent event or authorization
to disclose data or execute an EFFECT.

## 1. Named authentication

A1. The service MUST issue a cryptographically random 16-byte, base64url
unpadded, single-use nonce and a short expiry, bound in its own challenge
journal to the service's exact `aud`, the requested name and the current
registration outpoint and compressed owner key. The lifetime MUST NOT exceed
120 seconds. Reusing another service's nonce or audience refuses.

A2. The response uses the existing envelope container, CCJ-1 canonicalization,
author-signature algorithm and digest, `id` calculation, and replay rules of
LIP-0029 sections 4–5. The body-kind signing and ID tag is exactly `swarma-link auth-response/1`, followed
by the existing `0x0a` separator; its author role is the envelope's existing
author role. The typed body has `type: "auth-response/1"`, `aud`,
`nonce`, `iat`, `exp`, `name`, `registration`, `owner`, and, for named login,
`devices` and optional `device_list` in the existing section 5.1 forms. `nonce` echoes
the challenge. `iat` and `exp` are UTC `YYYY-MM-DDTHH:MM:SSZ` strings, **not**
Unix numbers. `registration` is `txid:vout`, not just a transaction ID.
The service checks the signed name/registration/owner against its challenge.

An envelope has one author signature by the identified device, never by the
cold name-owner key or the landlord grant key. An arbitrary key found in
`nostr`, a credential issuer key, or an invented authentication pin is not
an authorized device. An attached manifest and set bytes may accompany the
request under LIP-0033; they are not a new source of authority or an invented
envelope member. Their enclosing transport packaging remains outside this LIP.

A3. The service MUST resolve a live name from its own verified chain view,
match registration and owner, validate its manifest and `swarma-devices` set,
then verify the device, its live seal and the envelope signature. Pin and
journal checks use LIP-0010 section 11, not a direct device pin. Failure to
obtain bytes is not permission to use a stale or unpinned list.

A4. A supported signing device at ceiling 0, 1 or 2 MAY prove identity for
login; this proof grants no L1 or L2 authority. P-256/FIDO2 algorithms use
only the admitted LIP-0029 signature profiles. A messenger-only record with
no supported direct-envelope signature cannot authenticate by pretending to
be BIP-340. Presence and ceiling 2 remain required for L2 owner commands,
not for an identity-only login. An executor policy MAY demand stronger login.

A5. On success, atomically consume the nonce and create a local session bound
to `(name, registration outpoint, owner key, device key)`. A session MUST NOT
outlive its explicit local expiry or waive fresh authority checks for effects.
Name closure, device-seal spend and owner/registration changes invalidate the
named binding on observation. Device-list edits obey their existing journal
and membership rules. A local session is not portable cryptographic authority.

The external `swarm-envelope/2` registry currently has a closed body-kind set.
Adding `auth-response/1` and its conditional shape requires the corresponding
external specification review before implementation admission. This Draft
does not claim that external registry has already accepted the addition.

## 2. Provisional key-only account

P1. The client generates and retains the cold name-owner key and a separate
supported authentication/device key locally, preferably hardware backed.
The service and any fee sponsor MUST NOT receive either private key.

P2. A key-only response uses the same `auth-response/1` envelope, with body
members `type`, `aud`, `nonce`, `iat`, `exp`, and `key`. It MUST NOT claim
`name`, `registration`, `owner`, `devices`, or `device_list`. The author key
equals `key`, in the exact `p256:` or `bip340:` key-identifier form of
LIP-0029 section 4 and the envelope signature profile; the service verifies
proof of possession using a supported
LIP-0029 envelope signature algorithm. No nonexistent name or device seal
is fabricated. This conditional external body schema is part of the same
registration gate described in section 1.

P3. The provisional account cell is bound only to that key, is explicitly
unnamed, has no on-chain reputation and MUST NOT exercise named EFFECT
grants or high-value authority. A service MAY allow local profile setup and
other explicitly restricted operations. A provisional login MUST NOT be
reported as a live Swarma name or as an issuer/recipient ownership proof.

## 3. Client-owned registration and atomic upgrade

N1. Self-funded registration is the default. If the client has no NMC, a
sponsor MAY create `funding_tx` paying an output controlled exclusively by
the client. The client MAY construct `OP_NAME_NEW` spending that output
before it confirms. Inclusion in the same or next block depends on node
mempool policy, fees and miners; it is not guaranteed by this protocol.
The sponsor never owns the eventual name or its output script.

N2. The consensus maturity condition is that `OP_NAME_FIRSTUPDATE` is mined
at least 12 blocks after the `OP_NAME_NEW` commit, not that the funding
transaction has 12 confirmations. Waiting for 12 commit confirmations before
broadcast is a conservative client policy. There is no promised wall-clock
duration. [Names](../protocol/names.md) specifies name verification and values,
not this transaction-construction or funding API.

N3. The first-update value pins a LIP-0010 manifest whose device-list entry
contains the provisional key in an admitted device record. The name-owner
key signs name transactions, never the login response. A valid device seal
must exist; its construction follows LIP-0029, including a fresh disposable
seal key and destruction of that key after the pre-signed revoke is prepared.
Do not reuse the cold owner key as the device-seal key. The client supplies
manifest/list bytes inline if no secondary retrieval channel exists.

N4. After the first update reaches the service's required confirmation depth,
the service issues a fresh named challenge. The provisional key must answer
it as a member of the confirmed pinned device list. The service verifies all
named checks and atomically binds the existing cell to the exact name,
registration outpoint and owner. A concurrent or replayed upgrade MUST NOT
produce a second account or bind an account to a different name. Failure
leaves the restricted provisional cell unchanged. A mere transaction ID,
unconfirmed reveal, owner screenshot or sponsor statement is insufficient.

## 4. Portability and third parties

The account owner is the pinned identity, not the replaceable service. A
service SHOULD provide an authenticated migration/export path consistent
with LIP-0009; this LIP does not standardize its application data format.

Another person acts under a separately verified, exactly targeted grant.
For a contract-free grant apply all LIP-0035 root/no-`delegate`/non-hire/
non-rental restrictions. Recipient proof at invocation uses the applicable
Link request-key rules; a successful device login is not a grant signature,
contract consent, or a substitute for the executor's grant checks. A service
MUST NOT make a wildcard recipient out of all accounts that logged in.

## 5. Deterministic refusal order

1. Existing envelope shape, canonicalization, algorithm and signature errors
   in LIP-0029 order. Unknown external body kinds refuse until admitted.
2. `AUTH_CHALLENGE` for wrong audience, missing/expired/reused nonce, excessive
   lifetime, or response/challenge identity mismatch; no session is created.
3. For named mode, existing name/manifest/device-list mismatch, rollback,
   unsupported-device and device-seal refusals in their profile order.
   A key-only mode carrying named members fails shape checks first.
4. `AUTH_UPGRADE` for an otherwise valid response that cannot atomically bind
   the provisional cell to the confirmed name. Keep the old cell unchanged.

Grant refusal codes belong to the later grant pipeline, not to an identity
login. A credential issuer closure is not `ISSUER_NAME_CLOSED` for a login;
do not conflate the different key roles.

## 6. LIP-0018 checklist and conformance

- Identifier/bytes: one existing envelope format with one new body kind and
  two explicit conditional shapes; CCJ-1, not the LIP-0020 grant wire format.
- Bounds/binding: nonce 16 bytes, lifetime at most 120 seconds, exact audience,
  name/registration/owner/device binding and confirmed-list membership.
- Refusals/security: section 5; replay, ownership separation, provisional
  limits, propagation limits and atomic failure are specified above.
- No new anchor action, contract profile, limit kind or certificate subject
  is introduced. Their specialized extension checklists are not applicable.
- Adoption: external envelope-kind registration, reader rollout and service
  account-journal implementation are gates, not claims of deployed behavior.

Vectors are **not required for Draft LIPs** and are not supplied. Future
conformance needs valid named/key-only controls; cold-key rejection; ceiling-0
identity versus L2 authority; wrong nonce/audience/expiry; missing/rolled-back
manifest; spent seal; unconfirmed/immature reveal; unsupported algorithm;
and upgrade replay/concurrency with no duplicate or partially rebound cell.

## Open questions

Co-author agreement on amended Draft decisions and external envelope-kind
acceptance remain pending. Application session lifetimes, data export format,
service confirmation depths, and transport packaging of inline manifests
are deployment choices or separate profiles, not fabricated canonical bytes.
