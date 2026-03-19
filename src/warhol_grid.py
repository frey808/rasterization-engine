from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window
from scene_renderer import landscape


WINDOW_Y, WINDOW_X = 300, 600
DIVISIONS = 2 # number of rows and columns in the grid

# Color schemes for each grid cell
color_schemes = [
    (1, 1, 1), # original colors
    (1, 0.5, 0.5), # red tint
    (0.5, 1, 0.5), # green tint
    (0.5, 0.5, 1) # blue tint
]


def warhol_grid(window: RIT_Window, engine: CGI_Engine):
    # render the same scene in a 2x2 grid with different color schemes
    for x in range(DIVISIONS):
        for y in range(DIVISIONS):
            custom_viewport = (
                (y + 1) * WINDOW_Y // DIVISIONS,
                y * WINDOW_Y // DIVISIONS - (1 if y > 0 else 0),
                (x + 1) * WINDOW_X // DIVISIONS,
                x * WINDOW_X // DIVISIONS - (1 if x > 0 else 0)
            )
            landscape(window, engine, custom_viewport=custom_viewport, custom_tint=color_schemes[y * DIVISIONS + x])

def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_Y, WINDOW_X, "CSCI 610 - Project 1 - Landscape")
    win.run(warhol_grid, engine)

if __name__ == "__main__":
    main()
