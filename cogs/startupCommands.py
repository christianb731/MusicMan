# -*- coding: utf-8 -*-

from discord.ext import commands

class startupCommands(commands.Cog):
    """The description for startupCommands goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def hello(self, ctx: commands.Context):
        await ctx.send('Hello {0.display_name}.'.format(ctx.author))


def setup(bot):
    bot.add_cog(startupCommands(bot))