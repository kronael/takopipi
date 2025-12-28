"""refresh command: restart vite dev server."""

import asyncio

from takopi.api import CommandContext
from takopi.api import CommandResult


class RefreshCommand:
    """restart vite by killing it (loop auto-restarts)."""

    id = "refresh"
    description = "restart web server"

    async def handle(
        self, ctx: CommandContext
    ) -> CommandResult | None:
        proc = await asyncio.create_subprocess_exec(
            "pkill", "-f", "vite"
        )
        await proc.wait()
        return CommandResult(text="vite restarting")


BACKEND = RefreshCommand()
