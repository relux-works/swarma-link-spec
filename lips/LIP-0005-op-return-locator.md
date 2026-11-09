# LIP-0005: OP_RETURN locator — where to find what a hash points to

- **Status:** Draft
- **Created:** 2026-11-08
- **Affects:** issuance (the per-grant on-chain commitment), any future anchor
- **Motivation:** a micro protocol in `OP_RETURN` that says where to go — a blob store,
  BitTorrent, another network — with the hash as the pointer in that place; the pointer may be the grant's own hash or
  an info-hash; inspired by the Memo protocol that the Swarma Forum takes as is.

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
| `0x01` | grant issuance | `version(1) || commitment(32) || locator` |
| `0x02` | anchor batch | `version(1) || batch_commitment(32) || locator` |
| `0x03`-`0x7f` | reserved for Swarma Link | — |
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

Where to fetch is the *location*; which server or tracker is not on chain (it comes from the agent's or landlord's
Namecoin name value, e.g. a `blob` or `tracker` field, so it can change without touching history).

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
3. Bare `6a20<32>`: legacy v0.1 anchor; the 32 bytes are the hash, location unspecified.
4. A Memo output (prefix byte `0x6d`) is not a Swarma Link output and is ignored by Link readers.
5. The pointer is verified after fetching: the fetched bytes must hash to the pointer (type `0x01`) or match the
   torrent's info dictionary (types `0x02`-`0x04`), and the object must hash to the value the commitment binds.

## 4. Effect on the reference implementation

The landlord-grant issuer (LIP-0004) writes action `0x01` with locator type `0x01` (pointer = grant id), replacing the bare
commitment push; the kernel parses per §3. One small delta after K1 lands.

## 5. Open

- Whether the Swarma Forum lists Swarma Link in its protocol id table (so its indexers skip or index it).
- Whether a location hint (e.g. a short server id) is ever worth bytes on chain; proposed: no.
