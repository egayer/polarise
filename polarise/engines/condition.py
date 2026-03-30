"""Condition evaluation engine.

This is the DRY heart of all highlight_* methods. All highlighting operations
funnel through this single evaluation function.
"""

from typing import Literal
import polars as pl
from ..specs import Condition


def eval_condition(
    df: pl.DataFrame,
    col: str,
    condition: Condition,
    scope: Literal["column", "table"],
    all_cols: list[str] | None = None
) -> pl.Series:
    """Evaluate condition to create boolean mask.

    This function handles ALL condition types (gt, ge, lt, le, eq, between, max, min).
    All highlight_* methods funnel through here.

    Parameters:
        df: DataFrame to evaluate against
        col: Column name to evaluate
        condition: Condition specification
        scope: 'column' (per-column stats) or 'table' (global stats)
        all_cols: List of all selected columns (needed for table-scope max/min)

    Returns:
        Boolean Series (True where condition is met)

    Examples:
        >>> cond = Condition(op="gt", value=10)
        >>> mask = eval_condition(df, "price", cond, "column")
        >>> # mask is True where df["price"] > 10
    """
    series = df[col]

    # Cross-column expression (evaluate expression directly)
    if condition.op == "expr":
        if condition.expr is None:
            raise ValueError("expr operator requires condition.expr to be set")
        # Evaluate the Polars expression and return the boolean mask
        return df.select(condition.expr).to_series()

    # Simple value comparisons (don't need scope)
    if condition.op == "gt":
        return series > condition.value

    elif condition.op == "ge":
        return series >= condition.value

    elif condition.op == "lt":
        return series < condition.value

    elif condition.op == "le":
        return series <= condition.value

    elif condition.op == "eq":
        return series == condition.value

    elif condition.op == "between":
        return series.is_between(condition.low, condition.high, closed="both")

    # Statistical comparisons (need scope)
    elif condition.op == "max":
        if scope == "column":
            max_val = series.max()
        elif scope == "table":
            if all_cols is None:
                raise ValueError("all_cols required for table scope")
            # Compute global max across all selected columns
            max_val = df.select(all_cols).max().max_horizontal().item()
        else:
            raise ValueError(f"scope must be 'column' or 'table', got '{scope}'")
        return series == max_val

    elif condition.op == "min":
        if scope == "column":
            min_val = series.min()
        elif scope == "table":
            if all_cols is None:
                raise ValueError("all_cols required for table scope")
            # Compute global min across all selected columns
            min_val = df.select(all_cols).min().min_horizontal().item()
        else:
            raise ValueError(f"scope must be 'column' or 'table', got '{scope}'")
        return series == min_val

    else:
        raise ValueError(f"Unknown condition operator: {condition.op}")


def eval_highlight_identical(
    df: pl.DataFrame,
    columns: list[str]
) -> set[tuple[int, str]]:
    """Evaluate highlight_identical (special case - not using Condition).

    Finds cells where values match across columns in the same row.

    Parameters:
        df: DataFrame to evaluate
        columns: List of column names to compare

    Returns:
        Set of (row_idx, col_name) tuples to highlight

    Examples:
        >>> # df has columns 'actual', 'predicted'
        >>> # Row 0: actual=100, predicted=100 (match!)
        >>> # Row 1: actual=200, predicted=195 (no match)
        >>> cells = eval_highlight_identical(df, ['actual', 'predicted'])
        >>> # cells = {(0, 'actual'), (0, 'predicted')}
    """
    cells_to_highlight = set()

    for row_idx in range(len(df)):
        # Get values for this row across specified columns
        row_values = [df[col][row_idx] for col in columns]

        # Check if all values in this row are the same
        # (meaning all columns have identical values)
        first_val = row_values[0]
        if all(val == first_val for val in row_values):
            # All values match - highlight all cells in this row
            for col in columns:
                cells_to_highlight.add((row_idx, col))

    return cells_to_highlight
