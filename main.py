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

reaction_count = []


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def get_insult():
    response = requests.get(
        "https://evilinsult.com/generate_insult.php?lang=en&type=json")
    json_data = json.loads(response.text)
    quote = json_data['insult']
    return (quote)


def get_wit_message(wit_message):
    resp = wit_client.message(wit_message)
    return (resp)


@client.event
async def on_ready():
    print('we have logged in  {0.user}'.format(client))

@client.event
async def on_reaction_add(reaction, user):
    print('reaction count: ' + str(len(reaction_count)))
    # reaction_count = reaction.message.reactions
    if (reaction.emoji == '💩' or reaction.emoji == '👎🏿') and (reaction.message.author != client.user and len(reaction_count) < 1):
        reaction_count.append(reaction.emoji)
        insult = get_insult()
        print('reaction count 2: ' + str(len(reaction_count)))
        await reaction.message.channel.send(reaction.message.author.mention + ' ' + insult)

@client.event
async def on_message(message):
    if message.author != client.user:
        reaction_count.clear()
        
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
