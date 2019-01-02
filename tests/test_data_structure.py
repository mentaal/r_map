from copy import deepcopy
def test_get_item(data):
    "test the different ways that an item can be referenced"

    #key based lookup
    spi = data['spi']

    #attribute based
    cfg0 = spi.cfg0
    print(f'cfg: {cfg0}')
    field = spi.cfg0['bf0']
    field = spi.cfg0.bf0.bf
    #field = spi.bf0
    print(field)
    print("Updating field value to spi_enabled")
    field.value = field.spi_enabled.value
    print(field)
    print(spi.cfg0.bf0)
    assert field.annotation == field.spi_enabled.name

    print(f'bf0 annotation: {field.annotation}')

def test_list_node(data):
    "display the node's public attributes and the names of its children"
    print(dir(data))

def test_walk(data):
    "obtain an iterator from the root object and get the next item"
    i = iter(data)
    block = next(i)

    for item in block._walk(levels=3):
        print(item)

def test_copy(data):
    c = deepcopy(data)
    i = iter(data)
    n = next(i)
    print(dir(c))
    i = iter(c)
    item = next(i)
    print(item)
    print(item.parent)

def test_repr(data):
    item = next(iter(data))

    print(repr(item))

def test_bad_name(data):
    assert data.name != data['name']
    assert data['name'] is data._children['name']


def test_bit_reg_linkage(data):
    #get first available register
    w = (m for m in data)
    m = next(w)
    rs = (r for r in m)
    r = next(rs)
    print("Register: ", r)

    print(f"Register access: {r.access}")

    v = 0x12345678
    r.value = v
    for ref in r:
        print("bitfield: ", ref.bf)
        field_expected_value = (r.value >> ref.reg_offset) & ref.bf.mask
        assert field_expected_value == ref.bf.value

    new_value = 12345678
    for ref in r:
        ref.bf.value = (new_value >> ref.reg_offset) & ref.bf.mask
    assert r.value == new_value
