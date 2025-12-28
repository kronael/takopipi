# takopi-reload

Restart takopi to reload project configuration.

## Usage

```
/reload
```

Triggers a graceful shutdown (exit 0). Use with a process supervisor that auto-restarts.

## How it works

Sends a reload message, then exits with code 0. The container entrypoint or systemd service restarts the process, picking up updated config from `~/.takopi/takopi.toml`.

## Requirements

Process supervisor (systemd, docker, supervisor) configured to restart on exit.

## Configuration

None.
