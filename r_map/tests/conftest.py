import pytest
from r_map.tests.data import get_data
from r_map.tests.basic_data import get_basic_data

@pytest.fixture(scope='session')
def data():
    return get_data()

@pytest.fixture(scope='session')
def basic_data():
    return get_basic_data()

