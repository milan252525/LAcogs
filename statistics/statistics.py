import discord
from redbot.core import commands, Config, checks
import asyncio
import brawlstats

class Statistics(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=42424242)
        default_guild = {"tags": []}
        self.config.register_guild(**default_guild)

    async def initialize(self):
        ofcbsapikey = await self.bot.get_shared_api_tokens("ofcbsapi")
        if ofcbsapikey["api_key"] is None:
            raise ValueError("The Official Brawl Stars API key has not been set.")
        self.ofcbsapi = brawlstats.OfficialAPI(ofcbsapikey["api_key"], is_async=True)

    @commands.command()
    @commands.guild_only()
    async def addclub(self, ctx, tag : str):
        await ctx.trigger_typing()

        tag = tag.lower().replace('O', '0')
        if tag.startswith("#"):
            tag = tag.strip('#')

        try:
            club = await self.ofcbsapi.get_club(tag)
            await self.config.guild(ctx.guild).tags.set(tag)
            await ctx.send(embed=discord.Embed(description=f"Club {club.name} successfully added.", color=discord.Colour.blue()))

        except brawlstats.errors.NotFoundError:
            await ctx.send(embed=discord.Embed(description="No club with this tag found.", color=discord.Colour.red()))

        except brawlstats.errors.RequestError as e:
            await ctx.send(embed=discord.Embed(f"BS API is offline, please try again later! ({str(e)})", color=discord.Colour.red()))

        except Exception as e:
            await ctx.send(f"**Something went wrong, please send a personal message to LA Modmail bot or try again!**** ({str(e)})")

    @commands.command()
    @commands.guild_only()
    async def removeclub(self, ctx, tag : str):
        await ctx.trigger_typing()

        tag = tag.lower().replace('O', '0')
        if tag.startswith("#"):
            tag = tag.strip('#')

        try:
            entry = await self.config.guild(ctx.guild).clubs.get_raw(tag)
            await self.config.guild(ctx.guild).tags.clear_raw(entry)
            await ctx.send(embed=discord.Embed(description=f"Club {club.name} successfully removed.", color=discord.Colour.blue()))
        except KeyError:
            await ctx.send(embed=discord.Embed(description=f"{tag} isn't saved in this server.", color=discord.Colour.red()))

    @commands.command()
    async def clubtags(self, ctx):
        await ctx.trigger_typing()

        tags = await self.config.guild(ctx.guild).clubs.get_raw(tag)

        await ctx.send(tags)