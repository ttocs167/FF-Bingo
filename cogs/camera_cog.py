import discord
from discord.ext import commands

try:
    from utilities import webcam_photo, picam_photo
except:
    print("could not import picam module")


class CamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="plant", hidden=False)
    async def webcam_image(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply("Sorry, the plants are away for winter! But don't worry, we'll be back next year"
                            " :slight_smile:")
        #     image_path = await picam_photo.take_image()
        #     img = discord.File(image_path)
        # await ctx.reply("", file=img)
