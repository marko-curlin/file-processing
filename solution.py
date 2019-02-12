from collections import defaultdict, namedtuple
import matplotlib.pyplot as plt
from utils import *
import sys


def sumAndGraphData(inputFiles, userInputChannel, outputLocation, speedCases):

    dataList = []

    for filePath in inputFiles:

        with filePath.open() as file:

            tempData, tempParameters = parseFile(file, userInputChannel, speedCases)

            if tempData is not None:
                newData = namedtuple('Data', 'speed param userChannelData')
                newData.userChannelData = tempData
                newData.param = tempParameters
                newData.speed = tempParameters[SPEED]
                dataList.append(newData)

    if not dataList:
        sys.exit("No data has been found! Finishing execution of this script!")

    totalAverage = defaultdict(float)
    counter = defaultdict(int)

    for data in dataList:
        dataDict = data.userChannelData

        for key, value in dataDict.items():
            totalAverage[key] += value
            counter[key] += 1

    userUnit = dataList[0].param[UNIT_STRING]
    crankAngleUnit = dataList[0].param[CRANK_ANGLE]

    with cd(outputLocation):

        with open('total_average_{0}.gid'.format(userInputChannel.replace(':', '-')), 'w', buffering=BUFFER_SIZE) \
                as outputFile:  # Windows doesn't accept ':' as a part of a file name

            outputLines = getOutputLines(userInputChannel, userUnit, crankAngleUnit)
            outputFile.writelines(outputLines)

            for key, count in counter.items():  # create an average for totalAverage
                totalAverage[key] /= count
                outputFile.write('{0} {1}\n'.format(key, totalAverage[key]))

        for data in dataList:
            fig, ax = plt.subplots()
            ax.plot(sorted(data.userChannelData.keys()), data.userChannelData.values(),
                    label='{0} ({1})'.format(userInputChannel, userUnit))

            ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit),
                   ylabel='{0} ({1})'.format(userInputChannel, userUnit),
                   title='Total @ {0} rpm'.format(data.speed))
            ax.grid()
            ax.legend()
            fig.savefig('{0}rpm_graph.png'.format(data.speed))

        fig, ax = plt.subplots()
        ax.plot(sorted(totalAverage.keys()), totalAverage.values(),
                label='Average {0} ({1})'.format(userInputChannel, userUnit))
        ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit), ylabel='{0} ({1})'.format(userInputChannel, userUnit),
               title='Average Total')
        ax.grid()
        ax.legend()

        fig.savefig('Total_Average_graph.png')
