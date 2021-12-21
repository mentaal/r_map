import random
from operator import or_
from functools import reduce, partial
import r_map
from r_map import Register, BitFieldRef, BitField, ArrayedNode

def make_arrayed_reg():
    bf_base = BitField(name='scratch', width=8)
    bf_ref = BitFieldRef(name='scratch_ref', reg_offset=0)
    bf_ref._add(bf_base)
    scratch_base = Register(name='scratch_reg', width=8, local_address=0)
    scratch_base._add(bf_ref)

    arrayed = ArrayedNode(name='scratch[n]', end_index=256, base_node=scratch_base)
    return arrayed

def test_scratch():
    arrayed = make_arrayed_reg()
    assert 'scratch0' in arrayed
    assert 'scratch10' in arrayed
    assert 'scratch250' in arrayed
    assert 'scratch256' not in arrayed
    assert arrayed.scratch255 in arrayed
    assert arrayed['scratch12'] in arrayed

