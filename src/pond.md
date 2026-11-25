---
title: Pond
description: A Pond is a community server for Puddle, with channels and many members, joined by invite link.
permalink: /pond/
image: /assets/img/feature-pond.svg
image_alt: Many Puddles joined to one Pond, with light passing through the hub.
---

# Pond

<p class="lede">A place for a community to gather, joined from your Puddle.</p>

Puddles are for talking privately with people you know. A **Pond** is the public side: a community server, like a
Discord server, with text channels and many members. Someone runs a Pond, creates channels and gives out invite links.
People join by pasting a link into their Puddle.

## How it works

A Pond is a separate program from Puddle, with its own code. It's built to be run by someone looking after a community,
on a server of their own.

- **`pondd`** is the service. It has no window, and serves HTTPS on one port.
- **`pondctl`** is the admin's tool. It runs on the same machine, with the same config, and creates the Pond, its
  channels and its invites.

Messages are stored in MariaDB on the Pond.

## Joining a Pond

1. The admin runs `pondctl invite create`, which prints a `pond://…` link. Invites can be limited by number of uses and
   by expiry.
2. You paste the link into Puddle (the **+** at the bottom of the server rail).
3. Your Puddle joins and the Pond's channels appear beside your chats.

Your Puddle always makes the connection to the Pond, never the other way round, so joining works from behind a home
router with no ports open. It holds one request open for the Pond's events, so new messages, channels and members arrive
as they happen. It keeps the newest 200 messages of each channel and asks the Pond for anything older.

Every request your Puddle makes to a Pond is signed with your key, the same way it signs requests to friends.

## Status

Text channels are built. Roles, files and voice are planned.

## Next

- [Run a Pond]({{ '/wiki/pond/running-a-pond/' | relative_url }})
- [Pond wiki]({{ '/wiki/pond/' | relative_url }})
- [Source on GitHub](https://github.com/ezp2p/pond)
