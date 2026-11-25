---
title: Calls and voice channels
nav_order: 50
---

The design is in [Puddle: Calls](/wiki/puddle/design/calls/), [Pond: Voice channels](/wiki/pond/design/voice/) and
[Protocol: Calls](/wiki/protocol/calls/).

## Calls between Puddles

Decided with the owner for roadmap phase 8.

### Who carries a call?

**Decided:** **the two Puddles**, since they are what other Puddles can already reach. Each passes the call to and
from its owner's window (in the same process) or phone (over a leg of its own).

**Why:** a phone stays a thin client that only ever connects to its own Puddle, so it needs no NAT traversal. The cost
is one more hop for a phone, and the Puddle's upload carrying the call.

### What technology?

**Decided:** **WebRTC through libdatachannel** (standard ICE, DTLS-SRTP and RTP), Opus for voice, and H.264
(Constrained Baseline, OpenH264) for video at 640×480 and 15 frames a second. libdatachannel is small, MPL-2.0, and
builds on Linux, macOS, Windows and Android.

### STUN and TURN?

**Decided:** **only the Puddles' own addresses.** No STUN or TURN server run by anyone else, so nobody outside learns
who calls whom. A Puddle behind a Levee goes through its Levee's relay, which belongs to its owner.

### In what order?

**Decided:** one-to-one in the window first, then phones, then group calls, then video. All four are built.

### How do group calls work?

**Decided:** **a mesh**: a connection between each pair of people in the call, over the connections the group already
has. No Puddle carries anyone else's call. Up to 8 in a call.

## Voice channels in Ponds

Decided with the owner for roadmap phase 9.

### A call, or a place?

**Decided:** a voice channel is Discord's: you join it and sit there, and nothing rings. Administrators make them.
Voice activation or push to talk. No cap on people or voices, and cameras and shared screens too.

### Why not the group-call mesh?

**Decided:** in a Pond, **the Pond forwards** (an SFU). Each Puddle sends its owner's voice once, to the Pond, which
sends each Puddle what the others say, decoding and mixing nothing.

**Why:** a channel may hold 50 people, and a Puddle on a home connection can't send 49 copies of anything. It also fits
how Ponds work: the Puddle always connects to the Pond, which has the public address, so a Puddle behind NAT can join.

### Can the Pond hear?

**Decided:** yes, for now. Encryption that only members can undo (SFrame) comes later (ezp2p/pond#48).

### Who moderates?

**Decided:** whoever has the permission, for the whole Pond or one channel (`voice_mute`, `move_members`). A channel's
permissions decide who may connect, speak and show video. *(Protocol 13)*

### Pond voice behind a Levee

**Decided:** through the Levee's relay by default, so Ponds don't learn the Puddle's address. The owner may send it
straight to the Pond instead: shorter, but the Pond sees the address.

## Pools

**Planned:** a Pool's voice channel is a mesh of up to 8, like a group call (ezp2p/puddle#65). How to go beyond 8 is
open (ezp2p/puddle#66).
