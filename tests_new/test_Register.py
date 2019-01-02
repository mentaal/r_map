import r_map
import random
from operator import ior, or_
from functools import reduce

def test_reg_inst(reg):
    for bf_ref in reg:
        bf = bf_ref.bf
        assert bf.mask == (1 << bf.width) - 1

    new_val = random.randint(0, 0xFFFFFFFFFF)
    new_val_mask = (1 << (bf1.width+bf2.width)) - 1
    reg.value = new_val
    exp = new_val & new_val_mask
    assert reg.value == exp, f"Expected reg.value=={exp:#010x}, got:{reg.value:#010x}"
    reg.reset()
    assert reg.value == (bf1.reset_val << bf1_ref.reg_offset) |\
                        (bf2.reset_val << bf2_ref.reg_offset)

    assert reg.bf1_ref.bf1.value == bf1.reset_val

def test_reg_reset(reg):
    """Ensure that a register's reset value matches the sum of its child
    BitFieldRef's reset values"""
    new_val = random.randint(0, 0xFFFFFFFFFF)
    reg.value = new_val
    reg.reset()
    expected_reset_val = reduce(or_, (r.value for r in reg))
    assert reg.value == expected_reset_val


def test_reg_copy():
    root = r_map.Node(name='root')
    reg1 = get_reg(root)

    print(f"reg1.bf1_ref.bf1: {reg1.bf1_ref.bf1!r}")
    reg2 = reg1._copy(parent=root, name='reg2')
    print("Children in reg2:")
    for c in reg2:
        print(repr(c))

    assert reg1.bf1_ref is not reg2.bf1_ref
    assert reg1.bf1_ref.bf1 is not reg2.bf1_ref.bf1

def test_reg_alias():
    root = r_map.Node(name='root')
    reg1 = get_reg(root)

    print(f"reg1.bf1_ref.bf1: {reg1.bf1_ref.bf1!r}")
    reg2 = reg1._copy(parent=root, name='reg2', alias=True)
    print("Children in reg2:")
    for c in reg2:
        print(repr(c))

    assert reg1.bf1_ref is not reg2.bf1_ref
    assert reg1.bf1_ref.bf1 is reg2.bf1_ref.bf1

