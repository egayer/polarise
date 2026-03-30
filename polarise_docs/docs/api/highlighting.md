# Highlighting

Highlighting methods colour specific cells based on conditions.
All highlighting methods accept `fill` (background colour) and `color` (text colour).
If `color` is omitted, contrast is computed automatically (black or white).

---

<a id="highlight_max"></a>

**`highlight_max(in_col, scope="column", color=None, fill="yellow", exclude=None)`**

Highlight the maximum value in each selected column.

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`scope`** `"column" | "table"`, default `"column"` — Compute max per column or across all selected columns
- **`color`** `str | None`, default `None` — Text colour (auto-contrast if None)
- **`fill`** `str`, default `"yellow"` — Background fill colour
- **`exclude`** `str | list | None`, default `None` — Columns to exclude when `in_col` is an expression

**Example:**

```python
df.style().highlight_max("Revenue").show()
```

{{ read_html('snippets/api_highlight_max_ex1.html') }}

---

<a id="highlight_min"></a>

**`highlight_min(in_col, scope="column", color=None, fill="lightblue", exclude=None)`**

Highlight the minimum value in each selected column.

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`scope`** `"column" | "table"`, default `"column"` — Compute min per column or across all selected columns
- **`color`** `str | None`, default `None` — Text colour (auto-contrast if None)
- **`fill`** `str`, default `"lightblue"` — Background fill colour
- **`exclude`** `str | list | None`, default `None` — Columns to exclude

**Example:**

```python
df.style().highlight_min("Profit").show()
```

{{ read_html('snippets/api_highlight_min_ex1.html') }}

---

<a id="highlight_above"></a>

**`highlight_above(in_col, value, inclusive=False, scope="column", color=None, fill="yellow")`**

Highlight values strictly above (or equal to, if `inclusive=True`) a threshold.

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`value`** `float` — Threshold value
- **`inclusive`** `bool`, default `False` — Include the threshold value itself
- **`scope`** `"column" | "table"`, default `"column"` — Unused for this method (kept for API consistency)
- **`color`** `str | None`, default `None` — Text colour
- **`fill`** `str`, default `"yellow"` — Background fill colour

**Example:**

```python
df.style().highlight_above("Growth", value=10.0).show()
```

{{ read_html('snippets/api_highlight_above_ex1.html') }}

---

<a id="highlight_below"></a>

**`highlight_below(in_col, value, inclusive=False, scope="column", color=None, fill="yellow")`**

Highlight values strictly below (or equal to, if `inclusive=True`) a threshold.

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`value`** `float` — Threshold value
- **`inclusive`** `bool`, default `False` — Include the threshold value itself
- **`scope`** `"column" | "table"`, default `"column"` — Unused for this method (kept for API consistency)
- **`color`** `str | None`, default `None` — Text colour
- **`fill`** `str`, default `"yellow"` — Background fill colour

**Example:**

```python
df.style().highlight_below("Profit", value=73).show()
```

{{ read_html('snippets/api_highlight_below_ex1.html') }}

---

<a id="highlight_equal"></a>

**`highlight_equal(in_col, value, color=None, fill="yellow")`**

Highlight cells whose value exactly equals the target.

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`value`** `float | str` — Target value
- **`color`** `str | None`, default `None` — Text colour
- **`fill`** `str`, default `"yellow"` — Background fill colour

**Example:**

```python
df.style().highlight_equal("Employees_k", value=182).show()
```

{{ read_html('snippets/api_highlight_equal_ex1.html') }}

---

<a id="highlight_between"></a>

**`highlight_between(in_col, low, high, scope="column", color=None, fill="yellow")`**

Highlight values within the range `[low, high]` (inclusive).

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`low`** `float` — Lower bound (inclusive)
- **`high`** `float` — Upper bound (inclusive)
- **`scope`** `"column" | "table"`, default `"column"` — Unused for this method
- **`color`** `str | None`, default `None` — Text colour
- **`fill`** `str`, default `"yellow"` — Background fill colour

**Example:**

```python
df.style().highlight_between("Revenue", low=200.0, high=400.0).show()
```

{{ read_html('snippets/api_highlight_between_ex1.html') }}

---

<a id="highlight_identical"></a>

**`highlight_identical(in_col, color=None, fill="yellow")`**

Highlight rows where all specified columns share the same value.
Unlike other highlight methods, this operates **row-wise** across columns.

- **`in_col`** `list[str]` — Columns to compare (must be a list)
- **`color`** `str | None`, default `None` — Text colour
- **`fill`** `str`, default `"yellow"` — Background fill colour

**Example:**

```python
df.style().highlight_identical(["Col_A", "Col_B"]).show()
```

{{ read_html('snippets/api_highlight_identical_ex1.html') }}

---

<a id="highlight_when"></a>

**`highlight_when(in_col, when, then_fill="yellow", then_color=None, exclude=None)`**

Highlight cells in `in_col` when a Polars expression `when` evaluates to `True`.
The expression can reference **any** column, enabling cross-column conditions.

- **`in_col`** `str | list | Expr` — Column(s) to colour
- **`when`** `pl.Expr` — Boolean Polars expression
- **`then_fill`** `str`, default `"yellow"` — Background colour when condition is True
- **`then_color`** `str | None`, default `None` — Text colour when condition is True
- **`exclude`** `str | list | None`, default `None` — Columns to exclude

**Example:**

```python
import polars as pl

# Highlight Revenue where Growth > 15%
df.style().highlight_when(
    "Revenue",
    when=pl.col("Growth") > 15,
    then_fill="lightgreen"
).show()
```

{{ read_html('snippets/api_highlight_when_ex1.html') }}
