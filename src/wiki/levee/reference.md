---
title: Reference
nav_order: 30
---

*Moved here from the `ezp2p/levee` README on 2026-11-25.* Setting one up is in
[Installation](/wiki/levee/installation/) and [Binding a Levee](/wiki/levee/binding/).

## What a Levee does

The public side of one Puddle. Your Puddle connects **out** to its Levee and needs no open ports; everyone else reaches
your Puddle at the Levee's address:

- **Friends, phones and new contacts** reach your Puddle at the Levee's address, which stays the same when your home
  network changes.
- **While your Puddle is on**, what they send passes straight through.
- **While it is off**, what they send that needs no answer (messages, profiles, address changes, friend requests) waits at
  the Levee and is handed over when your Puddle comes back. The sender is told it arrived (a custody receipt the Levee signs).
  What waits longer than `spool.keep_days` (or is still there when your Puddle leaves) is given up, and both ends are
  told: the sender, so it counts as not delivered and can be sent again once you are back; your Puddle, so it can tell
  you something from that friend expired.
- **What your Puddle sends** goes out through the Levee too, so nobody you talk to learns your home address.
- **Files you send** wait at the Levee, encrypted under keys it never sees, until each friend has fetched them; then they
  are deleted. A friend who asks again later asks your Puddle, which puts the file there again.
- **Calls** go through the Levee's relay (a small TURN server), since nothing can reach your Puddle by UDP either.

**Your chats stay on your Puddle.** Everything the Levee carries is sealed end to end, or encrypted under a key it doesn't
have, and it signs nothing in your name. It does see what any carrier sees: who talks to your Puddle, when and how much.
Run it yourself, or have someone you trust run it.

One Levee serves one Puddle. It is a headless daemon with a config file and a data folder: no database, no app.

## The protocol

A Levee speaks the [Puddle Protocol](/wiki/protocol/) (`ezp2p/protocol`, in the levee repository as the submodule
`third_party/protocol`): [part 06](/wiki/protocol/levee/) is the Levee's own, and it uses the protocol's library, **libpuddle-proto** (`third_party/protocol/lib`), for ids, key chains,
signatures, receipts and sealing, as Puddle and Pond do.

## levee.yaml

| Setting | Default | |
|---|---|---|
| `listen`, `port` | `0.0.0.0`, `8443` | where leveed takes HTTPS |
| `address` | (required) | how others reach your Puddle, `host[:port]`; what its links say |
| `data_dir` | (required) | the Levee's key, certificate and everything it keeps |
| `threads` | 2 | |
| `spool.max_mb`, `spool.keep_days` | 1024, 30 | what waits for your Puddle while it is off; the oldest goes first, and what is given up on is said to the sender and your Puddle. `keep_days` may be a fraction (`0.5`: twelve hours) |
| `files.max_mb`, `files.total_mb`, `files.keep_days` | 100, 4096, 30 | files left for friends |
| `trusted_proxies` | none | reverse proxies in front (`[127.0.0.1, 172.16.0.0/12]`): a request from one is taken to come from the address its `X-Forwarded-For` names |
| `turn.port`, `turn.relay_ports`, `turn.public_ip` | 3478, `49160-49199`, the address's host | the relay for calls (UDP); `turn: false` turns it off |

## leveectl

| | |
|---|---|
| `leveectl init` | make the key and certificate; says the Levee's id |
| `leveectl join` | a link for your Puddle to join with (good once) |
| `leveectl join --replace` | the same, when another Puddle is joined: the one that joins with it replaces it, and everything kept for the old one goes |
| `leveectl status` | who is joined, how much waits |

## The data folder

Plain files, nothing else: `levee.key` (keep it: a new key is a new Levee, and your friends would no longer believe its
custody receipts until your Puddle tells them), `cert.pem`/`key.pem`, `join.json`, `peers.json` (your friends' public keys,
so strangers get nowhere, and where they are and which Levee answers for them, so they can be told what was given up on),
`spool/`, `undelivered.json` (notices owed to senders, and what your Puddle is to be told), `next_n` (item numbers only
grow, across restarts too) and `files/`.

## Tests

In the [levee repository](https://github.com/ezp2p/levee/tree/dev):

`ctest --test-dir build`: `config` (levee.yaml, and where a request comes from behind a proxy), `store` (the data folder), `turn` (the relay, as a TURN client and a peer meet it) and `levee`
(leveed as a Puddle and its friends meet it: joining, spooling, passing through, a notice from a friend's Levee, sending,
files, leaving). `e2e` puts a real `puddled` behind it (`-DPUDDLED=<path>`; skipped without one), including a message the
Levee gives up on, which both Puddles are told about and the sender sends again.
