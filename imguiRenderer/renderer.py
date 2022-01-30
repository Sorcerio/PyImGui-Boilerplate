## ImGui Renderer
# A Pyglet render protocol wrapper to render with ImGui.

## Imports
import os
import pyglet
from pyglet import gl, image
import imgui
from imgui.integrations.pyglet import create_renderer

from .testwindow import show_test_window
from .components.all import AllComponents

## Constants
DEFAULT_WIN_WIDTH = 1280
DEFAULT_WIN_HEIGHT = 720
DEFAULT_WIN_SIZE = (DEFAULT_WIN_WIDTH, DEFAULT_WIN_HEIGHT)
DEFAULT_FULLSCREEN = False
DEFAULT_MAXIMIZE = False

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
        # Init the supers
        super(PygletImGui, self).__init__()

        # Assign variables
        self.window = None
        self._renderer = None

    ## Methods
    def present(self, title, maximize = DEFAULT_MAXIMIZE, fullscreen = DEFAULT_FULLSCREEN, size = DEFAULT_WIN_SIZE, iconsPath = None):
        """
        When called, opens the Pyglet window and renders the configured content.

        title: A string title to present on the window.
        fullscreen: A bool inidicating if the window should start in fullscreen.
        size: A tuple representing the initial window size as (width, height).
        iconsPath: A string directory path indicating where the 16x16, 32x32, 64x64, and 128x128 PNG icon images are stored. Supply `None` to resolve the two default locations. These being any encompasing package's icons at `../icons` and this package's included default icons at `./icons`.
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

        # Check for a supplied icons package
        if not ((iconsPath != None) and (os.path.isdir(os.path.abspath(iconsPath)))):
            # Resolve default icon locations
            iconsPath = os.path.join(packageDir, "../", "icons")

            if not os.path.isdir(iconsPath):
                # Load default icons package
                iconsPath = os.path.join(packageDir, "icons")
        else:
            # Make sure its a full path
            iconsPath = os.path.abspath(iconsPath)

        # Set the icons
        self.window.set_icon(
            image.load(os.path.join(iconsPath, "16.png")),
            image.load(os.path.join(iconsPath, "32.png")),
            image.load(os.path.join(iconsPath, "64.png")),
            image.load(os.path.join(iconsPath, "128.png"))
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
        # Start the Frame
        imgui.new_frame()

        # Configure the menu bar
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        # Run the default ImGui test window
        show_test_window()

        # Run another demo ImGui window
        imgui.begin("Custom window", True)
        imgui.text("Bar")
        imgui.text_colored("Eggs", 0.2, 1., 0.)

        imgui.text_ansi("B\033[31marA\033[mnsi ")
        imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)

        imgui.end() # Ends building of "Custom Window". Does _not_ end the frame.

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

class PygletImGuiFull(PygletImGui, AllComponents):
    """
    A wrapper for Pyglet that allows ImGui to be rendered directly.
    Also includes all extra UI components.
    """
    ## Constructor
    def __init__(self) -> None:
        """
        Constructs the PygletImgui Renderer.
        Run `present(...)` to present the window.
        """
        # Init the supers
        super(PygletImGuiFull, self).__init__()

    ## Render Methods
    def renderImgui(self, data):
        """
        Configures what ImGui content will be shown.

        Overide this function to change the Gui.

        data: Some number?
        """
        # Run the super
        super(PygletImGuiFull, self).renderImgui(data)

        # Show the test windows
        self.uiError("This is a demo error.")

        def textInputAction(answer):
            print(f"Text Input: {answer}")
        self.uiTextInput("Text Input", "This is a demo text input.", "Submit", textInputAction)

        def fileSelectComp(filepath):
            print(f"File Selected: {filepath}")
        self.uiFileSelect(completion=fileSelectComp)