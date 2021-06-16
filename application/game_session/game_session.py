__all__ = ["ShowMenuGameSessionState", "OnPlayGameSessionState", "GameSession"]

from application.game_session.base_game_session_state import AbstractGameSessionState


class GameSession:
    def __init__(self, menu_chain, menus):
        self.show_menu_state = ShowMenuGameSessionState(self, menu_chain)
        self.on_play_state = OnPlayGameSessionState()
        self.state = self.show_menu_state
        self.menus = menus
        self.end = False

    def handle_mouse(self, key, pos):
        self.state.handle_mouse(key, pos)

    def handle_keyboard_key(self, key, status):
        self.state.handle_keyboard_key(key, status)

    def set_state(self, state):
        self.state = state

    def get_show_menu_state(self):
        return self.show_menu_state

    def get_on_play_state(self):
        return self.on_play_state

    def finish(self) -> None:
        self.end = True


class ShowMenuGameSessionState(AbstractGameSessionState):
    state = "ShowMenu"

    def __init__(self, session, chain):
        self._chain = chain
        self.session = session
        self.mouse_dict = {
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

    def handle_keyboard_key(self, key, status):
        self.key_dict.get(key, lambda x: None)(status)

    def handle_mouse(self, key, pos):
        self.mouse_dict.get(key)(pos)

    def handle_return(self, status):
        if status == "up":
            self.session.menus.main_menu_objects[self.session.menus.current_button].click(self)
            self.session.menus.main_menu_objects[self.session.menus.current_button].free()
        elif status == "down":
            self.session.menus.main_menu_objects[self.session.menus.current_button].press_return()

    def draw(self, display):
        self._chain.draw(display)

    def get_chain(self):
        return self._chain

    def handle_esc(self, status):
        if status == "up":
            self.session.finish()

    def handle_mouse_move(self, pos):
        for obj in self.session.menus.main_menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.hover()
                self.session.menus.remove_current_button()
            else:
                obj.remove()

    def handle_mouse_down(self, pos):
        for obj in self.session.menus.main_menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.press()

    def handle_mouse_up(self, pos):
        for obj in self.session.menus.main_menu_objects:
            obj.free()

    def handle_key_up(self, status):
        length = len(self.session.menus.main_menu_objects)
        if status == "down":
            prev = (self.session.menus.current_button - 1) % length
            obj = self.session.menus.main_menu_objects[self.session.menus.current_button]
            obj.remove()
            obj.remove_current()
            self.session.menus.main_menu_objects[prev].hover()
            self.session.menus.current_button = prev

    def handle_key_down(self, status):
        length = len(self.session.menus.main_menu_objects)
        if status == "down":
            next_ = (self.session.menus.current_button + 1) % length
            obj = self.session.menus.main_menu_objects[self.session.menus.current_button]
            obj.remove()
            obj.remove_current()
            self.session.menus.main_menu_objects[next_].hover()
            self.session.menus.current_button = next_


class OnPlayGameSessionState(AbstractGameSessionState):
    state = "OnPlay"

    def draw(self, display):
        pass

    def handle_mouse(self, key, pos):
        pass

    def handle_keyboard_key(self, key):
        pass
