import re

import urwid

from fixup_chooser.git import CandidateCommitStruct, get_modified_files_in_commit, get_staged_files, \
    get_pretty_staged_diff
from fixup_chooser.gui.urwidhelper import translate_text_for_urwid

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
blank = urwid.Divider()
separator = urwid.AttrMap(urwid.Divider('―'), 'separator')


def add_diff_line(list_items, line):
    ansi_free_line = ansi_escape.sub('', line)
    if re.match(r'diff --git', ansi_free_line):
        list_items.append(separator)
        return

    if re.match(r'^(--- a|\+\+\+ b|index [0-9a-f]{7}..[0-9a-f]{7})', ansi_free_line):
        list_items.append(urwid.AttrMap(urwid.Text(ansi_free_line), 'diff_file_header'))
        return
    list_items.append(urwid.Text(translate_text_for_urwid(line)))


class CandidateCommitDetailView(urwid.WidgetWrap):
    def __init__(self):
        self.walker = urwid.SimpleFocusListWalker([])

        urwid.WidgetWrap.__init__(self, urwid.ListBox(self.walker))

    def set_candidate_commit(self, candidate_commit: CandidateCommitStruct):
        while len(self.walker) > 0:
            self.walker.pop()

        list_items = []
        modified_files = []
        if candidate_commit is not None:
            modified_files = get_modified_files_in_commit(candidate_commit.sha)

            list_items = [
                urwid.Text('Date/Sha: %s %s' % (candidate_commit.commit.date, candidate_commit.sha), align='left'),
                blank,
                urwid.Text('Committer: %s' % candidate_commit.commit.committer, align='left'),
                blank,
                urwid.Text('Message: %s' % candidate_commit.commit.message, align='left'),
                blank,
                urwid.Text('Files: (%d/%d)' % (
                    candidate_commit.numbers_of_file_found,
                    candidate_commit.total_file_staged
                ), align='left'),
                separator,
            ]

        for staged_file in get_staged_files():
            list_items.append(urwid.AttrMap(
                urwid.Text(staged_file),
                'detail_file_ok' if staged_file in modified_files else 'detail_file_nok'
            ))

        for line in get_pretty_staged_diff().split('\n'):
            if line != '':
                add_diff_line(list_items, line)

        self.walker.extend(list_items)
        self.walker.set_focus(0)
