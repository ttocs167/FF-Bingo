import os
import discord
from discord.ext import commands
from generate_cards import generate_card
from dotenv import load_dotenv
import utils
import inspect
import time

load_dotenv()
description = '''A Bot for Bingo! All hail BingoBot'''
intents = discord.Intents.default()


class Bot(commands.Bot):

    def __init__(self):

        super().__init__(command_prefix='$', description=description, intents=intents, time_of_last_bingo=time.time())

        Bot.time_of_last_bingo = time.time()
        Bot.rolling_index = 0

        members = inspect.getmembers(self)
        for name, member in members:
            if isinstance(member, commands.Command):
                if member.parent is None:
                    self.add_command(member)

    @staticmethod
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @commands.command(name='8ball')
    async def _ball(ctx):
        """Sends randomly selected 8ball response"""
        await ctx.send(utils.random_8ball_response())

    @commands.command(name='add')
    async def add(ctx, *, line):
        """Adds a new statement to the bingo pool"""
        # msg = ctx.message.content
        # line = utils.emoji_free_text(msg.split("$add ", 1)[1])
        await ctx.send("New line: \n_" + line + "_ \nAdded to pool!")
        await utils.add_to_list(line, str(ctx.message.guild))
        print("New line: _" + line + "_ Added to pool in " + str(ctx.message.guild) +
              " by " + (str(ctx.message.author)))
        # refresh_bools[str(message.guild)] = True

    @commands.command()
    async def freeadd(ctx):
        """Adds a new statement to the bingo free space pool"""
        msg = ctx.message.content
        line = msg.split("$freeadd ", 1)[1]
        await ctx.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line, str(ctx.message.guild))
        print("New line: _" + line + "_ Added to free space pool in " + str(ctx.message.guild) +
              " by " + (str(ctx.message.author)))
        # refresh_bools[str(message.guild)] = True

    @commands.command()
    async def bingo(ctx):

        time_since_last_bingo = time.time() - Bot.time_of_last_bingo
        print(time_since_last_bingo)

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + str(ctx.guild) + '/output_' + str(Bot.rolling_index) + '.jpg')
            await ctx.reply(utils.random_animal_emoji(), file=img)

            await generate_card(Bot.rolling_index, str(ctx.guild))

            print('image generated for ' + str(ctx.guild))

            Bot.rolling_index = (Bot.rolling_index + 1) % 5
            Bot.time_of_last_bingo = time.time()

        else:
            print("bingo command recieved in " + str(ctx.guild) + " too soon to generate!")

    async def on_message(self, message):
        if not os.path.isdir("lists/" + str(message.guild)):
            os.mkdir("lists/" + str(message.guild))
            await utils.reset_list(str(message.guild))
            await utils.reset_free_list(str(message.guild))

        if not os.path.isdir("output_folder/" + str(message.guild)):
            os.mkdir("output_folder/" + str(message.guild))

        await bot.process_commands(message)


bot = Bot()
bot.run(os.getenv('BINGO_BOT_TOKEN'))
