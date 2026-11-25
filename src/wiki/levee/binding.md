---
title: Binding a Levee
nav_order: 20
---

**Binding** a Levee joins it to one Puddle. From then on the Levee is that Puddle's public front: friends, phones and
Ponds reach the Puddle at the Levee's address, and the Puddle needs no open ports.

You need a running Levee (see [Installation]({{ '/wiki/levee/installation/' | relative_url }})) and a Puddle that's
already set up, with its recovery phrase written down.

## 1. Make a binding link, on the Levee

```sh
docker compose exec levee leveectl join          # with Docker
build/leveectl -c levee.yaml join                # without
```

It prints a link like this:

```
levee://levee.example.org?id=…&k=…&token=…
```

The link carries the Levee's id and key, so your Puddle knows exactly which Levee it's talking to, and a token that
**works once**. Treat it like a password until it's used: whoever uses it first binds their Puddle to your Levee.

## 2. Use it, on your Puddle

**In the app:** open **Settings → Levee**, paste the link, and choose **Join**.

**In Docker or another Puddle with no window:** pass the link to `puddled`, in single quotes because it contains `&`:

```sh
docker exec puddle puddled --join-levee 'levee://levee.example.org?id=…&k=…&token=…'
```

## 3. Check it

**In the app**, Settings → Levee shows the address friends reach you at now, and whether the Puddle is connected to the
Levee.

**With `puddled`:**

```sh
docker exec puddle puddled --levee
```

**On the Levee:**

```sh
docker compose exec levee leveectl status
```

This shows which Puddle is bound, and how much is waiting for it.

## What changes when you bind

- **Your address becomes the Levee's.** Your link, your phone pairing links, and the address your friends have for you
  all switch to the Levee's address. Friends are told at once; nobody has to add you again.
- **Your Puddle connects out.** It keeps a connection open to the Levee, so you can close the port forward on your
  router if you had one.
- **While your Puddle is off**, messages, profile changes and friend requests wait at the Levee. Senders get a signed
  receipt and see "waiting at your Levee" rather than "delivered". If the Levee ever has to give up on one (it was full,
  or it waited too long), both you and the sender are told, and the sender can send it again.
- **What you send** goes out through the Levee too, so nobody you talk to learns your home address.
- **Files you send** wait at the Levee, encrypted under keys it never sees, until each friend has fetched them.
- **Calls** go through the Levee's relay.
- **Pond voice** goes through the relay as well. Settings → Levee has a switch, **Pond voice straight to the Pond**, for
  a shorter path that doesn't load the Levee; the Pond then sees your own address. It's off unless you turn it on.

## Unbinding

**In the app:** Settings → Levee → **Leave**.
**With `puddled`:**

```sh
docker exec -it puddle puddled --leave-levee
```

The Levee forgets your Puddle and everything it was holding for it, and friends are told your Puddle's own address again.
If your Puddle has no public address of its own (no `advertise:`, no port forward), friends can't reach it until you set
one up or bind another Levee.

## Moving to a new Puddle

A Levee serves one Puddle at a time. To bind a different one, make a link with `--replace`:

```sh
docker compose exec levee leveectl join --replace
```

The Puddle that uses it replaces the old one, and everything the Levee was keeping for the old one is deleted.

## Troubleshooting

- **The link was refused.** Each link works once. Make a new one with `leveectl join`.
- **Connected, but friends can't reach you.** Check that the Levee's name points at the server, and that its HTTPS port
  (or your reverse proxy) is reachable from outside.
- **Messages work but calls don't.** Open UDP `3478` and `49160-49199` in the Levee server's firewall.
