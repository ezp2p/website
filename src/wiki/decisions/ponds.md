---
title: Ponds
nav_order: 60
---

The design is in [Pond design](/wiki/pond/design/), [Pond: Direct messages](/wiki/pond/design/dms/),
[Puddle: Ponds](/wiki/puddle/design/ponds/) and [Protocol: Ponds](/wiki/protocol/ponds/).

## The Pond itself

### Is a Pond a Puddle?

**Decided:** no. A Pond is a community server, like a Discord server: someone runs it, it has channels, and people
join with an invite. It is its own program (`pondd`, `pondctl`, MariaDB), and its members are Puddles, each connecting
with the same key it uses everywhere else.

### Who talks to the Pond?

**Decided:** **the Puddle, never the app.** The Puddle holds the owner's key, so it signs requests to the Pond. The
window and the phone use the Puddle's owner API, as for everything else. A Puddle behind NAT or a Levee works the same,
because the Puddle always opens the connection.

### How does someone get in?

**Decided:** **invite only**: a `pond://` link with a token, which can have a number of uses and an expiry. There is no
other way in. Since protocol 13, a Pond can also ask new members to fill in an entry form for an administrator to
accept. Joining a public Pond from its address alone is being discussed (ezp2p/pond#41).

### What does a Puddle keep of a Pond?

**Decided:** the newest 200 messages of each channel, cleaned before they are kept. Older history is fetched from the
Pond when the owner scrolls back. Leaving deletes it all.

### Bans

**Decided:** by user id. A member who makes a new identity is a new member. Banning by address or device isn't
possible, since the Pond knows nothing else about them.

### Can members trust what the Pond shows?

**Decided for now:** members trust the Pond for what it shows, as they trust a Discord server. Messages signed by
their authors, so a Pond can't forge them, come later (ezp2p/pond#37).

## Files in a Pond

### Who serves the bytes?

**Decided:** **the Pond keeps the file**, and members don't serve it to each other.

**Why:** a Pond's members are strangers, mostly offline and often behind NAT. A Pond is meant to be the place that is
always up, so it serves the bytes, as a Discord server does. This costs the operator disk and bandwidth, which is why
the sizes are theirs to choose.

### What shape, and where?

**Decided:** chunks and ids exactly as Puddles have them, so a Puddle that already holds a file never fetches it
again, and the Pond can check every chunk. Files are kept on disk, not in MariaDB, so the database stays small enough
to back up easily. A file is sent before its message, so nobody sees a message whose file never arrives. Each member
has a rate on chunks.

### Public links to files?

**Decided:** not planned. A file is only reachable by a member's signed request.

### Open

A total cap on file storage (ezp2p/pond#30), allowed file types (ezp2p/pond#32), deleting a file with its last message
(ezp2p/pond#33), thumbnails (ezp2p/pond#29), and a total bandwidth limit (ezp2p/pond#34). Who may send files is now
the `attach_files` permission (protocol 13).

## Roles and permissions

### Ranks

**Decided:** three ranks: **operator**, **administrator** and **member**. Becoming one is an offer that has to be
accepted. An operator or administrator has every permission, whatever roles they hold, and roles never make anyone an
operator or administrator.

### Roles like Discord's

**Decided:** named roles with permissions, a colour, an order, and an option to show them apart in the members list
*(protocol 10, 2026-11-23)*. Permissions are set for everyone and overridden per channel by role *(protocol 13)*. A
member may act on someone (kick, ban, mute) only if that person's highest role is below their own. A member with
`manage_roles` works only below their own highest role.

**Open:** what operators may do that administrators may not (ezp2p/pond#46), per-member overrides (ezp2p/pond#44), and
"Is Administrator" and "Is Moderator" groupings (ezp2p/pond#50).

## Direct messages through a Pond

The owner's answers, built 2026-11-21:

| Question | Decision |
|---|---|
| Relay, or introduce members to each other? | **Relay.** The Pond relays between members and stores nothing once a message is delivered. While the other side is away, the *sender's* Puddle holds the message and sends it again. |
| Friend offers | Yes, from either side. Only that member learns the address. |
| Blocks | As Puddle's blocks: kept by the Puddle, silent. There are two: block direct messages only, and block everywhere, which also hides their messages in every Pond. |
| Who may write | Configurable. The admin turns DMs on or off for the Pond, DMs are only between current members, and each member may turn them off for themselves in a Pond. |
| What the Pond sees | Who writes to whom, for rate limits. It never stores messages, since its admin can't moderate what they can't see. |
| Files | Yes, bundled in, relayed and never stored. |
| How long the sender keeps trying | **30 days.** |
| Where they show | In the Puddle's direct messages, as **"Ann @ Lily Pad"**, so they can't be confused with a friend. |
| Where the format goes | Protocol part 10, [Letters](/wiki/protocol/letters/), for Levee and Drip to reuse. |

**Why:** the letters are sealed end to end and signed by their authors, so the Pond can neither read nor forge them.
