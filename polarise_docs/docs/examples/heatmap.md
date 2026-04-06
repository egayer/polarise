# Heatmap

Monthly temperature statistics (average, max, min) across all months of the year — a compact dataset ideal for visualising patterns with `heat_map()`.

**Columns:** Month (str), January → December (f64, °C)

```python
import polars as pl
import polarise
from polarise.datasets import get_temperature_stats_data
df = get_temperature_stats_data()
```

---

### Orange-Yellow colormap

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="OrYel" · colorspace }</span>

```python
(df.style()
   .heat_map(exclude='Month', cmap='OrYel_r')
   .footnote('source : en.climate-data.org')
   .fashion_grid()
   .show()
 )
```

{{ read_html('snippets/examples_heatmap_ex1.html') }}

---

### Blue-Coral colormap

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="CET_D11" · built-in or colorcet }</span>

```python
(df.style()
   .heat_map(exclude='Month', cmap='CET_D11')
   .footnote('source : en.climate-data.org')
   .fashion_grid()
   .show()
 )
```

{{ read_html('snippets/examples_heatmap_ex2.html') }}
