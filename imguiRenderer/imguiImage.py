## ImGui Image
# Object that contains information needed to render images within ImGui more easily.

## Imports
import os
from turtle import back
import imgui
from io import BytesIO
from PIL import Image
from pyglet import image as pygletImage

## Classes
class ImguiImage():
    """
    Object that contains information needed to render images within ImGui more easily.
    """
    # Constructor
    def __init__(self, filepath: str, metadata=None, thumbLimit=(1280, 720), verbose=False):
        """
        path: A string filepath poiting to the image file.
        metadata: A dict of additonal data for the item. Can also provided `None` for no additonal data.
        thumbLimits: A tuple representing the maximum long and short sides of the generated thumbnail display texture as (long side length, short side length). Provide `None` to use the image's real size.
        verbose: If `True`, enables verbose output.
        """
        # Provided
        self.path = filepath
        self.metadata = metadata
        self.verbose = verbose
        self._thumbLimit = thumbLimit

        # Assigned
        self.loaded = False
        self._tempFile = None
        self._texture = None

    ## Internal
    def __str__(self) -> str:
        return f"\"{self.title}\" at \"{self.path}\""

    def __repr__(self) -> str:
        return f"<{self.title}_{self.__hash__()}>"

    def __del__(self):
        self.close()

    def __hash__(self) -> int:
        return hash(self.path)

    # Functions
    def load(self, skipTexture = False, background: tuple = None):
        """
        Loads the image into a temporary file if it is remote.
        If the file is local, the image is prepared.

        skipTexture: If True, the display texture will not preloaded.
        background: A tuple containing a background color to add behind the image as (r, g, b)[255]. Supply `None` to indicate no background should be added.
        """
        # Close if a previous exists
        if self._tempFile != None:
            self._tempFile.close()

        # Check if the local file exists
        if os.path.isfile(self.path):
            # Check if background color provided
            if background != None:
                # Create background image
                # Open the target image
                with Image.open(self.path) as targetImg:
                    # Create working image
                    workingImg = Image.new("RGBA", targetImg.size, background)

                    # Paste the target image into the background
                    workingImg.paste(targetImg, (0, 0), targetImg)
            else:
                # Open the image
                workingImg = Image.open(self.path)

            # Flip the image for texture display
            self._tempFile = workingImg.transpose(Image.FLIP_TOP_BOTTOM)

            # Preload the texture
            if not skipTexture:
                self._preloadTexture()

            # Verbose
            if self.verbose:
                if len(self.path) > 64:
                    sPath = f"{self.path[:64]} ..."
                else:
                    sPath = self.path

                print(f"Loaded \"{sPath}\".")

            # Mark as loaded
            self.loaded = True
            workingImg.close()
        else:
            # Report the problem and release the tempfile
            print(f"{self} has been provided with incorrect path information.")

            # Mark as failed
            self.loaded = False

    def close(self):
        """
        Explicitly closes any loaded temporary files.
        """
        # Mark as not loaded
        self.loaded = False

        # Clean temp file
        if self._tempFile != None:
            self._tempFile.close()
            self._tempFile = None

    def draw(self, containerSize: tuple, shouldFit: bool = True, center: bool = True, offset = (0, 0), border=(0, 0, 0, 0)):
        """
        Draws this image into an ImGui window as an ImGui Image.

        containerSize: A tuple containing the container's size as (width, height).
        shouldFit: A boolean indicating if the source image should fit within the content area or cover the content area. Fit is indicated by `True` and ensures the whole source image will be seen but some background color may be visible. Cover is indicated by `False` and ensures that the entirety of the content area will be covered but the source image will likely be cropped.
        center: A boolean indicating if the rendered image should be centered in the provided `containerSize`.
        offset: A tuple containing points of offset for the image as (x, y).
        border: An RGBA tuple containing a border color as (r, g, b, a).
        """
        # Check if image item was loaded
        if self.loaded:
            # Get the texture
            tex = self.getTexture()

            # Draw the texture
            ImguiImage.drawTexture(
                tex,
                self.size(),
                containerSize,
                shouldFit,
                center,
                offset,
                border
            )
        else:
            # Draw text instead
            imgui.text("Image has not been loaded.")

    def drawButton(self, containerSize: tuple, shouldFit: bool = True, center: bool = True, offset = (0, 0), border=(0, 0, 0, 0)) -> bool:
        """
        Draws this image into an ImGui window as an ImGui Image.

        containerSize: A tuple containing the container's size as (width, height).
        shouldFit: A boolean indicating if the source image should fit within the content area or cover the content area. Fit is indicated by `True` and ensures the whole source image will be seen but some background color may be visible. Cover is indicated by `False` and ensures that the entirety of the content area will be covered but the source image will likely be cropped.
        center: A boolean indicating if the rendered image should be centered in the provided `containerSize`.
        offset: A tuple containing points of offset for the image as (x, y).
        border: An RGBA tuple containing a border color as (r, g, b, a).
        """
        # Check if image item was loaded
        if self.loaded:
            # Get the texture
            tex = self.getTexture()

            # Draw the texture
            return ImguiImage.drawTexture(
                tex,
                self.size(),
                containerSize,
                shouldFit,
                center,
                offset,
                border,
                asButton=True
            )
        else:
            # Draw text instead
            imgui.text("Image has not been loaded.")
            return False

    def size(self):
        """
        Returns the size of the loaded image as a tuple like (width, height).

        If the image has not yet been loaded, it is loaded first.
        """
        # Load the image if needed
        if not self.loaded:
            self.load()

        return self._tempFile.size

    def getTexture(self):
        """
        Gets the thumbnail size display texture for this image.
        Aspect ratio will be maintained.
        The original image will not be modified.

        Returns a GL compatible texture.
        """
        # Load the image if needed
        if not self.loaded:
            self.load()

        # Check if the texture is not loaded
        if self._texture == None:
            self._preloadTexture()

        return self._texture

    ## Private functions
    def _preloadTexture(self):
        """
        Preloads the display texture for this image.
        """
        # Create thumbnail
        imgThumb = self._tempFile.copy()

        if self._thumbLimit != None:
            if imgThumb.size[0] > imgThumb.size[1]:
                # Width > height
                imgThumb.thumbnail((self._thumbLimit[0], self._thumbLimit[1]))
            else:
                # Height > width
                imgThumb.thumbnail((self._thumbLimit[1], self._thumbLimit[0]))

        # Get the image bytes
        imgBytes = BytesIO()
        imgThumb.save(imgBytes, "png")
        imgBytes.seek(0)

        # Open pyglet image
        # NOTE: This extension might need to be specific
        imgPig = pygletImage.load("hint.png", file=imgBytes)

        # Get the texture
        self._texture = imgPig.get_texture()

        # Close the thumbnail
        imgThumb.close()

    # Static Functions
    def nearestPowerOfTwo(x):
        """
        Calculates the nearest power of two (+ or -) for `x`.

        x: A number.
        """
        return 1 << (x - 1).bit_length()

    def calculateContentBestSize(contentSize: tuple, containerSize: tuple, shouldFit: bool):
        """
        Calculates the ideal size and center anchor point for the provided content size within the specified width and height.

        contentSize: A tuple containing the source content's size as (width, height).
        containerSize: A tuple containing the container's size as (width, height).
        shouldFit: A boolean indicating if the source image should fit within the content area or cover the content area. Fit is indicated by `True` and ensures the whole source image will be seen but some background color may be visible. Cover is indicated by `False` and ensures that the entirety of the content area will be covered but the source image will likely be cropped.

        Returns a tuple of a size tuple as (width, height) for the ideal content size and a position tuple as (x, y) indicating the correct top left anchor point for the content.
        """
        # Calculate resize ratio
        if shouldFit:
            # Fit inside the canvas
            resizeRatio = min(containerSize[0] / contentSize[0], containerSize[1] / contentSize[1])
        else:
            # Stretch across canvas
            resizeRatio = max(containerSize[0] / contentSize[0], containerSize[1] / contentSize[1])

        # Calculate the best size for the content
        finalW = round(contentSize[0] * resizeRatio)
        finalH = round(contentSize[1] * resizeRatio)

        # Calculate paste offset
        pasteOffsetX = 0
        pasteOffsetY = 0

        if finalW > containerSize[0]:
            # Need to adjust X
            pasteOffsetX = -(round((finalW - containerSize[0]) / 2))

        if finalH > containerSize[1]:
            # Need to adjust Y
            pasteOffsetY = -(round((finalH - containerSize[1]) / 2))

        return (
            (finalW, finalH),
            (pasteOffsetX, pasteOffsetY)
        )

    def drawTexture(tex, size: tuple, containerSize: tuple, shouldFit: bool, center: bool, offset: tuple, border: tuple, asButton: bool = False):
        """
        Draws the provided texture into an ImGui window as an ImGui Image.

        tex: A GL compatible texture.
        size: A tuple containing the dimensions of the texture as (width, height).
        containerSize: A tuple containing the container's size as (width, height).
        shouldFit: A boolean indicating if the source image should fit within the content area or cover the content area. Fit is indicated by `True` and ensures the whole source image will be seen but some background color may be visible. Cover is indicated by `False` and ensures that the entirety of the content area will be covered but the source image will likely be cropped.
        center: A boolean indicating if the rendered image should be centered in the provided `containerSize`.
        offset: A tuple containing points of offset for the image as (x, y).
        border: An RGBA tuple containing a border color as (r, g, b, a).
        asButton: If the texture should be drawn as a button. If the texture should be drawn as a button, will return `True` if the image is clicked. In all other cases, returns `False`.
        """
        # Calculate the image size
        modImgSize, imgAnchor = ImguiImage.calculateContentBestSize(size, containerSize, shouldFit)

        # Calculate texture offset
        texOffset = (
            tex.width / ImguiImage.nearestPowerOfTwo(tex.width),
            tex.height / ImguiImage.nearestPowerOfTwo(tex.height)
        )

        # Calculate position
        cursorX = 0
        cursorY = 0

        if center:
            cursorX += ((imgui.get_window_width() - modImgSize[0]) * 0.5)
            cursorY += imgui.get_cursor_pos()[1]

        if offset != (0, 0):
            cursorX += offset[0]
            cursorY += offset[1]

        if not ((cursorX == 0) and (cursorY == 0)):
            imgui.set_cursor_pos((cursorX, cursorY))

        # Check if button or image
        if not asButton:
            # Display image
            imgui.image(
                texture_id=tex.id,
                width=modImgSize[0],
                height=modImgSize[1],
                uv0=(0, 0),
                uv1=texOffset,
                border_color=border
            )
            return False
        else:
            # Display button
            return imgui.image_button(
                texture_id=tex.id,
                width=modImgSize[0],
                height=modImgSize[1],
                uv0=(0, 0),
                uv1=texOffset,
                border_color=border
            )
