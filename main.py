import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utilities import utils
from cogs.bingo_cog import BingoCog
from cogs.fun_cog import FunCog
from cogs.admin_cog import AdminCog
from cogs.qotd_cog import QotdCog
from cogs.maps_cog import MapsCog
from cogs.audio_cog import AudioCog


class Bot(commands.Bot):

    def __init__(ctx):

        super().__init__(command_prefix='$', description=description, intents=intents,
                         help_command=commands.DefaultHelpCommand(width=160, no_category="General"))

        Bot.rigged_statement = None

    async def setup_hook(self):
        await self.add_cog(BingoCog(bot))
        await self.add_cog(FunCog(bot))
        await self.add_cog(AdminCog(bot))
        await self.add_cog(QotdCog(bot))
        await self.add_cog(MapsCog(bot))
        await self.add_cog(AudioCog(bot))

    @staticmethod
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    async def on_message(self, message):
        """Called every time a message is received. Checks if the server is new, if so folders and lists are created"""
        if message.guild is not None:
            if not os.path.isdir("lists/" + str(message.guild)):
                os.mkdir("lists/" + str(message.guild))
                await utils.reset_list(str(message.guild))
                await utils.reset_free_list(str(message.guild))

            if not os.path.isdir("output_folder/" + str(message.guild)):
                os.mkdir("output_folder/" + str(message.guild))

            await bot.process_commands(message)
        elif str(message.content).lower().startswith("i love you"):
            await message.reply("<3")


if not os.path.isdir("lists/"):
    os.mkdir("lists/")

if not os.path.isdir("output_folder/"):
    os.mkdir("output_folder/")


load_dotenv()

description = '''A Bot for Bingo! All hail BingoBot'''
intents = discord.Intents.all()
utils.load_riddles()

bot = Bot()

# async def main():
#     async with bot:
#         bot.timed_refresh.start()
#         bot.send_qotd.start(bot)
#         # send_questions.start(bot)
#         await bot.start(os.getenv('BINGO_BOT_TOKEN'))

bot.run(os.getenv('BINGO_BOT_TOKEN'))

# asyncio.run(main())
