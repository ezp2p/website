---
title: Full comparison
description: Puddle and Pond side by side with Discord, Keet, WhatsApp, Telegram, Signal, iMessage, SMS and Guilded, in detail.
nav_order: 10
---

<p class="lede">Puddle and Pond next to texting, and the chat apps people already use, in detail. For the short version, see
<a href="{{ '/compare/' | relative_url }}">Puddle at a glance</a>.</p>

The short version: with ezp2p, **your chats live on a computer you control**, not on a company's servers, and there's
no company in the middle that could read them, sell them, or switch the service off. In exchange you look after that
computer, and ezp2p is still young.

<div class="compare-scroll" markdown="1">

| | **Puddle + Pond** | Discord | Keet | WhatsApp | Telegram | Signal | iMessage | SMS and phone calls | Guilded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Where your chats are kept** | Your own computer (a Pond's history: on the Pond) | Discord's servers | Your devices, and the peers you share with | Your phone | Telegram's servers (secret chats: on your devices) | Your devices | Your Apple devices, and iCloud if you turn it on | Your phone, and your carrier's records | Guilded's servers |
| **Needs one company to keep running** | No | Yes | No, though it finds peers through a shared DHT | Yes | Yes | Yes | Yes | Your carrier, though any carrier reaches any other | Yes |
| **To sign up you need** | Nothing: your identity is your keys | An email or phone number | Nothing: your identity is your keys | A phone number | A phone number | A phone number | An Apple Account, on an Apple device | A phone number and a carrier account, often with ID | A Roblox account |
| **Direct messages end-to-end encrypted** | Yes: sealed to your friend's Puddle's key, so nothing in between can read them, a Levee included | Calls only, not text | Yes | Yes | Only opt-in secret chats | Yes | Yes | No | No |
| **Group chats** | Yes: kept on every member's Puddle, end-to-end encrypted to each, with no server and no one in charge | Group DMs, up to 10 people, not end-to-end encrypted | Rooms, end-to-end encrypted | Groups of up to 1,024, end-to-end encrypted | Groups of up to 200,000, not end-to-end encrypted | Groups of up to 1,000, end-to-end encrypted | Groups of up to 32, end-to-end encrypted | Group texts, not encrypted | Group DMs, not end-to-end encrypted |
| **Communities with channels** | Yes: Ponds (and Pools, without a server, in development) | Yes: servers | Rooms | Communities (groups of groups) | Groups and channels | No | No | No | Yes: servers |
| **Voice channels you drop into** | Yes, in Ponds | Yes | No, calls | No, calls | Voice chats in groups | No, calls | No, calls (FaceTime) | No, calls | Yes |
| **Roles and permissions** | Yes, in Ponds | Yes | Limited | Admins | Admin rights | Admins | No | No | Yes |
| **Run it yourself** | Yes, every part | No | Nothing to run: it's peer-to-peer | No | No | No | No | No | No |
| **Source code** | Public on GitHub (no licence chosen yet) | Closed | Libraries open, the app itself not published | Closed | Apps open, servers closed | Open | Closed | Open standards, run by carriers | Closed |
| **Needs a computer that stays on** | Yes, or a Levee to hold messages | No | No | No | No | No | No | No | No |
| **Status** | Early testing | Established | Established | Established | Established | Established | Established | Established | Shut down in December 2025 |

</div>

## What it comes down to

- **SMS and phone calls** are the closest in how they work. You have an address, people who know it reach you directly,
  and no app company sits in the middle: any carrier reaches any other, the way any Puddle reaches any other. Puddle
  keeps that and adds what texts never had: end-to-end encryption, no phone number or carrier account, nobody able to
  message you until you've accepted them, and communities, files and video on top.
- **Discord and Guilded** are the closest in feel to Puddle with Ponds: servers, channels, roles and voice channels you
  drop into. The difference is that everything lives on one company's servers, so the service depends on that company.
  Unfortunately, we saw this when [Guilded was shut down](https://devforum.roblox.com/t/update-on-guilded-and-communities/3966775)
  at the end of 2025.
- **Telegram** is in the cloud by default; only opt-in one-to-one secret chats are end-to-end encrypted.
- **WhatsApp, Signal and iMessage** encrypt everything end to end, group chats included, and keep messages on your
  devices. But you sign up with a phone number or an Apple Account, and depend on one company's service being up. None
  of them has community servers with channels and voice rooms.
- **Group chats in Puddle** have no server at all: every member's Puddle keeps the whole chat and sends straight to the
  others, and the rules for who's in the group are the same on every Puddle, so no one owns it.
- **Keet** sets out to solve the same problems Puddle does: no sign-up, no company servers holding your messages, and
  everything end-to-end encrypted between the people talking. It solves them in a different way; see below.

### Keet and Puddle: two ways to the same place


While initially developing Puddle, I happened upon advertisements for Keet. 

Keet seems to address the same problems that I was trying to address, however I 
was curious about their "Pear Protocol" and how their system actually worked.

Originally, Session Messenger seemed like a solution and I was all-in on it from 
the start but I got burned by the relay protocol that it used. If Session were 
self hostable in the traditional sense, I don't think I'd have created Puddle.

With the life lesson from Session in mind, I took a skeptical view of Keet early
on (sorry Keet devs).

Keet and Puddle fundamentally address the same concerns about centralizing our 
online existence, however we've both taken different approaches to the same 
problem.

I've had an LLM summarize below:

**Keet finds peers through a shared network.** Keet is built on Holepunch's [Pear](https://docs.pears.com/) stack, which
connects people through [HyperDHT](https://docs.pears.com/building-blocks/hyperdht), a distributed hash table shared by
the apps built on it. A peer **announces** itself in the DHT under a key, others **look it up** by that key, and the DHT
helps the two **punch through** their home routers so they can connect directly. Joining starts from a few
**bootstrap nodes** (public ones at `hyperdht.org` by default, which an app can replace), and when a direct connection
isn't possible, a [blind relay](https://docs.pears.com/p2p/how-to/connect-to-peers/relay-connections-through-a-blind-relay/)
can carry the encrypted traffic without being able to read it. The result is that it just connects, wherever you are,
with nothing to set up.

**Puddle connects to an address.** A Puddle has an ordinary address, a domain name or IP and a port, the way a website
does, and your friends' Puddles connect straight to it over HTTPS. There's no shared network to join and nothing to look
up: your Puddle only ever talks to the people you talk to. When your address changes, your Puddle tells your friends
itself. The cost is that your Puddle has to be reachable, through a port forward, or through a Levee if it can't be.

---

Jumping in, the LLM doesn't really know this but Puddle was originally built for 
IPv6.

In a world of IPv6, all machines on the internet can directly communicate with 
one another like the internet was originally designed for. That's why the peer
to peer nature was chosen.

However we don't live in a perfect world, and we're all still stuck on IPv4.

Because the network libraries are generic, Puddle works just fine on IPv4 however
you still have to deal with NAT traversal (IE port forwarding).

In a perfect world, you'd just configure Puddle to live on port 443 of your home
computer, listen to a public IPv6 address and call it a day.

---

| | Keet | Puddle |
|---|---|---|
| **Finding someone** | Looks up their key in a shared DHT | Connects to the address they gave you |
| **Getting through a home router** | Hole punching, helped by the DHT: nothing to set up | A port forward, or a Levee |
| **Who it contacts to get started** | Bootstrap nodes, then the DHT | Only the people you talk to |
| **When a direct connection can't be made** | A blind relay carries it, encrypted | Your Levee carries it, encrypted |

One other difference: as far as we can find, Keet's own app source isn't published, though the Pear libraries it's
built on are open source.

Put simply, Keet builds a network of peers who self-discover one another, and 
allows new users to discover friends view a "twilight bark" of sorts.

In comparison, Puddle just lets you connect directly with one another; no network
or technology to interlink, just pure packets on the internet.

### Puddle on a private network, with no internet at all

Because a Puddle only ever connects to the addresses it's given, it doesn't need the internet. Give it an address on a
private network, and that's the only place it lives.

Take a family. Each person runs a Puddle, and everyone's devices join one private network: the home Wi-Fi, plus a VPN
such as WireGuard or Tailscale for when they're out. Each Puddle gives its address on that network
(`advertise: 10.8.0.5:8443`, say). They add each other, chat, share photos and call, and phones connect back to their
own Puddle over the same VPN. **Nothing is ever exposed to the internet**: no port forwards, no public address, and
nothing for a stranger to find.

It works because nothing in Puddle has to phone home:

- **No accounts or sign-in servers** to check with. Your identity is your keys.
- **No lookups.** No DHT, no bootstrap nodes, no directory: just the addresses you've exchanged.
- **No certificate authority.** Puddles prove who they are with their keys, so a self-signed certificate on a private
  address is all they need.
- **Calls stay inside too.** Voice and video go between the Puddles' own addresses, with no outside relay server.

The same goes for a Pond: run one on the private network, and a club, a team or an office can have their own community
server that the internet can't see.

## What ezp2p does well

<div class="strengths">
  <div class="strength">
    <h3>No sign-up. Ever.</h3>
    <p>No email, no phone number, no account with anyone. Open Puddle and you already have an identity: keys made on
    your own machine, backed by a recovery phrase only you hold.</p>
  </div>
  <div class="strength">
    <h3>It just works</h3>
    <p>Download it, run it, share your link. Your friend pastes it, you both accept, and you're talking. A Pond is one
    <code>docker compose up</code>, and the people you invite don't make an account either.</p>
  </div>
  <div class="strength">
    <h3>Nobody can switch it off</h3>
    <p>There's no company in the middle that the service depends on. Your Puddle keeps running for as long as you run
    it.</p>
  </div>
  <div class="strength">
    <h3>Nobody can ban you</h3>
    <p>There's no central account to suspend. A Pond's admins run their own Pond, and that's all: your identity, your
    friends and your chats stay yours.</p>
  </div>
  <div class="strength">
    <h3>You decide who reaches you</h3>
    <p>Nobody can message you until you've accepted them. Remove or block anyone, any time: a block takes effect at
    once, and the person blocked can't tell.</p>
  </div>
  <div class="strength">
    <h3>Invisible to strangers</h3>
    <p>Anyone your Puddle doesn't know gets the same answer as an empty address. No spam, no cold messages, and nobody
    can even tell there's a Puddle there.</p>
  </div>
  <div class="strength">
    <h3>Private between Puddles</h3>
    <p>Chats are end-to-end encrypted from your Puddle to your friends', and every message is signed by whoever wrote
    it. A Levee or proxy in between carries them without being able to read them.</p>
  </div>
  <div class="strength">
    <h3>One you, many faces</h3>
    <p>Keep a profile for work, one for friends and one for family, each with its own name and picture, and choose who
    sees which.</p>
  </div>
  <div class="strength">
    <h3>Nothing to sell you</h3>
    <p>No ads, no tracking and no subscription, because there's no company collecting anything. Your chats are files on
    your own disk: back them up, move them, or delete them.</p>
  </div>
</div>

## What ezp2p doesn't do well yet

- **It's early.** Puddle, Pond and Levee are usable enough to test, not polished. Pools are still being designed. See the
  [roadmap]({{ '/features/' | relative_url }}).
- **Someone has to run things.** Your Puddle needs a computer that's usually on and reachable, through a port forward or
  a [Levee]({{ '/levee/' | relative_url }}). A Pond needs someone to host it.
- **Chats aren't encrypted on disk yet.** Between Puddles, chats are end-to-end encrypted on the way. But once a message arrives, your
  Puddle stores it, and your keys, as plain files, so anyone who gets hold of the computer or a backup can read them. Until
  Puddle encrypts its own files, turn on your system's disk encryption (BitLocker, FileVault or LUKS).
- **A Pond can read its channels.** A Pond is a server that keeps its channels' history, so whoever runs it can read
  what's posted there, as with Discord. Direct messages between members through a Pond are end-to-end encrypted.
- **No phone app to install yet**, beyond connecting to your own Puddle; no app-store builds; no automatic updates.

<p class="compare-note">Compared from each service's public information in November 2026. Services change: if something
here is out of date, <a href="https://github.com/ezp2p/website">tell us on GitHub</a>.</p>
