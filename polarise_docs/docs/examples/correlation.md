# Correlation Matrix

`heat_map()` is a natural fit for correlation matrices — the symmetric structure and [-1, 1] value range map perfectly onto a divergent colormap, making strong positive and negative correlations immediately visible.

This example uses Fisher's Iris dataset: 150 samples across 3 species, with 4 numeric features (sepal/petal length and width).

```python
import polars as pl
import polarise
from polarise.datasets import get_iris_data
df = get_iris_data()

corr_df = df[:, :-1].corr(label='features').with_columns(
    pl.col(pl.Float64).round(2)
)
```

---

### Correlation matrix

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="CET_L19" · built-in or colorcet }</span>

```python
(corr_df.style()
        .heat_map(exclude='features', cmap='CET_L19')
        .footnote('source : UCI Machine Learning Repository — Fisher\'s Iris dataset')
        .fashion_grid()
        .show()
 )
```

{{ read_html('snippets/examples_correlation_ex1.html') }}
