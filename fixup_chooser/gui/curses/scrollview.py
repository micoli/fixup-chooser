import urwid

from fixup_chooser.gui.curses.urwidhelper import translate_text_for_urwid


class ScrollViewLine(urwid.WidgetWrap):
    def __init__(self, line_number, content):
        item = urwid.Text(translate_text_for_urwid('%4d %s' % (line_number, content)))
        urwid.WidgetWrap.__init__(self, urwid.AttrWrap(item,'scroll_line', 'scroll_line_selected'))

    def selectable(self):
        return True

    def keypress(self, _, key):
        return key


class ScrollView(urwid.WidgetWrap):

    def __init__(self):
        self.walker = urwid.SimpleFocusListWalker([])

        urwid.WidgetWrap.__init__(self, urwid.ListBox(self.walker))

    def set_lines(self, lines):
        while len(self.walker) > 0:
            self.walker.pop()

        self.walker.extend(
            [ScrollViewLine(index + 1, line) for index, line in enumerate(lines)]
        )

        self.walker.set_focus(0)
