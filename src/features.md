---
title: Feature roadmap
description: What Puddle, Pond and Levee can do today, what is being built, and what is planned.
permalink: /features/
layout: features
lede: What works today, what's being built, and what's planned.

# The statuses a feature can have, in the order the legend shows them.
# Each feature below uses one of these ids.
statuses:
  - id: done
    label: Done
  - id: in-progress
    label: In progress
  - id: planned
    label: Planned
  - id: idea
    label: Idea

# One group per program. Each feature has a name and a status; notes are optional
# and may use Markdown. Features show in the order they're written here.
groups:
  - title: Puddle
    url: /puddle/
    features:
      - name: Direct chats
        status: done
        notes: Signed messages delivered straight to each person.
      - name: Group chats
        status: done
      - name: Edits and deletions
        status: done
      - name: Files
        status: done
        notes: Fetched in checked chunks from whoever has them.
      - name: Voice and video calls
        status: done
      - name: Profiles
        status: done
        notes: A different name, picture and blurb for each person.
      - name: Recovery phrase and key rolling
        status: done
      - name: "`puddled` (no window) and Docker image"
        status: done
      - name: Joining Ponds
        status: done
      - name: Phone client
        status: planned
        notes: Connects back to your own Puddle; hosts nothing.

  - title: Pond
    url: /pond/
    features:
      - name: Text channels
        status: done
      - name: Invite links
        status: done
        notes: Limited by number of uses and by expiry.
      - name: "`pondctl` admin tool"
        status: done
      - name: Roles
        status: planned
      - name: Files
        status: planned
      - name: Voice
        status: planned

  - title: Pools
    url: /pools/
    features:
      - name: Design
        status: in-progress
        notes: "Tracked in [ezp2p/puddle#52](https://github.com/ezp2p/puddle/issues/52) and the [Pools project](https://github.com/orgs/ezp2p/projects/2)."
      - name: Creating, inviting, joining and leaving
        status: planned
        notes: "[ezp2p/puddle#56](https://github.com/ezp2p/puddle/issues/56). Any online seeder can let an invitee in."
      - name: Auth Puddles and roles
        status: planned
      - name: Channels synced between members
        status: planned
      - name: Seeders and gossip
        status: planned
        notes: Only seeders show their address; everyone else connects out to a few of them.
      - name: Files
        status: planned
      - name: Voice and video
        status: planned
        notes: A mesh, about 8 people per voice channel.
      - name: End-to-end encrypted content
        status: idea

  - title: Levee
    url: /levee/
    features:
      - name: Design
        status: in-progress
        notes: "[Part 06 of the Puddle Protocol](https://github.com/ezp2p/protocol/blob/master/spec/06-levee.md)."
      - name: Fixed address for a Puddle behind a router
        status: planned
      - name: Holding messages while a Puddle is offline
        status: planned
---

## Developers Notes

I wanted to add a note because the above I'm generating with an LLM to align 
with our Github Issues.

I've been doing a lot of documentation and decision making with the help of LLMs
because noone really wanted to help out with 'just another chat app'. All of the 
original discussion points were commited to markdown in git, but I've been 
getting Claude to pump into [https://github.com/orgs/ezp2p/projects/1].

As you can see, there are a lot of micro decisions that need to be made, and 
Claude doesn't always come up with the best ideas.

Right now I am focused on making it usable. That means:

1. You run a Puddle
2. You can connect to that Puddle from your phone, laptop, etc.
3. Your Puddle can connect to other Puddles
4. Your Puddle can connect to Ponds
5. Voice and video calls just work, no optimizations

Those are the primary points of interest right now, and I have a very limited 
amount of AI tokens to pump into this.

If you want to contribute, please pick an issue and submit a PR for it.

You are absolutely welcome to vibe code anything you want and submit it.

## Usability Notes

While not all features are implemented, there are some fun ones that might give
you an idea of direction while you use Puddle.

As it stands, you can absolutely install Puddle, forward some ports and start 
chatting to friends peer-to-peer. 

You can also host and join Ponds.
