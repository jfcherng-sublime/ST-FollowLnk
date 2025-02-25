# ST-FollowLnk

[![Required ST Build](https://img.shields.io/badge/ST-4105+-orange.svg?style=flat-square&logo=sublime-text)](https://www.sublimetext.com)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/jfcherng-sublime/ST-FollowLnk/python.yml?branch=main&style=flat-square)](https://github.com/jfcherng-sublime/ST-FollowLnk/actions)
[![Package Control](https://img.shields.io/packagecontrol/dt/FollowLnk?style=flat-square)](https://packagecontrol.io/packages/FollowLnk)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/jfcherng-sublime/ST-FollowLnk?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-FollowLnk/tags)
[![Project license](https://img.shields.io/github/license/jfcherng-sublime/ST-FollowLnk?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-FollowLnk/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jfcherng-sublime/ST-FollowLnk?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-FollowLnk/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/jfcherng/5usd)

`FollowLnk` is a Sublime Text plugin which opens the target file of a `.lnk` (Windows shortcut) file
instead of the `.lnk` file itself.

## Installation

This plugin is available on [Package Control][package-control] by the name of [FollowLnk][followlnk].

[followlnk]: https://packagecontrol.io/packages/FollowLnk
[package-control]: https://packagecontrol.io

## Implementation Details

Actually, Sublime Text will still open the `.lnk` file first.
And then this plugin opens the target file and closes the `.lnk` file.
