import pygame
from classes.entity import Entity
import src.constants as const


class Background(Entity):
    bg_image = pygame.image.load('imgs/bg.png')

    height = const.HEIGHT
    width = const.WIDTH

    def __init__(self):
        super().__init__(
                pos=(0, 0),
                image=pygame.transform.scale(self.bg_image,
                                             (self.width, self.height)),
                )
