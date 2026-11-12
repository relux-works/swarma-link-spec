package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/btcsuite/btcd/btcec/v2"
	"github.com/btcsuite/btcd/btcec/v2/schnorr"
)

// PUBLIC TEST KEYS ONLY. These are the secret keys of BIP-340 test vectors
// 0 and 1 (bitcoin/bips bip-0340/test-vectors.csv), published for testing.
// They are not, and must never become, keys of any real party.
const (
	bip340Index0Secret = "0000000000000000000000000000000000000000000000000000000000000003"
	bip340Index0Public = "f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9"
	bip340Index1Secret = "b7e151628aed2a6abf7158809cf4f3c762e7160f38b4da56a784d9045190cfef"
	bip340Index1Public = "dff1d77f2a671c5f36183726db2341be58feae1da2deced843240f7b502ba659"
	// BIP-340 test vector 5: "public key not on the curve".
	bip340OffCurvePublic = "eefdea4cdb677750a420fee807eacf21eb9898ae79b9768766e4faa04a2d4a34"
)

// Fixed vector parameters.
const (
	vNotBefore  = int64(1794528000) // 2026-11-13T00:00:00Z
	vNotAfter   = int64(1797120000) // 2026-12-13T00:00:00Z
	vNow        = int64(1794600000) // 2026-11-13T20:00:00Z, receiver clock
	vLandlord   = "id/ivanopcode"
	vAgent      = "id/ivanopcode-keeper"
	vRoom       = "!trustroom:matrix.example"
	vSender     = "@grantee:matrix.example"
	vRepoAlpha  = "https://git.example/swarma/alpha"
	vRepoBeta   = "https://git.example/swarma/beta"
	vRepoGamma  = "https://git.example/swarma/gamma"
	vSpendLimit = int64(1000000)
)

func signerKey(secretHex, wantPublic string) (*btcec.PrivateKey, error) {
	b, err := hex.DecodeString(secretHex)
	if err != nil {
		return nil, err
	}
	sk, _ := btcec.PrivKeyFromBytes(b)
	if got := hex.EncodeToString(schnorr.SerializePubKey(sk.PubKey())); got != wantPublic {
		return nil, fmt.Errorf("test key derives %s, want %s", got, wantPublic)
	}
	return sk, nil
}

// signBIP340 signs with aux_rand = 32 zero bytes, the BIP-340 default
// algorithm, so any conforming implementation reproduces the signature.
func signBIP340(sk *btcec.PrivateKey, msg32 []byte) (string, error) {
	sig, err := schnorr.Sign(sk, msg32, schnorr.CustomNonce([32]byte{}))
	if err != nil {
		return "", err
	}
	return hex.EncodeToString(sig.Serialize()), nil
}

func baseContract() Contract {
	return Contract{
		Profile: ProfileID, Network: "main", LandlordName: vLandlord, AgentName: vAgent,
		GranteeKey: bip340Index0Public, Actions: []string{"instruct", "review"}, Repos: []string{},
		SpendBudget: 0, NotBefore: vNotBefore, NotAfter: vNotAfter, Note: "",
	}
}

func grantFor(raw []byte, c Contract) GrantView {
	return GrantView{
		Network: c.Network, AgentName: c.AgentName, LandlordName: c.LandlordName, GranteeKey: c.GranteeKey,
		ContractSHA256: sha256Hex(raw), Scope: V3Scope(c), Budget: c.SpendBudget,
		NotBefore: c.NotBefore, NotAfter: c.NotAfter, ConsentTags: ConsentTags(raw),
	}
}

func placeholderGrantID(name string) string {
	return sha256Hex([]byte("LIP-0013 vector placeholder grant " + name))
}

// Generate builds the complete vector file. Output is deterministic.
func Generate() ([]byte, error) {
	sk0, err := signerKey(bip340Index0Secret, bip340Index0Public)
	if err != nil {
		return nil, err
	}
	sk1, err := signerKey(bip340Index1Secret, bip340Index1Public)
	if err != nil {
		return nil, err
	}
	vf := VectorFile{
		Schema: "swarma-link-spec/lip-0013-vectors/1",
		LIP:    "LIP-0013",
		Note: "Draft vectors for LIP-0013. Keys are BIP-340 published test keys, never real keys. " +
			"Grant ids are placeholders, not issued grants. Envelope outcomes cover the offline steps only; " +
			"PASS still requires a live rental.Check on the receiver's own node.",
		TestKeys: []TestKey{
			{Name: "bip340-0", Source: "BIP-340 test vector index 0 (secret key 3)", PublicKey: bip340Index0Public},
			{Name: "bip340-1", Source: "BIP-340 test vector index 1", PublicKey: bip340Index1Public},
		},
	}

	// Valid contracts.
	type named struct {
		id, claim string
		c         Contract
	}
	c1 := baseContract()
	c2 := baseContract()
	c2.Actions = []string{"instruct", "land", "review"}
	c2.Repos = []string{vRepoAlpha, vRepoBeta}
	c2.Note = "test repositories only"
	c3 := baseContract()
	c3.Actions = []string{"instruct", "spend"}
	c3.SpendBudget = vSpendLimit
	c4 := baseContract()
	c4.Actions = []string{"instruct", "land", "review", "spend"}
	c4.Repos = []string{vRepoAlpha}
	c4.SpendBudget = 50000000
	note := `Boundary note: exactly 280 bytes, with "quotes" and a \ backslash, which are the only escapes. `
	c4.Note = note + strings.Repeat(".", MaxNoteBytes-len(note))
	valid := []named{
		{"C-V1-instruct-review", "instruct and review have no v3 carrier: scope [] and budget 0", c1},
		{"C-V2-land", "land with two sorted repositories maps to scope [repository.push], budget 0", c2},
		{"C-V3-spend", "spend with spend_budget 1000000 maps to scope [pay] and v3 budget 1000000", c3},
		{"C-V4-all-note-280", "all four actions give scope [pay, repository.push]; a note of exactly 280 bytes with quote and backslash is accepted", c4},
	}
	raws := map[string][]byte{}
	contractsByID := map[string]Contract{}
	for _, v := range valid {
		raw := compact(v.c)
		if _, code := ParseContract(raw); code != "" {
			return nil, fmt.Errorf("%s: generator built an invalid contract: %s", v.id, code)
		}
		raws[v.id] = raw
		contractsByID[v.id] = v.c
		vf.ValidContracts = append(vf.ValidContracts, ValidContract{
			ID: v.id, Claim: v.claim, Contract: string(raw), ContractHex: hex.EncodeToString(raw),
			SHA256: sha256Hex(raw), Scope: V3Scope(v.c), Budget: v.c.SpendBudget, ConsentTags: ConsentTags(raw),
		})
	}

	// Invalid contracts: each is one defect applied to a valid contract.
	v1, v2, v3 := string(raws["C-V1-instruct-review"]), string(raws["C-V2-land"]), string(raws["C-V3-spend"])
	rep := func(s, old, new string) string {
		if !strings.Contains(s, old) {
			panic("generator: substring not found: " + old)
		}
		return strings.Replace(s, old, new, 1)
	}
	q := func(s string) string { return `"` + s + `"` }
	const backslash = string(rune(0x5c)) // kept out of literals so no editor folds the escape
	bad := []InvalidContract{
		{"C-N01-unsorted-actions", "actions out of byte order", rep(v1, `["instruct","review"]`, `["review","instruct"]`), "CONTRACT_ACTIONS"},
		{"C-N02-unknown-action", "a v3 scope name is not a profile action", rep(v1, `["instruct","review"]`, `["deliver","instruct"]`), "CONTRACT_ACTIONS"},
		{"C-N03-empty-actions", "actions must be non-empty", rep(v1, `["instruct","review"]`, `[]`), "CONTRACT_ACTIONS"},
		{"C-N04-duplicate-action", "actions are a set", rep(v1, `["instruct","review"]`, `["instruct","instruct"]`), "CONTRACT_ACTIONS"},
		{"C-N05-land-without-repos", "land requires non-empty repos", rep(v1, `["instruct","review"]`, `["instruct","land","review"]`), "CONTRACT_REPOS"},
		{"C-N06-repos-without-land", "repos must be empty without land", rep(v1, `"repos":[]`, `"repos":[`+q(vRepoAlpha)+`]`), "CONTRACT_REPOS"},
		{"C-N07-unsorted-repos", "repos out of byte order", rep(v2, q(vRepoAlpha)+","+q(vRepoBeta), q(vRepoBeta)+","+q(vRepoAlpha)), "CONTRACT_REPOS"},
		{"C-N08-repo-userinfo", "a repository URL with userinfo", rep(v2, q(vRepoAlpha), q("https://user@git.example/swarma/alpha")), "CONTRACT_REPOS"},
		{"C-N09-repo-http", "a repository URL that is not https", rep(v2, q(vRepoAlpha), q("http://git.example/swarma/alpha")), "CONTRACT_REPOS"},
		{"C-N10-spend-without-budget", "spend requires spend_budget > 0", rep(v3, `"spend_budget":1000000`, `"spend_budget":0`), "CONTRACT_BUDGET"},
		{"C-N11-budget-without-spend", "spend_budget must be 0 without spend", rep(v1, `"spend_budget":0`, `"spend_budget":1000`), "CONTRACT_BUDGET"},
		{"C-N12-budget-over-max", "spend_budget above MaxMoney", rep(v3, `"spend_budget":1000000`, `"spend_budget":2100000000000001`), "CONTRACT_BUDGET"},
		{"C-N13-field-order", "profile and network swapped", rep(v1, `"profile":"swarma-trust-contract/1","network":"main"`, `"network":"main","profile":"swarma-trust-contract/1"`), "CONTRACT_ENCODING"},
		{"C-N14-extra-field", "a field outside the profile", rep(v1, `,"note":""}`, `,"note":"","scope":[]}`), "CONTRACT_ENCODING"},
		{"C-N15-duplicate-key", "note appears twice", rep(v1, `,"note":""}`, `,"note":"","note":""}`), "CONTRACT_ENCODING"},
		{"C-N16-missing-field", "note absent", rep(v1, `,"note":""}`, `}`), "CONTRACT_ENCODING"},
		{"C-N17-whitespace", "a space after a colon", rep(v1, `"profile":"`, `"profile": "`), "CONTRACT_ENCODING"},
		{"C-N18-null-repos", "repos is null, not []", rep(v1, `"repos":[]`, `"repos":null`), "CONTRACT_ENCODING"},
		{"C-N19-escaped-spelling", "an escaped spelling of an action name", rep(v1, `["instruct",`, `["`+backslash+`u0069nstruct",`), "CONTRACT_ENCODING"},
		{"C-N20-trailing-newline", "a trailing LF", v1 + "\n", "CONTRACT_ENCODING"},
		{"C-N21-note-281", "note of 281 bytes", rep(v1, `"note":""`, `"note":"`+strings.Repeat("a", MaxNoteBytes+1)+`"`), "CONTRACT_NOTE"},
		{"C-N22-note-non-ascii", "note with a UTF-8 non-ASCII character", rep(v1, `"note":""`, `"note":"caf`+"é"+`"`), "CONTRACT_NOTE"},
		{"C-N23-profile", "another profile string", rep(v1, `swarma-trust-contract/1`, `swarma-trust-contract/2`), "CONTRACT_PROFILE"},
		{"C-N24-window", "not_after equal to not_before", rep(v1, `"not_after":1797120000`, `"not_after":1794528000`), "CONTRACT_FIELD"},
		{"C-N25-grantee-uppercase", "uppercase key hex", rep(v1, bip340Index0Public, strings.ToUpper(bip340Index0Public)), "CONTRACT_FIELD"},
		{"C-N26-grantee-off-curve", "BIP-340 vector 5 key, not on the curve", rep(v1, bip340Index0Public, bip340OffCurvePublic), "CONTRACT_FIELD"},
		{"C-N27-agent-is-landlord", "agent_name equal to landlord_name", rep(v1, q(vAgent), q(vLandlord)), "CONTRACT_FIELD"},
		{"C-N28-network", "a network other than main or regtest", rep(v1, `"network":"main"`, `"network":"testnet"`), "CONTRACT_FIELD"},
	}
	vf.BadContracts = bad

	// Bindings: every valid contract against its matching grant, then defects.
	for _, v := range valid {
		vf.Bindings = append(vf.Bindings, BindingVector{ID: "B-OK-" + v.id[2:], Claim: "the matching v3 grant fields bind", ContractRef: v.id, Grant: grantFor(raws[v.id], v.c), Expect: "OK"})
	}
	mut := func(id, claim, ref, expect string, f func(*GrantView)) {
		g := grantFor(raws[ref], contractsByID[ref])
		f(&g)
		vf.Bindings = append(vf.Bindings, BindingVector{ID: id, Claim: claim, ContractRef: ref, Grant: g, Expect: expect})
	}
	mut("B-N01-budget-mismatch", "v3 budget differs from spend_budget", "C-V3-spend", "BUDGET_MISMATCH", func(g *GrantView) { g.Budget = vSpendLimit - 1 })
	mut("B-N02-budget-absent", "spend contract under a grant with no budget", "C-V3-spend", "BUDGET_MISMATCH", func(g *GrantView) { g.Budget = 0 })
	mut("B-N03-scope-missing-push", "land contract under scope []", "C-V2-land", "SCOPE_MISMATCH", func(g *GrantView) { g.Scope = []string{} })
	mut("B-N04-scope-extra", "a v3 scope entry the contract does not derive", "C-V1-instruct-review", "SCOPE_MISMATCH", func(g *GrantView) { g.Scope = []string{"deliver"} })
	mut("B-N05-grantee", "grant names another grantee key", "C-V1-instruct-review", "CONTRACT_MISMATCH", func(g *GrantView) { g.GranteeKey = bip340Index1Public })
	mut("B-N06-window", "grant not_after differs by one second", "C-V1-instruct-review", "CONTRACT_MISMATCH", func(g *GrantView) { g.NotAfter++ })
	mut("B-N07-agent", "grant names another agent", "C-V1-instruct-review", "CONTRACT_MISMATCH", func(g *GrantView) { g.AgentName = "id/ivanopcode-other" })
	mut("B-N08-hash", "grant commits to another contract", "C-V1-instruct-review", "CONTRACT_HASH", func(g *GrantView) { g.ContractSHA256 = sha256Hex(raws["C-V3-spend"]) })
	mut("B-N09-booking", "booking tag without the booking suffix", "C-V1-instruct-review", "CONSENT_TAGS", func(g *GrantView) { g.ConsentTags[2][1] = sha256Hex(raws["C-V1-instruct-review"]) })
	mut("B-N10-privacy", "privacy tag of another label", "C-V1-instruct-review", "CONSENT_TAGS", func(g *GrantView) { g.ConsentTags[3][1] = sha256Hex([]byte("swarma-rental-privacy-v1")) })
	mut("B-N11-t-tag", "a changed t tag", "C-V1-instruct-review", "CONSENT_TAGS", func(g *GrantView) { g.ConsentTags[0][1] = "swarma-trust-consent-v1" })

	// Envelope grants held by the receiver.
	gIDs := map[string]string{"G1": placeholderGrantID("G1"), "G2": placeholderGrantID("G2"), "G3": placeholderGrantID("G3")}
	for _, e := range []struct{ name, ref string }{{"G1", "C-V1-instruct-review"}, {"G2", "C-V2-land"}, {"G3", "C-V3-spend"}} {
		vf.EnvelopeGrants = append(vf.EnvelopeGrants, EnvelopeGrant{GrantID: gIDs[e.name], ContractRef: e.ref, Grant: grantFor(raws[e.ref], contractsByID[e.ref])})
	}

	type evSpec struct {
		sk        *btcec.PrivateKey
		to, grant string
		action    string
		text      string
		room      string
		mxid      string
		nonce     string
		extra     []string
		createdAt int64
		kind      int
		content   string
	}
	build := func(id string, s evSpec) (Event, error) {
		if s.sk == nil {
			s.sk = sk0
		}
		if s.to == "" {
			s.to = vAgent
		}
		if s.room == "" {
			s.room = vRoom
		}
		if s.mxid == "" {
			s.mxid = vSender
		}
		if s.nonce == "" {
			s.nonce = sha256Hex([]byte("LIP-0013 vector nonce " + id))
		}
		if s.createdAt == 0 {
			s.createdAt = vNow - 60
		}
		if s.kind == 0 {
			s.kind = EnvelopeKind
		}
		tags := [][]string{{"t", EnvelopeTag}, {"to", s.to}, {"grant", s.grant}, {"action", s.action},
			{"body", sha256Hex([]byte(s.text))}, {"room", s.room}, {"mxid", s.mxid}, {"nonce", s.nonce}}
		if s.extra != nil {
			tags = append(tags, s.extra)
		}
		e := Event{Pubkey: hex.EncodeToString(schnorr.SerializePubKey(s.sk.PubKey())), CreatedAt: s.createdAt, Kind: s.kind, Tags: tags, Content: s.content}
		e.ID = EventID(e)
		idb, _ := hex.DecodeString(e.ID)
		sig, err := signBIP340(s.sk, idb)
		if err != nil {
			return e, err
		}
		e.Sig = sig
		return e, nil
	}
	msg := func(text string) Message { return Message{Room: vRoom, Sender: vSender, Text: text} }
	rcv := func() Receiver { return Receiver{AgentName: vAgent, Now: vNow, SeenNonces: []string{}} }
	add := func(id, claim string, e Event, m Message, r Receiver, expect string) {
		vf.Envelopes = append(vf.Envelopes, EnvelopeVector{ID: id, Claim: claim, Event: string(compact(e)), Message: m, Receiver: r, Expect: expect})
	}
	type simple struct {
		id, claim string
		s         evSpec
		expect    string
		mutate    func(*Message, *Receiver)
	}
	const tInstruct = "Run the LIP-0013 checker on main and report the summary line."
	const tReview = "Review verdict for PR 42 at head 0123abc: accept."
	const tLand = "Land PR 7 at its reviewed head into the default branch of alpha."
	const tSpend = "Pay 250000 atoms to the relay operator for November."
	land := func(repo string) []string { return []string{"repo", repo} }
	amount := func(a string) []string { return []string{"amount", a} }
	simples := []simple{
		{"E-V1-instruct", "a signed instruct under G1 passes every offline step", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct}, "PASS", nil},
		{"E-V2-review", "a signed review under G1 passes", evSpec{grant: gIDs["G1"], action: "review", text: tReview}, "PASS", nil},
		{"E-V3-land", "land on a listed repository under G2 passes", evSpec{grant: gIDs["G2"], action: "land", text: tLand, extra: land(vRepoAlpha)}, "PASS", nil},
		{"E-V4-spend", "spend below the budget under G3 passes", evSpec{grant: gIDs["G3"], action: "spend", text: tSpend, extra: amount("250000")}, "PASS", nil},
		{"E-V5-spend-at-budget", "an amount equal to the budget passes", evSpec{grant: gIDs["G3"], action: "spend", text: tSpend, extra: amount("1000000")}, "PASS", nil},
		{"E-V6-window-past-edge", "created_at = now - 900 is inside the window", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, createdAt: vNow - WindowPastSec}, "PASS", nil},
		{"E-V7-window-future-edge", "created_at = now + 120 is inside the window", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, createdAt: vNow + WindowFutureSec}, "PASS", nil},
		{"E-N01-body-text-tampered", "the delivered text differs from the signed body hash", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct}, "BODY_MISMATCH",
			func(m *Message, _ *Receiver) { m.Text = tInstruct + " Then delete the branch." }},
		{"E-N04-wrong-room", "delivered in another room", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct}, "ROOM_MISMATCH",
			func(m *Message, _ *Receiver) { m.Room = "!otherroom:matrix.example" }},
		{"E-N05-wrong-mxid", "delivered by another Matrix sender", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct}, "SENDER_MISMATCH",
			func(m *Message, _ *Receiver) { m.Sender = "@mallory:matrix.example" }},
		{"E-N06-stale", "created_at = now - 901", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, createdAt: vNow - WindowPastSec - 1}, "STALE", nil},
		{"E-N07-future", "created_at = now + 121", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, createdAt: vNow + WindowFutureSec + 1}, "STALE", nil},
		{"E-N08-replayed-nonce", "the nonce is already in the journal", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, nonce: sha256Hex([]byte("LIP-0013 vector nonce E-V1-instruct"))}, "REPLAY",
			func(_ *Message, r *Receiver) {
				r.SeenNonces = []string{sha256Hex([]byte("LIP-0013 vector nonce E-V1-instruct"))}
			}},
		{"E-N09-non-grantee-signer", "validly signed by bip340-1, which is not the grantee", evSpec{sk: sk1, grant: gIDs["G1"], action: "instruct", text: tInstruct}, "GRANTEE_MISMATCH", nil},
		{"E-N10-other-agent", "addressed to another agent", evSpec{to: "id/a1exis-keeper", grant: gIDs["G1"], action: "instruct", text: tInstruct}, "NOT_FOR_ME", nil},
		{"E-N11-unknown-grant", "a grant id the receiver does not hold", evSpec{grant: placeholderGrantID("G9"), action: "instruct", text: tInstruct}, "GRANT_UNKNOWN", nil},
		{"E-N12-action-not-granted", "land under the instruct/review grant G1", evSpec{grant: gIDs["G1"], action: "land", text: tLand, extra: land(vRepoAlpha)}, "ACTION_NOT_GRANTED", nil},
		{"E-N13-repo-not-granted", "land on a repository G2 does not list", evSpec{grant: gIDs["G2"], action: "land", text: tLand, extra: land(vRepoGamma)}, "REPO_NOT_GRANTED", nil},
		{"E-N14-over-budget", "an amount one atom above the budget", evSpec{grant: gIDs["G3"], action: "spend", text: tSpend, extra: amount("1000001")}, "OVER_BUDGET", nil},
		{"E-N15-amount-on-instruct", "an amount tag on an instruct envelope", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, extra: amount("1")}, "ENVELOPE_SHAPE", nil},
		{"E-N16-kind-8183", "the lab renter-request kind is not an envelope", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, kind: 8183}, "ENVELOPE_SHAPE", nil},
		{"E-N17-content", "non-empty content", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct, content: "do it"}, "ENVELOPE_SHAPE", nil},
		{"E-N18-amount-leading-zero", "a non-canonical amount", evSpec{grant: gIDs["G3"], action: "spend", text: tSpend, extra: amount("0250000")}, "ENVELOPE_SHAPE", nil},
	}
	for _, s := range simples {
		e, err := build(s.id, s.s)
		if err != nil {
			return nil, err
		}
		m, r := msg(s.s.text), rcv()
		if s.mutate != nil {
			s.mutate(&m, &r)
		}
		add(s.id, s.claim, e, m, r, s.expect)
	}

	// Tampered body hash with the id left as signed: the id no longer matches.
	tampered := tInstruct + " Then delete the branch."
	e, err := build("E-N02", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct})
	if err != nil {
		return nil, err
	}
	e.Tags[4][1] = sha256Hex([]byte(tampered))
	add("E-N02-body-tag-tampered", "body tag and text replaced together; the NIP-01 id no longer matches", e, msg(tampered), rcv(), "ENVELOPE_SIGNATURE")
	// Tampered body hash with the id recomputed: the signature no longer verifies.
	e.ID = EventID(e)
	add("E-N03-body-tag-tampered-id-recomputed", "body tag and text replaced and the id recomputed; the BIP-340 signature fails", e, msg(tampered), rcv(), "ENVELOPE_SIGNATURE")
	// Tag order changed: body and room swapped.
	e, err = build("E-N19", evSpec{grant: gIDs["G1"], action: "instruct", text: tInstruct})
	if err != nil {
		return nil, err
	}
	e.Tags[4], e.Tags[5] = e.Tags[5], e.Tags[4]
	e.ID = EventID(e)
	idb, _ := hex.DecodeString(e.ID)
	if e.Sig, err = signBIP340(sk0, idb); err != nil {
		return nil, err
	}
	add("E-N19-tag-order", "a correctly signed event whose tags are out of the fixed order", e, msg(tInstruct), rcv(), "ENVELOPE_SHAPE")

	var b bytes.Buffer
	enc := json.NewEncoder(&b)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	if err := enc.Encode(vf); err != nil {
		return nil, err
	}
	return b.Bytes(), nil
}
