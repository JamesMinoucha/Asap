# INITIALIZATION
import time
loadingStart = time.time()
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
def colorTime(string, orangeStart, redStart, colors=['#86f576','#eef576','#f57c76']):
    return f'[{colors[0] if int(string) < orangeStart else colors[1] if int(string) < redStart else colors[2]}]{string}[{colors[0] if int(string) < orangeStart else colors[1] if int(string) < redStart else colors[2]}]'

# COMPILING
plugins = os.listdir('plugins')
with open('compiler.json', 'r') as compiled:
    compilerJson = json.load(compiled)

compilationStart = time.time()
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
                    compilerJson['commands'][commandName].update({'source': f'plugins/{plugin}/{command["source"]}'})
                    compilerJson['commands'][commandName].update({'function': command['function']})

        compilerJson['plugins'][plugin]['size'] = int(getDirSize(f'plugins/{plugin}'))
        with open('compiler.json', 'w') as f:
            json.dump(compilerJson, f, indent=4)
compilationEnd = time.time()

loadingEnd = time.time()

# COMMAND PROMPT
cls()
while True:
    command = input('>> ')



    # SHELL (COMMAND UNKNOWN AT THIS POINT)
    string = command
    splited = string.split()
    textSection = False
    mathSection = False
    sectionType = ''
    firstIndex = True
    section = ''
    result = []
    sectionsTypes = []
    callstring = ''
    for part in splited:
        for i in range(len(part)):
            if part[i] == '"' and part[i - 1] != '\\':
                textSection = (not textSection)
                sectionType = "STRING"
            if part[i] == '(' or part[i] == ')' and (not textSection):
                mathSection = (not mathSection)
                sectionType = "MATH"
            section = f'{section}{part[i]}'

        if (not textSection) and (not mathSection):
            if firstIndex and sectionType == '':
                sectionType = 'CALLSTRING'
                callstring = part
            elif part.lower() == 'false' or part.lower() == 'true' and sectionType == '':
                sectionType = 'BOOLEAN'
            elif sectionType == '' and part.isdigit():
                sectionType = 'NUMBER'
            elif sectionType == '':
                sectionType = 'STRING'

            sectionsTypes.append(sectionType)
            result.append(section)
            section = ''

        if textSection:
            section = f'{section} '
        firstIndex = False
        sectionType = ''
    
    # EXECUTION (TRYING TO FIND THE COMMAND)
    targetCommand = {}
    if callstring != '':
        for command in compilerJson['commands']:
            if 'callString' in compilerJson['commands'][command]:
                if isinstance(compilerJson['commands'][command]['callString'], list):
                    if callstring in compilerJson['commands'][command]['callString']:
                        targetCommand = compilerJson['commands'][command]
                        break
                else:
                    if callstring == compilerJson['commands'][command]['callString']:
                        targetCommand = compilerJson['commands'][command]
                        break


    if targetCommand != {}:
        try:
            names = []
            types = []
            error = False
            typesDictionary = {
                "[]": "STRING",
                "()": "NUMBER",
                "##": "BOOLEAN"
            }
            splitedCommandFormatting = targetCommand['formatting'].split()
            for part in splitedCommandFormatting:
                start = part[0]
                end = part[-1]
                between = part[1:-1]
                if start+end in list(typesDictionary.keys()):
                    detectedType = list(typesDictionary.values())[list(typesDictionary.keys()).index(start+end)]
                    if len(between) > 0:
                        types.append(detectedType)
                        names.append(between)
                    else:
                        error = True
                        break
                else:
                    error = True
                    break

            if error:
                print('[red]La commande entré comporte des erreurs, cela n\'est pas de votre faute[/red]')
            else:
                finalCommand = result[1:]
                finalTypes = sectionsTypes[1:]
                # CALCULATING MATH PART (UNSECURE FOR THE MOMENT)
                for math in [index for index, chaine in enumerate(finalTypes) if chaine == "MATH"]:
                    calcul = eval(finalCommand[math])
                    if str(calcul).isdigit():
                        finalCommand[math] = calcul
                        finalTypes[math] = 'NUMBER'

                # VERIFY IF ARGUMENT LENGTH IS OKAY
                errorOn = 'Null'
                if len(finalTypes) != len(types):
                    errorOn = f'[red]{len(finalTypes)} arguments we\'re given, but {len(types)} we\'re needed[/red]'

                # VERIFY ALL ARGUMENT TYPES
                if errorOn == 'Null':
                    for i in range(len(finalTypes)):
                        if finalTypes[i] != types[i]:
                            errorOn = f'[red]Argument {i+1} must be {types[i]}, but is {finalTypes[i]}[/red]'
                            break

                if errorOn == 'Null':
                    if os.path.exists(targetCommand['source']):
                        source = importlib.import_module(targetCommand['source'][:-3].replace('/','.'))
                        if hasattr(source,targetCommand['function']):
                            function = getattr(source,targetCommand['function'])
                            function(*finalCommand)
                else:
                    print(errorOn)
        except Exception as err:
            print(f'[red]Unknown error during execution, please share to jamesfrench_ on discord: {err}[/red]')

    else:
        print('[red]Commande introuvable[/red]')
    


print(f'Compiling: {colorTime(round(compilationEnd - compilationStart, 3),0.1,0.5)}')
print(f'Total: {colorTime(round(loadingEnd - loadingStart, 3),0.3,1)}')