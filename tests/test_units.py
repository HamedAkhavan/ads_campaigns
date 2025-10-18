"""Unit tests all end up in this file.

We are using a single file given the size of this project. However,
feel free to start splitting the tests, if you feel it is necessary.

"""

from datetime import datetime

import pytest

from ads_campaigns.utils import get_hours_quarter


@pytest.mark.parametrize(
    "time, expected",
    [
        (datetime(2021, 1, 1, 0, 0), 1),
        (datetime(2021, 1, 1, 0, 15), 2),
        (datetime(2021, 1, 1, 0, 30), 3),
        (datetime(2021, 1, 1, 0, 45), 4),
    ],
)
def test_get_hours_quarter(time, expected):
    """Test get_hour_quarter function."""
    assert get_hours_quarter(time) == expected
