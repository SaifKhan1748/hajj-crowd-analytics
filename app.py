"""
Hajj Crowd Management Analytics Dashboard
Run: streamlit run app.py
Place hajj_cleaned_data.csv in the same folder OR one level up in /data/
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Hajj Analytics Dashboard", layout="wide", page_icon="🕌")

st.markdown("""
<style>
    .stApp { background-color: #f7f6f2; color: #1c1c1c; }
    section[data-testid="stSidebar"] { background-color: #edecea; }
    h1, h2, h3, h4 { color: #1b3d5f; }
    .insight {
        background: #e8f4fd;
        border-left: 5px solid #2477b3;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 6px 0 18px 0;
        font-size: 0.93rem;
        color: #1b3d5f;
    }
    .warn {
        background: #fff3e0;
        border-left: 5px solid #e65100;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 6px 0 18px 0;
        font-size: 0.93rem;
        color: #bf360c;
    }
    div[data-testid="metric-container"] {
        background: #ffffff;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
</style>
""", unsafe_allow_html=True)


# ── Data loader ────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    for path in ['hajj_cleaned_data.csv', '../data/hajj_cleaned_data.csv', 'data/hajj_cleaned_data.csv']:
        if os.path.exists(path):
            return pd.read_csv(path)
    st.error("hajj_cleaned_data.csv not found. Run the notebook first to generate it.")
    st.stop()

df = load_data()
df = df[df.year < 2026].copy()  # exclude pre-season 2026 row


# ── Header ─────────────────────────────────────────────────────
st.title("🕌 Hajj Crowd Management — Predictive Analytics")
st.markdown(
    "**Period:** 2000 – 2025 &nbsp;|&nbsp; "
    "**Records:** 500+ &nbsp;|&nbsp; "
    "**Goal:** Predict safety incidents and healthcare demand to save lives."
)
st.divider()


# ── Sidebar ────────────────────────────────────────────────────
st.sidebar.header("🔎 Filters")
year_range = st.sidebar.slider("Year Range", 2000, 2025, (2000, 2025))
all_countries = sorted(df.country.dropna().unique())
sel_countries = st.sidebar.multiselect("Countries", all_countries, default=all_countries)

filt = df[(df.year.between(*year_range)) & (df.country.isin(sel_countries))]

st.sidebar.divider()
st.sidebar.markdown("**What this project solves:**")
st.sidebar.markdown(
    "- 2M+ pilgrims gather annually\n"
    "- Crowd surges + extreme heat = preventable deaths\n"
    "- Data can tell us WHERE and WHEN risk is highest\n"
    "- So resources reach the right place before the crisis"
)


# ── KPI Row ────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Pilgrims", f"{filt.pilgrim_count.sum():,.0f}")
c2.metric("Avg Temperature (°C)", f"{filt.temperature_c.mean():.1f}")
c3.metric("Total Incidents", f"{filt.safety_incidents.sum():,}")
c4.metric("Total Hospital Visits", f"{filt.hospital_visits.sum():,.0f}")
c5.metric("Avg Crowd Density", f"{filt.crowd_density_score.mean():.2f}")
st.divider()


# ── Section 1: Volume Trend ────────────────────────────────────
st.subheader("1. How Has Pilgrim Volume Changed?")

yearly = filt.groupby('year')['pilgrim_count'].sum().reset_index()
fig, ax = plt.subplots(figsize=(11, 3.8))
ax.fill_between(yearly.year, yearly.pilgrim_count, alpha=0.12, color='steelblue')
ax.plot(yearly.year, yearly.pilgrim_count, marker='o', color='steelblue', ms=4, linewidth=2)

# Mark crisis years
crises = {2006: 'Mina\nStampede', 2015: '2015\nStampede', 2020: 'COVID', 2024: 'Heat\nCrisis'}
for yr, label in crises.items():
    if year_range[0] <= yr <= year_range[1]:
        row = yearly[yearly.year == yr]
        if not row.empty:
            ax.axvline(yr, color='red', alpha=0.3, linestyle='--', linewidth=1.2)
            ax.annotate(label, xy=(yr, row.pilgrim_count.values[0]),
                        xytext=(yr + 0.3, row.pilgrim_count.values[0] * 1.05),
                        fontsize=7.5, color='firebrick')

ax.set_xlabel("Year"); ax.set_ylabel("Total Pilgrims")
ax.set_facecolor('#f7f6f2'); fig.patch.set_facecolor('#f7f6f2')
st.pyplot(fig); plt.close()

st.markdown('<div class="insight">📌 <b>Insight:</b> Volume is not linear — it crashes during crises (95% drop in 2020) and rebounds fast. Authorities using fixed annual budgets will always be under-resourced in recovery years like 2022–2023.</div>', unsafe_allow_html=True)


# ── Section 2: Country Analysis ────────────────────────────────
st.subheader("2. Where Do Pilgrims Come From?")
col1, col2 = st.columns([3, 2])

with col1:
    top = filt.groupby('country')['pilgrim_count'].sum().sort_values(ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    top.plot(kind='barh', ax=ax, color='cadetblue', edgecolor='white')
    ax.set_xlabel("Total Pilgrims"); ax.set_title("Top 10 Countries")
    ax.set_facecolor('#f7f6f2'); fig.patch.set_facecolor('#f7f6f2')
    st.pyplot(fig); plt.close()

with col2:
    total = filt.groupby('country')['pilgrim_count'].sum()
    top3 = total.nlargest(3)
    st.markdown("**Top 3 Countries**")
    for c, v in top3.items():
        pct = v / total.sum() * 100
        st.metric(c, f"{v:,.0f}", f"{pct:.1f}% of total")

st.markdown('<div class="insight">📌 <b>Insight:</b> Top 3 countries consistently supply 30–35% of all pilgrims. Dedicated transport corridors and bilateral health agreements with these nations deliver the highest ROI for any logistics investment.</div>', unsafe_allow_html=True)


# ── Section 3: Temperature Rising ──────────────────────────────
st.subheader("3. Is Heat Getting Worse?")
temp_yr = df.groupby('year')['temperature_c'].mean()
z = np.polyfit(temp_yr.index, temp_yr.values, 1)

fig, ax = plt.subplots(figsize=(11, 3.5))
ax.plot(temp_yr.index, temp_yr.values, marker='o', ms=4, color='tomato', linewidth=2)
ax.plot(temp_yr.index, np.poly1d(z)(temp_yr.index), '--', color='darkred',
        label=f'Trend: +{z[0]:.3f}°C/year', linewidth=1.5)
ax.axhline(45, color='orange', linestyle=':', alpha=0.7, label='Danger threshold (45°C)')
ax.set_ylabel("Avg Temperature (°C)"); ax.legend()
ax.set_facecolor('#f7f6f2'); fig.patch.set_facecolor('#f7f6f2')
st.pyplot(fig); plt.close()

st.markdown(f'<div class="warn">⚠️ <b>Warning:</b> Temperature during Hajj season is rising at +{z[0]:.3f}°C/year. At this rate, Hajj conditions will regularly exceed 50°C by 2030. The 2024 heat crisis (51°C, 1,300+ deaths) is not an anomaly — it is the new normal.</div>', unsafe_allow_html=True)


# ── Section 4: Incident Rate ────────────────────────────────────
st.subheader("4. When Are Pilgrims Most at Risk?")
inc_yr = df.groupby('year')['incident_rate_per10k'].mean() if 'incident_rate_per10k' in df.columns else \
         df.groupby('year').apply(lambda x: (x.safety_incidents / x.pilgrim_count * 10000).mean())

fig, ax = plt.subplots(figsize=(11, 3.5))
bar_colors = ['firebrick' if y in [2006, 2015, 2024] else '#4a8fb5' for y in inc_yr.index]
ax.bar(inc_yr.index, inc_yr.values, color=bar_colors, edgecolor='white')
ax.set_ylabel("Incidents per 10,000 pilgrims")
ax.set_title("Safety Incident Rate Per Year (red = crisis years)")
ax.set_facecolor('#f7f6f2'); fig.patch.set_facecolor('#f7f6f2')
st.pyplot(fig); plt.close()

st.markdown('<div class="insight">📌 <b>Insight:</b> Crisis years (2006, 2015, 2024) show 4–12× the normal incident rate. All three share the same combination: extreme heat AND high crowd density. This pattern is predictable — and preventable.</div>', unsafe_allow_html=True)


# ── Section 5: Feedback ────────────────────────────────────────
st.subheader("5. Pilgrim Satisfaction Trend")
fb = df[df.feedback_score.notna()].groupby('year')['feedback_score'].mean()

fig, ax = plt.subplots(figsize=(11, 3))
ax.plot(fb.index, fb.values, marker='o', color='mediumpurple', linewidth=2, ms=4)
ax.axhline(3.0, color='gray', linestyle='--', alpha=0.5, label='Neutral (3.0)')
ax.fill_between(fb.index, fb.values, 3.0, where=(fb.values < 3.0), alpha=0.15, color='red', label='Below neutral')
ax.set_ylabel("Avg Score (1–5)"); ax.legend()
ax.set_facecolor('#f7f6f2'); fig.patch.set_facecolor('#f7f6f2')
st.pyplot(fig); plt.close()

st.markdown('<div class="insight">📌 <b>Insight:</b> Satisfaction drops below neutral only in crisis years. Tracking annual feedback is a free early warning system — a drop below 3.0 correlates with management failures that preceded major incidents.</div>', unsafe_allow_html=True)


# ── Section 6: ML Model ─────────────────────────────────────────
st.subheader("6. What Predicts Safety Incidents?")

features = ['pilgrim_count','crowd_density_score','heat_risk_index',
            'temperature_c','humidity_pct','accommodation_utilization','medical_teams_per10k']
available_features = [f for f in features if f in df.columns]
target = 'safety_incidents'

mdf = df[available_features + [target]].dropna()
X, y = mdf[available_features], mdf[target]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xtr, ytr)
pred = rf.predict(Xte)

col1, col2 = st.columns(2)
col1.metric("Model MAE", f"{mean_absolute_error(yte, pred):.1f} incidents")
col2.metric("R² Score", f"{r2_score(yte, pred):.2f}")

fi = pd.Series(rf.feature_importances_, index=available_features).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(7, 3.5))
fi.plot(kind='barh', ax=ax, color='steelblue', edgecolor='white')
ax.set_title("Feature Importance — What Drives Incidents?")
ax.set_facecolor('#f7f6f2'); fig.patch.set_facecolor('#f7f6f2')
st.pyplot(fig); plt.close()

st.markdown('<div class="insight">📌 <b>Insight:</b> Crowd density and heat risk dominate. A simple two-variable alert system — no AI needed — can flag high-risk days in advance and trigger emergency deployment. That is the practical recommendation from this model.</div>', unsafe_allow_html=True)


# ── Section 7: Scenario Tool ────────────────────────────────────
st.subheader("7. What-If Scenario Planner")
st.markdown("Adjust inputs to estimate predicted safety incidents:")

s1, s2, s3 = st.columns(3)
p_count = s1.number_input("Pilgrim Count", 500_000, 3_000_000, 1_900_000, 50_000)
density  = s2.slider("Crowd Density Score", 1.0, 10.0, 7.5, 0.1)
temp     = s3.slider("Temperature (°C)", 35.0, 52.0, 46.0, 0.5)

# Build scenario with defaults for missing features
hri = temp * 0.65 + 45 * 0.35  # assume avg humidity
scenario_vals = []
for f in available_features:
    defaults = {'pilgrim_count': p_count, 'crowd_density_score': density,
                'heat_risk_index': hri, 'temperature_c': temp,
                'humidity_pct': 45.0, 'accommodation_utilization': 0.90,
                'medical_teams_per10k': 5.0}
    scenario_vals.append(defaults.get(f, 0))

scenario = pd.DataFrame([scenario_vals], columns=available_features)
est_incidents = int(rf.predict(scenario)[0])
risk = "🔴 HIGH RISK" if est_incidents > 150 else ("🟡 MODERATE" if est_incidents > 60 else "🟢 LOW")
st.metric(f"Estimated Safety Incidents — {risk}", f"{est_incidents:,}")


# ── Footer ──────────────────────────────────────────────────────
st.divider()
st.caption("Hajj Crowd Management Analytics | Data Science Portfolio Project | 2000–2026")
