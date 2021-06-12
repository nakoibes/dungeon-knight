from application.config import Config as c
from application.service import create_sprite
import pygame

__all__ = ["Menus", "Button"]


class Menus:  # TODO
    current_menu = "main"  # FIXIT
    main_menu_objects = []
    show_menu = True
    menu_button_params = (c.menu_button_width, c.menu_button_height)

    def __init__(self, engine):
        self.engine = engine
        self.img = None

    def create_menus(self):
        self.create_main_menu()
        self.create_background()

    def create_background(self):
        self.img = create_sprite(c.menu_texture, c.SCREEN_RESOLUTION)

    def create_main_menu(self):
        def on_quit(engine):  # TODO
            engine.game_over = True

        buttons = [Button("Играть", self.menu_button_params, (300, 200)),
                   Button("Автоигра", self.menu_button_params, (300, 270)),
                   Button("Выход", self.menu_button_params, (300, 340), on_quit)]
        self.main_menu_objects.extend(buttons)
        for button in buttons:
            self.engine.subscribe_button(button)


class Button:  # TODO
    def __init__(self, text, params, position, on_click=lambda x: None):
        self.bounds = pygame.rect.Rect(position[0], position[1], params[0], params[1])
        self.on_click = on_click
        self.position = position
        self.text = TextObject(position, lambda: text, c.button_text_color,
                               c.font_name, c.font_size, params, centralized=True)
        self.state = "normal"
        self.params = params

    @property
    def back_color(self):
        return dict(normal=c.button_normal_back_color,
                    hover=c.button_hover_back_color,
                    pressed=c.button_pressed_back_color)[self.state]

    # def _get_surface(self, text):
    #     text_surface = self.font.render(text, False, self.color)
    #     return text_surface, text_surface.get_rect()


class ConcreteButton(Button):
    pass


class TextObject:
    def __init__(self, position, text_func, color, font_name, font_size, back_size, centralized=False):
        self.text = text_func()
        self.back_size = back_size
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.text_surface, self.bounds = self._get_surface(text_func())
        self.position = self._set_position(position, centralized)

    def _set_position(self, position, centralized):
        if centralized:
            return (position[0] + (self.back_size[0] - self.bounds.width) // 2,
                    position[1] + (self.back_size[1] - self.bounds.height) // 2)
        return position

    def _get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

# class Behavior:
#     pass
#
#
# class Quit(Behavior):
#     def act(self):
#         pass
