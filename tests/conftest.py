import pytest
from .data import get_data
from .basic_data import get_basic_data

def reg_write_func(addr, val):
    print(f"Writing {val:#010x} to {addr:#010x}")
def reg_read_func(addr):
    val = 0xbadbadba
    print(f"Reading {val:#010x} from {addr:#010x}")
    return val
def block_write_func(addr, data):
    print(f"Writing {len(data)} bytes to {addr:#010x}")
def block_read_func(addr, size):
    print(f"Reading {size} bytes from {addr:#010x}")
    return bytes(v%256 for v in range(size))

@pytest.fixture(scope='session')
def data():
    root = get_data()
    root._reg_read_func = reg_read_func
    root._reg_write_func = reg_write_func
    root._block_read_func = block_read_func
    root._block_write_func = block_write_func
    return root

@pytest.fixture()
def basic_data():
    return get_basic_data()


