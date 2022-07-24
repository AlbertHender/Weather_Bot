import disnake
from disnake.ext import commands


class Help(commands.Cog):
    file = open('commands.txt', 'r')

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helper(self, ctx):
        dm = ctx.author
        await dm.send(Help.file.read())


def setup(bot):
    bot.add_cog(Help(bot))