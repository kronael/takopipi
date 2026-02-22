import asyncio
import sys
from pathlib import Path

from takopi.api import CommandContext
from takopi.api import CommandResult

VITE_PID = Path("/srv/app/tmp/vite.pid")


class ReloadCommand:
    id = "reload"
    description = "reload projects (restarts container)"

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        await ctx.executor.send("reloading...")
        sys.exit(0)


class RefreshCommand:
    id = "refresh"
    description = "restart web server"

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        try:
            pid = int(VITE_PID.read_text().strip())
        except (FileNotFoundError, ValueError):
            return CommandResult(text="vite pid not found")
        try:
            proc = await asyncio.create_subprocess_exec("kill", str(pid))
            await proc.wait()
        except OSError as e:
            return CommandResult(text=f"kill failed: {e}")
        if proc.returncode != 0:
            return CommandResult(text=f"kill exited {proc.returncode}")
        return CommandResult(text="vite restarting")


RELOAD_BACKEND = ReloadCommand()
REFRESH_BACKEND = RefreshCommand()
