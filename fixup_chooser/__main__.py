import argparse
import re
import pprint
from ansi.colour import fg

import colored_traceback

from fixup_chooser.git import get_commits_in_branch, get_candidate_commit_struct, get_staged_files, get_modified_files_in_commit, \
    colored_git_show
from fixup_chooser.gui import App

colored_traceback.add_hook(always=True)
pp = pprint.PrettyPrinter(indent=4)


def candidates_commit_for_fixup():
    commit_shas = get_commits_in_branch()
    commit_shas.reverse()

    if len(commit_shas) == 0:
        return []

    staged_files = get_staged_files()
    commits = list(map(
        lambda sha: get_candidate_commit_struct(
            sha,
            staged_files,
            get_modified_files_in_commit(sha)
        ),
        commit_shas
    ))
    return list(filter(
        lambda commit: commit.numbers_of_file_found > 0 and not re.match(r'^(fixup|squash)', commit.commit.message),
        commits
    ))


def git_show(sha: str):
    modified_files = get_modified_files_in_commit(sha)
    for staged_file in get_staged_files():
        print('%s' % (
            fg.green(staged_file) if staged_file in modified_files else fg.yellow(staged_file)
        ))
    print(fg.red('-' * 80))
    print(colored_git_show(sha))


def format_candidates_commit_for_fixup(candidates_commit):
    _list = []
    for candidate in candidates_commit:
        formatted_files_found = "(%d/%d)" % (
            candidate.numbers_of_file_found,
            candidate.total_file_staged
        )
        _list.append('%s\t%s <%s> %s %s' % (
            candidate.commit.short_sha,
            fg.green(candidate.commit.date),
            fg.yellow(candidate.commit.committer),
            fg.green(formatted_files_found) if candidate.all_are_present else fg.magenta(formatted_files_found),
            candidate.commit.message,
        ))
    return _list


def parse_main_args():
    parser = argparse.ArgumentParser(description='Help to rebase by selecting commit sha depending of files already staged')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--gui', action='store_const', dest='action', const='gui', default='gui')
    group.add_argument('--list', action='store_const', dest='action', const='list')

    return parser.parse_args()


def main() -> None:
    args = parse_main_args()

    if args.action == 'list':
        for line in format_candidates_commit_for_fixup(candidates_commit_for_fixup()):
            print(line)

    if args.action == 'gui':
        app = App()
        app.update_candidates_commit_list(candidates_commit_for_fixup())
        try:
            app.start()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
