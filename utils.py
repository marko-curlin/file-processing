from pathlib import Path
import re
import os


def getAllSourceFiles(source: str) -> list:
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
    # return None


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

def readFile(file):
    for line in file:
        if line.startswith("#"):
            continue
        elif line.startswith("BEGIN"):
            begin = True
        elif line.startswith("END"):
            if changeSpeedCases == "n":
                pass
            elif tempParameters["SPEED"] not in speedCases:
                continue
            begin = False
        elif begin:
            splitLine = line.split(" = ")
            if splitLine[0] == CHANNEL_STRING:
                allChannels = ""
                while line.endswith("&\n"):
                    allChannels += line.rstrip("&\n")  # check if \n is needed. so far testing it worked without it
                    line = next(file)
                allChannels += line.rstrip("\n")
                userChannelIndex = findChannel(userInputChannel, allChannels)
                crankAngleChannel = findChannel(CRANK_ANGLE, allChannels)
            elif splitLine[0] == UNIT_STRING:
                allUnits = ""
                while line.endswith("&\n"):
                    allUnits += line.rstrip("&\n")
                    line = next(file)
                allUnits += line.rstrip("\n")
                userUnit = findUnit(userChannelIndex, allUnits)
                crankAngleUnit = findUnit(crankAngleChannel, allUnits)
                multiplier = 1000 if userUnit == "kg" else 1
            else:
                tempParameters[splitLine[0]] = ''.join(splitLine[1:]).rstrip("\n")
        else:
            splitLine = line.split()
            tempData[float(splitLine[crankAngleChannel])] = float(splitLine[userChannelIndex]) * multiplier
