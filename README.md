# Predictive Analytics for Hajj Crowd Management

> **Using 26 years of data to predict safety incidents, forecast pilgrim volumes, and support real-time resource planning decisions during the world's largest annual human gathering.**

---

## The Problem

Every year, **1.8 to 2 million pilgrims** from over 180 countries travel to Mecca for Hajj. Managing that many people — in extreme summer heat, across a compressed 5-day window — is one of the most complex logistics challenges on the planet.

The data tells a painful story:

- **2006** — Mina stampede. **346 deaths.**
- **2015** — Mina stampede. **2,400+ deaths.**
- **2024** — Record heat wave, 51°C. **1,300+ deaths.**

These are not accidents. They are the result of planning systems that rely on fixed annual budgets instead of data. Crowd density and temperature have measurable, predictable relationships with safety outcomes — and this project proves it.

---

## What This Project Does

Analyses historical Hajj data from **2000 to 2026** across **20 countries** to answer six real operational questions:

| Question | Answer Found |
|---|---|
| Which factors drive safety incidents most? | Crowd density + heat risk (65–70% of model importance) |
| Is temperature getting worse over time? | Yes — rising ~+0.3°C/year during Hajj season |
| Which countries need the most resources? | Top 3 nations supply 33% of all pilgrims |
| Does more medical staffing reduce deaths? | Yes — statistically confirmed (p < 0.05) |
| How many pilgrims in 2026? | ~1.9 million (ARIMA forecast) |
| When should emergency protocols trigger? | When density > 7.5 AND temperature > 45°C |

---

## Key Business Findings

| Finding | Evidence | Recommended Action |
|---|---|---|
| Pilgrim volume is not linear | 10,000 (2020) → 1,850,000 (2023) | Replace fixed annual budgets with dynamic capacity planning |
| Heat is rising every year | +0.3°C/year trend confirmed 2000–2024 | Mandatory cooling infrastructure expansion every 3 years |
| 2024 was the worst healthcare burden on record | ~8× normal hospitalisation rate | Pre-position ICU units whenever forecast exceeds 46°C |
| Top 3 countries = 33% of total pilgrims | Indonesia, Pakistan, India (combined) | Bilateral transport agreements and visa fast-tracks for these nations |
| Medical team coverage reduces mortality | Negative correlation confirmed | Minimum 1 medical team per 500 pilgrims |
| 2026 forecast: ~1.9 million pilgrims | ARIMA(1,1,1) model | Pre-book 18,000+ buses and 300+ water stations now |

---

## Project Workflow

```
Raw Data (521 rows, 15 columns)
        │
        ▼
  Data Cleaning
  · Median imputation for skewed columns
  · Preserve intentional NaN (early feedback scores)
  · Separate 2026 pre-season record
        │
        ▼
  Feature Engineering
  · heat_risk_index (temp × 0.65 + humidity × 0.35)
  · incident_rate_per10k (normalised safety metric)
  · yoy_growth per country
  · medical_teams_per10k (resource adequacy)
  · crisis_year binary flag
        │
        ▼
  Exploratory Data Analysis
  · Yearly volume trends with crisis annotations
  · Temperature trend + linear regression line
  · Country-wise contribution breakdown
  · Correlation heatmap across all features
        │
        ▼
  Statistical Analysis
  · Independent t-test: heat vs hospital visits (p < 0.05)
  · Independent t-test: density vs incidents (p < 0.05)
  · Pearson correlation: temperature ↔ hospital visits
        │
        ▼
  Machine Learning
  · Linear Regression (baseline)
  · Random Forest Regressor — best model (R² = 0.75)
  · Gradient Boosting Regressor
  · Target: safety_incidents + hospital_visits
        │
        ▼
  Time Series Forecasting
  · ARIMA(1,1,1) on annual pilgrim volume
  · Forecast: 2026 → ~1.9M pilgrims
        │
        ▼
  Streamlit Dashboard
  · Live filters by year and country
  · 5 KPI cards + 6 charts
  · What-If Scenario Planner (real-time risk label)
```

---


## Dataset

**521 records · 20 countries · 2000–2026 · 15 raw features · 23 after engineering**

| Column | Type | Description |
|---|---|---|
| `year` | int | 2000 – 2026 |
| `country` | string | Country of origin (20 nations) |
| `pilgrim_count` | int | Pilgrims from that country that year |
| `temperature_c` | float | Avg temperature in Mecca during Hajj (°C) |
| `humidity_pct` | float | Avg humidity during Hajj period |
| `safety_incidents` | int | Recorded safety incidents |
| `transport_trips` | int | Bus and train trips for pilgrim movement |
| `hospital_visits` | int | Pilgrim hospital visits |
| `crowd_density_score` | float | Composite crowd density score (1–10) |
| `accommodation_utilization` | float | Hotel and camp occupancy rate (0–1) |
| `feedback_score` | float | Pilgrim satisfaction score (1–5) |
| `water_stations` | int | Water distribution points deployed |
| `medical_teams_deployed` | int | Medical teams on the ground |
| `buses_allocated` | int | Buses allocated for transportation |
| `note` | string | Key real-world event for that year |

**Engineered features added in notebook:**

| Feature | Formula | Purpose |
|---|---|---|
| `heat_risk_index` | temp × 0.65 + humidity × 0.35 | Combined physiological heat stress |
| `incident_rate_per10k` | incidents / pilgrims × 10,000 | Normalised risk across years |
| `yoy_growth` | pct_change grouped by country | Year-over-year demand signal |
| `medical_teams_per10k` | teams / pilgrims × 10,000 | Resource adequacy measure |
| `hospital_rate_pct` | hospital_visits / pilgrims × 100 | Healthcare burden rate |
| `crisis_year` | binary flag | 2006, 2015, 2024 marked as 1 |
| `covid_year` | binary flag | 2020, 2021 marked as 1 |
| `sentiment` | mapped from feedback_score | Positive / Neutral / Negative |

**Real-world events calibrated in the data:**

| Year | Event |
|---|---|
| 2001 | Post 9/11 international travel drop |
| 2003 | SARS anxiety, reduced international movement |
| 2006 | Mina stampede — 346 deaths, incident spike |
| 2009 | H1N1 swine flu precautions |
| 2012 | MERS outbreak in Saudi Arabia |
| 2013–14 | Masjid al-Haram expansion, reduced capacity |
| 2015 | Mina mega-stampede — 2,400+ deaths; crane collapse |
| 2016 | Saudi Arabia imposes 20% quota cut |
| 2020 | COVID-19 — domestic pilgrims only (~10,000) |
| 2021 | COVID-19 — vaccinated pilgrims only (~60,000) |
| 2022 | Gradual reopening — capped at 1,000,000 |
| 2023 | Full capacity restored — 1,845,000 pilgrims |
| 2024 | Record heat wave 51°C — 1,300+ deaths |
| 2025 | Post-reform enhanced health protocols |
| 2026 | Pre-Hajj season data only (Hajj: June 2026) |

---

## How to Run

### Requirements
```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels scipy streamlit
```

### Run the Notebook
```bash
# Open in Anaconda Navigator or from terminal:
jupyter notebook notebooks/hajj_analysis.ipynb
```
Run all cells top to bottom. The notebook reads `data/hajj_raw_data.csv` and saves `data/hajj_cleaned_data.csv` at the end.

### Launch the Dashboard
```bash
cd app
streamlit run app.py
```
Make sure `hajj_cleaned_data.csv` is in the same folder as `app.py`, or one level up in `data/`.

---

## Model Results

| Model | MAE | R² Score |
|---|---|---|
| Linear Regression (baseline) | ~35 incidents | ~0.45 |
| Gradient Boosting | ~22 incidents | ~0.72 |
| **Random Forest** *(selected)* | **~20 incidents** | **~0.75** |

**Top predictive features (Random Forest):**
1. `crowd_density_score` — ~38% importance
2. `heat_risk_index` — ~28% importance
3. `pilgrim_count` — ~14% importance
4. `medical_teams_per10k` — ~10% importance

**Time Series:**
- Model: ARIMA(1,1,1)
- 2026 forecast: ~1,900,000 pilgrims
- 2027 forecast: ~1,950,000 pilgrims

---

## Tech Stack

| Category | Tools |
|---|---|
| Data manipulation | `pandas`, `numpy` |
| Visualisation | `matplotlib`, `seaborn` |
| Machine learning | `scikit-learn` (RandomForest, GradientBoosting, LinearRegression) |
| Time series | `statsmodels` (ARIMA) |
| Statistical tests | `scipy.stats` (t-test, Pearson correlation) |
| Dashboard | `Streamlit` |
| Environment | Anaconda, Jupyter Notebook |

---

## Why This Project Matters

This is not a prediction exercise. It is a **decision support tool**.

The goal was to take data that already exists — temperature records, crowd measurements, incident reports — and turn it into a clear operational answer:

> *"Here is where the risk is. Here is when it will happen. Here is what to deploy, and how much of it."*

A simple real-time monitor combining crowd density and temperature forecast — built from this analysis — could have flagged the 2024 crisis days in advance. That is the value of data science in public safety.

---


