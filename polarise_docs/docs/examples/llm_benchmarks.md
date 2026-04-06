# LLM Benchmarks

Performance metrics for leading large language models across standardised benchmarks.

```python
import polars as pl
import polarise
from polarise.datasets import get_llm_benchmarks
df = get_llm_benchmarks()
```

---

### Multi-column gradient

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="imola" · cmcrameri }</span>

```python
(df.style()
   .gradient(["MMLU", "HumanEval", "GPQA"], cmap="imola")
   .fashion_minimal()
   .title("LLM Benchmark Scores")
   .show()
 )
```

{{ read_html('snippets/examples_llm_ex1.html') }}

---

### Highlight best in class

```python
(df.style()
   .highlight_max("MMLU")
   .highlight_max("HumanEval", fill="lightblue")
   .highlight_min("Cost_per_1M", fill="lightgreen")
   .fashion_grid()
   .title("Best in Class")
   .footnote("Cost per 1M tokens. Lower is better.")
   .show()
 )
```

{{ read_html('snippets/examples_llm_ex2.html') }}

---

### Cost vs context window

<span style="font-size: 0.8rem; font-family: monospace; color: #555555;">{ cmap="managua" · built-in or cmcrameri }</span>

```python
(df.style()
   .gradient_divergent("Cost_per_1M", center=15.0, cmap="managua")
   .bar("Context_k", fill="lightgreen")
   .fashion_zebra()
   .title("Cost vs Context Window")
   .show()
 )
```

{{ read_html('snippets/examples_llm_ex3.html') }}
