---
title: Levee
nav_order: 70
---

A Levee is the public side of one Puddle. The design is in [Puddle: Levee](/wiki/puddle/design/levee/) and
[Protocol: Levee](/wiki/protocol/levee/). Built 2026-11-21. The first draft's seven open questions were settled with
the owner (ezp2p/levee#5).

| Question | Decision |
|---|---|
| Who runs it | One Levee per Puddle, run by its owner, like an extension of the Puddle in a DMZ. It may know the owner's friends (their public keys), never their messages. |
| Joining | `leveectl join` on the Levee makes a one-time `levee://` link, and the owner pastes it into Settings → Levee. |
| Live, or a mailbox | Both. Requests pass straight through while the Puddle is attached, and the one-way ones are spooled while it isn't, with a custody receipt to the sender. |
| What goes out | Everything, through the Levee, so nobody the Puddle talks to learns its home address. |
| Strangers | The Levee knows the Puddle's friends and phones and refuses anyone else, except first contacts (a stream request, a phone pairing), which are rate-limited. |
| Files | Left at the Levee, sealed under a key only the message carries, until each friend has fetched them, then deleted. Asking again puts it there again. |
| Calls | Through a TURN relay on the Levee. Its UDP ports are published directly, beside the proxy. |
| Pond voice | Through the relay by default, so Ponds don't learn the Puddle's address. The owner may send it straight to the Pond. |
| Storage | Plain files in the Levee's data folder, with no database. |
| Certificate pinning | Gone with sealing: who answers rests on signatures and sealing, and the Levee's TLS is transport only. *(2026-11-25)* |
| How long it holds things | Until the Puddle comes back, up to the operator's limits (1 GiB, 30 days). What it gives up on, it tells both ends. *(2026-11-25)* |
| Several Levees | No. A Puddle has one Levee, and a Levee one Puddle. A spare isn't worth the complexity. *(2026-11-25)* |
| Direct and Levee together | Always the Levee. Friends dial only the newest address record, which names the Levee alone. *(2026-11-25)* |
| Phones | Through the Levee like friends: signed by the device key and sealed to the Puddle, so no owner token travels. |

### When the Levee gives up

**Decided 2026-11-25.** The Levee's side is built (ezp2p/levee#14). The Puddle's and the protocol's are in review (ezp2p/puddle#73, ezp2p/protocol#8). A request the Levee gives
up on had already been receipted to its sender, so the Levee says so. The sender's messages turn **not delivered**,
and once the friend is seen again the chat offers **Resend** or **Delete** on each. The receiving Puddle is told that
something from that friend expired before it came back. It can't say what, because the Levee held only sealed bytes.

### Receipts through a Levee (replaced)

**Decided 2026-11-12, replaced by sealing:** a Puddle answering through its Levee would sign its receipt over the
Levee's certificate, and its address record would name the Levee's key. Once receipts stopped naming certificates,
none of this was needed.

### Open

Holding outgoing messages for an away friend who has no Levee (ezp2p/levee#15), voice over TCP for networks that block
UDP (ezp2p/levee#16), and a phone's call leg through the Levee (ezp2p/puddle#110).
