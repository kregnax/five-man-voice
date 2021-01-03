import json

VOICE_COMMANDS_JSON_PATH = "voice_commands_alias.json"


def get_voice_commands_json():
    with open(VOICE_COMMANDS_JSON_PATH) as json_file:
        nestedCmds = json.load(json_file)
    flattenedAliasCmd = get_flattened_alias_dict(nestedCmds)
    return nestedCmds, flattenedAliasCmd


def get_flattened_alias_dict(voiceCMDAlias):
    flattenedAliasDict = {}
    for category in voiceCMDAlias:
        for alias in voiceCMDAlias[category]:
            flattenedAliasDict[alias] = '{0}/{1}'.format(
                category, voiceCMDAlias[category][alias])
    return flattenedAliasDict


def get_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def get_voice_command_help(voice_commands):
    commands = 'Available voice lines:\n'
    for category in voice_commands.keys():
        commands += '\t__{}__\n'.format(category)
        for alias in voice_commands[category].keys():
            commands += '\t\t{} : {}\n'.format(alias,
                                               voice_commands[category][alias])
    commands += ("```Typing `!voice` followed by a category (e.g. `!voice genji`) will " +
                 "play a random file from that category. To play a specific file, type " +
                 "`!voice` followed by the alias of the file. `!voice worst` will play " +
                 "'This game is the worst game ever designed'```")
    return commands
