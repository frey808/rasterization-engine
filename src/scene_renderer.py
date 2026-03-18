import numpy as np
from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window


WINDOW_Y, WINDOW_X = 300, 600

# layer 1 data
layer1_mountains = np.array([
    0, 184, 63, 208, 0, 0, #peak1
    63, 208, 107, 178, 0, 0,
    107, 178, 165, 209, 0, 0, #peak2
    165, 209, 210, 180, 0, 0,
    210, 180, 300, 230, 0, 0, #peak3
    300, 230, 322, 230, 0, 0,
    322, 230, 370, 260, 0, 0, #peak4
    370, 260, 599, 180, 0, 0,
    0, 0, 599, 180, 599, 0
])
layer1_color_data = np.array([144/255, 194/255, 221/255] * (layer1_mountains.shape[0]//2))
layer1_index_data = np.arange(layer1_mountains.shape[0]//2)

# layer 2 data
layer2_mountains = np.array([
    0, 80, 160, 170, 0, 0, #peak1
    160, 170, 200, 155, 0, 0,
    200, 155, 230, 163, 0, 0, #peak2
    230, 163, 280, 167, 0, 0,
    280, 167, 305, 165, 0, 0,
    305, 165, 330, 153, 0, 0,
    330, 153, 387, 170, 0, 0, #peak3
    387, 170, 403, 158, 0, 0,
    403, 158, 434, 158, 0, 0,
    434, 158, 445, 167, 0, 0, #peak4
    445, 167, 463, 167, 0, 0,
    463, 167, 495, 198, 0, 0, #peak5
    495, 198, 531, 198, 0, 0,
    531, 198, 599, 224, 0, 0,
    0, 0, 599, 224, 599, 0
])
layer2_color_data = np.array([116/255, 167/255, 215/255] * (layer2_mountains.shape[0]//2))
layer2_index_data = np.arange(layer2_mountains.shape[0]//2)

# layer 3 data
layer3_mountains = np.array([
    0, 228, 32, 194, 0, 0,
    32, 194, 66, 190, 0, 0,
    66, 190, 76, 180, 0, 0,
    76, 180, 94, 176, 0, 0,
    94, 176, 108, 169, 0, 0,
    108, 169, 137, 171, 0, 0,
    137, 171, 152, 161, 0, 0,
    152, 161, 162, 161, 0, 0,
    162, 161, 177, 146, 0, 0,
    177, 146, 202, 147, 0, 0,
    202, 147, 222, 139, 0, 0,
    222, 139, 249, 149, 0, 0,
    249, 149, 278, 149, 0, 0,
    278, 149, 281, 147, 0, 0,
    281, 147, 298, 147, 0, 0,
    298, 147, 344, 127, 0, 0,
    344, 127, 364, 129, 0, 0,
    364, 129, 386, 120, 0, 0,
    386, 120, 412, 119, 0, 0,
    412, 119, 433, 107, 0, 0,
    433, 107, 456, 107, 0, 0,
    456, 107, 475, 93, 0, 0,
    475, 93, 501, 91, 0, 0,
    501, 91, 599, 0, 0, 0,
])
layer3_color_data = np.array([51/255, 111/255, 154/255] * (layer3_mountains.shape[0]//2))
layer3_index_data = np.arange(layer3_mountains.shape[0]//2)


def landscape(window: RIT_Window, engine: CGI_Engine):
    # Setup
    window.clear_fb(207/255, 229/255, 238/255) # light blue background
    engine.set_viewport(WINDOW_Y, 0, WINDOW_X, 0)

    # Helper matrices
    normT = engine.normalize(WINDOW_Y, 0, WINDOW_X, 0)
    base = engine.identity()

    engine.draw_triangles(window, layer1_mountains, layer1_color_data, layer1_index_data, base, normT)
    engine.draw_triangles(window, layer2_mountains, layer2_color_data, layer2_index_data, base, normT)
    engine.draw_triangles(window, layer3_mountains, layer3_color_data, layer3_index_data, base, normT)
    

def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_Y, WINDOW_X, "CSCI 610 - Project 1 - Landscape")
    win.run(landscape, engine)


if __name__ == "__main__":
    main()
