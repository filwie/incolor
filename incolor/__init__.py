""""""
import os
import sys
from typing import Any, List, Optional, TextIO, Tuple, Union

_DO_COLOR = True
if os.name == "nt":
    try:
        import colorama
        colorama.init()
    except ImportError:
        print("incolor: Package colorama is required on Windows!",
              file=sys.stderr)
        _DO_COLOR = False

BG_OFFSET = 40
BG_OFFSET_BRIGHT = 100 - 8  # sub 8 because Color indices for bright start @ 8
FG_OFFSET = 30
FG_OFFSET_BRIGHT = 90 - 8  # sub 8 because Color indices for bright start @ 8
SCI = "\033["

ColorType = Union[int, str, Tuple[int, int, int]]


class ColorError(ValueError):
    pass


class Color:
    """Enumeration of the 16 base colors."""
    black   = 0
    red     = 1
    green   = 2
    yellow  = 3
    blue    = 4
    magenta = 5
    cyan    = 6
    white   = 7
    brightblack   = 8
    brightred     = 9
    brightgreen   = 10
    brightyellow  = 11
    brightblue    = 12
    brightmagenta = 13
    brightcyan    = 14
    brightwhite   = 15

    @staticmethod
    def get_fg_code(color: Union[str, int]) -> int:
        """Translate color index to actual foreground code."""
        return Color._get_code(color, FG_OFFSET, FG_OFFSET_BRIGHT)

    @staticmethod
    def get_bg_code(color: Union[str, int]) -> int:
        """Translate color index to actual background code."""
        return Color._get_code(color, BG_OFFSET, BG_OFFSET_BRIGHT)

    @staticmethod
    def _get_code(c: Union[str, int], offset: int, offset_bright: int) -> int:
        if isinstance(c, str):
            c = getattr(Color, c)
        if 0 <= c <= 7:  # regular
            return c + offset
        elif 8 <= c <= 15:  # bright
            return c + offset_bright
        else:
            raise ValueError


def _is_rgb_tuple(items: Any) -> bool:
    if not isinstance(items, Tuple):
        return False
    if len(items) != 3:
        return False
    for elem in items:
        if not isinstance(elem, int):
            return False
        if not 0 <= elem <= 255:
            return False
    return True


def _validate_arg(val: Any, name: str) -> bool:
    """Ensure $val is of one of the accepted formats.

    Check if $val is either an int in range 0..15 or a tuple of 3 ints
    in range 0..255. If not, raise a ColorError.

    :return: A boolean saying whether $val is an RGB tuple. If false then
             it is surely an int in range 0..15.
    """
    is_base_int = isinstance(val, int) and 0 <= val <= 15
    is_base_str = val in vars(Color).keys()
    is_rgb = _is_rgb_tuple(val)
    if not is_base_int and not is_base_str and not is_rgb:
        raise ColorError(f"Invalid value of {name}: {val}.\n"
                         "Has to be a number in range 0..15 "
                         "or a tuple of 3 integers in range 0..255.")
    return is_rgb


def incolor(*args,
            fg: Optional[ColorType] = None,
            bg: Optional[ColorType] = None,
            join: bool = True,
            sep: str = " ") -> Union[str, List[str]]:

    # foreground
    if fg is not None:
        is_rgb = _validate_arg(fg, "fg")
        if is_rgb:
            fg = [38, 2, *fg]
        else:
            fg = [Color.get_fg_code(fg)]
    else:
        fg = []

    # background
    if bg is not None:
        is_rgb = _validate_arg(bg, "bg")
        if is_rgb:
            bg = [48, 2, *bg]
        else:
            bg = [Color.get_bg_code(bg)]
    else:
        bg = []

    if fg or bg:
        codes = ";".join(map(str, fg + bg))
        args = list(args)
        args[0] = f"{SCI}{codes}m{args[0]}"
        args[-1] = f"{args[-1]}{SCI}0m"

    if join:
        return sep.join(map(str, args))
    else:
        return args


def cprint(*args,
           fg: Optional[ColorType] = None,
           bg: Optional[ColorType] = None,
           file: TextIO = sys.stdout,
           only_tty: bool = True,
           **kwargs) -> None:
    if _DO_COLOR and (not only_tty or (only_tty and file.isatty())):
        args = incolor(*args, fg=fg, bg=bg, join=False)
    print(*args, file=file, **kwargs)
