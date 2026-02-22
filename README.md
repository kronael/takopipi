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

## Quick Start

```sh
# 1. build
make build

# 2. one-time: seed credentials into data volume
mkdir -p /srv/data/takopi_mybot/home/.claude
cp ~/.claude/.credentials.json /srv/data/takopi_mybot/home/.claude/

# 3. one-time: create instance config (cfg volume needed)
docker run --rm \
  -v /srv/data/takopi_mybot/cfg:/srv/app/cfg \
  takopipi takopipi create mybot
# edit /srv/data/takopi_mybot/cfg/mybot/takopi.toml

# 4. run (all volume mounts every time)
docker run \
  -v /srv/data/takopi_mybot/cfg:/srv/app/cfg \
  -v /srv/data/takopi_mybot/home/.claude:/root/.claude \
  -v /srv/data/takopi_mybot/data/web:/web \
  -v /srv/spool/takopi_mybot/.takopi:/root/.takopi \
  -v /home/<user>/app:/refs:ro \
  takopipi ./takopipi mybot
```

Volume mounts are not optional -- they must appear on every
`docker run`. The one-time steps only populate the volume dirs
before first start.

## Plugins

- `/start`, `/help` -- welcome and command list
- `/reload` -- restart container (re-discovers projects)
- `/refresh` -- restart vite dev server
- `/ship <file>` -- run [ship](https://github.com/kronael/ship) on a design file
- `/login` -- authenticate user

`/ship design.txt` runs `uvx --from git+https://github.com/kronael/ship ship <file>`.
`uvx` fetches and caches the tool on first use via uv (already installed).

## Web serving

Vite runs inside the container on port 49165, serving `/web/`.
Each subdirectory with an `index.html` becomes a live page at
`your-domain/<name>/`.

File changes auto-reload -- no restart needed.

## Multi-instance

Run multiple bots from the same image with different configs:

```sh
docker run ... takopipi ./takopipi prod
docker run ... takopipi ./takopipi staging
```

Each instance gets isolated volumes under `/srv/data/takopi_<name>/`.

## Layout

```
plugins/     custom command plugins
cfg/         config templates (example/) and per-instance (gitignored)
takopipi     container entrypoint
Dockerfile   single-stage build
Makefile     build
```

## Config

Use `takopipi create <name>` to seed a new instance config from
the example template. Then edit:
- `takopi.toml` -- bot_token, chat_id, API keys
- `.claude/CLAUDE.local.md` -- bot context (overwritten each start)

The entrypoint auto-activates the `telegram` output style and
seeds CLAUDE.md + hooks from kronael/assistants on first run.

See [ARCHITECTURE.md](ARCHITECTURE.md) for internals.
