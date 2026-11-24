---
title: Installation
nav_order: 10
---

## Puddle at home

The easiest way to run Puddle is on a computer in your home, ideally one that's always on. Your other devices, such as
your phone or another computer, connect back to it.

Running Puddle is as easy as running the desktop app. For friends to reach you, forward one port (TCP and UDP, `8443` by
default) on your router to that computer.

## Puddle on a server, with Docker

`puddled` is Puddle with no window. It's published as a container image for amd64 and arm64:
`ghcr.io/ezp2p/puddle:latest`. You need a machine that's always on with Docker, and an address other people's Puddles
can reach it at: a domain name or a fixed public IP, with the port forwarded if it's behind a router.

### 1. Start it

The repository's `compose.yaml` and `.env.example` are all you need:

```sh
mkdir puddle && cd puddle
curl -fsSLO https://raw.githubusercontent.com/ezp2p/puddle/master/compose.yaml
curl -fsSL https://raw.githubusercontent.com/ezp2p/puddle/master/.env.example -o .env
$EDITOR .env          # set PUDDLE_ADVERTISE at least
docker compose up -d
```

`PUDDLE_ADVERTISE` is the address other Puddles reach you at, such as `home.example.org:8443`: the address and port on
the outside of your router, not the container's. Until it's set up, the Puddle waits and serves nothing.

### 2. Set it up

Once, from a terminal:

```sh
docker compose exec puddle puddled --init
```

This makes your identity and shows your **recovery phrase**, in that terminal only, never in the logs. Write it down:
it's the only way to get your identity back if the volume is lost. Press Enter and the Puddle starts.

To have a first profile made for you, set `PUDDLE_NAME="Your name"` in `.env` before the first start.

### 3. Connect your phone or desktop app

A Puddle in Docker has no window, so you use it from the phone app, or the desktop app connecting to a remote Puddle.
Ask the Puddle for a pairing link with its owner token. The link works once, for ten minutes:

```sh
TOKEN=$(docker exec puddle cat /data/data/state/owner-token)
curl -sk -X POST -H "Authorization: Bearer $TOKEN" -d '{}' https://127.0.0.1:8443/api/v1/devices/pair
```

Paste the `link` from the answer into the app, name the device, and note the six digits it shows. Then let it in,
checking the same six digits are in the list:

```sh
curl -sk -H "Authorization: Bearer $TOKEN" https://127.0.0.1:8443/api/v1/devices
curl -sk -X POST -H "Authorization: Bearer $TOKEN" -d '{}' https://127.0.0.1:8443/api/v1/devices/<id>/accept
```

### 4. Make friends

Give people your address (`home.example.org:8443`) and send them requests from the app.

### Everyday

- **Logs:** `docker compose logs -f puddle`
- **Update:** `docker compose pull && docker compose up -d`. Everything is kept in the `puddle` volume.
- **Back up** the volume: it holds your keys and chats. The recovery phrase gets your identity back without it, but not
  your chats.

The full guide, with `docker run` and what's in the volume, is
[docs/docker.md](https://github.com/ezp2p/puddle/blob/master/docs/docker.md).
