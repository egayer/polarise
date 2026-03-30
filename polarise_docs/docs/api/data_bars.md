# Data Bars

<a id="bar"></a>

**`bar(in_col, scope="column", color=None, fill="steelblue", fill_pos=None, fill_neg=None, exclude=None)`**

Add in-cell bar charts using CSS gradients. Bar width is proportional to the value.
For signed data, use `fill_pos` and `fill_neg` to colour positive and negative bars differently.

- **`in_col`** `str | list | Expr` — Column(s) to apply to
- **`scope`** `"column" | "table"`, default `"column"` — Compute max per column or across all selected
- **`color`** `str | None`, default `None` — Text colour
- **`fill`** `str`, default `"steelblue"` — Bar colour (used when `fill_pos`/`fill_neg` are not set)
- **`fill_pos`** `str | None`, default `None` — Bar colour for positive values (enables signed mode)
- **`fill_neg`** `str | None`, default `None` — Bar colour for negative values
- **`exclude`** `str | list | None`, default `None` — Columns to exclude

**Example — standard bars:**

```python
df.style().bar("Revenue").show()
```

{{ read_html('snippets/api_bar_ex1.html') }}

**Example — signed bars (positive/negative):**

```python
df.style().bar(
    "Temp_Anomaly",
    fill_pos="steelblue",
    fill_neg="#FF6347"
).show()
```

{{ read_html('snippets/api_bar_signed_ex1.html') }}
