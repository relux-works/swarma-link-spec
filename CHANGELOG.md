# Changelog

## 0.1.67 — 2026-11-20

Net change over 0.1.66: re-file the earlier action-profiles draft as
LIP-0038, leaving LIP-0032 for credentials. No implementation, adoption,
wire members, vector changes or production migration is claimed.

- Add the four PROPOSED leaves `swarma/post-message`,
  `swarma/spend-coins`, `swarma/name-update` and `swarma/model-call`,
  preserving their original scope and reservation-before-effect checks.
- Record the owner's option A settlement decision of 2026-11-20, event
  `$VY_Ow-Yi4YWA695VYxcLlg0EdizZ6p8UzPkpr37ZyGU`: actual consumption
  is charged and the difference released, by one shared rule referring
  to LIP-0031 L9. Add a reserve-10/actual-4 control and one-defect case
  for each shared kind, plus the unknown-outcome retention countercase.
- Reference LIP-0031's existing resource/unit/period forms, exact
  accounting and refusal order instead of proposing incompatible kind
  definitions. Index LIP-0030's distinct grant leaves and station kinds
  alongside LIP-0038 in LIP-0020 W11.14; halt remains an owner command.
- Reconcile LIP-0035's scoped unilateral roots, lowercase slash actions
  and W11.4 limit arrays; LIP-0034's auth-key separation; and LIP-0010
  section 11's manifest service declaration, which supplies discovery,
  not authority. Preserve all other Draft/PROPOSED status and open points.
- Update the README version/LIP list and UNRESOLVED_QUESTIONS; unchanged
  trust and grant checks still do not qualify these new action profiles.

## 0.1.66 — 2026-11-20

Net change over 0.1.65: six new Draft proposals, LIP-0032 to LIP-0037,
reconciled with Ivan Oparin's decisions of 2026-11-20. Those decisions take
precedence over conflicting older Draft/PROPOSED text; the co-author's
agreement on every amended decision is pending. No implementation, adoption,
production name migration or deployed reader support is claimed.

- LIP-0010 section 11 defines one `swarma-manifest` head and document,
  carrying device, holder, certificate and card heads and the LIP-0007
  declaration. It frees the 150-byte reserve and recomputes the 520-byte
  budget. Legacy H8 stays explicitly readable; mixed forms refuse. Manifest
  counters strictly increase; set counters do not decrease. Inline-only
  operation and the per-verifier reader rollout gate are explicit.
- LIP-0032 separates credential issuance from notary attestations, retains
  typed notary `/2` for its two kinds, uses LIP-0020 canonical/digest rules,
  assigns credential actions `0x09`/`0x0a` and authenticated compromise-break
  action `0x0b`, and preserves eternal anchors below `h_c`. Credential anchors
  cover signed bytes, not precomputable payload digests; a break may close
  an authorized retired key without republishing it. LIP-0012,
  LIP-0014, LIP-0020, LIP-0021 and the key registries are reconciled.
- LIP-0033 makes delivery non-exclusive, keeps `LIST_UNKNOWN`, assigns
  dedicated Nostr kind 30079 and 32-byte event-ID location `0x05`, preserves
  SSRF boundaries and clarifies inline step 0 in LIP-0019. Neither the
  name nor manifest has `loc`.
- LIP-0034 uses a dedicated BIP-340 auth key and registered typed challenge/
  upgrade objects, with paired manifest auth key/seal, TTL at most 120 seconds
  and atomic replay-safe upgrade. Device keys stay internal; cold keys never
  log in. Existing key derivations win over conflicting v0.3 path proposals;
  fixed auth/reserve accounts 2/3 stay outside the dynamic 10+ pool.
- LIP-0035 selects scoped Option B: no contract only for root EFFECT grants
  without `delegate`, never hire/rental. LIP-0017 C5/C12 and LIP-0020 consent
  and W11.2 are scoped accordingly. Private delivery, targeted single-use/
  standing modes, no obligations, no delegation and durable revocation stay.
  Preparation `/2` and issuance payload `0x03` specify both unilateral branches.
  The editor also accepts an optional signed unilateral mandate contract,
  exact grant equality, signed broker invocation and externally fenced
  single-use journal. The mandate's checked signature is bound in `/2`,
  without separate assent or recipient consent; W9.4 orders equality and
  scope checks. Contract-byte routing applies only to the mandate branch;
  ordinary `/1` root issuance keeps section 10's given contract identifier
  and needs no contract bytes. Later F6(a)/C6 checks reject a mandate
  presented as an ordinary contract with `ISSUANCE_MODE`.
  Journal continuity keeps LIP-0025's existing loss/fencing
  codes and precedence; root wire/scope and child refusals are unambiguous.
- LIP-0036 composes credentials, supported screening limits and a human-gated
  disclosure grant, with `curator-trust` explicitly external, role-separated
  hub names and direct Contour A PII routing that bypasses screening hubs. LIP-0037 is
  the unsigned manifest-only identity card, with full relays/transports,
  projection boundaries and future signing option (d) left open.
- Each new LIP has an extension checklist, ordered refusals and a conformance
  section. Draft vectors are not required. Exact child-notary v2 mapping,
  selective-disclosure proofs and application profiles remain open, not
  invented byte fixtures. Decision provenance cites the binding record;
  editorial/v0.3 resolutions do not claim owner-decision status. No existing
  vector or checker is changed; their new-branch coverage gap is explicit.


## 0.1.65 — 2026-11-20

Net change over 0.1.64: records the owners' K3, b1 and c1 decisions, with
their dated sources, in section 2.4 of the LIP-0014 Source-contract
companion. Only an owner (KEY-MAP K3) creates an agent identity; the
homeserver registration credential is the owner's secret, outside every
agent's reach; the new account's access token goes straight into keyvault
custody. The enrollment contract lives in the keyvault specification,
`docs/agent-enrollment.md` (swarma-keyvault PR #123, merged on 2026-11-20 at
`eb103c8f361ce430589c50b26e42604c43b2e83e`); that text remains **PROPOSED**,
and merging it is not acceptance. On acceptance, Link cites it rather than
restating it. The Enrollment register and B1/B2 question entries distinguish
the decided custody and contract home from the still-OPEN B2 registration-route
mechanism and acceptance of the keyvault text. Section 2.4 retains the owners'
b1 wording and records the keyvault decision record's differing date,
deployment scope and holder; the scope and owner/administrator identity
remain OPEN, and the keyvault text must align before acceptance. Acceptance
with those gates retained remains the replacement trigger. Section 11's
proposed paired control requires a named and accepted B2 mechanism and aligned
decision records, and refuses before reservation and network submission if
either is missing. The decision record clarifies owner and co-author
terminology, notes the cited book deviation, and names the deciders of the
remaining B1/B2 questions. The transaction clauses stay **PROPOSED**; no
normative rule, wire member, vector or implementation changes, and no
qualification or adoption is claimed.

## 0.1.64 — 2026-11-19

Net change over 0.1.63: a PROPOSED clarification of LIP-0014 section 8.4,
row F11. A channel that yields no key contributes no key to compare. A
value refused as a whole under LIP-0010 section 2 makes F11 refuse
without closure; the code remains open (O9). Section 8.7 adds two planned
vectors on stated facts with controls. The open-points rule of section 8.4 admits
`step-f-51` for the refusal alone, not its code. Nothing is adopted and
no wire member changes.

## 0.1.63 — 2026-11-19

Net change over 0.1.62: revises only the PROPOSED enrollment boundary in
section 2.4 of the LIP-0014 Source-contract companion, its decision register,
paired valid and forbidden controls, and the companion's indexes. It
conforms the proposed registration authority to KEY-MAP K3, distinguishes
homeserver accounts from ledger and OS accounts, bars the enrollment role
from writing H1 records and the enrollment journal from writing station
state, and places the proposed
registration/create route inside the owning native custody executable.
It states the owner-only closure of unresolved transactions, the refusal
before network submission while owning inputs are undefined, and the
accepted-source replacement condition.

Review amendments to C1-C6 make C5's register closure require the owners'
custody decision for both the registration credential and the new account's
token, replace the dangling child-token reference with the new account's
access token, and add three paired controls for H1 fidelity and unchanged
H1/station state, owner-only closure, and refusal while owning inputs are
undefined.

B1 (adoption and home), B2 (custody of the homeserver registration credential
and of the new account's token), B3 (the process boundary) and B4 (native
management-code admission and the required session policy) remain OPEN.
Section 2.4 stays PROPOSED: nothing is adopted and no owner-reserved choice
is decided. No existing normative rule, wire member, tool or vector changes;
no implementation, native qualification or end-to-end conformance is claimed.

## 0.1.62 — 2026-11-19

Net change over 0.1.61: makes the LIP-0014 source-contract companion's
adoption boundary state that its remaining content is proposed and updates
the companion date. No normative rule, wire member, vector or implementation
changes.

## 0.1.61 — 2026-11-19

Net change over 0.1.60: records three owner decisions on the contract
seal as an amendment of Draft LIP-0017, registers its proposed refusal
codes, and inserts the bound/framework contract-seal check in the existing
child admission order and LIP-0030 start admission. The limit-kind profiles
added in 0.1.58 are retained; the agent-session profile and child-issuer
companion of 0.1.59 and 0.1.60 carry the seal check and updated controls.
No member of `swarma-grant/4` changes, and no octet of a tool or vector file
changes. Every LIP stays a Draft, and nothing of this version is
implemented.

**State, and its source.** Ivan Oparin decided the three points on
2026-11-17. In event `$KhhzZv1s7jj238dOQ_cnvhJbUXZta1R19JU748Fiutw`
of 2026-11-17 the co-author wrote «ок, звучит вроде разумно , но я доверюсь Ване)»:
the co-author agrees and leaves the judgement to Ivan. LIP-0017 stays Draft;
adoption follows LIP-0001, and no earlier order is stretched to it. What
is decided and what is this draft's form are stated apart in each place:
the refusal without
a confirmed seal, at the issuer's signing service and at every verifier,
is decided; the code names, their place in the order tables, and the two
scope readings below are proposals of this version.

- **The seal decides termination (LIP-0017, decision C10; section 5,
  rule 6; section 6, rule 7).** The termination type of a contract is the
  type of its seal: issuer only, either party, both together, or arbiter,
  per its script. The type is a machine field of the contract, and every
  reader, renderer and user interface MUST show it from the seal script
  and MUST NOT take it from prose. Section 5, rule 6, already said that a
  clause in words ends nothing; it now says the same of a type that prose
  states. Where prose and script differ, the script decides what is shown
  and what ends the contract. A contract with no seal has no type to
  show, and none is supplied from its prose. Which script gives which of
  the four types is fixed with the scripts of the four clauses, which
  stay open.
- **Drafting starts with the seal (LIP-0017, decision C11; section 6).**
  The parties first create the seal output; the contract then names it
  and is signed only once it is confirmed. That the seal is confirmed
  before the contract is signed is the sentence that section 6 already
  had; the order before it is new. The identifier of the contract, which
  commits to the parts other than the clauses (section 2), therefore
  commits to a seal that already exists.
- **No grant without a contract seal (LIP-0017, decision C12; section 5,
  rule 7; section 6, rule 6).** A v4 grant, and a grant under a framework
  contract, MUST NOT be issued under a contract without a confirmed seal
  (the scope of section 6). The landed minimal v3 path needs no contract
  seal; whether C12 reaches it is open against C8. The signing service checks
  before it signs, and every verifier at admission, each on its own node
  in its observation, that the bound contract and any named framework
  each name a seal and that the node
  shows it confirmed as named: the named transaction confirmed in the
  active chain, an output at the named index, and its script octet for
  octet the named script. A contract that names no seal, or whose seal
  the node does not so show, is refused by both sides with no signature
  and no closure. Two proposed codes are defined once in LIP-0020
  section 11.11: `CONTRACT_SEAL_MISSING` for no seal named or a conclusive
  node finding, and `CONTRACT_SEAL_UNAVAILABLE`, pending, for an unknown
  transaction or read that proves nothing. Node knowledge is established
  before a node finding; the bound seal is checked before the framework's.
  A seal conclusively shown confirmed as named and then spent is neither
  code: it ends the contract under rules 1 and
  2 of section 6, and its step, code and closure stay open. A read that
  proves nothing is pending, not proof of a missing seal; no side signs or
  admits on it. Equal chain tips alone do not imply equal read availability.
- **Scope, as this draft reads it.** LIP-0017 section 6 is for v4 grants
  and for framework contracts and says that Grant v3 does not change
  (decision C8). Sections 5 and 6 read C11 and C12 in that scope: a
  contract that a v4 grant binds and a framework contract MUST name a
  seal, a minimal contract that a v3 grant binds needs none here, and a
  contract under which no grant is issued and which is not a framework
  contract may have none, as the last row of
  section 7 has it. Whether the owner meant the ban for every grant, v3
  included, against C8, and whether C11 takes the seal-less contract
  away, are open and are stated in LIP-0017 and in the unresolved
  questions. In section 1 the part "Seal" is no longer "Optional"
  without qualification, and the rental row of section 7 now ends by the
  contract seal as its script states, beside the seal of each grant.
- **The step of a v4 child (LIP-0014 section 8.4, row F6, part (c); rule
  T11; pair Q28; case S8-30; section 8.5, I4).** Row F6 gains one part
  and no row is added: after the contract has recomputed to the
  identifier that both grants bind, and before the findings that wait
  for a v4 contract profile, both sides judge the confirmed contract
  seals and distinguish `CONTRACT_SEAL_MISSING` from a pending
  `CONTRACT_SEAL_UNAVAILABLE`. A document that names no
  seal is reported there and not under the open code of the profile
  findings. The part that version 0.1.55 numbered (c) — a valid contract
  of its profile, mirroring the terms of each grant — is part (d) since
  this version, and each place that cited it says so: rules T1 and T11,
  open point O4, sections 8.5 (I4), 8.6 and 8.7 of LIP-0014, and
  LIP-0020 section 11.11. Texts of versions 0.1.55 to 0.1.60 that cite
  part (c), the entries below among them, mean that part. Current
  references in LIP-0031 and the child-issuer companion now name (d);
  the W11.14 limit-kind registry introduced in 0.1.58 is unchanged. The
  vectors
  `step-f-39` to `step-f-49` are planned on stated facts, as every result
  at or after part (b) is, and none is generated; none is planned for a
  spent contract seal. Because part (c) reads a node, it stands in the
  repeat of step 6 of the order of one request (LIP-0014 section 11.1)
  between I3 and I5, refused there as event 12 with the place held; the
  principle of that step, every check of step 1 that reads a node or a
  journal, already reaches it, so only its enumerations, there and in
  row I11 of section 8.5, are amended in place and marked there.
  I4 lists both seal codes; case S8-33 pairs a sound fresh-read control
  with conclusive and unavailable framework-read failures in that repeat.
- **The start verdict (LIP-0030 C6, N1 and section 6 list 3).** The
  0.1.58 citation is extended to the 0.1.61 F6(c), T11 and Q28 amendment.
  The root and child check both required contract seals; the child's
  place is F6(c), while the root remains **P** with no proposed order
  against other root checks. Seal refusals precede the session entry,
  debit and start order. S30-73 to S30-77 pair controls with root, child,
  framework, unavailable-read and post-clearance negatives. N12 leaves
  the event and stop path for a spent contract seal open.
- **The wire registry (LIP-0020 section 11.11).** A grant gives its
  contract seal through `contract` alone: no member of `swarma-grant/4`
  names it, which the table "Which rule reads which member" now states.
  The new codes are registered beside the codes of version 0.1.55, in the
  state of W11.11. They are no fifth comparison of W11.11, which keeps its
  four. For a root grant the duty and the codes are the same (LIP-0017
  section 6, rule 6), and no step table fixes their place among the checks
  of a root; none is proposed.
- **Left open.** Every form that this version marks as its own:
  the code names and their place; the two scope readings; framework
  presentation and resolution; how a node is read for the confirmation and the
  script of a contract seal against one tip; the step, the code and the
  closure for a spent contract seal; and the scripts of the four
  termination clauses, with the rest of LIP-0017's open questions.

## 0.1.60 — 2026-11-19

Adds a companion to LIP-0014, `lips/LIP-0014-source-contract-proposals.md`.
It collects **PROPOSED** choices for H1 (identity latch), T1 (contract
profile), the action-profile mapping and the points O1 to O8 of LIP-0014
section 8.4. Each choice has its acceptance condition and paired valid and
forbidden cases.

- It points to LIP-0026 section 8 for the state of the R8.3 count order.
- LIP-0014 section 8.4, README and UNRESOLVED_QUESTIONS gain a pointer
  paragraph.
- No LIP is adopted, and no rule, wire member, vector or implementation changes.

## 0.1.59 — 2026-11-19

Adds Draft LIP-0030, action profile no. 1, an agent session on a host.
It proposes the authority that a v4 grant gives the host's service set,
separate from the process lifecycle of station/1 version 1. No rule of
the profile is adopted by this version, and nothing of it is implemented.

- **Session authority.** Five action leaves for start, restart, renewal,
  stop and owner halt; starts, level and span limits; height leases;
  checker verdict content and currency; and a five-state authority table
  covering 36 events, with journal-before-effect rules and refusal codes.
- **Admission and station boundaries.** Authenticated root-issuer input
  solely for selecting start classes, never lifting a human stop; atomic
  final profile and human-stop rereads with R03 in the one store;
  restart ordering, quarantine after store loss, and mappings to admitted
  station/1 stop triggers. Five unsupported direct stop reasons and their
  DI requester authority are proposed additions, not admitted runtime
  behavior; refusals retain the stop duty and bar slot reuse without proof.
- **Draft index and open decisions.** README and unresolved questions
  record the profile, its owner choices and station-integration gaps.
  No grant member, wire schema, tool or vector octet changes.

## 0.1.58 — 2026-11-19

Adds Draft LIP-0031, the first three limit-kind profiles for Grant
v4, and enters their kinds in the registry of LIP-0020 W11.14.
The paragraph of section 5 that states the four rules is decided
by the owner on 2026-11-17 and in force in this version; every other
rule of it is proposed, nothing else is in force by this text, and
neither owner has
decided another rule of it. The owner's requirement of the same day
that a period be expressible in clock time and, for chain coins, in
blocks is recorded in the LIP, and the rules that carry it are
proposed like the rest. No member of
`swarma-grant/4` changes, and no octet of a tool or of a vector file
changes. Every LIP stays a Draft, and nothing of this version is
implemented.

- **Three limit kinds (LIP-0031).** Until a type profile defines a
  limit kind, a child that states a limit is neither signed nor
  admitted (LIP-0020 W11.14 rule 2). LIP-0008 section 2 lists the
  kinds by meaning, and LIP-0018 section 2 lists what a proposal for
  a kind states. LIP-0031 proposes a profile for each of
  `swarma/coins` (asset and payment-system identifier, atomic unit,
  maximum for one spend, maximum for a period, total over the term
  including fees), `swarma/model-cost` (cumulative ceiling per
  period, exact currency and scale, reserve the maximum and settle
  the actual) and `swarma/model-tokens` (separate cumulative input
  and output ceilings per period under a named model and
  token-accounting profile), each with every item of LIP-0018
  section 2, the comparison of a child against the template of its
  row and the pool of its parent, and who meters on what evidence.
  The kinds share one reading of `period` and one account for each
  period instance. That reading states the period item of
  LIP-0018 section 2 for every kind: clock time for all three, and
  blocks of the chain for chain coins, with the half-open instance
  arithmetic and the reorganisation cases; clock-only periods for
  the two model kinds are a draft choice. Fixed-length epoch
  seconds do not define calendar months, years or local-time days;
  those remain open. A child's period counting must be its
  template's. Three codes are new: `LIMIT_UNSUPPORTED`, `SPEND_OVER`
  and `LIMIT_CLOCK_REGRESSION`; the rest are codes that landed texts
  already name. The new ledger check stands after the per-request
  ceiling and, for each clock-counted key, before its own account,
  even where LIP-0022 does not run; it changes no observation code
  or order. An unbounded model request refuses `SPEND_OVER` where
  its per-request key is stated, or at reservation otherwise.
  Debits, sums, products and accounts are
  exact integers, with no wrap or rounding and refusal on overflow;
  L17 and L18 compute rational costs exactly over the whole request,
  without binary64 or rounding any price or part, then convert
  upward once each for reservation and settlement. Paired text
  fixtures include the overshoot with room, unbounded model
  requests, clock-refusal order, exact-room and 2^64 boundaries,
  fractional over- and under-reservation, sum-before-rounding and
  settlement; named mutation witnesses narrow the fractional
  regression. The vector set is described and not built.
  Even at a side that runs a profile, row F6 of LIP-0014
  section 8.4 ends every child admission before F17 until a v4
  contract profile exists.
- **Exhaustion and continuation (LIP-0031 section 5).** One
  paragraph, decided by the owner on 2026-11-17 and in force in
  this version, states what an exhausted counter does and how work
  continues; this entry, the README and the unresolved questions
  point to that paragraph and restate none of it. Every draft
  interpretation is outside section 5 in a separate PROPOSED
  subsection with no interim force: the extended trigger, report
  recipients and root continuation are not decided. Under that
  PROPOSED reading, a refused overshoot or unbounded maximum does
  not exhaust remaining room.
  The relation of the fourth rule to both the whole-term and the
  no-new-grant sentences of LIP-0008 section 2.1 remains open, as
  does a code for any post-stop request that L8 would admit.
- **The registry of limit kinds (LIP-0020 W11.14).** The three
  kinds enter the table, each proposed by version 0.1.58, LIP-0031.
  At a side that runs a profile of that LIP the kind is judged under
  it in rows F17 and E2; at a side that runs none, rule 2 refuses as
  before. The registry of action identifiers is untouched, and no
  rule, code placement or octet of section 11 changes beside the
  entry, W11.4's sentence on the registry and type profiles, the
  two prose sentences of W11.14 that state its effect at
  a side that runs a profile and at a side that runs none, and the
  framing of the table that holds it.
- **Unresolved questions.** Two rows: the limit-kind profiles, with
  what they leave open, and exhaustion and continuation, which
  points to LIP-0031 section 5. One clause of the row "Members of
  `swarma-grant/4`" no longer says that section 11.14 states the
  registries as empty.

## 0.1.57 — 2026-11-17

Puts one owner decision in force and closes the contradiction that version
0.1.56 recorded. No member of `swarma-grant/4` changes, and no octet of a
tool or of a vector file changes. Every LIP stays a Draft, and nothing of
this version is implemented.

- **The order of the count of rows (LIP-0026 R8.3 and section 8; LIP-0014
  section 8.4, row F13).** Ivan Oparin accepted the order explicitly on
  2026-11-17: the groups in their signed order, the ranges of a group in
  their signed order, the coins of a range by ascending output index,
  counted from 1. LIP-0026 section 8 now states the order in force since
  this version, as LIP-0020 W11.6 has stated it for the octets of a parent
  since version 0.1.53; row F13 points to that state. The rest of proposal
  Q2 stays proposed.
- **Unresolved questions.** The row "Order of the count of rows (R8.3)" is
  removed: the owner's decision answers it.

## 0.1.56 — 2026-11-17

Closes three findings on the step table and the reservation ledger of
version 0.1.55, records one owner decision on the names of working agents,
and adds two proposals and one contradiction to the unresolved questions.
No member of `swarma-grant/4` changes, and no octet of a tool or of a vector
file changes. Every LIP stays a Draft, and nothing of this version is
implemented.

- **Step 6 and the words it reads (LIP-0014 sections 8.4 and 11.1).** The
  Amends list of section 8.4 now names rule J4.4 (c) and event 12 of the
  table of states beside step 6 of the order of one request, whose words
  "the checks of J4.4 on the parent and on the row" step 6 reads as naming
  the checks that it lists. The pointer after that order in section 11.1
  states the same: no rule of J4.4 (a) to J4.4 (g) changes its words, rule
  J4.4 (c) keeps its words, and event 12 keeps those words and gains one
  sentence, as the next bullet states, marked there.
- **The coin spent by the child's own anchor before the second check
  (LIP-0014 sections 8.5 and 11.1).** Where the confirmed issuance anchor
  of this child spends the coin of its row between step 1 and step 6, the
  repeat refuses as `ROW_COIN_REQUIRED` (event 12), the place is held and
  no signature of the ledger exists; the service also writes an entry of
  the operational audit and notifies its operator that a signature exists
  outside the ledger, as in event 39. The sentence is introduced with
  version 0.1.56 as normative text, in step 6 and in event 12 alike, each
  marked there. Case S4-30b states the case with S4-11 as its control.
- **The kinds of entry (LIP-0014 section 11.1).** The entry-kind list of
  J4.4 (g) is carried, unchanged, into the text of the table of states
  where the kinds are referenced: the entry of a delegation key, a
  reservation, a use of the key, a result, a reconciliation and a genesis,
  with the words of J4.4 (g) for each.
- **Names of working agents (key map).** By the owner's decision of
  2026-11-16 a long-lived working agent has an `id/` name of its own, as a
  permanent role does; a one-task executor that a grant names by key may
  stay key-only. The scope of K2 in the key map states the decision, and
  the flow for registering an agent's identity applies to a long-lived
  working agent as it does to a permanent role. No new member or field is
  stated.
- **Two proposals, in the unresolved questions alone.** Neither is
  normative and neither binds a reader. The first: no new key assents to a
  child's contract; the child's contract must equal the parent's, and the
  delegator's existing signature on it counts. The second: the agent's
  message key is pinned in the value of the agent's own `id/` name.
- **Left open, with both texts as they are.** The order of the count of
  LIP-0026 R8.3: LIP-0020 W11.6 states it in force since version 0.1.53,
  and LIP-0026 section 8 states it proposed in force with the owner's
  explicit acceptance pending. One line of the unresolved questions names
  the contradiction and the two ways out. Neither text changes.

## 0.1.55 — 2026-11-16

Proposes one step table for a v4 child, with the codes and the order of
every step, for the signing service before it signs and for a verifier at
admission.

**State, and its source.** On 2026-11-16 the owner ordered that Grant v4
does not wait for the co-author's agreement, which is folded in by
amendment. That order covers the members of the grant, as LIP-0020 section
11 says since version 0.1.53. It is not stretched to this version: every
rule, code and order that version 0.1.55 adds is a proposal of version
0.1.55, in force by no word of this draft, and binds a reader of
`swarma-grant/4` when the version lands. A step that restates a landed text
keeps the state of that text. One point is stated apart, in one place: the
order of the count of LIP-0026 R8.3 is proposed in force by this version,
with the owner's explicit acceptance pending (LIP-0026 section 8). Every
other statement of status in this entry, in the README and in the LIPs
follows this paragraph.

Every LIP stays a Draft and nothing of this version is implemented. No
member of `swarma-grant/4` changes, and no octet of a tool or of a vector
file changes: `tools/grantv4` and `vectors/LIP-0020/grant-v4.json` are
those of version 0.1.53. Version 0.1.54, the entry below, changed none
of them either.

### The step table (LIP-0014 section 8.4)

LIP-0014 section 8.4 proposes the steps F1 to F24 of one predicate that
the signing service of the delegation key runs before it signs a child and
that a verifier runs at every admission, the step A1 that authenticates a
request, and the steps E0 to E3 of a request under an admitted child. For
each step the table says what it reads, which side makes it, the result,
the refusal code, what the refusal leaves behind, what the side has not
observed yet, and its status: carried from a landed text with the state of
that text, new with its reason, or amending a landed text. A list of
twenty-seven pairs gives, for every boundary between two neighbouring
steps and for the order inside a step with more than one code, either the
sentence that states the order or the mark NEW with a reason. The claim is
bounded: the order between the rows is total, with the checks of an
invocation unordered against two of the steps that follow them; inside a
row it is total where the row says so; and the section names what is
unordered, the three blocs of the seal and the issuance above all. Eight
open points are named. An order is called carried only where a cited
sentence states it: step 4 of LIP-0008 section 4 lists its checks without
an order, and the orders that the table takes inside that list are marked
NEW. Every step that a side makes has one place in the order of that side,
and a step that both sides make gives the same code on both, except where
its row states a difference. The table of the v3 steps V1 to V18 is
unchanged.

The points that had no answer in any text, and what this version proposes:

- **The same contract.** A child states the contract identifier of its
  parent, or refuses as `CHILD_CONTRACT_DIFFERS` (LIP-0020 W11.11, rule 1;
  F5). The rule is a new restriction and needs the owners' decision: the
  point that both owners agree on, that a v4 re-delegation appends no text,
  fixes no byte and does not entail it. It compares the two values of the
  member `contract` and is decided before any contract is read.
- **A contract that is missing or does not recompute.** Two new codes at a
  step that stands before the parent is read (F6): `CONTRACT_NOT_PRESENTED`
  for a contract that is not presented, which says nothing about the
  grants, and `CONTRACT_ID` for a document that does not recompute to the
  identifier. The place is new for the child and for the parent alike; v3
  runs the other way. `CONTRACT_ID` cannot be computed until a v4 contract
  profile fixes the preimage of the identifier (LIP-0017 section 2), and
  the codes of a contract that is invalid under its profile or does not
  mirror the terms of its grant are open. The v3 codes `CONTRACT_HASH` and
  `CONTRACT_MISMATCH` are not used on v4.
- **The parent keeps its codes.** A refusal of the parent at the admission
  of a child keeps the code of the rule that refused it, in one order of
  six parts (F7): the recent block, the issuer's name, the recipient's
  name, the closure journal, the window, the seal and the issuance.
  `PARENT_NOT_LIVE` reports four findings alone: a recipient name that its
  owner key does not hold (J4.5), a journaled closure, the window, and a
  spent seal. The Draft text of LIP-0008 section 5.2 (J6) is no part of
  the step while it awaits the co-author's agreement: neither its journal,
  nor its read of pending operations, nor `ISSUER_NAME_CLOSED`. A journal
  of closures that cannot be read admits nothing, and its code is open.
- **The parent as a document, and its groups.** At the admission of a
  child the parent is read through steps 1 to 8 of the pipeline and the
  rules of every grant, with the forms of `delegate.actions` and of
  `notaries` (F1). The rules of LIP-0020 W11.10 for a group and a range
  are judged for the group and the range of the child alone, after the
  bound of its ordinal (F13, `GRANT_DELEGATE`). The table asks nothing of
  another group and decides nothing of proposal Q1 of LIP-0026, the
  refusal of a whole parent: for a defect outside the child's group two
  outcomes conform until the owner decides. The earlier drafts of this
  version refused such a child; that is withdrawn.
- **A child wider than its parent.** The actions of a child are a subset of
  `delegate.actions` (`CHILD_ACTIONS_WIDER`, F16), its window lies inside
  the parent's in block heights (`CHILD_WINDOW_NOT_NESTED`, F18), and it
  states the chain of its parent (`SUBJECT_MISMATCH`, F8). The three codes
  are those of v3, taken where the v4 comparison is the same relation on
  the corresponding members. No step reads a clock for the validity of a
  grant, by Ivan Oparin's decision of 2026-11-16 that the window of a v4
  grant is stated in heights only.
- **The limits and their kinds.** A limit of a child whose kind has no type
  profile refuses at the admission of the child as `LIMIT_KIND_UNDEFINED`,
  after the keys of the limits and before their amounts (F17), and a floor
  is not compared as a ceiling. No kind is defined yet, so only a child
  without limits passes that step.
- **The child-seal key.** A parent without one (`CHILD_SEAL_KEY`, F10) and
  a child whose `seal.key` is another key (`CHILD_SEAL_KEY`, F12) refuse
  before any row is read, beside the key comparisons of J4.3 (F9, F11). The
  script of the seal on a node is judged with the seal (F21,
  `SEAL_SCRIPT`). Two readings are new: the split of CS2 between the two
  steps, and that the equality of F12 includes the parity octet. The
  signing service reads the seal that a child names before it signs
  (section 8.5, I8).
- **Two amendments of landed text.** LIP-0014 section 11.1 put every child
  check of J4.3 (b) at the place of step V7. The comparison of the
  delegation key with the attestation key of the row's notary stands in
  the certifier step (F23), because the row is known only from the
  ordinal, and the sentence now says so. And case S4-9 of section 11.2
  said "whose seal pays another key" for `CHILD_SEAL_KEY`; it now names
  the `seal.key` that the child states for that code and the script of the
  output for `SEAL_SCRIPT`, as rows F12 and F21 decide. Both are amended
  in place and marked there, as proposals of this version.
- **Two amendments of the order of one request** (LIP-0014 section 11.1),
  each in place and marked there, as proposals of this version. Step 6
  read "It repeats the checks of J4.4 on the parent and on the row"; it
  now repeats, on a fresh observation, every check of step 1 that reads a
  node or a journal or is made on what such a read gave, which are I3 and
  I5 to I9 of section 8.5, so that no child is signed whose window ended
  or whose recipient's evidence changed between step 1 and step 6. The
  cost is one more read of the node for every signature. Step 3 gains one
  branch: a request that passed the check of the coin of its row only
  because the confirmed issuance anchor of its own child has spent that
  coin, for a place with no record and no open mark, is refused with no
  code; nothing is reserved, and the operator is notified that a signature
  exists outside the ledger (event 39 of the table of states, case
  S4-30a). With these there are four amendments of landed text.
- **Three sentences in the text of the reservation ledger** (LIP-0014
  section 11.1), none of which changes a rule of it: a pointer from the
  order of one request to section 8.5 and to the two amended steps; that
  the entry which records a hold names the reservation key, the intent and
  the kind of the entry of the mark that it closes; and that a
  reconciliation which confirms a signature (event 31) writes a result
  `signed`, which records that it came by a reconciliation and which hold
  it closes and is the last entry of its place, so that the release rule
  reads as landed. A fourth sentence names event 39 among the requests
  that take neither code of the ledger.
- **The recipient and the request.** The proof of the name of a child's
  recipient has one place, with the checks of a class (F19), and it is a
  duty of the signing service as of a verifier. A request is authenticated
  after it (A1), as LIP-0008 section 4 orders names and authentication, and
  not before the checks of a row, as the consuming side proposed. The code
  of a request that is not authenticated is open.
- **The window of the child at the two sides.** The signing service signs a
  child whose window has not opened yet and refuses one whose window has
  ended, that is backdated or that is closed; a verifier refuses a child at
  every tip outside its window, and admits it when the window opens (F20).
- **The coin and the attestation.** The three checks of the coin of a row
  stand before the first step that reads an attestation (F22 before F23),
  which closes the point that LIP-0026 R6.1 left to the profile of the
  attestation. The order is new and rests on no landed text.
- **The order of the signing service's checks.** One signing request has
  one order, the order of one request that landed with the reservation
  ledger in version 0.1.54 (LIP-0014 section 11.1), and this version
  amends its steps 3 and 6 and no other step of it. Section 8.5 is the inner order of its step 1, the
  checks of J4.4, as the steps I0 to I9: the caller is identified first,
  then the documents are read, then the caller's list, the observation,
  the contract, the parent, the keys, the row, the child on the node, and
  the coin with the stop coin. Steps 2 to 9 of the order of one request
  follow, with the two amendments named above, and no check of section 8.5
  makes a signature: a replay is answered from the record, another intent
  for a taken place and a lost ledger refuse with the codes of the ledger,
  and the second check after the reservation makes I3 and I5 to I9 again
  on a fresh observation. The duties that section 8.5 adds to J4.4 are
  marked new: the observation, the contract, the recipient, the window and
  the seal of the child, the coin, and the stop coin. The service reads
  the coin as unspent, or as spent by the confirmed issuance anchor of the
  child in the request, so that a replay after publication reaches its
  record; that exception is marked new, reads nothing of the ledger in
  step 1 and does not hold in the second check.
  The reading of a payload before it is signed is a proposal of five steps
  (rule T7), for which LIP-0020 W9.1 has no class yet.
- **One place for the observation.** The observation of a side (F3) stands
  after the documents and before every later step of the predicate, at the
  signing service and at a verifier alike (LIP-0022 B6.1; pair Q3). The
  service establishes it in a step of its own (section 8.5, I3) before it
  holds the contract (I4), so that a child that binds another contract, at
  a void observation, gives `OBSERVATION_VOID` on both sides (case S8-3). At an
  admission the observation also stands before the authentication of the
  request and before the names (pair Q21, case S8-25). That is a reading
  of LIP-0022 B6.1 and is marked new in both recipient modes, because
  LIP-0008 section 4 numbers the healthy observation as its step 3, after
  the names and the authentication; neither text is amended. The documents
  stand before the observation, which is marked new as well. The service's
  checks of its caller read no node and stay before its observation.
- **A child outside its own window or closed.** A new code,
  `CHILD_NOT_LIVE` (F20, F21), for a child alone.

Section 8.6 holds one case for each pair of steps whose order decides a
code, and one case that keeps apart a limit that a child states under a
key its row lacks (`CHILD_BUDGET_OVER`) and a key under which nobody states
a limit (a ceiling of 0 at the reservation). Section 8.7 plans the vectors
of the order; none is generated, and none is planned on an open point or
on a result that this version cannot compute.

### Actions and limit kinds (LIP-0020 section 11.14)

LIP-0020 section 11.14 states the registry of action identifiers and the
registry of limit kinds. Neither has a defined entry; `policy` is reserved
and undefined. An executor refuses a request for an action that no profile
defines (`ACTION_UNDEFINED`) and one that consumes a limit kind without a
profile (`LIMIT_KIND_UNDEFINED`). Two facts for whoever plans on Grant v4,
both until a profile exists: a v4 grant has no effect at an executor,
because no action is defined, and a child that states a limit is neither
signed nor admitted, because no limit kind is defined.

### The order of the count (LIP-0026 R8.3)

The order in which the rows of a parent are counted, groups and ranges in
their signed order and coins by ascending output index, from 1, is an
addition of the draft. This version proposes it in force, with the owner's
explicit acceptance pending; LIP-0026 section 8 is the one place that
states that state, and no owner decision is cited for it. The same order
of the octets is text in force since version 0.1.53 (LIP-0020 W11.6).
Proposal Q2 of LIP-0026 keeps its other parts.

### New codes

Six codes are new, counted from the tables of LIP-0014 section 8.4:
`CHILD_CONTRACT_DIFFERS` (F5), `CONTRACT_NOT_PRESENTED` and `CONTRACT_ID`
(F6), `CHILD_NOT_LIVE` (F20, F21), `ACTION_UNDEFINED` (E1) and
`LIMIT_KIND_UNDEFINED` (F17, E2). Every other code of the tables comes
from a text of an earlier version. Taken for v4 from v3:
`SUBJECT_MISMATCH`, `CHILD_ACTIONS_WIDER`, `CHILD_WINDOW_NOT_NESTED`.
LIP-0020 section 11.11 registers all nine in one table. Two names replace
names of the first draft of this version, so that neither is read as
`CONTRACT_MISMATCH` of LIP-0013: `CONTRACT_ID` was `CONTRACT_ID_MISMATCH`,
and `CHILD_CONTRACT_DIFFERS` was `CHILD_CONTRACT_MISMATCH`.

No earlier code changes its meaning. The first code of some children
changes against the text before this version, in which a v4 child had only
the coded checks of its keys, its row and its coin:

- a child with an action outside `delegate.actions` and a limit above its
  row reported `CHILD_BUDGET_OVER` and now reports `CHILD_ACTIONS_WIDER`;
- a child with another `genesis` and a reused delegation key, a wrong seal
  key or a defect of its row reported the code of that defect and now
  reports `SUBJECT_MISMATCH`;
- a child with another `contract` than its parent, or without a presented
  contract, reported the code of whatever else was wrong, or none, and now
  reports `CHILD_CONTRACT_DIFFERS` or `CONTRACT_NOT_PRESENTED`, also under
  a parent that is closed;
- a child with a limit of a kind without a profile reported no code at its
  admission and now reports `LIMIT_KIND_UNDEFINED`;
- a child with a defect of its row, under a parent whose notary of that
  row publishes the delegation key as its attestation key, reported
  `DELEGATE_KEY_REUSE` at the place of step V7 and now reports the code of
  the row, because that one comparison stands in the certifier step (the
  amended sentence of section 11.1);
- a child that states the child-seal key of its parent over a seal output
  that pays another key could be read as `CHILD_SEAL_KEY` under case S4-9
  and now reports `SEAL_SCRIPT`, at the step of the seal (the amended
  case);
- a parent with a defect in the group or the range of the child (rules 4
  and 5 of LIP-0020 W11.10) keeps `GRANT_DELEGATE`, and at the admission
  of a child that code now stands after the keys and the bound of the
  ordinal, so that a child with a wrong signer or a reused key under such
  a parent reports `CHILD_SIGNER` or `DELEGATE_KEY_REUSE` first.

No verdict changes for a child of a parent with a defect outside its
group: that stays undecided with proposal Q1 of LIP-0026.

### Left open

Eight points, O1 to O8 of LIP-0014 section 8.4: the order of the three
blocs of the seal and the issuance of a grant against each other; the code
of a request that is not authenticated; the codes, the inner order and the
place of the checks of an invocation; after the contract identifier, the
code of a contract that is no valid contract of its v4 profile and the code
of a contract that does not mirror the terms of its grant, with the
preimage of the identifier; the code of a journal of closures of a grant
that cannot be read; the place of a validated spend of a seal against the
checks of the anchor and of the issuance; what a side does with a finding
of rules 2 and 6 to 8 of LIP-0020 W11.10, and with a finding of rules 4
and 5 outside the group and the range of the child, which waits for
proposal Q1 of LIP-0026; and the class under which a
signing service judges the age of the tip. Also open: the entries of the
two registries, and the owners' line on every choice that the text marks
NEW. Outside this version, and decided by none of its text: whether the
key that signs children may run under the OS user of the delegating agent,
which product holds the delegation key on a host, who funds the coin of a
row and holds the path of its spend, where a key slot comes from, and which
party of the delegating side makes the issuer's checks of the consent of a
child's recipient. The refusals of the signing service's record of places
are not open: they are the reservation ledger of version 0.1.54.

## 0.1.54 — 2026-11-16

Records three owner decisions: the reservation ledger of the signing
service of a delegation key, the terms of the window of a v4 grant, and the
holder of an agent's request key under J7. Every LIP stays a Draft. No octet
of a grant changes, LIP-0020 sections 11 and 12, `tools/grantv4` and
`vectors/LIP-0020/` are untouched, no vector byte or vector outcome changes,
and nothing of this version is implemented.

### The reservation ledger of the signing service

Ivan Oparin decided on 2026-11-16, as the lead relayed it, to take the
issuer's reservation ledger into the v4 specification: «да берем - годно».
It is written as a duty of the signing service of the delegation key, in
the manner of J4.4, and marked in every row as a duty that a verifier
cannot observe and that proves nothing to a consumer. The co-author's
agreement has not been given, and the co-author's answer is folded in by
amendment.

LIP-0014 section 11.1 gains the rules J4.4 (a) to J4.4 (g), directly after
J4.4. J4.5 to J4.7 keep their numbers.

- **The reservation key (J4.4 (a)).** The parent's identifier and the
  place, which is the ordinal of a row under the count of LIP-0026 R8.3 and
  R8.8 (J12), as LIP-0020 W11.2 and W11.6 carry it. For one place of one
  parent the service makes one signature, ever. The same ordinal under
  another parent and another ordinal under the same parent are other keys.
- **The intent (J4.4 (b)).** The SHA-256 of the exact signing preimage of
  the child, which is the typed digest of LIP-0020 W4.1 that the signature
  covers. It is not the identifier of the child. It binds the payload
  alone, so one payload from two listed callers is one intent.
- **The record and its states (J4.4 (c)).** A place has no record or is
  `reserved`, `signed` or `held`, and the ledger as a whole is usable or
  lost. A record is durable before the key is used, by one atomic test and
  set at the one writer, and the result is durable before the signature is
  released. Only the request that created a record takes it to `signed`,
  under a claim that does not outlive a stop of the service. No entry is
  deleted, and a place for which the key was used never takes another
  signature. A signing call of unknown outcome and a signature that fails
  the service's own verification hold the place: such octets are never
  released, and the service never signs again for the place. Between the
  reservation and the use of the key the service repeats the checks of
  J4.4 on the parent and the row. A place is `signed` only when every
  write of the result is durable: its mark, its entry and the kept head
  over that entry.
- **Replay (J4.4 (d)).** The same parent, place and intent are answered
  with the stored octets of the signature and never with a new signature,
  whose octets would differ under the auxiliary randomness of BIP-340. A
  replay is answered only after the checks of J4.4: under a parent that is
  closed or whose window has ended, and for a caller that is no longer on
  the list, it discloses nothing.
- **Conflict (J4.4 (e)).** Another intent for the same parent and place
  refuses with a code that is not retryable, in every state of the record
  or of an open mark, and no signature exists.
- **Held (J4.4 (f)).** An interrupted write, a write whose outcome is
  unknown, and a stop of the service between the reservation and the
  durable result, the moment between the signature and its record
  included, hold the place. Every write is one entry in one order: a mark
  that is durable outside the ledger, then the entry, then the kept head.
  Each partial outcome has one state: a mark that did not land leaves
  nothing; a write that ends after its mark leaves the place held under
  the open mark, and an entry that stands whole beyond the kept head is
  evidence only and is never completed by the service; a mark or a kept
  head that cannot be read loses the ledger. The service appends nothing
  beyond an open mark: it first records the hold of that place as an
  entry of the chain, moves the kept head, and only then writes for
  another place. The service does not retry, releases no signature for
  the place and answers with no new key and no other place. A held place
  has two exits, each a reconciliation by the operator that never uses the
  delegation key and takes no octets from outside the service: it confirms
  a signature that the service itself wrote into the ledger, or it proves
  that the key was never used, which returns the place to "no record".
  That proof covers the whole life of the key, from its making, and
  exists only in a chain that is continuous from the making of the key: a
  key that was not made under the ledger, or that the service held when a
  new ledger was started, has every place held, and no reconciliation
  frees one. Where neither is proved the place stays held for ever. The
  creating request and a reconciliation are fenced against each other.
  The ledger has one fenced writer and is one chain whose head the service
  keeps outside it; a ledger that is absent, rolled back, forked or not
  continuing the kept head is lost, and a lost ledger holds every place of
  every parent whose delegation key the service holds, a parent first seen
  after the loss included, until the complete ledger is restored or the
  operator makes a genesis, whose entry names the loss that it ends. A new
  ledger starts with every place of every such parent held, with no
  exception; the way forward is a new parent with a new key. A restore of
  the whole host that puts back the ledger and the kept head together is a
  lost ledger that the service cannot find by itself: to keep the kept
  head out of that reach, and to keep a key in one custody, are duties of
  the operator.
- **Audit and capacity (J4.4 (g)).** The audit is two. The proof-bearing
  audit stands in the chain of the ledger, under the kept head, and has
  the ledger's contract: an entry carries its record and its audit entry
  as one, and the chain holds the entry of a key, a reservation, a use of
  the key, a result, a reconciliation and a genesis, and nothing else.
  Only these are read as proof. The operational audit stands apart: the
  refusals by the checks of J4.4, every finding that the ledger is lost,
  and the other answers of the service. It is bounded, proves nothing,
  and a write to it that fails changes no state of a place. The entry of
  a use of the key is durable before the signer is called, and a
  signature is released only after the entry of its result is durable
  under the kept head. The room for the three writes of a request is
  secured before any mark; a refusal for want of room holds no place, and
  a write that fails after its mark does.

The section states the ledger as one table of states: for each of the four
states of a place and for a lost ledger, and for each of 38 events, the
next state, the use of the key, the answer and the code, with the pairs
that cannot occur marked as such. The three writes of a request are taken
apart by their last durable component, and the recording of a hold, the
restore, the genesis and the entry of a key are events of the table. The
rules, the cases and the vector plan are read from it, and the order of
the steps of one request is fixed beside it: the caller and the checks of
J4.4 first, then the continuity of the ledger, then the place.

Two codes are new, `PLACE_CONFLICT` (J4.4 (e), not retryable) and
`PLACE_HELD` (J4.4 (f), not retryable as a request to sign; the same request
asked again reads the record; it is also the answer for every intent under
a lost ledger and for a place of a key whose whole life the ledger does not
show). They are answers of the signing service to
its caller and stand in LIP-0014 section 11.1 alone: no verifier reports
them and no pipeline of LIP-0020 section 9 holds them. The existing closed
sets state no place that is taken or held, which the section says.

Cases S4-11 to S4-30 are new. S4-11 to S4-17 are the first signature, the
exact replay with the same stored octets, another payload for the same
place, a stop after the reservation and before the signature, a stop after
the signature and before the record of the result, a second parent with
the same place number, and a second place of the same parent. S4-15a
stands beside S4-15: a signature that fails the service's own
verification, which holds the place and is neither released nor repeated.
S4-18 to S4-26 are the two exits of a held place, the fence between the
creating request and a reconciliation, a reservation write that fails, two
requests together, two writers, a lost ledger, the genesis, and room and
the two audits. S4-27 to S4-30 are an entry beyond the kept head while
another place is asked for, the write of the result by its last durable
component, a key that signed before it came under the ledger, and the
second check. A vector plan follows them and holds no vector: the intent,
the replay, the conflict, the independence of keys, the answer on a held
place and under a lost ledger, the partial outcomes of a write, the order
of the checks, the outcomes of a reconciliation and the start of a new
ledger can become deterministic
vectors of a transition, in a file of their own,
`vectors/LIP-0014/ledger-vectors.json`; the order of record and signature,
the stops, the failed write, the fence, concurrent requests, two writers,
the continuity check, the room and the audit are behavioural and belong to
the qualification of a service on its real store.

The section "Decisions recorded" of LIP-0014 gains the decision, and its
open questions gain what the text leaves open, each with its clause: the
window after the second check, the payload in the record, a record
`signed` whose octets do not verify when read, the authentication of the
operator's act, the form of the marks and of the kept head and where the
kept head stands against a restore of the host, a proof from outside the
chain for a key whose life the ledger does not show, single custody, a
mark of a use that stayed open, the contents and the bound of the
operational audit, separate codes for a request still served and for a
lost ledger, the interface and the octets of the codes, and the entries
of the ledger on the form of LIP-0025. Other questions are not among
them, because the table of states answers them: the exit of a held place
for which the key was never used, the place of a request that ends with
the key unused, a replay under a closed parent, the store of the audit
that is proof, an entry beyond the kept head beside the service of other
places, the reach of the proof of an unused key, and the partial outcomes
of a write. The key registry names the duty in the entry of the
delegation key.

### The window of a v4 grant keeps heights

Ivan Oparin decided on 2026-11-16, as the lead relayed it, the terms of the
window: a v4 grant keeps block heights and has no clock member; a calendar
interval is converted to a height at issuance and written into the parent;
and a clock check on the issuer's side is the issuer's own rule, no member
of a grant and no step of the shared predicate: «ок так им и скажи».
LIP-0008 section 7.1 gains one sentence that says so. The members were
already heights alone: LIP-0020 W11.2 gives a grant `not_before_height` and
`not_after_height` and no other time member, and LIP-0008 section 7.1 says
that no clock enters the comparison and that a date is never an admission
input. What no text said was the conversion at issuance and the standing of
an issuer's own clock check. LIP-0020 section 11 is not changed.

### The key holder of J7 is Keymaker

Ivan Oparin decided on 2026-11-14, with J7, that the key holder under J7,
the service that holds the agent's request key and runs the gate for each
run, is Keymaker and not the messaging daemon: «Держатель ключа по J7 — это
Keymaker, а не a2a. a2a только просит подписать через сокет». LIP-0013
section 3.6 quotes the decision in English. Keymaker holds the agent's
request key under J7 and signs the typed J7 objects; the messaging daemon
only asks for signatures over the socket, and the agent's OS user never
reads the key. The texts do not say that Keymaker holds the agent's Nostr
key for every use: whether NIP-17 messages use the same key, and through
which holder, is not decided. The holder is named per owner. The texts
record the decision for the deployment of the owner who took it, and
another owner names its own holder under the same J7 rules. Naming a
holder selects no deployment of another owner's holder and grants no
waiver from J4: the delegation signer stays outside the agent's OS user
and outside the request-key service. That the holder runs under an OS user
of its own is written as a consequence of LIP-0013 section 3.6 and not as
part of the decision.

Three texts named the gateway of the agent's host
instead and are corrected, each with the decision cited: LIP-0013 section
3.6, in the sentence that names the key holder of an agent; the key
registry, in the holder line of the entry "Agent's Nostr key"; and the key
map, in the fifth row of its table, in the paragraph after K4, in the row
"Agent's Nostr key" of the proposed key layout and in the opening of the
proposed registration flow. LIP-0014 section 11.1 follows in the one
sentence that named the gateway as the holder of that key. The gateway
stays named as the holder in the implemented rental profile, where no gate
of J7 runs. LIP-0006 section 1 already named Keymaker as the key holder of
LIP-0013 section 3.6 and is unchanged. LIP-0003 section 1 now says that
the gateway holds the secret of an agent's `nostr` key in the implemented
rental profile. The authority-path diagram of the
key map and the numbered steps of its registration flow keep the word
"gateway": they describe the rental profile and an undecided proposal.

The README and the open-question index follow.

## 0.1.53 — 2026-11-16

This version holds two changes: the hash-pinned holders list of a landlord,
and the members of the v4 grant.

### The holders list

Replaces the five-entry member `holders` of the landlord binding by a
hash-pinned holders list, on an owner decision of 2026-11-16. The text is
in force without the co-author's agreement, which has not been given; the
co-author's answer is folded in by amendment. Every LIP stays a Draft,
nothing of this version is implemented, and no historical protocol byte,
tool, vector byte or vector outcome changes.

LIP-0010 section 10 is rewritten. The landlord's name value pins the hash
and the version of a holders list in a top-level member `swarma-holders`,
outside `swarma`, on the method of the device list of LIP-0029 sections 3.1
to 3.3; the list lives off the value. It is one JSON object in the encoding
of LIP-0013 section 2.1 with the members `schema`, `network`, `owner`, `seq`
and `holders`, and its hash is the SHA-256 of its exact octets. An entry
names one agent or station name, the owner pin of that name and the outpoint
of a seal. The cap of five, which followed from the 520 bytes of a value,
does not apply; a list holds at most 1024 entries and 262144 bytes.

A change of the list no longer ends the v4 grants that the landlord issued.
Rule 7 of version 0.1.51 is replaced by H13: the holders are no part of
`swarma`, an update that changes only `swarma-holders` is no break and
records no closure, and a grant depends in the landlord's name on its
registration, its owner key and the octets of `swarma`, which are the
landlord binding with its grant key alone. LIP-0008 section 3 is unchanged
and says so for this member.

A verifier of a landlord class reads, at each admission and on its own
node, the pin from the landlord's confirmed value and the seal of the entry
that names the recipient; it takes the list from its cache or from the
presenter and counts only the list that the current confirmed value pins. A
list has no expiry, and the freshness of the check is that of the
observation under LIP-0022. A verifier that cannot get the pinned list
refuses the child as `LIST_UNKNOWN`, records no closure and falls back to no
older list. The list is distributed as LIP-0029 section 3.5 has it.

One name is revoked by the spend of the seal of its entry, on the model of
the device seal of LIP-0029 section 8: a fresh key, a revocation signed in
advance, the key destroyed, and the spend kept by the devices of the
landlord's owner. A verifier that validates the spend on its own node
journals a closure that no rollback lifts; other names stay, those of the
same key included; no grant ends, one agent's own grant is still ended by
that grant's seal, and the name stays with its key holder. A listed name
passes only while the pinned key holds it and wrote its value. A stolen
holder key is answered by the spend of every entry with that pin; there is
no seal of a key. Names may be listed ahead and kept in reserve at the cost
of their seals, and a reserve name is registered before it is listed. A
removed entry and a sealed-off entry are set side by side in section 10.8.

An independent second read of the section found the shape sound and sixteen
defects in the seal layer, the journal rules and the transition. The
section closes them before the version is released, with the rules H38 to
H53 and changed rows of the older rules:

- **The seal read (H45 to H48).** A verifier reads, on its own node and
  against the named tip of the admission, the funding transaction of the
  seal, its spend state with the mempool included, and its spenders. A
  seal counts only while its funding output is confirmed in the active
  chain, at a height that is not above the anchor block of the pin, with a
  witness key hash script. The anchor block holds the first operation of
  the run of outputs that carry the current pin; a later operation that
  carries the same pin does not move it. No verifier can check that the seal's key is fresh or
  destroyed, and the text says what follows. A validated spend is defined:
  the octets of the spending transaction, accepted by the verifier's own
  node and checked by the verifier against the script of the seal.
- **Three codes where there was one.** `HOLDER_REVOKED` for a journaled
  closure; the new `HOLDER_SEAL_NOT_LIVE` for a seal that is not on the
  chain as stated or is not shown unspent without a validated spend, with
  no closure; `CLASS_HISTORY_UNAVAILABLE` for a read that failed. A spend
  that the node shows definitely, with a node that has no means to name
  the spender, is `HOLDER_SEAL_NOT_LIVE` and no failed read (H45). The
  order inside step 5 and step 8 is fixed (H53, H48).
- **The holder journal (H39 to H43).** A landlord in it is its name with
  its registration. It holds the head, a form mark, the binding of each
  seal, removal marks and closures. Each kind has its key: a binding is
  keyed by the landlord and the seal outpoint, a removal mark by the entry
  (landlord, name, key and seal), and a closure by the seal outpoint alone,
  across landlords. It advances at one point, the take of a verified list. An equal
  `seq` with another hash refuses. A journal that cannot be written admits
  nobody; a lost one makes a newcomer, which reports nothing that it does
  not hold; replicas of one executor share it.
- **No downgrade (H42).** A verifier that took a pinned list for a landlord
  never reads the inline form of that landlord again:
  `HOLDER_FORM_DOWNGRADE`.
- **One seal, one entry, within one landlord (H38, H49).** Within one
  landlord a seal outpoint serves one name and one key, across its lists:
  `HOLDER_SEAL_REUSED`. The binding of one landlord says nothing about
  another: a landlord that copies the seal of another landlord's entry
  gains an entry that the other landlord's keepers revoke and takes nothing
  from that entry, so the copy harms only the copier. A seal is no other
  outpoint of the admission: `HOLDER_SEAL_ALIAS`.
- **A removed entry does not return after a reorganisation** at a verifier
  that took the list which dropped it (H41), as section 11 SH5 has it; the
  first text of this version had it return. This holds in whatever order
  the lists were taken: a verifier whose first list for the landlord was
  the dropping one writes the removal mark when the reorganisation makes it
  take the older list, or a list of the same `seq` (H40, point 5). Removal
  alone is no answer to a compromise.
- **One observation and the read before the effect (H44).** The pin read
  and the seal read bind to one named tip, and the seal is read again
  immediately before a reservation or an effect. LIP-0022 B1.2 and B1.5
  name the holder reads.
- **The non-witness (H50), with a pointer in LIP-0029 section 8.1.** A
  verifier that reads only seal states through a gateway refuses on every
  state but unspent, admits on unspent only when the gateway shows the
  seal's funding as H46 asks, and records no enforcement closure; it may
  keep an
  observe-grade record that is never used for enforcement. An enforcement
  closure needs the spending transaction validated by the reader, every
  spender and one named tip, and the watcher journal of a deployment is
  named as the source of that evidence.
- **Custody and construction (H27, H51, H52).** The prepared spends are
  kept by the devices with `ceiling` 2 of the device list that the landlord
  name's own value pins and by a cold copy; a landlord with neither claims
  no fast revocation. One keeper holds the revocation of the whole list.
  The prepared spend has the seal as its one input and hash type `01`. Its
  amount, its fee and a fee-raising output stay open, and until they are
  closed nobody claims the fast path. Keepers broadcast again, and the
  landlord completes by a list.
- **Encoding corners and labels.** The seal object and duplicate members
  have rule sentences; an escaped spelling of `swarma-holders` gives no
  list; sections 1 and 2 name the member. H16, H26, H27, H36, H51, H52 and
  M4 are labelled as rules that no verifier observes. The two secondary
  paths of the list are stated as not yet implementable.
- **Cases and vectors.** Cases S10-12 to S10-28 are new. Section 10.11
  states the facts that an admission vector holds and lists the vectors by
  rule, compound vectors for the order of codes included. It fixes no
  octet.

A review of record of the section in that state asked for a revision on
eight points, and the section closes them before the version is released.
The rules changed are H38, H39, H40, H41, H45, H46 and H48, with step 6 of
section 10.6; none is a new rule number.

- **The dropping list as a verifier's first list (H40 point 5, H41, case
  S10-26).** The removal mark no longer depends on the entry having been
  bound earlier.
- **No lever across landlords (H38, H39, case S10-27).** The binding and
  the removal mark are kept for each landlord, and the closure stays keyed
  by the bare outpoint. Two landlords that name one outpoint are both
  admitted while it is unspent, and both refuse as `HOLDER_REVOKED` after a
  validated spend. The security consequence that described the lever is
  rewritten.
- **The removal mark is the mark of an entry** (landlord, name, key and
  seal), and step 6 tests that identity, so that a seal moved to another
  name or pin within a landlord refuses as `HOLDER_SEAL_REUSED` at step 8,
  as cases S10-4 and S10-17 state.
- **One code for a spender that the node has no means to name:**
  `HOLDER_SEAL_NOT_LIVE` (H45, H48 points 6 and 8, case S10-13).
- **One anchor for the height bound of a seal** (H46, case S10-12).
- **Provenance.** The owner pin in an entry with the refusal of another
  current owner (H34), and the answer to a stolen key (H35), are owner
  decisions of 2026-11-16 and are no longer marked NEW or listed as open.
- **The vector table** gains the vectors of H7 (case S10-28) and of H48
  point 6 alone, with those of the points above.
- **The key registry's summary row** of the holder seal key agrees with
  its entry.

A delta review of record of that text asked for one sentence, and an
independent delta read of an earlier state of the section named eight
further points, of which the text had closed part: the two codes for a
spender that the node cannot name, and a vector of H48 point 6 alone. The
section closes the rest before the version is released. No rule number is
new; the rules changed are H28, H40, H43, H44, H48 and H50, with steps 5
and 8 of section 10.6.

- **The same pin on a new operation after a reorganisation (H40, step 5,
  case S10-18).** In the branch of H23, point 4, the take is made even
  where the pin's `seq` and `sha256` equal those of the removed head; it
  replaces the operation and the block of the head and writes no mark.
  Without it one reader kept a removed operation as its head and later
  took a list of a lower `seq`.
- **A closure that a watcher supplies (H28, by ruling).** Point 2 of H48
  in step 8, and the read before the effect, consult an enforcement
  closure that the watcher of the verifier's deployment supplies. It
  counts only with what H47 requires: the validated spender, the seal's
  confirmed funding and one named tip. The verifier then journals it; one
  that lacks any of the three counts for nothing. The watcher journal, the
  format of such a closure and its transport stay outside the section and
  open.
- **The reader behind a gateway (H50, by ruling, case S10-23).** It makes
  every step of section 10.6 and only cannot write an enforcement closure.
  It admits only when H46 holds through what the gateway shows, the
  confirmed funding with its script and its height, and refuses as
  `CLASS_HISTORY_UNAVAILABLE` where the gateway cannot show it. The earlier
  point that left those checks optional is withdrawn, and the
  observe-grade record no longer needs an earlier journaled sighting.
- **The mark of a lost journal (H43, by ruling, case S10-21).** A journal
  is created once, with an identity. A verifier that finds none where its
  configuration says that one existed refuses every class admission of
  every landlord as `JOURNAL_LOST`, and takes no list, until its operator
  states a new start. How the state after a failed write is carried across
  a restart while the journal is still found stays open, as in LIP-0027.
- **No closure on two refusals (H48, section 10.8, case S10-22).** An
  admission that ends as `HOLDER_SEAL_ALIAS` or `HOLDER_SEAL_REUSED` reads
  no seal and writes no closure. The text states this as an accepted
  divergence and does not move the seal read before those refusals.
- **The cost of binding at the take (H40).** A take binds every seal of a
  list, and nothing bounds or prunes the journal; the security
  consequences say so, and a bound is listed as open. The rule does not
  change.
- **The facts of an admission vector (section 10.11).** The fact table
  gains the outputs and registrations that the alias check compares, the
  sighting tip and the funding state of a closure that a watcher supplies,
  the pending operation and the closure at the read before the effect,
  what a gateway shows of the funding, and a journal that is not found.
  The table gains a row for the same pin on a new operation, and the rows
  of H28, H44, H50 and step 0 gain their vectors.
- **The device seal keeps its own reading (LIP-0029 section 8.1, O9.2).**
  LIP-0029 states that the conditions of the holder seal do not bind the
  device seal, how the two readings differ and why, and leaves the
  alignment open. O9.2 says that "higher" is the condition of a take.
- **The read before the effect in the observation profile.** LIP-0022 B1.6
  names the holder reads of a class admission, and case S10-15 separates a
  void admission without a validated spend from one whose closure stands.

The member of version 0.1.51 stays readable as the inline form (section
10.9), with its rules 1 to 8 and its vectors unchanged. A value with both
forms has no holder. A landlord moves by one update that removes the inline
member and writes the pin; that update is the last to which the old rule 7
applies, and a landlord that never wrote the inline member moves at no cost
to its grants.

Decided by the owners on 2026-11-16 and stated as such: the entry of agent
name, owner pin and seal outpoint; the refusal of a current owner other
than the pin; the answer to a stolen key by the spend of the seal of every
entry with that pin.

Marked NEW in the text, for the owners: the member name and the schema
string; that an entry has no member beside the three; the bounds; the reading of a duplicate pin under section 11 SH6 instead of
LIP-0029 O3.5; the presenter as the sender of the list, the well-known path
and the `d` tag; the nine codes `HOLDER_PIN_INVALID`, `HOLDER_LIST_INVALID`,
`HOLDER_LIST_MISMATCH`, `HOLDER_LIST_ROLLBACK`, `HOLDER_REVOKED`,
`HOLDER_SEAL_NOT_LIVE`, `HOLDER_SEAL_REUSED`, `HOLDER_SEAL_ALIAS` and
`HOLDER_FORM_DOWNGRADE`; the whole of the seal of an entry, with its read,
its single script form, the height bound of its funding with its anchor,
the one code for a spender that the node cannot name and the definition
of a validated spend; the holder journal, its one point of advance, the
removal marks of a take of an equal `seq` through the reorganisation
branch and its failure rules; the form mark; one seal for one entry within
a landlord; the alias check; the read before the effect; the keepers
with `ceiling` 2 and the cold floor; the one input and the hash type of the
prepared spend and the duties to broadcast again and to complete; the
reserve and its registration before the list; and the rules of the
transition. Taken by ruling after the second read, and stated as such: the
closure is of the entry; no seal of a key; the writer of check (d) is the
entry's own key; both forms give no holder; a removed entry does not return
after a reorganisation; the non-witness. Taken by ruling after the review
of record: the removal mark at a verifier whose first list was the
dropping one; the keys of the journal's records, with the binding and the
removal mark for each landlord and the closure by the bare outpoint. Taken
by ruling after the independent delta read: the step that consults a
closure which a watcher supplies and what it must carry; the gateway
reader that makes every step and admits only on the funding that the
gateway shows; the mark of a lost journal. This text's choices of the same
round, for the owners: no closure on an alias or a reused seal as an
accepted divergence, and the device seal's own reading in LIP-0029.

LIP-0010 section 11 registers `swarma-holders` as a head member (SH2) and
counts its bytes. LIP-0008 section 3, LIP-0014 section 8.3, LIP-0026
sections 9 to 11 with its security consequences and open questions,
LIP-0029 sections 3.3 and 8.1 with O9.2, LIP-0022 B1.2, B1.5 and B1.6, the
key registry,
the README and the open-question index follow. The key registry gains the
entry "Holder seal key", whose danger line states the reach of one keeper
and the open fee. LIP-0026 R9.6 and R9.7 read the entry of the recipient
name; the eight codes of a class keep their meaning, and the class vectors,
whose landlord values are in the inline form, keep their bytes and
outcomes. That last claim rests on a reading of the rules; the existing
checkers were not run for it.

No vector of the list is published. LIP-0010 section 10.11 states what a
vector set holds, with the facts of an admission and the vectors by rule;
the length and the hash of the example in section 10.2 were computed by one
implementation only, and the octets of that example did not change.

### The members of the v4 grant

Gives the v4 grant its members. Until this version the registry of LIP-0020
held `swarma-grant/4` with an identifier, a digest and no member, so no
reader could accept a v4 grant and no vector could hold one. Every LIP stays
a Draft. No earlier vector byte or vector outcome changes, and nothing of
this version is implemented in the reference laboratory.

LIP-0020 gains section 11, the members of `swarma-grant/4`, and section 12,
its vectors. Section 11 is text in force: on 2026-11-16 Ivan Oparin ordered,
as the lead relayed it, that Grant v4 does not wait, so the members are
written as text in force and not as a proposal. The co-author's agreement
has not been given, and the co-author's answer is folded in by amendment.
The section carries in octets what LIP-0008, LIP-0014, LIP-0024, LIP-0026
and LIP-0027 state for a v4 grant and changes no rule of them; each rule
keeps the state that its own text gives it. Every decision that section 11
carries (J2, J4, CS1 to CS3, J9 to J12, LIP-0008 sections 7.1 and 11.4)
binds a reader of `swarma-grant/4` from this version under that order; a
draft's own additions bind no reader until they are accepted (the script
form of LIP-0026 R3.1 and R8.2, LIP-0027 H1.2 and H1.3, LIP-0023 C2.3).
LIP-0008 section 12.6 and LIP-0014 section 11.1, which call the signature
of a child by the parent's recipient the rule in force, each gain one
sentence: for the octets of `swarma-grant/4` the rule in force is LIP-0020
W11.8, the delegation key.

What section 11 fixes:

- Forms: a hash, a signing key (x-only), an output key (the compressed form
  of an owner pin, for owner keys, seal keys and the child-seal key), text
  of printable ASCII, an outpoint, a script, a height in the number form
  and an amount in the string form up to 2^64 - 1.
- Two member lists. A root grant has `issuer` (name, registration, owner
  key and grant key) and may have `delegate`. A child has `parent` and
  `ordinal` and neither of those. Both have `genesis`, `contract`,
  `recipient`, `executor`, `actions`, `limits`, `not_before_height`,
  `not_after_height`, `recent_block` and `seal`.
- The recipient by key or by name, as exactly one of two member lists.
- The seal with its construction profile, its kind, its outpoint and its
  key in the grant; no endorsement is read.
- The right of re-delegation: a delegation key, a child-seal key, the
  delegable actions, one pool for each limit key that a template limits, at
  most four pinned notaries, and 1 to 16 groups. A group is a template and
  1 to 16 ranges; a range is a transaction id, a first index, a count of 1
  to 4096 and a script. The signed form of a grant has at most 65536
  octets.
- The recipient constraint of a template in three forms: a request key, a
  name with its owner key, or a class of pinned landlords. The grant holds
  no holder of a landlord.
- No certifier: a template has `certifier`, the name of a pinned notary, or
  `no_certifier` with the value `true`, and never neither. A `null`, an
  empty string and a missing member all refuse. The encoding widens nothing
  of J9: a template without a certifier whose recipient is not limited to
  the issuer's own landlord refuses as `GRANT_DELEGATE`.
- Stop coins of a group: a range of a group with a certifier states a run
  of stop coins, one for each of its coins, and a range of a group without
  one states none. The member `stop` may be absent or present at the member
  step; rule 5 of W11.10 judges its presence in step 9, as
  `GRANT_DELEGATE`.
- The pipeline: a root grant verifies under `issuer.grant_key`, a child
  under the delegation key of the parent that the reader already read
  (`WIRE_ID`, `CHAIN_DEPTH`, `NOT_DELEGABLE`, then `CHILD_SIGNER`). Two new
  codes report the rules that a reader judges on the octets of one grant,
  in a fixed order: `GRANT_SHAPE` for the window, the action set and the
  own limits, and `GRANT_DELEGATE`, the code that LIP-0026 R1.5 left to the
  members of the grant, for the rules of a parent's rows, pools and coins.
  `WIRE_INTEGER` also reports an integer below the smallest value of its
  member, and `WIRE_KEY` an output key that is no point.
- Which rules of a parent every reader judges. W11.10 names, for each of
  its rules, the decision or the form of section 11 that gives it: the
  order of the delegable actions and of the notaries, one pool for a limit
  key and the exact sum against it (J12), distinct coins that are not the
  seal (J12), a class without a repeated name (J10), and a row without a
  certifier only for the issuer's own landlord (J9). Every reader also
  judges the points on stop coins that a decision gives: no `stop` where
  the template has no certifier (J9.4), `stop` where it names one (J2.7 as
  section 11 carries it), the last index of a run of stop coins, and a
  stop coin of its own for each row. Two points are carried as proposals
  of their LIPs, and this version does not determine that a reader judges
  them: the witness key hash form of a range script and of a stop script,
  and the placement of a stop coin against the coins of rows, the seal and
  the output after it. Their code is fixed: a reader that judges one
  reports `GRANT_DELEGATE` in step 9. What a verifier reads of a parent at
  admission stays with proposal Q1 of LIP-0026.

Agreement pending, and carried in the octets so that they do not change
when the answer comes: section 11 as a whole; the delegation key that signs
a child (LIP-0014 J4); the stop coin of a row (LIP-0014 J2, LIP-0027); the
seal in the grant and the child-seal key (LIP-0008 section 11.4, LIP-0014
section 11.2); and J10 to J12 as before. None blocks.

Chosen by section 11 where no decision gives a form, marked in its table
"Where each member comes from" and open to the owners: the member names;
`issuer.grant_key` in the payload; one executor for the own scope of a
grant; `delegate` present or absent in place of a member `depth`; the two
members for a certifier; the place of the stop coins of a group; the order
of `actions`; the two codes. Marked NEW: the smallest count of one group
and one range, in LIP-0020 and in LIP-0026 alike; and that a reader of a
document refuses on the rules of W11.10 which a decision gives, which is
marked for the owner and awaits the owner's line, with the recommendation
"yes" of the review of record.

The bounds have one status. The largest counts of 16 groups, 16 ranges and
4096 coins and the size of 65536 octets are decided limits of J12, and
LIP-0020 W11.6 and LIP-0026 R8.4 both state them as bounds of the schema;
LIP-0026 no longer calls them proposed. No statement of J12 in the
specification names one of the four numbers: each rests on the owners'
decision register alone, which this repository does not hold, and LIP-0020
W11.6 marks them so.

Not decided and left open: proposal Q1 of LIP-0026, which would keep the
size alone and drop the three counts, and until it is decided the counts
bind; whether dropping a bound takes a new version of the type under
LIP-0020 W3.3; the two proposal points of W11.10;
the registries of action names and of limit kinds; the octets of a scope
text on v4 and of typed constraints such as a ref, a payee or a list of
targets; a v4 code for a child that is wider than its parent in chain,
actions or window; the key that assents to a child's contract; the seal of
a single-use grant.

`vectors/LIP-0020/grant-v4.json` holds 112 vectors: 11 valid signed grants;
84 refusals with one defect each, over 19 codes together with the next
group, which are all the codes that the pipeline of a grant reports; 13
with several defects for the order of refusals; and 4 whose outcome is
"`ok` or `GRANT_DELEGATE`". Each refusal with one
defect names a valid neighbour that differs from it in that defect and in
nothing else; one, the stand-in octets of the earlier vectors, which a
reader of grants now refuses as `WIRE_MEMBER`, names none and says so. The
statement of one defect does not cover the vectors with several defects.
The four undetermined vectors are parents that break one proposal point of
W11.10 and nothing else. Each passes steps 1 to 8; a reader that judges
the point reports `GRANT_DELEGATE` in step 9, a reader that does not judge
it reads `ok`, and the checker refuses any other code. Among the vectors
are a parent of exactly 65536 octets and the same parent with one octet
more, a parent at 16 groups, 16 ranges and four notaries beside the same
parent with one more of each, a pool that its rows exceed only when the
sum is computed beyond 64 bits and one that they exceed only when a
product is, four vectors on the presence, the last index and the
distinctness of stop coins, and four document defects on the octets of
a grant. Four codes that section 11 names have no vector in the file,
because the pipeline never reports them: `CHILD_ORDINAL`, `CHILD_SEAL_KEY`,
`DELEGATE_KEY_REUSE` and `SEAL_PROFILE`. Section 12 says for each where it
is exercised; `CHILD_SEAL_KEY` and `DELEGATE_KEY_REUSE` have no vector in
this repository.

`tools/grantv4/grantv4.py`, in Python with the standard library alone, is a
reader of section 11 with the generator and the checker of the file. The
file was computed by that one implementation, whose reader also checked
it; no second one has recomputed it. Section 12 and the header of the tool
state what an independent implementation must recompute. No vector reads a
chain.

LIP-0026, LIP-0008, LIP-0014, LIP-0021, LIP-0023 and LIP-0027 point to the
new section where they called the octets of a grant, of a row, of a pin, of
the profile pin or of a stop coin open, and change no rule. LIP-0026 says
that `GRANT_DELEGATE` is the code that R1.5 left open, states the four
numbers of R8.4 as decided bounds of the schema, and says that this does
not decide its proposal Q1. The README and the open-question index follow.

## 0.1.52 — 2026-11-16

Closes the specification-side reconciliation gaps in Decision 0004. Every
LIP retains its status. J9 to J12 keep their version 0.1.51 classification;
no historical protocol, tool, vector byte or vector outcome changes.

LIP-0029 decision 1, section 1 and row X1, and LIP-0013 section 3.7 point 2
carry the signed-at-minimum, encrypted-at-maximum rule: the transitional
stage M0 delivers unsigned work but labels it, the unsigned message itself
is given no effect, and after the M6 switch unsigned input is ignored.
LIP-0029 section 1 defines M0 and M6, and LIP-0013 no longer uses the bare
label M6, which names a scenario there. LIP-0029 records the conditions of
the M6 switch: the live messenger-device check, the owner's own test and
break-glass, with observe-only verification until then. LIP-0029 states
that a host is one node under chain rules and keeps its device-list
protocol. Registry simplification inside a host and the other owner-open
reconciliation questions stay open.

One point of the signed-communication rule is open, and no mechanism is
proposed for it: a run started by labelled unsigned work still gets the
owner row; binding of effects to the key holder signature is not specified
(LIP-0013 open question T12; LIP-0029 "Open questions").

LIP-0028 states the caller authority of today's proxy: the bearer holds the
dispatcher-prepared run binding, issued upstream under J7, and on-use checks
cover mode, window and account block without consulting the key holder or
chain. The text names the platform dispatcher and the gateway as preparers
of a binding; whether they are one preparer in today's deployment is listed
as open. LIP-0013 states plainly that a receiver cannot verify an origin and
that the level holds at an honest key holder only.

The authority frame arrives in a separate channel; its signature is NOT
established by the corrected source. LIP-0013 withdraws the earlier claim
of a decided signer and the dependent format and key: rules FE1 to FE7,
case S3-4F and the frame-key entry of the key registry. The paragraph of
open points and the draft's proposal of a local, unsigned frame stand as
before version 0.1.51 worded them, with the channel named as separate.
LIP-0029, the key registry, the README and the open-question index follow
the correction.
The version 0.1.51 changelog below records the superseded claim as history.

LIP-0008 section 5.2 cites J6 grant closure at foreign verifiers separately
from the platform project stop (section 22.5) and installation stop (section
6.6.2). Section 5.3 follows those distinct mechanisms. Sections 3 and 7.1,
and LIP-0003 section 2, limit issuance to issuer name expiry observed at
issuance, 36000 blocks from the last update; the issuer refuses to sign
beyond it. LIP-0003 leaves its clock-time conversion open. LIP-0008 section
2.1 records the contract plus at least TEXT and EFFECT grants per hire, and
the rental row of LIP-0017 section 7 follows it. LIP-0006 section 1 records
wallet request signing through Keymaker, with
origin and operator-table checks, while keeping the existing wallet slice.

LIP-0026 gives four explicit proposals, each marked "proposed, owner
decision pending": whole-parent atomic refusal with the existing byte bound
instead of count caps, ordinal-to-row mapping, class checkpoint derivation
and normative class refusal codes. None is enabled in the in-force profile.
The decision map at version 0.1.51 remains the boundary, and whole-parent
and whole-child composition stay unavailable under it.

The owner decisions first recorded in this version are in force in it:
the hire split, wallet request signing through Keymaker, signed
communication with the M0 transition, the one-host rule, the staging of
the M6 switch, the separate channel of the authority frame and the grant
term against name expiry. The co-author's answer to each is folded in later
by amendment and gates nothing. Decision 0004, "Status of the decisions of
this version", names the decider and date of each. These markers of a
pending agreement stood over the texts that carry them, and none blocks:

- the status line of LIP-0029 ("until the co-author agrees every text that
  this LIP revises stands as written") and its header "Revises, once
  agreed";
- "written optimistically: the co-author's agreement is pending", over the
  decision tables of LIP-0029;
- "the co-author's agreement is pending", over the pattern of LIP-0013
  section 3.7, and "awaits the co-author's agreement" in that section's
  last paragraphs;
- "the co-author's agreement is pending", over the authority frame of
  LIP-0013 section 3.4;
- "The co-author's agreement is pending", after the term and hire rules in
  the README's account of the v4 draft;
- the same marker in the rows "Text and effects; the authority frame" and
  "Owner control by signed envelopes and a pinned device list" of the
  open-question index.

Each marker keeps its force for the other text under it.

Decision 0004 records completion of v4 and landing of the row-groups and
session laboratories as prerequisites to freeze, without declaring either
a freeze or a landing. Existing text already carries v4 seals, confirmed
statement heads, the emergency brake, delayed anchor overwrite, shadow
observation between owners, J10 to J12 and the night's device decisions;
the reconciliation does not duplicate them. Book-only rows remain for the
book round.

## 0.1.51 — 2026-11-16

Adds Draft text for eleven decisions of Ivan Oparin of 2026-11-16: five that
the lead recorded in the consolidated brief, three on owner control that
the lead relayed at about 00:40Z, and three more on owner control relayed at
about 01:15Z and 01:40Z. The text is written optimistically: the
co-author's agreement is pending, and until it is given every text that it
revises stands. Puts J10, J11 and J12 in force. Every LIP stays a Draft,
nothing is implemented, no v3 byte changes, and no vector outcome changes;
the notes of three vector files change.

The seal binding and the child-seal key (LIP-0008 section 11.4, LIP-0014
section 11.2). The decision drops the separate seal-key endorsement only if it
is redundant. Section 11.4 shows that it is: once a v4 grant carries the seal
public key, each of the endorsement's eight members is in the grant or follows
from it, and the same grant key signs both at the same time. Six cases in which
the endorsement could still carry something are checked, and none does. The
grant states its seal (SB1), the verifier compares the script on its own node
before the spend counts as the issuer's (SB2, SB3), and the endorsement type
leaves the registry once agreed (SB4). The spec review confirmed the argument
in substance. Every text that still reads the endorsement points to section
11.4 and stands until agreement: section 11, rule 4 of sections 11.1 and 11.3,
the watch-only import, the two conformance rows of the endorsement, LIP-0029
O10.2 and the README. Section 11.4 no longer says that sections 11, 11.1 and
11.3 do not change: a child's seal pays its parent's child-seal key, not a key
of its own, and the child's grant states that key. Every v4 parent names a
child-seal key from the first version (CS1). Every child's seal pays it (CS2),
and it differs from the grant key, the delegation key and the other keys of
the path (CS3). The delegating operator holds it apart from the delegation
signer (CS4), so a child that a thief of the delegation key signs can still be
revoked. Cases S4-9 and S4-10.

One mechanism for statement sets (LIP-0010 section 11, LIP-0016 section 3.1).
The head of every statement set of an owner is a member `{"seq","sha256"}` of
the owner's name value outside `swarma`, and only the last head confirmed in
the active chain counts. A pending update gives no head, and a defect of a
head member refuses that set and no other part of the value (SH1 to SH8).
After a reorganisation that removes the name operation of the head that a
reader journaled, the last confirmed head counts again, as the Link book §9.4
has it, and every refusal that the reader journaled stays; a lower `seq` that
a later name operation carries still refuses (SH5). This narrows the version
pin of LIP-0029 O9.2, and LIP-0029 says so. `swarma-devices` of LIP-0029 is
the first head and `swarma-certs` the second. The certificate store drops its
anchor, its chain of spends and the mempool step, and its head is no longer
signed (CH1 to CH4). With both heads, a landlord value with a NIP-05 object
and one relay leaves 22 of 520 bytes, which is stated as a cost.

The emergency brake on v4 (LIP-0008 section 5.3, LIP-0011 section 4). The brake
names the stops of v4 that one owner starts alone: a device seal, a recorded
seal spend and the break of the issuer name. It states, for a witness, for a
node that has not seen the transaction and for a newcomer, when each act takes
effect before confirmation and after a reorganisation. An issuer keeps a
confirmed UTXO of a cold wallet for the fee of the break (EB1, the decision).
The draft proposes the rest: the break's inputs and change (EB2), restoring
the reserve (EB3), the fee raise through the break's change (EB4), the
monitor (EB5), and that no act is undone (EB6). A break signed in advance and
held by the L2 devices is proposed and not decided; it needs no cold key only
while its fixed fee suffices. A recorded seal spend carries no verdict
reference, and LIP-0011 says that this is no defect.

The trust-root pin (LIP-0015 section 5.1). An overwrite by the administrator
that no rotation statement carries is pending for a stated delay, proposed as
1008 blocks. The loader notifies the owner over a channel the agent cannot
reach. It takes the pin into effect only at `E`, the later of
`effective_height` and `h_first` plus the delay, where `h_first` is the
height its node reports at the first notice on a node that is caught up: out
of initial block download and with no header more than `LAG` above its tip
(LIP-0022 B2.3), taken as the greater of the tip and the best header. Until
the node is caught up the loader keeps the current pin and records no
anchor. A backdated pin, a late loader or a node that comes back in initial
block download or with headers above its tip leaves the owner the whole delay
(S51-3). A node that is behind and still passes that test, without peers or
restarted before its headers sync, is stated as a limit. The currently
pinned grant key can cancel until then with `swarma-root-cancel/1` (AO1 to
AO6). The administrator account owns the pin and the loader's records, so
whoever takes it can rewrite the pin directly; the section states this as a
limit, as for a replaced loader. The thief of a stolen grant key can veto
recovery by overwrite. The draft proposes that a key that the name owner has
since replaced cannot cancel, and leaves it open.

The authority frame (LIP-0013 section 3.4). The frame is an envelope of body
kind `authority-frame/1`, signed by the key holder with a frame key that signs
nothing else (FE1 to FE3). It reaches the run on the run's own channel, and the
harness verifies it before the agent sees it (FE4, FE6). Text in the stream
that looks like a frame is data (FE5), and a frame is presented once (FE7). T11
is narrowed.

Owner control, three decisions relayed at about 00:40Z (LIP-0029 sections
3.5, 4.1 and 8.3; decisions 14 to 16). Figure 1, the device seal, stands in
the LIP in the words of the decision, for the book to carry in the same words:
a seal on a fresh key, a revocation signed in advance with it, the key
destroyed, the revocation with the other devices, and the list hash in the
name by the cold key; per command the device signature, the hash from the name
and `gettxout` of the seal; on loss any device broadcasts the revocation, and a
rollback cannot restore the device (O8.8 to O8.10). The name pins only the
hash; the list is addressed by its content; the sender attaches it, and
executors cache it by hash. The owner's domain, at
`/.well-known/swarma/device-list/<h(D)>`, and a Nostr event are secondary
paths, and their unavailability never blocks a sender that attaches the list
(O3.11 to O3.14). A messenger device is an ordinary
record: `alg` `matrix-ed25519` for a Matrix device's Ed25519 key, `ceiling` 1
and no presence. A Megolm event counts as an L1 owner command only when the
receiver binds its session to that key through the Olm channel; forwarded,
backed-up or imported sessions and every event whose device it cannot bind are
refused (`MESSENGER_UNAUTHENTICATED`), and plaintext never counts (OM1 to
OM7). Section 3.2 gains an example list of 789 bytes with its hash, so that an
implementation can check its encoding. Cases S29-16 to S29-18.

Owner control, three decisions relayed at about 01:15Z and 01:40Z (LIP-0029
sections 3.5 and 3.6; decisions 17 to 19). Distribution is refined: the
sender attaches the full list when it changes and at first contact with a
receiver, and otherwise the envelope carries the hash alone; the receiver
caches by hash; an unknown hash refuses with the named `LIST_UNKNOWN`, which
replaces the draft's `DEVICE_LIST_UNAVAILABLE`, and the sender re-sends; no
silent fetch replaces the refusal, and a reader fetches only from the two
places that the owner's name value names. The Nostr path is a parameterized
replaceable event with the tag `d` `swarma-device-list`, signed by the Nostr
key in the name; a storage service by grant comes later (O3.12 to O3.14).
An algorithm registry gives every `alg` of a device record its key
encoding, its signature encoding, its presence semantics and its highest
level: Secure Enclave P-256, FIDO2/WebAuthn with the UP and UV flags as
signed presence, YubiKey PIV P-256 and P-384, TPM 2.0 P-256, Android
Keystore/StrongBox P-256, Matrix device Ed25519, XMPP OMEMO, Signal identity,
Nostr BIP-340, OpenPGP Ed25519, and SSH Ed25519 and sk-ecdsa; Telegram
secret chats and WhatsApp are not supported, with the reason stated. Only
Matrix has a verifier in M5n; the entries other than `p256` and `bip340` are
reserved, and a receiver without a verifier admits the list and refuses the
device's commands (O3.15 to O3.17, `DEVICE_ALG_UNSUPPORTED`). A verifier
enforces the highest level per `alg` value, because it cannot tell the four
`p256` entries apart; the lower level of a PIV, TPM or Android key binds the
owner's client at enrolment (O3.16). The D2 signer threat model is accepted
with limits: a key without per-signature presence is L1 at most, the
presence flag is a claim, and a host console with agent shells is not L2. L2
is strengthened at the signer: `biometryCurrentSet` with no passcode
fallback, a fresh authentication for every signature without `LAContext`
reuse, the fields shown by the signer itself, and the signer qualified for
these on a real Mac; several L2 devices each have a record, a finger change
invalidates that device's key and the device returns by the slow add path,
and two L2 devices are recommended (O3.18 to O3.20, O6.2). Case S29-19. OM6
pins which Matrix event counts as a plain command: `m.room.message` with
`m.text`, its `body` without the reply fallback; an edit and every other
event are ignored. The staging relayed with decision 19 is not written into
the LIP: it is a deployment matter, and O1.1 stands as written.

Puts J10, J11 and J12 in force. Ivan Oparin decided them on 2026-11-15, and on
2026-11-16 decided to put them in force without waiting for the co-author's
agreement, which has not been given: «принимаем оптимистично их не ждем. но
ответы учитываем и потом правим». The co-author's answer, when it comes, is
folded in by amendment. J12, groups of rows, is LIP-0026 section 8; J10, the
landlord class, is LIP-0026 section 9; J11, the list `holders` in the landlord
binding, is LIP-0010 section 10. Each section now opens "In force since
version 0.1.51", and LIP-0014 "Decisions of 2026-11-15" records the state of
each. What those sections mark as the draft's stays a proposal: the bounds of
R8.4, the order of the count in R8.3 and the witness key hash of R8.2, the
checkpoint of R9.2, the fifth step of R9.5, the eight codes of a class, the
order of `holders` and the refusals of its rule 3, and the rules R8.9, R8.10,
R9.11 and R9.12 for the two signers.

The gate of J9 is lifted. Under 0.1.49 no child of a row without a certifier
was admitted, because both recipient constraints of J9.2 rested on J10 and J11.
With J10 and J11 in force, such a child is admitted where its recipient passes
the checks of LIP-0026 section 9 for a class, or of R10.3 for an exact name,
and it needs no attestation (LIP-0014 J9.1). That admission rests on J9, which
both owners agreed, and on J10 and J11, which only Ivan Oparin has decided; the
texts say so in place. Other texts follow: LIP-0027, KEY-REGISTRY, the notes
of `vectors/LIP-0010/holders-vectors.json`, `vectors/LIP-0026/class-vectors.json`
and `vectors/LIP-0026/groups-vectors.json`, the README paragraphs of 0.1.47 and
0.1.49, and two rows of the index of open questions. The co-author's answer on
J10 to J12 is listed as open.

Review. The spec review of 77cc51d (rev372) found four defects, fixed in this
version: the cancellation window of section 5.1 ended before the pin took
effect; the claim that the administrator account cannot hide an overwrite was
not held by the rules; the surfaces that read the endorsement were not
revised; and SH5 refused the last confirmed head after a reorganisation. Two
citation slips are corrected (§7.7, «Доставка памяти агенту»). The delta
review of 82c5eda (rev372 r2) found two more, fixed in this version: the
anchor `h_first` of LIP-0015 AO3 could come from a lagging node and shorten
the window, and OM7 of LIP-0029 left step 5 of the admission to refuse a
plain encrypted text that carries no `devices` member. The review of 4286c11
(spec-r3) found four more, fixed in this version: case S29-16 admitted an
owner command of Alisa's device at Bob's executor, against O10.4; the
per-entry levels of the registry were written as verifier refusals, though a
verifier cannot tell the entries of one `alg` apart, and S29-19 refused a
record identical to its own control; a staging paragraph conditioned
decision 1 without a decision; and the real-Mac check of O3.19 was written as
an act of the client at enrolment instead of a qualification of the signer.
Two of its notes are taken: the last sentence of AO3 no longer claims that
every node behind the chain leaves the whole delay, and OM6 pins the event
and the part of it that count.

Reconciliation. The text cites:
- the platform book: chapter 22 §22.5, chapter 6 §6.6.2, chapter 7 §7.7 and
  §7.12, chapter 8 §8.3 and chapter 11 §11.10;
- the Link book: §3.9, §3.10, §3.12, §4.9.3, §4.9.9, §5.4, §6.13, §9.2, §9.4
  and §10.3 to §10.4;
- curator-spec CIP-0011 revision 6.

Where the books say otherwise, it names the update for the book: the child-seal
key as a profile option, the endorsement, the store's anchor and mempool step,
the rule that only both acts together change the pin, and the unsigned local
frame. The brief's chapters 05, 08 and 11 are read as the platform book's
chapters 6, 7 and 9 before the renumbering of 2026-11-10, or as chapters 5, 8
and 11 after it; the citations name sections by title.

Pointers. The key registry adds the emergency fee reserve key and the frame key
of a key holder, marks the child-seal key, the grant key and the seal keys,
and gives the device key a Matrix form, the reserved entries of the registry
and the enrolment rule of a Secure Enclave key at ceiling 2, and the device
seal key no holder. The key map, LIP-0020, LIP-0024 and LIP-0029 point to the
new text. LIP-0029 gains the fourth body kind and the reading of SH3 to SH6
for `swarma-devices`.

## 0.1.50 — 2026-11-15

Adds Draft LIP-0029, owner control by signed envelopes and a pinned device
list, for thirteen decisions that Ivan Oparin accepted on 2026-11-15 on
question R4. The text is written optimistically: the co-author's agreement was
not awaited and is pending, and until it is given every text that the LIP
revises stands. Every LIP stays a Draft, nothing of the LIP is implemented,
and no v3 byte changes.

The decisions. Only a signed envelope counts, and an unsigned message is
ignored. Free text directs work; an effect happens only through typed fields
that define it completely, and the executor's gate recomputes the actual
arguments and compares them before the effect. The owner's client forms the
fields and shows them. The action registry is the action profiles of LIP-0006
and LIP-0008, and an unknown class requires L2 or is refused. The owner's name
value pins the hash and version of a device list outside `swarma`, added only
after every verifier runs a LIP-0010 reader; the v3 outage while an update is
pending is accepted. A device record holds a label, the key, its algorithm
(BIP-340 or P-256, taken from the record), a claimed presence flag, a level
ceiling and the outpoint of a revocation seal. A device is revoked by the
spend of its seal, of which the other devices hold a prepared spend, and by an
L2-signed revocation that executors journal; a name update completes the
removal. Adding a device needs a new list, a new seal and a name update. Policy
lives in executor configuration sections with an increasing number, signed by
an L2 device, and every limit belongs to a named executor. P-256 keys are 33
bytes of SEC1 and signatures 64 bytes of r and s under a domain tag, and the
envelope identifier and the replay journal exclude the signature. The one
envelope format is `swarm-envelope/2` with three body kinds: owner command,
LIP-0013 instruction and wallet request. Levels L0, L1 and L2; a launch inherits
the level of the envelope that started it, and at every level that level bounds
what the run's key holder signs: no effect at L0, and at L1 and L2 only the
classes and amounts that the executor's policy admits at that level. The grant key grants to others only,
device keys are the owner at the owner's own executors and agents' key holders,
there is no statement key, and the authority key of a person leaves the key map
for device keys, which closes R5. Three honest limits are stated in the text.

What the draft adds, and marks. Member names and orders of the device record
and the list, the name-value member `swarma-devices`, the type names, tags,
members and lifetimes of the three body kinds, the rows of the key holder's
table by level with the refusal `LEVEL_NOT_FOR_RUN`, the key holder's copy of
each executor's policy section from the owner's L2 device and its checks at every
level (O6.6 to O6.12), the carrier of a policy section as an L2 owner command,
the action `swarma/device/revoke`, the order of admission and its refusal codes,
and fifteen cases.

Reconciliation. The LIP cites the platform book (chapter 6 §6.6 to §6.8,
chapter 7 §7.12, chapter 22 §22.5, chapter 24), the Link book (§3.4, §3.7,
§3.10 to §3.13, §4.9.2 to §4.9.4, §4.9.10, §5.2, §8.9), curator-spec CIP-0011
revision 6 (R-OPERATOR) and `swarm-envelope/2`, and lists fifteen conflicts for
the owners without choosing: among them three anchors for the owner's devices,
BIP-340 device keys against the P-256-only device profile of `swarm-envelope/2`,
and the closed types of that format, which this repository does not own.

Pointers. The key map records that K6 leaves it once agreed; the key registry
adds the device key of an owner and the device seal key; LIP-0010, LIP-0013,
LIP-0015 and LIP-0016 each point to the text that LIP-0029 holds for them.
No vector is added.

## 0.1.49 — 2026-11-15

Puts J9 in force: no certifier for a row inside one owner. Ivan Oparin decided
J9 on 2026-11-15, and the co-author, Alexey Grigorev, agreed on 2026-11-15, so
J9 is decided and agreed by both owners on 2026-11-15. LIP-0014 and LIP-0026
stay Drafts, nothing of J9 is implemented, and no v3 byte, no vector outcome
and no other decision changes.

The rule. LIP-0014 section 8.3 states the decision as four rules in force for a
v4 parent. J9.1: the right of re-delegation states for each row whether it
names a certifier, a child of a row that names one is admitted only with a
valid attestation (D1), and a child of a row without one needs none. J9.2: a
row without a certifier has a recipient constraint limited to the issuer's own
landlord, a class with exactly the issuer's landlord or an exact name that
passes the landlord and holder checks of a class against it; any other such
row refuses the parent. J9.3: across owners a certifier stays mandatory, as D8
says. J9.4: a row without a certifier states no stop coin. LIP-0026 section 10
opens with the same decision; R10.1 and R10.2 now apply to a row, and under
section 8 to a template, and R1.1 admits a row that states no certifier. R10.3
and the second sentence of R10.4 stay the draft's proposals, and so do the
codes of section 9 that R10.3 gives.

What J9 needs from the pending decisions, stated in place. Both recipient
constraints of J9.2 rest on J10, the class and its checks, and on J11, the list
`holders`, and the co-author's agreement to both is pending. In the text in
force a row names a request key or a name with its owner key, and a landlord
value has no `holders`. A parent may hold a row without a certifier whose
recipient is an exact name, and that row admits no child: until both owners
have decided J10 and J11, no child of a row without a certifier is admitted,
and every admitted v4 child is certified. J12 does not bear on J9.

Interactions, stated and not changed. D8 compares the owner of the issuer with
the owner of the delegator, and J9.2 tests the recipient of the child; for a
row without a certifier "across owners" is read for that recipient, the owner
of the delegator is not tested (case S9-K1), and whether it should be is now
an open question of LIP-0014 as well. On v4 the certifier that J1.1 fixes for
an ordinal is a pinned notary or the signed statement that the row has none;
J1.2 to J1.5, J1.8 and the coin of J1.9 apply to such a row unchanged, and J1.6
and the notary's record of J1.7 have no subject in it. The member `notary` of
profile `swarma-trust-contract/2` stays mandatory in every row, a right of
re-delegation without a notary still refuses as `DELEGATE_NO_NOTARY`, and every
v3 child is certified.

Other texts follow the decision: LIP-0006, LIP-0008 and LIP-0012, which
restate D1, say how J9 narrows it on v4; LIP-0027 no longer calls J9 pending;
the note of `vectors/LIP-0026/class-vectors.json` says that J9 is decided and
that its vectors rest on the checks of J10 and the holders of J11; the README
and the index of open questions close J9. No rule of those texts and no
vector changes.

## 0.1.48 — 2026-11-15

Adds Draft LIP-0028, sessions for clients that cannot sign, for a decision of
Ivan Oparin of 2026-11-15 (J13). The co-author's agreement is pending, and
until then a v4 service admits signed invocations alone. Every LIP stays a
Draft, nothing of the LIP is implemented, and no v3 byte changes.

The decision. A service whose client is a third-party program admits a session,
and the model proxy with the harness of a vendor is the first case. The key
holder of the recipient checks the origin of the run against its table and
signs one session-open request under the grant, with the authority path, the
executor, the slot binding, a window of at most one hour and limits within the
grant. The service verifies it like any request and returns a bearer token of
32 random octets, bound in its journal to the grant, the session, the slot
binding, the end of the window and the limits. The slot binding is the user id
of the caller on one host and the address of the slot over a network. The token
stays the same for the run; the key holder extends the window by further signed
requests, and without one the token expires. The service ends every session of
a grant when it observes the seal spent. The harness gets a base URL and the
token.

What the draft adds, and marks. The three requests of a session are signed
invocations, so the proof path has to allow their commands, and a request with
a token never asks for one of them. An end lies at most 3600 seconds after the
service's clock at the admission, an extend request never moves an end back,
and an end is final. A repeated request opens no session and returns no token,
and after a journal that was started anew the service refuses every session
request whose `iat` is not later than the `fenced_at` of the recovery; the
journal holds the SHA-256 of the token and never the token; a lost answer is
not repeated. A token, and the answer that carries it, travel only on a local
socket or on a channel that authenticates the service and that others cannot
read. Before every reservation in a session the service makes the checks of
LIP-0008 sections 4 and 12 for the proof path again, in an observation of its
own, and requires that the key of the session's last signed request is still
the recipient's key; the reservation is one atomic step with the reads that the
session has no end and its path no closure. A session has accounts of its own
beside those of the grant, with the ceiling 0 for a limit key that it does not
state. A closure of any grant on the path ends the session. Seven rules bind
the key holder, which builds the three requests itself, takes the slot from its
own record of the run and keeps runs of one origin in a slot. Eleven refusal
codes are proposed.

Consequences that the text states. A token works until the last end that the
key holder signed, at most one hour after its signature on its own clock; the
end is read on the service's clock. Every process of a slot can read the token,
so a session equals a signature on every request only where the slot holds runs
of one origin; a deployment that mixes origins under one user id lets one run
use the grant of another. An address does not tell the users of one host apart,
nor the hosts behind one translation of addresses. Requests in a session are
unsigned, so a billing dispute has the records of the two parties and nothing
else. `SO_PEERCRED` works only for a local socket, and the decision gives the
harness a base URL: how the two meet is open, and the binding by user id cannot
be built until then. After the operator removes a grant from the key holder's
table, the key holder can sign no close request under it, and the session ends
with its window.

No vector is added: the three signed requests are invocations, which have no
members yet, and the record of a session waits for the entries of a service
journal. Section 9 of the LIP states twenty-four cases and four known limits
in words.

Other texts: pointers in LIP-0007 section 1, LIP-0008 sections 5 and 12.1 and
LIP-0013 section 3.6; a row for the sessions of a service in LIP-0025 section
7; the key registry, at the model bearer of a slot; the list of decisions that
stand outside LIP-0014; the README and the index of open questions.

## 0.1.47 — 2026-11-15

Records four decisions of Ivan Oparin of 2026-11-15 on the rows of a v4 parent,
as Draft text. The co-author's agreement on each is pending, and until then the
text in force stays as it is. Every LIP stays a Draft, and nothing of the four
is implemented. No v3 byte changes: the contract profile
`swarma-trust-contract/2` keeps its member set, each of its rows names a
notary, and every v3 child is certified.

Groups (J12; LIP-0026 section 8). A parent states its rows as groups: a
template with the executor, the recipient constraint, the limits of each child
and a certifier or none, and ranges of coins, each a transaction id, a first
output index, a count and a script. Each coin is one row, and one ordinal runs
across groups and ranges. The pool bounds, for each limit key, the sum over the
groups of the number of rows times the amount of the template. The bounds are
proposals: at most 16 groups, 16 ranges in a group and 4096 coins in a range,
and a parent of at most 65536 octets. One standard transaction of Namecoin Core
holds at most 3223 outputs of this kind, so 10,000 rows need four funding
transactions. Under groups one key of the row account serves one range.

Landlord class (J10; LIP-0026 section 9). The recipient constraint of a row
gains a third form: a list of landlords, each pinned by name, registration and
owner key, with the recent block of the parent as the checkpoint. A child of
such a row names its recipient by name. The executor checks, in this order,
that the value of the recipient name is an agent binding of a listed landlord;
that the landlord is live, unchanged in its owner since the checkpoint and
without a pending operation; that a holder of the landlord holds the recipient
name; and that a holder wrote its value. The fourth check answers an attack
that the text states: anybody can send a name to the address of a holder, with
a value of its own choice. Eight refusal codes are proposed.

Holders (J11; LIP-0010 section 10). The landlord binding gains a member
`holders`: the owner keys of the names of the landlord's agents and stations,
as owner pins in ascending order. An absent or empty list admits no name. A
landlord value holds at most five holders without a `nostr` member, four with
a key string or a NIP-05 object, three with one relay and two with two relays.
The list is part of `swarma`, so an update that changes it ends the v4 grants
that the landlord issued before, under LIP-0008 section 3; a reader that does
not know the member refuses the value, so a landlord with live v3 grants adds
it only after its verifiers read the new shape.

No certifier inside one owner (J9; LIP-0014 section 8.3, LIP-0026 section 10).
A child needs an attestation only where its row names a certifier. A row
without one is valid only where its recipient is a class of exactly the
issuer's landlord, or an exact name that passes the checks of a class against
the issuer's landlord. Across owners a certifier stays mandatory. Such a row
has no stop coin, and LIP-0027 says so.

What the draft adds without a decision, and marks: the order of the count of
rows; that the landlord's value was written by its pinned owner; a rule for the
signer of a holder key, which signs only for names that it registered or that
its operator accepted, because a holder that renews a name which was sent to it
adopts its value; the ascending order of `holders`; and the eight codes. Open,
and listed in LIP-0026: the stop coins of a group, a bound on the landlords of
a class, whether a change of `holders` should end an issuer's grants, and the
owner of the delegator in a row without a certifier.

Vectors. `vectors/LIP-0010/holders-vectors.json` holds 28 landlord values and
the five largest lists. `vectors/LIP-0026/groups-vectors.json` holds 26 parents
and 12 ordinals, and `vectors/LIP-0026/class-vectors.json` 15 templates and 50
admissions, among them the gift of a name beside its valid control, the same
gift by a holder of a co-listed landlord in both positions of the class, and
two children that the proof of the recipient by name refuses. A second
implementation that shares no code with the generator decides all 136 with 0
mismatches. No checker for them is published.

Other texts: the key registry says where a name-owner key of an agent's name is
published under J11, and the README and the index of open questions name the
four decisions.

## 0.1.46 — 2026-11-15

Gives the contract profile `swarma-trust-contract/2` of LIP-0014 one member set
and adds vectors for it. Both owners have decided the two points that this
rests on. Ivan Oparin decided the rows on 2026-11-14 (J1) and accepted the pins
of a notary's name on 2026-11-13 (J3), and the co-author, Alexey Grigorev,
agreed to both on 2026-11-15. LIP-0014 stays a Draft, and nothing of it is
implemented. No v3 byte changes, and neither does any rule or vector of profile
`swarma-trust-contract/1` or the reference checker.

What it answers. Since 0.1.31 LIP-0014 described the right of re-delegation
twice. Its sections 2 to 9 held the first draft: the lists `agents` and
`grantees`, the count `max_children`, notaries as bare names, and an
attestation that added up a pool over siblings. Its sections 7.1 and 9.1 held
the rows and the pinned notaries as Draft text that waited for the co-author.
One profile string stood for two sets of members, and an implementation could
not tell which of them to read.

The one member set. A right of re-delegation is the member `delegate` with
`depth`, `actions`, `budget`, `slots`, `notaries` and `checkpoint`, in this
order. A row of `slots` has `executor`, `grantee`, `cap` and `notary`, and the
ordinal of a child selects its row. An entry of `notaries` has `name`,
`registration`, with `txid` and `vout`, and `owner`; `checkpoint` is the block
from which the history of each notary's name is constrained. A grant without
the right, and every child, carries the one value of depth 0. The contract
keeps its fifteen members.

What is removed. The members `agents`, `grantees` and `max_children`; notaries
as bare names; the attestation members `budget` and `prev_attestation_id`, so
that `swarma-notary-attestation/1` has eighteen members; the verifier's step
V15 with the code `ATTESTATION_ARITHMETIC`, whose number stays unused so that
the later steps keep theirs; the predecessor attestations in a bundle; and the
notary's ledger of a sum. The sections 7.1 and 9.1 keep their numbers, their
rules J1.1 to J1.9 and J3.1 to J3.9 and their cases, and now hold text that
both owners decided. An object with the members of the first draft refuses as
`CONTRACT_DELEGATE`.

What stays pending. The decisions J2, J4 and J5 await the co-author and keep
their Draft text, and one consequence is said in place: a row names its
certifier, and the check that an attestation comes from that notary is rule
J2.2. Until the co-author agrees to it, an attestation by any notary that the
parent names satisfies step V12.

What the draft fixes without a decision. The names, the order, the bytes and
the codes of the profile are still the draft's proposal; this revision fixes
them so that an implementation can be built against one text. Section 3.1 now
says what each rule of a reader owns. Rule 1 owns the form of the bytes at
every depth, the fifteen members and the JSON type of each member except
`delegate`. Rule 9 owns the value of `delegate` as a whole and reports in three
steps: the six members and their types; then depth 1 without a notary, as
`DELEGATE_NO_NOTARY`; then every other rule. Rule 8 reads the depth of a child
only where it is the first member of `delegate` and an integer. Four points of
form belong to no decision and are named for the owners: the owner pin of a
notary as a compressed public key in 66 lowercase hexadecimal characters, which
is the form that Draft LIP-0021 proposes; an output index of at most
4294967295; a largest integer of 9223372036854775807 in the form of the bytes;
and that the key of a row is a valid key, as the key of a grantee is. D12 is a
rule of the reader: a right of re-delegation that lists `spend` refuses as
`CONTRACT_DELEGATE`.

Two corrections come with the exact rules. A contract that names a parent with
ordinal 0 refuses as `CONTRACT_PARENT` under rule 8 and never reaches
`CHILD_ORDINAL`, which earlier text named for it. And step V1 no longer lists
six of the ten contract codes as if they were all.

Vectors. `vectors/LIP-0014/contract-vectors.json` holds 190 vectors: 151
contracts, of which 15 are valid, 3 are valid in the spend profile alone and
133 are refused, and 39 pairs of a parent and a child with the steps that two
contracts decide. A second implementation that shares no code with the
generator decides all of them with 0 mismatches, and both give the 36 published
contracts of profile `/1` their published outcomes. No checker for the new
vectors is published. They hold no grant, no delegation request and no
attestation.

Other texts follow the two decisions: LIP-0008, LIP-0010, LIP-0012, LIP-0013,
LIP-0020, LIP-0021, LIP-0025 and LIP-0026, the key map, the key registry, the
README and the index of open questions no longer call J1 and J3 pending, and
LIP-0021 no longer quotes a sentence of LIP-0014 that is gone. No rule of those
texts changes.
## 0.1.45 — 2026-11-14

Adds Draft LIP-0027, a first profile for the stop coin of a row on v4, with
vectors. Every rule of it is the draft's proposal, and neither owner has
decided one. No rule of another text changes, and no v3 byte does. No node
and no store was run.

What it answers. LIP-0014 section 10.1 records the decision of 2026-11-14
on the stop coin (J2.7), with the co-author's agreement pending: a v4 row
names a coin of its notary, the notary ends the row for cause by spending
it, and every verifier whose node shows the spend refuses the row. The
decision names one code, `ROW_CLOSED_FOR_CAUSE`, for the spent coin. It
names none for a coin that is not there, and a node answers the question
whether an output is unspent in the same way for a coin that was spent and
for one that never existed. What a recovery of the journal of such closures
charges is not stated either.

The profile. A row states its stop coin as an outpoint and a script, a
witness key hash. The stop coins of one parent are different outpoints;
none is the coin of a row, the seal of the parent or the output after that
seal, which the parent's own anchor spends, and the stop coin of a child's
row is neither the seal of that child nor the output after it. At
an admission a verifier reads its journal first. It then establishes that
the coin is on the active chain as stated, at or below the parent's recent
block, and that it is unspent in its view, the mempool included. A coin
that is not on the chain as stated refuses as `ROW_STOP` and records
nothing. A coin that is on the chain and spent closes the row: the verifier
writes an entry `row-closed/1` to a journal of LIP-0025 before any further
admission, and the row stays closed there across eviction, restart and
reorganisation. A closure that cannot be written makes the journal lost for
that verifier, which admits nothing until its operator has acted, as
LIP-0008 section 5.1 says of a seal. A recovery by starting anew charges
nothing, and the verifier is a newcomer. The notary keeps its stop keys at
`m/84'/7'/<stop-account>'/0/<i>` in an account of their own, creates the
coin before the parent is signed, and spends it with inputs that nobody
else can spend first.

Three codes: `ROW_CLOSED_FOR_CAUSE`, with its name from LIP-0014, and two
new ones, `ROW_STOP_ALIAS` and `ROW_STOP`. Only the first records
something.

Vectors. `vectors/LIP-0027/stop-vectors.json` holds 52 vectors over 27
rules: 14 parents, 19 admissions, 8 octet strings that are or are not an
entry, and 11 traces of one verifier and its journal, among them a witness
across an eviction and a restart, a verifier that starts later, a closure
that cannot be written, a lost journal, and a parent whose row names the
output after its own seal, which is refused before anything is recorded.

LIP-0014 section 10.1, LIP-0025 section 7, LIP-0026 section 1 and the entry
of the row stop key in the key registry gain one pointer each. The pointer
in LIP-0026 also says that a v4 row has a sixth thing beside the five of
its rule R1.1.

## 0.1.44 — 2026-11-14

Adds Draft LIP-0026, a first profile for the rows of a v4 parent, their
coins and the accounts of a grant, with vectors. Every rule of it is the
draft's proposal, and neither owner has decided one. No rule of another
text changes, and no v3 byte does. No node, no signer and no store was run.

What it answers. LIP-0014 section 9.1 records the decision of 2026-11-14 on
rows (J1), with the co-author's agreement pending: a parent signs one row
for each child, an executor reserves a request under a child in two
ledgers, and on v4 each row pins a coin that the issuance of its child
spends. It leaves open who funds the coin and the account and the path of
its key, and it names no code for a child whose issuance does not spend the
coin. LIP-0008 section 12.2 charges a request against every applicable
link, and LIP-0014 section 9 keeps the parent's own budget apart from the
pool; neither says which counter an executor keeps under which key.

The profile. A row states its executor, the recipient of the child in one
mode, its limits, its certifier and its coin, as an outpoint and a script.
For each limit key a pool bounds the sum of the rows. A verifier checks a
child against the row of its ordinal on signed octets alone, in the order
and with the four codes of J1.2. The coin has a witness key hash script and
is confirmed on the active chain at or below the parent's committed recent
block, which is how a verifier reads "confirmed before the parent is
signed"; one input of the child's anchor spends it. The coin is no output
of the child's seal transaction, so that the linkage input of LIP-0023 and
the input of the coin are two inputs: LIP-0023 alone admits an anchor in
which one input is both. A row key has the path
`m/84'/7'/<row-account>'/0/<i>` in an account of 10 or above that holds row
keys alone; the operator of the re-delegating side funds the coin; and the
signer signs with a row key one kind of input, the one that spends the coin
in the anchor of that row's child. An executor keeps own accounts and row
accounts. A request under a child debits the own account of the child and
the row of its parent, and no own account of the parent; the pool is no
account, and no row borrows from another. One request identity holds one
reservation.

Two points are the draft's own reading where texts meet, and the LIP names
them first for the owners: the recent block as the mark of the moment of
signing, and the row as the parent's link for a request under a child.

Nine codes with an order. Five have their names from LIP-0014:
`CHILD_ORDINAL`, `CHILD_AGENT_NOT_ALLOWED`, `CHILD_GRANTEE_NOT_ALLOWED`,
`CHILD_BUDGET_OVER` and `ROW_CAP_OVER`. Four are new:
`ROW_COIN_IN_SEAL_TRANSACTION`, `ROW_COIN`, `ROW_COIN_REQUIRED` and
`OWN_LIMIT_OVER`. The three codes of the coin stand after the checks of
LIP-0023, whose codes keep their meaning.

Vectors. `vectors/LIP-0026/rows-vectors.json` holds 64 vectors over 34
rules: 13 parents, 18 children against their rows, 20 on the coin, and 13
traces of an executor's ledger, among them one parent over three executors,
direct requests beside the requests of two siblings, two documents of one
row, a repeated request and a request that consumes two limit keys. They
state facts and hold no grant, no transaction and no entry of a journal.

LIP-0014 section 9.1, LIP-0008 section 12.2 and the open points of the key
registry gain one pointer each.

## 0.1.43 — 2026-11-14

Adds Draft LIP-0025, the journal continuity profile for Grant v4, with
vectors. Every rule of it is the draft's proposal, and neither owner has
decided one. No rule of another text changes, and no v3 byte does. The
draft selects no store, and nothing of it was built or run.

What it answers. LIP-0014 section 9.1 (J1.4) states the contract of a store
whose continuity is proved against a record outside it, and says that the
form of that record and the proof of continuity are an open deployment
profile. LIP-0008 section 5.1 keeps evidence under a recovery and
anti-rollback profile whose encoding is open. LIP-0020 W7.9 has an issuer
record a consumed consent durably and before it signs the grant.

The form. A journal has an identity and a position, and its entries are
JSON objects in the canonical form of LIP-0020. Its history commitment is
`c(0) = D(identity)` and `c(n) = D(c(n-1) || e(n))`, with the typed digest
of LIP-0020 under the tag `swarma-journal/1`. The outside record holds the
identity, a position, the commitment at that position and a write token,
and it has one operation that changes the history: it takes a new
commitment only as the successor of the exact one that it holds, from the
writer with the current token. An entry goes to the store first and to the
outside record second, and the act that it records happens after both.

The check. Four outcomes: intact; pending, where the store is exactly one
entry ahead on the same history and the writer completes the outside write;
fenced, where the writer does not hold the current token; and lost, which
is every other state. Equal positions with different commitments are lost.
The token is compared before the histories, so that a replica that was cut
off is fenced and does not call the journal lost.

Recovery. A lost journal refuses every act that needs it. Its operator
restores a store that passes the check, or starts a new journal in one
attended act. The new journal begins with an entry that states the lost
identity and the time of the fencing, and it charges everything that the
lost journal could have held. A journal that counts from blocks gains a
boundary: a block of the active chain in a healthy observation whose header
time is more than 7200 seconds later than the fencing. The two hours are
the bound that consensus puts on a header time: no node with a right clock
had accepted such a block before the fencing, so the lost journal holds
nothing that rests on it. That shows when a node accepted the block and not
when it was mined, and the LIP says where this is less than the words of
LIP-0014 section 9.1.

The consent journal. One journal for one grant key. The issuer writes an
entry `consent-consumed/1` after the checks of LIP-0020 W7.4 to W7.8 and
before it signs the grant. Its clock does not read less than the largest
time in the journal. After a recovery by starting anew it treats as
consumed every consent whose `created_at` is not later than the fencing.

Three codes: `JOURNAL_LOST`, `JOURNAL_FENCED` and `JOURNAL_CLOCK`.

Vectors. `vectors/LIP-0025/journal-vectors.json` holds 66 vectors over 33
rules: 7 histories, 12 octet strings that are or are not entries, 16 states
of a store against its outside record, 10 operations of the outside record,
9 on the boundary, and 12 traces of the consent journal, among them a crash
between the two writes, a restore, two histories at one position, a fenced
writer and a recovery. No store was run.

LIP-0014 section 9.1, LIP-0008 section 5.1 and LIP-0020 section 7.4 gain
one pointer each.

## 0.1.42 — 2026-11-14

Adds Draft LIP-0024, the seal and endorsement profile for Grant v4 on
Namecoin, with vectors. It gives the registered type
`swarma-seal-endorsement/1` its members. Every rule of it is the draft's
proposal, and neither owner has decided one. No rule of another text
changes, and no v3 byte does.

What it answers. LIP-0008 section 11.2 records Ivan Oparin's decision of
2026-11-14, with the co-author's agreement pending: the eight members of an
endorsement by their meaning, and the order of the verifier's five steps.
It says that the bytes stay open and that the refusal codes come with the
bytes. LIP-0020 registers the type without a member.

The seal. A revocable-only seal under the Witness profile: an output that
pays the witness key hash of its own seal key, as LIP-0008 section 11.1
decides for that profile.

The endorsement. A signed object of LIP-0020 under the issuer's grant key,
at most 2048 octets, with nine members: `type`, `genesis`, `issuer` with
the name, the registration and the owner pin, `construction`, `seal`,
`outpoint`, `seal_public_key`, `script` and `grant`. The reference is the
identifier of the grant, which exists before any signature; the decision
allows the grant or the signed preparation.

The order. Parsing first, without any signature check. Then the decided
steps: the verifier's node supplies the output (`SEAL_OUTPUT`) and its
script equals the endorsed one (`SEAL_SCRIPT`); the profile is the
verifier's (`SEAL_PROFILE`) and the script is the script of the endorsed
key (`SEAL_SCRIPT_KEY`); the signature verifies under the grant key of the
pinned issuer; the endorsement speaks of this grant (`SEAL_BINDING`). The
read of the output stands before the signature, which differs from the
pipeline of a signed object in LIP-0020 W9.1; the LIP states the
difference. To the one binding that the decision names, the same outpoint,
the draft adds three: the grant's identifier, its chain and its issuer pin.

Custody. The provisioning and custody of the seal account are open and
before an owner. The draft proposes five points and nothing beyond them:
separate seal and funding accounts; a grant key that signs no transaction
and pays no fee; a seal account that is not `m/84'/7'/0'`; no seal account
derived from a grant key; and a provisioning sitting and a wrapping of its
own for each account. No rule of the endorsement and no vector depends on
them.

Vectors. `vectors/LIP-0024/endorsement-vectors.json` holds 47 vectors over
15 rules: 6 on the seal script and 41 signed endorsements with a stated
context, eight of them with two defects for the order. The signatures are
BIP-340 signatures under published test keys. The grant is given as stated
facts, because a grant has no members yet. No node was run.

LIP-0008 section 11.2 and LIP-0020 section 3 gain one pointer each.

## 0.1.41 — 2026-11-14

Adds Draft LIP-0023, a first Witness construction profile for Grant v4 on
Namecoin, with vectors. Every rule of it is the draft's proposal, and
neither owner has decided one. No rule of another text changes, and no v3
byte does.

What it answers. LIP-0008 sections 1.1 and 9 state the Witness profile:
native witness inputs with `SIGHASH_ALL`, confirmed ordinary funding, and
two permitted unconfirmed dependencies, the linkage output and a same-chain
payment output. Section 1.1 says that the exact dependency and payment
checks still need versioned fixtures.

The profile. A verifier takes the construction profile from its own
authenticated configuration; a missing value, another value and the Legacy
profile refuse. The linkage output of a grant is the output that follows
its seal in the seal transaction. The anchor spends that output, no other
output of the seal transaction, and never the seal. That holds for every
grant, also where the seal transaction was confirmed long before, so that
only the holder of the key of that one output can publish an anchor; an
issuer signs a grant only where that output pays a key of its own signer.
Every input of
both transactions spends a witness key hash, has an empty unlocking script
and a witness of two items: a signature that ends in `01` and the
compressed key that hashes to the spent output. A name output is no such
input. Every input other than the linkage input spends an output of a
transaction that is confirmed below its spender; a parent in the spender's
own block counts as unconfirmed. An effect needs a confirmed anchor. A
replaced seal transaction needs a new grant and a fresh consent; a replaced
anchor that spends the same linkage output and carries the same frame
changes nothing that was signed.

Narrower than LIP-0008 in one point: an unconfirmed payment output refuses,
because nothing that a grant signs today lets a verifier tell it from other
unconfirmed funding.

Thirteen codes with an order. Twelve of the names are stable reasons of the
reference laboratory, which implements a linkage-only subset of the Witness
profile for Grant v3; `W_LINKAGE_REQUIRED` is wider here, because the
laboratory asks for the linkage only while the seal transaction is pending
or shares the anchor's block and takes whichever output of the seal
transaction the anchor spends; `W_LINKAGE_SCRIPT` reports the script of the
fixed output; and `W_ANCHOR_PENDING` is new.

Vectors. `vectors/LIP-0023/construction-vectors.json` holds 63 vectors over
18 rules: 22 on the octets of one input and 41 on stated pairs of
transactions, twelve of them with two defects for the order. Nine of the
pairs test the fixed place of the linkage output, among them a seal
transaction with an output of another party, one with the seals of two
grants, and one whose seal is its last output. No node was run.

LIP-0008 section 1.1 gains one pointer.

## 0.1.40 — 2026-11-14

Adds Draft LIP-0022, the observation, freshness and risk profile for Grant
v4 on Namecoin, with vectors. Every rule of it is the draft's proposal, and
neither owner has decided one. No rule of another text changes, and no v3
byte does; the observation and the 30-minute stop of normative v0.1 stay as
they are.

What it answers. LIP-0008 section 6 records as decided design that money or
irreversible actions stop at a tip age of 60 minutes and other privileged
actions at 90, and that admission needs two independent nodes that agree on
the tip. It leaves open the age measure, the clocks and the criteria for
the nodes. Section 7 leaves open the recency policy of the committed recent
block, and LIP-0021 leaves open how one consistent observation is taken.

The profile. An observation is a set of reads between two reads of the same
tip; where the tip moved, it is void, and nothing is recorded as closed.
The verifier's configuration names the comparison nodes, and an observation
asks each of them for its tip and for what shows its health. Two nodes
count as two when their operator labels them as of different sources. A tip
agrees when it is the reading node's tip or at most one block below it on
the same chain, and it conflicts when it lies above that tip or on another
branch. One healthy comparison node whose tip conflicts refuses the
observation, whatever the others answer, and at least one node of another
source has to agree. The age of the tip is the larger of two ages: the
verifier's clock minus the time in the header of the tip block, and the
clock minus the first sight, the reading at which the verifier first
observed that block as the tip. The verifier keeps every first sight
durably. On one tip a money or irreversible action is therefore admitted
for less than 3600 seconds from the first sight, for every header that
consensus accepts; the bound counts from the verifier's first observation
of the tip and not from the moment at which its node received the block. A
clock that reads less than the largest reading that the verifier has used
refuses, and so does a header that is more than 600 seconds ahead of the
clock. An action whose profile
states no class has the stricter one. A verifier checks that the recent
block of a grant is on the active chain and that the issuance anchor is
confirmed above it by at most 432 blocks. The depth of a fact is the height
of the tip minus the height of its block, plus one.

Three numbers are provisional: the 600 seconds, the lag of one block and
the 432 blocks. The LIP names for each the measurement on a real host that
has to precede its freezing.

Nine codes with an order: `OBSERVATION_CHAIN`, `OBSERVATION_VOID`,
`NODE_UNHEALTHY`, `NODE_DISAGREEMENT`, `OBSERVATION_CLOCK`, `TIP_AGE`,
`RECENT_BLOCK`, `RECENT_BLOCK_WINDOW` and `CONFIRMATIONS`. The first six
stand before every rule of a grant, and none records a closure.

Vectors. `vectors/LIP-0022/observation-vectors.json` holds 97 vectors over
28 rules, at both sides of every boundary: the two cutoffs for both ages,
the bound on a header, the kept mark of the clock, the lag, the window of
the anchor, the half-open window of a grant in heights and the larger of
two minimum depths. The node vectors hold a node that is ahead and a node
on another branch, each beside a node that agrees. Ten vectors are
sequences of observations over time, among them a tip whose header is two
hours ahead and a tip with an ordinary header. They state tips, times and
heights and read no node. No node was run and no measurement was taken.

LIP-0008 sections 6 and 7 and LIP-0021 section 1 gain one pointer each.
O6.3 of LIP-0021 gains the definition of a step of a walk, the examination
of one output: a walk that ends with the last output that the bound allows
is complete. No vector of LIP-0021 changes.

## 0.1.39 — 2026-11-14

Adds Draft LIP-0021, the name ownership and history profile for Grant v4 on
Namecoin, with vectors. Every rule of it is the draft's proposal, and
neither owner has decided one. No rule of another text changes, and no v3
byte does.

What it answers. LIP-0008 section 3 binds a grant to the owner key of its
issuer's name and says that the exact key encoding and the script coverage
remain open. LIP-0014 section 7.1 writes a notary's owner pin in "the
encoding that LIP-0008 section 3 will fix", and LIP-0020 reads the evidence
output of a consent under an ownership profile that it calls open.

The profile (sections 1 to 6). A verifier reads its own node, which keeps a
transaction index, and nothing that a presenter supplies. The owner pin is
a compressed public key, 66 lowercase hexadecimal characters. A verifier
parses the octets of an output script itself: three exact prefixes, for an
update, a registration and a reservation, and two address scripts, the key
hash and the witness key hash, which both pay the hash of one public key.
A reading has three outcomes, controlled, another key and unsupported, and
an unsupported script is evidence of nothing. The pinned owner wrote a
value when the name input of its operation spends an output that the pin
controls and its signature ends with the hash type `01`. A name is live at height `H` when `H < h + D`. A
walk follows the name inputs back to a registration; a verifier may bound
it, and a walk that it cannot finish proves nothing.

The rules that use it (section 7). For the issuer rule and for a recipient
by name, where LIP-0008 names no code, the draft proposes
`ISSUER_NAME_CHANGED`, `ISSUER_SNAPSHOT`, `ISSUER_HISTORY_UNAVAILABLE`,
`RECIPIENT_NAME_NOT_HELD` and `RECIPIENT_NAME_UNAVAILABLE`, and the order in
which a verifier reports them: what the chain proved before what the
verifier could not read. For a notary's name, for the consent of a
recipient by name and for a change that the owner signed it says which
reading each existing rule takes, and it adds no code.

One proposal is stated and gates nothing: that the issuer rule also require
that the bound owner wrote the value in force, as J3.4 requires of a
notary's name. LIP-0008 lists that question as open, and the vectors hold
the rule in force.

Vectors. `vectors/LIP-0021/name-vectors.json` holds 140 vectors over 27
rules: pins, output scripts, the inputs of an operation, heights, and 56
histories for the four rules that walk or read a name. Each refused vector
names a valid neighbour, and five vectors with two findings test the order.
The vectors state octets and facts and read no chain. No node was run: the
statements about Namecoin come from the source of Namecoin Core at the tag
`nc28.0` and from the reference laboratory, and the LIP lists them.

LIP-0008 section 3, LIP-0014 section 7.1 and LIP-0020 section 7.3 gain one
pointer each.

## 0.1.38 — 2026-11-14

Corrects the order of the issuance check in Draft LIP-0020. No byte, no
code and no earlier vector changes.

Version 0.1.37 had a verifier take each part of a presentation through its
own pipeline and check the mode afterwards. For a recipient by name the
consent step needs the evidence outpoint, which the consent event does not
hold. A presentation without the outpoint therefore refused in that step
as `CONSENT_EVIDENCE`, while section 8 and a vector promised
`ISSUANCE_MODE`.

Rule W9.4 now states six steps: the signed grant; the inputs, which are
the mode of the grant and the presence of the evidence outpoint; the
issuer's assent; the consent event; the frame; the commitment. The inputs
stand before the consent event, and the missing outpoint refuses as
`ISSUANCE_MODE`. Rules W8.4 and W8.6 refer to that order.

The vectors gain a group for the whole check, with the grant given as
stated facts: 2 valid presentations, 7 refused ones and 5 with two defects
each, which test the order. The file has 219 vectors over 47 rules.

## 0.1.37 — 2026-11-14

Adds Draft LIP-0020, the wire registry for Grant v4, with vectors. It is
the first proposal of bytes for Grant v4. Two points of its consent rules
were decided on 2026-11-14 under Ivan Oparin's delegation; he may override
them, and the co-author's agreement is pending. Every other rule is the
draft's proposal, and neither owner has decided a byte. No v3 byte changes,
and neither does any rule or vector of profile `swarma-trust-contract/1` or
the reference checker.

The layer that every v4 object shares (sections 1 to 6). The canonical
bytes are the RFC 8785 serialization of one JSON object over a restricted
set of values: no `null`, no code point below U+0020, numbers only as
integers up to 2^53 - 1. A reader refuses unless its own serialization of
the parsed value equals the octets it received. An integer has one of two
forms, a JSON number or a decimal string with a stated bound, and the wrong
form refuses; amounts and cumulative counters take the string form. Every
payload states its `type`, the name of the object type and its version in
one string, and that string is also the tag of the typed digest, the tagged
hash of BIP-340. A signature is BIP-340 over the typed digest under strict
verification. The identifier of an object is the SHA-256 of its canonical
payload and leaves the signature out; the SHA-256 of the signed form is
its content address. The registry lists seven types. Five have an
identifier and a digest and no members: the grant, the invocation, the
receipt, the seal-key endorsement and a successor of the notary
attestation. No reader accepts a payload of those five, and the LIP names
what the members of each wait for.

Consent (section 7). The issuer signs a typed assent to the contract. The
recipient signs a Nostr event of kind 8181, as a browser signer can. The
two decided points: the state of a name at the issuance snapshot
authorises, and a state that held earlier or later is no substitute; and a
consent names its contract, its issuer and its recipient, is consumed by
one issuance, and is at most 72 hours old when the issuer starts that
issuance. The draft carries them so: the event has the tags `t`,
`genesis`, `contract` and `issuer`, and for a recipient by name a fifth,
`name`; the snapshot is the state at the grant's recent block; the issuer
records the output of the recipient's name that it read; and a verifier
establishes that this output was the name's current one at that block,
which takes a walk of the name's operations since issuance. A later change
of the channel key by the same owner leaves the consent valid. The issuer
records a consumed consent and refuses it for any other grant; a verifier
cannot see that from one issuance, which the LIP states as a limit. The
`created_at` of the event is never compared with a block height.

Issuance (section 8). The issuance preparation states the grant, the
issuer's assent and the recipient's consent, each with its signature, and
for a recipient by name the output that was read. Its typed digest is the
issuance commitment, carried in a LIP-0005 frame with action `0x01` and
payload version `0x02`; the pointer is the content address of the signed
grant. Payload version `0x01` keeps its v3 meaning.

Pipelines, codes and vectors (sections 9 and 10). A reader takes a signed
object, an unsigned payload, a Nostr event and an issuance through four
pipelines, selected by what the place expects, with one order of refusals
inside a document and inside the members. The layer has 27 new codes.
`vectors/LIP-0020/wire-vectors.json` holds 205 vectors over the 46 rules,
in seven stages. A refused vector holds one defect and names a valid
neighbour; vectors with several defects are marked and test the order.
They were computed by two implementations that share no code; no checker
for them is in this repository.

LIP-0008 section 8.1, LIP-0005 section 2 and LIP-0014 section 6.1 each
gain one sentence that names LIP-0020, and three rows of the index of open
questions point to it. No rule of those texts changes.

## 0.1.36 — 2026-11-14

Three points of LIP-0014 that 0.1.35 left open now have an answer. Both
owners agree on the first. Ivan Oparin decided the other two on 2026-11-14,
and the co-author's agreement on them is pending. No v3 byte changes, and
neither does any rule or vector of profile `swarma-trust-contract/1` or
the reference checker.

The text of a v4 child (section 3.4). In the first version of v4 a
re-delegation narrows only typed fields and appends no text. The co-author
answered so on 2026-11-14, and the owner who decided the other parts of J5
agreed on the same day, on the condition that the system can be built
without layers of text. Narrowing by text that a notary checks, possibly
with keys, stays in the plans for the next revision, and nothing of it is
defined. The draft reads the agreement as the inheritance of J5.1: a child
carries its parent's text unchanged. The v4 bytes are open.

An effect requested under a text (J5b, section 3.4). An executor refuses a
landing or a payment that is requested under a grant with a text. That is
the default. The owner's confirmation of one operation stays as an
exception, with its exact arguments (J5.9) and recorded as the owner's
decision. The exception is course (c), the confirmation of effects, and
course (b), the confirmation of every action, is not taken; its rule, its
case S5-4b and its clause in J5.9 are removed, and the table of courses
keeps its row. All of that is the owner's decision. What selects the
exception is open. The draft proposes that the executor's owner chooses
the exception for an executor; the proposal is no part of the decision,
and no rule, step or case depends on it. The open point on reviews now
says that the one operation an owner confirmed is the only landing or
payment under a grant with a text. LIP-0013 section 3.4 says the same of
its steps.

The key of a row's coin (J1, section 9.1). On v4 the coin of a row pays a
separate key, derived from the seed of the operator's signer in an account
of its own, as seal keys are derived (LIP-0008 section 11.1). Who funds
the coin, and the account and the path of the key, stay open. The key
registry and the key map carry the key. The open point on forks now says
what a second child after a reorganisation takes: the delegation key and
a spend of the coin, which the delegation key alone cannot make.

## 0.1.35 — 2026-11-14

Records the co-author's answer on one open point of LIP-0014 and decides
nothing. The point is what a v4 child does with its parent's scope text
(J5, section 3.4). The co-author answered on 2026-11-14: as a first
approximation, a re-delegation on v4 narrows only typed fields and appends
no text, and narrowing by text with a notary, possibly with keys, goes into
the plans for the next revision. The joint decision is not made; its state
is "owner confirmation pending". The owner who decided the other parts of
J5 leaned towards layers of text that a notary checks, and the answer
defers that lean and does not reject it. No rule, case, byte or code
changes, and LIP-0014 still holds no rule for the text of a v4 child. The
later revision is listed under the open questions of the LIP.

## 0.1.34 — 2026-11-14

Four additions record decisions that Ivan Oparin made on 2026-11-14. The
co-author's agreement on each is pending, and nothing of them is
implemented.

LIP-0019, retrieval by hash. A locator can name a blob store and a hash,
and nothing said how a reader gets the bytes. The draft proposes a delivery
profile and its loader: endpoints from the loader's own configuration and,
under a policy of its operator, from an unsigned hint; a fetch by SHA-256
with bounds on size and time and without a redirect to another host; and a
check that the bytes hash to what was asked, after which the object is
checked exactly like a presented one. A grant id addresses the canonical
signed grant alone; a presentation is not fetched but completed by the
reader, from the fetched signed grant and an issuance locator that it
checks as LIP-0004 section 4 does. A contract of LIP-0017 is fetched by
the hash of its stored bytes, and the reader recomputes its identifier.
Retrieval adds availability and no authority: a store can make a reader
refuse and cannot make it accept. The uses are audits, disputes, parent grants and
certificate sets. LIP-0005 points to the draft.

LIP-0008, section 11.2, the seal-key endorsement. Its members by meaning:
the issuer pin, network and genesis, the profile, the exact outpoint, the
seal public key, the exact script, the grant or preparation it belongs to,
and a BIP-340 signature by the grant key under a domain of its own. A
verifier checks, in this order: the script on its own node equals the
endorsed script; that script is the single-key script of the endorsed key;
the signature verifies under the pinned issuer's grant key; the grant
names the same outpoint; and only then does it classify a spend as the
issuer's. The bytes stay open.

LIP-0008, section 11.3. Before it signs a grant, the issuer's signer shows
that it can spend the seal: it signs the spending transaction, records it
in its journal and does not broadcast it. The recorded transaction can
also revoke the grant when the signer is down. Its fee is fixed when it is
signed, which the section names as a limit.

LIP-0008 also states the names of the parties. Grant v3 keeps its byte
names `landlord_name`, `landlord_sig` and `agent_name`; the prose and
Grant v4 name the roles: issuer, recipient and executor.

LIP-0017, section 8 and decision C9. A contract under which the platform
starts an agent carries the hash of the configuration manifest that the
parties agreed on, expressed only through Curator profiles, Curator skills
and the systems that the agent may use. The platform executes exactly that
manifest. The draft adds that the profile of such a contract requires the
hash, that a reader refuses a contract of that profile without it, and that
a launcher which cannot reproduce the hash starts nothing; a contract that
starts no agent carries none. LIP-0018 section 1 says the same for a
contract profile. For a rental the slot launcher composes the agent's
read-only runtime context from the pinned profile, the human terms of the
contract, the machine terms of the grant and any scope text. The reference
rental path gives a slot no contract text today.

## 0.1.33 — 2026-11-14

LIP-0015 and LIP-0016 record that Ivan Oparin accepted their direction as a
whole on 2026-11-14. The co-author's agreement is pending, no rule of
either is adopted, and both owners still decide them.

LIP-0015. The pin and the configuration statements have a first use that
needs nothing else of the LIP: signing the profiles and manifests of
Curator, each as a section with a subject of its own. Section 6 records
three directions for certificate statements. Of the two Matrix kinds,
`matrix-cross-signing` is preferred: one statement then covers each device
whose chain of signatures to the certified cross-signing key verifies. A
device that carries only its own signature is not covered. A key of another
transport, such as the OMEMO identity keys of an XMPP account or a key that
signs email, gets a kind of its own through a LIP. And a binding lets a
receiver check a sending device against a key that the operator of a name
certified, where it otherwise relies on the transport's server; it gives no
authority.

LIP-0018 gains a fourth list, for a certificate subject kind: the kind, the
members of the subject, what the key does in its own system, what a
receiver checks against it, and that revocation follows LIP-0015 unchanged.

LIP-0016. The draft answers the open questions of its first version; the
answers are proposals. The Git provider adds no format: a file holds the
exact bytes of the head or of one record, the list is the set of record
files, and a reader computes each id from the bytes and takes no evidence
from the repository's history. A head covers one issuer, and one anchor
transaction anchors one head; a head for several issuers and a batch of
heads are left to later proposals. Between a change of an issuer's grant
key and the first head under the new key a reader has no verified set:
every subject is unbound, and the reader does not fall back to the old
set. The vector set is described and not built. Open stay the key that
controls the output of a head and the way a reader learns where a store
is.

## 0.1.32 — 2026-11-14

Five further directions of Ivan Oparin of 2026-11-14 are recorded. The
co-author's agreement on each is pending.

LIP-0013, new section 3.7, instructions across owners. The grantee of a
grant from one owner to the other is an agent of the receiving owner. That
owner directs the agent over the owner channel, the agent signs the
envelope with its key through its key holder under the gate of section
3.6, and the executor admits it under section 3.4. A person's keys that
need presence are for rare acts: issuing a grant, and consenting to a
grant whose grantee is the person. A session key is named as a later
option. The section also states that a transport only carries: authority
comes from the signed envelope inside a message, on every transport.

Key map. The requirements on a key service describe a personal key
service for each person, on every platform the person uses, with a social
key under a policy for each application and an authority key that signs
only with the person present and every field shown. Decision K6: for
grants issued to Ivan Oparin a separate authority key is named in each
grant, the name keeps the social Nostr key for messages, and for the
interim the authority key lives in the macOS Keychain like the grant key;
the reading that puts an authority key into the name is rejected. The
scope of K2 is settled: permanent roles have names, a worker agent may
stay key-only, and an agent that becomes permanent keeps its key. The key
registry points to K6.

LIP-0008, section 1. Grant v3 is frozen after the first public
demonstration: no new feature and no new byte. Once Grant v4 is
qualified, new grants are issued on v4 only, and v3 remains for
verification alone. What becomes of a v3 grant that is still live then is
not decided.

## 0.1.31 — 2026-11-14

Holds Draft text for the eight gaps that version 0.1.24 recorded, labelled
J1 to J8, and records the decisions that Ivan Oparin made on them: J3, J6
and J8 on 2026-11-13, and J1, J2, J4, J5 and J7 on 2026-11-14. The
co-author's agreement on each is pending. One part of J5 stays a pending
owner decision. Nothing of it is adopted until both owners agree. The rules
in force are not rewritten: each decision stands in one subsection that
first says what holds until then, and the places it would change carry a
pointer. No gap is called closed for a property that its subsection lists as
open. No v3 byte changes, and neither does any rule or vector of profile
`swarma-trust-contract/1` or the reference checker.

The number 0.1.29 is not used. This revision was prepared under it and
landed after 0.1.30, so it takes the next number.

LIP-0014, section 9.1 (J1). The parent signs one row for each child, with
the executor, the grantee, the cap and the certifier. On v3 the limit is a
number of compartments, and one child object for each row stays open
there. On v4 each row also pins a coin that the issuance of its child must
spend, so that one child for each row holds on the active chain and not
across forks, which the decision accepts. Which key of the re-delegating
side the coin pays is open. The member of a row that names the performing
party is `executor`; the v3 grant and the contract keep `agent_name`. The
row ledger has a store contract in which continuity is proved against an
outside record that binds the committed history; the proof protocol is an
open deployment profile, and no executor qualifies for `spend` without it.

LIP-0014, section 10.1 (J2). One notary for each row, one succession of
seals for the row, an authenticated cause and three states with their
codes. On v3 D5 holds in a narrower form, and the subsection says so in so
many words. On v4 each row names a stop coin of its notary from the first
version, and its spend ends the row for every verifier whose node shows
it. A coarser form, one coin for each notary and parent, is recorded as a
future option.

LIP-0014, section 7.1 (J3). Pins, a signed checkpoint and a writer rule
for a notary's name. A notary's name that the funding wallet registered
needs one update by its owner before a parent may name it.

LIP-0014, section 11.1 (J4). Each parent names a delegation key of its
own, which signs children on v4 and nothing else, because the messaging
key never grants authority. The delegation signer signs without a person,
bounded by the rows, the notary and the two coins of each row. A key that
the seals of children pay is a profile option outside the first v4
version.

LIP-0014, section 3.4 (J5). On v3 a child carries its parent's scope text
unchanged. What a v4 child does with its parent's text is not decided, and
nothing of it is written. A text governs an agent's work and never a
service's effect, and money and landings go into a grant without a text. An
executor that cannot read refuses a grant with a text, and no executor
performs a landing or a payment automatically under one. Whether it refuses
such a request, as the Draft text does until then, or holds it for the
owner's one-time confirmation is a pending owner decision. Profile `/2`
gains no member; the ref, the exact revision and the payee are machine
members of the v4 action profile from its first version, and a path inside a
repository stays words. The table of gaps under Open questions gives way to
these subsections; every fact of its rows stands in their first paragraphs.

LIP-0008 section 5.2 (J6, accepted on 2026-11-13): an owner-signed change of
an issuer's name that a verifier validated, in its mempool or in a block,
closes the issuer's grants in that verifier's journal; the read follows
every pending name operation; an issuer funds every operation of its name
from coins that no hot service can spend. A verifier that saw the change and
one that starts later can differ, and the text says so. A new open question
asks whether the issuer rule should carry the writer rule that LIP-0014
drafts for a notary.

LIP-0013 section 3.6 (J7): the service that holds an agent's key binds each
run to its origin and signs only what its operator listed for that origin,
with a separate permission for consents; a grant that the operator removes
stays removed. By the decision the gate is a condition of enforcing mode,
it holds against an untrusted run at an honest key holder, the operator's
table is a file of the key holder's OS user with a version that only moves
forward, and for an agent's key the gate takes the place of presence. T10
points to the subsection, and T11 lists what the authority frame of
section 3.4 leaves open.

LIP-0011 section 7 (J8, accepted on 2026-11-13): the signed v4 invocation is
the request of a verdict, and an invocation inside an encrypted message
binds a salted hash of the content. A reader reports reference, attribution,
eligibility, admission, and time and delivery apart.

The key map carries the sentence that the decision adds to K2 and a row
for the delegation key (J4), the changed presence rule (J7) and a note for
a notary's name beside its registration flow (J3). The key registry points
to the sections that hold the rules of the v4 keys. LIP-0012, LIP-0010 and
LIP-0008 point to the texts that concern them.

## 0.1.30 — 2026-11-14

Two new drafts and one extension record decisions that Ivan Oparin made on
2026-11-14. The co-author's agreement on each is pending. They state
semantics without canonical bytes, and nothing of them is implemented.

LIP-0017, contracts. Until now a contract existed only as the hash that a
grant signs. The LIP makes it an object: one document that two or more
parties sign, with free text for people and members for machines. Its
identifier commits to a salt and to a salted hash of each clause, so that a
party can disclose single clauses. A contract is anchored as LIP-0005
action `0x07`, and two parties can show their assent on chain by spending
an output that needs both signatures. Every grant binds a contract, which
may be minimal, and a contract may exist without any grant. A grant's
window lies inside its contract's window; profile `swarma-trust-contract/1`
keeps equality, and no rule of LIP-0013 changes. A framework contract
covers several grants over time. A contract ends early only through a
machine rule that names who may declare the end. For v4 and for framework
contracts a contract can name a seal of its own: its script is the
termination clause (the issuer alone, either party, both together, or an
arbiter), every grant under the contract requires it unspent, and its
spend, with action `0x08` and the hash of the signed termination
statement, ends them all. Grant v3 does not change. A table of scenarios
shows rental, trust, services between companies, employment and an
agreement without a grant.

LIP-0018, an extension guide. It lists what a proposal has to state for a
contract profile, for a limit kind and for an action leaf name. For a
limit kind these are the identifier and resource, the unit and integer
scale, bounds and rounding, period and aggregation, reservation,
concurrency, uncertain outcomes, replay, denials, the contract mirror,
defaults, refusal codes, vectors with a checker, and the path of the LIP.
The guide assigns no identifier and no byte.

LIP-0008 section 2 records the decision that further limit kinds join
its list: external service cost, runtime and concurrency, rate, outbound
messages, repository writes, storage and egress, name operations, secret
releases and an owner-confirmation threshold; that coins carry a maximum
for one spend and for a period and name their asset and payment system;
and that an allowance of zero of any kind authorizes nothing. The kinds
are the decision. The one-line meaning beside each kind is the draft's
proposal, and a type profile binds it only if it adopts it.

LIP-0005 lists the actions `0x07` and `0x08` as proposals; the reference
parser accepts neither. The authority frame of LIP-0013 section 3.4 names
the framework contract of LIP-0017 as its fifth member. The key registry
gains entries for the keys of a contract seal and of an assent output.

## 0.1.28 — 2026-11-14

Three additions record decisions that Ivan Oparin made on 2026-11-14. The
co-author's agreement on each is pending, and no implementation is claimed.

LIP-0006, new section 7. Text always governs an agent's work and never a
service's effect. A service that performs an effect at a resource, such as a
payment, a landing or the release of a secret, decides from members that a
machine compares and refuses a grant whose terms carry a text. A service
that carries requests to an agent passes the text on unchanged, and the
agent applies it to its work. Money and landings are authorized by members
only, so a party that wants both a text and an effect issues two grants.
The cost is stated with the rule: a limit for which no profile has a
machine member binds no effect service, and whether an agent applied a text
is judged only afterwards. The former section 7, on related drafts, is now
section 8. LIP-0014 section 3.3 points to the rule and says that the LIP
does not yet apply it to profile `/2`.

LIP-0013, section 3.4, the authority frame. The admission gate is the
program at an executor that runs the checks, and the terms of the LIP now
name it. It hands each admitted peer instruction to the agent inside a
read-only frame with the principal, the grant id, the contract terms, the
scope text of a `/2` contract and the hash of a framework agreement where
one exists. The frame is built from verified objects only and is outside the
agent's write authority. An agent's standing instructions carry one rule
about frames and no contract. On v3 a grant names one agent; on v4 a grant
can name several executors with signed partitions, and what a frame carries
there is fixed with the v4 bytes. Before a frame carries a scope text the
gate checks the octets of that text against the hash in the contract, for a
root as for a child, and refuses as `TEXT_UNAVAILABLE` otherwise; the steps
of LIP-0014 make that check for a child only. Whether a frame is signed,
whether it leaves the executor, its encoding, its channel and the proof that
an agent cannot write it are open, and the text marks which rules are the
decision and which are the draft's own. No other step or code changes, and
no vector.

A new document, the key registry (`KEY-REGISTRY.md`). It lists every key the specification names, in 29 entries. Each entry states the owner, the place
where the key is published, the holder, the complete list of what it signs,
a danger level from critical to low, the effect of a leak, the recovery and
the source. Its rules: one entry for every key; the list of uses is closed,
and a use that a part defines and an entry omits is a defect of the entry; a
messaging key grants no authority; an entry has the status of the part that
defines its key. A level belongs to a key with all its uses: a key that can
use authority under any grant is high, and a key that can only end authority
or forge a record without authority is medium. Five entries follow decisions
of the same day: the authority key of a person who receives grants and, on
v4, the delegation key, the coin key of a row, the optional child-seal key
and the stop key of a row. The entry of the agent's Nostr key records that a
gate at the key holder takes the place of presence. LIP-0014, LIP-0013 and
the key map take those rules in later revisions and state the earlier text
until then. The danger levels are the draft's proposal. The release order in
`RELEASE.md` and the specification set in the README include the new
document.

## 0.1.27 — 2026-11-13

LIP-0010, section 7: a note that is not normative, recorded at Ivan Oparin's
direction. The pair of `id/<label>` and `d/<label>` is a convention outside
Namecoin consensus and misleads: a person reads the two as one identity, and
the chain holds two unrelated names. An additional naming convention with a
single level of registration is under consideration, and the authors' own
parsers would handle only that level. Nothing of that convention is defined.
The protocol rule and the deployment rule of section 7 are unchanged, and
the list of open questions names the point.

## 0.1.26 — 2026-11-13

LIP-0008, the conformance row for an unconfirmed parent under profile W. The
row gave one reason why a funding transaction with a legacy or a wrapped
input refuses: a third party could change its txid. That reason holds for a
legacy input. A wrapped witness input is signed in the witness, which BIP141
keeps out of the txid, and BIP141 requires its scriptSig to be exactly the
push of the redeem script. It refuses because profile W admits native
P2WPKH inputs only (section 1.1). The row now gives each reason. The valid
control and both refusals are unchanged.

## 0.1.25 — 2026-11-13

Ten rows of the action tables render whole again. Each row gave its payload
as one code span with two bars inside, such as
`version(1) || commitment(32) || locator`. A Markdown table splits a row at
every unescaped bar, also inside a code span, so the rendered row ended
after `version(1)` and lost the commitment and the locator. The operands are
now separate code spans with escaped bars between them. The rows are the six
actions of LIP-0005, action `0x03` in LIP-0011, actions `0x04` and `0x05` in
LIP-0014 and action `0x06` in LIP-0016. No byte, name or rule changes.

## 0.1.24 — 2026-11-13

Records eight gaps that two independent reviews of the design found. Each is
an open question with the case that shows it. The fixes named are
candidates, proposals that the owners decide; no mechanism is chosen, and no
rule, format or check changes.

LIP-0014, five gaps under "Gaps found in review". Each notary certifies
against its own record, so two children that carry one ordinal and are
certified by different notaries both pass, and together they can exceed the
pool or the number of children; the case needs a child signer that uses an
ordinal twice, which on v4 is the delegator itself. A withdrawal for cause
reaches only the parties that observed its frame: another named notary can
certify the child again, and a verifier that starts later admits it. The
notary is bound by name only, so a transfer or a new registration of that
name passes on the right to certify. On v4 an agent signs a child with its
Nostr key, the only key its name carries, which the host's gateway holds.
Under the current rules for a parent issued by name, a child signed with a
key that the name no longer lists refuses at use, so a change of that key
stops the agent's children; whether that rule stays, and whether the agent
gets a key of its own, is open. No admission step compares an instruction
with a scope text. The Motivation, sections 3.3, 7, 8.1, 9 and 10, the
security section and one conformance row implied that these cases were
covered and now state the limit; the table of section 11 names the rule in
force and the open point. LIP-0012 points to the three gaps that concern
the notary.

LIP-0008: replacing a leaked grant key takes effect only once the update is
confirmed and is undone by a reorganisation, while a seal spend closes a
grant durably from the mempool; for a grant that the thief signs the owner
has no seal to spend. The security section says so. LIP-0013, open question
T10: a grant is issued to a key, and every run of the agent that holds the
key can act under it, so an agent that works for two parties can carry one
party's instruction into an action under the other's grant. LIP-0011: under
NIP-17 and NIP-59 the sender signs the encrypted seal and not the message,
so a disclosed message does not by itself show its sender; the sentence that
said it does is corrected.

Conformance plans: LIP-0014 lists two cases that are admitted today and are
planned as negative cases of a v4 vector set. LIP-0008 adds two cases for a
permitted unconfirmed parent: a legacy input of its own, and a legacy input
in a further unconfirmed transaction that funds it. Both refuse.

Key map, K5: the interim grant key is an item of the data protection
keychain. Version 0.1.23 also named the login keychain; that keychain is
file-based, controls access with access control lists and cannot require
Touch ID for one item, so it does not give presence per signature. The
owner's decision is unchanged.

## 0.1.23 — 2026-11-12

The key map records Ivan Oparin's decision of 2026-11-12 on the interim
custody of the landlord grant key (K5). Until the keyvault's grant-signing
purpose is qualified, for which no date is set, the key on a Mac is a
software secp256k1 key stored as a generic-password item of the macOS
Keychain, in the login or data-protection keychain. Every signature needs
Touch ID, the signer shows every field of what it signs before the prompt,
and the key is not exported. It is replaced by a new item and an update of
`swarma.landlord.grant` by the name-owner key. The keyvault's BIP-85 path at `m/83696968'/2'/7'`, which 0.1.21 and
0.1.22 gave as where the grant key comes from, is now stated as the later
target. The proposed key layout lists both custodies. No tool that
implements the interim custody is released.

One sentence of LIP-0013 contradicted the owner's decision of 2026-11-12 on
the order of work: it named v4 as the target for the public demonstration.
That demonstration runs on the implemented v3 rental profile, and v4
follows it.

## 0.1.22 — 2026-11-12

Adds two Draft proposals in which nothing is decided; both owners decide
them. LIP-0015, Trust-root pin and typed statements, proposes the trust
anchor that the owners' decision K4 of 2026-11-12 waits for: a pin written
once at installation where the agent's OS user cannot write, naming the root
name with its registration, owner script and grant key; resolution of that
name on the loader's own node at every load; a separate signing domain for
every kind of object the grant key signs; configuration statements with a
sequence number against rollback; a root rotation statement; and certificate
statements that bind messaging, commit-signing and release keys to a name
without giving authority. LIP-0016, Certificate store, proposes where such
statements are published: signed records, a signed head over the complete
set, an anchor as LIP-0005 action `0x06` whose transaction spends the
previous head's output, and providers trusted for availability only, so that
a dropped record and a withheld newer head are both detected.

The key map gains two proposals: a key layout with the name-owner key on a
seed of its own, a hardened path per purpose and the grant key at the
keyvault's fixed BIP-85 path, and a flow for
registering an agent's identity in which the gateway generates the agent's
key and the funding wallet registers the name to the operator's owner
address. LIP-0010 section 8 gains a proposed plan for the 520 bytes: a name
carries only keys a reader must resolve on chain, and other bindings go to
the certificate store. An organization identity and release statements for
binaries are recorded as sketches in LIP-0015 and as open questions. LIP-0005
lists action `0x06` as proposed. Nothing is implemented.

## 0.1.21 — 2026-11-12

The key map records four owners' decisions of 2026-11-12. A principal has
three keys: the name-owner key, the Nostr key and the grant key, with no
administrative key for now. An agent has its own `id/` name; its operator
holds the owner key and the agent controls only its Nostr key. Only an owner
creates an identity. Sections of an agent host's configuration are not
signed until a trust anchor exists.

The key map also restates four Grant v3 rules, without adding one. A name is
written only in the exact LIP-0004 value shapes until every verifier runs a
LIP-0010 reader: one additional member makes the value unreadable and every
v3 grant under the name refuses, without closure, until the value is
restored. A table gives the effect of each name change on v3 and on v4
grants: v3 binds no owner key, so a transfer closes nothing there, and a
change of the grant key ends every grant signed by the old key. No agent
holds a grant key on v3. The landlord pointer is a name on v3. A second
table lists where each key is published before and after LIP-0010 readers.

Three requirements on a key service follow from the grant key's formats: a
grant-key purpose with BIP-340 and, on v3, an ECDSA seal spend; presence per
signature; and typed display with the hash computed by the service. The
keyvault interface at `swarma-keyvault` `662623f9` prepares the grant root
by BIP-85 at `m/83696968'/2'/7'` and does not sign with it yet. A grant key
is replaced by a new recovery group.
LIP-0010 section 6 states the v3 cost of rewriting a name before its readers
are upgraded.

## 0.1.20 — 2026-11-12

Adds Draft LIP-0014, Notary-certified re-delegation, and records the owners'
decisions of 2026-11-12 as D1 to D12. Every child grant is admitted only
with a valid notary attestation, whatever its scope; a root grant with a
right of re-delegation names its notaries and needs none. The parent's signed
right of re-delegation names one to four notaries by `id/` name, and each
notary publishes its attestation key in its own name; one attestation is
enough. Within one owner the notary is the issuer's, and across owners it is
an agreed third party. A withdrawal is durable, and the same child may be
certified again after a plain withdrawal only. Children draw on a separate
signed pool; depth stays at two links; one LIP-0005 frame anchors each
attestation. Staging: after the first proof of LIP-0013, in shadow mode
first, with a separate approval of enforcing mode for children by each
owner; in Goal 1 `instruct`, `review` and `land` are delegable and `spend`
is not.

The draft proposes, without deciding them: the seven members of the right of
re-delegation; contract profile `swarma-trust-contract/2`, which adds a scope
text hash, the parent's grant id, an ordinal and the right to profile `/1`;
the kind-8186 delegation request by which the parent's grantee asks the
landlord's signer for a child on v3; the object
`swarma-notary-attestation/1` with its signing domain; the anchor as action
`0x04` and a withdrawal for cause as action `0x05`; the order of an
executor's checks, in which every mechanical comparison precedes the
attestation; and the refusal codes, with separate codes for a notary that is
the delegator, the delegatee or an executor. No v3 byte changes.

Follows the decision in other drafts. LIP-0008 section 12.6 records it and
marks three of its five proposals as settled. LIP-0012 gains the directions
N5 to N10 and a section on designation and independence, and closes its
open points on the anchor, on naming a notary and on withdrawal. LIP-0010
gains section 9, a Draft amendment with a third `swarma` shape for a
notary's attestation key. LIP-0005 lists actions `0x04` and `0x05` as
proposed. LIP-0006 no longer calls agent-issued child grants an open
decision. Nothing is implemented.

## 0.1.19 — 2026-11-12

Adds Draft LIP-0013, the trust contract profile `swarma-trust-contract/1` and
the kind-8185 instruction envelope for Grant v3, for Goal 1 as agreed by both
co-leads on 2026-11-12. The profile defines only the preimage of the v3
`contract_sha256`: canonical compact JSON in a fixed field order; the actions
`instruct`, `land`, `review` and `spend`, of which `land` implies the v3 scope
`repository.push` and `spend` implies `pay` with a budget equal to
`spend_budget`; the validity rules with their refusal codes; and the consent
tags, with `t` unchanged, `booking` over the contract bytes and `privacy` over
`swarma-trust-privacy-v1`. No v3 byte, signing domain or `rental.Check` rule
changes. The envelope section fixes the exact tags, the body hash, the nonce
journal, the time window and the admission check order. Kind 8185 is unused
in chain-lab and here; it remains a draft allocation, an open question.

Admission needs enforcing mode. Shadow mode is the default: the executor
reports its verification results, every peer message stays data and only
the owner directs. Enforcing mode follows only after the first proof has
passed and both owners have approved it; a switch is not retroactive, and
scenarios cover no proof, one approval, both approvals and an envelope
verified while still in shadow mode. The `review` action authorizes who may
review and does not change a repository's reviewer policy. Refusal codes
follow one layer: a sign on an integer and a non-ASCII character or a control
escape in any string, the note included, refuse as `CONTRACT_ENCODING` before
any value rule.

Adds draft vectors in `vectors/LIP-0013/` (4 valid and 32 invalid contracts,
15 bindings, 26 envelopes signed with BIP-340 published test keys) and the
reference checker `tools/trustcheck`. Nothing is implemented in a product.

## 0.1.18 — 2026-11-11

Adds Draft LIP-0012, Notary, by decisions of Ivan Oparin of 2026-11-11; the
co-author's agreement is pending. A notary is an additional link that
certifies a grant and can revoke it; for a child grant it certifies that the
child does not exceed its parent, including conditions written in words; the
performer is an agent or a person. The draft proposes the mechanism on the
basis of the laboratory comparison: a separate signed attestation with the
notary's own seal, a signed requirement in a grant or in a right of
re-delegation that names the notary and the kind of statement demanded, one
added admission step that also checks that statement and its binding to the
contracts of the child and the parent, and revocation by spending the
notary's seal. The grant's own seal is untouched by that. Durability of the
refusal, certification by another notary after a withdrawal, the anchor and
all bytes are open. LIP-0008 section 12.6 now points to this LIP. Nothing is
implemented in a grant profile.

## 0.1.17 — 2026-11-11

Amends Draft LIP-0008 by a decision of Ivan Oparin of 2026-11-11, with which
Alexey Grigorev concurred the same day. Nothing is implemented.

New section 12.6, Re-delegation: child grants are part of the protocol; an
agent issues one only when it holds a grant with the right of re-delegation,
which is the issue capability of section 12.2; a child is never broader than
its parent. Countable conditions are checked mechanically, as section 12.2
already requires. Scope expressed in words is not checked by this LIP and
needs a separate mechanism; the notary is the party that performs that
check and has no specification yet. Whether a notary attestation is
mandatory for every child with textual scope stays a proposal.
Re-delegation and issuance by the operator's signer are compared side by
side. Five proposals for the "not broader" check are listed beside today's
rules and are not decided. The section also states which key signs a child
and leaves open whether a re-delegating agent needs a grant key of its own.

Staging (R6): issuance by the operator's signer is implemented first;
re-delegation follows once a mechanism exists that checks that a child is not
broader than its parent. The five proposals are the candidates.

The section 12 preamble no longer calls agent-issued child grants a separate
undecided question. No rule of sections 12.1 to 12.5 changes; the depth
stays at two links.

## 0.1.16 — 2026-11-11

Records six decisions of Ivan Oparin of 2026-11-11 on points that the drafts
listed as open; the co-author's agreement is pending. No rule changes: each
text already described the decided option.

LIP-0010: D5, a duplicate or a fold alias of `nostr` at the top level refuses
the whole value; D6, the pair rule covers every `id/` name that has a `d/`
counterpart, agents included. The two matching open questions are removed.

LIP-0008: the rule that a window may not open below the committed recent
block (section 7.1 rule 3) is decided policy; the invocation's `iat`/`exp`
stay in clock time; the single-key script of the revocable-only seal per
construction profile and non-hardened seal indices by default, with the
extended public key as an operator secret, are decided (section 11.1). The
matching open questions and index rows are updated. The universal seal-script
restriction withdrawn in 0.1.13 stays withdrawn; the single-use seal's output
profile stays open.

## 0.1.15 — 2026-11-11

Adds Draft LIP-0011, Termination for violation, by decisions of Ivan Oparin
of 2026-11-11; the co-author's agreement is pending. The contract carries the
hash of the moderation rules and names who applies them, a model or a person.
Each violation is a signed verdict record with the request hash, the violated
rule and the hash of the moderator's response; verdicts of one grant form a
chain. The transaction that spends the seal for a violation carries a
72-byte LIP-0005 frame with the new action `0x03`: a termination commitment
over `grant_id`, `contract_sha256` and `verdict_id`, and a blob-store pointer
to the verdict. Closure does not depend on the reference; a refund is a
contract term. An independent reader authenticates the grant and requires
the carrying transaction to spend that grant's seal under the issuer's
authorization, so a frame copied into another transaction is not evidence.
The evidence is verified, invalid, absent or not established; an unfetched
record is not established and is never reported as a termination without
cause. The four owner directions are listed apart from the draft's own
proposals. LIP-0005 lists the action as proposed and not accepted by the
reference parser. Nothing is implemented; no canonical bytes for the records;
no change to v3, wallet-v1 or historical v0.1.

## 0.1.14 — 2026-11-11

Amends Draft LIP-0008 by three decisions of Ivan Oparin of 2026-11-11; the
co-author's agreement is pending.

Issuer name (section 3 rewritten; section 4 step 1 aligned): the grant binds
the issuer name's registration and owner key instead of its exact current
output. It lives while the name's updates change neither the owner nor the
`swarma` member. The verifier walks the name's history back to the bound
registration through the node's transaction index; an owner or `swarma`
change since the committed recent block refuses the grant for every verifier
of that chain without local memory. The verdict is relative to the active
chain and is not journalled: a change orphaned by a reorganisation no longer
refuses, for a fresh and an existing verifier alike, while a seal spend seen
in the mempool stays a durable closure. Renewal, a `nostr` update and owner-member updates
close nothing. The earlier exact-output rule moves to Alternatives. The start
point of the constrained stretch (the committed block) is this draft's
choice and is listed as open.

Term and period (new section 2.1): one grant per hire for the whole term in
block heights, about 13,000 blocks for three months; early end by seal
spend; an hour is a period of a limit and of payment, never a grant window.

Payment after a reorganisation (new section 2.2): a displaced payment that
stays valid is awaited for `N` blocks and nothing is revoked; the same coins
spent by a different transaction revoke. `N` and the still-unconfirmed case
are open. The reference booking service implements the earlier rule.

Conformance plan rows, open questions, key map, README and index follow. No
bytes, fixtures or implementation; v3, wallet-v1 and historical v0.1 are
unchanged.

## 0.1.13 — 2026-11-10

Amends Draft LIP-0008 in three places, following Ivan Oparin's decisions of
2026-11-10; the co-author's agreement is pending.

Recipient (new section 3.1): a v4 grant names its recipient by key or by name,
never both. A grant by key carries no recipient name; v3's unresolved
`grantee_name` has no v4 counterpart. A grant by name carries the name and its
owner key and no request key; the request key is read at admission from the
channel member of the name's current value, which is `nostr.names._` or the
key string for the Nostr channel (LIP-0010).

Validity (new section 7.1, section 12.5 aligned): the signed window is
`not_before_height` and `not_after_height`, half-open, compared with the height
of the verifier's validated tip. The window may not open below the committed
recent block. Contracts show approximate dates for people; a date is never an
admission input. The invocation keeps `iat`/`exp` in clock time. States the
variance from the section 6 sample and the interplay with the 60/90-minute
freshness cutoffs.

Seal keys (new section 11.1): BIP-32 derivation in an account that holds only
seal keys, for the revocable-only seal on Namecoin:
`m/84'/7'/<seal-account>'/0/<i>` in profile W and
`m/44'/7'/<seal-account>'/0/<i>` in profile L. The single-use seal keeps its
two distinct branches and its output profile stays open. The signer holds the
extended private key; a watch-only node may hold the extended public key.
States the non-hardened-index weakness, its blast radius and the hardened
alternative. The verifier checks the typed endorsement and needs no path.

The admission outline of section 4 authenticates the request by the signed
recipient mode. Adds six paired conformance-plan rows and updates the open questions and the
key map. No bytes, fixtures, implementation or normative adoption; v3,
wallet-v1 and historical v0.1 are unchanged.

## 0.1.12 — 2026-11-10

Adds Draft LIP-0010, Name value. `swarma` is the only member of a name value
that Link defines: a reader ignores the owner's other top-level members and
refuses only a duplicate or a fold alias of `swarma` or `nostr`; parsing inside
`swarma` stays strict. The agent key is written once, in `nostr` in the NIP-05
shape, and `swarma.agent` keeps only the landlord pointer. A reader accepts the
key string and the NIP-05 object and derives the same key for `_`; a `nostr`
member it does not understand removes the key and never the authority. `d/`
stays discovery only; the deployment rule registers `d/<label>` with
`id/<label>` because the two names are unrelated on chain. Recomputes every
example against the 520-byte limit. Records Ivan Oparin's four decisions of
2026-11-10; the co-author's agreement is pending. No implementation, normative
adoption or change to LIP-0004 bytes or historical v0.1 evidence.

## 0.1.11 — 2026-11-10

Adds Draft LIP-0009, Replaceable services: compatible type interfaces, portable
data and accounting evidence, exclusive cut-over with replacement executor-bound
grants, Namecoin discovery, bounded prepaid liability and a Blossom-backed
`store.blob` first profile. Records Ivan Oparin's acceptance of the five RS1
design choices on 2026-11-10. Rebind, exact wire/export/accounting/payment
profiles and qualification remain separate; no existing native NMC/BTC/LTC BUD
or automatic budget/credit migration is claimed. This is specification/book
work, not an M5 or first-demo implementation requirement. No historical v0.1,
wallet-v1/v3 or existing v4 draft bytes change; no implementation is added.

Adds decision 0003 as v0.1 errata: a route-health precheck cannot suppress a
spent/unknown/failed seal-state result or its durable refuse-and-close rule.
Route-only failure alone creates no closure; the historical protocol body,
evidence and documented failed-write/crash limitation remain unchanged. This
clarifies §1.4 under existing §4 and decision 0002, without new runtime evidence.

## 0.1.10 — 2026-11-10

Adds pre-freeze Swarma requirements to Draft LIP-0008: separate signed
invocations; signed subject, command, arguments, ordered proof IDs, nonce,
times and concrete executor; explicit issuance-capability paths of at most
two authority links, fixed parent binding, at-use attenuation and per-ancestor
budget accounting. Each grant keeps its complete action set under one seal.

Aligns LIP-0007's lowercase slash-command naming and reserved `swarma/`
namespace. Requires signed but non-authoritative metadata, signed type/version
consistent with application hash domains, canonical object IDs and strict
BIP-340 signatures without assuming unique signatures per message. Defines
half-open time/intersection checks and receiver-recomputed proof bundles;
reserves a future `policy` kind without syntax or an evaluator.
Corrects LIP-0007's wallet-v1 action listing to wire `spend`, consistent with
LIP-0006; `pay` retains its grant-scope/executor meaning.

Adds paired conformance-plan cases for the new rules. UCAN is provenance only,
with no new dependency or compatibility claim. General agent sub-delegation
retains its separate both-owner gate. Exact wire/proof/accounting profiles,
canonical fixtures and the post-freeze spike remain open; no implementation,
runtime result, normative adoption or historical v0.1/v3/wallet-v1 change.

## 0.1.9 — 2026-11-10

Records owner acceptance on 2026-11-10 of the proposed Grant v4 change: replace
the 30-minute
stop with risk cutoffs of 60 minutes for money or irreversible actions and
90 minutes for other privileged actions, plus a node-health check requiring
at least two independent nodes to agree on the tip. This is decided design;
implementation follows in GV4. The reported basis remains 70.7 min/day beyond
the 30-minute cutoff over 137.2 days on one node, not service availability or
a future bound. Historical normative v0.1 and its 30-minute STOP stay unchanged.

## 0.1.8 — 2026-11-10

Adds Draft LIP-0007 for service types/actions and typed name self-declaration,
and Draft LIP-0008 for Grant v4: directly signed rental limits, mirrored
contract terms, operator-wide ceilings and name recipients pinned to current
output ownership before channel-key checks. Includes v3 compatibility and a
semantic conformance outline; exact wire bytes, ownership proofs and accounting
profiles remain open. Binds issuer closure to the exact name output, including
issuer renewal. Grantee names bind their owner key, permitting same-owner
renewal/channel rotation and checking current listed channel keys. General
agent sub-delegation stays a separate open both-owner decision. Scopes budgets/
single use to concrete executors with shared replica journals.
Records proposed 60/90-minute risk cutoffs alongside node health and corrects
LIP-0003's seal-time inference as an acceptance rule, with a recent-block
commitment proposed for v4. Records chain-pin-selected W/L construction:
W uses native P2WPKH/SIGHASH_ALL with explicit unconfirmed linkage/payment
dependencies; L references confirmed outputs and builds the anchor after seal
confirmation. Both keep the same grant checks and fail closed on changed
parents; current P2PKH funding alone qualifies neither construction. No implementation claim, normative adoption or historical
conformance change.

Second design review adds registration-instance pins across grant, agent pointer
and verifier; typed signing from validated full objects; durable validated
issuer-branch mempool closure; confirmation minima; dependent T/L/A issuance and
profile-specific timing; topology/trust boundaries and per-seal keys. Plans JCS exact
unit schemas, canonical/signature/error/state vectors, runner and independent
Swift verification. Static signing audit found both issuer paths recompute authenticated contract
hashes, with no demonstrated oracle. Matched role/version migration and
wire/profile decisions remain open; historical v0.1 is frozen, including its documented false closures.

The immutable-config decision assigns configuration to the administrator, with
service-group read-only access (file `0640`, directory `0750`), a pre-start
manifest hash check and new reviewed packages for ceiling changes. This is
accepted design without an implementation or host-qualification claim.

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
