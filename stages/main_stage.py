from .stage import Stage

from classes.button import Button
from classes.stats import Stats
from classes.background import Background
from classes.ground import Ground
from classes.bird import Bird
from classes.pipe import Pipe

import src.constants as const

import neat


class GameStage(Stage):
    neat_config = neat.config.Config(neat.DefaultGenome,
                                     neat.DefaultReproduction,
                                     neat.DefaultSpeciesSet,
                                     neat.DefaultStagnation,
                                     "neat_config.txt")
    population = neat.Population(neat_config)

    def __init__(self):
        super().__init__()

        self.next = 'Settings'
        self.birds = []
        self.pipes = []

        self.stats_display = Stats()
        self.layers['UI'].add(self.stats_display)
        self.layers['BACKGROUND'].add(Background())

        self.population.add_reporter(neat.StdOutReporter(True))
        population_stats = neat.StatisticsReporter()
        self.population.add_reporter(population_stats)

        self.population.run(self.new_gen_thread.start, 1)

    def new_generation(self, genomes, config):
        self.pipes.clear()
        self.birds.clear()
        for layer in const.LAYERS:
            if layer not in ['BACKGROUND', 'UI']:
                self.layers[layer].empty()

        self.ground_tiles = [Ground()]
        self.layers['UNITS'].add(tile for tile in self.ground_tiles)
        self.pipes.append(Pipe())
        self.layers['GROUND'].add(pipe for pipe in self.pipes)

        for _, genome in genomes:
            bird = Bird(genome=genome,
                        network=neat.nn.FeedForwardNetwork.create(genome, config))
            self.birds.append(bird)
            self.layers['PLAYER'].add(bird)

        self.create_buttons()
        while True:
            print(1)

    def update(self):
        super().update()
        if [bird.dead for bird in self.birds] == [True] * len(self.birds):
            self.population.run(self.new_generation, 1)
            return

        # Spawning and removing pipes
        # TODO(Aa_Pawelek): change self.birds[0] to something better
        if self.pipes[-1].pos_x + self.pipes[-1].width < self.birds[0].pos_x:
            self.pipes.append(Pipe())
            self.layers['GROUND'].add(self.pipes[-1])

        if self.pipes[0].rect.x + self.pipes[0].width < 0:
            self.layers['GROUND'].remove(self.pipes[0])
            del self.pipes[0]

        for bird in self.birds:
            # TODO(Aa_Pawelek): Collide pipe[0]
            for pipe in self.pipes:
                bird.pipe_collide(pipe)

            output = bird.network.activate((bird.pos_y,
                                            bird.vel_y,
                                            self.pipes[0].pos_x,
                                            self.pipes[0].gap_start))
            if output[0] > 0.5:
                bird.jump()



        # Spawning and removing ground tiles
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

    def create_buttons(self):
        button_size = (200, 40)
        buttons = [
            Button(
                pos=(10, 10),
                size=button_size,
                color=(255, 255, 255, 100),
                text='DISPLAY STATS',
                click_event=self.stats_display .toggle),
            Button(
                pos=(10, 10 + 1.2*button_size[1]),
                size=button_size,
                color=(255, 255, 255, 100),
                text='SPEED: x1',
                click_event=None),
        ]

        for btn in buttons:
            self.layers['UI'].add(btn)
