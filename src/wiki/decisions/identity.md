---
title: Identity and keys
nav_order: 10
---

How a Puddle knows who it is, and how others know it. The design is in
[Puddle: Identity and keys](/wiki/puddle/design/identity/) and [Protocol: Identity](/wiki/protocol/identity/).

### Where do the keys come from?

**Decided:** from a **recovery phrase**, written down as eight groups of four characters
(`7QK4-M2XB-9TDW-HC5R-ZP3E-A8VN-4YJF-X2K7`, the last group a checksum). The phrase gives two daily keys (signing and
encryption), kept on the machine, and a **roll key** that is never stored. *(Roadmap phase 1)*

**Why:** one thing to write down restores everything. A thief who copies the daily keys (a stolen phone, a copied file)
can't take over the identity, because rolling needs the roll key, which exists only while the phrase is typed in.

**Considered:** a word list. Characters from an alphabet with no look-alikes were chosen: 140 bits in 28 characters,
with forgiving typing (case, spaces and hyphens ignored; O is 0, I and L are 1), and every single wrong character or
swapped pair caught.

### What happens to the phrase when keys roll?

**Decided:** **the phrase rolls with the keys.** Each roll makes a new phrase, authorized by the roll key from the old
one, and the old phrase stops mattering. The new record carries three signatures: the roll key, the new signing key
and the old signing key. *(Roadmap decision 1)*

**Why:** a leaked *old* phrase is then harmless: its daily keys are retired and its roll key is spent. The current
phrase is the one master secret.

**Considered:** the old key counter-signing pre-generated "next keys". That was built first, and replaced.

### How is the phrase shown?

**Decided:** `puddled` prints it once on first run, only to a terminal (otherwise it refuses and says to run
`puddled --init`). The app shows it once, on a small first-run screen with a "written down" tick before Continue.
*(Roadmap decision 2)*

A new identity stays **unconfirmed** until the owner confirms, and the Puddle won't open one that is unconfirmed.
Quitting while the phrase is on screen would otherwise leave an identity nobody wrote down, found out only much later.
An unconfirmed identity is safe to throw away and redo, because nothing could have used it.

### What is a user id made from?

**Decided:** the hash of the first signing key **and** the first roll key's hash. *(Roadmap 1.4)*

**Why:** found while building restore. With the signing key alone, someone holding just the daily keys could sign a
different first record, with a roll key of their own, and have a valid chain for the same id. Committing to the roll
key gives any such forgery a different id. The id can still be derived from the phrase alone.

### How do you add a friend?

**Decided:** **by address**, not by user id. Adding someone means typing their address (`203.0.113.7`,
`home.example.org:8443`, port 443 by default), and the ids are exchanged over the stream. First contact trusts whoever
answers at the address. *(Roadmap 4.6)*

**Why:** nobody should have to handle a user id. Developer Mode in Settings still shows ids and short codes.

**Later:** friend codes and a handshake, an invite link that adds someone automatically, like a Discord invite, and
better address handling.

### Is a phone a full Puddle?

**Decided:** no. **A phone is a thin client of its own Puddle.** It holds none of the identity's keys and stores no
chats. It signs every request with a device key of its own, and the Puddle signs every answer. *(Roadmap phase 7)*

**Why:** one place holds the identity and the chats, so nothing has to sync between devices, and a lost phone is
revoked, not rolled.

**Considered:** copying the keys to each device, and per-device identity keys. Device keys that only authenticate to
the owner's own Puddle won.

### One encryption key, or one per chat?

**Decided:** one encryption key per Puddle, for now. No per-chat or per-group keys, and no rotation on membership
changes.

**Why:** a member who wants to leak a conversation can always forward what they read, so per-chat keys mostly limit
the damage of one stolen key. They are possible later without changing the API, which never exposes keys. For the
wire, [sealing](/wiki/decisions/streams/) now covers every body.

### Is it the same identity everywhere?

**Decided:** yes. A Puddle shows a different profile in each place (a friend, each group, each Pond), but it is the
same Puddle with the same user id. Someone who shares two places with you can see both profiles, and nobody is told
when two of your profiles meet.

**Why:** profiles are about how you present yourself, not about hiding who you are. Someone who wants two identities
that can't be linked runs two Puddles. Several identities in one Puddle is ezp2p/puddle#91.

### Which profile does a place see?

**Decided:** **nothing is shown where the owner hasn't chosen a profile.** Choosing a profile for a place is consent
for it to go there, and only there. Someone the owner has chosen nothing for sees only the user id.
([Profiles](/wiki/puddle/design/profiles/))
