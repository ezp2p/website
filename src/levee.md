---
title: Levee
description: A Levee is a relay that gives a Puddle a steady public address and holds its messages while it's offline.
permalink: /levee/
image: /assets/img/feature-levee.svg
og_image: /assets/img/og-levee.png
image_alt: A friend's Puddle reaching another Puddle through its Levee, with light passing along the line.
---

# Levee

<p class="lede">A steady address for a Puddle that can't take connections from the internet.</p>

A Puddle normally needs a port open so friends can reach it. That isn't always possible: some networks don't allow it,
and a home address can change. A **Levee** solves both. It runs on a server with a public address (rented, or a VPS of
your own), and your Puddle connects *out* to it. Friends then reach your Puddle at the Levee's address.

## What a Levee does

- **Passes everything through** while your Puddle is connected.
- **Holds messages** that arrive while your Puddle is offline, and hands them over when it comes back.
- **Keeps your address the same** when your home network changes.
- **Sends for you** too: what your Puddle sends goes out through the Levee, so nobody you talk to learns your home
  address.
- **Holds your files** for friends, encrypted under keys it never sees, until each friend has fetched them.
- **Relays calls**, since nothing can reach your Puddle directly for voice and video either.

## What a Levee can't do

**Your chats stay on your Puddle.** A Levee only holds what is in transit. It decrypts nothing and signs nothing in your
name. Everything it holds was signed by its sender, and your Puddle checks it exactly as if it had arrived directly.

A Levee is a middle, so the protocol makes it an *announced* one. Your Puddle publishes which Levee answers for it, and
your friends' Puddles can tell that Levee apart from anyone trying to sit in between. When a Levee takes a message for
you while you're away, it gives the sender a signed receipt, so the sender sees "waiting at your Levee" rather than
"delivered".

## Status

Levee works and is ready to test. It's a headless service (`leveed`) with an admin tool (`leveectl`): no database, just a
config file and a data folder. One Levee serves one Puddle. Run it on a server with a public address, such as a small
VPS, then join your Puddle to it with a one-time link.

What it says on the wire is
[part 06 of the Puddle Protocol](https://github.com/ezp2p/protocol/blob/master/spec/06-levee.md).

## Next

- [Install a Levee]({{ '/wiki/levee/installation/' | relative_url }})
- [Bind it to your Puddle]({{ '/wiki/levee/binding/' | relative_url }})
- [Levee wiki]({{ '/wiki/levee/' | relative_url }})
- [Source on GitHub](https://github.com/ezp2p/levee)
