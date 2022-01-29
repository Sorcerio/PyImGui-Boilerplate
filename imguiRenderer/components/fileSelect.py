## ImGui Renderer Components: File Select
## File Select components for ImGui.

## Imports
import os
import imgui

class FileSelectorComponent():
    """
    Allows for local file browsing and selection in ImGui.
    This includes class components to handle this.
    """
    ## Constructor
    def __init__(self) -> None:
        # Assign variables
        self.fsFilepath = self.expandStringPath("./")
        self._fsFilelist = []

    ## Functions
    def uiFileSelect(self):
        """
        Renders a File Select Ui.
        The currently selected path is accessible at `fsFilepath`.
        """
        # Display the text input window
        imgui.begin(label="File Select", closable=False, flags=0)

        # Get the available size for the window
        winSizeAvail = imgui.get_content_region_max()

        # Calculate top bar size
        barAddrW = (winSizeAvail[0] * .85)

        # Show top bar
        imgui.push_item_width(barAddrW)
        clicked, self.fsFilepath = imgui.input_text(label="", value=self.fsFilepath, buffer_length=256)
        imgui.pop_item_width()

        print(imgui.get_content_region_max())

        # Show top bar go button
        imgui.same_line()
        if imgui.button(label="Go", width=-1):
            pass

        # Directory content
        imgui.push_item_width(-1.0)
        for f in self._fsFilelist:
            _, _ = imgui.selectable(f, False)

            if imgui.is_item_visible():
                if imgui.is_mouse_double_clicked():
                    print("Double")
                elif imgui.is_mouse_clicked():
                    print("Single")
        imgui.pop_item_width()

        imgui.end()

    def expandStringPath(self, path) -> str:
        """
        Expands a provided string path.

        path: A string path.

        Returns a cleaned string path.
        """
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        return path