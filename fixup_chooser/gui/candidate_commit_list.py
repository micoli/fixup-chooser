import urwid

from fixup_chooser.git import CandidateCommitStruct


class CandidateCommitStructItem(urwid.WidgetWrap):
    def __init__(self, candidate: CandidateCommitStruct):
        self.content = candidate
        formatted_files_found = '(%d/%d)' % (
            candidate.numbers_of_file_found,
            candidate.total_file_staged
        )
        cols = [
            ('fixed', 10, urwid.AttrWrap(
                urwid.Text(candidate.commit.short_sha),
                'candidate_sha',
                'candidate_sha_selected'
            )),
            ('fixed', 20, urwid.AttrWrap(
                urwid.Text(candidate.commit.date),
                'candidate_date',
                'candidate_date_selected'
            )),
            ('fixed', 30, urwid.AttrWrap(
                urwid.Text(candidate.commit.committer),
                'candidate_committer',
                'candidate_committer_selected'
            )),
            ('fixed', 10, urwid.AttrWrap(
                urwid.Text(formatted_files_found),
                'candidate_number_ok' if candidate.all_are_present else 'candidate_number_nok',
                'candidate_committer_selected'
            )),
            ('fixed', 80, urwid.AttrWrap(
                urwid.Text(candidate.commit.message),
                'candidate_message',
                'candidate_message_selected'
            )),
        ]
        urwid.WidgetWrap.__init__(self, urwid.Columns(cols, focus_column=4, dividechars=2))

    def selectable(self):
        return True


class CandidateCommitListView(urwid.WidgetWrap):

    def __init__(self):
        urwid.register_signal(self.__class__, ['candidate_commit_changed'])

        self.walker = urwid.SimpleFocusListWalker([])

        urwid.WidgetWrap.__init__(self, urwid.ListBox(self.walker))

    def modified(self):
        focus_w, _ = self.walker.get_focus()

        urwid.emit_signal(self, 'candidate_commit_changed', focus_w.content if focus_w is not None else None)

    def set_candidates_commit_list(self, candidate_commits):
        urwid.disconnect_signal(self.walker, 'modified', self.modified)

        while len(self.walker) > 0:
            self.walker.pop()

        self.walker.extend([CandidateCommitStructItem(c) for c in candidate_commits])
        urwid.connect_signal(self.walker, "modified", self.modified)

        self.walker.set_focus(len(candidate_commits)-1)
