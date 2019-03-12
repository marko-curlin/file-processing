from utils import *
from solution import sum_and_graph_data


def command_line_client():
    bad_input = True

    while bad_input:
        user_defined_source = input('Where is your data stored >> ')
        try:
            input_files = get_all_source_files(user_defined_source)
            if input_files is not None:
                bad_input = False
            else:
                print('The given folder does not exist!')
        except OSError:
            print("Please specify a valid path!")

    user_input_channel = input('Which channel would you like to plot >> ')

    bad_input = True

    while bad_input:
        change_output_location = input('Do you wish to change the output location '
                                       '({0}/{1}) >> '.format(POSITIVE_ANSWER, NEGATIVE_ANSWER))

        if change_output_location == POSITIVE_ANSWER:
            output_location = input('Please choose your new location >> ')
            try:
                if Path(output_location).exists():
                    bad_input = False
                else:
                    print('The selected output location does not exist!')
            except OSError:
                print("Please specify a valid path")
        elif change_output_location == NEGATIVE_ANSWER:
            output_location = os.path.dirname(__file__)
            bad_input = False

    bad_input = True

    speed_cases = None

    while bad_input:
        change_speed_cases = input('Would you like to change which speed cases are processed '
                                   '({0}/{1}) >> '.format(POSITIVE_ANSWER, NEGATIVE_ANSWER))

        if change_speed_cases == POSITIVE_ANSWER:
            speed_cases = input('Which speed cases would you like to use (ex. 3000 3500 3750) >> ')
            speed_cases = speed_cases.split()
            bad_input = False
        elif change_speed_cases == NEGATIVE_ANSWER:
            bad_input = False

    return input_files, user_input_channel, output_location, speed_cases


if __name__ == '__main__':
    args = command_line_client()
    sum_and_graph_data(*args)
