---
title: "10. Letters: a message sealed from one Puddle to another, carried by someone else"
nav_order: 11
---

*Moved here from `ezp2p/protocol/spec/10-letters.md` on 2026-11-25.*

**Status:** built in Puddle and Pond (protocol 8 of `/pond/v1`, feature `dms`), 2026-11-21, for direct messages between
members of a Pond. A Levee (part 06) or Drip (part 07) could carry the same thing later; nothing here is particular to a
Pond but the section "Through a Pond".

## Why

Two members of a Pond can write to each other without being friends: no stream (part 03), and no address given out.
What one writes must reach only the other, and must be known to be theirs, though a third party carries it. A **letter**
is that: signed by its author, sealed to its reader, and opaque to whoever carries it. The carrier sees who writes to
whom, when and how much, so it can limit the rate; it can withhold a letter, as any carrier can, but not read, change or
forge one.

## Keys

Nothing new. The author signs with its current signing key and seals to the reader's encryption key, both from their
chains (part 01). The author has the reader's chain from the carrier, and checks it against the reader's id: the id is
the hash of the chain's first key, so a carrier that answered with another key would have to forge a chain for that id,
which it can't. The reader checks the author's signature against the author's chain the same way.

## A letter

The letter's own text, JSON, signed:

```json
{"v": 1, "kind": "message", "from": "<author id>", "to": "<reader id>", "pond": "<the carrier's id>", "id": "<64 hex>",
 "ts": <ms>, ...}
```

| `kind` | what else it carries | `id` |
|---|---|---|
| `message` | `event`: a chat event (part 03: a message, an edit or a deletion), exactly as signed; `event_sig`: its signature; `keys`: one per file the event names, base64 of 32 bytes (below) | the event's id: the SHA-256 of its bytes, hex |
| `offer` | `link`: a `puddle://` link to the author's Puddle, with an invite good once (part 03), to become friends | random |
| `receipt` | `ids`: the letters it says arrived | random |

The event in a `message` is signed by the same key as the letter, for the chat whose id is
`base32(SHA-256("pdm" || pond || the two user ids, sorted))`. Both Puddles keep it in that chat, as they keep a DM's
events, so edits and deletions work as they do between friends.

**Signed**: `sig` = the author's signature over `"puddle-letter-v1\n"` followed by the letter's text, written
`"<kid>:<base64>"` as an event's is (part 02). **Sealed**: the plaintext `{"letter": "<the letter's text>", "sig": "..."}` is
sealed with HPKE exactly as part 09 seals a request body (`DHKEM(X25519, HKDF-SHA256)`, `HKDF-SHA256`,
`ChaCha20-Poly1305`, base mode, no associated data), to the reader's encryption key, with `info` =
`puddle-letter-v1\n<from>\n<to>\n<pond>\n<id>`. What travels is `enc` (base64 of 32 bytes), `sealed` (base64), the
`id`, and `kid`: the hex SHA-256 of the encryption key it was sealed to.

The reader opens it, checks the signature against the author's chain, and checks that `from`, `to`, `pond` and `id` are
what the carrier said and that it is the reader. A letter that fails any check is dropped.

## Receipts and trying again

The reader answers every `message` and `offer` with a `receipt` letter, sealed and carried the same way, also when it
dropped the letter unread because it blocks the author: a block is never told. A receipt is not answered.

The author keeps each letter until its receipt comes: the carrier keeps nothing. When the carrier says the reader isn't
there, the author tries again when told the reader is back, or after a while (15 minutes, doubling up to 4 hours). When
the carrier took it but no receipt came within a minute, the author sends it again, doubling, since a reader that had
just gone may still have looked present. The reader drops a letter it has already kept, by its `id`. After 30 days
without a receipt, the author gives up and says so.

## Files

A `message` whose event names files (part 03, "Files") carries one key per file. Each file goes in **pieces**, asked for
by the reader and passed on by the carrier, never kept by it:

- the piece `hashes`: the file's size as 8 bytes big-endian, then its chunk hashes (32 bytes each, as part 03 lists them);
- piece `n`: chunk `n` of the file (1 MiB, the last one shorter).

A piece is sealed under the file's key as records of up to 64 KiB (part 09's answer records: ChaCha20-Poly1305 under that
key), record `k` of piece `p` with the index `p × 64 + k` (`p` for `hashes` is 2^40), the file's place in the letter as its
status, and the last record marked. The reader checks the hashes against the file's id and each chunk against its
hash, as for any file.

## Through a Pond

The carrier is a Pond the two are members of (part 05). Its routes, in `/pond/v1`:

- `GET /pond/v1/members/{member}/chain`: a member's chain, to seal to and to check signatures with.
- `POST /pond/v1/dms/send` `{to, id, kid, enc, sealed}` (sealed up to 128 KiB as base64): `200 {"relayed": true}` when the
  reader's Puddle is following the Pond's events (it held a request on `/pond/v1/events` in the last 15 seconds), and the
  letter goes to it on that request as the event `dm` `{id, from, kid, enc, sealed, ts}`, for it alone; `{"relayed": false}`
  when it isn't, and the Pond, which keeps no letter, later sends the author the event `dm_back` `{member}` when that
  member's Puddle follows again. Neither event is kept in the Pond's event log, nor numbered; they are in memory only.
  `404` if either is not a member now; `409 not_accepted` if the reader takes no direct messages there; `409 dms_off` if
  the Pond relays none; `429 slow_down`, or `too_many_new` past 20 new people a day.
- `GET /pond/v1/dms/files/{letter}/{n}/{piece}?from=<author>`: the reader asks for a piece. The Pond sends the author the
  event `dm_want` `{to, letter, file, part}` and waits up to 30 seconds; `409 away` if the author's Puddle isn't
  following, or it didn't send it.
- `POST /pond/v1/dms/files/{letter}/{n}/{piece}?to=<reader>` (the sealed piece): the author's answer, passed on to the
  request waiting for it. `404 not_asked` if none is.
- `POST /pond/v1/dms/settings` `{accept}`: whether the member takes direct messages there (a member's `dms` says it to
  everyone). The Pond's admin turns them off for the whole Pond, or files in them (`pond.dms` `{on, files_max}` in
  `/info`, and the features `dms` and `dm_files`).

Blocks are the reader's own and stay in the reader's Puddle: the Pond never learns of them.

## Not yet

- **A key rolled while a letter was on its way**: the reader can't open a letter sealed to its previous encryption key,
  and drops it; the author tries again with the new chain after a while (it asks the carrier for the chain afresh on a
  second try). Keeping the previous key for a few days, just to open letters, would close that gap.
- **Hiding the author from the carrier** ("sealed sender") would cost the carrier its rate limits.
