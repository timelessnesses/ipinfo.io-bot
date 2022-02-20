import discord
import ez_rq
from discord.ext import commands

from src.cogs.utils import exceptions
from src.cogs.utils.whois import NetInfo, NetInfoRecords, POCInfo, POCInfoRecords

class WhoIs_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="whois", aliases=["whoisinfo"])
    async def whois(self, ctx, type: str=None,*, domain: str=None):
        if domain is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="WhoIs Info",
                    description="Please enter a domain name.",
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
        if type is None:
            return await ctx.send(
                embed=discord.Embed(
                    title="WhoIs Info",
                    description="Please enter a type.\n`net` for net info.\n`poc` for poc info.",
                    color=0xFF0000,
                )
            )
        if type.lower() == "net":
            whois = await ez_rq.get(f"https://api.hackertarget.com/whois/?q={domain}")
            if whois.status_code == 400:
                raise exceptions.DomainNotFound(domain)
                return
            elif whois.status_code == 429:
                raise exceptions.Ratelimited(domain)
                return
            whois = await whois.json()
            for record in whois["records"]:
                whois["records"].remove(record)
                whois["records"].append(NetInfoRecords(**record))
            whois = NetInfo(**whois)
            embed = discord.Embed(
                title=f"WhoIs Info for {domain}",
                description="Here's some info about the domain you provided.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Basic Info",
                value=f"""
                Net Name: {whois.net}
                Total of records: {whois.total}
                """
            )
            text = ""
            for record in whois.records:
                text += f"""
{record.name}:
    Range: {record.range}
    ID: {record.id}
    Country: {record.country}
    Organization: {record.organization}
    Admin: {record.admin}
    Tech: {record.tech}
    Abuse: {record.abuse}
    Maintainer: {record.maintainer}
    Created: {record.created}
    Updated: {record.updated}
    Status: {record.status}
    Source: {record.source}
                """
                
            
