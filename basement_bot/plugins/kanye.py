import asyncio
from random import choice, randint

from discord import Embed

from cogs import HttpPlugin, LoopPlugin


def setup(bot):
    bot.add_cog(KanyeQuotes(bot))


class KanyeQuotes(LoopPlugin, HttpPlugin):

    PLUGIN_NAME = __name__
    API_URL = "https://api.kanye.rest"
    KANYE_PICS = [
        "https://i.imgur.com/ITmTXGz.jpg",
        "https://i.imgur.com/o8BkPrL.jpg",
        "https://i.imgur.com/sA5qP3F.jpg",
        "https://i.imgur.com/1fX29Y3.jpg",
        "https://i.imgur.com/g1o2Gro.jpg",
    ]

    async def loop_preconfig(self):
        min_wait = self.config.min_hours
        max_wait = self.config.max_hours

        if min_wait < 0 or max_wait < 0:
            raise RuntimeError("Min and max times must both be greater than 0")
        if max_wait - min_wait <= 0:
            raise RuntimeError(f"Max time must be greater than min time")

        self.channel = self.bot.get_channel(self.config.channel)
        if not self.channel:
            raise RuntimeError("Unable to get channel for Kanye Quotes plugin")

        if not self.config.on_start:
            await self.wait()

    async def execute(self):
        response = await self.http_call("get", self.API_URL)
        quote = response.json().get("quote")

        if quote:
            message = f"'*{quote}*' - Kanye West"
            embed = Embed(title=f'"{quote}"', description="Kanye Quest")
            embed.set_thumbnail(url=choice(self.KANYE_PICS))
            await self.channel.send(embed=embed)

    async def wait(self):
        await asyncio.sleep(
            randint(self.config.min_hours * 3600, self.config.max_hours * 3600,)
        )
