import click
import re
import shlex
import subprocess
from pathlib import Path

@click.command()
@click.option('--input', '-i', default='ls -a',
              help="Type stdin linux shell command,\n"
                                                     "A command with multiple parameters should be in quotation marks, example: 'ls -a'")
@click.option('--grep', '-g', default='py',
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
