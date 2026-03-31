# Getting Started

## Installation

```bash
pip install polarise
```

## Basic Usage

Import polarise once to register the `.style()` method on `pl.DataFrame`:

```python
import datetime as dt
import polars as pl
import polarise

df = pl.DataFrame({
    "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
    "birthdate": [
        dt.date(1997, 1, 10),
        dt.date(1985, 2, 15),
        dt.date(1983, 3, 22),
        dt.date(1981, 4, 30),
    ],
    "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
    "height": [1.56, 1.77, 1.65, 1.75],  # (m)
})

df.style().gradient("height").show()
```

{{ read_html('snippets/gs_basic.html') }}

## Method Chaining

Every styling method returns a new `Styler` — chain as many as you like:

```python
(df.style()
   .gradient("height", cmap="plasma")
   .highlight_max("birthdate", fill="gold")
   .fashion_minimal()
   .title("A polars DataFrame")
   .show()
)
```

{{ read_html('snippets/gs_chaining.html') }}

## Scope: `column` vs `table`

Many methods accept a `scope` parameter controlling how min/max values are computed:

| `scope` | Min/max computed per… | Use when… |
|---------|----------------------|-----------|
| `"column"` (default) | Each column independently | Columns have different scales |
| `"table"` | All selected columns together | Comparing columns on the same scale |

```python
# Column scope: each column coloured relative to itself
df.style().gradient(["A", "B", "C"], scope="column")

# Table scope: all columns share the same colour scale
df.style().gradient(["A", "B", "C"], scope="table")
```

With `scope="table"`, `height` and `weight` share the same colour scale — values are compared across both columns:

```python
df.style().gradient(["height", "weight"], scope="table", cmap="plasma").show()
```

{{ read_html('snippets/gs_scope_table.html') }}

## Immutability

`Styler` is immutable. Every method returns a **new** `Styler` — the original is unchanged.
This makes chaining safe and predictable:

```python
base = df.style().gradient("revenue")
v1 = base.fashion_minimal()
v2 = base.fashion_scientific()
# v1 and v2 are independent — base is untouched
```

## Rendering

| Method | Output |
|--------|--------|
| `.show()` | [Opens HTML in default browser](../api/display_export/#show) |
| `.to_html()` | Returns HTML string |
| `.to_html("report.html")` | Saves HTML to file |
| `.to_latex()` | Returns LaTeX booktabs table |
| `display(df.style()...)` | Renders inline in Jupyter |

## Display Limits

<span style="color: red;">By default, Polarise limits rendering to 500 rows × 500 columns (max 250,000 cells) to prevent browser slowdowns. To override:</span>

```python
df.style(max_rows=2000, max_cols=100).show()
```
