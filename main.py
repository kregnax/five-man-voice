import discord
from discord.ext import commands
import config
from time import sleep
import loader
import helper

CLIENT = discord.Client()

bot = commands.Bot(command_prefix="!",
                   description="Plays voicelines to delight the people")

userRateLimiter = {}


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user))


@bot.command()
async def voice(ctx, *msg: str):
    cmdWords = msg[0:2]
    if cmdWords[0] == 'help':
        await ctx.send(helper.get_help_string())
        return
    if not ctx.author.voice:
        await ctx.author.send('You have to be in a voice channel to try and play an audio file, genius.')
        return
    if not helper.can_user_play(ctx.author, userRateLimiter):
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
    helper.play_file(cmdWords, vc)

bot.run(config.BOT_KEY)
