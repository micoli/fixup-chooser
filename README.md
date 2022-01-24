# Fixup Chooser

![CI](https://github.com/micoli/fixup-chooser/actions/workflows/ci.yml/badge.svg)

`fixupChooser` allow to select a git commit sha from staged files

It is purely inspired from https://github.com/keis/git-fixup, thanks to him

Merge requests are welcomed

## Installation
```
pip install git+https://github.com/micoli/fixup-chooser.git
```
or for upgrade
```
pip install --upgrade --force-reinstall git+https://github.com/micoli/fixup-chooser.git
```

depending of your installation `pip` can be replaced by `pip3`

## Example of executions:

```
$ git status
On branch branch2
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   src/file1.txt
	modified:   src/file4.txt
```

```
$fixupChooser
┌─────────────── Commit Detail/Staged files ────────────────┐┌────────────────────── Commit ──────────────────────────┐
│Date/Sha: 2022-01-24 22:49:27 38a490e                      ││   1 commit 38a490e96670863108e7307a0a4ad50353664fdc    │
│                                                           ││   2 Author: Name ofCommitter <bar@example.org>         │
│Committer: foo@example.org                                 ││   3 Date:   Mon Jan 24 22:49:27 2022 +0100             │
│                                                           ││   4                                                    │
│Message: File 1 modified                                   ││   5     File 1 modified                                │
│                                                           ││   6                                                    │
│Files: (1/2)                                               ││   7 diff --git a/src/file1.txt b/src/file1.txt         │
│―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――││   8 index e69de29..4e5e8f2 100644                      │
│src/file1.txt                                              ││   9 --- a/src/file1.txt                                │
│src/file4.txt                                              ││  10 +++ b/src/file1.txt                                │
│―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――││  11 @@ -0,0 +1 @@                                      │
│index f6aa43e..40df6e8 100644                              ││  12 +modification 2                                    │
│--- a/src/file1.txt                                        ││                                                        │
│+++ b/src/file1.txt                                        ││                                                        │
│@@ -1,2 +1,3 @@                                            ││                                                        │
└───────────────────────────────────────────────────────────┘└────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────── Commits ─────────────────────────────────────┐
│2022-01-24 22:49:26   foo@example.org                 (1/2)       File 4 added                                       │
│2022-01-24 22:49:27   bar@example.org                 (1/2)       File 4 modified                                    │
│2022-01-24 22:49:27   foo@example.org                 (1/2)       File 4 revised                                     │
│2022-01-24 22:49:27   bar@example.org                 (1/2)       File 1 modified                                    │
│2022-01-24 22:49:27   barbar@example.org              (1/2)       File 4 revised 2                                   │
│2022-01-24 22:49:27   foo@example.org                 (1/2)       File 4 revised 3                                   │
│2022-01-24 22:49:27   foo@example.org                 (1/2)       File 4 revised 4                                   │
│2022-01-24 22:49:27   bar@example.org                 (2/2)       File 1 revised2, File 4 revised 5                  │
│2022-01-24 22:49:27   foo@example.org                 (1/2)       File 4 revised 6                                   │
│                                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```
$ fixupChooser --list

9d5bc48	2022-01-23 20:30:24 <test@example.com> (1/2) File 4 revised
7901992	2022-01-23 20:30:24 <test@example.com> (1/2) File 1 modified
ce1294e	2022-01-23 20:30:24 <test@example.com> (1/2) File 4 revised 2
1b5c1bb	2022-01-23 20:30:24 <test@example.com> (1/2) File 4 revised 3
7885d33	2022-01-23 20:30:24 <test@example.com> (1/2) File 4 revised 4
af8b9a2	2022-01-23 20:30:24 <test@example.com> (2/2) File 1 revised2, File 4 revised 5
3a0553b	2022-01-23 20:30:24 <test@example.com> (1/2) File 4 revised 6
```

## Command options
```
usage: fixupChooser [-h] [--gui | --list ]

Help to rebase by selecting commit sha depending of files already staged

optional arguments:
  -h, --help  show this help message and exit
  --gui
  --list

```

`FIXUP_CHOOSER_ORIGIN` set the origin of the branch, if not set then `origin/master` is used, if it
does not exists, then `ALL` commits are processed

## How to Develop
```
$ make init
....
$ make test
```
