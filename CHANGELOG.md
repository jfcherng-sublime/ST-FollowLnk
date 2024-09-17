# FollowLnk Changelog

## 1.0.6

- feat: also works on init views

## 1.0.5

Package Control v4 is required due to the use of `more-itertools` py38 dependency.

- refactor: use `more-itertools`
- chore: add `more-itertools` as a dependency

## 1.0.4

- fix: improve parsing LNK for non-ansi target path
- refactor: replace `pylnk3` with `LnkParse3`

## 1.0.3

- fix: modules should be reloaded when update plugin
- refactor: simplify boot.py

## 1.0.2

- refactor: only run on Windows OS

## 1.0.1

- fix: support following `.lnk` to a folder
- fix: do not follow `.lnk` which points to another `.lnk`

## 1.0.0

- initial release
