import discord
from discord.ext import commands, tasks
from utilities.qotd import enable_qotd, get_question, get_channels
import datetime


class QotdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_qotd.start()

    @commands.command()
    async def enable_qotd(self, ctx: commands.Context):
        """Enable the question of the day message in the channel this command is sent"""
        guild = ctx.guild.id
        channel_id = ctx.channel.id
        await enable_qotd(channel_id)

    @tasks.loop(time=[datetime.time(12, 2, 0)])
    async def send_qotd(self):
        """sends the question of the day to the enabled servers every day at UTC time"""
        question = get_question()
        channel_ids = get_channels()
        for channel_id in channel_ids:
            channel = self.bot.get_channel(int(channel_id))
            if channel is not None:
                await channel.send(question)
