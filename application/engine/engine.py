__all__ = ["Engine"]


class Engine:
    game_over = False
    show_menu = True
    objects = []
    menu_objects = set()

    def subscribe_button(self, obj):
        self.menu_objects.add(obj)

    def unsubscribe_button(self, obj):
        if obj in self.menu_objects:
            self.menu_objects.remove(obj)

    def handle_mouse_move(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                if obj.state != 'pressed':
                    obj.state = 'hover'
            else:
                obj.state = 'normal'

    def handle_mouse_down(self, pos):
        for obj in self.menu_objects:
            if obj.bounds.collidepoint(pos):
                obj.state = 'pressed'

    def handle_mouse_up(self):
        for obj in self.menu_objects:
            if obj.state == 'pressed':
                obj.on_click(self)
                obj.state = 'hover'

