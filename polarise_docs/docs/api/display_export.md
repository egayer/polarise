# Display & Export

---

<a id="title"></a>

**`title(title=None, subtitle=None)`**

Add a title and optional subtitle above the table.

- **`title`** `str | None`, default `None` — Main title text
- **`subtitle`** `str | None`, default `None` — Subtitle text (smaller, below title)

```python
df.style().title("Big Tech Financials", subtitle="FY 2023").show()
```

{{ read_html('snippets/api_title_ex1.html') }}

---

<a id="footnote"></a>

**`footnote(text)`**

Add footnote text below the table (smaller font, muted colour).

- **`text`** `str` — Footnote text

```python
df.style().footnote("Source: Company annual reports. Revenue in $B.").show()
```

{{ read_html('snippets/api_footnote_ex1.html') }}

---

<a id="caption"></a>

**`caption(text)`**

Add a caption above the table following scientific convention (e.g. "Table 1: ...").
Use with `fashion_scientific()` for publication-style tables.

- **`text`** `str` — Caption text

```python
df.style().caption("Table 1: Summary statistics").fashion_scientific().show()
```

{{ read_html('snippets/api_caption_ex1.html') }}

---

<a id="show_idx"></a>

**`show_idx()`**

Show the row index column (hidden by default).

No parameters.

```python
df.style().show_idx().show()
```

{{ read_html('snippets/api_show_idx_ex1.html') }}

---

<a id="hide_columns"></a>

**`hide_columns()`**

Hide the column header row. The data remains fully visible; only the `<thead>` row is suppressed.

No parameters.

```python
df.style().hide_columns().fashion_minimal().show()
```

{{ read_html('snippets/api_hide_columns_ex1.html') }}

---

<a id="show_info"></a>

**`show_info(name=None)`**

Display DataFrame metadata (name, shape) above the table.

- **`name`** `str | None`, default `None` — Optional dataset name to display

```python
df.style().show_info(name="finance").show()
```

{{ read_html('snippets/api_show_info_ex1.html') }}

---

<a id="to_html"></a>

**`to_html(path=None) -> str`**

Generate the styled HTML table as a string, or save to a file.

- **`path`** `str | None`, default `None` — If provided, writes HTML to this file path

**Returns:** HTML string.

```python
# Get HTML string
html = df.style().gradient("Revenue").to_html()

# Save to file
df.style().gradient("Revenue").to_html("output/report.html")
```

---

<a id="to_latex"></a>

**`to_latex(caption=None, label=None) -> str`**

Export the table as a LaTeX `tabular` environment using booktabs formatting.

- **`caption`** `str | None`, default `None` — Table caption (placed in `\caption{}`)
- **`label`** `str | None`, default `None` — Table label for cross-referencing (`\label{}`)

**Returns:** LaTeX string.

```python
latex = df.style().fashion_scientific().to_latex(
    caption="Big Tech financials",
    label="tab:finance"
)
print(latex)
```

> **Note:** Cell background colours are not exported to LaTeX. Only table structure and text formatting are preserved.

```latex
% Required packages:
% \usepackage{booktabs}
% \usepackage{caption}

\begin{table}[ht]
\centering
\caption{Big Tech financials}
\label{tab:finance}
\begin{tabular}{lrrrr}
\toprule
\textbf{Company} & \textbf{Revenue} & \textbf{Profit} & \textbf{Growth} & \textbf{Employees\_k} \\
\midrule
Apple & 383.3 & 97.0 & 7.8 & 161 \\
Microsoft & 211.9 & 72.4 & 6.9 & 221 \\
Google & 307.4 & 73.8 & 8.7 & 182 \\
Amazon & 574.8 & 30.4 & 11.8 & 1541 \\
Meta & 134.9 & 39.1 & 16.4 & 67 \\
\bottomrule
\end{tabular}
\end{table}
```

---

<a id="show"></a>

**`show() -> None`**

Open the rendered HTML table in the system default browser. Alias for `view_html()` with no arguments.

No parameters.

```python
df.style().gradient("Revenue").show()
```

> **Jupyter users:** You don't need `.show()`. polarise implements `_repr_html_()`, so styled tables render automatically when a `Styler` is the last expression in a cell.

---

<a id="view_html"></a>

**`view_html(browser=None) -> str`**

Open the rendered HTML table in a browser. Returns the path to the temporary HTML file.

- **`browser`** `str | None`, default `None` — Browser to use (macOS only): `"Chrome"`, `"Safari"`, or `"Orion"`. On other platforms the system default is always used.

**Returns:** Path to the temporary HTML file.

```python
df.style().gradient("Revenue").view_html()              # default browser
df.style().gradient("Revenue").view_html("Chrome")      # Chrome (macOS only)
```
