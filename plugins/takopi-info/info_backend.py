import os

from takopi.api import CommandContext
from takopi.api import CommandResult
from takopi.commands import list_command_ids


def _web_url():
    host = os.environ.get("WEB_HOST", "")
    if host:
        return f"https://{host}/"
    return ""


class StartCommand:
    id = "start"
    description = "show welcome info"

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        lines = ["takopipi - ai dev assistant", ""]
        projects = ctx.runtime.project_aliases()
        if projects:
            lines.append("projects: " + ", ".join(projects))
        cmds = list_command_ids(allowlist=ctx.runtime.allowlist)
        if cmds:
            lines.append("commands: /" + ", /".join(cmds))
        url = _web_url()
        if url:
            lines.append(f"web: {url}")
        lines += ["", "send a message to start working."]
        return CommandResult(text="\n".join(lines))


class HelpCommand:
    id = "help"
    description = "show available commands"

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        cmds = list_command_ids(allowlist=ctx.runtime.allowlist)
        lines = ["available commands:", ""]
        lines += [f"  /{c}" for c in sorted(cmds)]
        lines.append("")
        if ctx.runtime.project_aliases():
            lines.append("switch project: @project_name")
        url = _web_url()
        if url:
            lines.append(f"web: {url}")
        else:
            lines.append("web deploy: vite (see takopi.toml)")
        return CommandResult(text="\n".join(lines))


START_BACKEND = StartCommand()
HELP_BACKEND = HelpCommand()
