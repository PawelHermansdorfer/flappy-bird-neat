from .main_stage import GameStage
from .settings import Settings


def get_stages_name():
    return ['MainGame',
            'Settings']


def get_stages():
    return [GameStage,
            Settings]


def get_starting_stage_name():
    return get_stages_name()[0]
