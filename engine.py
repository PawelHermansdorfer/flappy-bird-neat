import pygame


class Engine:
    def __init__(self, display,
                 clock, game_stages, starting_stage_name,
                 event_handler, fps):
        self.display = display
        self.clock = clock
        self.game_stages = game_stages
        self.staring_stage_name = starting_stage_name
        self.event_handler = event_handler
        self.fps = fps

        # Accessing first game stage
        self.current_stage_name = self.staring_stage_name
        self.current_stage = self.game_stages[self.staring_stage_name]()

    def run_game(self):

        # Main game loop
        while True:
            self.clock.tick(self.fps)
            # print(self.clock.get_fps())

            self.event_handler.handle_events(current_stage=self.current_stage)
            self.update_and_render_stage()
            pygame.display.flip()

    def update_and_render_stage(self):
        if self.current_stage.done:
            try:
                self.change_stage(self.current_stage.next)
            except KeyError:
                raise Exception('Current stage has no next scene to load')

        self.current_stage.update()
        self.current_stage.render(self.display)

    def change_stage(self, stage_name):
        self.current_stage_name = stage_name
        self.current_stage = self.game_stages[stage_name]()

    def get_current_stage(self):
        return self.current_stage

    def get_current_stage_name(self):
        return self.current_stage_name
