import os
import discord
from discord.ext import commands
from utilities.generate_cards import generate_card
from utilities.generate_card_data import generate_card_data
from utilities.html_creator import htmlCreator
from dotenv import load_dotenv
from utilities import utils
from utilities import analyser
import time
import inspect
import asyncio
import requests

load_dotenv()

if "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" in os.environ:
    from utilities.spotipy_test import get_random_from_library

if "OPENAI_API_KEY" in os.environ:
    from utilities.openAI_test import get_ai_response

description = '''A Bot for Bingo! All hail BingoBot'''
intents = discord.Intents.default()
utils.load_riddles()


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


async def set_status(activity_type, activity, url=""):
    if activity_type == "watching":
        # setting `watching ` status
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

    elif activity_type == "playing":
        # Setting `Playing ` status
        await bot.change_presence(activity=discord.Game(name=activity))

    elif activity_type == "streaming":
        # Setting `Streaming ` status
        await bot.change_presence(activity=discord.Streaming(name=activity, url=url))

    elif activity_type == "listening":
        # Setting `Listening ` status
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))


class Bot(commands.Bot):

    def __init__(ctx):

        super().__init__(command_prefix='$', description=description, intents=intents,
                         help_command=commands.DefaultHelpCommand(width=160, no_category="General"))

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
        await utils.add_to_list(line, str(ctx.guild))
        print("New line: _" + line + "_ Added to pool in " + str(ctx.guild) +
              " by " + (str(ctx.message.author)))
        Bot.refresh_bools[str(ctx.guild)] = True

    @commands.command()
    async def freeadd(ctx):
        """Adds a new statement to the bingo free space pool"""
        msg = ctx.message.content
        line = msg.split("$freeadd ", 1)[1]
        await ctx.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line, str(ctx.guild))
        print("New line: _" + line + "_ Added to free space pool in " + str(ctx.guild) +
              " by " + (str(ctx.message.author)))
        Bot.refresh_bools[str(ctx.guild)] = True

    @commands.command()
    async def bingo(ctx):
        """Sends pre-generated bingo card as reply to command"""
        time_since_last_bingo = time.time() - Bot.time_of_last_bingo

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + str(ctx.guild) + '/output_' + str(Bot.rolling_index) + '.jpg')
            await ctx.reply(utils.random_animal_emoji(), file=img)

            await regenerate_images(Bot.rolling_index, str(ctx.guild))

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

    @commands.command(name='rig', hidden=True)
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
        await regenerate_all_images(str(ctx.guild))
        await ctx.send("Cards refreshed!")

    @commands.command()
    async def bigrefresh(ctx):
        """regenerate all big images"""
        await regenerate_all_big_images(str(ctx.guild))
        await ctx.send("Big Cards refreshed!")

    @commands.command()
    async def list(ctx):
        """Lists all items in bingo pool. Use the index with the del command."""
        lines = await utils.list_all_lines(str(ctx.guild))

        for line in lines:
            line = ' '.join(line).lstrip()
            await ctx.send(line, delete_after=20)

    @commands.command()
    async def freelist(ctx):
        """Lists all items in free space pool. Use the index with the freedel command."""
        lines = await utils.list_all_free_lines(str(ctx.guild))

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

    @commands.command(hidden=True)
    async def resetlist(ctx):
        """Resets the bingo list to default. WARNING: lost lists are unrecoverable"""
        await utils.reset_list(str(ctx.guild))
        await ctx.send("List has been reset to default.")

    @commands.command(hidden=True)
    async def resetfreelist(ctx):
        """Resets the free space bingo list to default. WARNING: lost lists are unrecoverable"""
        await utils.reset_free_list(str(ctx.guild))
        await ctx.send("Free list has been reset to default.")

    @commands.command()
    async def animal(ctx):
        """:frog:"""
        await ctx.reply(utils.random_animal_emoji())

    @commands.command(name='fullrefresh', hidden=True)
    async def full_refresh_all_servers(ctx):
        """Refreshes all cards on all servers."""
        for guild_name in bot.guilds:
            await regenerate_all_images(str(guild_name))

    @commands.command(name="status")
    @commands.has_role("Admin")
    async def set_status(ctx, *, content):
        """Set status of bot"""
        activity_type = content.split(" ", 1)[0]
        url = ""
        if activity_type == "streaming":
            activity = content.split(" ", 1)[1].rsplit(" ", 1)[0]
            url = content.split(" ")[-1]
        else:
            url = ""
            activity = content.split(" ", 1)[1]

        await set_status(activity_type, activity, url)

    @commands.command(name='funfact')
    async def fun_fact(ctx):
        """Generates fun facts! Sourced from https://uselessfacts.jsph.pl"""
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        text = response['text']
        # source = response['source']
        await ctx.send(text)

    @commands.command(hidden=True)
    async def frog(ctx):
        """sends frog emote!"""
        frog = "🐸"
        await ctx.reply(frog)

    @commands.command()
    async def riddle(ctx):
        """Gives a random riddle and answer"""
        out = await utils.random_riddle_answer()
        await ctx.send(out)

    @commands.command(name="answer")
    async def answer_riddle(ctx, *, answer):
        """Try to answer the riddle!"""
        if await utils.check_riddle(answer):
            await ctx.reply("Correct!")
        else:
            await ctx.reply("Wrong!")

    @commands.command(name='blame')
    async def who_killed_us(ctx):
        """Who killed us?"""
        caller = ctx.author.id
        out = utils.random_wipe_reason(str(caller))
        await ctx.send(out)

    @set_status.error
    async def set_status_error(ctx, error):
        """Send this message if the setstatus command is called by non-Admin"""
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Only Admins can set my status...')

    @commands.command(hidden=True)
    async def adv_rel(ctx):
        """sends e12 P2 advanced relativity"""
        img = discord.File('resources/images/e12p2_adv_rel.png')
        await ctx.reply("", file=img)

    @commands.command(hidden=True)
    async def get_guild(ctx):
        """returns the name of the guild this command was used in"""
        current_guild = str(ctx.guild)
        await ctx.reply(current_guild)

    @commands.command(name="wingo", hidden=True)
    # Stop snooping on my code >:(
    # new cowwand owo
    async def web_card(ctx):
        """Returns card data in JSON format"""
        data = generate_card_data(str(ctx.guild))
        htmlcreator = htmlCreator()
        htmlcreator.generate_html_file(data)
        # TODO stuff with json
        print(data)
        await ctx.reply(utils.random_animal_emoji())

    @commands.command(name="yolo", hidden=True)
    async def yolo_detect(ctx):
        url = ctx.message.attachments[0].url

        image_path = utils.yolo_response(url)
        img = discord.File(image_path)
        await ctx.reply("", file=img)

    @commands.command()
    async def teanalyse(ctx, *, report_id):
        """Gives statistics on FF logs reports from The Epic of Alexander. Requires log URL"""
        api_key = os.getenv('FFLOGS_API_KEY')
        if api_key is None:
            await ctx.send("Command is not currently configured on")
            return
        message = analyser.analyse_tea_fight(report_id, api_key)

        if message is None:
            await ctx.send("No TEA fights found")
            return
        await ctx.send(message)

    @commands.command()
    async def uwunalyse(ctx, *, report_id):
        """Gives statistics on FF logs reports from the Weapon's Refrain (Ultimate). Requires log URL"""
        api_key = os.getenv('FFLOGS_API_KEY')
        if api_key is None:
            await ctx.send("Command is not currently configured on")
            return
        message = analyser.analyse_uwu_fight(report_id, api_key)

        if message is None:
            await ctx.send("No UWU fights found")
            return
        await ctx.send(message)

    if "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" in os.environ:
        @commands.command()
        async def random_song(ctx):
            """Returns a random song from my library"""
            out = get_random_from_library()
            await ctx.reply(out)

    if "OPENAI_API_KEY" in os.environ:
        @commands.command()
        async def ai(ctx, *, new_prompt):
            """Get a real AI response from BingoBot!"""

            if str(ctx.guild) in os.getenv('GUILD_WHITELIST'):
                author = str(ctx.message.author).split('#')[0]
                response = get_ai_response(new_prompt, author)
                await ctx.reply(response)
            else:
                await ctx.reply("Sorry, this guild is not authorised to use the AI function.")

    async def on_message(self, message):
        """Called every time a message is received. Checks if the server is new, if so folders and lists are created"""
        if not os.path.isdir("lists/" + str(message.guild)):
            os.mkdir("lists/" + str(message.guild))
            await utils.reset_list(str(message.guild))
            await utils.reset_free_list(str(message.guild))

        if not os.path.isdir("output_folder/" + str(message.guild)):
            os.mkdir("output_folder/" + str(message.guild))

        await bot.process_commands(message)

    async def timed_refresh(ctx):
        """Automatically refreshes bingo card pools for servers if any new lines have been added"""
        ctx.generate_refresh_bools()
        while not bot.is_closed():
            for guild_name in Bot.refresh_bools:
                if Bot.refresh_bools[guild_name]:
                    print("automatically regenerating cards in: " + str(guild_name))
                    await regenerate_all_images(guild_name)
                    Bot.refresh_bools[guild_name] = False

            await asyncio.sleep(30)

    @staticmethod
    def generate_refresh_bools():  # This function generates a dictionary of bools for every server the bot is in
        guilds = bot.guilds
        for i, guild_name in enumerate(guilds):
            Bot.refresh_bools[guild_name] = False


if not os.path.isdir("lists/"):
    os.mkdir("lists/")

if not os.path.isdir("output_folder/"):
    os.mkdir("output_folder/")

bot = Bot()
bot.run(os.getenv('BINGO_BOT_TOKEN'))
