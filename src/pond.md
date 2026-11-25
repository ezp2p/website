---
title: Pond
description: A Pond is a community server for Puddle, with channels and many members, joined by invite link.
permalink: /pond/
image: /assets/img/feature-pond.svg
og_image: /assets/img/og-pond.png
image_alt: Many Puddles joined to one Pond, with light passing through the hub.
---

# Pond

<p class="lede">
    A place for a community to gather, joined from your Puddle.
</p>

Ponds are community servers which provide everything a server admin needs:

- Text Channels
- Voice Channels
- Video Calls
- Pages for information (instead of locked chat channels)
- Events Calendar
- Application Form (for esports teams and guilds)
- Integrated Shop (with Stripe for selling stuff to fund your Pond)

A **Pond** is the public side: a community server, like a Discord server, with 
text channels and many members. Someone runs a Pond, creates channels and gives
out invite links. People join by pasting a link into their Puddle.

## How it works

A Pond is a separate program from Puddle, with its own code. It's built to be run by someone looking after a community,
on a server of their own.

- **`pondd`** is the service. It has no window, and serves HTTPS on one port.
- **`pondctl`** is the admin's tool. It runs on the same machine, with the same config, and creates the Pond, its
  channels and its invites.

Messages are stored in MariaDB on the Pond.

## Joining a Pond

1. The admin runs `pondctl invite create`, which prints a `pond://…` link. Invites can be limited by number of uses and
   by expiry.
2. You paste the link into Puddle (the **+** at the bottom of the server rail).
3. Your Puddle joins and the Pond's channels appear beside your chats.

Your Puddle always makes the connection to the Pond, never the other way round, so joining works from behind a home
router with no ports open. It holds one request open for the Pond's events, so new messages, channels and members arrive
as they happen. It keeps the newest 200 messages of each channel and asks the Pond for anything older.

Every request your Puddle makes to a Pond is signed with your key, the same way it signs requests to friends.

## Pond Channels

Pond currently supports two types of channels; voice and text.

A voice channel operates much like a Discord voice channel. It has an integrated 
text channel and supports desktop sharing and video calls.

## Pond Pages

Pond supports markdown formatted pages that are displayed separately from 
channels.

Unlike other applications, these pages are not locked chat channels. These are 
markdown pages where you can put server rules, server information or whatever 
you feel you need a page for.

Pages can also be used for role selection, so users can select their own roles.

## Pond Events

You can configure a community calendar on your Pond for scheduling events, such 
as scrims or meetups.

Calendars are not fully hashed out yet, but we'll eventually support in-Puddle 
reminders for upcoming events, as well as an exportable webcal so that you can 
add the calendar to your phone.

## Pond Application Forms

If you're running an esports team or WoW guild, you'll probably want to have a 
form that users have to fill out before being granted access to the Pond.

Users with the correct permissions can create an application form.

Users trying to join your team can fill out the application form, and whoever 
has the correct permissions can review and accept them in.

Application forms are still highly WIP but they work to give entry to the Pond, 
as well as to provide automated access to a role to give further permissions.

## Pond Shop

I know you scrolled past everything above for this.

Pond has a built in shop front where you can configure products to sell. Right 
now it's extremely basic; configure your Stripe code, then create some basic 
products.

Over time we'll introduce integrations so that you can sell physical and digital
goods more efficiently.

Because it's all self hosted, we can't actually take a slice of anything. So 
it's all for you.

## Status

Pond works and is ready to test: text and voice channels, roles and permissions, direct messages between members, and invites and moderation from the app. Shared files are planned. See the [roadmap]({{ '/features/' | relative_url }}#pond) for the details.

## Next

- [Install a Pond]({{ '/wiki/pond/installation/' | relative_url }})
- [Pond ports]({{ '/wiki/pond/ports/' | relative_url }})
- [Pond wiki]({{ '/wiki/pond/' | relative_url }})
- [Source on GitHub](https://github.com/ezp2p/pond)
