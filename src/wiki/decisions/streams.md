---
title: Streams and the wire
nav_order: 20
---

How Puddles talk to each other, and what a stranger can learn. The design is in
[Puddle: Streams](/wiki/puddle/design/streams/), [Protocol: Signatures](/wiki/protocol/signatures/) and
[Protocol: Sealing](/wiki/protocol/sealing/).

### What does a stranger learn from a Puddle?

**Decided:** nothing. **Nothing is public.** Every route is authenticated (the owner's token, or a request signed by a
peer), and a failed check is answered `404`, exactly as an unknown path is, never `401` or `403`. A body too large for
a stranger is refused unread with the same `404`, so the size where they stop doesn't reveal which routes take bodies.

### What does a friend request answer?

**Decided:** a properly signed request always gets `202` with no body: pending, approved, blocked, closed,
rate-limited and full all produce the same bytes. Anything unsigned gets the usual `404`. *(Roadmap 3.2)*

**Considered:** "202 whatever happens". That was dropped because answering garbage with `202` tells a stranger there is
a Puddle at the address.

### How is the other end proven? (three steps)

1. **First: pin the TLS certificate.** Self-generated certificates, any accepted, the fingerprint recorded on first
   contact, and changes announced in the signed address record. An unannounced change held sending until the owner
   trusted it. *(Roadmap 3.4, decision 3)*
2. **Then: signed receipts.** The owner decided the certificate should only encrypt, and the far end should prove
   itself by its keys. Every answer carried a receipt signed by the responder, over the request's nonce, the status,
   the body's hash and the certificate's fingerprint. *(Roadmap phase 6)*
3. **Now: TLS is transport only.** Receipts that named the certificate broke behind a reverse proxy and on every
   Let's Encrypt renewal. So **nothing in the protocol may depend on a TLS certificate**: every request body is sealed
   (HPKE, RFC 9180) to the recipient's encryption key, every answer to the caller, and receipts stop naming a
   certificate. *(2026-11-18, roadmap phase 10, [Sealing](/wiki/protocol/sealing/))*

**Why:** most people will run a Puddle or Pond behind a reverse proxy, often on certificates that change every few
months. A proxy, or a Levee, now sees routes and sizes but no contents.

### Sealing's open decisions

These were taken as recommended, when phase 10 was built:

- **A bare address with no `k` (key) in it:** allowed, for the one `access` request only, sealed by nothing but TLS.
  The app always hands out links with `k`, so it is rare. Refusing such addresses was safer, but would mean a friend
  could never just type your address.
- **Change v1 in place, or add v2 paths:** in place. Nothing had been released, and keeping the old unsealed paths
  would have kept the certificate tie alive with them.
- **Hide routes from a proxy behind one sealed endpoint:** not now. It would cost proxies the ability to route and log
  by path, and the bodies are what matter.
- **An unsealed fallback for old peers:** none. A peer that doesn't seal is answered like any other request that fails
  its checks.

### When is a send retried?

**Decided:** if the other Puddle is **offline** (refused, timed out, unreachable), retry every 5 minutes for a day,
then every 30, and at once when they're heard from. **Anything else fails once** and isn't retried, and the reason is
kept for the owner. *(Roadmap decision 4)*

### May old keys sign new messages?

**Decided:** no. A delivery must be signed by the sender's **current** key. *(Roadmap 4.1a)*

**Why:** accepting retired keys would let someone with a stolen phone's old keys keep writing as the owner after a
roll, which is exactly what rolling is for. So the signature travels *outside* the event's bytes, and messages queued
before a roll are signed again. Checking old history with old keys is ezp2p/puddle#94.

### Asking whether a request was answered

**Decided:** `access/status` is a `POST` carrying the chain, not a `GET`. *(Roadmap 3.5)*

**Why:** the target may hold nothing about the requester (a request it ignored leaves no trace), so it couldn't
otherwise tell who is asking.

### HTTP style

**Decided:** only `GET` and `POST`. A `GET` reads and never changes anything, and a `POST` does everything else, with
the verb in the path (`dm/delete`, `user/unblock`). Ids go in the path (`users/{id}/block`), and a message embeds its
author's partial user rather than pointing into a side list.

### Limits on a request

**Decided:** a note of up to 500 characters, five requests an hour per requester, 200 waiting for the owner, 5,000 on
record, and 96 KiB per request. Every body is capped at 4 MiB, decided from the headers before it is read.
*(Roadmap 2.1, 3.2)*

### What to call the group-only connection

**Decided:** **scoped stream**, the name it already had. *(Roadmap decision 5)*

**Considered:** Brook, Rill, Tributary.
