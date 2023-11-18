import os
from typing import Optional, Set

import sublime
import sublime_plugin

from .libs.pylnk import pylnk3

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

        raise RuntimeError(f"[{PACKAGE_NAME}] Uh, what's this {path = }")

    @classmethod
    def _resolve_lnk(cls, path: str) -> Optional[str]:
        is_parsed = False
        seen_path: Set[str] = set((path,))
        while cls._is_lnk(path):
            if not (candidate := pylnk3.parse(path).path or ""):
                break
            if (path := candidate) in seen_path:
                return None  # there is a LNK cycle
            seen_path.add(path)
            is_parsed = True
        return path if is_parsed else None

    @classmethod
    def _is_lnk(cls, name: str) -> bool:
        return name.lower().endswith(".lnk")
