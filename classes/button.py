import pygame
from .entity import Entity
import src.constants as const
from src.colors import BLACK, TRANSPARENT, WHITE


class Button(Entity):
    def __init__(self, pos=const.TOP_LEFT, size=const.TILE_SIZE_MEDIUM,
                 color=WHITE, text=None,
                 color_multiplier=0.7, font_size=const.FONT_SIZE,
                 frame_width=const.BUTTON_FRAME_WIDTH, click_event=None):
        super().__init__(pos, pygame.Surface(size), color)

        self.click_event = click_event
        self.hidden = False

        self.font = pygame.font.Font(const.FONT_VICTOR_MONO, font_size)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.width // 2,
                                                    self.height // 2))

        self.not_pressed_color = color
        self.pressed_color = (color[0] * color_multiplier,
                              color[1] * color_multiplier,
                              color[2] * color_multiplier)
        self.color = self.not_pressed_color

        self.frame_rect = self.image.get_rect()
        self.frame_width = int(frame_width)
        self.update_image()

    def update_text(self, text):
        self.text = self.font.render(text, True, (0, 0, 0))
        self.update_image()

    def mouse_click(self, left_click, scroll_click, right_click, mouse_pos):
        super().mouse_click(left_click, scroll_click, right_click, mouse_pos)
        if left_click and self.left_clicked and not self.hidden:
            self.color = self.pressed_color
            self.update_image()

    def mouse_release(self, mouse_pos):
        if (self.left_clicked
            and self.click_event is not None
                and not self.hidden):
            self.click_event()
        super().mouse_release(mouse_pos)
        self.color = self.not_pressed_color
        self.update_image()

    def update_image(self):
        if self.hidden:
            self.image.fill(TRANSPARENT)
        else:
            self.image.fill(self.color)
            self.image.blit(self.text, self.text_rect)
            pygame.draw.rect(
                self.image,
                BLACK,
                self.frame_rect,
                self.frame_width)

    def hide(self):
        self.hidden = True
        self.update_image()

    def unhide(self):
        self.hidden = False
        self.update_image()
