from engine.cgi_engine import CGI_Engine
from engine.rit_window import RIT_Window
from scene_renderer import landscape


WINDOW_Y, WINDOW_X = 300, 600


def zooming_view(window: RIT_Window, engine: CGI_Engine):
    # render the same scene zoomed in on the center
    custom_viewport = (
        WINDOW_Y // 2, 0,
        WINDOW_X, WINDOW_X // 2
    )
    zoomT = engine.scale(2, 2) @ engine.translate(-WINDOW_X // 3, -WINDOW_Y // 2)
    landscape(window, engine, custom_viewport=custom_viewport, custom_transform=zoomT)

def main():
    engine = CGI_Engine()
    win = RIT_Window(WINDOW_Y, WINDOW_X, "CSCI 610 - Project 1 - Landscape")
    win.run(zooming_view, engine)

if __name__ == "__main__":
    main()
