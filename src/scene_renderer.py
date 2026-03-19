import numpy as np
import math
from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window


WINDOW_Y, WINDOW_X = 300, 600

def circle_triangle_fan(x, y, r, num_triangles=20):
    verts = []

    for i in range(num_triangles):
        # Angles for this slice
        theta1 = (i / num_triangles) * 2 * math.pi
        theta2 = ((i + 1) / num_triangles) * 2 * math.pi

        # Points on circle
        x1 = x + r * math.cos(theta1)
        y1 = y + r * math.sin(theta1)

        x2 = x + r * math.cos(theta2)
        y2 = y + r * math.sin(theta2)

        # Triangle: center → edge1 → edge2
        verts.extend([
            x,  y,   # center
            x1, y1,  # first edge point
            x2, y2   # second edge point
        ])

    return verts

# moon data
moon_vertices = np.array(circle_triangle_fan(336, 250, 36, num_triangles=30))
moon_color_data = np.array([1, 1, 1] * (moon_vertices.shape[0]//2))
moon_index_data = np.arange(moon_vertices.shape[0]//2)

# layer 1 data
layer1_mountains = np.array([
    0, 184, 63, 208, 0, 0, #peak1
    63, 208, 107, 178, 0, 0,
    107, 178, 165, 209, 0, 0, #peak2
    165, 209, 210, 180, 0, 0,
    210, 180, 300, 230, 0, 0, #peak3
    300, 230, 322, 230, 0, 0,
    322, 230, 370, 260, 0, 0, #peak4
    370, 260, 600, 180, 0, 0,
    0, 0, 600, 180, 600, 0
])
layer1_color_data = np.array([144/255, 194/255, 221/255] * (layer1_mountains.shape[0]//2))
layer1_index_data = np.arange(layer1_mountains.shape[0]//2)

# layer 2 data
layer2_mountains = np.array([
    0, 80, 160, 170, 600, 0, #peak1
    160, 170, 200, 155, 600, 0,
    200, 155, 230, 163, 600, 0, #peak2
    230, 163, 280, 167, 600, 0,
    280, 167, 305, 165, 600, 0,
    305, 165, 330, 153, 600, 0,
    330, 153, 387, 170, 600, 0, #peak3
    387, 170, 403, 158, 600, 0,
    403, 158, 434, 158, 600, 0,
    434, 158, 445, 167, 600, 0, #peak4
    445, 167, 463, 167, 600, 0,
    463, 167, 495, 198, 600, 0, #peak5
    495, 198, 531, 198, 600, 0,
    531, 198, 600, 224, 600, 0,
    # 0, 0, 600, 224, 600, 0 #fills in gap beneath peaks, but is unecessary since other layers cover it up
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
    501, 91, 600, 0, 0, 0,
])
layer3_color_data = np.array([51/255, 111/255, 154/255] * (layer3_mountains.shape[0]//2))
layer3_index_data = np.arange(layer3_mountains.shape[0]//2)

# layer 4 data
layer4_mountains = np.array([
    0, 68, 8, 76, 0, 0,
    8, 76, 25, 76, 0, 0,
    25, 76, 41, 66, 0, 0,
    41, 66, 74, 75, 0, 0,
    74, 75, 85, 73, 0, 0,
    85, 73, 101, 58, 0, 0,
    101, 58, 108, 57, 0, 0,
    0, 0, 108, 57, 300, 0, #stitching point
    108, 57, 126, 75, 300, 0,
    126, 75, 169, 103, 300, 0,
    169, 103, 187, 106, 300, 0,
    187, 106, 246, 78, 300, 0,
    246, 78, 255, 70, 300, 0,
    255, 70, 314, 77, 300, 0,
    314, 77, 330, 85, 300, 0,
    330, 85, 347, 101, 300, 0,
    347, 101, 365, 104, 300, 0,
    365, 104, 375, 100, 300, 0,
    375, 100, 388, 88, 300, 0,
    388, 88, 400, 87, 300, 0,
    400, 87, 412, 90, 300, 0,
    412, 90, 433, 75, 300, 0,
    433, 75, 446, 80, 300, 0,
    446, 80, 477, 84, 300, 0,
    300, 0, 477, 84, 600, 0, #stitching point
    477, 84, 485, 91, 600, 0,
    485, 91, 499, 94, 600, 0,
    499, 94, 503, 106, 600, 0,
    503, 106, 532, 111, 600, 0,
    532, 111, 543, 123, 600, 0,
    543, 123, 557, 127, 600, 0,
    557, 127, 573, 124, 600, 0,
    573, 124, 600, 126, 600, 0,
])
layer4_color_data = np.array([29/255, 69/255, 104/255] * (layer4_mountains.shape[0]//2))
layer4_index_data = np.arange(layer4_mountains.shape[0]//2)

# tree data
tree_vertices = np.array([
    16, 70, #tip
    14, 0, 18, 0, #trunk base
    16, 6, 16, 11, 16, 16, 16, 21, 16, 26, 16, 31, 16, 36, 16, 41, 16, 46, 16, 51, 16, 56, 16, 61, 16, 66, #foliage bases (idx 3-15)
    6, 9, 0, 16, 1, 21, 3, 26, 4, 31, 6, 36, 8, 41, 10, 47, 11, 54, 12, 58, 13, 64, #left side foliage tips (idx 16-26)
    26, 9, 32, 16, 31, 21, 29, 26, 28, 31, 26, 36, 24, 41, 22, 47, 21, 54, 20, 58, 19, 64, #right side foliage tips (idx 27-37)
])
tree_layer1_color_data = np.array([29/255, 58/255, 74/255] * (tree_vertices.shape[0]//2))
tree_layer2_color_data = np.array([17/255, 33/255, 44/255] * (tree_vertices.shape[0]//2))
tree_index_data = np.array([
    0, 1, 2, #trunk
    3, 5, 16, 4, 6, 17, 5, 7, 18, 6, 8, 19, 7, 9, 20, 8, 10, 21, 9, 11, 22, 10, 12, 23, 11, 13, 24, 13, 14, 25, 14, 15, 26, #left side foliage
    3, 5, 27, 4, 6, 28, 5, 7, 29, 6, 8, 30, 7, 9, 31, 8, 10, 32, 9, 11, 33, 10, 12, 34, 11, 13, 35, 13, 14, 36, 14, 15, 37, #right side foliage
])
tree_heights = np.array([1, 1, 0.9, 0.8, 0.7, 0.5, 0.8, 0.75, 0.55, 0.6, 0.65, 0.5, 0.4, 0.55, 0.7, 0.5, 0.8, 0.4, 0.6, 0.0, 1, 0.65, 0.0, 0.75, 0.4, 0.45, 0.0, 0.45, 0.35, 0.55, 0.3, 0.4, 0.0, 0.7, 0.3, 0.75, 0.0, 0.5, 0.6, 0.0, 0.65, 0.7, 0.75, 0.4, 0.35, 0.0, 0.3, 0.9, 0.0, 0.75, 0.0, 0.45, 0.5, 0.55, 0.65, 0.0, 0.4, 0.0, 0.5, 0.6, 0.45, 0.0, 0.8, 0.4, 0.6])


def landscape(window: RIT_Window, engine: CGI_Engine):
    # Setup
    window.clear_fb(207/255, 229/255, 238/255) #light blue background
    normT = engine.normalize(WINDOW_Y, 0, WINDOW_X, 0)
    engine.set_viewport(WINDOW_Y-1, 0, WINDOW_X-1, 0)
    base = engine.identity()
    centerTreeT = engine.translate(-16, 0) #center trees at origin for easier transformations

    # Draw the scene
    engine.draw_triangles(window, moon_vertices, moon_color_data, moon_index_data, base, normT)
    engine.draw_triangles(window, layer1_mountains, layer1_color_data, layer1_index_data, base, normT)
    engine.draw_triangles(window, layer2_mountains, layer2_color_data, layer2_index_data, base, normT)
    engine.draw_triangles(window, layer3_mountains, layer3_color_data, layer3_index_data, base, normT)
    engine.draw_triangles(window, layer4_mountains, layer4_color_data, layer4_index_data, base, normT)

    # Draw trees with varying heights
    for i in range(len(tree_heights)):
        scale = tree_heights[(i+len(tree_heights)//12)%len(tree_heights)] #rotate array to get different heights for trees in the back vs front layers
        if scale == 0:
            continue # skip invisible trees
        tree = base @ engine.translate(i * 598/len(tree_heights), -7 * (1 - scale)) @ engine.scale(1 - 0.75 * (1 - scale), scale) @ centerTreeT
        engine.draw_triangles(window, tree_vertices, tree_layer1_color_data, tree_index_data, tree, normT)
    
    for i, scale in enumerate(tree_heights):
        if scale == 0:
            continue # skip invisible trees
        tree = base @ engine.translate(i * 598/len(tree_heights), -7 * (1 - scale)) @ engine.scale(1 - 0.75 * (1 - scale), scale) @ centerTreeT
        engine.draw_triangles(window, tree_vertices, tree_layer2_color_data, tree_index_data, tree, normT)


def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_Y, WINDOW_X, "CSCI 610 - Project 1 - Landscape")
    win.run(landscape, engine)


if __name__ == "__main__":
    main()
