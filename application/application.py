import pygame

__all__ = ["Application"]

from application.config import Config
from application.engine import Engine


class Application:
    def __init__(self, name: str, config: Config):
        self._name = name
        self._engine = Engine()
        self._screen_resolution = None
        if config:
            self.config_from_object(config)

    def config_from_object(self, config: Config):
        self._screen_resolution = config.SCREEN_RESOLUTION

    def open(self):
        pygame.init()
        game_display = pygame.display.set_mode(self._screen_resolution)
        pygame.display.set_caption(self._name)

    def close(self):
        pygame.display.quit()
        pygame.quit()
        exit(0)

    def run(self):
        self.open()
        while self._engine.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._engine.working = False
        self.close()
