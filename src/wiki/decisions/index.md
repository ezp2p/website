---
title: Decisions
nav_order: 0
---

Every question that came up while building ezp2p, and the direction taken. Each entry gives the question, what was
decided, why, and what else was considered. Where a later decision replaced an earlier one, both are kept, so the
reasoning can be followed.

These were collected on 2026-11-25 from the decision tables, "Decided with the owner" notes and parked questions that
used to live in each repository (Puddle's `docs/roadmap.md` and `docs/discuss-later.md`, the protocol's
`decisions.md`, Pond's `docs/design.md` and `docs/dms.md`, and others).

- [Identity and keys](/wiki/decisions/identity/): the recovery phrase, rolling, adding friends by address, devices
- [Streams and the wire](/wiki/decisions/streams/): trust, from certificates to sealing, retries, what strangers see
- [Group chats](/wiki/decisions/groups/)
- [Files](/wiki/decisions/files/)
- [Calls and voice channels](/wiki/decisions/calls/)
- [Ponds](/wiki/decisions/ponds/): files, roles, direct messages through a Pond
- [Levee](/wiki/decisions/levee/)
- [The protocol](/wiki/decisions/protocol/): why it is separate, the shared library, versioning
- [Versions and compatibility](/wiki/decisions/versions/): what happens when Puddles, Ponds and Pools run different versions
- [The apps](/wiki/decisions/clients/): the desktop window and the phone client
- [Builds and releases](/wiki/decisions/releases/)
- [Open questions](/wiki/decisions/open-questions/): what is still waiting for a decision

## Adding a decision

When a question is settled, add it to the matching page in the same piece of work, as a pull request to
[`ezp2p/website`](https://github.com/ezp2p/website). Use this shape:

```markdown
### The question, asked plainly

**Decided:** the answer. *(2026-11-25, ezp2p/puddle#123)*

**Why:** the reasons.

**Considered:** the alternatives, and why they lost.
```

A question that is open becomes an issue labelled `needs decision` on the
[project board](https://github.com/orgs/ezp2p/projects/1). When it is decided, close the issue and add the entry here.

## Features that span repositories

A feature often needs work in more than one repository. A Pond feature, for example, needs the Pond's side and the
Puddle's window. The convention is:

- **The parent issue lives where the behaviour lives**: the Pond for a Pond feature, the protocol for a change to the
  wire, Puddle for something only Puddles do.
- **Each other repository's part is a sub-issue** of it. GitHub sub-issues work across the repositories of the
  organisation, and the board's *Parent issue* and *Sub-issues progress* fields show them together.
- A feature that touches many places, such as pinned messages in DMs, groups, Ponds and Pools, gets a tracking issue
  in Puddle with a sub-issue per repository.
