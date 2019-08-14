import click
import shlex
import subprocess
from pathlib import Path

@click.command()
@click.option('--input', '-i', default='ls -a',
              help="Type stdin linux shell command,\n"
                                                     "A command with multiple parameters should be in quotation marks, example: 'ls -a'")
@click.option('--grep', '-g', default='.',
              help="Type any key word you wonna find,\n"
                                                "A multiple strig should be in quotation marks example: 'find me'")
@click.option('--color', '-c', default='red',
              help="insert color")

@click.option('--underline', is_flag=True,
              help="add text underline")

def cli(input, grep, color, underline):
        if input == 'history':
                home = str(Path.home())
                with open(home + '/.bash_history', 'r') as file:
                        output = file.read()
                print_match_lines(output, grep, color,underline)
        else:
            try:
                input = shlex.split(input)
                output = subprocess.check_output(input).decode('ascii')
                print_match_lines(output, grep, color, underline)
            except:
                # This will check for any exception and then execute this print statement
                print("Error: Could not find file or read data")

def print_match_lines(output, grep, color, underline):
    output = iter(output.splitlines())
    for i in output:
        if greps(i, grep, color, underline) != None:
            print(greps(i, grep, color, underline))

def greps(word, find, color, underline):
    for x in range(len(word) - len(find) + 1):
        if find[0] == word[x]:
            for i in range(len(find)):
                if find[i] != word[x + i]:
                    break
            else:
                if i + 1 == len(find):
                    word = word.replace(word[x + i - len(find) + 1:x + i + 1], style(word[x + i - len(find) + 1:x + i + 1], color, underline))
                return word

def style(txt, color, underline):
       return click.style(f'{txt}', fg=color, underline=underline)
