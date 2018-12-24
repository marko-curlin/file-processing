# C:\Users\mcurlin\Documents\My Documents\AVL_ZAG_Test_Assignment_Analyse_Total_Mass[504]\Data\003_B1_SN2c2_FL_3500rpm\2D_Results\003_B1_SN2c2_FL_3500rpm_fl2.gid
import re
import plotly.offline as offline
import plotly.graph_objs as go
import matplotlib
import matplotlib.pyplot as plt

CHANNEL_STRING = "CHANNELNAME"
UNIT_STRING = "UNIT"
CRANK_ANGLE = "Crank Angle"

inputFile = open(r"C:\Users\mcurlin\Documents\My Documents\AVL_ZAG_Test_Assignment_Analyse_Total_Mass[504]\Data"
                 r"\003_B1_SN2c2_FL_3500rpm\2D_Results\003_B1_SN2c2_FL_3500rpm_fl2.gid", "r")


userInputChannel = input("Which channel would you like to plot >> ")
userInputChannel = ":flow:total_mass"


def findChannel(searchChannel, allChannels):
    splitChannels = re.findall(r"'(.*?)'", allChannels) # order is guaranteed
    counter = 0
    for channel in splitChannels:
        if searchChannel == channel:
            return counter
        counter += 1
    raise ValueError("The given channel [{0}] doesn't exist!".format(searchChannel))


def findUnit(searchUnit, allUnits):
    splitUnits = re.findall(r"'(.*?)'", allUnits)
    return splitUnits[searchUnit]


parameters = {}
crankAngleData = []
userChannelData = []
for line in inputFile:
    if line.startswith("#"):
        continue
    if line.startswith("BEGIN"):
        begin = True
        continue
    if line.startswith("END"):
        begin = False
        continue
    if begin:
        splitLine = line.split(" = ")
        if splitLine[0] == CHANNEL_STRING:
            allChannels = ""
            while line.endswith("&\n"):
                allChannels += line.rstrip("&\n")  # check if \n is needed. so far testing it worked without it
                line = next(inputFile)
            allChannels += line.rstrip("\n")
            print(allChannels)
            userChannel = findChannel(userInputChannel, allChannels)
            crankAngleChannel = findChannel(CRANK_ANGLE, allChannels)
        if splitLine[0] == UNIT_STRING:
            allUnits = ""
            while line.endswith("&\n"):
                allUnits += line.rstrip("&\n")
                line = next(inputFile)
            allUnits += line.rstrip("\n")
            userUnit = findUnit(userChannel, allUnits)
            crankAngleUnit = findUnit(crankAngleChannel, allUnits)
        parameters[splitLine[0]] = splitLine[1].split()[0]  # split - in case it has comments behind the parameter value
    else:
        splitLine = line.split()
        crankAngleData.append(float(splitLine[crankAngleChannel]))
        userChannelData.append(float(splitLine[userChannel]) * (1000 if userUnit == "kg" else 1))

if userUnit == "kg":
    userUnit = "g"

inputFile.close()
# možda zamjenit cijeli gornji kod sa WITH statment

# trace = go.Scatter(y = userChannelData, x = crankAngleData)
#
# offline.plot([trace], image='png')

fig, ax = plt.subplots()
ax.plot(crankAngleData, userChannelData)

ax.set(xlabel='Crank Angle ({0})'.format(crankAngleUnit), ylabel='{0} ({1})'.format(userInputChannel, userUnit),
       title='Total Mass @ 3700 rpm')
ax.grid()

fig.savefig("test.png") # user defined location, else a default location
plt.show()


