# Architecture

Plugin overlay on banteg/takopi v0.22.1.

## Dockerfile (single stage)

1. python:3.14-slim + node 22 + git
2. uv + claude-code (npm global)
3. takopi from upstream git (pinned v0.22.1)
4. plugins installed via `uv pip install -e` per plugin
5. seed template baked at `/srv/app/seed/example/`
6. cfg/, entrypoint copied last

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

**refresh** -- part of takopi-reload package.
Kills vite by PID; entrypoint loop auto-restarts it.

**login** -- authenticates claude-code inside container.
OAuth URL relay or direct API key.

**ship** -- `uvx --from git+https://github.com/kronael/ship ship <file>`
with 1h timeout. Validates file exists before spawning.

## Entrypoint Flow

```
takopipi create <name>
  -> cp seed/example -> cfg/<name>/
  -> seed external data dir .claude with config from:
     - instance template (cfg/<name>/.claude/)
     - kronael/assistants: CLAUDE.md, hooks, skills,
       credentials template
  -> print setup instructions

takopipi <instance>
  -> cp cfg/<instance>/takopi.toml -> /root/.takopi/takopi.toml
  -> auto-discover /web projects, append to config
  -> remove stale lock file
  -> read [vite] port from config (default 49165)
  -> takopi claude &  (background)
  -> vite --host 0.0.0.0 --port <configured>  (restart loop)
  -> trap SIGINT/SIGTERM, wait
```

## Container Mounts

```
host                                        container
/srv/data/takopipi_<name>/cfg            -> /srv/app/cfg
/srv/data/takopipi_<name>/home/.claude   -> /root/.claude
/srv/data/takopipi_<name>/data/web       -> /web
/srv/spool/takopipi_<name>/.takopi       -> /root/.takopi
/home/<user>/app                         -> /refs:ro
```

## cfg Layout

```
cfg/
  example/                    committed; seed template
    takopi.toml               example config
    .claude/
      CLAUDE.local.md         bot context
      settings.json           outputStyle=telegram
      output-styles/
        telegram.md           short plain-text for mobile chat
      skills/
        web/
          SKILL.md            web deployment skill template
          template/           web project scaffold
        self/SKILL.md         self-inspection + skill creation
  <instance>/                 gitignored; per-instance
```

## Claude-code Layering

All native claude-code features, no custom injection:

- `~/.claude/CLAUDE.md` -- dev wisdom; provisioned by `create`
  from kronael/assistants
- `~/.claude/CLAUDE.local.md` -- bot context; provisioned by `create`
- `~/.claude/output-styles/telegram.md` -- auto-activated each prompt
- `~/.claude/skills/` -- provisioned by `create` from instance
  template and kronael/assistants
- `~/.claude/hooks/` -- provisioned by `create` from kronael/assistants

/root/.claude is fully host-mounted; provisioned once by `create` and
updated live via the self skill. CLAUDE.local.md and output-styles are
native claude-code features: auto-loaded, no hooks needed.
