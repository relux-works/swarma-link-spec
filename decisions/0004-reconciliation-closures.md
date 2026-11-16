# Decision 0004: Reconciliation closures and proposal boundaries

## Status and sources

This record carries the specification-side closures of 2026-11-16. The
sources are the reconciliation closure list r5.4 of that date, the owner
agenda of 2026-11-15 and its night entries, and the lead's corrections of
2026-11-16 at 03:09Z, 03:15Z and 05:30Z. The closure list has SHA-256
`9dc49e7786b234e4d498cf47923c7559b8e754ccb17dc7a6b390f7302cae11d2`.
The check base is version 0.1.51, commit
`bd3bc80e5543d8a563343ec05abd1a5f3f67284c`.

Every LIP retains its status. An owner decision recorded in Draft text
before this version keeps its existing agreement boundary; the section
"Status of the decisions of this version" covers the others. J9 to J12
keep the in-force classification
of version 0.1.51. This record adopts no wire format or conformance class.

## Closures

| Subject | Decision source | Specification text |
| --- | --- | --- |
| Caller authority at the model proxy | Reconciliation closure list, caller authority | LIP-0028, Motivation: the bearer holds the dispatcher-prepared run binding; on-use checks cover mode, window and account block, without consulting the key holder or chain. |
| Hire | Owner agenda, hire decision of 2026-11-15 at 15:25Z; closure list, hire | LIP-0008 section 2.1 and the rental row of LIP-0017 section 7: a contract and at least a TEXT grant and an EFFECT grant. |
| Wallet request key | Owner agenda, wallet-key decision of 2026-11-15 at 17:05Z; closure list, wallet request signing | LIP-0006 section 1: Keymaker holds the request key and checks the run origin and the operator's table before signing. The existing wallet slice stays as it is. |
| Signed communication | Owner agenda, 2026-11-16 at 03:15Z; lead correction at 03:09Z, item 3 | LIP-0029 decision 1 and section 1; LIP-0013 section 3.7 point 2: signed at minimum, encrypted at maximum, with the M0 transition and unsigned input ignored after M6. The text denies effect to the unsigned message itself; the run that such work starts is open (below). |
| One host | Owner agenda, 2026-11-16 at 03:08Z; closure list, one-host scope | LIP-0029 Summary: chain rules apply inside one host too; the host is one node. Registry simplification inside a host stays open. |
| Origin and level | Reconciliation closure list, receiver's limit on origin verification | LIP-0013 section 3.6: the level holds at an honest key holder only; a receiver cannot verify the origin. |
| Authority frame | Reconciliation closure list, authority-frame correction (r3) | LIP-0013 section 3.4: the frame arrives in a separate channel. A signature on it is not established. The earlier claim of a decided signer and its dependent format and key are withdrawn. The draft's proposal of a local, unsigned frame stands as a proposal. |
| Grant closure and stops | Reconciliation closure list, emergency-brake citation | LIP-0008 sections 5.2 and 5.3 distinguish J6 closure at foreign verifiers, the project stop of platform section 22.5 and the installation stop of platform section 6.6.2. |
| Grant term | Reconciliation closure list, grant term against name expiry | LIP-0008 sections 3 and 7.1; LIP-0003 section 2: the issuer refuses to sign beyond its name expiry observed at issuance, 36000 blocks from the last update. |

## Status of the decisions of this version

The decisions in this table are in force in version 0.1.52. The co-author's
answer to each is folded in later by amendment and gates nothing. In force
means that the decision binds the text that carries it; it changes no LIP
status and gives no format, code or implementation.

| Decision | Decider and date | Text |
| --- | --- | --- |
| Hire: a contract plus at least a TEXT grant and an EFFECT grant | Ivan Oparin, 2026-11-15 at 15:25Z | LIP-0008 section 2.1; LIP-0017 section 7 |
| Wallet request key held by Keymaker, as the decided successor path | Ivan Oparin, 2026-11-15 at 17:05Z | LIP-0006 section 1 |
| Signed communication, with the M0 transition | Ivan Oparin, 2026-11-16 at 03:15Z | LIP-0029 decision 1 and section 1; LIP-0013 section 3.7 point 2 |
| One host | Ivan Oparin, 2026-11-16 at 03:08Z | LIP-0029 Summary |
| Staging of the M6 switch | Ivan Oparin, 2026-11-16 at 01:45Z | LIP-0029, "What is decided and what is proposed" |
| Authority frame in a separate channel | Ivan Oparin, 2026-11-16 | LIP-0013 section 3.4 |
| Grant term against name expiry | The reconciliation closure list; it gives neither a decider nor a date | LIP-0008 sections 3 and 7.1; LIP-0003 section 2 |

These markers of a pending agreement stood over the texts that carry those
decisions. None of them blocks a decision of the table:

- the status line of LIP-0029, "until the co-author agrees every text that
  this LIP revises stands as written", and its header "Revises, once
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

One point of the signed-communication decision is open. A run started by
labelled unsigned work still gets the owner row; binding of effects to the
key holder signature is not specified (LIP-0013, open question T12;
LIP-0029, "Open questions").

## Completion before freeze

The owner agenda and the lead's item-9 relay require completion before a v4
freeze: row groups, the seal and head decisions, the emergency brake, anchor
recovery, the separate authority-frame channel, the two-operator shadow run,
J10 to J12, and the night's owner-control decisions. The row-groups and
session laboratories must land before freeze. This record declares no freeze
and no laboratory landing.

The device protocol of LIP-0029 stays: the hash in the name, the device list,
the algorithm registry and seal-spend revocation. The external device-format
replacement was not accepted. Key, action-registry, landing, run-window,
level-ladder and first-proof-scope questions remain open. Platform-book
changes remain on hold, and no platform-first precedence is adopted.

## Proposals awaiting the owner

The lead's 05:30Z relay requests four proposals and leaves the in-force
profile unchanged. LIP-0026, "Owner decision proposals", gives one text for
each. The classification is the public
[decision map at version 0.1.51](https://github.com/relux-works/swarma-chain-lab/blob/0f50d9151cfdb9d46cebacec0fa229788d73fc4f/experiments/grant-v4/identity/R1-DECISIONS-051.md),
reviewed in [change 134](https://github.com/relux-works/swarma-chain-lab/pull/134).
Whole-parent admission remains unavailable under that in-force profile.
