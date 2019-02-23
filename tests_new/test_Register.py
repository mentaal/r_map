import r_map
import random
from operator import or_
from functools import reduce, partial


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


