import discord
import os
from generate_cards import generate_card
import utils
import time
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
time_of_last_bingo = time.time()
rolling_index = 0


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global time_of_last_bingo
    global rolling_index

    guild = str(message.guild)
    msg = utils.emoji_free_text(message.content)
    
    if not os.path.isdir("output_folder/" + guild):
        os.mkdir("output_folder/" + guild)
        await regenerate_all_images(guild)

    if not os.path.isdir("lists/" + guild):
        os.mkdir("lists/" + guild)
        await utils.reset_list(guild)
        await utils.reset_free_list(guild)

    if message.author == client.user:
        return

    if msg.startswith('$bingo'):

        time_since_last_bingo = time.time() - time_of_last_bingo

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/' + guild + '/output_' + str(rolling_index) + '.png')
            await message.reply(utils.random_animal_emoji(), file=img)

            await regenerate_images(rolling_index, guild)

            print('image generated for ' + guild)

            rolling_index = (rolling_index + 1) % 5
            time_of_last_bingo = time.time()

        else:
            print("bingo command recieved in " + guild + " too soon to generate!")

    if msg.startswith('$add'):
        line = utils.emoji_free_text(msg.split("$add ", 1)[1])
        await message.channel.send("New line: \n_" + line + "_ \nAdded to pool!")
        await utils.add_to_list(line, guild)
        print("New line: _" + line + "_ Added to pool in " + guild)

    if msg.startswith('$addfree'):
        line = msg.split("$addfree ", 1)[1]
        await message.channel.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line, guild)
        print("New line: _" + line + "_ Added to free space pool in " + guild)

    if msg.startswith('$refresh'):
        # regenerate all images
        await regenerate_all_images(guild)
        await message.channel.send("Cards refreshed!")

    if msg.startswith('$list'):
        lines = await utils.list_all_lines(guild)
        await message.channel.send(lines, delete_after=10)

    if msg.startswith('$listfree'):
        lines = await utils.list_all_free_lines(guild)
        await message.channel.send(lines)

    if msg.startswith('$del'):
        argument = msg.split("$del ", 1)[1]
        try:
            index = int(argument)
            await utils.delete_line(index, guild)
            await message.channel.send("deleted line: " + str(index))
        except:
            await message.reply(argument + " is not an integer you dingus!")

    if msg.startswith('$delfree'):
        argument = msg.split("$delfree ", 1)[1]
        try:
            index = int(argument)
            await utils.delete_free_line(index, guild)
            await message.channel.send("deleted free space line: " + str(index))
        except:
            await message.reply(argument + " is not an integer you dingus!")

    if msg.startswith('$RESETLIST'):
        await utils.reset_list(guild)
        await message.channel.send("List has been reset to default.")

    if msg.startswith('$RESETFREELIST'):
        await utils.reset_free_list(guild)
        await message.channel.send("Free list has been reset to default.")

    if msg.startswith('$animal'):
        await message.reply(utils.random_animal_emoji())


async def regenerate_images(index, guild):
    generate_card(index, guild)


async def regenerate_all_images(guild):
    generate_card(0, guild, 5)
    print("ALL CARDS IN " + guild + " REGENERATED")

client.run(os.getenv('BINGO_BOT_TOKEN'))
