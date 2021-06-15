from application.config import Config as c
from application.service import create_sprite
from application.models.buttons import PlayButton, AutoPlayButton, QuitButton, Button

__all__ = ["Menus"]


class Menus:  # TODO
    current_menu = "main"
    main_menu_objects: list[Button] = []
    current_button = None
    show_menu = True
    menu_button_params = (c.menu_button_width, c.menu_button_height)

    def __init__(self, engine):
        self._engine = engine
        self.img = None

    def create_menus(self):
        self.create_main_menu()
        self.create_background()

    def create_background(self):
        self.img = create_sprite(c.menu_texture, c.SCREEN_RESOLUTION)

    def create_main_menu(self):
        buttons = [
            PlayButton("Играть", self.menu_button_params, (300, 200), state="hover", current=True),
            AutoPlayButton("Автоигра", self.menu_button_params, (300, 270)),
            QuitButton("Выход", self.menu_button_params, (300, 340)),
        ]
        self.main_menu_objects.extend(buttons)
        self.current_button = buttons[0]
        for button in buttons:
            self._engine.subscribe_button(button)
        self._engine.current_button = 0
