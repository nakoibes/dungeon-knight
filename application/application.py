import pygame

__all__ = ["Application"]

from application.config import Config
from application.engine import GameSession
from application.screen_chain import ScreenHandle, MenuHandler
from application.models import Menus


class Application:
    def __init__(self, name: str, config: Config):

        self._name = name
        self._menus = Menus()
        self._screen_resolution = (0, 0)
        if config:
            self.config_from_object(config)
        self.menu_chain = MenuHandler(
            self._screen_resolution, pygame.SRCALPHA, self._menus, (0, 0), ScreenHandle((0, 0))
        )
        self._game_session = GameSession(self.menu_chain, self._menus)
        self.menu_chain.connect_engine(self._game_session)
        self._game_display = pygame.display.set_mode(self._screen_resolution)
        self._menus.session = self._game_session

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

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._game_session.state.handle_mouse_move(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._game_session.state.handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._game_session.state.handle_mouse_up()

    def handle_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._game_session.state.handle_key_up()
            elif event.key == pygame.K_DOWN:
                self._game_session.state.handle_key_down()
            elif event.key == pygame.K_RETURN:
                self._game_session.menus.main_menu_objects[self._game_session.menus.current_button].set_pressed_state()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self._game_session.menus.main_menu_objects[self._game_session.menus.current_button].set_hover_state()
                self._game_session.menus.main_menu_objects[self._game_session.menus.current_button].click(
                    self._game_session.state
                )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_session.state.handle_esc()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_event(event)
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.handle_key_event(event)

    def run(self):
        self.open()
        self.create_objects()
        while self._game_session.state.state != "End":
            self._game_display.blit(self._game_session.state.get_chain(), (0, 0))
            self._game_session.state.draw(self._game_display)
            pygame.display.update()
            self.handle_events()
        self.close()
