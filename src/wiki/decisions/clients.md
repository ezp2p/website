---
title: The apps
nav_order: 90
---

The desktop window and the phone client.

### What is the window built with?

**Decided:** Qt 6, with Qt Quick (QML). It talks to its own Puddle over the owner API on HTTPS, like a phone, with the
Puddle's own certificate pinned. It is Discord-style: a narrow rail (Friends on top, Ponds below), a list of
conversations, and flat messages without bubbles.

### The phone client

**Decided:** a **thin client** (see [Identity](/wiki/decisions/identity/#is-a-phone-a-full-puddle)), built from the
desktop app's Qt Quick code, **Android first**, with notifications **only while the app is open**, for now.
*(Roadmap phase 7)*

Pairing is a link (and a QR code where libqrencode is found). A phone that pairs shows a check code for the owner to
compare. It has no product name yet (ezp2p/puddle#92). Notifications while the app is closed are ezp2p/puddle#111.

### Notifications

**Decided:** a tray notification never shows the message's text.

### Developer Mode

**Decided:** user ids and codes are hidden from normal use, and **Developer Mode** in Settings shows them, with
"Copy user ID". *(Roadmap 4.6)*

### Menus

**Decided:** the right-click menus offer only what the owner API can already do. They use a styled menu of Puddle's
own, so the app builds on Qt 6.2 to 6.8. Native menus are ezp2p/puddle#90.

### Theming

**Decided:** an optional `theme.yaml` beside `puddle.yaml`, with colours and sizes, restyled live while the app runs.
Fonts, menus, dialogs and the message layout aren't themeable yet.
