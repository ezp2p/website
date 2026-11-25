---
title: Open questions
nav_order: 110
---

Questions still waiting for a decision. Each one is an issue labelled `needs decision` on the
[project board](https://github.com/orgs/ezp2p/projects/1), where the discussion happens. When one is decided, the
answer moves to its page in this section and the issue is closed.

This list was made on 2026-11-25 from the parked questions in Puddle's `docs/discuss-later.md` and the "Open
questions" and "Not decided" sections of the design documents. The live list is
[the issues labelled `needs decision`](https://github.com/issues?q=org%3Aezp2p+is%3Aissue+is%3Aopen+label%3A%22needs+decision%22).


## Levee

- [Hold what goes out for an away friend who has no Levee](https://github.com/ezp2p/levee/issues/15) (ezp2p/levee#15)

## Protocol

- [Version mismatch between Puddles](https://github.com/ezp2p/protocol/issues/10) (ezp2p/protocol#10)
- [Version mismatch between a Puddle and a Pond](https://github.com/ezp2p/protocol/issues/11) (ezp2p/protocol#11)

## Pond

- [Messages signed by their authors](https://github.com/ezp2p/pond/issues/37) (ezp2p/pond#37)
- [Public Ponds should be accessible directly from their URL](https://github.com/ezp2p/pond/issues/41) (ezp2p/pond#41)
- [What operators may do that administrators may not](https://github.com/ezp2p/pond/issues/46) (ezp2p/pond#46)
- [Voice channels only members can decrypt (SFrame)](https://github.com/ezp2p/pond/issues/48) (ezp2p/pond#48)
- [Roles: "Is Administrator" and "Is Moderator" groupings of permissions](https://github.com/ezp2p/pond/issues/50) (ezp2p/pond#50)

## Puddle

- [Encrypt data at rest](https://github.com/ezp2p/puddle/issues/42) (ezp2p/puddle#42)
- [Pools: voice channels for more than 8](https://github.com/ezp2p/puddle/issues/66) (ezp2p/puddle#66)
- [Allow SVG for display pictures and banners?](https://github.com/ezp2p/puddle/issues/75) (ezp2p/puddle#75)
- [Limits on pictures that arrive from other Puddles](https://github.com/ezp2p/puddle/issues/81) (ezp2p/puddle#81)
- [Detect forked key chains after an old phrase leaks](https://github.com/ezp2p/puddle/issues/83) (ezp2p/puddle#83)
- [A public profile shown before sending a friend request](https://github.com/ezp2p/puddle/issues/84) (ezp2p/puddle#84)
- [Several identities in one Puddle](https://github.com/ezp2p/puddle/issues/91) (ezp2p/puddle#91)
- [A name for the phone client](https://github.com/ezp2p/puddle/issues/92) (ezp2p/puddle#92)
- [Show each Pond the same key, or one derived for it?](https://github.com/ezp2p/puddle/issues/93) (ezp2p/puddle#93)
- [Check history signed by retired keys](https://github.com/ezp2p/puddle/issues/94) (ezp2p/puddle#94)
- [An outside review of the key chain and pre-rotation](https://github.com/ezp2p/puddle/issues/95) (ezp2p/puddle#95)
- [Update itself](https://github.com/ezp2p/puddle/issues/98) (ezp2p/puddle#98)
- [Pools: version mismatch inside a Pool](https://github.com/ezp2p/puddle/issues/130) (ezp2p/puddle#130)
- [Notifications while the app is closed](https://github.com/ezp2p/puddle/issues/111) (ezp2p/puddle#111)
- [Sign Pond messages, and check authors' signatures](https://github.com/ezp2p/puddle/issues/119) (ezp2p/puddle#119)

## Parked on purpose, and since settled

- **What the app says if the owner skips writing down the phrase:** it can't be skipped. A new identity stays
  unconfirmed until the owner ticks "written down" ([Identity](/wiki/decisions/identity/#how-is-the-phrase-shown)).
- **The signature scheme for requests between Puddles:** settled in [Protocol: Signatures](/wiki/protocol/signatures/).
- **Whether a block hides someone's messages in groups, or makes you leave:** hides them, and you stay
  ([Group chats](/wiki/decisions/groups/#what-does-blocking-do-in-a-group)).
- **Who may remove someone from a group:** whoever invited them, or a majority vote
  ([Group chats](/wiki/decisions/groups/#can-anyone-remove-a-member)).
- **Encrypting message bodies end to end:** done on the wire by sealing ([Streams](/wiki/decisions/streams/)).
  Encrypting data at rest is ezp2p/puddle#42, which also covers protecting the key file.
