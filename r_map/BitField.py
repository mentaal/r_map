from .Node import Node
class BitField(Node):
    _nb_attrs = ('width', 'position', 'reset', 'access')
    def __init__(self, width=1, position=0, reset=0, access='XX', **kwargs):
        super().__init__(width=width, position=position, reset=reset,
                access=access, **kwargs)
        self.field_mask = (1 << width)-1
        self.register_mask = ((1<<width)-1) << position
        self._value = self.reset
        if width < 1:
            raise ValueError("Width needs to be >= 1")

    def __str__(self):
        return super().__str__() + ' width: {}, position: {}, reset: {:#x}, value: {}'.format(
                self.width, self.position, self.reset, self.annotation)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value & ((1<<self.width)-1)

    @property
    def annotation(self):
        return next((a.name for a in self if a.value == self.value), hex(self.value))

