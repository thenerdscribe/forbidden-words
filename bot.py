import os
import json
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

with open('words.json', 'r') as wordsfile:
    words = json.load(wordsfile)

with open('score.json', 'r') as scorefile:
    score = json.load(scorefile)

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


def point_scored(user):
    if user not in score.keys():
        score[user] = 1       
    else:
        score[user] += 1
    
    with open('score.json', 'w') as scorefile:
        json.dump(score, scorefile)


@bot.command('myword', help="Claim your one word that is not allowed")
async def register_word(ctx, word: str):
    word = str.lower(word)
   
    with open('safe_words.txt', 'r') as safeword_file:
        safe_words = safeword_file.read().splitlines()

    if word in safe_words:
        await ctx.send(f'Sorry {word} is a safe word and cannot be claimed.')
        return False

    author = ctx.author.name
    save_word(author, word)
    await ctx.send(f"{author}'s word is now {word}")


@bot.command('leaderboard', help="Show current score.")
async def show_board(ctx):
    msg = '''
===================
|  Current Score  |
===================
'''

    for player, cur_score in sorted(score.items(), key=lambda item: item[1], reverse=True):
        msg = f'{msg}\n{cur_score}  {player}'

    msg = f'```{msg}```'
    await ctx.send(msg)


@bot.listen('on_message')
async def forbidden_word_check(message):
    split_up = message.content.lower().split(' ')
    if message.author.name != bot.user.name:
        for word in words.values():
            if word.lower() in split_up:
                word_owner = get_key(word)
                if message.author.name != word_owner:
                    user = message.author
                    await message.channel.send(f"{message.author} used {word_owner}'s word.")
                    point_scored(word_owner)
                    break


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
