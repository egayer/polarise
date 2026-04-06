"""Styler class - the public API for Polarise.

IMPORTANT: DataFrame must be immutable after .style() is called.
Users should transform data BEFORE styling, then render.
"""

from typing import Any, Literal, Union
import polars as pl
from .specs import Condition, Mapper, StyleSpec


class Styler:
    """Style a Polars DataFrame for HTML rendering.

    **IMPORTANT: Immutability Contract**
    The DataFrame should NOT be modified after calling .style().
    Transform your data FIRST, then style, then render.

    Example:
        >>> df = df.filter(...).with_columns(...)  # Transform FIRST
        >>> styled = df.style().highlight_max(...)  # THEN style
        >>> styled.to_html()  # THEN render

    All methods return a new Styler instance (immutable chaining).
    """

    def __init__(
        self,
        df: pl.DataFrame,
        max_rows: int = 500,
        max_cols: int = 500,
        max_cells: int = 250_000,
        null_cell_color: str = "#F0F0F0",
        null_text_color: str = "#999999"
    ):
        """Initialize Styler.

        Parameters:
            df: DataFrame to style
            max_rows: Maximum rows to display (truncation limit)
            max_cols: Maximum columns to display (truncation limit)
            max_cells: Maximum total cells to display (truncation limit)
            null_cell_color: Background color for null cells
            null_text_color: Text color for null cells
        """
        self.df = df
        self.styles: list[StyleSpec] = []
        self.hidden_axes: set[str] = {"index"}  # Hide index by default (Polars has no index)
        self.fashion: str = "raw"  # Default fashion

        # Safety limits
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.max_cells = max_cells

        # Null styling
        self.null_cell_color = null_cell_color
        self.null_text_color = null_text_color

        # Table metadata
        self.table_title: str | None = None
        self.table_subtitle: str | None = None
        self.table_caption: str | None = None
        self.table_footnote: str | None = None
        self.info_name: str | None = None
        self.show_info_flag: bool = False

    def _copy(self) -> "Styler":
        """Create a copy of this Styler."""
        new_styler = Styler(
            self.df,
            self.max_rows,
            self.max_cols,
            self.max_cells,
            self.null_cell_color,
            self.null_text_color
        )
        new_styler.styles = self.styles.copy()
        new_styler.hidden_axes = self.hidden_axes.copy()
        new_styler.fashion = self.fashion
        new_styler.table_title = self.table_title
        new_styler.table_subtitle = self.table_subtitle
        new_styler.table_caption = self.table_caption
        new_styler.table_footnote = self.table_footnote
        new_styler.info_name = self.info_name
        new_styler.show_info_flag = self.show_info_flag
        return new_styler

    def _add_style(
        self,
        kind: Literal["highlight", "gradient", "bar", "format", "highlight_identical"],
        in_col: Any,
        scope: Literal["column", "table"] | None = None,
        condition: Condition | None = None,
        mapper: Mapper | None = None,
        color: str | None = None,
        fill: str | None = None,
        exclude: list[str] | str | None = None,
        params: dict[str, Any] | None = None
    ) -> "Styler":
        """Internal: Add a style specification and return new Styler.

        This is the translation layer - all public methods funnel through here.
        """
        spec = StyleSpec(
            kind=kind,
            in_col=in_col,
            scope=scope,
            condition=condition,
            mapper=mapper,
            color=color,
            fill=fill,
            exclude=exclude,
            params=params or {}
        )

        new_styler = self._copy()
        new_styler.styles = self.styles + [spec]
        return new_styler

    # ========================================================================
    # HIGHLIGHT METHODS
    # ========================================================================

    def highlight_max(
        self,
        in_col: Any,
        scope: Literal["column", "table"] = "column",
        color: str | None = None,
        fill: str = "yellow",
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Highlight maximum values.

        Parameters:
            in_col: Column selector (pl.col(), pl.all(), or list of column names)
            scope: 'column' (per-column max) or 'table' (global max)
            color: Text color (None = auto contrast)
            fill: Background color
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> df.style().highlight_max(in_col="price", fill="yellow")
            >>> df.style().highlight_max(in_col=pl.all(), exclude='Date', scope='table')
        """
        condition = Condition(op="max")
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope=scope,
            condition=condition,
            color=color,
            fill=fill,
            exclude=exclude
        )

    def highlight_min(
        self,
        in_col: Any,
        scope: Literal["column", "table"] = "column",
        color: str | None = None,
        fill: str = "lightblue",
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Highlight minimum values.

        Parameters:
            in_col: Column selector
            scope: 'column' (per-column min) or 'table' (global min)
            color: Text color (None = auto contrast)
            fill: Background color
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> df.style().highlight_min(in_col=pl.all(), scope="table")
            >>> df.style().highlight_min(in_col=pl.all(), exclude=['Date', 'Name'])
        """
        condition = Condition(op="min")
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope=scope,
            condition=condition,
            color=color,
            fill=fill,
            exclude=exclude
        )

    def highlight_above(
        self,
        in_col: Any,
        value: float,
        inclusive: bool = False,
        scope: Literal["column", "table"] = "column",
        color: str | None = None,
        fill: str = "yellow"
    ) -> "Styler":
        """Highlight values above threshold.

        Parameters:
            in_col: Column selector
            value: Threshold value
            inclusive: If True, use >= instead of >
            scope: Not used (kept for API consistency)
            color: Text color
            fill: Background color

        Example:
            >>> df.style().highlight_above(in_col="sales", value=100, fill="lightgreen")
        """
        condition = Condition(
            op="ge" if inclusive else "gt",
            value=value
        )
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope=scope,
            condition=condition,
            color=color,
            fill=fill
        )

    def highlight_below(
        self,
        in_col: Any,
        value: float,
        inclusive: bool = False,
        scope: Literal["column", "table"] = "column",
        color: str | None = None,
        fill: str = "yellow"
    ) -> "Styler":
        """Highlight values below threshold.

        Parameters:
            in_col: Column selector
            value: Threshold value
            inclusive: If True, use <= instead of <
            scope: Not used (kept for API consistency)
            color: Text color
            fill: Background color

        Example:
            >>> df.style().highlight_below(in_col="price", value=20, fill="lightblue")
        """
        condition = Condition(
            op="le" if inclusive else "lt",
            value=value
        )
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope=scope,
            condition=condition,
            color=color,
            fill=fill
        )

    def highlight_equal(
        self,
        in_col: Any,
        value: float,
        color: str | None = None,
        fill: str = "yellow"
    ) -> "Styler":
        """Highlight values equal to target.

        Parameters:
            in_col: Column selector
            value: Target value
            color: Text color
            fill: Background color

        Example:
            >>> df.style().highlight_equal(in_col="status", value=1, fill="green")
        """
        condition = Condition(op="eq", value=value)
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope="column",
            condition=condition,
            color=color,
            fill=fill
        )

    def highlight_between(
        self,
        in_col: Any,
        low: float,
        high: float,
        scope: Literal["column", "table"] = "column",
        color: str | None = None,
        fill: str = "yellow"
    ) -> "Styler":
        """Highlight values in range [low, high].

        Parameters:
            in_col: Column selector
            low: Lower bound (inclusive)
            high: Upper bound (inclusive)
            scope: Not used (kept for API consistency)
            color: Text color
            fill: Background color

        Example:
            >>> df.style().highlight_between(in_col="score", low=70, high=90, fill="yellow")
        """
        condition = Condition(op="between", low=low, high=high, inclusive=True)
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope=scope,
            condition=condition,
            color=color,
            fill=fill
        )

    def highlight_identical(
        self,
        in_col: list[str],
        color: str | None = None,
        fill: str = "yellow"
    ) -> "Styler":
        """Highlight rows where values are identical across specified columns.

        **EXCEPTION:** This is the only highlight method that doesn't use Condition.
        It performs row-wise comparison.

        Parameters:
            in_col: List of column names to compare (must be list[str])
            color: Text color
            fill: Background color

        Example:
            >>> df.style().highlight_identical(in_col=['actual', 'predicted'], fill='lightgreen')
        """
        return self._add_style(
            kind="highlight_identical",
            in_col=in_col,
            scope=None,
            condition=None,
            mapper=None,
            color=color,
            fill=fill
        )

    def highlight_when(
        self,
        in_col: Any,
        when: pl.Expr,
        then_fill: str = "yellow",
        then_color: str | None = None,
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Highlight cells based on cross-column conditions.

        Parameters:
            in_col: Column selector (column to highlight)
            when: Polars expression that evaluates to boolean (the condition)
            then_fill: Background color when condition is True
            then_color: Text color when condition is True (None = auto contrast)
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> # Highlight "value" cells when "reference" > 10
            >>> df.style().highlight_when(
            ...     in_col="value",
            ...     when=pl.col("reference") > 10,
            ...     then_fill="orange",
            ...     then_color="black"
            ... )
            >>> # Highlight cells when multiple conditions are met
            >>> df.style().highlight_when(
            ...     in_col="sales",
            ...     when=(pl.col("region") == "North") & (pl.col("quarter") == "Q4"),
            ...     then_fill="lightgreen"
            ... )
        """
        condition = Condition(op="expr", expr=when)
        return self._add_style(
            kind="highlight",
            in_col=in_col,
            scope="column",  # Not used for expr-based conditions
            condition=condition,
            color=then_color,
            fill=then_fill,
            exclude=exclude
        )

    # ========================================================================
    # GRADIENT METHODS
    # ========================================================================

    def gradient(
        self,
        in_col: Any,
        scope: Literal["column", "table"] = "column",
        cmap: Union[str, Any] = "viridis",
        color: bool = False,
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Apply sequential color gradient.

        Parameters:
            in_col: Column selector
            scope: 'column' (per-column normalization) or 'table' (global)
            cmap: Colormap name (str) or matplotlib-like colormap object
                  (e.g., 'viridis', 'RdYlGn', cm.jet, cmocean.cm.thermal)
            color: Apply gradient to text (default: False = background gradient)
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> # Background gradient with auto-contrast text (default)
            >>> df.style().gradient(in_col="sales", cmap="viridis")
            >>> # Text gradient (no background)
            >>> df.style().gradient(in_col="sales", cmap="viridis", color=True)
            >>> # Using matplotlib colormap object
            >>> from matplotlib import cm
            >>> df.style().gradient(in_col="temperature", cmap=cm.jet)
        """
        # Validate color parameter
        if not isinstance(color, bool):
            raise TypeError(
                f"'color' parameter only accepts boolean values (True/False), got {type(color).__name__}."
            )

        # Derive fill automatically: if color=True, then fill=False (and vice versa)
        fill = not color

        mapper = Mapper(kind="sequential", cmap=cmap)
        return self._add_style(
            kind="gradient",
            in_col=in_col,
            scope=scope,
            mapper=mapper,
            color=None,  # Auto-contrast
            exclude=exclude,
            params={"apply_fill": fill, "apply_color": color}
        )

    def gradient_divergent(
        self,
        in_col: Any,
        center: float,
        scope: Literal["column", "table"] = "column",
        cmap: Union[str, Any] = "RdBu",
        color: bool = False,
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Apply divergent color gradient (splits at center point).

        Parameters:
            in_col: Column selector
            center: Center point (e.g., 0 for positive/negative)
            scope: 'column' or 'table'
            cmap: Divergent colormap name (str) or matplotlib-like colormap object
                  (e.g., 'RdBu', 'RdYlGn', cm.RdBu, cmocean.cm.balance)
            color: Apply gradient to text (default: False = background gradient)
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> # Red for negative, white at 0, blue for positive (background, default)
            >>> df.style().gradient_divergent(in_col="change", center=0, cmap="RdBu")
            >>> df.style().gradient_divergent(in_col=pl.all(), center=0, exclude='Date')
            >>> # Text gradient (no background)
            >>> df.style().gradient_divergent(in_col="change", center=0, color=True)
            >>> # Using matplotlib colormap object
            >>> from matplotlib import cm
            >>> df.style().gradient_divergent(in_col="change", center=0, cmap=cm.RdBu)
        """
        # Validate color parameter
        if not isinstance(color, bool):
            raise TypeError(
                f"'color' parameter only accepts boolean values (True/False), got {type(color).__name__}."
            )

        # Derive fill automatically: if color=True, then fill=False (and vice versa)
        fill = not color

        mapper = Mapper(kind="divergent", cmap=cmap, center=center)
        return self._add_style(
            kind="gradient",
            in_col=in_col,
            scope=scope,
            mapper=mapper,
            color=None,  # Auto-contrast
            exclude=exclude,
            params={"apply_fill": fill, "apply_color": color}
        )

    def gradient_between(
        self,
        in_col: Any,
        low: float,
        high: float,
        scope: Literal["column", "table"] = "column",
        cmap: Union[str, Any] = "viridis",
        color: bool = False,
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Apply gradient only within specified range.

        Parameters:
            in_col: Column selector
            low: Lower bound for gradient
            high: Upper bound for gradient
            scope: 'column' or 'table'
            cmap: Colormap name (str) or matplotlib-like colormap object
                  (e.g., 'viridis', cm.plasma, cmocean.cm.thermal)
            color: Apply gradient to text (default: False = background gradient)
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> df.style().gradient_between(in_col="temp", low=0, high=100)
            >>> df.style().gradient_between(in_col=pl.all(), low=0, high=100, exclude='ID')
        """
        # Validate color parameter
        if not isinstance(color, bool):
            raise TypeError(
                f"'color' parameter only accepts boolean values (True/False), got {type(color).__name__}."
            )

        # Derive fill automatically: if color=True, then fill=False (and vice versa)
        fill = not color

        mapper = Mapper(kind="sequential", cmap=cmap, vmin=low, vmax=high)
        return self._add_style(
            kind="gradient",
            in_col=in_col,
            scope=scope,
            mapper=mapper,
            color=None,  # Auto-contrast
            exclude=exclude,
            params={"apply_fill": fill, "apply_color": color}
        )

    def heat_map(
        self,
        in_col: Any = pl.all(),
        cmap: Union[str, Any] = "viridis",
        color: bool = False,
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Apply heatmap coloring across entire table.

        This is a convenience method - equivalent to gradient() with scope='table'.
        Colors are normalized globally across all selected columns.

        Parameters:
            in_col: Column selector (default: pl.all() - all columns)
            cmap: Colormap name (str) or matplotlib-like colormap object
                  (e.g., 'viridis', 'roma', cm.jet, cmocean.cm.thermal)
            color: Apply gradient to text (default: False = background gradient)
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> # Classic heatmap with background gradient (default)
            >>> df.style().heat_map(exclude='date')
            >>> # Heatmap with text gradient (no background)
            >>> df.style().heat_map(exclude='date', color=True)
            >>> # Heatmap with custom colormap
            >>> df.style().heat_map(cmap='roma', exclude=['date', 'name'])
            >>> # Using matplotlib colormap object
            >>> import cmocean
            >>> df.style().heat_map(cmap=cmocean.cm.thermal, exclude='date')
        """
        # Validate color parameter
        if not isinstance(color, bool):
            raise TypeError(
                f"'color' parameter only accepts boolean values (True/False), got {type(color).__name__}."
            )

        return self.gradient(
            in_col=in_col,
            scope="table",
            cmap=cmap,
            color=color,
            exclude=exclude
        )

    # ========================================================================
    # BAR METHOD
    # ========================================================================

    def bar(
        self,
        in_col: Any,
        scope: Literal["column", "table"] = "column",
        color: str | None = None,
        fill: str = "lightblue",
        fill_pos: str | None = None,
        fill_neg: str | None = None,
        exclude: list[str] | str | None = None
    ) -> "Styler":
        """Add in-cell bar charts using CSS gradients.

        Parameters:
            in_col: Column selector
            scope: 'column' (normalize per column) or 'table' (global)
            color: Text color
            fill: Bar color (used for positive-only bars, or positive bars if fill_pos not set)
            fill_pos: Color for positive bars when data has mixed signs (default: fill)
            fill_neg: Color for negative bars when data has mixed signs (default: indianred)
            exclude: Column(s) to exclude from selection (useful with pl.all())

        Example:
            >>> df.style().bar(in_col="sales", fill="steelblue")
            >>> df.style().bar(in_col="change", fill_pos="green", fill_neg="red")
            >>> df.style().bar(in_col=pl.all(), exclude=['Date', 'Category'])
        """
        return self._add_style(
            kind="bar",
            in_col=in_col,
            scope=scope,
            color=color,
            fill=fill,
            exclude=exclude,
            params={"fill_pos": fill_pos, "fill_neg": fill_neg}
        )

    # ========================================================================
    # FORMAT METHOD
    # ========================================================================

    def format(self, formatters: dict[str, str]) -> "Styler":
        """Apply Python format strings to columns.

        Parameters:
            formatters: Dictionary mapping column names to format strings

        Example:
            >>> df.style().format({
            ...     'price': '${:.2f}',
            ...     'percentage': '{:.1%}',
            ...     'count': '{:,}'
            ... })
        """
        return self._add_style(
            kind="format",
            in_col=None,
            params={"formatters": formatters}
        )

    # ========================================================================
    # DISPLAY CONTROL METHODS
    # ========================================================================

    def show_idx(self) -> "Styler":
        """Show row index column.

        By default, row indices are hidden (since Polars has no index concept).
        Use this method to display row numbers.

        Example:
            >>> df.style().show_idx().show()
        """
        new_styler = self._copy()
        new_styler.hidden_axes.discard("index")
        return new_styler

    def hide_columns(self) -> "Styler":
        """Hide column headers.

        Example:
            >>> df.style().hide_columns().show()
        """
        new_styler = self._copy()
        new_styler.hidden_axes.add("columns")
        return new_styler

    def show_info(self, name: str | None = None) -> "Styler":
        """Show dataframe info (name and shape) above the table.

        Parameters:
            name: Optional name to display (e.g., 'df_sales')
                  If None, only shape is shown

        Example:
            >>> df.style().show_info(name='df_sales').show()
            # Displays:
            # df_sales:
            # shape: (100, 5)
        """
        new_styler = self._copy()
        new_styler.show_info_flag = True
        new_styler.info_name = name
        return new_styler

    def title(self, title: str | None = None, subtitle: str | None = None) -> "Styler":
        """Add title and optional subtitle above the table.

        Parameters:
            title: Main title text
            subtitle: Optional subtitle (displayed in smaller font below title)

        Example:
            >>> df.style().title('Sales Report', subtitle='Q4 2024').show()
        """
        new_styler = self._copy()
        new_styler.table_title = title
        new_styler.table_subtitle = subtitle
        return new_styler

    def footnote(self, text: str) -> "Styler":
        """Add footnote text below the table.

        Parameters:
            text: Footnote text

        Example:
            >>> df.style().footnote('Data as of December 2024').show()
        """
        new_styler = self._copy()
        new_styler.table_footnote = text
        return new_styler

    def caption(self, text: str) -> "Styler":
        """Add caption above the table (scientific convention).

        Parameters:
            text: Caption text (plain text, no formatting)

        Example:
            >>> df.style().caption('Table 1 — Sales by quarter after normalization').show()
        """
        new_styler = self._copy()
        new_styler.table_caption = text
        return new_styler

    # ========================================================================
    # FASHION METHODS
    # ========================================================================

    def fashion_grid(self) -> "Styler":
        """Apply grid fashion (clean white table with grid lines).

        Features:
        - White background for table, headers, and cells
        - Bold column headers
        - Bold first column
        - Light grey grid lines

        Example:
            >>> df.style().fashion_grid().highlight_max(...)
        """
        new_styler = self._copy()
        new_styler.fashion = "grid"
        return new_styler

    def fashion_zebra(self, fill1: str | None = None, fill2: str | None = None) -> "Styler":
        """Apply zebra fashion (alternating row colors, no grid).

        Parameters:
            fill1: Color for odd rows (default: from fashion.zebra.ZEBRA_DEFAULT_FILL1)
            fill2: Color for even rows (default: from fashion.zebra.ZEBRA_DEFAULT_FILL2)

        Features:
        - Alternating row colors
        - Bold column headers
        - Bold first column
        - No grid lines

        Example:
            >>> df.style().fashion_zebra().gradient(...)
            >>> df.style().fashion_zebra(fill1='white', fill2='lightblue')
        """
        new_styler = self._copy()
        # Pass None values through - css.py will handle defaults
        new_styler.fashion = {'name': 'zebra', 'params': {'fill1': fill1, 'fill2': fill2}}
        return new_styler

    def fashion_raw(self) -> "Styler":
        """Apply raw fashion (mimics Polars print style).

        Features:
        - Black lines around title row and columns
        - Monospace font (Courier)
        - No bold text
        - Clean, minimal look

        Example:
            >>> df.style().fashion_raw().gradient(...)
        """
        new_styler = self._copy()
        new_styler.fashion = "raw"
        return new_styler

    def fashion_scientific(self) -> "Styler":
        """Apply scientific fashion (publication-ready tables).

        Features:
        - Horizontal lines only
        - Thick line at top of table
        - Thick line below headers
        - Thick line at bottom of table
        - Bold column headers and first column
        - Times New Roman font

        Example:
            >>> df.style().fashion_scientific().highlight_max(...)
        """
        new_styler = self._copy()
        new_styler.fashion = "scientific"
        return new_styler

    def fashion_minimal(self) -> "Styler":
        """Apply minimal fashion (clean table with column dividers).

        Features:
        - Vertical column dividers only (no horizontal lines)
        - Light gray header background (#f2f2f2)
        - Sans-serif font (same as grid)
        - Bold column headers and first column
        - Clean, minimal look

        Example:
            >>> df.style().fashion_minimal().gradient(...)
        """
        new_styler = self._copy()
        new_styler.fashion = "minimal"
        return new_styler

    def fashion_compact(self) -> "Styler":
        """Apply compact fashion (dense layout for viewing more data).

        Features:
        - Smaller font (11px) and reduced padding
        - Black borders (same as raw)
        - Monospace font (Courier)
        - Fits more data on screen while remaining readable

        Example:
            >>> df.style().fashion_compact().highlight_max(...)
        """
        new_styler = self._copy()
        new_styler.fashion = "compact"
        return new_styler

    def fashion_presentation(self) -> "Styler":
        """Apply presentation fashion (spacious layout for slides/presentations).

        Features:
        - Larger font (14px) and increased padding
        - Vertical column dividers only
        - Light gray header background (#f2f2f2)
        - Sans-serif font
        - Extra spacing for better readability at distance

        Example:
            >>> df.style().fashion_presentation().highlight_max(...)
        """
        new_styler = self._copy()
        new_styler.fashion = "presentation"
        return new_styler

    # ========================================================================
    # RENDERING METHODS
    # ========================================================================

    def to_html(self, path: str | None = None) -> str:
        """Generate HTML table.

        Parameters:
            path: If provided, saves HTML to this file path

        Returns:
            HTML string

        Example:
            >>> html = df.style().highlight_max(...).to_html()
            >>> # Or save to file:
            >>> df.style().highlight_max(...).to_html('report.html')
        """
        from .render.html import generate_html
        from .limits import truncate_dataframe

        # Truncate DataFrame if needed
        df_display, truncation_info = truncate_dataframe(
            self.df,
            self.max_rows,
            self.max_cols,
            self.max_cells
        )

        # Generate HTML
        html = generate_html(
            df_display,
            self.styles,
            self.hidden_axes,
            self.fashion,
            truncation_info,
            self.null_cell_color,
            self.null_text_color,
            self.table_title,
            self.table_subtitle,
            self.table_caption,
            self.table_footnote,
            self.show_info_flag,
            self.info_name
        )

        # Save to file if path provided
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)

        return html

    def to_latex(self, caption: str | None = None, label: str | None = None) -> str:
        """Export styled table to LaTeX (booktabs format).

        Only supports fashion_minimal() and fashion_scientific().
        Colors, gradients, and bars are not exported (HTML-only features).

        Parameters:
            caption: Table caption (LaTeX \\caption{...})
            label: Table label for cross-referencing (LaTeX \\label{...})

        Returns:
            LaTeX table code as string

        Raises:
            ValueError: If no fashion is applied
            NotImplementedError: If fashion is not 'minimal' or 'scientific'

        Example:
            >>> latex = df.style().fashion_scientific().to_latex(
            ...     caption="Sales by quarter",
            ...     label="tab:sales"
            ... )
            >>> print(latex)

        Required LaTeX packages (add to your preamble):
            \\usepackage{booktabs}
            \\usepackage{caption}
        """
        # ------------------------------------------------------------------
        # Validate fashion
        # ------------------------------------------------------------------
        if self.fashion is None or self.fashion == "raw":
            raise ValueError(
                "LaTeX export requires a fashion. "
                "Use .fashion_minimal() or .fashion_scientific() before calling to_latex()."
            )

        # Extract fashion name (handle both string and dict formats)
        if isinstance(self.fashion, dict):
            fashion_name = self.fashion.get("name")
        else:
            fashion_name = self.fashion

        if fashion_name not in {"minimal", "scientific"}:
            raise NotImplementedError(
                f"LaTeX export is only supported for 'minimal' and 'scientific' fashions. "
                f"Got: '{fashion_name}'. "
                f"Use .fashion_minimal() or .fashion_scientific()."
            )

        # ------------------------------------------------------------------
        # Helper: Escape LaTeX special characters
        # ------------------------------------------------------------------
        def _escape_latex(text: str) -> str:
            """Escape special LaTeX characters."""
            if text is None:
                return ""
            text = str(text)
            replacements = {
                '\\': r'\textbackslash{}',
                '&': r'\&',
                '%': r'\%',
                '$': r'\$',
                '#': r'\#',
                '_': r'\_',
                '{': r'\{',
                '}': r'\}',
                '~': r'\textasciitilde{}',
                '^': r'\^{}',
            }
            for char, escaped in replacements.items():
                text = text.replace(char, escaped)
            return text

        # ------------------------------------------------------------------
        # Check if index should be shown
        # ------------------------------------------------------------------
        show_index = "index" not in self.hidden_axes

        # ------------------------------------------------------------------
        # Get DataFrame
        # ------------------------------------------------------------------
        df = self.df

        # Handle empty DataFrame
        if df.is_empty():
            raise ValueError("Cannot export empty DataFrame to LaTeX")

        # ------------------------------------------------------------------
        # Column alignment
        # ------------------------------------------------------------------
        align = []
        if show_index:
            align.append("r")  # Index column: right-aligned

        for col in df.columns:
            dtype = df[col].dtype
            # Right-align numeric columns, left-align others
            if dtype.is_numeric():
                align.append("r")
            else:
                align.append("l")

        colspec = "".join(align)

        # ------------------------------------------------------------------
        # Header row
        # ------------------------------------------------------------------
        header = []
        if show_index:
            header.append("")  # Empty cell above index column

        # Escape column names
        for col in df.columns:
            header.append(_escape_latex(str(col)))

        header_line = " & ".join(r"\textbf{" + h + "}" for h in header) + r" \\"

        # ------------------------------------------------------------------
        # Data rows
        # ------------------------------------------------------------------
        rows = []
        for i, row in enumerate(df.iter_rows()):
            values = []

            # Add index if shown
            if show_index:
                values.append(str(i))

            # Add cell values
            for val in row:
                if val is None:
                    values.append("")  # Empty string for null values
                else:
                    values.append(_escape_latex(str(val)))

            rows.append(" & ".join(values) + r" \\")

        # ------------------------------------------------------------------
        # Rules (booktabs)
        # ------------------------------------------------------------------
        top_rule = r"\toprule"
        mid_rule = r"\midrule"
        bottom_rule = r"\bottomrule"

        # Assemble table body
        table_lines = [
            top_rule,
            header_line,
            mid_rule,
            *rows,
            bottom_rule,
        ]

        tabular = "\n".join(table_lines)

        # ------------------------------------------------------------------
        # Caption handling (goes above table)
        # ------------------------------------------------------------------
        caption_block = ""

        # Use provided caption first, fallback to table_caption
        final_caption = caption if caption is not None else self.table_caption

        if final_caption:
            caption_block += f"\\caption{{{_escape_latex(final_caption)}}}\n"

        if label:
            caption_block += f"\\label{{{label}}}\n"

        # ------------------------------------------------------------------
        # Footnote handling (goes below table)
        # ------------------------------------------------------------------
        footnote_block = ""
        if self.table_footnote:
            footnote_block = f"\\caption*{{{_escape_latex(self.table_footnote)}}}\n"

        # ------------------------------------------------------------------
        # Assemble final LaTeX code
        # ------------------------------------------------------------------
        latex_code = f"""% Required packages:
% \\usepackage{{booktabs}}
% \\usepackage{{caption}}

\\begin{{table}}[ht]
\\centering
{caption_block}\\begin{{tabular}}{{{colspec}}}
{tabular}
\\end{{tabular}}
{footnote_block}\\end{{table}}"""

        return latex_code

    def view_html(self, browser: str | None = None) -> str:
        """Generate HTML and open in specified or default browser.

        Creates a temporary HTML file and opens it in the browser.
        The temporary file is cleaned up after a short delay to allow
        the browser to load it.

        Parameters:
            browser: Browser to use. Options (macOS): 'Chrome', 'Safari', 'Orion'.
                     If None, uses system default browser.

        Returns:
            Path to the temporary HTML file

        Example:
            >>> df.style().highlight_max(...).view_html()  # Default browser
            >>> df.style().highlight_max(...).view_html(browser='Chrome')  # Chrome
        """
        import tempfile
        import webbrowser
        import os
        import time
        from pathlib import Path

        # Browser command templates for macOS
        browser_command_templates = {
            'Chrome': 'open -a "/Applications/Google Chrome.app" %s',
            'Safari': 'open -a "/Applications/Safari.app" %s',
            'Orion': 'open -a "/Applications/Orion.app" %s',
        }

        html_file_path = None
        temp_file_object = None

        try:
            # Create temporary file
            temp_file_object = tempfile.NamedTemporaryFile(
                suffix=".html",
                delete=False,
                mode='w',
                encoding='utf-8'
            )
            html_file_path = temp_file_object.name

            # Generate and write HTML
            html = self.to_html()
            temp_file_object.write(html)
            temp_file_object.close()

            # Create file URL
            file_url = Path(html_file_path).as_uri()

            # Open in browser
            if browser and browser in browser_command_templates:
                # Use specific browser
                command_template = browser_command_templates[browser]
                try:
                    browser_controller = webbrowser.get(command_template)
                    browser_controller.open_new_tab(file_url)
                    print(f"✓ Opened in {browser}")
                except (FileNotFoundError, webbrowser.Error) as e:
                    print(f"Warning: Could not open {browser}. Using default browser instead.")
                    print(f"  Details: {e}")
                    webbrowser.open_new_tab(file_url)
            else:
                # Use system default browser
                webbrowser.open_new_tab(file_url)
                if browser:
                    print(f"Note: '{browser}' not in configured browsers. Using system default.")
                else:
                    print("✓ Opened in system default browser")

            # Return the path (will be cleaned up after delay)
            return html_file_path

        except Exception as e:
            print(f"Error opening HTML in browser: {e}")
            if html_file_path:
                print(f"HTML saved to: {html_file_path}")
                return html_file_path
            raise

        finally:
            # Clean up temporary file after delay
            if html_file_path and os.path.exists(html_file_path):
                # Schedule cleanup in a separate thread to not block
                def cleanup():
                    time.sleep(1.5)  # Wait for browser to load the file
                    try:
                        os.remove(html_file_path)
                    except OSError:
                        pass  # File already deleted or in use

                import threading
                cleanup_thread = threading.Thread(target=cleanup, daemon=True)
                cleanup_thread.start()

    def show(self) -> None:
        """Generate HTML and open in the system default browser.

        Cross-platform: works on macOS, Linux (including Snap-packaged Firefox
        on Ubuntu 22.04+), and Windows.

        On Linux, the temp file is written to the home directory because
        Snap-sandboxed browsers cannot access /tmp/. The file persists until
        manually deleted. On macOS and Windows, the file is written to the
        system temp directory and cleaned up by the OS on reboot.

        Example:
            >>> df.style().highlight_max(...).show()
        """
        import platform
        import tempfile
        import time
        import webbrowser
        from pathlib import Path

        html = self.to_html()
        system = platform.system()

        if system == "Linux":
            # Snap-packaged Firefox (Ubuntu 22.04+) cannot access /tmp/.
            # Home directory is accessible from the Snap sandbox.
            # Note: file is not auto-cleaned; persists until manually removed.
            tmp_dir = Path.home()
        else:
            # macOS: /tmp/ works fine (not Snap-sandboxed).
            # Windows: %TEMP% is user-owned, accessible to all browsers.
            tmp_dir = Path(tempfile.gettempdir())

        timestamp = int(time.time())
        tmp_path = tmp_dir / f"polarise_preview_{timestamp}.html"
        tmp_path.write_text(html, encoding="utf-8")

        webbrowser.open_new_tab(tmp_path.as_uri())

    def _repr_html_(self) -> str:
        """Return HTML representation for Jupyter notebook display.

        This method is automatically called by Jupyter notebooks to display
        the styled table inline. Just type the styled object at the end of
        a cell to see it rendered.

        Returns:
            HTML string for rendering

        Example:
            >>> # In Jupyter notebook:
            >>> df.style().highlight_max(in_col='price')  # Auto-displays!
            >>> # No need to call .show() or .view_html()
        """
        return self.to_html()
