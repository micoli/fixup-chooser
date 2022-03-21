import os

import urwid

from fixup_chooser.fixup import candidates_commit_for_fixup
from fixup_chooser.git import CandidateCommitStruct, colored_git_show, do_commit, do_commit_fixup
from fixup_chooser.gui.candidate_commit_detail import CandidateCommitDetailView
from fixup_chooser.gui.candidate_commit_list import CandidateCommitListView
from fixup_chooser.gui.git_commit_message import PopupCommitMessage, CommitMessage
from fixup_chooser.gui.git_status import PopupGitStatus
from fixup_chooser.gui.scrollview import ScrollView
# pylint: disable=too-many-instance-attributes
from fixup_chooser.gui.shortcut import shortcuts, get_shortcut_by_key, shortcut_list
from fixup_chooser.gui.shortcuts_help import PopupShortcutsHelp
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
    def __init__(self, rebase_origin, add_patch_command, commit_fixup_command, commit_command, fixup_on_enter):
        self.only_candidate = True
        self.add_patch_command = add_patch_command
        self.rebase_origin = rebase_origin
        self.commit_fixup_command = commit_fixup_command
        self.commit_command = commit_command
        self.fixup_on_enter = fixup_on_enter
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
                    title='Commits ' + shortcut_list()
                ),
                height=15
            ), 'window', 'window_selected')
        ), 'bg')

        self.git_status_popup = PopupGitStatus()
        urwid.connect_signal(self.git_status_popup, 'validated', self.show_main_screen)

        self.shortcuts_help_popup = PopupShortcutsHelp()
        urwid.connect_signal(self.shortcuts_help_popup, 'validated', self.show_main_screen)

        self.git_commit_popup = PopupCommitMessage()
        urwid.connect_signal(self.git_commit_popup, 'validated', self.git_commit_popup_validated)
        urwid.connect_signal(self.git_commit_popup, 'close', self.show_main_screen)

        self.loop = urwid.MainLoop(self.frame, self.palette, unhandled_input=self.unhandled_input, pop_ups=True)
        self.tabular_items = TabularItems(self.frame.original_widget, [
            ['footer'],
            ['body', 0],
            ['body', 1],
        ])

    def git_commit_popup_validated(self, commit_message: CommitMessage):
        def command():
            do_commit(self.commit_command, commit_message.message, commit_message.body)
        self.shell_command(command)

    def start(self):
        candidates_commit = self.get_candidates_commit_for_fixup()
        if len(candidates_commit) == 0:
            self.only_candidate = False
            candidates_commit = self.get_candidates_commit_for_fixup()
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
        self.loop.draw_screen()

    def refresh_commit_candidate_commits(self):
        self.update_candidates_commit_list(self.get_candidates_commit_for_fixup())

    def toggle_only_candidate(self):
        self.only_candidate = not self.only_candidate
        self.refresh_commit_candidate_commits()

    def get_candidates_commit_for_fixup(self):
        if self.loop_screen_is_started():
            self.loop.widget = urwid.Overlay(
                urwid.Filler(urwid.LineBox(urwid.GridFlow([urwid.Text('Scanning')], 10, 1, 1, 'center'))),
                self.frame,
                align='center', width=('relative', 10),
                valign='middle', height=('relative', 10)
            )
            self.loop.draw_screen()
        candidates = candidates_commit_for_fixup(self.only_candidate, self.rebase_origin)
        if self.loop_screen_is_started():
            self.show_main_screen()
        return candidates

    def loop_screen_is_started(self):
        return self.loop.screen._started # pylint: disable=protected-access

    def shell_command(self, command):
        self.loop.screen.stop()
        print(chr(27) + "[2J")
        if callable(command):
            command()
        else:
            os.system(command)
        input('---------------\nPress enter to continue')
        self.loop.screen.start(alternate_buffer=True)
        self.loop.screen.clear()
        self.show_main_screen()
        self.refresh_commit_candidate_commits()

    def display_git_commit_popup(self):
        self.loop.widget = urwid.Overlay(
            self.git_commit_popup,
            self.frame,
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 30)
        )

    def display_shortcuts_help(self):
        self.loop.widget = urwid.Overlay(
            self.shortcuts_help_popup,
            self.frame,
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 30)
        )

    def unhandled_input(self, key):  #pylint: disable=too-many-branches
        custom_shortcut = get_shortcut_by_key(key, False)
        if custom_shortcut is not None:
            self.shell_command(custom_shortcut.message)
            return

        if key == shortcuts.get('QUIT').key:
            raise KeyboardInterrupt()

        if key == shortcuts.get('GIT_STATUS').key:
            if self.loop.widget == self.frame:
                self.loop.widget = self.git_status_popup
                self.git_status_popup.reload()
            else:
                self.show_main_screen()

        if key == 'esc':
            self.show_main_screen()

        if key == shortcuts.get('GIT_ADD_PATCH').key:
            self.shell_command(self.add_patch_command)

        if key == shortcuts.get('GIT_COMMIT_FIXUP').key:
            if self.selected_candidate_commit is None:
                return

            def command():
                do_commit_fixup(self.commit_fixup_command, self.selected_candidate_commit.sha)

            self.shell_command(command)

        if key == shortcuts.get('GIT_COMMIT_MESSAGE').key:
            self.display_git_commit_popup()

        if key == shortcuts.get('SHOW_SHORTCUTS').key:
            self.display_shortcuts_help()

        if key == shortcuts.get('TOGGLE_FILTER').key:
            self.toggle_only_candidate()

        if key == shortcuts.get('GIT_COMMIT_FIXUP_AND_EXIT').key:
            if self.fixup_on_enter:
                raise urwid.ExitMainLoop()

        if key == shortcuts.get('SELECT_NEXT_PANE').key:
            self.tabular_items.handle_next()

        if key == shortcuts.get('SELECT_PREVIOUS_PANE').key:
            self.tabular_items.handle_previous()
