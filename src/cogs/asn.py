import discord
import ez_rq
from discord.ext import commands

from src.cogs.utils import exceptions
from src.cogs.utils.asn import ASN, Prefixes


class ASN_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="asn", aliases=["asninfo"])
    async def asn(self, ctx, *, asn: str=None):
        if asn is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="ASN Info",
                    description="Please enter an ASN number.",
                    color=0xFF0000,
                )
            )
        asn = await ez_rq.get(f"https://ipinfo.io/{asn}/json?token={self.bot.ip_token}")
        if asn.status_code == 400:
            raise exceptions.ASNNotFound(asn)
            return
        elif asn.status_code == 429:
            raise exceptions.Ratelimited(asn)
            return
        asn = await ez_rq.get(f"https://ipinfo.io/{asn}/json?token={self.bot.ip_token}")
        asn = await asn.json()
        for prefix in prefixes:
            asn["prefixes"].remove(prefix)
            asn["prefixes"].append(ASN(**prefix))
        asn = ASN(**asn)
        embed = discord.Embed(
            title=f"ASN: {asn.asn}",
            description=f"Here's some brief info about this ASN.",
            color=0x00FF00,
        )
        embed.add_field(name="ASN", value=f"{asn.asn}", inline=True)
        embed.add_field(name="Name", value=f"{asn.name}", inline=True)
        embed.add_field(name="Country", value=f"{asn.country}", inline=True)
        embed.add_field(
            name="Allocated", value=f"{asn.allocated}".replace("-", "/"), inline=True
        )
        embed.add_field(name="Registry", value=f"{asn.registry}", inline=True)
        embed.add_field(name="Number IPs", value=f"{asn.num_ips}", inline=True)
        embed.add_field(name="Type", value=f"{asn.type}", inline=True)
        text = ""
        for prefix in asn.prefixes:
            text += f"""
{prefix.name}:
    Netblock: {prefix.netblock}
    ID: {prefix.id}
    Country: {prefix.country}
            """
        embed.add_field(name="Prefixes", value=text, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ASN_Info(bot))
