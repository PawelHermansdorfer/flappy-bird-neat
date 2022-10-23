import pygame
from .entity import Entity
import src.constants as const
from src.colors import TRANSPARENT_GREY, DARK_GREY


class Stats(Entity):
    display_center = const.CENTER
    display_size = (const.WIDTH//4, const.HEIGHT//4)

    def __init__(self):
        super().__init__(
                pos=(self.display_center[0]-self.display_size[0]//2,
                     self.display_center[1]-self.display_size[1]//2),
                image=pygame.Surface(self.display_size),
                bg_color=TRANSPARENT_GREY
                )
        pygame.draw.rect(
            self.image,
            DARK_GREY,
            self.image.get_rect(),
            2
            )

        def update(self):
            super().update()
