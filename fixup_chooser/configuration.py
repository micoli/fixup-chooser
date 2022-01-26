import os
from dataclasses import dataclass
import argparse

from tabulate import tabulate
from fixup_chooser.git import git_get_config, git_set_config
from fixup_chooser.helper import to_camel_case

CONFIG_KEY_SECTION = 'fixupChooser'
ENVIRONMENT_VARIABLE_PREFIX = 'FIXUP_CHOOSER'


@dataclass
class ConfigurationOption:
    argument_name: str
    default_value: str
    message: str
    config_key: str = None
    environment_variable: str = None
    current_default_value: str = None

    def __post_init__(self):
        if self.config_key is None:
            self.config_key = to_camel_case(self.argument_name)
        self.config_key = CONFIG_KEY_SECTION + '.' + self.config_key

        if self.environment_variable is None:
            self.environment_variable = self.argument_name.replace('-', '_').upper()
        self.environment_variable = ENVIRONMENT_VARIABLE_PREFIX + '_' + self.environment_variable

        self.current_default_value = self.default_value

        git_config_value = git_get_config(self.config_key)
        if git_config_value is not None:
            self.current_default_value = git_config_value

        environment_variable = os.environ.get(self.environment_variable)
        if environment_variable is not None:
            self.current_default_value = environment_variable


options = [ConfigurationOption(
    argument_name='rebase-origin',
    default_value='origin/master',
    message='Origin for rebase',
), ConfigurationOption(
    argument_name='commit-fixup-command',
    default_value='git commit --fixup ',
    message='GIT command to "commit fixup"',
), ConfigurationOption(
    argument_name='add-patch-command',
    default_value='git add -p',
    message='GIT command to "git add -p"',
), ConfigurationOption(
    argument_name='commit-command',
    default_value='git commit ',
    message='GIT command to "git commit"',
)]


def add_options_list(parser: argparse.ArgumentParser):
    for option in options:
        parser.add_argument(
            '--%s' % option.argument_name,
            default=option.current_default_value,
            type=str,
            help="%s (%s)\n"
                 % (option.message, option.current_default_value),
        )


def display_options_help(formatter):
    table = []
    for option in options:
        table.append([
            option.message,
            option.environment_variable,
            option.config_key,
            option.default_value,
        ])
    return tabulate(table, headers=[
        "",
        "Environment key",
        "GIT option",
        "Internal Default value"
    ], tablefmt=formatter)


def init_git_configuration():
    for option in options:
        print('Adding option %s to "%s"' % (option.config_key, option.default_value))
        git_set_config(option.config_key, option.default_value)
