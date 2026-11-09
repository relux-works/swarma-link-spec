# Changelog

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
