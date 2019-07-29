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
def cli(input, grep):
        if input == 'history':
                home = str(Path.home())
                with open(home + '/.bash_history', 'r') as file:
                        output = file.read()
                print_match_lines(output, grep)
        else:
            try:
                input = shlex.split(input)
                output = subprocess.check_output(input).decode('ascii')
                print_match_lines(output, grep)
            except:
                # This will check for any exception and then execute this print statement
                print("Error: Could not find file or read data")

def print_match_lines(pss_output, pss_grep):
    pss_output = iter(pss_output.splitlines())
    for i in pss_output:
        if greps(i, pss_grep) != None:
            print(greps(i, pss_grep))

def greps(word, find):
    for x in range(len(word) - len(find) + 1):
        if find[0] == word[x]:
            for i in range(len(find)):
                if find[i] != word[x + i]:
                    break
            else:
                if i + 1 == len(find):
                    # word = word.replace(word[x + i - len(find) + 1:x + i + 1], word[x + i - len(find) + 1:x + i + 1].upper())
                    red = lambda text: '\033[0;31m' + text + '\033[0m'
                    word = word.replace(word[x + i - len(find) + 1:x + i + 1], red(word[x + i - len(find) + 1:x + i + 1]))
                return word
