# LIP-0007: Service types and self-declaration

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** service discovery and action vocabulary; builds on LIP-0006

## Summary

A grant-gated service declares its type, supported actions, receipt public key
and endpoint in a typed member of its Namecoin name value. A client can discover
an interface without mistaking the declaration for permission to act. A grant
and the selected action profile still control admission.

This proposal does not adopt a normative profile or extend the existing closed
name parsers. Member spelling, canonical encoding and action schemas need a
profile before interoperable publication.

## Motivation

A wallet, a model proxy and a repository service perform different effects.
A common term does not give them a common action schema. A type identifier lets
a client select the correct schema and identify unsupported operations before
sending a signed request or credentials.

## Current state

LIP-0006 describes the experimental `wallet.nmc` v1 service and its exact five
actions. LIP-0004 records separate, strict authority and discovery name values.
Neither parser accepts the new service declaration described here. This draft
introduces no implementation, deployment or historical conformance evidence.

## Proposal

### 1. Type identifiers and action tables

A type identifies an action family, not an operator, endpoint or trusted key.
The following table proposes initial identifiers and the actions their future
profiles need to define. Only the wallet v1 row records an existing action set;
the other rows are semantic candidates, not accepted wire action strings.

| Type | Actions and required boundary |
| --- | --- |
| `wallet.nmc` | Existing v1: `balance`, `history`, `receive`, `budget`, `spend`; retain their current grant, proof and receipt rules. |
| `model.proxy` | Invoke an explicitly selected model; account for requests, input/output tokens, cost and per-request output. |
| `slot.station` | Admit access to a named rental slot/station and end access; bind the renter, resources and rental window. |
| `mail.send` | Send mail; bind sender identity, allowed recipients and sending limits. |
| `store.blob` | Read, write and remove objects; bind the allowed object namespace and resource limits. |
| `names.nmc` | Register and update names; bind permitted names, operation stages, fees and ownership policy. |
| `repo.git` | Read or push to a repository; bind repository identity, refs and allowed mutations. |

Delegated issuance needs a separate type/action profile: no listed action implicitly permits
issuing grants or passing authority onward.

The wallet-v1 wire action `spend` maps to the existing grant-scope/executor
verb `pay` under LIP-0006. This table does not rename that internal authority
or change the wallet request schema.

Each type profile defines exact action identifiers, parameters, target binding,
units, admission, repeat handling, journal reservation, receipts and recovery.
Unsupported types or actions refuse. A shared word such as "read" is not a
substitute for the service's exact schema. New types or action meanings arrive
through separate LIPs; changing a deployed type's meaning silently is excluded.

For the proposed v4 registry, a capability binds a subject, exact command and
applicable policy/constraints under [LIP-0008 section 12](LIP-0008-grant-v4.md#12-invocation-and-bounded-issuance-capability-chains).
Command names MUST use lowercase slash-separated segments and exact leaf
matching; a prefix or top command `/` grants nothing. The `swarma/` namespace
is reserved for protocol-defined capabilities, not provider extensions.
Exact grammar, leaf assignments and mapping from existing actions remain open.
This does not rename wallet-v1 actions, adopt a policy evaluator or expand any
existing closed parser. Registry additions still require separate profiles/LIPs.

### 2. Concrete executors and budget scope

A type selects an interface; it does not identify an executor. The Grant v4
proposal in LIP-0008 binds a concrete service's Namecoin name and public key,
assigns that executor its signed budget, and requires a single-use request to
commit its chosen executor. Multiple executors need explicit partitions rather
than each receiving the full apparent budget. Replicas of one executor share
one authoritative journal/accounting state; separate local journals do not
provide cross-replica single use or budget enforcement. This is proposed v4
behaviour, not an added wallet-v1 request field or type-declaration guarantee.

### 3. Typed name-value member

The service declaration is a typed member within the service's Namecoin name
value. It has these logical members; this table is not a JSON byte fixture:

| Logical member | Meaning |
| --- | --- |
| `type` | One exact service type selecting its profile. |
| `actions` | Supported subset of that type's defined actions. |
| Receipt key | Public key for verifying this service's signed receipts. |
| `endpoint` | Address of the service interface under its transport profile. |

The containing member path, spelling of the receipt-key field, key algorithm,
canonical field order, multiplicity and versioning remain open. A profile must
fit the complete Namecoin value within the chain's size limit and specify how
it coexists with authority and channel descriptors. An existing strict consumer
must not be assumed to ignore this member; publish only after compatible
consumers and an explicit value profile exist.

### 4. Discovery and trust

A client verifies the current name binding, expiry and freshness using its
pinned chain/network view. It selects a known type and checks that the requested
action is both defined by the profile and declared by the service. The service
then checks the grant and request at its own effect boundary. Advertisement
alone supplies neither a grant nor evidence that the service keeps its promise.

A receipt key read from an arbitrary name or response is not automatically a
trusted pin. The client first establishes which service name and ownership
policy it trusts, then binds the advertised key under that policy. Under v4 this
includes the independently pinned registration instance and owner key; a
re-registration or an endpoint response cannot supply replacement trust pins.
The issuer/agent/verifier pin and renewal rules are in LIP-0008. Key changes
require the profile's rotation and journal rules; changing a declaration cannot
silently make old receipts or consumed reservations valid under a new key.

An advertised type cannot select a weaker admission profile. Anchored admission
and an explicit no-block-wait profile have different publication evidence and
need separate signed selection under LIP-0008; unavailable chain evidence
never enables a fallback.

The endpoint is untrusted discovery data. A transport profile must constrain
schemes, destination access, peer identity and TLS where applicable. Reading a
value does not contact its endpoint or forward credentials. Redirects and
service-name transfers cannot silently change a client's trusted peer.

## Alternatives

Separate hard-coded endpoints avoid a common discovery member but need another
way to bind type and receipt key. A universal command broker needs a broader
effect and authority model than these service-specific action tables. Naming
a type after an operator confuses interface selection with trust in that operator.

## Security consequences

A malicious operator can advertise actions it cannot perform, a stolen receipt
key or an attacker endpoint. The declaration proves only what the observed name
value says under the verified ownership policy. Grant checks, independent pins,
OS custody, effects and usage accounting remain separate boundaries. A valid
receipt proves a signed service statement, not independent completion evidence.

## Conformance impact

No normative conformance class changes. A future vector set pairs valid typed
lookup and authenticated service requests with unknown types/actions, malformed
or duplicate members, unsupported key/transport profiles, stale/expired names,
changed receipt keys, untrusted endpoints and declarations that advertise an
action absent from the grant. Rejected discovery must cause no connection,
credential forwarding or effect. A valid nearby request must remain admissible.

## Open questions

- Exact member path, wire spelling, canonical bytes, key/endpoint profiles and
  complete-value size budget; integration with existing closed parsers.
- Versioning and multi-service names; precise non-wallet action schemas and
  a separate type/action profile for delegated issuance.
- Lowercase slash-command grammar, reserved `swarma/` leaf assignments and
  legacy-action mappings aligned with LIP-0008; exact declaration/version bytes.
- Trust provisioning, name/receipt-key rotation, old receipt verification and
  durable journal migration; remote transport and endpoint access policy.
- Decision record, normative adoption and profile-specific public vectors.
