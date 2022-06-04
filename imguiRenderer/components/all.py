## ImGui Renderer Components: All Components
## Provides a special class to provide all included components to the subclass.

## Imports
from .alerts import AlertsComponents
from .inputs import InputComponents
from .fileSelect import FileSelectorComponent
from .generalUi import GeneralUiFunctions

## Classes
class AllComponents(AlertsComponents, InputComponents, FileSelectorComponent, GeneralUiFunctions):
    """
    Includes access to all components and their class components.
    """
    ## Constructor
    def __init__(self) -> None:
        super(AlertsComponents, self).__init__()
        super(InputComponents, self).__init__()
        super(FileSelectorComponent, self).__init__()
        super(GeneralUiFunctions, self).__init__()
