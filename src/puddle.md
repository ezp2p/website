---
title: Puddle
description: Puddle is self-hosted chat that runs on your own computer and talks directly to your friends' Puddles.
permalink: /puddle/
image: /assets/img/feature-puddle.svg
og_image: /assets/img/og-puddle.png
image_alt: Two Puddles connected directly, with light passing between them.
---

# Puddle

<p class="lede">Your own chat, on your own computer, with no servers in between.</p>

Puddle is the app you run. It keeps everything that is yours (your identity, your friends, your chats and your files) on
your own machine, and holds a port open so your friends' Puddles can reach it. You add friends directly, and chat over the
internet the way chat was originally meant to work.

## What it does

- **Direct chats and groups.** Messages, edits and deletions are signed by whoever wrote them and delivered straight to
  each person in the chat.
- **Files.** Shared files are fetched in checked chunks from whoever has them.
- **Calls.** Voice and video calls between friends.
- **Profiles.** Choose how you appear to each person: a work profile, one for friends, one for family. Each has its own
  name, picture and blurb.
- **Ponds.** Join community servers from the same app, with a `pond://` invite link.

## Streams: how Puddles talk

When two people become friends, their Puddles open a **stream**: a trusted connection between the two. Nothing passes
between two Puddles without one, apart from asking for one. Every request on a stream is signed with the sender's key,
and every answer is signed back, so each side knows exactly who it's talking to.

Your identity is a key chain that starts from a **recovery phrase**. Keep the phrase safe: it's how you get your identity
back on a new machine, and how you can roll to new keys if one is ever lost.

## Ways to run it

- **The desktop app.** Run Puddle on your computer, ideally one that's always on. This is the simplest way to start.
- **`puddled`.** The same Puddle with no window, for a home server or a VPS. There's a Docker image.
- **A phone.** The phone client doesn't host anything. It connects back to your own Puddle, wherever that runs, and is
  paired with it by keys.

## Nothing is public

Every route on a Puddle is checked: your own apps use your owner token, and other Puddles sign their requests. A request
that fails a check gets the same `404` as a path that doesn't exist, so a stranger can't even tell there's a Puddle
there.

## Next

- [Install Puddle]({{ '/wiki/puddle/installation/' | relative_url }})
- [Puddle wiki]({{ '/wiki/puddle/' | relative_url }})
- [Source on GitHub](https://github.com/ezp2p/puddle)
