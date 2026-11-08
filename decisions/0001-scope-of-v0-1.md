# Decision 0001: scope of v0.1

## Context

The first experiment issued a grant over Namecoin mainnet, admitted it on a
verifier that reads a full node, revoked it by spending the seal, and observed
the refusal in the mempool and at the first block. Grant envelopes, message
envelopes and trust policy already have owners in other specifications.

## Decision

v0.1 specifies only what that experiment fixed: name values, the seal and
anchor transactions, the verifier's observation and revocation rules, and the
evidence of the reference run. The grant envelope belongs to keyvault,
message envelopes to waggle, and issuance policy to curator-trust; this
specification refers to them and does not restate them.

## Consequences

v0.1 has one chain (Namecoin), one script type (P2PKH), one grant per owner
name and a full-node verifier. Single-use grants, multi-party seals, light
clients and other chains need their own proposals before they enter the
normative text.
