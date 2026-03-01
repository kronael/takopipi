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
#   edit cfg/mybot.toml  (bot_token, chat_id)
#   create cfg/mybot.env with CLAUDE_CODE_OAUTH_TOKEN=<token>
#     (token from claude.ai account settings; fallback: mount credentials.json)
#   rebuild: make image

# 4. run via generated service file, or manually:
docker run \
  -v /srv/data/takopipi_mybot/home:/root \
  -v /srv/data/takopipi_mybot/web:/web \
  takopipi ./takopipi mybot /cfg/mybot.toml
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
template/    seed template for new instances
cfg/         per-instance configs (gitignored)
takopipi     container entrypoint
Dockerfile   single-stage build
Makefile     build
```

## Config

Run `takopipi create <name>` on the host. It:
1. Seeds `cfg/<name>.toml` from the template (baked into image)
2. Creates runtime dirs under `/srv/{spool,run,data}/takopipi_<name>/`
3. Seeds `/srv/data/takopipi_<name>/home/.claude/` with
   instance template, kronael/assistants (hooks, skills, CLAUDE.md)
4. Generates a systemd service file and offers to install it

Then edit:
- `cfg/<name>.toml` -- bot_token, chat_id, vite port, API keys
- `cfg/<name>.env` -- CLAUDE_CODE_OAUTH_TOKEN (preferred over credentials.json mount)

See [ARCHITECTURE.md](ARCHITECTURE.md) for internals.
