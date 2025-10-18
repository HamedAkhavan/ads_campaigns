"""Thisk module contains the type definitions for the data used in the project."""

from typing import NamedTuple


class Banner(NamedTuple):
    """Banner data class."""

    id: int
    click: int
    banner: int
    campaign: int
    quarter: int
