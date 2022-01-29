import os
import subprocess
import re
import sys
from dataclasses import dataclass
from fixup_chooser.process import process_exec

cache = {}

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
    cache_key = 'get_commit_struct-%s' % sha
    cached_value = cache.get(cache_key)
    if cached_value is not None:
        return cached_value

    values = process_exec([
        'git', '--no-pager', 'log',
        '--date=format:%Y-%m-%d %H:%M:%S',
        '--format=%h\t%ad\t%ae\t%s',
        '-n', '1', sha
    ]).split('\t')
    cache[cache_key] = CommitStruct(
        short_sha=values[0],
        date=values[1],
        committer=values[2],
        message=values[3],
    )

    return cache[cache_key]


def get_candidate_commit_struct(sha, staged_files, modified_files):
    return CandidateCommitStruct(
        sha=sha,
        commit=get_commit_struct(sha),
        all_are_present=all(elem in modified_files for elem in staged_files),
        numbers_of_file_found=sum([elem in modified_files for elem in staged_files]),
        files_found=list(set(staged_files).intersection(modified_files)),
        total_file_staged=len(staged_files),
    )


def get_commits_in_branch(origin_branch):
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
    cache_key = 'get_modified_files_in_commit-%s' % sha
    cached_value = cache.get(cache_key)
    if cached_value is not None:
        return cached_value

    cache[cache_key] = process_exec(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', sha]).split("\n")
    return cache[cache_key]


def get_staged_files():
    return filter_not_empty(
        process_exec(['git', 'diff', '--cached', '--name-only']).split("\n")
    )


def get_pretty_staged_diff():
    return re.sub(r'^diff --git/m', '\n', process_exec(['git', 'diff', '--color', '--staged']).strip())


def get_branch_name():
    return process_exec(['git', 'symbolic-ref', '--short', 'HEAD'])


def do_commit_fixup(command_format, sha):
    os.system(command_format + ' ' + sha)


def do_commit(command_format, message, body):
    command = (command_format + ' -m "%s"') % message
    if body is not None or len(body.strip()) != 0:
        command = (command_format + ' -m "%s" -m "%s"') % (message, body)
    os.system(command)


def colored_git_show(sha):
    cache_key = 'colored_git_show-%s' % sha
    cached_value = cache.get(cache_key)
    if cached_value is not None:
        return cached_value

    cache[cache_key] = process_exec(['git', 'show', '--color', sha])
    return cache[cache_key]


def colored_git_status():
    return process_exec(['git', '-c', 'color.status=always', 'status'])


def git_get_config(config_key):
    try:
        return process_exec(['git', 'config', '--get', config_key]).strip()
    except:  # pylint: disable=bare-except
        return None


def git_set_config(config_key, value):
    try:
        process_exec(['git', 'config', '--global', '--unset-all', config_key])
    except subprocess.CalledProcessError:
        pass
    return process_exec(['git', 'config', '--global', '--add', config_key, value]).strip()
