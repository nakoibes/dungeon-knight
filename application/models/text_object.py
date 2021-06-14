import pygame

__all__ = ["TextObject"]


class TextObject:
    def __init__(self, position, text_func, color, font_name, font_size, back_size, centralized=False):
        self.text = text_func()
        self.back_size = back_size
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.text_surface, self.bounds = self._get_surface(text_func())
        self.position = self._set_position(position, centralized)

    def _set_position(self, position, centralized):
        if centralized:
            return (position[0] + (self.back_size[0] - self.bounds.width) // 2,
                    position[1] + (self.back_size[1] - self.bounds.height) // 2)
        return position

    def _get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()
