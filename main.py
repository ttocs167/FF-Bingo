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

    if message.author == client.user:
        return

    if message.content.startswith('$bingo'):

        time_since_last_bingo = time.time() - time_of_last_bingo

        if time_since_last_bingo > 0.5:
            img = discord.File('output_folder/output_' + str(rolling_index) + '.png')
            await message.channel.send(utils.random_animal_emoji(), file=img)

            await regenerate_images(rolling_index)

            print('image generated!')

            rolling_index = (rolling_index + 1) % 5
            time_of_last_bingo = time.time()

        else:
            print("bingo command recieved, too soon to generate!")

    if message.content.startswith('$add'):
        line = message.content.split("$add ", 1)[1]
        await message.channel.send("New line: \n_" + line + "_ \nAdded to pool!")
        await utils.add_to_list(line)
        print("New line: _" + line + "_ Added to pool!")

    if message.content.startswith('$addfree'):
        line = message.content.split("$addfree ", 1)[1]
        await message.channel.send("New line: \n_" + line + "_ \nAdded to free space pool!")
        await utils.add_to_free_list(line)
        print("New line: _" + line + "_ Added to free space pool!")

    if message.content.startswith('$refresh'):
        # regenerate all images
        await regenerate_all_images()
        await message.channel.send("Cards refreshed!")

    if message.content.startswith('$animal'):
        await message.channel.send(utils.random_animal_emoji())

    if message.content.startswith('$list'):
        lines = await utils.list_all_lines()
        await message.channel.send(lines)

    if message.content.startswith('$listfree'):
        lines = await utils.list_all_free_lines()
        await message.channel.send(lines)

    if message.content.startswith('$del'):
        argument = message.content.split("$del ", 1)[1]
        try:
            index = int(argument)
            await utils.delete_line(index)
            await message.channel.send("deleted line: " + str(index))
        except:
            await message.channel.send(argument + " is not an integer you dingus!")

    if message.content.startswith('$delfree'):
        argument = message.content.split("$delfree ", 1)[1]
        try:
            index = int(argument)
            await utils.delete_free_line(index)
            await message.channel.send("deleted free space line: " + str(index))
        except:
            await message.channel.send(argument + " is not an integer you dingus!")

    if message.content.startswith('$RESETLIST'):
        await utils.reset_list()
        await message.channel.send("List has been reset to default.")

        
async def regenerate_images(index):
    generate_card(index)


async def regenerate_all_images():
    generate_card(0, 5)
    print("ALL CARDS REGENERATED")

client.run(os.getenv('BINGO_BOT_TOKEN'))
