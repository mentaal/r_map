from .Node import Node
class BitField(Node):
    _nb_attrs = ('width', 'position', 'reset', 'access')
    def __init__(self, width=32, position=0, reset=0, access='XX', **kwargs):
        super().__init__(width=width, position=position, reset=reset,
                access=access, **kwargs)
        self.field_mask = (1 << width)-1
        self.register_mask = ((1<<width)-1) << position

    def __str__(self):
        return super().__str__() + ' width: {}, position: {}, reset: {:#x}, value: {}'.format(
                self.width, self.position, self.reset, self.annotation)

    @property
    def value(self):
        return (self.parent.value >> self.position) & self.field_mask
    @value.setter
    def value(self, new_value):
        v = self.parent.value & ~self.register_mask
        v |= (new_value << self.position)&self.register_mask
        self.parent.value = v

    @property
    def annotation(self):
        return next((a.name for a in self if a.value == self.value), hex(self.value))

