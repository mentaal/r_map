import r_map
import random


def test_bitfield_0_slice_width():
    width = 5
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, slice_width=0)
    bf = r_map.BitField(name='bf', width=width, reset_val=0x15, parent=bf1_ref)

    assert bf1_ref.slice_width == bf.width, "bitfield reference slice width did"\
            "not automatically update to the width of the child's bitfield when"\
            "it was initially set to 0"

