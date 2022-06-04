## ImGui Renderer Components: Input
## Input UI components for ImGui.

## Imports
import os
import subprocess
import platform
import imgui

## Classes
class GeneralUiFunctions():
    """
    Adds functions for generalized, more complex UI features like external linkouts.
    """
    ## Functions
    def linkoutButton(self, title: str, filepath: str):
        """
        Renders an Imgui button that links out to the provided filepath.

        title: A string to preface the link out button with.
        filepath: A string filepath.
        """
        imgui.text(f"{title}: ")
        imgui.same_line()
        if imgui.button(f"... {filepath[-32:]}"):
            self._openFilepathExternally(filepath)
        self._addTooltip("Open externally")

    ## Private Functions
    def _openFilepathExternally(self, path):
        """
        Opens the filepath in the external file browser.

        path: A string path to the file.
        """
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])