import os
import discord
from discord.ext import commands, tasks
import datetime
from utilities import utils
from utilities import generate_secret_bingo as gsb
from utilities import hangman
import requests
from utilities import wordle_cheat
import json
from utilities.wordle_cheat import save_user_data
import random
from dotenv import load_dotenv


load_dotenv()

if "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" in os.environ:
    from utilities.spotipy_test import get_random_from_library


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
        self.hangman = None

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
    async def compliment(self, ctx: commands.Context):
        await ctx.reply(utils.random_compliment())

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
        """🐸"""
        button = discord.ui.Button(emoji="🐸", style=discord.ButtonStyle.blurple)

        async def frog_callback(interaction: discord.Interaction):
            print(interaction.user)
            await interaction.response.send_message("🐸")

        button.callback = frog_callback

        view = discord.ui.View(timeout=None)
        view.add_item(button)

        await ctx.send(view=view)

    @commands.command(hidden=True)
    async def legend(self, ctx):
        button = discord.ui.Button(emoji="<:legend:1003796537748504677>", style=discord.ButtonStyle.blurple)

        clives = ["<:cliveParty:939589378785828934>",
                  "<:cliveClown:950563664971329566>",
                  "<:cliveCool:948872198922321931>",
                  "<:cliveCopium:945748416959492117>",
                  "<:cliveCry:914303922095685743>",
                  "<:cliveFingerGuns:914303921818828801>",
                  "<:cliveGun:939588984160542790>",
                  "<:cliveHuh:914303922154385448>",
                  "<:clivePeek:939588984378650664>",
                  "<:cliveRage:914303922175352862>",
                  "<:cliveShy:914303922292789248>",
                  "<:cliveThink:914303922171166800>",
                  "<:cliveWizard:942812467132784672>",
                  "<:cliveEvil:939588984105992272>",
                  "<:legend:1003796537748504677>",
                  "<:grr:1003796966976782467>",
                  "<:gremlin:1009824312708059317>"
                  ]

        async def legend_callback(interaction: discord.Interaction):
            print(interaction.user)
            await interaction.response.send_message(random.choice(clives))

        button.callback = legend_callback

        view = discord.ui.View(timeout=None)
        view.add_item(button)

        await ctx.send(view=view)

    @commands.command()
    async def raffle(self, ctx: commands.Context):
        author = ctx.author
        entries = []

        enter_button = discord.ui.Button(label=">enter raffle<", emoji="🎟",
                                         style=discord.ButtonStyle.blurple)

        draw_button = discord.ui.Button(label=">finish raffle<", emoji="✅",
                                        style=discord.ButtonStyle.grey)

        async def enter_raffle(interaction: discord.Interaction):
            if interaction.user not in entries:
                entries.append(interaction.user)
                await interaction.response.send_message("{} entered the raffle".format(interaction.user.mention))
            else:
                await interaction.response.send_message("You cannot enter the raffle twice", ephemeral=True)
                return

        async def finalise_raffle(interaction: discord.Interaction):
            if interaction.user != author:
                await interaction.response.send_message("Only the author can finalise the raffle", ephemeral=True)
                return
            elif len(entries) == 0:
                await interaction.response.send_message("Nobody has entered the raffle yet", ephemeral=True)
            else:
                winner = random.choice(entries)
                await interaction.response.send_message("🎉 {} has won the raffle! 🎉".format(winner.mention))

                enter_button.disabled = True
                draw_button.disabled = True
                await raffle.edit(view=view)

        enter_button.callback = enter_raffle
        draw_button.callback = finalise_raffle

        view = discord.ui.View(timeout=None)
        view.add_item(enter_button)
        view.add_item(draw_button)

        raffle = await ctx.send(view=view)

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
        days, hours, minutes, seconds = utils.get_booba_time()
        await ctx.send("It has been **{}** Days, **{}** Hours,"
                       " **{}** Minutes, and **{}** seconds since last booba".format(days, hours, minutes, seconds))

    @commands.command(name='resetbooba')
    async def reset_booba_count(self, ctx, member: discord.Member = None):
        """resets the booba timer. You can optionally mention a user to record their offense"""
        days, hours, minutes, seconds, msg_pt4 = utils.booba(member)

        msg_pt1 = ("It had been **{}** Days, **{}** Hours,"
                       " **{}** Minutes, and **{}** seconds since last booba".format(days, hours, minutes, seconds))
        utils.reset_booba()
        msg_pt2 = ("Booba reset")
        msg_pt3 = ("It now has been **{}** Days, **{}** Hours,"
                       " **{}** Minutes, and **{}** seconds since last booba".format(0, 0, 0, 0))

        await ctx.send(msg_pt1 + "\n" + msg_pt2 + "\n" + msg_pt3 + "\n" + msg_pt4)

    @commands.command(aliases=["boobaboard", "leaderboard",
                                              "boobaleaderboards", "boobaleaderboard", "booba_leaderboards"])
    async def booba_leaderboard(self, ctx: commands.Context):
        """Returns the leaderboard sorted by reset offenses"""

        response = await utils.booba_board(ctx)

        await ctx.send(response)

    @commands.command(hidden=True)
    async def adv_rel(self, ctx):
        """sends e12 P2 advanced relativity"""
        img = discord.File('resources/images/e12p2_adv_rel.png')
        await ctx.reply("", file=img)


    if "SPOTIPY_CLIENT_ID" and "SPOTIPY_CLIENT_SECRET" in os.environ:
        @commands.command()
        async def random_song(self, ctx):
            """Returns a random song from my library"""
            out = get_random_from_library()
            await ctx.reply(out)

    @commands.command(aliases=["addquote", "aquote"])
    async def add_quote(self, ctx: commands.Context):
        """Reply to a quotable message with this command to add it to the quotes database"""
        message = ctx.message
        if ctx.message.reference is not None:
            resolved_reference = message.reference.resolved

            message_content = resolved_reference.content
            quote_author_id = resolved_reference.author.id
            quote_time = resolved_reference.created_at
            reference_id = resolved_reference.id

            output = utils.store_quote(ctx.guild.name, message_content, quote_author_id, quote_time, reference_id)

            await ctx.reply(output)

        else:
            await ctx.reply("you must reply to the message you want to quote.")

    @commands.command(aliases=["rquote", "randomquote", "getquote", "random_quote", "quote"])
    async def get_random_quote(self, ctx: commands.Context):
        """this will return a random quote from the database!"""
        if ctx.message.reference is not None:
            await ctx.reply("lmao, idiot")
            return

        content, author_id, time = utils.get_random_quote(ctx.guild.name)

        if content is not None:
            author = ctx.guild.get_member(author_id)

            nick_or_name = author.nick
            if nick_or_name is None:
                nick_or_name = author.name

            out = "_" + content + "_\n- **" + nick_or_name + "**" + "\n" + time.strftime("%Y/%m/%d, %H:%M:%S")
            await ctx.reply(out)

        else:
            await ctx.reply("There don't seem to be any quotes for your server...")

    @commands.command(aliases=["getquotes", "myquotes"])
    async def get_my_quotes(self, ctx: commands.Context):
        """Use this to get a list of your quotes in the database and the index needed to delete them"""

        await ctx.reply("DM with more info on the way...")

        out = utils.get_personal_quotes(str(ctx.guild.name), ctx.author.id)

        author = ctx.author
        dm = await author.create_dm()
        await dm.send(out)

    @commands.command(aliases=["dquote", "delquote", "rmquote"])
    async def del_quote(self, ctx: commands.Context, guild: str, quote_index: int):
        """This will allow you to delete a quote from you from the database"""
        out = utils.delete_quote_at_index(guild, quote_index, ctx.author.id)
        await ctx.reply(out)

    @commands.is_owner()
    @commands.command()
    async def get_all_quotes(self, ctx: commands.Context):

        out = utils.get_all_quotes(ctx.guild.name)

        author = ctx.author
        dm = await author.create_dm()
        await dm.send(out)

    @commands.is_owner()
    @commands.command()
    async def owner_del_quote(self, ctx: commands.Context, guild: str, quote_index: int):

        out = utils.owner_del_quote_at_index(guild, quote_index)

        await ctx.reply(out)

    @commands.command(aliases=["hangman", "hm"])
    async def hangman(self, ctx: commands.Context, *, letter: str = None):
        """Starts a game of hangman or guesses a letter in the current game"""

        if self.hangman is None:
            await ctx.reply("Starting a game of hangman...")
            self.hangman = hangman.Hangman()
            await ctx.send("```" + self.hangman.word_list + "```")

        else:
            if letter is None:
                await ctx.reply("You must guess a letter!")
                return

            if len(letter.strip()) >= 1:
                await ctx.reply("You can only guess one letter at a time!")
                return

            if self.hangman.guesses > 1:
                success, word_list = self.hangman.guess_letter(letter)
                if success:
                    await ctx.send("```" + word_list + "```")
                elif self.hangman.guesses > 1:
                    await ctx.send("```" + word_list + "```")
                    await ctx.send("You have {} guesses left".format(self.hangman.guesses))
                else:
                    await ctx.send("```" + word_list + "```")
                    await ctx.send("You have {} guesses left".format(self.hangman.guesses))
                    await ctx.send("Better luck next time!")
                    await ctx.send("The word was {}".format(self.hangman.word))
                    self.hangman = None


