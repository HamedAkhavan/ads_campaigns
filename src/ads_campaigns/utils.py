"""Utility functions.

This module contains any generic logic that is used in the project.
"""

from datetime import datetime


def get_hours_quarter(time: datetime = datetime.utcnow()) -> int:
    """Get which quarter of the hour a time is in.

    Args:
        time (datetime): The time to get the quarter for.

    Returns:
        int: The quarter of the hour the time is in.
    """
    return (time.minute // 15) + 1
