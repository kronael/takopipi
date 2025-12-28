"""info commands: /start and /help for takopi."""

from takopi.api import CommandContext
from takopi.api import CommandResult
from takopi.commands import list_command_ids


class StartCommand:
    """welcome message for new users."""

    id = "start"
    description = "show welcome info"

    async def handle(
        self, ctx: CommandContext
    ) -> CommandResult | None:
        """output welcome and available commands."""
        lines = ["takopi - ai dev assistant", ""]
        projects = ctx.runtime.project_aliases()
        if projects:
            lines.append(
                "projects: " + ", ".join(projects)
            )
        commands = list_command_ids(
            allowlist=ctx.runtime.allowlist
        )
        if commands:
            lines.append(
                "commands: /"
                + ", /".join(commands)
            )
        lines.append("")
        lines.append(
            "send a message to start working."
        )
        return CommandResult(text="\n".join(lines))


class HelpCommand:
    """list available commands and usage."""

    id = "help"
    description = "show available commands"

    async def handle(
        self, ctx: CommandContext
    ) -> CommandResult | None:
        """output command list with descriptions."""
        lines = ["available commands:", ""]
        commands = list_command_ids(
            allowlist=ctx.runtime.allowlist
        )
        for cmd in sorted(commands):
            lines.append(f"  /{cmd}")
        lines.append("")
        projects = ctx.runtime.project_aliases()
        if projects:
            lines.append(
                "switch project: @project_name"
            )
        lines.append(
            "web deploy: takopi.fiu.wtf"
        )
        return CommandResult(text="\n".join(lines))


START_BACKEND = StartCommand()
HELP_BACKEND = HelpCommand()
