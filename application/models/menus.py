from application.config import Config as c
from application.service import create_sprite
from application.models.buttons import PlayButton, AutoPlayButton, QuitButton, Button

__all__ = ["Menus"]


class Menus:  # TODO
    current_menu = "main"
    main_menu_objects: list[Button] = []
    current_button = 0
    menu_button_params = (c.menu_button_width, c.menu_button_height)

    def __init__(self):
        self.img = None
        self.game_session = None

    def create_menus(self):
        self.create_main_menu()
        self.create_background()

    def create_background(self):
        self.img = create_sprite(c.menu_texture, c.SCREEN_RESOLUTION)

    def create_main_menu(self):
        buttons = [
            PlayButton("Играть", self.menu_button_params, (300, 200), self, state="current"),
            AutoPlayButton("Автоигра", self.menu_button_params, (300, 270), self),
            QuitButton("Выход", self.menu_button_params, (300, 340), self),
        ]
        self.main_menu_objects.extend(buttons)
        # self.current_button = 0

    def set_game_session(self, session):
        self.game_session = session

    def remove_current_button(self):
        for obj in self.main_menu_objects:
            obj.remove_current()
