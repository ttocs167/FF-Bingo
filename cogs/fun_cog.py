import os
import discord
from discord.ext import commands, tasks
import datetime
from utilities import utils
from utilities import generate_secret_bingo as gsb
import requests
from utilities import wordle_cheat
import json
from utilities.wordle_cheat import save_user_data

try:
    from utilities import webcam_photo, picam_photo
except:
    print("could not import picam module")

if "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" in os.environ:
    from utilities.spotipy_test import get_random_from_library

if "OPENAI_API_KEY" in os.environ:
    from utilities.openAI_test import get_ai_response


async def set_status(bot: commands.Bot, activity_type, activity, url=""):
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


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rigged_statement = None
        self.reset_wordle_counts.start()

    @commands.command(name='8ball')
    async def _ball(self, ctx):
        """Sends randomly selected 8ball response"""
        if self.rigged_statement is not None:
            await ctx.send("_**" + str(self.rigged_statement) + "**_")
            self.rigged_statement = None
            print("Rigged message sent.")
        else:
            await ctx.send(utils.random_8ball_response())

    @commands.command()
    async def secretbingo(self, ctx):
        """DMs the user with secret tasks"""
        await ctx.reply("Secret missions on the way...")

        out = gsb.generate_secret_bingo()

        author = ctx.author
        dm = await author.create_dm()

        await dm.send(out)

    @commands.command()
    async def secretrules(self, ctx):
        """explains the rules to secret bingo!"""

        out = "Use the _$secretbingo_ command to receive 4 secret missions.\n" \
              "Complete 3 missions first to win.\n" \
              "When you complete a mission you must immediately claim it.\n" \
              "When attempting to complete a mission, if another player asks you" \
              " if what you are doing is for the mission, the mission is failed and cannot be completed.\n" \
              "You must be honest when confronted about your mission if they are correct.\n" \
              "Good luck!"

        await ctx.reply(out)

    @commands.command(name='rig', hidden=True)
    @commands.is_owner()
    async def rig(self, ctx, *, line):
        """rigs the next 8ball command to be a custom string. Only available to bot owner"""
        await ctx.send("Next message rigged. _Our little secret..._")
        self.rigged_statement = line
        print("Next message rigged: " + str(line))

    @rig.error
    async def rig_error(self, ctx, error):
        """Send this message if the rig command is called by non-owner"""
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Nothing to see here comrade...')

    @commands.command(name="status")
    @commands.has_role("Admin")
    async def set_status(self, ctx, *, content):
        """Set status of bot"""
        activity_type = content.split(" ", 1)[0]
        url = ""
        if activity_type == "streaming":
            activity = content.split(" ", 1)[1].rsplit(" ", 1)[0]
            url = content.split(" ")[-1]
        else:
            url = ""
            activity = content.split(" ", 1)[1]

        await set_status(self.bot, activity_type, activity, url)

    @set_status.error
    async def set_status_error(self, ctx, error):
        """Send this message if the setstatus command is called by non-Admin"""
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Only Admins can set my status...')

    @commands.command(name='funfact')
    async def fun_fact(self, ctx):
        """Generates fun facts! Sourced from https://uselessfacts.jsph.pl"""
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        text = response['text']
        # source = response['source']
        await ctx.send(text)

    @commands.command(hidden=True)
    async def frog(self, ctx):
        """sends frog emote!"""
        frog = "🐸"
        await ctx.reply(frog)

    @commands.command()
    async def animal(self, ctx: commands.Context):
        """:frog:"""
        await ctx.reply(utils.random_animal_emoji())

    @commands.command()
    async def riddle(self, ctx):
        """Gives a random riddle and answer"""
        out = await utils.random_riddle_answer()
        await ctx.send(out)

    @commands.command(name="answer")
    async def answer_riddle(self, ctx, *, answer):
        """Try to answer the riddle!"""
        if await utils.check_riddle(answer):
            await ctx.reply("Correct!")
        else:
            await ctx.reply("Wrong!")

    @commands.command(hidden=False, aliases=['dailywordle', 'dwordle'])
    async def daily_wordle(self, ctx, *, answer):
        """A daily Wordle! Not the same as the real wordle, no spoilerino!"""
        out = await wordle_cheat.daily_wordle(answer, str(ctx.author.id))
        out = "||" + out + "||"
        await ctx.send(out)

    @commands.command(hidden=True)
    async def reveal_daily_wordle(self, ctx):
        """Reveals the daily wordle word with spoiler tags"""
        out = await wordle_cheat.reveal_daily_wordle()
        out = "||" + out + "||"
        await ctx.send(out)

    @commands.command(hidden=True)
    async def moar_guesses_please(self, ctx):
        """resets your attempts at the daily wordle"""
        await wordle_cheat.moar_guesses_please(str(ctx.author.id))
        await ctx.send("Okay, okay. fine... Here you go.")

    @commands.command(hidden=False)
    async def wordle(self, ctx, *, answer):
        """Wordle! Now infinitely repeatable"""
        out = await wordle_cheat.wordle(answer)
        out = "||" + out + "||"
        await ctx.send(out)

    @commands.command(hidden=False)
    async def reset_wordle(self, ctx):
        """Resets the repeatable wordle word"""
        old_word = await wordle_cheat.reset_word()
        out = "Internal word reset!" + "\nThe old word was: ||" + old_word + "||"
        await ctx.send(out)

    @tasks.loop(time=[datetime.time(0, 0, 0)])
    async def reset_wordle_counts(self):
        print("resetting daily wordle attempts!")
        with open("wordle_user_data.json") as f:
            user_data = json.load(f)

        for user in user_data:
            user_data[user] = 0

        # Save the reset data back to file
        save_user_data()

    @commands.command(name='blame')
    async def who_killed_us(self, ctx):
        """Who killed us?"""
        caller = ctx.author.id
        out = utils.random_wipe_reason(str(caller))
        await ctx.send(out)

    @commands.command()
    async def ffxiv(self, ctx):
        pasta = "Did you know that the critically acclaimed MMORPG Final Fantasy XIV has a free trial," \
                " and includes the entirety of A Realm Reborn AND the award-winning Heavensward expansion up to" \
                " level 60 with no restrictions on playtime? Sign up, and enjoy Eorzea today!" \
                " https://secure.square-enix.com/account/app/svc/ffxivregister?lng=en-gb"

        await ctx.send(pasta)

    @commands.command(name='booba')
    async def days_since_booba(self, ctx):
        days, hours, minutes, seconds = utils.booba()
        await ctx.send("It has been **{}** Days, **{}** Hours,"
                       " **{}** Minutes, and **{}** seconds since last booba".format(days, hours, minutes, seconds))

    @commands.command(name='resetbooba')
    async def reset_booba_count(self, ctx):
        days, hours, minutes, seconds = utils.booba()
        msg_pt1 = ("It had been **{}** Days, **{}** Hours,"
                       " **{}** Minutes, and **{}** seconds since last booba".format(days, hours, minutes, seconds))
        utils.reset_booba()
        msg_pt2 = ("Booba reset")
        msg_pt3 = ("It now has been **{}** Days, **{}** Hours,"
                       " **{}** Minutes, and **{}** seconds since last booba".format(0, 0, 0, 0))

        await ctx.send(msg_pt1 + "\n" + msg_pt2 + "\n" + msg_pt3)

    @commands.command(hidden=True)
    async def adv_rel(self, ctx):
        """sends e12 P2 advanced relativity"""
        img = discord.File('resources/images/e12p2_adv_rel.png')
        await ctx.reply("", file=img)

    @commands.command(name="plant", hidden=False)
    async def webcam_image(self, ctx):

        image_path = await picam_photo.take_image()
        img = discord.File(image_path)
        await ctx.reply("", file=img)

    if "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" in os.environ:
        @commands.command()
        async def random_song(self, ctx):
            """Returns a random song from my library"""
            out = get_random_from_library()
            await ctx.reply(out)

    if "OPENAI_API_KEY" in os.environ:
        @commands.command()
        async def ai(self, ctx, *, new_prompt):
            """Get a real AI response from BingoBot!"""

            if str(ctx.guild) in os.getenv('GUILD_WHITELIST'):
                author = str(ctx.message.author).split('#')[0]
                response = get_ai_response(new_prompt, author)
                await ctx.reply(response)
            else:
                await ctx.reply("Sorry, this guild is not authorised to use the AI function.")