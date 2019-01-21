from collections import defaultdict, namedtuple
import matplotlib.pyplot as plt
from utils import *
import sys


while True:
    userDefinedSource = input('Where is your data stored >> ')
    # userDefinedSource = 'Data'
    inputFiles = getAllSourceFiles(userDefinedSource)
    if inputFiles is not None:
        break
    print('The given folder does not exist!')

userInputChannel = input('Which channel would you like to plot >> ')
# userInputChannel = ':flow:total_mass'  # delete this line

while True:
    changeOutputLocation = input('Do you wish to change the output location '
                                 '({0}/{1}) >> '.format(POSITIVE_ANSWER, NEGATIVE_ANSWER))
    if changeOutputLocation == POSITIVE_ANSWER:
        outputLocation = input('Please choose your new location >> ')
        if not Path(outputLocation).exists():
            print('The selected output location does not exist!')
            continue
        break
    elif changeOutputLocation == NEGATIVE_ANSWER:
        outputLocation = os.path.dirname(__file__)
        break

speedCases = None
while True:
    changeSpeedCases = input('Would you like to change which speed cases are processed '
                             '({0}/{1}) >> '.format(POSITIVE_ANSWER, NEGATIVE_ANSWER))
    if changeSpeedCases == POSITIVE_ANSWER:
        speedCases = input('Which speed cases would you like to use (ex. 3000 3500 3750) >> ')
        speedCases = speedCases.split()
        break
    elif changeSpeedCases == NEGATIVE_ANSWER:
        break


# parameters = []
# userChannelDataList = []
dataList = []
for filePath in inputFiles:

    with filePath.open() as file:

        tempData, tempParameters, userUnit, crankAngleUnit = parseFile(file, userInputChannel, speedCases)

        if tempData is not None:
            newData = namedtuple('Data', 'speed param userChannelData')
            newData.userChannelData = tempData
            newData.param = tempParameters
            newData.speed = tempParameters[SPEED]
            dataList.append(newData)

            # parameters.append(tempParameters)   # zamini s klasom
            # userChannelDataList.append(tempData)

if not dataList:
    sys.exit("No data has been found! Finishing execution of this script!")

totalAverage = defaultdict(float)
counter = defaultdict(int)

for i in range(len(dataList)):
    dataDict = dataList[i].userChannelData
# for dataDict in userChannelDataList:
    for key, value in dataDict.items():
        totalAverage[key] += value
        counter[key] += 1


with cd(outputLocation):

    with open('total_average_{0}.gid'.format(userInputChannel.replace(':', '-')), 'w') as outputFile:
        outputLines = get_output_lines(userInputChannel, userUnit, crankAngleUnit)
        outputFile.writelines(outputLines)
        for key, count in counter.items():  # create an average for totalAverage
            totalAverage[key] /= count
            outputFile.write('{0} {1}\n'.format(key, totalAverage[key]))

    # lengthOfUserChannelDataList = len(userChannelDataList)

    lengthOfDataList = len(dataList)

    for i in range(lengthOfDataList):
    # for i in range(lengthOfUserChannelDataList):
        fig, ax = plt.subplots()
        ax.plot(sorted(dataList[i].userChannelData.keys()), dataList[i].userChannelData.values(),
        # ax.plot(sorted(userChannelDataList[i].keys()), userChannelDataList[i].values(),  # order is preserved
                label='{0} ({1})'.format(userInputChannel, userUnit))

        ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit),
               ylabel='{0} ({1})'.format(userInputChannel, userUnit),
               title='Total @ {0} rpm'.format(dataList[i].speed))
               # title='Total @ {0} rpm'.format(parameters[i][SPEED]))
        ax.grid()
        ax.legend()
        fig.savefig('{0}rpm_graph.png'.format(dataList[i].speed))
        # fig.savefig('{0}rpm_graph.png'.format(parameters[i][SPEED]))
        plt.show()

    fig, ax = plt.subplots()
    ax.plot(sorted(totalAverage.keys()), totalAverage.values(),
            label='Average {0} ({1})'.format(userInputChannel, userUnit))
    ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit), ylabel='{0} ({1})'.format(userInputChannel, userUnit),
           title='Average Total')
    ax.grid()
    ax.legend()
    plt.show()

    fig.savefig('Total_Average_graph.png')
