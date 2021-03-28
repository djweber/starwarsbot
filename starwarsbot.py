import os
import sqlite3

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.command()
async def planet(ctx, arg):
    r = requests.get("https://swapi.dev/api/planets/?search={0}".format(arg))
    await ctx.send(r.json())


bot.run(os.environ["DISCORD_TOKEN"])
