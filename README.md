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
┌───────────────── Commit ─────────────────┐┌─────────────────────────── Staged files ───────────────────────┐
│Date: 2022-01-23 21:23:00                 ││  10 +++ b/src/file1.txt                                        │
│                                          ││  11 @@ -1 +1,2 @@                                              │
│Committer: test@example.com               ││  12  modification 2                                            │
│                                          ││  13 +modification 2.5.1                                        │
│Message: File 1 revised2, File 4 revised 5││  14 diff --git a/src/file4.txt b/src/file4.txt                 │
│                                          ││  15 index dc7ce73..f5843fc 100644                              │
│Files: (2/2)                              ││  16 --- a/src/file4.txt                                        │
│------------------------------------------││  17 +++ b/src/file4.txt                                        │
│src/file1.txt                             ││  18 @@ -3,3 +3,4 @@                                            │
│src/file4.txt                             ││  19  modification 2.2                                          │
│                                          ││  20  modification 2.3                                          │
│                                          ││  21  modification 2.4                                          │
│                                          ││  22 +modification 2.5.2                                        │
└──────────────────────────────────────────┘└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────── Commits ─────────────────────────────────────────────────────────────┐
│02f12ac     2022-01-23 21:22:59   test@example.com        (1/2)       File 4 revised                        │
│702f0ba     2022-01-23 21:23:00   test@example.com        (1/2)       File 1 modified                       │
│878d358     2022-01-23 21:23:00   test@example.com        (1/2)       File 4 revised 2                      │
│4d2b453     2022-01-23 21:23:00   test@example.com        (1/2)       File 4 revised 3                      │
│81f660b     2022-01-23 21:23:00   test@example.com        (1/2)       File 4 revised 4                      │
│985381d     2022-01-23 21:23:00   test@example.com        (2/2)     * File 1 revised2, File 4 revised 5     │
│5db4e30     2022-01-23 21:23:00   test@example.com        (1/2)       File 4 revised 6                      │
│                                                                                                            │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
usage: fixupChooser [-h] [--fzf | --list | --curses | --show] [--sha SHA]

Help to rebase by selecting commit sha depending of files already staged

optional arguments:
  -h, --help  show this help message and exit
  --curses
  --fzf
  --list
  --show
  --sha SHA

```

`FIXUP_CHOOSER_ORIGIN` set the origin of the branch, if not set then `origin/master` is used, if it
does not exists, then `ALL` commits are processed

## How to Develop
```
$ make init
....
$ make test
```
