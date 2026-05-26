"""
Hajj Data Generator: 2000 – May 2026
Real-world events reflected:
  2001 - Post 9/11 drop in international travel
  2003 - SARS scare, slight dip
  2006 - Mina stampede (346 deaths), incident spike
  2012 - MERS outbreak in Saudi Arabia
  2015 - Mina stampede (2,400+ deaths), huge incident spike; crane collapse
  2016 - Saudi Arabia caps quotas after 2015 disaster
  2020 - COVID: only ~10,000 domestic pilgrims allowed
  2021 - COVID: ~60,000 vaccinated pilgrims only
  2022 - Gradual reopening: 1 million pilgrims
  2023 - Full capacity restored: 1.8 million+
  2024 - Record heat wave (June 51°C reported), 1,300+ deaths
  2025 - Post-record reforms, enhanced health protocols
  2026 - Partial data through May (pre-Hajj season)
"""

import pandas as pd
import numpy as np

np.random.seed(2024)

# ── Real approximate country-wise pilgrim quotas (% of total) ─────────────────
COUNTRY_SHARES = {
    'Indonesia':   0.135,
    'Pakistan':    0.110,
    'India':       0.105,
    'Bangladesh':  0.075,
    'Nigeria':     0.065,
    'Egypt':       0.060,
    'Turkey':      0.055,
    'Iran':        0.050,
    'Morocco':     0.045,
    'Malaysia':    0.040,
    'Algeria':     0.038,
    'Sudan':       0.030,
    'Saudi Arabia':0.028,  # domestic
    'Iraq':        0.025,
    'Yemen':       0.020,
    'Senegal':     0.018,
    'Kazakhstan':  0.015,
    'Tunisia':     0.014,
    'Libya':       0.012,
    'Afghanistan': 0.010,
}

# ── Realistic total pilgrim counts by year ───────────────────────────────────
YEARLY_TOTALS = {
    2000: 1_800_000,
    2001: 1_563_000,   # post 9/11 drop
    2002: 1_654_000,
    2003: 1_431_000,   # SARS anxiety
    2004: 1_730_000,
    2005: 1_829_000,
    2006: 1_654_000,   # Mina stampede, quota review
    2007: 1_707_000,
    2008: 1_784_000,
    2009: 1_613_000,   # H1N1 swine flu caution
    2010: 1_799_000,
    2011: 1_828_000,
    2012: 1_752_000,   # MERS outbreak
    2013: 1_379_000,   # Masjid al-Haram expansion cuts capacity
    2014: 1_389_000,   # continued construction
    2015: 1_952_000,   # record before stampede; after: quota cut
    2016: 1_325_000,   # 20% quota cut post-2015
    2017: 1_752_000,
    2018: 1_758_000,
    2019: 1_854_000,
    2020:    10_000,   # COVID – domestic only
    2021:    60_000,   # COVID – vaccinated domestic + limited
    2022: 1_000_000,   # reopening cap
    2023: 1_845_000,   # full capacity
    2024: 1_833_000,   # record heat, ~1,300 deaths
    2025: 1_900_000,   # post-reform, enhanced protocols
    2026:       None,  # pre-Hajj (Hajj is June 2026), no pilgrims yet
}

# ── Real-world event modifiers ────────────────────────────────────────────────
# (year: incident_multiplier, hospitalization_multiplier, note)
EVENT_MODIFIERS = {
    2001: (1.8, 1.3, 'Post 9/11 security heightened'),
    2006: (8.5, 4.2, 'Mina stampede – 346 deaths'),
    2009: (2.1, 2.8, 'H1N1 flu precautions'),
    2012: (1.6, 2.4, 'MERS cases in Saudi Arabia'),
    2015: (12.0, 6.5, 'Mina stampede – 2,400+ deaths; crane collapse'),
    2020: (0.3, 0.8, 'COVID restrictions, minimal pilgrims'),
    2021: (0.5, 1.1, 'COVID – vaccinated pilgrims only'),
    2024: (9.0, 8.0, 'Record heat wave 51°C – 1,300+ deaths'),
}

# ── Hajj-month temperature baselines (Mecca, June–July typical) ──────────────
# Hajj date shifts yearly due to lunar calendar
TEMP_BY_YEAR = {
    2000: 42, 2001: 41, 2002: 40, 2003: 39, 2004: 38,
    2005: 37, 2006: 38, 2007: 39, 2008: 40, 2009: 41,
    2010: 43, 2011: 44, 2012: 45, 2013: 46, 2014: 47,
    2015: 46, 2016: 44, 2017: 43, 2018: 42, 2019: 43,
    2020: 41, 2021: 40, 2022: 43, 2023: 45, 2024: 49,
    2025: 47, 2026: 38,  # pre-summer data
}

rows = []

for year, total in YEARLY_TOTALS.items():
    if year == 2026:
        # Only infrastructure/planning data — no pilgrims yet in May 2026
        rows.append({
            'year': year,
            'country': 'N/A',
            'pilgrim_count': 0,
            'temperature_c': round(np.random.uniform(34, 40), 1),
            'humidity_pct': round(np.random.uniform(25, 45), 1),
            'safety_incidents': 0,
            'transport_trips': 0,
            'hospital_visits': 0,
            'crowd_density_score': 0.0,
            'accommodation_utilization': round(np.random.uniform(0.05, 0.20), 2),
            'feedback_score': None,
            'water_stations': np.random.randint(180, 240),
            'medical_teams_deployed': np.random.randint(8500, 12000),
            'buses_allocated': np.random.randint(12000, 18000),
            'note': 'Pre-Hajj data – Hajj season June 2026'
        })
        continue

    inc_mult, hosp_mult, note = EVENT_MODIFIERS.get(year, (1.0, 1.0, 'Normal year'))
    base_temp = TEMP_BY_YEAR.get(year, 43)

    for country, share in COUNTRY_SHARES.items():
        # Allocate pilgrims with some variance per country
        count = int(total * share * np.random.uniform(0.88, 1.12))
        count = max(count, 0)

        if year in [2020, 2021] and country != 'Saudi Arabia':
            count = max(int(count * 0.02), 0)

        temp = round(base_temp + np.random.uniform(-2, 2), 1)
        humidity = round(np.random.uniform(18, 65), 1)

        # Base incidents scaled by pilgrims and event modifiers
        base_incidents = int((count / 100000) * np.random.uniform(8, 25) * inc_mult)
        base_incidents = min(base_incidents, 9999)

        transport = int((count / 1000) * np.random.uniform(2.5, 6.0))
        hospital = int(count * np.random.uniform(0.015, 0.06) * hosp_mult)
        density = round(np.random.uniform(2.0, 9.5), 2)
        if year in [2015, 2024]: density = round(np.random.uniform(7.5, 9.9), 2)
        if year in [2020, 2021]: density = round(np.random.uniform(0.5, 2.5), 2)

        accommodation = round(np.random.uniform(0.65, 0.99), 2)
        if year in [2020, 2021]: accommodation = round(np.random.uniform(0.02, 0.10), 2)

        feedback = round(np.random.uniform(2.0, 5.0), 2)
        if year in [2015, 2024]: feedback = round(np.random.uniform(1.5, 3.2), 2)
        if year in [2022, 2023, 2025]: feedback = round(np.random.uniform(3.5, 5.0), 2)

        water_stations = np.random.randint(80, 240)
        if year >= 2016: water_stations = np.random.randint(140, 260)
        if year >= 2023: water_stations = np.random.randint(200, 320)

        medical_teams = np.random.randint(2000, 12000)
        if year >= 2016: medical_teams = np.random.randint(5000, 14000)
        if year in [2024, 2025]: medical_teams = np.random.randint(9000, 18000)

        buses = int(count / np.random.uniform(40, 60))

        rows.append({
            'year': year,
            'country': country,
            'pilgrim_count': count,
            'temperature_c': temp,
            'humidity_pct': humidity,
            'safety_incidents': base_incidents,
            'transport_trips': transport,
            'hospital_visits': hospital,
            'crowd_density_score': density,
            'accommodation_utilization': accommodation,
            'feedback_score': feedback,
            'water_stations': water_stations,
            'medical_teams_deployed': medical_teams,
            'buses_allocated': buses,
            'note': note
        })

df = pd.DataFrame(rows)

# Introduce realistic missing values (some fields weren't tracked early)
missing_mask = (df['year'] < 2005)
df.loc[missing_mask & (np.random.rand(len(df)) < 0.12), 'hospital_visits'] = np.nan
df.loc[missing_mask & (np.random.rand(len(df)) < 0.08), 'crowd_density_score'] = np.nan
df.loc[(df['year'] < 2008) & (np.random.rand(len(df)) < 0.06), 'feedback_score'] = np.nan

df.to_csv('hajj_raw_data.csv', index=False)
print(f"✓ Raw dataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  Years: {df.year.min()} – {df.year.max()}")
print(f"  Countries: {df.country.nunique()}")
print(f"  Missing values:\n{df.isnull().sum()[df.isnull().sum()>0]}")
print("\nSample:")
print(df[df.year == 2024][['year','country','pilgrim_count','temperature_c','safety_incidents','note']].head(5).to_string(index=False))
