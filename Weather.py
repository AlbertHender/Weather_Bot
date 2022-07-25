import os

import disnake
from disnake.ext import commands, tasks
import requests
import json
from datetime import datetime
from dotenv import load_dotenv


class Weather(commands.Cog):

    def __init__(self, bot):
        load_dotenv('config.env')
        self.bot = bot
        self.city = {}
        self.key = os.getenv('WEATHER')
        self.furl = {}
        self.days = 1
        self.guilds = {}
        self.dailyForecast.start()

    @commands.command()
    async def setCity(self, ctx, *, city):
        self.city[ctx.guild.id] = city
        self.furl[ctx.guild.id] = 'http://api.weatherapi.com/v1/forecast.json?key=' \
                                  '{}&q={}&days={}'.format(self.key, self.city[ctx.guild.id], self.days)
        self.guilds[ctx.guild.id] = ctx
        print(f"City is now {city}")

    @commands.command()
    async def superior(self, ctx):
        print(self.city[ctx.guild.id] + ' superior')
        guild = ctx.guild
        channel_id = ctx.channel.id
        channel = await guild.fetch_channel(channel_id)
        await channel.send(self.city[ctx.guild.id] + ' is the best city!!!')

    @commands.command()
    async def forecast(self, ctx, days):
        data = await self.getForecastInfo(ctx=ctx, days=days)

        if data is None:
            return

        intro = 'The forecast for the next {} days in {} is....'.format(days, self.city[ctx.guild.id])
        data = data['forecast']['forecastday']
        guild = ctx.guild
        channel_id = ctx.channel.id
        channel = await guild.fetch_channel(channel_id)
        await channel.send(intro)

        for i in data:
            highlight = "@here "
            forecast_imp = '{} can be expected to have a max temperature of {}F and a minimum temperature of {}F with ' \
                           'predicted conditions being {}'.format(i['date'],
                                                                  i['day']['maxtemp_f'], i['day']['mintemp_f'],
                                                                  i['day']['condition']['text']) + "\n"

            forecast_met = "\n" + 'And for those using the inferior system, you can expect a maximum ' \
                                  'temperature of {}C and a minimum temperature of {}C'.format(i['day']['maxtemp_c'],
                                                                                               i['day'][
                                                                                                   'mintemp_c']) + "\n"
            await channel.send(highlight + forecast_imp + forecast_met)

    @commands.command()
    async def current(self, ctx):
        data = await self.getCurrentInfo(ctx=ctx)

        if data is None:
            return

        data = data['current']
        guild = ctx.guild
        channel_id = ctx.channel.id
        info = ("It is currently {}F or {}C for those who don't know freedom units and it's also currently {} outside "
                "with " "{}MPH or {}KPH winds here in {}"). \
            format(data['temp_f'], data['temp_c'], data['condition']['text'],
                   data['wind_mph'], data['wind_kph'], self.city[ctx.guild.id])
        channel = await guild.fetch_channel(channel_id)
        await channel.send(info)

    async def getCurrentInfo(self, ctx):
        correct = await self.cityCheck(ctx=ctx)
        if not correct:
            return None

        return requests.get(self.furl[ctx.guild.id]).json()

    async def getForecastInfo(self, ctx, days):
        correct = await self.cityCheck(ctx=ctx)
        if not correct:
            return None

        self.days = days
        self.furl[ctx.guild.id] = 'http://api.weatherapi.com/v1/forecast.json?key=' \
                                  '{}&q={}&days={}'.format(self.key, self.city[ctx.guild.id], self.days)
        self.days = 1
        data = requests.get(self.furl[ctx.guild.id]).json()
        return data

    async def cityCheck(self, ctx):
        if ctx.guild.id not in self.city:
            print("City not set")

            async def sendMistake(cx):
                channel = await cx.guild.fetch_channel(cx.channel.id)
                await channel.send('City not set yet!')

            await sendMistake(cx=ctx)
            return False

        elif requests.get(self.furl[ctx.guild.id]).status_code >= 400:
            print('Invalid city name')

            async def sendMistake(cx):
                channel = await cx.guild.fetch_channel(cx.channel.id)
                await channel.send('The city name you entered is invalid')

            await sendMistake(cx=ctx)
            return False

        else:
            return True

    async def rundown(self, ctx):
        correct = await self.cityCheck(ctx=ctx)
        if not correct:
            return None

        data = await self.getForecastInfo(ctx, days=1)
        data = data['forecast']['forecastday'][0]['hour']
        guild = ctx.guild
        chanel_id = ctx.channel.id
        channel = await guild.fetch_channel(chanel_id)
        hours = ''
        for i in data[6:]:
            day = '({}, {}, {}, {}),'.format(i['time'], i['temp_f'], i['temp_c'], i['condition']['text']) + "\n"
            hours += day
        await channel.send(hours)

    @tasks.loop(seconds=1)
    async def dailyForecast(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time >= '07:00:00' or current_time <= '7:00:00':
            for i in self.guilds.values():
                await self.rundown(ctx=i)


def setup(bot):
    bot.add_cog(Weather(bot))
