import urwid

from fixup_chooser.git import CandidateCommitStruct, get_modified_files_in_commit, get_staged_files


class CandidateCommitDetailView(urwid.WidgetWrap):
    def __init__(self):
        self.walker = urwid.SimpleFocusListWalker([])

        urwid.WidgetWrap.__init__(self, urwid.ListBox(self.walker))

    def set_candidate_commit(self, candidate_commit: CandidateCommitStruct):
        modified_files = get_modified_files_in_commit(candidate_commit.sha)
        blank = urwid.Divider()
        list_items = [
            urwid.Text('Date: %s' % candidate_commit.commit.date, align='left'),
            blank,
            urwid.Text('Committer: %s' % candidate_commit.commit.committer, align='left'),
            blank,
            urwid.Text('Message: %s' % candidate_commit.commit.message, align='left'),
            blank,
            urwid.Text('Files: (%d/%d)' % (
                candidate_commit.numbers_of_file_found,
                candidate_commit.total_file_staged
            ), align='left'),
            urwid.Divider('-'),
        ]
        for staged_file in get_staged_files():
            list_items.append(urwid.AttrMap(
                urwid.Text(staged_file),
                'detail_file_ok' if staged_file in modified_files else 'detail_file_nok'
            ))

        while len(self.walker) > 0:
            self.walker.pop()

        self.walker.extend(list_items)
