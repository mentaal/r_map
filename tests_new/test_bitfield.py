import pytest
import r_map

def test_bf_reset_on_creation(bf):
    assert bf.value == bf.reset_val

def test_bf_contains_enum(bf):
    enum2 = bf.enum2
    assert enum2 in bf

def test_bf_annotation(bf):
    enum2 = bf.enum2
    bf.value = enum2
    assert 'enum2' == bf.annotation

def test_bf_assign_enum(bf):
    enum1 = bf.enum1
    bf.value = enum1
    assert bf.value == enum1.value

def test_bf_reflected_equality(bf):
    enum1 = bf.enum1
    bf.value = enum1
    assert enum1 == bf
    assert bf == enum1

def test_assignment_by_enumeration_name(bf):
    bf.value = 'enum2'
    assert bf.value == bf.enum2

def test_non_enum_string_assigment_fails(bf):
    with pytest.raises(ValueError) as e:
        bf.value = "this string isn't an enumeration name"
    print(e)

def test_value_assignment_width_aware(bf):
    bf.value = 0x123
    assert bf.value == 0x23 #value assignment is width aware

def test_default_hex_string_annotation(bf):
    bf.value = 0x23
    assert bf.annotation == hex(0x23)

def test_bitfield_reset(bf):
    bf.value = 0x123
    bf.reset()
    assert bf.reset_val == bf.value

def test_bitfield_same_enum_value_validation(bf):
    bf.enum2.value = bf.enum1.value
    errors = list(bf.validate())
    assert len(errors) == 1
    print(errors[0])

def test_bf_serialization(bf):
    primitive = r_map.dump(bf)
    bf2 = r_map.load(primitive)
    assert len(bf2) == len(bf)


    attrs = next(iter(bf))._nb_attrs - set(['parent'])
    for c in bf:
        for a in attrs:
            assert getattr(c, a) == getattr(bf2[c.name], a)


