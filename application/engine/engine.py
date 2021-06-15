__all__ = ["Engine"]

from application.models.buttons import Button


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
                    obj.set_hover_state()
            else:
                if obj is not self.menu_objects[self.current_button]:
                    obj.set_normal_state()

    def handle_mouse_down(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.set_pressed_state()

    def handle_mouse_up(self):
        for obj in self.menu_objects:
            if obj.state == "pressed":
                obj.click(self)
                obj.set_hover_state()

    def prev_menu_button(self):
        self.current_button = (self.current_button - 1) % len(self.menu_objects)
        for obj in self.menu_objects:
            if obj is self.menu_objects[self.current_button]:
                obj.set_hover_state()
            else:
                obj.set_normal_state()

    def next_menu_button(self):
        self.current_button = (self.current_button + 1) % len(self.menu_objects)
        for obj in self.menu_objects:
            if obj is self.menu_objects[self.current_button]:
                obj.set_hover_state()
            else:
                obj.set_normal_state()
