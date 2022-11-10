import pygame
from setup import Setup



def main():
    pygame.init()
    setup = Setup()
    engine = setup.get_engine()

    # Start main game loop
    engine.run_game()


if __name__ == '__main__':
    main()
