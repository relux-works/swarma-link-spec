# LIP-0006: Grant-gated actions

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** action services, authenticated requests, receipts and recovery

## Summary

An agent signs a bounded action request. A separate service owns the credentials
and journal needed to perform the effect, checks current authority, reserves the
action durably, and returns a signed receipt. Delivering a command, fetching a
grant or verifying a signature alone does not authorize the effect.

This proposal separates a common service pattern from the concrete experimental
`wallet.nmc` v1 profile described below. Other services need their own actions,
parameters, budget units and effect schemas. This draft does not adopt a new
normative Swarma Link profile or alter the historical v0.1 conformance set.

### Common term and examples

A **grant-gated service** (Russian book term: *сервис по доверенности*) checks
current grant authority before an effect and keeps its execution credentials
and journal outside the client. Examples include wallet payments, model
inference, rental slots/stations, mail sending, file/blob storage, name
registration/updates and repository access.
Each needs a service-specific action and parameter contract; this list grants
no action and adds none to the implemented wallet v1 closed set.

Delegated issuance is a capability of the same pattern: a signing service can
be entrusted by a grant to issue bounded child grants. This requires explicit
issuance authority and a separate profile for child scope, recipient, lifetime,
budgets, parent closure and delegation-chain verification. Neither `deliver`
nor `pay` implies delegation. An agent's v3 messaging key gains no grant-issuing
role. This capability is outside the current rental rehearsal and the wallet
v1 actions; it has no adopted wire format or implementation claim here.
Agent-issued child grants are since decided as part of the protocol
(LIP-0008 section 12.6, 2026-11-11), and every child needs a notary
attestation ([LIP-0014](LIP-0014-notary-certified-redelegation.md),
2026-11-12). The signer capability described here still authorizes no
sub-delegation.

## Motivation

A same-user command-line checker cannot keep wallet credentials from an agent
that can read its files or call the wallet directly. Moving execution credentials
to a service permits a smaller interface: a signed request for an allowed action,
rather than arbitrary RPC, shell commands or caller-selected file paths. Actual
custody still depends on the OS permissions and deployment around that service.

## Current state

The implementation reference is
[`swarma-chain-lab` at `ca074ca645bc69d7bba41e7889504612eaa7f7d4`](https://github.com/relux-works/swarma-chain-lab/tree/ca074ca645bc69d7bba41e7889504612eaa7f7d4/experiments/agent-wallet),
especially `SERVICE.md`, `service_wire.go`, `service.go`, `service_receipt.go`,
`service_socket.go`, `service_config.go`, `service_client.go` and `single_use.go`.
It supplies `agent-walletd`, the signing socket client `agent-wallet`, and a
same-user legacy CLI. The legacy CLI provides no custody separation against its
own user. The following descriptions record landed implementation behaviour;
they are not new normative conformance requirements.

The service and wallet configurations bind Namecoin network/genesis together.
Explicit `main` and `regtest` pins are supported; omitted paired service/client
pins retain the historical regtest default. Node reads and address checks use the
configured network. Configuration support is not mainnet execution evidence or
qualification of a production installation. The public socket/Core suites are
regtest evidence under their stated fixture conditions.

## Proposal

### 1. Roles, custody and transport

One service instance binds one peer UID and one grantee key. It runs under a
dedicated non-root OS user, owning the wallet RPC configuration, grant-object
directory, journals and receipt key. The client holds its action-signing key,
socket path, expected service UID and independently pinned receipt public key.
The receipt key is distinct from the grantee key; the service rejects their
reuse. No response chooses its own trusted key. This is not a multi-tenant broker.

There is one request and one response per Unix connection. Each body has a
four-byte unsigned big-endian length prefix, then 1–65536 bytes of compact JSON.
The prefix and any terminal display newline are outside the signed wire bytes.
The server checks kernel peer credentials before reading the frame, using
`SO_PEERCRED` on Linux and `LOCAL_PEERCRED` on Darwin, and records UID/GID. The
configured connection deadline is 1–60 seconds. Peer or framing failure closes
without a signed response; a valid frame body can receive a signed refusal.

The socket is mode `0660` in a canonical service-owned `0750` directory with a
dedicated group. Startup rejects root, a peer equal to the service UID, group
zero, invalid paths and an existing socket. It does not automatically unlink a
possibly live service's socket. The client checks socket type/mode/owner and
the actual service peer UID before trusting a signed receipt. Operators provision
parent directories without client write access; private-file checks do not
claim universal protection against ancestor replacement or privileged races.

### 2. Exact request bytes and signatures

The unsigned request has exactly this field order:

```text
v, service, action, params, grant, nonce, created_at, grantee
```

`v` is integer 1 and `service` is `wallet.nmc`. `nonce` is 16 random bytes
encoded as 32 lowercase hex characters; `created_at` is positive Unix seconds
in a signed 64-bit integer; `grantee` is a 64-hex BIP-340 x-only public key.
The action and grant schemas below are closed. A signed request is carried in
an object ordered `request`, `signature`, then optional `proof`:

```text
request_hash = SHA256(canonical unsigned request bytes)
action_digest = SHA256(UTF8("swarma-action-v1") || binary32(request_hash))
signature = BIP340_sign(grantee_key, action_digest)

proof = {use_txid: <32-byte transaction id as lowercase hex>}
```

The signature is 128 lowercase hex characters. The prefix is followed directly
by the decoded 32-byte hash, with no terminator, length or separator. ASCII hex
of that hash gives a different digest. The wrapper is not the hashed request,
and the request is not a Nostr event or event ID.

The reference codec requires exact Go `encoding/json.Marshal` bytes for typed
objects: compact JSON in the field order shown, canonical decimal integers,
lowercase hex and the encoder's string escaping. No unknown, duplicate,
case-aliased, null or missing required members, alternate ordering, trailing
whitespace or extra document is accepted. A cross-language canonical format and
its complete escaping/number vectors remain adoption work; merely producing
semantically equivalent JSON does not satisfy this implementation profile.

`proof` has exactly `use_txid` and is permitted only for a single-use `spend`.
It is outside `request_hash` and the action signature. Its transaction ID is a
locator, not authority: the service independently checks the referenced spend.
Changing a well-formed proof leaves the signed request unchanged but cannot
make the wrong spend satisfy the grant.

For single use in this profile, the seal-spending transaction commits SHA-256
of these unsigned canonical request bytes. [LIP-0002](LIP-0002-single-use-grants.md)
retains its historical commitment to exact signed request-envelope bytes.
Those profiles coexist. Neither the signed wrapper nor a Nostr event ID can
substitute for this profile's unsigned request hash.

### 3. Wallet actions and grant binding

| Action | `params`, exact member order | `grant`, exact member order |
| --- | --- | --- |
| `spend` | `to`, `amount_sat`, `fee_limit_sat` | `kind`, `id`; kind `standing` or `single-use` |
| `balance`, `history`, `receive` | empty object `{}` | only `kind`, value `none` |
| `budget` | empty object `{}` | `kind`, `id`; kind `standing` or `single-use` |

`id` is the stable 32-byte grant ID in lowercase hex. It resolves only in the
service-controlled object directory, never from a request path. The decoded
grant kind and grantee match the signed request; mismatching/malformed objects
refuse. `to` is a canonical P2PKH address for the configured network.
`amount_sat` is positive atomic NMC units, at most
`21000000 * 100000000`; `fee_limit_sat` is an integer in 1–1000000. Amount plus
fee also fits that money limit. No floating-point monetary amount is accepted.

Standing spending maps to the wallet's existing `pay` executor, retaining scope,
recipient, validity-window, fee-inclusive cumulative budget, plan and signature
checks. Its exact terms object has fields `version`, `recipients`, `spend_cap_sat`,
`name_cap_sat`, `name_count` in that order. Its canonical hash matches the
grant's contract binding and consent. A complete booking contract v2 is a
different byte format; it is not automatically a wallet terms object.

The single-use grant binds the recipient and amount, its fee limit, issuer,
grantee, seal, window and authority profile. The requested amount/recipient are
exact, and the requested fee limit is no larger than the grant's. The service
checks the use transaction on its own node, including seal binding, grantee-only
signature attribution, exact unsigned-request commitment and active confirmation.
A mempool use has no spending effect. An issuer spend is revocation, even if its
hash happens to match the request.

No-grant reads still require the signed request, pinned grantee and kernel peer.
Every read checks the configured network/genesis. `budget` requires a grant but
can report `live=false`; a successful query is not spending authority.
`receive` allocates an address, so it reserves durably before allocation.
Registration, updates and other name actions are rejected. Their commit/reveal
continuations need a separate design; changing duplicate semantics is not one.

### 4. Admission, duplicate states and effect ordering

The reference service handles requests in this order:

1. Validate peer, bounded canonical schema/service/action, signature and pinned
   grantee. A poisoned/unavailable service refuses. Authentication still applies
   to duplicates.
2. Look up the durable per-grantee nonce. The same nonce with a different
   `request_hash` refuses with `NONCE_CONFLICT`. With usable state, a terminal
   duplicate returns its stored signed receipt byte-for-byte, even outside skew
   or after expiry; it performs no new effect. A reserved entry becomes durable
   `uncertain` with `DURABLE_RESERVATION_NO_RETRY`. A pending entry continues
   observation of the same request.
3. Only a first admission checks the configured 1–300-second clock skew and
   journal capacity, then persists admission before resolving grants or effects.
   This skew is separate from the grant's validity interval.
4. Resolve service-owned grant/terms objects when the action needs them, check
   their binding and observe the configured node/network. Apply the wallet
   executor's current authority, budget and plan checks. Single use additionally
   validates the proof described above.
5. Before spending, reserve both wallet plan/budget and service action durably;
   recheck authority, use proof and input coins before broadcast. `receive`
   separately reserves before RPC allocation and re-observes the network. A
   final refusal after reservation retains the reservation.
6. Persist the result and signed receipt. A pending result can be observed again;
   an ambiguous or reserved outcome never authorizes rebroadcast or a fresh
   request intended to repeat the effect.

Missing single-use proof gives terminal `USE_PROOF_REQUIRED`. Adding a proof
later does not convert that terminal refusal into execution under the same nonce.
`USE_PENDING` can advance after confirmation with the same request, beyond its
initial admission skew if necessary, while current authority checks still run.
A returned terminal receipt is a replay of the original result, not renewed
authority. No `already-executed` service verdict exists.

Observations and effects are not atomic. Revocation or a reorganisation after
the last check can race with broadcast; a later reorganisation does not undo an
external effect. For the same admitted request and nonce, the preserved journal
prevents a second reserved effect attempt. It does not guarantee exactly-once
completion across a crash.

### 5. Receipts and client verification

A receipt has exactly this order:

```text
v, service, grantee, request_hash, verdict, reason, effect,
journal_seq, observed_height, peer

peer: uid, gid
wrapper: receipt, signature
receipt_digest = SHA256(UTF8("swarma-action-receipt-v1") || canonical receipt bytes)
```

The service signs that digest using BIP-340. The client binds its independently
pinned receipt key, service, grantee and exact request hash before trusting a
result. A valid receipt for another request and an unsigned error cannot become
success. The four verdicts are:

| Verdict | Meaning |
| --- | --- |
| `executed` | The action returned a result recorded by the service, including authenticated reads. |
| `pending` | The same request needs further observation; no spending effect has occurred. |
| `refused` | The service rejects the action; a retained reservation may still exist. |
| `uncertain` | An outcome or persistence boundary is ambiguous; this is not proof of success or absence of an effect. |

Reasons are 1–96 uppercase ASCII letters, digits or underscores. The profile
reuses wallet/grant reason codes and bounded `ACTION_`/`SERVICE_` codes, without
echoing raw errors, request input or credentials. `journal_seq` is one-based
admission order, or zero for a pre-admission refusal. `observed_height` is a
sampled nonnegative height, with zero meaning unavailable/not observed; it is
not an atomic authorization snapshot.

Spending effects contain optional `txid`, then `reserved_sat`, then optional
`phase`. Receive effects contain `address`; read effects use the wallet's
projections. Their presence does not add authority. A malformed body reaching
schema parsing gets a refusal bound to SHA-256 of the raw frame body, because
no authenticated canonical request hash exists. Transport failure can close
silently instead.

### 6. Bounded persistence and recovery

The reference service journal holds a lifetime lock, private `0600` single-link
files in a `0700` root, at most 32 entries and 65536 bytes, with 16384 bytes of
receipt headroom. Admission can stop earlier when headroom is exhausted.
Oversize receipts become uncertain. These are limits of this implementation,
not universal capacities for future services.

Corrupt state or changed configuration/receipt-key binding refuses reopen.
Write uncertainty poisons the live service. A crash after reservation, including
the wallet-reserved/service-pending gap, never permits rebroadcast. An ambiguous
receive reservation never allocates a second address by replay. Preserve state
and reconcile the outcome; changing a nonce, key, root or journal to retry an
uncertain effect is outside this recovery contract. There is no automatic
pruning, migration or reset that restores consumed authority.

### 7. Related design drafts

[LIP-0007](LIP-0007-service-types.md) proposes service type/action tables and
name self-declaration. [LIP-0008](LIP-0008-grant-v4.md) proposes signed resource
limits and owner-pinned name recipients. Neither extends the wallet v1 actions,
wire bytes, receipt pins or recovery rules described above. A future model
proxy with its own chain observation is separate from the current proxy's
gateway-supplied binding.

## Alternatives

- A same-user CLI retains compatibility but cannot enforce custody against
  its own OS user.
- A generic command broker exposes arbitrary effects rather than this closed
  action interface. It needs a separate threat model and authorization contract.
- Remote transports and multi-service routing need independent peer identity,
  replay and deployment designs; this Unix profile does not specify them.

## Security consequences

The service's credentials, executable, grant objects and journals need real
OS ownership and denied client access. Same-UID socket fixtures, cross-compilation
and template checks do not prove different-UID isolation. Before a deployment
claim, test denied reads of credentials/journals/another agent's socket beside a
successful own-agent request. Root compromise and privileged state rollback
remain outside this journal guarantee.

A small wallet controlled by the agent is a separate risk tier: its key holder
can spend its balance directly. Service grants can gate refills but cannot
retroactively restrict that key. A receipt proves the service's signed statement,
not an independent proof of an external world's state. Discovery, storage and
message delivery confer no action authority. The current observer also cannot
reconstruct an unobserved name-key change followed by a return from only the
current value.

## Conformance impact

There is no new normative conformance class in v0.1.4. Adoption requires a decision,
protocol changes and a separate profile-specific vector set under LIP-0001.
The historical v0.1 records and LIP-0002 byte domain stay unchanged.

The reference has public synthetic no-newline request/wrapper/receipt fixtures
in `testdata/service-v1/`. `TestActionGolden`, `TestActionWire` and `TestActionProof`
exercise exact bytes, domains, signatures, closed actions and unsigned proof
exclusion. The golden empty effect is a codec fixture, not a live balance result.
Stateful Core/socket and crash tests are separately opt-in and do not qualify
OS custody. A future public conformance set needs at least these paired cases:

| Valid neighbour | Negative or boundary case and expected result |
| --- | --- |
| Correct unsigned request and pinned receipt | ASCII-hash signature, signed-wrapper/event commitment, wrong key/service/request: reject at the corresponding boundary. |
| Signed, peer-pinned read; one reserved receive | Unsigned/wrong-peer read, grant-bearing ordinary read, no-grant spend or unsupported name action: refuse; receive replay allocates nothing extra. |
| Single-use request progressing pending to confirmed | Missing proof is terminal; wrong signer/commitment refuses; proof does not enter the request hash; mempool use has no effect. |
| Terminal duplicate outside skew/expiry | Conflicting nonce refuses; original valid terminal duplicate retains identical bytes, signature and sequence. |
| Persisted allowed action | Reservation/write/crash gaps preserve uncertainty; no rebroadcast, automatic reset or second effect. |
| Own-agent request under separate UIDs | Wrong UID/key, private-file reads and other-agent socket access fail; malformed/truncated/oversize frames close without inventing a receipt. |

## Open questions

- Formal adoption and partition between common service vocabulary and the
  wallet-specific wire, limits, reasons and effect schemas.
- Language-independent canonical escaping/numbers and complete profile vectors.
- Name commit/reveal continuation, remote transports, multi-service/broker
  routing, non-coin budgets and future effect formats.
- Mainnet deployment policy and qualification; peer UID/group, key and private
  root provisioning/rotation; journal migration, backup, anti-rollback and
  reconciliation of uncertain external effects.
- Compatible issuance of booking and wallet terms; provisioning, refill limits
  and lease/revocation policy for the agent-controlled second tier.

Unsigned request commitment, unsigned `use_txid`, signed no-grant reads, the five
actions, four verdicts, pinned service receipt key and terminal duplicate replay
are implemented choices of this v1 profile, not unresolved alternatives.
