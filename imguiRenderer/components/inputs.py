## ImGui Renderer Components: Input
## Input UI components for ImGui.

## Imports
import imgui

## Classes
class InputComponents():
    """
    Adds input based components to the subclass.
    This includes a system to handle multiple text inputs gracefully.
    """
    ## Statics
    BAD_RESPONSE = "Invalid Tag"

    ## Constructor
    def __init__(self) -> None:
        # Assign variables
        self._textInputValues = {}

    ## Functions
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

        fromTag: The tag to return the associated input string from. If the tag does not exist, the `BAD_RESPONSE` value is returned instead.
        """
        if fromTag in self._textInputValues:
            return self._textInputValues[fromTag]

        return InputComponents.BAD_RESPONSE