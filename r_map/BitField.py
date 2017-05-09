from .Node import Node
class BitField(Node):
    _nb_attrs = ('width', 'position', 'reset')
    def __init__(self, *args, width=32, position=0, reset=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.width    = width
        self.position = position
        self.reset    = reset
        self.field_mask = (1 << width)-1
        self.register_mask = ((1<<width)-1) << position

    def __str__(self):
        return super().__str__() + ' width: {}, position: {}, reset: {:#x}'.format(
                self.width, self.position, self.reset)

    @property
    def value(self):
        return (self.parent.value >> self.position) & self.field_mask
    @value.setter
    def value(self, new_value):
        v = self.parent.value & ~self.register_mask
        v |= (new_value << self.position)&self.register_mask
        self.parent.value = v



