from engine.rit_window import RIT_Window
from engine.vertex import Vertex

from pyglm import glm
import math

EPSILON = 0 # extremely small value to handle numerical precision issues

class CGI_Engine():
    VIEWPORT_T = glm.mat3(1)

    def rasterize_line(self, window, p0, p1, color0, color1=None):
        x0, y0 = p0
        x1, y1 = p1
        r0, g0, b0 = color0
        r1, g1, b1 = color1 if color1 is not None else color0

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
            u = i / steps
            r = r0 + u * (r1 - r0)
            g = g0 + u * (g1 - g0)
            b = b0 + u * (b1 - b0)

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

    def draw_lines(self, window: RIT_Window, vertices: list[int], colors: list[float], indices: list[int], modelT, normT):
        # Unpack vertices and colors
        mapped_vertices = []
        for i in indices:
            vec = glm.vec3(vertices[2 * i], vertices[2 * i + 1], 1)
            vec = normT * modelT * vec
            V = Vertex(int(vec[0]), int(vec[1]), colors[3 * i], colors[3 * i + 1], colors[3 * i + 2])
            mapped_vertices.append(V)
        
        # Separate into line segments
        for i in range(0, len(mapped_vertices), 2):
            line = self.clip_line(mapped_vertices[i], mapped_vertices[i + 1], 1, -1, 1, -1)
            if line is None:
                continue
            vec0 = self.VIEWPORT_T * glm.vec3(line[0].x, line[0].y, 1)
            vec1 = self.VIEWPORT_T * glm.vec3(line[1].x, line[1].y, 1)
            V0 = Vertex(int(vec0[0]), int(vec0[1]), line[0].r, line[0].g, line[0].b)
            V1 = Vertex(int(vec1[0]), int(vec1[1]), line[1].r, line[1].g, line[1].b)

            self.rasterize_line(window, (V0.x, V0.y), (V1.x, V1.y), (V0.r, V0.g, V0.b), (V1.r, V1.g, V1.b))

    def draw_triangles(self, window: RIT_Window, vertices: list[int], colors: list[float], indices: list[int], modelT, normT):
        # unpack vertices and colors, then rasterize them as triangles
        for idx, i in enumerate(indices):
            vec = glm.vec3(vertices[2 * i], vertices[2 * i + 1], 1)
            vec = normT * modelT * vec
            V = Vertex(vec[0], vec[1], colors[3 * i], colors[3 * i + 1], colors[3 * i + 2])
            
            if idx % 3 == 0:
                V0 = V
            elif idx % 3 == 1:
                V1 = V
            else:
                V2 = V

                # Clip triangle and rasterize
                clipped_vertices = self.clip_poly([V0, V1, V2], 1, -1, 1, -1)
                for i, V in enumerate(clipped_vertices):
                    vec = self.VIEWPORT_T * glm.vec3(V.x, V.y, 1)

                    clipped_vertices[i] = Vertex(vec[0], vec[1], V.r, V.g, V.b)
                for i in range(0, len(clipped_vertices), 3):
                    self.rasterize_triangle(window, clipped_vertices[i], clipped_vertices[i + 1], clipped_vertices[i + 2])

    def rasterize_triangle(self, window: RIT_Window, V0: Vertex, V1: Vertex, V2: Vertex):
        # Rasterize a triangle defined by vertices V0, V1, V2 with color interpolation

        # get axis aligned bounding box
        min_x = math.floor(min(V0.x, V1.x, V2.x))
        max_x = math.ceil(max(V0.x, V1.x, V2.x))
        min_y = math.floor(min(V0.y, V1.y, V2.y))
        max_y = math.ceil(max(V0.y, V1.y, V2.y))

        # precompute denominator for barycentric coordinates and normalize vertex order to counter-clockwise
        denom = (V1.y - V2.y) * (V0.x - V2.x) + (V2.x - V1.x) * (V0.y - V2.y)
        if denom < 0:
            V1, V2 = V2, V1
            denom = -denom
        if abs(denom) <= EPSILON:
            return
        inv_denom = 1 / denom #avoid potential division by zero


        # rasterize within bounding box
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                # calculate barycentric coordinates
                w0 = ((V1.y - V2.y) * (x - V2.x) + (V2.x - V1.x) * (y - V2.y)) * inv_denom
                w1 = ((V2.y - V0.y) * (x - V2.x) + (V0.x - V2.x) * (y - V2.y)) * inv_denom
                w2 = 1 - w0 - w1

                # check if pixel is inside triangle
                if w0 < 0 or w1 < 0 or w2 < 0:
                    continue

                # top-left rule
                if abs(w0) < EPSILON: # w0 == 0 → edge V1–V2
                    if not ((V2.y > V1.y) or (abs(V2.y - V1.y) < EPSILON and V2.x > V1.x)):
                        continue

                if abs(w1) < EPSILON: # w1 == 0 → edge V2–V0
                    if not ((V0.y > V2.y) or (abs(V0.y - V2.y) < EPSILON and V0.x > V2.x)):
                        continue

                if abs(w2) < EPSILON: # w2 == 0 → edge V0–V1
                    if not ((V1.y > V0.y) or (abs(V1.y - V0.y) < EPSILON and V1.x > V0.x)):
                        continue
                
                r = w0 * V0.r + w1 * V1.r + w2 * V2.r
                g = w0 * V0.g + w1 * V1.g + w2 * V2.g
                b = w0 * V0.b + w1 * V1.b + w2 * V2.b
                window.set_pixel(x, y, r, g, b)

    # Cohen-Sutherland line clipping algorithm
    def clip_line(self, p0: Vertex, p1: Vertex, top: float, bottom: float, right: float, left: float):
        code0 = self.compute_outcode(p0, top, bottom, right, left)
        code1 = self.compute_outcode(p1, top, bottom, right, left)
        while True:
            # Trivial accept or reject cases
            if (code0 | code1) == 0:
                return p0, p1
            if (code0 & code1) != 0:
                return None
            
            # Find an endpoint that is outside the viewport
            if code0 != 0:
                code_out = code0
                p_out = p0
            else:
                code_out = code1
                p_out = p1
            
            # Find intersection point with viewport boundary
            if code_out & 8:
                x = p_out.x + (p1.x - p0.x) * (top - p_out.y) / (p1.y - p0.y)
                y = top
            elif code_out & 4:
                x = p_out.x + (p1.x - p0.x) * (bottom - p_out.y) / (p1.y - p0.y)
                y = bottom
            elif code_out & 2:
                y = p_out.y + (p1.y - p0.y) * (right - p_out.x) / (p1.x - p0.x)
                x = right
            else:
                y = p_out.y + (p1.y - p0.y) * (left - p_out.x) / (p1.x - p0.x)
                x = left
            
            # Replace outside point with intersection point and update outcode
            if code_out == code0:
                p0 = Vertex(x, y, p_out.r, p_out.g, p_out.b)
                code0 = self.compute_outcode(p0, top, bottom, right, left)
            else:
                p1 = Vertex(x, y, p_out.r, p_out.g, p_out.b)
                code1 = self.compute_outcode(p1, top, bottom, right, left)

    # Helper function to compute outcode for Cohen-Sutherland line clipping
    def compute_outcode(self, p: Vertex, top: float, bottom: float, right: float, left: float):
        code = 0
        if p.y > top:
            code |= 8
        if p.y < bottom:
            code |= 4
        if p.x > right:
            code |= 2
        if p.x < left:
            code |= 1
        return code

    # Sutherland-Hodgman polygon clipping algorithm
    def clip_poly(self, vertices: list[Vertex], top: float, bottom: float, right: float, left: float):
        edges = [(top, 'top'), (bottom, 'bottom'), (right, 'right'), (left, 'left')]
        for edge in edges:
            new_vertices = []
            for i in range(len(vertices)):
                prev = vertices[i - 1]
                V = vertices[i]
                new_vertices.extend(self.evaluate_edge(prev, V, edge))
            vertices = new_vertices
        if len(vertices) > 3:
            vertices = self.triangulate_polygon(vertices)
        return vertices
    
    # Helper function to evaluate a line segment against a single edge and clip it if necessary
    def evaluate_edge(self, prev: Vertex, V: Vertex, edge):
        if edge[1] == 'top':
            inside0 = prev.y <= edge[0]
            inside1 = V.y <= edge[0]
        elif edge[1] == 'bottom':
            inside0 = prev.y >= edge[0]
            inside1 = V.y >= edge[0]
        elif edge[1] == 'right':
            inside0 = prev.x <= edge[0]
            inside1 = V.x <= edge[0]
        else: # left
            inside0 = prev.x >= edge[0]
            inside1 = V.x >= edge[0]
        if inside0 and inside1:
            return [V]
        if inside0 and not inside1:
            return [self.find_intersection(prev, V, edge)]
        if not inside0 and inside1:
            return [self.find_intersection(prev, V, edge), V]
        return []
    
    # Helper function to interpolate the vertex at the intersection of a line segment and a clipping edge
    def find_intersection(self, prev: Vertex, V: Vertex, edge):
        if edge[1] == 'top' or edge[1] == 'bottom':
            x = prev.x + (V.x - prev.x) * (edge[0] - prev.y) / (V.y - prev.y)
            y = edge[0]
            r = prev.r + (V.r - prev.r) * ((y - prev.y) / (V.y - prev.y))
            g = prev.g + (V.g - prev.g) * ((y - prev.y) / (V.y - prev.y))
            b = prev.b + (V.b - prev.b) * ((y - prev.y) / (V.y - prev.y))
        else:
            y = prev.y + (V.y - prev.y) * (edge[0] - prev.x) / (V.x - prev.x)
            x = edge[0]
            r = prev.r + (V.r - prev.r) * ((x - prev.x) / (V.x - prev.x))
            g = prev.g + (V.g - prev.g) * ((x - prev.x) / (V.x - prev.x))
            b = prev.b + (V.b - prev.b) * ((x - prev.x) / (V.x - prev.x))
        return Vertex(x, y, r, g, b)
    
    # Helper function for triangulation of convex polygons
    def triangulate_polygon(self, vertices: list[Vertex]):
        triangles = []
        for i in range(1, len(vertices) - 1):
            triangles.extend([vertices[0], vertices[i], vertices[i + 1]])
        return triangles

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
        self.VIEWPORT_T = glm.mat3(
            ((right-left-1)/2, 0, 0),
            (0, (top-bottom-1)/2, 0),
            ((right+left)/2, (top+bottom)/2, 1)
        )
