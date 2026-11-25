---
title: Drip
description: Drip is peer-to-peer social media, built like Puddle. You host your own feed, and the people you choose pull it down to theirs. Coming soon.
permalink: /drip/
image: /assets/img/feature-drip.svg
image_alt: One person's feed, pulled down by each of the people they share it with.
og_image: /assets/img/og-drip.png
---

# Drip <span class="status">Coming soon</span>

<p class="lede">Social media where you host your own feed, and you decide exactly who sees it.</p>

> **Drip is an idea for now.** Nothing is built yet, and the details may change. We'll be starting on it soon.

Puddle is for talking with people you know, and a Pond is for a community. **Drip** is for sharing: photos, updates and
whatever else you'd post to a feed. It works the way Puddle does, so there's no platform in the middle owning your posts,
your audience or you.

## How it will work

1. **You run Drip, and it hosts your feed.** Like a Puddle, your Drip runs on your own computer, and your feed lives
   there.
2. **Posting is writing to your own feed.** When you post, you're just creating a post on your own device. Nothing is
   uploaded anywhere.
3. **People add you, the way friends do in Puddle.** Your friends, your family, whoever you like add you, and once you
   accept, your Drips are connected by a [stream]({{ '/terminology/' | relative_url }}#stream): a trusted connection
   between the two of you.
4. **Their Drips pull your feed down.** Over that stream, their Drip fetches your new posts and keeps them on their
   device, ready to read.

## You decide, completely

What you share, and who you share it with, is entirely up to you as the owner of your Drip. Your posts only ever go to
the people you've accepted, and only the posts you've chosen to share with them. There's no public timeline unless you
want one, no algorithm deciding who sees what, and no company that can read, sell or remove your posts.

That's really what Drip is for. It's designed so that **families can keep in touch** through a feed, the way social
media should work: no advertisements, nothing pushed at you by an algorithm, just the life updates of the people you
care about. Grandparents see the new photos, cousins catch up on each other's news, and everyone posts when they have
something to share, safely and responsibly, without it all getting lost in a busy group chat.

## Built on Puddle

Drip reuses what Puddle already does well:

- **One you.** Your Drip identity is your Puddle identity: the same keys and the same recovery phrase.
- **Streams.** The same trusted, signed connections Puddle uses between friends, so only the people you've accepted can
  ask for your feed. To everyone else, there's nothing there.
- **Signed posts.** Every post is signed by you, so the people you share with know it's really yours and unchanged.
- **Levees.** A [Levee]({{ '/levee/' | relative_url }}) can keep your feed reachable while your computer is off.

## Follow along

- The early protocol notes are [part 07 of the Puddle Protocol](https://github.com/ezp2p/protocol/blob/master/spec/07-drip.md).
- The code will live at [ezp2p/drip](https://github.com/ezp2p/drip).
- The [roadmap]({{ '/features/' | relative_url }}#drip) will show progress once work starts.
