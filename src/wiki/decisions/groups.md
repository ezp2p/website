---
title: Group chats
nav_order: 30
---

The design is in [Puddle: Group chats](/wiki/puddle/design/groups/). Decided with the owner for roadmap phase 5.

### Is there a server, or someone in charge?

**Decided:** neither. A group's members are worked out from signed events (`chat.create`, `chat.rename`,
`member.invite`, `member.join`, `member.leave`), and every Puddle applies the same rules, so the same events give the
same members in any order of arrival.

### Where do groups show?

**Decided:** in the same list as direct messages, and also on their own **Groups** page under Friends.

### How do members who aren't friends reach each other?

**Decided:** directly, by a **group-only connection** (a scoped stream), not relayed through the creator. The cost is
that every member learns every other member's address. That cost is accepted, and it is shown before joining, like
phone numbers in a group text: nothing hides it.

**Considered:** relaying through the creator, which hides addresses but makes one member everyone's carrier, and
breaks the group when they are away.

### Who can do what?

**Decided:** any member can invite a friend, rename the group or leave. At most 50 members, counting people who have
been invited. A new member sees nothing from before they joined.

### Can anyone remove a member?

**Decided at first:** nobody can remove another member, not even the creator. Leaving was each member's own choice.

**Proposed in ezp2p/puddle#69 (in review):** the creator, or whoever invited someone, can take them out at once, and
anyone can vote someone out, who is removed once more than half of the other members have voted.

### What does blocking do in a group?

**Decided:** neither of you gets the other's messages in a group you share, and you can both still be in it. A block
never makes you leave.

### What does an invitation show?

**Decided:** who invited you, and nothing about how many are in the group, which would have to be asked again every
time it was looked at. Accepting shows a plain statement that your address will be visible to the other members.
