# Wellbeing

National wellbeing indicators: life expectancy, healthcare spending, life satisfaction, and work hours.

```python
from polarise.datasets import get_wellbeing_data
df = get_wellbeing_data()
```

---

### Wellbeing heatmap

```python
(df.style()
   .heat_map(["Life_Expectancy", "Healthcare_Pct_GDP", "Life_Satisfaction"], cmap="mint")
   .fashion_minimal()
   .title("Wellbeing Indicators by Country")
   .show()
 )
```

{{ read_html('snippets/examples_wellbeing_ex1.html') }}

---

### Best and worst life expectancy

```python
(df.style()
   .highlight_max("Life_Expectancy", fill="lightgreen")
   .highlight_min("Life_Expectancy", fill="lightblue")
   .gradient("Life_Satisfaction", cmap="peach")
   .fashion_grid()
   .show()
 )
```

{{ read_html('snippets/examples_wellbeing_ex2.html') }}

---

### Life expectancy vs work hours

```python
(df.style()
   .bar("Life_Expectancy", fill="steelblue")
   .bar("Work_Hours_Year", fill="#FF6347")
   .fashion_compact()
   .title("Life Expectancy vs Work Hours")
   .footnote("Longer bars = higher values. Red = more work hours.")
   .show()
 )
```

{{ read_html('snippets/examples_wellbeing_ex3.html') }}
