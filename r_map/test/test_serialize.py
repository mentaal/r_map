from r_map.Node import Node
def test_serialize_to_dict(data):
    d =  dict(data._serialize())
    #print("Number of items: {}".format(len(d)))
    #for item in d.values():
    #    print('{} ({}) parent uuid: {}'.format(
    #        item['name'], item['class_type'], item['parent']))

    #now deserialize it
    root = Node.deserialize(d)

    d2 = dict(root._serialize())

    assert d == d2

    print("Test data has: {} elements".format(len(d2)))
