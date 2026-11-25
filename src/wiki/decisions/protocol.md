---
title: The protocol
nav_order: 80
---

*From `ezp2p/protocol/decisions.md`.* The protocol itself is in [Protocol](/wiki/protocol/).

### Do we need a separately defined protocol?

**Decided:** yes: a specification and test vectors. *(2026-11-12)*

**Why:**

- **There were already two implementations.** Pond shared no code with Puddle: it checked key chains and request
  signatures in its own code, written from Puddle's documentation. Levee would be a third, and Drip a fourth. Programs
  that must agree byte for byte need one text that says what the bytes are, owned by none of them.
- **Puddle's documents weren't that text.** They mixed the wire with how Puddle happens to be built (its folders, its
  outbox schedule, its app). A Pond or Levee author had to dig the rules out, and a Puddle change could move a rule
  without anyone noticing that the Pond now disagreed.
- **The parts depend on each other.** Proving who answers changed what every responder must send, Ponds included, and
  broke a Puddle behind a Levee unless the Levee was designed for it: a decision across projects, which needed a place
  that spans projects.
- **Versioning needs one owner.** Pond versions by path (`/pond/v1`) and advertises `protocol` and `features`, and
  Puddle versions by path (`/stream/v1`). Both need the same rules for what may change within a version, stated once
  ([Overview](/wiki/protocol/overview/)).

### Why test vectors?

**Decided:** fixed inputs, the exact expected outputs, and the answer a checker must give. Each implementation's tests
load `vectors/*.json` from a checkout beside it, so any disagreement fails a build instead of a conversation. The
vectors were made by Puddle's code, which is the reference until something says otherwise.

### A shared library?

**Decided at first: no** *(2026-11-12)*. The programs were built very differently on purpose (Puddle on plain CMake
and OpenSSL, Pond on Drogon, MariaDB and Redis). The shared part was small and stable, and two implementations
agreeing proved the text complete. The plan was to revisit when Levee was built.

**Then: yes, libpuddle-proto** *(2026-11-21)*. Levee made three implementations, and the owner chose the library first.
`lib/` in `ezp2p/protocol` is C-callable, needs only OpenSSL 3, builds with CMake, and is pulled in with
`add_subdirectory` (each program carries the protocol as a git submodule). It holds ids, key chains, request
signatures, receipts, custody receipts, sealing and pieces, and nothing that is one program's own. Puddle, Pond and
Levee all use it. The vectors stay, and the library is checked against them on every build.

### Where does it live?

**Decided:** `ezp2p/protocol`, a repository of its own, so it is versioned and reviewed apart from any one program.

### Ponds sign receipts

**Decided and built:** Ponds answered members with the same receipt Puddles use, signed by the Pond's key, so a Pond
could renew its certificate without cutting everyone off (feature `receipts`, protocol 3 of `/pond/v1`). This was
later replaced by sealing.

### TLS is transport only

**Decided 2026-11-18:** nothing in the protocol may depend on a TLS certificate. See
[Streams and the wire](/wiki/decisions/streams/#how-is-the-other-end-proven-three-steps).
