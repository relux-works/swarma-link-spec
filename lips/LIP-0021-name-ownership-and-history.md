# LIP-0021: Name ownership and history profile for Grant v4 on Namecoin

- **Status:** Draft
- **Created:** 2026-11-14
- **Affects:** how a verifier of Grant v4 decides, on Namecoin, that a pinned
  key controls an output of a name, that the pinned owner wrote a value and
  that a name is live, and how it walks the history of a name
- **Builds on:** LIP-0008 sections 3, 3.1, 4 and 5.2, LIP-0014 section 7.1
  and LIP-0020 section 7.3; relates to LIP-0010 and `protocol/names.md`

## Summary

LIP-0008 binds a grant to the owner key of its issuer's name and has a
verifier check that every output on a stretch of the name's history is
controlled by that key. It does not say how the key is written or which
output scripts one key controls. A verifier cannot compare a pin with an
output until both are fixed, and two verifiers that fix them differently
disagree about whether a name changed hands.

Four other rules wait for the same answer: the owner check of a recipient
by name (LIP-0008 section 3.1), the pins of a notary's name (LIP-0014
section 7.1), the closure for a change of a name that its owner signed
(LIP-0008 section 5.2) and the consent of a recipient by name (LIP-0020
section 7.3).

This LIP proposes the first profile for all five, on Namecoin:

- the node that a verifier reads (section 1);
- the owner pin, a compressed public key (section 2);
- the exact scripts of a name output that a verifier reads, the two address
  scripts that one key controls, and the three outcomes of a reading:
  controlled, another key, unsupported (section 3);
- how a verifier establishes that the pinned owner wrote a value (section
  4);
- when a name is live (section 5);
- the walk of a name's history, its end and its bound (section 6);
- what each of the five rules takes from the profile, with refusal codes
  and an order for the two rules that have none (section 7);
- vectors (section 8).

It changes no rule of the texts that it serves. It proposes what their
words "owner key", "controlled by" and "the history is not available" mean
on Namecoin.

## What is decided and what is proposed

One point that this profile serves is decided, and no rule of the profile
itself is. LIP-0020 section 7 records a decision of 2026-11-14 under Ivan
Oparin's delegation, which he may override and on which the co-author's
agreement is pending: authorisation by name at issuance is judged under the
first ownership profile, a closed list of single-key scripts that is read
on a node with a transaction index. The decision names that kind of
profile. It names neither the form of the pin nor a script of the list.

Every rule of this LIP is the draft's proposal: the pin as a compressed
key, the exact scripts, the three outcomes, the reading of the hash type,
the bound of a walk, and the five codes and the order of section 7. Neither
owner has decided them, and nothing of them is implemented. The owners
accept or change them through this LIP, under LIP-0001.

The rules that the profile serves keep the state that their own texts give
them.

| Rule that the profile serves | Its state |
| --- | --- |
| The issuer rule: the registration, the owner key, the unchanged owner and `swarma`, the walk (LIP-0008 section 3) | Ivan Oparin's decision of 2026-11-11. That the stretch starts at the committed recent block is the choice of that draft and needs confirmation; this profile uses that start and confirms nothing |
| A recipient by key or by name (LIP-0008 section 3.1) | Ivan Oparin's decision of 2026-11-10, as the changelog of version 0.1.13 dates it; the co-author's agreement is pending |
| The pins, the checkpoint and the writer rule of a notary's name (LIP-0014 section 7.1, J3) | Accepted by Ivan Oparin on 2026-11-13; the co-author's agreement is pending |
| The durable closure for a change of the issuer's name that its owner signed (LIP-0008 section 5.2, J6) | Accepted by Ivan Oparin on 2026-11-13; the co-author's agreement is pending |
| The consent of a recipient by name (LIP-0020 section 7.3, W7.6) | The decided point above; the conditions of W7.6 are the proposal of that draft |
| The comparison of keys by their x coordinate (LIP-0014 section 11.1, J4.3) | Decided by Ivan Oparin on 2026-11-14; the co-author's agreement is pending |

The table says which open point each section answers.

| Open point | Proposed here |
| --- | --- |
| LIP-0008 section 3: "Exact key encoding and script coverage remain open", and its open question "Owner-key encoding and supported scripts" | Sections 2 and 3 |
| LIP-0014 section 7.1: the owner pin "in the encoding that LIP-0008 section 3 will fix", and a first owner-proof profile that "accepts `SIGHASH_ALL` without `ANYONECANPAY` only" | Sections 2 and 4 |
| LIP-0020 section 7.3: the evidence output is controlled "under the ownership profile of LIP-0008 section 3, which is open" | Sections 3, 5 and 6 |
| LIP-0008, open questions: whether the issuer rule should also require that the bound owner wrote the `swarma` value in force | Section 4.1 states a proposal and leaves the question open |
| LIP-0008, open questions: "history proofs for a verifier without a full node" | Not proposed. The profile is for a verifier with its own node |

## What can be built from this LIP

| Part | Can be built now | Waits for |
| --- | --- | --- |
| The check of a pin, the reading of an output script against a pin, the writer check on the octets of an unlocking script and of a witness, and the comparison of heights for a live name (sections 2 to 5) | Yes, as functions of octets and heights | The owners' acceptance |
| The walk and the verdicts of section 7, as decisions on stated facts | Yes | The same |
| The reads on a node: the current output of a name and a transaction with the height of its block, all in one observation | No | The observation profile, which is open (LIP-0008 sections 4 and 6), and a run that shows what the pinned build of the node returns |
| The comparison of the `swarma` member along a stretch | Only as an equality of given octets | A rule that says which octets of a value are its `swarma` member. This profile hands a value to the rule as the octets of its push |
| The pin as a member of a grant, of a notary entry or of an agent's pointer | No | The members of those objects (LIP-0020; LIP-0014 section 7.1) |

## Motivation

Three questions have more than one defensible answer, and each answer
changes a verdict.

**How is the key written?** The script that pays a single key commits to a
hash of the key's compressed form, 33 octets with the parity of y in the
first. The x coordinate alone does not determine that hash: the two keys
with one x coordinate hash to different scripts. A pin that held the x
coordinate alone, as a signing key of LIP-0020 does, could not be compared
with an output. A pin that held the hash could not be compared with another
key, and the Draft text of LIP-0014 section 11.1 requires that a delegation
key differ from the owner keys that its parent binds (J4.3).

**Which outputs does the key control?** An output that two of three keys
can spend can be spent with the pinned key and is not controlled by it.
LIP-0008 section 3 says that not every script reduces to one key and that
an unsupported or ambiguous proof refuses. A verifier needs the list of
scripts, and it needs the rule that a script outside the list is no
evidence of a transfer: under the Draft text of LIP-0008 section 5.2 a
verifier that took it for one would close an issuer's grants for good on a
change that nobody proved.

**How far does a walk go?** The walk of LIP-0008 section 3 follows one
operation of the name at a time. A verifier that stops after a fixed number
of steps and reports that it found no change has not walked the stretch,
and a limit that one implementation chose is no rule.

## Current state

- LIP-0008 section 3 says that the exact key encoding and the script
  coverage remain open and that an unsupported or ambiguous proof refuses.
- LIP-0014 section 7.1 writes the owner pin of a notary in "the encoding
  that LIP-0008 section 3 will fix" and states one property of the first
  owner-proof profile: it accepts `SIGHASH_ALL` without `ANYONECANPAY`
  only.
- LIP-0020 covers signing keys and no other key (W3.6). It leaves the form
  of a key that controls an output to the ownership and seal profiles, and
  its W7.6 reads an evidence output under an ownership profile that it
  calls open.
- Grant v3 pins no owner key: a v3 verifier compares the grant key in the
  value of the landlord's name. The reference laboratory, `swarma-chain-lab`
  at `839bdcca41cd17ffd7c4057de2dc88a521745515`, compares the name prefix
  of a name output octet for octet and leaves the rest of the script to its
  node. It holds no v4 code.
- The key map proposes a layout in which a name-owner key has a BIP-84
  address, which pays a witness key hash (`KEY-MAP.md`, "Proposed key
  layout"). Nothing in that layout is decided.

## Proposal

### 1. The node

A verifier makes every read of this profile on its own node, and nothing
that a presenter supplies is an input.

| Rule | Requirement |
| --- | --- |
| O1.1 | The verifier reads its own node, which validates the pinned chain (LIP-0008 section 4) and keeps a transaction index. The node supplies three kinds of fact: the tip of the active chain; for a name, the transaction id and the output index of its current output with the height of the block that holds it, or the fact that the name has no live output; and for a transaction id, the octets of the transaction with the height of the block of the active chain that holds it. A history, a transaction or a height that a presenter supplies is no input. |
| O1.2 | All reads of one check belong to one consistent observation of the node. How that observation is taken is the matter of the observation profile, which is open (LIP-0008 sections 4 and 6). Pending operations enter a check only through LIP-0008 section 5.2 (J6.4), and a verifier reads their scripts as it reads confirmed ones. |
| O1.3 | A node that does not supply a fact of O1.1 has proved nothing. The rule that needed the read refuses, and the refusal is no evidence about the name. |

[LIP-0022](LIP-0022-observation-freshness-and-risk.md) proposes the
observation of O1.2.

### 2. The owner pin

The owner pin is the public key itself in its compressed form, because both
address scripts of section 3 commit to a hash of exactly those 33 octets.

| Rule | Requirement |
| --- | --- |
| O2.1 | An owner pin is a compressed secp256k1 public key, written as 66 lowercase hexadecimal characters. Its form: 66 characters from `0` to `9` and from `a` to `f`, of which the first two are `02` or `03`. Its point: the other 64 characters are the x coordinate of a point of the curve. |
| O2.2 | The pin is the key itself. A hash of the key, an address and an x coordinate alone are no pin. |
| O2.3 | Where a rule compares an owner key with a signing key of LIP-0020, the two are the same key when the 64 characters after the first two of the pin equal the signing key. This is the comparison by x coordinate of the Draft text of LIP-0014 section 11.1 (J4.3). |

A value that does not meet O2.1 is no pin, and the object or the
configuration that holds it refuses. The rule states the form and the point
apart, as LIP-0020 states them for a signing key (W3.6), so that the schema
of an object that carries a pin can report them as it reports its other
members. The code comes with the members of that object; this profile
names none.

The pin holds the whole key for two reasons that pull in different
directions. The address scripts of section 3 commit to a hash of the
compressed key, the parity octet included, so the parity must be in the
pin. And the
rule of LIP-0014 that a delegation key differs from every owner key
compares keys, so a hash would not do. Under this profile every owner pin
is one key, so that comparison can be made on octets, and the case that
J4.3 (c) leaves to custody, an owner pin that is not one key, does not
arise.

### 3. The script of a name output

A verifier parses the octets of an output script itself. It supports three
exact prefixes and two address scripts, and every other script is
unsupported: the rule that needed the reading refuses, and the script
proves nothing about the owner.

The script of a name output is a name prefix followed by an ordinary output
script. The prefix holds the operation, the name and the value, as pushes
that the script drops again; what follows it decides who can spend the
output, and this profile calls it the address script. `P(x)` below is the
shortest push of the octets `x`: the single octet `00` for no octets; one
octet with the length and then `x` for 1 to 75 octets; `4c`, one octet with
the length and then `x` for 76 to 255 octets; `4d`, the length in two
octets with the lower one first and then `x` for 256 to 65535 octets.
Consensus allows a name of at most 255 octets and a value of at most 1023,
so no push of a name operation needs a longer form.

| Rule | Requirement |
| --- | --- |
| O3.1 | The verifier parses the octets of an output script itself and takes them from a transaction that its node supplied (O1.1). Its reading depends on those octets and on nothing that the node or a presenter says about them. |
| O3.2 | A supported prefix is one of three, at the start of the script. An update, which Namecoin calls `name_update`: `53 P(name) P(value) 6d 75`. A registration, `name_firstupdate`: `52 P(name) P(rand) P(value) 6d 6d`. A reservation, `name_new`: `51 P(hash) 6d`, with a hash of 20 octets. The octets after the prefix are the address script. A script that starts with none of the three has no supported prefix. |
| O3.3 | Two address scripts are supported, and both hold the hash of one public key in 20 octets. The key hash: 25 octets, `76 a9 14`, then the 20 octets, then `88 ac`. The witness key hash: 22 octets, `00 14`, then the 20 octets. A pin controls either when the 20 octets are the RIPEMD-160 of the SHA-256 of the 33 octets of the pin. The witness key hash is unsupported in an output that is confirmed below the height from which the pinned chain enforces the witness rules, which is 475000 on the Namecoin main chain. |
| O3.4 | The reading of an output script against a pin has exactly three outcomes. **Controlled:** a supported prefix, and a supported address script with the 20 octets of the pin. **Another key:** a supported prefix, and a supported address script with other 20 octets. **Unsupported:** every other script. |
| O3.5 | An unsupported script is no evidence of a change of owner and none against one. A rule that needed the reading refuses, and nothing is recorded as closed. |

The three prefixes are the ones that Namecoin Core itself writes. Its
parser accepts more. After the pushes it skips any run of the opcodes
`OP_DROP`, `OP_2DROP` and `OP_NOP`, and it does not ask for the shortest
push. A verifier that followed the parser would have to reproduce it octet
for octet, and two verifiers that reproduced it differently would read one
output in two ways. Under O3.2 and O3.3 that cannot happen in the direction
that matters: a script with a supported prefix and a supported address
script is, for that parser, the same operation with the same name, the
same value and the same address script. A script that the parser accepts in
another spelling is unsupported here. Both statements about the parser were
read in its source and not run (section "Sources").

Each of the two address scripts has its reason. The key hash is what the
wallet of Namecoin Core pays a name to unless its caller names another
destination. The witness key hash is what a BIP-84 address pays, and the
key map proposes such an address for a name-owner key. The node's script
verification treats a witness key hash behind a name prefix as it treats
one anywhere else: only a witness with a signature and the key spends it.
Below the height of O3.3 the chain did not enforce that, and anybody could
spend such an output, which is why the rule draws the line there.

"Another key" is a statement about these two scripts. A script that pays
the hash of the uncompressed form of the pinned key has other 20 octets,
and a verifier reads it as another key.

That has a consequence for the owner of a bound name: it pays every output
of the name to a supported address script for its pin. An output that reads
as another key is a change of owner under the rules that use this profile.
Verifiers then refuse the issuer's grants (LIP-0008 section 3), and where
the owner signed the operation, the Draft text of LIP-0008 section 5.2 has
every verifier that validated it close them for good. An unsupported output
is no better for an issuer's grants that exist: it stays on their stretch,
so verifiers refuse every grant whose recent block lies below the block of
the output that replaces it, as nothing proved and without closure. The
owner replaces the output, and the issuer issues those grants again. A
recipient's name is read at its current output alone, so there the refusal
ends with the replacement.

The list is short on purpose, and the cost is that a name whose output is
in another script cannot issue or receive by name under this profile. Each
of these address scripts is unsupported: a script hash, also where it wraps
a witness key hash; a witness script hash; a Taproot output, whose rules
the main chain has not activated; a bare key; a bare multi-signature. A
script with several keys is no candidate for a list of single-key scripts.

A verifier reads a name of every namespace alike under this profile. Which
names a role may use is the rule of that role.

### 4. Who wrote a value

Receiving an output is not consent. LIP-0014 section 7.1 gives the case: a
party that holds a reservation signs the registration of a name with a
value of its own choice and pays the name output to an honest owner, who
signs nothing. A rule that asks only who controls the output passes that
value. The writer check asks who authorized the operation.

| Rule | Requirement |
| --- | --- |
| O4.1 | The operation that created an output is the transaction that holds it. Its name input is its one input that spends an output with a supported prefix: for an update, an update or a registration prefix with the same name; for a registration, a reservation prefix. A fee input is no name input. Where the verifier finds no such input, the check is unsupported. |
| O4.2 | The value of an output was written by the pinned owner when two things hold: the output that the name input spends reads as controlled by the pin (O3.4), and the signature that authorizes the name input has the hash type `SIGHASH_ALL` without `ANYONECANPAY`. |
| O4.3 | The verifier reads the hash type from the name input, in the place that the address script of the spent output fixes. For the key hash the unlocking script is exactly `P(s) P(k)`, and the input has no witness. For the witness key hash the unlocking script is empty, and the witness has exactly two items, `s` and then `k`. In both, `k` is the 33 octets of the pin, and `s` is a signature whose last octet is the hash type. The hash type that O4.2 requires is the octet `01`. The verifier does not verify the signature again: its node validated the transaction. |
| O4.4 | The check has exactly three outcomes. **Written by the owner:** O4.2 holds, read as O4.3 says. **Written by another:** the spent output reads as another key. **Unsupported:** every other case, among them a spent output that is unsupported, an unlocking script or a witness that is not as O4.3 states it, and a hash type that is another octet than `01`. Unsupported is no evidence of either. |

The hash type matters because of what it signs. A signature with the hash
type `01` covers every input and every output of the transaction, the name
output with its value among them. Under `SIGHASH_NONE`, under
`SIGHASH_SINGLE` and under every type with `ANYONECANPAY` somebody else can
change an output or add an input after the owner signed, and the value need
not be the owner's. The octet is the last of the signature because that is
where the node itself takes the hash type from, in an unlocking script and
in a witness alike.

Two rules use the writer check: the value in force of a notary's name
(LIP-0014 section 7.1, J3.4) and the authentication of a change of an
issuer's name (LIP-0008 section 5.2, J6.3). Both are Draft text that awaits
the co-author.

#### 4.1. The issuer's value in force: a proposal that is not the rule

The issuer rule in force asks who controls the outputs of the stretch and
does not ask who wrote the value in force. LIP-0008 lists the question as
open and claims no attack on an issuer: its registration and its owner are
pinned by independently provisioned verifier pins, and the root is
independently trusted.

This draft puts the extension before the owners, to accept or to refuse:
the operation that created the current output of an issuer's name is
written by the bound owner under O4.2 to O4.4, as J3.4 requires of a
notary's name. Its cost is the one that LIP-0014 states for a notary: a
name that another party registered for its owner, or transferred to it,
needs one update that the owner signs before it can issue. Its benefit is
one rule for both kinds of name and no value in force that the pinned owner
never signed.

Until both owners accept the extension, it is no part of the issuer rule.
No rule of this LIP depends on it, and the vectors hold the rule in force,
under which an issuer's name passes whoever wrote its value
(`walk-issuer-16`).

### 5. A live name

A name is live at a block when its current output is confirmed fewer than
`D` blocks below that block, and `D` is 36000 on the Namecoin main chain.

| Rule | Requirement |
| --- | --- |
| O5.1 | A name whose current output is confirmed at height `h` is live at the block of height `H` when `H < h + D`, where `D` is the expiration depth that the consensus rules of the chain give for `H`. At `H = h + D` the name is expired. On the Namecoin main chain `D` is 36000 from height 48000 on; on a regression test chain it is 30. |
| O5.2 | An expired name refuses wherever a rule needs it live (`protocol/names.md`; LIP-0008 section 3). A registration of the same name after an expiry is another registration: a walk from it does not reach the earlier one. |

The comparison is the node's own. An update of a name cannot be confirmed
in a block of height `h + D` or above, and a new registration of the name
can be confirmed from that height on.

### 6. The walk

A walk follows the name inputs back from the current output of a name, one
operation at a time, and ends at a registration. A walk that the verifier
cannot finish proves nothing.

| Rule | Requirement |
| --- | --- |
| O6.1 | A walk starts at the current output of the name. At an output with an update prefix the verifier takes the transaction that holds it, finds its name input (O4.1) and goes to the output that this input spends. An output with a registration prefix ends the walk: its transaction and its output index are what a pin calls the registration. Every output of a walk has a supported prefix and carries, octet for octet, the name that the rule reads. |
| O6.2 | The output that was current at a block of height `R` is the first output of the walk, going back, that is confirmed at a height not above `R`. The stretch from `R` is that output and every later output up to the current one. Where the registration that ends the walk is confirmed above `R`, no output of that registration was current at `R`. |
| O6.3 | A verifier MAY bound the steps of one walk. A step is the examination of one output, so a bound of `n` lets a walk examine `n` outputs, and a walk that ends with the `n`-th of them is complete. A walk that would have to examine a further output, that needs a transaction which the node does not supply, or that meets an output without a supported prefix has proved nothing: the rule that needed it refuses, and the refusal says neither that the name changed nor that it did not. The bound is the operator's. No grant states it, and a limit in the code of one implementation is no rule. |
| O6.4 | A verifier MAY cache the result of a walk, under LIP-0008 section 3 and LIP-0014 section 7.1 (J3.8): a result holds for the predicate that it was computed for, on the active chain up to the cached output. `R` is part of that predicate. |
| O6.5 | After a reorganisation that touches a block of the walked stretch the verifier walks again on the chain that it then validates (LIP-0008 section 3). |

A walk is short for a name that its owner alone updates. LIP-0008 section 3
proposes a renewal about every 220 days, which is fewer than two operations
a year. A name of five years with twenty other updates has about thirty
operations, so a walk to its registration takes about thirty steps. The
bound of O6.3 is there for a name that somebody updates in order to make it
costly to verify, and a walk that it cuts short refuses without a verdict
about the name.

A cache pays for a verifier that checks grants of one issuer again and
again: the next walk reads the operations since the cached output and no
more. It costs a store that the verifier discards after a reorganisation
which touches the cached stretch, and it saves nothing for a predicate that
the verifier has not computed before: another `R`, another pin, or the
notary rule in place of the issuer rule.

### 7. What each rule takes from the profile

Five rules read a name. Three of them have their refusals in their own
texts. For the issuer rule and for a recipient by name LIP-0008 names no
code and no order, and this draft proposes five codes and the order in
which a verifier reports them. No verdict of this section records a
closure.

#### 7.1. The issuer's name at admission

The verifier has the bound name, the bound registration, the bound owner
pin, the octets of the `swarma` member under which the grant was issued,
the height `R` of the committed recent block and the tip of its
observation (LIP-0008 section 3). `R` is the height of a block of the
active chain; that check belongs to LIP-0008 section 7 and not to this
profile. The outputs in view are the outputs that the walk read and that
are confirmed above `R`, together with the first output that it read which
is not confirmed above `R`. Where the walk got that far, they are the
stretch of O6.2.

O7.1. The verifier reports the first row that applies.

| # | Finding | Refusal |
| --- | --- | --- |
| 1 | The name has no live output at the tip (O5.1) | `ISSUER_NAME_CHANGED` |
| 2 | An output in view reads as another key, or carries another `swarma` member than the bound one, or none | `ISSUER_NAME_CHANGED` |
| 3 | The walk ended at another registration than the bound one | `ISSUER_NAME_CHANGED` |
| 4 | The walk ended at the bound registration, and that registration is confirmed above `R` | `ISSUER_SNAPSHOT` |
| 5 | The walk did not end at a registration (O6.3), or an output in view is unsupported, or the node did not supply a fact (O1.3) | `ISSUER_HISTORY_UNAVAILABLE` |
| | None of the five | The rule passes |

| Code | Meaning |
| --- | --- |
| `ISSUER_NAME_CHANGED` | The active chain shows that the name is not the bound issuer's from the recent block on: it is expired, an output in view has another key, an output in view has another `swarma` or none, or the name was registered again. The refusal repeats while the chain shows it (LIP-0008 section 3, rule 5). Under the Draft text of LIP-0008 section 5.2 a verifier that validated an owner-signed change refuses as `ISSUER_NAME_CLOSED` from its journal |
| `ISSUER_SNAPSHOT` | The bound registration is confirmed above the committed recent block: at the block that the grant commits, the name did not exist under this registration |
| `ISSUER_HISTORY_UNAVAILABLE` | Nothing was proved |

The order puts what the chain proved before what the verifier could not
read. A change in view decides although the walk was cut short behind it,
and a missing read never hides it; both refuse, and the first says more. A
verifier MAY end a walk at the first output in view that row 2 refuses,
because no later read changes the code.

An output before the stretch is not judged. Its address script may be
unsupported, and it may have belonged to another key; the walk needs its
prefix and nothing else.

#### 7.2. A recipient by name at admission

The verifier has the name and the owner key that the grant signs, and the
tip of its observation (LIP-0008 sections 3.1 and 4). It reads the current
output of the name and walks nothing.

O7.2. The verifier reports the first row that applies.

| # | Finding | Refusal |
| --- | --- | --- |
| 1 | The name has no live output at the tip | `RECIPIENT_NAME_NOT_HELD` |
| 2 | The current output reads as another key | `RECIPIENT_NAME_NOT_HELD` |
| 3 | The current output is unsupported, or the node did not supply a fact | `RECIPIENT_NAME_UNAVAILABLE` |
| | None of the three | The owner check passes, and the verifier reads the channel key (LIP-0008 section 3.1) |

The rule reads the current output alone. LIP-0008 binds no registration of
a recipient's name, so a name that expired and that the same key registered
again passes, and a transfer and return that the verifier did not observe
passes as well; LIP-0008 section 3 says the second in its own words.

#### 7.3. A notary's name

O7.3. The rules of LIP-0014 section 7.1 take these readings.

| Finding | Rule | Refusal |
| --- | --- | --- |
| The name has no live output at the tip; the walk ended at another registration; an output of the stretch from the checkpoint reads as another key | J3.2 | `NOTARY_NAME_CHANGED` |
| The bound registration is confirmed above the checkpoint, so that the name has no output of that registration at the checkpoint | J3.2 | `NOTARY_CHECKPOINT` |
| The writer check of the operation that created the current output gives "written by another" | J3.4 | `NOTARY_VALUE_UNAUTHORIZED` |
| The writer check is unsupported; an output of the stretch is unsupported; the walk did not end at a registration; the node did not supply a fact | J3.5 | `NOTARY_HISTORY_UNAVAILABLE` |

LIP-0014 puts the checkpoint and the walk before the writer check and
gives no further order among the four codes. This profile adds none, and
no vector of a notary's name holds two findings at once. Whether the
checkpoint block is in the active chain, which J3.2 also asks, is a read of
the observation and not of this profile.

#### 7.4. The consent of a recipient by name

O7.4. A verifier establishes the first four conditions of LIP-0020 W7.6
with these readings.

| Condition of W7.6 at a verifier | Reading |
| --- | --- |
| 1. The evidence transaction is confirmed at a height not above `R` | The height that the node supplies (O1.1) |
| 2. The output is an operation of the signed name, and the name was live at `R` | An update or a registration prefix with that name (O3.2), and O5.1 with `H = R` |
| 3. The output is controlled by the signed owner key | "Controlled" under O3.4, and no other outcome |
| 4. The output was the name's current output at `R` | The walk from the current output of the name meets the evidence output (O6.1), and the output that the walk read just before it is confirmed above `R`; or the evidence output is the current output |

LIP-0020 gives one code, `CONSENT_EVIDENCE`, to a condition that fails and
to a read that proves nothing, so the three outcomes of section 3 do not
show in the code. A walk that the verifier cannot finish before it meets
the evidence output refuses in the same way.

One consequence of condition 4 is not stated in LIP-0020. After the
recipient's name expired and was registered again, the walk from its
current output ends at the new registration and does not meet the evidence
output. The consent then refuses, although the owner check of section 7.2
passes for the same key. A grant by name does not outlive a lapse of its
recipient's name.

#### 7.5. A change of an issuer's name that its owner signed

O7.5. The Draft text of LIP-0008 section 5.2 takes these readings for an
operation that spends an output of a bound issuer's name.

| What J6 asks | Reading |
| --- | --- |
| The spent output is controlled by the bound owner key (J6.1, J6.3) | "Controlled" under O3.4 |
| The signature that authorizes the name input commits to the new name output (J6.3) | "Written by the owner" under O4.4 |
| The new output has another owner (J6.1) | "Another key" under O3.4 |
| An unsupported owner script or signature-hash type (J6.3) | An unsupported spent output, and "unsupported" under O4.4: admission refuses where the read was needed, and no closure is recorded |

A new output that is unsupported shows no other owner. Where its prefix is
supported and its `swarma` member differs from that of the spent output or
is absent, J6.1 makes the operation a break on that ground alone. Where its
`swarma` member is the same, the verifier has validated no break: admission
refuses where the read was needed, and no closure is recorded. Which
pending operations a verifier reads, and when the closure is written, is
J6.4.

### 8. Vectors

[`vectors/LIP-0021/name-vectors.json`](../vectors/LIP-0021/name-vectors.json)
holds 140 vectors over the 27 rules of this LIP, as decisions on stated
octets and stated facts. No vector reads a chain, and none shows what a
node returns.

| Group | Vectors | What a checker does |
| --- | --- | --- |
| `pins` | 3 valid, 9 refused, 3 comparisons | O2.1 on a string, with the part that fails, the form or the point; O2.3 on a pin and a signing key |
| `scripts` | 10 controlled, 4 another key, 25 unsupported | O3.2 to O3.4 on the octets of an output script and a pin, with the height of the block for a witness key hash: the prefix, the name and the value that it holds, the address script and the outcome |
| `writers` | 4 written by the owner, 3 written by another, 17 unsupported | O4.1 to O4.4 on the inputs of an operation: for each input the script of the output that it spends, its unlocking script and its witness |
| `live` | 3 live, 3 expired | O5.1 on two heights and a depth, at both sides of the boundary |
| `walks` | 29 for an issuer, 5 for a recipient, 12 for a consent, 10 for a notary | A rule of section 7 on a history that is given as a list of outputs from the current one back, each with its height, its prefix and its readings |

A vector whose outcome is not the passing one holds one defect, states the
expected outcome and names a neighbour with the passing outcome that
differs from it in that defect. The issuer group also holds five vectors
with two findings each, which state the row of O7.1 that reports first and
name no neighbour. The list `rules` of the file
names for each rule its section, its state, which is `proposed` for all,
its vectors and what no vector covers.

The limits of the file are these. The keys are the compressed forms of the
published test keys of BIP-340 and belong to nobody. Names, values, hashes
and the octets of signatures are placeholders, and no signature in the file
verifies: the writer check reads the last octet of a signature, and the
node that validated the rest is not part of the file. A history states for
each output what the readings of sections 3 and 4 gave; the scripts behind
such readings are in the groups `scripts` and `writers` and not in the
history. No vector holds a pending operation, a closure or a cache.

No checker for these vectors is in this repository. The expected outcomes
were computed by one implementation and decided again, from the octets and
the stated facts, by a second one that shares no code with the first;
neither is published here. Both come from the author of this text, so an
error of understanding that they share is in the vectors. The vectors bind
nothing until both owners accept the rules that they follow.

## Sources

No node was run for this LIP. Its statements about Namecoin come from the
source of Namecoin Core at the tag `nc28.0` and from the reference
laboratory.

| Statement | Source |
| --- | --- |
| The opcodes of the three name operations are `51`, `52` and `53` | Namecoin Core, `src/script/script.h` |
| The node writes the three prefixes as O3.2 states them; its parser skips a run of `OP_DROP`, `OP_2DROP` and `OP_NOP` after the pushes and takes the rest as the address | `src/script/names.cpp`: `GetPrefix` and the constructor of `CNameScript` |
| The node's script builder writes the shortest push, as `P(x)` | `src/script/script.h`, the operator that appends a vector of octets |
| A name has at most 255 octets and a value at most 1023 | `src/names/main.h`; `src/names/main.cpp`, `CheckNameTransaction` |
| A transaction has at most one name input and one name output; the name input of an update is an update or a registration of the same name; the name input of a registration is a reservation whose 20 octets are the hash of `rand` and the name; an update of an expired name is invalid | `src/names/main.cpp`, `CheckNameTransaction` |
| A name last updated at `h` is expired at `H` when `h + D <= H`; `D` is 36000 on the main chain from height 48000 on and 30 on a regression test chain | `src/names/main.cpp`, `isExpired`; `src/consensus/params.h` |
| The script that pays the hash of a public key is the 25 octets of O3.3 | `src/script/solver.cpp`, `MatchPayToPubkeyHash` |
| The node's wallet pays a name output to a key hash unless its caller names another destination | `src/wallet/wallet.h`, `DEFAULT_ADDRESS_TYPE`; `src/wallet/rpc/walletnames.cpp`, the option `destAddress` |
| The node's script verification strips a name prefix before it asks whether a script is a witness program; for one it requires an empty unlocking script, and for a program of 20 octets a witness of exactly two items, which it runs against the hash of a key | `src/script/interpreter.cpp`, `VerifyScript` and `VerifyWitnessProgram`; `src/script/script.cpp`, `IsWitnessProgram` |
| The main chain enforces the witness rules from height 475000 and has not activated Taproot | `src/kernel/chainparams.cpp`, `CMainParams` |
| The hash type is the last octet of a signature; `01` is `SIGHASH_ALL`, and the bit `80` is `ANYONECANPAY` | `src/script/interpreter.cpp`, `CheckECDSASignature`; `src/script/interpreter.h` |
| A client builds an update with the prefix of O3.2, and a verifier can compare that prefix octet for octet | `swarma-chain-lab` at `839bdcca41cd17ffd7c4057de2dc88a521745515`: `experiments/single-use/node.go`, `NameUpdateScript`; `experiments/rental/detached_kernel.go`, `bindAgentNameOutput` |

## Alternatives

- **An x-only pin**, as for signing keys. It is shorter and matches the
  keys of LIP-0020. It does not determine the script of an output, so a
  verifier would have to accept either parity, and the second is a key that
  nobody pinned.
- **A pin of the script hash**, the 20 octets or an address. It compares
  with an output directly. It cannot be compared with another key, and it
  hides which key the owner must keep.
- **The node's own split of a script.** A verifier would take the
  operation, the name and the address from its node's decoding. It would
  then support every spelling that the node's parser accepts, and its
  reading would rest on an interface of the node that this profile would
  have to pin as well. The exact prefixes need the octets of a transaction
  and nothing else.
- **The key hash alone.** It is what the node's wallet writes by default,
  and its spend is read from the unlocking script alone. A name that is
  held as the key map proposes, at a BIP-84 address, could then neither
  issue nor receive by name.
- **A longer list from the start**, with script hashes and scripts of
  several keys. Every entry is a form that two verifiers must read alike
  and that the writer check must cover, and a script of several keys is
  outside what LIP-0008 pins, which is one owner key. The list grows by
  proposals, each with its evidence from a node.
- **Verifying the signature of the name input again.** It would not depend
  on the node's validation. The verifier already rests on its node for the
  chain, and the hash type is the one fact about the signature that the
  node does not report as a verdict.
- **A fixed bound of the walk in the profile.** Every verifier would then
  stop at the same step. A number that suits one deployment cuts off an
  honest long history in another, and a refusal that proves nothing is the
  same at any bound.

## Security consequences

- **A script outside the list is a refusal and nothing else.** A verifier
  that read it as a transfer would close an issuer's grants under the Draft
  text of LIP-0008 section 5.2 on a change that it did not prove. A
  verifier that read it as controlled would accept a key that shares
  control with others.
- **An owner can stop its own grants by paying a name to the wrong
  script.** An update that the owner signs and that pays the name to the
  hash of its uncompressed key, or to any other key hash, reads as a change
  of owner, and one that pays an unsupported script refuses the same grants
  without a verdict about the name. The tool that builds the operations of
  a bound name is the place to prevent both.
- **The witness key hash rests on the witness rules.** Where a chain does
  not enforce them, anybody can spend such an output. O3.3 therefore
  supports the script only from the height at which the pinned chain
  enforces them, and a verifier that applied the profile to another chain
  without that height would read an unprotected output as controlled.
- **The pin shows the key.** An output that pays the hash of a key hides
  the key until it is spent, and the pin publishes it. The margin that the
  hash gives against a break of the curve is gone for that key from the
  moment the pin is published. Nothing else is given away, and after the
  first spend of an output of that key the chain holds the key in any case.
- **The writer check rests on the node.** A node that accepts an invalid
  transaction makes the check pass for a signature that is none. The same
  node is the verifier's source for every other fact about the chain.
- **A walk is work that somebody else can raise.** Whoever holds a name
  can add operations to it. The owner of an issuer's name gains nothing by
  it, and the bound of O6.3 and the cache of O6.4 limit what a verifier
  spends. A previous holder can have left a long history, or an output
  without a supported prefix, between the registration and the outputs of
  the present owner. A name with such an output cannot be bound under this
  profile, and a name whose history is longer than a verifier's bound
  refuses at that verifier; the owner of either registers another name.
- **Nothing here proves an unobserved transfer and return of a recipient's
  name.** LIP-0008 section 3 says so, and under this profile a verifier
  reads only the current output for that rule.

## Conformance impact

None on normative v0.1 and none on Grant v3, which pins no owner key. No
conformance class is added. The cases of LIP-0008 section 5.2 and of
LIP-0014 section 7.1 that name an unsupported owner script or
signature-hash type get their meaning from sections 3 and 4, and they still
run on a node.

## Open questions

- **The owners' acceptance** of the pin as a compressed key, of the three
  prefixes and the two address scripts, of the three outcomes, and of the
  five codes and the order of section 7.
- **The writer check for the issuer rule** (section 4.1), which LIP-0008
  lists as open.
- **The start of the stretch.** LIP-0008 section 3 takes the committed
  recent block and says that the choice needs confirmation. This profile
  takes `R` from that rule.
- **A run on a node.** No node was run for this LIP. That the pinned build
  creates, relays and spends name outputs of both address scripts, and that
  its wallet signs the witness form, is to be shown before an
  implementation claims the profile.
- **The observation.** How one consistent reading of the node is taken,
  which pending operations it holds and how the block of `R` is validated
  belong to the observation profile.
- **The pin in the octets of a grant**, of a notary entry and of an agent's
  pointer, and the code that reports a value which is no pin.
- **The octets of the `swarma` member.** The issuer rule compares them
  along the stretch, and no text says how they are cut out of a value.
- **Other chains.** The profile is Namecoin's. Another chain has its own
  scripts and its own rule of expiry.
- **A verifier without its own node.** LIP-0008 says that a light client
  without proofs for every step refuses. A profile with such proofs is not
  proposed.
