// Command trustcheck is the reference checker for the LIP-0013 vectors: the
// swarma-trust-contract/1 profile and the kind-8185 instruction envelope.
//
//	trustcheck check <vectors.json>   recompute every vector; exit 0 iff all match
//	trustcheck gen                    print the deterministic vector file
//
// Exit codes: 0 all vectors as expected, 1 at least one mismatch, 2 usage or
// input error. The checker reads no network, node, clock or key file.
package main

import (
	"bytes"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"slices"
)

// VectorFile is the schema of vectors/LIP-0013/trust-vectors.json.
type VectorFile struct {
	Schema         string            `json:"schema"`
	LIP            string            `json:"lip"`
	Note           string            `json:"note"`
	TestKeys       []TestKey         `json:"test_keys"`
	ValidContracts []ValidContract   `json:"valid_contracts"`
	BadContracts   []InvalidContract `json:"invalid_contracts"`
	Bindings       []BindingVector   `json:"bindings"`
	EnvelopeGrants []EnvelopeGrant   `json:"envelope_grants"`
	Envelopes      []EnvelopeVector  `json:"envelopes"`
}

type TestKey struct {
	Name      string `json:"name"`
	Source    string `json:"source"`
	PublicKey string `json:"public_key"`
}

type ValidContract struct {
	ID          string     `json:"id"`
	Claim       string     `json:"claim"`
	Contract    string     `json:"contract"`
	ContractHex string     `json:"contract_hex"`
	SHA256      string     `json:"sha256"`
	Scope       []string   `json:"v3_scope"`
	Budget      int64      `json:"v3_budget"`
	ConsentTags [][]string `json:"consent_tags"`
}

type InvalidContract struct {
	ID       string `json:"id"`
	Claim    string `json:"claim"`
	Contract string `json:"contract"`
	Expect   string `json:"expect"`
}

type BindingVector struct {
	ID          string    `json:"id"`
	Claim       string    `json:"claim"`
	ContractRef string    `json:"contract_ref"`
	Grant       GrantView `json:"grant"`
	Expect      string    `json:"expect"`
}

type EnvelopeGrant struct {
	GrantID     string    `json:"grant_id"`
	ContractRef string    `json:"contract_ref"`
	Grant       GrantView `json:"grant"`
}

type EnvelopeVector struct {
	ID       string   `json:"id"`
	Claim    string   `json:"claim"`
	Event    string   `json:"event"`
	Message  Message  `json:"message"`
	Receiver Receiver `json:"receiver"`
	Expect   string   `json:"expect"`
}

func main() {
	if len(os.Args) == 3 && os.Args[1] == "check" {
		os.Exit(runCheck(os.Args[2], os.Stdout))
	}
	if len(os.Args) == 2 && os.Args[1] == "gen" {
		b, err := Generate()
		if err != nil {
			fmt.Fprintln(os.Stderr, "gen:", err)
			os.Exit(2)
		}
		os.Stdout.Write(b)
		return
	}
	fmt.Fprintln(os.Stderr, "usage: trustcheck check <vectors.json> | trustcheck gen")
	os.Exit(2)
}

func runCheck(path string, out io.Writer) int {
	raw, err := os.ReadFile(path)
	if err != nil {
		fmt.Fprintln(out, "ERROR read:", err)
		return 2
	}
	var vf VectorFile
	dec := json.NewDecoder(bytes.NewReader(raw))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&vf); err != nil {
		fmt.Fprintln(out, "ERROR parse:", err)
		return 2
	}
	total, failed := Check(vf, out)
	fmt.Fprintf(out, "SUMMARY vectors=%d failed=%d\n", total, failed)
	if failed != 0 {
		return 1
	}
	return 0
}

// Check recomputes every vector and reports one line per vector.
func Check(vf VectorFile, out io.Writer) (total, failed int) {
	report := func(kind, id, want, got string) {
		total++
		status := "PASS"
		if want != got || want == "" {
			status = "FAIL"
			failed++
		}
		fmt.Fprintf(out, "%s %s %s want=%s got=%s\n", status, kind, id, want, got)
	}
	ids := map[string]bool{}
	unique := func(id string) string {
		if ids[id] {
			return "DUPLICATE_ID"
		}
		ids[id] = true
		return ""
	}
	if vf.Schema != "swarma-link-spec/lip-0013-vectors/1" {
		report("file", "schema", "swarma-link-spec/lip-0013-vectors/1", vf.Schema)
	}
	for _, k := range vf.TestKeys {
		got := "VALID_KEY"
		if !isPubkey(k.PublicKey) {
			got = "BAD_KEY"
		}
		report("test-key", k.Name, "VALID_KEY", got)
	}
	contracts := map[string][]byte{}
	for _, v := range vf.ValidContracts {
		raw := []byte(v.Contract)
		contracts[v.ID] = raw
		got := unique(v.ID)
		if got == "" {
			got = validContractResult(v, raw)
		}
		report("contract-valid", v.ID, "OK", got)
	}
	for _, v := range vf.BadContracts {
		got := unique(v.ID)
		if got == "" {
			_, got = ParseContract([]byte(v.Contract))
			if got == "" {
				got = "OK"
			}
		}
		report("contract-invalid", v.ID, v.Expect, got)
	}
	for _, v := range vf.Bindings {
		got := unique(v.ID)
		raw, ok := contracts[v.ContractRef]
		if got == "" && !ok {
			got = "UNKNOWN_CONTRACT_REF"
		}
		if got == "" {
			if _, got = Bind(raw, v.Grant); got == "" {
				got = "OK"
			}
		}
		report("binding", v.ID, v.Expect, got)
	}
	store := map[string]StoredGrant{}
	for _, g := range vf.EnvelopeGrants {
		raw, ok := contracts[g.ContractRef]
		if !ok || !isDigest(g.GrantID) {
			report("envelope-grant", g.GrantID, "OK", "BAD_GRANT_ENTRY")
			continue
		}
		store[g.GrantID] = StoredGrant{Grant: g.Grant, Contract: raw}
	}
	for _, v := range vf.Envelopes {
		got := unique(v.ID)
		if got == "" {
			got = AdmitOffline([]byte(v.Event), v.Message, v.Receiver, store)
		}
		report("envelope", v.ID, v.Expect, got)
	}
	return total, failed
}

// validContractResult recomputes bytes, hash, scope, budget and consent tags.
func validContractResult(v ValidContract, raw []byte) string {
	hb, err := hex.DecodeString(v.ContractHex)
	if err != nil || !bytes.Equal(hb, raw) {
		return "HEX_MISMATCH"
	}
	c, code := ParseContract(raw)
	if code != "" {
		return code
	}
	if sha256Hex(raw) != v.SHA256 {
		return "SHA256_MISMATCH"
	}
	if v.Scope == nil || !slices.Equal(V3Scope(c), v.Scope) {
		return "SCOPE_MISMATCH"
	}
	if c.SpendBudget != v.Budget {
		return "BUDGET_MISMATCH"
	}
	if !bytes.Equal(compact(ConsentTags(raw)), compact(v.ConsentTags)) {
		return "CONSENT_TAGS"
	}
	return "OK"
}
