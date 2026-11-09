# Changelog

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
