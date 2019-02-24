from math import ceil
from functools import reduce
from operator import ior
import r_map
from .AddressedNode import AddressedNode
from .ValueNodeMixins import UnsignedValueNodeMixin
from .ValidationError import ValidationError

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
                first, *remaining = sorted(self, key=lambda x:x.reg_offset)
                for second in remaining:
                    if second.reg_offset < first.reg_offset + first.slice_width:
                        yield ValidationError(self,
                                f"{second!s} overlaps with {first!s}")
                    first = second


