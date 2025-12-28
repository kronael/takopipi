"""demiurg command: run autonomous design sessions."""

import asyncio
from pathlib import Path

from takopi.api import CommandContext
from takopi.api import CommandResult


class DemiurgCommand:
    """run autonomous design session via demiurg tool."""

    id = "demiurg"
    description = "run autonomous design session"

    async def handle(
        self, ctx: CommandContext
    ) -> CommandResult | None:
        """execute demiurg with design file."""
        if not ctx.args_text.strip():
            return CommandResult(
                text=(
                    "usage: /demiurg <design-file>\n"
                    "example: /demiurg design.txt"
                )
            )

        design_file = ctx.args_text.strip()

        design_path = Path(design_file)
        if not design_path.exists():
            return CommandResult(
                text=f"FileNotFound: {design_file}"
            )

        if not design_path.is_file():
            return CommandResult(
                text=f"not a file: {design_file}"
            )

        try:
            proc = await asyncio.create_subprocess_exec(
                "demiurg",
                design_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError:
            return CommandResult(
                text="demiurg command not found in PATH"
            )
        except PermissionError:
            return CommandResult(
                text="permission denied executing demiurg"
            )

        await ctx.executor.send(
            f"started demiurg on {design_file}\n"
            f"pid: {proc.pid}"
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=3600.0,
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return CommandResult(
                text=f"timeout running demiurg on {design_file}"
            )

        if proc.returncode == 0:
            result = f"design complete: {design_file}"
        else:
            err = stderr.decode().strip()
            result = (
                f"design failed: {design_file}\n"
                f"exit code: {proc.returncode}"
            )
            if err:
                result += f"\n{err}"

        return CommandResult(text=result)


BACKEND = DemiurgCommand()
