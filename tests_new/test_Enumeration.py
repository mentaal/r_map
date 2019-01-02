import r_map
def test_enumeration_inst():
    enum1 = r_map.Enumeration(name='enum1', value=1)
    enum2 = r_map.Enumeration(name='enum2', value=2)
    enum3 = r_map.Enumeration(name='enum3', value=1)

    assert enum1 != enum2
    assert enum1 == enum3
    assert enum1 < enum2
    assert enum1 < 2
    assert enum2 >= enum1
    assert enum2 >= 1
    assert enum2 > enum1
    assert enum1 != 'enum1'


