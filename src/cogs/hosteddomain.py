import discord
import ez_rq
from discord.ext import commands

from src.cogs.utils import exceptions
from src.cogs.utils.hosted_domain import HostedDomain


class HostedDomain_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hosteddomain", aliases=["hosteddomaininfo"])
    async def hosteddomain(self, ctx, *, domain: str=None):
        if domain is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="Hosted Domain Info",
                    description="Please enter a domain name.",
                    color=0xFF0000,
                )
            )
        hosted_domain = await ez_rq.get(
            f"https://ipinfo.io/domain/{domain}/json?token={self.bot.ip_token}"
        )
        if hosted_domain.status_code == 400:
            raise exceptions.HostedDomainNotFound(hosted_domain)
            return
        elif hosted_domain.status_code == 429:
            raise exceptions.Ratelimited(hosted_domain)
            return
        hosted_domain = HostedDomain(**await hosted_domain.json())
        embed = discord.Embed(
            title=f"Hosted Domain: {hosted_domain.domain}",
            description=f"Here's some brief info about this Hosted Domain.",
            color=0x00FF00,
        )
        embed.add_field(name="Domain", value=f"{hosted_domain.domain}", inline=True)
        embed.add_field(name="IP", value=f"{hosted_domain.ip}", inline=True)
        text = ""
        for range in hosted_domain.ranges:
            text += f"""{range}\n"""
        embed.add_field(name="Ranges", value=text, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HostedDomain_Info(bot))
