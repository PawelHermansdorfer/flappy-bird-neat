import pygame
from setup import Setup


""" NOTE(Aa_Pawelek): LEFT CLICK TO PAINT WALLS OR DRAG START/END NODE AND RIGHT CLICK TO ERASES """


def main():
    pygame.init()
    setup = Setup()
    engine = setup.get_engine()

    # Start main game loop
    engine.run_game()


if __name__ == '__main__':
    main()
