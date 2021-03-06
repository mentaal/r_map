import json
import r_map
import random

def test_bitfield_0_slice_width():
    width = 5
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, slice_width=0)
    bf = r_map.BitField(name='bf', width=width, reset_val=0x15)
    bf1_ref._add(bf)

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

def test_reg_with_arrayed_bf_ref():
    reg = r_map.Register(name='a_reg', local_address=0)
    bf = r_map.BitField(name='a_bf', width=1)
    bf_ref = r_map.BitFieldRef(name='a_bf_ref', reg_offset=0)
    bf_ref._add(bf)

    arrayed_bf = r_map.ArrayedNode(
            name='irq_[n]',
            start_index=0,
            incr_index=1,
            descr='irq for pin [n]',
            end_index=12,
            increment=0x1,
            base_val=0,
            base_node=bf_ref)
    reg._add(arrayed_bf)

    val = 0x235
    reg.value = val
    assert reg.value == val

    for i in range(12):
        assert arrayed_bf[i].value == val&(1<<i)

def test_array_bf_serialization():
    reg = r_map.Register(name='a_reg', local_address=0)
    bf_ref = r_map.BitFieldRef(name='a_bf_ref', reg_offset=0)
    bf = r_map.BitField(name='a_bf', width=1)
    bf_ref._add(bf)

    arrayed_bf = r_map.ArrayedNode(
            name='irq_[n]',
            start_index=0,
            incr_index=1,
            descr='irq for pin [n]',
            end_index=12,
            increment=0x1,
            base_val=0,
            base_node=bf_ref)
    reg._add(arrayed_bf)

    reg.value = 0x12
    assert reg.value == 0x12

    reg_primitive = r_map.dump(reg)
    print(reg_primitive)
    #print(json.dumps(reg_primitive, indent='\t'))
    reg2 = r_map.load(reg_primitive)

    val = 0x235
    reg2.value = val
    assert reg2.value == val

    arrayed_bf = reg2['irq']
    for i in range(12):
        assert arrayed_bf[i].value == val&(1<<i)


def test_copied_and_aliased_bitfield(bf):
    """Ensure that copies can be made of bitfields without having them become
    aliases
    """
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, slice_width=0)
    bf1_ref._add(bf)
    for _ in range(10):
        copy = bf1_ref._copy()
        assert not copy._alias, "BitFieldRef copy is an alias but it shouldn't be"
    assert len(bf._references) == 1, "BitField has multiple references but it shouldn't"

def test_automatic_alias(bf):
    """Ensure that adding a bitfield to a bitfieldref automatically turns
    bitfieldref into an alias
    """
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, slice_width=0)
    bf1_ref_copy = r_map.BitFieldRef(name='bf1_ref_copy', reg_offset=0, slice_width=0)
    bf1_ref._add(bf)
    bf1_ref_copy._add(bf)
    assert bf1_ref_copy._alias, "bf1_ref_copy should be an alias but isn't"

def test_spanned_bitfield_deep_copy(bf):
    """Ensure that deep copying a node maintains the integrity of spanned
    bitfields
    """
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, slice_width=4)
    bf1_ref._add(bf)
    bf1_ref2 = r_map.BitFieldRef(name='bf1_ref2', reg_offset=0, slice_width=4,
                                 field_offset=4)
    bf1_ref2._add(bf)

    assert bf1_ref.bf is bf1_ref2.bf

    root = r_map.Node(name='root')
    root._add(bf1_ref)
    root._add(bf1_ref2)


    root_copy = root._copy()

    assert root_copy.bf1_ref.bf is root_copy.bf1_ref2.bf
