from r_map.Node import Node

def test_derive_class_without_registration(data):
    print("Before redefing BitField...")
    for name, c in Node._class_registry.items():
        print(name, c)
    class BitField(Node):
        def __init__(self, *args, **kwargs):
            raise Exception("Shouldn't be any instantiations of this!")
    d =  dict(data._serialize())
    for name, c in Node._class_registry.items():
        print(name, c)

    #now deserialize it
    root = Node._deserialize(d)
