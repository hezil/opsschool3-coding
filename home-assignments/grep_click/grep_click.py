import click
import re
import shlex
import subprocess
from pathlib import Path

class Config(object):
    pass
    # def __init__(self):
    #     self.grep = grep
    #     self.color = color
    #     self.underline = underline
    #     self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
# @click.option('--verbose', is_flag=True)
# @click.option('--home-directory', type=click.Path())
@click.option('--grep', '-g', default='py',
              help="Type any key word you wonna find,\n"
                                                "A multiple strig should be in quotation marks example: 'find me'")
@click.option('--color', '-c', default='red',
              help="insert color")

@click.option('--underline', is_flag=True,
              help="add text underline")
@pass_config
# def cli(config, verbose, home_directory):
def cli(config, grep, color, underline):
    # pass
    config.grep = grep
    config.color = color
    config.underline = underline

    # if verbose:
    #     click.echo('we are in verbose mode')

    # config.verbose = verbose
    # if home_directory is None:
    #     home_directory = '.'
    # config.home_directory = home_directory


@cli.command()
@click.option('--input', '-i', default='ls -a',
              help="Type stdin linux shell command,\n"
                                                     "A command with multiple parameters should be in quotation marks, example: 'ls -a'")
@pass_config
def stdin(config, input):
    # if config.verbose:
    #     click.echo('we are in verbose')
    # click.echo(f'Home directory is {config.home_directory}')

    if input == 'history':
        home = str(Path.home())
        with open(home + '/.bash_history', 'r') as file:
            output = file.read()
            # print(type(output))
            # print(output)
        print_match_lines(output, config.grep, config.color, config.underline)
    else:
        input = shlex.split(input)
        output = subprocess.check_output(input).decode('ascii')
        print_match_lines(output, config.grep, config.color, config.underline)
    # else:
    #     try:
    #         input = shlex.split(input)
    #         output = subprocess.check_output(input).decode('ascii')
    #         print_match_lines(output, grep, color, underline)
    #     except:
    #         # This will check for any exception and then execute this print statement
    #         print("Error: Could not find file or read data")


@cli.command()
@click.argument('input', type=click.File('r'), nargs=-1)
# @click.argument('output', type=click.File('wb'))
@pass_config
def files(config, input):
    """This script works similar to the Unix `cat` command but it writes
    into a specific file (which could be the standard output as denoted by
    the ``-`` sign).
    \b
    Copy stdin to stdout:
        inout - -
    \b
    Copy foo.txt and bar.txt to stdout:
        inout foo.txt bar.txt -
    \b
    Write stdin into the file foo.txt
        inout - foo.txt
    """
    for f in input:
        while True:
            output = f.read()
            if not output:
                break
            # output.write(chunk)
            # output.flush()
            # print(output)
            # output = output.decode('ascii')
            # print(type(output))
            # print(output)
            print_match_lines(output, config.grep, config.color, config.underline)



def print_match_lines(output, grep, color, underline):
    output = iter(output.splitlines())
    line_num = 0
    for i in output:
        line_num += 1
        if grep in match(i, grep, color, underline):
            print(f'line:{line_num} start_positon:{start_pos(i, grep)} matched_text:{multi_match(i, grep, color, underline)}')
            # print(f'i is {i} and grep is {grep}')
            # print(greps(i, grep, color, underline))
            # greps(i, grep, color, underline)

# def greps(word, find, color, underline):
#     for x in range(len(word) - len(find) + 1):
#         if find[0] == word[x]:
#             for i in range(len(find)):
#                 if find[i] != word[x + i]:
#                     break
#             else:
#                 if i + 1 == len(find):
#                     word = word.replace(word[x + i - len(find) + 1:x + i + 1], style(word[x + i - len(find) + 1:x + i + 1], color, underline))
#                 return word


def match(word, find, color, underline):
    # print(f'find is {find} type {type(find)} and word is {word} type {type(word)}')
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


# import click
# import re
#
# color = 'red'
# underline = True
# word = 'hello old freind shcoool7 old5 school2'
# find = '[0-9]{1}'
# # find = 'old'
#
# def greps(word, find, color, underline):
#     return re.sub(find, style(find, color, underline), word)
#
# def style(txt, color, underline):
#        return click.style(f'{txt}', fg=color, underline=underline)
#
# def start_pos(word, find):
#     pos = re.search(find, word)
#     return pos.start()
#
#
# finds = list(dict.fromkeys(re.findall(find, word)))
#
# w = word
# for f in finds:
#     w = greps(w, f, color, underline)
#
# print(f'start_pos: {start_pos(word, find)} matched_text: {w}')


# def greps(word, find, color, underline):
#         # print(find)
#         for x in range(len(word) - len(find) + 1):
#             if find[0] == word[x]:
#                 for i in range(len(find)):
#                     if find[i] != word[x + i]:
#                         break
#                 else:
#                     if i + 1 == len(find):
#                         word = word.replace(word[x + i - len(find) + 1:x + i + 1],style(word[x + i - len(find) + 1:x + i + 1], color, underline))
#         return word




# str = "The rain in Spain"
# x = re.findall("ai", str)
# print(x)
