__all__ = ["ShowMenuGameSessionState", "GameSession"]

from typing import Callable

import pygame
from application.game_session.base_game_session_state import AbstractGameSessionState
from application.models import Menus
from application.screen_chain import ScreenHandler


class GameSession:
    def __init__(self, menu_chain: ScreenHandler, menus: Menus):
        self.show_menu_state = ShowMenuGameSessionState(self, menu_chain)
        # self.on_play_state = OnPlayGameSessionState()
        self.state: AbstractGameSessionState = self.show_menu_state
        self.menus = menus
        self.end = False

    def handle_mouse(self, key: str, pos: tuple[int]):
        self.state.handle_mouse(key, pos)

    def handle_keyboard_key(self, key: str, status: str):
        self.state.handle_keyboard_key(key, status)

    def set_state(self, state: AbstractGameSessionState):
        self.state = state

    def get_show_menu_state(self):
        return self.show_menu_state

    # def get_on_play_state(self):
    #     return self.on_play_state

    def finish(self) -> None:
        self.end = True


class ShowMenuGameSessionState(AbstractGameSessionState):
    def __init__(self, session: GameSession, chain: ScreenHandler):
        self._chain = chain
        self.mouse_dict: dict[str, Callable[[tuple[int]], None]] = {
            "mouse_motion": self.handle_mouse_move,
            "mouse_button_down": self.handle_mouse_down,
            "mouse_button_up": self.handle_mouse_up,
        }
        self.key_dict = {
            "key_return": self.handle_return,
            "key_esc": self.handle_esc,
            "key_down": self.handle_key_down,
            "key_up": self.handle_key_up,
        }
        super(ShowMenuGameSessionState, self).__init__(session)

    def handle_keyboard_key(self, key: str, status: str):
        self.key_dict.get(key, lambda x: None)(status)

    def handle_mouse(self, key: str, pos: tuple[int]):
        self.mouse_dict[key](pos)

    def handle_return(self, status: str):
        if status == "up":
            self.session.menus.current_buttons[self.session.menus.current_button].click(self)
            self.session.menus.current_buttons[self.session.menus.current_button].free()
        elif status == "down":
            self.session.menus.current_buttons[self.session.menus.current_button].press_return()

    def draw(self, display: pygame.Surface):
        self._chain.draw(display)

    def get_chain(self):
        return self._chain

    def handle_esc(self, status: str):
        if status == "up":
            self.session.finish()

    def handle_mouse_move(self, pos):
        for obj in self.session.menus.current_buttons:
            if obj.bounds.collidepoint(pos):
                obj.hover()
                self.session.menus.remove_current_button()
            else:
                obj.remove()

    def handle_mouse_down(self, pos: tuple[int]):
        for obj in self.session.menus.current_buttons:
            if obj.bounds.collidepoint(pos):
                obj.press()

    def handle_mouse_up(self, pos: tuple[int]):
        for obj in self.session.menus.current_buttons:
            obj.free()

    def handle_key_up(self, status: str):
        length = len(self.session.menus.current_buttons)
        if status == "down":
            prev = (self.session.menus.current_button - 1) % length
            obj = self.session.menus.current_buttons[self.session.menus.current_button]
            obj.remove()
            obj.remove_current()
            self.session.menus.current_buttons[prev].hover()
            self.session.menus.current_button = prev

    def handle_key_down(self, status: str):
        length = len(self.session.menus.current_buttons)
        if status == "down":
            next_ = (self.session.menus.current_button + 1) % length
            obj = self.session.menus.current_buttons[self.session.menus.current_button]
            obj.remove()
            obj.remove_current()
            self.session.menus.current_buttons[next_].hover()
            self.session.menus.current_button = next_


# class OnPlayGameSessionState(AbstractGameSessionState):
#     state = "OnPlay"
#
#     def draw(self, display: pygame.Surface):
#         pass
#
#     def handle_mouse(self, key: str, pos):
#         pass
#
#     def handle_keyboard_key(self, key: str, status: str):
#         pass
