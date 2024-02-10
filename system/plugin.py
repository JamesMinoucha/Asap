from rich import print

def summonError(error='An error has occurred',pluginName=''):
    if error == 'An error has occurred' or error == '':
        print(f'[red]An error has occurred{f' with [bold]{pluginName}[/bold]' if pluginName != '' else ''}[/red]')
    else:
        print(f'[red]{f'[bold]{pluginName}[/bold]: ' if pluginName != '' else ''}{error}[/red]')