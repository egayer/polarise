"""
Generate all HTML snippet files for the polarise documentation site.

Run from polarise_docs/:
    python generate_snippets.py

Outputs to docs/snippets/*.html (overwrites existing files).
"""

import sys
import os
import re
import hashlib

# Add project root to path so we can import polarise and examples/datasets
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "examples"))

import datetime as dt
import polars as pl
import polarise  # noqa: F401 — registers .style() on pl.DataFrame

# Import datasets module (it's a script, not a package)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "datasets", os.path.join(ROOT, "examples", "datasets.py")
)
datasets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(datasets)

OUT = os.path.join(os.path.dirname(__file__), "docs", "snippets")
os.makedirs(OUT, exist_ok=True)


def _scope_css(css: str, prefix: str) -> str:
    """Prefix top-level .pl-* CSS selectors with a scope prefix.

    This raises snippet CSS specificity above MkDocs Material's
    .md-typeset table rules, so fashion styles are not overridden.
    Only prefixes .pl-* selectors that are NOT compound (e.g. th.pl-bar-col
    is left alone, but .pl-table is prefixed).
    """
    return re.sub(r'(?<![\w.])(\.pl-[\w-]+)', rf'{prefix} \1', css)


def extract_fragment(html: str) -> str:
    """Extract <style> block + <body> content from a full HTML document.

    Each snippet gets a unique CSS scope class derived from a hash of its CSS,
    so multiple snippets on the same page never override each other's styles.
    """
    style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    raw_css = style_match.group(1) if style_match else ""

    # Unique class per snippet — prevents CSS bleed between snippets on same page
    uid = "ps" + hashlib.md5(raw_css.encode()).hexdigest()[:8]
    scoped_css = _scope_css(raw_css, f".{uid}")

    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    body = body_match.group(1).strip() if body_match else html

    return f'<style>{scoped_css}</style>\n<div class="pol-snippet {uid}">{body}</div>'


def save(name: str, html: str) -> None:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(extract_fragment(html))
    print(f"  ✓ {name}")


# ── Color reference ────────────────────────────────────────────────────────────

def gen_color_reference():
    src = os.path.join(ROOT, "Documentation", "color_reference.html")
    with open(src, encoding="utf-8") as f:
        html = f.read()

    # Extract body content only — CSS lives in extra.css under .pol-color-ref
    # so no <style> tag is injected into the page content (which disrupts layout).
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    body = body_match.group(1).strip() if body_match else html

    # Remove the standalone-page .container wrapper div
    body = re.sub(r'<div\s+class="container">', '', body, count=1)
    if body.rstrip().endswith('</div>'):
        body = body.rstrip()[:-6].rstrip()

    fragment = f'<div class="pol-color-ref">{body}</div>'

    path = os.path.join(OUT, "color_reference_body.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(fragment)
    print("  ✓ color_reference_body.html")


# ── Home hero ──────────────────────────────────────────────────────────────────

def gen_home():
    df = pl.DataFrame({
        "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "region": ["EU", "EU", "US", "US"],
        "sales": [120, 85, 210, 250],
        "profit": [20, -15, 45, 55],
    })
    html = (
        df.style()
        .highlight_when(
            in_col="date",
            when=pl.col("profit") < 0,
            then_fill="alert_orange"
        )
        .gradient("sales", cmap="greens")
        .bar("profit", fill_pos="alert_green", fill_neg="alert_orange")
        .fashion_zebra()
        .to_html()
    )
    save("home_hero.html", html)


# ── Home page hero panes ───────────────────────────────────────────────────────

def _hero_df():
    return pl.DataFrame({
        "language": ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
        "rank": [1, 2, 3, 4, 5, 6],
        "users_m": [15.7, 17.8, 12.3, 6.4, 3.2, 2.1],
        "salary_usd": [120000, 110000, 105000, 115000, 130000, 135000],
        "growth_pct": [12, 5, 2, 3, 18, 22],
    })


def gen_hero_raw():
    html = _hero_df().style().fashion_raw().to_html()
    save("hero_raw.html", html)


def gen_hero_explore():
    df = _hero_df()
    html = (
        df.style()
        .show_info("sales_df")
        .gradient("growth_pct", cmap="blue_red_2")
        .gradient("rank", color=True, cmap="blues_r")
        .bar("users_m", fill="alert_orange")
        .highlight_when("language", when=pl.col("rank") == 1, then_fill="alert_yellow")
        .fashion_grid()
        .to_html()
    )
    save("hero_explore.html", html)


def gen_hero_presentation():
    df = _hero_df()
    html = (
        df.style()
        .title("Top Programming Languages (2025)", "Usage, growth, and compensation overview")
        .gradient("users_m", cmap="oryel_r", color=True)
        .highlight_when("language", when=pl.col("rank") == 1, then_fill="alert_yellow")
        .highlight_above("salary_usd", value=120000, fill="alert_red")
        .highlight_above("growth_pct", value=10, color="alert_green", fill=False)
        .format({
            "users_m": "{:.1f}M",
            "growth_pct": "{:+.0f}%",
            "salary_usd": "${:,.0f}",
        })
        .footnote("Negative profits are highlighted for inspection.")
        .fashion_minimal()
        .to_html()
    )
    save("hero_presentation.html", html)


# ── Getting Started ────────────────────────────────────────────────────────────

def gen_getting_started():
    df = pl.DataFrame({
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],
        "height": [1.56, 1.77, 1.65, 1.75],
    })

    save("gs_basic.html",
         df.style().gradient("height").to_html())

    save("gs_chaining.html",
         df.style()
           .gradient("height", cmap="plasma")
           .highlight_max("birthdate", fill="gold")
           .fashion_minimal()
           .title("A polars DataFrame")
           .to_html())

    save("gs_scope_table.html",
         df.style().gradient(["height", "weight"], scope="table", cmap="plasma").to_html())


# ── API: Highlighting ──────────────────────────────────────────────────────────

def gen_api_highlighting():
    df = datasets.get_finance_data()

    save("api_highlight_max_ex1.html",
         df.style().highlight_max("Revenue").to_html())

    save("api_highlight_min_ex1.html",
         df.style().highlight_min("Profit").to_html())

    save("api_highlight_above_ex1.html",
         df.style().highlight_above("Growth", value=10.0).to_html())

    save("api_highlight_below_ex1.html",
         df.style().highlight_below("Profit", value=73).to_html())

    save("api_highlight_equal_ex1.html",
         df.style().highlight_equal("Employees_k", value=182).to_html())

    save("api_highlight_between_ex1.html",
         df.style().highlight_between("Revenue", low=200.0, high=400.0).to_html())

    # highlight_identical: use a small inline DataFrame with duplicate values
    df_identical = pl.DataFrame({
        "actual":    [1, 2, 3, 2, 5],
        "predicted": [1, 3, 3, 4, 5],
    })
    save("api_highlight_identical_ex1.html",
         df_identical.style().highlight_identical(["actual", "predicted"]).to_html())

    # highlight_when: highlight Revenue column where Growth > 15
    save("api_highlight_when_ex1.html",
         df.style().highlight_when(
             "Revenue",
             when=pl.col("Growth") > 15,
             then_fill="lightgreen"
         ).to_html())


# ── API: Gradients ─────────────────────────────────────────────────────────────

def gen_api_gradients():
    df = datasets.get_finance_data()
    llm = datasets.get_llm_benchmarks()

    save("api_gradient_ex1.html",
         df.style().gradient("Revenue", cmap="viridis").to_html())

    # gradient_divergent: use LLM cost data centred at median
    save("api_gradient_divergent_ex1.html",
         llm.style().gradient_divergent("Cost_per_1M", center=15.0, cmap="vik").to_html())

    save("api_gradient_between_ex1.html",
         df.style().gradient_between("Revenue", low=100.0, high=400.0, cmap="lapaz").to_html())

    save("api_heat_map_ex1.html",
         df.select(["Revenue", "Profit", "Growth"]).style().heat_map().to_html())


# ── API: Data Bars ─────────────────────────────────────────────────────────────

def gen_api_bar():
    df = datasets.get_finance_data()

    save("api_bar_ex1.html",
         df.style().bar("Revenue").to_html())

    # Signed bar: climate data has positive/negative values
    climate = datasets.get_climate_data()
    save("api_bar_signed_ex1.html",
         climate.style().bar(
             "Temp_Anomaly",
             fill_pos="steelblue",
             fill_neg="#FF6347"
         ).to_html())


# ── API: Formatting ────────────────────────────────────────────────────────────

def gen_api_format():
    df = datasets.get_finance_data()
    save("api_format_ex1.html",
         df.style().format({
             "Revenue": "{:.1f}B",
             "Growth": "{:+.1f}%"
         }).to_html())


# ── API: Fashion Presets ───────────────────────────────────────────────────────

def gen_api_fashion():
    df = datasets.get_education_data()
    base = df.style().gradient("Math", cmap="blues_2")

    save("api_fashion_grid_ex1.html",       base.fashion_grid().to_html())
    save("api_fashion_zebra_ex1.html",      base.fashion_zebra().to_html())
    save("api_fashion_zebra_ex2.html",      base.fashion_zebra(fill1="white", fill2="#e8f4f8").to_html())
    save("api_fashion_raw_ex1.html",        base.fashion_raw().to_html())
    save("api_fashion_scientific_ex1.html", base.fashion_scientific().to_html())
    save("api_fashion_minimal_ex1.html",    base.fashion_minimal().to_html())
    save("api_fashion_compact_ex1.html",    base.fashion_compact().to_html())
    save("api_fashion_presentation_ex1.html", base.fashion_presentation().to_html())


# ── API: Display & Export ──────────────────────────────────────────────────────

def gen_api_display_export():
    df = datasets.get_finance_data()

    save("api_title_ex1.html",
         df.style()
           .title("Big Tech Financials", subtitle="FY 2023 — Revenue in $B")
           .to_html())

    save("api_footnote_ex1.html",
         df.style()
           .footnote("Source: Company annual reports. Revenue in $B.")
           .to_html())

    save("api_caption_ex1.html",
         df.style()
           .caption("Table 1: Big Tech company financial summary")
           .fashion_scientific()
           .to_html())

    save("api_show_idx_ex1.html",
         df.style().show_idx().to_html())

    save("api_hide_columns_ex1.html",
         df.style().hide_columns().fashion_minimal().to_html())

    save("api_show_info_ex1.html",
         df.style().show_info(name="finance").to_html())


# ── Examples: Correlation Matrix ───────────────────────────────────────────────

def gen_examples_correlation():
    df = datasets.get_iris_data()
    corr_df = df[:, :-1].corr(label='features').with_columns(
        pl.col(pl.Float64).round(2)
    )

    save("examples_correlation_ex1.html",
         corr_df.style()
                .heat_map(exclude='features', cmap='bam')
                .footnote('source: UCI Machine Learning Repository — Fisher\'s Iris dataset')
                .fashion_grid()
                .to_html())


# ── Examples: Heatmap ──────────────────────────────────────────────────────────

def gen_examples_heatmap():
    df = datasets.get_temperature_stats_data()

    save("examples_heatmap_ex1.html",
         df.style()
           .heat_map(exclude='Month', cmap='oryel_r')
           .footnote('source : en.climate-data.org')
           .fashion_grid()
           .to_html())

    save("examples_heatmap_ex2.html",
         df.style()
           .heat_map(exclude='Month', cmap='blue_red_2')
           .footnote('source : en.climate-data.org')
           .fashion_grid()
           .to_html())


# ── Examples: Finance ──────────────────────────────────────────────────────────

def gen_examples_finance():
    df = datasets.get_finance_data()

    # Ex1: gradient on Revenue
    save("examples_finance_ex1.html",
         df.style()
           .gradient("Revenue", cmap="lapaz")
           .fashion_minimal()
           .title("Revenue Distribution")
           .to_html())

    # Ex2: highlight max profit + bar on revenue
    save("examples_finance_ex2.html",
         df.style()
           .highlight_max("Profit", fill="gold")
           .bar("Revenue", fill="steelblue")
           .fashion_grid()
           .to_html())

    # Ex3: cross-column highlight + format
    save("examples_finance_ex3.html",
         df.style()
           .highlight_when("Revenue", when=pl.col("Growth") > 12, then_fill="lightgreen")
           .format({"Revenue": "{:.0f}B", "Growth": "{:+.1f}%"})
           .fashion_zebra()
           .title("High-Growth Companies", subtitle="Green = Growth > 12%")
           .to_html())


# ── Examples: LLM Benchmarks ──────────────────────────────────────────────────

def gen_examples_llm():
    df = datasets.get_llm_benchmarks()

    save("examples_llm_ex1.html",
         df.style()
           .gradient(["MMLU", "HumanEval", "GPQA"], cmap="viridis")
           .fashion_minimal()
           .title("LLM Benchmark Scores")
           .to_html())

    save("examples_llm_ex2.html",
         df.style()
           .highlight_max("MMLU")
           .highlight_max("HumanEval", fill="lightblue")
           .highlight_min("Cost_per_1M", fill="lightgreen")
           .fashion_grid()
           .title("Best in Class")
           .footnote("Cost per 1M tokens. Lower is better.")
           .to_html())

    save("examples_llm_ex3.html",
         df.style()
           .gradient_divergent("Cost_per_1M", center=15.0, cmap="vik")
           .bar("Context_k", fill="steelblue")
           .fashion_zebra()
           .title("Cost vs Context Window")
           .to_html())


# ── Examples: Education ────────────────────────────────────────────────────────

def gen_examples_education():
    df = datasets.get_education_data()

    save("examples_education_ex1.html",
         df.style()
           .heat_map(["Reading", "Math", "Science"], cmap="mint")
           .fashion_scientific()
           .caption("Table 1: OECD PISA 2022 Scores by Country")
           .to_html())

    save("examples_education_ex2.html",
         df.style()
           .highlight_max("Math", fill="gold")
           .highlight_min("Math", fill="#FF6347")
           .gradient("GDP_per_capita", cmap="blues_2")
           .fashion_minimal()
           .title("Math Performance vs Wealth")
           .to_html())

    save("examples_education_ex3.html",
         df.style()
           .bar("Reading")
           .bar("Math")
           .bar("Science")
           .fashion_compact()
           .title("PISA Scores — Bar View")
           .to_html())


# ── Examples: Climate ─────────────────────────────────────────────────────────

def gen_examples_climate():
    df = datasets.get_climate_data()

    save("examples_climate_ex1.html",
         df.style()
           .gradient_divergent("Temp_Anomaly", center=0.0, cmap="vik")
           .fashion_minimal()
           .title("Global Temperature Anomaly by Decade")
           .footnote("Anomaly relative to 1951–1980 baseline. Source: NASA GISS.")
           .to_html())

    save("examples_climate_ex2.html",
         df.style()
           .gradient("CO2_ppm", cmap="heat_2")
           .bar("Temp_Anomaly", fill_pos="#FF6347", fill_neg="steelblue")
           .fashion_grid()
           .title("CO₂ and Temperature Trends")
           .to_html())

    save("examples_climate_ex3.html",
         df.style()
           .highlight_above("CO2_ppm", value=400)
           .highlight_below("Arctic_Ice_M_km2", value=6.0, fill="#FF6347")
           .fashion_scientific()
           .caption("Table 2: Climate indicators exceeding critical thresholds")
           .to_html())


# ── Examples: Air Quality ─────────────────────────────────────────────────────

def gen_examples_airquality():
    df = datasets.get_air_quality_data()

    save("examples_airquality_ex1.html",
         df.style()
           .gradient("AQI", cmap="heat_2")
           .fashion_minimal()
           .title("Air Quality Index by City")
           .to_html())

    save("examples_airquality_ex2.html",
         df.style()
           .highlight_above("PM2_5", value=25.0, fill="#FF6347")
           .highlight_above("NO2", value=40.0, fill="orange")
           .fashion_grid()
           .title("Pollutants Exceeding WHO Limits")
           .footnote("WHO limit: PM2.5 < 25 μg/m³, NO2 < 40 μg/m³")
           .to_html())

    save("examples_airquality_ex3.html",
         df.style()
           .gradient_divergent("Change_vs_2015", center=0.0, cmap="vik")
           .bar("AQI", fill="steelblue")
           .fashion_zebra()
           .title("Air Quality Change Since 2015")
           .to_html())


# ── Examples: Wellbeing ───────────────────────────────────────────────────────

def gen_examples_wellbeing():
    df = datasets.get_wellbeing_data()

    save("examples_wellbeing_ex1.html",
         df.style()
           .heat_map(["Life_Expectancy", "Healthcare_Pct_GDP",
                      "Life_Satisfaction"], cmap="mint")
           .fashion_minimal()
           .title("Wellbeing Indicators by Country")
           .to_html())

    save("examples_wellbeing_ex2.html",
         df.style()
           .highlight_max("Life_Expectancy", fill="lightgreen")
           .highlight_min("Life_Expectancy", fill="#FF6347")
           .gradient("Life_Satisfaction", cmap="peach")
           .fashion_grid()
           .to_html())

    save("examples_wellbeing_ex3.html",
         df.style()
           .bar("Life_Expectancy", fill="steelblue")
           .bar("Work_Hours_Year", fill="#FF6347")
           .fashion_compact()
           .title("Life Expectancy vs Work Hours")
           .footnote("Longer bars = higher values. Red = more work hours.")
           .to_html())


# ── Tutorial ──────────────────────────────────────────────────────────────────

def gen_tutorial():
    df = datasets.get_finance_data()

    # Step 1: Raw table with default fashion
    save("tutorial_step1.html",
         df.style().to_html())

    # Step 2: Add gradient on Revenue
    save("tutorial_step2.html",
         df.style()
           .gradient("Revenue", cmap="lapaz")
           .to_html())

    # Step 3: Add highlight on max Profit
    save("tutorial_step3.html",
         df.style()
           .gradient("Revenue", cmap="lapaz")
           .highlight_max("Profit", fill="gold")
           .to_html())

    # Step 4: Apply fashion preset
    save("tutorial_step4.html",
         df.style()
           .gradient("Revenue", cmap="lapaz")
           .highlight_max("Profit", fill="gold")
           .fashion_minimal()
           .to_html())

    # Step 5: Add title and footnote
    save("tutorial_step5.html",
         df.style()
           .gradient("Revenue", cmap="lapaz")
           .highlight_max("Profit", fill="gold")
           .fashion_minimal()
           .title("Big Tech Financials", subtitle="FY 2023 — Revenue in $B")
           .footnote("Source: Company annual reports.")
           .to_html())

    # Step 6: Add formatting (final result)
    save("tutorial_step6.html",
         df.style()
           .gradient("Revenue", cmap="lapaz")
           .highlight_max("Profit", fill="gold")
           .fashion_minimal()
           .title("Big Tech Financials", subtitle="FY 2023 — Revenue in $B")
           .footnote("Source: Company annual reports.")
           .format({"Revenue": "{:.0f}B", "Growth": "{:+.1f}%"})
           .to_html())


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating polarise documentation snippets...")
    gen_color_reference()
    gen_home()
    gen_hero_raw()
    gen_hero_explore()
    gen_hero_presentation()
    gen_api_highlighting()
    gen_api_gradients()
    gen_api_bar()
    gen_api_format()
    gen_api_fashion()
    gen_api_display_export()
    gen_examples_finance()
    gen_examples_llm()
    gen_examples_education()
    gen_examples_climate()
    gen_examples_airquality()
    gen_examples_wellbeing()
    gen_tutorial()
    html_files = [f for f in os.listdir(OUT) if f.endswith(".html")]
    print(f"\nDone. {len(html_files)} snippet files in docs/snippets/")
