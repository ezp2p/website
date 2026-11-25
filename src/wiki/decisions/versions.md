---
title: Versions and compatibility
nav_order: 85
---

Puddles, Ponds, Levees and phones are each updated by their own owners, so they will run different versions side by
side. This page records what is decided about that, and what is still open. The rules themselves are in
[Protocol: Overview, Versioning](/wiki/protocol/overview/#versioning).

### How is the protocol versioned?

**Decided:** by path (`/stream/v1`, `/pond/v1`, `/device/v1`, `/levee/v1`). Within a version things are only
**added**, and an implementation ignores what it doesn't know. A change an older implementation would misread gets new
paths, served beside the old ones. *(2026-11-12)*

**Why:** programs built apart and upgraded at their own pace still understand each other, without agreeing on a
release.

### How does a caller know what the other side supports?

**Decided, for Ponds:** a Pond advertises `protocol` (a number that goes up with each addition, 15 today) and
`features` (names) in `/info` and when someone joins. A Puddle checks them before using an addition, rather than
guessing from a `404`, which is also what a refusal looks like.

**Open, for Puddles:** a Puddle advertises nothing, to other Puddles or to Ponds. See below.

### Are signatures tied to a version?

**Decided:** yes. Every signed string carries its own label (`puddle-request-v1`, `puddle-receipt-v2`,
`puddle-seal-v1`, ...), so a signature made for one purpose or version can never be taken for another.

### May v1 still change in place?

**Decided:** yes, until the first release. Sealing changed `/stream/v1` in place because nothing had been released,
and keeping the old unsealed paths would have kept the certificate tie alive *(2026-11-18,
[Streams](/wiki/decisions/streams/))*. After the first release, a change an older peer would misread must get new
paths.

## Open

- **Between Puddles** (ezp2p/protocol#10): new event kinds and fields lost by older Puddles, group state diverging when
  the rules change (removing members is the first case), and hard breaks that look like outages. The recommendation:
  Puddles advertise `protocol` and `features`, senders check before using an addition, events that change shared state
  are marked critical, a group records the protocol its rules need, message-like events carry fallback text, and there
  is a support window after the first release.
- **Between a Puddle and a Pond** (ezp2p/protocol#11): an older Puddle ignores deletions and edits, so moderated
  content stays on its screen. The recommendation: Puddles tell the Pond their protocol, a Pond has a minimum Puddle
  protocol (defaulting to the one that carries moderation), and the Pond sends a fallback deletion to older members.
- **Inside a Pool** (ezp2p/puddle#130, to discuss later): with no server to arbitrate, mixed versions can fork a Pool's
  admin state. The idea to weigh: a Pool protocol raised by a signed upgrade event in the admin log.
