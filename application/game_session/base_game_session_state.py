from abc import ABCMeta, abstractmethod


class AbstractGameSessionState(metaclass=ABCMeta):
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def draw(self, display):
        pass

    @abstractmethod
    def handle_keyboard_key(self, key, status):
        pass

    @abstractmethod
    def handle_mouse(self, key, pos):
        pass

    @abstractmethod
    def get_chain(self):
        pass
