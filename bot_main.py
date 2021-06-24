import os
import discord
from discord.ext import commands
from generate_cards import generate_card
from dotenv import load_dotenv
import utils
import inspect
import time
import asyncio

load_dotenv()
description = '''A Bot for Bingo! All hail BingoBot'''
intents = discord.Intents.default()


async def regenerate_images(index, guild):
    await generate_card(index, guild)


async def regenerate_all_images(guild):
    await generate_card(0, guild, 5)
    print("ALL CARDS IN " + guild + " REGENERATED")


async def regenerate_big_images(index, guild):
    await generate_card(index, guild, x_cells=7, y_cells=7, beeg=True, free_x=3, free_y=3)


async def regenerate_all_big_images(guild):
    await generate_card(0, guild, 5, x_cells=7, y_cells=7, beeg=True, free_x=3, free_y=3)
    print("ALL BIG CARDS IN " + guild + " REGENERATED")


class Bot(commands.Bot):

    def __init__(ctx):

        super().__init__(command_prefix='$', description=description, intents=intents,
                         help_command=commands.DefaultHelpCommand(width=160, no_category="General"))

        ctx.generate_refresh_bools()

        Bot.time_of_last_bingo = time.time()
        Bot.rolling_index = 0
        Bot.rigged_statement = None
        Bot.refresh_bools = {}

        members = inspect.getmembers(ctx)
        for name, member in members:
            if isinstance(member, commands.Command):
                if member.parent is None:
                    ctx.add_command(member)

        # Initialise the timed refresh of bingo cards. Refresh occurs once every 30s if new lines have been added
        ctx.loop.create_task(ctx.timed_refresh())

    @staticmethod
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @commands.command(name='8ball')
    async def _ball(ctx):
        """Sends randomly selected 8ball response"""
        if Bot.rigged_statement is not None:
            await ctx.send("_**" + str(Bot.rigged_statement) + "**_")
            Bot.rigged_statement = None
            print("Rigged message sent.")
        else:
            await ctx.send(utils.random_8ball_response())

    @commands.command()
    async def add(ctx, *, line):
        """Adds a new statement to the bingo pool"""
        await ctx.send("New line: \n_" + line + "_ \nAdded to pool!")
        await utils.add_to_list(line, str(ctx.message.guild))
        print("New line: _" + line + "_ Added to pool in " + str(ctx.message.guild) +
              " by " + (str(ctx.message.author)))
        Bot.refresh_bools[str(ctx.guild)] = True

    @commands.command()
    async def freeadd(ctx):
        """Adds a new statement to the bingo free space pool"""
        msg = ctx.message.content
        line = msg.split("$freeadd ", 1)[1]
        await ctx.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line, str(ctx.message.guild))
        print("New line: _" + line + "_ Added to free space pool in " + str(ctx.message.guild) +
              " by " + (str(ctx.message.author)))
        Bot.refresh_bools[str(ctx.guild)] = True

    @commands.command()
    async def bingo(ctx):
        """Sends pre-generated bingo card as reply to command"""
        time_since_last_bingo = time.time() - Bot.time_of_last_bingo
        print(time_since_last_bingo)

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + str(ctx.guild) + '/output_' + str(Bot.rolling_index) + '.jpg')
            await ctx.reply(utils.random_animal_emoji(), file=img)

            await regenerate_images(Bot.rolling_index, ctx.guild)

            print('image generated for ' + str(ctx.guild))

            Bot.rolling_index = (Bot.rolling_index + 1) % 5
            Bot.time_of_last_bingo = time.time()

        else:
            print("bingo command recieved in " + str(ctx.guild) + " too soon to generate!")

    @commands.command()
    async def bigbingo(ctx):
        """Sends a large bingo card as reply to command"""
        time_since_last_bingo = time.time() - Bot.time_of_last_bingo
        print(time_since_last_bingo)

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + str(ctx.guild) + '/big_output_' + str(Bot.rolling_index) + '.jpg')
            await ctx.reply(utils.random_animal_emoji(), file=img)

            await regenerate_big_images(Bot.rolling_index, str(ctx.guild))

            print('Big image generated for ' + str(ctx.guild))

            Bot.rolling_index = (Bot.rolling_index + 1) % 5
            Bot.time_of_last_bingo = time.time()

        else:
            print("Big bingo command recieved in " + str(ctx.guild) + " too soon to generate!")

    @commands.command(name='rig')
    @commands.is_owner()
    async def rig(ctx, *, line):
        """rigs the next 8ball command to be a custom string. Only available to bot owner"""
        await ctx.send("Next message rigged. _Our little secret..._")
        Bot.rigged_statement = line
        print("Next message rigged: " + str(line))

    @rig.error
    async def rig_error(ctx, error):
        """Send this message if the rig command is called by non-owner"""
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Nothing to see here comrade...')

    @commands.command()
    async def refresh(ctx):
        """Regenerate all images. Called automatically on list change"""
        await regenerate_all_images(ctx.guild)
        await ctx.send("Cards refreshed!")

    @commands.command()
    async def bigrefresh(ctx):
        """regenerate all big images"""
        await regenerate_all_big_images(ctx.guild)
        await ctx.send("Big Cards refreshed!")

    @commands.command()
    async def list(ctx):
        """Lists all items in bingo pool. Use the index with the del command."""
        lines = await utils.list_all_lines(ctx.guild)

        for line in lines:
            line = ' '.join(line).lstrip()
            await ctx.send(line, delete_after=20)

    @commands.command()
    async def freelist(ctx):
        """Lists all items in free space pool. Use the index with the freedel command."""
        lines = await utils.list_all_free_lines(ctx.guild)

        for line in lines:
            line = ' '.join(line).lstrip()
            await ctx.send(line, delete_after=20)

    @commands.command(name='del')
    async def delete_line(ctx, index: int):
        """Deletes the line at [index] in the list. Use $list command to view indices"""
        line = await utils.get_line(index, str(ctx.guild))
        await utils.delete_line(index, str(ctx.guild))
        print("deleted line: " + line)
        await ctx.send("deleted line: " + line)

    @commands.command(name='freedel')
    async def delete_free_line(ctx, index: int):
        """Deletes the free line at [index] in the free list. Use $freelist command to view indices"""
        line = await utils.get_free_line(index, str(ctx.guild))
        await utils.delete_free_line(index, str(ctx.guild))
        print("deleted free line: " + line)
        await ctx.send("deleted free line: " + line)

    @commands.command()
    async def resetlist(ctx):
        """Resets the bingo list to default. WARNING: lost lists are unrecoverable"""
        await utils.reset_list(str(ctx.guild))
        await ctx.send("List has been reset to default.")

    @commands.command()
    async def resetfreelist(ctx):
        """Resets the free space bingo list to default. WARNING: lost lists are unrecoverable"""
        await utils.reset_free_list(str(ctx.guild))
        await ctx.send("Free list has been reset to default.")

    @commands.command()
    async def animal(ctx):
        """:frog:"""
        await ctx.reply(utils.random_animal_emoji())

    @commands.command(name='fullrefresh')
    async def full_refresh_all_servers(ctx):
        for guild_name in bot.guilds:
            await regenerate_all_images(str(guild_name))

    async def on_message(self, message):
        """Called every time a message is received. Checks if the server is new, if so folders and lists are created"""
        if not os.path.isdir("lists/" + str(message.guild)):
            os.mkdir("lists/" + str(message.guild))
            await utils.reset_list(str(message.guild))
            await utils.reset_free_list(str(message.guild))

        if not os.path.isdir("output_folder/" + str(message.guild)):
            os.mkdir("output_folder/" + str(message.guild))

        await bot.process_commands(message)

    @staticmethod
    async def timed_refresh():
        """Automatically refreshes bingo card pools for servers if any new lines have been added"""
        while not bot.is_closed():
            for guild_name in Bot.refresh_bools:
                if Bot.refresh_bools[guild_name]:
                    print("automatically regenerating cards in: " + str(guild_name))
                    await regenerate_all_images(guild_name)
                    Bot.refresh_bools[guild_name] = False

            await asyncio.sleep(30)

    @staticmethod
    async def generate_refresh_bools():  # This function generates a dictionary of bools for every server the bot is in
        Bot.refresh_bools = {}
        guilds = bot.guilds
        for i, guild_name in enumerate(guilds):
            Bot.refresh_bools[guild_name] = False


bot = Bot()
bot.run(os.getenv('BINGO_BOT_TOKEN'))