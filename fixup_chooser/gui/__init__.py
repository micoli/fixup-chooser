import os
import urwid

from fixup_chooser.fixup import candidates_commit_for_fixup
from fixup_chooser.git import CandidateCommitStruct, colored_git_show
from fixup_chooser.gui.candidate_commit_detail import CandidateCommitDetailView
from fixup_chooser.gui.candidate_commit_list import CandidateCommitListView
from fixup_chooser.gui.git_status import PopupGitStatus
from fixup_chooser.gui.scrollview import ScrollView
# pylint: disable=too-many-instance-attributes
from fixup_chooser.gui.tabular_items import TabularItems

palette = {
    ("bg", 'white', 'black'),

    ("window", 'white', 'black'),
    ("window_selected", 'light red', 'black'),

    ("candidate_sha", 'brown', 'black'),
    ("candidate_sha_selected", 'black', 'brown'),

    ("candidate_date", 'light blue', 'black'),
    ("candidate_date_selected", 'light blue,bold', 'black'),

    ("candidate_committer", 'light cyan', 'black'),
    ("candidate_committer_selected", "light cyan,bold", 'black'),

    ("candidate_number_ok", 'dark green', 'black'),
    ("candidate_number_nok", 'light red', 'black'),
    ("candidate_number_selected", 'dark green,bold', 'black'),

    ("candidate_message", 'light red', 'black'),
    ("candidate_message_selected", 'black', 'light red'),

    ("scroll_line", 'light red', 'black'),
    ("scroll_line_selected", 'black,bold', 'brown'),

    ("detail_file_ok", 'light green', 'black'),
    ("detail_file_nok", 'light red', 'black'),

    ("separator", 'brown, bold', 'black'),
    ("diff_file_header", 'brown, bold', 'black'),
}


class App:
    def __init__(self, rebase_origin, add_patch_command):
        self.only_candidate = True
        self.add_patch_command = add_patch_command
        self.rebase_origin = rebase_origin
        self.selected_candidate_commit = None
        self.palette = palette
        self.detail_view = CandidateCommitDetailView()
        self.commit_scroll_view = ScrollView()
        self.candidates_commit_list_view = CandidateCommitListView()

        urwid.connect_signal(
            self.candidates_commit_list_view,
            'candidate_commit_changed',
            self.candidate_commit_changed
        )

        self.frame = urwid.AttrMap(urwid.Frame(
            body=urwid.Columns([
                (
                    'weight',
                    40,
                    urwid.AttrMap(urwid.LineBox(
                        self.detail_view,
                        title='Commit Detail/Staged files'
                    ), 'window', 'window_selected')
                ),
                (
                    'weight',
                    60,
                    urwid.AttrMap(urwid.LineBox(
                        self.commit_scroll_view,
                        title='Commit'
                    ), 'window', 'window_selected')
                ),
            ]),
            footer=urwid.AttrMap(urwid.BoxAdapter(
                urwid.LineBox(
                    self.candidates_commit_list_view,
                    title='Commits - [f] toggle filter on candidate - [s] git status - [a] add patch'
                ),
                height=15
            ), 'window', 'window_selected')
        ), 'bg')

        self.git_status_popup = PopupGitStatus()
        urwid.connect_signal(self.git_status_popup, 'validated', self.show_main_screen)

        self.loop = urwid.MainLoop(self.frame, self.palette, unhandled_input=self.unhandled_input, pop_ups=True)
        self.tabular_items = TabularItems(self.frame.original_widget,[
            ['footer'],
            ['body', 0],
            ['body', 1],
        ])

    def start(self):
        candidates_commit = candidates_commit_for_fixup(self.only_candidate, self.rebase_origin)
        if len(candidates_commit) == 0:
            self.only_candidate = False
            candidates_commit = candidates_commit_for_fixup(self.only_candidate, self.rebase_origin)
        self.update_candidates_commit_list(candidates_commit)

        self.loop.run()
        return self.selected_candidate_commit.sha if self.selected_candidate_commit is not None else None

    def candidate_commit_changed(self, candidate_commit: CandidateCommitStruct):
        self.selected_candidate_commit = candidate_commit
        if candidate_commit is not None:
            self.detail_view.set_candidate_commit(candidate_commit)
            self.commit_scroll_view.set_lines(colored_git_show(candidate_commit.sha).split('\n'))
            return
        self.detail_view.set_candidate_commit(None)
        self.commit_scroll_view.set_lines([])

    def update_candidates_commit_list(self, candidates_commit_list):
        self.candidates_commit_list_view.set_candidates_commit_list(candidates_commit_list)

    def show_main_screen(self, *kwargs):  # pylint: disable=unused-argument
        self.loop.widget = self.frame

    def refresh_commit_candidate_commits(self):
        self.update_candidates_commit_list(candidates_commit_for_fixup(self.only_candidate, self.rebase_origin))

    def toggle_only_candidate(self):
        self.only_candidate = not self.only_candidate
        self.refresh_commit_candidate_commits()

    def shell_command(self, command):
        self.loop.screen.stop()
        print(chr(27) + "[2J")
        os.system(command)
        self.loop.screen.start(alternate_buffer=True)
        self.loop.screen.clear()
        self.refresh_commit_candidate_commits()

    def unhandled_input(self, key):
        if key in ('q',):
            raise KeyboardInterrupt()

        if key in ('s',):
            if self.loop.widget == self.frame:
                self.loop.widget = self.git_status_popup
                self.git_status_popup.reload()
            else:
                self.show_main_screen()

        if key in ('a',):
            self.shell_command(self.add_patch_command)

        if key in ('f',):
            self.toggle_only_candidate()

        if key in ('enter',):
            raise urwid.ExitMainLoop()

        if key in ('tab',):
            self.tabular_items.handle_next()

        if key in ('shift tab',):
            self.tabular_items.handle_previous()
