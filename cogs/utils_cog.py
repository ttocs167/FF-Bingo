import discord
from discord.ext import commands
import re
import asyncio
import datetime
from dateutil import parser


class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["timers", "time"])
    async def timer(self, ctx: commands.Context, time_string, *reminder_text):
        """Bingobot will @ you in the channel this is used after the time specified.
        uses s, m , h, d... to format time. Accepts any combination with or without spaces.
        Also accepts 'second(s)', 'minute(s)', 'hour(s)', 'day(s)' etc...

        Reacting to the bot's initial response will also add you to the list of people
        mentioned when the timer elapses"""

        reminder_text = ' '.join(reminder_text)
        time_string = time_string.lower()

        def calc_time(time_stringy):
            split_string = re.split("(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)", time_stringy)
            time_dict = {"s": 1,
                         "second": 1,
                         "seconds": 1,
                         "secs": 1,
                         "m": 60,
                         "mins": 60,
                         "min": 60,
                         "minute": 60,
                         "minutes": 60,
                         "h": 3600,
                         "hour": 3600,
                         "hours": 3600,
                         "d": 3600 * 24,
                         "day": 3600 * 24,
                         "days": 3600 * 24,
                         "w": 3600 * 24 * 7,
                         "week": 3600 * 24 * 7,
                         "weeks": 3600 * 24 * 7,
                         "mo": 3600 * 24 * 28,
                         "month": 3600 * 24 * 28,
                         "months": 3600 * 24 * 28,
                         "y": 3600 * 24 * 356.25,
                         "year": 3600 * 24 * 356.25,
                         "years": 3600 * 24 * 356.25,
                         }

            total_seconds = 0
            a = iter(split_string)
            for num, multiplier in zip(a, a):
                total_seconds += float(num) * time_dict[multiplier]

            return total_seconds

        time_to_wait = calc_time(time_string)

        message = await ctx.reply(f"Waiting **{str(datetime.timedelta(seconds=time_to_wait))}"
                                  f"** to remind you about: **{reminder_text}**\n"
                                  f"_Others can react to this message to be mentioned when the timer is up._")
        await asyncio.sleep(time_to_wait)

        cache_message = await ctx.fetch_message(message.id)  # this returns an up to date version of the message

        users = set()
        for reaction in cache_message.reactions:
            async for user in reaction.users():
                users.add(user)

        await ctx.send(f"{ctx.author.mention} This is your reminder about **{reminder_text}**!\n"
                       f"{', '.join(user.mention for user in users)}")

    @commands.command(aliases=["reminders", "reminder", "remindme"])
    async def remind(self, ctx: commands.Context, *, time_string):
        """Bingobot will @ you in the channel this is used at the time specified.
        The time can be formatted in any standar way, just be consistent.

        Reacting to the bot's initial response will also add you to the list of people
        mentioned when the timer elapses"""

        time_string = time_string.lower()

        try:
            time_of_alarm, tokens = parser.parse(time_string, fuzzy_with_tokens=True)
        except parser.ParserError:
            await ctx.reply("Sorry, I can't parse that message into a time.")
            return

        time_to_wait = (time_of_alarm - datetime.datetime.now()).seconds

        if time_to_wait < 0:
            time_to_wait += 86400  # if time is negative then the user probably means tomorrow at that time

        if time_to_wait < 0:  # if the time is still negative then the requested time is in the past
            await ctx.reply("You cannot set a timer in the past!")
            return

        reminder_text = max(tokens, key=len)

        message = await ctx.reply(f"Waiting **{str(datetime.timedelta(seconds=time_to_wait))}"
                                  f"** to remind you about: **{reminder_text}**\n"
                                  f"_Others can react to this message to be mentioned when the reminder is up._")
        await asyncio.sleep(time_to_wait)

        cache_message = await ctx.fetch_message(message.id)  # this returns an up to date version of the message

        users = set()
        for reaction in cache_message.reactions:
            async for user in reaction.users():
                users.add(user)

        await ctx.send(f"{ctx.author.mention} This is your reminder about **{reminder_text}!**\n"
                       f"{', '.join(user.mention for user in users)}")
