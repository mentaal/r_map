from math import ceil
from .Node import Node
class BitField(Node):
    _nb_attrs = ('width', 'reset', 'access')
    def __init__(self, *, parent=None, width=1, reset=0, access='XX', **kwargs):
        self.references = set()
        super().__init__(parent=parent, width=width, reset=reset, access=access, **kwargs)
        self._value = self.reset
        if width < 1:
            raise ValueError("Width needs to be >= 1")

    def __str__(self):
        return super().__str__() + ' width: {}, reset: {:#0{width}x}, value: {:#0{width}x}'.format(
                self.width,
                self.reset,
                self.value,
                width=ceil(self.width/4+2)) #+2 to account for the "0x"

    def __getattr__(self, name):
        """Redefine this function to prevent infinite recursion. Recursion would
        otherwise result because this function would delegate to a BitFieldRef
        which is higher in the Register Map tree structure"""
        raise AttributeError(f"{self} doesn't contain: {name}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        if isinstance(x, str):
            for enumeration in self:
                if enumeration.name == x:
                    self._value = enumeration.value
                    return
            raise ValueError(f"{x} doesn't match any enumeration pertaining to bitfield: {self.name}")
        else:
            self._value = x & self.width

    @property
    def annotation(self):
        return next((a.name for a in self if a.value == self.value), hex(self.value))


    #TODO: add __eq__ and __req__ to check for equality against an enumeration
    #string or a value
    #Should I? does this make sense to do? Maybe it would make more sense to
    #check if the bitfield's other fiels are matching....

