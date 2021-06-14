import pygame
from application.models.text_object import TextObject
from application.config import Config as c

__all__ = ["PlayButton", "AutoPlayButton", "QuitButton"]


class Button:
    def __init__(self, text, params, position, state="normal", current=False):
        self.bounds = pygame.rect.Rect(position[0], position[1], params[0], params[1])
        self.position = position
        self.text = TextObject(position, lambda: text, c.button_text_color,
                               c.font_name, c.font_size, params, centralized=True)
        #self.current = current
        self.state = state
        self.params = params

    @property
    def back_color(self):
        return dict(normal=c.button_normal_back_color,
                    hover=c.button_hover_back_color,
                    pressed=c.button_pressed_back_color)[self.state]

    def click(self, engine):
        pass

    # def _get_surface(self, text):
    #     text_surface = self.font.render(text, False, self.color)
    #     return text_surface, text_surface.get_rect()


class QuitButton(Button):
    def click(self, engine):
        engine.game_over = True


class PlayButton(Button):
    def click(self, engine):
        pass


class AutoPlayButton(Button):
    def click(self, engine):
        pass
