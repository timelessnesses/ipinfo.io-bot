import discord
import ez_rq
from discord.ext import commands

from src.cogs.utils import exceptions
from src.cogs.utils.ipinfo import (ASN, ASP, IP, Abuse, Company, Domains,
                                   Privacy)


class Infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ipinfo", aliases=["ip"])
    async def ipinfo(self, ctx, *, ip: str=None):
        if ip is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="IP Info",
                    description="Please enter an IP address.",
                    color=0xFF0000,
                )
            )
        if ctx.guild:
            await ctx.message.delete()
            return await ctx.send(
                embed=discord.Embed(
                    title="Error!",
                    description="This command can only be used in DMs. Due to privacy reasons, this command is not available in guilds.",
                    color=discord.Color.red(),
                )
            )
        ipinfo = await ez_rq.get(f"http://ipinfo.io/{ip}?token{self.bot.ip_token}")
        if ipinfo.status_code == 400:
            raise exceptions.IPNotFound(ip)
            return
        elif ipinfo.status_code == 429:
            raise exceptions.Ratelimited(ip)
            return
        ipinfo = await ipinfo.json()
        ipinfo["asn"] = ASP(**ipinfo["asn"])
        ipinfo["company"] = Company(**ipinfo["company"])
        ipinfo["abuse"] = Abuse(**ipinfo["abuse"])
        ipinfo["privacy"] = Privacy(**ipinfo["privacy"])
        ipinfo["domains"] = Domains(**ipinfo["domains"])
        ipinfo = IP(**ipinfo)
        embed = discord.Embed(
            title=f"IP: {ipinfo.ip}",
            description="Here's some info about the IP address you provided.",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Basic Info",
            value=f"""
        IP: {ipinfo.ip}
        Hostname: {ipinfo.hostname}
        City: {ipinfo.city}
        Region: {ipinfo.region}
        Country: {ipinfo.country}
        Location: {ipinfo.loc}
        Organization: {ipinfo.org}
        Postal Code: {ipinfo.postal}
        Timezone: {ipinfo.timezone}
        """,
        )
        embed.add_field(
            name="ASN",
            value=f"""
        ASN: {ipinfo.asn.asn}
        Name: {ipinfo.asn.name}
        Domain: {ipinfo.asn.domain}
        Route: {ipinfo.asn.route}
        Type: {ipinfo.asn.type}
        """,
        )
        embed.add_field(
            name="Company",
            value=f"""
        Name: {ipinfo.company.name}
        Domain: {ipinfo.company.domain}
        Type: {ipinfo.company.type}
        """,
        )
        embed.add_field(
            name="Abuse",
            value=f"""
        Address: {ipinfo.abuse.address}
        Country: {ipinfo.abuse.country}
        Email: {ipinfo.abuse.email}
        Name: {ipinfo.abuse.name}
        Network: {ipinfo.abuse.network}
        Phone: {ipinfo.abuse.phone}
        """,
        )
        newline = "\n"
        embed.add_field(
            name="Domains",
            value=f"""
        Total: {ipinfo.domains.total}
        Domains: {newline.join(ipinfo.domains.domains)}
        """,
        )
        embed.add_field(
            name="Privacy",
            value=f"""
        VPN: {ipinfo.privacy.vpn}
        Proxy: {ipinfo.privacy.proxy}
        Tor: {ipinfo.privacy.tor}
        Relay: {ipinfo.privacy.relay}
        Hosting: {ipinfo.privacy.hosting}
        Service: {ipinfo.privacy.service}
        """,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Infos(bot))
