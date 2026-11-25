---
title: Installation
nav_order: 10
---

A Levee is two programs: `leveed`, the service, which has no window, serves HTTPS and relays calls over UDP; and
`leveectl`, the admin's tool, which runs beside it with the same config. One Levee serves one Puddle. There's no
database: just a config file and a data folder.

You need a server with a public address (a small VPS will do), and a name for it, such as `levee.example.org`. Once it's
running, [bind it to your Puddle]({{ '/wiki/levee/binding/' | relative_url }}).

Levee is in early testing, so there's no stable release yet: use the **dev** image, `ghcr.io/ezp2p/levee:dev`, the
newest build of Levee's `dev` branch.

## Ports

| Port | Protocol | Carries |
|---|---|---|
| `8443` (or 443 through a reverse proxy) | TCP | Everything your Puddle and its friends send: messages, files, friend requests, phones |
| `3478` | UDP | The call relay: setting up calls |
| `49160-49199` | UDP | The call relay: the calls themselves |

Open them in the server's firewall. Without the UDP ports everything works except calls.

## With Docker

In a new folder, a `compose.yaml`:

```yaml
services:
  levee:
    image: ghcr.io/ezp2p/levee:dev
    restart: unless-stopped
    environment:
      LEVEE_ADDRESS: levee.example.org   # how others reach your Puddle: this server's name
    ports:
      - "127.0.0.1:8443:8443"            # HTTPS, for a reverse proxy on this server
      - "3478:3478/udp"                  # call relay
      - "49160-49199:49160-49199/udp"    # call relay
    volumes:
      - levee:/data

volumes:
  levee:
```

```sh
docker compose up -d
```

This publishes HTTPS only to `127.0.0.1`, for a [reverse proxy](#behind-a-reverse-proxy) on the same server that holds
the certificate for your name. To go without a proxy, publish it to everyone instead, as `"443:8443"`. If you publish
it on a port other than 443, add that port to the address: `LEVEE_ADDRESS: levee.example.org:8443`. The call relay is
UDP, which a reverse proxy doesn't carry, so it's always published directly.

Then make the link to bind your Puddle with:

```sh
docker compose exec levee leveectl join
```

The rest is on [Binding a Levee]({{ '/wiki/levee/binding/' | relative_url }}).

### Everyday

- **Update to the newest dev build:** `docker compose pull && docker compose up -d`.
- **See who's bound and what's waiting:** `docker compose exec levee leveectl status`.
- **Back up the volume.** It holds `levee.key`: a new key is a new Levee, and your friends won't trust its receipts
  until your Puddle tells them about it.

## Behind a reverse proxy

Any certificate works (Let's Encrypt, or the proxy's own): the protocol never looks at certificates. Forward everything
for the Levee's name to its HTTPS port, and let requests wait: your Puddle holds one open for up to 25 seconds.

nginx:

```nginx
server {
    listen 443 ssl;
    server_name levee.example.org;
    # ssl_certificate and ssl_certificate_key as for any site

    location / {
        proxy_pass https://127.0.0.1:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 75s;
        proxy_request_buffering off;
        client_max_body_size 64m;   # files go up in 1 MB pieces, plus sealing
    }
}
```

The Levee lets a few first contacts through from each address, so it needs to know who's really asking. The Docker image
already trusts Docker's private ranges, where a proxy's requests come from; without Docker, set `trusted_proxies` in
`levee.yaml` to the proxy's address. An Apache example is in the
[README](https://github.com/ezp2p/levee/tree/dev#behind-a-reverse-proxy).

## Manual installation

Build it (needs CMake, a C++20 compiler, OpenSSL 3, jsoncpp and yaml-cpp; Drogon is fetched and built the first time):

```sh
git clone -b dev --recurse-submodules https://github.com/ezp2p/levee && cd levee
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel 4
```

Copy `levee.yaml.example` to `levee.yaml`, and set at least:

```yaml
address: levee.example.org
data_dir: /var/lib/levee
```

Then make the link and start it:

```sh
build/leveectl -c levee.yaml join
build/leveed -c levee.yaml
```

Every setting in `levee.yaml` is listed in the [README](https://github.com/ezp2p/levee/tree/dev#leveeyaml).

## What it can see

Everything a Levee carries is sealed end to end, or encrypted under a key it doesn't have, and it signs nothing in your
name. It does see what any carrier sees: who talks to your Puddle, when, and how much. Run it yourself, or have someone
you trust run it.
