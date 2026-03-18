import numpy as np
from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window

# a 10 x 10 equilateral triangle
triangle_data = np.array([0.0, 0.0, 100.0, 0.0, 50.0, 100.0])
triangle_index_data = np.array([0, 2, 1])

# color data
layer1_color_data = np.array([144/255, 194/255, 221/255, 144/255, 194/255, 221/255, 144/255, 194/255, 221/255])


WINDOW_Y, WINDOW_X = 300, 600


def landscape(window: RIT_Window, engine: CGI_Engine):
    # Setup
    window.clear_fb(207/255, 229/255, 238/255) # light blue background
    engine.set_viewport(WINDOW_Y, 0, WINDOW_X, 0)

    # Helper matrices
    normT = engine.normalize(WINDOW_Y, 0, WINDOW_X, 0)
    centerPeakT = engine.translate(-50, 0)
    base = engine.identity()

    # Mountain layer 1
    layer1 = base @ engine.translate(0, 0)
    peak1 = layer1 @ engine.translate(50, 0) @ engine.scale(2, 0.6) @ centerPeakT
    engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak1, normT)
    peak2 = layer1 @ engine.translate(160, 0) @ engine.scale(2, 0.5) @ centerPeakT
    engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak2, normT)
    peak3 = layer1 @ engine.translate(310, 0) @ engine.scale(3, 0.7) @ centerPeakT
    engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak3, normT)
    peak4 = layer1 @ engine.translate(410, 0) @ engine.scale(4, 1) @ centerPeakT
    engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak4, normT)


def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_Y, WINDOW_X, "CSCI 610 - Project 1 - Landscape")
    win.run(landscape, engine)


if __name__ == "__main__":
    main()
