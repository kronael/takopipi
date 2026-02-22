# takopipi

Telegram bot overlay on [takopi](https://github.com/banteg/takopi).
Adds custom plugins (login, reload, refresh, ship, info) and
Docker packaging.

## Layout

```
plugins/          custom command plugins (tracked)
cfg/              config templates and agent context (tracked)
refs/takopi/      upstream takopi v0.22.1 source (gitignored, reference only)
takopipi          container entrypoint (bash)
Dockerfile        single-stage build
Makefile          build
```

## Reference source

`refs/takopi/` contains the full upstream takopi v0.22.1 source for
API reference when writing plugins. Key files:
- `refs/takopi/api.py` - public plugin API
- `refs/takopi/commands.py` - CommandContext, CommandResult, CommandExecutor
- `refs/takopi/transport.py` - Transport protocol (send, edit, delete)
- `refs/takopi/telegram/commands/executor.py` - executor implementation

## Plugin API

Plugins implement `CommandBackend` protocol:
- `id: str` - command name
- `description: str` - help text
- `async handle(ctx: CommandContext) -> CommandResult | None`

`CommandContext` fields: `command`, `text`, `args_text`, `args`,
`message` (MessageRef), `executor` (send/run_one/run_many),
`runtime`, `plugin_config`.

`CommandResult(text=..., notify=True, reply_to=None)`.
