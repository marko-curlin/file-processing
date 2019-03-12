from pathlib import Path
import re
import os
from constants import *


def get_all_source_files(source: str) -> list or None:
    source_dir = Path(source)

    if not source_dir.exists():
        return None

    gid_files_list = []

    for dir_name, subdir_list, file_list in os.walk(source_dir):
        for fname in file_list:
            if fname.split(".")[-1] == "gid":
                gid_files_list.append(Path(__file__).parent / dir_name / fname)

    return gid_files_list


def find_channel(search_channel, all_channels):
    split_channels = re.findall(r"'(.*?)'", all_channels)
    return split_channels.index(search_channel)


def find_unit(search_unit, all_units):
    split_units = re.findall(r"'(.*?)'", all_units)
    try:
        return split_units[search_unit]
    except IndexError:
        return None


def get_output_lines(user_input_channel, user_unit, crank_angle_unit):
    return ['BEGIN\n', "{0} = ['{1}', '{2}']\n".format(CHANNEL_STRING, CRANK_ANGLE, user_input_channel),
            "{0} = ['{1}', '{2}']\n".format(UNIT_STRING, crank_angle_unit, user_unit), 'END\n']


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def parse_file(file, user_input_channel, speed_cases):
    none_tuple = (None,) * 2
    temp_parameters = {}
    temp_data = {}

    temp_parameters[SPEED] = os.path.basename(file.name).split('_')[4].rstrip('rpm')

    begin = False

    kg_multiplier = 1

    for line in file:
        if line.startswith('#'):
            continue

        elif line.startswith('BEGIN'):
            begin = True

        elif line.startswith('END'):
            if speed_cases is not None and temp_parameters[SPEED] not in speed_cases:
                return none_tuple
            begin = False

        elif begin:
            split_line = line.split(' = ')
            left_side_assignment = split_line[0]

            if left_side_assignment == CHANNEL_STRING:
                all_channels = process_multiline_assignment(line, file)

                try:
                    user_channel_index = find_channel(user_input_channel, all_channels)
                    crank_angle_channel = find_channel(CRANK_ANGLE, all_channels)
                except ValueError:
                    return none_tuple

            elif left_side_assignment == UNIT_STRING:
                all_units = process_multiline_assignment(line, file)
                user_unit = find_unit(user_channel_index, all_units)
                crank_angle_unit = find_unit(crank_angle_channel, all_units)
                if user_unit == KILOGRAM:
                    kg_multiplier = 1000

            else:
                temp_parameters[left_side_assignment] = ''.join(split_line[1:]).rstrip('\n')

        else:
            split_line = line.split()
            temp_data[float(split_line[crank_angle_channel])] = float(split_line[user_channel_index]) * kg_multiplier

    if user_unit == KILOGRAM:
        user_unit = GRAM

    temp_parameters[UNIT_STRING] = user_unit
    temp_parameters[CRANK_ANGLE] = crank_angle_unit

    return temp_data, temp_parameters


def process_multiline_assignment(starting_line: str, file):
    all_lines = ''

    while starting_line.endswith('&\n'):
        all_lines += starting_line.rstrip('&\n')
        starting_line = next(file)

    all_lines += starting_line.rstrip('\n')

    return all_lines
