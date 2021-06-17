import discord
import os
from generate_cards import generate_card
import utils
import time
from dotenv import load_dotenv
import asyncio

load_dotenv()
client = discord.Client()

time_of_last_bingo = time.time()
rolling_index = 0
whitelist = ["ttocsicle#1826", "noah#5386"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global time_of_last_bingo
    global rolling_index

    guild = str(message.guild)
    msg = utils.emoji_free_text(message.content).lower()

    if not os.path.isdir("lists/" + guild):
        os.mkdir("lists/" + guild)
        await utils.reset_list(guild)
        await utils.reset_free_list(guild)

    if not os.path.isdir("output_folder/" + guild):
        os.mkdir("output_folder/" + guild)
        await regenerate_all_images(guild)

    if message.author == client.user:
        return

    elif msg.startswith('$bingo'):

        time_since_last_bingo = time.time() - time_of_last_bingo

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + guild + '/output_' + str(rolling_index) + '.jpg')
            await message.reply(utils.random_animal_emoji(), file=img)

            await regenerate_images(rolling_index, guild)

            print('image generated for ' + guild)

            rolling_index = (rolling_index + 1) % 5
            time_of_last_bingo = time.time()

        else:
            print("bingo command recieved in " + guild + " too soon to generate!")

    elif msg.startswith('$bigbingo'):

        time_since_last_bingo = time.time() - time_of_last_bingo

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + guild + '/big_output_' + str(rolling_index) + '.jpg')
            await message.reply(utils.random_animal_emoji(), file=img)

            await regenerate_big_images(rolling_index, guild)

            print('big image generated for ' + guild)

            rolling_index = (rolling_index + 1) % 5
            time_of_last_bingo = time.time()

        else:
            print("big bingo command recieved in " + guild + " too soon to generate!")

    elif msg.startswith('$8ball'):
        await message.channel.send(utils.random_8ball_response())

    elif msg.startswith('$add'):
        line = utils.emoji_free_text(msg.split("$add ", 1)[1])
        await message.channel.send("New line: \n_" + line + "_ \nAdded to pool!")
        await utils.add_to_list(line, guild)
        print("New line: _" + line + "_ Added to pool in " + guild + " by " + str(message.author))

    elif msg.startswith('$freeadd'):
        line = msg.split("$freeadd ", 1)[1]
        await message.channel.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line, guild)
        print("New line: _" + line + "_ Added to free space pool in " + guild)

    elif msg.startswith('$refresh'):
        # regenerate all images
        await regenerate_all_images(guild)
        await message.channel.send("Cards refreshed!")

    elif msg.startswith('$bigrefresh'):
        # regenerate all big images
        await message.channel.send("This might take a while...")
        await regenerate_all_big_images(guild)
        await message.channel.send("Big cards refreshed!")

    elif msg.startswith('$list'):
        lines = await utils.list_all_lines(guild)

        for line in lines:
            line = ' '.join(line).lstrip()
            await message.channel.send(line, delete_after=20)

    elif msg.startswith('$freelist'):
        lines = await utils.list_all_free_lines(guild)

        for line in lines:
            line = ' '.join(line).lstrip()
            await message.channel.send(line, delete_after=20)

    elif msg.startswith('$del'):
        argument = msg.split("$del ", 1)[1]
        try:
            index = int(argument)
            await utils.delete_line(index, guild)
            await message.channel.send("deleted line: " + str(index))
        except:
            await message.reply(argument + " is not an integer you dingus!")

    elif msg.startswith('$freedel'):
        argument = msg.split("$freedel ", 1)[1]
        try:
            index = int(argument)
            await utils.delete_free_line(index, guild)
            await message.channel.send("deleted free space line: " + str(index))
        except:
            await message.reply(argument + " is not an integer you dingus!")

    elif msg.startswith('$resetlist'):
        await utils.reset_list(guild)
        await message.channel.send("List has been reset to default.")

    elif msg.startswith('$resetfreelist'):
        await utils.reset_free_list(guild)
        await message.channel.send("Free list has been reset to default.")

    elif msg.startswith('$animal'):
        await message.reply(utils.random_animal_emoji())

    elif msg.startswith("$id") and str(message.author) in whitelist:
        guild_id = message.guild.id
        channel_id = message.channel.id
        await message.reply(str(guild_id) + "\n" + str(channel_id))

    elif msg.startswith('$msg') and str(message.author) in whitelist:
        content = msg.split("msg ", 1)[1]
        msg = content.split("]", 1)[1].lstrip()
        channel_id = content.split("]", 1)[0].lstrip("[")
        channel = client.get_channel(int(channel_id))
        await channel.send(msg)

    elif msg.startswith('$status') and str(message.author) in whitelist:

        content = msg.split("$status ", 1)[1]
        activity_type = content.split(" ", 1)[0]
        url = ""
        if activity_type == "streaming":
            activity = content.split(" ", 1)[1].rsplit(" ", 1)[0]
            url = content.split(" ")[-1]
        else:
            url = ""
            activity = content.split(" ", 1)[1]

        await set_status(activity_type, activity, url)
        
    elif msg.startswith("$help"):
        await message.channel.send("\n**Current commands:** \n\n"
                                   "**$bingo** \n_generates a random bingo card_\n"
                                   "**$bigbingo** \n_generates a random big bingo card_\n"
                                   "**$list** \n_lists all statements in pool with index_\n"
                                   "**$freelist** \n_lists all statements in free pool with index_\n"
                                   "**$del** [integer index] \n_deleted statement at index_\n"
                                   "**$freedel** [integer index] \n_deletes statement at index in free list_\n"
                                   "**$add** [bingo statement] \n_adds statement to list_\n"
                                   "**$freeadd** [free space statement] \n_adds statements to free list_\n"
                                   "**$refresh** \n_refreshes bingo card pool (use after adding new statements)_\n"
                                   "**$bigrefresh** \n_refreshes big bingo card pool_\n"
                                   "**$animal**\n " + utils.random_animal_emoji() + "\n"
                                   "**$8ball**\n \n_ask the great BingoBot for wisdom_\n"                                         
                                   "**$RESETLIST** \n_resets list to default. lost changes cannot be recovered_\n"
                                   "**$RESETFREELIST** \n_resets freelist to default. lost changes cannot be recovered_\n"
                                   "**$status** [activity type (watching, listening, playing, streaming)]"
                                                                                    " [activity] [url(streaming only)]"
                                                                                    "\n_sets status of bot."
                                                                                    " Note: resticted usage_\n")
        
    elif msg.startswith('$frog') and str(message.author) in whitelist:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=":frog:"))


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
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))

    elif activity_type == "playing":
        # Setting `Playing ` status
        await client.change_presence(activity=discord.Game(name=activity))

    elif activity_type == "streaming":
        # Setting `Streaming ` status
        await client.change_presence(activity=discord.Streaming(name=activity, url=url))

    elif activity_type == "listening":
        # Setting `Listening ` status
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))


client.run(os.getenv('BINGO_BOT_TOKEN'))
