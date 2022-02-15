from discord.ext import commands

class startupCommands(commands.Cog):
    """The description for startupCommands goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def hello(self, ctx: commands.Context):
        await ctx.send('Hello {0.display_name}.'.format(ctx.author))

    @commands.command(pass_context=True)
    async def commands(self, ctx:commands.Context):
        await ctx.send("Commands:\n"+
                       "!commands: Lists all commands.\n"+
                       "!play (query/url): Plays a url link or searches youtube for a song\n"+
                       "!join: Forces bot to join user's current voice channel\n"+
                       "!queue: Displays the current song queue and currently playing song\n"+
                       "!skip: Skips currently playing song\n"+
                       "!pause: Pauses the player\n"+
                       "!resume: Resumes the player after a pause\n"+
                       "!volume (value): Changes bot volume to a value between 0 - 100.")

def setup(bot):
    bot.add_cog(startupCommands(bot))