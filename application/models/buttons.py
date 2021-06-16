import pygame
from application.models.text_object import TextObject
from application.config import Config as c
from abc import abstractmethod, ABCMeta
from application.models.base_game_button_state import AbstractButtonState

__all__ = ["PlayButton", "AutoPlayButton", "QuitButton", "Button"]


class Button(metaclass=ABCMeta):
    def __init__(self, text, params, position, menu, state="normal"):
        self.menu = menu
        self.normal_state = NormalState(self)
        self.hover_state = HoverState(self)
        self.pressed_state = PressedState(self)
        self.current_state = CurrentButtonState(self)
        self.state = self.init_state(state)
        self.bounds = pygame.rect.Rect(position[0], position[1], params[0], params[1])
        self.position = position
        self.text = TextObject(
            position, lambda: text, c.button_text_color, c.font_name, c.font_size, params, centralized=True
        )
        self.params = params

    def get_normal_state(self):
        return self.normal_state

    def get_hover_state(self):
        return self.hover_state

    def get_pressed_state(self):
        return self.pressed_state

    def get_current_state(self):
        return self.current_state

    def set_state(self, state):
        self.state = state

    def press(self):
        self.state.press()

    def hover(self):
        self.state.hover()

    def remove(self):
        self.state.remove()

    def free(self):
        self.state.free()

    def remove_current(self):
        self.state.remove_current()

    def press_return(self):
        self.state.press_return()

    def init_state(self, state):
        return dict(
            normal=self.normal_state, hover=self.hover_state, pressed=self.pressed_state, current=self.current_state
        )[state]

    @abstractmethod
    def click(self, state):
        pass

    # def _get_surface(self, text):
    #     text_surface = self.font.render(text, False, self.color)
    #     return text_surface, text_surface.get_rect()


class QuitButton(Button):
    def click(self, state):
        state.session.finish()


class PlayButton(Button):
    def click(self, state):
        pass


class AutoPlayButton(Button):
    def click(self, state):
        pass


class NormalState(AbstractButtonState):
    def __init__(self, button):
        self.color = c.button_normal_back_color
        self.button = button

    def press(self):
        pass

    def hover(self):
        self.button.set_state(self.button.get_hover_state())
        self.button.menu.remove_current_button()
        self.button.menu.current_button = self.button.menu.main_menu_objects.index(self.button)

    def remove(self):
        pass

    def free(self):
        pass

    def remove_current(self):
        pass

    def press_return(self):
        pass


class HoverState(AbstractButtonState):
    def __init__(self, button):
        self.color = c.button_hover_back_color
        self.button = button

    def press(self):
        self.button.set_state(self.button.get_pressed_state())

    def hover(self):
        pass

    def remove(self):
        self.button.set_state(self.button.get_current_state())

    def free(self):
        pass

    def remove_current(self):
        pass

    def press_return(self):
        self.button.set_state(self.button.get_pressed_state())


class PressedState(AbstractButtonState):
    def __init__(self, button):
        self.color = c.button_pressed_back_color
        self.button = button

    def press(self):
        pass

    def hover(self):
        pass

    def remove(self):
        self.button.set_state(self.button.get_current_state())

    def free(self):
        self.button.click(self.button.menu.game_session.state)
        self.button.set_state(self.button.get_hover_state())

    def remove_current(self):
        pass

    def press_return(self):
        pass


class CurrentButtonState(AbstractButtonState):
    def __init__(self, button):
        self.color = c.button_hover_back_color
        self.button = button

    def press(self):
        pass

    def hover(self):
        self.button.set_state(self.button.get_hover_state())

    def remove(self):
        pass

    def free(self):
        pass

    def remove_current(self):
        self.button.set_state(self.button.get_normal_state())

    def press_return(self):
        self.button.set_state(self.button.get_pressed_state())
