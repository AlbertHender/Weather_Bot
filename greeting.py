import disnake
from disnake.ext import commands, tasks


class Greeting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.disabled = {}

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print("Joined a server!!")
        f = open('intro.txt', 'r')
        await guild.system_channel.send("Thanks the for the invite!!!!")
        await guild.system_channel.send(f.read())

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if before.guild.id not in self.disabled.values():

            if after.status == disnake.Status('online') and after.status != before.status:
                print('Hello!')
                guild = self.bot.get_guild(after.guild.id)
                await guild.system_channel.send(f'Hello {after.name}')

            elif after.status == disnake.Status('offline') and after.status != before.status:
                print(f'See ya!')
                guild = self.bot.get_guild(after.guild.id)
                await guild.system_channel.send(f'See you later {after.name}!')

            elif after.status == disnake.Status('idle') and after.status != before.status:
                print(f"WE'RE WAITING!!!!")
                guild = self.bot.get_guild(after.guild.id)
                await guild.system_channel.send(f"COME BACK {after.name}!!!!")

            elif before.status == disnake.Status('idle') and after.status == disnake.Status('online') and \
                    after.status != before.status:
                print(f"Welcome Back!!!!")
                guild = self.bot.get_guild(after.guild.id)
                await guild.system_channel.send(f"Welcome Back {after.name}!!!!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            print('Welcome!')

    @commands.command()
    async def disable(self, ctx):
        self.disabled[ctx.guild] = ctx.guild.id
        print('Cog Removed')


def setup(bot):
    bot.add_cog(Greeting(bot))
