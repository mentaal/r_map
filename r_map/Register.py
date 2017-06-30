from .AddressedNode import AddressedNode
from math import ceil
from functools import reduce
from operator import ior
class Register(AddressedNode):
    _nb_attrs = ('width', 'reset')
    def __init__(self, width=32, reset=0, **kwargs):
        super().__init__(width=width, reset=reset, **kwargs)

    @property
    def access(self):
        return '|'.join(sorted(set(o.access for o in self._children.values())))

    @property
    def value(self):
        return reduce(ior, (f.value<<f.position for f in self))

    @value.setter
    def value(self, x):
        for f in self:
            f.value = x >> f.position


    def __str__(self):
        return super().__str__() + ' value: {:#0{width}x}'.format(self.value,
                width=ceil(self.width/4))

