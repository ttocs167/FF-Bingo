import discord
from discord.ext import commands
import time
import asyncio
from os.path import exists
import urllib
import re
import pafy
import glob
import os
import queue


def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match


class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Q = queue.Queue()
        self.vc = None
        self.source = None
        self.paused = False
        self.skip = False
        self.now_playing = None

    @commands.hybrid_command(name="sound")
    async def play_soundbite(self, ctx: commands.Context, args):
        """plays a soundbite in the current channel you're in."""
        if not exists('resources/audio_clips/' + args + '.mp3'):
            return

        if ctx.message.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command!")
            return

        voice_channel = ctx.author.voice.channel

        if self.vc is not None and self.vc.is_playing():
            await ctx.reply("The bot is already playing audio!", ephemeral=True)
            return

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
        if ctx.interaction:
            await ctx.interaction.response.send_message("sound sent!", ephemeral=True)

    @commands.hybrid_command()
    async def soundlist(self, ctx: commands.Context):
        """Lists the available soundbites to play with the /sound command."""
        available_files = glob.glob('resources/audio_clips/*.mp3')
        filenames = []
        for filename in available_files:
            filenames.append(os.path.basename(filename)[:-4])

        out = '\n'.join(sorted(filenames))
        if ctx.interaction:
            await ctx.interaction.response.send_message(out, ephemeral=True)
        else:
            await ctx.reply(out)

    @commands.command(name="addsong")
    async def queue_song(self, ctx: commands.Context, *, args):
        """Adds a song via YouTube url or search to the queue"""
        search = args.replace(" ", "+")

        if youtube_url_validation(search):
            html = urllib.request.urlopen(search)
        else:
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        first_result = video_ids[0]

        self.Q.put(first_result)
        await ctx.message.edit(suppress=True)
        await ctx.reply("{} Added new video to queue: https://www.youtube.com/watch?v={}".format(ctx.author.mention,
                                                                                                 first_result))

    @commands.command(name='playsongs', hidden=True)
    async def play_queue(self, ctx: commands.Context):

        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn -filter:a "volume=0.5"'}

        if ctx.message.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command!")
            return

        voice_channel = ctx.author.voice.channel
        if voice_channel is not None and not self.Q.empty():
            try:
                self.vc = await voice_channel.connect()
            except TimeoutError:
                await ctx.reply("connection to voice channel timed out")
                return

        def play_from_queue():
            video_id = self.Q.get()

            song = pafy.new(video_id)  # creates a new pafy object

            self.now_playing = song.title

            audio = song.getbestaudio()  # gets an audio source

            # converts the youtube audio source into a source discord can use
            self.source = discord.FFmpegPCMAudio(audio.url, **ffmpeg_options)
            self.vc.play(self.source)  # play the source

        while not self.Q.empty():
            self.skip = False
            play_from_queue()
            await ctx.send("now playing: {}".format(self.now_playing))

            while self.vc.is_playing() or self.paused:
                if self.skip:
                    break
                await asyncio.sleep(.1)

        if self.vc is not None and not self.paused:
            self.now_playing = None
            await self.vc.disconnect()

    @commands.command()
    async def kick_bot(self, ctx: commands.Context):
        """removes the bot from the channel and empties the song queue"""
        if self.vc is not None:
            self.vc.stop()
        self.paused = False
        self.now_playing = None
        self.Q.queue.clear()
        await self.vc.disconnect()

    @commands.command(aliases=["play, resume"])
    async def pause(self, ctx: commands.Context):
        """pauses the currently playing audio"""
        if self.vc is not None:
            if self.vc.is_playing():
                self.paused = True
                self.vc.pause()
            else:
                self.paused = False
                self.vc.play(self.source)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """skips the current playing song"""
        if self.vc is not None:
            self.vc.pause()
            self.skip = True
            self.paused = False

    @commands.command(aliases=["clearqueue"])
    async def clear_queue(self, ctx: commands.Context):
        if self.vc is not None:
            self.vc.stop()
        self.Q.queue.clear()
        self.now_playing = None

    @commands.command()
    async def now_playing(self, ctx: commands.Context):
        await ctx.reply(self.now_playing)
