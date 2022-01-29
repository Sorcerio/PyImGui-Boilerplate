## ImGui Renderer Components: Alerts
## Alerts UI components for ImGui.

## Imports
import imgui

## Classes
class AlertsComponents():
    """
    Adds alert based functions to the subclass.
    """
    ## Functions
    def uiAlert(self, title, message):
        """
        Renders a simple alert panel.

        title: A string title for the panel.
        message: A string message to display in the panel.
        """
        # TODO: Figure out how to make this stupid thing a modal
        # Display the window
        imgui.begin(label=str(title), closable=True, flags=0)
        imgui.text(str(message))
        imgui.end()

    def uiError(self, message):
        """
        Renders an error panel.

        message: A string message to display in the panel.
        """
        # print(message)
        self.uiAlert("An Error Has Occured", message)