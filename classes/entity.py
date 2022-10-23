import pygame
import src.constants as const


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos=const.TOP_LEFT,
                 image=pygame.Surface(const.TILE_SIZE_MEDIUM),
                 bg_color=None
                 ):
        super().__init__()
        self.image = image
        # self.rect = self.image.get_rect(top=pos[0], left=pos[1])
        self.rect = self.image.get_rect()

        self.image = self.image.convert_alpha()
        self.bg_color = bg_color
        self.pos_x, self.pos_y = float(pos[0]), float(pos[1])
        self.width, self.height = self.rect.width, self.rect.height

        self.left_clicked, self.right_clicked = False, False

        if self.bg_color:
            self.image.fill(self.bg_color)

    def update(self):
        self.update_pos()

    def update_pos(self):
        self.rect.left = self.pos_x
        self.rect.top = self.pos_y

    def mouse_click(self, left_click, scroll_click, right_click, mouse_pos):
        if (mouse_pos[0] in range(int(self.pos_x),
                                  int(self.pos_x + self.width))
            and mouse_pos[1] in range(int(self.pos_y),
                                      int(self.pos_y + self.height))):
            if left_click:
                self.left_clicked = True
            if right_click:
                self.right_clicked = True

    def mouse_release(self, mouse_pos):
        self.left_clicked, self.right_clicked = False, False

    def keyboard_pressed(self, key):
        pass

    def set_bg_color(self, color):
        self.bg_color = color
        self.image.fill(self.bg_color)
