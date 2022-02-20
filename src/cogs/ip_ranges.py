import discord
import ez_rq
from discord.ext import commands

from src.cogs.utils import exceptions
from src.cogs.utils.ip_range import IPRanges


class IPRange_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="iprange", aliases=["ipranges"])
    async def iprange(self, ctx, *, ip_range: str=None):
        if ip_range is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="IP Range Info",
                    description="Please enter an IP range.",
                    color=0xFF0000,
                )
            )
        ip_range = await ez_rq.get(
            f"https://ipinfo.io/{ip_range}/json?token={self.bot.ip_token}"
        )
        if ip_range.status_code == 400:
            raise exceptions.IPRangeNotFound(ip_range)
            return
        elif ip_range.status_code == 429:
            raise exceptions.Ratelimited(ip_range)
            return
        ip_range = await ez_rq.get(
            f"https://ipinfo.io/ranges/{ip_range}/json?token={self.bot.ip_token}"
        )
        ip_range = await ip_range.json()
        ip_range = IPRanges(**ip_range)
        embed = discord.Embed(
            title=f"IP Range: {ip_range.domain}",
            description=f"Here's some brief info about this IP Range.",
            color=0x00FF00,
        )
        embed.add_field(name="Domain", value=f"{ip_range.domain}", inline=True)
        embed.add_field(
            name="Number of IPs", value=f"{ip_range.num_ranges}", inline=True
        )
        text = ""
        for range in ip_range.ranges:
            text += f"""{range}\n"""
        embed.add_field(name="Ranges", value=text, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(IPRange_Info(bot))
