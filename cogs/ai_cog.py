import discord
from discord.ext import commands
import openai
from utilities.openAI_test import get_ai_response, get_ai_pun
import os


class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(aliases=["ai_image", "aiim", "aimage"])
    async def get_dalle_image(self, ctx: commands.Context, *, prompt):
        """Generate a DALLE image based on a prompt!"""
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        await ctx.reply(image_url)

    @commands.command()
    async def ai(self, ctx, *, new_prompt):
        """Get a real AI response from BingoBot!"""
        async with ctx.channel.typing():
            if str(ctx.guild) in os.getenv('GUILD_WHITELIST'):
                author = str(ctx.message.author).split('#')[0]
                response = get_ai_response(new_prompt, author)
                await ctx.reply(response)
            else:
                await ctx.reply("Sorry, this server is not authorised to use the AI function.")

    @commands.command(aliases=["ai_pun"])
    async def aipun(self, ctx: commands.Context, *, pun_prompt):
        """Get a painfully unfunny AI generated pun or joke from BingoBot!"""
        async with ctx.channel.typing():
            if str(ctx.guild) in os.getenv('GUILD_WHITELIST'):
                response = get_ai_pun(pun_prompt)
                await ctx.reply(response)
            else:
                await ctx.reply("Sorry, this server is not authorised to use the AI function.")