"""Column selector normalization utilities.

Handles conversion of different column selector formats (pl.Expr, list[str])
into actual column names.
"""

from typing import Any
import polars as pl


def resolve_columns(df: pl.DataFrame, in_col: Any, exclude: list[str] | str | None = None) -> list[str]:
    """Resolve column selector to list of column names.

    Parameters:
        df: DataFrame to resolve columns from
        in_col: Column selector (pl.Expr, list[str], or str)
        exclude: Column name(s) to exclude from selection (useful with pl.all())

    Returns:
        List of resolved column names

    Examples:
        >>> resolve_columns(df, pl.col("price"))
        ['price']
        >>> resolve_columns(df, pl.all())
        ['col1', 'col2', 'col3']
        >>> resolve_columns(df, pl.all(), exclude='Date')
        ['col1', 'col2']  # Excludes 'Date' column
        >>> resolve_columns(df, pl.all(), exclude=['Date', 'Name'])
        ['col1', 'col2']  # Excludes multiple columns
        >>> resolve_columns(df, ["A", "B"])
        ['A', 'B']
    """
    # Normalize exclude to a list
    exclude_list = []
    if exclude is not None:
        if isinstance(exclude, str):
            exclude_list = [exclude]
        elif isinstance(exclude, list):
            exclude_list = exclude
        else:
            raise ValueError(f"exclude must be str or list[str], got {type(exclude)}")

    # If it's already a list of strings, return as-is (after exclusion)
    if isinstance(in_col, list):
        cols = [c for c in in_col if c not in exclude_list]
        if not cols:
            raise ValueError(f"All columns were excluded. Original: {in_col}, Excluded: {exclude_list}")
        return cols

    # If it's a string, wrap it in a list (after checking exclusion)
    if isinstance(in_col, str):
        if in_col in exclude_list:
            raise ValueError(f"Column '{in_col}' was excluded")
        return [in_col]

    # If it's a polars expression, evaluate it to get column names
    # This handles pl.all(), pl.col('name'), and other polars selectors
    if isinstance(in_col, pl.Expr):
        try:
            # Evaluate the expression to get the selected columns
            selected = df.select(in_col)
            cols = list(selected.columns)

            # Make sure we got at least one column
            if not cols:
                raise ValueError("Expression resolved to no columns")

            # Apply exclusion
            if exclude_list:
                original_cols = cols.copy()
                cols = [c for c in cols if c not in exclude_list]

                if not cols:
                    raise ValueError(
                        f"All columns were excluded. "
                        f"Selected: {original_cols}, Excluded: {exclude_list}"
                    )

            return cols
        except Exception as e:
            raise ValueError(
                f"Failed to resolve polars expression: {e}\n"
                f"Expression type: {type(in_col)}\n"
                f"Hint: Use pl.col('name') for single column or pl.all() for all columns"
            )

    # If we get here, the type is not supported
    raise ValueError(
        f"Invalid column selector type: {type(in_col)}.\n"
        f"Supported types:\n"
        f"  - pl.Expr (e.g., pl.col('name'), pl.all())\n"
        f"  - str (e.g., 'name')\n"
        f"  - list[str] (e.g., ['col1', 'col2'])"
    )
