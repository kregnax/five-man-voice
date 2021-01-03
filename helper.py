import discord
import time
from datetime import datetime, timedelta
import loader
import config

voiceCMDAlias, flattenedAlias = loader.get_voice_commands_json()


def get_filepath_from_command(cmdWords):
    fullPath = './.voice_lines/{path}'
    if len(cmdWords) == 1:
        return fullPath.format(path=flattenedAlias[cmdWords[0]])
    elif len(cmdWords) == 2:
        return fullPath.format(path=cmdWords[0]+'/'+voiceCMDAlias[cmdWords[0]][cmdWords[1]])
    else:
        return 'ERROR'


def get_help_string():
    return loader.get_voice_command_help(voiceCMDAlias)


def play_file(cmdWords, vc):
    filePath = get_filepath_from_command(cmdWords)
    # Lets play that mp3 file in the voice channel
    if vc.is_playing() or filePath == 'ERROR':
        return
    vc.play(discord.FFmpegPCMAudio(filePath))
    # Lets set the volume to 0.5
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 0.5


def can_user_play(author, userRateLimiter):
    id = int(author.id)
    if id == config.ADMIN_ID:
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


def make_chan_dictionary(bot):
    channels = {
        "text": [],
        "voice": []
    }
    for c in bot.get_all_channels():
        if c.category is not None:
            if c.category is not None and c.category.name == 'Text Channels':
                channels['text'].append(tuple([c.id, c.name]))
            elif c.category is not None and c.category.name == 'Voice Channels':
                channels['voice'].append(tuple([c.id, c.name]))
    return channels
