from dotenv import load_dotenv

load_dotenv()

from os import environ, listdir

from discord.ext import commands

bot = commands.Bot("ip")
bot.ip_token = environ("IPLOOKUP_TOKEN")
bot.invite_link = environ("INVITE")
bot.cmd_count = 0


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(
            name=f"with {len(bot.guilds)} servers and {len(bot.users)} users and {bot.cmd_count} commands has been ran!"
        )
    )


bot.load_extension(f"src.cogs.{cog}" for cog in listdir(f"src/cogs/"))

bot.run(environ["DISCORD_TOKEN"])
