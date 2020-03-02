import pytest
import r_map

def get_bf(parent=None):
    reset = 0x5c
    width = 8
    bf = r_map.BitField(name='bf1', width=width, reset_val=reset)
    bf._add(r_map.Enumeration(name='enum1', value=1))
    bf._add(r_map.Enumeration(name='enum2', value=2))
    bf._add(r_map.Enumeration(name='enum3', value=3))
    if parent:
        parent._add(bf)
    return bf

def get_reg(parent=None, name='reg1'):
    reg = r_map.Register(parent=parent, name=name, width=28, local_address=0)
    if parent:
        parent._add(reg)
    bf1 = r_map.BitField(name='bf1', width=5, reset_val=0x15)
    bf2 = r_map.BitField(name='bf2', width=10, reset_val=0x312)
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0)
    bf2_ref = r_map.BitFieldRef(name='bf2_ref', reg_offset=bf1.width)
    bf1_ref._add(bf1)
    bf2_ref._add(bf2)
    reg._add(bf1_ref)
    reg._add(bf2_ref)
    return reg

@pytest.fixture
def bf():
    return get_bf()

@pytest.fixture
def bf_ref(bf):
    bf_ref = r_map.BitFieldRef(name=bf.name+'_ref', reg_offset=0)
    bf_ref._add(bf)
    return bf_ref

@pytest.fixture
def reg():
    return get_reg()

@pytest.fixture
def full_map():
    root = r_map.Node(name='root')
    bf1 = r_map.BitField(name='bf1', width=8)
    enum1 = r_map.Enumeration(name='enum1', value=1)
    enum2 = r_map.Enumeration(name='enum2', value=2)
    bf1._add(enum1)
    bf1._add(enum2)
    bf1_ref = r_map.BitFieldRef(name='bf1', reg_offset=0, slice_width=4,
                                field_offset=0)
    bf1_ref._add(bf1)
    bf2_ref = bf1_ref._copy(name='bf2', reg_offset=4, slice_width=2,
                            field_offset=4, alias=True)
    reg1 = r_map.Register(name='reg1', local_address=0x1000)
    reg1._add(bf1_ref)
    reg1._add(bf2_ref)
    reg2 = reg1._copy(name='reg2', alias=True)
    reg3 = reg1._copy(name='reg3')

    rm = r_map.RegisterMap(name='rm', local_address=0)
    rm._add(reg1)
    rm._add(reg2)
    rm._add(reg3)

    root._add(rm)

    return root
