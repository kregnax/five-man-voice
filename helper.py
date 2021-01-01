import discord
import time
from datetime import datetime, timedelta
import loader

voiceCMDAlias = loader.get_voice_commands_json()


def get_filepath_from_command(cmdWords):
    try:
        voiceLine = voiceCMDAlias[cmdWords[0]]['filename'][cmdWords[1]]
        return './.voice_lines/{0}/{1}'.format(cmdWords[0], voiceLine)
    except:
        return 'ERROR'


def get_help_string():
    return loader.get_voice_command_help(voiceCMDAlias)


def play_file(cmdWords, vc):

    filePath = get_filepath_from_command(cmdWords)
    # Lets play that mp3 file in the voice channel
    if vc.is_playing():
        return
    vc.play(discord.FFmpegPCMAudio(filePath))
    # Lets set the volume to 0.5
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0.5


def can_user_play(author, userRateLimiter):
    if author.server_permissions.administrator:
        return True
    now = int(time.time())
    if author.id not in userRateLimiter.keys():
        userRateLimiter[author.id] = now
        return True
    lastCmdTime = userRateLimiter[author.id]
    delta = now - lastCmdTime
    if delta < 15:
        return False
    userRateLimiter[author.id] = now
    return True
