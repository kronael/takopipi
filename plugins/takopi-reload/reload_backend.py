"""reload command: exit process to trigger container restart."""

import sys

from takopi.api import CommandContext
from takopi.api import CommandResult


class ReloadCommand:
    """exit process to reload projects via container restart."""

    id = "reload"
    description = "reload projects"

    async def handle(
        self, ctx: CommandContext
    ) -> CommandResult | None:
        """exit process cleanly."""
        await ctx.executor.send("reloading projects...")
        sys.exit(0)


BACKEND = ReloadCommand()
