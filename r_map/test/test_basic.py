def test_get_data(basic_data):
    root = basic_data

    print(root)

    bf = root.r_map1.reg1.bf1_ref.bf
    bf.value = 0x12345

    bf_value = bf.value
    for ref in bf:
        ref_view = (bf_value >> ref.field_offset) & ref.slice_width
        ref_view <<= ref.reg_offset
        assert ref.value == bf1_view

    for item in root._walk(top_down=True):
        print(item)

def test_contains(basic_data):
    """assert contains works as expected"""

    assert 'reg1' in basic_data.r_map1

    reg1 = basic_data.r_map1.reg1

    assert reg1 in basic_data.r_map1

def test_deep_copy(basic_data):

    root = basic_data
    r_map1 = root.r_map1
    r_map2 = r_map1._copy(parent=root, local_address=0x20000000)

    assert r_map1.name == r_map2.name
    assert r_map1.address != r_map2.address
    assert r_map2.local_address == 0x20000000

    assert r_map1.reg1 is not r_map2.reg1

    for item in r_map2._walk(top_down=True):
        print(item)

