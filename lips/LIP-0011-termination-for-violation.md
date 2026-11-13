# LIP-0011: Termination for violation

- **Status:** Draft
- **Created:** 2026-11-11
- **Affects:** the contract, the revocation transaction, the `OP_RETURN`
  actions of LIP-0005
- **Builds on:** LIP-0004, LIP-0005 and LIP-0008

## Summary

A contract can end early because the recipient broke its rules. This LIP
makes that ending checkable by a third party. The contract carries the hash
of the moderation rules and names who applies them. Each violation is a
signed verdict record. The transaction that spends the seal carries a
reference to the verdict, in the same `OP_RETURN` frame in which the issuance
transaction refers to the contract.

The seal spend still closes the grant by itself. The reference adds evidence:
it lets the recipient and an arbiter find the verdict behind a termination
and check it against the contract both parties signed.

Nothing in this LIP is implemented. It proposes semantics and one frame
layout, without canonical bytes for the records.

## Decisions recorded

Ivan Oparin decided the following on 2026-11-11. The LIP stays Draft until
the co-author agrees; adoption follows LIP-0001.

| Decision | Direction |
| --- | --- |
| V1. Rules in the contract | The contract carries the hash of the moderation rules and names who applies them. The applier can be a model or a person. |
| V2. Verdict record | Each violation is a signed verdict record with the request hash, the violated rule and the hash of the moderator's response. |
| V3. Reference on chain | The seal spend references that verdict in `OP_RETURN`, the same way the issuance references the contract. |
| V4. Refund | Whether a prepayment is refunded depends on the contract. It is not a rule of the protocol. |

The four directions are the owner's. Everything else in this LIP is the
draft's proposal and is not decided: the chain of previous verdicts, the
record's fields beyond the three items of V2 (the request hash, the
violated rule and the response hash), the action number, the
commitment formula and its prefix, the evidence states of section 4 and the
reader's ordered checks.

## Motivation

An issuer can always spend a seal: it holds the seal key. Without a record,
the recipient cannot show whether a termination followed the contract or was
arbitrary, and the issuer cannot show that it followed the rules. A signed
verdict that names the rule, the request and the moderator's answer gives
both sides something to present.

## Current state

In the reference rental path at `swarma-chain-lab`
`839bdcca41cd17ffd7c4057de2dc88a521745515` the gateway counts explicit
refusals of its content check and ends the slot at the second one. That
counter is local to the gateway. The signer service accepts a revoke request
from the booking service for reason `payment_reorged` and from the operator's
private source for reason `operator`; it has no reason for a violation. The
contract has no field for moderation rules. The revocation transaction spends
the seal and carries no `OP_RETURN`.

So a violation today ends the slot on the issuer's machine. It does not end
the grant on chain, and it leaves no record that binds the ending to a rule.

## Proposal

### 1. Contract terms

The contract gains two terms. Both parties' consent covers them through the
contract hash, like every other term.

| Term | Meaning |
| --- | --- |
| Rules hash | SHA-256 of the exact bytes of the moderation rules text. The text says what counts as a violation and which violation ends the contract, for example the second one. |
| Moderator | The key that signs verdict records, and the kind of applier behind it: a model or a person. For a model the contract also names the model and the hash of its configuration. |

The moderator can be the issuer's own service or another party. A person and
a model are equal in this LIP: each verdict is signed with the moderator key.
When the applier is a model, the key is held by the service that runs the
model and by that service's operator; the model does not hold it. The model
name and configuration hash in the contract are that operator's claim about
what ran. They are not a proof of execution.
The protocol binds the hash of the rules and never interprets the text.

Field names and their place in the contract's canonical bytes are open. The
terms belong to the v4 contract profile; the v2 contract of the landlord
profile is not extended.

### 2. Verdict record

A verdict record is a signed object of its own type under LIP-0008 section 8.
It has these logical fields; the table is not a byte fixture:

| Field | Meaning |
| --- | --- |
| Grant | The `grant_id` the verdict belongs to. |
| Contract | The `contract_sha256` of that grant. |
| Rules hash | Equal to the rules hash in the contract. |
| Violated rule | The identifier of one rule inside the rules text. |
| Request hash | SHA-256 of the exact bytes of the request that was judged, as the service profile defines them. |
| Response hash | SHA-256 of the exact bytes of the moderator's response: the model's output, or the person's written decision. |
| Ordinal and previous verdict | The number of this verdict for the grant, starting at 1, and the identifier of the previous verdict, absent for the first. |
| Height | The height of the tip the moderator's node validated when the verdict was made. It is a claim of the signer. |
| Moderator | The moderator key; for a model, the model name and configuration hash named in the contract. |
| Signature | A BIP-340 signature by the moderator key over the record's typed digest. |

`verdict_id` is the SHA-256 of the canonical signed record.

The record holds hashes, never the request or the response. Their bytes stay
with the parties. In a dispute a party discloses them, and anyone recomputes
the two hashes. Where the service profile has the recipient sign the request
bytes themselves, a disclosed request also shows who sent it. That does not
hold for every profile: section 7 states a case in which the bytes that
were judged carry no signature, and holds Draft text for it, under a
pending owner decision (J8).

Verdicts for one grant form a chain through the previous-verdict field. The
last one commits to the bytes of the earlier ones: a termination after the
second violation refers to the second verdict, and the first is named by it.
The commitment does not replace the earlier records. A reader fetches each
predecessor and checks it like the last one: grant, contract, rules hash,
moderator key, signature and an ordinal lower by one. The chain proves
neither that a judgement is right nor that an earlier record is still
available. What counts as a separate violation, for example two verdicts on
one request that was sent twice, is a matter of the rules text and is open.

### 3. The reference in the seal spend

The transaction that spends the seal for a violation carries exactly one
zero-value `OP_RETURN` output in the LIP-0005 frame, with a new action:

| Action | Name | Payload |
| --- | --- | --- |
| `0x03` | termination for violation | `version(1) || termination_commitment(32) || locator` |

The commitment binds the grant, the contract and the verdict:

```text
termination_commitment = SHA-256( "swarma-terminate-v1" || grant_id
                                  || contract_sha256 || verdict_id )
```

The preimage is raw bytes with no lengths or separators: the 19-byte ASCII
prefix followed by three decoded 32-byte values, 115 bytes in all. The
locator has type `0x01`, a content-addressed blob store, and its pointer is
`verdict_id`. The script is 72 bytes, the same length as an issuance script:

```text
6a 03 53 4c 03 42 01 <termination_commitment:32> 01 <verdict_id:32>

offset    contents
0         OP_RETURN (6a)
1         direct push of 3 bytes (03)
2-3       protocol SL (53 4c)
4         termination action (03)
5         direct push of 66 bytes (42)
6         payload version (01)
7-38      termination commitment (32 bytes)
39        blob location (01)
40-71     verdict_id (32 bytes)
```

The issuance commitment of LIP-0004 binds the contract into the transaction
that starts the grant. This commitment binds the same contract, with the
verdict, into the transaction that ends it.

The output adds 81 bytes to the revocation transaction: 8 for the amount, 1
for the script length and 72 for the script. The prefix form follows
LIP-0004; the typed-hash plan of LIP-0008 section 8 may replace it before
adoption.

### 4. Rules

1. Closure does not depend on the reference. A verifier closes a grant on
   the issuer's spend of its seal under the existing rules, whatever outputs
   that transaction has. A verifier MUST NOT keep a grant open because the
   `OP_RETURN` is absent, malformed, or points to a record it cannot fetch.
2. The reference is evidence for the parties and an arbiter. A reader does
   not assume that the transaction was built by a signer that followed
   rule 3. It checks, in this order:
   1. the grant and its contract, authenticated on their own: the grant's
      signature and issuance under its profile, its `grant_id`, its
      `contract_sha256`, and the seal outpoint the grant names;
   2. that the transaction which carries the frame spends exactly that seal
      outpoint, and spends it under the issuer's authorization for that
      seal. For a seal with a recipient branch, a spend through the
      recipient's branch is a use of the grant and is not termination
      evidence, whatever outputs it carries;
   3. the exact frame and action, and that the frame is the only
      `OP_RETURN` output;
   4. the commitment recomputed from `grant_id`, `contract_sha256` and
      `verdict_id`;
   5. that the fetched record hashes to `verdict_id`;
   6. the record's grant, contract and rules hash against the contract;
   7. the signature under the moderator key that the contract names;
   8. every previous verdict, as section 2 describes.

   A well-formed frame in a transaction that fails check 2 is not evidence
   about that grant. It neither terminates the grant nor shows a
   termination: the grant's seal is unspent, or was spent by another
   transaction, or was spent by this transaction through the recipient's
   branch.
3. The signer verifies the same facts before it spends the seal, and writes
   the verdict identifier into its journal before the first signature. It
   spends only the seal that is bound to that grant.
4. The evidence has one of four states for a reader, and closure is the same
   in all of them:

   | State | When | What it shows |
   | --- | --- | --- |
   | Verified | Every check of rule 2 passed. | The issuer ended the grant with a verdict signed by the contract's moderator under the contract's rules. |
   | Invalid | The reader holds the bytes and a check of rule 2 fails: the frame, the commitment, the record hash, a field, the signature or a predecessor. | The reference does not support the termination. |
   | Absent | The issuer spent the seal and the transaction carries no action `0x03` frame. | A revocation with no verdict claimed on chain (rule 6). |
   | Not established | The reader could not fetch the record or a predecessor, or could not read the transaction. | Nothing. The reader has no evidence in either direction. |

   A reader MUST NOT report the state "not established" as invalid, as
   absent, or as a termination without cause. A failed fetch is a fact about
   the reader's storage path. When the record is fetched later, the state
   becomes verified or invalid; the facts of the contract did not change in
   between. What each state means for cause and for refund is a term of the
   contract. This LIP supplies no default consequence for any of them.
5. A verdict closes nothing. Only the seal spend ends the grant. A verdict
   that does not end the contract, such as a first warning, is recorded and
   delivered to the recipient and needs no transaction.
6. A revocation for another reason keeps today's plain spend. This LIP
   defines no reference for it.

### 5. The whole flow

| Step | Where | Who acts | What appears |
| ---: | --- | --- | --- |
| 1 | Off chain | Issuer and recipient | The contract with the rules hash and the moderator; both sign it. |
| 2 | On chain | Issuer's signer | The issuance transaction with the issuance commitment; the seal stays unspent. |
| 3 | Off chain | Recipient | A request signed by the recipient's request key. |
| 4 | Off chain | Moderator, a model or a person | The response to that request under the rules. |
| 5 | Off chain | Moderator | A verdict record with the request hash, the violated rule and the response hash, signed and stored under `verdict_id`. |
| 6 | Off chain | Issuer's service | The verdict identifier delivered to the recipient. A verdict that does not end the contract stops here. |
| 7 | Off chain | Issuer's signer | The verdict checked against the contract and journalled. |
| 8 | On chain | Issuer's signer | The seal spend with the termination reference. |
| 9 | On chain, read by each verifier | Verifiers | Closure of the grant on the seal spend, in the mempool or in a block. |
| 10 | Off chain | Recipient or arbiter | The path back: the grant and its seal outpoint, the transaction that spends that seal under the issuer's authorization, commitment, verdict record and its predecessors, request and response hashes, disclosed bytes, rules hash, rules text. |
| 11 | Off chain | Parties | Refund or no refund, as the contract says. |

Steps 3 to 6 repeat for every violation. Steps 7 to 9 happen once.

### 6. Refund

Whether the issuer returns a prepayment after a termination, in full, in part
or not at all, is a term of the contract. The protocol provides the evidence
on which that term is applied and prescribes no refund.

### 7. The request as evidence

Owner decision pending: J8. Every rule of this section is Draft text, for
v4 only. Until the decision the request bytes of a verdict are what the
service profile defines (section 2), and one profile is known to break the
assumption that a disclosed request shows its sender: a renter's message in
the rental profile, which travels under NIP-17 and NIP-59. There the sender
signs the seal event, whose content is the encrypted message; the message
itself is an unsigned event inside the seal. A hash of the readable message
is then a hash of bytes nobody signed, and the message proves its sender
only together with the signed seal and the means to decrypt it.

Under this section the request of a verdict is the signed invocation of
LIP-0008 section 12.1. v4 requires a signed invocation for every request,
and a rental message is not exempt: the signed invocation travels inside
the encrypted message, its arguments bind the content to be judged, and the
verdict's request hash is the invocation's identity. One object serves
authorization and evidence. The rental invocation gains one argument, the
salted hash of the message content, and a salt travels beside the content.
No object type is added. The service keeps a record for every request it
admitted. No v3 request-evidence object is defined: the terms of this LIP
belong to the v4 contract profile (section 1).

The salted content hash that rule J8.3 binds is:

```text
salted_content_hash = SHA-256( salt || content )
```

`content` is the exact octets to be judged. `salt` is 32 bytes that travel
beside the content and outside the invocation.

| # | Rule | Refusal or result |
| --- | --- | --- |
| J8.1 | For every service profile the request bytes of a verdict are a signed invocation, and the request hash is that invocation's object ID under LIP-0008 section 8.1. That the service admitted the invocation is a statement of the service under J8.6 and not a property of those bytes. | none of its own |
| J8.2 | A signature of a transport over ciphertext or over a wrapper, the NIP-59 seal and wrap included, is not request evidence. A verdict MUST NOT cite the hash of a plaintext, of an inner event, of a seal or of a wrap. | Attribution invalid (J8.5) |
| J8.3 | A profile whose requests travel inside an encrypted message MUST carry the signed invocation inside the plaintext. The invocation's arguments MUST bind the salted content hash that the formula above the table defines. Duties of the sender: the invocation's nonce and the salt are each 32 bytes from a cryptographically secure generator, and neither leaves the sender except inside the encrypted message. The salt is drawn separately and fresh for each request. It MUST NOT equal the nonce, MUST NOT be derived from the nonce or from any field of the invocation, MUST NOT be derivable from anything that a holder of the invocation sees, and MUST NOT be used for a second request. Two separate draws of the generator for each request meet this; one draw used for both does not, because the nonce is in the invocation. Checks of the receiver: canonical length and encoding, the signature over every bound field, expiry and replay; and, on the live path after decryption and before admission or any call to a moderator, that the salt and the content that travelled beside the invocation hash to the bound value. A receiver cannot tell how a value was made, nor from one message whether a salt was independent, and MUST NOT report that it did. | A mismatch of salt and content with the bound value refuses the message as a request |
| J8.4 | The invocation is signed by the sender's own key holder before the content is encrypted: a person's client, or an agent's key holder under LIP-0013 section 3.6. The receiving service, a relay and a moderator MUST NOT sign an invocation for a sender, MUST NOT build one from unsigned content, and MUST NOT give a moderator content that no admitted invocation binds. The bytes do not show who operated the key. | A message without a valid invocation is refused as a request and is never judged as one |
| J8.5 | A reader reports five results apart and never one in place of another. (1) Reference: the four states of section 4 rule 4, by the checks of rule 2, unchanged. (2) Attribution: the disclosed invocation is canonical, its signature verifies, and the disclosed salt and content hash to the bound value; it is established, invalid, or not established when bytes are missing. (3) Eligibility: the signing key is the grant's request key, or, for a recipient by name, a key that the name listed for the channel under the bound owner at a height inside the grant's window; and the invocation's type and version, subject, command, executor and ordered proof path are those of the verdict's grant and contract. A key outside the window, another owner, another executor or another path fail this. (4) Admission: what the service's record of J8.6 states, always labelled as the service's statement. (5) Time and delivery: not established by any of the above. The reader MUST NOT conclude from `iat`, from the verdict's height or from the key's listing when the request was signed, received or admitted. The audit does not run today's admission: an expired invocation and a key that was rotated since are no reasons to reject old evidence. And the audit authorizes nothing: no result of it admits a request or resets a journal. | The five results |
| J8.6 | A service whose contract carries moderation terms MUST keep, with every admitted invocation, the tip it validated, the recipient mode with the name and owner evidence it used, the key it verified under, the proof path and the result of its nonce journal. That record is a statement of the service and is reported as such. | none of its own |
| J8.7 | Missing request bytes leave attribution "not established" and leave the reference state as the checks of rule 2 found it. Wrong bytes or a wrong signature make attribution invalid and do not make the reference invalid. No result changes a closure (rules 1 and 4). | The results named |
| J8.8 | The privacy notice that the consent signs MUST say that requests under the grant are signed and can be disclosed to the moderator and to an arbiter. | none of its own |

What a disclosure then shows, and to whom. A reader that holds the
disclosed invocation, salt and content sees that the request bytes of the
verdict are bytes that a key signed, and that the judged content is the
content those bytes bind. A reader that also holds the grant, and for a
recipient by name has the name's history on its node, sees that the key was
a request key of the verdict's grant and that the invocation is bound to
that grant, subject, command, executor and proof path. Four things are not
shown:

- **Admission.** That the service admitted this request, and when, is a
  statement of the service, which it must keep (J8.6).
- **Time and delivery.** When the request was signed, and that it was
  delivered, is shown by nothing here. A stolen request key signs
  attributable requests with any `iat`. A renter who replaced a key because
  it leaked is not protected against a request signed with the old key
  afterwards; the service's record speaks against it only as far as the
  service is believed.
- **The operator of the key.** Two holders of one key produce the same
  bytes. A request under a moderated grant can be shown to carry a
  signature of a key of that grant, which is less than who sent it.
- **Randomness.** Whether the nonce and the salt were random and secret is
  a duty of the sender and is tested at the sender. With a random, secret
  nonce the public request hash reveals nothing. With a random salt that is
  independent of everything in the invocation, a holder of the invocation
  alone cannot test a guess of the content. A sender that fails either duty
  loses that protection, and no receiver notices.

The response hash and what counts as one violation stay open (section 2),
and the object ID waits for the bytes of LIP-0008 section 8.1.

The owners decide two things with this text. The first is the trade
itself: a request under a moderated grant carries a signature that can be
shown to a moderator and an arbiter. The proposal is to accept it, with the
notice of J8.8, whose wording is the owners'. The alternative keeps
requests deniable; a verdict can then show no signature at all, and the
case of the first paragraph stays. The second is the service's record. The
proposal is the MUST of J8.6, at the cost of storage and retention at every
moderated service; the record remains the service's own statement. As a
SHOULD, a service may have nothing to show for admission in a dispute.

Seven other designs were set aside, and none is proposed. Hashing the seal
and opening the ciphertext for the arbiter needs the conversation key,
which opens every message between the two keys, and the seal binds no
grant, nonce or executor. Signing the inner event departs from the
transport and is still no invocation. A second evidence object beside the
invocation gives two signatures per request for one fact. A v3 extension
has no use, because no verdict exists on v3. An anchor of the invocation's
ID for every request shows that the invocation existed when the anchoring
block was mined, under the chain's assumptions; anyone who holds the
invocation can anchor it, so it shows no delivery, it bounds the time of
signing from above only, and it costs one chain write per request. A
receipt signed by the service for every request is the service's signed
statement that it received the invocation, the record of J8.6 in a form
the sender can hold; its time is the service's assertion, a later holder
of the service's key can sign a receipt about an earlier time, and it costs
one countersigned object per request. A receipt that commits to a recent
block and is itself anchored shows that a holder of the service's key
acknowledged the invocation between those two blocks; it is still a
statement of that key and still not the instant at which the request was
signed, at both costs.

Cases (owner decision pending: J8). Their identifiers begin with S8, for
this decision. All are v4 cases; no implementation exists, and no result is
claimed. Today no check of request bytes exists, and vectors wait for the
preimage of the object ID:

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S8-1 | A verdict whose request hash is the object ID of a disclosed invocation; salt and content disclosed; attribution established | A verdict whose request hash is the hash of a decrypted text, of an inner event, of a seal or of a wrap: attribution invalid. The reference result of the same verdict is reported separately and is still what rule 2 finds. |
| S8-2a | The invocation verifies under the grant's request key, with the intended executor, subject and proof path | Signed by another key; citing another grant; another executor; another subject or command; a proof path in another order: attribution or eligibility fails. |
| S8-2b | At the sender's key holder: an authorized client or run obtains the signature | A process with no authority at the sender's key holder, a transport gateway for example, obtains none (LIP-0013 section 3.6). No claim is made about a party that holds the key: its invocation is indistinguishable, and a compromised key holder defeats this boundary. |
| S8-3 | The disclosed salt and content hash to the bound value | The judged content changed by one byte, with the original valid invocation and a valid moderator record: attribution invalid, reference unchanged. Octets are compared, not rendered text. The same with the salt changed by one byte: attribution invalid. With the salt missing: attribution not established. |
| S8-4 | On the service's real path: a rental message that carries a valid invocation is decrypted, admitted and passed to the moderator | A message without an invocation, or with an invalid one, is refused, and the moderator is not called. Invalid includes a validly signed invocation beside content or a salt that do not hash to the bound value: refused before the moderator is called, on the live path and not only in the later audit. |
| S8-5 | A request under `Kold`, which the name listed under the bound owner inside the window; the key rotated later; the service's record present: attribution and eligibility established, admission reported as the service's statement | The same bytes signed by a thief after the rotation with an old `iat`, with no service record: attribution and eligibility established, admission not established, time not established. A reader that rejects for the current key, one that accepts `Kold` outside the window or under another owner, and one that reports a time are all wrong. |
| S8-6 | Authentic old evidence is audited after the grant closed | A new request under the removed `Kold` with a backdated `iat` refuses live admission; a replayed nonce refuses; an audit result never admits anything. |
| S8-7 | The same invocation carried over a second transport keeps its identity and is valid evidence there | A second effect for it refuses, across transports, replicas and a restart; the nonce journal is keyed by the nonce, so a re-signed copy does not escape. |
| S8-8 | A genuine issuer seal spend with a valid reference, record and predecessors: reference verified | The request body cannot be fetched: reference still verified; attribution not established; the grant stays closed. Reporting the reference as not established, invalid or absent is wrong. |
| S8-9 | At the sender: the signing entry point makes two separate draws of the system generator for each request, one for the nonce and one for the salt, and writes neither outside the encrypted payload; the receiver accepts 32 canonical bytes and refuses a replay | Each a failure of the sender's qualification, by inspection of its generator and its logs: a counter or a public value; one draw used as nonce and as salt; a salt computed from the nonce or from another field of the invocation; a salt used for two requests. The instrumented entry point shows the draws; a test that only asks whether both values came from the generator passes the second of these and is not this case. The receiver accepts all of them, because it cannot tell. Two different hashes for two messages are no test of hiding. |

A further case, S8-10, applies only if a receipt or an anchor is ever
adopted. Its control is a request that the intended service acknowledged
with a signed receipt and whose ID is anchored. The same kind of invocation,
anchored by an unrelated holder and never delivered, MUST NOT be reported as
delivered, and a reader that takes either anchor as proof of delivery, or
the time in a receipt as the time of signing, is wrong.

## Alternatives

Leaving the violation count inside the issuer's service keeps today's
behaviour and gives the recipient nothing to check. Publishing the request
and the response on chain would let anyone judge the case; it would also
publish private content, and the bytes do not fit. Storing only the verdict
identifier without a commitment would locate the record; the commitment
additionally binds it to this grant and this contract in the transaction
itself. Letting the moderator's signature close the grant without a seal
spend would add a second closure path that every verifier must watch.

## Security consequences

The issuer can end any of its grants at any moment. This LIP does not limit
that. It makes visible a termination whose claimed cause the reference does
not support: an issuer seal spend whose reference a reader checked and found
invalid, or one that carries no reference where the issuer claimed a
violation. Whether such a termination breaks the contract is for the
contract to say (rule 4). A record that a reader could not fetch shows
nothing about the cause.

The frame is public bytes, and anyone can copy a valid frame into another
transaction. A copy proves nothing about the grant it names: the reader
requires the transaction to spend that grant's seal under the issuer's
authorization. Without that check a copied frame would attach a false
termination record to a grant that is still open.

A verdict proves that the moderator key signed that statement about those
hashes. It does not prove that the judgement is right. A model's response can
be disclosed and read; it cannot in general be reproduced.

A stolen moderator key forges verdicts. The forger still cannot spend a seal,
so no grant closes by a forged verdict alone. The contract should say how the
moderator key is replaced.

The record and the chain carry hashes only. A short request can be guessed
from its hash. A salt beside the request would prevent that; section 7
drafts one, under a pending owner decision (J8).

The reference is read after the fact. A recipient whose node never fetched
the verdict loses no protection: closure and the right to dispute it do not
depend on the storage being reachable. If the record is lost, the commitment
on chain still shows that a verdict with that identifier was claimed.

## Conformance impact

No normative conformance class changes. A future vector set pairs these
controls; each refused case leaves the closure rules untouched. Section 7
carries the cases of its Draft text, which is under a pending owner
decision (J8):

| Valid control | Refusal or invariant |
| --- | --- |
| Seal spend with a well-formed action `0x03` frame whose commitment recomputes and whose verdict verifies under the contract's moderator key | A wrong action or version, an extra `OP_RETURN`, a commitment over another grant, contract or verdict, or a pointer that differs from `verdict_id` fails the evidence check. |
| Verdict whose rules hash, grant and contract equal the contract's | A verdict for another grant or contract, another rules hash, or a signature by a key the contract does not name fails. |
| Second verdict whose previous-verdict field names the first | A broken or reordered chain, a repeated ordinal, or a predecessor that fails its own grant, contract, rules or signature check fails. |
| A valid frame for grant B in the transaction that spends B's seal by the issuer | The same frame in a transaction that spends another grant's seal, in one that spends no seal, and in a spend of B's seal through the recipient's branch is not evidence about B. B's closure follows only from its own seal. |
| Valid termination whose record is fetched and verifies | The same termination read while the record is unavailable has the state "not established", and after recovery "verified"; reporting it as without cause is wrong. A fetched record with a wrong hash or a bad signature is "invalid", a different state. |
| Issuer seal spend with a valid reference, and one without any `OP_RETURN` | Both close the grant; keeping a grant open because the reference is missing, malformed or unfetchable is wrong. |
| Disclosed request and response bytes that hash to the record's two hashes | Other bytes fail; the record alone is not accepted as proof of content. |
| A first verdict that the rules treat as a warning | No transaction is required and the grant stays open; closing on a verdict without a seal spend is wrong. |
| Person and model as moderator with the same record shape | Refusing a verdict because its applier is a person, or because it is a model, is wrong. |

## Open questions

- Canonical bytes, type tag and signing domain of the verdict record; the
  contract's field names for the rules hash and the moderator.
- The definition of the request bytes for each service profile, and a salt
  against guessing short requests (a gap found in review). Section 7 states
  the case of the rental profile and holds Draft text for both, under a
  pending owner decision (J8).
- How the rules text expresses which verdict ends the contract, and whether
  that threshold is also a machine-readable contract term.
- Replacement of the moderator key during a contract.
- Whether verdicts that end nothing are stored where the recipient can fetch
  them, and for how long.
- The fee source of the longer revocation transaction when the seal amount is
  small.
- A reference for revocations with other reasons, such as a payment conflict.
- Decision record, normative adoption and public vectors.

## Sources

- [LIP-0004](LIP-0004-landlord-grants.md) section 4, the issuance commitment;
  [LIP-0005](LIP-0005-op-return-locator.md), frame, actions and locator;
  [LIP-0008](LIP-0008-grant-v4.md) section 8, typed signing;
  [revocation](../protocol/revocation.md).
- Reference rental path at chain-lab
  `839bdcca41cd17ffd7c4057de2dc88a521745515`:
  [`signer-service/README.md`](https://github.com/relux-works/swarma-chain-lab/blob/839bdcca41cd17ffd7c4057de2dc88a521745515/experiments/signer-service/README.md),
  the accepted revoke reasons;
  [`rental-booking/README.md`](https://github.com/relux-works/swarma-chain-lab/blob/839bdcca41cd17ffd7c4057de2dc88a521745515/experiments/rental-booking/README.md),
  the revoke request fields; and
  [`rental-gateway/README.md`](https://github.com/relux-works/swarma-chain-lab/blob/839bdcca41cd17ffd7c4057de2dc88a521745515/experiments/rental-gateway/README.md),
  the content check whose second refusal ends the slot.
