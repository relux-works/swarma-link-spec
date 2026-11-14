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
grant under it.

The LIP records Ivan Oparin's decisions of 2026-11-14; the co-author's
agreement is pending. It proposes semantics without canonical bytes, and
nothing of it is implemented.

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

The eight directions are the owner's. Everything else in this LIP is the
draft's proposal and is not decided: the members of the contract object,
the construction of its identifier, the two action numbers, the checks of a
reader and their order, and the limit of one framework contract above a
contract.

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
| Seal | Optional. The contract's own seal (section 6). |
| Assent output | Optional. The output whose spend shows assent on chain (section 4). |

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
   contract, both ends included, in the measure of the profile. Profile
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
   ends nothing by itself; LIP-0011 says the same of a verdict.

### 6. The contract seal

The contract seal is for v4 grants and for framework contracts. Grant v3
does not change: there the issuer spends the seal of each grant, and
LIP-0011 gives the form of the reason. The grants under a contract are the
grants that bind it and, for a framework contract, the grants whose own
contract names it.

A contract MAY name a seal of its own: an output, given by transaction,
index and script, that is confirmed before the contract is signed. The
script of the seal is the termination clause of the contract:

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
| Rental of an agent | A renter and the operator who rents the agent out | The booking contract, with the price, the period and the limits | One grant for the whole term (LIP-0008 section 2.1) | The issuer, by the seal of the grant |
| Trust between the agents of two owners | A principal and an agent of another owner | A trust contract (LIP-0013) | One grant; under LIP-0014 also child grants | The issuer, by the seal of the grant |
| Services between two companies | Two companies | A framework contract for a year, anchored under section 3 | One grant for each order, each inside the year | Either company, when the termination clause says "either party" |
| Employment | A company and a person | A framework contract for the employment | Grants that let the person, or the person's agent, act on the company's resources | The parties together, or an arbiter, when the clause says so |
| An agreement without a grant | Alice and Bob | A contract with two signatures and an anchor | None | Nothing ends it early; it has no seal |

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
  anything.
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
| A termination frame that the signatures on the seal input cover | A frame in another transaction, and one that the signatures do not cover: the contract is ended by the spend, and the frame is no evidence. |
| An anchor that spends the assent output that the contract names | An anchor that spends another output shows no assent on chain; the signatures of the contract stand. |
| A grant under a contract that names a framework contract, all three windows nested | A contract whose window reaches outside its framework contract refuses, and so does a framework contract that names another one. |

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
  belongs to the closure profile of v4 (LIP-0008 section 5.1).
- Refunds at an early end, which LIP-0011 leaves to the contract.
