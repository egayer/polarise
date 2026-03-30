"""Mapper evaluation engine.

This is the DRY heart of all gradient* methods and bar.
All value-to-color mapping operations funnel through this single evaluation function.
"""

from typing import Literal
import polars as pl
from ..specs import Mapper
from ..utils.colormaps import get_colormap


def eval_mapper(
    df: pl.DataFrame,
    col: str,
    mapper: Mapper,
    scope: Literal["column", "table"],
    all_cols: list[str] | None = None
) -> dict[int, str]:
    """Evaluate mapper to get value-to-color mappings.

    This function handles BOTH sequential and divergent gradients.
    All gradient* methods and bar funnel through here.

    Parameters:
        df: DataFrame to evaluate
        col: Column name to map
        mapper: Mapper specification
        scope: 'column' (per-column normalization) or 'table' (global normalization)
        all_cols: List of all selected columns (needed for table-scope)

    Returns:
        Dictionary mapping row_idx -> hex_color

    Examples:
        >>> mapper = Mapper(kind="sequential", cmap="viridis")
        >>> colors = eval_mapper(df, "price", mapper, "column")
        >>> # colors = {0: '#440154', 1: '#21908C', 2: '#FDE725', ...}
    """
    series = df[col]

    # Determine normalization range
    if mapper.vmin is not None and mapper.vmax is not None:
        vmin, vmax = mapper.vmin, mapper.vmax
    else:
        if scope == "column":
            vmin = series.min()
            vmax = series.max()
        elif scope == "table":
            if all_cols is None:
                raise ValueError("all_cols required for table scope")
            vmin = df.select(all_cols).min().min_horizontal().item()
            vmax = df.select(all_cols).max().max_horizontal().item()
        else:
            raise ValueError(f"scope must be 'column' or 'table', got '{scope}'")

    # Get colormap function
    cmap_func = get_colormap(mapper.cmap)

    # Handle edge case: all values are the same
    if vmax == vmin:
        # Map everything to middle of colormap
        mid_color = cmap_func(0.5)
        return {idx: mid_color for idx in range(len(series))}

    # Sequential gradient
    if mapper.kind == "sequential":
        colors = {}
        for idx, val in enumerate(series.to_list()):
            if val is None:
                colors[idx] = None  # Will be handled as null in rendering
            else:
                # Normalize to [0, 1]
                normalized = (val - vmin) / (vmax - vmin)
                # Clamp to [0, 1]
                normalized = max(0.0, min(1.0, normalized))
                colors[idx] = cmap_func(normalized)
        return colors

    # Divergent gradient
    elif mapper.kind == "divergent":
        if mapper.center is None:
            raise ValueError("Divergent mapper requires 'center' parameter")

        center = mapper.center
        colors = {}

        for idx, val in enumerate(series.to_list()):
            if val is None:
                colors[idx] = None
            else:
                # Split at center
                if val < center:
                    # Map to left half of colormap [0, 0.5]
                    if vmin == center:
                        normalized = 0.0
                    else:
                        normalized = 0.5 * (val - vmin) / (center - vmin)
                        normalized = max(0.0, min(0.5, normalized))
                elif val > center:
                    # Map to right half of colormap [0.5, 1]
                    if vmax == center:
                        normalized = 1.0
                    else:
                        normalized = 0.5 + 0.5 * (val - center) / (vmax - center)
                        normalized = max(0.5, min(1.0, normalized))
                else:
                    # Exactly at center
                    normalized = 0.5

                colors[idx] = cmap_func(normalized)

        return colors

    else:
        raise ValueError(f"Unknown mapper kind: {mapper.kind}")


def eval_bar(
    df: pl.DataFrame,
    col: str,
    scope: Literal["column", "table"],
    all_cols: list[str] | None = None
) -> dict:
    """Evaluate bar extents for signed bar rendering.

    Uses maximum absolute value as reference (100% width).
    For mixed positive/negative values:
    - Positive bars extend right from center (50% position)
    - Negative bars extend left from center (50% position)
    - Each bar length = (value / max_absolute) * 50% of cell width

    Parameters:
        df: DataFrame to evaluate
        col: Column name
        scope: 'column' or 'table'
        all_cols: All selected columns (for table scope)

    Returns:
        Dictionary with keys:
            'max_absolute': float - maximum absolute value (reference for 100%)
            'has_negative': bool - whether data contains negative values
            'has_positive': bool - whether data contains positive values
            'values': list - raw values for this column

    Examples:
        >>> result = eval_bar(df, "change", "column")
        >>> # values: [20, -15, 45]
        >>> # result = {'max_absolute': 45, 'has_negative': True, 'has_positive': True, 'values': [...]}
        >>> # Bar for 20:  (20/45)*50% = 22.2% width, extends RIGHT from center
        >>> # Bar for -15: (15/45)*50% = 16.7% width, extends LEFT from center
        >>> # Bar for 45:  (45/45)*50% = 50% width, extends RIGHT from center (full right half)
    """
    series = df[col]

    # Determine value range
    if scope == "column":
        vmin = series.min()
        vmax = series.max()
    elif scope == "table":
        if all_cols is None:
            raise ValueError("all_cols required for table scope")
        vmin = df.select(all_cols).min().min_horizontal().item()
        vmax = df.select(all_cols).max().max_horizontal().item()
    else:
        raise ValueError(f"scope must be 'column' or 'table', got '{scope}'")

    # Compute maximum absolute value (this is the reference for 100% width)
    max_absolute = max(abs(vmin if vmin is not None else 0.0),
                       abs(vmax if vmax is not None else 0.0))

    # Determine if we have positive, negative, or mixed values
    has_negative = (vmin is not None and vmin < 0)
    has_positive = (vmax is not None and vmax > 0)

    # Return max absolute value and values
    return {
        'max_absolute': max_absolute,
        'has_negative': has_negative,
        'has_positive': has_positive,
        'values': series.to_list()
    }
