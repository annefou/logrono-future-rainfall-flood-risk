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
# # 02 — The inputs of this finding
#
# From the analysis release (01), the tables this finding needs — all for the **current
# green cover** (REACHOUT `Baseline`), so that only the rainfall differs:
#
# | Table | From the analysis's `results/` | Content |
# |---|---|---|
# | `at_risk.csv` | `building_risk.parquet` | residents and buildings at risk (either risk index above zero, and each risk) per climate and return period |
# | `transitions.csv` | `class_transitions.csv` | buildings and residents moving between risk classes (present-day limits), present → future |
# | `rainfall.csv` | `reachout_inventory.csv` | the design rainfall (mm in 15 min) of each climate and return period |
# | `rainfall_checks.csv` | `climatedt_projection_change.csv`, `storyline_change.csv`, `cordex_match.csv` | how plausible the future rainfall is |
#
# Both indicator versions of the analysis are kept (`counts`, the paper's definition, and
# `rates`); whether a building is at risk does not depend on the version, its class does.

# %%
import json
from pathlib import Path

import pandas as pd

RAW = Path("../data/raw")
ANALYSIS = Path(json.loads((RAW / "sources.json").read_text())["analysis"]["path"])
RESULTS_A = ANALYSIS / "results"
CLEAN = Path("../data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)
CLIMATES = ["present", "CC_Q50", "CC_Q90"]

# %% [markdown]
# ## Residents and buildings at risk

# %%
risk = pd.read_parquet(RESULTS_A / "building_risk.parquet",
                       filters=[("variant", "==", "counts"), ("land_cover", "==", "Baseline")])
risk["either"] = (risk["PFRWB"] > 0) | (risk["PFRMA"] > 0)
rows = []
for (climate, rp), g in risk.groupby(["climate", "rp"]):
    for name, mask in {"either": g["either"], "PFRWB": g["PFRWB"] > 0, "PFRMA": g["PFRMA"] > 0}.items():
        rows.append({"climate": climate, "rp": rp, "risk": name, "buildings_at_risk": int(mask.sum()),
                     "residents_at_risk": float(g.loc[mask, "R"].sum())})
at_risk = pd.DataFrame(rows)
at_risk.to_csv(CLEAN / "at_risk.csv", index=False)
print(at_risk[at_risk["risk"] == "either"].pivot(index="rp", columns="climate", values="residents_at_risk")[CLIMATES]
      .round(0).to_string())

# %% [markdown]
# ## Class transitions, present → future

# %%
tr = pd.read_csv(RESULTS_A / "class_transitions.csv")
tr = tr[(tr["land_cover"] == "Baseline") & (tr["climate"] != "present")]
tr.to_csv(CLEAN / "transitions.csv", index=False)
print(f"{len(tr)} transition rows (both indicator versions, both risks, 2 climates, 7 return periods)")

# %% [markdown]
# ## Design rainfall and its plausibility

# %%
inv = pd.read_csv(RESULTS_A / "reachout_inventory.csv").drop_duplicates(["climate", "rp"])
rain = inv.pivot(index="rp", columns="climate", values="published_mm")[CLIMATES]
rain.to_csv(CLEAN / "rainfall.csv")
print(rain.to_string())

proj = pd.read_csv(RESULTS_A / "climatedt_projection_change.csv").assign(source="Climate DT projection (IFS-NEMO, SSP3-7.0)")
story = pd.read_csv(RESULTS_A / "storyline_change.csv")
story = story[story["climate"] == "Tplus2.0K"].assign(source="Climate DT storylines (+2 °C vs present)")
checks = pd.concat([proj, story], ignore_index=True)[["source", "domain", "duration_h", "rp", "change", "ci_lo", "ci_hi"]]
checks.to_csv(CLEAN / "rainfall_checks.csv", index=False)
cordex = pd.read_csv(RESULTS_A / "cordex_match.csv")
cordex.to_csv(CLEAN / "cordex_match.csv", index=False)
print(cordex.head(3).round(3).to_string(index=False))
