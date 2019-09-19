import os
from sys import stdout


class ColorError(Exception):
    pass


class Color:
    names = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
             'brblack', 'brred', 'brgreen', 'bryellow', 'brblue', 'brmagenta', 'brcyan', 'brwhite']


for color_number, color_name in enumerate(Color.names):
    setattr(Color, color_name, color_number)


class ColorCode:
    prefix = {
        'posix': '\u001b',
        'windows': '^<ESC^>'
    }

    def __init__(self, number=Color.brwhite):
        self.number = number

    @property
    def os_prefix(self):
        try:
            return ColorCode.prefix[os.name]
        except KeyError:
            raise ColorError('Could not determine color code to use for ', os.name)

    @property
    def reset(self):
        return f'{self.os_prefix}[0m'

    @property
    def code(self):
        return f'{self.os_prefix}[3{self.number}m'


def incolor(color, *args, sep=' '):
    text = sep.join(map(str, args))
    if type(color) is int:
        return f'{ColorCode(color).code}{text}{ColorCode().reset}'


def cprint(*args, **kwargs):
    print(incolor(*args, **kwargs))
