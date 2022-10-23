import pygame
import stages
from engine import Engine
from event_handler import EventHandler
import src.constants as const


class Setup:
    def __init__(self):
        self.set_title()
        self.display = pygame.display.set_mode(size=const.SIZE)
        self.clock = pygame.time.Clock()
        self.event_handler = EventHandler()

        # Combining names of stages to actual stages classes
        stages_names = stages.get_stages_name()
        stages_objects = stages.get_stages()
        starting_stage = stages.get_starting_stage_name()
        self.game_stages = {stages_names[i]: stages_objects[i]
                            for i in range(len(stages_names))}
        self.staring_stage = starting_stage

        self.fps = const.FPS

    def set_title(self):
        pygame.display.set_caption(const.TITLE)

    def get_display(self) -> pygame.display.set_mode:
        return self.display

    def get_clock(self) -> pygame.time.Clock:
        return self.clock

    def get_surface(self) -> pygame.Surface:
        return pygame.Surface(size=const.SIZE)

    def get_game_stages(self) -> dict:
        return self.game_stages

    def get_event_handler(self) -> EventHandler:
        return self.event_handler

    def get_fps(self):
        return self.fps

    def get_engine(self) -> Engine:
        return Engine(self.display, self.clock,
                      self.game_stages, self.staring_stage,
                      self.event_handler, self.fps)
