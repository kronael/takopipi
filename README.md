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
mkdir -p /srv/data/takopipi_mybot/home/.claude
cp ~/.claude/.credentials.json /srv/data/takopipi_mybot/home/.claude/

# 3. one-time: create instance (provisions cfg, .claude config, hooks, skills, CLAUDE.md)
docker run --rm \
  -v /srv/data/takopipi_mybot/cfg:/srv/app/cfg \
  -v /srv/data/takopipi_mybot/home/.claude:/root/.claude \
  takopipi takopipi create mybot
# edit /srv/data/takopipi_mybot/cfg/mybot/takopi.toml

# 4. run (all volume mounts every time)
docker run \
  -v /srv/data/takopipi_mybot/cfg:/srv/app/cfg \
  -v /srv/data/takopipi_mybot/home/.claude:/root/.claude \
  -v /srv/data/takopipi_mybot/data/web:/web \
  -v /srv/spool/takopipi_mybot/.takopi:/root/.takopi \
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

Use `takopipi create <name>` to provision a new instance: it seeds the
cfg directory from the example template and populates `.claude` with
config, hooks, skills, and CLAUDE.md from kronael/assistants. Then edit:
- `takopi.toml` -- bot_token, chat_id, vite port, API keys
- `.claude/CLAUDE.local.md` -- bot context

To update .claude config later, follow the instructions in the self skill.

See [ARCHITECTURE.md](ARCHITECTURE.md) for internals.
