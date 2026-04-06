# Wellbeing

National wellbeing indicators: life expectancy, healthcare spending, life satisfaction, and work hours.

```python
import polars as pl
import polarise
from polarise.datasets import get_wellbeing_data
df = get_wellbeing_data()
```

---

### Wellbeing heatmap

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="hawaii" · built-in or cmcrameri }</span>

```python
(df.style()
   .heat_map(["Life_Expectancy", "Healthcare_Pct_GDP", "Life_Satisfaction"], cmap="hawaii")
   .fashion_minimal()
   .title("Wellbeing Indicators by Country")
   .show()
 )
```

{{ read_html('snippets/examples_wellbeing_ex1.html') }}

---

### Best and worst life expectancy

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="orange-to-purple" · built-in }</span>

```python
(df.style()
   .highlight_max("Life_Expectancy", fill="lightgreen")
   .highlight_min("Life_Expectancy", fill="lightblue")
   .gradient("Life_Satisfaction", cmap="orange-to-purple")
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
