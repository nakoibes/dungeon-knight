import pygame
from collections import defaultdict

__all__ = ["Application"]

from application.config import Config
from application.engine import Engine
from application.screen_chain import ScreenHandle, MenuHandler
from application.system_objects import Menus


class Application:
    def __init__(self, name: str, config: Config):
        self._name = name
        self._engine = Engine()
        self._menus = Menus(self._engine)
        self._screen_resolution = None
        if config:
            self.config_from_object(config)
        self._chain = MenuHandler(self._screen_resolution, pygame.SRCALPHA, self._menus, (0, 0),
                                  ScreenHandle(
                                      (0, 0)
                                  ))
        self._chain.connect_engine(self._engine)
        self._game_display = pygame.display.set_mode(self._screen_resolution)
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def config_from_object(self, config: Config):
        self._screen_resolution = config.SCREEN_RESOLUTION

    def open(self):
        pygame.init()
        pygame.display.set_caption(self._name)

    @staticmethod
    def close():
        pygame.display.quit()
        pygame.quit()
        exit(0)

    def create_objects(self):
        self._menus.create_menus()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._engine.game_over = True
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION): #TODO
                if event.type == pygame.MOUSEMOTION:
                    self._engine.handle_mouse_move(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._engine.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._engine.handle_mouse_up()


    def run(self):
        self.open()
        self.create_objects()
        while not self._engine.game_over:
            self.handle_events()
            self._game_display.blit(self._chain, (0, 0))
            self._chain.draw(self._game_display)
            pygame.display.update()
        self.close()
