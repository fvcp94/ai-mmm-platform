import streamlit as st
import pandas as pd
from analytics.experiments import ab_test_sample_size_per_group, geo_test_mde

st.set_page_config(page_title="Experiment Designer", page_icon="🧪", layout="wide")

st.title("🧪 Causal Experiment Designer")
st.caption("Quick planning for A/B tests and geo-tests: sample size, MDE, power, and rollout timeline.")

tab1, tab2 = st.tabs(["🅰️ A/B Test (Digital)", "🌍 Geo-Test (Regional)"])

with tab1:
    st.subheader("A/B Test Sample Size (per group)")

    c1, c2, c3, c4 = st.columns(4)
    baseline = c1.number_input("Baseline metric", value=0.05, min_value=0.0, help="Ex: conversion rate 0.05 OR revenue/user")
    mde_pct = c2.slider("MDE (%)", 1.0, 50.0, 10.0, 1.0)
    alpha = c3.selectbox("Alpha", [0.1, 0.05, 0.01], index=1)
    power = c4.selectbox("Power", [0.7, 0.8, 0.9], index=1)

    std = st.number_input("Std dev (optional, 0 = auto)", value=0.0, min_value=0.0)

    n = ab_test_sample_size_per_group(baseline, mde_pct, alpha=alpha, power=power, std=None if std == 0 else std)

    st.success(f"✅ Required sample size ≈ **{n:,} users per group**")

    st.markdown("### Recommended checklist")
    st.write(
        [
            "Define primary KPI and guardrails",
            "Randomize unit (user/session/geo) and confirm logging",
            "Run full business cycle (min 1–2 weeks)",
            "Avoid peeking; pre-register decision rule",
        ]
    )

with tab2:
    st.subheader("Geo-Test MDE (approx)")

    c1, c2, c3 = st.columns(3)
    baseline_weekly = c1.number_input("Weekly KPI per geo ($)", value=100000.0, min_value=0.0, step=1000.0)
    weeks = c2.slider("Duration (weeks)", 1, 12, 4)
    geos = c3.slider("Geos per arm", 5, 200, 20)

    cv = st.slider("Geo variability (CV)", 0.05, 0.6, 0.2, 0.01)
    alpha2 = st.selectbox("Alpha", [0.1, 0.05, 0.01], index=1, key="geo_alpha")
    power2 = st.selectbox("Power", [0.7, 0.8, 0.9], index=1, key="geo_power")

    res = geo_test_mde(baseline_weekly, weeks, geos, alpha=alpha2, power=power2, cv=cv)

    st.success(f"✅ Estimated MDE ≈ **${res.mde_abs:,.0f} / geo / week**  (≈ **{res.mde_pct:.2f}%**)")

    st.info(res.notes)

    st.markdown("### Suggested timeline")
    timeline = pd.DataFrame(
        [
            {"Week": "W-2 to W-1", "Action": "Select geos, match treatment/control, confirm tracking"},
            {"Week": "W0", "Action": "Launch spend change in treatment geos only"},
            {"Week": f"W1–W{weeks}", "Action": "Monitor compliance + guardrails (no decision peeking)"},
            {"Week": f"W{weeks+1}", "Action": "Analyze lift (DiD/synth control), write exec summary"},
        ]
    )
    st.dataframe(timeline, use_container_width=True)
