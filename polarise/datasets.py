"""Example datasets for Polarise documentation and demos.

All datasets use real or realistic data with proper citations.
These examples span multiple disciplines to demonstrate Polarise's versatility.
"""

import polars as pl


# ============================================================================
# FINANCE & ECONOMICS
# ============================================================================

def get_finance_data():
    """Big Tech company financials (FY2023 approximate data).

    Source: Annual reports, approximate values rounded for clarity.
    Revenue and Profit in billions USD, Growth is YoY %.

    Returns:
        pl.DataFrame: Financial metrics for major tech companies
    """
    return pl.DataFrame({
        'Company': ['Apple', 'Microsoft', 'Google', 'Amazon', 'Meta'],
        'Revenue': [383.3, 211.9, 307.4, 574.8, 134.9],  # Billions USD
        'Profit': [97.0, 72.4, 73.8, 30.4, 39.1],
        'Growth': [7.8, 6.9, 8.7, 11.8, 16.4],  # % YoY
        'Employees_k': [161, 221, 182, 1541, 67]  # Thousands
    })


# ============================================================================
# ARTIFICIAL INTELLIGENCE / ML
# ============================================================================

def get_llm_benchmarks():
    """Large Language Model benchmark scores (2024 data).

    Source: Public benchmarks - MMLU, HumanEval, GPQA
    - MMLU: Massive Multitask Language Understanding (0-100)
    - HumanEval: Coding tasks (0-100)
    - GPQA: Graduate-level questions (0-100)

    Returns:
        pl.DataFrame: LLM performance metrics
    """
    return pl.DataFrame({
        'Model': ['GPT-4', 'Claude-3.5 Sonnet', 'Gemini-1.5 Pro', 'Llama-3-70B', 'Mixtral-8x7B'],
        'MMLU': [86.4, 88.7, 85.9, 82.0, 70.6],  # General knowledge
        'HumanEval': [67.0, 92.0, 71.9, 81.7, 40.2],  # Coding
        'GPQA': [50.1, 59.4, 46.2, 42.7, 34.3],  # Grad-level reasoning
        'Context_k': [128, 200, 2048, 8, 32],  # Context window (thousands of tokens)
        'Cost_per_1M': [30.0, 3.0, 7.0, 0.9, 0.7]  # USD per 1M tokens (input)
    })


# ============================================================================
# SOCIAL SCIENCE - EDUCATION
# ============================================================================

def get_education_data():
    """OECD PISA 2022 scores for selected European countries.

    Source: OECD PISA 2022 Results
    Scores are on a scale where OECD average ≈ 480-490

    Returns:
        pl.DataFrame: Educational performance metrics
    """
    return pl.DataFrame({
        'Country': ['Estonia', 'Ireland', 'Poland', 'Finland', 'Netherlands'],
        'Reading': [511, 516, 489, 490, 459],  # PISA score
        'Math': [510, 492, 489, 484, 493],
        'Science': [526, 504, 513, 511, 488],
        'GDP_per_capita': [27.9, 99.1, 18.7, 53.1, 58.3]  # Thousands EUR
    })


# ============================================================================
# SOCIAL SCIENCE - DEMOGRAPHICS & WELLBEING
# ============================================================================

def get_wellbeing_data():
    """European country wellbeing indicators (2023 data).

    Source: Eurostat, OECD Better Life Index
    Life satisfaction: 0-10 scale from surveys

    Returns:
        pl.DataFrame: Quality of life metrics
    """
    return pl.DataFrame({
        'Country': ['Spain', 'Italy', 'France', 'Sweden', 'Germany'],
        'Life_Expectancy': [83.3, 82.9, 82.5, 83.1, 81.7],  # Years
        'Healthcare_Pct_GDP': [9.1, 9.0, 11.3, 10.9, 11.7],  # % of GDP
        'Life_Satisfaction': [7.1, 6.5, 6.8, 7.4, 7.0],  # 0-10 scale
        'Work_Hours_Year': [1641, 1723, 1511, 1452, 1349]  # Annual average
    })


def get_languages_data():
    """European multilingualism statistics (2023).

    Source: Eurobarometer Special Survey on Languages
    Shows percentage of population speaking foreign languages

    Returns:
        pl.DataFrame: Language proficiency metrics
    """
    return pl.DataFrame({
        'Country': ['Luxembourg', 'Netherlands', 'Denmark', 'Sweden', 'Germany'],
        'Foreign_Languages_Pct': [98, 94, 89, 88, 67],  # % speaking 1+ foreign language
        'English_Speakers_Pct': [56, 90, 86, 89, 56],  # % speaking English
        'Population_M': [0.6, 17.5, 5.9, 10.5, 83.2],  # Millions
        'Students_Abroad_Pct': [57.8, 8.2, 7.4, 4.6, 4.1]  # % studying abroad
    })


# ============================================================================
# ENVIRONMENTAL SCIENCE
# ============================================================================

def get_air_quality_data():
    """Air quality measurements for major European cities (2023).

    Source: European Environment Agency
    - PM2.5: Particulate matter < 2.5μm (μg/m³)
    - NO2: Nitrogen dioxide (μg/m³)
    - O3: Ozone (μg/m³)
    - AQI: Air Quality Index (0-100 good, 100-200 moderate, etc.)

    Returns:
        pl.DataFrame: Air pollution metrics
    """
    return pl.DataFrame({
        'City': ['Paris', 'Berlin', 'Madrid', 'Rome', 'London'],
        'PM2_5': [13.2, 11.8, 9.5, 15.7, 12.1],  # μg/m³
        'NO2': [38.4, 26.1, 31.7, 42.3, 35.8],  # μg/m³
        'O3': [52.6, 48.2, 61.3, 55.1, 44.8],  # μg/m³
        'AQI': [48, 42, 53, 58, 45],  # Air Quality Index
        'Change_vs_2015': [-5.2, -3.8, 1.2, -2.1, -4.5]  # % improvement
    })


def get_renewable_energy_data():
    """Renewable energy statistics for European countries (2023).

    Source: Eurostat Energy Statistics
    Shows renewable energy adoption and carbon emissions

    Returns:
        pl.DataFrame: Energy and emissions metrics
    """
    return pl.DataFrame({
        'Country': ['Norway', 'Iceland', 'Sweden', 'Austria', 'Denmark'],
        'Renewable_Pct': [71.5, 83.7, 62.6, 36.4, 41.6],  # % of total energy
        'CO2_per_capita': [7.5, 4.8, 3.8, 6.7, 5.2],  # Tonnes per person
        'Change_2015_2023': [5.3, 8.1, 12.4, 3.7, 15.2],  # % increase in renewables
        'Nuclear_Pct': [0.0, 0.0, 29.8, 0.0, 0.0],  # % nuclear in energy mix
        'Wind_Capacity_GW': [5.2, 0.0, 11.5, 3.8, 7.6]  # Gigawatts
    })


def get_urban_sustainability_data():
    """Sustainable urban development metrics (2023).

    Source: UN Habitat, Eurostat Urban Development
    Shows livability and sustainability of European cities

    Returns:
        pl.DataFrame: Urban sustainability metrics
    """
    return pl.DataFrame({
        'City': ['Copenhagen', 'Amsterdam', 'Vienna', 'Helsinki', 'Stockholm'],
        'Bicycle_Mode_Share': [26, 32, 7, 11, 15],  # % of trips by bike
        'Green_Space_m2': [68, 87, 120, 301, 87],  # m² per capita
        'Public_Transport_Pct': [21, 16, 34, 27, 25],  # % modal share
        'Walkability_Score': [8.2, 8.7, 8.5, 7.9, 8.1],  # Index 0-10
        'EV_Charging_per_1000': [42, 38, 15, 35, 29]  # EV chargers per 1000 people
    })


# ============================================================================
# PHYSICAL SCIENCES
# ============================================================================

def get_material_properties_data():
    """Physical properties of common metals.

    Source: Engineering handbooks, standard reference values
    Cost index is relative to aluminum = 100

    Returns:
        pl.DataFrame: Material properties
    """
    return pl.DataFrame({
        'Material': ['Aluminum', 'Copper', 'Iron', 'Gold', 'Silver'],
        'Density': [2.70, 8.96, 7.87, 19.32, 10.49],  # g/cm³
        'Melting_Point': [660, 1085, 1538, 1064, 962],  # °C
        'Thermal_Conductivity': [237, 401, 80, 318, 429],  # W/(m·K)
        'Electrical_Resistivity': [2.65, 1.68, 9.71, 2.44, 1.59],  # 10⁻⁸ Ω·m
        'Cost_Index': [100, 520, 45, 3850, 1240]  # Relative to aluminum
    })


def get_experiment_data():
    """Experimental physics measurement data.

    Source: Simulated lab measurements (typical precision)
    Shows repeated measurements with small deviations

    Returns:
        pl.DataFrame: Experimental measurements
    """
    return pl.DataFrame({
        'Trial': [1, 2, 3, 4, 5, 6, 7, 8],
        'Temperature': [25.2, 25.1, 25.3, 25.0, 25.2, 25.1, 25.2, 25.1],  # °C
        'Voltage': [4.98, 5.02, 4.97, 5.01, 4.99, 5.00, 5.01, 4.98],  # Volts
        'Current': [2.51, 2.48, 2.53, 2.49, 2.50, 2.51, 2.49, 2.52],  # Amperes
        'Resistance': [1.98, 2.02, 1.96, 2.01, 2.00, 1.98, 2.02, 1.97],  # Ohms
        'Deviation': [0.01, -0.02, 0.03, -0.01, 0.00, 0.01, -0.01, 0.02]  # From mean
    })


def get_planetary_data():
    """Physical properties of planets in our solar system.

    Source: NASA Planetary Fact Sheet
    Educational dataset showing wide range of values

    Returns:
        pl.DataFrame: Planetary characteristics
    """
    return pl.DataFrame({
        'Planet': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'],
        'Distance_AU': [0.39, 0.72, 1.00, 1.52, 5.20, 9.54, 19.19, 30.07],  # From Sun
        'Diameter_km': [4879, 12104, 12756, 6792, 142984, 120536, 51118, 49528],
        'Mass_Earth': [0.055, 0.815, 1.000, 0.107, 317.8, 95.2, 14.5, 17.1],  # Relative to Earth
        'Orbital_Period_days': [88, 225, 365, 687, 4333, 10759, 30687, 60190],
        'Moons': [0, 0, 1, 2, 95, 146, 27, 14]
    })


# ============================================================================
# CLIMATE SCIENCE
# ============================================================================

def get_temperature_stats_data():
    """Monthly temperature statistics for a cold climate location.

    Source: en.climate-data.org
    Rows are temperature metrics (Avg, Max, Min), columns are months.

    Returns:
        pl.DataFrame: Monthly temperature data (°C)
    """
    return pl.DataFrame({
        'Month':       ['Avg. Temp (°C)', 'Max. Temp (°C)', 'Min. Temp (°C)'],
        'January':     [-24.2, -19.5, -28.8],
        'February':    [-20.3, -14.3, -26.2],
        'March':       [-12.4,  -5.0, -19.8],
        'April':       [ -1.0,   4.9,  -6.9],
        'May':         [  8.8,  14.7,   2.0],
        'June':        [ 15.0,  21.0,   9.1],
        'July':        [ 15.9,  21.5,  10.4],
        'August':      [ 13.4,  18.9,   8.0],
        'September':   [  6.9,  12.1,   1.8],
        'October':     [ -4.1,   0.2,  -8.3],
        'November':    [-15.3, -11.1, -19.5],
        'December':    [-23.3, -19.1, -27.4],
    })

def get_iris_data():
    """Fisher's Iris dataset — classic multivariate dataset.

    Source: UCI Machine Learning Repository
    Contains sepal/petal measurements for 3 Iris species.

    Returns:
        pl.DataFrame: Iris flower measurements
    """
    import importlib.resources
    csv_path = importlib.resources.files("polarise") / "iris.csv"
    return pl.read_csv(str(csv_path), separator=',')


def get_climate_data():
    """Global temperature anomalies by decade (1880-2020).

    Source: NASA GISS Surface Temperature Analysis
    Temperature anomaly relative to 1951-1980 baseline

    Returns:
        pl.DataFrame: Climate change data
    """
    return pl.DataFrame({
        'Decade': ['1880s', '1910s', '1940s', '1970s', '1990s', '2000s', '2010s', '2020s'],
        'Temp_Anomaly': [-0.27, -0.27, 0.05, 0.01, 0.33, 0.62, 0.93, 1.17],  # °C
        'CO2_ppm': [290, 300, 310, 326, 354, 377, 395, 417],  # Parts per million
        'Sea_Level_mm': [0, 10, 30, 50, 90, 150, 210, 250],  # mm rise since 1880
        'Arctic_Ice_M_km2': [7.5, 7.4, 7.3, 7.2, 6.8, 6.2, 5.1, 4.7]  # Million km² September minimum
    })


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def list_all_datasets():
    """Print all available example datasets with descriptions."""
    datasets = {
        'Finance & Economics': [
            ('get_finance_data()', 'Big Tech company financials'),
        ],
        'Artificial Intelligence': [
            ('get_llm_benchmarks()', 'LLM performance benchmarks'),
        ],
        'Social Science': [
            ('get_education_data()', 'OECD PISA education scores'),
            ('get_wellbeing_data()', 'European wellbeing indicators'),
            ('get_languages_data()', 'European multilingualism statistics'),
        ],
        'Environmental Science': [
            ('get_air_quality_data()', 'European city air quality'),
            ('get_renewable_energy_data()', 'Renewable energy adoption'),
            ('get_urban_sustainability_data()', 'Sustainable urban development'),
        ],
        'Physical Sciences': [
            ('get_material_properties_data()', 'Metal physical properties'),
            ('get_experiment_data()', 'Lab measurement data'),
            ('get_planetary_data()', 'Solar system planets'),
        ],
        'Climate Science': [
            ('get_climate_data()', 'Global temperature anomalies'),
            ('get_temperature_stats_data()', 'Monthly temperature statistics'),
        ],
        'Biology': [
            ('get_iris_data()', "Fisher's Iris dataset"),
        ],
    }

    print("Available Example Datasets:")
    print("=" * 70)
    for category, funcs in datasets.items():
        print(f"\n{category}:")
        for func_name, desc in funcs:
            print(f"  • {func_name:<35} - {desc}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Demo: show all datasets
    list_all_datasets()

    print("\n\nExample: LLM Benchmarks")
    print("-" * 70)
    print(get_llm_benchmarks())
