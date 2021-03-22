import discord
from discord.ext import commands
import config
from time import sleep
import loader

CLIENT = discord.Client()

bot = commands.Bot(command_prefix="!",
                   description="Plays voicelines to delight the people")

userRateLimiter = {}
chanDict = {}


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user))
    chanDict = loader.make_chan_dictionary(bot)


@bot.command()
async def voice(ctx, *msg: str):
    cmdWords = msg[0:2]
    if cmdWords[0] == 'help':
        await ctx.send(loader.get_help_string())
        return
    if len(cmdWords) > 2:
        return
    if not ctx.author.voice:
        await ctx.author.send('You have to be in a voice channel to try and play an audio file, genius.')
        return
    canPlay, timeLeft = loader.can_user_play(
        ctx.author, userRateLimiter, cmdWords)
    if not canPlay:
        await ctx.author.send('Get rate-limited, idiot. Wait {} seconds.'.format(timeLeft))
        return
    channel = ctx.author.voice.channel
    vc = ctx.voice_client  # We use it more than once, so make it an easy variable
    if vc:
        if vc.is_playing():
            return
        if vc.channel != channel:
            await ctx.voice_client.disconnect()
            await channel.connect()
            vc = ctx.voice_client
    else:
        await channel.connect()
        vc = ctx.voice_client
    loader.play_file(cmdWords, vc)


@bot.command()
async def request(ctx):
    await ctx.author.send('lol no')


@bot.command()
async def reloadlines(ctx):
    if id == config.ADMIN_ID:
        nested, flattened = loader.get_voice_commands()
        loader.setNewLookups(nested, flattened)


@bot.command()
async def addline(ctx, *msg: str):
    if ctx.author.id == config.ADMIN_ID:
        loader.add_to_db(msg)


bot.run(config.BOT_KEY)
