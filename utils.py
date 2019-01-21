from pathlib import Path
import re
import os
from constants import *


def getAllSourceFiles(source: str) -> list or None:
    sourceDir = Path(source)
    if not sourceDir.exists():
        return None
    gidFilesList = []
    for dirName, subdirList, fileList in os.walk(sourceDir):
        for fname in fileList:
            if fname.split(".")[-1] == "gid":
                gidFilesList.append(Path(__file__).parent / dirName / fname)
    return gidFilesList


def findChannel(searchChannel, allChannels):
    splitChannels = re.findall(r"'(.*?)'", allChannels)  # order is guaranteed
    counter = 0
    for channel in splitChannels:
        if searchChannel == channel:
            return counter
        counter += 1
    raise ValueError("The given channel [{0}] doesn't exist!".format(searchChannel))


def findUnit(searchUnit, allUnits):
    splitUnits = re.findall(r"'(.*?)'", allUnits)
    return splitUnits[searchUnit]


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def parseFile(file, userInputChannel, speedCases):
    tempParameters = {}
    tempData = {}

    tempParameters[SPEED] = os.path.basename(file.name).split('_')[4].rstrip('rpm')

    begin = False

    for line in file:
        if line.startswith('#'):
            continue
        elif line.startswith('BEGIN'):
            begin = True
        elif line.startswith('END'):
            if speedCases is None:
                pass
            elif tempParameters[SPEED] not in speedCases:
                return
            begin = False
        elif begin:
            splitLine = line.split(' = ')
            leftSideAssignment = splitLine[0]
            if leftSideAssignment == CHANNEL_STRING:
                allChannels = processMultilineAssignment(line, file)
                try:
                    userChannelIndex = findChannel(userInputChannel, allChannels)
                    crankAngleChannel = findChannel(CRANK_ANGLE, allChannels)
                except ValueError:
                    return
            elif leftSideAssignment == UNIT_STRING:
                allUnits = processMultilineAssignment(line, file)
                userUnit = findUnit(userChannelIndex, allUnits)
                crankAngleUnit = findUnit(crankAngleChannel, allUnits)
                multiplier = 1000 if userUnit == 'kg' else 1
            else:
                tempParameters[leftSideAssignment] = ''.join(splitLine[1:]).rstrip('\n')
        else:
            splitLine = line.split()
            tempData[float(splitLine[crankAngleChannel])] = float(splitLine[userChannelIndex]) * multiplier

    if userUnit == 'kg':
        userUnit = 'g'

    return tempData, tempParameters, userUnit, crankAngleUnit


def processMultilineAssignment(startingLine: str, file):
    allLines = ''
    while startingLine.endswith('&\n'):
        allLines += startingLine.rstrip('&\n')
        startingLine = next(file)
    allLines += startingLine.rstrip('\n')
    return allLines
