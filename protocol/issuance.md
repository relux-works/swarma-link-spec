# Issuance

This document is normative.

An issuance binds one grant envelope to the owner's name and to one seal. It
takes two transactions: the seal, then the anchor. They cannot be merged: the
anchor names the seal by transaction id, and that id depends on the outputs
of the transaction that creates it.

## 1. Seal

1. The seal is one unspent transaction output that the issuer creates for
   this grant. In v0.1 it MUST pay to the address that currently holds the
   owner name, with a legacy P2PKH script (compressed key).
2. The seal value is not significant to this specification. The v0.1
   experiment used 100000 sat.
3. A verifier requires the seal to have at least one confirmation when it
   observes ([observation](observation.md) §3.4).
4. The issuer SHOULD keep the seal out of automatic coin selection, so that
   only a deliberate revocation spends it.

## 2. Anchor

1. The anchor is a single Namecoin transaction that:
   1. spends the current owner name output and creates the new name output
      with `OP_NAME_UPDATE`, keeping the same owner address;
   2. sets the owner value to the unchanged `keyvault_owner_spki` plus
      `keyvault_certificate_sha256` and `keyvault_seal` for this grant
      ([names](names.md) §2);
   3. contains exactly one output whose script is `6a20` followed by the 32
      bytes of the same certificate SHA-256 (`OP_RETURN` with a 32-byte push),
      with value zero.
2. The anchor MUST NOT spend the seal.
3. The anchor transaction id and the hash of the block that confirms it are
   the anchor pins a verifier uses.

## 3. Order and custody

1. Issuer order (informative, not chain-observable): seal broadcast → seal
   outpoint known → anchor built with that outpoint → anchor broadcast →
   anchor confirmed. Only the confirmations are checked by a verifier.
2. Keys that control the owner name and the seal stay with the issuer's
   custodian. Building, signing and broadcasting are the custodian's acts;
   this specification does not require any party to hold another's keys.

## Limitations

- Only P2PKH seal and name outputs are specified. Segwit, multisig and the
  two-party seals of single-use grants are future work (LIP-0002).
- One grant per owner name at a time: a new anchor replaces the owner value,
  so every grant anchored to the previous generation is closed by the new
  one ([observation](observation.md) §4).
