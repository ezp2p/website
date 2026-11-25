---
title: Builds and releases
nav_order: 100
---

How Puddle is built and published. The details are in [Puddle: Builds and releases](/wiki/puddle/releases/).

### What is published, and when?

**Decided:**

- A pull request is built and tested only.
- A push to `dev` (a merged PR) replaces the **dev build**: the prerelease tagged `dev-build`, always at the same link,
  for friends trying the newest. Its tag isn't `dev`, so it never shares a name with the branch.
- A tag like `0.3.0` makes a release. A tag with a `-` (`0.3.0-rc.1`) makes a prerelease. Releases are tagged by hand.
- A push to `main` is built and tested only.

### Which platforms, built how?

**Decided:** Windows x64 (MSYS2 UCRT64), macOS arm64 and Intel (Homebrew, signed ad hoc), Linux desktop as an AppImage
(Ubuntu 22.04, so it runs on glibc 2.35 or later), and `puddled` alone for Linux servers (amd64 and arm64), plus a
container image. Every desktop build **stops if libdatachannel isn't found**, rather than publishing an app without
calls.

### Branches and pull requests

**Decided:** work branches from `dev`, with a pull request into `dev` that says `Closes #N`. `master` takes pull
requests only from `dev` or `hotpatch/*`, and every pull request needs a review from the ezp2p team.

### Not yet

Android (ezp2p/puddle#36), iOS (ezp2p/puddle#96), signing and notarizing (ezp2p/puddle#97), updating itself
(ezp2p/puddle#98), and running the tests on Windows (ezp2p/puddle#99).
