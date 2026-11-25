---
title: Design
nav_order: 50
---

*Moved here from `ezp2p/puddle/docs/` on 2026-11-25.* These are the design documents the Puddle's code follows. Paths
such as `src/core/identity.cpp`, `api/openapi.yaml` and `tests/e2e_test.c` are in the
[puddle repository](https://github.com/ezp2p/puddle/tree/dev). When a change to Puddle changes its design, update the
matching page here, in a website pull request beside the code's.

**Who you are**
- [Identity and keys](/wiki/puddle/design/identity/): the recovery phrase, the key chain, rolling, devices
- [Profiles](/wiki/puddle/design/profiles/): how the owner appears, and which place sees which profile

**Talking to others**
- [Streams](/wiki/puddle/design/streams/): Puddle to Puddle: requests, answers, proving who answers
- [Group chats](/wiki/puddle/design/groups/), [Files](/wiki/puddle/design/files/), [Calls](/wiki/puddle/design/calls/)
- [Ponds](/wiki/puddle/design/ponds/): being a member of Ponds; [Direct messages through a Pond](/wiki/puddle/design/pond-dms/)
- [Levee](/wiki/puddle/design/levee/): the Puddle's side of a Levee

**Inside a Puddle**
- [Storage](/wiki/puddle/design/storage/), [Objects](/wiki/puddle/design/objects/), [Backups](/wiki/puddle/design/backup/),
  [Theming](/wiki/puddle/design/theming/)
- [Hardening](/wiki/puddle/design/hardening/): what junk and floods cost a Puddle, and the gaps still open
- [Protocol](/wiki/puddle/design/protocol/): which parts of the [Puddle Protocol](/wiki/protocol/) Puddle implements
- [The C++ port](/wiki/puddle/design/cpp-port/): the move to C++ and to layers
- [Build history](/wiki/puddle/design/history/): roadmap phases 1 to 10, step by step, as built

What was decided along the way is in [Decisions](/wiki/decisions/). What is still to do is on the
[project board](https://github.com/orgs/ezp2p/projects/1).
