from copy import deepcopy
def test_get_item(data):

    spi = data['spi']

    cfg0 = spi.cfg0
    print('cfg: {}'.format(cfg0))
    field = spi.cfg0['bf0']
    field = spi.cfg0.bf0
    #field = spi.bf0

def test_list_node(data):
    print(dir(data))

def test_walk(data):
    i = iter(data)
    block = next(i)

    for item in block.walk(levels=3):
        print(item)

def test_copy(data):

    data2 = deepcopy(data)
