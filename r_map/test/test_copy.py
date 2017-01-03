import copy

def test_copy(data):
    c = copy.deepcopy(data)
    i = iter(data)
    n = next(i)


    print(dir(c))

    i = iter(c)
    item = next(i)
    print(item)
    print(item.parent)
