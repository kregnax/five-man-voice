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


def can_user_play(author, userRateLimiter, cmdWords):
    now = int(time.time())
    if len(cmdWords) == 1 and cmdWords[0] == 'garbagewater':
        if 'garbagewater' not in userRateLimiter.keys():
            userRateLimiter['garbagewater'] = now
            return True, 0
        lastCmdTime = userRateLimiter['garbagewater']
        delta = now - lastCmdTime
        if delta < 120:
            return False, 120-delta
        userRateLimiter['garbagewater'] = now
        return True, 0
    id = int(author.id)
    if id == config.ADMIN_ID:
        return True, 0
    if author.id not in userRateLimiter.keys():
        userRateLimiter[author.id] = now
        return True, 0
    lastCmdTime = userRateLimiter[author.id]
    delta = now - lastCmdTime
    if delta < 15:
        return False, 15-delta
    userRateLimiter[author.id] = now
    return True, 0


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
