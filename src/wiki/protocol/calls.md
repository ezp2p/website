---
title: "08. Calls: live voice and video between friends, and in groups"
nav_order: 9
---

*Moved here from `ezp2p/protocol/spec/08-calls.md` on 2026-11-25.*

Puddle's [`docs/calls.md`](/wiki/puddle/design/calls/) is the fuller design. What every implementation must agree on is here.

## Who carries a call

The two **Puddles**. Each passes the call to and from its owner's device (its window, or a phone over a leg of its own);
the devices record and play. The media goes between the Puddles over **WebRTC**: ICE, DTLS-SRTP and RTP, with **Opus**
(payload type 111, 48 kHz) for voice and **H.264** for video (below).

## Media

Every connection carries two tracks, by `mid`: `audio` (Opus, payload type 111) and `video` (H.264 Constrained Baseline,
`profile-level-id=42e01f;packetization-mode=1`, payload type 96, 90 kHz), both `sendrecv`. A side sends on a track only
from the SSRC its description names for it (`a=ssrc`); an answerer names its own in the answer. A Puddle passes whole frames
on (for video, whole access units, reassembled from FU-A and cut again) and decodes nothing; it may restamp RTP timestamps,
but keeps the spacing between a sender's frames. A sender sends a key frame (IDR with SPS and PPS) at least every 2
seconds, since nothing asks for one (no PLI yet). A device with its camera off sends no video; one that has had none from
a sender for 2 seconds shows that sender as having none.

A third track, `screen` (H.264 as `video`, `sendrecv`), carries a shared screen, sent only while its owner shares one.
A Puddle passes it on as it does `video`, and shows it apart from the camera. A phone's leg has no `screen` yet. A track
whose `mid` a side does not know is left alone: nothing is sent on it, and what comes on it is dropped.

## Setting it up: over the stream (part 03)

Three signed requests (part 02) between friends with an active stream, each answered with a receipt. They don't go
through a retrying outbox: a call that can't be set up now is missed.

| route | body | answers |
|---|---|---|
| `POST /stream/v1/call/offer` | `{call, sdp, udp}` | `200 {"state":"ringing"}`, `409 busy`, `409 no_calls`, `403 no_stream` |
| `POST /stream/v1/call/answer` | `{call, sdp, udp}` | `204`, `404 no_call` |
| `POST /stream/v1/call/end` | `{call, reason}` | `204`, `404 no_call` |

- `call`: 26 characters of base32 (16 random bytes), chosen by the caller.
- `sdp`: the full offer or answer, candidates included (nothing trickles). It names the DTLS certificate's fingerprint,
  and it arrives signed by the friend's identity: that binds the media to who they are. An implementation must take
  the fingerprint only from a signed `offer` or `answer`, and DTLS must check it.
- `udp`: the UDP port the sender's calls arrive on.
- `reason`: `hung_up`, `declined`, `cancelled`, `no_answer`, `busy` or `failed`; anything else counts as `hung_up`.

## Finding a path

No STUN or TURN server run by a third party. Each side offers the addresses of its own interfaces, and adds the other's
advertised addresses (its signed address record, part 03) at the `udp` port it gave. One UDP port carries all of a
Puddle's calls (ICE multiplexes them by username fragment).

## A phone's leg (part 04)

A phone's calls are carried by its Puddle like any other; the phone has a WebRTC leg of its own to its Puddle for the
sound. That leg is signalled over the owner API, in requests the phone signs with its device key (part 04), each
answered with the Puddle's receipt:

- The phone that starts (`POST /api/v1/calls/start`) or answers (`POST /api/v1/calls/{call}/accept`) a call has it. Only
  that phone may set up a leg for it, and no other device's sound is sent.
- `POST /api/v1/calls/{call}/media` with `{sdp}`: the phone's offer, with an Opus track `audio` and an H.264 track
  `video` (both `sendrecv`, each with its SSRC), seven `recvonly` H.264 tracks `v1` to `v7` (a group call's members' video,
  below), and a data channel `frames` (unordered, no retransmissions: their sound in a group call, below), candidates
  included. Answered `200 {sdp, udp}`: the Puddle's answer and the UDP port its calls use, the same one friends reach.
  `400 not_a_phone` without a device signature, `404 no_call` from another phone or for a call that is over, `400
  bad_sdp`. Asking again replaces the leg.
- The phone adds, as a candidate at `udp`, the address it reaches its Puddle at. No STUN or TURN here either.
- The fingerprints are taken only from these signed exchanges, as on the stream, which binds the leg to the pairing.
- The Puddle passes Opus frames between the leg and the friend's connection without decoding them, on each connection's
  own RTP clock.

## Group calls (part 03)

A call in a group is a WebRTC connection between each pair of the people in it, over the streams the group already has (a
friendship, or a group-only stream). Every request below is signed by its sender and answered with a receipt, and comes
from a member of `group` to another member (`403 not_member` otherwise). `call` is 26 characters of base32 (16 random
bytes), chosen by whoever started it. At most 8 are in a call.

- `POST /stream/v1/call/group/join` with `{call, group, seq}`: the sender is in that call, and in no other call of the
  group. Sent to every member on joining, and again every 20 seconds while in it; a member not heard from in three of
  those, with no connection up, has gone. Answered `200 {in, call?}`: `in` says whether the recipient is in the same call;
  `call`, if present, is the id of another call the recipient knows of in the group, smaller than this one. A member that
  learns of a call in the group with a smaller id than its own moves to it, so two started at once become one. A recipient
  not in the call, and in no other, may ring its owner.
- `POST /stream/v1/call/group/leave` with `{call, group, seq}`: the sender left. Sent to every member. `204`.
- `seq` is a number that only goes up from each sender (its clock in microseconds, or one more than the last one sent).
  A join or a leave whose `seq` is no greater than the last the recipient had from that sender in that group is ignored:
  they go out to everyone at once and can arrive out of order.
- For each two in the call, the one whose user id is the smaller (as bytes) offers: `POST /stream/v1/call/group/offer`
  with `{call, group, sdp, udp}` as for a friend's offer, answered `204` (`404 no_call` if the recipient isn't in that
  call, `409 ours_to_offer` from the larger id, `409 full`). The recipient answers once it has made its side, with `POST
  /stream/v1/call/group/answer` and `{call, group, sdp, udp}`, answered `204` (`404 no_call` if no such offer waits). An
  offer replaces any connection the two had; a connection lost is offered again on the next join.
- Fingerprints are taken only from these signed requests, as for a friend's call.
- A Puddle in a group call while a friend rings answers the friend `409 busy`, and the other way round: one call at a time.

On a phone (part 04), the leg is the same. The phone's own frames go on its track and its Puddle sends them on every
connection of the call; the others' frames come to the phone over the `frames` data channel, one message per frame:
1 byte, the member's number in the call (its `slot` in the owner API's `members`), 4 bytes, the frame's RTP timestamp in
that member's own count, big-endian; then the Opus frame. A member's video comes on the track `v<slot>`. A Puddle gives
each other member in the call the smallest slot not held by another member in it now, so slots stay within 1 to 7.

## Behind a Levee (part 06)

A Puddle behind a Levee can't be reached by UDP, so its media goes through its Levee's relay (a TURN server, part 06,
"Calls: the relay"). It offers only relayed candidates and sends `udp: 0`, which tells the other side to add no
candidates of its own making (from the address record) and use the SDP's alone. Nothing else in the signalling changes.

## Not yet

Asking for a key frame (RTCP PLI), resending lost packets (NACK), and a bitrate that follows the connection.
