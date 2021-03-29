import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="?")

cache = {}


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.group(name="sw")
async def starwars(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid subcommand")


@starwars.command()
async def planet(ctx, query: str):

    url = "https://swapi.dev/api/planets/?search={0}"

    r = requests.get(url.format(query))

    if r.status_code != 200:
        embed = discord.Embed(
            title="Oh dear, an error!",
            description="An error occurred",
            color=0xFFD700,
        )
        embed.set_thumbnail(
            url="https://lh3.googleusercontent.com/proxy/g57Bu8-Xrioz3rqRgnS9rD2i4nZQylt_irFShi5zCkshKiMoamlxAPx1iKkTx_hyiJZUdhGAMUBQG0oq_TbfRz7ChTz6mAgC"
        )
        await ctx.send(embed=embed)
        return

    results = r.json()["results"]

    if len(results) == 0:
        embed = discord.Embed(
            title="I find your lack of results disturbing...",
            description="No results found for search: `{0}`".format(query),
            color=0xEB212E,
        )
        embed.set_thumbnail(
            url="https://64.media.tumblr.com/tumblr_m9wotokOFJ1rfjowdo1_500.gifv"
        )
        await ctx.send(embed=embed)
        return

    # Handle a set of planet results
    if len(results) > 1:
        description = "```\n"
        for result in results:
            description += "{0}\n".format(result["name"])
        description += "```\n"

        embed = discord.Embed(
            title="Found, planets were!",
            description=description,
            color=0x2FF924,
        )
        embed.set_thumbnail(
            url="https://64.media.tumblr.com/tumblr_m9xumc3nlt1rfjowdo1_500.gifv"
        )

        await ctx.send(embed=embed)
        return

    # Handle a single planet
    result = results[0]

    url = result["url"]

    embed = discord.Embed(
        title="Found, a planet was!",
        description="",
        color=0x2FF924,
    )
    embed.set_thumbnail(
        url="https://64.media.tumblr.com/tumblr_m9xumc3nlt1rfjowdo1_500.gifv"
    )

    embed.add_field(name="Name", value="`{0}`".format(result["name"]))
    embed.add_field(name="Population", value="`{0}`".format(result["population"]))
    embed.add_field(
        name="Rotation Period", value="`{0}`".format(result["rotation_period"])
    )
    embed.add_field(
        name="Orbital Period", value="`{0}`".format(result["orbital_period"])
    )
    embed.add_field(name="Diameter", value="`{0}`".format(result["diameter"]))
    embed.add_field(name="Climate", value="`{0}`".format(result["climate"]))
    embed.add_field(name="Gravity", value="`{0}`".format(result["gravity"]))
    embed.add_field(name="Terrain", value="`{0}`".format(result["terrain"]))
    embed.add_field(name="Surface Water", value="`{0}`".format(result["surface_water"]))

    residents_value = "```\n"

    # Get list of residents
    for resident_url in result["residents"]:
        resident = None

        if resident_url in cache:
            print("Resident already cached: {0}".format(resident_url))
        else:
            resident_result = requests.get(resident_url)
            print("Resident not cached. Caching with key {0}".format(resident_url))
            cache[resident_url] = resident_result.json()

        resident = cache[resident_url]

        residents_value += "{0}\n".format(resident["name"])

    residents_value += "```\n"

    embed.add_field(name="Residents", value=residents_value)

    films_value = "```\n"

    # Get list of movies
    for film_url in result["films"]:
        film = None

        if film_url in cache:
            print("Film already cached: {0}".format(film_url))
        else:
            film_result = requests.get(film_url)
            print("Film not cached. Caching with key {0}".format(film_url))
            cache[film_url] = film_result.json()

        film = cache[film_url]

        films_value += "{0}\n".format(film["title"])

    films_value += "```\n"

    embed.add_field(name="Films", value=films_value)

    await ctx.send(embed=embed)


bot.run(os.environ["DISCORD_TOKEN"])
