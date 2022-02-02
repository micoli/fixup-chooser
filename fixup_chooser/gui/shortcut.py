import re
import sys
from dataclasses import dataclass

from fixup_chooser.configuration import CONFIG_KEY_SECTION
from fixup_chooser.git import git_get_config_by_regexp


@dataclass
class Shortcut:
    key: str
    message: str
    builtin: bool
    short_message: str = None


shortcuts = {
    'QUIT': Shortcut('q', 'quit without committing with fixup', True, 'quit'),
    'SHOW_SHORTCUTS': Shortcut('?', 'show help', True, 'help'),
    'GIT_STATUS': Shortcut('s', 'git status', True, 'gst'),
    'GIT_ADD_PATCH': Shortcut('a', 'add patch', True, 'patch'),
    'GIT_COMMIT_FIXUP': Shortcut('x', 'commit fixup', True, 'fixup'),
    'GIT_COMMIT_MESSAGE': Shortcut('m', 'commit with message', True, 'commit'),
    'TOGGLE_FILTER': Shortcut('f', 'toggle filter', True, 'filter'),
    'GIT_COMMIT_FIXUP_AND_EXIT': Shortcut('enter', 'quit with committing with', True, 'fixup+quit'),
    'SELECT_NEXT_PANE': Shortcut('tab', 'select next pane', True, 'next'),
    'SELECT_PREVIOUS_PANE': Shortcut('shift tab', 'select previous pane', True, 'previous'),
}


def add_git_option_shortcuts():
    git_config_shortcuts = git_get_config_by_regexp(CONFIG_KEY_SECTION + r'\.shortcut-[0-9]+')
    if git_config_shortcuts is None:
        return
    for group in re.finditer(
            CONFIG_KEY_SECTION + r'\.(shortcut-[0-9]+) (.*?):(.*)',
            git_config_shortcuts,
            re.IGNORECASE | re.MULTILINE
    ):
        if get_shortcut_by_key(group[2], True) is not None:
            print('Could not assign %s shortcut, "%s" already assigned' % (group[1], group[2]))
            sys.exit(1)
        shortcuts[group[1]] = Shortcut(group[2], group[3], False)


def get_shortcut_by_key(key: str, builtin: bool):
    for shortcut in shortcuts.values():
        if shortcut.key == key and shortcut.builtin == builtin:
            return shortcut
    return None


def shortcut_list():
    return ' '.join(list(map(
        lambda shortcut: '[%s] %s' % (
            shortcut.key, shortcut.short_message if shortcut.short_message is not None else shortcut.message
        ),
        shortcuts.values()
    )))
