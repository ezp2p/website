---
title: "09. Sealing: privacy that doesn't lean on TLS"
nav_order: 10
---

*Moved here from `ezp2p/protocol/spec/09-sealing.md` on 2026-11-25.*

**Status:** built in Puddle (streams, phones, its Pond client) and Pond (protocol 5, feature `sealed`), 2026-11-18. Parts
00, 02, 03, 04 and 05 describe it; part 06 (Levee) was rewritten on it. The decisions at the end were
taken as recommended.

## Why

Before this, TLS did one job nobody checked: it was the only thing keeping what is sent private. Bodies are not encrypted
with anyone's keys yet (Puddle's [`docs/identity.md`](/wiki/puddle/design/identity/), "Encryption", was planned and never built). Certificates are
self-signed and nobody verifies them, so anyone in the middle could show their own and read everything. What stops
that today is the `fp` in every receipt (part 02): the answer names the certificate the responder served, and the
caller refuses one that doesn't match what it saw.

That ties the protocol to certificates after all, and it breaks in the places people actually run these programs:

- **Behind a reverse proxy** (Apache, nginx, Caddy, Traefik, a Kubernetes ingress, Cloudflare). The proxy shows its
  own certificate, which never matches the one the Puddle or Pond signs for, so every answer looks intercepted and the
  Pond is marked `not_proven`.
- **Let's Encrypt renewals**, every 60 to 90 days: a Pond has to be restarted to sign for the new certificate, and a
  proxy's certificate changes underneath it without the Pond ever knowing.
- **Levee** (part 06) needs its own rules, signing over the Levee's certificate instead, only because of this tie.

## The rule

**TLS is transport only.** Nothing in the protocol names, pins, remembers, compares or signs over a certificate. Any
certificate works: self-signed, Let's Encrypt, a proxy's, one that changes every hour.

- **Who** a party is: its signing keys, as now (requests signed by the sender, answers by the responder).
- **Privacy**: its encryption key. Every request body is sealed to the recipient's X25519 key, and every answer
  to the caller, so only the two ends can read it, whatever carried it.

## Keys

| Party | Signing | Sealing (X25519) | Where the other side gets the sealing key |
|---|---|---|---|
| Puddle | its current Ed25519 key | the encryption key already in its chain (part 01) | its chain; on first contact, the link (below) |
| Pond | `pond.key` (Ed25519) | **new**: derived from the same seed (HKDF-SHA256, info `pond-seal-v1`), so no new file to lose | the invite link; `/pond/v1/info` and the join answer, under a receipt |
| Phone (device) | its device key | none needed | it only seals to its Puddle; answers come back under the request's own key (below) |
| Levee | its key | its own, in its chain | the Puddle's address record that names the Levee |

A party that rolls its keys (part 01) rolls its sealing key with them; a sender sealing to a key the recipient has
just retired gets `409 stale_key`, unsealed but signed, with the recipient's chain in it (`chain`), so only someone the
recipient knows learns it, and the sender can take the new keys and try again.

## Sealing a request

The construction is **HPKE** (RFC 9180), base mode: `DHKEM(X25519, HKDF-SHA256)`, `HKDF-SHA256`,
`ChaCha20-Poly1305`. A standard construction, not our own; see "Building it" for the OpenSSL version it needs.

The caller sets up an HPKE sender context to the recipient's sealing key with

    info = puddle-seal-v1\n<sender id>\n<recipient id, or * for a first contact>\n<the request signature's nonce>

and sends one header beside the signature:

    X-Puddle-Seal: v1 kid=<hex SHA-256 of the recipient's sealing key>; enc=<base64 of HPKE's 32-byte enc>

The body, if there is one, is the HPKE seal of the plaintext body with `aad` = `<METHOD>\n<request target>`, sent as
`Content-Type: application/puddle-sealed`. A GET has no body but still carries the header, because the answer is
sealed under it.

The request signature (part 02) is unchanged: it covers the SHA-256 of **the body as sent**, so of the sealed bytes.
The recipient checks the signature first and answers a stranger the same plain `404` as before, without opening
anything; then it opens the body. A body that won't open, from a sender who did authenticate, is `400 bad_seal`.

Because `info` names both parties and the signature's nonce, a sealed body can't be lifted into another request, to
another recipient, or replayed: the nonce is already single use (part 02).

## Sealing an answer

The answer key comes from the same HPKE context: `Export(ctx, "puddle-answer-v1", 32)`. Only the caller, who made the
context, and the recipient, who opened it, can derive it. This is why a phone needs no sealing key of its own.

The answer body is cut into **records** of up to 64 KiB of plaintext. Each is sealed with ChaCha20-Poly1305 under the
answer key, the nonce being the record's index as a 12-byte big-endian number, and `aad` = `puddle-answer-v1\n<status>\n`
followed by `0` for every record but the last and `1` for the last one, so an answer cut short is noticed. A small answer is
one record. The answer is `application/puddle-sealed`; what is inside is what the route always answered.

**Every answer to a request that authenticated is sealed**, refusals and errors included, except a `204`, which has no
body. The plain `404` to someone whose request didn't open is not, so it stays byte for byte the answer to a path that
doesn't exist. A Pond seals its `404` to a request it opened but refuses (not a member): only it could, so a removed
member can believe it (part 05). The answers that must look the same to
everyone (`access`, `access/status`, part 03) are sealed too: sealing them gives nothing away, since only the asker can
open them.

**Downloads and `Range`.** A file is sealed record by record as it is read, so nothing is held in memory. A `Range`
request is answered `206` with the whole records that cover it; its `Content-Range` gives the plaintext range of those
records (starting on a record boundary, so the first record's index is its start divided by 64 KiB), and the caller
opens them and cuts out the bytes it asked for.

## Receipts lose `fp`

A receipt still proves who answered and what they answered, signed by the responder's current key. It just stops
naming a certificate:

    X-Puddle-Receipt: v2 id=<responder id>; kid=<key id>; sig=<base64>

    puddle-receipt-v2
    <the responder's id>
    <the request's nonce>
    <the HTTP status>
    <hex SHA-256 of the answer's body, as sent>

What goes with it:

- **No handshake.** `GET /stream/v1/hello` existed to prove a certificate before anything private was sent. Now what
  is private is sealed to the key the caller already holds, so a request goes straight out. (`/device/v1/status` stays,
  for what it says; it just isn't a handshake any more.)
- **No pinning, no proving certificates.** A Pond's answers are checked by receipt only; a Puddle never asks a Pond to
  prove a certificate, and `not_proven` / `certificate_changed` caused by a certificate go away.
- **"Intercepted" goes away.** Someone in the middle can still drop or delay things (the caller sees nothing
  answered, and retries), or answer for the other side (no good receipt: not delivered). They can't read anything, and
  they can't make anyone believe an answer.

## First contact

A sealed request needs the recipient's sealing key, and a first contact is exactly when there is no chain yet. So
**links carry the key**: `k=<base32 of the recipient's 32-byte sealing key>` (52 characters).

| Link | Becomes |
|---|---|
| a Puddle's link (part 03) | `puddle://home.example.org:8443?k=<key>`, and `&invite=` as before |
| a phone's pairing link (part 04) | `puddle-pair://<address>?id=<id>&k=<key>&secret=<secret>` |
| a Pond invite (part 05) | `pond://<address>?invite=<token>&k=<key>` |

The key in a link is trusted as much as the address in it: both came from the person who gave it. When the chain
arrives (the `access/result`, the pairing answer, the join answer), the caller checks the chain's sealing key is the
one in the link, and stops if it isn't.

**A bare address** (someone types `home.example.org` with no `k`) is the one case left: the `access` request can't be
sealed, so it goes as today, protected by TLS alone. That request carries the asker's chain, profile, note and
invite token. See "Open decisions", 1.

## Ponds

- The Pond derives its sealing key from `pond.key`'s seed and gives it in `/pond/v1/info` (`seal_key`) and in the
  join answer, both under a receipt. Invites carry it as `k`.
- Joining is sealed to the invite's `k`; every request a member makes after that is sealed to `seal_key`.
- The Pond still reads what members send it, because it is the Pond: sealing is between each Puddle and the Pond, not
  between members. (Encryption only members can undo stays where Puddle's [`roadmap.md`](/wiki/puddle/design/history/) put it: later.)
- A Pond behind a reverse proxy, or renewing its certificate, needs nothing from anyone: no restart, no shared
  certificate, no deploy hook. The receipts never mention one.
- **Voice is not affected.** Calls and voice channels use WebRTC, whose DTLS fingerprints are per session and arrive in
  the signed SDP (part 08); they have nothing to do with the HTTPS certificate. Voice still goes straight to the Pond over
  UDP, not through a proxy. A WebSocket fallback through the proxy (for networks that block UDP) would carry its frames
  sealed under the session's keys; that belongs with its own design in the Pond's [`docs/voice.md`](/wiki/pond/design/voice/).

## Levee

Part 06 gets simpler. A Levee is just something that carries sealed requests: it can't read what it spools for an
offline Puddle (a real gain: today it could), and the Puddle behind it signs ordinary receipts with no certificate in
them. Custody receipts lose their `fp` the same way. The address-record field naming the Levee stays.

## What someone in the middle (or a proxy) still sees

Sealing hides bodies, not traffic. Whoever terminates TLS, an honest reverse proxy included, sees which address is
asked for which route (`POST /stream/v1/events`), when, how big the bodies are, the status codes, and the signature
header (the sender's id and key id). That is what TLS already hid from everyone else and what a proxy operator could
always see. Hiding routes too (one `POST /sealed` that carries the method and path inside the seal) is possible later
without changing anything else here; see "Open decisions", 3.

## The owner API is not part of this

The desktop app talks to its own Puddle on `127.0.0.1` with the owner token (Puddle's `api/openapi.yaml`). That stays
local and unchanged. Phones use device signatures and are sealed like everyone else.

## What changes in the other parts

- **00**, principle 1: "TLS is transport only. Privacy is the recipient's sealing key, identity the signing keys."
- **01**: a Pond's sealing key, derived from its seed.
- **02**: receipts v2 without `fp`; no handshake; `X-Puddle-Seal`, `bad_seal`, `stale_key`.
- **03**: links carry `k`; `hello` goes; every route sealed both ways; the "intercepted" outcome goes.
- **04**: pairing links carry `k`; `status` is no longer a handshake.
- **05**: `seal_key`, sealed join, no certificate proving or pinning; `protocol` goes up and the feature is `sealed`.
- **06**: no Levee certificate in receipts; spooled requests stay sealed.
- **vectors**: `sealing.json` (RFC 9180's own test vectors for the suite, plus a sealed request and answer with fixed
  keys); `signatures.json` gains v2 receipts.

## Building it

- **Crypto.** OpenSSL has an HPKE API only from 3.2; Debian 12 (Pond's image, and many servers) ships 3.0. So each
  program implements HPKE base mode for this one suite over primitives 3.0 has (X25519, HKDF, ChaCha20-Poly1305): about
  two hundred lines, checked against RFC 9180's published vectors, so the two implementations can't quietly differ.
- **Order:** (1) sealing, records and vectors in Puddle; (2) streams, Puddle to Puddle, receipts v2, `hello` and the
  certificate code removed; (3) phones; (4) the Pond and Puddle's Pond client; (5) Levee, when it is built.

## Open decisions

1. **A bare address with no `k`.** Recommended: allow it, for that one `access` request only, sealed by nothing but
   TLS, and have the app always hand out links with `k` so it is rare. The alternative, refusing addresses without `k`,
   is safer but means a friend can never just type your address.
2. **Changing v1 in place or adding v2 paths** (part 00, "Versioning"). Recommended: in place. Nothing has been
   released (no version tags exist yet), every Puddle and Pond running today is a dev build, and keeping the old
   unsealed paths alive would keep the certificate tie alive with them.
3. **Hiding routes from a proxy** (one sealed endpoint). Recommended: not now; it costs proxies their ability to route
   and log by path, and the bodies are what matter.
4. **Old peers.** Recommended: no unsealed fallback. A Puddle or Pond that doesn't seal is answered like any other
   request that fails its checks.
