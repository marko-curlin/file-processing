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
    splitChannels = re.findall(r"'(.*?)'", allChannels)
    return splitChannels.index(searchChannel)


def findUnit(searchUnit, allUnits):
    splitUnits = re.findall(r"'(.*?)'", allUnits)
    try:
        return splitUnits[searchUnit]
    except IndexError:
        return None


def getOutputLines(userInputChannel, userUnit, crankAngleUnit):
    return ['BEGIN\n', "{0} = ['{1}', '{2}']\n".format(CHANNEL_STRING, CRANK_ANGLE, userInputChannel),
                       "{0} = ['{1}', '{2}']\n".format(UNIT_STRING, crankAngleUnit, userUnit), 'END\n']


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
    noneTuple = (None,)*2
    tempParameters = {}
    tempData = {}

    tempParameters[SPEED] = os.path.basename(file.name).split('_')[4].rstrip('rpm')

    begin = False

    kgMultiplier = 1

    for line in file:
        if line.startswith('#'):
            continue

        elif line.startswith('BEGIN'):
            begin = True

        elif line.startswith('END'):
            if speedCases is not None and tempParameters[SPEED] not in speedCases:
                return noneTuple
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
                    return noneTuple

            elif leftSideAssignment == UNIT_STRING:
                allUnits = processMultilineAssignment(line, file)
                userUnit = findUnit(userChannelIndex, allUnits)
                crankAngleUnit = findUnit(crankAngleChannel, allUnits)
                if userUnit == KILOGRAM:
                    kgMultiplier = 1000

            else:
                tempParameters[leftSideAssignment] = ''.join(splitLine[1:]).rstrip('\n')

        else:
            splitLine = line.split()
            tempData[float(splitLine[crankAngleChannel])] = float(splitLine[userChannelIndex]) * kgMultiplier

    if userUnit == KILOGRAM:
        userUnit = GRAM

    tempParameters[UNIT_STRING] = userUnit
    tempParameters[CRANK_ANGLE] = crankAngleUnit

    return tempData, tempParameters


def processMultilineAssignment(startingLine: str, file):
    allLines = ''

    while startingLine.endswith('&\n'):
        allLines += startingLine.rstrip('&\n')
        startingLine = next(file)

    allLines += startingLine.rstrip('\n')

    return allLines
