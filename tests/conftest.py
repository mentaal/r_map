import pytest
from .data import get_data
from .basic_data import get_basic_data

@pytest.fixture(scope='session')
def data():
    return get_data()

@pytest.fixture(scope='session')
def basic_data():
    return get_basic_data()

