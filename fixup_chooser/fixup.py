import re
from ansi.colour import fg

from fixup_chooser.git import get_commits_in_branch, get_candidate_commit_struct, get_staged_files, get_modified_files_in_commit


def candidates_commit_for_fixup(only_candidate, origin_branch):
    commit_shas = get_commits_in_branch(origin_branch)
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

    commits = list(filter(
        lambda commit: not re.match(r'^(fixup|squash)', commit.commit.message),
        commits
    ))

    if not only_candidate:
        return commits

    return list(filter(
        lambda commit: commit.numbers_of_file_found > 0,
        commits
    ))


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
