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
    ## Statics
    FS_BACK_INDICATOR = ".."
    FS_START_PATH = "./"

    ## Constructor
    def __init__(self) -> None:
        # Set initial variables
        self._fsIsOpen = False

    ## UI Functions
    def uiFileSelect(self, completion = None, selectButton = "Open", cancelButton = "Cancel"):
        """
        Renders a File Select Ui.
        The currently selected path is accessible at `fsSelectedFilepath`.

        completion: A function to execute when the select or cancel buttons are pressed. This function must has 1 parameter to take the selected filepath. `None` will be sent to the provided completion function if the cancel action is taken. Provide `None` here to provide no completion.
        selectButton: A string to label the open action button with.
        cancelButton: A string to label the cancel action button with. Provide `None` to show no cancel option.
        """
        # Check if the file select is not yet open
        if not self._fsIsOpen:
            # Show the initial directory
            self._fsSetToProvidedDir(FileSelectorComponent.FS_START_PATH)

            # Mark as open
            self._fsIsOpen = True

        # Display the text input window
        imgui.begin(label="File Select", closable=False, flags=0)

        # Get the available size for the window
        winSizeAvail = imgui.get_content_region_max()

        # Calculate top bar size
        barAddrW = (winSizeAvail[0] * .85)

        # Show top bar
        imgui.push_item_width(barAddrW)
        clicked, self._fsInputPath = imgui.input_text(label="", value=self._fsInputPath, buffer_length=256)
        imgui.pop_item_width()

        # Show top bar go button
        imgui.same_line()
        if imgui.button(label="Go", width=-1):
            self._fsSetToProvidedDir(self._fsInputPath)

        # Show directory content
        imgui.push_item_width(-1.0)

        for f in self._fsFilelist:
            # Decide if a directory
            isDir = os.path.isdir(os.path.join(self.fsFileDir, f))

            # Create the ui label name
            label = f
            if isDir:
                label += "/"

            # Render the selectable
            _, _ = imgui.selectable(label, (f == os.path.basename(self.fsSelectedFilepath)))

            # Handle selectable interaction
            if imgui.is_item_hovered():
                # Check type of click
                if imgui.is_mouse_double_clicked():
                    # Attempt to Enter or Execute
                    if isDir:
                        # Enter directory
                        self._fsSetSelectedDir(f)
                    else:
                        # Execute file
                        pass
                elif imgui.is_mouse_clicked():
                    # Selected
                    self._fsSetSelectedFile(f)

        imgui.pop_item_width()

        # Show completion buttons
        # Check if a cancel option is available
        if cancelButton != None:
            # Both buttons
            # Calculate button size
            btnCompW = round(winSizeAvail[0] / 2)

            if imgui.button(label=selectButton, width=btnCompW):
                self._fsCompleteSelect(completion)

            imgui.same_line()
            if imgui.button(label=cancelButton, width=btnCompW):
                self._fsCompleteCancel(completion)
        else:
            # Only select button
            if imgui.button(label=selectButton, width=-1.0):
                self._fsCompleteSelect(completion)

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
            # Set the selected file normally
            self._fsSelected = self._fsFilelist.index(filename)

            if filename != FileSelectorComponent.FS_BACK_INDICATOR:
                self.fsSelectedFilepath = os.path.join(self.fsFileDir, self._fsFilelist[self._fsSelected])
            else:
                self.fsSelectedFilepath = self.fsFileDir

            self._fsInputPath = self.fsSelectedFilepath

    def _fsSetSelectedDir(self, dirname):
        """
        Navigates the currently focused directory into the one provided.

        dirname: A string directory name from the current directory to focus.
        """
        # Check if the directory name is present
        if dirname in self._fsFilelist:
            # Resolve the full new path
            dirPath = os.path.join(self.fsFileDir, dirname)

            # Check if a directory
            if os.path.isdir(dirPath):
                # Set the new target directory
                self.fsFileDir = self.expandStringPath(dirPath)

                # Get the files at the start directory
                self._fsFilelist = sorted(os.listdir(self.fsFileDir))

                # Add controls to the file list
                self._fsFilelist.insert(0, FileSelectorComponent.FS_BACK_INDICATOR)

                # Select the first item
                self._fsSelected = 0
                self.fsSelectedFilepath = self.fsFileDir

                # Set the current input path
                self._fsInputPath = self.fsSelectedFilepath

    def _fsSetToProvidedDir(self, dirPath):
        """
        Sets the currently focused directory to the provided.

        dirPath: A string directory path to focus on.
        """
        # Expand the dirpath
        dirPath = self.expandStringPath(dirPath)

        # Check if the dirpath is a directory
        if os.path.isdir(dirPath):
            # Proceed with this directory
            # Get the starting dir name
            startingDir = os.path.basename(dirPath)

            # Focus on the provided directory
            self.fsFileDir = self.expandStringPath(os.path.join(dirPath, "../"))
            self._fsFilelist = os.listdir(self.fsFileDir)
            self._fsSetSelectedDir(startingDir)
        else:
            # Get the file's directory name
            self._fsSetToProvidedDir(os.path.dirname(dirPath))

    def _fsCompleteSelect(self, completion):
        """
        Completes the file select with as a selection action.

        completion: A function to call in completetion. Provide `None` for no completion.
        """
        if completion != None:
            completion(self._fsInputPath)

        self.fsSelectedFilepath = self._fsInputPath
        self._fsIsOpen = False

    def _fsCompleteCancel(self, completion):
        """
        Completes the file select with as a cancel action.

        completion: A function to call in completetion. Provide `None` for no completion.
        """
        if completion != None:
            completion(None)

        self.fsSelectedFilepath = None
        self._fsIsOpen = False