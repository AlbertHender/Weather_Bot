import disnake
from disnake.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file = open('commands.txt', 'r')

    @commands.command()
    async def helper(self, ctx):
        dm = ctx.author
        await dm.send(self.file.read())


def setup(bot):
    bot.add_cog(Help(bot))
