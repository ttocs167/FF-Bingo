import discord
from discord.ext import commands, tasks


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='role')
    async def give_role(self, ctx: commands.Context, *, role_name):
        """Use this to give yourself a role! (can only gives roles lower rank than the bot."""
        user = ctx.message.author  # user

        # await ctx.send("""Attempting to Verify {}""".format(user))
        try:
            await user.add_roles(discord.utils.get(user.guild.roles, name=role_name))  # add the role
        except Exception as e:
            await ctx.send('There was an error running this command ' + str(e))  # if error
        else:
            await ctx.send("""Giving Role: {} to user {}""".format(role_name, user))  # no errors, say verified

    @commands.command(hidden=True)
    async def get_guild(self, ctx: commands.Context):
        """returns the name of the guild this command was used in"""
        current_guild = str(ctx.guild)
        await ctx.reply(current_guild)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def clean_messages(self, ctx: commands.Context):
        def is_bot(m):
            return m.author == self.bot.user

        deleted = await ctx.channel.purge(limit=100, check=is_bot)
        await ctx.channel.send(f'Deleted {len(deleted)} message(s)')
