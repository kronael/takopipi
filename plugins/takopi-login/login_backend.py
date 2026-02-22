"""login command: authenticate claude code via oauth."""

import asyncio
import json
import os
import re

from takopi.api import CommandContext
from takopi.api import CommandResult

URL_RE = re.compile(r"https://claude\.ai/oauth/authorize\S+")
ENV = {
    "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin"),
    "HOME": os.environ.get("HOME", "/root"),
}


class LoginCommand:
    id = "login"
    description = "authenticate claude code"

    def __init__(self):
        self._proc: asyncio.subprocess.Process | None = None
        self._notify: asyncio.Task | None = None

    async def handle(self, ctx: CommandContext) -> CommandResult | None:
        if self._proc and self._proc.returncode is None:
            return CommandResult(text="login already in progress")
        return await self._login(ctx)

    async def _login(self, ctx):
        try:
            self._proc = await asyncio.create_subprocess_exec(
                "claude",
                "auth",
                "login",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                env=ENV,
            )
        except FileNotFoundError:
            return CommandResult(text="claude cli not found")
        except OSError as e:
            return CommandResult(text=f"failed to start claude: {e}")
        url = await self._read_url()
        if not url:
            self._proc.kill()
            self._proc = None
            return CommandResult(text="failed to get auth url")
        self._notify = asyncio.create_task(self._wait(ctx))
        return CommandResult(text=f"open this link to sign in:\n{url}")

    async def _read_url(self):
        if not self._proc or not self._proc.stdout:
            return None
        buf = b""
        try:
            while True:
                chunk = await asyncio.wait_for(
                    self._proc.stdout.read(4096),
                    timeout=10,
                )
                if not chunk:
                    break
                buf += chunk
                m = URL_RE.search(buf.decode(errors="replace"))
                if m:
                    return m.group(0)
        except asyncio.TimeoutError:
            pass
        return None

    async def _wait(self, ctx):
        if not self._proc:
            return
        try:
            await asyncio.wait_for(self._proc.wait(), timeout=300)
            if self._proc.returncode == 0:
                status = await self._status()
                await ctx.executor.send(f"authenticated\n{status}")
            else:
                await ctx.executor.send("authentication failed")
        except asyncio.TimeoutError:
            self._proc.kill()
            await ctx.executor.send("authentication timed out (5m)")
        finally:
            self._proc = None

    async def _status(self):
        proc = await asyncio.create_subprocess_exec(
            "claude",
            "auth",
            "status",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=ENV,
        )
        out, _ = await proc.communicate()
        try:
            d = json.loads(out)
            email = d.get("email", "?")
            plan = d.get("subscriptionType", "?")
            return f"{email} ({plan})"
        except (json.JSONDecodeError, KeyError):
            return out.decode().strip() or "unknown"


BACKEND = LoginCommand()
