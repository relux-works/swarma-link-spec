package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"slices"
	"strconv"

	"github.com/btcsuite/btcd/btcec/v2/schnorr"
)

// Constants of the swarma-instruction-v1 envelope (LIP-0013 section 3).
const (
	EnvelopeKind     = 8185
	EnvelopeTag      = "swarma-instruction-v1"
	WindowPastSec    = 900 // now - 15 min
	WindowFutureSec  = 120 // now + 2 min
	MaxTagValueBytes = 512
	MaxEnvelopeBytes = 16384
)

// requiredTags is the fixed order of the eight tags every envelope carries.
var requiredTags = []string{"t", "to", "grant", "action", "body", "room", "mxid", "nonce"}

// Event is a NIP-01 event in canonical wire field order.
type Event struct {
	ID        string     `json:"id"`
	Pubkey    string     `json:"pubkey"`
	CreatedAt int64      `json:"created_at"`
	Kind      int        `json:"kind"`
	Tags      [][]string `json:"tags"`
	Content   string     `json:"content"`
	Sig       string     `json:"sig"`
}

// Envelope is the parsed tag view of a valid kind-8185 event.
type Envelope struct {
	Event  Event
	To     string
	Grant  string
	Action string
	Body   string
	Room   string
	MXID   string
	Nonce  string
	Amount int64
	Repo   string
}

// EventID is the NIP-01 id: SHA-256 of [0,pubkey,created_at,kind,tags,content].
func EventID(e Event) string {
	return sha256Hex(compact([]any{0, e.Pubkey, e.CreatedAt, e.Kind, e.Tags, e.Content}))
}

// isLowerHex reports exactly n bytes written as 2n lowercase hex digits.
func isLowerHex(s string, n int) bool {
	b, err := hex.DecodeString(s)
	return err == nil && len(b) == n && hex.EncodeToString(b) == s
}

func isMatrixID(s string, sigil byte, needColon bool) bool {
	if len(s) < 2 || len(s) > 255 || s[0] != sigil {
		return false
	}
	colon := false
	for _, c := range []byte(s[1:]) {
		if c <= 0x20 || c > 0x7e {
			return false
		}
		if c == ':' {
			colon = true
		}
	}
	return colon || !needColon
}

// isAmount accepts a canonical positive decimal integer of atoms <= MaxMoney.
func isAmount(s string) (int64, bool) {
	if s == "" || s[0] == '0' || len(s) > 16 {
		return 0, false
	}
	for _, c := range []byte(s) {
		if c < '0' || c > '9' {
			return 0, false
		}
	}
	n, err := strconv.ParseInt(s, 10, 64)
	if err != nil || n < 1 || n > MaxMoney {
		return 0, false
	}
	return n, true
}

// ParseEnvelope applies admission step 3 (LIP-0013 section 3.4): exact shape,
// then the NIP-01 id and the BIP-340 signature.
func ParseEnvelope(raw []byte) (Envelope, string) {
	var env Envelope
	var e Event
	if len(raw) == 0 || len(raw) > MaxEnvelopeBytes {
		return env, "ENVELOPE_SHAPE"
	}
	dec := json.NewDecoder(bytes.NewReader(raw))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&e); err != nil || e.Tags == nil || !bytes.Equal(compact(e), raw) {
		return env, "ENVELOPE_SHAPE"
	}
	if e.Kind != EnvelopeKind || e.Content != "" || e.CreatedAt < 1 || e.CreatedAt > MaxTime ||
		!isDigest(e.ID) || !isPubkey(e.Pubkey) || !isLowerHex(e.Sig, 64) {
		return env, "ENVELOPE_SHAPE"
	}
	if len(e.Tags) != 8 && len(e.Tags) != 9 {
		return env, "ENVELOPE_SHAPE"
	}
	for i, tag := range e.Tags {
		if len(tag) != 2 || len(tag[1]) > MaxTagValueBytes || !isPrintableASCII(tag[0]) || !isPrintableASCII(tag[1]) {
			return env, "ENVELOPE_SHAPE"
		}
		if i < len(requiredTags) && tag[0] != requiredTags[i] {
			return env, "ENVELOPE_SHAPE"
		}
	}
	v := func(i int) string { return e.Tags[i][1] }
	env = Envelope{Event: e, To: v(1), Grant: v(2), Action: v(3), Body: v(4), Room: v(5), MXID: v(6), Nonce: v(7)}
	if v(0) != EnvelopeTag || !isStation(env.To) || !isDigest(env.Grant) || !isDigest(env.Body) ||
		!isMatrixID(env.Room, '!', false) || !isMatrixID(env.MXID, '@', true) || !isDigest(env.Nonce) {
		return env, "ENVELOPE_SHAPE"
	}
	switch env.Action {
	case "instruct", "review":
		if len(e.Tags) != 8 {
			return env, "ENVELOPE_SHAPE"
		}
	case "land":
		if len(e.Tags) != 9 || e.Tags[8][0] != "repo" || !isRepoURL(e.Tags[8][1]) {
			return env, "ENVELOPE_SHAPE"
		}
		env.Repo = e.Tags[8][1]
	case "spend":
		if len(e.Tags) != 9 || e.Tags[8][0] != "amount" {
			return env, "ENVELOPE_SHAPE"
		}
		n, ok := isAmount(e.Tags[8][1])
		if !ok {
			return env, "ENVELOPE_SHAPE"
		}
		env.Amount = n
	default:
		return env, "ENVELOPE_SHAPE"
	}
	if EventID(e) != e.ID {
		return env, "ENVELOPE_SIGNATURE"
	}
	sb, _ := hex.DecodeString(e.Sig)
	sig, err := schnorr.ParseSignature(sb)
	if err != nil {
		return env, "ENVELOPE_SIGNATURE"
	}
	pb, _ := hex.DecodeString(e.Pubkey)
	pk, _ := schnorr.ParsePubKey(pb)
	idb, _ := hex.DecodeString(e.ID)
	if !sig.Verify(idb, pk) {
		return env, "ENVELOPE_SIGNATURE"
	}
	return env, ""
}

// Message is what the authenticated Matrix sync delivered (admission step 1).
type Message struct {
	Room   string `json:"room"`
	Sender string `json:"sender"`
	Text   string `json:"text"`
}

// Receiver is the executor's own view: its name, its clock at receipt and
// its nonce journal.
type Receiver struct {
	AgentName  string   `json:"agent_name"`
	Now        int64    `json:"now"`
	SeenNonces []string `json:"seen_nonces"`
}

// StoredGrant is a bundle held by the receiver, reduced to what the offline
// steps read: the grant fields and the contract bytes.
type StoredGrant struct {
	Grant    GrantView
	Contract []byte
}

// AdmitOffline runs the offline subset of LIP-0013 section 3.4 in order:
// steps 3, 4 and the offline part of step 6. "PASS" means every offline step
// passed; admission still needs a live rental.Check on the receiver's node.
func AdmitOffline(raw []byte, m Message, r Receiver, store map[string]StoredGrant) string {
	env, code := ParseEnvelope(raw)
	if code != "" {
		return code
	}
	switch {
	case env.To != r.AgentName:
		return "NOT_FOR_ME"
	case env.Room != m.Room:
		return "ROOM_MISMATCH"
	case env.MXID != m.Sender:
		return "SENDER_MISMATCH"
	case env.Body != sha256Hex([]byte(m.Text)):
		return "BODY_MISMATCH"
	case env.Event.CreatedAt < r.Now-WindowPastSec || env.Event.CreatedAt > r.Now+WindowFutureSec:
		return "STALE"
	case slices.Contains(r.SeenNonces, env.Nonce):
		return "REPLAY"
	}
	sg, ok := store[env.Grant]
	if !ok {
		return "GRANT_UNKNOWN"
	}
	if sg.Grant.AgentName != r.AgentName {
		return "NOT_FOR_ME"
	}
	if env.Event.Pubkey != sg.Grant.GranteeKey {
		return "GRANTEE_MISMATCH"
	}
	// rental.Check (live/pending/refused on the receiver's own node) runs here
	// in a real admission; it is outside the offline vectors.
	c, code := Bind(sg.Contract, sg.Grant)
	if code != "" {
		return code
	}
	if !slices.Contains(c.Actions, env.Action) {
		return "ACTION_NOT_GRANTED"
	}
	if env.Action == "land" && (!slices.Contains(sg.Grant.Scope, "repository.push") || !slices.Contains(c.Repos, env.Repo)) {
		return "REPO_NOT_GRANTED"
	}
	if env.Action == "spend" && (!slices.Contains(sg.Grant.Scope, "pay") || env.Amount > sg.Grant.Budget) {
		return "OVER_BUDGET"
	}
	return "PASS"
}
