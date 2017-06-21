from .AddressedNode import AddressedNode
from math import ceil
class Register(AddressedNode):
    _nb_attrs = ('width', 'reset')
    def __init__(self, width=32, reset=0, **kwargs):
        super().__init__(width=width, reset=reset, **kwargs)
        self.value = reset

    @property
    def access(self):
        return '|'.join(sorted(set(o.access for o in self._children.values())))

    def __str__(self):
        return super().__str__() + ' value: {:#0{width}x}'.format(self.value,
                width=ceil(self.width/4))

