# Air Quality

Air quality metrics for major world cities: particulate matter, nitrogen dioxide, ozone, and AQI.

```python
from polarise.datasets import get_air_quality_data
df = get_air_quality_data()
```

---

### AQI gradient

```python
(df.style()
   .gradient("AQI", cmap="heat_2")
   .fashion_minimal()
   .title("Air Quality Index by City")
   .show()
 )
```

{{ read_html('snippets/examples_airquality_ex1.html') }}

---

### WHO limit exceedances

```python
(df.style()
   .highlight_above("PM2_5", value=25.0, fill="#FF6347")
   .highlight_above("NO2", value=40.0, fill="orange")
   .fashion_grid()
   .title("Pollutants Exceeding WHO Limits")
   .footnote("WHO limit: PM2.5 < 25 μg/m³, NO2 < 40 μg/m³")
   .show()
 )
```

{{ read_html('snippets/examples_airquality_ex2.html') }}

---

### Change since 2015

```python
(df.style()
   .gradient_divergent("Change_vs_2015", center=0.0, cmap="vik")
   .bar("AQI", fill="steelblue")
   .fashion_zebra()
   .title("Air Quality Change Since 2015")
   .show()
 )
```

{{ read_html('snippets/examples_airquality_ex3.html') }}
