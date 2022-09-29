import discord
from discord.ext import commands
import re
import asyncio


class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["reminders", "reminder", "remindme"])
    async def remind(self, ctx: commands.Context, time_string, *reminder_text):
        """Bingobot will @ you in the channel this is used after the time specified.
         uses s, m , h, d... to format time"""
        reminder_text = ' '.join(reminder_text)
        time_string = time_string.lower()

        def calc_time(time_stringy):
            split_string = re.split("(?<=\\D)(?=\\d)|(?<=\\d)(?=\\D)", time_stringy)
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24, "w": 3600 * 24 * 7, "mo": 3600 * 24 * 28,
                         "y": 3600 * 24 * 356.25}

            total_seconds = 0
            a = iter(split_string)
            for num, multiplier in zip(a, a):
                total_seconds += float(num) * time_dict[multiplier]

            return total_seconds

        time_to_wait = calc_time(time_string)

        await ctx.reply(f"Waiting **{time_string}** to remind you about: **{reminder_text}**")
        await asyncio.sleep(time_to_wait)
        await ctx.send(f"{ctx.author.mention} This is your reminder about **{reminder_text}**!")

