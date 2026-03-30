# Heatmap

Monthly temperature statistics (average, max, min) across all months of the year — a compact dataset ideal for visualising patterns with `heat_map()`.

**Columns:** Month (str), January → December (f64, °C)

```python
from examples.datasets import get_temperature_stats_data
df = get_temperature_stats_data()
```

---

### Orange-yellow colormap

```python
(df.style()
   .heat_map(exclude='Month', cmap='oryel_r')
   .footnote('source : en.climate-data.org')
   .fashion_grid()
   .show()
 )
```

{{ read_html('snippets/examples_heatmap_ex1.html') }}

---

### Blue-red colormap

```python
(df.style()
   .heat_map(exclude='Month', cmap='blue_red_2')
   .footnote('source : en.climate-data.org')
   .fashion_grid()
   .show()
 )
```

{{ read_html('snippets/examples_heatmap_ex2.html') }}
