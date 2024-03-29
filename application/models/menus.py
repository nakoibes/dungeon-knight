from application.config import Config as c
from application.models.base_models import AbstractMenu

from application.service import create_sprite
from application.models.buttons import PlayButton, AutoPlayButton, QuitButton

from application.service.linked_list import DoubleLinkedList

__all__ = ["Menus"]


class Menus:
    def __init__(self):
        self.menus = []
        self.main_menu = None
        self.img = None
        self.game_session = None
        self.state = None

    @property
    def current_buttons(self):
        return self.state.buttons

    def create_menus(self, session):
        # self.set_game_session(session)
        self.main_menu = MainMenu()
        self.menus.extend([self.main_menu])
        for menu in self.menus:
            menu.create_menu(session)
        self.state = self.main_menu

    # def set_game_session(self, session):
    #     self.state.set_game_session(session)

    def remove_current_button(self):
        self.state.remove_current_button()


class MainMenu(AbstractMenu):
    def __init__(self):
        self.menu_button_params = (c.menu_button_width, c.menu_button_height)
        self.img = None
        self.game_session = None
        self.buttons = None

    def create_menu(self, session):
        self.set_game_session(session)
        self.create_background()
        self.buttons = DoubleLinkedList(
            [
                PlayButton("Играть", self.menu_button_params, (300, 200), self, state="current"),
                AutoPlayButton("Автоигра", self.menu_button_params, (300, 270), self),
                QuitButton("Выход", self.menu_button_params, (300, 340), self),
            ]
        )

    def create_background(self):
        self.img = create_sprite(c.menu_texture, c.SCREEN_RESOLUTION)

    def set_game_session(self, session):
        self.game_session = session

    def remove_current_button(self):
        for obj in self.buttons:
            obj.remove_current()
