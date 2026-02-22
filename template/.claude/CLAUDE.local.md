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

## Rules

- ALWAYS respond in the same language the user writes in
- Keep responses short (users read on mobile)
- Never expose secrets or tokens in responses
