---
title: Pools
description: A Pool is a Pond without a server, a community held and shared by its members' Puddles. In development.
permalink: /pools/
image: /assets/img/feature-pools.svg
og_image: /assets/img/og-pools.png
image_alt: Several seeders joined to each other, each with Puddles of its own, with light passing between them.
---

# Pools <span class="status">In development</span>

<p class="lede">
    A true Peer-to-Peer Community Server
</p>

> **Pools are in development.** Nothing here can be installed or tried yet, and the details below may change as the
> design settles. Follow along on the [roadmap]({{ '/features/' | relative_url }}#pools) and in
> [ezp2p/puddle#52](https://github.com/ezp2p/puddle/issues/52).

A [Pond]({{ '/pond/' | relative_url }}) is a community server: someone runs it, and the members' Puddles join it. A
**Pool** does the same job with nobody running anything. Channels, members, files and voice are all there, but the
content lives on the members' own Puddles, which share it between them, much like BitTorrent shares files.

Pools are built into Puddle itself. There's no separate program to install.

## How it works

- **Auth Puddles are in charge.** The Puddles that create a Pool are its **Auth Puddles**. They can make other members
  Auth Puddles, or give them **roles** (named sets of permissions). There's no voting.
- **Seeders keep it running.** A member can choose to **seed**: to keep the Pool's content and serve it to others. Auth
  Puddles seed by default. Seeders pass new messages on to each other, a few at a time, so nobody has to send to
  everyone and a Pool can grow to thousands of members.
- **Your address stays private.** Only seeders show their address to the Pool. Everyone else connects out to a few
  seeders and sends and fetches through them.
- **Nothing can be forged.** Every message and admin change is signed by whoever made it, the same way as in a chat
  between friends. A seeder can fail to pass a message on, but it can't change or fake one, and a missed message is
  fetched again from another seeder.
- **History is shared out.** Auth Puddles keep the whole history. Other seeders keep all of it or just the recent part.
  A member who doesn't seed keeps the newest messages of each channel, as with a Pond, and fetches older ones when they
  scroll back.
- **Joining doesn't wait.** An invite is signed by an Auth Puddle, so any online seeder can let the new member in.

## Pool or Pond?

|                     | Pond                               | Pool                                   |
|----------------------|-------------------------------------|----------------------------------------|
| Who runs it         | Someone, on a server of their own  | Nobody: its members' Puddles           |
| Where history lives | On the Pond                        | Shared between seeders                 |
| Who is in charge    | The Pond's admin, with `pondctl`   | Its Auth Puddles                       |
| Voice               | Voice channels                     | A mesh, about 8 people per channel     |
| Status              | Ready to test                      | In development                         |
| Shops               | Supported                          | Not Supported/really possible          |


## Not yet decided

- End-to-end encryption of Pool content.
- Moving a community from a Pond to a Pool, or back.

## Next

- [Feature roadmap]({{ '/features/' | relative_url }}#pools)
- [Pools in the terminology]({{ '/terminology/' | relative_url }}#pool)
- [The design issue on GitHub](https://github.com/ezp2p/puddle/issues/52)
- [The Pools project board](https://github.com/orgs/ezp2p/projects/2)
