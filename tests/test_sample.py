"""
Basic unit tests to verify pytest is working correctly.
"""


def add(a, b):
    """Simple function to add two numbers."""
    return a + b


class TestBasicOperations:
    """Test basic mathematical operations."""

    def test_add_positive_numbers(self):
        """Test addition of positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test addition of negative numbers."""
        assert add(-1, -2) == -3


def test_string_operations():
    """Test basic string operations."""
    text = "pytest"
    assert text == "pytest"
    assert len(text) == 6
    assert text.upper() == "PYTEST"


def test_list_operations():
    """Test basic list operations."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert 3 in numbers
    assert sum(numbers) == 15


