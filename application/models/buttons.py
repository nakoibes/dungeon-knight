import pygame

from application.game_session.base_game_session_state import AbstractGameSessionState
from application.models.text_object import TextObject
from application.config import Config as c
from abc import abstractmethod, ABCMeta
from application.models.base_models import AbstractButtonState


# __all__ = ["PlayButton", "AutoPlayButton", "QuitButton", "Button"]


class Button(metaclass=ABCMeta):
    def __init__(self, text, params, position, menu, state="normal"):
        self.menu = menu
        self.state = self.init_state(state)
        self.bounds = pygame.rect.Rect(position[0], position[1], params[0], params[1])
        self.position = position
        self.text = TextObject(
            position, lambda: text, c.button_text_color, c.font_name, c.font_size, params, centralized=True
        )
        self.params = params
        self.prev = None
        self.next = None

    def get_normal_state(self):
        return NormalState(self)

    def get_hover_state(self):
        return HoverState(self)

    def get_pressed_state(self):
        return PressedState(self)

    def get_current_state(self):
        return CurrentButtonState(self)

    def set_state(self, state: AbstractButtonState):
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

    def init_state(self, state: str):
        return dict(
            normal=NormalState(self),
            hover=HoverState(self),
            pressed=PressedState(self),
            current=CurrentButtonState(self),
        )[state]

    def next_button(self):
        self.state.next_button()

    def prev_button(self):
        self.state.prev_button()

    @property
    def is_current(self) -> bool:
        return self.state.is_current()

    @abstractmethod
    def click(self, state: AbstractGameSessionState):
        pass

    # def _get_surface(self, text):
    #     text_surface = self.font.render(text, False, self.color)
    #     return text_surface, text_surface.get_rect()


class QuitButton(Button):
    def click(self, state: AbstractGameSessionState):
        state.session.finish()


class PlayButton(Button):
    def click(self, state):
        pass


class AutoPlayButton(Button):
    def click(self, state):
        pass


class ContinueButton(Button):
    def click(self, state: AbstractGameSessionState):
        pass


class RestartButton(Button):
    def click(self, state: AbstractGameSessionState):
        pass


class HelpButton(Button):
    def click(self, state: AbstractGameSessionState):
        pass


class MainMenuButton(Button):
    def click(self, state: AbstractGameSessionState):
        pass


class NormalState(AbstractButtonState):
    def __init__(self, button: Button):
        self.color = c.button_normal_back_color
        super().__init__(button)

    def press(self):
        pass

    def hover(self):
        self.button.set_state(self.button.get_hover_state())
        self.button.menu.remove_current_button()
        self.button.menu.current_button = self.button.menu.buttons.index(self.button)

    def remove(self):
        pass

    def free(self):
        pass

    def remove_current(self):
        pass

    def press_return(self):
        pass

    def next_button(self):
        pass

    def prev_button(self):
        pass

    def is_current(self) -> bool:
        return False


class HoverState(AbstractButtonState):
    def __init__(self, button: Button):
        self.color = c.button_hover_back_color
        super(HoverState, self).__init__(button)

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

    def next_button(self):
        pass

    def prev_button(self):
        pass

    def is_current(self) -> bool:
        return False


class PressedState(AbstractButtonState):
    def __init__(self, button: Button):
        self.color = c.button_pressed_back_color
        super(PressedState, self).__init__(button)

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

    def next_button(self):
        self.button.set_state(self.button.get_normal_state())
        self.button.next.set_state(self.button.next.get_current_state())

    def prev_button(self):
        self.button.set_state(self.button.get_normal_state())
        self.button.prev.set_state(self.button.prev.get_current_state())

    def is_current(self) -> bool:
        return True


class CurrentButtonState(AbstractButtonState):
    def __init__(self, button: Button):
        self.color = c.button_hover_back_color
        super(CurrentButtonState, self).__init__(button)

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

    def next_button(self):
        self.button.set_state(self.button.get_normal_state())
        self.button.next.set_state(self.button.next.get_current_state())

    def prev_button(self):
        self.button.set_state(self.button.get_normal_state())
        self.button.prev.set_state(self.button.prev.get_current_state())

    def is_current(self) -> bool:
        return True
