from abc import ABCMeta, abstractmethod


# __all__ = ["Engine", "GameSession"]


class GameSession:
    def __init__(self, menu_chain, menus):
        self.show_menu_state = ShowMenuState(self, menu_chain)
        self.on_play_state = OnPlayState()
        self.game_over_state = GameOverState(self)
        self.state = self.show_menu_state
        self.menus = menus

    def handle_esc(self):
        self.state.handle_esc()

    def set_state(self, state):
        self.state = state

    def get_show_menu_state(self):
        return self.show_menu_state

    def get_on_play_state(self):
        return self.on_play_state

    def get_game_over_state(self):
        return self.game_over_state


class AbstractState(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, display):
        pass

    @abstractmethod
    def handle_esc(self):
        pass


class ShowMenuState(AbstractState):
    state = "ShowMenu"

    def __init__(self, session, chain):
        self._chain = chain
        self.session = session

    def draw(self, display):
        self._chain.draw(display)

    def get_chain(self):
        return self._chain

    def handle_esc(self):
        self.session.set_state(self.session.get_game_over_state())

    def handle_mouse_move(self, pos):
        for obj in self.session.menus.main_menu_objects:
            if obj.bounds.collidepoint(pos):
                if obj.state != "pressed":
                    self.session.menus.current_button = self.session.menus.main_menu_objects.index(obj)
                    obj.set_hover_state()
            else:
                if obj is not self.session.menus.main_menu_objects[self.session.menus.current_button]:
                    obj.set_normal_state()

    def handle_mouse_down(self, pos):
        for obj in self.session.menus.main_menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.set_pressed_state()

    def handle_mouse_up(self):
        for obj in self.session.menus.main_menu_objects:
            if obj.state == "pressed":
                obj.click(self)
                obj.set_hover_state()

    def handle_key_up(self):
        self.session.menus.current_button = (self.session.menus.current_button - 1) % len(
            self.session.menus.main_menu_objects)
        for obj in self.session.menus.main_menu_objects:
            if obj is self.session.menus.main_menu_objects[self.session.menus.current_button]:
                obj.set_hover_state()
            else:
                obj.set_normal_state()

    def handle_key_down(self):
        self.session.menus.current_button = (self.session.menus.current_button + 1) % len(
            self.session.menus.main_menu_objects)
        for obj in self.session.menus.main_menu_objects:
            if obj is self.session.menus.main_menu_objects[self.session.menus.current_button]:
                obj.set_hover_state()
            else:
                obj.set_normal_state()


class OnPlayState(AbstractState):
    state = "OnPlay"

    # def __init__(self, chain):
    #     self._chain = chain

    def draw(self, display):
        pass

    def handle_esc(self):
        pass


class GameOverState(AbstractState):
    state = "End"

    def __init__(self, session):
        self._chain = None
        self.session = session

    def draw(self, display):
        pass

    def handle_esc(self):
        pass

    def get_chain(self):
        pass
