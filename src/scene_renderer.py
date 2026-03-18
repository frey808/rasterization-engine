import numpy as np
from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window


WINDOW_Y, WINDOW_X = 300, 600

# a 10 x 10 equilateral triangle
# triangle_data = np.array([0.0, 0.0, 100.0, 0.0, 50.0, 100.0])
# triangle_index_data = np.array([0, 2, 1])

# # color data
# layer1_color_data = np.array([144/255, 194/255, 221/255, 144/255, 194/255, 221/255, 144/255, 194/255, 221/255])
# layer2_color_data = np.array([116/255, 167/255, 215/255, 116/255, 167/255, 215/255, 116/255, 167/255, 215/255])

# layer 1 data
layer1_mountains = np.array([
    0, 184, 63, 208, 107, 178, #peak1
    0, 0, 0, 184, 107, 178,
    107, 178, 165, 209, 210, 180, #peak2
    0, 0, 107, 178, 210, 180,
    210, 180, 300, 230, 322, 230, #peak3
    0, 0, 210, 180, 322, 230,
    322, 230, 370, 260, 599, 180, #peak4
    0, 0, 322, 230, 599, 180,
    0, 0, 599, 180, 599, 0
])
layer1_color_data = np.array([144/255, 194/255, 221/255] * (layer1_mountains.shape[0]//2))
layer1_index_data = np.arange(layer1_mountains.shape[0]//2)


def landscape(window: RIT_Window, engine: CGI_Engine):
    # Setup
    window.clear_fb(207/255, 229/255, 238/255) # light blue background
    engine.set_viewport(WINDOW_Y, 0, WINDOW_X, 0)

    # Helper matrices
    normT = engine.normalize(WINDOW_Y, 0, WINDOW_X, 0)
    centerPeakT = engine.translate(-50, -100)
    base = engine.identity()

    engine.draw_triangles(window, layer1_mountains, layer1_color_data, layer1_index_data, base, normT)

    # Mountain layer 1
    # layer1 = base @ engine.translate(0, 130)
    # peak11 = layer1 @ engine.translate(50, 80) @ engine.scale(2.5, 0.8) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak11, normT)
    # peak12 = layer1 @ engine.translate(160, 70) @ engine.scale(2.5, 0.7) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak12, normT)
    # peak13 = layer1 @ engine.translate(320, 90) @ engine.rotate(20) @ engine.scale(2.0, 0.25) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak13, normT)
    # peak14 = layer1 @ engine.translate(410, 120) @ engine.scale(4.5, 1.2) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer1_color_data, triangle_index_data, peak14, normT)

    # Mountain layer 2
    # layer2 = base @ engine.translate(0, 110)
    # peak21 = layer2 @ engine.translate(150, 0) @ engine.scale(2, 0.5) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer2_color_data, triangle_index_data, peak21, normT)
    # peak22 = layer2 @ engine.translate(250, 0) @ engine.scale(5, 0.5) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer2_color_data, triangle_index_data, peak22, normT)
    # peak23 = layer2 @ engine.translate(410, 0) @ engine.scale(2, 0.5) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer2_color_data, triangle_index_data, peak23, normT)
    # peak24 = layer2 @ engine.translate(460, 0) @ engine.scale(2, 0.5) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer2_color_data, triangle_index_data, peak24, normT)
    # peak25 = layer2 @ engine.translate(510, 0) @ engine.scale(3, 0.8) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer2_color_data, triangle_index_data, peak25, normT)
    # peak26 = layer2 @ engine.translate(560, 0) @ engine.scale(4.5, 1.0) @ centerPeakT
    # engine.draw_triangles(window, triangle_data, layer2_color_data, triangle_index_data, peak26, normT)


def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_Y, WINDOW_X, "CSCI 610 - Project 1 - Landscape")
    win.run(landscape, engine)


if __name__ == "__main__":
    main()
