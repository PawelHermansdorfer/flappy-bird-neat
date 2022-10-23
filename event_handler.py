import pygame
import sys


class EventHandler():
    def handle_events(self, current_stage) -> None:
        for event in pygame.event.get():
            self.check_quit_event(event)
            self.check_keyboard_event(event, current_stage)
            self.check_mouse_events(event, current_stage)

    def check_quit_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                         and event.key == pygame.K_ESCAPE):
            self.quit_game()

    def check_keyboard_event(self, event, current_stage):
        if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
            # Passing pressed keys to current game stage
            current_stage.keyboard_input(event.key)

    def check_mouse_events(self, event, current_stage):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            current_stage.mouse_pressed(left_click=pressed_buttons[0],
                                        scroll_click=pressed_buttons[1],
                                        right_click=pressed_buttons[2],
                                        mouse_pos=mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            current_stage.mouse_release(mouse_pos=mouse_pos)

    def quit_game(self):
        pygame.quit()
        sys.exit()

