from .Node import Node
class BitField(Node):
    _nb_attrs = ('width', 'position', 'reset')
    def __init__(self, *args, width=32, position=0, reset=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.width    = width
        self.position = position
        self.reset    = reset

    def __str__(self):
        return super().__str__() + ' width: {}, position: {}, reset: {:#x}'.format(
                self.width, self.position, self.reset)


