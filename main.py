# INITIALIZATION
import time
loadingStart = time.time()
from rich import print
import os
import json
import importlib
import sys

## IL FAUT AJOUTER LES VALEURS DES PARAMETRES OPTIONNEL EN NULL (SINON MARCHE PAS)
## IL FAUT AJOUTER LES VALEURS DES PARAMETRES OPTIONNEL EN NULL (SINON MARCHE PAS)
## IL FAUT AJOUTER LES VALEURS DES PARAMETRES OPTIONNEL EN NULL (SINON MARCHE PAS)

#  - Optional Argument **(WIP)**
#  - Math Detection and Result **(WIP)**


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
compilerJsonPath = 'system/compiler.json'

with open(compilerJsonPath, 'r') as compiled:
    compilerJson = json.load(compiled)

compilationStart = time.time()

pluginConflicts = [i.split('/')[0] for i in compilerJson['conflicts'].keys()]

# This 3 line prevent keeping conflicts alive without reasons
compilerJson['conflicts'] = {}
with open(compilerJsonPath, 'w') as f:
    json.dump(compilerJson, f, indent=4)

for plugin in plugins:

    # Define new plugin
    if not plugin in compilerJson['plugins']:
        if os.path.exists(f'plugins/{plugin}/index.py'):
            compilerJson['plugins'].update({plugin: {}})
            compilerJson['plugins'][plugin].update({'size': -1})
            with open(compilerJsonPath, 'w') as f:
                json.dump(compilerJson, f, indent=4)

    # Compiling
    if getDirSize(f'plugins/{plugin}') != compilerJson['plugins'][plugin]['size'] or plugin in pluginConflicts:
        print(f'Compiling plugin "{plugin}"...')

        # Command
        if os.path.exists(f'plugins/{plugin}/commands.json'):

            commandsAddition = {}

            with open(f'plugins/{plugin}/commands.json') as data:
                commandsJson = json.load(data)

            for commandName in commandsJson:
                command = commandsJson[commandName]

                conflict = False       
                # Conflict detection         
                for i in range(len(compilerJson['commands'])):
                    incompatibilityPathName = f"{plugin}/{list(compilerJson['commands'].values())[i]['pluginName']}"
                    
                    if not list(compilerJson['commands'].values())[i]['pluginName'] == plugin:
                        # Command name
                        if list(compilerJson['commands'].keys())[i] == commandName:
                            if not incompatibilityPathName in compilerJson['conflicts']:
                                compilerJson['conflicts'].update({incompatibilityPathName: {
                                    "callStrings": [], "commandNames": []
                                }})
                            if not commandName in compilerJson['conflicts'][incompatibilityPathName]['commandNames']:
                                compilerJson['conflicts'][incompatibilityPathName]['commandNames'].append(commandName)
                            conflict = True
                        # CallString
                        if list(compilerJson['commands'].values())[i]['callString'] == command['callString']:
                            if not incompatibilityPathName in compilerJson['conflicts']:
                                compilerJson['conflicts'].update({incompatibilityPathName: {
                                    "callStrings": [], "commandNames": []
                                }})
                            if not command['callString'] in compilerJson['conflicts'][incompatibilityPathName]['callStrings']:
                                compilerJson['conflicts'][incompatibilityPathName]['callStrings'].append(command['callString'])
                            conflict = True

                if not conflict:
                    if 'callString' in command and 'formatting' in command and 'source' in command and 'function' in command:
                            commandsAddition.update({commandName: {}})
                            commandsAddition[commandName].update({
                                "callString": command['callString'],
                                "formatting": command['formatting'],
                                "source": f'plugins/{plugin}/{command["source"]}',
                                "function": command['function'],
                                "pluginName": plugin
                            })
                            if 'description' in command:
                                commandsAddition[commandName].update({"description": command['description']})
            compilerJson['commands'].update(commandsAddition)



        compilerJson['plugins'][plugin]['size'] = int(getDirSize(f'plugins/{plugin}'))
        with open(compilerJsonPath, 'w') as f:
            json.dump(compilerJson, f, indent=4)
pluginConflicts = [i.split('/')[0] for i in compilerJson['conflicts'].keys()]
compilationEnd = time.time()

loadingEnd = time.time()

# SAVING INFORMATIONS ABOUT LOADING TIME
with open(f'system/informations.json') as data:
    informationsJson = json.load(data)

informationsJson['lastTotalLoadingTime'] = loadingEnd - loadingStart
informationsJson['lastCompilingTime'] = compilationEnd - compilationStart

with open(f'system/informations.json', 'w') as data:
    json.dump(informationsJson, data, indent=4)

# TOP NOTIFICATIONS

cls()
notifications = [
    "[#568ebf]Welcome to the demo 🎉[/#568ebf]"
]
for notification in notifications:
    print(notification)
print('')


# COMMAND PROMPT
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
        pluginToPop = []
        commandsToPop = []
        for command in compilerJson['commands']:

            # Check if a callString is here
            if 'callString' in compilerJson['commands'][command]:
                
                # If this the callString we're searching
                callStringSearched = compilerJson['commands'][command]['callString'] if isinstance(compilerJson['commands'][command]['callString'], list) else [compilerJson['commands'][command]['callString']]
                if callstring in callStringSearched:

                    # Check if the plugin still existing lol
                    if compilerJson['commands'][command]['pluginName'] in plugins or compilerJson['commands'][command]['pluginName'] == '/system':
                        # Check if the command isnt in conflict
                        if not compilerJson['commands'][command]['pluginName'] in pluginConflicts:
                            targetCommand = compilerJson['commands'][command]
                            break
                    else:
                        pluginToPop.append(command)
                        commandsToPop.append(command)

        for plugin in pluginToPop:
            compilerJson['plugins'].pop(compilerJson['commands'][plugin]['pluginName'], None)
        for command in commandsToPop:
            compilerJson['commands'].pop(command, None)

        with open(compilerJsonPath, 'w') as f:
            json.dump(compilerJson, f, indent=4)

    if targetCommand != {}:
        try:
            names = []
            types = []
            optionals = []
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
                optional = True if part[1] == "!" else False
                between = part[1 + (1 if optional else 0):-1]
                if start+end in list(typesDictionary.keys()):
                    detectedType = list(typesDictionary.values())[list(typesDictionary.keys()).index(start+end)]
                    if len(between) > 0:
                        types.append(detectedType)
                        names.append(between)
                        optionals.append(optional)
                    else:
                        error = True
                        break
                else:
                    error = True
                    break

            if error:
                print('[red]Command formatting is incorrect, that\'s not you\'re fault[/red]')
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
                if not len(finalTypes) >= optionals.count(False) and len(finalTypes) <= (optionals.count(False) + optionals.count(True)):
                    errorOn = f'[red]{len(finalTypes)} arguments we\'re given, but {len(types)} we\'re needed[/red]'

                # VERIFY IF STRING ARE CORRECT
                for string in [index for index, chaine in enumerate(finalTypes) if chaine == "STRING"]:
                    if '"' in finalCommand[string]:
                        if finalCommand[string].count('"') != 2 or finalCommand[string][-1] != '"':
                            errorOn = f'[red]Argument {string+1} string is not valid[/red]'
                if errorOn == 'Null':
                    if ' '.join(finalCommand).count('"')%2 != 0:
                        errorOn = f'String sequence not closed'

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
                            try:
                                function(*finalCommand)
                            except Exception as err:
                                print(f'[red]An error occurred during execution: {err}.[/red]')
                else:
                    print(errorOn)
        except Exception as err:
            print(f'[red]Unknown error during execution, please share to jamesfrench_ on discord: {err}[/red]')

    else:
        print('[red]Command does not exist[/red]')
    print('')