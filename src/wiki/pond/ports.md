---
title: Ports
nav_order: 20
---

A Pond uses two ports. Both are **443** unless you change them: one for TCP, one for UDP.

| Port | Protocol | Carries | Without it |
|---|---|---|---|
| **Chat port** (443) | TCP | Everything but voice: joining, channels, messages, files, invites, and the events a member's Puddle waits for | Nothing works |
| **Voice port** (443) | UDP | Voice and video in voice channels | Everything works except voice channels |

Open both on the machine's firewall, and if it's behind a router, forward both to it: same number, one rule for TCP and
one for UDP.

## Who connects to whom

Members' Puddles always connect **to** the Pond; the Pond never connects to them. So only the Pond needs open ports.
Members need none, which means people can join from behind a home router, a phone network, or a [Levee]({{ '/levee/' | relative_url }}).

A member's Puddle keeps one request open on the chat port for up to 25 seconds at a time, waiting for new messages, then
asks again. That's how messages arrive the moment they're sent.

## Why 443

443 is the usual HTTPS port, so it's open on almost every network people join from, including strict office and campus
ones that block anything unusual. UDP 443 is what HTTP/3 uses, so it's usually allowed too. Keep both on 443 unless
something else on the machine already has one.

## Changing them

| Where | Chat port | Voice port |
|---|---|---|
| Docker (`compose.yaml` or `.env`) | `POND_CHAT_PORT` | `POND_VOICE_PORT` (the chat port's number unless set) |
| `pond.yaml` | `ports.chat` | `ports.voice` |

If the chat port isn't 443, add it to the Pond's address so invite links carry it: `POND_ADDRESS=pond.example.org:8444`
(or `address:` in `pond.yaml`).

In Docker, change the published ports in `compose.yaml` to match.

## Behind a reverse proxy

If a reverse proxy (nginx, Apache, Caddy, Traefik) already has TCP 443, it can pass the chat port through to the Pond.
Point it at `https://<pond>:<chat port>`. The Pond always speaks TLS, and the proxy doesn't need to check its self-signed
certificate. The proxy must:

- pass the request path and query **exactly as sent** (Apache: `ProxyPass … nocanon`), since members sign them;
- pass the `X-Puddle-Signature`, `X-Puddle-Seal` and `X-Puddle-Receipt` headers and the bodies untouched;
- let answers wait up to 30 seconds.

**Voice doesn't go through the proxy.** A reverse proxy only carries TCP, so forward the voice port (UDP) straight to
the Pond. UDP 443 is usually free beside a proxy on TCP 443. Pick another voice port only if the proxy uses UDP 443
itself (Caddy does, and so does nginx with HTTP/3 turned on).

The certificate the proxy uses doesn't matter: members seal what they send to the Pond's own key and check its signed
answers, so the certificate only carries the bytes.

## Members behind a Levee

A member whose Puddle sits behind a Levee reaches the Pond's voice port through the Levee's relay, so the Pond sees the
Levee's address rather than theirs. Nothing changes on the Pond's side.
