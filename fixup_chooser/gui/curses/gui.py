import sys

import urwid
from fixup_chooser.git import CandidateCommitStruct, colored_git_show
from fixup_chooser.gui.curses import palette
from fixup_chooser.gui.curses.candidate_commit_detail import CandidateCommitDetailView
from fixup_chooser.gui.curses.candidate_commit_list import CandidateCommitListView
from fixup_chooser.gui.curses.scrollview import ScrollView


# pylint: disable=too-many-instance-attributes
from fixup_chooser.process import process_exec


class App:
    def __init__(self):
        self.palette = palette
        self.detail_view = CandidateCommitDetailView()
        self.scroll_view = ScrollView()
        self.candidates_commit_list_view = CandidateCommitListView()
        self.selected_candidate_commit = None

        urwid.connect_signal(
            self.candidates_commit_list_view,
            'candidate_commit_changed',
            self.candidate_commit_changed
        )

        self.frame = urwid.AttrMap(urwid.Frame(
            body=urwid.Columns([
                (
                    'weight',
                    30,
                    urwid.AttrMap(urwid.LineBox(
                        self.detail_view,
                        title='Commit'
                    ), 'window', 'window_selected')
                ),
                (
                    'weight',
                    70,
                    urwid.AttrMap(urwid.LineBox(
                        self.scroll_view,
                        title='Staged files'
                    ), 'window', 'window_selected')
                ),
            ]),
            footer=urwid.AttrMap(urwid.BoxAdapter(
                urwid.LineBox(self.candidates_commit_list_view, title='Commits'),
                height=15
            ), 'window', 'window_selected')
        ), 'bg')

        self.loop = urwid.MainLoop(self.frame, self.palette, unhandled_input=self.unhandled_input)

        self.tabular_items = [
            ['footer'],
            ['body', 1],
        ]
        self.frame.original_widget.set_focus_path(self.tabular_items[0])

    def start(self):
        self.loop.run()
        print(process_exec(['git', 'commit', '--fixup', self.selected_candidate_commit.sha]))

    def candidate_commit_changed(self, candidate_commit: CandidateCommitStruct):
        self.selected_candidate_commit = candidate_commit
        self.detail_view.set_candidate_commit(candidate_commit)
        self.scroll_view.set_lines(colored_git_show(candidate_commit.sha).split('\n'))

    def update_candidates_commit_list(self, candidates_commit_list, sha):
        # pylint: disable=unused-argument
        if len(candidates_commit_list) == 0:
            print('No commits are candidate to fixup')
            sys.exit(1)

        self.candidates_commit_list_view.set_candidates_commit_list(candidates_commit_list)

    def unhandled_input(self, key):
        if key in ('q',):
            raise KeyboardInterrupt()

        if key in ('enter',):
            raise urwid.ExitMainLoop()

        if key in ('tab',):
            current_focus_path = self.frame.original_widget.get_focus_path()
            self.frame.original_widget.set_focus_path(
                self.tabular_items[(self.tabular_items.index(current_focus_path) + 1) % len(self.tabular_items)]
            )
