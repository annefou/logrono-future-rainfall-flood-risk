# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 03 — Does heavier future rainfall put more residents at risk?
#
# The finding under test (AIDA): *heavier future design rainfall increases the number of
# residents of Logroño living in buildings at pluvial flood risk.*
#
# It is checked in every case the analysis computed — both future scenarios (EURO-CORDEX
# median Q50 and 90th percentile Q90), all seven return periods, each risk (well-being,
# mobility) and either — and three measures follow:
#
# 1. **Residents at risk**, present against future, per return period.
# 2. **Class transitions** with present-day limits: does any building move *down*?
# 3. **The shift in return period**: which future storm carries today's 100-year rainfall,
#    and how many residents does it put at risk?
#
# The plausibility of the future rainfall itself (REACHOUT's EURO-CORDEX factors against
# the Destination Earth Climate DT) is summarised in §4. This notebook only measures.

# %%
import json
from pathlib import Path

import numpy as np
import pandas as pd

CLEAN = Path("../data/clean")
RESULTS = Path("../results")
RESULTS.mkdir(parents=True, exist_ok=True)
FUTURE = ["CC_Q50", "CC_Q90"]

at_risk = pd.read_csv(CLEAN / "at_risk.csv")
transitions = pd.read_csv(CLEAN / "transitions.csv")
rain = pd.read_csv(CLEAN / "rainfall.csv", index_col="rp")

# %% [markdown]
# ## 1. Residents at risk, present against future

# %%
wide = at_risk.pivot_table(index=["risk", "rp"], columns="climate", values="residents_at_risk")
change = pd.DataFrame({f"{c}_minus_present": wide[c] - wide["present"] for c in FUTURE})
change = change.join(pd.DataFrame({f"{c}_pct": 100 * (wide[c] / wide["present"] - 1) for c in FUTURE}))
change = wide.join(change).reset_index()
change.to_csv(RESULTS / "residents_at_risk_change.csv", index=False)
print(change[change["risk"] == "either"].round(1).to_string(index=False))

# %% [markdown]
# ## 2. Class transitions, present → future (present-day class limits)

# %%
moves = transitions.assign(direction=np.sign(transitions["to_class"] - transitions["from_class"]))
moves = (moves.groupby(["variant", "climate", "rp", "risk", "direction"])[["buildings", "residents"]].sum()
         .unstack("direction", fill_value=0))
moves.columns = [f"{m}_{ {-1: 'down', 0: 'same', 1: 'up'}[d]}" for m, d in moves.columns]
moves = moves.reset_index()
moves.to_csv(RESULTS / "class_moves.csv", index=False)
print(moves[(moves["variant"] == "counts") & (moves["rp"] == 100)].round(0).to_string(index=False))

# %% [markdown]
# ## 3. The shift in return period
#
# For each future scenario, the return period whose design rainfall is closest to today's
# 100-year rainfall, and the residents at risk at that return period against today's
# 100-year storm.

# %%
shift = []
for c in FUTURE:
    rp_eq = int((rain[c] - rain.loc[100, "present"]).abs().idxmin())
    either = wide.loc["either"]
    shift.append({"climate": c, "present_rp100_mm": rain.loc[100, "present"],
                  "future_rp_with_closest_rainfall": rp_eq, "its_rainfall_mm": rain.loc[rp_eq, c],
                  "residents_at_risk_present_rp100": either.loc[100, "present"],
                  "residents_at_risk_future_at_that_rp": either.loc[rp_eq, c]})
shift = pd.DataFrame(shift)
shift.to_csv(RESULTS / "return_period_shift.csv", index=False)
print(shift.round(2).to_string(index=False))

# %% [markdown]
# ## 4. How plausible is the future rainfall?
#
# REACHOUT's change factors (future / present design rainfall) against the Climate DT
# changes over La Rioja (1 h and 3 h; return periods common to both), from the analysis.

# %%
factors = pd.DataFrame({c: 100 * (rain[c] / rain["present"] - 1) for c in FUTURE})
checks = pd.read_csv(CLEAN / "rainfall_checks.csv")
checks = checks[(checks["domain"] == "La Rioja") & checks["duration_h"].isin([1, 3])]
compare = checks.assign(change_pct=100 * checks["change"], ci_lo_pct=100 * checks["ci_lo"],
                        ci_hi_pct=100 * checks["ci_hi"])[["source", "duration_h", "rp", "change_pct", "ci_lo_pct", "ci_hi_pct"]]
compare.to_csv(RESULTS / "rainfall_plausibility.csv", index=False)
print("REACHOUT change factors (%):")
print(factors.round(1).T.to_string())
print(compare.round(1).to_string(index=False))

# %% [markdown]
# ## Does the finding hold in every case?

# %%
either = change[change["risk"] == "either"]
claim = {
    "aida": "Heavier future design rainfall increases the number of residents of Logroño living in buildings "
            "at pluvial flood risk.",
    "residents_at_risk_higher_in_every_case": bool((change[[f"{c}_minus_present" for c in FUTURE]] > 0).all().all()),
    "cases_checked": int(len(change) * len(FUTURE)),
    "buildings_moving_down_a_class": int(moves[[c for c in moves.columns if c.startswith("buildings_down")]].sum().sum()),
    "residents_increase_range_either": [float(either[[f"{c}_minus_present" for c in FUTURE]].min().min()),
                                        float(either[[f"{c}_minus_present" for c in FUTURE]].max().max())],
    "residents_increase_pct_range_either": [float(either[[f"{c}_pct" for c in FUTURE]].min().min()),
                                            float(either[[f"{c}_pct" for c in FUTURE]].max().max())],
}
claim["holds"] = claim["residents_at_risk_higher_in_every_case"]
(RESULTS / "claim_test.json").write_text(json.dumps(claim, indent=2, ensure_ascii=False))
claim
