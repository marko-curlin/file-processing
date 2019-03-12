from collections import defaultdict, namedtuple
import matplotlib.pyplot as plt
from src.utils import *
import sys


def sum_and_graph_data(input_files, user_input_channel, output_location, speed_cases):
    data_list = []

    for filePath in input_files:

        with filePath.open() as file:

            temp_data, temp_parameters = parse_file(file, user_input_channel, speed_cases)

            if temp_data is not None:
                newData = namedtuple('Data', 'speed param userChannelData')
                newData.userChannelData = temp_data
                newData.param = temp_parameters
                newData.speed = temp_parameters[SPEED]
                data_list.append(newData)

    if not data_list:
        sys.exit("No data has been found! Finishing execution of this script!")

    total_average = defaultdict(float)
    counter = defaultdict(int)

    for data in data_list:
        data_dict = data.userChannelData

        for key, value in data_dict.items():
            total_average[key] += value
            counter[key] += 1

    user_unit = data_list[0].param[UNIT_STRING]
    crank_angle_unit = data_list[0].param[CRANK_ANGLE]

    with cd(output_location):

        with open('total_average_{0}.gid'.format(user_input_channel.replace(':', '-')), 'w', buffering=BUFFER_SIZE) \
                as output_file:  # Windows doesn't accept ':' as a part of a file name

            output_lines = get_output_lines(user_input_channel, user_unit, crank_angle_unit)
            output_file.writelines(output_lines)

            for key, count in counter.items():  # create an average for total_average
                total_average[key] /= count
                output_file.write('{0} {1}\n'.format(key, total_average[key]))

        for data in data_list:
            fig, ax = plt.subplots()
            ax.plot(sorted(data.userChannelData.keys()), data.userChannelData.values(),
                    label='{0} ({1})'.format(user_input_channel, user_unit))

            ax.set(xlabel='Crank Angle ({0})'.format(crank_angle_unit),
                   ylabel='{0} ({1})'.format(user_input_channel, user_unit),
                   title='Total @ {0} rpm'.format(data.speed))
            ax.grid()
            ax.legend()
            fig.savefig('{0}rpm_graph.png'.format(data.speed))

        fig, ax = plt.subplots()
        ax.plot(sorted(total_average.keys()), total_average.values(),
                label='Average {0} ({1})'.format(user_input_channel, user_unit))
        ax.set(xlabel='Crank Angle ({0})'.format(crank_angle_unit),
               ylabel='{0} ({1})'.format(user_input_channel, user_unit),
               title='Average Total')
        ax.grid()
        ax.legend()

        fig.savefig('Total_Average_graph.png')
