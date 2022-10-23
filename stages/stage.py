from src.constants import LAYERS, BACKGROUND_COLOR
from pygame.sprite import Group


# Stage scheme
class Stage:
    def __init__(self):
        self.layers = {layer: Group() for layer in LAYERS}
        self.done = False
        self.next = None
        self.background_color = BACKGROUND_COLOR

    def update(self):  # Function in which each element of stage is updated
        for group in self.layers.values():
            group.update()

    # Function in which each element of stage is rendered
    def render(self, display):
        display.fill(self.background_color)
        for group in self.layers.values():
            group.draw(display)

    def mouse_pressed(self, left_click, scroll_click, right_click, mouse_pos):
        for group in self.layers.values():
            for element in group:
                element.mouse_click(
                    left_click, scroll_click, right_click, mouse_pos)

    def mouse_release(self, mouse_pos):
        for group in self.layers.values():
            for element in group:
                element.mouse_release(mouse_pos=mouse_pos)

    def keyboard_input(self, key):
        for group in self.layers.values():
            for element in group:
                element.keyboard_pressed(key=key)

    def add_to_layer(self, layer_name, *args):
        for arg in args:
            self.layers[layer_name].add(arg)

    def end_stage(self):
        self.done = True
