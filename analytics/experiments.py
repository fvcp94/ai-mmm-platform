import numpy as np
import pandas as pd
import statsmodels.api as sm


def detect_columns(df: pd.DataFrame):
    date_col = None
    for c in df.columns:
        if "date" in c.lower():
            date_col = c
            break

    target_col = None
    for key in ["revenue", "sales", "conversions", "orders", "target"]:
        for c in df.columns:
            if key in c.lower():
                target_col = c
                break
        if target_col:
            break

    spend_cols = [
        c for c in df.columns
        if any(k in c.lower() for k in ["spend", "cost", "media"])
        and c != target_col
    ]

    return date_col, target_col, spend_cols


def geometric_adstock(x, alpha=0.5):
    out = np.zeros_like(x, dtype=float)
    carry = 0.0
    for i in range(len(x)):
        carry = x[i] + alpha * carry
        out[i] = carry
    return out


def prepare_mmm_design(df, date_col, target_col, spend_cols, adstock_alpha=0.5, use_saturation=True):
    work = df.copy()

    if date_col:
        work[date_col] = pd.to_datetime(work[date_col])
        work = work.sort_values(date_col)

    X_parts = []
    meta = {"channels": {}}

    for c in spend_cols:
        x = work[c].fillna(0).values
        x_ad = geometric_adstock(x, adstock_alpha)

        meta["channels"][c] = {"adstock_alpha": adstock_alpha}

        X_parts.append(pd.DataFrame({f"{c}__x": x_ad}, index=work.index))

    X = pd.concat(X_parts, axis=1)
    y = work[target_col]

    X = sm.add_constant(X)
    return X, y, meta


def fit_mmm_ols(X, y):
    model = sm.OLS(y.valu
@'
import math
from dataclasses import dataclass


@dataclass
class PowerResult:
    mde_abs: float
    mde_pct: float
    notes: str


def ab_test_sample_size_per_group(baseline, mde_pct, alpha=0.05, power=0.8, std=None):
    z_alpha = 1.96
    z_beta = 0.84

    sigma = std if std is not None else max(baseline, 1e-6)
    delta = baseline * (mde_pct / 100.0)

    n = 2 * (z_alpha + z_beta)**2 * sigma**2 / (delta**2 + 1e-9)
    return int(math.ceil(n))


def geo_test_mde(baseline, weeks, n_geos_per_arm, alpha=0.05, power=0.8, cv=0.2):
    z_alpha = 1.96
    z_beta = 0.84

    sigma = cv * baseline
    se = math.sqrt(2) * sigma / math.sqrt(n_geos_per_arm * weeks)

    mde_abs = (z_alpha + z_beta) * se
    mde_pct = (mde_abs / baseline) * 100 if baseline > 0 else 0

    return PowerResult(
        mde_abs=mde_abs,
        mde_pct=mde_pct,
        notes="Simplified approximation. Use DiD or synthetic control for production."
    )
