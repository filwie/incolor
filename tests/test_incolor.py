from unittest import mock
import pytest
from incolor import Color, ColorError, ColorCode, incolor, cprint


def test_color_attributes():
    assert Color.red == 1
    assert Color.green == 2
    assert Color.brblue == 12
    assert Color.brwhite == 15
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


@pytest.mark.parametrize("test_input,expected",
                         [((Color.brblue,), f'{prefix_posix}12m{reset_posix}'),
                          ((Color.brblue, 123, 'kek', 'fek'), f'{prefix_posix}12m123 kek fek{reset_posix}')])
@mock.patch("os.name", "posix")
def test_incolor(test_input, expected):
    assert incolor(*test_input) == expected


@mock.patch("os.name", "posix")
def test_incolor_separator():
    assert incolor(12, 'a', 1, 'b', 2, sep='||') == f'{prefix_posix}12ma||1||b||2{reset_posix}'
