# Big Tech Finance

Big Tech company financial data for FY 2023 — revenue, profit, growth rate, and headcount.

```python
import sys; sys.path.insert(0, "../")
import polars as pl
import polarise
from polarise.datasets import get_finance_data
df = get_finance_data()
```

---

### Revenue gradient

Visualise revenue distribution with a sequential colormap:

```python
(df.style()
   .gradient("Revenue", cmap="lapaz")
   .fashion_minimal()
   .title("Revenue Distribution")
   .show()
 )
```

{{ read_html('snippets/examples_finance_ex1.html') }}

---

### Highlight best performer + bar chart

```python
(df.style()
   .highlight_max("Profit", fill="gold")
   .bar("Revenue", fill="steelblue")
   .fashion_grid()
   .show()
 )
```

{{ read_html('snippets/examples_finance_ex2.html') }}

---

### Cross-column condition + formatting

Highlight revenue for companies with growth above 12%, and format numbers:

```python
(df.style()
   .highlight_when("Revenue", when=pl.col("Growth") > 12, then_fill="lightgreen")
   .format({"Revenue": "{:.0f}B", "Growth": "{:+.1f}%"})
   .fashion_zebra()
   .title("High-Growth Companies", subtitle="Green = Growth > 12%")
   .show()
 )
```

{{ read_html('snippets/examples_finance_ex3.html') }}
