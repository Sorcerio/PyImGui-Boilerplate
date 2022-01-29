## ImGui Boilerplate
## Runs the base, unmodified, menu.

## Imports
from imguiRenderer.renderer import PygletImGui

## Execution
if __name__ == "__main__":
    runner = PygletImGui()
    runner.present("ImGui Boilerplater Demo")