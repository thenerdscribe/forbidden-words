import os
import json
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

with open('words.json', 'r') as wordsfile:
    words = json.load(wordsfile)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


def get_key(val):
    for key, value in words.items():
        if val == value:
            return key


def save_word(author, word):
    words[author] = word
    with open('words.json', 'w') as wordsfile:
        json.dump(words, wordsfile)


@bot.command('myword', help="Claim your one word that is not allowed")
async def register_word(ctx, word: str):
    if word == '!myword':
        return
    author = ctx.author.name
    save_word(author, word)
    await ctx.send(f"{author}'s word is now {word}")


@bot.listen('on_message')
async def forbidden_word_check(message):
    split_up = message.content.lower().split(' ')
    if message.author.name != bot.user.name:
        for word in words.values():
            if word.lower() in split_up:
                if message.author.name != get_key(word):
                    user = message.author
                    role = get(message.guild.roles, name="jail")
                    await user.add_roles(role)
                    await message.delete()
                    await message.channel.send(f"{message.author} used a **FORBIDDEN** word")
                    break


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
