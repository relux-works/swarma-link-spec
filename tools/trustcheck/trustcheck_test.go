package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"slices"
	"strings"
	"testing"

	"github.com/btcsuite/btcd/btcec/v2/schnorr"
)

const vectorPath = "../../vectors/LIP-0013/trust-vectors.json"

func loadVectors(t *testing.T) VectorFile {
	t.Helper()
	raw, err := os.ReadFile(vectorPath)
	if err != nil {
		t.Fatal(err)
	}
	var vf VectorFile
	dec := json.NewDecoder(bytes.NewReader(raw))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&vf); err != nil {
		t.Fatal(err)
	}
	return vf
}

// Claim: the signing path reproduces BIP-340 test vector 0 byte for byte
// (secret key 3, aux_rand 0, message 0), so generated envelope signatures
// follow the standard algorithm. Limit: one published vector, not the suite.
func TestSigningReproducesBIP340Vector0(t *testing.T) {
	sk, err := signerKey(bip340Index0Secret, bip340Index0Public)
	if err != nil {
		t.Fatal(err)
	}
	got, err := signBIP340(sk, make([]byte, 32))
	if err != nil {
		t.Fatal(err)
	}
	want := "e907831f80848d1069a5371b402410364bdf1c5f8307b0084c55f1ce2dca821525f66a4a85ea8b71e482a74f382d2ce5ebeee8fdb2172f477df4900d310536c0"
	if got != want {
		t.Fatalf("signature %s, want %s", got, want)
	}
}

// Claim: both test signers derive the public keys published in the BIP-340
// CSV, and the off-curve key of vector 5 is refused as a key.
func TestTestKeysArePublishedBIP340Keys(t *testing.T) {
	if _, err := signerKey(bip340Index1Secret, bip340Index1Public); err != nil {
		t.Fatal(err)
	}
	if !isPubkey(bip340Index0Public) || !isPubkey(bip340Index1Public) || isPubkey(bip340OffCurvePublic) {
		t.Fatal("key validity does not match the BIP-340 CSV")
	}
}

// Claim: the committed vector file is exactly what the generator produces,
// so the file can be regenerated and reviewed as a diff.
func TestCommittedVectorsEqualGenerator(t *testing.T) {
	raw, err := os.ReadFile(vectorPath)
	if err != nil {
		t.Fatal(err)
	}
	gen, err := Generate()
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(raw, gen) {
		t.Fatal("committed vectors differ from `trustcheck gen` output")
	}
}

// Claim: every committed vector reproduces its expected hash or refusal.
func TestCommittedVectorsPass(t *testing.T) {
	vf := loadVectors(t)
	var out bytes.Buffer
	total, failed := Check(vf, &out)
	if failed != 0 || total < 60 {
		t.Fatalf("total=%d failed=%d\n%s", total, failed, out.String())
	}
}

// Claim (instrument control): the checker fails when one byte of a valid
// contract, its expected hash, an expected refusal or a signed event changes.
// Each plant must produce the named mismatch, not merely any failure. A
// changed contract also fails every binding and envelope that references it;
// the other plants touch one vector only, so exactly one line fails.
func TestCheckerDetectsPlantedDefects(t *testing.T) {
	cases := []struct {
		name  string
		plant func(*VectorFile)
		want  string
		fails int // exact number of failing lines; 0 means "at least one"
	}{
		{"contract byte, hex left as is", func(vf *VectorFile) {
			vf.ValidContracts[0].Contract = strings.Replace(vf.ValidContracts[0].Contract, `"not_after":1797120000`, `"not_after":1797120001`, 1)
		}, "FAIL contract-valid C-V1-instruct-review want=OK got=HEX_MISMATCH", 0},
		{"contract byte, hex changed with it", func(vf *VectorFile) {
			c := strings.Replace(vf.ValidContracts[0].Contract, `"not_after":1797120000`, `"not_after":1797120001`, 1)
			vf.ValidContracts[0].Contract = c
			vf.ValidContracts[0].ContractHex = hex.EncodeToString([]byte(c))
		}, "FAIL contract-valid C-V1-instruct-review want=OK got=SHA256_MISMATCH", 0},
		{"expected hash", func(vf *VectorFile) {
			h := []byte(vf.ValidContracts[1].SHA256)
			h[0] ^= 1
			vf.ValidContracts[1].SHA256 = string(h)
		}, "FAIL contract-valid C-V2-land want=OK got=SHA256_MISMATCH", 1},
		{"expected refusal", func(vf *VectorFile) { vf.BadContracts[0].Expect = "CONTRACT_REPOS" },
			"FAIL contract-invalid C-N01-unsorted-actions want=CONTRACT_REPOS got=CONTRACT_ACTIONS", 1},
		{"signed event", func(vf *VectorFile) {
			vf.Envelopes[0].Event = strings.Replace(vf.Envelopes[0].Event, `"created_at":1794599940`, `"created_at":1794599941`, 1)
		}, "FAIL envelope E-V1-instruct want=PASS got=ENVELOPE_SIGNATURE", 1},
	}
	for _, tc := range cases {
		vf := loadVectors(t)
		tc.plant(&vf)
		var out bytes.Buffer
		_, failed := Check(vf, &out)
		if failed < 1 || (tc.fails > 0 && failed != tc.fails) || !strings.Contains(out.String(), tc.want+"\n") {
			t.Fatalf("%s: failed=%d (want %d), want line %q\n%s", tc.name, failed, tc.fails, tc.want, out.String())
		}
	}
}

// Claim: an empty expectation never counts as a pass, so a vector without
// an expected outcome cannot satisfy the checker.
func TestEmptyExpectationFails(t *testing.T) {
	vf := loadVectors(t)
	vf.BadContracts[0].Expect = ""
	_, failed := Check(vf, io.Discard)
	if failed != 1 {
		t.Fatalf("failed=%d, want 1", failed)
	}
}

// Claim: the profile's fixed digests match an independent recomputation:
// privacy = SHA-256("swarma-trust-privacy-v1") and booking appends the
// 7-byte ASCII suffix to the exact contract bytes.
func TestConsentTagDigests(t *testing.T) {
	raw := []byte(`{"x":1}`)
	tags := ConsentTags(raw)
	if tags[0][1] != "swarma-rental-consent-v1" || tags[1][1] != sha256Hex(raw) ||
		tags[2][1] != sha256Hex([]byte(`{"x":1}booking`)) || tags[3][1] != sha256Hex([]byte("swarma-trust-privacy-v1")) {
		t.Fatalf("unexpected consent tags %v", tags)
	}
}

// Claim: a valid envelope signature verifies with the generic BIP-340
// verifier over the NIP-01 id, independent of ParseEnvelope.
func TestEnvelopeSignatureVerifiesIndependently(t *testing.T) {
	vf := loadVectors(t)
	var e Event
	if err := json.Unmarshal([]byte(vf.Envelopes[0].Event), &e); err != nil {
		t.Fatal(err)
	}
	pb, _ := hex.DecodeString(e.Pubkey)
	pk, err := schnorr.ParsePubKey(pb)
	if err != nil {
		t.Fatal(err)
	}
	sb, _ := hex.DecodeString(e.Sig)
	sig, err := schnorr.ParseSignature(sb)
	if err != nil {
		t.Fatal(err)
	}
	idb, _ := hex.DecodeString(e.ID)
	if !sig.Verify(idb, pk) || e.Pubkey != bip340Index0Public {
		t.Fatal("E-V1 signature does not verify under bip340-0")
	}
}

// Claim: rule 1 (CONTRACT_ENCODING) owns the sign and the character rules of
// section 2.1 for every member: a minus sign on each integer member, and a
// non-ASCII character, a control character or an escape other than \" and \\
// in each string member, refuse as CONTRACT_ENCODING, never as the member's
// value code. Controls: the unmodified contracts parse, a 281-byte ASCII note
// is still CONTRACT_NOTE, a budget above the maximum is still CONTRACT_BUDGET
// and a quote and backslash in note stay valid. Limit: one spelling per
// member and defect, built from the generator's valid contracts.
func TestLexicalRulesRefuseAtRuleOne(t *testing.T) {
	spend := baseContract()
	spend.Actions, spend.SpendBudget = []string{"instruct", "spend"}, vSpendLimit
	land := baseContract()
	land.Actions, land.Repos = []string{"instruct", "land", "review"}, []string{vRepoAlpha}
	expect := func(name string, raw []byte, want string) {
		t.Helper()
		if _, got := ParseContract(raw); got != want {
			t.Errorf("%s: got %q, want %q (%s)", name, got, want, raw)
		}
	}
	for _, c := range []Contract{baseContract(), spend, land} {
		expect("control "+strings.Join(c.Actions, ","), compact(c), "")
	}
	for _, f := range []string{"spend_budget", "not_before", "not_after"} {
		raw := string(compact(spend))
		i := strings.Index(raw, `"`+f+`":`) + len(f) + 3
		expect("sign "+f, []byte(raw[:i]+"-"+raw[i:]), "CONTRACT_ENCODING")
	}
	type mut struct {
		name string
		c    Contract
		f    func(*Contract, string)
	}
	muts := []mut{
		{"profile", baseContract(), func(c *Contract, x string) { c.Profile += x }},
		{"network", baseContract(), func(c *Contract, x string) { c.Network += x }},
		{"landlord_name", baseContract(), func(c *Contract, x string) { c.LandlordName += x }},
		{"agent_name", baseContract(), func(c *Contract, x string) { c.AgentName += x }},
		{"grantee_key", baseContract(), func(c *Contract, x string) { c.GranteeKey += x }},
		{"actions", baseContract(), func(c *Contract, x string) { c.Actions = []string{"instruct", "review" + x} }},
		{"repos", land, func(c *Contract, x string) { c.Repos = []string{vRepoAlpha + x} }},
		{"note", baseContract(), func(c *Contract, x string) { c.Note = "n" + x }},
	}
	for _, m := range muts {
		for _, x := range []string{"é", "\n", "\t", "\x7f", " "} {
			c := m.c
			c.Actions, c.Repos = slices.Clone(m.c.Actions), slices.Clone(m.c.Repos)
			m.f(&c, x)
			expect(fmt.Sprintf("char %q in %s", x, m.name), compact(c), "CONTRACT_ENCODING")
		}
	}
	long := baseContract()
	long.Note = strings.Repeat("a", MaxNoteBytes+1)
	expect("control note 281 ASCII", compact(long), "CONTRACT_NOTE")
	over := spend
	over.SpendBudget = MaxMoney + 1
	expect("control budget above max", compact(over), "CONTRACT_BUDGET")
	quoted := baseContract()
	quoted.Note = `a "quote" and a \ backslash`
	expect("control quote and backslash", compact(quoted), "")
}
