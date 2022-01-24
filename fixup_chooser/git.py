import os
import subprocess
import sys
from dataclasses import dataclass
from fixup_chooser.process import process_exec


@dataclass
class CommitStruct:
    short_sha: str
    date: str
    committer: str
    message: str


@dataclass
class CandidateCommitStruct:
    sha: str
    commit: CommitStruct
    all_are_present: bool
    numbers_of_file_found: int
    files_found: list
    total_file_staged: int


def get_commit_struct(sha):
    values = process_exec([
        'git', '--no-pager', 'log',
        '--date=format:%Y-%m-%d %H:%M:%S',
        '--format=%h\t%ad\t%ae\t%s',
        '-n', '1', sha
    ]).split('\t')

    return CommitStruct(
        short_sha=values[0],
        date=values[1],
        committer=values[2],
        message=values[3],
    )


def get_candidate_commit_struct(sha, staged_files, modified_files):
    return CandidateCommitStruct(
        sha=sha,
        commit=get_commit_struct(sha),
        all_are_present=all(elem in modified_files for elem in staged_files),
        numbers_of_file_found=sum([elem in modified_files for elem in staged_files]),
        files_found=list(set(staged_files).intersection(modified_files)),
        total_file_staged=len(staged_files),
    )


def get_commits_in_branch():
    if os.environ.get('FIXUP_CHOOSER_ORIGIN') is None:
        origin_branch = 'origin/master'
    else:
        origin_branch = os.environ.get('FIXUP_CHOOSER_ORIGIN')
    try:
        return get_commits_in_range('%s..%s' % (origin_branch, get_branch_name()))
    except subprocess.CalledProcessError:
        try:
            return get_commits_in_range(None)
        except subprocess.CalledProcessError as error:
            print(str(error) + '\n' + error.stderr.decode("utf-8"))
            sys.exit(1)


def filter_not_empty(_list):
    return list(filter(lambda x: x != '', _list))


def get_commits_in_range(_range):
    return filter_not_empty(list(map(
        lambda line: line.split(' ')[0],
        process_exec(
            ['git', 'log', '--oneline', _range] if _range is not None else ['git', 'log', '--oneline']
        ).split("\n")
    )))


def get_modified_files_in_commit(sha):
    return process_exec(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', sha]).split("\n")


def get_staged_files():
    staged_files = filter_not_empty(
        process_exec(['git', 'diff', '--cached', '--name-only']).split("\n")
    )
    if len(staged_files) == 0:
        print('Nothing in staged area')
        sys.exit(1)

    return staged_files


def get_branch_name():
    return process_exec(['git', 'symbolic-ref', '--short', 'HEAD'])


def colored_git_show(sha):
    return process_exec(['git', 'show', '--color', sha])