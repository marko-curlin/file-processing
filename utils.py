from pathlib import Path
import re
import os


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
