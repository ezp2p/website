---
title: Installation
nav_order: 10
---

Puddle is in early testing, so there's no stable release yet. Everything here uses the **dev build**: the newest build of
Puddle's `dev` branch, replaced every time a change is merged. Expect rough edges, and download it again now and then for
fixes (it doesn't update itself yet).

## Get the dev build

Download it from **[github.com/ezp2p/puddle/releases/tag/dev-build](https://github.com/ezp2p/puddle/releases/tag/dev-build)**.
The file names carry the commit they were built from, such as `Puddle-dev-e8d3708-windows-x64.zip`.

| You have | Download | Then |
|---|---|---|
| Windows | `Puddle-dev-…-windows-x64.zip` | Unzip it and run `Puddle.exe`. Windows may warn that the app isn't signed: choose **More info → Run anyway**. |
| A Mac with Apple silicon | `Puddle-dev-…-macos-arm64.zip` | Unzip it and move `Puddle.app` to Applications. The first time, right-click it and choose **Open**, since it isn't notarized. |
| An Intel Mac | `Puddle-dev-…-macos-intel.zip` | As above. |
| Linux | `Puddle-dev-…-linux-x86_64.AppImage` | `chmod +x` it and run it. |
| A Linux server, no screen | `puddled-dev-…-linux-amd64.tar.gz` (or `arm64`) | See [On a server](#on-a-server-with-docker) below; Docker is the easier way. |

`SHA256SUMS` lists the checksum of every file, if you want to check your download.

## On your computer at home

This is the simplest way to start: Puddle runs as an app on your own laptop or desktop, and your chats live there.

### 1. Start Puddle

Run the app. On its first run it makes your identity and shows your **recovery phrase**, once. Write it down and keep it
somewhere safe: it's the only way to get your identity back on a new machine.

Puddle works best on a computer that stays on. While it's asleep or off, friends can't reach you; what they send waits on
their side and arrives when you're back.

### 2. Open a port so friends can reach you

Friends' Puddles connect straight to yours, so your router has to let them in. That's done with a **port forward**: a
rule on your router that sends one port from the internet to your computer. Every router has this, usually under a name
like *Port forwarding*, *Virtual server* or *NAT*, in its admin page (often at `192.168.0.1` or `192.168.1.1`).

Forward this to your computer:

| Port | Protocol | Carries |
|---|---|---|
| `8443` | **TCP** | Everything: messages, files, friend requests, your phone connecting home |
| `8443` | **UDP** | Voice and video calls |

Make both rules: same port number, one for TCP and one for UDP (some routers have a *Both* or *TCP/UDP* option). Without
the UDP rule, everything works except calls.

To set it up:

1. **Find your computer's local address**, something like `192.168.1.23`. It's in your network settings
   (Windows: `ipconfig`; macOS: *System Settings → Network*; Linux: `ip addr`).
2. **Keep that address fixed.** In the router, reserve it for your computer (often called *DHCP reservation* or
   *static lease*), so the forward still points at the right machine after a restart.
3. **Add the forward**: external port `8443`, internal port `8443`, TCP and UDP, to that local address.
4. **Allow it through your computer's firewall**, if it asks. Windows will usually ask the first time Puddle runs:
   allow it on private networks.

### 3. Tell Puddle its public address

Your friends need the address on the *outside* of your router. Find your public IP (search "what is my IP"), then add it
to Puddle's settings file, `puddle.yaml`:

| System | `puddle.yaml` is at |
|---|---|
| Windows | `%APPDATA%\puddle\puddle.yaml` |
| macOS and Linux | `~/.config/puddle/puddle.yaml` |

Add a line (or uncomment the one that's there):

```yaml
advertise: 203.0.113.7:8443
```

Then restart Puddle. Friends are told whenever this changes.

> **Home addresses change.** Most home internet connections get a new public IP now and then. A free dynamic DNS name
> (such as `yourname.duckdns.org`), kept up to date by your router or a small program, stays the same: use it instead,
> as `advertise: yourname.duckdns.org:8443`.

### 4. Add friends

Share your link from the app with a friend, or paste theirs. Once you've accepted each other, your Puddles hold a
[stream]({{ '/terminology/' | relative_url }}#stream) and you can chat.

**Can't forward a port?** Some connections don't allow it at all: mobile broadband, many apartment and student networks,
and providers using carrier-grade NAT. See [Levee](#cant-open-a-port-use-a-levee) at the end of this page.

## On a server, with Docker

`puddled` is Puddle with no window, for a home server or a VPS that's always on. Its image is
`ghcr.io/ezp2p/puddle:dev`, for amd64 and arm64.

The same ports apply: forward **8443, TCP and UDP**, to the machine running Docker (or open them in your VPS's firewall).

### 1. Write a compose file

Make a folder with this `compose.yaml` in it:

```yaml
services:
  puddle:
    image: ghcr.io/ezp2p/puddle:dev
    container_name: puddle
    restart: unless-stopped
    environment:
      PUDDLE_ADVERTISE: home.example.org:8443   # how other Puddles reach you: your public address and port
      PUDDLE_NAME: "Your name"                  # optional: a first profile, made on the first start
      PUDDLE_PORT: 8443
    ports:
      - "8443:8443/tcp"   # everything
      - "8443:8443/udp"   # calls
    volumes:
      - puddle:/data

volumes:
  puddle:
```

`PUDDLE_ADVERTISE` is the address on the outside of your router or server, not the container's. Until it's set up, the
Puddle waits and serves nothing.

### 2. Start it and make your identity

```sh
docker compose up -d
docker compose exec puddle puddled --init
```

`--init` makes your identity and shows your **recovery phrase**, in that terminal only, never in the logs. Write it down,
press Enter, and the Puddle starts.

### 3. Connect an app to it

A Puddle in Docker has no window, so you use it from the desktop app (on its first run, choose **Connect to my Puddle**)
or the phone app. On the server:

```sh
docker compose exec puddle puddled --pair
```

It shows a pairing link that works once, for ten minutes. Paste it into the app, name the device, and check that the six
digits the app shows match the ones in the terminal before you accept.

### Everyday

- **Logs:** `docker compose logs -f puddle`
- **Update to the newest dev build:** `docker compose pull && docker compose up -d`. Everything is kept in the `puddle`
  volume.
- **Back up the volume:** it holds your keys and chats. The recovery phrase gets your identity back without it, but not
  your chats.

The full Docker guide, with `docker run` and what's in the volume, is
[docs/docker.md](https://github.com/ezp2p/puddle/blob/dev/docs/docker.md).

## Can't open a port? Use a Levee

If you can't forward a port, or would rather not show friends your home address, put a **Levee** in front of your
Puddle. A Levee runs on a small server with a public address; your Puddle connects *out* to it and needs no open ports at
all. Friends reach you at the Levee's address, and it holds messages for you while your Puddle is off, without being able
to read them.

**→ [What a Levee is, and how it works]({{ '/levee/' | relative_url }})**, then
[install one]({{ '/wiki/levee/installation/' | relative_url }}) and
[bind it to your Puddle]({{ '/wiki/levee/binding/' | relative_url }}).
