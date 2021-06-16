from abc import ABCMeta, abstractmethod


class AbstractState(metaclass=ABCMeta):#TODO
    @abstractmethod
    def draw(self, display):
        pass

    @abstractmethod
    def handle_esc(self):
        pass

    @abstractmethod
    def get_chain(self):
        pass

    @abstractmethod
    def handle_mouse_move(self, pos):
        pass

    @abstractmethod
    def handle_mouse_down(self, pos):
        pass

    @abstractmethod
    def handle_mouse_up(self):
        pass

    @abstractmethod
    def handle_key_up(self):
        pass

    @abstractmethod
    def handle_key_down(self):
        pass

    @abstractmethod
    def handle_key_left(self):
        pass

    @abstractmethod
    def handle_key_right(self):
        pass
