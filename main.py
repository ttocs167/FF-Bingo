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

            rolling_index = (rolling_index + 1) % 20
            time_of_last_bingo = time.time()

        else:
            print("bingo command recieved, too soon to generate!")

    if message.content.startswith('$animal'):
        await message.channel.send(utils.random_animal_emoji())


async def regenerate_images(index):
    generate_card(index)


client.run(os.getenv('BINGO_BOT_TOKEN'))
