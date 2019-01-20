from collections import defaultdict
import matplotlib.pyplot as plt
from utils import *


CHANNEL_STRING = "CHANNELNAME"
UNIT_STRING = "UNIT"
CRANK_ANGLE = "Crank Angle"

while True:
    # userDefinedSource = input("Where is your data stored >> ")
    userDefinedSource = "Data"
    inputFiles = getAllSourceFiles(userDefinedSource)
    if inputFiles is not None:
        break
    print("The given folder does not exist!")

# userInputChannel = input("Which channel would you like to plot >> ")
userInputChannel = ":flow:total_mass"  # delete this line

while True:
    changeOutputLocation = input("Do you wish to change the output location (y/n) >> ")
    if changeOutputLocation == 'y':
        outputLocation = input("Please choose your new location >> ")
        if not Path(outputLocation).exists():
            print("The selected output location does not exist!")
            continue
        break
    elif changeOutputLocation == 'n':
        outputLocation = os.path.dirname(__file__)
        break


while True:
    changeSpeedCases = input("Would you like to change which speed cases are processed (y/n) >> ")
    if changeSpeedCases == 'y':
        speedCases = input("Which speed cases would you like to use (ex. 3000 3500 3750) >> ")
        speedCases = speedCases.split()
        break
    elif changeSpeedCases == 'n':
        break


parameters = []
userChannelDataList = []
for filePath in inputFiles:

    with filePath.open() as file:

        tempParameters = {}
        tempData = {}

        tempParameters["SPEED"] = os.path.basename(file.name).split("_")[4].rstrip("rpm")

        skip = False

        for line in file:
            if line.startswith("#"):
                continue
            elif line.startswith("BEGIN"):
                begin = True
            elif line.startswith("END"):
                if changeSpeedCases == "n":
                    pass
                elif tempParameters["SPEED"] not in speedCases:
                    skip = True
                    break
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

        if skip:
            continue
        parameters.append(tempParameters)
        userChannelDataList.append(tempData)

if userUnit == "kg":
    userUnit = "g"

totalAverage = defaultdict(float)
counter = defaultdict(int)

for dataDict in userChannelDataList:
    for key, value in dataDict.items():
        totalAverage[key] += value
        counter[key] += 1


with cd(outputLocation):

    with open("total_average_{0}.gid".format(userInputChannel.replace(":", '-')), "w") as outputFile:
        outputLines = ["BEGIN\n", "CHANNELNAME = ['Crank Angle, '{0}']\n".format(userInputChannel),
                       "UNIT = ['{0}', {1}]\n".format(crankAngleUnit, userUnit), "END\n"]
        outputFile.writelines(outputLines)
        for key, count in counter.items():  # create an average for totalAverage
            totalAverage[key] /= count
            outputFile.write("{0} {1}\n".format(key, totalAverage[key]))

    # fig, ax = plt.subplots(len(userChannelDataList), 2)
    # lengthOfUserChannelDataList = len(userChannelDataList)
    # for i in range(lengthOfUserChannelDataList):
    #     ax.item(i).plot(crankAngleDataList[i], userChannelDataList[i])
    #
    #     ax.item(i).set(xlabel='Crank Angle ({0})'.format(crankAngleUnit), ylabel='{0} ({1})'.format(userInputChannel, userUnit),
    #                    title='Total Mass @ {0}'.format(parameters[i]["SPEED"]))
    #     ax.item(i).grid()
    #
    # ax.item(lengthOfUserChannelDataList).plot(sorted(totalAverage.keys()), totalAverage.values())
    # ax.item(lengthOfUserChannelDataList).set(xlabel='Crank Angle ({0})'.format(crankAngleUnit), ylabel='{0} ({1})'.format(userInputChannel, userUnit),
    #                                          title='Average Total Mass')
    # ax.item(lengthOfUserChannelDataList).grid()
    #
    # fig.delaxes(ax.item(3))
    # fig.savefig("test.png")  # user defined location, else a default location
    # plt.show()

    # plotData = [*userChannelDataList, totalAverage]

    lengthOfUserChannelDataList = len(userChannelDataList)

    # fig, ax = plt.subplots(lengthOfUserChannelDataList + 1)
    # for i in range(lengthOfUserChannelDataList):
    #     ax.item(i).plot(sorted(userChannelDataList[i].keys()), userChannelDataList[i].values())  # order is preserved
    #
    #     ax.item(i).set(xlabel='Crank Angle ({0})'.format(crankAngleUnit),
    #                    ylabel='{0} ({1})'.format(userInputChannel, userUnit),
    #                    title='Total @ {0}'.format(parameters[i]["SPEED"]))
    #     ax.item(i).grid()
    #
    # ax.item(lengthOfUserChannelDataList).plot(sorted(totalAverage.keys()), totalAverage.values())
    # ax.item(lengthOfUserChannelDataList).set(xlabel='Crank Angle ({0})'.format(crankAngleUnit),
    #                                          ylabel='{0} ({1})'.format(userInputChannel, userUnit),
    #                                          title='Average Total')
    # ax.item(lengthOfUserChannelDataList).grid()
    #
    # fig.savefig("graph.png")
    # plt.show()

    for i in range(lengthOfUserChannelDataList):
        fig, ax = plt.subplots()
        ax.plot(sorted(userChannelDataList[i].keys()), userChannelDataList[i].values(),  # order is preserved
                label='{0} ({1})'.format(userInputChannel, userUnit))

        ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit),
               ylabel='{0} ({1})'.format(userInputChannel, userUnit),
               title='Total @ {0} rpm'.format(parameters[i]["SPEED"]))
        ax.grid()
        ax.legend()
        fig.savefig("{0}rpm_graph.png".format(parameters[i]["SPEED"]))
        # fig.canvas.set_window_title('Figure {0}'.format(i+1))
        plt.show()

    fig, ax = plt.subplots()
    ax.plot(sorted(totalAverage.keys()), totalAverage.values(),
            label='Average {0} ({1})'.format(userInputChannel, userUnit))
    ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit), ylabel='{0} ({1})'.format(userInputChannel, userUnit),
           title='Average Total')
    ax.grid()
    ax.legend()

    fig.savefig("Total_Average_graph.png")
    # fig.canvas.set_window_title('Figure {0}'.format(lengthOfUserChannelDataList+1))
    plt.show()
