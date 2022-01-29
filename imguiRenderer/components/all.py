## ImGui Renderer Components: All Components
## Provides a special class to provide all included components to the subclass.

## Imports
from .alerts import AlertsComponents
from .inputs import InputComponents
from .fileSelect import FileSelectorComponent

## Classes
class AllComponents(AlertsComponents, InputComponents, FileSelectorComponent):
    pass