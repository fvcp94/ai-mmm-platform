import numpy as np
import pandas as pd
import statsmodels.api as sm


def detect_columns(df: pd.DataFrame):
    # date
    date_col = None
    for c in df.columns:
        if "date" in c.lower():
            date_col = c
            break

    # target
    target_col = None
    for key in ["revenue", "sales", "conversions", "orders", "target"]:
        for c in df.columns:
            if key in c.lower():
                target_col = c
                break
        if target_col:
            break

    # spend columns
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

    if date_col and date_col in work.columns:
        work[date_col] = pd.to_datetime(work[date_col], errors="coerce")
        work = work.sort_values(date_col)

    X_parts = []
    meta = {"channels": {}}

    for c in spend_cols:
        x = pd.to_numeric(work[c], errors="coerce").fillna(0.0).values
        x_ad = geometric_adstock(x, adstock_alpha)
        meta["channels"][c] = {"adstock_alpha": float(adstock_alpha)}

        X_parts.append(pd.DataFrame({f"{c}__x": x_ad}, index=work.index))

    X = pd.concat(X_parts, axis=1) if X_parts else pd.DataFrame(index=work.index)
    y = pd.to_numeric(work[target_col], errors="coerce")

    mask = y.notna()
    X = X.loc[mask]
    y = y.loc[mask]

    X = sm.add_constant(X, has_constant="add")
    return X, y, meta


def fit_mmm_ols(X, y):
    model = sm.OLS(y.values, X.values)
    return model.fit()


def channel_contributions(X, params):
    return pd.DataFrame(X.values * params.reshape(1, -1), columns=X.columns, index=X.index)


def roi_by_channel(df, contrib, spend_cols):
    rows = []
    for c in spend_cols:
        col = f"{c}__x"
        if col not in contrib.columns:
            continue
        total_contrib = float(contrib[col].sum())
        total_spend = float(pd.to_numeric(df[c], errors="coerce").fillna(0.0).sum())
        roi = (total_contrib / total_spend) if total_spend > 0 else np.nan
        rows.append({"channel": c, "total_spend": total_spend, "total_contribution": total_contrib, "roi": roi})
    return pd.DataFrame(rows).sort_values("roi", ascending=False)
