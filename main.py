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
debugMode = False

validLibrary = False
while not validLibrary:
    try:
        from rich import print
        validLibrary = True
    except:
        os.system("pip install rich")

pluginPath = 'plugins'
plugins = [file for file in os.listdir(pluginPath) if file.endswith(".py")]
topInformations = ["[green]Welcome to the Demo <3[/green]"]
if os.name != "nt":
    topInformations.append("[red]It seems you are not on Windows, Asap is not tested on your OS. Proceed at your own risk[/red]")

class intern:
    class commands:
        compiledPluginsConfig = ["plugins","Afficher les commandes compilers"]
        def compiledPlugins():
            print("Success compile")
            for command in range(len(cp.cmd.commandID)):  
                print(f"|[blue]    plugins.{cp.cmd.source[command][:-3]}.commands.{cp.cmd.commandID[command]}[/blue]")
                print(f"|[blue]    {cp.cmd.callName[command]} < {cp.cmd.formatting[command]} - {cp.cmd.commandDescription[command]}  [/blue]")
                print("|")

            print("Failed compile")
            for error in range(len(cp.cmd.commandError)):
                print(f"|[red]    plugins.{cp.cmd.commandErrorSource[error]}.commands.{cp.cmd.commandError[error]} - {cp.cmd.commandErrorDescription[error]}[/red]")
                print("|")


class cp:
    class cmd:
        def addCommandError(commandID,reason,source):
            cp.cmd.commandError.append(commandID)
            cp.cmd.commandErrorDescription.append(reason)
            cp.cmd.commandErrorSource.append(source)

        def addCommand(commandID,formatting,callName,source,commandDescription,baseSource):
            cp.cmd.commandID.append(commandID)
            cp.cmd.formatting.append(formatting)
            cp.cmd.callName.append(callName)
            cp.cmd.source.append(source)
            cp.cmd.commandDescription.append(commandDescription)
            cp.cmd.baseSource.append(baseSource)


        callName = ["plugins"]
        formatting = [[]]
        source = ["main.py"]
        commandID = ["compiledPlugins"]
        commandDescription = ["Afficher les commandes compilers"]
        baseSource = ["^"]

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

                    # Si la liste à de 1 à 2 élément, ou que c'est une simple variable
                    if len(commandConfig) > 0 and len(commandConfig) < 3 or not type(commandConfig) is list:

                        if len(commandConfig) > 0:
                            
                            try:
                                callName = commandConfig[0].split()[0] if type(commandConfig) is list else commandConfig.split()[0]
                                description = commandConfig[1] if len(commandConfig) == 2 and type(commandConfig) is list else "¤"
                                formatting = commandConfig[0].split()[1:] if type(commandConfig) is list else commandConfig.split()[1:]

                                # Compatibility IF
                                if not callName in cp.cmd.callName:
                                    cp.cmd.addCommand(function,formatting,callName,plugin,description,source)
                                else:
                                    cp.cmd.addCommandError(function, f"Is incompatible with plugins.{cp.cmd.source[cp.cmd.callName.index(callName)][:-3]}.commands.{cp.cmd.callName[cp.cmd.callName.index(callName)]}", plugin[:-3])
                            except:
                                cp.cmd.addCommandError(function, "Unkown error, please read documentation about Config", plugin[:-3])

                        else:
                            cp.cmd.addCommandError(function, "Format is empty, callName not found", plugin[:-3])
                    else:
                        cp.cmd.addCommandError(function, "The config is empty or wrong", plugin[:-3])

                else:
                    ## Variable format manquant
                    cp.cmd.addCommandError(function, f"Variable {function}Config not found", plugin[:-3])

for topInformation in topInformations:
    print(topInformation)
while True:
    print()
    command = input(">> ")
    command = command.lower()

    if command in cp.cmd.callName:
        index = cp.cmd.callName.index(command)
        source = intern() if cp.cmd.baseSource[index] == "^" else cp.cmd.baseSource[index]
        commandCall = getattr(getattr(source, "commands"), cp.cmd.commandID[index])
        commandCall()
