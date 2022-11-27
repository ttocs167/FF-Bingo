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
from cogs.utils_cog import UtilCog
from cogs.ai_cog import AICog
from cogs.camera_cog import CamCog


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
        await self.add_cog(UtilCog(bot))
        await self.add_cog(CamCog(bot))
        if "OPENAI_API_KEY" in os.environ:
            await self.add_cog(AICog(bot))

    @staticmethod
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.tree.sync()  # this enables slash commands to appear

    async def on_message(self, message):
        """Called every time a message is received. Checks if the server is new, if so folders and lists are created"""
        if message.guild is not None:
            if not os.path.isdir("lists/" + str(message.guild)):
                os.mkdir("lists/" + str(message.guild))
                await utils.reset_list(str(message.guild))
                await utils.reset_free_list(str(message.guild))

            if not os.path.isdir("output_folder/" + str(message.guild)):
                os.mkdir("output_folder/" + str(message.guild))

        elif str(message.content).lower().startswith("i love you"):
            await message.reply("<3")

        if str(message.content).lower().startswith("good bot"):
            await message.reply(":robot::heart:<:BingoBot:1025438478273626172>")
        await bot.process_commands(message)


if not os.path.isdir("lists/"):
    os.mkdir("lists/")

if not os.path.isdir("output_folder/"):
    os.mkdir("output_folder/")


load_dotenv()

description = '''A Bot for Bingo! All hail BingoBot'''
intents = discord.Intents.all()
utils.load_riddles()

bot = Bot()

bot.run(os.getenv('BINGO_BOT_TOKEN'))
