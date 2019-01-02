import r_map

def test_bitfield_creation():
    reset = 0x5c
    width = 8
    bf = r_map.BitField(name='bf1', width=width, reset_val=reset)
    assert bf.value == reset
    enum1 = r_map.Enumeration(parent=bf, name='enum1', value=1)
    enum2 = r_map.Enumeration(parent=bf, name='enum2', value=2)
    enum3 = r_map.Enumeration(parent=bf, name='enum3', value=1)
    assert enum2 in bf

    bf.value = enum1
    assert bf.value == enum1.value

    bf.value = 'enum2'
    assert bf.value == enum2.value
    assert bf.annotation == 'enum2'

    bf.value = 0x123
    assert bf.value == 0x23 #value assignment is width aware
    assert bf.annotation == hex(0x23)

    bf.reset()
    assert bf.value == reset


