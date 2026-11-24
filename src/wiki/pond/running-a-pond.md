---
title: Running a Pond
nav_order: 10
---

A Pond is two programs: `pondd`, the service, which has no window and serves HTTPS on one port; and `pondctl`, the
admin's tool, which runs on the same machine with the same config.

## Build

Pond is C++20, built on [Drogon](https://github.com/drogonframework/drogon), which CMake fetches and builds the first
time (a few minutes). It needs MariaDB (the server and its C client), OpenSSL 3 or later, hiredis, jsoncpp and yaml-cpp.

```sh
# Debian / Ubuntu
apt install mariadb-server libmariadb-dev libssl-dev libhiredis-dev libjsoncpp-dev libyaml-cpp-dev uuid-dev zlib1g-dev
# macOS
brew install mariadb openssl hiredis jsoncpp yaml-cpp

git clone https://github.com/ezp2p/pond.git && cd pond
scripts/build.sh      # builds and runs the tests
```

## Set up

Make a database and a user for it, then configure and initialise the Pond:

```sh
mariadb -e "CREATE DATABASE pond; CREATE USER pond@localhost IDENTIFIED BY 'secret'; GRANT ALL ON pond.* TO pond@localhost"
cp pond.yaml.example pond.yaml     # and edit it
build/pondctl init "My Pond"       # makes the key, the tables and #general
```

## Invite people

```sh
build/pondctl invite create --uses 10 --expires 7d
```

Give out the `pond://…` link it prints. People join by pasting it into Puddle (the **+** at the bottom of the server
rail).

## Run

```sh
build/pondd
```

## Trying it out

`scripts/dev.sh` starts a throwaway MariaDB and a Pond with an invite, for trying things out.
