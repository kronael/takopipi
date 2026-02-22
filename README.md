# takopipi

Plugin overlay for [banteg/takopi](https://github.com/banteg/takopi)
(pinned v0.22.1). Adds custom commands and web serving for a
Telegram-based AI agent.

## What you get

- Telegram bot that dispatches coding agents to repositories
- Custom plugins: login, reload, refresh, demiurg, info
- Built-in vite dev server for web apps with auto-reload
- Multi-instance support (run several bots from one image)
- Docker packaging with auto-discovery of web projects

## Quick Start

```sh
# 1. copy and edit config
cp cfg/takopi.toml.example cfg/takopipi_mybot.toml
# set bot_token, chat_id, api keys in the new file

# 2. build
make build

# 3. run
docker run -v /srv/data/takopi:/srv/data/takopi \
  takopipi ./takopipi mybot
```

The instance name maps to `cfg/takopipi_<instance>.toml`.

## Plugins

| Command | Description |
|---------|-------------|
| `/start`, `/help` | welcome and command list |
| `/reload` | restart container (re-discovers projects) |
| `/refresh` | restart vite dev server |
| `/demiurg <file>` | spawn demiurg design session |
| `/login` | authenticate user |

## Web serving

Vite runs inside the container on port 49165, serving
`/srv/data/takopi/web/`. Each subdirectory with an
`index.html` becomes a live page at `your-domain/<name>/`.

File changes auto-reload -- no restart needed.

## Multi-instance

Run multiple bots from the same image with different configs:

```sh
docker run ... takopipi ./takopipi prod
docker run ... takopipi ./takopipi staging
```

Each reads `cfg/takopipi_<name>.toml`.

## Layout

```
plugins/     custom command plugins
cfg/         config templates and agent context
takopipi     container entrypoint
Dockerfile   single-stage build
Makefile     build
```

## Config

Copy `cfg/takopi.toml.example` and set:
- `bot_token` -- Telegram bot token from @BotFather
- `chat_id` -- allowed Telegram chat ID
- API keys for whichever LLM provider you use

See [ARCHITECTURE.md](ARCHITECTURE.md) for internals.
