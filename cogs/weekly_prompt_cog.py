import discord
from discord.ext import commands, tasks
import datetime
import shelve


def get_enabled_channels():
    s = shelve.open('weekly_prompt.db')
    try:
        enabled_channels = s['enabled_channels']
    except KeyError:
        s['enabled_channels'] = []
        enabled_channels = []
    finally:
        s.close()
    return enabled_channels


async def enable_weekly_prompt(channel_id: int):
    s = shelve.open('weekly_prompt.db')
    try:
        enabled_channels = s['enabled_channels']
    except KeyError:
        s['enabled_channels'] = []
        enabled_channels = []

    enabled_channels.append(channel_id)
    s['enabled_channels'] = enabled_channels
    s.close()
    return


async def disable_weekly_prompt(channel_id: int):
    s = shelve.open('weekly_prompt.db')
    try:
        enabled_channels = s['enabled_channels']
    except KeyError:
        s['enabled_channels'] = []
        enabled_channels = []

    try:
        enabled_channels.remove(channel_id)
    except ValueError:
        pass
    s['enabled_channels'] = enabled_channels
    s.close()
    return


async def add_weekly_prompt(prompt: str):
    s = shelve.open('weekly_prompt.db')
    try:
        prompts = s['prompts']
    except KeyError:
        s['prompts'] = []
        prompts = []

    prompts.append(prompt)
    s['prompts'] = prompts
    s.close()
    return


def load_day_index():
    s = shelve.open('weekly_prompt.db')
    try:
        day_index = s['day_index']
    except KeyError:
        s['day_index'] = 0
        day_index = 0
    finally:
        s.close()
    return day_index


def set_day_index(day: int):
    s = shelve.open('weekly_prompt.db')
    try:
        s['day_index'] = day
    finally:
        s.close()
    return


def load_whitelist():
    s = shelve.open('weekly_prompt.db')
    try:
        whitelist = s['whitelist']
    except KeyError:
        s['whitelist'] = []
        whitelist = []
    finally:
        s.close()
    return whitelist


def add_user_to_whitelist(user: int):
    s = shelve.open('weekly_prompt.db')
    try:
        whitelist = s['whitelist']
    except KeyError:
        s['whitelist'] = []
        whitelist = []

    whitelist.append(user)
    s['whitelist'] = whitelist
    s.close()
    return


def load_prompts():
    s = shelve.open('weekly_prompt.db')
    try:
        prompts = s['prompts']
    except KeyError:
        s['prompts'] = []
        prompts = []
    finally:
        s.close()

    return prompts


def load_current_prompt_index():
    s = shelve.open('weekly_prompt.db')
    try:
        current_prompt_index = s['current_prompt_index']
    except KeyError:
        s['current_prompt_index'] = 0
        current_prompt_index = 0
    finally:
        s.close()
    return current_prompt_index


def increment_prompt_index():
    s = shelve.open('weekly_prompt.db')
    try:
        s['current_prompt_index'] += 1
    finally:
        s.close()
    return


class WeeklyPromptCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.day_index = load_day_index()
        self.current_day_index = datetime.datetime.today().weekday()
        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.pinned_message_ids = []

        self.send_weekly_prompt.start()

    @tasks.loop(time=[datetime.time(11, 0, 0)])
    async def send_weekly_prompt(self):
        """sends the weekly prompt to the enabled servers every week at UTC time"""
        self.current_day_index = datetime.datetime.today().weekday()
        if self.current_day_index == self.day_index:

            prompts = load_prompts()
            current_prompt_index = load_current_prompt_index()

            prompt = prompts[current_prompt_index]

            enabled_channels = get_enabled_channels()

            for channel_id in enabled_channels:
                channel = self.bot.get_channel(channel_id)
                if channel is not None:

                    # unpin the old message
                    for channel_id_msg_pair in self.pinned_message_ids:
                        if channel_id_msg_pair[0] == channel_id:
                            msg_id = channel_id_msg_pair[1]

                            try:
                                old_msg = await channel.fetch_message(msg_id)
                                await old_msg.unpin()
                            except AttributeError:
                                pass

                    # send the new message and pin it
                    msg = await channel.send(prompt)
                    await msg.pin()
                    self.pinned_message_ids.append([channel_id, msg.id])

            increment_prompt_index()

            return

    @commands.command()
    async def force_weekly_prompt(self, ctx: commands.Context):
        """Force the weekly prompt to be sent"""

        # check that the current channel is in the list of enabled channels
        enabled_channels = get_enabled_channels()
        if ctx.channel.id not in enabled_channels:
            await ctx.reply("_The weekly prompt has not been enabled in this channel_")
            return

        # now we can be sure that the weekly prompt is enabled in this channel

        # load the prompt
        prompts = load_prompts()
        current_prompt_index = load_current_prompt_index()

        prompt = prompts[current_prompt_index]

        # send the prompt
        await ctx.channel.send(prompt)
        
        return

    @commands.command()
    async def enable_weekly_prompt(self, ctx: commands.Context):
        """Enable the weekly prompt message in the channel this command is sent"""
        channel_id = ctx.channel.id

        if channel_id not in get_enabled_channels():

            await enable_weekly_prompt(channel_id)
            await ctx.reply("_Weekly prompt has been enabled in this channel!_")

    @commands.command()
    async def disable_weekly_prompt(self, ctx: commands.Context):
        """disables the weekly prompt message in the channel this command is sent"""
        channel_id = ctx.channel.id
        await disable_weekly_prompt(channel_id)
        await ctx.reply("_Weekly prompt has been disabled in this channel!_")

    @commands.command()
    async def add_weekly_prompt(self, ctx: commands.Context, prompt: str):
        """Add a new weekly prompt to the list of prompts"""

        whitelist = load_whitelist()

        # check if the user is on the whitelist to add prompts

        if ctx.author.id not in whitelist:
            await ctx.reply("_You do not have permission to add a new prompt._")
            return

        await add_weekly_prompt(prompt)

        # delete the message that was sent to hide the prompt
        await ctx.message.delete()

    @commands.is_owner()
    @commands.command()
    async def add_user_to_whitelist(self, ctx: commands.Context, user: discord.User):
        """Add a user to the whitelist of users who can add prompts"""

        add_user_to_whitelist(user.id)

        await ctx.reply(f"_The user {user.mention} has been added to the whitelist!_")

    @commands.command()
    @commands.is_owner()
    async def set_weekly_prompt_day(self, ctx: commands.Context, day: int):
        """Set the day of the week that the weekly prompt will be sent"""

        day = day % 7

        assert 0 < day < 6, "Day must be between 0 and 6"

        # set the day of the week that the prompt will be sent
        self.day_index = day

        set_day_index(day)

        await ctx.reply(f"_The weekly prompt will now be sent on {self.days_of_week[day]}!_")

    @commands.command()
    async def echo_prompt(self, ctx: commands.Context, prompt: str):
        """Echo the prompt to the channel"""

        await ctx.reply(prompt)
        return
