import math
from dataclasses import dataclass
from scipy.stats import norm


# ============================================================
# A/B TEST SAMPLE SIZE
# ============================================================

def ab_test_sample_size_per_group(
    baseline: float,
    mde_pct: float,
    alpha: float = 0.05,
    power: float = 0.8,
    std: float | None = None,
):
    """
    Estimate sample size per group for an A/B test.
    """

    # Convert % → absolute lift
    mde_abs = baseline * (mde_pct / 100)

    p1 = baseline
    p2 = baseline + mde_abs

    if std is None:
        pooled = (p1 + p2) / 2
        std = math.sqrt(2 * pooled * (1 - pooled))

    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)

    numerator = (z_alpha + z_beta) ** 2 * std**2
    denominator = mde_abs**2

    n = numerator / denominator

    return math.ceil(n)


# ============================================================
# GEO TEST RESULT STRUCTURE
# ============================================================

@dataclass
class GeoTestResult:
    mde_abs: float
    mde_pct: float
    notes: str


# ============================================================
# GEO TEST MDE
# ============================================================

def geo_test_mde(
    baseline: float,
    weeks: int,
    n_geos_per_arm: int,
    alpha: float = 0.05,
    power: float = 0.8,
    cv: float = 0.2,
):
    """
    Estimate Minimum Detectable Effect for geo experiments.
    """

    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)

    std = baseline * cv

    mde_abs = (z_alpha + z_beta) * std / math.sqrt(n_geos_per_arm * weeks)
    mde_pct = (mde_abs / baseline) * 100

    notes = (
        "MDE decreases with more geos and longer duration. "
        "Lower variability improves sensitivity."
    )

    return GeoTestResult(
        mde_abs=mde_abs,
        mde_pct=mde_pct,
        notes=notes,
    )
