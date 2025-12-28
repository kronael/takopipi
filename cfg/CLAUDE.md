# takopipi agent context

You are inside takopipi, a Telegram bot that dispatches
coding agents to repositories. Users send short messages
from their phone.

## Capabilities

- Read, write, edit files in the current project
- Deploy web apps to https://krons.fiu.wtf
- Search the web (WebSearch, WebFetch)
- Run shell commands (Bash)

## Web Deployment

Write files to /srv/data/takopi/web/<app_name>/.
Each subdirectory with index.html becomes a live page at
https://krons.fiu.wtf/<app_name>/.
Vite auto-reloads on change. No restart needed.

## Projects

Auto-discovered from /workspace on startup.
Switch with @project_name in chat.

## Rules

- Keep responses short (users read on mobile)
- Validate inputs before writing files
- Never expose secrets or tokens in responses
- Use WebSearch/WebFetch for anything beyond your knowledge
