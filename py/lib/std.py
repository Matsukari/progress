#!/usr/bin/env python3

"""
    convenient function collection
"""


from datetime import datetime
from datetime import timedelta
from pathlib import Path
import os

# Similar to ListToString but made for extracting values from sys.arg(commandline argument) to string
def ArgToString(list):
    string = ''
    for i in list:
        if i.find(' ') != -1:
            string += '"' + i + '" '
        else:
            string += i + ' '

    return string

def StringFind(base, s):
    if s in base:
        return s

    return ''

def StringReverse(base):
    string = ''
    for s in base:
        string = s + string
    return string

def StringBetween(base, a, b, n=0):
    bet = ''
    curr = 0
    for i in range(len(base)):
        if base[i] == a:
            for j in range(i+1, len(base)):
                if base[j] == b:
                    if curr == n:
                        break
                    curr += 1
                    bet = ''
                    continue
                bet += base[j]

            return bet
    return bet
def RStringBetween(base, a, b, n=0):
    bet = ''
    curr = 0
    for i in range(len(base)-1, -1, -1):
        if base[i] == a:
            for j in range(i-1, -1, -1):
                if base[j] == b:
                    if curr == n:
                        break
                    curr += 1
                    bet = ''
                    continue
                bet += base[j]
            return StringReverse(bet)
    return bet


start_time = datetime.now()

# Get the time lapsed since the program started
def GetTicks():
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


# Send all files inside <paths> path with the <formats> format to stage:
def GetFiles(paths, formats):
    stage = []

    for obj in paths:
        objfile = obj

        if Path(obj).is_dir():
            for folder, dirs, files in os.walk(obj):

                for file in files:
                    if Path(file).suffix in formats:
                        # get whole path
                        objfile = folder + '/' + file
                        #print(f'{file} added to compilation')

                        stage.append(objfile)
        else:
            stage.append(objfile)
    return stage

# <dict> dictionary keye and values should be string
def GetCLArgs_Next(dict, deldef=False):
    # get the values next to given option(argument)
    for i, arg in enumerate(sys.argv):
        if arg in dict.keys():

            nextarg = sys.argv[i+1]

            # check every space delimited; should the next argument enclosed in quotes(""), split it and add it
            for val in nextarg.split():
                new = val

                if arg == '--flags' and val in flags.keys():
                    new = flags[val] + ' '
                if deldef:
                    # if argument is in default of configs, empty it
                    for default in dict.values(): 
                        if val in default.split(): dict[arg] = ''

                dict[arg] += new + ' '

# overwrites option
def GetCLArgs_Flat(dict, key, deldef=False):
    if key not in dict.keys():
        print(f'warn: {key} key, does not exist')
        return False

    # get the values next to given option(argument)
    for i, arg in enumerate(sys.argv):

        if deldef:
            for default in dict[key].values():
                if arg in default.split(): dict[key] = ''
        dict[key] += arg + ' '

    return True