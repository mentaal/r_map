from r_map import BitField, Register, RegisterMap, Enumeration, BitFieldRef, Node


def get_basic_data():

    root = Node(name='root')

    r_map1 = RegisterMap(name='r_map1', local_address=0x10000000,
            descr="An example register map containing registers")
    root._add(r_map1)
    reg1 = Register(name='reg1', local_address=0x0)
    r_map1._add(reg1)
    bf1_ref = BitFieldRef(name='bf1_ref', slice_width=6,
                          field_offset=7, reg_offset=8)
    reg1._add(bf1_ref)
    bf1 = BitField(name='bf1', width=20, reset_val=0x12345,
            access='RW', doc="Some documentation to describe the bitfield")
    bf1_ref._add(bf1)
    enum1 = Enumeration(name='use_auto_inc', value=20)
    enum2 = Enumeration(name='use_auto_dec', value=10)
    for e in enum1,enum2:
        bf1._add(e)

    reg2 = Register(name='reg2', local_address=0x4)
    r_map1._add(reg2)
    bf2_ref = BitFieldRef(name='bf2_ref', slice_width=4,
                          field_offset=3, reg_offset=4)
    reg2._add(bf2_ref)
    bf2_ref._add(bf1)

    bf3_ref = BitFieldRef(name='bf3_ref', slice_width=5,
                          field_offset=2, reg_offset=5)
    reg2._add(bf3_ref)
    bf2 = BitField(name='bf2', width=20, reset_val=0x6789, access='R')
    bf3_ref._add(bf2)
    bf4_ref = BitFieldRef(name='bf4_ref', slice_width=2,
                          field_offset=0, reg_offset=0)
    reg2._add(bf4_ref)
    bf4_ref._add(bf2)

    return root


