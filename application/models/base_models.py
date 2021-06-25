from abc import ABCMeta, abstractmethod


class AbstractButtonState(metaclass=ABCMeta):
    def __init__(self, button):
        self.button = button

    @abstractmethod
    def press(self):
        pass

    @abstractmethod
    def hover(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def free(self):
        pass

    @abstractmethod
    def remove_current(self):
        pass

    @abstractmethod
    def press_return(self):
        pass

    @abstractmethod
    def next_button(self):
        pass

    @abstractmethod
    def prev_button(self):
        pass

    @abstractmethod
    def is_current(self) -> bool:
        pass


class AbstractMenu(metaclass=ABCMeta):
    @abstractmethod
    def create_menu(self, session):
        pass

    @abstractmethod
    def create_background(self):
        pass
