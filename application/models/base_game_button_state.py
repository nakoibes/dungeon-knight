from abc import ABCMeta, abstractmethod


class AbstractButtonState(metaclass=ABCMeta):
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

    # @abstractmethod
    # def keyboard_down(self):
    #     pass
    # @abstractmethod
    # def keyboard_up(self):
    #     pass

    @abstractmethod
    def press_return(self):
        pass