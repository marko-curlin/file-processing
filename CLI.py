from utils import *
from solution import sumAndGraphData


def commandLineClient():

    badInput = True

    while badInput:
        userDefinedSource = input('Where is your data stored >> ')
        try:
            inputFiles = getAllSourceFiles(userDefinedSource)
            if inputFiles is not None:
                badInput = False
            else:
                print('The given folder does not exist!')
        except OSError:
            print("Please specify a valid path!")

    userInputChannel = input('Which channel would you like to plot >> ')

    badInput = True

    while badInput:
        changeOutputLocation = input('Do you wish to change the output location '
                                     '({0}/{1}) >> '.format(POSITIVE_ANSWER, NEGATIVE_ANSWER))

        if changeOutputLocation == POSITIVE_ANSWER:
            outputLocation = input('Please choose your new location >> ')
            try:
                if Path(outputLocation).exists():
                    badInput = False
                else:
                    print('The selected output location does not exist!')
            except OSError:
                print("Please specify a valid path")
        elif changeOutputLocation == NEGATIVE_ANSWER:
            outputLocation = os.path.dirname(__file__)
            badInput = False

    badInput = True

    speedCases = None

    while badInput:
        changeSpeedCases = input('Would you like to change which speed cases are processed '
                                 '({0}/{1}) >> '.format(POSITIVE_ANSWER, NEGATIVE_ANSWER))

        if changeSpeedCases == POSITIVE_ANSWER:
            speedCases = input('Which speed cases would you like to use (ex. 3000 3500 3750) >> ')
            speedCases = speedCases.split()
            badInput = False
        elif changeSpeedCases == NEGATIVE_ANSWER:
            badInput = False

    return inputFiles, userInputChannel, outputLocation, speedCases


if __name__ == '__main__':
    args = commandLineClient()
    sumAndGraphData(*args)
