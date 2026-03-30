"""HTML table generation engine.

This is the rendering layer that evaluates all styles and generates the final HTML.
"""

from typing import Any
import polars as pl
from ..specs import StyleSpec
from ..selectors import resolve_columns
from ..engines.condition import eval_condition, eval_highlight_identical
from ..engines.mapper import eval_mapper, eval_bar
from ..utils.colors import normalize_color
from ..utils.contrast import auto_text_color
from .css import get_fashion_css


def _bar_widths(x, max_absolute):
    """Compute bar widths for signed bar rendering.

    Uses maximum absolute value as reference.
    Each direction (left/right) gets 50% of cell width.
    Bar length = (value / max_absolute) * 50%

    Parameters:
        x: Cell value
        max_absolute: Maximum absolute value (reference for 100%)

    Returns:
        Tuple of (pos_width, neg_width) as normalized values in [0, 0.5]
        - pos_width: Width for positive bar (0-50%)
        - neg_width: Width for negative bar (0-50%)

    Examples:
        >>> # max_absolute = 45
        >>> _bar_widths(45, 45)  # (0.5, 0.0) - full right half
        >>> _bar_widths(20, 45)  # (0.222, 0.0) - 22.2% of cell, right side
        >>> _bar_widths(-15, 45) # (0.0, 0.167) - 16.7% of cell, left side
    """
    if x is None:
        return 0.0, 0.0

    if max_absolute == 0:
        return 0.0, 0.0

    if x >= 0:
        # Positive: extends right from center
        # Width is (value / max_absolute) * 50%
        pos = (x / max_absolute) * 0.5
        return pos, 0.0
    else:
        # Negative: extends left from center
        # Width is (abs(value) / max_absolute) * 50%
        neg = (abs(x) / max_absolute) * 0.5
        return 0.0, neg


def generate_html(
    df: pl.DataFrame,
    styles: list[StyleSpec],
    hidden_axes: set[str],
    fashion: str,
    truncation_info: dict,
    null_cell_color: str,
    null_text_color: str,
    table_title: str | None = None,
    table_subtitle: str | None = None,
    table_caption: str | None = None,
    table_footnote: str | None = None,
    show_info: bool = False,
    info_name: str | None = None
) -> str:
    """Generate complete HTML table with all styling applied.

    This is the orchestration layer that:
    1. Pre-evaluates all style specs
    2. Builds HTML table structure
    3. Applies cell-by-cell styling
    4. Handles formatting

    Parameters:
        df: DataFrame to render (already truncated)
        styles: List of style specifications
        hidden_axes: Set of axes to hide ('index', 'columns')
        fashion: Fashion name ('grid', 'zebra')
        truncation_info: Truncation metadata
        null_cell_color: Background color for null cells
        null_text_color: Text color for null cells
        table_title: Optional title to display above table
        table_subtitle: Optional subtitle to display below title
        table_caption: Optional caption to display above table (scientific convention)
        table_footnote: Optional footnote to display below table
        show_info: Whether to show dataframe info (name and shape)
        info_name: Optional dataframe name for info display

    Returns:
        Complete HTML string
    """
    # Identify numeric columns for right alignment
    numeric_cols = set()
    for col in df.columns:
        dtype = df[col].dtype
        if dtype.is_numeric():
            numeric_cols.add(col)

    html_parts = []

    # HTML header
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html>")
    html_parts.append("<head>")
    html_parts.append('<meta charset="UTF-8">')
    html_parts.append("<style>")
    html_parts.append(get_fashion_css(fashion))
    # Add CSS for container centering, title, subtitle, info, caption, and footnote
    html_parts.append("""
body {
    display: flex;
    justify-content: center;
    padding: 20px;
}
.pl-container {
    display: inline-block;
}
.pl-title {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 4px;
    color: #333;
    text-align: left;
}
.pl-subtitle {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 14px;
    font-weight: 400;
    margin-bottom: 12px;
    color: #666;
    text-align: left;
}
.pl-info {
    font-family: 'Courier New', Courier, monospace;
    font-size: 12px;
    margin-bottom: 12px;
    color: #555;
    text-align: left;
}
.pl-caption {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 14px;
    margin-top: 6px;
    margin-bottom: 8px;
    color: #000;
    text-align: left;
}
.pl-footnote {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 12px;
    margin-top: 12px;
    color: #666;
    font-style: italic;
    text-align: left;
}
""")
    html_parts.append("</style>")
    html_parts.append("</head>")
    html_parts.append("<body>")
    html_parts.append('<div class="pl-container">')

    # Title
    if table_title:
        html_parts.append(f'<div class="pl-title">{_escape_html(table_title)}</div>')

    # Subtitle
    if table_subtitle:
        html_parts.append(f'<div class="pl-subtitle">{_escape_html(table_subtitle)}</div>')

    # Info (dataframe name and shape)
    if show_info:
        info_lines = []
        if info_name:
            info_lines.append(f'{_escape_html(info_name)}:')
        info_lines.append(f'shape: ({len(df)}, {len(df.columns)})')
        html_parts.append(f'<div class="pl-info">{"<br>".join(info_lines)}</div>')

    # Truncation warning
    if truncation_info['rows_truncated'] or truncation_info['cols_truncated']:
        orig_r = truncation_info['original_rows']
        orig_c = truncation_info['original_cols']
        final_r = truncation_info['final_rows']
        final_c = truncation_info['final_cols']
        html_parts.append(
            f'<div class="pl-warning">'
            f'⚠️ DataFrame truncated for display: '
            f'{orig_r}×{orig_c} → {final_r}×{final_c}'
            f'</div>'
        )

    # Caption (scientific convention: above the table)
    if table_caption:
        html_parts.append(f'<div class="pl-caption">{_escape_html(table_caption)}</div>')

    # Pre-evaluate all styles
    style_cache = _evaluate_styles(df, styles)

    # Get formatters
    formatters = _get_formatters(styles)

    # Identify columns with bars (for header alignment)
    bar_columns = set()
    for key, style_data in style_cache.items():
        if style_data['type'] == 'bar':
            _, col = key
            bar_columns.add(col)

    # Start table
    html_parts.append('<table class="pl-table">')

    # Column headers
    if "columns" not in hidden_axes:
        html_parts.append("<thead><tr>")
        if "index" not in hidden_axes:
            html_parts.append("<th></th>")  # Empty cell for index column
        for col in df.columns:
            # Add class if this column has bars (for right alignment)
            if col in bar_columns:
                html_parts.append(f'<th class="pl-bar-col">{_escape_html(str(col))}</th>')
            else:
                html_parts.append(f"<th>{_escape_html(str(col))}</th>")
        html_parts.append("</tr></thead>")

    # Table body
    html_parts.append("<tbody>")
    for row_idx in range(len(df)):
        html_parts.append("<tr>")

        # Row index
        if "index" not in hidden_axes:
            html_parts.append(f"<td>{row_idx}</td>")

        # Data cells
        for col in df.columns:
            value = df[col][row_idx]

            # Compute cell style
            cell_style, cell_class, needs_span = _compute_cell_style(
                row_idx,
                col,
                value,
                style_cache,
                null_cell_color,
                null_text_color,
                numeric_cols
            )

            # Format value
            formatted_value = _format_value(value, col, formatters)

            # Wrap in span if needed (for bar cells)
            if needs_span:
                formatted_value = f"<span>{formatted_value}</span>"

            # Render cell
            if cell_style and cell_class:
                html_parts.append(f'<td class="{cell_class}" style="{cell_style}">{formatted_value}</td>')
            elif cell_style:
                html_parts.append(f'<td style="{cell_style}">{formatted_value}</td>')
            elif cell_class:
                html_parts.append(f'<td class="{cell_class}">{formatted_value}</td>')
            else:
                html_parts.append(f'<td>{formatted_value}</td>')

        html_parts.append("</tr>")
    html_parts.append("</tbody>")

    # Close table
    html_parts.append("</table>")

    # Footnote
    if table_footnote:
        html_parts.append(f'<div class="pl-footnote">{_escape_html(table_footnote)}</div>')

    html_parts.append("</div>")  # Close pl-container
    html_parts.append("</body>")
    html_parts.append("</html>")

    return "\n".join(html_parts)


def _evaluate_styles(df: pl.DataFrame, styles: list[StyleSpec]) -> dict:
    """Pre-evaluate all styles for performance.

    Returns a cache of evaluation results keyed by (spec_idx, column).
    """
    cache = {}

    for spec_idx, spec in enumerate(styles):
        if spec.kind == "highlight" and spec.condition:
            # Evaluate condition for each column
            cols = resolve_columns(df, spec.in_col, exclude=spec.exclude)
            for col in cols:
                mask = eval_condition(df, col, spec.condition, spec.scope, cols)
                cache[(spec_idx, col)] = {
                    'type': 'highlight',
                    'mask': mask,
                    'color': spec.color,
                    'fill': spec.fill
                }

        elif spec.kind == "gradient" and spec.mapper:
            # Evaluate mapper for each column
            cols = resolve_columns(df, spec.in_col, exclude=spec.exclude)
            for col in cols:
                colors = eval_mapper(df, col, spec.mapper, spec.scope, cols)
                cache[(spec_idx, col)] = {
                    'type': 'gradient',
                    'colors': colors,
                    'apply_fill': spec.params.get('apply_fill', True),  # Default True for backward compat
                    'apply_color': spec.params.get('apply_color', False)  # Default False
                }

        elif spec.kind == "bar":
            # Evaluate bar normalization for each column
            cols = resolve_columns(df, spec.in_col, exclude=spec.exclude)
            for col in cols:
                bar_data = eval_bar(df, col, spec.scope, cols)
                cache[(spec_idx, col)] = {
                    'type': 'bar',
                    'bar_data': bar_data,  # Dict with neg_extent, pos_extent, values
                    'color': spec.color,
                    'fill': spec.fill,
                    'fill_pos': spec.params.get('fill_pos'),
                    'fill_neg': spec.params.get('fill_neg')
                }

        elif spec.kind == "highlight_identical":
            # Evaluate identical highlighting
            cells = eval_highlight_identical(df, spec.in_col)
            cache[spec_idx] = {
                'type': 'highlight_identical',
                'cells': cells,
                'color': spec.color,
                'fill': spec.fill
            }

    return cache


def _get_formatters(styles: list[StyleSpec]) -> dict[str, str]:
    """Extract formatters from styles."""
    formatters = {}
    for spec in styles:
        if spec.kind == "format":
            formatters.update(spec.params.get("formatters", {}))
    return formatters


def _compute_cell_style(
    row_idx: int,
    col: str,
    value: Any,
    style_cache: dict,
    null_cell_color: str,
    null_text_color: str,
    numeric_cols: set[str]
) -> tuple[str, str, bool]:
    """Compute final CSS style for a cell.

    Applies all matching styles in order, with later styles taking precedence.

    Returns:
        Tuple of (css_style, cell_class, needs_span_wrap)
    """
    # Handle null values
    if value is None:
        bg = normalize_color(null_cell_color)
        txt = normalize_color(null_text_color)
        # Add numeric class even for null cells in numeric columns
        cell_class = "numeric" if col in numeric_cols else ""
        return f"background-color: {bg}; color: {txt};", cell_class, False

    css_parts = []
    background = None
    text_color = None
    cell_class = "numeric" if col in numeric_cols else ""
    needs_span = False

    # Apply styles in order
    for key, style_data in style_cache.items():
        if style_data['type'] == 'highlight':
            spec_idx, style_col = key
            if style_col == col:
                # Check if this cell matches the condition
                if style_data['mask'][row_idx]:
                    if style_data['fill']:
                        background = normalize_color(style_data['fill'])
                    if style_data['color']:
                        text_color = normalize_color(style_data['color'])

        elif style_data['type'] == 'gradient':
            spec_idx, style_col = key
            if style_col == col:
                # Get gradient color for this row
                gradient_color = style_data['colors'].get(row_idx)
                if gradient_color:
                    # Apply gradient to background if requested
                    if style_data.get('apply_fill', True):
                        background = gradient_color

                    # Apply gradient to text if requested
                    if style_data.get('apply_color', False):
                        text_color = gradient_color

        elif style_data['type'] == 'bar':
            spec_idx, style_col = key
            if style_col == col:
                bar_data = style_data['bar_data']
                max_absolute = bar_data['max_absolute']
                has_negative = bar_data['has_negative']
                has_positive = bar_data['has_positive']
                cell_value = bar_data['values'][row_idx]

                # Get colors (with custom overrides)
                fill_pos_color = style_data.get('fill_pos') or style_data['fill']
                fill_neg_color = style_data.get('fill_neg') or "indianred"
                bar_color = normalize_color(fill_pos_color)
                neg_color = normalize_color(fill_neg_color)

                # Skip rendering for None values
                if cell_value is None:
                    continue

                # Determine rendering mode based on data range
                if has_positive and not has_negative:
                    # POSITIVE-ONLY: Use linear-gradient from left
                    # Width = (value / max_absolute) * 100%
                    width = cell_value / max_absolute if max_absolute > 0 else 0.0
                    width = max(0.0, min(1.0, width))
                    width_pct = int(width * 100)

                    bar_style = (
                        f"linear-gradient(90deg, "
                        f"{bar_color} 0%, {bar_color} {width_pct}%, "
                        f"transparent {width_pct}%, transparent 100%)"
                    )
                    css_parts.append(f"background: {bar_style};")

                elif has_negative and not has_positive:
                    # NEGATIVE-ONLY: Use linear-gradient from right
                    # Width = (abs(value) / max_absolute) * 100%
                    width = abs(cell_value) / max_absolute if max_absolute > 0 else 0.0
                    width = max(0.0, min(1.0, width))
                    width_pct = int(width * 100)

                    bar_style = (
                        f"linear-gradient(90deg, "
                        f"transparent 0%, transparent {100 - width_pct}%, "
                        f"{neg_color} {100 - width_pct}%, {neg_color} 100%)"
                    )
                    css_parts.append(f"background: {bar_style};")

                else:
                    # MIXED: Use signed bars with CSS variables
                    # Each bar is (value / max_absolute) * 50% of cell width
                    pos_width, neg_width = _bar_widths(cell_value, max_absolute)

                    css_parts.append(f"--pos: {pos_width};")
                    css_parts.append(f"--neg: {neg_width};")
                    css_parts.append(f"--bar-color: {bar_color};")
                    css_parts.append(f"--bar-neg-color: {neg_color};")

                    # Mark as bar cell (append to existing classes)
                    cell_class = f"{cell_class} pl-bar".strip()
                    needs_span = True

                # Apply user-specified text color if provided
                if style_data['color']:
                    text_color = normalize_color(style_data['color'])

        elif style_data['type'] == 'highlight_identical':
            if (row_idx, col) in style_data['cells']:
                if style_data['fill']:
                    background = normalize_color(style_data['fill'])
                if style_data['color']:
                    text_color = normalize_color(style_data['color'])

    # Apply background color (not for bars, which use CSS variables)
    if background and "pl-bar" not in cell_class:
        css_parts.append(f"background-color: {background};")

        # Auto-calculate text color if not specified
        if text_color is None:
            text_color = auto_text_color(background)

    # Apply text color
    if text_color:
        css_parts.append(f"color: {text_color};")

    return " ".join(css_parts), cell_class, needs_span


def _format_value(value: Any, col: str, formatters: dict[str, str]) -> str:
    """Format cell value according to formatters.

    Parameters:
        value: Cell value
        col: Column name
        formatters: Dictionary of column -> format string

    Returns:
        Formatted string (HTML-escaped)
    """
    # Handle null
    if value is None:
        return '<em>null</em>'

    # Apply formatter if available
    if col in formatters:
        try:
            formatted = formatters[col].format(value)
        except Exception:
            # Fallback to string conversion if formatting fails
            formatted = str(value)
    else:
        formatted = str(value)

    return _escape_html(formatted)


def _escape_html(text: str) -> str:
    """Escape HTML special characters.

    Parameters:
        text: Text to escape

    Returns:
        HTML-escaped text
    """
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
