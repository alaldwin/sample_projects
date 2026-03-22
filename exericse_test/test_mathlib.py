import pytest
from mathlib import UserManager

@pytest.fixture
def user_manager():
    """Creates a fresh instance of Usermanager before each test."""
    return UserManager()

def test_add_user(user_manager):
    assert user_manager.add_user("john_doe", "john@example.com") == True
    assert user_manager.get_user("john_doe") == "john@example.com"

def test_add_duplication(user_manager):
    user_manager.add_user("john_doe", "john@example.com")
    with pytest.raises(ValueError):
        user_manager.add_user("john_doe", "another@example.com")
