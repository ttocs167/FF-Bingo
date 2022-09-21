import discord
from discord.ext import commands
import time
from os.path import exists
import urllib
import re
import pafy
import glob
import os


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
            # vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.5)
            print("playing voice clip: " + args)
            vc.play(discord.FFmpegPCMAudio('resources/audio_clips/' + args + '.mp3', options='-filter:a "volume=0.3"'),
                    after=lambda e: print('done', e))
            while vc.is_playing():
                time.sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")

    @commands.command()
    async def soundlist(self, ctx: commands.Context):
        available_files = glob.glob('resources/audio_clips/*.mp3')
        filenames = []
        for filename in available_files:
            filenames.append(os.path.basename(filename)[:-4])

        out = '\n'.join(filenames)
        await ctx.reply(out)

    @commands.command(name='soundurl')
    async def play_sound_from_url(self, ctx: commands.Context, args):
        search = args
        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn -filter:a "volume=0.5"'}

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

        search = search.replace(" ", "+")

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        # await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

        song = pafy.new(video_ids[0])  # creates a new pafy object

        audio = song.getbestaudio()  # gets an audio source

        source = discord.FFmpegPCMAudio(audio.url,
                                        **ffmpeg_options)  # converts the youtube audio source into a source discord can use

        vc.play(source)  # play the source
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()


