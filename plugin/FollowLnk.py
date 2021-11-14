from .libs.pylnk import pylnk3
import sublime_plugin


PACKAGE_NAME = __package__.partition(".")[0]


class FollowLnk(sublime_plugin.ViewEventListener):
    def on_load(self) -> None:
        if not (
            # ...
            (window := self.view.window())
            and (path := self.view.file_name())
            and path.lower().endswith(".lnk")
        ):
            return

        info = pylnk3.parse(path)
        if not (target_path := info.path):
            print(f"[{PACKAGE_NAME}] Unable to determinate the target path with information: {info}")
            return

        view_group = window.get_view_index(self.view)[0]
        self.view.close()
        window.open_file(target_path, 0, view_group)
