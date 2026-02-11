import numpy as np
import pandas as pd


class OLSResult:
    def __init__(self, params, rsquared, rsquared_adj, nobs):
        self.params = params
        self.rsquared = rsquared
        self.rsquared_adj = rsquared_adj
        self.nobs = nobs


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
        c
        for c in df.columns
        if any(k in c.lower() for k in ["spend", "cost", "media"])
        and c != target_col
    ]

    return date_col, target_col, spend_cols


def _adstock(x: np.ndarray, alpha: float) -> np.ndarray:
    out = np.zeros_like(x, dtype=float)
    carry = 0.0
    for i, v in enumerate(x):
        carry = float(v) + alpha * carry
        out[i] = carry
    return out


def prepare_mmm_design(
    df: pd.DataFrame,
    date_col: str | None,
    target_col: str,
    spend_cols: list[str],
    adstock_alpha: float = 0.5,
    use_saturation: bool = True,
):
    d = df.copy()

    # Sort by date if available
    if date_col and date_col in d.columns:
        d[date_col] = pd.to_datetime(d[date_col], errors="coerce")
        d = d.dropna(subset=[date_col]).sort_values(date_col)

    d = d.dropna(subset=[target_col]).copy()

    X = pd.DataFrame(index=d.index)
    X["const"] = 1.0

    for c in spend_cols:
        x = pd.to_numeric(d[c], errors="coerce").fillna(0.0).to_numpy()

        # adstock
        x = _adstock(x, adstock_alpha)

        # optional saturation (simple, stable)
        if use_saturation:
            x = np.log1p(np.maximum(x, 0))

        X[f"{c}__x"] = x

    y = pd.to_numeric(d[target_col], errors="coerce").to_numpy(dtype=float)

    meta = {"date_col": date_col, "target_col": target_col, "spend_cols": spend_cols}
    return X, y, meta


def fit_mmm_ols(X: pd.DataFrame, y: np.ndarray) -> OLSResult:
    Xmat = X.to_numpy(dtype=float)
    y = np.asarray(y, dtype=float)

    # least squares solve
    beta, *_ = np.linalg.lstsq(Xmat, y, rcond=None)

    yhat = Xmat @ beta
    resid = y - yhat

    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y - y.mean()) ** 2)) if len(y) else 0.0

    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    n = Xmat.shape[0]
    p = Xmat.shape[1] - 1  # exclude intercept
    r2_adj = 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1) if n > (p + 1) else r2

    return OLSResult(params=beta, rsquared=r2, rsquared_adj=r2_adj, nobs=n)


def channel_contributions(X: pd.DataFrame, params: np.ndarray) -> pd.DataFrame:
    # contribution per feature per row
    return X.multiply(params, axis=1)


def roi_by_channel(df: pd.DataFrame, contrib: pd.DataFrame, spend_cols: list[str]) -> pd.DataFrame:
    rows = []
    for c in spend_cols:
        feat = f"{c}__x"
        if feat not in contrib.columns:
            continue

        total_contrib = float(contrib[feat].sum())
        spend = float(pd.to_numeric(df[c], errors="coerce").fillna(0.0).sum())
        roi = (total_contrib / spend) if spend > 0 else np.nan

        rows.append(
            {
                "channel": c,
                "spend": spend,
                "contribution": total_contrib,
                "roi": roi,
            }
        )

    out = pd.DataFrame(rows)
    if len(out):
        out = out.sort_values("roi", ascending=False)
    return out
