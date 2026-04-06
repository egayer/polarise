# Tutorial

This tutorial builds a styled table step by step, adding one feature at a time.
We use the Big Tech financials dataset throughout.

```python
import polars as pl
import polarise

df = pl.DataFrame({
    "Company":     ["Apple", "Microsoft", "Google", "Amazon", "Meta"],
    "Revenue":     [383.3,   211.9,       307.4,    574.8,    134.9],
    "Profit":      [ 97.0,    72.4,        73.8,     30.4,     39.1],
    "Growth":      [  7.8,     6.9,         8.7,     11.8,     16.4],
    "Employees_k": [  161,     221,         182,     1541,       67],
})
```

---

## Step 1 — Render the raw table

Just calling `.style()` renders a plain table:

```python
df.style().show()
```

{{ read_html('snippets/tutorial_step1.html') }}

---

## Step 2 — Add a gradient

Apply a sequential colormap to the Revenue column:

```python
(df.style()
   .gradient("Revenue", cmap="CET_L19")
   .show()
 )
```

{{ read_html('snippets/tutorial_step2.html') }}

---

## Step 3 — Highlight the best profit

Chain a `highlight_max` on top of the gradient:

```python
(df.style()
   .gradient("Revenue", cmap="CET_L19")
   .highlight_max("Profit", fill="gold")
   .show()
 )
```

{{ read_html('snippets/tutorial_step3.html') }}

---

## Step 4 — Apply a fashion preset

Replace the default style with `fashion_minimal` for a cleaner look:

```python
(df.style()
   .gradient("Revenue", cmap="CET_L19")
   .highlight_max("Profit", fill="gold")
   .fashion_minimal()
   .show()
 )
```

{{ read_html('snippets/tutorial_step4.html') }}

---

## Step 5 — Add a title and footnote

```python
(df.style()
   .gradient("Revenue", cmap="CET_L19")
   .highlight_max("Profit", fill="gold")
   .fashion_minimal()
   .title("Big Tech Financials", subtitle="FY 2023 — Revenue in $B")
   .footnote("Source: Company annual reports.")
   .show()
 )
```

{{ read_html('snippets/tutorial_step5.html') }}

---

## Step 6 — Format the numbers

Apply format strings to clean up the display:

```python
(df.style()
   .gradient("Revenue", cmap="CET_L19")
   .highlight_max("Profit", fill="gold")
   .fashion_minimal()
   .title("Big Tech Financials", subtitle="FY 2023 — Revenue in $B")
   .footnote("Source: Company annual reports.")
   .format({"Revenue": "{:.0f}B", "Growth": "{:+.1f}%"})
   .show()
 )
```

{{ read_html('snippets/tutorial_step6.html') }}

---

## What's next?

- Browse the [API Reference](api/highlighting.md) for all available methods
- See [Examples](examples/finance.md) for more complete use cases
- Check [Colors & Colormaps](colors.md) for the full list of available `cmap` values
