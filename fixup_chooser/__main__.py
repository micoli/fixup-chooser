import argparse
import pprint
import sys

import colored_traceback

from fixup_chooser.configuration import add_options_list, display_options_help, init_git_configuration
from fixup_chooser.fixup import format_candidates_commit_for_fixup, candidates_commit_for_fixup
from fixup_chooser.git import do_commit_fixup
from fixup_chooser.gui import App

colored_traceback.add_hook(always=True)
pp = pprint.PrettyPrinter(indent=4)


def parse_main_args():
    parser = argparse.ArgumentParser(
        description='Help to rebase by selecting commit sha depending of files already staged',
        epilog="""
        Option values are taken in the following order:
         - Internal default value at first
         - Then, if set, `GIT option` value
         - Then, if set, `environment` value
         - Then, if set, `argument` value
        """.replace('    ', '') + display_options_help("fancy_grid"),
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gui', action='store_const', dest='action', const='gui', default='gui',
                       help='GUI mode'
                       )
    group.add_argument('--list', action='store_const', dest='action', const='list',
                       help='Only display candidate commit list'
                       )
    group.add_argument('--git-init', action='store_true',
                       help='set .gitconfig initial configuration'
                       )
    add_options_list(parser)

    return parser.parse_args()


def main() -> None:
    args = parse_main_args()

    if args.git_init:
        init_git_configuration()
        sys.exit(0)

    if args.action == 'list':
        for line in format_candidates_commit_for_fixup(candidates_commit_for_fixup(True, args.rebase_origin)):
            print(line)

    if args.action == 'gui':
        app = App(args.rebase_origin, args.add_patch_command, args.commit_fixup_command, args.commit_command)
        try:
            sha = app.start()
            if sha is not None:
                do_commit_fixup(args.commit_fixup_command, sha)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
