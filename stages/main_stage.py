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
from src.colors import *


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

        self.current_score = 0
        self.highest_score = 0
        self.score_size = 64
        self.score_font = pygame.font.Font(const.FONT_PUBLIC_PIXEL, self.score_size)
        self.score_text = self.score_font.render(str(self.current_score), True, WHITE)

        self.PIPE_SPAWN_DELAY = 90
        self.time_to_pipe = self.PIPE_SPAWN_DELAY

        self.stats_display = Stats('Current generation',
                                   'Highest score',
                                   'Highest fitness',
                                   'Lowest fitness',
                                   'Mean fitness')
        self.layers['UI'].add(self.stats_display)
        self.layers['BACKGROUND'].add(Background())
        self.create_buttons()

        self.start_new_generation()
        self.best_genome = None


    def start_new_generation(self):
        """
        Starts new generation of birds
        Restarts pipes
        Restarts stats
        """
        # Clear display
        self.pipes.clear()
        self.birds.clear()
        for layer in const.LAYERS:
            if layer not in ['BACKGROUND', 'UI']:
                self.layers[layer].empty()

        # Reset score
        self.highest_score = max(self.current_score, self.highest_score)
        self.current_score = 0
        self.score_text = self.score_font.render(str(self.current_score), True, WHITE)

        # Reset best genome
        self.best_genome = None

        # Add entities to layers
        self.ground_tiles = [Ground()]
        self.layers['UNITS'].add(tile for tile in self.ground_tiles)
        self.pipes.append(Pipe())
        self.prev_pipe_index = 0
        self.layers['GROUND'].add(pipe for pipe in self.pipes)
        self.time_to_pipe = self.PIPE_SPAWN_DELAY

        # Spawn new birds
        for _, genome in list(iteritems(self.population.population)):
            bird = Bird(genome=genome,
                        network=neat.nn.FeedForwardNetwork.create(genome,
                                                                  self.neat_config))
            self.birds.append(bird)
            self.layers['PLAYER'].add(bird)

        # Update generation index in stats
        self.population.reporters.start_generation(self.population.generation)
        self.stats_display.update_stats('Current generation', str(self.population.generation))
        self.stats_display.update_stats('Highest score', str(self.highest_score))


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

        # Create the next generation from the current generation.
        self.population.population = self.population.reproduction.reproduce(
            self.neat_config, self.population.species,
            self.neat_config.pop_size, self.population.generation)

        # Divide the new population into species.
        self.population.species.speciate(self.neat_config, self.population.population, self.population.generation)

        self.population.reporters.end_generation(self.neat_config, self.population.population, self.population.species)

        self.population.generation += 1

        if self.neat_config.no_fitness_termination:
            self.population.reporters.found_solution(self.neat_config, self.population.generation, self.population.best_genome)

        return self.population.best_genome


    def update(self):
        """
        Update state of all entities, stats and everything  what needs to be
        updated in current frame
        """
        if [bird.dead for bird in self.birds] == [True] * len(self.birds):
            self.end_current_generation()
            self.start_new_generation()

            super().update()
            return

        # Update mean fitenss in stats
        all_fitness = [bird.genome.fitness for bird in self.birds]
        self.stats_display.update_stats('Mean fitness', str(sum(all_fitness) // len(all_fitness)))
        self.stats_display.update_stats('Highest fitness', str(round(max(all_fitness), 2)))
        self.stats_display.update_stats('Lowest fitness', str(round(min(all_fitness), 2)))
        # Handle spawning pipes
        self.time_to_pipe -= 1
        if self.time_to_pipe <= 0:
            self.spawn_pipe()
            self.time_to_pipe = self.PIPE_SPAWN_DELAY

        # Remove pipes that went off screen
        if self.pipes[0].rect.x + self.pipes[0].width < 0:
            self.layers['GROUND'].remove(self.pipes[0])
            del self.pipes[0]
            self.prev_pipe_index -= 1

        passed_pipe = True
        # Find next pipe not passed by bird
        next_pipe_index = 0
        for bird in self.birds:
            while self.pipes[next_pipe_index].pos_x + self.pipes[next_pipe_index].width < bird.pos_x:
                next_pipe_index += 1

        if self.prev_pipe_index == next_pipe_index:
            passed_pipe = False
        self.prev_pipe_index = next_pipe_index

        for bird in self.birds:
            bird.pipe_collide(self.pipes[next_pipe_index])

            if passed_pipe and not bird.dead:
                bird.new_next_pipe(next_pipe_index)
                bird.passed_pipe()

            # Activate bird brain
            if not bird.dead:
                output = bird.neural_network.activate((bird.pos_y,
                                                       bird.vel_y,
                                                       self.pipes[next_pipe_index].pos_x - bird.pos_x,
                                                       self.pipes[next_pipe_index].gap_start,
                                                       self.pipes[next_pipe_index].gap_end
                                                       ))
                if output[0] > 0.5:
                    bird.jump()
                # Display graph of best bird
                if self.best_genome is None:
                    self.best_genome = bird.genome
                    self.stats_display.draw_nn(self.best_genome, self.neat_config)
                elif bird.genome.fitness > self.best_genome.fitness:
                    self.best_genome = bird.genome
                    self.stats_display.draw_nn(self.best_genome, self.neat_config)

        if passed_pipe:
            self.current_score = max([bird.score for bird in self.birds])
            self.score_text = self.score_font.render(str(self.current_score), True, WHITE)
            if self.current_score > self.highest_score:
                self.highest_score = self.current_score
                self.stats_display.update_stats('Highest score', str(self.highest_score))

        # Removng ground tiles
        if self.ground_tiles[0].pos_x + self.ground_tiles[0].width <= 0:
            self.layers['UNITS'].remove(self.ground_tiles[0])
            del self.ground_tiles[0]

        # Creating ground tiles
        end_of_last_tile = (self.ground_tiles[-1].pos_x
                            + self.ground_tiles[-1].width)
        if end_of_last_tile <= const.WIDTH:
            self.ground_tiles.append(Ground(off_screen=True))
            self.layers['UNITS'].add(self.ground_tiles[-1])

        # Move ground tiles
        for tile in self.ground_tiles:
            tile.pos_x -= const.GAME_SPEED

        super().update()


    def render(self, display):
        super().render(display)
        # Render score
        display.blit(self.score_text, ((const.WIDTH // 2) - (self.score_text.get_rect().width // 2),
                                       const.HEIGHT * 0.15),
                     )


    def spawn_pipe(self):
        """
        Spawns new pipe behind the display
        """
        self.pipes.append(Pipe())
        self.layers['GROUND'].add(self.pipes[-1])


    def create_buttons(self):
        """
        Spawns all buttons needed for this stage
        """
        button_size = (200, 35)
        buttons = [
            Button(
                pos=(10, 10),
                size=button_size,
                color=(255, 255, 255, 100),
                text='DISPLAY STATS',
                click_event=self.stats_display .toggle),
        ]
        for btn in buttons:
            self.layers['UI'].add(btn)


    def keyboard_input(self, key):
        """
        Handles keybord inputs
        """
        super().keyboard_input(key)
        if key == pygame.K_SPACE:
            self.stats_display.toggle()
        if key == pygame.K_d:
            for bird in self.birds:
                bird.die()
