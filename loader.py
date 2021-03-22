import json
import sqlite3
import time
import discord
import config

from enum import Enum

VOICE_COMMANDS_JSON_PATH = "voice_commands_alias.json"
DB_NAME = "../voice-line-alias"

con = sqlite3.connect(DB_NAME)
cur = con.cursor()


class Column():
    ID = 0
    CATEGORY = 1
    COMMAND = 2
    FILE = 3


class Alias():
    nestedAlias = {}
    flattenedAlias = {}


def get_voice_commands():
    cur.execute("SELECT DISTINCT category FROM alias")
    cats = cur.fetchall()
    nestedAlias = {}
    for row in cats:
        nestedAlias[row[0]] = {}
    flattenedAlias = {}
    column = Column
    cur.execute("SELECT * FROM alias")
    rows = cur.fetchall()
    for row in rows:
        flattenedAlias[row[column.COMMAND]
                       ] = '{}/{}'.format(row[column.CATEGORY], row[column.FILE])
        nestedAlias[row[column.CATEGORY]
                    ][row[column.COMMAND]] = row[column.FILE]
    return nestedAlias, flattenedAlias


alias = Alias
voiceCMDAlias, flattenedAlias = get_voice_commands()
alias.flattenedAlias = flattenedAlias
alias.nestedAlias = voiceCMDAlias


def get_voice_command_help(voice_commands):
    commands = 'Available voice lines:\n'
    for category in voice_commands.keys():
        commands += '\t__{}__\n'.format(category)
        for alias in voice_commands[category].keys():
            commands += '\t\t{} : {}\n'.format(alias,
                                               voice_commands[category][alias])
    commands += ("```Type `!voice` followed by the alias of the file. `!voice worst` will play " +
                 "'This game is the worst game ever designed'```")
    return commands


def add_to_db(msg):
    cmd = "INSERT INTO alias (category, command, file) VALUES ('{}','{}','{}')".format(
        msg[0], msg[1], msg[2])
    cur.execute(cmd)
    nested, flattened = get_voice_commands()
    setNewLookups(nested, flattened)


def setNewLookups(nested, flattened):
    alias.nestedAlias = nested
    alias.flattenedAlias = flattened


def get_filepath_from_command(cmdWords):
    fullPath = './.voice_lines/{path}'
    if len(cmdWords) == 1:
        return fullPath.format(path=alias.flattenedAlias[cmdWords[0]])
    elif len(cmdWords) == 2:
        return fullPath.format(path=cmdWords[0]+'/'+alias.nestedAlias[cmdWords[0]][cmdWords[1]])
    else:
        return 'ERROR'


def get_help_string():
    return get_voice_command_help(alias.nestedAlias)


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
