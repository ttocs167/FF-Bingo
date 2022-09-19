import discord
from discord.ext import commands
import time


class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play_soundbite(self, ctx: commands.Context, args):
        voice_channel = ctx.author.voice.channel
        if voice_channel is not None:
            vc = await voice_channel.connect()
            print("playing voice clip: " + args)
            vc.play(discord.FFmpegPCMAudio('resources/audio_clips/args.mp3'), after=lambda e: print('done', e))
            while vc.is_playing():
                time.sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
