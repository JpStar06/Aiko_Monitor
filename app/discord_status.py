import os
import aiohttp
from datetime import datetime, timezone


class DiscordStatus:
    def __init__(self):
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        self.channel_id = os.getenv("STATUS_CHANNEL_ID")

        if not self.bot_token:
            raise RuntimeError("DISCORD_BOT_TOKEN não foi configurado.")

        if not self.channel_id:
            raise RuntimeError("STATUS_CHANNEL_ID não foi configurado.")

        self.base_url = (
            f"https://discord.com/api/v10/channels/"
            f"{self.channel_id}/messages"
        )

    async def _send(self, *, content=None, embed=None):
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        payload = {}

        if content:
            payload["content"] = content

        if embed:
            payload["embeds"] = [embed]

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url,
                headers=headers,
                json=payload,
            ) as response:

                if response.status >= 300:
                    body = await response.text()
                    raise RuntimeError(
                        f"Discord API retornou HTTP "
                        f"{response.status}: {body}"
                    )

    async def send_offline(self, seconds_without_heartbeat: float):
        minutes = seconds_without_heartbeat / 60

        embed = {
            "title": "🔴 AikoBot Offline",
            "description": (
                "O monitor detectou que o AikoBot parou de "
                "enviar heartbeats."
            ),
            "color": 0xFF0000,
            "fields": [
                {
                    "name": "⏱️ Tempo sem heartbeat",
                    "value": f"**{minutes:.1f} minutos**",
                    "inline": True,
                },
                {
                    "name": "📡 Status",
                    "value": "🔴 Offline",
                    "inline": True,
                },
            ],
            "footer": {
                "text": "AikoMonitor"
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        await self._send(embed=embed)

    async def send_online(self):
        embed = {
            "title": "🟢 AikoBot Online",
            "description": (
                "O AikoBot voltou a enviar heartbeats "
                "normalmente."
            ),
            "color": 0x00FF00,
            "fields": [
                {
                    "name": "📡 Status",
                    "value": "🟢 Online",
                    "inline": True,
                },
            ],
            "footer": {
                "text": "AikoMonitor"
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        await self._send(embed=embed)