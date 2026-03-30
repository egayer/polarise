# Polarise

*Style your data to explore. Style your results to present.*

**A Polars-native DataFrame styling tool for HTML visualization**

- Fast, expressive styling with a clean, chainable API
- Turn Polars DataFrames into clear, expressive HTML views
- Style using native Polars expressions
- Built for data inspection, debugging, and exploration
- Ready for reports, presentations, and sharing

---

## Installation

```bash
pip install polarise
```

---

## Quickstart

```python
import polars as pl
import polarise

df = pl.DataFrame({
    "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
    "region": ["EU", "EU", "US", "US"],
    "sales": [120, 85, 210, 250],
    "profit": [20, -15, 45, 55]
})

(
    df.style()
      .highlight_when(
          in_col="date",
          when=pl.col("profit") < 0,
          then_fill="alert_orange"
      )
      .gradient("sales", cmap="greens")
      .bar("profit", fill_pos="alert_green", fill_neg="alert_orange")
      .fashion_zebra()
      .show()
)
```

---

## Where Polarise fits

Polarise is inspired by the styling capabilities of pandas, but built for a Polars workflow.

While [Great Tables](https://posit-dev.github.io/great-tables/articles/intro.html) provides a rich and highly customizable system for building publication-quality tables, it comes with a more structured and declarative approach.

Polarise takes a different path:

- Lightweight and fast
- Fully aligned with Polars expressions
- Designed for quick inspection and clean presentation

It started as a simple tool to explore Polars DataFrames visually, and grew into a practical way to produce clear, styled HTML tables for reports and sharing — with optional LaTeX export for simple use cases.

**At a glance**

| Feature | pandas Styler | Great Tables | Polarise |
|---|---|---|---|
| Ecosystem | pandas | Polars | Polars |
| Philosophy | Flexible, built-in | Rich, declarative | Lightweight, expressive |
| Best for | General styling | Publication workflows | Inspection & quick presentation |
| Syntax | pandas-based | Table grammar | Polars expressions |
| Complexity | Medium | High | Low |
| Speed (iteration) | Medium | Slower | Fast |

---

## Documentation

Full documentation: https://egayer.github.io/polarise/

---

## License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.
