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
