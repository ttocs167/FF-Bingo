import discord
from discord.ext import commands, tasks
from utilities.qotd import enable_qotd, get_todays_question, disable_qotd, shuffle_in_new_question, shuffle_future_questions, get_remaining_questions_count
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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def increment_qotd(self, ctx: commands.Context):
        s = shelve.open('qotd.db')
        try:
            s['day_index'] += 1
        finally:
            s.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def decrement_qotd(self, ctx: commands.Context):
        s = shelve.open('qotd.db')
        try:
            s['day_index'] -= 1
        finally:
            s.close()

    @commands.command(aliases=['remaining_questions'])
    async def questions_remaining(self, ctx: commands.Context):
        s = shelve.open('qotd.db')
        try:
            questions_remaining = get_remaining_questions_count(s)
            await ctx.reply("There are **{}** questions remaining!".format(questions_remaining))
        finally:
            s.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shuffle_future_questions(self, ctx: commands.Context):
        s = shelve.open('qotd.db')
        shuffle_future_questions(s)
        s.close()
        await ctx.reply("_Shuffled future questions!_")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def addq_admin(self, ctx: commands.Context, *, new_q):
        s = shelve.open('qotd.db')

        shuffle_in_new_question(s, new_q)

        s.close()
        await ctx.reply("__Shuffled in new question__ **{}** __ to the list of future questions!__".format(new_q))

    @commands.command()
    async def addqotd(self, ctx: commands.Context, *, new_q):

        yay_voters = set()
        nay_voters = set()

        yay_button = discord.ui.Button(label="", emoji="✔",
                                       style=discord.ButtonStyle.green)

        nay_button = discord.ui.Button(label="", emoji="❌",
                                       style=discord.ButtonStyle.grey)

        async def vote_yay(interaction: discord.Interaction):
            if interaction.user not in yay_voters:
                yay_voters.add(interaction.user)

                await interaction.response.send_message("You voted **yay**", ephemeral=True)

                if interaction.user in nay_voters:
                    nay_voters.remove(interaction.user)

                await check_votes(interaction)
            else:
                await interaction.response.send_message("You have already voted **yay**!", ephemeral=True)
                return

        async def vote_nay(interaction: discord.Interaction):
            if interaction.user not in nay_voters:
                nay_voters.add(interaction.user)

                await interaction.response.send_message("You voted **nay**", ephemeral=True)

                if interaction.user in yay_voters:
                    print("removing user from yay")
                    yay_voters.remove(interaction.user)

                await check_votes(interaction)
            else:
                await interaction.response.send_message("You have already voted **nay**!", ephemeral=True)
                return

        async def check_votes(interaction: discord.Interaction):
            yay_votes = len(yay_voters)
            nay_votes = len(nay_voters)

            await vote.edit(content="VOTE: Add **{}** to the list of possible qotd's?\n"
                            "_A 3 vote difference is needed for this to succeed_\n"
                            "{} Yay votes : {} Nay votes".format(new_q, yay_votes, nay_votes), view=view)

            if yay_votes - 2 > nay_votes:
                s = shelve.open('qotd.db')

                shuffle_in_new_question(s, new_q)

                s.close()

                await interaction.followup.send("_Shuffled in new question_ **{}** _"
                                                " to the list of future questions!_".format(new_q))

                yay_button.disabled = True
                nay_button.disabled = True
                await vote.edit(view=view)

        yay_button.callback = vote_yay
        nay_button.callback = vote_nay

        view = discord.ui.View(timeout=None)
        view.add_item(yay_button)
        view.add_item(nay_button)

        vote = await ctx.send("VOTE: Add **{}** to the list of possible qotd's?\n"
                              "_A 3 vote difference is needed for this to succeed_\n"
                              "{} Yay votes : {} Nay votes".format(new_q, len(yay_voters),
                                                                   len(nay_voters)), view=view)
