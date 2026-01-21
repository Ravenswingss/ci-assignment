import pytest
from math_utils import MathUtils


@pytest.fixture
def math_utils():
    """Fixture providing access to MathUtils."""
    return MathUtils


# ---------------------------
# add(a, b)
# ---------------------------

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-2, -5, -7),
        (-3, 7, 4),
        (999999, 1, 1000000),
    ],
)
def test_add(math_utils, a, b, expected):
    assert math_utils.add(a, b) == expected


# ---------------------------
# subtract(a, b)
# ---------------------------

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 4, 6),
        (0, 0, 0),
        (3, 8, -5),
        (-5, -2, -3),
        (-5, 2, -7),
    ],
)
def test_subtract(math_utils, a, b, expected):
    assert math_utils.subtract(a, b) == expected


# ---------------------------
# multiply(a, b)
# ---------------------------

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (4, 5, 20),
        (10, 0, 0),
        (0, 999, 0),
        (-3, 6, -18),
        (-3, -6, 18),
    ],
)
def test_multiply(math_utils, a, b, expected):
    assert math_utils.multiply(a, b) == expected


# ---------------------------
# divide(a, b)
# ---------------------------

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (-9, 3, -3.0),
        (0, 5, 0.0),
    ],
)
def test_divide_valid(math_utils, a, b, expected):
    assert math_utils.divide(a, b) == expected


def test_divide_by_zero_returns_negative_one(math_utils):
    assert math_utils.divide(5, 0) == -1.0
    assert math_utils.divide(0, 0) == -1.0
    assert math_utils.divide(-10, 0) == -1.0
 

