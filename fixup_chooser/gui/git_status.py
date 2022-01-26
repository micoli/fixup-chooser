import urwid

from fixup_chooser.git import colored_git_status
from fixup_chooser.gui.scrollview import ScrollView


class PopupGitStatus(urwid.WidgetWrap):
    signals = ['validated']

    def __init__(self):  #pylint: disable=super-init-not-called
        self.git_status_scroll_view = ScrollView()
        self.__super.__init__(urwid.Frame(
            body=urwid.LineBox(self.git_status_scroll_view, title='Git status'),
            footer=urwid.GridFlow([urwid.Button('Ok', self.validated)], 8, 1, 1, 'center'),
            focus_part='footer'
        ))

    def validated(self, _):
        urwid.emit_signal(self, 'validated', 'ok')

    def reload(self):
        self.git_status_scroll_view.set_lines(colored_git_status().split('\n'))
