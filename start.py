## ImGui Boilerplate
## Runs the base, unmodified, menu.

## Imports
from imguiRenderer.renderer import PygletImGuiFull

## Execution
if __name__ == "__main__":
    runner = PygletImGuiFull()
    runner.present("ImGui Boilerplater Demo")