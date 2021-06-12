__all__ = ["Engine"]


class Engine:
    game_over = False
    show_menu = True
    objects = []
    menu_objects = []
    current_button = None



    def subscribe_button(self, obj):
        self.menu_objects.append(obj)

    def unsubscribe_button(self, obj):
        if obj in self.menu_objects:
            self.menu_objects.remove(obj)

    def handle_mouse_move(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                if obj.state != 'pressed':
                    self.current_button = self.menu_objects.index(obj)
                    obj.state = 'hover'
            else:
                if obj is not self.menu_objects[self.current_button]:
                    obj.state = 'normal'

    def handle_mouse_down(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.state = 'pressed'

    def handle_mouse_up(self):
        for obj in self.menu_objects:
            if obj.state == 'pressed':
                obj.click(self)
                obj.state = 'hover'

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
