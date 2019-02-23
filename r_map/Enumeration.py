from .Node import Node
from .ValueNodeMixins import UnsignedValueNodeMixin
import r_map

class Enumeration(UnsignedValueNodeMixin, Node):
    _nb_attrs = frozenset(['value',])

    __hash__ = Node.__hash__

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return super().__str__() + ' value: {}'.format(self.value)

    def __eq__(self, other):
        if isinstance(other, (Enumeration,  r_map.BitField)):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (Enumeration,  r_map.BitField)):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, (Enumeration, r_map.BitField)):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, (Enumeration, r_map.BitField)):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, (Enumeration, r_map.BitField)):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        else:
            return NotImplemented

