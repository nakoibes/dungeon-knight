from application.config import Config as c


from application.service import create_sprite
from application.models.buttons import PlayButton, AutoPlayButton, QuitButton, Button

__all__ = ["Menus"]


class Menus:
    menu_button_params = (c.menu_button_width, c.menu_button_height)

    def __init__(self):
        self.main_menu = None
        self.img = None
        self.game_session = None
        self.state = None

    @property
    def current_buttons(self):
        return self.state.buttons

    current_button = property()

    @current_button.getter
    def current_button(self):
        return self.state.current_button

    @current_button.setter
    def current_button(self, current_button):
        self.state.current_button = current_button

    def create_menus(self):
        self.main_menu = MainMenu()

        self.state = self.main_menu
        self.state.create_background()

    def set_game_session(self, session):
        self.state.set_game_session(session)

    def remove_current_button(self):
        self.state.remove_current_button()


class MainMenu:
    menu_button_params = (c.menu_button_width, c.menu_button_height)
    main_menu_objects: list[Button] = []
    current_button = 0

    def __init__(self):
        self.current_button = 0
        self.img = None
        self.game_session = None
        self.buttons = [
            PlayButton("Играть", self.menu_button_params, (300, 200), self, state="current"),
            AutoPlayButton("Автоигра", self.menu_button_params, (300, 270), self),
            QuitButton("Выход", self.menu_button_params, (300, 340), self),
        ]

    def create_background(self):
        self.img = create_sprite(c.menu_texture, c.SCREEN_RESOLUTION)

    def set_game_session(self, session):
        self.game_session = session

    def remove_current_button(self):
        for obj in self.buttons:
            obj.remove_current()
