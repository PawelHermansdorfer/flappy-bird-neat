import pygame
import time
from classes.entity import Entity
import src.constants as const
from src.colors import TRANSPARENT


class Bird(Entity):
    bird_imgs = [pygame.image.load(f'imgs/bird{i}.png') for i in range(1, 4)]
    width, height = 40, 30
    img_size = (width*2, height*2)

    gravity_force = 1
    max_angle = 45
    max_speed = 15
    jump_force = 15

    def __init__(self):
        self.bird_imgs = [pygame.transform.scale(img,
                                                 (self.width, self.height))
                          for img in self.bird_imgs]
        self.current_bird_img = self.bird_imgs[0]
        self.start_time = time.time()
        self.animation_speed = 2
        super().__init__(
            pos=(const.WIDTH // 2 - self.width, const.HEIGHT_CENTER),
            image=pygame.Surface(self.img_size),
        )
        self.vel_y = 0
        self.acc_y = 0
        self.dead = False
        self.angle = 0

    def pipe_colide(self, pipe):
        bird_mask = pygame.mask.from_surface(self.image)
        pipe_mask = pygame.mask.from_surface(pipe.image)
        offset = (pipe.pos_x - self.pos_x, pipe.pos_y - self.pos_y)

        if bird_mask.overlap(pipe_mask, offset):
            self.die()

    def update(self):
        self.apply_gravity()
        # Add acceleration to velocity
        self.vel_y += self.acc_y

        # Add velocity to pos
        self.pos_y += self.vel_y
        if self.dead:
            self.pos_x -= const.GAME_SPEED
        else:
            self.animate()

        # Limit velocity
        if self.vel_y > self.max_speed:
            self.vel_y = self.max_speed
        elif self.vel_y < -self.max_speed:
            self.vel_y = -self.max_speed

        # Set acceleration to 0
        self.acc_y = 0

        # Collide bootom of window
        ground_pos = const.HEIGHT - const.GROUND_HEIGHT
        if self.pos_y + (self.rect.height//2) > ground_pos:
            self.pos_y = ground_pos - (self.rect.height // 2)
            self.die()

        if self.vel_y < 0:
            self.angle = -max(self.vel_y * 4, -self.max_angle)
        elif self.vel_y > 0:
            self.angle = -min(self.vel_y * 4, self.max_angle)

        # Blit rotated bird image to bird surface
        rotated_img = pygame.transform.rotate(self.current_bird_img,
                                              self.angle)
        new_rect = rotated_img.get_rect(center=self.image.get_rect().center)
        self.image.fill(TRANSPARENT)
        self.image.blit(rotated_img, new_rect)

        super().update()

    # Animate bird by using keyframs from list
    def animate(self):
        self.current_bird_img = self.bird_imgs[
            round(abs(((self.start_time - time.time())
                       * self.animation_speed
                       % 4)
                      - 2))
        ]

    def keyboard_pressed(self, key):
        super().keyboard_pressed(key)
        if key == pygame.K_SPACE:
            self.jump()

    def apply_gravity(self):
        self.acc_y += self.gravity_force

    def jump(self):
        if not self.dead:
            self.vel_y = -self.jump_force

    def die(self):
        self.jump()
        self.dead = True
