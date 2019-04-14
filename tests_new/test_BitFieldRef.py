import r_map
import random


def test_bitfield_0_slice_width():
    width = 5
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, slice_width=0)
    bf = r_map.BitField(name='bf', width=width, reset_val=0x15, parent=bf1_ref)

    assert bf1_ref.slice_width == bf.width, "bitfield reference slice width did"\
            "not automatically update to the width of the child's bitfield when"\
            "it was initially set to 0"

def test_arrayed_bitfieldref(bf_ref):
    arrayed_bf = r_map.ArrayedNode(
            name='irq_[n]',
            start_index=0,
            incr_index=1,
            descr='irq for pin [n]',
            end_index=12,
            increment=0x1,
            base_val=0,
            base_node=bf_ref)

    r = arrayed_bf[4]
    assert r.name == 'irq_4'
    assert r.reg_offset == 4
    r = arrayed_bf['irq_8']
    assert r.name == 'irq_8'
    assert r.reg_offset == 8
    assert r.descr == 'irq for pin 8'





