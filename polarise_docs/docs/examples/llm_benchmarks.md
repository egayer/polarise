# LLM Benchmarks

Performance metrics for leading large language models across standardised benchmarks.

```python
from examples.datasets import get_llm_benchmarks
df = get_llm_benchmarks()
```

---

### Multi-column gradient

```python
(df.style()
   .gradient(["MMLU", "HumanEval", "GPQA"], cmap="viridis")
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

```python
(df.style()
   .gradient_divergent("Cost_per_1M", center=15.0, cmap="vik")
   .bar("Context_k", fill="steelblue")
   .fashion_zebra()
   .title("Cost vs Context Window")
   .show()
 )
```

{{ read_html('snippets/examples_llm_ex3.html') }}
