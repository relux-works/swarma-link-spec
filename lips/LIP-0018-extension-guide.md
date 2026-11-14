# LIP-0018: Extension guide for contract profiles, limit kinds, action names and certificate kinds

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** the process of this repository: what a proposal that extends
  the protocol has to contain
- **Builds on:** LIP-0001, LIP-0007, LIP-0008 sections 2 and 12.3, LIP-0013
  and LIP-0017

## Summary

Four things in this protocol are meant to grow: the profiles of a contract,
the kinds of limit that a grant carries, the names of actions, and the kinds
of key that a certificate statement binds. LIP-0008 says that a new limit
kind arrives through a LIP of its own and that leaf names need their own
profiles. It does not say what such a LIP has to state. A proposal for a
limit that leaves out what happens to a reservation after an uncertain
outcome cannot be implemented the same way by two parties, and nobody
notices until their journals disagree.

This guide lists, for each of them, what a proposal MUST state before
it can be reviewed. The lists record Ivan Oparin's decision of 2026-11-14;
the co-author's agreement is pending. The guide assigns no identifier and
no byte, and it changes no rule of an existing profile.

## Motivation

The existing proposals answer these questions unevenly. LIP-0013 states
every item of its contract profile, with vectors and a checker. LIP-0008
names its limit kinds by meaning and leaves their profiles open. A third
author who adds a profile today has to infer from those two what is
expected. A single list lets an author see what is missing and gives a reviewer
something to count.

## 1. A contract profile

A contract profile fixes the bytes of one kind of contract and its binding
to a grant. LIP-0013 is the worked example; its section numbers stand in
the last column.

| Item | What the proposal states | In LIP-0013 |
| --- | --- | --- |
| Profile identifier | A name and a version. Every change of bytes or of meaning takes a new version. | `swarma-trust-contract/1` |
| Canonical bytes | The members and their order, the encoding rules and the largest size. A reader refuses unless re-encoding the parsed value gives the identical octets. | Section 2.1 |
| Binding to the grant | Which members must equal fields of the grant, how the scope and the limits of the grant follow from the contract or are mirrored by it, and which relation the two windows have: equality or containment (LIP-0017 section 5). | Sections 2.2 and 2.5 |
| Consent tags | For a v3 profile: the values of the four tags of the consent event. | Section 2.4 |
| Refusal codes | One code for each rule, and the order in which a reader reports the first failure. | Sections 2.3 and 2.5 |
| Vectors and checker | Valid contracts with their exact bytes and hashes; invalid ones that are each one defect away from a valid one, with the expected code; a reference checker that recomputes all of them, with tests that catch planted defects. | Section 4 |
| Path | The LIP that carries the profile, the decisions it records, and its adoption under LIP-0001. | The header and the open questions |

A profile that carries a text also says so. LIP-0006 section 7 then
applies: the text governs an agent's work, and whatever an effect depends
on is a machine member.

## 2. A limit kind

A limit kind is one countable resource that a grant can bound for an
executor (LIP-0008 section 2). A proposal for a kind states:

| Item | What the proposal states |
| --- | --- |
| Identifier and resource | The identifier of the kind and the exact resource it counts, with the service, the asset or the system that the resource belongs to. |
| Unit and integer scale | The unit and the scale of the integers that express it. No amount is a floating-point number. |
| Bounds and rounding | The smallest and the largest value, and how a consumption that is not a whole number of units is rounded. |
| Period and aggregation | Whether the limit holds for one request, for a period or for the whole window; whether a period is counted in blocks or in clock time; how consumption adds up inside it. |
| Reservation | When the allowance is reserved in relation to the effect, and what is made durable before the effect. |
| Concurrency | How parallel requests and the replicas of one executor share one allowance. |
| Uncertain outcomes | What happens to a reservation when the outcome of the effect is not known. |
| Replay | What identifies a request, and that a repeated request is charged once. |
| Denials | Whether a refused request consumes any of the allowance. |
| Contract mirror | How the contract states the same limit, so that a mismatch between grant and contract refuses. |
| Defaults | Which default applies inside the signed limit. A default never supplies authority that the grant lacks. |
| Refusal codes | The code of each refusal of the kind. |
| Vectors and checker | Paired valid and refused cases, and the checker that recomputes them. |
| Path | The LIP that carries the kind, and its adoption under LIP-0001. |

Two rules of LIP-0008 section 2 hold for every kind and are not restated by
a proposal: an allowance of zero authorizes nothing, and a limit that is
missing, unknown or contradictory refuses.

## 3. An action leaf name

An action name is one exact leaf of a service's action table (LIP-0007,
LIP-0008 section 12.3). A proposal for a leaf states:

| Item | What the proposal states |
| --- | --- |
| Name | The leaf, in lowercase segments separated by slashes. It matches exactly; a prefix grants nothing. The `swarma/` namespace belongs to the protocol. |
| Service type | The type of service that offers the action. |
| Arguments and targets | The complete typed parameters and targets, which the request signature covers (LIP-0008 section 12.1). |
| Effect or work | Whether the action ends in an effect at a resource or is an agent's work. An effect is authorized by machine members only (LIP-0006 section 7). |
| Limits | The limit kinds that bound the action. |
| Receipt | What the service's receipt states about the effect. |
| Refusal codes, vectors and checker, path | As for a limit kind. |

## 4. A certificate subject kind

A certificate statement binds a key of another system to a name (LIP-0015
section 6). A proposal for a new kind of subject states:

| Item | What the proposal states |
| --- | --- |
| Kind | The identifier of the kind, as it stands in `subject_kind`. |
| Subject | The members of `subject` and their exact bytes: the account or the address in the other system, and the key that is bound. |
| The key in its own system | What the key signs or decrypts there, and which other keys of that system depend on it. |
| Use of the binding | What a receiver on that transport checks against the bound key, and what it then no longer takes from the transport's server. |
| Revocation | That the rules of LIP-0015 section 6 hold unchanged: the statement with the highest `seq` decides, and a later statement ends a binding. A kind adds no rule of its own here. |
| Vectors and checker, path | As for a limit kind. |

A binding gives no authority under any kind.

## What the guide leaves out

It defines no registry and no format of its own. A proposal that follows
it is still a LIP: it passes review and is adopted under LIP-0001. Whether
an identifier is free is decided by the registry of its kind, which for
actions is the one LIP-0007 describes and for limit kinds does not exist
yet.

## Conformance impact

None. The guide concerns proposals and no implementation.

## Open questions

- A registry for limit kinds and for contract profiles, and who assigns an
  identifier.
- Whether the lists become conformance requirements on a proposal, or stay
  guidance for authors and reviewers.
