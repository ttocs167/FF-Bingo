import discord
from discord.ext import commands
import time
from os.path import exists


class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sound")
    async def play_soundbite(self, ctx: commands.Context, args):

        if not exists('resources/audio_clips/' + args + '.mp3'):
            return

        if ctx.message.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command!")
            return

        voice_channel = ctx.author.voice.channel
        if voice_channel is not None:
            try:
                vc = await voice_channel.connect()
            except TimeoutError:
                await ctx.reply("connection to voice channel timed out")
                return
            print("playing voice clip: " + args)
            vc.play(discord.FFmpegPCMAudio('resources/audio_clips/' + args + '.mp3', options='-filter:a "volume=0.5"'),
                    after=lambda e: print('done', e))
            while vc.is_playing():
                time.sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
