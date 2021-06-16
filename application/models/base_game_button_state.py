from abc import ABCMeta, abstractmethod


class AbstractButtonState(metaclass=ABCMeta):
    def press(self):
        pass

    def hover(self):
        pass
