import difflib
import traceback

import discord
from discord.ext import commands

from src.cogs.utils import exceptions


class Error_Hander(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error.original, exception.Ratelimited):
            return await ctx.send(
                embed=discord.Embed(
                    title="Ratelimited",
                    description="The bot has been ratelimited to ipinfo.io. Please try again later.",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error.original, exception.BadRequest):
            return await ctx.send(
                embed=discord.Embed(
                    title="Bad Request",
                    description="The bot has recieved a bad request from the server. Please try again later.",
                    color=discord.Color.red(),
                )
            )
        elif isinstance(error.original, commands.errors.CommandNotFound):
            commands = [command.name for command in self.bot.commands]
            closest = difflib.get_close_matches(error.original.command, commands, n=1)
            if closest:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Command Not Found",
                        description=f"The command `{error.original.command}` was not found. Did you mean `{closest[0]}`?",
                        color=discord.Color.red(),
                    )
                )
            else:
                return await ctx.send(
                    embed=discord.Embed(
                        title="Command Not Found",
                        description=f"The command `{error.original.command}` was not found.",
                        color=discord.Color.red(),
                    )
                )
        else:
            print("Traceback:")
            traceback.print_exception(type(error), error, error.__traceback__)


def setup(bot):
    bot.add_cog(Error_Hander(bot))
