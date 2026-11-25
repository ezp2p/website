---
title: Installation
nav_order: 10
---

A Pond is two programs: `pondd`, the service, which has no window and serves HTTPS; and `pondctl`, the admin's tool,
which runs beside it with the same config. Messages are kept in MariaDB.

You need a machine that's always on with a public address (a VPS, or a home server with ports forwarded), and a name
for it, such as `pond.example.org`. Open the Pond's ports to it first: by default that's **443, TCP and UDP**. What
each port is for, and how to change them, is on [Ports]({{ '/wiki/pond/ports/' | relative_url }}).

Pond is in early testing, so there's no stable release yet: use the **dev** image, `ghcr.io/ezp2p/pond:dev`, the newest
build of Pond's `dev` branch.

## With Docker

The easy way. Docker runs the Pond and its database together, writes the config, and sets the Pond up on its first
start: there's nothing to build or install.

### 1. Write the two files

In a new folder, a `compose.yaml`:

```yaml
services:
  pond:
    image: ghcr.io/ezp2p/pond:dev
    container_name: pond
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      POND_ADDRESS: ${POND_ADDRESS}
      POND_NAME: ${POND_NAME}
      POND_CHAT_PORT: 443
      POND_VOICE_PORT: 443
      POND_DB_HOST: db
      POND_DB_PASSWORD: ${POND_DB_PASSWORD}
    ports:
      - "443:443/tcp"   # chat: joining, channels, messages, files
      - "443:443/udp"   # voice and video
    volumes:
      - pond:/data

  db:
    image: mariadb:11
    container_name: pond-db
    restart: unless-stopped
    environment:
      MARIADB_DATABASE: pond
      MARIADB_USER: pond
      MARIADB_PASSWORD: ${POND_DB_PASSWORD}
      MARIADB_RANDOM_ROOT_PASSWORD: "1"
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 5s
      timeout: 5s
      retries: 20
    volumes:
      - db:/var/lib/mysql

volumes:
  pond:
  db:
```

And beside it, a `.env`:

```sh
POND_ADDRESS=pond.example.org              # how people reach the Pond; what invite links say
POND_NAME=My Pond                          # the Pond's name, set on the first start
POND_DB_PASSWORD=change-me-to-something-long
```

The database password is only used between the two containers, so make it long and random and forget it.

### 2. Start it

```sh
docker compose up -d
```

On its first start the Pond waits for MariaDB, makes its key, its tables and a `#general` channel, and starts serving.
`docker compose logs -f pond` shows it happening.

### 3. Invite people

```sh
docker exec pond pondctl invite create --uses 10 --expires 7d
```

Give out the `pond://…` link it prints. People join by pasting it into Puddle (the **+** at the bottom of the server
rail). Every other `pondctl` command works the same way:

```sh
docker exec pond pondctl channel create random --topic "Anything goes"
docker exec pond pondctl info
```

### Everyday

- **Update to the newest dev build:** `docker compose pull && docker compose up -d`.
- **Back up both volumes:** `pond` holds the Pond's key (a new key is a new Pond, and members would have to join again),
  and `db` holds everything else.
- **Change a setting:** the container writes `/data/pond.yaml` on its first start and reads it from then on. Copy it
  out with `docker cp pond:/data/pond.yaml .`, edit it, copy it back, and `docker restart pond`.

Running behind a reverse proxy, or against a MariaDB you already have, is in
[docs/docker.md](https://github.com/ezp2p/pond/blob/dev/docs/docker.md).

## Manual installation

Building it yourself is useful for development, or for running it without Docker.

### Build

Pond is C++20, built on [Drogon](https://github.com/drogonframework/drogon), which CMake fetches and builds the first
time (a few minutes). It needs MariaDB (the server and its C client), OpenSSL 3 or later, hiredis, jsoncpp and yaml-cpp.

```sh
# Debian / Ubuntu
apt install mariadb-server libmariadb-dev libssl-dev libhiredis-dev libjsoncpp-dev libyaml-cpp-dev uuid-dev zlib1g-dev
# macOS
brew install mariadb openssl hiredis jsoncpp yaml-cpp

git clone -b dev --recurse-submodules https://github.com/ezp2p/pond.git && cd pond
scripts/build.sh      # builds and runs the tests
```

### Set up

Make a database and a user for it:

```sh
mariadb -e "CREATE DATABASE pond; CREATE USER pond@localhost IDENTIFIED BY 'secret'; GRANT ALL ON pond.* TO pond@localhost"
```

Copy the example config and edit it:

```sh
cp pond.yaml.example pond.yaml
```

The settings that matter first:

```yaml
listen: 0.0.0.0
ports:
  chat: 443     # TCP
  voice: 443    # UDP
address: pond.example.org      # what invite links say
data_dir: /var/lib/pond        # the Pond's key and TLS certificate
database:
  host: 127.0.0.1
  user: pond
  password: secret
  name: pond
```

Then initialise the Pond, which makes its key, its tables and `#general`:

```sh
build/pondctl init "My Pond"
```

### Run and invite

```sh
build/pondd
build/pondctl invite create --uses 10 --expires 7d
```

### Trying it out

`scripts/dev.sh` starts a throwaway MariaDB and a Pond with an invite, for trying things out on your own machine.
