from discord.ext import commands
import discord
try:
    from utilities.maps_solver import get_closest_match
except ImportError:
    print("could not import scipy packages for map solver. Maps command will be unavailable")


class MapsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='maps')
    async def map_solver(self, ctx, *, expac=""):
        """attempts to find the location of a treasure map image. Give expansion for a limited search eg. $maps ew"""
        filepath = None
        for attachment in ctx.message.attachments:
            filepath = "resources/images/maps/temp.png"
            await attachment.save(filepath)

        best_match, coords = get_closest_match(filepath, expac)
        img = discord.File(best_match)
        await ctx.send("closest match: " + str(coords), file=img)
