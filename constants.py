

CHANNEL_STRING = 'CHANNELNAME'
UNIT_STRING = 'UNIT'
CRANK_ANGLE = 'Crank Angle'
SPEED = 'SPEED'
POSITIVE_ANSWER = 'y'
NEGATIVE_ANSWER = 'n'


def get_output_lines(userInputChannel, userUnit, crankAngleUnit):
    return ['BEGIN\n', "{0} = ['{1}', '{2}']\n".format(CHANNEL_STRING, CRANK_ANGLE, userInputChannel),
                       "{0} = ['{1}', '{2}']\n".format(UNIT_STRING, crankAngleUnit, userUnit), 'END\n']
