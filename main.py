from keep_alive import keep_alive
import discord
import os
import requests
import json
from wit import Wit
import logging

access_token = os.getenv('WIT_TOKEN')
wit_client = Wit(access_token)
wit_client.logger.setLevel(logging.WARNING)
logger = logging.getLogger()

client = discord.Client()


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    print("response: ", json_data)
    return (quote)


def get_insult():
    response = requests.get(
        "https://evilinsult.com/generate_insult.php?lang=en&type=json")
    print(response.text)
    json_data = json.loads(response.text)
    quote = json_data['insult']
    return (quote)


def get_wit_message(wit_message):
    print('just trying to show something, boys, boys, boys: ' +
          str(wit_message))
    resp = wit_client.message(wit_message)
    print('Yay, got Wit.ai response: ' + str(resp))
    return (resp)


@client.event
async def on_ready():
    print('we have logged in  {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, user):
    print('reaction: ' + str(reaction))
    print('reaction author: ' + str(reaction.message.author))
    print('client.user: ' + str(client.user))
    print('is this true: ' + str((reaction.emoji == '💩' or reaction.emoji == '👎🏿') and (reaction.message.author != client.user)))
    if (reaction.emoji == '💩' or reaction.emoji == '👎🏿') and (reaction.message.author != client.user):
        print('this worked with the unicode')
        insult = get_insult()
        await reaction.message.channel.send(reaction.message.author.mention + ' ' + insult)
        print('done')

@client.event
async def on_message(message):
    discord_message = message.content
    # discord_chat = get_wit_message(discord_message)

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("what's goodie")

    if message.content.startswith('$insult'):
        insult = get_insult()
        await message.channel.send(insult)

    if message.content.startswith('$what is'):
        message = get_wit_message(discord_message)

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

# client.run(os.getenv('TOKEN'))
TOKEN = os.getenv('TOKEN')
keep_alive()
client.run(TOKEN)
