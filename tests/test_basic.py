import pytest
import r_map

def test_BitField_creation():
    bf = r_map.BitField(name='bf1')

def test_get_data(basic_data):
    root = basic_data

    print(root)

    bf = root.r_map1.reg1.bf1_ref.bf
    bf.value = 0x12345
    print(f"bf now: {bf}")
    assert bf.value == 0x12345 & ((1 << bf.width) - 1)

    bf_value = bf.value
    print(f"bf_value == {bf_value:#0x}")
    for ref in bf._references.values():
        ref_view = (bf_value >> ref.field_offset) & ((1 << ref.slice_width) - 1)
        print(f"ref_view now: {ref_view}")
        ref_view <<= ref.reg_offset
        assert ref.value == ref_view

    for item in root._walk(top_down=True):
        print(item)

def test_BitFieldRef_value(basic_data):
    bf_ref = basic_data.r_map1.reg1.bf1_ref
    bf = bf_ref.bf

    val = 0xFFFF_FFFF
    bf.value = val

    assert bf.value == val & ((1 << bf.width)-1)

    print(f"bf width: {bf.width}, value: {bf.value}")

    assert bf_ref.value == ((bf.value << bf_ref.field_offset) & ((1 << bf_ref.slice_width)-1) << bf_ref.reg_offset)

def test_BitField_value(basic_data):
    bf_ref = basic_data.r_map1.reg1.bf1_ref
    bf = bf_ref.bf

    val = 0x33333333
    bf_ref.value = val

    old_bf_val = bf.value
    mask = (1 << bf_ref.slice_width) - 1

    old_bf_val &= ~(mask << bf_ref.field_offset)

    new_val = ((val >> bf_ref.reg_offset) & mask) << bf_ref.field_offset

    assert bf.value == new_val | old_bf_val

def test_contains(basic_data):
    """assert contains works as expected"""
    assert 'reg1' in basic_data.r_map1
    reg1 = basic_data.r_map1.reg1
    assert reg1 in basic_data.r_map1

def test_enumeration_setting(basic_data):
    root = basic_data._copy()
    reg1 = root.r_map1.reg1

    bf = reg1.bf1_ref.bf
    bf.value = 'use_auto_inc'

    assert bf.value == 20
    assert bf.value == bf['use_auto_inc'].value

    bf.value = 10
    bf.value = bf['use_auto_inc']

    assert bf.value == bf['use_auto_inc'].value
    assert bf.use_auto_inc > bf.use_auto_dec

    #test reflected equality
    assert bf.use_auto_inc == bf
    assert bf == bf.use_auto_inc

def test_deep_copy(basic_data):
    root = basic_data._copy()

    r_map1 = root.r_map1
    r_map2 = r_map1._copy(local_address=0x20000000)
    root._add(r_map2)

    assert r_map1.name == r_map2.name
    assert r_map1.address != r_map2.address
    assert r_map2.local_address == 0x20000000

    assert r_map1.reg1 is not r_map2.reg1

    for item in r_map2._walk(top_down=True):
        print(item)

def test_no_recursion_on_attribute_error(basic_data):
    #Expecting AttributeError on invalid name in obj
    with pytest.raises(AttributeError):
        basic_data.r_map1.reg1.bf1_ref.blah

def test_register_access(basic_data):
    reg = basic_data.r_map1.reg1
    print(f"Reg: {reg} access: {reg.access}")
