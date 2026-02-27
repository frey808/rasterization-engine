from typing import Callable, Any

import pygame


class RIT_Window:
    """
    This class represents the main display window and rendering surface for the RIT Rasterizer Engine.
    """
    __slots = '_width', '_height', '_started', '_screen'
    _width: int
    _height: int
    _title: str
    _started: bool  # flag indicating if the window has been initialized correctly and must remain opened.
    _screen: pygame.Surface  # the underline pygame.Surface object used for drawing

    def __init__(self, height: int, width: int, title: str = "CSCI 610"):
        """
        Constructs a new window.

        The window uses a Cartesian coordinate system where the default position for (0,0)
        is the bottom-left corner.

        :param height: The height of the window in pixels.
        :param width: The width of the window in pixels.
        :param title: The title to display in the window's title bar.
        """
        self._width = width
        self._height = height
        self._title = title
        self._started = False
        self._screen = None

    def run(self, action: Callable, *args: Any, **kwargs: Any) -> None:
        """
        Initializes and displays the window, then executes the given action.
        :param action: A callable function that contains the logic to draw the scene displayed in the window.
        :param args: Optional positional arguments to be passed to the action function.
        :param kwargs: Optional keyword arguments to be passed to the action function.
        :return: None
        """
        if not self._started:
            pygame.init()

            # Set up the display
            self._screen = pygame.display.set_mode((self._width, self._height))
            pygame.display.set_caption(self._title)

            # do what needs to be done
            action(self, *args, **kwargs)

            # Main game loop
            self._started = True
            while self._started:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._started = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Example: quit on escape key
                            self._started = False

                # Update the display to show the result of action
                pygame.display.flip()

            pygame.quit()

    def clear_fb(self, r: float, g: float, b: float) -> None:
        """
        Clear the entire framebuffer (display surface) to a single solid color.

        This method sets every pixel in the framebuffer to the color defined
        by the given RGB components, effectively resetting the drawing canvas.

        :param r: The red component of the clear color (typically a float value between 0.0 and 1.0)
        :param g: The green components of the clear color (typically a float value between 0.0 and 1.0)
        :param b: The blue component of the clear color (typically a float value between 0.0 and 1.0)
        :return: None
        """
        for x in range(self._width):
            for y in range(self._height):
                self.set_pixel(x, y, r, g, b)

    def set_pixel(self, x: int, y: int, r: float, g: float, b: float) -> None:
        """
        Color the pixel at (x,y) position with the given RGB components.
        :param x: The pixel's x coordinate
        :param y: The pixel's y coordinate
        :param r: The red component (typically a float value between 0.0 and 1.0)
        :param g: The blue component (typically a float value between 0.0 and 1.0)
        :param b: The blue component (typically a float value between 0.0 and 1.0)
        :return: None
        """
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            print("set_pixel error:  pixel [", x, ",", y, "] is out of range")
        else:
            # sets the pixel at (x,y) to (r, g, b, 255), with 8-bit integer colors
            rr = int(r * 255)
            gg = int(g * 255)
            bb = int(b * 255)

            c = (rr, gg, bb)

            self._screen.set_at((x, self._height - 1 - y), c)

    def draw_outline(self, top: float, bottom: float, right: float, left: float, r: float, g: float, b: float) -> None:
        """
        Draws a hollow rectangular boundary (wireframe) on the display.

        :param top: The clip window's top y coordinate
        :param bottom: The clip window's bottom y coordinate
        :param right: The clip window's right x coordinate
        :param left: The clip window's left x coordinate
        :param r: The red component (typically a float value between 0.0 and 1.0)
        :param g: The blue component (typically a float value between 0.0 and 1.0)
        :param b: The blue component (typically a float value between 0.0 and 1.0)
        :return: None
        """
        # top and bottom edges
        x = left
        while x <= right:
            self.set_pixel(int(round(x)), int(round(top)), r, g, b)
            self.set_pixel(int(round(x)), int(round(bottom)), r, g, b)
            x += 1.0

        # left and right edges
        y = bottom
        while y <= top:
            self.set_pixel(int(round(left)), int(round(y)), r, g, b)
            self.set_pixel(int(round(right)), int(round(y)), r, g, b)
            y += 1.0
