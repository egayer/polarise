"""Polarise - Polars DataFrame Styling Package

A polars-native DataFrame styling package that generates styled HTML tables
for data exploration and export.

Example:
    >>> import polars as pl
    >>> import polarise
    >>>
    >>> df = pl.DataFrame({
    ...     'product': ['A', 'B', 'C', 'D'],
    ...     'price': [19.99, 29.99, 15.50, 45.00],
    ...     'sales': [120, 85, 200, 65]
    ... })
    >>>
    >>> df.style().highlight_max(in_col="price", fill="yellow").show()

**IMPORTANT: DataFrame Immutability**
The DataFrame should NOT be modified after calling .style().
Transform your data FIRST, then style, then render.

Correct workflow:
    >>> df = df.filter(...).with_columns(...)  # Transform FIRST
    >>> styled = df.style().highlight_max(...)  # THEN style
    >>> styled.to_html()  # THEN render

Incorrect workflow (undefined behavior):
    >>> styled = df.style().highlight_max(...)
    >>> df = df.with_columns(...)  # DON'T modify after styling!
"""

__version__ = "1.0.1"
__author__ = "Eric Gayer"
__license__ = "GPL-3.0"

import polars as pl
from .styler import Styler


def _style(self, **kwargs) -> Styler:
    """Create a Styler instance for this DataFrame.

    **IMPORTANT:** Do not modify the DataFrame after calling .style().
    Transform your data first, then style, then render.

    Returns:
        Styler instance for method chaining

    Example:
        >>> df.style().highlight_max(in_col="price").show()
    """
    return Styler(self, **kwargs)


# Monkey-patch polars DataFrame
pl.DataFrame.style = _style


# Export main class
__all__ = ['Styler']
