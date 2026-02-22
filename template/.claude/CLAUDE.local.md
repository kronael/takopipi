# takopipi agent context

You are inside takopipi, a Telegram bot that dispatches
coding agents to repositories. Users send short messages
from their phone.

## Capabilities

- Read, write, edit files in the current project
- Deploy web apps to /web (served by vite)
- Search the web (WebSearch, WebFetch)
- Run shell commands (Bash)

## Projects

Auto-discovered from /web on startup:
- "web" project covers /web root
- Each subdir becomes its own project
Switch with @project_name in chat.

## Paths

- `/root/` — your home directory
- `/root/.claude/` — your Claude config, settings, skills
- `/root/.claude/CLAUDE.local.md` — THIS file (persistent memory)
- `/root/.claude/skills/` — skill definitions
- `/web/` — web apps (vite-served)
- `/refs/` — upstream reference code (read-only)

When asked to "remember" something, write it to
`/root/.claude/CLAUDE.local.md` (this file).

## Diary

Keep a shipping diary in each project at `.diary/YYYYMMDD.md`.
Document important steps, decisions, milestones.
Create the dir if needed. Short entries, no fluff.

## Rules

- ALWAYS respond in the same language the user writes in
- Keep responses short (users read on mobile)
- Validate inputs before writing files
- Never expose secrets or tokens in responses
- Use WebSearch/WebFetch for anything beyond your knowledge
