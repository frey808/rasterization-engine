from engine.rit_window import RIT_Window
from engine.vertex import Vertex

from pyglm import glm
import math

EPSILON = 1e-6 # extremely small value to handle numerical precision issues

class CGI_Engine():
    VIEWPORT_T = glm.mat3(1)

    def rasterize_line(self, window, p0, p1, color0, color1=None):
        x0, y0 = p0
        x1, y1 = p1
        r0, g0, b0 = color0
        if color1 is not None:
            r1, g1, b1 = color1

        # reverse x and y for steep lines
        reversed = abs(y1 - y0) > abs(x1 - x0)
        if reversed:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # ensure line is plotted left to right
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            r0, r1 = r1, r0
            g0, g1 = g1, g0
            b0, b1 = b1, b0

        #set up variables
        dx = x1 - x0
        dy = abs(y1 - y0)
        y_step = 1 if y0 < y1 else -1
        err = dx // 2
        y = y0
        steps = dx

        for i, x in enumerate(range(x0, x1 + 1)):

            # color interpolation
            if color1 is not None:
                u = i / steps
                r = r0 + u * (r1 - r0)
                g = g0 + u * (g1 - g0)
                b = b0 + u * (b1 - b0)
            else:
                r, g, b = r0, g0, b0

            # plot pixel
            if reversed:
                window.set_pixel(y, x, r, g, b)
            else:
                window.set_pixel(x, y, r, g, b)

            # decision variable update
            err -= dy
            if err < 0:
                y += y_step
                err += dx

    def rasterize_interpolated_lines(self, window: RIT_Window, vertices: list[int], colors: list[float], n: int):
        #unpack vertices and colors, then rasterize them as lines
        for i in range(n):
            p0 = (vertices[4 * i], vertices[4 * i + 1])
            p1 = (vertices[4 * i + 2], vertices[4 * i + 3])
            color0 = (colors[6 * i], colors[6 * i + 1], colors[6 * i + 2])
            color1 = (colors[6 * i + 3], colors[6 * i + 4], colors[6 * i + 5])
            self.rasterize_line(window, p0, p1, color0, color1)

    def draw_lines(self, window: RIT_Window, vertices: list[int], colors: list[float], indices: list[int], modelT, normT):
        #unpack vertices and colors, then rasterize them as lines
        mapped_vertices = []
        for i in indices:
            vec = glm.vec3(vertices[2 * i], vertices[2 * i + 1], 1)
            vec = self.VIEWPORT_T * normT * modelT * vec
            V = Vertex(vec[0], vec[1], colors[3 * i], colors[3 * i + 1], colors[3 * i + 2])
            mapped_vertices.append(V)
        unpacked_vertices = []
        unpacked_colors = []
        for V in mapped_vertices:
            unpacked_vertices.extend([int(V.x), int(V.y)])
            unpacked_colors.extend([V.r, V.g, V.b])
        self.rasterize_interpolated_lines(window, unpacked_vertices, unpacked_colors, len(mapped_vertices)//2)

    def draw_triangles(self, window: RIT_Window, vertices: list[int], colors: list[float], indices: list[int], modelT, normT):
        # unpack vertices and colors, then rasterize them as triangles
        for idx, i in enumerate(indices):
            V = Vertex(vertices[2 * i], vertices[2 * i + 1], colors[3 * i], colors[3 * i + 1], colors[3 * i + 2])
            vec = glm.vec3(V.x, V.y, 1)
            vec = self.VIEWPORT_T * normT * modelT * vec
            V = Vertex(vec[0], vec[1], V.r, V.g, V.b)
            
            if idx % 3 == 0:
                V0 = V
            elif idx % 3 == 1:
                V1 = V
            else:
                V2 = V
                self.rasterize_triangle(window, V0, V1, V2)

    def rasterize_triangle(self, window: RIT_Window, V0: Vertex, V1: Vertex, V2: Vertex):
        # Rasterize a triangle defined by vertices V0, V1, V2 with color interpolation

        # get axis aligned bounding box
        min_x = int(min(V0.x, V1.x, V2.x))
        max_x = int(max(V0.x, V1.x, V2.x))
        min_y = int(min(V0.y, V1.y, V2.y))
        max_y = int(max(V0.y, V1.y, V2.y))

        # precompute denominator for barycentric coordinates and normalize vertex order to counter-clockwise
        denom = (V1.y - V2.y) * (V0.x - V2.x) + (V2.x - V1.x) * (V0.y - V2.y)
        if abs(denom) < EPSILON:
            return
        if denom < 0:
            V1, V2 = V2, V1
            denom = -denom
        inv_denom = 1 / denom #avoid potential division by zero


        # rasterize within bounding box
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                #calculate barycentric coordinates
                w0 = ((V1.y - V2.y) * (x - V2.x) + (V2.x - V1.x) * (y - V2.y)) * inv_denom
                w1 = ((V2.y - V0.y) * (x - V2.x) + (V0.x - V2.x) * (y - V2.y)) * inv_denom
                w2 = 1 - w0 - w1

                #check if pixel is inside triangle
                if w0 < -EPSILON or w1 < -EPSILON or w2 < -EPSILON:
                    continue

                # top-left rule
                if abs(w0) < EPSILON:
                    if not ((V1.y > V0.y) or (abs(V1.y - V0.y) < EPSILON and V1.x > V0.x)):
                        continue
                if abs(w1) < EPSILON:
                    if not ((V2.y > V1.y) or (abs(V2.y - V1.y) < EPSILON and V2.x > V1.x)):
                        continue
                if abs(w2) < EPSILON:
                    if not ((V0.y > V2.y) or (abs(V0.y - V2.y) < EPSILON and V0.x > V2.x)):
                        continue
                
                r = w0 * V0.r + w1 * V1.r + w2 * V2.r
                g = w0 * V0.g + w1 * V1.g + w2 * V2.g
                b = w0 * V0.b + w1 * V1.b + w2 * V2.b
                window.set_pixel(x, y, r, g, b)
    
    def identity(self):
        return glm.mat3(1)

    def translate(self, tx: float, ty: float):
        return glm.mat3((1, 0, 0),
                        (0, 1, 0),
                        (tx, ty, 1))

    def scale(self, sx: float, sy: float):
        return glm.mat3((sx, 0, 0),
                        (0, sy, 0),
                        (0, 0, 1))
    
    def rotate(self, angle: float):
        rad = math.radians(angle)
        return glm.mat3((math.cos(rad), math.sin(rad), 0),
                        (-math.sin(rad), math.cos(rad), 0),
                        (0, 0, 1))
    
    def normalize(self, top: float, bottom: float, right: float, left: float):
        return glm.mat3((2/(right-left), 0, 0),
                        (0, 2/(top-bottom), 0),
                        (-2*left/(right-left)-1, -2*bottom/(top-bottom)-1, 1))
    
    def set_viewport(self, top: int, bottom: int, right: int, left: int):
        self.VIEWPORT_T = glm.mat3(((right-left)/2, 0, 0),
                        (0, (top-bottom)/2, 0),
                        ((right+left)/2, (top+bottom)/2, 1))
