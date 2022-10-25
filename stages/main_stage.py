from operator import ne
import pygame
import neat
from neat.six_util import iteritems, itervalues

from .stage import Stage
from classes.button import Button
from classes.stats import Stats
from classes.background import Background
from classes.ground import Ground
from classes.bird import Bird
from classes.pipe import Pipe
import src.constants as const


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
        self.PIPE_SPAWN_DELAY = 90
        self.time_to_pipe = self.PIPE_SPAWN_DELAY

        self.stats_display = Stats('Generation',
                                   'Highest score',
                                   'Highest fitness',
                                   'Avg fitness')
        self.layers['UI'].add(self.stats_display)
        self.layers['BACKGROUND'].add(Background())
        self.create_buttons()

        self.population.add_reporter(neat.StdOutReporter(True))
        population_stats = neat.StatisticsReporter()
        self.population.add_reporter(population_stats)

        self.start_new_generation()

    def start_new_generation(self):
        self.pipes.clear()
        self.birds.clear()
        for layer in const.LAYERS:
            if layer not in ['BACKGROUND', 'UI']:
                self.layers[layer].empty()

        self.ground_tiles = [Ground()]
        self.layers['UNITS'].add(tile for tile in self.ground_tiles)
        self.pipes.append(Pipe())
        self.layers['GROUND'].add(pipe for pipe in self.pipes)
        self.time_to_pipe = self.PIPE_SPAWN_DELAY

        for _, genome in list(iteritems(self.population.population)):
            bird = Bird(genome=genome,
                        network=neat.nn.FeedForwardNetwork.create(genome,
                                                                  self.neat_config))
            self.birds.append(bird)
            self.layers['PLAYER'].add(bird)


        self.population.reporters.start_generation(self.population.generation)

    def end_current_generation(self):
        # Gather and report statistics.
        best = None
        for g in itervalues(self.population.population):
            if best is None or g.fitness > best.fitness:
                best = g
        self.population.reporters.post_evaluate(self.neat_config,
                                                self.population.population,
                                                self.population.species,
                                                best)

        # Track the best genome ever seen.
        if self.population.best_genome is None or best.fitness > self.population.best_genome.fitness:
            self.population.best_genome = best

        if not self.neat_config.no_fitness_termination:
            # End if the fitness threshold is reached.
            fv = self.population.fitness_criterion(g.fitness for g in itervalues(self.population.population))
            if fv >= self.neat_config.fitness_threshold:
                self.population.reporters.found_solution(self.neat_config, self.population.generation, best)
                # TODO(Aa_Pawelek): MAKE END WHEN FITNESS CAP IS REACHED
                print('Fitness cap')

        # Create the next generation from the current generation.
        self.population.population = self.population.reproduction.reproduce(
            self.neat_config, self.population.species,
            self.neat_config.pop_size, self.population.generation)

        # Check for complete extinction.
        if not self.population.species.species:
            self.population.reporters.complete_extinction()

            # If requested by the user, create a completely new population,
            # otherwise raise an exception.
            if self.neat_config.reset_on_extinction:
                self.population.population = self.population.reproduction.create_new(self.neat_config.genome_type,
                                                                self.neat_config.genome_config,
                                                                self.neat_config.pop_size)
            else:
                raise neat.CompleteExtinctionException()

        # Divide the new population into species.
        self.population.species.speciate(self.neat_config, self.population.population, self.population.generation)

        self.population.reporters.end_generation(self.neat_config, self.population.population, self.population.species)

        self.population.generation += 1

        if self.neat_config.no_fitness_termination:
            self.population.reporters.found_solution(self.neat_config, self.population.generation, self.population.best_genome)

        return self.population.best_genome

    def update(self):
        if [bird.dead for bird in self.birds] == [True] * len(self.birds):
            self.end_current_generation()
            self.start_new_generation()
            super().update()
            return

        self.time_to_pipe -= 1
        if self.time_to_pipe <= 0:
            self.spawn_pipe()
            self.time_to_pipe = self.PIPE_SPAWN_DELAY

        if self.pipes[0].rect.x + self.pipes[0].width < 0:
            self.layers['GROUND'].remove(self.pipes[0])
            del self.pipes[0]

        for bird in self.birds:
            # TODO(Aa_Pawelek): Collide pipe[0]
            next_pipe_index = 0
            while self.pipes[next_pipe_index].pos_x + self.pipes[next_pipe_index].width < bird.pos_x:
                next_pipe_index += 1
            bird.pipe_collide(self.pipes[next_pipe_index])

            if not bird.dead:
                output = bird.neural_network.activate((bird.pos_y,
                                                       bird.vel_y,
                                                       self.pipes[next_pipe_index].gap_start,
                                                       self.pipes[next_pipe_index].gap_end
                                                       ))
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

        super().update()

    def spawn_pipe(self):
        self.pipes.append(Pipe())
        self.layers['GROUND'].add(self.pipes[-1])

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

    def keyboard_input(self, key):
        super().keyboard_input(key)
        # NOTE: DEBUG
        if key == pygame.K_SPACE:
            self.stats_display.toggle()
