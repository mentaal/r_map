import random
from operator import or_
from functools import reduce, partial

import r_map


rand_int = partial(random.randint, 0, 0xFFFFFFFF)

def test_validate_reg(reg):
    errors = list(reg.validate())
    assert len(errors) == 0

def test_reg_apply_value(reg):
    "Test that the value's new value is set according to its children's widths"

    new_val = rand_int()
    new_val_mask = (1 << (reg.bf1_ref.slice_width+reg.bf2_ref.slice_width)) - 1
    reg.value = new_val
    exp = new_val & new_val_mask
    assert reg.value == exp, f"Expected reg.value=={exp:#010x}, got:{reg.value:#010x}"

def test_reg_reset(reg):
    """Ensure that a register's reset value matches the sum of its child
    BitFieldRef's reset values"""
    new_val = random.randint(0, 0xFFFFFFFFFF)
    reg.value = new_val
    reg.reset()
    expected_reset_val = reduce(or_, (r.value for r in reg))
    assert reg.value == expected_reset_val


def test_reg_copy(reg):
    root = r_map.Node(name='root')
    reg1 = reg

    print(f"reg1.bf1_ref.bf1: {reg1.bf1_ref.bf1!r}")
    reg2 = reg1._copy(parent=root, name='reg2')
    print("Children in reg2:")
    for c in reg2:
        print(repr(c))

    assert reg1.bf1_ref is not reg2.bf1_ref
    assert reg1.bf1_ref.bf1 is not reg2.bf1_ref.bf1

def test_reg_alias(reg):
    """test that when a register is made to be an alias of another, it  gets
    deep copied until the level of bitfieldref."""
    root = r_map.Node(name='root')
    reg1 = reg

    print(f"reg1.bf1_ref.bf1: {reg1.bf1_ref.bf1!r}")
    reg2 = reg1._copy(parent=root, name='reg2', alias=True)
    print("Children in reg2:")
    for c in reg2:
        print(repr(c))

    assert reg1.bf1_ref is not reg2.bf1_ref
    assert reg1.bf1_ref.bf1 is reg2.bf1_ref.bf1

def test_install_bitfield(reg, bf):
    """Check that children of registers need to be of type BitFieldRef and not
    BitField"""
    bf.parent = reg
    assert bf.parent == reg
    errors = list(reg.validate())
    assert len(errors) == 1
    assert 'is not of type' in errors[0].error

def test_validate_no_bitrefs_present():
    """Check that validation flags an error if no bitfieldrefs are present"""
    reg = r_map.Register(name='some_reg')
    errors = list(reg.validate())
    for error in errors:
        print(str(error))
    assert len(errors) == 1
    assert 'No bitfieldrefs present' in errors[0].error

def test_iterate_over_reg(reg):
    bfs = list(reg)
    assert len(bfs) == 2

def test_serialize_reg(reg):
    root = r_map.Node(name='root')
    reg_copy = reg._copy(name=reg.name+'_copy', alias=True)
    assert reg_copy.bf1_ref.bf1 is reg.bf1_ref.bf1
    assert reg.bf1_ref.reg_offset == 0
    root._add(reg)
    root._add(reg_copy)
    primitive = r_map.dump(root)
    assert reg.bf1_ref.reg_offset == 0
    print(primitive)
    root2 = r_map.load(primitive)
    assert root2.reg1.bf1_ref.bf1 is root2.reg1_copy.bf1_ref.bf1
    assert root2.reg1.bf2_ref.bf2 is root2.reg1_copy.bf2_ref.bf2
    assert root2.reg1.bf2_ref is not root2.reg1_copy.bf2_ref
    assert root2.reg1.bf2_ref.uuid != root2.reg1_copy.bf2_ref.uuid


def test_arrayed_register(reg):
    arrayed_reg = r_map.ArrayedNode(
            name='TX_FIFO[nn]_[n]',
            start_index=0,
            incr_index=4,
            descr='TX FIFO register [nn]',
            end_index=20*4,
            increment=0x4,
            base_val=0x100)
    arrayed_reg.base_node=reg

    r = arrayed_reg[4]
    assert r.name == 'TX_FIFO04_4'
    assert r.local_address == 0x104
    r = arrayed_reg['TX_FIFO08_8']
    assert r.name == 'TX_FIFO08_8'
    assert r.local_address == 0x108

    assert r.descr == 'TX FIFO register 08'



