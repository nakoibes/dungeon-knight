import pygame

__all__ = ["Application"]

from application.config import Config
from application.engine import Engine
from application.screen_chain import ScreenHandle, MenuHandler
from application.models import Menus


class Application:
    def __init__(self, name: str, config: Config):
        self._name = name
        self._engine = Engine()
        self._menus = Menus(self._engine)
        self._screen_resolution = (0, 0)
        if config:
            self.config_from_object(config)
        self._chain = MenuHandler(self._screen_resolution, pygame.SRCALPHA, self._menus, (0, 0), ScreenHandle((0, 0)))
        self._chain.connect_engine(self._engine)
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
        self._menus.create_menus()

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._engine.handle_mouse_move(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._engine.handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._engine.handle_mouse_up()

    def handle_key_event(self, event):
        pass

    def handle_menu(self, event):
        if self._engine.show_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._engine.prev_menu_button()
                elif event.key == pygame.K_DOWN:
                    self._engine.next_menu_button()
                elif event.key == pygame.K_RETURN:
                    self._engine.menu_objects[self._engine.current_button].state = "pressed"#FIXME
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self._engine.menu_objects[self._engine.current_button].state = "hover"
                    self._engine.menu_objects[self._engine.current_button].click(self._engine)


    def handle_events(self):
        for event in pygame.event.get():
            self.handle_menu(event)
            if event.type == pygame.QUIT:
                self._engine.game_over = True
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_event(event)
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.handle_key_event(event)

    def run(self):
        self.open()
        self.create_objects()
        while not self._engine.game_over:
            self.handle_events()
            self._game_display.blit(self._chain, (0, 0))
            self._chain.draw(self._game_display)
            pygame.display.update()
        self.close()
