"""ship command: run ship on a design file."""

import asyncio
from pathlib import Path

from takopi.api import CommandContext
from takopi.api import CommandResult


class ShipCommand:
    """run ship on a design file."""

    id = "ship"
    description = "run ship on a design file"

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        """execute ship with design file."""
        if not ctx.args_text.strip():
            return CommandResult(
                text=("usage: /ship <design-file>\nexample: /ship design.txt")
            )

        design_file = ctx.args_text.strip()

        design_path = Path(design_file)
        if not design_path.exists():
            return CommandResult(text=f"FileNotFound: {design_file}")

        if not design_path.is_file():
            return CommandResult(text=f"not a file: {design_file}")

        try:
            proc = await asyncio.create_subprocess_exec(
                "uvx",
                "--from",
                "git+https://github.com/kronael/ship",
                "ship",
                design_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError:
            return CommandResult(text="uvx command not found in PATH")
        except PermissionError:
            return CommandResult(text="permission denied executing uvx")

        await ctx.executor.send(f"started ship on {design_file}\npid: {proc.pid}")

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=3600.0,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return CommandResult(text=f"timeout running ship on {design_file}")

        if proc.returncode == 0:
            result = f"design complete: {design_file}"
        else:
            err = stderr.decode().strip()
            result = f"design failed: {design_file}\nexit code: {proc.returncode}"
            if err:
                result += f"\n{err}"

        return CommandResult(text=result)


BACKEND = ShipCommand()
