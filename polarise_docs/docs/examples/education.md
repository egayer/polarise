# PISA Score

OECD PISA 2022 scores measuring 15-year-olds' performance in reading, mathematics, and science.

```python
import polars as pl
import polarise
from polarise.datasets import get_education_data
df = get_education_data()
```

---

### Heatmap across all scores

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="Mint" · colorspace }</span>

```python
(df.style()
   .heat_map(["Reading", "Math", "Science"], cmap="Mint")
   .fashion_scientific()
   .caption("Table 1: OECD PISA 2022 Scores by Country")
   .show()
 )
```

{{ read_html('snippets/examples_education_ex1.html') }}

---

### Best and worst math scores

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="blues" · built-in }</span>

```python
(df.style()
   .highlight_max("Math", fill="gold")
   .highlight_min("Math", fill="alert_orange")
   .gradient("GDP_per_capita", cmap="blues")
   .fashion_minimal()
   .title("Math Performance vs Wealth")
   .show()
 )
```

{{ read_html('snippets/examples_education_ex2.html') }}

---

### Bar view across subjects

```python
(df.style()
   .bar("Reading").bar("Math",fill='gold').bar("Science", fill='orange')
   .fashion_compact()
   .title("PISA Scores — Bar View")
   .show()
 )
```

{{ read_html('snippets/examples_education_ex3.html') }}
