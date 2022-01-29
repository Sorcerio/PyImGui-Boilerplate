## ImGui Renderer
# A Pyglet render protocol wrapper to render with ImGui.

## Imports
import os
import pyglet
from pyglet import gl, image
import imgui
from imgui.integrations.pyglet import create_renderer
from .testwindow import show_test_window

## Constants
DEFAULT_WIN_WIDTH = 1280
DEFAULT_WIN_HEIGHT = 720
DEFAULT_WIN_SIZE = (DEFAULT_WIN_WIDTH, DEFAULT_WIN_HEIGHT)
DEFAULT_FULLSCREEN = False
DEFAULT_MAXIMIZE = False

TAG_BAD_RESPONSE = "Invalid Tag"

## Classes
class PygletImGui():
    # Support Docs: https://pyglet.readthedocs.io/en/latest/programming_guide/windowing.html
    """
    A wrapper for Pyglet that allows ImGui to be rendered directly.
    """
    ## Constructor
    def __init__(self) -> None:
        """
        Constructs the PygletImgui Renderer.
        Run `present(...)` to present the window.
        """
        # Get the current directory path
        curDirPath = os.path.split(__file__)[0]

        # Assign variables
        self.window = None
        self._renderer = None
        self._textInputValues = {}
        self._fileBrowser = {
            "path": curDirPath,
            "curInd": 0,
            "files": sorted(os.listdir(path=curDirPath))
        }

    ## Methods
    def present(self, title, maximize = DEFAULT_MAXIMIZE, fullscreen = DEFAULT_FULLSCREEN, size = DEFAULT_WIN_SIZE):
        """
        When called, opens the Pyglet window and renders the configured content.

        title: A string title to present on the window.
        fullscreen: A bool inidicating if the window should start in fullscreen.
        size: A tuple representing the initial window size as (width, height).
        """
        # Get the directory of the package
        packageDir = os.path.split(__file__)[0]

        # Create the render window
        self.window = pyglet.window.Window(width=size[0], height=size[1], resizable=True, caption=title)
        gl.glClearColor(0, 0, 0, 0)

        # Setup events
        self.window.on_resize = self.onResize
        self.window.on_key_press = self.onKeyPress
        self.window.on_key_release = self.onKeyRelease

        # Build icon paths
        icon16Path = os.path.join(packageDir, "icons", "16.png")
        icon32Path = os.path.join(packageDir, "icons", "32.png")
        icon64Path = os.path.join(packageDir, "icons", "64.png")
        icon128Path = os.path.join(packageDir, "icons", "128.png")

        # Set the icons
        self.window.set_icon(
            image.load(icon16Path),
            image.load(icon32Path),
            image.load(icon64Path),
            image.load(icon128Path)
        )

        # Maximize if needed
        if maximize:
            self.window.maximize()

        # Mark fullscreen status
        self.window.set_fullscreen(fullscreen)

        # Setup rendering
        imgui.create_context()
        self._renderer = create_renderer(self.window)
        pyglet.clock.schedule_interval(self._draw, 1/120.)

        # Open the window
        pyglet.app.run()
        self._renderer.shutdown()

    def setTitle(self, title):
        """
        Sets the title of the window to the new `title`.

        title: A string title to present on the window.
        """
        self.window.set_caption(title)

    def addImguiTooltip(self, text):
        """
        When called before an ImGui element adds a tooltip.
        From ImGui.

        text: A string to add to the tooltip.
        """
        imgui.text_disabled("(?)")
        if imgui.is_item_hovered():
            imgui.begin_tooltip()
            imgui.push_text_wrap_pos(imgui.get_font_size() * 35.0)
            imgui.text_unformatted(text)
            imgui.pop_text_wrap_pos()
            imgui.end_tooltip()

    ## Render Methods
    def renderImgui(self, data):
        """
        Configures what ImGui content will be shown.

        Overide this function to change the Gui.

        data: Some number?
        """
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        show_test_window()

        imgui.begin("Custom window", True)
        imgui.text("Bar")
        imgui.text_colored("Eggs", 0.2, 1., 0.)

        imgui.text_ansi("B\033[31marA\033[mnsi ")
        imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)

        imgui.end()

    def renderBackground(self, data):
        """
        Configures what regular render content will be shown.

        Overide this function to render under the Gui.

        data: Some number?
        """
        pass

    ## Event Methods
    def onResize(self, width, height):
        """
        Called when the window is resized.

        width: The new width.
        height: The new height.
        """
        pass

    def onKeyPress(self, symbol, modifiers):
        """
        Called when a key combination is pressed.
        Key values can be found in `pyglet.window.key`.

        symbol: An int related to a Pyglet key value.
        modifiers: Bitwise combination of active key modifiers.
        """
        pass

    def onKeyRelease(self, symbol, modifiers):
        """
        Called when a key combination is released.
        Key values can be found in `pyglet.window.key`.

        symbol: An int related to a Pyglet key value.
        modifiers: Bitwise combination of active key modifiers.
        """
        pass

    ## UI Components
    def uiTextInput(self, title: str, message: str, button: str, action, tag: str = None, bufferLength: int = 64):
        """
        Renders a text input window with a single text field and a labeled button.
        The text input values are stored in `_textInputValues` under the provided `tag`.
        Does _not_ accept empty strings as valid input.

        title: A string title for the window. Must be unique or supply a `tag`. Will be used as the `tag` if no identifier is provided. No warning will occur if a tag is duplicated due to the nature of ImGui rendering.
        message: A string message to display to the user.
        button: A string to label the button with.
        action: A function to call when the button is pressed. The function should have one parameter to accept the inputed string.
        tag: A string identifier for the text input's value. Will use `title` if `None` is provided.
        bufferLength: An int representing the max length of any text input.
        """
        # Supply a tag if needed
        if (tag == None) or (tag.strip() == ""):
            tag == title

        # Check if the value needs to be init
        if not (tag in self._textInputValues):
            self._textInputValues[tag] = ""

        # Display the text input window
        imgui.begin(label=str(title), closable=False, flags=0)

        imgui.text(str(message))

        clicked, self._textInputValues[tag] = imgui.input_text(label="", value=self._textInputValues[tag], buffer_length=bufferLength)

        if imgui.button(label=str(button)):
            # Call the provided function
            if self._textInputValues[tag] != "":
                action(self._textInputValues[tag])

        imgui.end()

    def text(self, fromTag) -> str:
        """
        Returns the input string associated with the provided tag.
        For use with `uiTextInput(...)`.

        fromTag: The tag to return the associated input string from. If the tag does not exist, the `TAG_BAD_RESPONSE` value is returned instead.
        """
        if fromTag in self._textInputValues:
            return self._textInputValues[fromTag]

        return TAG_BAD_RESPONSE

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

    ## Static Methods
    def _draw(self, data):
        """
        Pyglet's `draw` function.
        Called to render each frame.

        data: Some number?
        """
        # Display pregui render
        self.renderBackground(data)

        # Display ImGui
        self.renderImgui(data)

        # Reset window
        self.window.clear()

        # Render the frame
        imgui.render()
        self._renderer.render(imgui.get_draw_data())