from .stage import Stage
from classes.button import Button
from classes.stats import Stats
from classes.background import Background
from classes.ground import Ground
from classes.bird import Bird
from classes.pipe import Pipe
import src.constants as const


class GameStage(Stage):
    def __init__(self):
        super().__init__()
        self.next = 'Settings'
        self.create_buttons()
        # self.layers['UI'].add(Stats())

        self.layers['BACKGROUND'].add(Background())

        self.ground_tiles = [Ground()]
        self.layers['UNITS'].add(tile for tile in self.ground_tiles)

        self.bird = Bird()
        self.layers['PLAYER'].add(self.bird)

        self.pipes = [Pipe()]
        self.layers['GROUND'].add(pipe for pipe in self.pipes)

    def update(self):
        # Spawning and removing pipes
        if self.pipes[-1].pos_x + self.pipes[-1].width < self.bird.pos_x:
            self.pipes.append(Pipe())
            self.layers['GROUND'].add(self.pipes[-1])

        if self.pipes[0].rect.x + self.pipes[0].width < 0:
            self.layers['GROUND'].remove(self.pipes[0])
            del self.pipes[0]

        for pipe in self.pipes:
            self.bird.pipe_colide(pipe)

        # Spawning and removing gorund tiles
        if self.ground_tiles[0].pos_x + self.ground_tiles[0].width <= 0:
            self.layers['UNITS'].remove(self.ground_tiles[0])
            del self.ground_tiles[0]

        end_of_last_tile = (self.ground_tiles[-1].pos_x
                            + self.ground_tiles[-1].width)
        if end_of_last_tile <= const.WIDTH:
            self.ground_tiles.append(Ground(off_screen=True))
            self.layers['UNITS'].add(self.ground_tiles[-1])

        for tile in self.ground_tiles:
            tile.pos_x -= const.GAME_SPEED

        super().update()

    def create_buttons(self):
        button_size = (200, 40)
        buttons = [
                Button(
                    pos=(10, 10),
                    size=button_size,
                    color=(255, 255, 255, 100),
                    text='DISPLAY STATS',
                    click_event=self.display_stats),
                Button(
                    pos=(10, 10 + 1.2*button_size[1]),
                    size=button_size,
                    color=(255, 255, 255, 100),
                    text='SPEED: x1',
                    click_event=None),
                ]

        for btn in buttons:
            self.layers['UI'].add(btn)

    def toggle_stats(self):
        self.display_stats = True

    def display_stats(self):
        pass
