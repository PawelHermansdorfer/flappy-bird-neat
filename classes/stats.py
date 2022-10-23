import pygame
from .entity import Entity
import src.constants as const
from src.colors import BLACK, TRANSPARENT, TRANSPARENT_GREY


class Stats(Entity):
    display_center = (const.WIDTH_CENTER, const.HEIGHT * 0.8)
    display_size = (const.WIDTH//1.2, const.HEIGHT//4)

    def __init__(self):
        super().__init__(
            pos=(self.display_center[0]-self.display_size[0]//2,
                 self.display_center[1]-self.display_size[1]//2),
            image=pygame.Surface(self.display_size),
            bg_color=TRANSPARENT
        )
        self.hidden = True

    def toggle(self):
        if self.hidden:
            pygame.draw.rect(
                self.image,
                TRANSPARENT_GREY,
                self.image.get_rect(),
            )
            pygame.draw.rect(
                self.image,
                BLACK,
                self.image.get_rect(),
                2
            )
        else:
            self.image.fill(TRANSPARENT)

        self.hidden = not self.hidden
