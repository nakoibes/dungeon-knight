import pygame

__all__ = ["ScreenHandler", "MenuHandler"]


class ScreenHandler(pygame.Surface):
    def __init__(self, *args, **kwargs):
        self.engine = None
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)

    def draw(self, canvas: pygame.Surface):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class MenuHandler(ScreenHandler):
    def __init__(self, *args, **kwargs):
        self.menus = args[-3]
        args = args[:-3] + args[-2:]
        super().__init__(*args, **kwargs)

    def draw_background(self):
        self.blit(self.menus.state.img, (0, 0))

    def draw_buttons(self):
        for obj in self.menus.current_buttons:
            pygame.draw.rect(self, obj.state.color, (obj.position[0], obj.position[1], obj.params[0], obj.params[1]))
            self.blit(obj.text.text_surface, obj.text.position)

    def draw(self, canvas: pygame.Surface):
        self.draw_background()
        self.draw_buttons()

        super().draw(canvas)
