# LIP-0017: Contracts

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** the contract that a grant binds, the action table of LIP-0005,
  validity windows, the ending of a contract
- **Builds on:** LIP-0004, LIP-0005, LIP-0008, LIP-0011 and LIP-0013

## Summary

A contract exists in this specification only as a hash. A Grant v3 signs
`contract_sha256`, the consent repeats it, and the issuance commitment binds
it. What the document says is left to a profile, and two parties who agree
on something without issuing a grant have nothing to anchor.

This LIP makes the contract an object of its own. A contract is one
document that two or more parties sign: free text for people, together with
members that machines compare. Its identifier commits to a salt and to a
salted hash of each clause, so that a party can disclose one clause and
keep the others. The parties anchor the identifier in one LIP-0005 frame,
and they can show their assent on chain by spending an output that needs
all their signatures. Every grant binds a contract, which may be minimal,
and a contract may exist without any grant.

Two rules connect a contract with the grants under it. A grant's window
lies inside its contract's window, so one framework contract can cover many
grants over time. And a contract can name a seal of its own: an output
whose script says who may end the contract, and whose spend ends every
grant under it. Decisions of 2026-11-17 make that seal the whole
termination rule of the contract and a condition of issuance: the
termination type of a contract is the type of its seal, shown by every
reader from the seal's script and never from prose; drafting a contract
starts with creating its seal; and no grant is issued under a contract
without a confirmed seal (sections 5 and 6).

The LIP records Ivan Oparin's decisions of 2026-11-14, for which the
co-author's agreement is pending, and, since this amendment, of 2026-11-17.
On C10 to C12, the co-author agrees and leaves
the judgement to Ivan (source below). It proposes semantics without
canonical bytes, and nothing of it is implemented.

## Decisions recorded

Ivan Oparin decided the following on 2026-11-14. The LIP stays Draft until
the co-author agrees; adoption follows LIP-0001.

| Decision | Direction |
| --- | --- |
| C1. Free form | A contract is bytes that N parties sign. Its text is free: prose for people and members for machines stand in one document. |
| C2. Salts | The contract carries a salt, and each clause a salt of its own, so that a party can disclose single clauses. |
| C3. Anchor | A contract is anchored in a LIP-0005 frame with an action code of its own. |
| C4. Assent on chain | Optionally, both parties show their assent by spending a shared output that needs both signatures. |
| C5. Contract and grant | Every grant references a contract, which may be minimal. A contract may exist without any grant. |
| C6. Any parties, many kinds | Contracts and grants work for any pair of parties, people, companies and agents in any combination, and for many kinds of contract: between businesses, for services, employment, rental and trust. |
| C7. Windows | A grant's window lies inside its contract's window. Profile `swarma-trust-contract/1` keeps equality as the special case. A framework contract may cover several grants over time. A contract ends early only through a machine rule that names who may declare the end. |
| C8. Contract seal | For v4 and for framework contracts: the contract names its own confirmed output. Every grant under it also requires that output unspent, and one spend ends them all. The script of the output encodes the termination clause: the issuer alone, either party, both together, or an arbiter. The spend carries a frame with the hash of the signed termination statement. v3 stays as it is: the issuer spends seals, and the reason follows LIP-0011. |
| C9. Configuration | The contract carries the hash of the configuration manifest that the parties agreed on. The manifest is expressed only through Curator profiles, Curator skills, from the catalog or custom and reviewed, and the systems that the agent may use. Both parties sign it with the contract, and the platform executes exactly it. For a rental the slot launcher composes the agent's read-only runtime context from the pinned profile, the human terms of the contract, the machine terms of the grant and any scope text. |

Ivan Oparin decided three further points on 2026-11-17. For these points,
the co-author agrees and leaves the judgement to Ivan. The co-author's
words in
event `$KhhzZv1s7jj238dOQ_cnvhJbUXZta1R19JU748Fiutw` of 2026-11-17
are «ок, звучит вроде разумно , но я доверюсь Ване)». This records that
position and no stronger one; the LIP stays Draft and adoption follows LIP-0001.
The labels C10 to C12 are this draft's numbering, continuing the table above.

| Decision | Direction |
| --- | --- |
| C10. The seal decides termination | The termination type of a contract is the type of its seal: issuer only, either party, both together, or arbiter, per its script. It is a machine field of the contract, and every reader, renderer and user interface shows it from the seal script, never from prose. A prose clause on termination ends nothing (section 5, rule 6). |
| C11. Drafting starts with the seal | Drafting a contract starts with creating its seal. |
| C12. No grant without a contract seal | A grant is not issued under a contract without a confirmed seal. The issuer's signing service and every verifier check this deterministically and refuse. |

The nine directions of 2026-11-14 and the three of 2026-11-17 are the
owner's. Everything else in this LIP is the draft's proposal and is not
decided: the members of the contract object, the construction of its
identifier, the two action numbers, the checks of a reader and their order,
the limit of one framework contract above a contract, and, in section 8,
which contracts must carry the configuration hash and what a reader and a
launcher refuse. Of the amendment of 2026-11-17 the same holds for its
form: the refusal codes `CONTRACT_SEAL_MISSING` and
`CONTRACT_SEAL_UNAVAILABLE` (section 6), their place in the order tables of
LIP-0014 section 8.4 and LIP-0020
section 11.11, and the readings in sections 5 and 6 that state the scope
of C11 and C12 against Grant v3 and against a contract without a grant,
whose questions the open questions below name. The refusal itself, and
that both sides make it, are the decided part of C12.

## Motivation

Four cases have no form today.

Alice and Bob agree that Bob delivers a design by the end of the month. No
grant is involved, so nothing of their agreement can be anchored, and
neither can later show when it was made or that the other signed it.

A company engages a contractor for a year, and each month's work runs under
a grant of its own. Each grant binds its own contract hash. Nothing says
that the twelve belong to one agreement, and nothing ends them together.

Only an issuer can end a grant early, because the seal pays its key. The
other party cannot end anything, both parties cannot end something
together, and an arbiter has no part at all.

A party that shows its contract to an arbiter shows all of it. The grant
binds one hash over the whole document, so one clause cannot be disclosed
without the rest.

## Current state

- A Grant v3 signs `contract_sha256` and treats the document as opaque
  (LIP-0004 section 2, LIP-0013).
- The consent of LIP-0004 section 3 holds two signatures over that hash:
  the grantee's kind-8181 event with the tag `contract`, and `landlord_sig`
  by the grant key. The issuance commitment of section 4 binds the hash,
  both signatures and the grant id.
- The bytes of the document belong to a profile. This specification names
  three: the terms object of the wallet service (LIP-0006 section 3), and
  the profiles `swarma-trust-contract/1` (LIP-0013) and `/2` (LIP-0014, a
  draft). The rental path of the reference laboratory has a booking
  contract of its own.
- In profile `/1` the window of the contract equals the window of the grant
  (LIP-0013 section 2.5, check 3).
- The v4 draft binds the contract hash in the signed grant, requires both
  parties' consent to the matching contract, has the contract mirror every
  limit of the grant, and lists a contract assent among the typed objects
  that need a signing domain of their own (LIP-0008 sections 1, 2 and 8).
- A grant ends early when its issuer spends its seal. LIP-0011 proposes a
  reference to a verdict in that spend, for a violation.

No object exists for a contract without a grant or for a contract above
several grants, and no party other than the issuer can end a grant.

## Proposal

### 1. The contract

A contract is the exact octets of one document, and every hash of this LIP
is over octets. The document has these parts. They are named by meaning;
their bytes come with a profile (LIP-0018).

| Part | Meaning |
| --- | --- |
| Profile | The contract profile and its version. It selects the rules under which the document is read. |
| Parties | Two or more parties. Each is named by the key that signs for it and, where it has one, by its Namecoin name. |
| Window | The time that the contract covers, in the measure of its profile: Unix seconds in the v3 profiles, block heights on v4 (LIP-0008 section 7.1). |
| Clauses | An ordered list. A clause holds free text, or machine members, or both. |
| Salts | One random value for the contract and one for each clause (section 2). |
| Framework | Optional. The identifier of the one framework contract that this contract stands under (section 5). |
| Seal | The contract's own seal (section 6). Required in a contract under which a v4 grant is issued and in a framework contract (decision C12); a contract under which no grant is issued and which is not a framework contract may have none. Its script gives the contract's termination type, a machine member that a reader derives from the script (decision C10, section 6). |
| Assent output | Optional. The output whose spend shows assent on chain (section 4). |
| Configuration | The hash of the configuration manifest that the parties agreed on. The profile of a contract under which the platform starts an agent requires it; other contracts carry none (section 8). |

1. **Free form.** The protocol does not interpret the text of a clause. The
   text binds the parties. Under LIP-0006 section 7 it governs an agent's
   work and never a service's effect, so whatever a machine has to compare
   is a machine member. On v4 the machine members mirror the limits of the
   grant (LIP-0008 section 2).
2. **Signatures.** Every party signs the same contract identifier with its
   own key, under a signing domain that belongs to contracts alone
   (LIP-0008 section 8). A contract is concluded when every party it names
   has signed. A signature by a key that the contract does not name adds
   nothing. The consent of LIP-0004 section 3 is this rule for two parties.
3. **Which key signs** is a rule of the profile. In the v3 profiles the
   issuer signs with its grant key and the grantee with the grantee key.
4. **A minimal contract** holds what the grant needs and nothing more: the
   parties, the window and the members that mirror the grant. The trust
   contract of LIP-0013 and the terms object of the wallet service are
   minimal contracts.

### 2. Salts and the disclosure of single clauses

Each clause is committed by a hash over its own salt and its octets. The
identifier of the contract is a hash over the contract's salt, the parts
other than the clauses, and the clause commitments in their order. The
exact preimages, their prefixes and the length of a salt come with the
bytes.

The construction gives two things. A reader who sees only the identifier
cannot test a guessed text against it, because it does not know the salts;
LIP-0011 notes the same weakness for a short request. And a party
discloses one clause by showing its octets and its salt together with the
commitments of the other clauses. The reader recomputes the identifier and
learns the number and the positions of the other clauses, and nothing of
their content.

The disclosure has limits. A clause shown alone can mislead, because
another clause may qualify it; an arbiter can ask for the rest. The parts
other than the clauses are shown with every disclosure, the parties and the
window among them. A clause that a verifier must compare with a grant is
disclosed to that verifier. And a party that loses a clause's salt can no
longer disclose that clause.

### 3. The anchor

A contract is anchored in one zero-value `OP_RETURN` output, in a LIP-0005
frame with a new action:

| Action | Name | Payload |
| --- | --- | --- |
| `0x07` | contract anchor | `version(1)` \|\| `contract_commitment(32)` \|\| `locator` |

The commitment binds the identifier of the contract; its preimage comes
with the bytes. The locator points at the signed contract by the hash of
its stored bytes. Parties that do not publish their contract use the
locator type `0x00`, which gives no location.

The anchor shows that the identifier existed when its block was mined. It
does not show who signed: that is in the signatures of section 1, or on
chain under section 4. A contract that a v3 grant binds needs no anchor of
its own, because the issuance commitment of that grant already binds its
hash. The anchor serves a contract without a grant and a framework
contract.

### 4. Assent on chain

Two parties MAY show their assent on chain. The contract then names an
assent output: an output that both parties must sign to spend, confirmed
before the contract is signed, as a seal exists before its grant (LIP-0008
section 9). The anchor transaction spends that output.

1. The anchor transaction spends exactly the named output, under the named
   script, and carries exactly one `OP_RETURN` output, the frame of section
   3 for this contract.
2. Each signature that authorizes that input commits to every output of the
   transaction: `SIGHASH_ALL` without `ANYONECANPAY`.
3. The signatures of section 1 stay mandatory. Assent on chain is added to
   them and replaces none.

The spend shows that the holders of both keys of the named script signed a
transaction that commits to this contract, at a time that the chain fixes,
and it shows this to a reader who never sees the contract. The chain keys
are tied to the parties by the contract, which names the output and which
the parties signed with their contract keys. For more than two parties the
output needs all their signatures.

The cost is one more output and a script with two keys. Under profile W of
LIP-0008 section 1.1 the inputs of an anchor are native single-key inputs,
so an input with two keys needs a construction profile of its own, which is
open.

### 5. Contracts and grants

1. Every grant binds exactly one contract: `contract_sha256` on v3, the
   contract hash of the signed grant on v4. The contract may be minimal.
2. A contract may exist without any grant. It is concluded by its
   signatures and anchored under section 3.
3. **Containment.** The window of a grant lies inside the window of its
   contract: it begins no earlier and ends no later, in the measure of the
   profile. This compares two windows and changes nothing in how a window
   is read. On v4 a window stays half-open, and admission at its end
   height refuses (LIP-0008 section 7.1). Profile
   `swarma-trust-contract/1` requires the two windows to be equal, which is
   the special case, and that rule of LIP-0013 does not change. A new
   profile says which of the two relations it requires.
4. **A framework contract** is a contract under which several grants are
   issued over time. A grant is under a framework contract when the grant's
   own contract names that framework contract by its identifier. A contract
   names at most one framework contract, and a framework contract names
   none. The window of the naming contract lies inside the window of the
   framework contract, and with it the window of the grant.
5. The authority frame of LIP-0013 section 3.4 carries the identifier of
   the framework contract to the agent.
6. **Early end.** A contract ends before its window closes only through a
   rule that a machine checks and that names who may declare the end. On v3
   that rule is the issuer's spend of a grant's seal. Under section 6 it is
   the spend of the contract seal by the parties that its script names. A
   clause that states reasons for an end in words binds the parties and
   ends nothing by itself; LIP-0011 says the same of a verdict. By decision
   C10 of 2026-11-17 the termination type of a contract is the type of its
   seal — issuer only, either party, both together, or arbiter, per its
   script (section 6) — and no other. The type is a machine field of the
   contract: every reader, renderer and user interface MUST derive the
   type that it shows from the script of the seal that the contract
   names, and MUST NOT take it from the prose of a clause, from a summary
   or from any other text. A prose clause on termination, whether it
   states reasons or names a party that may end the contract, ends
   nothing and changes no type; where the prose and the script say
   different things, the script decides what is shown and what ends the
   contract, and the prose binds the parties as text alone. A contract
   that names no seal has no termination type to show, and a reader MUST
   NOT supply one from its prose. A stored type member that disagrees with
   the script does not override the type derived from the script.
7. **No grant without a contract seal.** By decision C12 of 2026-11-17 a
   v4 grant, and a grant under a framework contract, MUST NOT be issued
   under a contract without a confirmed seal (the scope of section 6).
   A minimal contract of the landed v3 path still needs no contract seal;
   whether C12 reaches v3 as well is open against decision C8.
   Section 6 states the check, its scope and its refusal codes: the
   issuer's signing service makes it before it signs, and every verifier
   makes it at admission, each deterministically on its own node. A
   contract without a seal, or whose named seal the node does not show
   confirmed as named, therefore carries no grant in the scope of
   section 6, however complete its text and its signatures are.

### 6. The contract seal

The contract seal is for v4 grants and for framework contracts. Grant v3
does not change: there the issuer spends the seal of each grant, and
LIP-0011 gives the form of the reason. The grants under a contract are the
grants that bind it and, for a framework contract, the grants whose own
contract names it.

By decision C12 of 2026-11-17 a contract in the scope of this section —
a contract under which a v4 grant is issued, and a framework contract —
MUST name a seal of its own: an output, given by transaction, index and
script, that is confirmed before the contract is signed. A contract under
which no grant is issued and which is not a framework contract MAY name
one and MAY have none; whether decision C11 takes
that choice away is open (see "Open questions"). Grant v3 does not change,
as the paragraph above says: a minimal contract that a v3 grant binds
needs no contract seal under this section, and whether C12 is meant to
reach v3 as well, against decision C8, is open there too. By decision C11
drafting a contract starts with creating its seal. In the scope above
that is an order, not a style: the parties first create the seal output,
whose script fixes the termination type below; the contract then names
that output, and it is signed only once the output is confirmed, as
decision C8 requires for the contract's own output. A contract therefore
never waits for a seal that is still to be made, and its identifier,
which commits to the parts other than the clauses (section 2), commits
to a seal that already exists on the chain. The script of the seal is
the termination clause of the contract, and by decision C10 its type is
the contract's termination type, a machine field of the contract that
every reader, renderer and user interface MUST show from the seal script
and never from prose (section 5, rule 6):

| Termination clause | Who may end the contract | Script of the seal |
| --- | --- | --- |
| Issuer only | The issuer | One key, the issuer's |
| Either party | Each party alone | Either of the two parties' keys |
| Both together | The parties by agreement, and neither alone | Both parties' keys |
| Arbiter | An arbiter that the contract names | A script that includes the arbiter's key; its exact form is the profile's |

The transaction that spends the seal carries exactly one `OP_RETURN`
output, a LIP-0005 frame with a new action:

| Action | Name | Payload |
| --- | --- | --- |
| `0x08` | contract termination | `version(1)` \|\| `contract_end_commitment(32)` \|\| `locator` |

1. Every grant under the contract requires, beside every check of its own,
   that the contract seal exists with the named script and is unspent, the
   mempool included.
2. One spend ends them all. A verifier that validated a spend of the
   contract seal refuses every grant under the contract from then on, as it
   does for a grant whose own seal the issuer spent (LIP-0008 section 5.1).
3. The commitment of the frame binds the identifier of the contract and the
   hash of the signed termination statement, and the locator points at that
   statement. Each signature that authorizes the seal input commits to
   every output: `SIGHASH_ALL` without `ANYONECANPAY`.
4. The termination statement is signed by the party or the parties that end
   the contract. It names the contract, the termination clause and the
   reason. The reason is free text, or it refers to a verdict of LIP-0011.
   The bytes of the statement are open.
5. The spend alone ends the contract. The frame adds evidence: it lets the
   other party and an arbiter find the statement behind an ending. A frame
   that the seal signatures do not cover is no evidence, and the contract
   is ended all the same.
6. **No grant without a confirmed seal (decision C12).** Before a grant
   in the scope of this section is signed, the issuer's signing service
   MUST check, and at every admission every verifier MUST check, each on
   its own node and in the observation of that signing or admission, that
   the contract that the grant binds and, where it names one, its
   framework contract each name a contract seal confirmed as named.
   Both complete documents must be presented or resolved and recompute
   to their respective identifiers before any seal is read. The form of
   that presentation and resolution remains open below. The side checks
   the bound contract first, then its framework contract. For each, a
   seal is confirmed as named when the named transaction is confirmed in
   the active chain, it has an output at the named index, and the script
   of that output is, octet for octet, the script that its contract names.
   No side takes these facts from the party that presents the grant or
   asks for the signature. The same documents against the same confirmed
   chain give the same answer and code where both nodes can read those
   facts; equal chain tips alone do not imply equal availability.

   The two refusal codes and their retry marks are defined once in
   LIP-0020 section 11.11. For each contract, no seal named gives
   `CONTRACT_SEAL_MISSING` without a node read. With a seal named, the
   side first establishes whether its node read is conclusive. A named
   transaction unknown to the node, or any read that proves nothing,
   gives `CONTRACT_SEAL_UNAVAILABLE`, pending, and never establishes
   absence. Only a conclusive read can give `CONTRACT_SEAL_MISSING` for
   a transaction not confirmed in the active chain (mempool only
   included), no output at the named index, or another script. In either
   refusal the signing service MUST NOT sign and a verifier MUST NOT
   admit; neither refusal records a closure. The code names and their
   order are this draft's proposal; the refusal at both sides is C12.
   At a v4 child this check is part (c) of row F6 of LIP-0014 section 8.4,
   after both documents recompute in (b) and before the open profile
   findings of (d). A confirmed-as-named seal that is spent is neither
   refusal: it ends the contract under rules 1 and 2 above, whose step,
   code and closure stay open below. An unavailable read of such a
   transaction still proves nothing and is pending, not a missing seal.
7. **The type that is shown (decision C10).** A reader, a renderer and a
   user interface derive the termination type from the script of the
   named seal, by the script forms of the contract's profile, and show
   that type. They MUST NOT show a type taken from prose, and a type that
   prose states beside a seal of another type is not shown instead and
   not shown beside it as an alternative. The exact scripts of the four
   rows are open (see "Open questions"), so which script gives which row
   is fixed with those scripts. No reader classifies a script
   that its profile does not give a form, and it has no type to show for
   it. This rule assigns that case no code.

Each grant keeps its own seal, whose spend ends that one grant. The
contract seal adds a second way to end, for all grants at once and for the
parties that the clause names. Its keys are new keys of the protocol, and
the [key registry](../KEY-REGISTRY.md) lists them.

### 7. Any parties, many kinds

The protocol asks three things of a party: a key that signs; for a party
that issues grants, a name that publishes its grant key; for a party that
receives them, a key or a name (LIP-0008 section 3.1). It does not ask what
the party is. A person, a company and an agent are parties in the same way,
in any combination. A company acts through the keys that its officers hold;
how an organization binds those keys to its name is the sketch of LIP-0015
and is not proposed here.

The scenarios show which objects each kind of contract uses:

| Scenario | Parties | Contract | Grants under it | Who can end it |
| --- | --- | --- | --- | --- |
| Rental of an agent | A renter and the operator who rents the agent out | The booking contract, with the price, the period and the limits | At least a TEXT grant and an EFFECT grant, each for the whole term (LIP-0008 section 2.1) | By the contract seal, as its script states; the issuer also by the seal of each grant |
| Trust between the agents of two owners | A principal and an agent of another owner | A trust contract (LIP-0013) | One grant; under LIP-0014 also child grants | On v4, by the contract seal as its script states; the issuer also by each grant's seal. On v3, the issuer by the grant's seal |
| Services between two companies | Two companies | A framework contract for a year, anchored under section 3 | One grant for each order, each inside the year | Either company, when the termination clause says "either party" |
| Employment | A company and a person | A framework contract for the employment | Grants that let the person, or the person's agent, act on the company's resources | The parties together, or an arbiter, when the clause says so |
| An agreement without a grant | Alice and Bob | A contract with two signatures and an anchor | None | Nothing ends it early; it has no seal |

### 8. The agreed configuration

A renter who is promised a certain agent has no way to hold the operator to
it: the contract names a price and limits, and what actually runs in the
slot is whatever the operator's launcher starts. The decision closes that
by putting the configuration into the contract.

1. A contract under which the platform starts an agent in an agreed
   configuration carries the hash of that configuration's manifest. The
   manifest states what the agent is, and it does so only through three
   things: Curator profiles; Curator skills, which come from the catalog
   or are custom skills that were reviewed; and the systems that the agent
   may use.
2. Both parties sign the contract and with it the hash, so the manifest is
   a term like any other.
3. The platform executes exactly the manifest whose hash the contract
   carries. A launcher that cannot reproduce the hash from what it is about
   to start does not start it.
4. For a rental, the slot launcher composes the agent's runtime context
   from four sources and gives it to the agent read-only: the pinned
   profile of the manifest, the human terms of the contract, the machine
   terms of the grant, and a scope text where the contract has one.

Rules 1 to 4 restate decision C9, with two readings that are the draft's.
Rule 1 takes "the contract" of the decision to be a contract under which
the platform starts an agent. The second sentence of rule 3 reads
"executes exactly it" as a refusal to start.

The draft also says where the hash is required and what happens without
it. Whether a contract carries the hash is a rule of its profile, which
fixes the members (LIP-0018 section 1). The profile of a rental, and of
any other contract under which the platform starts an agent, requires the
member. A reader of such a profile refuses a contract that lacks it, as it
refuses any contract that lacks a required member, and so a launcher never
starts a slot without a hash to reproduce. The profile of a contract that
starts no agent, such as the agreement without a grant of section 7, has
no such member, and section 1 therefore does not ask it of every contract.
The profiles that exist today have no such member, and none of them
changes.

Rule 4 is the counterpart, for a rental, of the authority frame of LIP-0013
section 3.4. A slot serves one grant and lives as long as that grant, so
its context is composed once, when the slot starts, and it cannot outlive
the grant. Under LIP-0006 section 7 the human terms and the scope text in
that context govern the agent's work and no service's effect.

The reference rental path gives a slot no contract text today. The
initial data that a new slot receives is one closed block with a version
number and at most six further members: the booking identifier, the
slot's name, the channel secret, the bearer token for the model, the
address of the model proxy and the hash of its certificate. This is a
reading of the
[bootstrap schema](https://github.com/relux-works/swarma-chain-lab/blob/65bf8aa171bb3ee7b2ab09d96d426d8e5e9f5cbf/experiments/single-use/payloadbootstrap/codec/codec.go#L18-L26)
of the reference laboratory at that commit, and the Link book describes the
same six in its
[chapter on rental](https://github.com/relux-works/swarma-docs/blob/de27b6b008b1ac061bb6ca0b6660e9fa74a2b4f4/link-book/ru/08-arenda.md#L241);
no running slot was inspected for it. The bytes of a manifest, the way a
launcher recomputes its hash, and what "the systems that the agent may
use" lists are open.

## Alternatives

- **One hash over the whole document, without salts,** as today. A party
  then discloses all or nothing, and a short contract can be guessed from
  its hash.
- **A tree of clause commitments in place of the ordered list.** It gives
  shorter proofs for a long contract and needs more structure. Open.
- **The contract in a name value.** A value holds 520 bytes, and the
  landlord and agent shapes are closed.
- **An end that a clause in words triggers,** judged by a model or by a
  service. LIP-0006 section 7 excludes it: ending grants is an effect.
- **A contract seal for Grant v3.** Not taken: v3 stays as it is.

## Security consequences

- **Text binds no machine.** A clause in words is applied by people and by
  agents and is judged afterwards. Only machine members and the seals stop
  anything. Since decision C10 this holds for what a reader shows as
  well: a termination type read from prose can promise an end that the
  seal's script gives to nobody, or hide an end that it gives to the other
  party, so the type is shown from the script alone.
- **A contract without a confirmed seal carries no grant** in the scope
  of section 6 (decision C12). The check closes the gap in which a grant
  was live under a contract that nothing could end as its text promised,
  because the seal that the text named was never created or never
  confirmed. It proves confirmation and script alone: who holds the
  seal's keys, and whether they still exist, no read of the output shows,
  so a seal that nobody can spend passes the check and ends nothing.
- **The contract seal moves power.** Under "either party" the recipient of
  the grants can end them, and so can a thief of either party's seal key.
  The thief ends authority and creates none. Under "both together" a party
  that disappears blocks a common end; the windows still close, and the
  issuer keeps the seal of each grant.
- **A framework contract is one point.** One spend of its seal ends every
  grant under it.
- **An arbiter's key can end a contract.** It cannot issue or widen
  anything.
- **A disclosed clause can mislead** without the clauses that qualify it,
  and the parts other than the clauses are shown with every disclosure.
- **Assent on chain is public.** The identifier reveals nothing of the
  content, but the spend links the two parties' chain keys to one anchor.
- **A lost salt** ends the ability to disclose its clause, and a lost
  contract salt ends the ability to show any of it.

## Conformance impact

None while this LIP is a Draft. A future vector set pairs these controls:

| Valid control | Refusal or invariant |
| --- | --- |
| A grant whose window lies inside the window of its contract, and one whose window equals it | A grant that begins before its contract, and one that ends after it, refuse. |
| A contract of profile `/1` whose window equals the grant's | A `/1` contract with another window refuses as `CONTRACT_MISMATCH`, as today. |
| A contract of three clauses; the second is disclosed with its salt and with the commitments of the other two, and the identifier recomputes | A changed clause, a wrong salt and commitments in another order do not recompute. |
| A v4 grant under a contract whose seal is unspent | The contract seal spent, in the mempool or in a block: every grant under the contract refuses, while the seal of each grant is unspent. |
| A v4 grant under a presented, identifier-valid contract whose named seal is confirmed in the active chain with the named script: the signing service passes this check and a verifier passes it | No seal named; a held transaction only in the mempool; no output at the named index; another script: each gives `CONTRACT_SEAL_MISSING` at both sides, no signature and no admission or closure. A seal confirmed as named and spent is not this code. |
| The same valid control with a conclusive own-node read of the named transaction | The named transaction is unknown to the node, including a pruned confirmed-and-spent transaction, or the read proves nothing: `CONTRACT_SEAL_UNAVAILABLE`, pending, no signature, admission or closure; never infer a missing seal or a spend from that read. |
| The bound contract and its named framework contract are both presented, recompute, and each has its named seal confirmed as named | With the bound contract unchanged, the framework names no seal, has a held mempool-only transaction, no output at the named index, or another script: `CONTRACT_SEAL_MISSING`. Its named transaction is unknown: `CONTRACT_SEAL_UNAVAILABLE`, pending. Neither side signs or admits on any of these negatives; no closure. |
| A minimal landed v3 contract without a framework and without a contract seal remains valid under its existing profile | Applying section 5 rule 7 to refuse that control is forbidden; removing the confirmed seal from an otherwise valid v4 contract instead gives `CONTRACT_SEAL_MISSING`. |
| A contract whose prose and whose seal script give the same termination type: the reader shows that type | Prose or a stored type member that differs from the script never overrides it. With no seal, or a script outside every form of its profile, no type is shown and none is supplied from prose. This remains true after the four script forms are fixed. |
| A termination frame that the signatures on the seal input cover | A frame in another transaction, and one that the signatures do not cover: the contract is ended by the spend, and the frame is no evidence. |
| An anchor that spends the assent output that the contract names | An anchor that spends another output shows no assent on chain; the signatures of the contract stand. |
| A grant under a contract that names a framework contract, all three windows nested | A contract whose window reaches outside its framework contract refuses, and so does a framework contract that names another one. |
| A rental contract whose configuration hash the launcher reproduces from what it is about to start | A manifest that differs in one profile, one skill or one system gives another hash, and the launcher starts nothing. A contract of a profile that requires the hash and carries none is refused, and nothing starts. A contract that starts no agent is valid without the hash. |

## Open questions

- The canonical bytes of the contract, of its identifier, of the two
  commitments and of the termination statement; the length of a salt; the
  signing domains.
- The scripts of the assent output and of the four termination clauses,
  and their fit with the construction profiles W and L of LIP-0008 section
  1.1; the form for more than two parties.
- Whether the parts other than the clauses are salted as well, so that the
  parties are not shown with every disclosure.
- A list or a tree of clause commitments.
- Whether one level of framework contract is enough.
- Which key of a party signs a contract under which no grant is issued.
- The closure that a verifier records for a spent contract seal, which
  belongs to the closure profile of v4 (LIP-0008 section 5.1), and with it
  the step and the code at which an order table reports a confirmed
  contract seal that is spent; section 6, rule 6, assigns
  `CONTRACT_SEAL_MISSING` to a seal that is absent or not confirmed as
  named, and to no spend.
- Whether decision C12 of 2026-11-17 reaches a contract that a Grant v3
  grant binds. Decision C8 says that v3 stays as it is, and sections 5
  and 6 read C12 in the scope of section 6 — v4 grants and framework
  contracts — so a minimal v3 contract needs no contract seal here. If
  the owner meant every grant, the v3 profiles change, and no text says
  how.
- Whether decision C11 leaves a contract under which no grant is issued
  and which is not a framework contract free to
  have no seal, as the last row of section 7 has it, or takes that choice
  away, so that every contract is drafted from a seal and every contract
  has a termination type. Sections 5 and 6 state the first reading and
  keep the case.
- How a node is read for the confirmation and the script of a named
  contract seal against one tip, in the observation of the signing or the
  admission; section 6, rule 6, states the facts that the check needs
  and no read for them, as the reads for other seals are open in their
  profiles.
- Refunds at an early end, which LIP-0011 leaves to the contract.
- How the full framework document is presented or resolved at signing
  and admission, and how its identifier is recomputed with the bound
  contract's under their accepted profiles. The requirement applies to
  both documents; unavailable presentation or recomputation never permits
  signing or admission. For a child, F6(a) and (b) carry these requirements;
  no transport or canonical framework bytes are fixed here.
- How a validated spend of either required contract seal ends an existing
  LIP-0030 session, with its event, verdict, stop path and closure. C6 and
  N1 carry the signing/admission check, not this session-ending event.
- The bytes of a configuration manifest, how a launcher recomputes its
  hash, and the list of systems that an agent may use.
