## ImGui Renderer Components: File Select
## File Select components for ImGui.

## Imports
import os
import imgui

## Classes
class FileSelectorComponent():
    """
    Allows for local file browsing and selection in ImGui.
    This includes class components to hanlde this.
    """
    def uiFileSelect(self):
        # Display the text input window
        imgui.begin(label="File Select", closable=False, flags=0)

        # self._fileBrowser = {
        #    "path": os.path.split(__file__)[0],
        #    "curInd": 0,
        #    "files": []
        # }

        # self._fileBrowser = {
        #    "path": os.path.split(__file__)[0],
        #    "files": {}
        # }

        # TODO: You definitely need to make this its own class

        # Top input bar
        imgui.push_item_width(-1.0)
        clicked, self._fileBrowser["path"] = imgui.input_text(label="", value=self._fileBrowser["path"], buffer_length=256)

        for f in self._fileBrowser["files"]:
            _, _ = imgui.selectable(f, False)

            if imgui.is_item_visible():
                if imgui.is_mouse_double_clicked():
                    print("Double")
                elif imgui.is_mouse_clicked():
                    print("Single")

        imgui.pop_item_width()

        imgui.end()