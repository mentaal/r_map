from math import ceil
from functools import reduce
from operator import ior, attrgetter
import r_map
from .AddressedNode import AddressedNode
from .ValueNodeMixins import UnsignedValueNodeMixin
from .ValidationError import ValidationError
from .Node import Node

class Register(UnsignedValueNodeMixin, AddressedNode):
    _nb_attrs = frozenset(['width'])
    def __init__(self, *, width=32, **kwargs):
        super().__init__(width=width, **kwargs)

    def reset(self):
        for f in self:
            f._bf.reset()

    def __str__(self):
        return super().__str__() + f' value: {self.value:#0{ceil(self.width/4)+2}x}'

    @property
    def access(self):
        return '|'.join(sorted(set(o.bf.access for o in self)))

    @property
    def value(self):
        return reduce(ior, (f.value for f in self), 0)

    @value.setter
    def value(self, x):
        for f in self:
            f.value = x

    @property
    def reset_val(self):
        return reduce(ior, (f.reset_val for f in self))

    def validate(self):
        yield from super().validate()
        continue_checks = True
        num_bitfieldrefs = len(self)
        if num_bitfieldrefs == 0:
            yield ValidationError(self, "No bitfieldrefs present")

        for c in self:
            if not isinstance(c, r_map.BitFieldRef):
                continue_checks = False
                yield ValidationError(self, f"Child object: {c!s} is not of type"
                        f"BitFieldRef, it's of type: {type(c)}")
        if continue_checks:
            if num_bitfieldrefs > 1:
                #check for overlapping bitfieldrefs
                first, *remaining = list(self)
                for second in remaining:
                    if second.reg_offset < first.reg_offset + first.slice_width:
                        yield ValidationError(self,
                                f"{second!s} overlaps with {first!s}")
                    first = second

    def read(self) -> int:
        val = self._reg_read_ex_func(self)
        self.value = val
        #Intentionally return val here and not self.value
        #User may wish to inspect the value of otherwise reserved or unspecified
        #bit fields
        return val

    def write(self, val=None):
        if val is None:
            val = self.value
        else:
            self.value = val
        self._reg_write_ex_func(self, val)

    def __iter__(self):
        children = list(Node.__iter__(self))
        if any(not hasattr(c, 'reg_offset') for c in children):
            return (s for s in children)
        else:
            return (s for s in sorted(children, key=attrgetter('reg_offset')))

    def __setattr__(self, key, value):
        """Used to simply register value assignment
        Behaves similarly to the __setattr__ method defined in Node but with
        the difference that when the user assignes to a register, like this:
            reg.bf_ref = 0x5,
        they most likely mean reg.bf_ref.bf.value so this method does the most
        intuitive
        """
        if '_children' in self.__dict__ and\
           key in self.__dict__['_children'] and\
           isinstance(value, int) and\
           hasattr(self.__dict__['_children'][key], 'bf'):
               getattr(self, key).bf.value = value
        else:
            super().__setattr__(key, value)

    def __eq__(self, other):
        if isinstance(other, Register):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Register):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Register):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Register):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Register):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        else:
            return NotImplemented
