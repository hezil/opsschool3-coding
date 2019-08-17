import click
import os
import re
import shlex
import subprocess
from pathlib import Path

class Config(object):
    pass

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--machine', '-m', default='py',
              help="Type any key word you wonna find,\n"
                                                "A multiple strig should be in quotation marks example: 'find me'")
@click.option('--color', '-c', default='red',
              help="insert color")

@click.option('--underline', '-u', is_flag=True,
              help="add text underline")
@pass_config
def cli(config, machine, color, underline):
    config.machine = machine
    config.color = color
    config.underline = underline

@cli.command()
@click.argument('input')
@pass_config
def stdin(config, input):
    """
    this command accept stdin and print stdout e.g. shell commands

    examples:

    \b
    history:
    stdin history

    \b
    ls -a:
    stdin 'ls -a'

    \b
    NOTE:
        A command with multiple parameters should be in quotation marks, e.g. 'ls -a'

    """
    if input == 'history':
        home = str(Path.home())
        with open(home + '/.bash_history', 'r') as file:
            output = file.read()
        input = None
        print_match_lines(input, output, config.machine, config.color, config.underline)
    else:
        input = shlex.split(input)
        output = subprocess.check_output(input).decode('ascii')
        input = None
        print_match_lines(input, output, config.machine, config.color, config.underline)

@cli.command()
@click.argument('input', type=click.File('r'), nargs=-1)
@pass_config
def cat(config, input):
    """
    this command works similar to the Unix `cat` command

    examples:

    \b
    cat single file:
    cat file.txt

    \b
    cat multiple files:
    cat file.txt file1.txt file2.txt
    """
    for f in input:
        while True:
            output = f.read()
            if not output:
                break
            print_match_lines(f, output, config.machine, config.color, config.underline)


def print_match_lines(input, output, machine, color, underline):
    output = iter(output.splitlines())
    line_num = 0
    num_of_matches = 0
    for i in output:
        line_num += 1
        if machine in match(i, machine, color, underline):
            num_of_matches += 1
            print_convention(input, line_num, i, machine, color, underline)
    if num_of_matches == 0:
        print('No matches found')

def match(word, find, color, underline):
    return re.sub(find, style(find, color, underline), word)

def style(txt, color, underline):
    return click.style(f'{txt}', fg=color, underline=underline)

def start_pos(word, find):
    pos = re.search(find, word)
    return pos.start()

def multi_match(word, find, color, underline):
    finds = list(dict.fromkeys(re.findall(find, word)))
    w = word
    for f in finds:
        w = match(w, f, color, underline)
    return w

def print_convention(input, line_num, word, find, color, underline):
    if input is None:
        print(f'line:{line_num} start_positon:{start_pos(word, find)} matched_text:{multi_match(word, find, color, underline)}') # stdin convention
    else:
        filename, file_extension = os.path.splitext(input.name)
        print(f'format:{file_extension} file_name:{filename} line:{line_num} start_positon:{start_pos(word, find)} matched_text:{multi_match(word, find, color, underline)}') # file convention
