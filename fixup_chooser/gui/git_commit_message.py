from dataclasses import dataclass
import urwid
from fixup_chooser.gui.tabular_items import TabularItems


@dataclass
class CommitMessage:
    message: str
    body: str


class PopupCommitMessage(urwid.WidgetWrap):
    signals = ['validated', 'close']

    def __init__(self):  #pylint: disable=super-init-not-called
        self.message = urwid.Edit("Message: ", multiline=False)
        self.body = urwid.Edit("Body: ", multiline=True)
        self.frame = urwid.Frame(
            body=urwid.LineBox(
                urwid.Filler(
                    urwid.Pile([
                        self.message,
                        self.body,
                    ])
                    , 'top'
                ),
                title='Git commit'
            ),
            footer=urwid.GridFlow([urwid.Button('Ok', self.validate)], 8, 1, 1, 'center'),
            focus_part='body'
        )

        self.__super.__init__(self.frame)
        self.tabular_items = TabularItems(self.frame, [
            ['body', 0],
            ['body', 1],
            ['footer', 0],
        ])

    def keypress(self, size, key):
        if key == 'enter' and self.frame.get_focus_path() == ['body', 0]:
            self.validate()
            return None

        if key == 'esc':
            urwid.emit_signal(self, 'close', None)

        if key == 'tab':
            self.tabular_items.handle_next()
            return None

        if key == 'shift tab':
            self.tabular_items.handle_previous()
            return None

        return self.frame.keypress(size, key)

    def validate(self, *kwargs):  # pylint: disable=unused-argument
        if len(self.message.get_edit_text().strip()) == 0:
            self.frame.set_focus_path(['body', 0])
            return
        urwid.emit_signal(self, 'validated', CommitMessage(
            message=self.message.get_edit_text(),
            body=self.body.get_edit_text()
        ))
