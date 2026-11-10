# Changelog

## 0.1.8 — 2026-11-10

Adds Draft LIP-0007 for service types/actions and typed name self-declaration,
and Draft LIP-0008 for Grant v4: directly signed rental limits, mirrored
contract terms, operator-wide ceilings and name recipients pinned to current
output ownership before channel-key checks. Includes v3 compatibility and a
semantic conformance outline; exact wire bytes, ownership proofs and accounting
profiles remain open. Binds closure to exact name outputs, including renewals;
scopes budgets/single use to concrete executors with shared replica journals.
Records proposed 60/90-minute risk cutoffs alongside node health and corrects
LIP-0003's seal-time inference as an acceptance rule, with a recent-block
commitment proposed for v4. Proposes witness-only seal/issuance funding inputs
for txid stability, with an explicit gap for current P2PKH funding and fail-closed liveness
boundaries. No implementation claim, normative adoption or historical
conformance change.

Second design review adds registration-instance pins across grant, agent pointer
and verifier; typed signing from validated full objects; durable validated
issuer-branch mempool closure; confirmation minima; dependent T/L/A issuance and
the SW1 candidate; topology/trust boundaries and per-seal keys. Plans JCS exact
unit schemas, canonical/signature/error/state vectors, runner and independent
Swift verification. Static signing audit found both issuer paths recompute authenticated contract
hashes, with no demonstrated oracle. Matched role/version migration and
wire/profile decisions remain open; historical v0.1 is frozen, including its documented false closures.

## 0.1.7 — 2026-11-10

Defines the common grant-gated service term and examples in LIP-0006. Records
delegated grant issuance as a capability requiring a separate authority and
delegation profile, outside wallet v1 and the current rental rehearsal. No new
wire action, normative adoption or conformance change.

## 0.1.6 — 2026-11-10

Adds an informative key map for the rental path and wallet service: separate
custodians, signing roles, rotation dependencies and compromise limits, with
a schematic authority diagram. Model caps are identified as signed contract
terms, without claiming the proposed integration is landed. No normative
change or proposal adoption. Historical profiles and evidence remain unchanged.

## 0.1.5 — 2026-11-10

Clarifies LIP-0004 section 6 after the main issuance funding fix: the V2 route
prepares framed main issuance plans with explicit pins and fees; the v1 payment
route remains regtest-only. Describes offline regression coverage and its
regtest observation projections without claiming mainnet qualification or
extending historical conformance evidence. No normative change or proposal
adoption.

## 0.1.4 — 2026-11-10

Reconciles Draft LIP-0004/0005 with the landed 72-byte issuance writer, exact
bare-commitment compatibility and completed-plan replay boundaries. Describes
optional typed social metadata in authority names and the separate discovery
mirror without granting it authority; removes unsupported blob/tracker name
field suggestions. Adds LIP-0006 (Draft), recording the wallet service v1 request,
unsigned single-use commitment, signed/pinned reads, reserved receive allocation,
receipts and recovery semantics. Historical LIP-0002 and v0.1 conformance evidence
are unchanged. No normative change or proposal adoption.

## 0.1.3 — 2026-11-09

Adds LIP-0004 (Draft): landlord grants — the agent name holds only its messaging key and a
pointer to its landlord; the landlord's grant key signs grants v3 that carry the renter's signed
consent event and the landlord's countersignature; one mandatory on-chain commitment per grant;
funding never from the seal script. Adds LIP-0005 (Draft): an OP_RETURN locator micro-protocol
(own protocol id, action, location type and pointer), with the bare v0.1 anchor kept as legacy.
No normative change.

## 0.1.2 — 2026-11-09

Adds LIP-0003 (Draft): detached grants under an agent identity — the agent's name
holds only its keys; each grant is a certificate signed by the grant key with its
own seal and validity window; no per-grant transaction; closure on seal spend or
grant-key rotation. RELEASE.md renders LICENSE-MIT too. No normative change.

## 0.1.1 — 2026-11-09

Improvement proposals are now Link Improvement Proposals (LIPs): `cips/` is
`lips/`, CIP-0001 is LIP-0001 and CIP-0002 is LIP-0002. No normative change.

## 0.1.0 — 2026-11-08

First public draft. Names, issuance, observation and revocation as proved by
the first Namecoin mainnet experiment; conformance cases and mainnet vectors;
decisions 0001-0002; CIP-0001 (process) and CIP-0002 (single-use grants,
Draft, with regtest and mainnet evidence).
