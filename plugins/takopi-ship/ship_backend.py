import asyncio
from pathlib import Path

from takopi.api import CommandContext
from takopi.api import CommandResult


class ShipCommand:
    id = "ship"
    description = "run ship on a design file"

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        f = ctx.args_text.strip()
        if not f:
            return CommandResult(
                text="usage: /ship <design-file>\nexample: /ship design.txt"
            )
        p = Path(f)
        if not p.is_file():
            return CommandResult(text=f"not a file: {f}")

        try:
            proc = await asyncio.create_subprocess_exec(
                "uvx",
                "--from",
                "git+https://github.com/kronael/ship",
                "ship",
                f,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except OSError as e:
            return CommandResult(text=f"failed to start uvx: {e}")

        await ctx.executor.send(f"started ship on {f}\npid: {proc.pid}")

        try:
            _, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=3600.0,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return CommandResult(text=f"timeout running ship on {f}")

        if proc.returncode == 0:
            return CommandResult(text=f"design complete: {f}")
        err = stderr.decode().strip()
        msg = f"design failed: {f}\nexit code: {proc.returncode}"
        if err:
            msg += f"\n{err}"
        return CommandResult(text=msg)


BACKEND = ShipCommand()
