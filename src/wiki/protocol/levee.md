---
title: "06. Levee: a front for one Puddle"
nav_order: 7
---

*Moved here from `ezp2p/protocol/spec/06-levee.md` on 2026-11-25.*

**Status:** being built (Levee 1, `/levee/v1`), 2026-11-21. Replaces the first sketch, which signed receipts over the
Levee's certificate; sealing (part 09) made that unnecessary.

A **Levee** is the public side of one Puddle. It runs on a server with a public address (a VPS, a box in a DMZ), usually
behind a reverse proxy, and is set up by the Puddle's owner, for that Puddle alone. The Puddle connects **out** to it and
needs no open ports:

- **Its address is the Puddle's address.** Friends, phones and new contacts reach the Puddle at the Levee's address,
  which stays the same when the Puddle's home network changes.
- **What comes in** is passed straight through while the Puddle is attached, and the one-way part of it is **spooled**
  while it is not, and handed over when it comes back.
- **What goes out** leaves through the Levee too, so nobody the Puddle talks to learns its home address.
- **Files the Puddle sends** wait at the Levee until each friend has fetched them, so they can be fetched while the
  Puddle is off.
- **Calls** go through the Levee's relay (a small TURN server), since nothing can reach the Puddle's UDP either.

**Chats stay on the Puddle.** Everything a Levee carries is sealed end to end (part 09) or encrypted under a key it never
sees, and it signs nothing in the Puddle's name. It sees what any carrier sees: who talks to the Puddle, when, how much,
and which routes.

One Levee serves one Puddle. It is a headless daemon with a config file and its own data folder; no database.

## Identity

A Levee has an Ed25519 key, `levee.key`, and an id `base32(SHA-256("puddle-levee-v1\n" || public key))` (part 01). Its
sealing key (X25519) is derived from the same seed, as a Pond's is: HKDF-SHA256 with info `levee-seal-v1`. It signs its
own statements only: the receipt on its attach answer, and custody receipts.

## Joining a Levee to a Puddle

1. The Levee's operator (the Puddle's owner) makes a join link on the Levee:

       levee://levee.example.org?id=<levee id>&k=<base32 of the Levee's sealing key>&token=<token>

   The token is 16 random bytes, base32; it is good once, and only while no Puddle is joined (a Levee already joined
   makes one only when told to replace its Puddle).
2. The owner gives the link to their Puddle (the desktop app: Settings, "Levee").
3. The Puddle sends `POST /levee/v1/attach`, signed for the Levee's id (part 02) and sealed to `k` (part 09):

       {"token": "<token>", "chain": <the Puddle's key chain>}

   The Levee checks the token and the chain, and the signature against the chain's current key, and keeps the Puddle's
   id and chain: from then on it is that Puddle's Levee. Answered, sealed, with a receipt signed by the Levee:

       200 {"levee": {"id": "<levee id>", "key": "<base64 public key>"},
            "address": "levee.example.org:443",
            "turn": {"port": 3478, "username": "<random>", "password": "<random>"}}

   The Puddle checks that the key hashes to the link's id and that the receipt is signed by it. `address` is where others
   reach it; `turn`, the relay's credentials (below).
4. Later attaches (after a restart, or after the Puddle rolls its keys: the new chain replaces the old) carry no token:
   only the joined Puddle's id is accepted. A wrong token, another Puddle, or a chain that doesn't check: plain `404`.

`POST /levee/v1/detach` (signed): the Levee forgets the Puddle and everything it holds for it, and can be joined again.

Both sides keep the join in a file: the Levee in its data folder, the Puddle beside its other state.

## The Puddle's address

A joined Puddle publishes a new address record (part 03) whose `addresses` are the Levee's `address` alone, with:

    "levee": {"id": "<levee id>", "key": "<base64 public key>"}

Its links (`puddle://`), phone pairing links (part 04) and first-contact answers carry the Levee's address. A Puddle that
leaves its Levee publishes a record without `levee`, with its own address again (or a new Levee's).

## Talking to the Levee

The Puddle's own requests to `/levee/v1/...` carry a request signature (part 02) for the Levee's id, but in the header
`X-Levee-Signature` (same format, same signed text), because on `send` the Puddle's request to someone else travels in
the same request with its own `X-Puddle-Signature`. Anything that fails: plain `404`, like an unknown path.

What is the Levee's own to read is sealed to it (part 09), as a request to anyone is: `attach` (whose answer is sealed
back), `peers` and a file's `ready`. The rest carry what is already sealed end to end (requests and answers between the
Puddle and others, and files under their own keys), so they go as they are. The Levee signs a receipt (part 02) on
`attach` alone, the one answer the Puddle has to believe.

## Coming in

Every request to the Levee's address whose path is not `/levee/v1/...` is for the Puddle.

**First, the Levee checks it** as the Puddle would, up to the signature (part 02): the recipient is the Puddle's id (or
`*` on a first-contact route), and the sender is someone the Puddle has told it about (below), with their current key, or
a first contact. Anything else is a plain `404`, and goes no further. A first contact (`*`: `POST /stream/v1/access`,
`/stream/v1/access/status`, a phone pairing) is rate-limited per source address and in all, and held apart from friends'
traffic. Clock skew and replays are refused as the Puddle would (`401 clock_skew`, `401 replayed`, unsealed, no
receipt).

The Puddle tells the Levee who may reach it, and again whenever that changes:

    POST /levee/v1/peers  (sealed) {"peers": [{"id": "...", "chain": [...]}, ...], "devices": [{"id": "...", "key": "<base64>"}, ...]}

`peers`: everyone with a stream the Puddle would take requests from; `devices`: its paired phones (part 04). The Levee
is the owner's own, so it may know the owner's friends; it keeps the list in its data folder and never passes it on.
Answered `204`.

**While the Puddle is attached** (below), the request is handed over at
once and the Levee waits up to 8 seconds for the Puddle's answer (less than a caller waits for any reply), which it passes back byte for byte: status, body and
the headers `X-Puddle-Receipt`, `Content-Type`, `Content-Range`. Nothing else in the stream protocol changes: the
receipt is the Puddle's own (part 02), which holds over any connection. No answer in time (the Puddle went away
meanwhile): a one-way request is spooled and answered as below; anything else is a plain `404`, so the sender tries again
as it would against an offline Puddle. A Puddle counts as attached while a request of its own waits on `inbox` over a
connection still open, or for 10 seconds after one was answered.

**While it is not**, a **one-way** request (the table below) is spooled, and answered:

    202  (no body)
    X-Puddle-Custody: v1 for=<the Puddle's id>; levee=<levee id>; sig=<base64>

`sig` is Ed25519 by the Levee's key over:

    puddle-custody-v1
    <the Puddle's id>
    <the Levee's id>
    <the request's nonce>
    <hex SHA-256 of the request's body as sent>

A sender that holds the Puddle's address record naming that Levee checks the signature against the record's key and
counts the request as **delivered**: it stops trying. (It may show "waiting at their Levee".) A custody receipt from a
Levee the Puddle hasn't announced counts for nothing, as no receipt at all. Any other request while the Puddle is away,
or a one-way one the spool has no room for, is answered a plain `404`: not delivered, try later.

| One-way: spooled while the Puddle is away | Needs the Puddle: `404` while it is away |
|---|---|
| `POST /stream/v1/address`, `access`, `access/result`, `close`, `events`, `profile`, `group/invite` | `GET /stream/v1/identity`, `POST /stream/v1/access/status` |
| `POST /stream/v1/files/{file}/request`, `granted`, `refused`, `done` | `GET /stream/v1/files/...`, `/stream/v1/media` |
| `POST /stream/v1/call/end`, `call/group/leave` | the other `call/...` routes (a call needs both ends) |
| | everything under `/device/v1/` (a phone needs its Puddle) |

### Handing over: `inbox` and `answer`

    GET /levee/v1/inbox?after=<n>

held open up to 25 seconds until something is there, answered:

    200 {"items": [{"n": 41, "live": true, "received": <ms>, "method": "POST", "target": "/stream/v1/events",
                    "headers": {"X-Puddle-Signature": "...", "X-Puddle-Seal": "...", "Content-Type": "...", "Range": "..."},
                    "body": "<base64>"}, ...]}

Items are numbered in the order they came. `after` says the Puddle has taken everything up to `n`: spooled items up to
it are deleted. `live` items wait for an answer; spooled ones (`live: false`) were answered by the custody receipt
already. A body over 256 KiB is not inline: the item has `"body_size"` instead, and the Puddle fetches it with
`GET /levee/v1/inbox/<n>/body`. Only the headers listed are passed; `Range` only on a `GET`.

The Puddle checks each item exactly as if it had come directly (part 02), except that clock skew is measured against
`received` instead of its own clock: a spooled request may be days old. The Levee has already refused replays, and
keeps the nonces of what it spools until it is handed over.

    POST /levee/v1/answer/<n>

with the headers `X-Levee-Status: <status>`, and `X-Puddle-Receipt`, `Content-Type`, `Content-Range` as the Puddle would
have answered, and the answer as the body. `204`, or `404` if no such live request is waiting any more.

## Going out

    POST /levee/v1/send

The Puddle's request to someone else, as it would have sent it directly, plus where it goes:

| header | |
|---|---|
| `X-Levee-To` | the address to call (`host`, `host:port`, `[v6]:port`) |
| `X-Levee-Method`, `X-Levee-Target` | the request's method and target |
| `X-Levee-Timeout` | seconds to wait for the answer, 1 to 60 (a Pond holds `events` up to 25) |
| `X-Puddle-Signature`, `X-Puddle-Seal`, `Content-Type`, `Range` | passed on as they are |

and the request's body as the body. The Levee makes the request over HTTPS, checking no certificate (part 09), and
answers `200` with `X-Levee-Status: <their status>`, their `X-Puddle-Receipt`, `X-Puddle-Custody`, `Content-Type` and
`Content-Range`, and their body. The Puddle checks the receipt itself, exactly as if it had called them: the Levee can
hold an answer back but not make one up. When the far end can't be reached, `200` with `X-Levee-Status: 0` and
`X-Levee-Error: unreachable` (or `timeout`), and the Puddle's outbox tries later, as it would.

The Levee keeps nothing that goes out. A signed request is good for five minutes (part 02), so holding one for a friend
who is away would only make it stale; the Puddle's outbox keeps trying, and a friend with a Levee of their own is
reached there anyway. It refuses addresses no one should dial, as a Puddle does (unspecified, multicast, link-local).

## Files

A file the Puddle sends (part 03, "Files") goes to its Levee first, so friends can fetch it while the Puddle is off. It
is **encrypted under a key of its own** before it leaves the Puddle, so the Levee holds only what it can't read.

**The key travels in the message.** A file in a message from a Puddle behind a Levee carries `key`: base64 of 32 random
bytes. The event is signed, and sealed to each recipient on the way (part 09), so only the chat's members see it.

**Pieces**, as part 10 seals a letter's: `hashes` (the file's size as 8 bytes big-endian, then its chunk hashes) and
chunk `n` (1 MiB, the last shorter), each sealed under the file's key as records of up to 64 KiB, record `k` of piece `p`
at index `p × 64 + k` (`p` for `hashes` is 2^40), with status `0`, the last record marked.

The Puddle puts them:

    POST /levee/v1/files/<file>/<piece>        the sealed piece as the body; piece is "hashes" or a number
    POST /levee/v1/files/<file>/ready  (sealed) {"for": ["<peer id>", ...]}

`ready` says the file is complete and who may fetch it; the Levee checks it holds every piece. A file is at most
`files.max_size` on the Levee (its config).

**A friend fetches** from the address the message came from (the Puddle's, so its Levee):

    GET /levee/v1/files/<file>/<piece>         signed for the Puddle's id, by someone in `for`

answered `200` with the sealed piece (not sealed again, and with no receipt: the hashes prove it), and checked against
the file's id and its chunk hashes as any file is. When it has the whole file:

    POST /levee/v1/files/<file>/done           signed, by someone in `for`

and the Levee strikes them off; when nobody is left, it deletes the file. A friend who fetched it once and asks again
asks the Puddle (`files/{file}/request`, as today); if the Puddle grants it, it puts the file on its Levee again, `for`
that friend, before answering `granted`. A file nobody fetches is deleted after `files.keep_days` (30 by default).
Someone not in `for`, a file it doesn't hold: plain `404`.

The Puddle is told when a friend is done, on `inbox`, as `{"n": .., "file_done": {"file": "...", "by": "<peer id>"}}`.

## Calls: the relay

Nothing can reach a Puddle behind a Levee by UDP either, so its calls (part 08) go through a relay on the Levee: a TURN
server (RFC 8656) over UDP, for its own Puddle only, using the `turn` credentials the attach answer gave (long-term
credentials, realm the Levee's id). It listens on one UDP port (`turn.port`, 3478 by default) and relays from a small
range of its own (`turn.relay_ports`), which a reverse proxy doesn't carry: they are published directly, beside the
HTTPS port the proxy forwards.

- The Puddle offers only relayed candidates (ICE transport policy "relay"), so nothing shows its home address, and
  sets `udp` to `0` in its offers and answers: the other side adds no candidates of its own making and uses the SDP's.
- The other side needs nothing new: it reaches the relayed candidates as it would any. Two Puddles both behind Levees
  meet relay to relay.
- The same relay carries the Puddle's phone legs and its voice in Ponds (part 08, part 05).
- A Levee relays only for allocations its Puddle made; the media is DTLS-SRTP end to end, so it sees sizes and timing.

## What a Levee keeps

In its data folder, as plain files: its key, the join (the Puddle's id and chain, the TURN credentials, the open token),
the peers list, the spool (one file per request) and the files (one folder per file). Limits are the operator's, in its
config: how much the spool may hold (1 GiB by default) and how long (30 days, then the oldest are dropped), the largest
file and how long files are kept.

## Not yet

- **Holding what goes out.** A friend who is away and has no Levee is reached when the Puddle's outbox next tries,
  which needs the Puddle on. Holding it at the Levee would need requests that stay good for longer than five minutes.
- **Several Levees** for one Puddle, and a Puddle reachable both directly and through its Levee: one address, the
  Levee's, for now.
- **Hiding routes from the Levee** (part 09, "Open decisions", 3).
- **Voice over HTTPS** for networks that block UDP.
