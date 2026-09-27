import os
import aiohttp


class DiscordStatus:
    def __init__(self):
        self.bot_token = os.getenv("DISCORD_BOT_TOKEN")
        self.channel_id = os.getenv("STATUS_CHANNEL_ID")

        if not self.bot_token:
            raise RuntimeError("DISCORD_BOT_TOKEN não foi configurado.")

        if not self.channel_id:
            raise RuntimeError("STATUS_CHANNEL_ID não foi configurado.")

        self.base_url = (
            f"https://discord.com/api/v10/channels/{self.channel_id}/messages"
        )

    async def _send(self, content: str):
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers=headers,
                json={"content": content},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status >= 300:
                    body = await response.text()
                    raise RuntimeError(
                        f"Discord API retornou HTTP {response.status}: {body}"
                    )

    async def send_offline(self, seconds_without_heartbeat: float):
        minutes = seconds_without_heartbeat / 60

        await self._send(
            "🔴 **AikoBot ficou offline.**\n"
            f"Não recebo heartbeat há aproximadamente **{minutes:.1f} minutos**."
        )

    async def send_online(self):
        await self._send(
            "🟢 **AikoBot voltou online!**"
        )
