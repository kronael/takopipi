---
name: self
description: Inspect and modify takopipi source, plugins, and skills
trigger: self-inspection, skill creation, plugin editing, "how do I work"
---

# Self-inspection and skill modification

## Source locations

- `/srv/app/` -- takopipi source (entrypoint, plugins, cfg)
- `/srv/app/takopipi` -- container entrypoint (bash)
- `/srv/app/plugins/` -- custom command plugins
- `/srv/app/cfg/` -- config templates and per-instance configs

## Skills

Skills live at `/root/.claude/skills/<name>/SKILL.md`.

### SKILL.md format

```yaml
---
name: skill-name
description: One-line description
trigger: comma-separated trigger phrases
---
```

Followed by markdown body with ALWAYS/NEVER statements and
instructions.

### Creating a new skill

1. `mkdir -p /root/.claude/skills/<name>`
2. Write `SKILL.md` with YAML frontmatter + body
3. Skill is available immediately (no restart needed)

### Modifying existing skills

- Read `/root/.claude/skills/` to list all skills
- Edit the SKILL.md file directly
- NEVER delete skills without explicit user request

## Plugin inspection

- Each plugin is a Python package in `/srv/app/plugins/`
- Entry points registered in `pyproject.toml`
- Implements `CommandBackend` protocol (see /srv/app/CLAUDE.md)

## Rules

- ALWAYS read before modifying any source file
- NEVER modify files in /refs (read-only reference)
- ALWAYS validate changes build correctly after editing plugins

## Updating from upstream

### Skills, hooks, CLAUDE.md (from kronael/assistants)

```sh
git clone --depth 1 https://github.com/kronael/assistants /tmp/a
cp /tmp/a/claude-template/global/CLAUDE.md /root/.claude/CLAUDE.md
cp -r /tmp/a/claude-template/global/hooks/. /root/.claude/hooks/
cp -rn /tmp/a/claude-template/global/skills/. /root/.claude/skills/
rm -rf /tmp/a
```

### Web/self skills (from takopipi source)

```sh
cp -r /srv/app/cfg/example/.claude/skills/. /root/.claude/skills/
```
