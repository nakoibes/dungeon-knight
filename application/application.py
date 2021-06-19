import pygame

__all__ = ["Application"]

from application.config import Config
from application.game_session import GameSession
from application.screen_chain import ScreenHandler, MenuHandler
from application.models import Menus
from application.vocabulary import KEYBOARD_MAPPING, MOUSE_MAPPING


class Application:
    def __init__(self, name: str, config: Config):
        self.pygame_mouse_buttons_dict = MOUSE_MAPPING
        self.pygame_keyboard_keys_dict = KEYBOARD_MAPPING
        self._name = name
        self._menus = Menus()
        self._screen_resolution = (0, 0)
        if config:
            self.config_from_object(config)
        self.menu_chain = MenuHandler(
            self._screen_resolution, pygame.SRCALPHA, self._menus, (0, 0), ScreenHandler((0, 0))
        )
        self._game_session = GameSession(self.menu_chain, self._menus)

        self._game_display = pygame.display.set_mode(self._screen_resolution)

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
        self._menus.create_menus(self._game_session)

    def handle_mouse_event(self, event):
        self._game_session.handle_mouse(self.pygame_mouse_buttons_dict.get(event.type), event.pos)

    def handle_keyboard_key_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self._game_session.handle_keyboard_key(self.pygame_keyboard_keys_dict.get(event.key, "no_key"), "down")
        elif event.type == pygame.KEYUP:
            self._game_session.handle_keyboard_key(self.pygame_keyboard_keys_dict.get(event.key, "no_key"), "up")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_session.finish()
            elif event.type in self.pygame_mouse_buttons_dict.keys():
                self.handle_mouse_event(event)
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                self.handle_keyboard_key_event(event)

    def run(self):
        self.open()
        self.create_objects()
        while not self._game_session.end:
            self._game_display.blit(self._game_session.state.get_chain(), (0, 0))
            self._game_session.state.draw(self._game_display)
            pygame.display.update()
            self.handle_events()
        self.close()
