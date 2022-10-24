import pygame
from .entity import Entity
import src.constants as const
from src.colors import BLACK, TRANSPARENT, TRANSPARENT_GREY, WHITE_SMOKE


class Stats(Entity):
    display_center = (const.WIDTH_CENTER, const.HEIGHT * 0.8)
    display_size = (const.WIDTH//1.2, const.HEIGHT//4)

    def __init__(self, *args):
        if len(args) == 0:
            raise ValueError('No stats passed')

        super().__init__(
            pos=(self.display_center[0]-self.display_size[0]//2,
                 self.display_center[1]-self.display_size[1]//2),
            image=pygame.Surface(self.display_size),
            bg_color=TRANSPARENT
        )
        self.hidden = True
        self.font_size = round((self.display_size[1] / len(args))
                               - 10)
        self.font_line_width = self.font_size
        self.font = pygame.font.Font(const.FONT_VICTOR_MONO, self.font_size)

        self.text_lines = {key: 'NAN' for key in args}


    def add_text(self, text):
        # TODO: dict 
        text = self.font.render(text, True, WHITE_SMOKE)
        self.text_lines.append(text)
        self.update_image()

    def clear_text(self):
        self.text_lines.clear()
        self.update_image()

    def update_image(self):
        if not self.hidden:
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
            for i, text in enumerate(self.text_lines):
                self.image.blit(text, text.get_rect(left=0, top=self.font_line_width*i))
        else:
            self.image.fill(TRANSPARENT)

    def toggle(self):
        self.hidden = not self.hidden
        self.update_image()
