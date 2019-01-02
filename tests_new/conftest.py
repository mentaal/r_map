import pytest
import r_map

def get_reg(parent=None, name='reg1'):
    reg = r_map.Register(parent=parent, name=name, width=28)
    bf1_ref = r_map.BitFieldRef(name='bf1_ref', reg_offset=0, parent=reg)
    bf1 = r_map.BitField(name='bf1', width=5, parent=bf1_ref, reset_val=0x15)
    bf2_ref = r_map.BitFieldRef(name='bf2_ref', reg_offset=bf1.width, parent=reg)
    bf2 = r_map.BitField(name='bf2', width=10, parent=bf2_ref, reset_val=0x312)
    return reg

@pytest.fixture(scope='function')
def reg():
    return get_reg()
