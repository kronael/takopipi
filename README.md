# takopipi

Plugin overlay for [banteg/takopi](https://github.com/banteg/takopi)
(pinned v0.22.1). Adds custom commands and web serving for a
Telegram-based AI agent.

## Plugins

| Command | Description |
|---------|-------------|
| `/start`, `/help` | welcome and command list |
| `/reload` | restart container (re-discovers projects) |
| `/refresh` | restart vite dev server |
| `/demiurg <file>` | spawn demiurg design session |
| `/login` | authenticate user |

## Quick Start

```sh
cp cfg/takopi.toml.example cfg/takopi.toml
# edit cfg/takopi.toml: set bot_token and chat_id
make build
```

## Web

Vite runs inside the container on port 49165, serving
`/srv/data/takopi/web/`. Each subdirectory with an
`index.html` becomes a page at `krons.fiu.wtf/<name>/`.

File changes auto-reload — no restart needed.

## Layout

```
plugins/     custom command plugins
cfg/         config templates and agent context
takopipi     container entrypoint
Dockerfile   multi-stage build
Makefile     build
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for internals.
