import pygame
from classes.entity import Entity
import src.constants as const


class Ground(Entity):
    ground_image = pygame.image.load('imgs/ground.png')
    img_width = ground_image.get_size()[0]
    number_of_tiles = 0
    while number_of_tiles*img_width < const.WIDTH * 2:
        number_of_tiles += 1

    def __init__(self, off_screen=False):
        super().__init__(
                pos=(0 if not off_screen else const.WIDTH,
                     const.HEIGHT - const.GROUND_HEIGHT),
                image=pygame.Surface((self.number_of_tiles*self.img_width,
                                     const.GROUND_HEIGHT))
                )
        for i in range(self.number_of_tiles):
            self.image.blit(self.ground_image,
                            self.ground_image.get_rect(left=self.img_width*i))
