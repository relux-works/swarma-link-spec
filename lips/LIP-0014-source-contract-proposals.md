# LIP-0014 companion: proposals for the unresolved integration inputs

- **Status:** PROPOSED integration choices. No choice takes effect by this
  file's own word.
  It changes no existing rule, wire member, vector or implementation.
- **Date:** 2026-11-17
- **Source baseline:** version 0.1.57, commit
  `819433846febb9404c11a5fcd1ba124770f7910b`.
- **Scope:** identity, contract/profile, first-refusal and ordinal inputs
  of the child issuer and its consumer, with their distinct decision states.

This companion puts the integration choices in one place for agreement. It
does not treat a recommendation, a release, an implementation's behaviour or
two readers agreeing as an owner's decision. The existing statements of
status in LIP-0014 sections 8.4 to 8.7, LIP-0017 and LIP-0026 section 8 keep
their meaning. A decision on one row below does not accept another row.

The open Source-contract clauses are H1, T1, the action-profile mapping
and O1 to O8. For the state of the R8.3 count order, see LIP-0026 section 8.
The remaining LIP-0026 proposal Q2 remains proposed. Invocation definitions
belong to O2/O3; the contract's issuing-party assent belongs to T1 and the
profile. Actual custody, implementation, installation, native qualification
and conformance remain separate requirements after textual agreement.

## 1. Input and decision register

| Clause | Existing source | Status in this proposal | What closes the clause |
| --- | --- | --- | --- |
| H1 | The identity-latch contract of the host and launcher; J4.4 and J7 require actual trusted caller/run binding | PROPOSED | Accepted identity input, custody and transition contract from its sources; no guessed home path or process selector |
| T1 | LIP-0014 F6/T1/O4; LIP-0017 sections 1, 2 and 5 | PROPOSED | One accepted v4 contract profile, including exact identifier preimages, validation and term-mirror rules, codes and issuing-party assent |
| Action profile | LIP-0020 W11.4/W11.14 and the action and limit registries; LIP-0018 | PROPOSED | Accepted concrete action/kind definitions and mapping to the host contracts; no effect authority from an empty registry |
| O1 | LIP-0014 F21 and F7 part 7.6; seal and issuance profiles | PROPOSED | Acceptance of the proposed order across the three blocs, preserving their existing internal orders |
| O2 | LIP-0014 A1; LIP-0020 invocation registry | PROPOSED | Invocation specification accepts the narrow authentication refusal and its exact place |
| O3 | LIP-0014 E0 to E3; LIP-0020 invocation registry | PROPOSED | Invocation specification accepts the codes and order below, together with actual invocation members |
| O4 | LIP-0014 F6(b)/(c) and T1 | PROPOSED | The same accepted contract profile as T1 fixes identifier, profile-validity and term-mirror checks |
| O5 | LIP-0014 F7 part 7.4, F20(a), J4.4; LIP-0025 | PROPOSED | Closure-journal source accepts the separate failures, recovery residue and continuity requirements |
| O6 | LIP-0014 F21 and F7 part 7.6; LIP-0008 SB3 | PROPOSED | Acceptance of validated-spend classification relative to the two other blocs, as part of O1 |
| O7 | LIP-0014 F13(b)/T10; LIP-0020 W11.10; LIP-0026 proposal Q1 | PROPOSED | Explicit decision on whole-parent admission, without silently changing the count bounds |
| O8 | LIP-0014 F3 at ISSUE and I3; LIP-0022 B3.5/B3.6 | PROPOSED | Freshness source or owning decision assigns child signing to the proposed class |
| R8 count order | LIP-0026 R8.3 and section 8; LIP-0020 W11.6 | See LIP-0026 section 8 for its state | The remaining LIP-0026 proposal Q2 is separate |

The register describes Source agreement, not a claim that the machine
interfaces or complete signed conformance vectors already exist. Matching
later accepted source text replaces only the corresponding proposal in one
revision, with its decision and exact source revision cited. Until then the
existing open-clause behaviour continues, including the inability to finish
F6 without the contract profile. No proposal here enables a private call.

### 1.1 Carried baseline and source pointers

The following are carried from the baseline, rather than proposed again:

- **N1, the Repeat cross-references:** LIP-0014 sections 8.4 and 11.1
  already identify J4.4 (c) and event 12 beside step 6. J4.4 keeps its
  words; the checks named by step 6 govern that Repeat. This companion
  proposes no alternative reading of those cross-references.
- **N2, the child's own confirmed anchor at Repeat:** the new sentences
  in sections 8.5 and 11.1 already require `ROW_COIN_REQUIRED`, a held
  place and the operational audit/notice of event 39 when that anchor
  spends the row coin between the two checks. The signer is not called
  and no signature of this ledger exists. S4-30b, with S4-11, S4-30 and
  S4-30a, states the control and neighbouring cases. Their audit limits
  and behavioural qualification requirements remain those of the source.
- **The entry-kind list:** section 11.1 now carries J4.4 (g)'s list
  unchanged. No new kind or replacement row-ledger schema is proposed
  here; O5 still concerns the separate grant-closure journal.
- **Long-lived working-agent names:** the [key map](../KEY-MAP.md)
  already requires their own `id/` names, like permanent roles. A
  one-task executor named by key may remain key-only. This does not
  settle H1's local home latch or the representation of a message-key
  pin in the name value.

Those version 0.1.56 changes closed no complete row of the register. Version
0.1.56 also records two non-normative proposals in the
[unresolved questions](../UNRESOLVED_QUESTIONS.md): assent using the
delegator's existing signature on an equal parent/child contract, and a
message-key pin in the agent's name value. Neither is an accepted T1 or
identity interface. For the state of the R8.3 count order, see LIP-0026
section 8. The remaining LIP-0026 proposal Q2 and the other register rows
remain proposed. Landed text and proposed choices retain their distinct
statuses; neither supplies implementation or conformance evidence.

## 2. Identity and contract-profile inputs — PROPOSED

### 2.1 Exact counterpart texts and unresolved joins

The cross-specification inputs read for this proposal are:

| Input | Exact public source | Scope and actual status |
| --- | --- | --- |
| `station/1` | [curator-spec, protocol/station.md at 7e280bef](https://github.com/relux-works/curator-spec/blob/7e280bef3dbd6a4d6ec8b6931dde8a5176315662/protocol/station.md) | Landed specification text; its header remains unreleased draft, with no implementation or qualified runtime claim. Section 1 defines lifecycle only. SR1/SR6 make the dispatcher the single writer of the authoritative station record and its session journal. Section 9.2's name latch is explicitly PROPOSED and awaits custody confirmation and owning admission. |
| Station runs | [curator-spec, protocol/station-runs.md at the same commit](https://github.com/relux-works/curator-spec/blob/7e280bef3dbd6a4d6ec8b6931dde8a5176315662/protocol/station-runs.md) | Explicitly PROPOSED/non-normative. Instruction delivery and runs inside a station are outside station/1 v1. The existence of station/1 therefore does not establish the trusted RUN/origin evidence J4.4 needs. |
| `host-registration/1` | [swarma-dispatcher, spec/host-registration.md at db6514e7](https://github.com/relux-works/swarma-dispatcher/blob/db6514e710e1fe89098352d6f034b068edbecf41/spec/host-registration.md) | Landed dispatcher-side draft specification for one Host: protected static registration, local peer pins, two epochs and fencing. It enables no implementation and remains behind its publication/activation gate. Host-side rules and unresolved station joins retain the status given in section 11. |
| Action profile | [swarma-link-spec PR #58, ceff0e1c](https://github.com/relux-works/swarma-link-spec/blob/ceff0e1c52281702d062beb6a5789a1a37beb5e6/lips/LIP-0030-action-profile-agent-session.md) | OPEN/DRAFT comparison input, not adopted action or limit-kind text. Its station dependencies do not become closed merely because those station documents are on their default branch. |

At the source read, curator-spec's default was three commits ahead of
`7e280bef`; the comparison changes README, CHANGELOG and protocol/core.md,
not either station file pinned above. The host-registration source pin is
`db6514e710e1fe89098352d6f034b068edbecf41`.

H1 in this companion means the **identity-latch admission**. It is not
host-registration/1 section 11.1's OPEN H1, which concerns durable attach
state and attach_wanted. Resolving one does not close the other.

The proposed join preserves these boundaries:

- A station name/account/generation, a process incarnation, a harness
  session and a J7 run are different objects. No PID, slot or lifecycle
  record is substituted for the holder's trusted run-origin record.
- The dispatcher owns station state and physical start/stop. A Host
  liveness report, grant checker or key service does not write that state.
  A valid grant is an admission input, not a physical-start command.
- Host registration's generation/counter and expected station state version
  are not a v4 parent ordinal, identity generation or signing allowance.
  They retain their replay/fence and single-owner rules.
- Station section 9.2's proposed record/copy publication and G2/G3 checks
  must be docked with the Core/launcher custody and two-record transition
  below. Neither document's placeholder becomes an admitted seam API or
  authorizes reading another component's state.
- Station section 11's validated binding remains PROPOSED/OPEN OQ19;
  host-registration's OPEN S4 retains the join to it. A locally asserted
  valid-grant boolean or a correct socket peer does not supply that
  binding, the missing grant profile, or actual native operation authority.

The later profile round's handoff and accepted candidate are not supplied
at this source read. Exact missing inputs are: the complete T1 contract
identifier preimages/prefixes/salt lengths and canonical document grammar;
profile validity, grant-term and party-assent rules; invocation members,
request identity/replay bindings and code/precedence assignments; concrete
registered action/kind arithmetic; the host/session/identity/configuration
mapping and actual run-origin provider; and each unresolved O1–O8 clause
not already decided by its cited source. A forecast supplies none of them.
Each remains open in its named clause, to be replaced only by accepted
matching text. No alternate handoff, byte encoding or acceptance is inferred.

### 2.2 Identity latch: H1 — PROPOSED

**P-HOME-1 — separate owners of separate records.** Curator Core/curator-spec selects and reserves the managed-home identity artifact and is its sole writer/comparer. The launcher alone writes/compares its complete typed selection in launcher state and never reads or writes Core's home artifact. Before runtime or registration, the launcher invokes a Core-owned create-once/compare/preserve-on-refusal seam and receives a closed result plus the name. An exact repeat is a no-op. Install, sync, repair, profile projection and removal cannot reset or overwrite established identity history.

**P-HOME-2 — one derivation, full origin retained.** Explicit selection supplies the exact opaque name. Synthetic selection supplies exactly `host_id`, `project_id`, `profile_id`; Core alone derives the name. The launcher retains the domain, identity kind, returned name and exact origin together. A three-ID context is not a triple of domain/kind/origin. There is no second launcher-local derivation, card/Pulse/vault discovery or automatic conversion to a Matrix identity.

The proposed existing synthetic encoding is retained byte for byte: `LP(x)` is a uint32 big-endian UTF-8 byte length followed by exact bytes. Hash input is ASCII `swarma.synthetic-identity/v1`, one zero byte, then `LP(host_id)`, `LP(project_id)`, `LP(profile_id)` in that order. The name is `syn1:` plus the lowercase SHA-256 hex digest, followed by LF in the home artifact. The domain does not enter this derivation. A synthetic name is 69 bytes, or 70 with LF; an explicit opaque name is at most 512 bytes, or 513 with LF. No Unicode normalization or case folding is added. This encoding remains a proposed public specification contribution until accepted here; no implementation is inferred from it.

**P-HOME-3 — same name does not erase a changed binding.** The full protected domain/kind/name/origin tuple must be compared before runtime/registration, independently of a name-only artifact. Same name with changed domain, kind or origin refuses and preserves existing records. Hash collision resistance alone does not prove equality of origins; a forced-equal-name control must exercise the typed comparer. For direct Core use without a launcher, the owning contract must either provide the protected origin authority and comparison or explicitly limit its claim to the opaque-name comparison. It cannot claim the launcher's full typed guarantee from the name file alone.

**P-HOME-4 — per-home concurrency and crash recovery.** Serialization covers the actual canonical home, including different station IDs that can reach it. A station-only lock is insufficient. First-create permission, compare-only repeats, prechecks and the writes of the two distinct records must form a recoverable transaction: a crash between them or one-record-only migration leaves a durable incomplete/fenced state until exact reconciliation, never an incompatible winner or a fresh identity. Refusal preserves established records and unrelated home data. Do not erase identity history to retry installation, use another station ID or interpret a missing record after rollback as a new home.

The actual reserved path, seam API/version, input discriminator, closed result/errors, first-create predicate, finite write set, typed-store/home lifetime, synchronization and crash protocol, cleanup and migration remain owning-interface agreement items. This proposal deliberately defines no guessed CLI flag, filename or native error spelling. Exact canonical context must be supplied for a direct Core caller; a caller-provided assertion cannot appoint its own origin authority.

Station/1 section 9.2 itself marks the name latch PROPOSED pending identity-custody confirmation and admission. Its manager-state record outside the home, publication from that record during R02, comparison before/after publication and preservation on mismatch are useful comparison requirements, not proof that the Core seam above exists. Its section 8 reserves `H/.identity/name` as a PROPOSED path and assigns publication to the user manager using Curator's record bytes. This contribution does not silently identify that publication operation with the Core-owned managed-home artifact or make the launcher its writer. The owning Core, launcher and station contracts must explicitly reconcile the artifact/path and privileged publication split, lifetime across a generation bump/removal, and first-create authority before implementation. A proposed reserved path in station/1 is not an adopted filename for the Core interface. Station/1 OPEN OQ15 (whether identity follows the agent or the place) is not decided here.

Replacement condition: an explicit owning admission of this home-latch custody split plus accepted Core/launcher interface text and exact station/home publication mapping replaces these proposed clauses in one affected revision. A policy refresh, restart or role declaration is not that admission.

### 2.3 T1 and action-profile mapping — PROPOSED

**P-MAP-1 — three identities remain distinct.** The recipient of the agent-session grant is the agent that works; the party submitting a request and the host executor are distinct principals. Proposed LIP-0030 section 3.1 already reads the recipient this way. The signed path fixes its public recipient/executor. Local native custody separately retains its complete selected identity, origin and immutable consumer binding. An MXID, a slot label, a profile name, a process ID or a public-key reference is not authority by itself.

**P-MAP-2 — no hidden public fields.** A local identity or consumer-binding record does not become a member of the public v4 grant. An adapter must verify the public path under its actual profile and separately verify the local typed operation under current protected state; it must compare their complete agreed mapping before an effect. No arbitrary grant blob, caller-selected role or copied digest authorizes native create. A mapping that cannot represent a local opaque name losslessly is refused; it is not repaired by truncation, transliteration or normalization.

**P-MAP-3 — an agent-session action is not enrollment authority.** Session start/restart authority does not implicitly authorize Matrix account registration, vault create, migration or direct access to a secret item. Those operations require the separate concrete operation authority and current native management-code admission. An existing message-author signature, an until-expiry grant or a valid session verdict cannot substitute for either predicate. A future public action that is meant to authorize enrollment must be separately specified and registered, not added as a free-text alias to the session profile.

**P-MAP-4 — configuration binding is explicit and reproducible.** Under the reading proposed here, the action profile names the contract profile that requires the agreed configuration commitment of LIP-0017 section 8. The commitment covers immutable Curator profile/skill revisions and the admitted systems, with the exact manifest bytes and reconstruction algorithm specified by that contract profile. Immediately before a start the launcher reproduces the commitment from what it will actually start; mismatch or missing input forbids the start. A profile label, branch name or previously generated environment is not the commitment.

Where one contract is intended to cover several configurations along a delegation path, the proposal is an explicitly committed, closed role/profile-to-manifest mapping in the contract profile, rather than one unqualified manifest silently reused for every participant. Selection must be authenticated and constrained by the path and the local operation; a caller cannot choose another role to widen rights. This is an addition for contract-profile agreement, not a new grant field or an interpretation already provided by LIP-0030. If that addition is rejected, the profile must instead use the one agreed configuration literally and document that limitation.

**P-MAP-5 — T1 and O4 are not replaced by a plain hash.** Keep F5 and F6 in their published order: compare the contract identifiers in the grants, establish a complete presentation, recompute the identifier under its actual v4 profile, validate that profile, and check the machine terms it requires against each grant. LIP-0017 section 2 commits salted clauses and the other parts; the identifier is not SHA256 of the received document as in the old v3 shortcut. The exact salted preimages, domain prefixes, salt lengths, canonical byte rules, contract validity/mirror rules and their refusal precedence must be defined by the new accepted profile. No stand-in preimage or fabricated success is used while they are absent. Under the current text, no side completes the predicate at F6(b); a proposed configuration mapping does not resolve this by itself.

**P-MAP-6 — lifecycle and Host transport are not the grant profile.** The pinned station/1 section 1.3 (SR1/SR6) and section 13 place the authoritative station state and its journal with the dispatcher; the workbench owns the launch description, Curator owns home composition/name-latch state, and the Host reports logical-session liveness. A requester-side registry or launcher latch is not a second station-state writer. Station/1 section 11 places J1 at the grant checker behind message origin: the dispatcher consumes the validated binding, not a self-authored admission assertion. Its exact binding form remains OPEN OQ19; the listed logical members are not accepted wire bytes. The run/J2 additions in station-runs must not be imported as lifecycle-v1 authority or implemented delivery semantics merely because their file is present.

The pinned host-registration/1 sections 3 and 5 define a Linux-only local Unix-socket seam with kernel-peer/pin authentication. Its registration epoch `(registration_generation, attach_counter)`, operation `state_version`, replay key `(logical_session_id, op, op_id)` and correlation `request_id` are distinct. They do not substitute for a grant contract identifier, native authorization revision or enrollment transaction identity. An exact supported Host repeat retains its original operation and current registration pair under that seam's rules; that is no permission to register another Matrix account or retry a native secret operation under a new identity. The mapping of the seam's version to the station compare-and-set remains OPEN S1; validated-binding/gate surfacing remains OPEN S4. No adapter fills these gaps with a guessed member or by renaming existing refusal codes.

The home-latch proposal in section 2.2 is separate from host-registration/1 **OPEN H1**, which concerns durable Host attach state. Their labels do not identify one contract. Host registration is also distinct from the remote Matrix registration of section 2.4. The Linux seam provides no macOS peer-admission, Keychain ACL or native recovery qualification; Host pin-only authentication is not a proposed replacement for native management-code admission. A proposed salted configuration commitment does not authorize a caller to edit protected registration configuration or bypass a current lifecycle gate.

Replacement condition: replace P-MAP-4/5 only with the accepted complete T1/contract/action profile and exact station/host-registration counterparts. Retain the current no-effect outcome for every unresolved machine comparison; do not treat an accepted interface direction as executable predicate evidence.

Contract-party assent is also an explicit input of this profile. It must
name the actual issuing party and its contract-signing key, purpose and
verification evidence. J4.2's child-delegation key signs children only;
neither it nor an arbitrary owner/root/request key supplies the missing
assent by fallback. This paper selects no assent key or extra owner prompt.
The alternative recorded by version 0.1.56, using the delegator's existing
signature on an equal parent/child contract, remains non-normative. Its
publication does not select it over the unresolved profile requirements.

### 2.4 Enrollment transaction boundary — PROPOSED

**P-ENROLL-1 — authority before registration.** A dedicated admitted native enrollment role first latches the complete intended identity, origin, consumer binding, exact server/admin connection, fresh destination, explicit required session policy and finite public write set. It proves both current account-registration authority and current native management/operation authority before any remote account effect. Native release clients, messenger daemons and a same-Team signed program do not acquire management rights through a flag, environment variable, parent process, room membership or a general session grant. Unqualified or absent authority refuses before network submission.

**P-ENROLL-2 — one original operation and no secret-bearing result.** Before registration the enrollment transaction durably binds its original native operation identity and immutable intended destination in a bounded nonsecret journal. There is at most one incomplete transaction for that destination. The separately admitted enrollment executable performs registration and native create in one process so the returned child access token passes from bounded owned memory directly to native create under the original operation. A two-process alternative requires its own authenticated secret-channel contract first. No token goes to argv, a room, prompt, generic result object, file store, journal, hash preimage for a public receipt, or fallback credential cache.

Existing account-password custody for an explicitly selected daemon E2EE/UIA route is a separate contract; it is not described as ephemeral when it is persistently held there. The child token cannot enter that password section. A new vault-backed enrollment must not reach the legacy Keychain recovery-password branch. This preserves the existing legitimate legacy path without making it a new enrollment fallback.

**P-ENROLL-3 — reserve, recheck, commit, publish.** A valid finite local authorization durably reserves the exact intended operation before remote registration. An old reservation is not proof of current authority at commit: the native management service rechecks its actual peer, original principal/intent, current protected authorization, expiry/revocation and finite caps before custody and immediately before effect. Native create uses its existing create-only/expected-revision-zero contract and explicit required policy. Only an authenticated complete committed receipt for the exact original operation permits publication of public vault selection/identity/revision metadata. Publication is not the private commit itself.

**P-ENROLL-4 — three independent uncertain outcomes.** A missing, malformed or mismatched registration response leaves the remote effect UNKNOWN; no second registration, login/reset, rotation or new account follows automatically. An uncertain native-create outcome is reconciled through the original operation under current scoped authority, never a new operation ID or alternate store. A committed private record with failed public publication permits only recovery of that public publication after exact reconciliation. No visible metadata, an absent operation response or lost token memory proves that an earlier effect did not happen. Exact supported replay returns the retained result without a second allowance or effect.

The journal's schema, transaction states, limits and nonsecret receipt preimage belong to the enrollment implementation contract; no octet schema is declared by these logical clauses. Prove bounds fit or refuse before the remote effect, never truncate. Buffer handling must state actual ownership/copies and cannot promise erasure of immutable strings, OS snapshots or memory outside its custody.

### 2.5 Native custody and limits of evidence — PROPOSED

**P-NATIVE-1.** Every new secret Keychain item directly trusts only its owning signed native custody executable and designated requirement. A generic reader, shell, same-Team wrong executable, enrollment/release IPC client or another product gets no direct item ACL trust. Endpoint pinning does not substitute for item ACL. Source-signature verification, the produced artifact's signature and actual native code/helper identity are separate checks. Existing migration source bytes and ACL remain unchanged; a target-item rule does not authorize widening a legacy ACL or exporting its secret.

**P-NATIVE-2.** H1 identity latching is metadata-only and makes zero vault/Keychain calls. A Linux service account or a public Go verifier is not a macOS-native custody executor. Pure model/codec tests and public signature mathematics do not qualify caller admission, Touch ID, secret non-extraction, actual item ACL, installed code identity or durable native recovery. The intended native route and finite disposable fixture need separate admission before behavioral claims.

**P-NATIVE-3.** A request/identity signing key is not the child-delegation key. The dedicated child issuer under a separate macOS user and its own key/journal does not inherit the owner's root keys, request-key custody, seal/row-coin/funding keys or another issuer's journal. Actual trusted run/origin/delegate-list admission remains required. The selected current build route is author-signed source, our build and Apple signing; a later grant-key artifact-signature scheme must resolve native code identity/Keychain requirements separately and does not retire the present route through this proposal.

## 3. O1 and O6: seal, issuance and a validated spend — PROPOSED

At the consumer, propose this order for F21 and for the parent's F7 part
7.6, after the already required grant-signature checks:

1. Bloc (s): the output, its script and the supported seal profile, in
   their existing order.
2. Classify a validated spend of that seal, after (s) and the signature as
   SB3 already requires. If a validated spend proves closure, retain that
   closure and refuse as `CHILD_NOT_LIVE` for the child or
   `PARENT_NOT_LIVE` for the parent before (w) or (i).
3. Bloc (w): the seal transaction and anchor checks of LIP-0023, in their
   existing order.
4. Bloc (i): the reference/identifier, issuance mode, assent, consent,
   frame, commitment and recent-block window in their existing order.

The four cross-bloc constraints already cited in F21 remain unchanged.
The total order above is a **new proposal**, not an order extracted from
an unordered list. It makes no read failure a validated spend. Missing or
unreadable evidence neither proves an unspent seal nor records closure.
An invalid signature does not become a valid proof of a spent grant.
An observation that is finally void still follows LIP-0022 B6.1; this
proposal does not publish a later code under a refused observation.

At ISSUE, the service still makes only its existing pre-sign bloc (s)
duty for the child: no anchor of that child exists. This ordering adds no
requirement to build the child's anchor before signing it. Row-coin
checks are a separate, carried duty: the initial own-anchor exception
and the Repeat refusal, hold and audit/notice follow the version 0.1.56
baseline in section 1.1. They are outside the proposed seal-bloc order.

## 4. O2: request authentication — PROPOSED

Propose `REQUEST_AUTH` for a request that fails A1 under the recipient
mode of the admitted child: wrong request key, an unknown channel, a
removed channel key or an invalid request signature. A1 retains its one
place after the complete F19 name/recipient evidence and before F20.
It does not become an issuer-caller check; I0/I2 keep their earlier place.

This adopts the spelling proposed for the action profile, but narrows
its attribution to A1. A signed owner-pin or writer failure found in F19
keeps F19's own code and earlier place, rather than being remapped to
`REQUEST_AUTH`. Malformed invocation structure follows its eventual
registered wire parser; this proposal does not supply invocation members
or a parser for the currently empty registry entry. No authentication
failure is called `CHILD_GRANTEE_NOT_ALLOWED`.

## 5. O3: invocation checks — PROPOSED

After completion of the child predicate and its existing A1 check,
propose the following order of E0's semantic checks, then E1, E2 and E3.
Parsing and signature authentication are not repeated as new E0 steps.

| Order | Check | Proposed refusal |
| --- | --- | --- |
| E0.1 | The signed proof path names the actual admitted parent and child, in that order | `REQUEST_PATH` (new) |
| E0.2 | The invocation's executor, the child's executor and the independently authenticated service pin agree | `GRANT_EXECUTOR` |
| E0.3 | The exact requested action occurs in the child's `actions` and the parent's `delegate.actions` | `GRANT_ACTION_ABSENT` |
| E0.4 | The executor's clock satisfies `iat <= now < exp` | `REQUEST_TIME` |
| E1 | The executor's profile defines that action | Existing `ACTION_UNDEFINED` |
| E2 | The executor has a profile for every kind the action will consume | Existing `LIMIT_KIND_UNDEFINED` |
| E3 | The existing atomic reservation checks the own account before the row account for each key | Existing `OWN_LIMIT_OVER`, then `ROW_CAP_OVER`, with the existing per-key ordering |

The spellings other than `REQUEST_PATH` are reconciled with the action
profile's proposals; they are not existing assignments by this file's
word. Their exact invocation/wire definitions still require the owning
invocation specification. A recipient/Subject rule of the action profile
must be docked with these checks, without giving one defect two codes.
No E0/E1/E2 failure creates a reservation, debits an account or invokes an
effect. The ledger's exact-intent replay/UNKNOWN rules still govern E3;
this proposal authorizes no retry of an uncertain effect.

## 6. O4: contract validation and term comparison — PROPOSED

Keep F6(a) presentation and F6(b) identifier recomputation in their
existing order and retain `CONTRACT_NOT_PRESENTED` and `CONTRACT_ID`.
For F6(c), propose two checks in this order:

1. The complete document is valid under the selected v4 contract profile:
   `CONTRACT_PROFILE_INVALID` (new).
2. Its machine terms mirror the grant under that profile's precise
   comparison rules: `CONTRACT_TERMS_MISMATCH` (new).

An unsupported profile is not treated as a valid minimal contract.
Identifier recomputation must use the profile's actual preimages, salts
and prefixes. A change of disclosed text, salt, clause order, parties or
other committed machine members cannot be hidden by normalization.
Textual resemblance never replaces the machine comparison. A broader
contract and a narrower child are judged by the profile's actual
containment/mirror rules, not an invented equality of every numeric term.

These proposed code names distinguish malformed profile content from
valid content whose terms do not mirror the grant. They replace neither
the existing v3 codes nor an already accepted future profile assignment.
Without accepted exact contract bytes, neither side can finish F6(b),
and these conditional F6(c) rules cannot be reported as executed.

## 7. O5: unusable grant-closure journals — PROPOSED

Give the grant-closure journal separate failures:

- `CLOSURE_JOURNAL_UNAVAILABLE`: its authoritative current state cannot be
  read. The attempt admits nothing, signs nothing and creates no new
  reservation; a later complete read may be judged anew.
- `CLOSURE_JOURNAL_FENCED`: its retained continuity cannot be established,
  including a missing, rolled-back or inconsistent required head. The
  service remains unable to admit or sign until the journal's own trusted
  recovery establishes continuity.

Both are **new code proposals** at the existing journal checks, F7 part
7.4 and F20(a). Neither creates a closure of a grant. Neither borrows
`JOURNAL_LOST` or `JOURNAL_FENCED` from the row ledger. Preserve known
closure evidence, prior records and protected heads; a failed write of
an observed closure permits no effect and needs journal recovery. When a
fence cannot itself be persisted, the current service remains refusing;
a new process still needs authoritative continuity before an admission.

A new empty journal, successful file open, restart or a fresh key proves
no absence of an earlier closure. Recovery must restore the journal's
verified history and trusted head through its own accepted mechanism.
The exact entries, storage/recovery mechanism and cross-process
observability are required from the closure-journal profile; this paper
is not a native journal format or a recovery implementation.

## 8. O7: whole-parent admission — PROPOSED

Propose whole-parent validation of the signed document at F13(b): besides
the selected group's mandatory rules, judge every applicable mandatory
rule of W11.10, including rules 2 and 6 to 8 and rules 4 and 5 in other
groups/ranges. Any such defect refuses as `GRANT_DELEGATE` there. Judge
the mandatory rules in their W11.10 order; rules 1 and 3 already judged
at F1 need not be recomputed. The existing two W11.10 proposal points
retain their pending status and do not become mandatory by this sentence.

This is the proposed resolution of the admission component of
LIP-0026 proposal Q1. It changes the currently permitted two outcomes for an
O7 defect into one refusal only if accepted. It does not read chain facts of
a foreign row, and it does not move every parent check to F1 or before the
observation.
Selected or foreign contributions are treated alike: a selected coin
equal to the parent's seal, an overlap with another range, a shared stop
coin and a global pool-sum defect cannot evade the check.

Count/byte bounds and ordinal order are separate decisions. This proposal
does not drop R8.4's bounds as an accidental consequence of agreeing on
whole-parent refusal, and does not claim that all of Q1 was accepted.
Until the actual decision, the existing two permitted stage outcomes
remain the source's statement; no full conformance claim is possible.

## 9. O8: the ISSUE freshness class — PROPOSED

Assign signing a child to the first class of LIP-0022 B3.5, money or
irreversible, explicitly for ISSUE. There is no invocation whose action
can supply a class at that point. Use B3.1 to B3.8's same age measure and
guards, with the B3.6 refusal `TIP_AGE` at age **3600 seconds or more**;
no 5400-second substitution and no grace. Apply it both at initial I3
and at Repeat's fresh I3, without reusing the first observation.

This is a new class assignment, not the claim that B3.5 already assigned
an actionless ISSUE operation. A caller cannot lower the class or select
another clock. It changes no block-height grant window, invocation
`iat`/`exp` rule, local authority cutoff or source status of the proposed
two-age measure. A local calendar limit is no public freshness substitute.

## 10. LIP-0026 R8.3 and the remaining proposal Q2

For the state of the R8.3 count order, see LIP-0026 section 8.

The remaining parts of LIP-0026 proposal Q2 stay **PROPOSED**;
LIP-0026 proposal Q2 states them.

## 11. Paired acceptance cases

These are specified positive and forbidden outcomes, not test results.
For a case that needs the complete predicate, all earlier checks are
valid under the eventually accepted profile. A stipulated contract-valid
flag is not an implementation of T1 or evidence for F6(b).

| Case | Positive control | Forbidden neighbour and required result |
| --- | --- | --- |
| O1 | A valid seal, anchor and issuance presentation completes their checks | Defects in both (w) and (i): report the first failure in (w); defect in (s) plus either later defect: report (s); do not reserve/sign |
| O6 | An unspent seal with valid evidence continues | Validated spent seal plus invalid anchor: retain closure and report the grant's not-live code before (w); failed spend-state read alone must not create closure |
| O2 | Correct request signature under the current recipient mode passes A1 | Wrong/removed channel key or wrong signature: `REQUEST_AUTH`; wrong owner/writer at F19 keeps its earlier code; zero effects |
| O3 | A permitted, current invocation for the actual path/executor reaches E1/E2 and the existing reservation | Wrong path plus wrong time: `REQUEST_PATH`; wrong executor plus undefined action: `GRANT_EXECUTOR`; expired but permitted action: `REQUEST_TIME`; no debit before all preconditions |
| O4 | Complete valid document, correct identifier and matching machine terms completes F6 | Missing document: `CONTRACT_NOT_PRESENTED`; changed committed octets: `CONTRACT_ID`; identifier-valid invalid profile: `CONTRACT_PROFILE_INVALID`; valid profile but wrong terms: `CONTRACT_TERMS_MISMATCH` |
| O5 | Readable closure journal with established continuity and no closure allows later checks | Unreadable state: `CLOSURE_JOURNAL_UNAVAILABLE`; lost continuity: `CLOSURE_JOURNAL_FENCED`; neither creates a grant closure or a fresh journal; known closure remains effective after recovery |
| O7 | A clean parent and a valid selected row pass the document checks | Global pool/overlap/seal/stop defect, including one to which the selected row contributes, or a mandatory foreign-group defect: `GRANT_DELEGATE`; no foreign row-chain lookup |
| O8 | Otherwise valid observation with tip age 3599 seconds passes this cutoff | Age exactly 3600 seconds: `TIP_AGE`; a fresh initial check followed by stale Repeat also refuses before USE/private entry; no caller downgrade |
| R8 | The nine-row example of LIP-0026 section 8 resolves ordinal 5 to the exact second range/second coin | Ordinal 0/10: `CHILD_ORDINAL`; swapped signed group order changes the mapping and is never accepted as the same signed parent; used rows are not removed from the count |

The implementation must later demonstrate the intended failure using
independent observations of private-entry counts, journals and effects,
paired with successful valid controls. Rejecting every input, matching
two copies of a checker, a skipped plant or an unrelated setup failure
does not establish these claims. Full signed both-mode vectors, real
observation/node/clock evidence and native custody qualification remain
required before an end-to-end result is accepted.

### Identity, enrollment and profile controls

All scenarios below are proposed acceptance requirements, NOT_RUN. Each negative has a nearby valid case. Codes and wire fixtures must come from the final owning interface; an unrelated crash, timeout or setup refusal is not the intended rejection.

| Valid control | Forbidden neighbor and required observation |
| --- | --- |
| Correct recipient/executor/path plus current independently authorized native enrollment operation | A session grant alone, caller label, copied binding digest, wrong endpoint or wrong current principal refuses before registration and before native secret entry; no reservation/effect outside its contract |
| Complete T1/profile with actual salted identifier and matching machine terms | Missing salts/preimage/profile, v3 plain-document hash shortcut, altered contract or unknown limit profile cannot produce a successful v4 predicate or private signature |
| Pinned lifecycle and qualified Host seam used only for their published purposes | Proposed runs, self-authored validated binding, reused correlation as a replay key, stale registration pair, or a Linux pin presented as Mac custody admission cannot authorize a start, registration or secret effect outside the owning contract |
| Exact selected immutable configuration reproduces its commitment at start | Wrong role/profile/manifest or changed system selection cannot start, even when a previously generated environment exists |
| Exact first home selection and exact repeat | Same name with changed domain/kind/origin, unsafe/malformed state and a forced-equal synthetic name give the intended conflict, preserve existing state and start no runtime/registration |
| First-create race on one canonical home, then exact recovery | Two station IDs, a crash between records or one-record migration cannot publish conflicting identities or reset the established history; incomplete state stays fenced until reconciled |
| Valid original register/create/publication transaction and exact supported replay | Lost registration/create reply, changed retry parameters or failed publication cannot issue a new ID, second account/key/allowance, credential fallback or false rollback |
| Valid explicitly selected existing password/UIA path and new vault enrollment | The vault enrollment's legacy recovery-password branch is unreachable, with no token in password custody or a generic result/store |
| Owning signed custody executable reaches its intended item | Generic/wrong/same-Team executable and IPC client direct reads fail at the actual ACL without trust weakening; a metadata-only H1 operation makes zero vault calls |

A future conformance harness must show that a bounded deliberate omission of origin comparison, pre-remote authority, secret-result suppression or one-effect replay protection fails at the intended branch, then restore the valid control. Fixture success covers only its admitted fixture, not a live migrated vault or every installed home. No live account, real secret, user session or private key is used to satisfy these proposed checks.

## 12. Adoption boundary

For the state of the R8.3 count order, see LIP-0026 section 8. The other
content here concerns the Source-contract inputs only. A later decision must
identify which clauses it accepts and the source revision that fixes
their exact text. Cross-check both sides after any accepted replacement;
do not leave one side using a superseded proposed code or ordering.
Unaffected clauses, byte formats and historical evidence keep their
existing status. No key creation, signing, journal initialization, host
registration, service start, installation or deployment is authorized by
the publication of this file.
