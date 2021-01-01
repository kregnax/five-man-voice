import json

VOICE_COMMANDS_JSON_PATH = "voice_commands_alias.json"


def get_voice_commands_json():
    with open(VOICE_COMMANDS_JSON_PATH) as json_file:
        return json.load(json_file)


def get_json(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)

def get_voice_command_help(voice_commands):
    commands = 'Available voice lines:\n'
    for owner, v in voice_commands.items():
        commands += '\t__{}__\n'.format(owner)
        for ind, filenames in v.items():
            for alias, filename in filenames.items():
                commands += '\t\t{} : {}\n'.format(alias, filename)
    commands += ("```Typing `!voice` followed by a category (e.g. `!voice genji`) will " +
                 "play a random file from that category. To play a specific file, type " +
                 "`!voice` category followed by the alias of the file. `!voice genji become` will play " +
                 "'The Dragon Becomes Me!'```")
    return commands
