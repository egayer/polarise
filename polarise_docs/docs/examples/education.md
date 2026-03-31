# PISA Score

OECD PISA 2022 scores measuring 15-year-olds' performance in reading, mathematics, and science.

```python
from polarise.datasets import get_education_data
df = get_education_data()
```

---

### Heatmap across all scores

```python
(df.style()
   .heat_map(["Reading", "Math", "Science"], cmap="mint")
   .fashion_scientific()
   .caption("Table 1: OECD PISA 2022 Scores by Country")
   .show()
 )
```

{{ read_html('snippets/examples_education_ex1.html') }}

---

### Best and worst math scores

```python
(df.style()
   .highlight_max("Math", fill="gold")
   .highlight_min("Math", fill="lightblue")
   .gradient("GDP_per_capita", cmap="blues_2")
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
   .bar("Reading").bar("Math").bar("Science")
   .fashion_compact()
   .title("PISA Scores — Bar View")
   .show()
 )
```

{{ read_html('snippets/examples_education_ex3.html') }}
