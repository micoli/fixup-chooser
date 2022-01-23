from pyfzf.pyfzf import FzfPrompt


def display_fzf_gui(candidates_commit_for_fixup, sha: str):
    fzf = FzfPrompt()
    try:
        print(fzf.prompt(
            candidates_commit_for_fixup,
            ' '.join([
                '--height=80%',
                '--bind="tab:toggle-preview,shift-up:preview-up,shift-down:preview-down"',
                '--preview="fixupChooser --show --sha={+1}"',
                '--preview-window="up:60%"',
                '--prompt="Select commit: "',
                '--ansi',
                '--select-1',
                '--query=%s' % sha
            ]),
            '\n'
        )[0].split('\t')[0])
    # pylint: disable=bare-except
    except:
        print('')
