import pygame
import random
from classes.entity import Entity
import src.constants as const
from src.colors import TRANSPARENT, GREEN_4


class Pipe(Entity):
    gap_size = 180
    gap_margin = const.HEIGHT // 4
    width = 80
    color = GREEN_4
    vel_x = -const.GAME_SPEED
    pipe_img = pygame.image.load('imgs/pipe.png')
    pipe_img = pygame.transform.scale(pipe_img,
                                      (width, pipe_img.get_size()[1]))

    def __init__(self):
        super().__init__(
            pos=(const.WIDTH, 0),
            image=pygame.Surface((self.width,
                                  const.HEIGHT-const.GROUND_HEIGHT)),
            bg_color=TRANSPARENT,
        )
        self.gap_start = random.randint(
                self.gap_margin,
                const.HEIGHT
                - const.GROUND_HEIGHT
                - self.gap_margin
                - self.gap_size
                )

        self.gap_end = self.gap_start + self.gap_size

        self.upper_pipe = pygame.transform.flip(self.pipe_img,
                                                flip_x=False,
                                                flip_y=False
                                                )
        self.lower_pipe = pygame.transform.flip(self.pipe_img,
                                                flip_x=False,
                                                flip_y=True,
                                                )
        self.image.blit(self.lower_pipe,
                        (0, self.gap_start-self.lower_pipe.get_size()[1]))
        self.image.blit(self.upper_pipe, (0, self.gap_end))

    def update(self):
        super().update()
        self.pos_x += self.vel_x

    def start(self):
        self.started = True
