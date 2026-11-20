# LIP-0032: Generalized notary attestations and verifiable credentials

- **LIP:** 0032
- **Status:** Draft
- **Author:** Ivan Oparin
- **Created:** 2026-11-20
- **Affects:** LIP-0005, LIP-0010 section 9.1, LIP-0012, LIP-0014,
  LIP-0017, LIP-0020, LIP-0021 and KEY-REGISTRY
- **Follows:** LIP-0001 and LIP-0018

## Summary

Third-party diplomas, deeds, licenses, work-completion acts, human-status
claims and runtime audits use one object family, `swarma-credential/1`.
Its two lifecycles are eternal and revocable. A distinct **credential
issuer key**, in `swarma.issuer.cred` of the issuer's own name, signs it.
Notary attestations retain `child-within-parent` and add
`contract-notarization`, not a second human-verification object.

Ivan Oparin decided on 2026-11-20 (source: `$-R4EXclWAkV9M95f3lhmqEzucNKId1XdrKY-YUtUJb0`, `$Gud1cjVYSeUB5efzCOTWCUKyo6_USVveOlma-8vPrXo`, `$rLXvqLJXXxqduX4JKe7QyLua9IPDECvVc6xmM_NtyOM`) that `subject-claim` and `agent-audit`
are credential kinds, that credentials have the new key role, and that an
eternal credential survives rotation unless an owner-authenticated break
covers its anchor at or above a declared compromise height `h_c`. The
co-author's agreement is pending. Sources: events
`$-R4EXclWAkV9M95f3lhmqEzucNKId1XdrKY-YUtUJb0`,
`$Gud1cjVYSeUB5efzCOTWCUKyo6_USVveOlma-8vPrXo` and
`$rLXvqLJXXxqduX4JKe7QyLua9IPDECvVc6xmM_NtyOM` of 2026-11-20.

The words MUST, MUST NOT, SHOULD and MAY have their RFC 2119 and RFC 8174
meanings. Every rule below is Draft, not an adoption or implementation claim.

## Motivation and current state

The notary of LIP-0012 certifies facts it checked, but its concrete
attestation/1 in LIP-0014 certifies only a child within a parent. LIP-0015
and LIP-0016 statements bind the owner's own keys and configuration, not
third-party facts. Neither is a diploma or a general institutional license.

A verified-human or age-bucket claim can limit Sybil abuse without putting
raw PII on chain; an auditor can attest a runtime's isolation profile;
a notary can witness contractual facts. These are signed claims, not
proofs of honesty, legal status, legal capacity or satisfactory work.
Trust policy still decides which issuers and claims it accepts.

## 1. Notary attestations

`swarma-notary-attestation/1` and its `child-within-parent` semantics stay
unchanged. `/2` is retained: it is already the typed-digest successor in
LIP-0020, and contract notarization needs the notary's current-key and
withdrawal semantics, not a credential's optional eternal lifecycle.
Moving notarization to credentials would erase that distinction. The
only `/2` kinds are `child-within-parent` and `contract-notarization`.

Both use LIP-0020 W1 to W6: restricted RFC 8785, `type` rather than
`profile`, the type's tagged digest, BIP-340 and `{payload,signature}`.
The proposed fixed `swarma-notary-v2` prefix is not used: W4 derives
the signing domain from the exact registered type string.
The signed form is at most 65536 bytes.

For `child-within-parent`, the binding, textual/mechanical checks, parties,
ordinal, notary seal, withdrawal and for-cause prohibition of LIP-0014
remain its semantics. Its exact `/2` member mapping awaits the J5/J2
v4 path and scope-text bytes of that LIP. It is **open**, not a guessed
copy of the v1 members with renamed hashes. A reader supports no kind
without its complete schema (W3.1).

For `contract-notarization`, the proposed payload has exactly these
members, sorted by RFC 8785, with the forms of section 2 below:
`type` = `swarma-notary-attestation/2`, `kind` = `contract-notarization`,
`network`, `genesis`, `notary` (the pinned name/registration/owner object),
`notary_key` (signing key), `contract_id` (hash), `party_names` (two or more
distinct name strings, increasing ASCII order), `notary_clause_sha256`
(hash), `witnessed_at` (Unix-seconds number), `notary_seal` (the
`notary_seal` member forms of LIP-0014 section 6.1, re-encoded in W1
order rather than copying the v1 byte order), `tip_height` (height),
`tip_hash` (hash) and `attested_at` (Unix-seconds number). It binds the
identifier of a separately supported contract profile, not a hash
invented for the still-unspecified general LIP-0017 contract bytes.
The notary resolves through LIP-0010 section 9 and LIP-0021 section 7.3;
it never reuses the credential key. Party names are witness claims, not
substitutes for checking the contract's parties and their assents.

Its anchor uses action `0x04`, payload version `0x02`, the typed digest
of the payload as commitment, and locator `0x00` or `0x01` (content
address of the signed form). The version-1 anchor and action `0x05`
notary-withdrawal-for-cause preimage remain unchanged. The precise
contract-notarization withdrawal-for-cause profile is open: a verifier
must not apply the child-specific `swarma-attest-cause-v1` meaning to it.
Plain notary-seal spend withdraws the notarization; no new grant authority
or child-recertification prohibition follows for a contract from that spend.

## 2. Credential bytes and issuer role

A credential is a LIP-0020 signed object with the following payload schema;
the **complete signed form** is at most **65536 bytes**. Every object has
only its listed members. Canonical bytes are W1, integers W2, keys W3.6,
the signing digest W4, signature and signed form W5, identifier and content
address W6. No `null`, fixed-prefix digest or v1 contract canonicalization is borrowed. Sensitive claim fields SHOULD use
per-claim salts for selective disclosure, as the original proposal requires.
The exact salted-clause/Merkle proof format is open; the claims container
below authenticates a complete privately delivered document, not a partial
disclosure proof. A verifier MUST NOT accept an invented partial proof.

| Member | Form and meaning |
| --- | --- |
| `type` | Exact string `swarma-credential/1` |
| `credential_kind` | `subject-claim`, `agent-audit`, or a supported application kind of lowercase ASCII slash segments as in LIP-0007 section 1 (for example `edu/diploma/1` or `id/human-verified/1`) |
| `network` | `main` or `regtest`, matching `genesis` and the pinned chain |
| `genesis` | Hash: exactly 64 lowercase hex characters |
| `issuer` | Exactly `name`, `registration`, `owner`: the issuer's name, first-registration outpoint and compressed name-owner output key (`owner` is the 66-hex compressed secp256k1 `owner_pin` of LIP-0021 O2.1), as W11.2 defines these forms |
| `issuer_key` | Valid 64-hex x-only BIP-340 key, read from that issuer name's `swarma.issuer.cred` |
| `subject` | Exactly `{mode,key}` with `mode` equal to `key` and a signing key, or exactly `{mode,name,registration,owner}` with `mode` equal to `name` and the same pinned name forms as `issuer`; no name string alone. These are this credential schema's members, not extra grant-recipient members |
| `claims_salt` | 32 random bytes, 64 lowercase hex; part of the signed payload |
| `claims` | Canonical object of machine-readable claims under the supported credential-kind schema. W1 values and depth limits apply; that schema states the exact W2 form and bound of every integer. No per-field quota beyond the complete-document bound is introduced here. Salted commitments or selective proofs require their separately specified schema below |
| `lifecycle` | `eternal` or `revocable` |
| `revocation_seal` | Absent for eternal; required for revocable, exactly `{txid,vout,script}`: 64-hex txid, W2 number-form output index at most 4294967295, lowercase hex script bytes, controlled solely by the issuer |
| `not_before_height` | W2 number-form height, 0 to 9007199254740991 |
| `not_after_height` | Optional only for eternal; required for revocable, same form, strictly greater than `not_before_height`; exclusive end of the window |
| `issued_at` | W2 number-form Unix seconds, a claim of the signer, never evidence of anchor height |

For `subject-claim`, `subject` is by name. Its claims may include
`human_verified`, an age bucket or jurisdiction. For `agent-audit`, the
subject is an agent or service name, and claims include
`code_or_config_sha256` (a hash) and `audit_profile` (a nonempty string);
an isolation tier is a claim, not an executor permission. Applications
define their exact accepted claim vocabulary and meanings. An unknown
kind or required claim refuses; agreeing signatures do not supply a schema.
Diploma, deed, license and work-act kinds require their own accepted
application profiles before machine admission; their names alone do not
create those profiles.

The credential issuer name has one shape, `{"issuer":{"cred":"<key>"}}`
inside `swarma` (LIP-0010 section 9.1). A notary that also issues credentials
uses a second name. The credential key signs no grant or notary attestation.
It cannot be moved into the manifest to evade name-history checks.

### 2.1. Privacy

Only commitments go on chain. Raw PII MUST NOT enter an anchor, locator,
public card or public store. PII-bearing documents SHOULD use `0x00` and
private delivery, or a separately specified encrypted-storage profile;
transport encryption does not change canonical plaintext verification.
Clear `claims` disclose the whole object to its recipient. A single
`claims_salt` does **not** implement per-claim selective disclosure.
Per-claim salts, Merkle commitments and their canonical disclosure proofs
remain open; LIP-0017 section 2 explicitly leaves their preimages open too.
No implementation may claim partial-claim verification from this schema.

An issuer deduplicating humans MUST NOT hash raw biometric vectors directly.
Per the owner's v0.3 draft, 2026-11-20, it uses salted HMAC-SHA256 for
discrete identifiers, an encrypted LSH/vector index, or an external KYC
`subject_dedup_id` for video verification. These are privacy requirements,
not a new on-chain biometric format or proof of unique humanity.

## 3. Anchoring, withdrawal and compromise

CREDENTIAL_ANCHOR is LIP-0005 action **`0x09`**, payload version `0x01`.
The commitment is the W6 content address: **SHA-256 of the canonical
`{payload,signature}` signed form**, not the bare payload or its typed
signing digest. The anchor height bounds the existence of the signature
only because the commitment covers that signature. A payload-digest-only
anchor never proves a credential was signed before compromise. Locators `0x00`, `0x01` and
`0x05` of LIP-0033 are admitted; `0x01` pins the signed form's content
address and `0x05` the exact Nostr event id. A reader checks the anchor on
its own node at its configured confirmation depth. `credential_id` is
W6.1's SHA-256 of the canonical payload. No undefined `issuer_name_hash`
is mixed into either value.

An eternal credential has no revocation seal. Its issuer key must have
been authorized by the pinned issuer at the confirmed anchor's chain
position, read through LIP-0021 section 7.6. Later ordinary key rotation,
expiry or transfer does not erase that historical fact. Its optional end
height still applies. A revocable credential additionally requires the
same pinned issuer and key current at the tip, and its seal unspent in
the node's mempool and chain view. Rotation therefore requires reissue
of revocable credentials; it does not reissue eternal ones.

A validated spend of a revocable credential's seal durably revokes it,
from first sight, following protocol/revocation.md. For cause has its own
action **`0x0a`**, version `0x01`, not LIP-0014's action `0x05`. Its
commitment is the typed digest of an unsigned payload of type
`swarma-credential-withdrawal/1`, exactly `type`, `genesis`, `credential_id`
and `cause_sha256` (three hashes). At most 512 bytes, W1/W2 canonical
encoding; locators `0x00`, `0x01` or `0x05`, pointing to this payload when
a location is given. The same transaction spends the credential's seal.
That spend authenticates the withdrawal; there is no detached signature.
A valid matching cause record gives `CRED_REVOKED_FOR_CAUSE`; missing or
invalid cause evidence never cancels the ordinary `CRED_REVOKED` spend.
Cause bytes are off chain and need not expose private facts publicly.

At an emergency closure the issuer declares compromise height `h_c` in
the **break transaction**, authenticated by the name-owner key, not by the
compromised credential key. The proposed commitment action is `0x0b`,
version `0x01`, locator `0x00`, committing to the typed digest of
`swarma-credential-break/1`. Its action-specific payload is exactly
`version(1) || typed_digest(32) || h_c_le64(8) || location_type(1)`.
`h_c_le64` is the compromise height as an unsigned eight-byte little-endian
integer, no greater than 9007199254740991; a larger value or a height
later than inclusion refuses `CRED_BREAK_INVALID` in the break reader and
records no closure. The script is exactly 48 bytes:
`6a 03 53 4c 0b 2a 01 <digest:32> <h_c:8 little endian> 00`.
This extends the break action only, not any existing action's payload. That unsigned payload, at most 1024 bytes,
has exactly `type`, `genesis`, `issuer`, `issuer_key`, `name_input`, `h_c`:
issuer/key forms as above, `name_input` an outpoint, `h_c` a W2 number-form
height. `issuer_key` MAY be any credential key authorized in the verified
history of this exact registration and pinned owner, current or retired.
The transaction spends the current issuer-name output irrespective of its
current `cred`. It MUST replace/remove `cred` if it equals `issuer_key`;
otherwise it MAY retain the different current key. A retired compromised
key MUST NOT be republished merely to make a break possible. Its bound
owner's signature must be the supported `SIGHASH_ALL` without
`ANYONECANPAY` of LIP-0021 O4.4, committing to every output and thus the
break frame. The reader reconstructs the payload from the spent issuer
name/history, name input and the on-chain `h_c`, testing the historically
authorized credential keys of that registration and pinned owner, and
requires exactly one reconstructed typed digest to match. An unavailable
or incomplete history refuses `CRED_ISSUER_HISTORY_UNAVAILABLE`; an
unauthorized key or no matching digest is `CRED_BREAK_INVALID`. Thus withholding an off-chain break
document cannot hide the compromise height or turn a break into an ordinary
rotation. No off-chain assertion of a height is sufficient.

LIP-0021 section 7.6 defines the verified history read and journal. For
that key and pinned issuer, anchor height **below** `h_c` stays valid;
height **at or above** `h_c` refuses `CRED_ISSUER_CLOSED`, for either
lifecycle. The threshold is at most the break's confirmed height (or the
candidate height for a validated mempool break). It is never inferred
from a timestamp. Validated closures are durable across reorganisation;
multiple breaks narrow by the smallest authenticated `h_c`, never widen.
Choosing `h_c` too late preserves earlier forgeries: this is the explicit
security cost of preserving historical documents. No credential break
is silently treated as a grant's `ISSUER_NAME_CLOSED` event.

## 4. Deterministic verification and refusals

The first failure wins, in this order:

1. LIP-0020 W9.1 to W9.3 document pipeline: its actual `WIRE_*` codes for
   size, JSON, duplicates, values, integers, strings, canonical bytes,
   type/members, key/signature form and BIP-340 signature. Lifecycle
   presence rules and window ordering are schema checks, `WIRE_MEMBER`.
2. Kind and application claims: `CRED_KIND`, then `CRED_CLAIMS`.
3. Chain/genesis and subject binding: `CRED_BINDING`.
4. The earliest confirmed matching signed-form anchor in the active chain,
   its frame, commitment and required depth (later re-anchors cannot change
   its compromise-height result):
   `CRED_ANCHOR_MISSING`; an unavailable node proves nothing and gives
   `CRED_ISSUER_HISTORY_UNAVAILABLE`, not a missing anchor.
5. Issuer registration/owner/key at the required historical position or
   tip: `CRED_ISSUER_KEY`; unavailable/unsupported history is
   `CRED_ISSUER_HISTORY_UNAVAILABLE`. Then the authenticated compromise
   journal: `CRED_ISSUER_CLOSED`.
6. Current height outside the half-open window: `CRED_WINDOW`.
7. Revocable seal state: `CRED_REVOKED_FOR_CAUSE` if the spend and matching
   cause record verify, otherwise `CRED_REVOKED` for a validated spend;
   unavailable seal evidence is `CRED_SEAL_UNAVAILABLE`, never unspent.

For `/2` contract notarization the order is wire pipeline, supported
contract profile (`NOTARY_CONTRACT_PROFILE`), contract/party/chain binding
(`NOTARY_CONTRACT_MISMATCH`), confirmed matching anchor (`NOTARY_ANCHOR`),
current pinned notary key/history (LIP-0014/LIP-0021 codes), then the
notary-seal withdrawal checks of LIP-0014. A child kind awaits its complete
schema and keeps the existing child-check order, not this contract order.

## Alternatives and security consequences

Reusing `swarma.notary.attest` is rejected: LIP-0010 section 9 rotation
refuses old attestations, incompatible with eternal credentials. Keeping
two human-verification objects is rejected. Universal retroactive
revocation would erase valid diplomas; no compromise closure would preserve
all forgeries. The owner chose the height boundary instead. A credential
is never a grant, and policy may only narrow what its claims admit.

## Conformance impact and extension checklist

This is a Draft. Vectors are **not required for Draft LIPs**. Adoption
needs paired valid and refused cases for each lifecycle, exact canonical
bytes and all hashes, wrong-chain/issuer/registration, anchor-before-key,
rotation survival, rotation followed by a break of the retired key,
payload-digest-only pre-anchors whose signatures were made later (refused),
a later duplicate anchor that cannot invalidate the earliest one, malformed
break heights above the W2 bound, compromise at `h_c - 1`, `h_c` and `h_c + 1`, unauthorized
break declarations, seal spends with and without cause, and unavailable
history. The boundary cases must prove that `h_c` itself refuses while the
valid prior anchor survives. No existing checker covers these new types.

LIP-0018 checklist and LIP-0020's new-type rule: identifiers, signers,
schemas, bounds and digests are sections 1 to 3; bindings and refusal
order are sections 3 and 4; alternatives/security and adoption are above.
This adds no contract profile, limit kind, action leaf or certificate-subject
kind; those specialized checklist items do not apply. Open byte contracts
are named explicitly, not supplied as conformance vectors.

## Open questions

- The co-author's agreement on these decisions and the amended name/key rules.
- Exact `/2` child member mapping under J5/J2, contract-notarization
  for-cause semantics, and supported general contract canonical profiles.
- Per-claim salted/Merkle selective-disclosure bytes and proofs; application
  kind schemas, `supersedes` for corrected deeds/diplomas, and storage privacy.
- Credential-seal construction profiles and independent implementations of
  the owner-authenticated break/history read before adoption.
