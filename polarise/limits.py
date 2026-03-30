"""Safety limits and DataFrame truncation logic.

Prevents browser crashes and performance issues from overly large tables.
"""

import polars as pl
import warnings


# Hard limits (non-negotiable)
MAX_ROWS = 500
MAX_COLS = 500
MAX_CELLS = 250_000


def truncate_dataframe(
    df: pl.DataFrame,
    max_rows: int = MAX_ROWS,
    max_cols: int = MAX_COLS,
    max_cells: int = MAX_CELLS
) -> tuple[pl.DataFrame, dict]:
    """Truncate DataFrame if it exceeds safety limits.

    Parameters:
        df: DataFrame to truncate
        max_rows: Maximum number of rows
        max_cols: Maximum number of columns
        max_cells: Maximum total cells (rows × cols)

    Returns:
        Tuple of (truncated_df, truncation_info)
        truncation_info contains keys:
            - rows_truncated: bool
            - cols_truncated: bool
            - original_rows: int
            - original_cols: int
            - final_rows: int
            - final_cols: int

    Examples:
        >>> df_large = pl.DataFrame({f'col{i}': range(1000) for i in range(100)})
        >>> df_safe, info = truncate_dataframe(df_large)
        >>> info['rows_truncated']
        True
    """
    original_rows = len(df)
    original_cols = len(df.columns)

    # Start with original dimensions
    target_rows = original_rows
    target_cols = original_cols

    # Check row limit
    rows_truncated = False
    if target_rows > max_rows:
        target_rows = max_rows
        rows_truncated = True

    # Check column limit
    cols_truncated = False
    if target_cols > max_cols:
        target_cols = max_cols
        cols_truncated = True

    # Check total cell limit
    if target_rows * target_cols > max_cells:
        # Proportionally reduce both dimensions
        ratio = (max_cells / (target_rows * target_cols)) ** 0.5
        target_rows = int(target_rows * ratio)
        target_cols = int(target_cols * ratio)
        rows_truncated = True
        cols_truncated = True

    # Actually truncate the DataFrame
    if rows_truncated or cols_truncated:
        truncated_df = df.head(target_rows).select(df.columns[:target_cols])

        # Issue warning
        warning_msg = (
            f"DataFrame truncated for display: "
            f"{original_rows}×{original_cols} → {target_rows}×{target_cols}"
        )
        warnings.warn(warning_msg, UserWarning)
    else:
        truncated_df = df

    truncation_info = {
        'rows_truncated': rows_truncated,
        'cols_truncated': cols_truncated,
        'original_rows': original_rows,
        'original_cols': original_cols,
        'final_rows': target_rows,
        'final_cols': target_cols,
    }

    return truncated_df, truncation_info
