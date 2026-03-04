from dataclasses import dataclass

@dataclass
class Vertex:
    x: int
    y: int
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0

    def coordinates(self):
        return [self.x, self.y]

    def color(self):
        return [self.r, self.g, self.b]