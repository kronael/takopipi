# takopipi

Plugin overlay for [banteg/takopi](https://github.com/banteg/takopi)
(pinned v0.22.1). Adds custom commands and web serving for a
Telegram-based AI agent.

## What you get

- Telegram bot that dispatches coding agents to repositories
- Custom plugins: login, reload, refresh, ship, info
- Built-in vite dev server for web apps with auto-reload
- Multi-instance support (run several bots from one image)
- Docker packaging with auto-discovery of web projects

## Live example

https://krons.fiu.wtf — web apps served by a running instance.

## Prerequisites

- Docker
- Telegram bot token (from [@BotFather](https://t.me/BotFather))

## Quick Start

```sh
# 1. build
make image

# 2. create instance (provisions config + seeds claude data dir)
./takopipi create mybot

# 3. configure
#   edit cfg/mybot/takopi.toml  (bot_token, chat_id)
#   copy credentials to /srv/data/takopipi_mybot/cfg/credentials.json
#   rebuild: make image

# 4. run via generated service file, or manually:
docker run \
  -v /srv/data/takopipi_mybot/cfg:/root/.claude \
  -v /srv/data/mybot/web:/web \
  takopipi ./takopipi mybot /cfg/takopipi_mybot.toml
```

`create` generates a systemd service file and offers to install it.

## Plugins

- `/start`, `/help` -- welcome and command list
- `/reload` -- restart container (re-discovers projects)
- `/refresh` -- restart vite dev server
- `/ship <file>` -- run [ship](https://github.com/kronael/ship) on a design file
- `/login` -- authenticate user

`/ship design.txt` runs `uvx --from git+https://github.com/kronael/ship ship <file>`.
`uvx` fetches and caches the tool on first use via uv (already installed).

## Web serving

Vite runs inside the container serving `/web/`. Port is set
via `[vite] port` in takopi.toml (default 49165).
Each subdirectory with an `index.html` becomes a live page at
`your-domain/<name>/`.

File changes auto-reload -- no restart needed.

## Multi-instance

Run multiple bots from the same image with different configs:

```sh
docker run ... takopipi ./takopipi prod
docker run ... takopipi ./takopipi staging
```

Each instance gets isolated volumes under `/srv/data/takopipi_<name>/`.

## Layout

```
plugins/     custom command plugins
cfg/         config templates (example/) and per-instance (gitignored)
takopipi     container entrypoint
Dockerfile   single-stage build
Makefile     build
```

## Config

Run `takopipi create <name>` on the host. It:
1. Seeds `cfg/<name>/` from the example template (baked into image)
2. Seeds `/srv/data/takopipi_<name>/cfg/` with `.claude` config
   (hooks, skills, CLAUDE.md) from kronael/assistants
3. Generates a systemd service file and offers to install it

Then edit:
- `cfg/<name>/takopi.toml` -- bot_token, chat_id, vite port, API keys
- `cfg/<name>/.claude/CLAUDE.local.md` -- bot context

See [ARCHITECTURE.md](ARCHITECTURE.md) for internals.
