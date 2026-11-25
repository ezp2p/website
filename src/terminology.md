---
title: Terminology
description: The words ezp2p uses for its programs, identities and connections, and what each one means.
permalink: /terminology/
layout: terminology
lede: The words used across Puddle, Pond and Levee, and what they mean.

# One section per topic, in the order they show. Each term has:
#   term:       the word, as it should be written
#   aka:        other names for it (optional list)
#   definition: what it means (Markdown)
#   see:        other terms on this page to link to (optional list; must match a `term` exactly)
#   spec:       a part of the Puddle Protocol that covers it, e.g. 03-streams (optional)
sections:
  - title: The programs
    terms:
      - term: Puddle
        definition: >-
          The app you run. It keeps your identity, friends, chats and files on your own computer and talks straight
          to your friends' Puddles. [More about Puddle](/puddle/).
        see: [puddled, Stream]
      - term: puddled
        definition: The same Puddle with no window, for a home server or a VPS. There's a Docker image.
        see: [Puddle]
      - term: Pond
        definition: >-
          A community server, like a Discord server, with channels and many members. Someone runs one and gives out
          invite links; people join from their Puddle. [More about Pond](/pond/).
        see: [pondd, pondctl, Invite link]
        spec: 05-ponds
      - term: leveed
        definition: The Levee service. It has no window, serves HTTPS on one port, and relays calls over UDP.
        see: [Levee, leveectl]
      - term: leveectl
        definition: >-
          The Levee admin's tool. It sets up the Levee's key, prints the one-time link your Puddle joins with, and
          shows what is waiting.
        see: [Levee]
      - term: pondd
        definition: The Pond service. It has no window and serves HTTPS on one port.
        see: [Pond]
      - term: pondctl
        definition: >-
          The Pond admin's tool. It runs on the same machine as `pondd`, with the same config, and creates the Pond,
          its channels and its invites.
        see: [Pond, Invite link]
      - term: Pool
        definition: >-
          A Pond without a server, still in development. A community (channels, members, files, voice) made of its
          members' Puddles, which hold and share its content between them, so nobody has to run a server for it.
          [More about Pools](/pools/).
        see: [Pond, Auth Puddle, Seeder]
      - term: Levee
        definition: >-
          A relay for a Puddle that can't take connections from the internet. It gives the Puddle a fixed address and
          holds messages and files while it is offline, without being able to read them.
          [More about Levee](/levee/).
        see: [leveed, leveectl, Custody receipt]
        spec: 06-levee
      - term: Phone client
        definition: >-
          A thin client of your own Puddle. It holds no identity keys and no chats; it connects back to your Puddle
          and signs every request with a key of its own.
        see: [Device, Pairing]
        spec: 04-devices
      - term: Drip
        definition: >-
          Peer-to-peer social media, built like Puddle. You host your own feed, and the people you've accepted pull it
          down to theirs over a stream. Coming soon. [More about Drip](/drip/).
        spec: 07-drip

  - title: Identity and keys
    terms:
      - term: Identity
        definition: >-
          Who you are to everyone else: a signing key, an encryption key and a roll key, all derived from your
          recovery phrase. Everything that matters is signed by it.
        see: [User id, Key chain, Recovery phrase]
        spec: 01-identity
      - term: Recovery phrase
        definition: >-
          The words your identity is made from. Shown to you once and never stored. It's how you get your identity
          back on a new machine, and how you roll to new keys.
        see: [Identity, Key roll]
      - term: User id
        definition: >-
          A 52-character id worked out from your first keys. It never changes when your keys roll, and anyone given
          your key chain can check it belongs to you, with no registry.
        see: [Key chain]
        spec: 01-identity
      - term: Key chain
        aka: [chain]
        definition: >-
          The signed list of every key your identity has had, from the first. Others use it to check that a key
          really is yours.
        see: [User id, Key roll]
        spec: 01-identity
      - term: Key roll
        aka: [rolling keys, rotation]
        definition: >-
          Swapping your keys for new ones, for example if one is lost. It needs your recovery phrase and adds a line
          to your key chain; your user id stays the same.
        see: [Recovery phrase, Key chain]
      - term: Profile
        definition: >-
          How you appear to someone: a name, a picture and a blurb. You can keep several (work, friends, family) and
          choose which each person sees.
      - term: Device
        definition: >-
          A phone client paired with your Puddle. It has its own key and device id, and can be removed without
          touching your identity.
        see: [Phone client, Pairing]
        spec: 04-devices
      - term: Pairing
        definition: Linking a phone client to your Puddle by keys, from a link your Puddle gives you.
        see: [Device]
        spec: 04-devices
      - term: Owner token
        definition: What your own apps use to reach your Puddle's owner API.

  - title: Talking to each other
    terms:
      - term: Stream
        definition: >-
          A trusted, signed connection between two friends' Puddles. Nothing passes between two Puddles without one,
          apart from asking for one. Messages, files and calls travel over it.
        see: [Puddle, Receipt]
        spec: 03-streams
      - term: Address
        definition: >-
          Where a Puddle can be reached right now. Puddles tell their friends when it changes, in a signed address
          record. A `puddle://` link carries one.
        spec: 03-streams
      - term: Event
        definition: >-
          A message, edit, deletion or group change. Each one is signed by whoever wrote it, so it can be checked
          wherever it was copied from.
        spec: 03-streams
      - term: Receipt
        definition: >-
          A signature on an answer, from whoever answered. It's how the sender knows its request reached the right
          Puddle, whatever sits in between.
        see: [Signature]
        spec: 02-signatures
      - term: Custody receipt
        definition: >-
          A receipt a Levee signs when it takes a message for a Puddle that's offline, so the sender sees "waiting at
          their Levee" rather than "delivered".
        see: [Levee, Receipt]
        spec: 06-levee
      - term: Signature
        definition: Every request carries the sender's signature, and every answer to a known sender carries a receipt.
        see: [Receipt]
        spec: 02-signatures
      - term: Sealing
        definition: >-
          Encrypting a request or answer to the other end's key, so it stays private without relying on TLS or any
          certificate.
        spec: 09-sealing

  - title: Ponds
    terms:
      - term: Channel
        definition: A text room in a Pond. The Pond keeps its history; your Puddle keeps the newest 200 messages.
        see: [Pond]
      - term: Invite link
        aka: [pond:// link]
        definition: >-
          A `pond://…` link made with `pondctl invite create`. Paste it into Puddle to join. It can be limited by
          number of uses and by expiry.
        see: [pondctl]
        spec: 05-ponds
      - term: Member
        definition: A Puddle that has joined a Pond or a Pool. Every request it makes is signed with its key.
        see: [Pond, Pool]

  - title: Pools
    terms:
      - term: Auth Puddle
        definition: >-
          One of the Puddles in charge of a Pool. The Puddles that create a Pool are its first Auth Puddles; they can
          make other members Auth Puddles or give them roles. The last one can't step down.
        see: [Pool, Role]
      - term: Role
        definition: A named set of permissions an Auth Puddle can give a member.
        see: [Auth Puddle]
      - term: Seeder
        definition: >-
          A member's Puddle that opts in to serve a Pool's content to others, as in BitTorrent. Only seeders show
          their address to the Pool; other members connect out to a few seeders, so their own address stays hidden.
          Auth Puddles seed by default.
        see: [Pool, Gossip]
      - term: Gossip
        definition: >-
          How seeders spread a Pool's events: each passes them on to a few others, so nobody sends to everyone and a
          Pool can grow to thousands of members. Events are signed by their authors, so a seeder can't change one.
        see: [Seeder, Event]

  - title: The protocol
    terms:
      - term: Puddle Protocol
        definition: >-
          The written rules every ezp2p program follows when talking to another, so each can be built and upgraded
          on its own. [Read it on GitHub](https://github.com/ezp2p/protocol).
        spec: 00-overview
      - term: The 404 rule
        aka: [Strangers learn nothing]
        definition: >-
          A request that fails any check gets the same `404` as a path that doesn't exist, so a stranger can't even
          tell anything is there.
        spec: 00-overview
---

Something missing or unclear? Ask on [GitHub](https://github.com/ezp2p).
