# Predictive Analytics for Hajj Crowd Management
### Data Science Portfolio Project | 2000 – May 2026

---

## Problem Statement
Every year 1.8–2 million pilgrims gather for Hajj in Mecca.  
Crowd surges, extreme heat, and poor resource allocation cause **preventable deaths**.  
In 2015 alone, a stampede killed 2,400+ people. In 2024, a heat wave killed 1,300+.

**Authorities still plan resources using fixed annual budgets — not data.**

---

## What This Project Does
Analyzes 26 years of Hajj data to answer:
- Which factors cause the most safety incidents?
- Is heat getting worse over time?
- How many hospital resources does a given crowd/temperature scenario need?
- What will pilgrim volume look like in 2026–2027?

---

## Key Business Findings

| Finding | Numbers | Action |
|---|---|---|
| Volume is not linear | 10k (2020) → 1.85M (2023) | Dynamic budgets, not fixed |
| Heat rising +0.3°C/year | Confirmed 2000–2024 | Mandatory cooling investment |
| 2024: worst healthcare burden | ~8× normal hospitalization | Pre-position ICU units >46°C |
| Top 3 nations = 33% of volume | Indonesia, Pakistan, India | Bilateral transport fast-track |
| More medical teams = fewer deaths | Negative correlation confirmed | 1 team per 500 pilgrims minimum |
| 2026 forecast: ~1.9M pilgrims | ARIMA model | Pre-book 18,000+ buses now |

---

## Project Structure

```
hajj_project/
│
├── data/
│   ├── generate_data.py        ← Run this first to create raw CSV
│   ├── hajj_raw_data.csv       ← Raw dataset (2000–2026, 521 rows, 15 cols)
│   └── hajj_cleaned_data.csv   ← Output of notebook (cleaned + engineered)
│
├── notebooks/
│   └── hajj_analysis.ipynb     ← Full analysis: cleaning → EDA → stats → ML → forecast
│
├── app/
│   └── app.py                  ← Streamlit dashboard
│
└── README.md
```

---

## How to Run

### Step 1 — Install requirements
```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels scipy streamlit
```

### Step 2 — Generate raw data
```bash
cd data
python generate_data.py
```

### Step 3 — Run the notebook (Anaconda / Jupyter)
```bash
cd notebooks
jupyter notebook hajj_analysis.ipynb
```
> Run all cells top to bottom. This generates `hajj_cleaned_data.csv`.

### Step 4 — Launch the Streamlit app
```bash
cd app
streamlit run app.py
```

---

## Dataset Description

| Column | Description |
|---|---|
| year | 2000–2026 |
| country | 20 countries of origin |
| pilgrim_count | Pilgrims from that country that year |
| temperature_c | Avg Hajj-period temperature in Mecca (°C) |
| humidity_pct | Avg humidity during Hajj |
| safety_incidents | Recorded safety incidents |
| transport_trips | Bus/train trips for pilgrim transport |
| hospital_visits | Pilgrim hospital visits |
| crowd_density_score | Composite crowd density (1–10 scale) |
| accommodation_utilization | Hotel/camp occupancy rate |
| feedback_score | Pilgrim satisfaction (1–5 scale) |
| water_stations | Water distribution points deployed |
| medical_teams_deployed | Medical teams on ground |
| buses_allocated | Buses allocated for that year |
| note | Key event for that year |

**Real-world events reflected:** 9/11 (2001), SARS (2003), Mina stampede (2006), H1N1 (2009), MERS (2012), Masjid expansion (2013–14), Mina mega-stampede (2015), quota cut (2016), COVID (2020–21), reopening (2022), full recovery (2023), record heat wave (2024).

---

## Tech Stack
`Python` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `scikit-learn` · `statsmodels` · `scipy` · `Streamlit`

---

## Why This Project Matters for Interviews
This is not a prediction exercise — it is a **decision support tool**.  
Every chart answers: *"So what should we do?"*  
That is what data science is for.
