---
title: Protocol
nav_order: 0
---

*Moved here from `ezp2p/protocol` (`README.md` and `spec/`) on 2026-11-25. This is the protocol as Puddle, Pond and
Levee build against it today: the `ezp2p/protocol` commit their `third_party/protocol` submodules point at.*

The Puddle Protocol is what every ezp2p program says on the wire. It is written down once so that programs built
apart, in their own code and upgraded at their own pace, still understand each other.

| Program | What it is | Speaks |
|---|---|---|
| **Puddle** (`ezp2p/puddle`) | Self-hosted chat with an identity, on the owner's computer | everything below |
| **Phone client** (inside `ezp2p/puddle`) | A thin client of its owner's Puddle | devices |
| **Pond** (`ezp2p/pond`) | A community server, like a Discord server. Its channels live on the Pond; Puddles cache them | identity, signatures, ponds |
| **Levee** (`ezp2p/levee`) | The public side of one Puddle: its address, spools while it is offline, carries what it sends, its files and its calls | identity, signatures, sealing, levee |
| **Drip** (`ezp2p/drip`) | P2P social media (not designed yet) | identity, signatures, events; see [Drip](/wiki/protocol/drip/) |

## The parts

Where a part says MUST, it is a rule an implementation breaks at its peril.

- [Overview](/wiki/protocol/overview/): the principles every part follows, and how the protocol is versioned
- [Identity](/wiki/protocol/identity/): ids, keys, the key chain
- [Signatures](/wiki/protocol/signatures/): request signatures and answer receipts, byte for byte
- [Streams](/wiki/protocol/streams/): Puddle to Puddle
- [Devices](/wiki/protocol/devices/): a phone and its Puddle
- [Ponds](/wiki/protocol/ponds/): a Puddle and a Pond
- [Levee](/wiki/protocol/levee/): a Puddle behind a Levee: joining, passing through, spooling, sending, files and calls
- [Drip](/wiki/protocol/drip/): what Drip can take from all this
- [Calls](/wiki/protocol/calls/): live voice and video between friends, and in groups
- [Sealing](/wiki/protocol/sealing/): bodies sealed to keys, so TLS is transport only
- [Letters](/wiki/protocol/letters/): messages sealed from one Puddle to another and carried by a third, such as a Pond

Why the protocol is its own repository, and why it now has a shared library, is in
[Decisions: Protocol](/wiki/decisions/protocol/).

## The code

The [`ezp2p/protocol`](https://github.com/ezp2p/protocol) repository holds what programs build against:

- `lib/`: **libpuddle-proto**, the protocol's bytes in C for every program (`lib/include/puddle_proto.h`).
- `vectors/`: test vectors, meaning fixed keys, ids, signed requests and receipts, each with the answer an
  implementation must give. Every implementation's tests load them (Puddle's `protocol_vectors` test). A change to the
  wire changes a vector.

## Status

| Part | Puddle | Pond | Levee | Drip |
|---|---|---|---|---|
| identity, chains | built | built | built | - |
| request signatures | built | built | built | - |
| receipts (v2) | built | built (protocol 5) | built (custody receipts) | - |
| sealing | built (phase 10) | built (protocol 5, feature `sealed`) | built | - |
| streams | built | - | passes them on | - |
| devices | built (phase 7) | - | - | - |
| ponds | built (member side) | built | passes them on | - |
| letters | built | built (feature `dms`) | - | - |
| levee | built | - | built | - |
| calls | built (phase 8) | - | relays them (TURN) | - |
