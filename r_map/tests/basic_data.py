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
    bf1_ref = BitFieldRef(name='bf1_ref', parent=reg1, slice_width=6,
                          field_offset=7, reg_offset=8)
    bf1 = BitField(name='bf1', parent=bf1_ref, width=20, reset=0x12345,
            access='RW', doc="Some documentation to describe the bitfield")
    enum1 = Enumeration(name='use_auto_inc', value=20, parent=bf1)
    enum2 = Enumeration(name='use_auto_dec', value=10, parent=bf1)

    reg2 = Register(name='reg2', parent=r_map1, local_address=0x4)
    bf2_ref = BitFieldRef(name='bf2_ref', parent=reg2, slice_width=4,
                          field_offset=3, reg_offset=4)
    bf2_ref.bf = bf1

    bf3_ref = BitFieldRef(name='bf3_ref', parent=reg2, slice_width=5,
                          field_offset=2, reg_offset=5)
    bf2 = BitField(name='bf2', parent=bf3_ref, width=20, reset=0x6789, access='R')
    bf4_ref = BitFieldRef(name='bf4_ref', parent=reg2, slice_width=2,
                          field_offset=0, reg_offset=0)
    bf4_ref._add(bf2)

    return root


