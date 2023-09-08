## Define basics informations and librarys for the code ^-^
import json
import os
import sys
import time
import importlib
class fonc:
    with open('resources/config.json', 'r') as config:
        data = json.load(config)

    global clear
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def configGet(name):
        return fonc.data[name]
    
    ## Example, convert string like this : importantString > Important String
    def betterName(name):
        result = ""
        name = name[0].upper() + name[1:]
        for i in range(len(name)):
            if name[i].isupper() and i != 0:
                result = f'{result} {name[i]}'
            else:
                result = f'{result}{name[i]}'
        return result
    
    ## Example, convert string like this : 'Hi! it\'s "cool cool" to see u' > ['Hi!','it\'s','"cool cool"','to','see','u']
    def stringSlice(string):
        string = string.split()

        working = ""
        result = []
        statut = False

        for word in string:
            if word.startswith('"') and word.endswith('"') and len(word) > 1:
                result.append(word)
            elif word.startswith('"') and not word.endswith('"'):  
                statut = True
                working = word
            elif word.endswith('"'):
                working = f"{working} {word}"
                statut = False
                result.append(working)
                working = ""
            else:
                if statut:
                    working = f"{working} {word}"
                else:
                    result.append(word)
        if not statut:
            return result
        else:
            return "¤"

clear()
color = fonc.configGet("color")
username = fonc.configGet("username")

validLibrary = False
while not validLibrary:
    try:
        from rich import print
        validLibrary = True
    except:
        os.system("pip install rich")

pluginPath = 'plugins'
plugins = [file for file in os.listdir(pluginPath) if file.endswith(".py")]
topInformations = ["[green]Welcome to the demo <3[/green]"]
if os.name != "nt":
    topInformations.append("[red]Asap is not yet tested on any OS other than Windows ~_~[/red]")

class commands:
    def addCommandError(commandID,reason,source):
        commands.commandError.append(commandID)
        commands.commandErrorDescription.append(reason)
        commands.commandErrorSource.append(source)

    def addCommand(commandID,formatting,source,commandDescription):
        commands.commandID.append(commandID)
        commands.formatting.append(formatting)
        commands.callName.append(formatting)
        commands.source.append(source)
        commands.commandDescription.append(commandDescription)


    callName = []
    formatting = []
    source = []
    commandID = []
    commandDescription = []

    commandError = []
    commandErrorDescription = []
    commandErrorSource = []

## Compiling Plugins
class pluginCompiling:  
    for plugin in plugins:
        source = importlib.import_module(f'{pluginPath}.{plugin[:-3]}')
        
        ## Compiling Command
        if hasattr(source, "commands"):
            global classCommands
            classCommands = getattr(source, "commands")
            functions = [func for func in dir(classCommands) if callable(getattr(classCommands, func)) and not func.startswith("__")]
            variables = [attr for attr in dir(classCommands) if not callable(getattr(classCommands, attr)) and not attr.startswith("__")]

            ## Avec toutes les fonctions de la classe "commands"
            for function in functions:

                # Si la fonction à une variable localisé dans "commands"
                if f'{function}Config' in variables:
                    commandConfig = getattr(classCommands, variables[variables.index(f'{function}Config')])

                    if len(commandConfig) > 0 and len(commandConfig) < 3 or not type(commandConfig) is list:
                        if type(commandConfig) is list:
                            formatting = commandConfig[0]
                        else:
                            formatting = commandConfig
                        if len(commandConfig) == 2:
                            description = commandConfig[1]
                        else:
                            description = "¤"
                        
                        if len(formatting) > 0:
                            commands.addCommand(function,formatting,plugin[:-3],description)
                        elif len(formatting) < 1:
                            commands.addCommandError(function, "Empty Format, CallName unavailable", plugin[:-3])

                else:
                    ## Et BAM, fallait mettre une variable
                    commands.addCommandError(function, f"Variable {function}Config not found", plugin[:-3])

for error in range(len(commands.commandError)):
    print(f"[red]plugins.{commands.commandErrorSource[error]}.commands.{commands.commandError[error]} - {commands.commandErrorDescription[error]}[/red]")
    print("")

for command in range(len(commands.commandID)):
    print(f"[blue]{commands.commandID[command]} :[/blue]")
    print(f"[blue]plugins.{commands.source[command][:-3]}.commands.{commands.commandID[command]}[/blue]")
    print(f"[blue]{commands.formatting[command]} - {commands.commandDescription[command]}  [/blue]")
    print("")
