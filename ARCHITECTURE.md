# Architecture

Plugin overlay on banteg/takopi v0.22.1.

## Dockerfile Stages (single stage)

1. python:3.14-slim + node 22 + git
2. uv + claude-code (npm global)
3. takopi from upstream git (pinned v0.22.1)
4. plugins installed via `uv pip install -e` per plugin
5. demiurg CLI via `uv tool install`
6. config, CLAUDE.md, entrypoint copied last

## Plugin Protocol

All plugins implement `CommandBackend`:

```
id: str              -- command name (no slash)
description: str     -- shown in /help menu
handle(ctx) -> CommandResult | None
```

Registered via pyproject.toml entry points under
`takopi.command_backends`.

## Plugins

**info** -- two backends (START_BACKEND, HELP_BACKEND).
Lists projects, commands, web deploy URL.

**reload** -- `sys.exit(0)` triggers container restart.
Entrypoint re-discovers projects on next boot.

**refresh** -- `pkill -f vite` kills the dev server;
entrypoint loop auto-restarts it.

**login** -- authenticates claude-code inside container.
OAuth URL relay or direct API key.

**demiurg** -- `asyncio.create_subprocess_exec("demiurg")`
with 1h timeout. Validates file exists before spawning.

## Entrypoint Flow

```
entrypoint
  -> mkdir -p /root/.takopi
  -> copy config to /root/.takopi/takopi.toml
  -> add /web root as project "web"
  -> scan /web/*/ for subdir projects
  -> symlink CLAUDE.md into each web app dir
  -> append [projects.<name>] sections to config
  -> remove stale lock file
  -> takopi claude &  (background)
  -> mkdir -p /srv/app/tmp
  -> vite --host 0.0.0.0 --port 49165  (restart loop)
  -> write inner vite PID to /srv/app/tmp/vite.pid
  -> trap SIGINT/SIGTERM, wait
```

## Container Mounts

```
host                              container
/srv/spool/takopi/.takopi      -> /root/.takopi
/home/<user>/app               -> /refs:ro
/home/<user>/.claude/CLAUDE.md -> /root/.claude/CLAUDE.md:ro
/home/<user>/.claude/skills    -> /root/.claude/skills:ro
/srv/data/takopi/web           -> /web
```
