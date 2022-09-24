import discord
from discord.ext import commands, tasks
from utilities.qotd import enable_qotd, get_todays_question, disable_qotd
import datetime
import shelve


class QotdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_qotd.start()

    @commands.command()
    async def enable_qotd(self, ctx: commands.Context):
        """Enable the question of the day message in the channel this command is sent"""
        channel_id = ctx.channel.id
        await enable_qotd(channel_id)
        await ctx.reply("_Question of the day has been enabled in this channel!_")

    @commands.command()
    async def disable_qotd(self, ctx: commands.Context):
        """disables the question of the day message in the channel this command is sent"""
        channel_id = ctx.channel.id
        await disable_qotd(channel_id)
        await ctx.reply("_Question of the day has been disabled in this channel!_")

    @tasks.loop(time=[datetime.time(11, 0, 0)])
    async def send_qotd(self):
        """sends the question of the day to the enabled servers every day at UTC time"""

        s = shelve.open('qotd.db')
        try:
            s['day_index'] += 1
        except KeyError:
            s['day_index'] = 0

        new_pin_ids = []
        try:
            old_pin_ids = s['old_pin_ids']
        except KeyError:
            old_pin_ids = []
            s['old_pin_ids'] = []

        question = get_todays_question(s)
        channel_ids = s['enabled_channels']

        for channel_id_msg_pair in old_pin_ids:
            channel_id = int(channel_id_msg_pair[0])
            msg_id = int(channel_id_msg_pair[1])

            channel = self.bot.get_channel(channel_id)
            old_msg = await channel.fetch_message(msg_id)
            await old_msg.unpin()

        for channel_id in channel_ids:
            channel = self.bot.get_channel(int(channel_id))
            if channel is not None:
                msg = await channel.send(question)
                await msg.pin()
                new_pin_ids.append([channel_id, msg.id])

        s['old_pin_ids'] = new_pin_ids

        s.close()

    @commands.command()
    async def force_qotd(self, ctx: commands.Context):
        """forces the question of the day to be sent in this channel"""
        s = shelve.open('qotd.db')
        question = get_todays_question(s)
        s.close()
        await ctx.reply(question)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def set_qotd(self, ctx: commands.Context, index: int):
        s = shelve.open('qotd.db')
        try:
            s['day_index'] = index
        finally:
            s.close()

    @commands.command()
    @commands.is_owner()
    async def pin_test(self, ctx: commands.Context):
        msg = await ctx.send("this message is pinned")
        await msg.pin()
        print(msg.id)


