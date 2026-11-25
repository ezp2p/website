---
title: Levee
nav_order: 0
---

A [Levee]({{ '/levee/' | relative_url }}) gives your Puddle a steady public address when it can't open a port of its own.
It runs on a server with a public address; your Puddle connects out to it.

- [Installation]({{ '/wiki/levee/installation/' | relative_url }}): with Docker or building it yourself, its ports,
  and running behind a reverse proxy.
- [Binding a Levee]({{ '/wiki/levee/binding/' | relative_url }}): joining your Levee to your Puddle, what changes, and
  leaving again.

The full reference (every setting in `levee.yaml`, every `leveectl` command, and what is kept in the data folder) is in
the [Levee README](https://github.com/ezp2p/levee/tree/dev#readme). What a Levee says on the wire is
[part 06 of the Puddle Protocol](https://github.com/ezp2p/protocol/blob/master/spec/06-levee.md).
