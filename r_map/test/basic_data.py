from r_map.RMapFactory import RMapFactory

Register = RMapFactory.Register
BitField = RMapFactory.BitField
BitFieldRef = RMapFactory.BitFieldRef
Enumeration = RMapFactory.Enumeration
RegisterMap = RMapFactory.RegisterMap
Node = RMapFactory.Node

def get_basic_data():

    root = Node(name='root')

    r_map1 = RegisterMap(name='r_map1', parent=root, local_address=0x10000000,
            descr="An example register map containing registers")
    reg1 = Register(name='reg1', parent=r_map1, local_address=0x0)
    reg2 = Register(name='reg2', parent=r_map1, local_address=0x4)
    bf1_ref = BitFieldRef(name='bf1_ref', parent=reg1, slice_width=6,
                          field_offset=7, reg_offset=8)
    bf1 = BitField(name='bf1', parent=bf1_ref, width=20, reset=0x12345)
    bf2_ref = BitFieldRef(name='bf2_ref', parent=reg2, slice_width=4,
                          field_offset=3, reg_offset=4)
    bf2_ref.bf = bf1_ref.bf


    return root


