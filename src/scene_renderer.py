import numpy as np
from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window

# a 10 x 10 square
square_data = np.array([0.0, 0.0, 10.0, 0.0, 10.0, 10.0, 0.0, 10.0])
square_index_data = np.array([0, 3, 2, 0, 2, 1])

# a 10 x 10 equilateral triangle
triangle_data = np.array([0.0, 0.0, 10.0, 0.0, 5.0, 10.0])
triangle_index_data = np.array([0, 2, 1])

# color data
sky_color2 = np.array([188/225, 233/255, 232/255, 188/225, 233/255, 232/255, 188/225, 233/255, 232/255, 188/225, 233/255, 232/255])


WINDOW_SIZE = 501


def landscape(window: RIT_Window, engine: CGI_Engine):
    # Setup
    window.clear_fb(168/225, 227/255, 225/255) #light blue background
    engine.set_viewport(WINDOW_SIZE, 0, WINDOW_SIZE, 0)

    # Helper matrices
    normT = engine.normalize(WINDOW_SIZE,0, WINDOW_SIZE, 0)
    centerT = engine.translate(-5, -5)

    base = engine.identity()

    sky2 = engine.scale(50, 42)
    engine.draw_triangles(window, square_data, sky_color2, square_index_data, sky2, normT)


def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_SIZE, WINDOW_SIZE, "CSCI 610 - Project 1 - Landscape")
    win.run(landscape, engine)


if __name__ == "__main__":
    main()
