import argparse
from incolor import cprint, demos


demo_funs = [item for item in dir(demos) if item.startswith("demo_")]

parser = argparse.ArgumentParser()
parser.add_argument(
    "--fg",
    help="[0..15]", type=int, default=None, required=False)
parser.add_argument(
    "--bg",
    help="[0..15]", type=int, default=None, required=False)
parser.add_argument(
    "--demo",
    choices=range(len(demo_funs)), default=None, required=False, type=int,
    help="print some colors")
parser.add_argument(
    "-n",
    action="store_true", required=False, default=False,
    help="do not output the trailing newline")
parser.add_argument(
    "text", nargs="*")
args = parser.parse_args()

if args.demo is not None:
    try:
        getattr(demos, demo_funs[args.demo])()
    except KeyboardInterrupt:
        pass
    finally:
        print()

if args.text:
    if args.n:
        cprint(*args.text, fg=args.fg, bg=args.bg, end="")
    else:
        cprint(*args.text, fg=args.fg, bg=args.bg)
