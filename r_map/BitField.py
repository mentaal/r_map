from math import ceil
from .Node import Node
class BitField(Node):
    _nb_attrs = ('width', 'reset', 'access')
    def __init__(self, width=1, reset=0, access='XX', **kwargs):
        super().__init__(width=width, reset=reset, access=access, **kwargs)
        self.value = self.reset
        if width < 1:
            raise ValueError("Width needs to be >= 1")

    def __str__(self):
        return super().__str__() + ' width: {}, reset: {:#0{width}x}, value: {:#0{width}x}'.format(
                self.width,
                self.reset,
                self.value,
                width=ceil(self.width/4+2)) #+2 to account for the "0x"

    @property
    def annotation(self):
        return next((a.name for a in self if a.value == self.value), hex(self.value))

    #TODO: add a property to handle safely setting the value (appropriately mask)

    #TODO: add __eq__ and __req__ to check for equality against an enumeration
    #string or a value
    #Should I? does this make sense to do? Maybe it would make more sense to
    #check if the bitfield's other fiels are matching....

