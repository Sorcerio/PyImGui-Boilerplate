## ImGui Renderer Components: File Select
## File Select components for ImGui.

## Imports
import os
import imgui

# self._fileBrowser = {
#    "path": os.path.split(__file__)[0],
#    "curInd": 0,
#    "files": []
# }

# self._fileBrowser = {
#    "path": os.path.split(__file__)[0],
#    "files": {}
# }

class FileSelectorComponent():
    """
    Allows for local file browsing and selection in ImGui.
    This includes class components to handle this.
    """
    ## Constructor
    def __init__(self) -> None:
        # Assign variables
        self.fsFilepath = "./"
        self._fsFilelist = []

    ## Functions
    def uiFileSelect(self):
        """
        Renders a File Select Ui.
        """
        # Display the text input window
        imgui.begin(label="File Select", closable=False, flags=0)

        # Top input bar
        imgui.push_item_width(-1.0)
        clicked, self.fsFilepath = imgui.input_text(label="", value=self.fsFilepath, buffer_length=256)

        # Directory content
        for f in self._fsFilelist:
            _, _ = imgui.selectable(f, False)

            if imgui.is_item_visible():
                if imgui.is_mouse_double_clicked():
                    print("Double")
                elif imgui.is_mouse_clicked():
                    print("Single")

        imgui.pop_item_width()

        imgui.end()