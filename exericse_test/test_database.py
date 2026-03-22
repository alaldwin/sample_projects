import pytest
from database import Databases

@pytest.fixture
def data():
    """provides a fresh instance of the Database class and clean ups after the test."""
    db = Databases()
    yield db

def test_add_user(data):
    data.add_user(1, "Alice")
    assert data.get_user(1) == "Alice"

def test_add_duplication(data):
    data.add_user(1, "Alice")
    with pytest.raises(ValueError, match="User already exists"):
        data.add_user(1, "Bob")

    
def test_delete_user(data):
    data.add_user(2, "Bob")
    data.delete_user(2)
    assert data.get_user(2) is None
