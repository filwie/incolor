from unittest import mock
import pytest
from incolor import Color, ColorError, ColorCode, incolor, cprint


def test_color_attributes():
    assert Color.red == 1
    assert Color.green == 2
    assert type(Color.yellow) is int


def test_color_attributes_negative():
    with pytest.raises(AttributeError):
        _ = Color.orange


@mock.patch("os.name", "posix")
def test_colorcode_os_prefix_posix():
    assert ColorCode().os_prefix == '\u001b'


@mock.patch("os.name", "windows")
def test_colorcode_os_prefix_windows():
    assert ColorCode().os_prefix == '^<ESC^>'


@mock.patch("os.name", "scooby")
def test_colorcode_os_prefix_negative():
    with pytest.raises(ColorError):
        _ = ColorCode().os_prefix


prefix_posix = f'\u001b[3'
reset_posix = f'\u001b[0m'


@mock.patch("sys.stdout.isatty", return_value=True)
@pytest.mark.parametrize("test_input,expected",
                         [((Color.blue,), f'{prefix_posix}4m{reset_posix}'),
                          ((Color.blue, 123, 'kek', 'fek'), f'{prefix_posix}4m123 kek fek{reset_posix}')])
@mock.patch("os.name", "posix")
def test_incolor(_, test_input, expected):
    assert incolor(*test_input) == expected


@mock.patch("os.name", "posix")
@mock.patch("sys.stdout.isatty", return_value=True)
def test_incolor_separator(*args):
    assert incolor(4, 'a', 1, 'b', 2, sep='||') == f'{prefix_posix}4ma||1||b||2{reset_posix}'


@mock.patch("os.name", "posix")
@mock.patch("sys.stdout.isatty", return_value=False)
def test_strippping_color_codes_if_not_tty(*args):
    assert incolor(Color.blue, 'Hooray', 123) == 'Hooray 123'
