# LIP-0013: Trust contract profile and instruction envelope for Grant v3

- **Status:** Draft
- **Created:** 2026-11-12
- **Affects:** the contract preimage of v3 trust grants, agent-to-agent
  instructions, admission of a peer instruction by an executor
- **Builds on:** LIP-0004; relates to LIP-0007 and LIP-0008
- **Extended by:** LIP-0014, which proposes profile `swarma-trust-contract/2`
  with a parent binding and a right of re-delegation. A reader of profile
  `/1` refuses a complete contract of that profile as `CONTRACT_ENCODING`,
  because it has fifteen members; an eleven-member object that carries only
  the `/2` profile string refuses as `CONTRACT_PROFILE`
- **Vectors:** [`vectors/LIP-0013/trust-vectors.json`](../vectors/LIP-0013/trust-vectors.json),
  checked by [`tools/trustcheck`](../tools/trustcheck)

## Summary

A Grant v3 (LIP-0004) already signs the SHA-256 of a contract document,
`contract_sha256`, and treats that document as opaque. This LIP defines one
such document for trust between our own agents: the profile
`swarma-trust-contract/1`. It names four actions, `instruct`, `land`,
`review` and `spend`, and states how each maps to the v3 `scope` and
`budget`. It also defines the kind-8185 signed instruction envelope that
carries one such action from a grantee to an executor, and the order of the
checks an executor runs before it admits an instruction. Admission needs
enforcing mode; the default is shadow mode, in which an executor reports its
verification results while peer messages stay data.

No v3 byte, signing domain, consent rule or `rental.Check` rule changes. An
old v3 verifier that ignores the contract still sees a valid grant whose v3
scope and budget are exactly what this profile derives.

## Motivation

Goal 1 is trust between the agents of our two owners on Namecoin, on Grant v3,
as agreed by both co-leads on 2026-11-12. Two of the four actions the agents
need exist in v3: `repository.push` and `pay` with `budget`. `instruct` and
`review` do not. Reusing a v3 scope name such as `deliver` to mean "instruct"
would reinterpret signed v3 bytes, so the missing actions go into the
contract instead. The design source is the Goal 1 design note of 2026-11-12,
sections 2.6, 4.1 and 4.2, and its open questions Q5, Q6 and Q10.

## Current state

- Grant v3, its consent event (kind 8181) and its canonical bytes are
  implemented in the reference laboratory
  (`swarma-chain-lab/experiments/rental/grant.go`, main `7ea1800`). The rental
  profile already uses the contract to carry `allowed` and `forbidden`
  actions (`issuance_v2.go`).
- `rental.Check` (`grant_kernel.go`) verifies a presentation on the
  verifier's own node and returns `live`, `pending` or `refused`. It reads
  `scope` and `budget` as outputs for a separate executor and never reads the
  contract.
- No signed message envelope exists between agents. The closest precedent is
  the lab-only kind-8183 renter request
  (`experiments/rental-executor/FORMAT-PROPOSAL.md`).
- Kinds 8181 to 8184 are in use in chain-lab. On 2026-11-12 no file outside
  `go.sum` on any of the 136 refs of `swarma-chain-lab` or the 29 refs of this
  repository contained `8185` as a word; the same search found `8184` in
  chain-lab.

Nothing in this LIP is implemented in a product. The reference checker in
`tools/trustcheck` recomputes the vectors; it is not a verifier or a signer.

## 1. Terms

- **Trust grant:** a Grant v3 whose `contract_sha256` is the SHA-256 of a
  `swarma-trust-contract/1` document.
- **Contract bytes:** the exact octets of that document. All hashes in this
  LIP are over these octets.
- **Executor:** the agent named by the grant's `agent_name`. It admits or
  refuses instructions.
- **Grantee:** the holder of the key `grantee_key`. It signs instructions.
- **Principal:** the grant's `landlord_name`, on whose authority the
  executor acts.
- **Owner:** one of the two people who direct the agents, Ivan Oparin and
  Alexey Grigorev. "Both owners" means these two.
- **Mode:** an executor runs in shadow mode or in enforcing mode
  (section 3.4). Only enforcing mode admits a peer instruction.

## 2. The trust contract `swarma-trust-contract/1`

### 2.1. Canonical bytes

The contract is one JSON object, encoded as compact UTF-8 with no whitespace
outside strings and no trailing newline, with exactly these eleven members
in this order:

| # | Member | Type | Rule |
| --- | --- | --- | --- |
| 1 | `profile` | string | exactly `swarma-trust-contract/1` |
| 2 | `network` | string | `main` or `regtest`; equals the grant's `network` |
| 3 | `landlord_name` | string | an `id/` name in the v3 name syntax; equals the grant's `landlord_name` |
| 4 | `agent_name` | string | an `id/` name in the v3 name syntax, different from `landlord_name`; equals the grant's `agent_name` |
| 5 | `grantee_key` | string | 64 lowercase hex, a valid BIP-340 x-only key; equals the grant's `grantee_key` |
| 6 | `actions` | array of strings | section 2.2 |
| 7 | `repos` | array of strings | section 2.3, rule 5 |
| 8 | `spend_budget` | integer | atoms, 0 to 2100000000000000 |
| 9 | `not_before` | integer | Unix seconds; equals the grant's `not_before` |
| 10 | `not_after` | integer | Unix seconds, greater than `not_before`, at most 253402300799; equals the grant's `not_after` |
| 11 | `note` | string | at most 280 bytes; carries no authority |

The v3 name syntax is `id/` followed by 1 to 252 bytes of `a-z`, `0-9`, `-`,
`_` and `.` (`station()` in `certificate.go`).

Example, with line breaks for display only; the real bytes contain none:

```json
{"profile":"swarma-trust-contract/1","network":"main","landlord_name":"id/ivanopcode",
"agent_name":"id/ivanopcode-keeper","grantee_key":"<64 hex>","actions":["instruct","review"],
"repos":[],"spend_budget":0,"not_before":1794528000,"not_after":1797120000,"note":""}
```

Encoding rules:

- Integers are canonical decimals: no sign, no leading zero, no fraction or
  exponent. A negative value of any integer member therefore breaks this
  rule.
- Every string value, `note` included, is printable ASCII, bytes 0x20 to
  0x7E. Inside strings the only escapes are `\"` and `\\`; every other
  character is written literally. No `\u` escape, no `\/` and no control
  escape such as `\n` appears.
- `actions` and `repos` are arrays, never `null`.
- The whole document is at most 8192 bytes.

These are the bytes Go's `encoding/json` produces with HTML escaping off, the
encoder chain-lab already uses for event and contract bytes. A reader MUST NOT
normalize: it parses the document and MUST refuse unless re-encoding the
parsed value under these rules gives the identical octets. Thus a reordered,
missing, extra or duplicated member, whitespace, a different number or string
spelling, or a trailing newline all refuse.

### 2.2. Actions

`actions` is a non-empty set, sorted ascending by byte value with no
duplicates, drawn from exactly these four names:

| Action | Meaning; the executor still applies its own safety rules | v3 scope entry |
| --- | --- | --- |
| `instruct` | The grantee may assign the executor work: tasks, requests, priorities. | none |
| `land` | The grantee may authorize a landing into the default branch of a repository listed in `repos`. | `repository.push` |
| `review` | The grantee's review verdicts count as reviews for the executor's landing gates, within the repository's reviewer policy (below). | none |
| `spend` | The grantee may request NMC payments up to `spend_budget` atoms in total, fees included. | `pay` |

The v3 `scope` of a trust grant is derived, never chosen: `repository.push`
if the actions include `land`, plus `pay` if they include `spend`, sorted;
otherwise `[]`. Its v3 `budget` equals `spend_budget`. The v3 scope names
`deliver`, `names.register`, `publish` and `secret.release` never occur in a
trust grant, and none of them is a profile action.

`review` authorizes who may review: it makes the grantee an admissible
reviewer for the executor. It does not change the reviewer policy of the
repository. That policy's requirements on the reviewer's model and effort, on
a fresh reviewer seat that is never the producer's, and on the labels of the
pull request all still apply. A review from another owner's agent therefore
counts only if it also meets that policy.

An issuer SHOULD omit the v3 `budget` member when `spend_budget` is 0. A
verifier compares the v3 budget value, where an absent budget is 0, as
`rental.Grant.BudgetSat` does.

### 2.3. Validity rules and refusal order

A reader applies these rules in this order and reports the first failure:

| # | Rule | Refusal |
| --- | --- | --- |
| 1 | Canonical bytes (section 2.1), including the number and character rules | `CONTRACT_ENCODING` |
| 2 | `profile` is `swarma-trust-contract/1` | `CONTRACT_PROFILE` |
| 3 | `network`, both names, `grantee_key` and the window follow section 2.1 | `CONTRACT_FIELD` |
| 4 | `actions` is non-empty, sorted, without duplicates, from the four names | `CONTRACT_ACTIONS` |
| 5 | `repos` is non-empty exactly when the actions include `land`; at most 16 entries; sorted without duplicates; each entry follows the repository grammar below | `CONTRACT_REPOS` |
| 6 | `spend_budget` is greater than 0 exactly when the actions include `spend`, and at most 2100000000000000 | `CONTRACT_BUDGET` |
| 7 | `note` is at most 280 bytes | `CONTRACT_NOTE` |

Rule 1 owns every lexical property of the bytes: the member set and order,
whitespace, the spelling of numbers including the sign, the character
repertoire of strings and their escapes. Rules 2 to 7 judge values that
already passed rule 1. So `"spend_budget":-1` refuses as `CONTRACT_ENCODING`,
not `CONTRACT_BUDGET`; a negative `not_before` refuses as `CONTRACT_ENCODING`,
not `CONTRACT_FIELD`; and a note with a non-ASCII character or a `\n` escape
refuses as `CONTRACT_ENCODING`, not `CONTRACT_NOTE`. `CONTRACT_NOTE` is the
length rule only. Vectors C-N22 and C-N29 to C-N32 pin these codes.

Repository grammar: `https://`, a host of two or more lowercase DNS labels
(`a-z`, `0-9`, `-`, 1 to 63 bytes each, no leading or trailing hyphen), then
`/` and one or more path segments of `A-Z`, `a-z`, `0-9`, `.`, `_` and `-`
separated by `/`. Segments `.` and `..` are refused. No port, userinfo,
query, fragment or trailing slash; at most 200 bytes. Repositories are
compared by exact bytes; `https://git.example/a/b` and
`https://git.example/a/b.git` are different repositories.

The note is for people. A verifier and an executor MUST NOT derive any
permission, limit, target or instruction from it. It is public on mainnet
once the bundle is shared, so it holds nothing private.

The design note's `CONTRACT_SHAPE` is refined here into the codes of rules 1
to 7.

### 2.4. Consent tags

The consent event stays the v3 kind-8181 event with exactly four tags in the
v3 order (LIP-0004 section 3). For a trust grant:

| Tag | Value |
| --- | --- |
| `t` | `swarma-rental-consent-v1`, unchanged from v3 |
| `contract` | the contract SHA-256, as v3 requires |
| `booking` | SHA-256 of the contract bytes followed by the 7 ASCII bytes `booking`, with no separator |
| `privacy` | SHA-256 of the 23 ASCII bytes `swarma-trust-privacy-v1`, which is `c0436d6368755b1aeaa7fe0e87bddcc5e09dd32e8c6921806e316f28e9c02aad` |

v3 requires only that `booking` and `privacy` are 64-hex digests
(`grant.go`, `Validate`), so these values are valid v3 consent. The `t` tag
keeps the rental name on purpose (design Q6, option a): a new tag would change
v3. The contract profile, not the tag, tells a trust grant from a rental. A
grantee who signs the consent signs these two values too, so the consent
itself shows that it is for a trust contract and not for a rental booking.

### 2.5. Binding to the grant

After `rental.Check` returns `live` for a presentation, a verifier that acts
on a trust grant checks, in this order:

| # | Check | Refusal |
| --- | --- | --- |
| 1 | SHA-256 of the contract bytes equals the grant's `contract_sha256` | `CONTRACT_HASH` |
| 2 | The contract passes section 2.3 | the section 2.3 code |
| 3 | `network`, `landlord_name`, `agent_name`, `grantee_key`, `not_before` and `not_after` equal the grant's fields | `CONTRACT_MISMATCH` |
| 4 | The grant's `scope` equals the scope derived in section 2.2 | `SCOPE_MISMATCH` |
| 5 | The grant's budget, absent meaning 0, equals `spend_budget` | `BUDGET_MISMATCH` |
| 6 | The consent tags equal section 2.4 | `CONSENT_TAGS` |

A grant that fails any of these refuses as a trust grant. It may still be a
valid v3 grant for some other profile; this LIP says nothing about that use.

### 2.6. v3 stays unchanged

This profile changes no v3 byte, no signing domain (`swarma-grant-v3`,
`swarma-issue-v1`), no consent rule and no `rental.Check` rule. Every trust
grant is an ordinary valid v3 grant.

An old v3 verifier or executor that ignores the contract sees:

- for a contract whose actions are within `instruct` and `review`: scope `[]`
  and budget 0. That authorizes no v3 effect, so ignoring the contract is
  harmless;
- for a contract with `land` or `spend`: scope `repository.push` or `pay` and
  the budget. These are the v3 effects the landlord signed. The contract only
  narrows them, for example to the listed repositories. An executor that
  ignores the contract loses that narrowing (see Security consequences).

### 2.7. Forward compatibility with v4

The four action names are proposed as the leaf names of the agent action
table that v4 will take from the LIP-0007 registry (LIP-0008 section 12.3).
That table, its grammar and its leaf names are still open there, so this is a
requirement on the future table, not a claim about an existing one. If v4
adopts the names unchanged, a v4 grant can carry the same vocabulary as signed
scope, and a trust contract maps to it one to one. This LIP defines no v4
bytes.

## 3. The instruction envelope, kind 8185

### 3.1. Event

The envelope is a NIP-01 event of kind **8185** with empty `content`. Its
wire form is compact JSON with exactly the members `id`, `pubkey`,
`created_at`, `kind`, `tags`, `content` and `sig`, in that order, under the
encoding rules of section 2.1, at most 16384 bytes. `pubkey` is the signer's
x-only key in 64 lowercase hex. `id` is the NIP-01 id, the SHA-256 of the
compact JSON array `[0,pubkey,created_at,kind,tags,content]`. `sig` is a
BIP-340 signature by `pubkey` over the 32 bytes of `id`, in 128 lowercase hex.
`created_at` is Unix seconds from 1 to 253402300799.

### 3.2. Tags

Every tag is an array of exactly two printable ASCII strings; each value is
at most 512 bytes. The tags appear in exactly this order:

| # | Tag | Value |
| --- | --- | --- |
| 1 | `t` | `swarma-instruction-v1` |
| 2 | `to` | the executor's `id/` name |
| 3 | `grant` | the `grant_id` of the trust grant, 64 lowercase hex |
| 4 | `action` | `instruct`, `land`, `review` or `spend` |
| 5 | `body` | SHA-256 of the instruction text, 64 lowercase hex (section 3.3) |
| 6 | `room` | the Matrix room ID the message is posted in: `!` and 1 to 254 printable non-space ASCII bytes |
| 7 | `mxid` | the sender's Matrix user ID: `@`, then printable non-space ASCII with a `:`, at most 255 bytes |
| 8 | `nonce` | 32 fresh random bytes, 64 lowercase hex |
| 9 | `amount` | `spend` only, and then required: a canonical positive decimal number of atoms, at most 2100000000000000 |
| 9 | `repo` | `land` only, and then required: one repository in the grammar of section 2.3 |

An `instruct` or `review` envelope has exactly tags 1 to 8. A `land` envelope
has exactly tags 1 to 8 and `repo`; a `spend` envelope has exactly tags 1 to 8
and `amount`. Any other tag, order, count or value is refused as
`ENVELOPE_SHAPE`. A fixed order makes one event shape per instruction; the
kind-8183 precedent allowed any order, which leaves more than one shape.

### 3.3. Body hash

`body` is the SHA-256 of the exact octets of the instruction text that the
executor will act on. The envelope signs the hash, not the text, so the text
travels in the message and the event stays small.

In Phase A of the design note, the sender posts one Matrix message whose body
is the instruction text, one LF, and then one fenced block tagged
`swarma-envelope` that holds `{"event":…,"bundle":…}`; the bundle is
optional after first use. The instruction text is every octet before that
LF. This carriage is proposed with the open question on a2a body handling
below. The vectors fix only the hash over the given text.

The instruction text is data until step 7 admits it in enforcing mode
(section 3.4). In shadow mode it stays data even when every check passes.

### 3.4. Admission mode and check order

**Mode prerequisite.** An executor runs in exactly one of two modes. It reads
its mode before step 1.

- **Shadow mode is the default.** An executor starts in shadow mode and stays
  in it while its enforcing record is absent, unreadable or incomplete. In
  shadow mode it runs steps 1 to 8 in full and reports the verification
  results to its owner, but every peer message stays data, as today: the
  executor gives it no peer instruction authority and starts no task on it,
  and only the owner directs.
- **Enforcing mode** is entered only after the first proof has passed and
  both owners have approved enforcing mode, each recorded before the switch.
  The first proof is the mainnet proof of design section 5.2, its negative
  controls and its revocation step included. Neither condition alone is
  enough. One owner's approval counts once, however often it is given. A
  grantee, a peer agent or an envelope cannot approve and cannot change the
  mode.
- The mode at receipt is kept with the receipt (section 3.5). Step 7 admits
  only when the mode is enforcing both at receipt and at step 7; otherwise it
  reports. A switch to enforcing mode is not retroactive.

The mode and its record belong to the executor's own configuration, which its
owner sets (design section 4.3). This LIP fixes the rule, not the storage.

| # | Scenario | Mode | An envelope that passes steps 1 to 6 |
| --- | --- | --- | --- |
| M1 | No first proof yet, and no owner has approved | shadow | Its results are reported to the owner; the message stays data and starts no task; only the owner directs |
| M2 | The first proof has not passed, though both owners have approved | shadow | As M1 |
| M3 | The first proof has passed, and only one owner has approved, once or repeatedly | shadow | As M1 |
| M4 | The first proof has passed, and both owners have approved | enforcing | Admitted at step 7 as an instruction from principal `landlord_name` under `grant_id`; step 9 still applies |
| M5 | An envelope passes every check while the executor is still in shadow mode, and both owners approve enforcing mode later | shadow | Reported as verified, never admitted; delivered again after the switch it refuses as `REPLAY`, or as `STALE` once outside the window (section 3.5), so the grantee signs a new envelope |
| M6 | An envelope fails a check, in either mode | either | Refused with the code only; the message is data |

**Check order.** The executor runs these steps in order and stops at the
first refusal. Steps 1 to 9 restate design section 4.1; the codes are the
ones this LIP fixes.

| # | Step | Refusal |
| --- | --- | --- |
| 1 | The Matrix event arrives through the authenticated sync, which gives sender `S`, room `R` and the body | — |
| 2 | Extract the envelope. Without one the message is data, as today | — |
| 3 | Sections 3.1 and 3.2: exact shape; then recompute the NIP-01 id and verify BIP-340 over it | `ENVELOPE_SHAPE`, then `ENVELOPE_SIGNATURE` |
| 4a | `to` equals the executor's own name | `NOT_FOR_ME` |
| 4b | `room` equals `R` | `ROOM_MISMATCH` |
| 4c | `mxid` equals `S` | `SENDER_MISMATCH` |
| 4d | `body` equals SHA-256 of the instruction text | `BODY_MISMATCH` |
| 4e | `created_at` is in [now − 900 s, now + 120 s], both ends included, where now is the executor's clock at receipt | `STALE` |
| 4f | The nonce is not in the nonce journal (section 3.5); on success it is recorded | `REPLAY` |
| 5 | If a local contacts pin maps `S` to `id/Y`, the Nostr key of `id/Y` equals `pubkey`. Consistency only, not authority | `SENDER_KEY_MISMATCH` |
| 6a | The bundle for `grant` is in the executor's store | `GRANT_UNKNOWN` |
| 6b | The grant's `agent_name` is the executor's own name | `NOT_FOR_ME` |
| 6c | `rental.Check` with `sender = pubkey` on the executor's own node; when `pubkey` is not the grantee it refuses `GRANTEE_MISMATCH` before any chain read | every `rental.Check` reason |
| 6d | Section 2.5, the contract against the grant | the section 2.5 codes |
| 6e | `action` is in the contract's `actions` | `ACTION_NOT_GRANTED` |
| 6f | For `land`: `repository.push` is in scope and `repo` is in `repos` | `REPO_NOT_GRANTED` |
| 6g | For `spend`: `pay` is in scope and `amount` is at most the budget | `OVER_BUDGET` |
| 7 | `live` and every check passed. In enforcing mode, at receipt and now: admit as an instruction from principal `landlord_name` under `grant_id`. In shadow mode: report the verified result to the owner; the message stays data and gains no instruction authority. In both modes record `{event_id, grant_id, tip_hash, mode}` | — |
| 8 | `pending` or the node unavailable: hold and retry within 24 h; otherwise refuse with the code only | — |
| 9 | Enforcing mode only; in shadow mode no peer message leads to an effect. Before any effect the executor's own role and safety rules apply. For `spend`, reserve from the cumulative ledger, then run step 6 again immediately before the effect | — |

Step 6g checks one request. The cumulative total, fees included, is the
executor's ledger, as LIP-0006 already does for the wallet.

A refusal is reported as its code only. The executor does not reveal grant
contents, ledger state or the reason a key was refused beyond the code.

For a contract of profile `/2`, LIP-0014 holds Draft text under pending
owner decisions that adds to these steps. Its section 3.4 adds two refusals
after 6d for a grant with a scope text, a field `scope_text` to the record
of step 7 and, by the owners' choice, a hold at step 9 (J5). Its section
9.1 adds a ledger for each row to the reservation of step 9 (J1). Profile
`/1`, its steps and its vectors do not change.

### 3.5. Nonce journal and the time window

- The journal maps each nonce to the event id that first used it, and it is
  stored with private permissions (0600). A nonce is reserved at step 4f, so
  every later event with that nonce refuses as `REPLAY`, whoever signed it.
  This includes the same event delivered again after a final verdict.
- The journal works the same in both modes. A nonce reserved in shadow mode
  stays reserved after a switch to enforcing mode, so an event verified in
  shadow mode and delivered again after the switch refuses as `REPLAY`, or
  as `STALE` once step 4e puts it outside the window.
- A held envelope (step 8) keeps its receipt time, its nonce reservation and
  its receipt mode. A retry of the same event id continues at step 6; it is
  not a replay, and step 4e is not evaluated again. Without this rule a retry
  after 15 minutes would refuse as `STALE`. An envelope received in shadow
  mode stays data when its retry completes after a switch to enforcing mode.
- An entry may be deleted once the executor's clock passes
  `created_at + 900`, because step 4e then refuses that event anyway. A
  journal that is lost or rolled back reopens replay inside that window. An
  executor that restarts at time `T0` without its journal therefore refuses,
  as `REPLAY`, every envelope whose `created_at` is at or before `T0 + 120`;
  such envelopes leave the window by `T0 + 1020`.
- The window [now − 15 min, now + 2 min] is the owner-command window a2a
  already uses for verified owner commands.

### 3.6. Signing under a grant

Owner decision pending: J7. Every rule of this subsection is Draft text.
Until the decision nothing limits which run of an agent signs under which
grant. A grant is issued to a key, and every run of the agent that holds
the key can act under it. Worker `W` is the grantee of a grant from
principal A for an action at A's executor. `W` also admits instructions
from an orchestrator of another party, B, under a second grant. B's
orchestrator instructs `W`, and in the course of that work `W` sends A's
executor an envelope under its own grant. A's executor runs section 3.4,
every check passes, and in enforcing mode it admits the envelope as an
instruction on A's authority. B's orchestrator has obtained an action that
A gave `W` for other work, and A's executor has no input that tells the two
apart. LIP-0014 gives a relaying agent a child grant that fits the relayed
work. It does not stop the agent from sending under a wider grant of its
own, and it does not apply when the agent acts itself.

Under this subsection the service that holds an identity's request key, the
key holder, signs a run's objects only under what its operator listed for
the origin of that run. For an agent the key holder is the gateway of its
host (key map). The origin is the exact admission that started the run, a
grant and an event, and not the principal: on v3 every admission of one
executor has the same principal (LIP-0004 section 5). The rule adds no key
and no object, nothing on the wire and nothing on chain, and it changes no
v3 byte. It does change behaviour: which signatures a run of an existing
grantee can obtain, and what an owner confirms before enforcing mode. For v4
the same rule stands beside the invocation of LIP-0008 section 12.1.

The key holder keeps three things, all local and all outside the agent's
write authority: the record of each run and its origin, which extends the
record of step 7, `{event_id, grant_id, tip_hash, mode}`; the table of
permissions that its operator sets, with its version; and its journal of
the consents it signed and of the denials of J7.3 (e).

| # | Rule | Refusal |
| --- | --- | --- |
| J7.1 | The key holder MUST bind every run of the identity, when the run is created, to its origin: the `event_id` and `grant_id` of the record of step 7 that admitted its instruction, or the owner's own command. The origin never changes. A run that a run creates, and a run that is resumed, has the origin of the run it comes from. The record of a run and its origin is kept outside the agent's write authority. | none of its own |
| J7.2 | The key holder MUST keep, outside the agent's write authority, a table that its operator sets. For each origin, and for the owner's commands, the table lists three kinds of permission: grants the run may sign under (`use`); parents under which the run may ask for a child (`delegate`); and contracts the run may consent to (`consent`), each given by its contract hash with the booking and privacy hashes. A missing row is an empty row, and an unreadable table is an empty table. The table has a version that only moves forward; the key holder records the version it last used, and a table older than that is unreadable. A permission that the operator removed is checked again immediately before a signature is released, so that a request in flight is not signed under it. | The refusals of J7.3 |
| J7.3 (a) | The key holder MUST refuse to sign an envelope for a run unless the grant that the envelope cites is in the `use` list of the run's origin. For a v4 invocation every grant on its proof path MUST be in that list. | `GRANT_NOT_FOR_RUN` |
| J7.3 (b) | It MUST refuse to sign a kind-8186 delegation request, and a request to a delegation signer (LIP-0014 section 11.1), unless the parent it names is in the origin's `delegate` list. | `GRANT_NOT_FOR_RUN` |
| J7.3 (c) | It MUST refuse to sign a kind-8181 consent unless it was given the complete contract, computed its hash itself, and found the triple of contract, booking and privacy hashes in the origin's `consent` list. The event keeps its four tags. | `CONSENT_NOT_FOR_RUN` |
| J7.3 (d) | A grant that results from a consent of (c) enters the origin's `use` list in one of two ways only. The operator lists it. Or it is enrolled: the operator's consent entry says "and use", and the signed grant shown to the key holder contains exactly the consent event that the key holder released under that entry. For a consent the key holder builds the event and its signature, makes its record of the exact signed event durable, and only then releases it. A run cannot add a grant to its own row in any other way. | A grant outside the list: `GRANT_NOT_FOR_RUN` |
| J7.3 (e) | Withdrawal takes precedence over enrollment. When the operator removes a grant from an origin's `use` list, the key holder records a denial for that origin and grant id. A denial is durable and survives a restart. Enrollment never lifts it: showing the same grant and consent again adds nothing. Only a later act of the operator that lists the grant again, in a newer table version, lifts it. A denial concerns one grant. The "and use" entry itself is a standing permission: while it is in the table, a new consent to that contract can be signed, and the grant that results from it enrolls. To stop that as well the operator removes the consent entry; removing the entry does not by itself remove grants that are already enrolled. A retried enrollment of a grant that was not withdrawn changes nothing. A withdrawal that is recorded before a signature is released wins: the check of J7.2 before release reads the denial. A key holder that cannot show the continuity of its denials and of its consent journal enrolls nothing; only grants that the operator lists are then usable. | A grant under a denial: `GRANT_NOT_FOR_RUN` |
| J7.4 | The key holder derives the run from its own record of the caller: a channel that the key holder, or the launcher it trusts, created for that run when the run was created, and that ends with the run. A run identifier, a principal, a label or a handle that the caller supplies is not that record; nor is a process id that the system may reuse, a socket that another run inherited, or a connection made again after the key holder restarted. After a restart the launcher binds a run again from the stored origin record. If the key holder cannot tell two runs apart, it MUST refuse both, and it MUST NOT fall back to the owner's row. | Nothing is signed |
| J7.5 | The key holder offers a run these typed operations and no other use of the key: an envelope under J7.3 (a); a v4 invocation under J7.3 (a); a consent under J7.3 (c); a delegation request and a request to a delegation signer under J7.3 (b); and the transport operations of the messaging profile, which the key holder builds itself from the message and which authorize nothing. It signs no arbitrary event, no event kind that a caller chooses, no batch that skips the checks and no digest that a caller supplies. | Nothing is signed |
| J7.6 | An instruction admitted under another grant MUST NOT enter an existing run as an instruction. It creates its own run, with its own channel, or stays data. | none of its own |
| J7.7 | A service cannot verify J7.1 to J7.6 and MUST NOT treat a request, a flag or a label as evidence of them. It validates the request, the path and the effect bounds itself. | none of its own |
| J7.8 | Deployment rule. A credential that acts without a signature of the key, such as a repository token or a wallet RPC, is outside this gate. It MUST be out of the run's reach or behind the same binding. | A deployment that leaves one within reach has not closed the case |

With every refusal nothing is signed.

The check itself is a lookup before each signature, at the key holder. The
work around it is larger than the lookup: the caller binding, the isolation
of the signing channel, the version of the table and recovery after a
restart all have to be qualified on the real key holder.

In the case of the first paragraph the origin of `W`'s run is the second
grant. The operator's table lists the first grant only for the origins of
the operator's own work, so the signature under the first grant is refused.
In the relaying case of LIP-0014's motivation the origin of the
orchestrator's instruction lists the child and not the standing grant; that
is what makes that motivation hold.

What the gate gives, it gives at an honest key holder on the agent's host:
a run cannot obtain the identity's signature under a grant that the
operator did not give to the run's origin; a first consent can be signed,
and only for a contract that the operator listed; and the key has no other
signing path. Six things stay open:

- **The host.** The gate is enforced on the agent's host by a service of
  that host's operator, which already holds the key. It protects against a
  confused or manipulated agent and not against that host. No receiver can
  see whether the gate ran.
- **The task.** A run whose origin lists a grant can use everything that
  grant allows. The gate does not intersect the grant with the task that
  started the run, and runs of one identity that share files can pass text
  to each other.
- **Credentials.** A credential that needs no signature bypasses the gate
  (J7.8).
- **The table.** A wrong row gives a wrong bound. The default is empty.
- **The standing entry.** "And use" is a standing permission. Removing one
  enrolled grant denies that grant for good; it does not stop a new grant
  under the same contract while the consent entry stands. An operator who
  wants both removes both.
- **The stores.** The denials, the table version and the consent journal
  must tell "empty" from "lost". The profile for that is open; until it
  exists, a key holder that lost them is one whose operator sets it up
  anew.

The owners decide five things with this text:

1. Whether to adopt the gate, with the six open points recorded. The
   proposal is to adopt it.
2. Whether the gate is a condition of enforcing mode. The case of the first
   paragraph arises with one-hop grants and does not wait for
   re-delegation. The proposal is that each owner confirms, with its
   approval of enforcing mode (section 3.4), that the key holders of its
   grantee identities run the gate; an executor cannot check that. Left to
   deployment, the first enforcing executor admits the case.
3. The threat boundary. The proposal is an honest key holder and an
   untrusted run, as here. A gate that also holds against a hostile host
   needs a signed origin that the receiver checks, with an authorizer and a
   custody boundary that the host does not control; one more label signed
   by the same host adds nothing. That stays an open option for v4.
4. Where the operator's table lives while sections of an agent host's
   configuration are unsigned (K4 of the key map). The proposal is a file
   of the key holder's OS user, outside the agent's write authority, set by
   the operator, with the version of J7.2, and without a signature until
   the trust anchor of LIP-0015 exists.
5. The presence rule of the key map. It asks for presence per signature for
   every key that a grant names as grantee, before the executors that admit
   it enter enforcing mode. An agent's key cannot have a person for each
   signature. The proposal is that for a grantee key that belongs to an
   agent the gate takes the place of presence, that presence stays for a
   person's key, and that the key map says so. If the rule is kept as it
   reads, no agent can be a grantee at an enforcing executor. Without this
   decision the gate and the key map contradict each other.

Four other designs were set aside. A grant per run puts one issuance on
chain for every run. The Link book estimates, at 355 bytes for an issuance
record, that 100 000 agents with ten runs a day need about 355 million
bytes of block space a day, about 2.4 times the 146 million bytes that a
day of blocks holds; the figure counts issuance records only and is an
estimate, not a measurement. A context keyed by the principal tells
nothing apart, because the principal is the same for every admission of
one executor. A list of grants that the creator of a run writes trusts the
party under suspicion. A table of actions, targets and expiry for each
origin would narrow what a run can do under a listed grant; it is a policy
language at the key holder, and the first version lists grants, parents and
contracts and says what that leaves open.

Cases (owner decision pending: J7). Their identifiers begin with S7, for
this decision. Every case runs against the real signing endpoint with real
callers; a helper that is handed a trusted run identifier tests nothing. On
a refusal the test checks that no signature exists. Today no gate exists,
and the signatures that S7-1 to S7-3 refuse are given:

| Case | Valid control | Refusal or invariant |
| --- | --- | --- |
| S7-1 | A run whose origin lists `Gy` signs an envelope under `Gy` | Same identity and key: a run whose origin is `G2`, without `Gy` in its row, asks for a signature under `Gy`: `GRANT_NOT_FOR_RUN`. This is the case of the first paragraph. |
| S7-2 | A typed envelope under a listed grant, and a kind-8186 request under a parent listed for delegation, are both signed | An otherwise valid kind-8186 request for a parent that is not listed; an arbitrary event; a supplied digest; a batch or alternate route: refused. A blanket ban on kind 8186 fails the control. |
| S7-3 | A run created by the owner's command signs under the owner's row | A caller that supplies the owner's label or another run's identifier; a copied handle; a reused process id; a reconnect after the key holder restarted: refused, and never the owner's row. |
| S7-4 | From no grant, a run whose origin lists the contract obtains the consent; the issuer signs the grant; with "and use" the new grant becomes usable by that run, and a later envelope under it is signed | A consent for a contract that is not listed: `CONSENT_NOT_FOR_RUN`. A grant that does not contain the consent the key holder signed is not added to the row. Placeholder grant ids and a grant consented in advance hide the case and are not this test. |
| S7-5 | A second instruction under the same origin continues the run | An instruction admitted under another grant gets a run and a channel of its own, or stays data. Changing a label on the same channel is not that. |
| S7-6 | A run started or resumed from a run keeps the origin and the current row | After the process and the session were re-created, and after an older table was put back: no signature under a grant missing from the current row; the old table is unreadable. |
| S7-7 | A known caller and a readable row: signed | Three separate negatives: an unknown caller; no row; an unreadable or corrupt table: nothing is signed, and no fallback to every grant of the identity. |
| S7-8 | At a receiver: a valid request is admitted on its own checks, whatever untrusted run label accompanies it | A request with an invalid grant, path or bound is refused although a label says the gate passed. The signed bytes are not altered in this test. |
| S7-9 | A permission is in force and a signature is released. A removal recorded after a release leaves that signature as it is and refuses the next request; a retried enrollment without a removal changes nothing; a grant that the operator lists again in a newer table version is usable again | The operator removes the permission while a request is in flight, and the removal is recorded before the release: no signature is released. The origin's consent entry says "and use", grant `G` is enrolled, the operator removes `G` from `use` and keeps the consent entry; the run shows the same `G` with the same journalled consent again: `G` is not added, and a signature under `G` refuses as `GRANT_NOT_FOR_RUN`, also after a restart of the key holder. A removal that races the enrollment itself ends with `G` denied. With the consent entry still present, a new consent to the same contract is signed and its new grant enrolls: that is what the standing entry means, and removing the entry stops it. |

A deployment check goes with these cases and is no protocol vector: a
repository token or a wallet RPC within the run's reach produces the
forbidden effect without a signature. Finding one is a failed qualification
(J7.8).

## 4. Vectors and reference checker

[`vectors/LIP-0013/trust-vectors.json`](../vectors/LIP-0013/trust-vectors.json)
holds:

- four valid contracts (`instruct`+`review`; `land` with two repositories;
  `spend` with a budget; all four actions with a 280-byte note that contains
  a quote and a backslash), each with its exact bytes, hex, SHA-256, derived
  v3 scope and budget, and consent tags;
- 32 invalid contracts, each one defect away from a valid one and each with
  its expected section 2.3 code, including a sign on an integer and a
  non-ASCII character or a `\n` escape in a string, which refuse under
  rule 1;
- 15 bindings: each valid contract against its matching grant fields, and 11
  defects with their section 2.5 codes;
- 26 envelopes signed with BIP-340 published test keys: 7 that pass every
  offline step, including both window edges and an amount equal to the
  budget, and 19 refusals with their expected codes.

The keys are the secret keys of BIP-340 test vectors 0 and 1, published for
testing. They are not keys of any party. Grant ids are placeholder digests,
not issued grants. Signatures use BIP-340 with `aux_rand` of 32 zero bytes,
so any conforming implementation reproduces them.

The envelope vectors cover steps 3, 4 and the offline part of 6 (6a, 6b, the
grantee comparison of 6c, 6d to 6g). They do not cover `rental.Check` on a
node, the contacts pin (step 5), holding and retry, journal persistence or
the mode (section 3.4). `PASS` in a vector means "passes every offline step",
not "admitted"; in shadow mode not even a live, fully checked envelope is
admitted.

[`tools/trustcheck`](../tools/trustcheck) recomputes every vector:

```text
go -C tools/trustcheck run . check ../../vectors/LIP-0013/trust-vectors.json
```

It prints one `PASS` or `FAIL` line per vector and a summary, and exits 0
only when every vector gives its expected result. `go -C tools/trustcheck run . gen`
regenerates the file byte for byte; `go -C tools/trustcheck test ./...`
checks the signing path against BIP-340 vector 0, the generator against the
committed file, and that planted defects fail with their named codes.

## Alternatives

- **Reuse a v3 scope name for `instruct`** (for example `deliver`): rejected,
  because it reinterprets signed v3 bytes.
- **A new consent tag such as `swarma-trust-consent-v1`:** rejected for v3,
  because v3 fixes the `t` tag; the profile tells the grant types apart
  (design Q6).
- **Contract fields in any order, compared semantically:** rejected. Two
  encodings of one contract would give two hashes for one meaning.
- **Envelope tags in any order** (the kind-8183 precedent): rejected for a
  single event shape per instruction.
- **Wait for v4:** v4 has no adopted bytes. By the owner's decision of
  2026-11-12 the first public demonstration also runs on the implemented v3
  rental profile, as it is, and v4 follows that demonstration. Per-action
  signed limits and name-bound grantees come with v4.

## Security consequences

- **No new v3 authority.** A trust grant never widens a v3 scope: the scope is
  derived from the contract, and a mismatch refuses (section 2.5).
- **Ignoring the contract loses only narrowing.** For `land` and `spend`, an
  executor that does not apply this profile still sees `repository.push` or
  `pay` with the budget and could act on any repository. An executor that
  holds trust grants MUST apply section 2.5 and steps 6d to 6g. For
  `instruct` and `review`, v3 alone authorizes nothing.
- **Key-only grantee.** Authority is the grantee key, as in v3. A rotated
  grantee key needs new grants. The `mxid` and `room` tags bind the signed
  envelope to one Matrix context; they confer no authority.
- **No authority before enforcing mode.** Until the first proof has passed
  and both owners have approved enforcing mode, a verified envelope confers
  no authority: the executor reports it, the message stays data and only the
  owner directs (section 3.4). An executor that cannot read its mode runs in
  shadow mode.
- **One key, every run.** A grant is issued to a key. Every run of the agent
  that holds the key can act under every grant issued to it, whichever
  party's work that run is doing. An agent that works for two parties can
  thereby carry one party's instruction into an action under the other
  party's grant. Section 3.6 states the case and holds Draft text for it,
  under a pending owner decision (J7); it is open question T10.
- **Replay and delay.** The nonce journal and the time window bound replay.
  Holding a pending envelope does not reopen the window (section 3.5).
- **Public graph.** On mainnet, names, keys and the bundle make "who trusts
  whom" public (design Q12). The `note` holds nothing private.
- **Test keys.** The vector keys are public. Any key whose secret appears in
  BIP-340 or in this repository MUST NOT be used for a real grant or
  envelope.

## Conformance impact

None while this LIP is a Draft. The vectors are draft vectors for this LIP,
not a conformance class. Adoption follows LIP-0001: a decision record, the
protocol text and a conformance change that names the vector set.

## Open questions

| # | Question | Proposal here |
| --- | --- | --- |
| T1 | Adoption: do thin tools around v3 with this profile count as "v3 as is" under the decision of 2026-11-11 (design Q1)? | Yes; Ivan confirms explicitly. |
| T2 | Agent names (design Q5) | `id/<owner>-<agent>`, for example `id/ivanopcode-keeper`, as in the vectors; `id/swarma` stays a social or brand name. |
| T3 | Kind number (design Q10) | 8185 is a draft allocation, not an allocated kind. It is unused in chain-lab and in this repository as of 2026-11-12, and the review of this LIP found no 8185 entry in the public NIPs index that day. Neither search allocates the kind or excludes an external deployment; the question stays open until adoption. |
| T4 | Non-ASCII notes | ASCII only in `/1`; a non-ASCII character in any string, the note included, refuses as `CONTRACT_ENCODING` (section 2.3). UTF-8 would need a byte rule and a normalization rule. |
| T5 | Phase A carriage: does `a2a post` preserve the body octets, including the LF and the fenced block, end to end? | Unverified; until it is, the text hash is computed over what `a2a inbox show` returns, and a mismatch refuses as `BODY_MISMATCH`. |
| T6 | Repository identity: exact bytes, no `.git` or case folding | Exact bytes; an issuer lists every spelling it means. |
| T7 | Whether an issuer MUST, rather than SHOULD, omit a zero v3 budget | SHOULD; the verifier compares the value, so both forms bind. |
| T8 | Nonce journal key: the nonce alone, or the pair of signer and nonce | The nonce alone, as the kind-8183 precedent does. |
| T9 | Leaving enforcing mode: who may return an executor to shadow mode, and what happens to admitted instructions not yet in effect? | Either owner at any time, since it only removes authority; admitted work not yet in effect goes back to the owner. Undecided. |
| T10 | A gap found in review: a grant is issued to a key, and every run of the agent that holds the key can act under it. Section 3.6 states the case. | Draft text in section 3.6, under a pending owner decision (J7): the service that holds the agent's key signs a run's objects only under what its operator listed for the origin of that run. This adds no record to the chain. Undecided. |
