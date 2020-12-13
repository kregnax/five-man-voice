import discord
from discord.ext import commands
import config
from time import sleep

CLIENT = discord.Client()

bot = commands.Bot(command_prefix="!",
                   description="Plays voicelines to delight the people")


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user))


@bot.command()
async def join(ctx):

    channel = ctx.author.voice.channel
    await channel.connect()
    vc = ctx.voice_client  # We use it more then once, so make it an easy variable
    if not vc:
        # We are not currently in a voice channel
        await ctx.send('I need to be in a voice channel to do this, please use the connect command.')
        return
    try:
        # Lets play that mp3 file in the voice channel
        vc.play(discord.FFmpegPCMAudio('./airhorn.mp3'))
        # Lets set the volume to 1
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.5
        while vc.is_playing():
            sleep(.1)
        await vc.disconnect()
    except TypeError as e:
        print(f'TypeError exception:\n`{e}`')
        await ctx.send('Uh oh, Alan programmed something poorly. How surprising.')


@bot.command()
async def cmd(ctx, *msg):

    await ctx.send(msg)

bot.run(config.BOT_KEY)
