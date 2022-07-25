from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import Weather
import greeting
import help
import os

load_dotenv('config.env')
file = os.getenv('DISCORD')
token = file
intents = disnake.Intents.all()

cogs = [greeting, Weather, help]
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
for i in cogs:
    i.setup(bot)


@bot.event
async def on_ready():
    game = disnake.Game('Flying')
    await bot.change_presence(activity=game)
    print('Logged in')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        channel = await ctx.guild.fetch_channel(ctx.channel.id)
        await channel.send("Not a valid command")
        print("Invalid command")
        return
    raise error


bot.run(token)
