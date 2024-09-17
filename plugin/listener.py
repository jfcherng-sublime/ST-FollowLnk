from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import sublime
import sublime_plugin
from more_itertools import first_true

from .constants import PLUGIN_NAME
from .libs.LnkParse3.extra.metadata import Metadata, SerializedPropertyStorage, SerializedPropertyValueIntegerName
from .libs.LnkParse3.lnk_file import LnkFile


class FollowLnkEventListener(sublime_plugin.EventListener):
    @classmethod
    def is_applicable(cls, settings: sublime.Settings) -> bool:
        return sublime.platform() == "windows"

    def on_init(self, views: list[sublime.View]) -> None:
        for view in views:
            _handle_view(view)


class FollowLnkViewEventListener(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(cls, settings: sublime.Settings) -> bool:
        return sublime.platform() == "windows"

    def on_load(self) -> None:
        _handle_view(self.view)


def _handle_view(view: sublime.View) -> None:
    if not ((window := view.window()) and (path := view.file_name()) and (target_path := _resolve_lnk(path))):
        return

    if os.path.isfile(target_path):
        view_group = window.get_view_index(view)[0]
        view.close()
        window.open_file(target_path, 0, view_group)
        return

    if os.path.isdir(target_path):
        project = window.project_data() or {}
        project.setdefault("folders", [])
        if target_path not in project["folders"]:
            project["folders"].append({"path": target_path})
        window.set_project_data(project)
        view.close()
        return

    raise RuntimeError(f"[{PLUGIN_NAME}] Uh, what's this: {path = }; {target_path = }")


def _resolve_lnk(path: str) -> str | None:
    if not (lnk_file := _make_lnk_file(path)):
        return None

    # print(f"[DEBUG] {lnk_file.get_json() = }")

    try:
        return first_true(_list_lnk_targets(lnk_file, lnk_path=path))
    except Exception:
        return None


def _list_lnk_targets(lnk_file: LnkFile, *, lnk_path: str | None = None) -> Generator[str, None, None]:
    string_data_dict = lnk_file.string_data.as_dict()

    # from property: relative path
    if lnk_path and lnk_file.has_relative_path():
        path = Path(lnk_path).parent / string_data_dict["relative_path"]
        yield str(path.resolve())

    # from metadata
    for extra in lnk_file.extras:
        if isinstance(extra, Metadata):
            for store in extra.property_store():
                assert isinstance(store, SerializedPropertyStorage)
                if store.format_id() == "28636AA6-953D-11D2-B5D6-00C04FD918D0":
                    for prop in store.serialized_property_values():
                        if isinstance(prop, SerializedPropertyValueIntegerName) and prop.id() == 30:
                            yield prop.value().value()  # type: ignore

    # from info
    if lnk_file.info:
        try:
            if target := lnk_file.info.local_base_path_unicode():
                yield target
        except Exception:
            pass
        try:
            if target := lnk_file.info.local_base_path():
                yield target
        except Exception:
            pass


def _make_lnk_file(path: str) -> LnkFile | None:
    if path.lower().endswith(".lnk"):
        with open(path, "rb") as indata:
            return LnkFile(indata)
    return None
