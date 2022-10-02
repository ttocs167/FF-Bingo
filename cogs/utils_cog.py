import discord
from discord.ext import commands
import re
import asyncio
import datetime


class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["reminders", "reminder", "remindme"])
    async def remind(self, ctx: commands.Context, time_string, *reminder_text):
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
                                  f"** to remind you about: **{reminder_text}**")
        await asyncio.sleep(time_to_wait)

        cache_message = await ctx.fetch_message(message.id)  # this returns an up to date version of the message

        users = set()
        for reaction in cache_message.reactions:
            async for user in reaction.users():
                users.add(user)

        await ctx.send(f"{ctx.author.mention} This is your reminder about **{reminder_text}**!\n"
                       f"{', '.join(user.mention for user in users)}")

