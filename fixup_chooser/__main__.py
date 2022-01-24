import argparse
import pprint

import colored_traceback

from fixup_chooser.fixup import format_candidates_commit_for_fixup, candidates_commit_for_fixup
from fixup_chooser.gui import App

colored_traceback.add_hook(always=True)
pp = pprint.PrettyPrinter(indent=4)


def parse_main_args():
    parser = argparse.ArgumentParser(description='Help to rebase by selecting commit sha depending of files already staged')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gui', action='store_const', dest='action', const='gui', default='gui')
    group.add_argument('--list', action='store_const', dest='action', const='list')

    return parser.parse_args()


def main() -> None:
    args = parse_main_args()

    if args.action == 'list':
        for line in format_candidates_commit_for_fixup(candidates_commit_for_fixup(True)):
            print(line)

    if args.action == 'gui':
        app = App()
        try:
            app.start()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
