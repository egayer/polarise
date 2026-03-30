"""Core internal dataclasses for styling specifications.

These are internal primitives used to represent styling instructions.
Users never interact with these directly - they're created by the translation
layer when public methods are called.
"""

from dataclasses import dataclass
from typing import Any, Literal, Union
import polars as pl


@dataclass(frozen=True)
class Condition:
    """Describes WHAT cells to highlight (boolean condition).

    This is an internal primitive used by all highlight_* methods
    (except highlight_identical).

    Operators:
        gt: greater than (>)
        ge: greater or equal (>=)
        lt: less than (<)
        le: less or equal (<=)
        eq: equal (==)
        between: value in [low, high]
        max: is maximum value (computed at render time)
        min: is minimum value (computed at render time)
        expr: custom Polars expression (for cross-column conditions)
    """
    op: Literal["gt", "ge", "lt", "le", "eq", "between", "max", "min", "expr"]
    value: float | None = None
    low: float | None = None
    high: float | None = None
    inclusive: bool = True
    expr: pl.Expr | None = None  # For cross-column highlighting


@dataclass(frozen=True)
class Mapper:
    """Describes HOW to map values to colors.

    This is an internal primitive used by gradient* and bar methods.

    Kinds:
        sequential: Linear mapping (low → high, one color scale)
        divergent: Split at center (low ← center → high, two color scales)

    Parameters:
        cmap: Colormap name (str) or matplotlib-like colormap object
              (e.g., 'viridis', 'RdBu', cm.jet, cmocean.cm.thermal)
        vmin: Minimum value for normalization (None = auto from data)
        vmax: Maximum value for normalization (None = auto from data)
        center: Center point for divergent gradients (required for divergent)
    """
    kind: Literal["sequential", "divergent"]
    cmap: Union[str, Any]  # str name or matplotlib-like colormap object
    vmin: float | None = None
    vmax: float | None = None
    center: float | None = None


@dataclass(frozen=True)
class StyleSpec:
    """Stores a styling instruction.

    This is the internal representation of all styling operations.
    Each public method creates one StyleSpec.

    Parameters:
        kind: Type of styling operation
        in_col: Column selector (pl.Expr or list[str])
        scope: How to compute statistics ('column' or 'table')
        condition: Condition for highlights (None for other operations)
        mapper: Mapper for gradients/bars (None for other operations)
        color: Text color (None = auto or no change)
        fill: Background color (None = no change)
        exclude: Column(s) to exclude from selection (useful with pl.all())
        params: Additional parameters (e.g., formatters for format())
    """
    kind: Literal["highlight", "gradient", "bar", "format", "highlight_identical"]
    in_col: Any  # pl.Expr | list[str]
    scope: Literal["column", "table"] | None
    condition: Condition | None
    mapper: Mapper | None
    color: str | None
    fill: str | None
    exclude: list[str] | str | None
    params: dict[str, Any]
