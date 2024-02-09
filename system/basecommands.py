import os
import json
from rich import print

def clear(*args):
    os.system('cls' if os.name == 'nt' else 'clear')

def loadingTimes(*args):
    def colorTime(string, orangeStart, redStart, colors=['#86f576','#eef576','#f57c76']):
        return f'[{colors[0] if int(string) < orangeStart else colors[1] if int(string) < redStart else colors[2]}]{string}[{colors[0] if int(string) < orangeStart else colors[1] if int(string) < redStart else colors[2]}]'
    with open(f'system/informations.json') as data:
        informationsJson = json.load(data)
    print(f'Compiling: {colorTime(round(informationsJson['lastCompilingTime'], 3),0.1,0.5)}')
    print(f'Total: {colorTime(round(informationsJson['lastTotalLoadingTime'], 3),0.3,1)}')