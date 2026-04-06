# Air Quality

Air quality metrics for major world cities: particulate matter, nitrogen dioxide, ozone, and AQI.

```python
import polars as pl
import polarise
from polarise.datasets import get_air_quality_data
df = get_air_quality_data()
```

---

### AQI gradient

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="CET_D12" · built-in or colorcet }</span>

```python
(df.style()
   .gradient("AQI", cmap="CET_D12")
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

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="managua_r" · built-in or cmcrameri }</span>

```python
(df.style()
   .gradient_divergent("Change_vs_2015", center=5.0, cmap="managua_r")
   .bar("AQI", fill="lightgreen")
   .fashion_zebra()
   .title("Air Quality Change Since 2015")
   .show()
 )
```

{{ read_html('snippets/examples_airquality_ex3.html') }}
