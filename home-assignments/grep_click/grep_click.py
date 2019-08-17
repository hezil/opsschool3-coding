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
@click.option('--regex', '-r',
              help="inset search keyword/regex pattern,\n"
                   "A multiple strig should be in quotation marks,\n"
                   "example: 'find me'")
@click.option('--color', '-c', default='red',
              help="choose matched text color")

@click.option('--underline', '-u', is_flag=True,
              help="add underline to the matched text")
@pass_config
def cli(config, regex, color, underline):
    '''
    \b
    info: sreach_matches application simply search
    and display pattern matches in file/s or stdout'''

    config.regex = regex
    config.color = color
    config.underline = underline

@cli.command()
@click.argument('input')
@pass_config
def stdin(config, input):
    """
    this command accept stdin same as in shell command line

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
        print_match_lines(input, output, config.regex, config.color, config.underline)
    else:
        input = shlex.split(input)
        output = subprocess.check_output(input).decode('ascii')
        input = None
        print_match_lines(input, output, config.regex, config.color, config.underline)

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
            print_match_lines(f, output, config.regex, config.color, config.underline)


def print_match_lines(input, output, regex, color, underline):
    output = iter(output.splitlines())
    line_num = 0
    num_of_matches = 0
    for i in output:
        line_num += 1
        if regex in mark_matches(i, regex, color, underline):
            num_of_matches += 1
            print_convention(input, line_num, i, regex, color, underline)
    if num_of_matches == 0:
        print('No matches found')

def mark_matches(word, find, color, underline):
    return re.sub(find, text_style(find, color, underline), word)

def text_style(txt, color, underline):
    return click.style(f'{txt}', fg=color, underline=underline)

def start_pos(word, find):
    pos = re.search(find, word)
    return pos.start()

def mark_multi_matches(word, find, color, underline): # handle regex pattern
    finds = list(dict.fromkeys(re.findall(find, word)))
    w = word
    for f in finds:
        w = mark_matches(w, f, color, underline)
    return w

def print_convention(input, line_num, word, find, color, underline):
    if input is None:
        print(f'line:{line_num} start_positon:{start_pos(word, find)} '
              f'matched_text:{mark_multi_matches(word, find, color, underline)}') # stdin convention
    else:
        filename, file_extension = os.path.splitext(input.name)
        print(f'format:{file_extension} file_name:{filename} line:{line_num} start_positon:{start_pos(word, find)} '
              f'matched_text:{mark_multi_matches(word, find, color, underline)}') # file convention
