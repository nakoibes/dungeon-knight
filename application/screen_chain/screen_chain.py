import pygame

#from application.engine import Engine

__all__ = ["ScreenHandle", "MenuHandler"]


class ScreenHandle(pygame.Surface):
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

    def connect_engine(self, engine):
        if self.successor is not None:
            self.successor.connect_engine(engine)


class MenuHandler(ScreenHandle):
    def __init__(self, *args, **kwargs):
        self.menus = args[-3]
        args = args[:-3] + args[-2:]
        super().__init__(*args, **kwargs)

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw_background(self):
        self.blit(self.menus.img, (0, 0))

    def draw_buttons(self):
        for obj in self.menus.main_menu_objects:
            pygame.draw.rect(self, obj.back_color, (obj.position[0], obj.position[1], obj.params[0], obj.params[1]))
            self.blit(obj.text.text_surface, obj.text.position)

    def draw(self, canvas: pygame.Surface):
        self.draw_background()
        self.draw_buttons()

        super().draw(canvas)
