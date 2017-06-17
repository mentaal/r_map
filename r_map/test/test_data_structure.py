from copy import deepcopy
def test_get_item(data):
    "test the different ways that an item can be referenced"

    #key based lookup
    spi = data['spi']

    #attribute based
    cfg0 = spi.cfg0
    print('cfg: {}'.format(cfg0))
    field = spi.cfg0['bf0']
    field = spi.cfg0.bf0
    #field = spi.bf0
    print(field)

def test_list_node(data):
    "display the node's public attributes and the names of its children"
    print(dir(data))

def test_walk(data):
    "obtain an iterator from the root object and get the next item"
    i = iter(data)
    block = next(i)

    for item in block.walk(levels=3):
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

    v = 0x12345678
    r.value = v
    for bf in r:
        print("bitfield: ", bf)
        field_expected_value = (r.value >> bf.position) & bf.field_mask
        assert field_expected_value == bf.value

    new_value = 12345678
    for bf in r:
        bf.value = (new_value >> bf.position) & bf.field_mask
    assert r.value == new_value
