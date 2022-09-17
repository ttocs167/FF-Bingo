import os
import discord
from discord.ext import commands
from utilities import utils
from utilities import analyser


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="yolo", hidden=True)
    async def yolo_detect(self, ctx):
        url = ctx.message.attachments[0].url

        image_path = utils.yolo_response(url)
        img = discord.File(image_path)
        await ctx.reply("", file=img)

    @commands.command()
    async def teanalyse(self, ctx, *, report_id):
        """Gives statistics on FF logs reports from The Epic of Alexander. Requires log URL"""
        api_key = os.getenv('FFLOGS_API_KEY')
        if api_key is None:
            await ctx.send("Command is not currently configured on")
            return
        message = analyser.analyse_tea_fight(report_id, api_key)

        if message is None:
            await ctx.send("No TEA fights found")
            return
        await ctx.send(message)

    @commands.command()
    async def uwunalyse(self, ctx, *, report_id):
        """Gives statistics on FF logs reports from the Weapon's Refrain (Ultimate). Requires log URL"""
        api_key = os.getenv('FFLOGS_API_KEY')
        if api_key is None:
            await ctx.send("Command is not currently configured on")
            return
        message = analyser.analyse_uwu_fight(report_id, api_key)

        if message is None:
            await ctx.send("No UWU fights found")
            return
        await ctx.send(message)
