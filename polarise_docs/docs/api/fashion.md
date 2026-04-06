# Fashion Presets

Fashion presets control the overall table appearance: borders, spacing, fonts, and background.
Apply one fashion per table — the last call wins.

Most fashion methods take no parameters. The exception is `fashion_zebra`, which accepts optional row colours — see below. All return a new `Styler`.

---

<a id="fashion_grid"></a>

**`fashion_grid()`**

Clean white table with visible grid lines. Excel-like appearance. Good default for data exploration.

```python
df.style().gradient("Math", cmap="Blues 2").fashion_grid().show()
```

{{ read_html('snippets/api_fashion_grid_ex1.html') }}

---

<a id="fashion_zebra"></a>

**`fashion_zebra(fill1=None, fill2=None)`**

Alternating row colours, no grid lines. Improves readability for wide tables.

- **`fill1`** `str | None`, default `"white"` — Colour for odd rows
- **`fill2`** `str | None`, default `"#f2f2f2"` — Colour for even rows

```python
df.style().gradient("Math", cmap="Blues 2").fashion_zebra().show()
```

{{ read_html('snippets/api_fashion_zebra_ex1.html') }}

```python
df.style().gradient("Math", cmap="Blues 2").fashion_zebra(fill1="white", fill2="#e8f4f8").show()
```

{{ read_html('snippets/api_fashion_zebra_ex2.html') }}

---

<a id="fashion_raw"></a>

**`fashion_raw()`**

Minimal styling that mimics Polars' default print output. No background colours or borders.

```python
df.style().gradient("Math", cmap="Blues 2").fashion_raw().show()
```

{{ read_html('snippets/api_fashion_raw_ex1.html') }}

---

<a id="fashion_scientific"></a>

**`fashion_scientific()`**

Publication-style booktabs table: top/bottom rules, mid-rule below header, no vertical lines.
Pair with `.caption()` for a proper figure caption.

```python
df.style().gradient("Math", cmap="Blues 2").fashion_scientific().show()
```

{{ read_html('snippets/api_fashion_scientific_ex1.html') }}

---

<a id="fashion_minimal"></a>

**`fashion_minimal()`**

Clean, borderless table with subtle header styling. Good for dashboards and web embedding.

```python
df.style().gradient("Math", cmap="Blues 2").fashion_minimal().show()
```

{{ read_html('snippets/api_fashion_minimal_ex1.html') }}

---

<a id="fashion_compact"></a>

**`fashion_compact()`**

Tight row spacing to display more data in less space. Useful for dense numeric tables.

```python
df.style().gradient("Math", cmap="Blues 2").fashion_compact().show()
```

{{ read_html('snippets/api_fashion_compact_ex1.html') }}

---

<a id="fashion_presentation"></a>

**`fashion_presentation()`**

Spacious layout with large fonts and high contrast. Designed for slides and presentations.

```python
df.style().gradient("Math", cmap="Blues 2").fashion_presentation().show()
```

{{ read_html('snippets/api_fashion_presentation_ex1.html') }}
