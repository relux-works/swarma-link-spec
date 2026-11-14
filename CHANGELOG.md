# Changelog

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
