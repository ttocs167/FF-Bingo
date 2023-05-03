import discord
from discord.ext import commands, tasks
import shelve
import datetime

class BirthdaysCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_birthday.start()

    @tasks.loop(time=[datetime.time(0, 0, 10)])
    async def send_birthday(self):
        """Sends a birthday message to the enabled servers if a member of that server has a birthday that day"""

        channel_ids = self.get_enabled_channels()

        birthdays = self.get_todays_birthdays()

        if len(birthdays) == 0:
            return

        for channel_id in channel_ids:
            channel = self.bot.get_channel(int(channel_id))
            if channel is not None:
                for birthday in birthdays:
                    if channel.guild.get_member(birthday) is not None:
                        await channel.send(f"Happy birthday to <@{birthday}>!")

    @staticmethod
    def get_todays_birthdays():
        today = datetime.datetime.today()
        key = str(today.day) + '/' + str(today.month)
        s = shelve.open('birthdays.db')
        try:
            birthdays = s['birthdays']
        except KeyError:
            birthdays = {}
            s['birthdays'] = {}
        try:
            todays_birthdays = birthdays[key]
        except KeyError:
            todays_birthdays = []
        s.close()
        return todays_birthdays


    @staticmethod
    def get_enabled_channels():
        s = shelve.open('birthdays.db')
        try:
            enabled_channels = s['enabled_channels']
        except KeyError:
            enabled_channels = []
            s['enabled_channels'] = []
        s.close()
        return enabled_channels

    @commands.command()
    async def enable_birthdays(self, ctx: commands.Context):
        """Enable the birthday message in the channel this command is sent"""
        channel_id = ctx.channel.id
        self.enable_birthday(channel_id)
        await ctx.reply("_Birthday message has been enabled in this channel!_")

    @staticmethod
    def enable_birthday(channel_id):
        s = shelve.open('birthdays.db')
        try:
            enabled_channels = s['enabled_channels']
        except KeyError:
            enabled_channels = []
            s['enabled_channels'] = []
        if channel_id not in enabled_channels:
            enabled_channels.append(channel_id)
            s['enabled_channels'] = enabled_channels
        s.close()

    @commands.command()
    async def disable_birthdays(self, ctx: commands.Context):
        """Disables the birthday message in the channel this command is sent"""
        channel_id = ctx.channel.id
        self.disable_birthday(channel_id)
        await ctx.reply("_Birthday message has been disabled in this channel!_")

    @staticmethod
    def disable_birthday(channel_id):
        s = shelve.open('birthdays.db')
        try:
            enabled_channels = s['enabled_channels']
        except KeyError:
            enabled_channels = []
            s['enabled_channels'] = []
        if channel_id in enabled_channels:
            enabled_channels.remove(channel_id)
            s['enabled_channels'] = enabled_channels
        s.close()

    @commands.command()
    async def my_birthday(self, ctx: commands.Context, day: int, month: int):
        """Set your birthday with the format 'day month' (e.g. 1 1 for January 1st)"""
        self.set_birthday(ctx.author.id, day, month)
        await ctx.reply("_Your birthday has been set!_")

    @staticmethod
    def set_birthday(user_id, day, month):
        key = str(day) + '/' + str(month)
        s = shelve.open('birthdays.db')
        try:
            birthdays = s['birthdays']
        except KeyError:
            birthdays = {}
            s['birthdays'] = {}

        people = birthdays[key] if key in birthdays else None
        if people is not None:
            if user_id in people:
                return
            else:
                birthdays[key].append(user_id)
        else:
            birthdays[key] = [user_id]

        s['birthdays'] = birthdays
        s.close()