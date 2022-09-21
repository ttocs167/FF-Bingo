import discord
from discord.ext import commands, tasks
import time
from utilities import utils
from utilities.generate_cards import generate_card
from utilities.generate_card_data import generate_card_data


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


class BingoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_of_last_bingo = time.time()
        self.rolling_index = 0
        self.refresh_bools = {}
        self.timed_refresh.start()

    # async def setup_hook(self):
    #     self.timed_refresh.start()

    @commands.command()
    async def bingo(self, ctx: commands.Context):
        """Sends pre-generated bingo card as reply to command"""
        time_since_last_bingo = time.time() - self.time_of_last_bingo

        if time_since_last_bingo > 0.5:
            async with ctx.channel.typing():
                img = discord.File('output_folder/' + str(ctx.guild) + '/output_' + str(self.rolling_index) + '.jpg')
                await ctx.reply(utils.random_animal_emoji(), file=img)

                await regenerate_images(self.rolling_index, str(ctx.guild))

                print('image generated for ' + str(ctx.guild))

                self.rolling_index = (self.rolling_index + 1) % 5
                self.time_of_last_bingo = time.time()

        else:
            print("bingo command recieved in " + str(ctx.guild) + " too soon to generate!")

    @commands.command()
    async def add(self, ctx: commands.Context, *, line):
        """Adds a new statement to the bingo pool"""
        await ctx.send("New line: \n_" + line + "_ \nAdded to pool!")
        await utils.add_to_list(line, str(ctx.guild))
        print("New line: _" + line + "_ Added to pool in " + str(ctx.guild) +
              " by " + (str(ctx.message.author)))
        self.refresh_bools[str(ctx.guild)] = True

    @commands.command()
    async def freeadd(self, ctx: commands.Context):
        """Adds a new statement to the bingo free space pool"""
        msg = ctx.message.content
        line = msg.split("$freeadd ", 1)[1]
        await ctx.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line, str(ctx.guild))
        print("New line: _" + line + "_ Added to free space pool in " + str(ctx.guild) +
              " by " + (str(ctx.message.author)))
        self.refresh_bools[str(ctx.guild)] = True

    @commands.command()
    async def bigbingo(self, ctx: commands.Context):
        """Sends a large bingo card as reply to command"""
        time_since_last_bingo = time.time() - self.time_of_last_bingo
        print(time_since_last_bingo)

        if time_since_last_bingo > 0.5:
            async with ctx.channel.typing():
                img = discord.File('output_folder/' + str(ctx.guild) + '/big_output_' + str(self.rolling_index) + '.jpg')
                await ctx.reply(utils.random_animal_emoji(), file=img)

                await regenerate_big_images(self.rolling_index, str(ctx.guild))

                print('Big image generated for ' + str(ctx.guild))

                self.rolling_index = (self.rolling_index + 1) % 5
                self.time_of_last_bingo = time.time()

        else:
            print("Big bingo command recieved in " + str(ctx.guild) + " too soon to generate!")

    @commands.command()
    async def refresh(self, ctx: commands.Context):
        """Regenerate all images. Called automatically on list change"""
        async with ctx.channel.typing():
            await regenerate_all_images(str(ctx.guild))
        await ctx.send("Cards refreshed!")

    @commands.command()
    async def bigrefresh(self, ctx: commands.Context):
        """regenerate all big images"""
        async with ctx.channel.typing():
            await regenerate_all_big_images(str(ctx.guild))
        await ctx.send("Big Cards refreshed!")

    @commands.command()
    async def list(self, ctx: commands.Context):
        """Lists all items in bingo pool. Use the index with the del command."""
        lines = await utils.list_all_lines(str(ctx.guild))

        for line in lines:
            line = ' '.join(line).lstrip()
            await ctx.send(line, delete_after=20)

    @commands.command()
    async def freelist(self, ctx: commands.Context):
        """Lists all items in free space pool. Use the index with the freedel command."""
        lines = await utils.list_all_free_lines(str(ctx.guild))

        for line in lines:
            line = ' '.join(line).lstrip()
            await ctx.send(line, delete_after=20)

    @commands.command(name='del')
    async def delete_line(self, ctx: commands.Context, *, indices):
        """Deletes the lines at indices given in the list. Use $list command to view indices"""
        indices = indices.split(" ")
        indices.sort(reverse=True)
        for index in indices:
            index = int(index)
            line = await utils.get_line(index, str(ctx.guild))
            await utils.delete_line(index, str(ctx.guild))
            print("deleted line: " + line)
            await ctx.send("deleted line: " + line)

    @commands.command(name='freedel')
    async def delete_free_line(self, ctx: commands.Context, index: int):
        """Deletes the free line at [index] in the free list. Use $freelist command to view indices"""
        line = await utils.get_free_line(index, str(ctx.guild))
        await utils.delete_free_line(index, str(ctx.guild))
        print("deleted free line: " + line)
        await ctx.send("deleted free line: " + line)

    @commands.command(hidden=True)
    async def resetlist(self, ctx: commands.Context):
        """Resets the bingo list to default. WARNING: lost lists are unrecoverable"""
        await utils.reset_list(str(ctx.guild))
        await ctx.send("List has been reset to default.")

    @commands.command(hidden=True)
    async def resetfreelist(self, ctx: commands.Context):
        """Resets the free space bingo list to default. WARNING: lost lists are unrecoverable"""
        await utils.reset_free_list(str(ctx.guild))
        await ctx.send("Free list has been reset to default.")

    @commands.command(name='fullrefresh', hidden=True)
    @commands.is_owner()
    async def full_refresh_all_servers(self, ctx: commands.Context):
        """Refreshes all cards on all servers."""
        for guild_name in ctx.guilds:
            await regenerate_all_images(str(guild_name))

    @tasks.loop(hours=24)
    async def timed_refresh(self):
        """Automatically refreshes bingo card pools for servers if any new lines have been added"""
        print("timed refresh!")
        self.generate_refresh_bools()
        if not self.bot.is_closed():
            for guild_name in self.refresh_bools:
                if self.refresh_bools[guild_name]:
                    print("automatically regenerating cards in: " + str(guild_name))
                    await regenerate_all_images(guild_name)
                    self.refresh_bools[guild_name] = False

    @commands.command(hidden=True)
    @commands.is_owner()
    async def silent_reset(self, ctx, *, content):
        """Resets a list for another guild"""
        split = content.split(" ", 1)
        custom_guild = split[1]
        list_type = split[0]

        if list_type == "free":
            await utils.reset_free_list(custom_guild)
            print("resetting " + str(custom_guild) + "'s free list")
        else:
            await utils.reset_list(custom_guild)
            print("resetting " + str(custom_guild) + "'s list")

    def generate_refresh_bools(self):  # This function generates a dictionary of bools for every server the bot is in
        guilds = self.bot.guilds
        for i, guild_name in enumerate(guilds):
            self.refresh_bools[guild_name] = False

