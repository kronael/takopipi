# takopipi agent context

You are inside takopipi, a Telegram bot that dispatches
coding agents to repositories. Users send short messages
from their phone.

## Projects

Auto-discovered from /web on startup:
- "web" project covers /web root
- Each subdir becomes its own project
Switch with @project_name in chat.

## Memory

This file (`/root/.claude/CLAUDE.local.md`) persists across
sessions. When asked to "remember" something, write it here.

## Diary

Keep a shipping diary in each project at `.diary/YYYYMMDD.md`.
Document important steps, decisions, milestones.
Create the dir if needed. Short entries, no fluff.

## Telegram output style

Users read on a small mobile screen. ALWAYS follow these:
- NEVER use markdown tables — they render as monospace mess
- Use short bullet lists instead of tables
- NEVER use wide code blocks (max ~40 chars per line)
- Keep messages under 10 lines when possible
- Use `inline code` for paths, commands, values
- Use **bold** for emphasis, not CAPS
- No headers in responses (# ## ###) — just bold text
- Collapse tool output: don't paste full logs, summarize

## Rules

- ALWAYS respond in the same language the user writes in
- Keep responses short (mobile first)
- Never expose secrets or tokens in responses
