import time
start = time.time()
from rich import print
import os
import json
import importlib
import sys

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def getDirSize(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += getDirSize(entry.path)
    return total

plugins = os.listdir('plugins')
with open('compiler.json', 'r') as compiled:
    compilerJson = json.load(compiled)

for plugin in plugins:
    if not plugin in compilerJson['plugins']:
        if os.path.exists(f'plugins/{plugin}/index.py'):
            compilerJson['plugins'].update({plugin: {}})
            compilerJson['plugins'][plugin].update({'size': -1})
            with open('compiler.json', 'w') as f:
                json.dump(compilerJson, f, indent=4)

    if getDirSize(f'plugins/{plugin}') != compilerJson['plugins'][plugin]['size']:
        print(f'Compiling plugin "{plugin}"...')
        if os.path.exists(f'plugins/{plugin}/commands.json'):
            with open(f'plugins/{plugin}/commands.json') as data:
                commandsJson = json.load(data)

            for commandName in commandsJson:
                command = commandsJson[commandName]
                if 'callString' in command and 'formatting' in command and 'source' in command and 'function' in command:
                    compilerJson['commands'].update({commandName: {}})
                    compilerJson['commands'][commandName].update({'callString': command['callString']})
                    compilerJson['commands'][commandName].update({'formatting': command['formatting']})
                    if 'description' in command:
                        compilerJson['commands'][commandName].update({'description': command['description']})
                    compilerJson['commands'][commandName].update({'source': command['source']})
                    compilerJson['commands'][commandName].update({'function': command['function']})
        compilerJson['plugins'][plugin]['size'] = int(getDirSize(f'plugins/{plugin}'))
        with open('compiler.json', 'w') as f:
            json.dump(compilerJson, f, indent=4)

end = time.time()
print(round(end - start, 3))