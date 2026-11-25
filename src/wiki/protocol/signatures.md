---
title: "02. Signatures: who sent it, and who answered"
nav_order: 3
---

*Moved here from `ezp2p/protocol/spec/02-signatures.md` on 2026-11-25.*

Two headers, one in each direction. Together they mean a request is from who it says, meant for who it names, used
once, and that its answer came from who the sender meant, over the connection the sender saw.

## Request signatures

    X-Puddle-Signature: v1 id=<sender id>; kid=<key id>; ts=<ms>; nonce=<base64>; sig=<base64>

`sig` is Ed25519 by the key `kid` names, over these lines joined by `\n` (no newline at the end):

    puddle-request-v1
    <METHOD>
    <request target: path and query, exactly as sent>
    <hex SHA-256 of the body; of nothing for an empty one>
    <ts>
    <nonce>
    <the recipient's id>

The header is parsed strictly: exactly these fields, in this order, nothing extra. The nonce is 16 random bytes.

The recipient checks, and answers **`404` to any failure up to and including the signature**:

1. the recipient id is its own. Only a route meant for a first contact (a stream request to an address, joining a
   Pond) also accepts `*`.
2. the sender is one it knows and `kid` is their **current** key; or the route proves the key another way (a chain in
   the body, a device pairing). Retired keys can't start new requests.
3. the signature verifies.

Only then may it say what is wrong: `401 clock_skew` (with its `now`) when `ts` is more than five minutes off,
`401 replayed` when the nonce was seen in that window, and the route's own refusals.

## Answer receipts

Every answer to a request that authenticated, from someone the responder already holds a record of, carries:

    X-Puddle-Receipt: v2 id=<responder id>; kid=<key id>; sig=<base64>

`sig` is Ed25519 by the responder's current key over:

    puddle-receipt-v2
    <the responder's id>
    <the request's nonce>
    <the HTTP status>
    <hex SHA-256 of the answer's body exactly as sent (sealed, part 09); of nothing for an empty one>

No certificate: TLS only carries the bytes (part 09), so a receipt holds over any connection, a reverse proxy included.
(`v1` receipts named the certificate; nothing makes or accepts them any more.)

**No receipt** on: the plain `404` a stranger gets; any answer to a stranger, even one who proved a request with a
chain of their own; and the routes that must answer everyone alike (a stream request and its status), so that a
receipt never tells anyone who lives at an address or whether they are blocked.

An answer sent straight from a file (any part of it, with `Range`) is signed over exactly the bytes sent.

### Checking a receipt (MUST, for any caller that holds the responder's key)

Accept an answer only if the receipt is there, names the id and key the caller holds for the responder, and carries
this request's nonce and the status and body received. Someone in the middle can pass a request on and an answer back,
but can't read either (part 09) or answer in the responder's name.

What a caller makes of the result:

| result | meaning |
|---|---|
| good receipt, `2xx` | delivered |
| good receipt, any other status | refused, in their name: final |
| no receipt (a plain `404` and the like) | not them, or they don't know us: **not delivered**, try again later |
| another key, or a signature that doesn't check | not proven: **not delivered** |

There is no handshake before a request: what it carries is sealed to the key the caller holds (part 09), so it can go
straight out over any connection.

Vectors: `vectors/signatures.json` (signed requests and receipts, with what a checker must say about each).
