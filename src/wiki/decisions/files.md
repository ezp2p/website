---
title: Files
nav_order: 40
---

Files, photos and videos in chats. The design is in [Puddle: Files](/wiki/puddle/design/files/).

## First round

| Question | Decision |
|---|---|
| Largest file | The owner's choice: `files.max_size` in `puddle.yaml`, **100 MiB** by default. A Puddle refuses to send or fetch anything larger. |
| Arriving | Fetched automatically up to `files.auto_download` (**100 MiB** by default). Anything larger waits for the owner to ask. |
| Groups | Fetched from the sender. If the sender can't be reached, from any other member who has it. |
| Video | Played once fully downloaded, from the local file. |
| Kept for | As long as a message refers to it. When the last message using a file is deleted, the file goes. |
| A message | Up to **10 files** and an optional caption. Photos show as a grid. |
| Choosing files | A paperclip button (the system's file picker), dropping files on the chat, and pasting. |
| Kinds of file | Anything. Photos and videos open in the app, and anything else is a card the owner opens or saves. |
| Before download | A tiny preview the sending app makes (at most 1 KiB, inside the signed message), plus the name, type and size. |

## Second round: security and bandwidth

Decided after a security review:

| Question | Decision |
|---|---|
| A file the owner sends from this computer | **Cloned** into the data folder (APFS `clonefile`, Btrfs or XFS reflink), which takes no space until one side changes, or **copied** where the file system can't clone. Never a symlink or a reference to the original: the Puddle acts only inside its data folder. |
| How the app hands it over | The app passes the open file. No route takes a path, so nothing on the network can make the Puddle read a file outside its data folder. A phone uploads. |
| Disk and bandwidth | Disk is the owner's to spend, and bandwidth the owner's to control. |
| Asking again | The first time a Puddle delivers a file whole to a peer, for a message, it does so automatically. After that, each new request needs the holder's approval. A download resuming after an interruption isn't a new request (an hour's grace). |
| Groups | A request goes to every member who can be reached, and any who has the file can accept. |
| Too large | A receiver that finds a file over its `files.max_size` doesn't fetch it and tells the sender, and both chats say so: "Bob accepts files up to 50 MB". |
| Showing | The client's call, not the protocol's. The desktop app embeds photos and videos only. Every other file is a card. |

## Profile pictures

**Decided for now:** SVG is excluded. Limits on pictures arriving from others are still open (ezp2p/puddle#81, and
ezp2p/puddle#75 for SVG).
