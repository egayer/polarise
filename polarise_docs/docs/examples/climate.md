# Temperature Anomaly

Global climate indicators by decade: temperature anomaly, CO₂ concentration, sea level rise, and Arctic ice extent.

```python
from examples.datasets import get_climate_data
df = get_climate_data()
```

---

### Temperature anomaly (divergent gradient)

```python
(df.style()
   .gradient_divergent("Temp_Anomaly", center=0.0, cmap="vik")
   .fashion_minimal()
   .title("Global Temperature Anomaly by Decade")
   .footnote("Anomaly relative to 1951–1980 baseline. Source: NASA GISS.")
   .show()
 )
```

{{ read_html('snippets/examples_climate_ex1.html') }}

---

### CO₂ and temperature bars

```python
(df.style()
   .gradient("CO2_ppm", cmap="heat_2")
   .bar("Temp_Anomaly", fill_pos="#FF6347", fill_neg="steelblue")
   .fashion_grid()
   .title("CO₂ and Temperature Trends")
   .show()
 )
```

{{ read_html('snippets/examples_climate_ex2.html') }}

---

### Threshold alerts

```python
(df.style()
   .highlight_above("CO2_ppm", value=400)
   .highlight_below("Arctic_Ice_M_km2", value=6.0, fill="#FF6347")
   .fashion_scientific()
   .caption("Table 2: Climate indicators exceeding critical thresholds")
   .show()
 )
```

{{ read_html('snippets/examples_climate_ex3.html') }}
