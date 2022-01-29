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
    def __init__(self, initialPath="./") -> None:
        """
        initialPath: A string path indicating the directory to start the file select in. Defaults to the present working directory.
        """
        # Get the current filepath
        self.fsFileDir = self.expandStringPath(initialPath)

        # Get the files at the start directory
        self._fsFilelist = os.listdir(self.fsFileDir)

        # Select the first item
        self._fsSelected = 0
        if len(self._fsFilelist) > 0:
            # Start with the top file
            self.fsSelectedFilepath = os.path.join(self.fsFileDir, self._fsFilelist[self._fsSelected])
        else:
            # Start with the current directory since it's empty
            self.fsSelectedFilepath = self.fsFileDir

        # Set the current input path
        self.fsInputPath = self.fsSelectedFilepath

    ## UI Functions
    def uiFileSelect(self):
        """
        Renders a File Select Ui.
        The currently selected path is accessible at `fsSelectedFilepath`.
        """
        # Display the text input window
        imgui.begin(label="File Select", closable=False, flags=0)

        # Get the available size for the window
        winSizeAvail = imgui.get_content_region_max()

        # Calculate top bar size
        barAddrW = (winSizeAvail[0] * .85)

        # Show top bar
        imgui.push_item_width(barAddrW)
        clicked, self.fsInputPath = imgui.input_text(label="", value=self.fsInputPath, buffer_length=256)
        imgui.pop_item_width()

        # Show top bar go button
        imgui.same_line()
        if imgui.button(label="Go", width=-1):
            pass

        # Directory content
        imgui.push_item_width(-1.0)

        for f in self._fsFilelist:
            _, _ = imgui.selectable(f, (f == os.path.basename(self.fsSelectedFilepath)))

            if imgui.is_item_hovered():
                if imgui.is_mouse_double_clicked():
                    # Entered
                    print(f"{f} (enter)")
                elif imgui.is_mouse_clicked():
                    # Selected
                    self._fsSetSelectedFile(f)

        imgui.pop_item_width()

        # End window
        imgui.end()

    ## Helper Functions
    def expandStringPath(self, path) -> str:
        """
        Expands a provided string path.

        path: A string path.

        Returns a cleaned string path.
        """
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        return path

    def _fsSetSelectedFile(self, filename):
        """
        Sets the currently selected file for the file select.

        filename: A string filename from the current directory to assign as selected.
        """
        # Check if the filename is present
        if filename in self._fsFilelist:
            # Set the selected file
            self._fsSelected = self._fsFilelist.index(filename)
            self.fsSelectedFilepath = os.path.join(self.fsFileDir, self._fsFilelist[self._fsSelected])
            self.fsInputPath = self.fsSelectedFilepath