import sys
from typing import Callable

from incolor import cprint


def demo_base():
    """Print the 16 base colors."""
    block = '████'
    for i in range(0, 8):
        cprint(block, fg=i, end='')
    print()
    for i in range(8, 16):
        cprint(block, fg=i, end='')
    print()


def _rgb_demo(do_printc: Callable[[int, int, int], None], div: int = 18):
    import os
    width = int(os.popen("stty size", "r").read().split()[1])
    width //= div  # 18 == len("██(rrr, ggg, bbb) ")
    stop = 0x100
    step = stop//width + 1

    for r in range(0, stop, step):
        for g in range(0, stop, step):
            for b in range(0, stop, step):
                do_printc(r, g, b)
                if b == 0xff:
                    print()
                else:
                    print(" ", end="", flush=True)
            print()


def demo_rgb_0():
    """Print a bunch of color samples together with their RGB values.

    Number of samples printed is determined by terminal width.
    """

    def do_printc(r, g, b):
        cprint(f"██({r:03d}, {g:03d}, {b:03d})",
               fg=(r, g, b), end='', flush=True)

    _rgb_demo(do_printc)


def demo_rgb_0_with_bg():
    """Print a bunch of color samples together with their RGB values.

    In this one, bg color is the inverse of fg color.
    Number of samples printed is determined by terminal width.
    """

    def do_printc(r, g, b):
        cprint(f"██({r:03d}, {g:03d}, {b:03d})",
               fg=(r, g, b), bg=(0xff-r, 0xff-g, 0xff-b), end="", flush=True)

    _rgb_demo(do_printc)
