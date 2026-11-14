# LIP-0005: OP_RETURN locator — where to find what a hash points to

- **Status:** Draft
- **Created:** 2026-11-08
- **Affects:** issuance (the per-grant on-chain commitment), any future anchor
- **Motivation:** a micro protocol in `OP_RETURN` that says where to go — a blob store,
  BitTorrent, another network — with the hash as the pointer in that place; the pointer may be the grant's own hash or
  an info-hash; inspired by the Memo protocol that the Swarma Forum takes as is.

This is a draft micro-protocol, not a replacement for normative v0.1 anchors.
The implementation notes below refer to
[`swarma-chain-lab` at `ca074ca645bc69d7bba41e7889504612eaa7f7d4`](https://github.com/relux-works/swarma-chain-lab/tree/ca074ca645bc69d7bba41e7889504612eaa7f7d4/experiments/rental).
They reconcile the landed parser/writer without adopting a new conformance profile.

## 1. Constraints

- **Size.** Namecoin Core 28 relay policy (not consensus) accepts one `OP_RETURN` output whose script is at most 83
  bytes. Writers stay within 83; readers accept any well-formed output found in a block, whatever its size.
- **No clash with Memo.** Memo uses the single prefix byte `0x6d` followed by an action byte (`6d01` name, `6d02`
  post, `6d03` reply, …); the Forum adopts that table as is. Swarma Link therefore uses its **own two-byte protocol id**
  and never the `0x6d` prefix.
- **Legacy.** v0.1 anchors are a bare `6a20<32-byte hash>`; they stay valid and are read as the legacy form.

## 2. Format

Like Memo, the protocol id and the action share one push, and the payload is one more push. Exact bytes:

```
6a                      OP_RETURN
03 53 4c <action>       direct push of 3 bytes: protocol id "SL" (Swarma Link) || action
<n> <payload>           one direct push, 1 <= n <= 75 (opcode byte = n)
```

Readers refuse every other encoding: OP_PUSHDATA1/2/4, a split id, OP_1..OP_16 forms, extra pushes, trailing bytes.

### Actions

| Action | Name | Payload |
| --- | --- | --- |
| `0x01` | grant issuance | `version(1)` \|\| `commitment(32)` \|\| `locator` |
| `0x02` | anchor batch | `version(1)` \|\| `batch_commitment(32)` \|\| `locator` |
| `0x03` | termination for violation, proposed in [LIP-0011](LIP-0011-termination-for-violation.md); the reference parser does not accept it | `version(1)` \|\| `termination_commitment(32)` \|\| `locator` |
| `0x04` | notary attestation, proposed in [LIP-0014](LIP-0014-notary-certified-redelegation.md); the reference parser does not accept it | `version(1)` \|\| `attestation_commitment(32)` \|\| `locator` |
| `0x05` | notary withdrawal for cause, proposed in LIP-0014; the reference parser does not accept it | `version(1)` \|\| `withdrawal_commitment(32)` \|\| `locator` |
| `0x06` | certificate set head, proposed in [LIP-0016](LIP-0016-certificate-store.md); the reference parser does not accept it | `version(1)` \|\| `head_commitment(32)` \|\| `locator` |
| `0x07` | contract anchor, proposed in [LIP-0017](LIP-0017-contracts.md); the reference parser does not accept it | `version(1)` \|\| `contract_commitment(32)` \|\| `locator` |
| `0x08` | contract termination, proposed in LIP-0017; the reference parser does not accept it | `version(1)` \|\| `contract_end_commitment(32)` \|\| `locator` |
| `0x09`-`0x7f` | reserved for Swarma Link | — |
| `0x80`-`0xff` | experimental / private use | — |

`commitment` for `0x01` is the issuance commitment defined by LIP-0004 (landlord grants):
`SHA-256("swarma-issue-v1" || contract_sha256 || consent_event_id || consent_event_sig || landlord_sig || grant_id)`.
`batch_commitment` for `0x02` is LIP-0003's count-bound batch commitment.

### Locator

```
locator = location_type(1) || pointer
```

| Type | Location | Pointer | Pointer length |
| --- | --- | --- | --- |
| `0x00` | none (no locator given) | — | 0 |
| `0x01` | content-addressed blob store (Blossom and compatible) | SHA-256 of the object's bytes (for a grant: its grant id) | 32 |
| `0x02` | BitTorrent v2 (BEP 52) | info-hash (SHA-256 of the info dictionary) | 32 |
| `0x03` | BitTorrent v1 (BEP 3) | info-hash (SHA-1) | 20 |
| `0x04` | Swarma separate BitTorrent network (same BEPs, own DHT; see grant-store note) | v2 info-hash | 32 |
| `0x05`-`0x7f` | reserved for further networks | defined by a later LIP | — |
| `0x80`-`0xff` | experimental / private use | — | — |

The location type describes the retrieval mechanism, not a server or tracker.
Endpoint discovery is separate configuration or future profile work;
[LIP-0019](LIP-0019-retrieval-by-hash.md) proposes a delivery profile for
the blob store. Current
landlord/agent name values have closed schemas: they do not accept `blob` or
`tracker` fields. Their optional Nostr relay hints do not supply a blob/torrent
endpoint or trigger a fetch. No new name field is implied by this format.

Reserved and experimental ranges are allocations for future profiles, not
currently accepted values. The reference parser accepts only the two defined
actions, `0x01` and `0x02`, and the five defined location types, with their
exact pointer lengths. Actions `0x03` to `0x08` are proposals of Draft LIPs.
[LIP-0020](LIP-0020-grant-v4-wire-registry.md) proposes payload version
`0x02` of action `0x01` for the issuance of a v4 grant; the reference parser
does not accept it.

### Sizes

| Locator | Payload | Script |
| --- | --- | --- |
| type `0x00` (none) | 1 + 32 + 1 = 34 | 1 + 4 + 1 + 34 = 40 |
| 32-byte pointer (`0x01`, `0x02`, `0x04`) | 1 + 32 + 1 + 32 = 66 | 1 + 4 + 1 + 66 = **72** |
| 20-byte pointer (`0x03`) | 1 + 32 + 1 + 20 = 54 | 60 |

The payload is always a single direct push of at most 75 bytes; every defined combination fits within 83.

## 3. Reading rules

1. Exactly one `OP_RETURN` output per issuance transaction (as today).
2. `6a 03 534c <action> <n> <payload>`: parse strictly — exactly these two direct pushes, known action, known
   version, known location type, exact pointer length, n = payload length; anything else is refused, never guessed.
3. Exact bare `6a20<32>`: explicit legacy syntax with location unspecified, not
   a fallback for malformed framing. The normative v0.1 profile interprets the
   bytes as its envelope hash; the landlord profile can interpret them as its
   issuance commitment. The caller pins the profile and expected hash.
4. A Memo output (prefix byte `0x6d` in its direct push) is classified as non-Link
   by the generic parser. It does not satisfy an issuance transaction's required
   commitment, and an extra Memo `OP_RETURN` still violates rule 1.
5. The pointer is verified after fetching: the fetched bytes must hash to the pointer (type `0x01`) or match the
   torrent's info dictionary (types `0x02`-`0x04`), and the object must hash to the value the commitment binds.

## 4. Effect on the reference implementation

The landlord-grant issuer now writes action `0x01` with location `0x01`
(pointer = grant id). The script is exactly 72 bytes:

```text
6a 03 53 4c 01 42 01 <commitment:32> 01 <grant_id:32>

offset    contents
0         OP_RETURN (6a)
1         direct push of 3 bytes (03)
2-3       protocol SL (53 4c)
4         issuance action (01)
5         direct push of 66 bytes (42)
6         payload version (01)
7-38      issuance commitment (32 bytes)
39        blob location (01)
40-71     grant_id (32 bytes)
```

The fresh writer and its fee projection use this frame. The landlord matcher
also accepts an exact bare commitment matching LIP-0004 section 4. The completed
plan comparator retains byte/fee/change/size equality for old regtest plans and
framed plans; it does not rewrite a completed record. Legacy projection is
regtest-only. A frame with old fees or a bare script with new fees refuses.

Generic parsing can return either defined action with any defined location.
Landlord issuance accepts only action `0x01`, blob location `0x01` and pointer
equal to the presented `grant_id`, with exactly one zero-value `OP_RETURN` and
no seal input. This acceptance rule is narrower than parser success.

The parser neither fetches the object nor verifies its availability or authority.
Rule 5 describes the check a location-specific retriever needs; it does not
claim the current parser implements such a retriever. The reference delivery
profile takes a complete grant presentation, independently of this locator.

## 5. Open

- Whether the Swarma Forum lists Swarma Link in its protocol id table (so its indexers skip or index it).
- Whether a location hint (e.g. a short server id) is ever worth bytes on chain; proposed: no.
