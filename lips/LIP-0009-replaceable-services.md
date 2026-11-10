# LIP-0009: Replaceable services

- **Status:** Draft
- **Created:** 2026-11-10
- **Affects:** service interfaces, state portability, discovery and settlement
- **Builds on:** LIP-0006, LIP-0007 and LIP-0008

## Summary

A holder should be able to choose another service provider while keeping its
identity and independently established authority. Compatible type profiles make
requests portable; data export alone does not transfer grants, remaining
allowance or permission to retry uncertain effects. Provider replacement needs
new executor-bound authority and accounting that preserves old exposure.

This LIP records five accepted design choices and proposes their protocol
boundaries. It defines no executable wire profile, new deployed action or
implementation. It is not a requirement for M5 or the first demo.

## Accepted design decisions

Ivan Oparin accepted the following five RS1 recommendations on 2026-11-10 for
the specification and book. These decisions select a design direction; the
exact profiles and qualification below remain Draft.

| Decision | Accepted direction |
| --- | --- |
| D1 — First portable service | Start with `store.blob`: immutable content hashes make data continuity inspectable; wallets and live compute have harder recovery boundaries. |
| D2 — Provider-change authority | Use replacement grants first. Defer rebinding an existing grant until its authority and fencing model receives a separate review. |
| D3 — Unavailable old provider | Operator reconciliation is the default. A separately authorized emergency budget may fund only nonconflicting work; old liability and uncertain exposure remain. |
| D4 — Initial commercial model | Start with small capped prepaid contracts. Unused credit remains the old provider's liability. Credit/postpaid and escrow require explicit dispute terms. |
| D5 — Blossom payments | Support native BUD-07 payment where offered, alongside a separately versioned grant-aware NMC/BTC/LTC option. No forced conversion or assertion that a native-coin BUD already exists. |

These decisions create no additional M5/first-demo implementation, installation
or release gate. Supporting interface, export and accounting rules below still
need agreed profiles, exact bytes and independent conformance evidence.

## Motivation and current state

Separating service provision from identity control lets providers compete for
holders on price, capacity, terms and compatible interfaces. A holder must be
able to leave without surrendering its identity or silently recreating spent
authority. Reputation derivable from events is outside this LIP.

LIP-0007 proposes typed Namecoin declarations and candidate service types;
existing closed name consumers do not thereby support that member. LIP-0008
binds concrete executors, partitions and shared journals, and keeps wire and
accounting profiles open. Neither supplies an implemented migration protocol.
The wallet-v1 Unix service and gateway-bound model proxy remain their narrower
existing profiles; changing provider endpoints does not qualify a remote wallet
transport, transfer an active bearer or add independent chain observation.

## Proposal

### 1. Compatible interfaces per type

A versioned type profile MUST fix exact actions and target binding, request and
response schemas, signature/canonicalization rules, error/refusal vocabulary,
receipt shape, limit kinds/units and reservation/recovery semantics. It MUST
define request identity, retry outcomes, version negotiation and export/import
capabilities. Selecting another provider of that exact profile can preserve
client action logic; transport authentication and trusted peer pins must still
be deliberately provisioned.

Providers may offer a declared subset and stricter operator ceilings. Optional
namespaced extensions MUST NOT change base action meaning, supply authority,
or become mandatory while claiming base compatibility. Unknown mandatory
versions/actions/constraints MUST refuse rather than silently downgrade.
Capability naming follows LIP-0007/LIP-0008; this LIP assigns no leaf commands
or new typed-name fields. Wallet wire `spend` and internal grant/executor `pay`
retain their existing separate meanings.

Signed invocation time windows retain LIP-0008's `iat <= now < exp` checks
without grace. Clock skew needs an explicit time profile; changing providers
MUST NOT widen a signed window. Strict BIP-340 validation and its non-malleability
do not imply one possible signature per message. A different valid signature,
object ID or receipt encoding MUST NOT create another logical request,
allocation or billable attempt.

### 2. Portable state and custody

An export profile MUST distinguish holder data, accounting evidence and
execution credentials. A replacement provider MUST NOT interpret imported
files as action authority or an unconsumed budget.

| Type | Data/evidence to consider | Boundary that does not transfer automatically |
| --- | --- | --- |
| `store.blob` | Bytes/hashes, holder inventory, metadata, retention and receipts | Delete authority, billing credit and old reservations |
| `model.proxy` | Holder conversations/tool records, usage and uncertain exposure | Upstream secrets, active bearers and opaque provider sessions |
| `wallet.nmc` | Public history, nonce/result journal, txids and reservations | Money/RPC keys, coins or permission to rebroadcast a pending spend |
| `slot.station` | Holder files, supported checkpoints and resource usage | Host credentials, active processes or exclusive execution rights |
| `mail.send` | Drafts, message IDs, queued status and delivery receipts | Sending credentials or proof an ambiguous message was never sent |
| `names.nmc` | Name/transaction history and pending registration stages | Cold ownership keys or permission to restart an incomplete operation |
| `repo.git` | Objects, refs and authorized mutation/result records | Provider credentials or uncoordinated final ref writes |

These are profile requirements, not portable formats already implemented by
those services. Private exports need an authenticated encrypted destination;
holder-held blob decryption keys need not be given to either provider.

A proposed export manifest binds a unique migration ID, holder, source and
destination executor, type/version, predecessor grant/partition lineage,
journal sequence/root, settled usage, outstanding exposure and a complete
hash inventory. Exact schema, domain and limits remain open. The old provider
signs its accounting snapshot/closing statement with its previously trusted
receipt key. The authorized holder signs consent to the root and destination;
a grantee may consent only within its explicit authority. The new provider
signs acceptance. Neither consent nor a provider receipt issues a grant.
Receipt verification MUST use independently established pins; an export cannot
choose its own trusted signer. Signatures do not prove an honest ledger.

### 3. Exclusive cut-over and replacement grants

The admission invariant is: old and new providers MUST NOT create a second
authorized attempt for one logical effect, or consume more than the agreed
allocation across settled usage and outstanding reservations. This is not a
promise of exactly-once completion or control over dishonest credential holders.

The proposed cooperative handover is:

1. Stage a complete, hash-checked data copy without admitting imported work at
   the new provider. The old provider remains the accounting authority.
2. Serialize and durably fence old admissions and replicas. Drain admitted work
   or conservatively record every unresolved outcome. Sign the final journal
   root/sequence and closing statement; preserve the journal for reconciliation.
3. Verify closure of the old grant under its chain/profile. A closing receipt
   alone is not revocation. The new provider MUST require a replacement grant
   naming its concrete executor and its new allocation. A type match, endpoint
   change or imported journal MUST NOT rebind the old grant. Single-use requests
   must commit the newly selected executor under their adopted profile.
4. Reconcile inventory and accounting; deduct settled usage and all bounded
   uncertain exposure before transferring any remaining predecessor allowance.
   The issuer authorizes that allocation and lineage. Persist import acceptance
   once, establish new trust pins and enable new effects only after admission
   requirements are satisfied. Keep the old provider fenced.

Reissuance MUST NOT reset consumed allowance or convert uncertainty into a
refund. An exact import retry returns its stored result without a new allocation;
a conflicting migration ID/root or rollback MUST refuse. A partial export MUST
NOT activate a transferred allocation. Separate data replicas may coexist,
but independent journals cannot each spend the same apparent remainder.
Existing wallet state files cannot simply be copied and reopened under new
configuration/key bindings; their current profile refuses that change.

If the old provider is unreachable, operator reconciliation is the default.
Retain old liability and all unresolved exposure. Recover available holder data
from verified copies, but do not infer a remaining budget or absence of an
effect from timeout, expiry, confirmed closure or a missing receipt. Already
admitted external work may complete later. A separately authorized emergency
allocation MUST be independent of the uncertain remainder and restricted to
nonconflicting work; it cannot erase old debt or authorize duplicate effects.
If exposure cannot be bounded, no automatic takeover of that allowance is safe.

Exact fencing, anti-rollback, journal interchange, outcome evidence and
allocation-lineage encoding need type-specific profiles. A future rebind
mechanism is deferred, not enabled by this proposal.

### 4. Namecoin discovery and comparable offers

Provider selection uses Namecoin names and the future LIP-0007 declaration.
Known names or a local, rebuildable index of observed name values supply
candidates; no central registry is authoritative. Exact-name resolution alone
cannot enumerate every provider of a type. Re-resolve each candidate under
pinned chain/network, ownership, expiry and key policies before trusting its
action declaration or connecting to its endpoint.

A future offer profile should bind provider/executor, type/version, action
subset, asset/unit price, limits, retention, quote identity and expiry.
Provider-signed offers may be off-chain, with their authenticity/location bound
under an adopted declaration profile. These are not already accepted name
members; whole-value size limits and closed-consumer migration still apply.
Endpoint redirects and destination access must not forward credentials or
silently replace trusted peer/receipt keys.

Privileged admission retains LIP-0008's decided freshness policy: 60 minutes
for money/irreversible actions, 90 for other privileged actions, with at least
two independent nodes agreeing on the tip. A long block gap alone is not node
failure. Exact clocks, age and independence criteria still need qualification;
an offer or healthy HTTP endpoint does not waive chain checks.

### 5. Authorization, accounting and payment

Grant budgets are authorization ceilings, contract/quote terms select the
commercial bargain, and provider receipts record signed accounting statements.
Before its effect the service MUST reserve bounded resource/cost exposure under
its type profile. Uncertain outcomes retain that exposure. A receipt alone
cannot widen a grant or independently prove completion.

Future receipt profiles should bind executor/key epoch, holder, request/quote
hashes, grant/partition lineage, journal sequence, verdict, actual usage,
retained exposure and settlement references. Exact fields and domains are not
assigned here. Keep historical receipt-key pins and journals through rotation.

Start with small capped prepaid contracts. Acknowledged deposits, debits and
refunds need signed records. Unused prepaid credit remains the old provider's
liability; it MUST NOT become the new provider's balance merely by export.
Refund/new payment or an explicitly accepted credit assignment is separate.
Postpaid credit and escrow are deferred until explicit dispute terms exist;
old accrued debt would remain with its original counterparty after switching.

NMC/BTC/LTC payment profiles MUST identify asset/network, atomic units, target,
fee/refund rules and confirmation risk. A wallet payment requires its own
authority and durable identity; an invoice is not spending permission. No
cross-chain atomicity or equivalence of confirmation counts is implied. A
Namecoin anchor cannot directly spend BTC/LTC outputs.

Keep name bindings, required issuance/closure and settlements on their chosen
chains; keep detailed quotes, manifests, usage and receipts off-chain. A dispute
bundle combines signed terms, grant lineage, request/receipts, closing records
and checked transaction evidence. It can show conflicting charges but cannot
compel storage, performance or a refund. Arbitration/escrow needs a separate
commercial arrangement. Paid retention obligations and authority to admit new
actions are distinct; grant expiry alone proves neither deletion nor fulfillment.

### 6. First profile: Blossom-backed `store.blob`

An eventual profile must declare exact BUD support and grant-aware versioning;
ordinary Blossom clients/servers do not acquire Swarma grant semantics.
At the pinned Blossom revision below, BUD-01 is a mandatory draft and the
other listed BUDs are optional drafts:

| Operation | Existing Blossom interface |
| --- | --- |
| Retrieve/stat | BUD-01 `GET`/`HEAD /<sha256>` |
| Upload | BUD-02 `PUT /upload`; optional BUD-06 `HEAD /upload` is only preflight |
| Mirror | BUD-04 `PUT /mirror`, preserving exact content hash |
| List/delete | BUD-12 `GET /list/<pubkey>` and `DELETE /<sha256>`; list is optional and unrecommended |
| Endpoint auth | BUD-11 signed Nostr kind `24242` events |
| Optional native payment | BUD-07 `402` challenge/proof flow; specified methods are Cashu and Lightning |

The holder keeps a complete inventory rather than depending on server listing.
A grant-aware upload request binds executor, content hash, size, terms/quote,
retention and logical action ID. Bytes, object count, storage duration/byte-time
and egress require separate limit-kind LIPs under LIP-0008's extension rule;
no current coin/token counter silently gains those meanings.

Where endpoint auth is required, retain a separate BUD-11 token with matching
verb, finite expiry, required hash `x` tags and lowercase domain `server` scope.
The grant-aware profile must authenticate the token signer as the permitted
holder/channel; attaching any token to a grant is insufficient. A kind-24242
event is neither the grant nor its invocation commitment. Do not overwrite its
auth header with grant data or give holder signing keys to the provider.

Check authority and reserve exposure before a permanent storage/billing effect.
Hash exact bytes, then return the BUD descriptor and a separate pinned-key
signed service receipt. A descriptor is not a signed receipt, content deduplication
does not deduplicate billing, and preflight success reserves nothing. Retention
receipts remain contractual statements, not proof of future availability.

To migrate, authorize the new concrete executor with a replacement grant.
Use a complete inventory and a fresh destination-scoped mirror token; BUD-04
copies bytes, not credit, retention or authority. Verify destination hashes,
sizes and retrieval before switching locators or requesting old-copy deletion.
Restrict mirror destinations/redirects to avoid internal-network access and
credential forwarding. Restore from holder/replica copies if the source is
unavailable; a hash alone cannot recover missing bytes.

BUD-07 native payment remains optional where offered. The accepted additional
grant-aware NMC/BTC/LTC option needs its own published, versioned payment-method
profile; it is not current native-coin BUD support. Never force conversion or
treat a payment proof as a grant. Follow BUD-07's rule that HEAD is not retried
with payment proof; authorize and account for the subsequent effect request.

## Security and conformance impact

No normative v0.1, wallet-v1, v3 or existing v4 draft wire bytes change. Adoption
needs exact type/export/receipt/payment profiles and independent evidence.
Future conformance must publish valid neighbours beside these outcomes:

| Valid control | Refusal or invariant |
| --- | --- |
| Same supported type/version, exact action and authenticated peer | Unknown mandatory profile/action/constraint, silent downgrade or extension changing base meaning refuses. |
| Complete signed export, trusted keys and holder consent | Missing objects/sequence, wrong signer/destination or metadata-only authority refuses transferred-allocation activation. |
| Old admissions fenced; reconciled exposure; replacement executor-bound grant | Both providers using one remainder, type-only substitution or a silent old-grant rebind refuses. |
| Exact import retry with unchanged allocation/result | Replayed/stale/conflicting export, rollback or another full allocation cannot restore consumed authority. |
| Retained uncertain outcomes and separately authorized nonconflicting emergency work | Timeout-based refund, ambiguous spend/send retry or reuse of uncertain remainder refuses; preserve old liability. |
| Independently allocated data replicas | Two independent journals charging a shared apparent allocation refuse; copies alone grant no effects. |
| Fresh verified Namecoin declaration and pinned endpoint/receipt key | Stale/expired/transferred name, substituted key, untrusted redirect or arbitrary offer cannot cause credential forwarding or authorized effects. |
| Prepaid debit/refund records bound to quote and grant | Exported credit presented as the new provider's balance, repeated settlement or charge above ceilings refuses. |
| Blob hash continuity, scoped BUD auth and live executor grant | Wrong hash, unrelated token signer, cross-server token replay or missing grant refuses; descriptor/preflight/payment alone is insufficient. |
| Verified destination copy and accepted retention terms | Partial mirror, list omission or missing source bytes cannot be called complete migration; no premature old-copy deletion. |
| Explicit supported payment-method profile and checked chain evidence | Unknown native-coin method, forced conversion, wrong asset/network or cross-chain proof substitution refuses. |

These are planned profile assertions, not passing migration, custody, billing
or availability tests. Malicious operators, stolen keys, incomplete records,
chain reorgs and effects already in flight remain explicit limits.

## Open questions

- Exact portable type versions/actions, transport pins and extension grammar;
  compatible upgrades of closed Namecoin consumers and offer authentication.
- Export/closing/import canonical bytes and signing domains; inventory bounds,
  private-data encryption, key rotation and historical receipt verification.
- Exclusive fencing and anti-rollback evidence; unresolved-work reconciliation,
  allocation lineage, atomic accounting and type-specific recovery formats.
- New blob limit-kind LIPs, retention/egress units, reservation and pricing
  semantics; exact grant-aware invocation/BUD signer binding.
- Versioned native NMC/BTC/LTC settlement, refunds and evidence; credit/escrow
  dispute terms if later introduced. Rebind authority remains separately deferred.
- Public positive/negative vectors and independent qualification. These items
  remain future spec/book work, not first-demo implementation gates.

## Sources

- [LIP-0006](LIP-0006-grant-gated-actions.md), wallet request/admission,
  receipts and recovery; [LIP-0007](LIP-0007-service-types.md), type/declaration
  boundaries; [LIP-0008](LIP-0008-grant-v4.md), executor partitions, budgets,
  freshness, typed signing and future-profile rules; [key map](../KEY-MAP.md).
- Current implementation boundary at chain-lab
  `4d31b9aeba2e2c217e4a09dae2c50f311e0a0652`:
  [wallet SERVICE.md](https://github.com/relux-works/swarma-chain-lab/blob/4d31b9aeba2e2c217e4a09dae2c50f311e0a0652/experiments/agent-wallet/SERVICE.md)
  and [model proxy](https://github.com/relux-works/swarma-chain-lab/blob/4d31b9aeba2e2c217e4a09dae2c50f311e0a0652/experiments/model-proxy/README.md).
- Blossom read 2026-11-10 at commit
  `b5bd2801d1763aa635fc8fea7a76597e0eb18990`
  (2026-06-15T16:08:10Z):
  [BUD-01](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/01.md),
  [BUD-02](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/02.md),
  [BUD-04](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/04.md),
  [BUD-06](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/06.md),
  [BUD-07](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/07.md),
  [BUD-11](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/11.md)
  and [BUD-12](https://github.com/hzrd149/blossom/blob/b5bd2801d1763aa635fc8fea7a76597e0eb18990/buds/12.md).
