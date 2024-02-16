from __future__ import annotations

import os
from collections.abc import Generator

import sublime
import sublime_plugin

from .libs.pylnk3 import Lnk
from .libs.pylnk3.exceptions import FormatException
from .libs.pylnk3.structures.extra_data import ExtraData_PropertyStoreDataBlock, PropertyStore

PACKAGE_NAME = __package__.partition(".")[0]


class FollowLnkViewEventListener(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(cls, settings: sublime.Settings) -> bool:
        return sublime.platform() == "windows"

    def on_load(self) -> None:
        if not (
            (window := self.view.window())
            and (path := self.view.file_name())
            and (target_path := self._resolve_lnk(path))
        ):
            return

        if os.path.isfile(target_path):
            view_group = window.get_view_index(self.view)[0]
            self.view.close()
            window.open_file(target_path, 0, view_group)
            return

        if os.path.isdir(target_path):
            project = window.project_data() or {}
            project.setdefault("folders", [])
            if target_path not in project["folders"]:
                project["folders"].append({"path": target_path})
            window.set_project_data(project)
            self.view.close()
            return

        raise RuntimeError(f"[{PACKAGE_NAME}] Uh, what's this: {path = }; {target_path = }")

    @classmethod
    def _resolve_lnk(cls, path: str) -> str | None:
        # note that ".lnk" can't be a shortcut of ".lnk"
        if lnk := cls._make_lnk(path):
            return cls._extract_lnk_target(lnk)
        return None

    @classmethod
    def _extract_extradata_propertystore(cls, lnk: Lnk) -> Generator[PropertyStore, None, None]:
        if not lnk.extra_data:
            return

        for block in lnk.extra_data.blocks:
            if isinstance(block, ExtraData_PropertyStoreDataBlock):
                yield from block.stores

    @classmethod
    def _extract_lnk_target(cls, lnk: Lnk) -> str:
        for store in cls._extract_extradata_propertystore(lnk):
            # print(f"[DEBUG] {str(store) = }")
            for name, value in store.properties:
                if name == 30:  # System.Link.TargetDOSName (?)
                    return str(value).partition(": ")[2].replace("\x00", "")  # this path is UTF-8

        return lnk.path  # this path may in a wrong encoding

    @staticmethod
    def _make_lnk(path: str) -> Lnk | None:
        if path.lower().endswith(".lnk"):
            try:
                return Lnk(path)
            except FormatException:
                return None
        return None
