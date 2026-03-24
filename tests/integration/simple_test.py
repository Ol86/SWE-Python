"""
Integration tests for simple operations.
"""

from pytest import mark


@mark.simple
def test_simple() -> None:
    """Test a simple operation."""
    assert True  # NOSONAR


@mark.skip(reason="Fails intentionally")
def test_always_fails() -> None:
    """Test an operation that always fails."""
    assert not True
