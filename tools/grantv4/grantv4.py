#!/usr/bin/env python3
"""Reader, vector generator and vector checker for `swarma-grant/4`.

LIP-0020 section 11 fixes the members of a v4 grant. This file is one
implementation of the reader of that section (the pipeline of a signed
object, LIP-0020 W9.1, on a signed grant), with the generator and the
checker of `vectors/LIP-0020/grant-v4.json`.

    python3 -I tools/grantv4/grantv4.py gen   > vectors/LIP-0020/grant-v4.json
    python3 -I tools/grantv4/grantv4.py check vectors/LIP-0020/grant-v4.json

`check` prints one PASS or FINDING line for each vector and a SUMMARY
line. Exit 0: every vector gives its expected result. Exit 1: a finding.
Exit 2: a usage or input error.

One implementation computed the vector file: this one. The generator, the
reader and the checker stand in this file and share its code, so `check`
shows that the file is what this reader gives and nothing more. The
expected results of the groups `valid`, `invalid` and `compound` were
stated by hand in the generator, from the text of section 11, and this
reader decided each of them again. An independent implementation must
recompute, from `signed_form_hex` and `context` alone and with none of
this code:

- for every vector of `valid`: that the pipeline reads it, and its typed
  digest, its identifier, its content address, the verification of its
  signature under the key of the place, and the witness key hash script
  of its seal key;
- for every vector of `invalid` and of `compound`: the first refusal of
  the pipeline, as a code;
- for every vector of `undetermined`: nothing that binds it. Section 11
  carries the rule of such a vector as a proposal of another LIP and does
  not determine whether a reader judges it. This reader judges every rule
  of W11.10 and refuses these vectors as GRANT_DELEGATE; the file states
  `refused` and no code, and `check` accepts any refusal there and
  compares no code. A reader that does not judge the rule reads the same
  octets as a well-formed parent.

`check` does not hold a refused vector against its valid neighbour: it
checks that the neighbour is a valid vector, and the statement that the
two differ in one defect is the generator's.

Only the Python standard library is used. Nothing reads a network, a node,
a clock or a key file. The signer accepts the public test scalars of the
vector file and nothing else; it runs in variable time and is no signer
for real keys. `check` is more than a reader: before it reads the file it
runs the calibration of the generator, which signs three stated values
with public test scalars. It reads at most 16777216 octets of a vector
file and decodes no vector above twice the largest size of a grant.
"""

import hashlib
import json
import sys

GRANT_TYPE = "swarma-grant/4"
MAX_GRANT = 65536
MAX_VECTOR = 2 * MAX_GRANT
MAX_FILE = 16777216
REFUSED = "refused"
UNDETERMINED = "not determined by this version"
MAX_DEPTH = 16
MAX_NUMBER = 9007199254740991
MAX_INDEX = 4294967295
MAX_AMOUNT = 18446744073709551615
MAX_GROUPS = 16
MAX_RANGES = 16
MAX_COINS = 4096
MAX_NOTARIES = 4


class Refusal(Exception):
    def __init__(self, code):
        Exception.__init__(self, code)
        self.code = code


# --------------------------------------------------------------------------
# Hashes

def sha256(b):
    return hashlib.sha256(b).digest()


def tagged_hash(tag, b):
    t = sha256(tag.encode("ascii"))
    return sha256(t + t + b)


def _rol(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


_R1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
       7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
       3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
       1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
       4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
_R2 = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
       6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
       15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
       8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
       12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
_S1 = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
       7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
       11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
       11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
       9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
_S2 = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
       9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
       9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
       15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
       8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
_K1 = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
_K2 = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]


def _f(j, x, y, z):
    if j < 16:
        return x ^ y ^ z
    if j < 32:
        return (x & y) | (~x & 0xFFFFFFFF & z)
    if j < 48:
        return (x | (~y & 0xFFFFFFFF)) ^ z
    if j < 64:
        return (x & z) | (y & ~z & 0xFFFFFFFF)
    return x ^ (y | (~z & 0xFFFFFFFF))


def ripemd160(msg):
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    m = msg + b"\x80" + b"\x00" * ((55 - len(msg)) % 64)
    m += (8 * len(msg)).to_bytes(8, "little")
    for off in range(0, len(m), 64):
        x = [int.from_bytes(m[off + 4 * i:off + 4 * i + 4], "little")
             for i in range(16)]
        a1, b1, c1, d1, e1 = h
        a2, b2, c2, d2, e2 = h
        for j in range(80):
            t = (a1 + _f(j, b1, c1, d1) + x[_R1[j]] + _K1[j // 16]) & 0xFFFFFFFF
            t = (_rol(t, _S1[j]) + e1) & 0xFFFFFFFF
            a1, e1, d1, c1, b1 = e1, d1, _rol(c1, 10), b1, t
            t = (a2 + _f(79 - j, b2, c2, d2) + x[_R2[j]] + _K2[j // 16]) & 0xFFFFFFFF
            t = (_rol(t, _S2[j]) + e2) & 0xFFFFFFFF
            a2, e2, d2, c2, b2 = e2, d2, _rol(c2, 10), b2, t
        t = (h[1] + c1 + d2) & 0xFFFFFFFF
        h[1] = (h[2] + d1 + e2) & 0xFFFFFFFF
        h[2] = (h[3] + e1 + a2) & 0xFFFFFFFF
        h[3] = (h[4] + a1 + b2) & 0xFFFFFFFF
        h[4] = (h[0] + b1 + c2) & 0xFFFFFFFF
        h[0] = t
    return b"".join(v.to_bytes(4, "little") for v in h)


def witness_key_hash_script(compressed_hex):
    """LIP-0024 E1.2: 00 14 and the RIPEMD-160 of the SHA-256 of the key."""
    return "0014" + ripemd160(sha256(bytes.fromhex(compressed_hex))).hex()


# --------------------------------------------------------------------------
# secp256k1 and BIP-340

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def _add(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = 3 * a[0] * a[0] * pow(2 * a[1], P - 2, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], P - 2, P) % P
    x = (lam * lam - a[0] - b[0]) % P
    return (x, (lam * (a[0] - x) - a[1]) % P)


def _mul(k, pt):
    r = None
    while k:
        if k & 1:
            r = _add(r, pt)
        pt = _add(pt, pt)
        k >>= 1
    return r


def lift_x(x):
    """The point with x coordinate `x` and an even y, or None."""
    if x >= P:
        return None
    c = (pow(x, 3, P) + 7) % P
    y = pow(c, (P + 1) // 4, P)
    if y * y % P != c:
        return None
    return (x, y if y % 2 == 0 else P - y)


def xonly(secret):
    return _mul(secret, G)[0].to_bytes(32, "big").hex()


def compressed(secret):
    x, y = _mul(secret, G)
    return ("02" if y % 2 == 0 else "03") + x.to_bytes(32, "big").hex()


def bip340_sign(secret, msg, aux):
    """Default signing of BIP-340, with a verification of the result."""
    pt = _mul(secret, G)
    d = secret if pt[1] % 2 == 0 else N - secret
    px = pt[0].to_bytes(32, "big")
    t = (d ^ int.from_bytes(tagged_hash("BIP0340/aux", aux), "big")).to_bytes(32, "big")
    k0 = int.from_bytes(tagged_hash("BIP0340/nonce", t + px + msg), "big") % N
    if k0 == 0:
        raise ValueError("nonce")
    r = _mul(k0, G)
    k = k0 if r[1] % 2 == 0 else N - k0
    rx = r[0].to_bytes(32, "big")
    e = int.from_bytes(tagged_hash("BIP0340/challenge", rx + px + msg), "big") % N
    sig = rx + ((k + e * d) % N).to_bytes(32, "big")
    if not bip340_verify(px.hex(), msg, sig):
        raise ValueError("signature does not verify")
    return sig


def bip340_verify(key_hex, msg, sig):
    """Strict verification of BIP-340 (LIP-0020 W5.2)."""
    if len(sig) != 64:
        return False
    pk = lift_x(int(key_hex, 16))
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    if pk is None or r >= P or s >= N:
        return False
    e = int.from_bytes(tagged_hash(
        "BIP0340/challenge", sig[:32] + bytes.fromhex(key_hex) + msg), "big") % N
    rp = _add(_mul(s, G), _mul(N - e, pk))
    return rp is not None and rp[1] % 2 == 0 and rp[0] == r


# --------------------------------------------------------------------------
# The document step (LIP-0020 W1.1 to W1.6, in the order of W9.2)

class Node:
    """kind: 'o' object, 'a' array, 's' string, 'n' number, 'b' boolean."""

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def get(self, name):
        if self.kind == "o":
            for k, v in self.value:
                if k == name:
                    return v
        return None

    def names(self):
        return [k for k, _ in self.value]


class _Parser:
    def __init__(self, b):
        self.b = b
        self.i = 0
        self.duplicate = False
        self.null = False
        self.bad_number = False
        self.bad_string = False

    def fail(self):
        raise Refusal("WIRE_JSON")

    def peek(self):
        return self.b[self.i] if self.i < len(self.b) else -1

    def space(self):
        while self.peek() in (0x20, 0x09, 0x0A, 0x0D):
            self.i += 1

    def document(self):
        self.space()
        if self.peek() != 0x7B:
            self.fail()
        v = self.value(1)
        self.space()
        if self.i != len(self.b):
            self.fail()
        return v

    def value(self, depth):
        c = self.peek()
        if c == 0x7B or c == 0x5B:
            if depth > MAX_DEPTH:
                raise Refusal("WIRE_SIZE")
            return self.object(depth) if c == 0x7B else self.array(depth)
        if c == 0x22:
            return Node("s", self.string())
        if c == 0x2D or 0x30 <= c <= 0x39:
            return self.number()
        for word, node in ((b"true", ("b", True)), (b"false", ("b", False)),
                           (b"null", ("z", None))):
            if self.b[self.i:self.i + len(word)] == word:
                self.i += len(word)
                if node[0] == "z":
                    self.null = True
                return Node(*node)
        self.fail()

    def object(self, depth):
        self.i += 1
        members, seen = [], set()
        self.space()
        if self.peek() == 0x7D:
            self.i += 1
            return Node("o", members)
        while True:
            self.space()
            if self.peek() != 0x22:
                self.fail()
            name = self.string()
            if name in seen:
                self.duplicate = True
            seen.add(name)
            self.space()
            if self.peek() != 0x3A:
                self.fail()
            self.i += 1
            self.space()
            members.append((name, self.value(depth + 1)))
            self.space()
            c = self.peek()
            if c == 0x7D:
                self.i += 1
                return Node("o", members)
            if c != 0x2C:
                self.fail()
            self.i += 1

    def array(self, depth):
        self.i += 1
        items = []
        self.space()
        if self.peek() == 0x5D:
            self.i += 1
            return Node("a", items)
        while True:
            self.space()
            items.append(self.value(depth + 1))
            self.space()
            c = self.peek()
            if c == 0x5D:
                self.i += 1
                return Node("a", items)
            if c != 0x2C:
                self.fail()
            self.i += 1

    def digits(self):
        start = self.i
        while 0x30 <= self.peek() <= 0x39:
            self.i += 1
        return self.i > start

    def number(self):
        start = self.i
        plain = True
        if self.peek() == 0x2D:
            plain = False
            self.i += 1
        if self.peek() == 0x30:
            self.i += 1
        elif 0x31 <= self.peek() <= 0x39:
            self.digits()
        else:
            self.fail()
        if self.peek() == 0x2E:
            plain = False
            self.i += 1
            if not self.digits():
                self.fail()
        if self.peek() in (0x45, 0x65):
            plain = False
            self.i += 1
            if self.peek() in (0x2B, 0x2D):
                self.i += 1
            if not self.digits():
                self.fail()
        if 0x30 <= self.peek() <= 0x39:
            self.fail()
        token = self.b[start:self.i].decode("ascii")
        if not plain or len(token) > 16 or int(token) > MAX_NUMBER:
            self.bad_number = True
            return Node("n", None)
        return Node("n", int(token))

    def hex4(self):
        h = self.b[self.i:self.i + 4]
        if len(h) != 4 or any(c not in b"0123456789abcdefABCDEF" for c in h):
            self.fail()
        self.i += 4
        return int(h, 16)

    def string(self):
        self.i += 1
        out = []
        simple = {0x22: '"', 0x5C: "\\", 0x2F: "/", 0x62: "\b",
                  0x66: "\f", 0x6E: "\n", 0x72: "\r", 0x74: "\t"}
        while True:
            c = self.peek()
            if c < 0x20:
                self.fail()
            self.i += 1
            if c == 0x22:
                return "".join(out)
            if c == 0x5C:
                e = self.peek()
                if e in simple:
                    self.i += 1
                    if ord(simple[e]) < 0x20:
                        self.bad_string = True
                    out.append(simple[e])
                elif e == 0x75:
                    self.i += 1
                    u = self.hex4()
                    if 0xD800 <= u <= 0xDBFF and self.b[self.i:self.i + 2] == b"\\u":
                        save = self.i
                        self.i += 2
                        lo = self.hex4()
                        if 0xDC00 <= lo <= 0xDFFF:
                            u = 0x10000 + ((u - 0xD800) << 10) + (lo - 0xDC00)
                        else:
                            self.i = save
                    if u < 0x20 or 0xD800 <= u <= 0xDFFF:
                        self.bad_string = True
                    out.append(chr(u))
                else:
                    self.fail()
            elif c < 0x80:
                out.append(chr(c))
            else:
                n = 1 if 0xC2 <= c <= 0xDF else 2 if 0xE0 <= c <= 0xEF else \
                    3 if 0xF0 <= c <= 0xF4 else 0
                seq = self.b[self.i - 1:self.i + n]
                try:
                    if n == 0 or len(seq) != n + 1:
                        raise ValueError
                    ch = seq.decode("utf-8", "strict")
                except ValueError:
                    self.fail()
                self.i += n
                out.append(ch)


def _utf16(s):
    return s.encode("utf-16-be", "surrogatepass")


def _write_string(s):
    return b'"' + s.replace("\\", "\\\\").replace('"', '\\"').encode("utf-8") + b'"'


def serialize(node):
    """The RFC 8785 serialization of a value that W1.4 and W1.5 admit."""
    if node.kind == "o":
        members = sorted(node.value, key=lambda m: _utf16(m[0]))
        return b"{" + b",".join(
            _write_string(k) + b":" + serialize(v) for k, v in members) + b"}"
    if node.kind == "a":
        return b"[" + b",".join(serialize(v) for v in node.value) + b"]"
    if node.kind == "s":
        return _write_string(node.value)
    if node.kind == "n":
        return str(node.value).encode("ascii")
    return b"true" if node.value else b"false"


def parse_document(b, limit):
    if len(b) > limit:
        raise Refusal("WIRE_SIZE")
    p = _Parser(b)
    root = p.document()
    for flag, code in ((p.duplicate, "WIRE_DUPLICATE"), (p.null, "WIRE_VALUE"),
                       (p.bad_number, "WIRE_NUMBER"), (p.bad_string, "WIRE_STRING")):
        if flag:
            raise Refusal(code)
    if serialize(root) != b:
        raise Refusal("WIRE_NOT_CANONICAL")
    return root


# --------------------------------------------------------------------------
# The member step (LIP-0020 W9.3) on the schema of section 11
#
# A leaf is ("leaf", form, range, point): `form` refuses as WIRE_MEMBER,
# `range` as WIRE_INTEGER and `point` as WIRE_KEY.

HEX = "0123456789abcdef"


def _is_hex(s, n):
    return len(s) == n and all(c in HEX for c in s)


def _text(limit):
    def form(node):
        return node.kind == "s" and 1 <= len(node.value) <= limit and \
            all(0x20 <= ord(c) <= 0x7E for c in node.value)
    return ("leaf", form, None, None)


def _hex(n):
    return ("leaf", lambda node: node.kind == "s" and _is_hex(node.value, n), None, None)


def _number(low, high):
    return ("leaf", lambda node: node.kind == "n",
            lambda node: low <= node.value <= high, None)


def _amount(s):
    grammar = s == "0" or (s != "" and s[0] in "123456789" and
                           all(c in "0123456789" for c in s))
    return grammar and len(s) <= 20 and int(s) <= MAX_AMOUNT


AMOUNT = ("leaf", lambda node: node.kind == "s", lambda node: _amount(node.value), None)
SIGNING_KEY = ("leaf", lambda node: node.kind == "s" and _is_hex(node.value, 64), None,
               lambda node: lift_x(int(node.value, 16)) is not None)
OUTPUT_KEY = ("leaf", lambda node: node.kind == "s" and _is_hex(node.value, 66) and
              node.value[:2] in ("02", "03"), None,
              lambda node: lift_x(int(node.value[2:], 16)) is not None)
SCRIPT = ("leaf", lambda node: node.kind == "s" and 2 <= len(node.value) <= 200 and
          len(node.value) % 2 == 0 and all(c in HEX for c in node.value), None, None)
TRUE = ("leaf", lambda node: node.kind == "b" and node.value is True, None, None)
TEXT = _text(255)
SHORT = _text(32)
HASH = _hex(64)
HEIGHT = _number(0, MAX_NUMBER)
INDEX = _number(0, MAX_INDEX)


def _obj(choose):
    """choose(names) gives (required names, optional names, {name: schema})."""
    return ("obj", choose)


def _arr(elem, low, high):
    return ("arr", elem, low, high)


OUTPOINT = _obj(lambda names: (["txid", "vout"], [], {"txid": HASH, "vout": INDEX}))
PIN = {"name": TEXT, "owner": OUTPUT_KEY, "registration": OUTPOINT}
PIN_OBJ = _obj(lambda names: (["name", "owner", "registration"], [], PIN))
ISSUER = _obj(lambda names: (["grant_key", "name", "owner", "registration"], [],
                             dict(PIN, grant_key=SIGNING_KEY)))
EXECUTOR = _obj(lambda names: (["key", "name"], [], {"key": SIGNING_KEY, "name": TEXT}))
LIMIT_MEMBERS = {"amount": AMOUNT, "kind": TEXT, "period": TEXT,
                 "resource": TEXT, "unit": TEXT}
LIMIT = _obj(lambda names: (["amount", "kind", "resource", "unit"], ["period"], LIMIT_MEMBERS))
LIMITS = _arr(LIMIT, 0, None)
ACTIONS = _arr(TEXT, 0, None)
BY_KEY = (["key"], [], {"key": SIGNING_KEY})
BY_NAME = (["name", "owner"], [], {"name": TEXT, "owner": OUTPUT_KEY})
BY_CLASS = (["class"], [], {"class": _arr(PIN_OBJ, 1, None)})
RECIPIENT = _obj(lambda names: BY_KEY if "key" in names else BY_NAME)
ROW_RECIPIENT = _obj(lambda names: BY_CLASS if "class" in names else
                     BY_KEY if "key" in names else BY_NAME)
SEAL = _obj(lambda names: (["construction", "key", "kind", "outpoint"], [],
                           {"construction": SHORT, "key": OUTPUT_KEY, "kind": SHORT,
                            "outpoint": OUTPOINT}))
STOP = _obj(lambda names: (["first", "script", "txid"], [],
                           {"first": INDEX, "script": SCRIPT, "txid": HASH}))
RANGE = _obj(lambda names: (["count", "first", "script", "txid"], ["stop"],
                            {"count": _number(1, MAX_COINS), "first": INDEX,
                             "script": SCRIPT, "stop": STOP, "txid": HASH}))
TEMPLATE_MEMBERS = {"certifier": TEXT, "executor": EXECUTOR, "limits": LIMITS,
                    "no_certifier": TRUE, "recipient": ROW_RECIPIENT}
TEMPLATE = _obj(lambda names: (
    ["executor", "limits", "no_certifier", "recipient"] if "no_certifier" in names else
    ["certifier", "executor", "limits", "recipient"], [], TEMPLATE_MEMBERS))
GROUP = _obj(lambda names: (["ranges", "template"], [],
                            {"ranges": _arr(RANGE, 1, MAX_RANGES), "template": TEMPLATE}))
DELEGATE = _obj(lambda names: (
    ["actions", "groups", "key", "notaries", "pools"], ["child_seal_key"],
    {"actions": ACTIONS, "child_seal_key": OUTPUT_KEY,
     "groups": _arr(GROUP, 1, MAX_GROUPS), "key": SIGNING_KEY,
     "notaries": _arr(PIN_OBJ, 0, MAX_NOTARIES), "pools": LIMITS}))
COMMON = {"actions": ACTIONS, "contract": HASH, "executor": EXECUTOR, "genesis": HASH,
          "limits": LIMITS, "not_after_height": HEIGHT, "not_before_height": HEIGHT,
          "recent_block": HASH, "recipient": RECIPIENT, "seal": SEAL,
          "type": ("leaf", lambda node: node.kind == "s", None, None)}
COMMON_NAMES = sorted(COMMON)
ROOT = (COMMON_NAMES + ["issuer"], ["delegate"], dict(COMMON, issuer=ISSUER, delegate=DELEGATE))
CHILD = (COMMON_NAMES + ["ordinal", "parent"], [],
         dict(COMMON, ordinal=HEIGHT, parent=HASH))
PAYLOAD = _obj(lambda names: CHILD if "parent" in names else ROOT)


def _check_names(node, schema):
    if schema[0] == "obj" and node.kind == "o":
        names = node.names()
        required, optional, members = schema[1](names)
        if any(r not in names for r in required) or \
                any(n not in required and n not in optional for n in names):
            raise Refusal("WIRE_MEMBER")
        for name, value in node.value:
            _check_names(value, members[name])
    elif schema[0] == "arr" and node.kind == "a":
        for item in node.value:
            _check_names(item, schema[1])


def _check_values(node, schema):
    if schema[0] == "obj":
        if node.kind != "o":
            raise Refusal("WIRE_MEMBER")
        members = schema[1](node.names())[2]
        for name, value in node.value:
            _check_values(value, members[name])
    elif schema[0] == "arr":
        if node.kind != "a" or len(node.value) < schema[2] or \
                (schema[3] is not None and len(node.value) > schema[3]):
            raise Refusal("WIRE_MEMBER")
        for item in node.value:
            _check_values(item, schema[1])
    else:
        if not schema[1](node):
            raise Refusal("WIRE_MEMBER")
        if schema[2] is not None and not schema[2](node):
            raise Refusal("WIRE_INTEGER")


def _check_keys(node, schema):
    if schema[0] == "obj":
        members = schema[1](node.names())[2]
        for name, value in node.value:
            _check_keys(value, members[name])
    elif schema[0] == "arr":
        for item in node.value:
            _check_keys(item, schema[1])
    elif schema[3] is not None and not schema[3](node):
        raise Refusal("WIRE_KEY")


# --------------------------------------------------------------------------
# The rules of the object (LIP-0020 W11.9 and W11.10)

def plain(node):
    if node.kind == "o":
        return {k: plain(v) for k, v in node.value}
    if node.kind == "a":
        return [plain(v) for v in node.value]
    return node.value


def _limit_key(x):
    return (x["kind"], x["resource"], x["unit"], x.get("period"))


def _ascending(items):
    octets = [s.encode("ascii") for s in items]
    return all(a < b for a, b in zip(octets, octets[1:]))


def _distinct(keys):
    return len(set(keys)) == len(keys)


def _is_wkh(script):
    return len(script) == 44 and script.startswith("0014")


def _meet(a, b):
    """Two runs (txid, first, last) share an output."""
    return a[0] == b[0] and a[1] <= b[2] and b[1] <= a[2]


def check_shape(g):
    if not g["not_before_height"] < g["not_after_height"]:
        raise Refusal("GRANT_SHAPE")
    if not _ascending(g["actions"]):
        raise Refusal("GRANT_SHAPE")
    if not _distinct([_limit_key(x) for x in g["limits"]]):
        raise Refusal("GRANT_SHAPE")


def check_delegate(g):
    """Every rule of W11.10, the proposal rules included.

    W11.10 marks three points as proposals of other LIPs that a reader need
    not judge: the witness key hash of a range script, every rule on `stop`
    in rule 5, and rule 8. This reader judges them and reports them under
    the same code. The vector file states no code for them (the group
    `undetermined`), and `check` compares none.
    """
    d = g.get("delegate")
    if d is None:
        return
    bad = Refusal("GRANT_DELEGATE")
    # 1. the lists of the right itself
    if not _ascending(d["actions"]):
        raise bad
    if not _distinct([_limit_key(x) for x in d["pools"]]):
        raise bad
    notaries = [n["name"] for n in d["notaries"]]
    if not _ascending(notaries):
        raise bad
    issuer = g["issuer"]
    coins, stops = [], []
    # 2. each group, in the order of the groups
    for group in d["groups"]:
        t = group["template"]
        if not _distinct([_limit_key(x) for x in t["limits"]]):
            raise bad
        r = t["recipient"]
        if "class" in r and not _distinct([e["name"] for e in r["class"]]):
            raise bad
        if "certifier" in t:
            if t["certifier"] not in notaries:
                raise bad
        else:
            if "key" in r:
                raise bad
            if "class" in r and not (
                    len(r["class"]) == 1 and
                    r["class"][0]["name"] == issuer["name"] and
                    r["class"][0]["registration"] == issuer["registration"] and
                    r["class"][0]["owner"] == issuer["owner"]):
                raise bad
        for rng in group["ranges"]:
            last = rng["first"] + rng["count"] - 1
            if last > MAX_INDEX or not _is_wkh(rng["script"]):
                raise bad
            if ("stop" in rng) != ("certifier" in t):
                raise bad
            coins.append((rng["txid"], rng["first"], last))
            if "stop" in rng:
                s = rng["stop"]
                last = s["first"] + rng["count"] - 1
                if last > MAX_INDEX or not _is_wkh(s["script"]):
                    raise bad
                stops.append((s["txid"], s["first"], last))
    # 3. the pools
    sums = {}
    for group in d["groups"]:
        rows = sum(rng["count"] for rng in group["ranges"])
        for x in group["template"]["limits"]:
            sums[_limit_key(x)] = sums.get(_limit_key(x), 0) + rows * int(x["amount"])
    pools = {_limit_key(x): int(x["amount"]) for x in d["pools"]}
    if set(pools) != set(sums) or any(sums[k] > pools[k] for k in sums):
        raise bad
    # 4. the coins
    seal = g["seal"]["outpoint"]
    seal_run = (seal["txid"], seal["vout"], seal["vout"])
    for i, a in enumerate(coins):
        if _meet(a, seal_run) or any(_meet(a, b) for b in coins[:i]):
            raise bad
    # 5. the stop coins
    after_seal = (seal["txid"], seal["vout"] + 1, seal["vout"] + 1)
    for i, a in enumerate(stops):
        if _meet(a, seal_run) or _meet(a, after_seal) or \
                any(_meet(a, b) for b in stops[:i]) or any(_meet(a, b) for b in coins):
            raise bad


# --------------------------------------------------------------------------
# The pipeline of a signed grant (LIP-0020 W9.1 with W11.8)

class Grant:
    def __init__(self, signed_form, root):
        payload = root.get("payload")
        self.signed_form = signed_form
        self.payload_octets = serialize(payload)
        self.payload = plain(payload)
        self.signature = root.get("signature").value
        self.typed_digest = tagged_hash(GRANT_TYPE, self.payload_octets)
        self.grant_id = sha256(self.payload_octets).hex()
        self.content_address = sha256(signed_form).hex()


def read_grant(signed_form, parent=None, reference=None):
    """Returns a Grant or raises the first Refusal of the pipeline.

    `parent` is the Grant that the reader already read for a child, or None.
    `reference` is an identifier that another object states for this grant.
    """
    root = parse_document(signed_form, MAX_GRANT)                      # step 1
    if sorted(root.names()) != ["payload", "signature"]:               # step 2
        raise Refusal("WIRE_MEMBER")
    payload = root.get("payload")
    kind = payload.get("type")
    if kind is None or kind.kind != "s" or kind.value != GRANT_TYPE:   # step 3
        raise Refusal("WIRE_TYPE")
    _check_names(payload, PAYLOAD)                                     # step 4
    _check_values(payload, PAYLOAD)
    _check_keys(payload, PAYLOAD)
    sig = root.get("signature")
    if sig.kind != "s" or not _is_hex(sig.value, 128):                 # step 5
        raise Refusal("WIRE_SIGNATURE_FORM")
    g = Grant(signed_form, root)
    if "parent" in g.payload:                                          # step 6
        if parent is None or g.payload["parent"] != parent.grant_id:
            raise Refusal("WIRE_ID")
        if "parent" in parent.payload:
            raise Refusal("CHAIN_DEPTH")
        if "delegate" not in parent.payload:
            raise Refusal("NOT_DELEGABLE")
        key, failure = parent.payload["delegate"]["key"], "CHILD_SIGNER"
    else:
        key, failure = g.payload["issuer"]["grant_key"], "WIRE_SIGNATURE"
    if not bip340_verify(key, g.typed_digest, bytes.fromhex(g.signature)):  # step 7
        raise Refusal(failure)
    if reference is not None and reference != g.grant_id:              # step 8
        raise Refusal("WIRE_ID")
    check_shape(g.payload)                                             # step 9
    check_delegate(g.payload)
    return g


# --------------------------------------------------------------------------
# The vector file: verification, shared by `gen` and `check`

DERIVED = ("typed_digest", "grant_id", "content_address", "seal_script")


def verify_file(data):
    """Returns a list of (vector id, 'PASS' or a finding).

    For a vector of `undetermined` no code is compared: any refusal passes.
    """
    out = []
    grants = {}
    unfixed = data["undetermined"]
    determined = data["valid"] + data["invalid"] + data["compound"]
    vectors = determined + unfixed
    known = {v["id"] for v in vectors}
    valid_ids = {v["id"] for v in data["valid"]}
    unfixed_ids = {v["id"] for v in unfixed}
    lone = set(data["no_neighbour"])
    single = {v["id"] for v in data["invalid"] + unfixed}
    for v in vectors:
        findings = []
        if len(v["signed_form_hex"]) > 2 * MAX_VECTOR:
            out.append((v["id"], "signed_form_hex is longer than the checker reads"))
            continue
        octets = bytes.fromhex(v["signed_form_hex"])
        if "signed_form" in v and v["signed_form"].encode("utf-8") != octets:
            findings.append("signed_form differs from signed_form_hex")
        if v.get("octets") != len(octets):
            findings.append("octets")
        context = v.get("context", {})
        parent = None
        if "parent" in context:
            parent = grants.get(context["parent"])
            if parent is None:
                findings.append("context.parent is no valid vector read before this one")
        try:
            g = read_grant(octets, parent, context.get("reference"))
            got = "ok"
        except Refusal as r:
            g, got = None, r.code
        if v["id"] in unfixed_ids:
            if v["expect"] != REFUSED or v.get("code") != UNDETERMINED:
                findings.append("an undetermined vector states an outcome or a code")
            if got == "ok":
                findings.append("expect a refusal, reader gives ok")
        elif got != v["expect"]:
            findings.append("expect %s, reader gives %s" % (v["expect"], got))
        if (v["expect"] == "ok") != (v["id"] in valid_ids):
            findings.append("group")
        if g is not None:
            grants[v["id"]] = g
            derived = {"typed_digest": g.typed_digest.hex(), "grant_id": g.grant_id,
                       "content_address": g.content_address,
                       "seal_script": witness_key_hash_script(g.payload["seal"]["key"])}
            for name in DERIVED:
                if v.get(name) != derived[name]:
                    findings.append(name)
            if v.get("signature") != g.signature:
                findings.append("signature")
            if "payload" in v and v["payload"].encode("utf-8") != g.payload_octets:
                findings.append("payload")
        elif any(name in v for name in DERIVED):
            findings.append("a refused vector states a derived value")
        if "valid_neighbour" in v:
            if v["valid_neighbour"] not in valid_ids or v["id"] in lone:
                findings.append("valid_neighbour")
        elif v["id"] in single and v["id"] not in lone:
            findings.append("a refused vector names no valid neighbour")
        out.append((v["id"], "PASS" if not findings else "; ".join(findings)))
    listed = {x for rule in data["rules"] for x in rule["vectors"]}
    out.append(("rules", "PASS" if listed <= known else
                "names an unknown vector: %s" % sorted(listed - known)))
    codes = {v["expect"] for v in determined} - {"ok"}
    out.append(("codes_exercised", "PASS" if codes == set(data["codes_exercised"]) else
                "differs from the codes of the vectors"))
    absent = {x["code"] for x in data["not_exercised"]}
    out.append(("not_exercised", "PASS" if not (absent & codes) and lone <= single else
                "names a code that a vector exercises, or a vector outside `invalid` "
                "and `undetermined`"))
    return out


# --------------------------------------------------------------------------
# The generator

GENESIS = "000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770"
CONTRACT = "6e01e587b9931de4a32076d48cd9a64460d6fa0aeaac953e19201127a4d7afbf"
ZERO_AUX = bytes(32)
ONE_AUX = bytes([1]) * 32
OFF_CURVE = "eefdea4cdb677750a420fee807eacf21eb9898ae79b9768766e4faa04a2d4a34"
DROP = object()

# Public test scalars. Three are the secret keys of BIP-340 test vectors 0,
# 1 and 2; the others are small integers. None is a real key.
SCALARS = {
    "issuer": 3,
    "recipient": 0xB7E151628AED2A6ABF7158809CF4F3C762E7160F38B4DA56A784D9045190CFEF,
    "other": 0xC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B14E5C9,
    "issuer-owner": 4,
    "recipient-owner": 5,
    "executor": 6,
    "row-executor": 7,
    "seal": 8,
    "delegation": 9,
    "child-seal": 10,
    "notary-owner": 11,
    "landlord-b-owner": 12,
    "row-recipient": 13,
    "row-coin": 14,
    "row-stop": 15,
    "agent-owner": 16,
}
ROLES = {
    "issuer": ("x-only", "the issuer's grant key; BIP-340 test vector 0"),
    "recipient": ("x-only", "a request key; BIP-340 test vector 1"),
    "other": ("x-only", "a key that the grant does not name; BIP-340 test vector 2"),
    "issuer-owner": ("compressed", "the owner key of the issuer's name"),
    "recipient-owner": ("compressed", "the owner key of a recipient's name"),
    "executor": ("x-only", "the key of the grant's executor"),
    "row-executor": ("x-only", "the key of the executor of a row"),
    "seal": ("compressed", "the seal key of a root grant"),
    "delegation": ("x-only", "the delegation key of a parent"),
    "child-seal": ("compressed", "the child-seal key of a parent"),
    "notary-owner": ("compressed", "the owner key of a notary's name"),
    "landlord-b-owner": ("compressed", "the owner key of a second landlord's name"),
    "row-recipient": ("x-only", "the request key that a row names"),
    "row-coin": ("compressed", "the key that the coins of a range pay"),
    "row-stop": ("compressed", "the key that the stop coins of a range pay"),
    "agent-owner": ("compressed", "the owner key of an agent's name"),
}


def key(name):
    return xonly(SCALARS[name]) if ROLES[name][0] == "x-only" else compressed(SCALARS[name])


def label_hash(label):
    """A placeholder: the SHA-256 of an ASCII label."""
    return sha256(label.encode("ascii")).hex()


RECENT = label_hash("lip-0020 grant-v4 recent block")
TX_SEAL = label_hash("lip-0020 grant-v4 seal transaction")
TX_CHILD_SEAL = label_hash("lip-0020 grant-v4 child seal transaction")
TX_ISSUER = label_hash("lip-0020 grant-v4 issuer registration")
TX_NOTARY = label_hash("lip-0020 grant-v4 notary registration")
TX_LANDLORD_B = label_hash("lip-0020 grant-v4 landlord b registration")
TX_COINS_A = label_hash("lip-0020 grant-v4 coins a")
TX_COINS_B = label_hash("lip-0020 grant-v4 coins b")
TX_STOPS = label_hash("lip-0020 grant-v4 stop coins")


def emit(obj):
    """The generator's own serializer, for the documents that it builds."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def limit(kind, resource, unit, amount, period=None):
    x = {"kind": kind, "resource": resource, "unit": unit, "amount": amount}
    if period is not None:
        x["period"] = period
    return x


REQUESTS = ("example/requests", "example/model-a", "request")
TOKENS = ("example/tokens", "example/model-a", "token")
HOUR = "example/hour"


def issuer_pin():
    return {"name": "id/lip0020-issuer", "owner": key("issuer-owner"),
            "registration": {"txid": TX_ISSUER, "vout": 0}}


def notary_pin():
    return {"name": "id/lip0020-notary", "owner": key("notary-owner"),
            "registration": {"txid": TX_NOTARY, "vout": 0}}


def landlord_b_pin():
    return {"name": "id/lip0020-landlord-b", "owner": key("landlord-b-owner"),
            "registration": {"txid": TX_LANDLORD_B, "vout": 1}}


def base_root():
    return {
        "type": GRANT_TYPE,
        "genesis": GENESIS,
        "contract": CONTRACT,
        "issuer": dict(issuer_pin(), grant_key=key("issuer")),
        "recipient": {"key": key("recipient")},
        "executor": {"name": "id/lip0020-executor", "key": key("executor")},
        "actions": ["example/instruct", "example/review"],
        "limits": [limit(*REQUESTS, "1000", HOUR), limit(*TOKENS, str(MAX_AMOUNT))],
        "not_before_height": 200000,
        "not_after_height": 252560,
        "recent_block": RECENT,
        "seal": {"construction": "W", "kind": "revocable-only", "key": key("seal"),
                 "outpoint": {"txid": TX_SEAL, "vout": 0}},
    }


def coin_script():
    return witness_key_hash_script(key("row-coin"))


def stop_script():
    return witness_key_hash_script(key("row-stop"))


def certified_range(txid, first, count, stop_first):
    return {"txid": txid, "first": first, "count": count, "script": coin_script(),
            "stop": {"txid": TX_STOPS, "first": stop_first, "script": stop_script()}}


def plain_range(txid, first, count):
    return {"txid": txid, "first": first, "count": count, "script": coin_script()}


def row_executor():
    return {"name": "id/lip0020-row-executor", "key": key("row-executor")}


def base_parent():
    """Two groups and nine rows, as in the example of LIP-0026 section 8."""
    g = base_root()
    g["delegate"] = {
        "key": key("delegation"),
        "child_seal_key": key("child-seal"),
        "actions": ["example/review"],
        "pools": [limit(*REQUESTS, "380", HOUR)],
        "notaries": [notary_pin()],
        "groups": [
            {"template": {"executor": row_executor(),
                          "recipient": {"key": key("row-recipient")},
                          "limits": [limit(*REQUESTS, "60", HOUR)],
                          "certifier": "id/lip0020-notary"},
             "ranges": [certified_range(TX_COINS_A, 0, 3, 0),
                        certified_range(TX_COINS_A, 10, 2, 3)]},
            {"template": {"executor": row_executor(),
                          "recipient": {"class": [issuer_pin()]},
                          "limits": [limit(*REQUESTS, "20", HOUR)],
                          "no_certifier": True},
             "ranges": [plain_range(TX_COINS_B, 0, 4)]},
        ],
    }
    return g


def unlimited_group(index):
    """A group of one row for an exact name, without a certifier and
    without a limit. Its coin is the output `index` of the coins b."""
    return {"template": {"executor": row_executor(),
                         "recipient": {"name": "id/lip0020-agent",
                                       "owner": key("agent-owner")},
                         "limits": [], "no_certifier": True},
            "ranges": [plain_range(TX_COINS_B, index, 1)]}


def exact_parent():
    """A parent that pins no notary and has no pool: one group of one row."""
    g = base_parent()
    g["delegate"]["notaries"] = []
    g["delegate"]["pools"] = []
    g["delegate"]["groups"] = [unlimited_group(7)]
    return g


def bound_parent():
    """The base parent at three largest counts: four notaries, 16 groups and
    16 ranges in its second group. Its rows sum to 680 for the one limit key,
    5 of 60 and 19 of 20, and its pool of 700 leaves room for one more row
    of 20, so that a 17th range breaks the count and nothing else."""
    g = base_parent()
    d = g["delegate"]
    d["notaries"] = [notary_pin()] + [
        dict(notary_pin(), name="id/lip0020-notary-%s" % c) for c in "bcd"]
    d["pools"] = [limit(*REQUESTS, "700", HOUR)]
    d["groups"][1]["ranges"] += [plain_range(TX_COINS_B, 10 + j, 1) for j in range(15)]
    d["groups"] += [unlimited_group(100 + i) for i in range(14)]
    return g


# The amount of the wrap vector: five rows of it and four rows of 20 sum to
# 2^64 + 4, which a sum in 64 bits reads as 4.
WRAP_AMOUNT = (2 ** 64 + 4 - 4 * 20) // 5


def base_child(parent_id):
    g = base_root()
    del g["issuer"]
    g["parent"] = parent_id
    g["ordinal"] = 1
    g["recipient"] = {"key": key("row-recipient")}
    g["executor"] = row_executor()
    g["actions"] = ["example/review"]
    g["limits"] = [limit(*REQUESTS, "60", HOUR)]
    g["not_before_height"] = 200010
    g["seal"] = {"construction": "W", "kind": "revocable-only", "key": key("child-seal"),
                 "outpoint": {"txid": TX_CHILD_SEAL, "vout": 0}}
    return g


def sign(payload_octets, signer, aux=ZERO_AUX):
    return bip340_sign(SCALARS[signer], tagged_hash(GRANT_TYPE, payload_octets), aux).hex()


def signed(payload, signer="issuer", aux=ZERO_AUX):
    return emit({"payload": payload, "signature": sign(emit(payload), signer, aux)})


class Builder:
    def __init__(self):
        self.valid, self.invalid, self.compound, self.undetermined = [], [], [], []
        self.rules = {}

    def _entry(self, vid, rules, claim, octets, expect, context):
        v = {"id": vid, "rules": rules, "claim": claim}
        if context:
            v["context"] = context
        if len(octets) <= 6000:
            v["signed_form"] = octets.decode("utf-8")
        v["signed_form_hex"] = octets.hex()
        v["octets"] = len(octets)
        v["expect"] = expect
        for r in rules:
            self.rules.setdefault(r, []).append(vid)
        return v

    def ok(self, vid, rules, claim, payload, signer="issuer", aux=ZERO_AUX, context=None):
        octets = signed(payload, signer, aux)
        v = self._entry(vid, rules, claim, octets, "ok", context)
        p = emit(payload)
        v["signing_key"] = signer
        v["aux_rand"] = aux.hex()
        if len(p) <= 6000:
            v["payload"] = p.decode("utf-8")
        v["typed_digest"] = tagged_hash(GRANT_TYPE, p).hex()
        v["signature"] = json.loads(octets.decode("utf-8"))["signature"]
        v["grant_id"] = sha256(p).hex()
        v["content_address"] = sha256(octets).hex()
        v["seal_script"] = witness_key_hash_script(payload["seal"]["key"])
        self.valid.append(v)
        return v

    def bad(self, vid, rules, claim, octets, expect, neighbour, context=None):
        v = self._entry(vid, rules, claim, octets, expect, context)
        if neighbour is not None:
            v["valid_neighbour"] = neighbour
        self.invalid.append(v)

    def unfixed(self, vid, rules, claim, octets, judged, neighbour):
        """A vector whose rule section 11 carries as a proposal: the file
        states that a reader which judges the rule refuses, and no code."""
        v = self._entry(vid, rules, claim, octets, REFUSED, None)
        v["code"] = UNDETERMINED
        v["judged"] = judged
        v["valid_neighbour"] = neighbour
        self.undetermined.append(v)

    def both(self, vid, rules, claim, octets, defects, expect, context=None):
        v = self._entry(vid, rules, claim, octets, expect, context)
        v["defects"] = defects
        self.compound.append(v)


def padded_parent(filler):
    """A parent with 16 groups of 16 ranges, a range of 4096 coins, a range
    that ends at the largest output index and a class of 78 landlords. The
    `filler` is the resource of one own limit and sets the size."""
    g = base_root()
    g["limits"] = [limit("example/filler", filler, "octet", "0")]
    groups = []
    for i in range(16):
        txid = label_hash("lip-0020 grant-v4 padded coins %d" % i)
        ranges = [plain_range(txid, 5000 * j, 4096 if (i, j) == (0, 0) else 1)
                  for j in range(16)]
        groups.append({"template": {"executor": row_executor(),
                                    "recipient": {"name": "id/lip0020-agent-%02d" % i,
                                                  "owner": key("agent-owner")},
                                    "limits": [],
                                    "no_certifier": True},
                       "ranges": ranges})
    groups[15]["ranges"][15] = plain_range(
        label_hash("lip-0020 grant-v4 padded coins 15"), MAX_INDEX - 4095, 4096)
    landlords = []
    for i in range(78):
        landlords.append({"name": "id/lip0020-landlord-%03d" % i,
                          "owner": key("landlord-b-owner"),
                          "registration": {"txid": label_hash("lip-0020 landlord %d" % i),
                                           "vout": i}})
    groups[0]["template"] = {"executor": row_executor(),
                             "recipient": {"class": landlords},
                             "limits": [],
                             "certifier": "id/lip0020-notary"}
    for j, rng in enumerate(groups[0]["ranges"]):
        rng["stop"] = {"txid": TX_STOPS, "first": 5000 * j, "script": stop_script()}
    g["delegate"] = {"key": key("delegation"), "child_seal_key": key("child-seal"),
                     "actions": [], "pools": [], "notaries": [notary_pin()],
                     "groups": groups}
    return g


def sized_parent(size):
    """The padded parent whose signed form has exactly `size` octets."""
    count = size - len(signed(padded_parent("x"))) + 1
    if not 1 <= count <= 255:
        raise ValueError("the filler of %d characters does not fit one label" % count)
    g = padded_parent("x" * count)
    if len(signed(g)) != size:
        raise ValueError("size")
    return g


def build():
    b = Builder()

    # ---- valid ----------------------------------------------------------
    root = base_root()
    v1 = b.ok("grant-v-01", ["W11.1", "W11.2", "W11.3", "W11.4", "W11.8", "W5.1", "W6.1"],
              "A root grant to a recipient by key, without a right of re-delegation: "
              "two own limits, one with a period and one at the largest amount.", root)
    by_name = base_root()
    by_name["recipient"] = {"name": "id/lip0020-recipient", "owner": key("recipient-owner")}
    b.ok("grant-v-02", ["W11.3"],
         "The same grant to a recipient by name: the name and its owner key, and no request key.",
         by_name)
    parent = base_parent()
    v3 = b.ok("grant-v-03", ["W11.5", "W11.6", "W11.7", "W11.10"],
              "A parent with two groups and nine rows. The first group names a certifier and "
              "has two ranges with their stop coins; the second states that it has no certifier "
              "and names the class of the issuer's own landlord. The pool of 380 is exactly "
              "5 rows of 60 and 4 rows of 20.", parent)
    b.ok("grant-v-04", ["W11.5", "W11.7", "W11.10"],
         "A parent that pins no notary: one group without a certifier whose recipient is an "
         "exact name, with no limit and therefore no pool.", exact_parent())
    child = base_child(v3["grant_id"])
    v5 = b.ok("grant-v-05", ["W11.2", "W11.8"],
              "A child of grant-v-03 for the row of ordinal 1, signed by the delegation key of "
              "its parent. Its seal key is the child-seal key of the parent.",
              child, signer="delegation", context={"parent": "grant-v-03"})
    b.ok("grant-v-06", ["W5.4", "W6.2", "W6.4"],
         "The payload of grant-v-01 signed with other auxiliary randomness: another signature "
         "and another content address, the same identifier.", root, aux=ONE_AUX)
    minimal = base_root()
    minimal["actions"] = []
    minimal["limits"] = []
    b.ok("grant-v-07", ["W11.4"],
         "A grant with an empty action set and no limit. It is well formed and authorizes nothing.",
         minimal)
    b.ok("grant-v-08", ["W11.6", "W11.7", "W1.1"],
         "A parent whose signed form has exactly 65536 octets: 16 groups of 16 ranges, a range "
         "of 4096 coins, a range whose last coin has the index 4294967295, a class of 78 "
         "landlords, and an own limit whose resource is a filler that brings the size to the "
         "bound.", sized_parent(MAX_GRANT))
    b.ok("grant-v-09", ["W6.3"],
         "grant-v-01 with a reference that states its identifier.", root,
         context={"reference": v1["grant_id"]})
    keyless = base_parent()
    del keyless["delegate"]["child_seal_key"]
    b.ok("grant-v-10", ["W11.5"],
         "The parent of grant-v-03 without a child-seal key. The document is well formed. "
         "Under LIP-0014 CS1 it is unusable as a parent: every child of it refuses as "
         "CHILD_SEAL_KEY at its admission, which is no step of this pipeline.", keyless)
    b.ok("grant-v-11", ["W11.5", "W11.6"],
         "The parent of grant-v-03 at three largest counts: four notaries, 16 groups, and 16 "
         "ranges in its second group. Each of the 14 further groups has one row for an exact "
         "name, without a certifier and without a limit. The rows sum to 680, 5 of 60 and 19 "
         "of 20, and the pool of 700 leaves room for one more row of 20.", bound_parent())

    # ---- refused, one defect -------------------------------------------
    def root_with(change):
        g = base_root()
        change(g)
        return g

    def parent_with(change):
        g = base_parent()
        change(g)
        return g

    def exact_with(change):
        g = exact_parent()
        change(g)
        return g

    def bound_with(change):
        g = bound_parent()
        change(g)
        return g

    def sized_with(change):
        g = sized_parent(MAX_GRANT)
        change(g)
        return g

    def setp(path, value):
        def change(g):
            x = g
            for p in path[:-1]:
                x = x[p]
            if value is DROP:
                del x[path[-1]]
            else:
                x[path[-1]] = value
        return change

    n = [0]

    def bad(rules, claim, octets, expect, neighbour="grant-v-01", context=None):
        n[0] += 1
        b.bad("grant-i-%02d" % n[0], rules, claim, octets, expect, neighbour, context)

    bad(["W1.1", "W11.6"],
        "The parent of grant-v-08 with one more character in its filler: 65537 octets.",
        signed(sized_parent(MAX_GRANT + 1)), "WIRE_SIZE", "grant-v-08")
    spaced = signed(root).replace(b'{"payload":', b'{"payload": ', 1)
    bad(["W1.6"], "A space after the first colon of grant-v-01.", spaced, "WIRE_NOT_CANONICAL")
    with_id = emit({"payload": root, "signature": sign(emit(root), "issuer"),
                    "grant_id": v1["grant_id"]})
    bad(["W5.3"], "A signed form that states the identifier of the grant as a third member.",
        with_id, "WIRE_MEMBER")
    bad(["W3.1", "W3.3"], "The type string of another version.",
        signed(root_with(setp(["type"], "swarma-grant/5"))), "WIRE_TYPE")
    bad(["W3.2", "W11.2"],
        "The stand-in of the vector prim-grant-01 of wire-vectors.json: a payload that holds "
        "`type` alone, under its valid signature. Before the grant had members a reader "
        "refused these octets as WIRE_TYPE. The payload lacks every other member, so the "
        "vector names no valid neighbour.", signed({"type": GRANT_TYPE}), "WIRE_MEMBER", None)
    bad(["W3.2", "W11.2"], "A member that the schema does not list: the `grantee_name` of v3.",
        signed(root_with(setp(["grantee_name"], "id/lip0020-recipient"))), "WIRE_MEMBER")
    bad(["W3.2", "W11.2"], "No `seal`.", signed(root_with(setp(["seal"], DROP))), "WIRE_MEMBER")
    bad(["W11.3"], "A recipient with a request key and a name with its owner key.",
        signed(root_with(setp(["recipient"], {"key": key("recipient"),
                                              "name": "id/lip0020-recipient",
                                              "owner": key("recipient-owner")}))), "WIRE_MEMBER")
    bad(["W11.3"], "A recipient with neither.", signed(root_with(setp(["recipient"], {}))),
        "WIRE_MEMBER")
    bad(["W11.3"], "A recipient by name without the owner key.",
        signed(root_with(setp(["recipient"], {"name": "id/lip0020-recipient"}))), "WIRE_MEMBER",
        "grant-v-02")
    bad(["W11.3"], "A grant whose own recipient is a class. A class stands in a template alone.",
        signed(root_with(setp(["recipient"], {"class": [issuer_pin()]}))), "WIRE_MEMBER")
    child_issuer = base_child(v3["grant_id"])
    child_issuer["issuer"] = dict(issuer_pin(), grant_key=key("issuer"))
    bad(["W11.2"],
        "The child of grant-v-05 with the member `issuer`: a grant with `issuer` and with "
        "`parent` and `ordinal`.",
        signed(child_issuer, "delegation"), "WIRE_MEMBER", "grant-v-05",
        {"parent": "grant-v-03"})
    child_delegate = base_child(v3["grant_id"])
    child_delegate["delegate"] = base_parent()["delegate"]
    bad(["W11.2", "W11.5"], "A child that carries a right of re-delegation.",
        signed(child_delegate, "delegation"), "WIRE_MEMBER", "grant-v-05",
        {"parent": "grant-v-03"})
    child_no_ordinal = base_child(v3["grant_id"])
    del child_no_ordinal["ordinal"]
    bad(["W11.2"], "A child without `ordinal`.", signed(child_no_ordinal, "delegation"),
        "WIRE_MEMBER", "grant-v-05", {"parent": "grant-v-03"})

    t0 = ["delegate", "groups", 0, "template"]
    t1 = ["delegate", "groups", 1, "template"]
    r00 = ["delegate", "groups", 0, "ranges", 0]
    r10 = ["delegate", "groups", 1, "ranges", 0]
    pv = "grant-v-03"
    bad(["W11.7"], "A template that names a certifier and also states that it has none.",
        signed(parent_with(setp(t0 + ["no_certifier"], True))), "WIRE_MEMBER", pv)
    bad(["W11.7"], "A template that says nothing about its certifier.",
        signed(parent_with(setp(t0 + ["certifier"], DROP))), "WIRE_MEMBER", pv)
    bad(["W11.7"], "`no_certifier` with the value false.",
        signed(parent_with(setp(t1 + ["no_certifier"], False))), "WIRE_MEMBER", pv)
    bad(["W11.7"], "A certifier that is the empty string.",
        signed(parent_with(setp(t0 + ["certifier"], ""))), "WIRE_MEMBER", pv)
    bad(["W1.4", "W11.7"], "A certifier that is `null`.",
        signed(parent_with(setp(t0 + ["certifier"], None))), "WIRE_VALUE", pv)

    bad(["W2.1", "W11.1"], "A height in the string form.",
        signed(root_with(setp(["not_after_height"], "252560"))), "WIRE_MEMBER")
    bad(["W2.1", "W11.1"], "An amount in the number form.",
        signed(root_with(setp(["limits", 0, "amount"], 1000))), "WIRE_MEMBER")
    bad(["W2.3", "W11.1"], "An amount with a leading zero.",
        signed(root_with(setp(["limits", 0, "amount"], "01000"))), "WIRE_INTEGER")
    bad(["W2.3", "W11.1"], "An amount of 2^64, one above the bound.",
        signed(root_with(setp(["limits", 1, "amount"], "18446744073709551616"))), "WIRE_INTEGER")
    bad(["W2.2", "W11.1"], "An output index of 4294967296.",
        signed(root_with(setp(["seal", "outpoint", "vout"], 4294967296))), "WIRE_INTEGER")
    bad(["W11.6"], "A range with the count 0.",
        signed(parent_with(setp(r10 + ["count"], 0))), "WIRE_INTEGER", pv)
    bad(["W11.6"],
        "A range of 4097 coins: the first range of grant-v-08, which has no limit and "
        "therefore no pool to exceed.",
        signed(sized_with(setp(["delegate", "groups", 0, "ranges", 0, "count"], 4097))),
        "WIRE_INTEGER", "grant-v-08")

    bv = "grant-v-11"
    bad(["W11.6"], "17 groups: the parent of grant-v-11 with one more group of one row.",
        signed(bound_with(lambda g: g["delegate"]["groups"].append(unlimited_group(114)))),
        "WIRE_MEMBER", bv)
    bad(["W11.6"],
        "A group of 17 ranges: the second group of grant-v-11 with one more range of one "
        "coin. The pool still holds the rows.",
        signed(bound_with(lambda g: g["delegate"]["groups"][1]["ranges"].append(
            plain_range(TX_COINS_B, 25, 1)))), "WIRE_MEMBER", bv)
    bad(["W11.6"],
        "A right of re-delegation without a group: the parent of grant-v-04 without its "
        "one group.",
        signed(exact_with(setp(["delegate", "groups"], []))), "WIRE_MEMBER", "grant-v-04")
    bad(["W11.6"], "A group without a range.",
        signed(parent_with(setp(["delegate", "groups", 1, "ranges"], []))), "WIRE_MEMBER", pv)
    bad(["W11.5"], "Five notaries: the parent of grant-v-11 with one more pin.",
        signed(bound_with(lambda g: g["delegate"]["notaries"].append(
            dict(notary_pin(), name="id/lip0020-notary-e")))), "WIRE_MEMBER", bv)
    bad(["W11.7"],
        "A class without a landlord: the class of the first template of grant-v-08, "
        "emptied. The template names a certifier.",
        signed(sized_with(setp(["delegate", "groups", 0, "template", "recipient"],
                               {"class": []}))), "WIRE_MEMBER", "grant-v-08")
    bad(["W11.1"], "An owner key that begins with 04.",
        signed(root_with(setp(["issuer", "owner"], "04" + key("issuer-owner")[2:]))), "WIRE_MEMBER")
    bad(["W11.1"], "A seal key in uppercase hexadecimal.",
        signed(root_with(setp(["seal", "key"], key("seal").upper()))), "WIRE_MEMBER")
    bad(["W11.1"], "A seal key in the x-only form of a signing key.",
        signed(root_with(setp(["seal", "key"], key("seal")[2:]))), "WIRE_MEMBER")
    bad(["W11.1"], "A request key in the compressed form of an output key.",
        signed(root_with(setp(["recipient", "key"], "02" + key("recipient")))), "WIRE_MEMBER")
    bad(["W11.1"], "An executor name with a character outside printable ASCII.",
        signed(root_with(setp(["executor", "name"], "id/lip0020-ex\u00e9cuteur"))), "WIRE_MEMBER")
    bad(["W11.1"], "An executor name of 256 characters.",
        signed(root_with(setp(["executor", "name"], "id/" + "a" * 253))), "WIRE_MEMBER")
    bad(["W11.1"], "An empty action name.",
        signed(root_with(setp(["actions"], ["", "example/review"]))), "WIRE_MEMBER")
    bad(["W11.1"], "A range script with an odd number of characters.",
        signed(parent_with(setp(r10 + ["script"], coin_script()[:-1]))), "WIRE_MEMBER", pv)
    bad(["W3.5", "W11.1"], "A recent block of 63 characters.",
        signed(root_with(setp(["recent_block"], RECENT[:-1]))), "WIRE_MEMBER")

    bad(["W3.6", "W11.1"], "An executor key that is no x coordinate of a curve point.",
        signed(root_with(setp(["executor", "key"], OFF_CURVE))), "WIRE_KEY")
    bad(["W11.1"], "A seal key whose x coordinate is on no point of the curve.",
        signed(root_with(setp(["seal", "key"], "02" + OFF_CURVE))), "WIRE_KEY")
    bad(["W3.6", "W5.5", "W11.8"],
        "A grant key that is no point of the curve. The signature is by the issuer's test key "
        "and verifies under no key that these octets name.",
        signed(root_with(setp(["issuer", "grant_key"], OFF_CURVE))), "WIRE_KEY")

    short_sig = emit({"payload": root, "signature": sign(emit(root), "issuer")[:-1]})
    bad(["W5.2"], "A signature of 127 characters.", short_sig, "WIRE_SIGNATURE_FORM")
    bad(["W5.5", "W11.8"], "A root grant signed by another key than `issuer.grant_key`.",
        signed(root, "other"), "WIRE_SIGNATURE")
    later = root_with(setp(["not_after_height"], 252561))
    moved = emit({"payload": later, "signature": sign(emit(root), "issuer")})
    bad(["W5.1", "W3.7"],
        "`not_after_height` raised by one after signing. The signature is that of grant-v-01.",
        moved, "WIRE_SIGNATURE")
    bad(["W6.3", "W6.4"], "A reference that states the content address of grant-v-01.",
        signed(root), "WIRE_ID", "grant-v-09", {"reference": v1["content_address"]})

    cv = "grant-v-05"
    bad(["W11.8", "W6.3"], "The child of grant-v-05, presented with grant-v-04 as its parent.",
        signed(child, "delegation"), "WIRE_ID", cv, {"parent": "grant-v-04"})
    bad(["W11.8", "W6.3"], "The child of grant-v-05, presented without a parent.",
        signed(child, "delegation"), "WIRE_ID", cv)
    bad(["W11.8"], "The child signed by the grant key of the parent's issuer.",
        signed(child, "issuer"), "CHILD_SIGNER", cv, {"parent": "grant-v-03"})
    bad(["W11.8"], "The child signed by the request key of the parent's recipient.",
        signed(child, "recipient"), "CHILD_SIGNER", cv, {"parent": "grant-v-03"})
    bad(["W11.8"], "A child that names grant-v-01, which carries no right of re-delegation.",
        signed(base_child(v1["grant_id"]), "delegation"), "NOT_DELEGABLE", cv,
        {"parent": "grant-v-01"})
    bad(["W11.8"], "A child that names the child grant-v-05 as its parent: a third link.",
        signed(base_child(v5["grant_id"]), "delegation"), "CHAIN_DEPTH", cv,
        {"parent": "grant-v-05"})

    bad(["W11.9"], "A window whose two heights are equal.",
        signed(root_with(setp(["not_after_height"], 200000))), "GRANT_SHAPE")
    bad(["W11.9"], "Actions in descending order.",
        signed(root_with(setp(["actions"], ["example/review", "example/instruct"]))), "GRANT_SHAPE")
    bad(["W11.9"], "An action twice.",
        signed(root_with(setp(["actions"], ["example/review", "example/review"]))), "GRANT_SHAPE")
    bad(["W11.9"], "Two own limits with one key and different amounts.",
        signed(root_with(setp(["limits", 1], limit(*REQUESTS, "5", HOUR)))), "GRANT_SHAPE")

    d = ["delegate"]
    bad(["W11.10"], "Delegable actions in descending order.",
        signed(parent_with(setp(d + ["actions"], ["example/review", "example/instruct"]))),
        "GRANT_DELEGATE", pv)
    bad(["W11.10"], "No pool for a key that a template limits.",
        signed(parent_with(setp(d + ["pools"], []))), "GRANT_DELEGATE", pv)
    bad(["W11.10"], "A pool for a key that no template limits.",
        signed(parent_with(lambda g: g["delegate"]["pools"].append(limit(*TOKENS, "1")))),
        "GRANT_DELEGATE", pv)
    bad(["W11.10"], "A pool of 379 for rows that sum to 380.",
        signed(parent_with(setp(d + ["pools", 0, "amount"], "379"))), "GRANT_DELEGATE", pv)

    if 5 * WRAP_AMOUNT + 4 * 20 != 2 ** 64 + 4 or WRAP_AMOUNT > MAX_AMOUNT:
        raise ValueError("wrap amount")
    bad(["W11.10", "W2.4"],
        "The amount of the first template raised from 60 to %d. Five rows of it and four "
        "rows of 20 sum to 2^64 + 4 against the pool of 380: a reader that adds in 64 bits "
        "gets 4 and admits the parent." % WRAP_AMOUNT,
        signed(parent_with(setp(t0 + ["limits", 0, "amount"], str(WRAP_AMOUNT)))),
        "GRANT_DELEGATE", pv)
    bad(["W11.10"], "Two pools with one key.",
        signed(parent_with(lambda g: g["delegate"]["pools"].append(
            limit(*REQUESTS, "380", HOUR)))), "GRANT_DELEGATE", pv)
    bad(["W11.10"], "Two limits of one template with one key.",
        signed(parent_with(lambda g: g["delegate"]["groups"][1]["template"]["limits"].append(
            limit(*REQUESTS, "1", HOUR)))), "GRANT_DELEGATE", pv)

    def descending_notaries(g):
        g["delegate"]["notaries"] = [dict(notary_pin(), name="id/lip0020-notary-z"),
                                     notary_pin()]
    bad(["W11.10"], "Two notaries in descending order of their names.",
        signed(parent_with(descending_notaries)), "GRANT_DELEGATE", pv)
    bad(["W11.10"], "A certifier that is no notary of the parent.",
        signed(parent_with(setp(t0 + ["certifier"], "id/lip0020-notary-z"))), "GRANT_DELEGATE", pv)

    def no_cert(recipient):
        return setp(t1 + ["recipient"], recipient)
    bad(["W11.10"], "A template without a certifier whose recipient is a request key.",
        signed(parent_with(no_cert({"key": key("row-recipient")}))), "GRANT_DELEGATE", pv)
    bad(["W11.10"],
        "A template without a certifier whose class holds the issuer's landlord and a second one.",
        signed(parent_with(no_cert({"class": [issuer_pin(), landlord_b_pin()]}))),
        "GRANT_DELEGATE", pv)
    bad(["W11.10"], "A template without a certifier whose class holds another landlord alone.",
        signed(parent_with(no_cert({"class": [landlord_b_pin()]}))), "GRANT_DELEGATE", pv)
    other_registration = issuer_pin()
    other_registration["registration"] = {"txid": TX_ISSUER, "vout": 1}
    bad(["W11.10"],
        "A template without a certifier whose one landlord has the issuer's name and owner key "
        "and another registration.",
        signed(parent_with(no_cert({"class": [other_registration]}))), "GRANT_DELEGATE", pv)
    bad(["W11.10"], "A class that states one name twice, in a template with a certifier.",
        signed(parent_with(setp(t0 + ["recipient"], {
            "class": [issuer_pin(), dict(landlord_b_pin(), name="id/lip0020-issuer")]}))),
        "GRANT_DELEGATE", pv)
    bad(["W11.10"],
        "A range whose last coin would have the index 4294967296: the range of the second "
        "group with its first coin at 4294967293.",
        signed(parent_with(setp(r10 + ["first"], MAX_INDEX - 2))), "GRANT_DELEGATE", pv)
    bad(["W11.10"],
        "Two ranges of one transaction that share the output 2: the second range of the "
        "first group with its first coin at 2.",
        signed(parent_with(setp(["delegate", "groups", 0, "ranges", 1, "first"], 2))),
        "GRANT_DELEGATE", pv)
    bad(["W11.10"],
        "A range that holds the seal of the parent: the range of the second group in the "
        "seal transaction.",
        signed(parent_with(setp(r10 + ["txid"], TX_SEAL))), "GRANT_DELEGATE", pv)

    # ---- refused, one defect, document step on the octets of a grant ----
    whole = signed(root)
    bad(["W1.2"], "grant-v-01 without its last octet, the closing brace of the signed form.",
        whole[:-1], "WIRE_JSON")
    twice = whole.replace(b'"type":"swarma-grant/4"}',
                          b'"type":"swarma-grant/4","type":"swarma-grant/4"}', 1)
    if twice == whole:
        raise ValueError("duplicate")
    bad(["W1.3"],
        "The member `type` twice in the payload of grant-v-01, with one value. The signature "
        "is that of grant-v-01.", twice, "WIRE_DUPLICATE")
    fraction = setp(["not_after_height"], 252560.0)
    control = setp(["executor", "name"], "id/lip0020-\x01executor")
    bad(["W1.4"], "A height with a fraction: `not_after_height` is written 252560.0.",
        signed(root_with(fraction)), "WIRE_NUMBER")
    bad(["W1.5"], "An executor name that holds the escape of U+0001.",
        signed(root_with(control)), "WIRE_STRING")

    # ---- refused by a reader that judges a proposal rule; no code -------
    u = [0]

    def unfixed(claim, octets, judged):
        u[0] += 1
        b.unfixed("grant-u-%02d" % u[0], ["W11.10"], claim, octets, judged, pv)

    presence = ("W11.10 rule 5: a range has `stop` exactly where its template names a "
                "certifier (LIP-0027 H1.1, LIP-0014 J9.4)")
    script = ("W11.10 rule 5: the script of a range is a witness key hash (LIP-0026 R8.2, "
              "R3.1)")
    place = ("W11.10 rule 8: no output is a stop coin of two rows, and no stop coin is a "
             "coin of a row, the seal of the parent or the output after it (LIP-0027 H1.3)")
    unfixed("A range of a template with a certifier that states no stop coins.",
            signed(parent_with(setp(r00 + ["stop"], DROP))), presence)
    unfixed("A range of a template without a certifier that states stop coins.",
            signed(parent_with(setp(r10 + ["stop"], {"txid": TX_STOPS, "first": 100,
                                                     "script": stop_script()}))), presence)
    unfixed("A range script that pays a key hash and no witness key hash.",
            signed(parent_with(setp(r10 + ["script"], "76a914" + coin_script()[4:] + "88ac"))),
            script)
    unfixed("Stop coins that are coins of another range: the stop coins of the first range "
            "in the transaction of the coins of the second group.",
            signed(parent_with(setp(r00 + ["stop", "txid"], TX_COINS_B))), place)
    unfixed("Stop coins that begin at the output after the seal of the parent.",
            signed(parent_with(setp(r00 + ["stop"], {"txid": TX_SEAL, "first": 1,
                                                     "script": stop_script()}))), place)
    unfixed("Two runs of stop coins that share the output 2: the stop coins of the second "
            "range with their first coin at 2.",
            signed(parent_with(setp(["delegate", "groups", 0, "ranges", 1, "stop", "first"],
                                    2))), place)

    # ---- compound -------------------------------------------------------
    c = [0]

    def both(rules, claim, octets, defects, expect, context=None):
        c[0] += 1
        b.both("grant-c-%02d" % c[0], rules, claim, octets, defects, expect, context)

    def two(*changes):
        def change(g):
            for ch in changes:
                ch(g)
        return change

    both(["W9.3"], "An unlisted member and an executor key that is no point. Names come first.",
         signed(root_with(two(setp(["note"], "x"), setp(["executor", "key"], OFF_CURVE)))),
         ["WIRE_MEMBER", "WIRE_KEY"], "WIRE_MEMBER")
    both(["W9.3"],
         "An amount above its bound in `limits` and a height in the string form in "
         "`not_after_height`. Values are taken in the order of the canonical bytes, and "
         "`limits` stands first.",
         signed(root_with(two(setp(["limits", 1, "amount"], "18446744073709551616"),
                              setp(["not_after_height"], "252560")))),
         ["WIRE_INTEGER", "WIRE_MEMBER"], "WIRE_INTEGER")
    both(["W9.3"],
         "An executor key that is no point and an output index above its bound, later in the "
         "bytes. Every value is checked before any key.",
         signed(root_with(two(setp(["executor", "key"], OFF_CURVE),
                              setp(["seal", "outpoint", "vout"], 4294967296)))),
         ["WIRE_KEY", "WIRE_INTEGER"], "WIRE_INTEGER")
    both(["W9.1", "W11.8"], "A window whose heights are equal, signed by another key.",
         signed(root_with(setp(["not_after_height"], 200000)), "other"),
         ["WIRE_SIGNATURE", "GRANT_SHAPE"], "WIRE_SIGNATURE")
    both(["W9.1"], "A signature of 127 characters over a payload with an unlisted member.",
         emit({"payload": root_with(setp(["note"], "x")),
               "signature": sign(emit(root), "issuer")[:-1]}),
         ["WIRE_MEMBER", "WIRE_SIGNATURE_FORM"], "WIRE_MEMBER")
    both(["W11.9", "W11.10"],
         "A parent with actions in descending order and a pool that its rows exceed.",
         signed(parent_with(two(setp(["actions"], ["example/review", "example/instruct"]),
                                setp(["delegate", "pools", 0, "amount"], "379")))),
         ["GRANT_SHAPE", "GRANT_DELEGATE"], "GRANT_SHAPE")
    both(["W11.8"],
         "A child signed by the request key and presented with another parent. The reference "
         "selects the key and is checked first.",
         signed(child, "recipient"), ["WIRE_ID", "CHILD_SIGNER"], "WIRE_ID",
         {"parent": "grant-v-04"})
    both(["W11.8", "W11.9"],
         "A child with a window whose heights are equal, signed by the request key.",
         signed(dict(child, not_after_height=200010), "recipient"),
         ["CHILD_SIGNER", "GRANT_SHAPE"], "CHILD_SIGNER", {"parent": "grant-v-03"})
    absent = setp(["recent_block"], None)
    both(["W9.2"],
         "A height with a fraction and, later in the octets, the member `type` twice. A "
         "repeated name is reported before a number, wherever each stands.",
         signed(root_with(fraction)).replace(
             b'"type":"swarma-grant/4"}',
             b'"type":"swarma-grant/4","type":"swarma-grant/4"}', 1),
         ["WIRE_NUMBER", "WIRE_DUPLICATE"], "WIRE_DUPLICATE")
    both(["W9.2"],
         "A height with a fraction and, later in the octets, a recent block that is `null`. "
         "Inside W1.4 a `null` is reported before a number.",
         signed(root_with(two(fraction, absent))),
         ["WIRE_NUMBER", "WIRE_VALUE"], "WIRE_VALUE")
    both(["W9.2"],
         "An executor name that holds the escape of U+0001 and, later in the octets, a "
         "recent block that is `null`.",
         signed(root_with(two(control, absent))),
         ["WIRE_STRING", "WIRE_VALUE"], "WIRE_VALUE")
    both(["W9.2"],
         "An executor name that holds the escape of U+0001 and, later in the octets, a "
         "height with a fraction.",
         signed(root_with(two(control, fraction))),
         ["WIRE_STRING", "WIRE_NUMBER"], "WIRE_NUMBER")
    both(["W9.2"],
         "A space after the first colon and, later in the octets, an executor name that "
         "holds the escape of U+0001. W1.6 comes last.",
         signed(root_with(control)).replace(b'{"payload":', b'{"payload": ', 1),
         ["WIRE_NOT_CANONICAL", "WIRE_STRING"], "WIRE_STRING")

    vectors = b.valid + b.invalid + b.compound
    order = ["W1.1", "W1.2", "W1.3", "W1.4", "W1.5", "W1.6", "W2.1", "W2.2", "W2.3", "W2.4",
             "W3.1", "W3.2", "W3.3", "W3.5", "W3.6", "W3.7", "W5.1", "W5.2", "W5.3", "W5.4",
             "W5.5", "W6.1", "W6.2", "W6.3", "W6.4", "W9.1", "W9.2", "W9.3"] + \
            ["W11.%d" % i for i in range(1, 11)]
    unknown = sorted(set(b.rules) - set(order))
    if unknown:
        raise ValueError("rules without a place: %s" % unknown)
    exercised = sorted({v["expect"] for v in vectors} - {"ok"})
    if {x["code"] for x in NOT_EXERCISED} & set(exercised):
        raise ValueError("a code is listed as not exercised and has a vector")
    if [v["id"] for v in b.invalid + b.undetermined
            if "valid_neighbour" not in v] != NO_NEIGHBOUR:
        raise ValueError("the vectors without a neighbour are not those of NO_NEIGHBOUR")
    return {
        "schema": "swarma-link-spec/lip-0020-grant-vectors/1",
        "lip": "LIP-0020",
        "note": NOTE,
        "base": BASE,
        "test_keys": [{"name": name, "form": ROLES[name][0], "role": ROLES[name][1],
                       "public_key": key(name)} for name in SCALARS],
        "parameters": {
            "genesis": GENESIS, "contract": CONTRACT, "recent_block": RECENT,
            "placeholders": "Every transaction id and the recent block are the SHA-256 of an "
                            "ASCII label and name no transaction and no block. Names, action "
                            "names and the kinds, resources, units and periods of limits are "
                            "placeholders: no registry assigns them.",
            "largest_grant": MAX_GRANT, "largest_depth": MAX_DEPTH,
            "largest_groups": MAX_GROUPS, "largest_ranges": MAX_RANGES,
            "largest_coins": MAX_COINS, "largest_notaries": MAX_NOTARIES,
            "largest_output_index": MAX_INDEX, "largest_amount": str(MAX_AMOUNT),
        },
        "rules": [{"rule": r, "vectors": b.rules[r]} for r in order if r in b.rules],
        "codes_exercised": exercised,
        "not_exercised": NOT_EXERCISED,
        "no_neighbour": NO_NEIGHBOUR,
        "valid": b.valid,
        "invalid": b.invalid,
        "compound": b.compound,
        "undetermined": b.undetermined,
    }


NOTE = (
    "Vectors for the members of `swarma-grant/4` (LIP-0020 section 11). Each vector is the "
    "signed form of a grant; `signed_form_hex` is the vector, and `signed_form`, where it is "
    "given, only shows the same octets. In the groups `valid`, `invalid` and `compound`, "
    "`expect` is `ok` or the first refusal of the pipeline of a signed object (W9.1 with "
    "W11.8 to W11.10), for a reader that judges the rules that W11.10 marks as judged by "
    "every reader. A vector with `context.parent` is read with that vector as the parent "
    "that the reader already read; `context.reference` is an identifier that another object "
    "states for the grant. A refused vector of `invalid` holds one defect and names a valid "
    "neighbour that differs from it in that defect: in one member of the payload, in octets "
    "outside the payload, or in the context. Where the defect is a property of the parent, "
    "the child names another parent, and its member `parent` and the context change "
    "together. The vectors of `no_neighbour` name none. Unless its claim says otherwise, the "
    "signature of a refused vector is valid for the octets shown. A vector of `compound` "
    "holds several defects on purpose and has no neighbour; the statement of one defect "
    "does not cover it. A vector of `undetermined` is a parent that breaks one rule which "
    "section 11 carries as a proposal of another LIP, named in `judged`, and nothing else. "
    "Its outcome is `refused`, code not determined by this version: a reader that judges "
    "the rule refuses the parent, this version fixes no code for that refusal, and a "
    "checker accepts any refusal and compares no code. This version does not determine "
    "that a reader judges the rule: one that does not reads the same octets as a "
    "well-formed parent, and the vector does not bind it. `not_exercised` lists the "
    "refusal codes that section 11 names and no vector of this file exercises, each with "
    "the reason and with the place where it is exercised. The file was computed by one "
    "implementation, tools/grantv4/grantv4.py, whose reader also checked it. An "
    "independent implementation recomputes, from `signed_form_hex` and `context` alone, "
    "the outcome of every vector of `valid`, `invalid` and `compound`, and for a valid "
    "vector its typed digest, its identifier, its content address, its signature under the "
    "key of the place and the script of its seal key. Keys are public test scalars and "
    "belong to nobody; signatures are made by the default signing algorithm of BIP-340 "
    "with the stated auxiliary randomness. No vector reads a chain: nothing here shows "
    "that a name, a coin, a seal or a block exists."
)

# The vectors of `invalid` and `undetermined` that name no valid neighbour.
NO_NEIGHBOUR = ["grant-i-05"]

# Refusal codes that section 11 names and that no vector of the file holds.
_ADMISSION = ("The pipeline of W11.8 never reports it. It is a check of an admission, and "
              "this file states results of the pipeline alone. ")
NOT_EXERCISED = [
    {"code": "CHILD_ORDINAL",
     "why": _ADMISSION + "The pipeline reads an `ordinal` of any value of its form; the "
            "ordinal is held against the rows of the parent at admission (LIP-0026 R2.1, "
            "R8.8).",
     "exercised": "vectors/LIP-0026/rows-vectors.json and "
                  "vectors/LIP-0026/groups-vectors.json, on stated facts and not on the "
                  "octets of a grant."},
    {"code": "CHILD_SEAL_KEY",
     "why": _ADMISSION + "A parent without a child-seal key is read (grant-v-10), and so is "
            "a child of it; the child refuses at its admission (LIP-0014 CS1, CS2, "
            "agreement pending).",
     "exercised": "No vector of this repository. LIP-0014 section 11.2 states the cases "
                  "S4-9 and S4-10."},
    {"code": "DELEGATE_KEY_REUSE",
     "why": _ADMISSION + "A parent whose delegation key or child-seal key repeats another "
            "of its keys is read; every child of it refuses at its admission (LIP-0014 "
            "J4.3 (a), CS3, agreement pending).",
     "exercised": "No vector of this repository. LIP-0014 sections 11.1 and 11.2 state the "
                  "cases S4-2a and S4-10."},
    {"code": "SEAL_PROFILE",
     "why": _ADMISSION + "The pipeline checks the form of `seal.construction` and of "
            "`seal.kind` and not their values; whether a verifier supports them depends on "
            "its configuration (LIP-0008 SB2).",
     "exercised": "vectors/LIP-0024/endorsement-vectors.json, for the profile of a seal-key "
                  "endorsement and not for the member `seal` of a grant. No vector holds a "
                  "grant with an unsupported profile."},
]

BASE = {
    "note": "The primitives below are not repeated here. These vectors rest on them.",
    "wire_vectors": {
        "file": "vectors/LIP-0020/wire-vectors.json",
        "uses": ["canonical", "integers", "primitives.types", "primitives.grant_stand_in"],
    },
    "laboratory": {
        "repository": "https://github.com/relux-works/swarma-chain-lab",
        "change": 146,
        "file": "experiments/grant-v4/vectors/vectors.json",
        "uses": ["arithmetic-0", "signature-0-1", "signature-0-3", "memberless-type-0",
                 "the canonical, integer, signature and key cases of its inventory"],
        "changes": "`memberless-type-0` reads the octets `{\"type\":\"swarma-grant/4\"}` as a "
                   "signed grant and expects WIRE_TYPE. With members those octets refuse as "
                   "WIRE_MEMBER, at the signed form (W5.3).",
    },
}

# Values of earlier vector files that this generator must reproduce before
# it writes anything: the signer and the typed digest are calibrated on them.
CALIBRATION = [
    # prim-grant-01 of wire-vectors.json, the laboratory's signature-0-3
    ("swarma-grant/4", b'{"type":"swarma-grant/4"}', 3,
     "e9498fc137f1bf3f6b1c2a85e03416a120b4512801a882f311da1f89b51508c1"
     "c7892206fa47f954e5e33d01710a6157e6f40195eb15dbfc463ad46710bd6561"),
    # assent-v-01 of wire-vectors.json
    ("swarma-contract-assent/1",
     b'{"contract":"6e01e587b9931de4a32076d48cd9a64460d6fa0aeaac953e19201127a4d7afbf",'
     b'"genesis":"000000000062b72c5e2ceb45fbc8587e807c155b0da735e6483dfba2f0a9c770",'
     b'"party":"f9308a019258c31049344f85f89d5229b531c845836f99b08601f113bce036f9",'
     b'"type":"swarma-contract-assent/1"}', 3,
     "199ea4f8552c7238ddf3f789ffa562e365d7d7ae87ed5cc4807fc601d134fc02"
     "7e6f17078562341451b9c75423cd9859e2c4f8077dfb6941809b947dcea93dc8"),
    # the laboratory's signature-0-1
    ("swarma-grant/4", b'{"type":"swarma-grant/4"}', 1,
     "93f48fe9b9d6859e3756092bbe02a2db47b54a910615acb865842d5389602c33"
     "b530dd78a582cfb3abccf4df25f6dc980a848384ee0f93585350c1e6bf152fce"),
]


def calibrate():
    if tagged_hash("swarma-grant/4", b'{"type":"swarma-grant/4"}').hex() != \
            "f1e62e34f6b79cd5c28a4b1edbb50b737bb3f4d2bd26805764b64eb5e7372f75":
        raise ValueError("typed digest")
    for tag, octets, scalar, sig in CALIBRATION:
        if bip340_sign(scalar, tagged_hash(tag, octets), ZERO_AUX).hex() != sig:
            raise ValueError("signature calibration: %s" % tag)
    if xonly(SCALARS["recipient"]) != \
            "dff1d77f2a671c5f36183726db2341be58feae1da2deced843240f7b502ba659" or \
            xonly(SCALARS["other"]) != \
            "dd308afec5777e13121fa72b9cc1b7cc0139715309b086c960e18fd969774eb8":
        raise ValueError("test keys")
    if ripemd160(b"").hex() != "9c1185a5c5e9fc54612808977ee8f548b2258d31" or \
            ripemd160(b"abc").hex() != "8eb208f7e05d987a9b044a8e98c6b087f15a0bfc" or \
            ripemd160(b"a" * 1000000).hex() != "52783243c1697bdbe16d37f97f68f08325dc1528":
        raise ValueError("ripemd160")
    if lift_x(int(OFF_CURVE, 16)) is not None:
        raise ValueError("off-curve value")


def main(argv):
    if len(argv) == 2 and argv[1] == "gen":
        calibrate()
        text = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
        failed = [r for r in verify_file(json.loads(text)) if r[1] != "PASS"]
        for vid, finding in failed:
            sys.stderr.write("FINDING %s: %s\n" % (vid, finding))
        if failed:
            return 1
        sys.stdout.write(text)
        return 0
    if len(argv) == 3 and argv[1] == "check":
        try:
            with open(argv[2], "rb") as f:
                raw = f.read(MAX_FILE + 1)
            if len(raw) > MAX_FILE:
                raise ValueError("the file has more than %d octets" % MAX_FILE)
            data = json.loads(raw.decode("utf-8"))
            calibrate()
            results = verify_file(data)
        except (OSError, ValueError, KeyError, TypeError) as e:
            sys.stderr.write("input error: %r\n" % (e,))
            return 2
        failed = 0
        for vid, finding in results:
            if finding == "PASS":
                print("PASS %s" % vid)
            else:
                failed += 1
                print("FINDING %s: %s" % (vid, finding))
        print("SUMMARY %d checked, %d findings" % (len(results), failed))
        return 1 if failed else 0
    sys.stderr.write(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
