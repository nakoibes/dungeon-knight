from abc import ABCMeta, abstractmethod

# __all__ = ["Engine", "GameSession"]

from application.models.buttons import Button
from application.screen_chain import MenuHandler, ScreenHandle


class Engine:
    game_over = False
    show_menu = True
    menu_objects: list[Button] = []
    current_button = None

    def subscribe_button(self, obj):
        self.menu_objects.append(obj)

    def unsubscribe_button(self, obj):
        if obj in self.menu_objects:
            self.menu_objects.remove(obj)

    def handle_mouse_move(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                if obj.state != "pressed":
                    self.current_button = self.menu_objects.index(obj)
                    obj.state = "hover"
            else:
                if obj is not self.menu_objects[self.current_button]:
                    obj.state = "normal"

    def handle_mouse_down(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.state = "pressed"

    def handle_mouse_up(self):
        for obj in self.menu_objects:
            if obj.state == "pressed":
                obj.click(self)
                obj.state = "hover"

    def prev_menu_button(self):
        self.current_button = (self.current_button - 1) % len(self.menu_objects)
        for obj in self.menu_objects:
            if obj is self.menu_objects[self.current_button]:
                obj.state = "hover"
            else:
                obj.state = "normal"

    def next_menu_button(self):
        self.current_button = (self.current_button + 1) % len(self.menu_objects)
        for obj in self.menu_objects:
            if obj is self.menu_objects[self.current_button]:
                obj.state = "hover"
            else:
                obj.state = "normal"


class MouseHandler:
    pass


class KeyboardHandler:
    pass


class GameSession:
    def __init__(self, menu_chain,menus):
        self.show_menu_state = ShowMenuState(self, menu_chain)
        self.on_play_state = OnPlayState()
        self.game_over_state = GameOverState()
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
    def draw(self):
        pass

    @abstractmethod
    def handle_esc(self):
        pass


class ShowMenuState(AbstractState):
    state = "ShowMenu"

    def __init__(self, session, chain):
        self._chain = chain
        self.session = session

    def draw(self):
        self._chain.draw()

    def get_chain(self):
        return self._chain

    def handle_esc(self):
        self.session.set_state(self.session.get_game_over_state())

    def handle_mouse_move(self, pos):
        for obj in self.session.menus.main_menu_objects:
            if obj.bounds.collidepoint(pos):
                if obj.state != "pressed":
                    self.session.menus.current_button = self.session.menus.main_menu_objects.index(obj)
                    obj.state = "hover"
            else:
                if obj is not self.session.menus.main_menu_objects[self.session.menus.current_button]:
                    obj.state = "normal"
        # self._chain = MenuHandler(self._screen_resolution, pygame.SRCALPHA, self._menus, (0, 0), ScreenHandle((0, 0)))
    # def handle_menu(self, event):
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_UP:
    #             self._engine.prev_menu_button()
    #         elif event.key == pygame.K_DOWN:
    #             self._engine.next_menu_button()
    #         elif event.key == pygame.K_RETURN:
    #             self._engine.menu_objects[self._engine.current_button].state = "pressed"
    #     elif event.type == pygame.KEYUP:
    #         if event.key == pygame.K_RETURN:
    #             self._engine.menu_objects[self._engine.current_button].state = "hover"
    #             self._engine.menu_objects[self._engine.current_button].click(self._engine)


class OnPlayState(AbstractState):
    state = "OnPlay"

    # def __init__(self, chain):
    #     self._chain = chain

    def draw(self):
        pass


class GameOverState(AbstractState):
    state = "End"

    def draw(self):
        pass
