import pytest
from r_map.test.data import get_data

@pytest.fixture(scope='session')
def data():
    return get_data()

