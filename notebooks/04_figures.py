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
# # 04 — Figures
#
# `figures/main_result.png` is this chain's headline figure. Saved and displayed inline
# (`plt.show()` after `fig.savefig()`; no `matplotlib.use('Agg')`). Before saving, the
# figure passes `scripts/figcheck.py`: no overlapping text, no legend over data.
#
# Colours: the three climates (or rainfall sources) take the first three categorical slots
# of a palette validated for colour-vision deficiency; lines are labelled directly.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path("../scripts").resolve()))
from figcheck import assert_layout, spread_labels  # noqa: E402

RESULTS = Path("../results")
CLEAN = Path("../data/clean")
FIGURES = Path("../figures")
FIGURES.mkdir(parents=True, exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")
DPI = 150
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
CLIMATE = {"present": (BLUE, "present rainfall"), "CC_Q50": (ORANGE, "future, median (Q50)"),
           "CC_Q90": (AQUA, "future, 90th pct. (Q90)")}
TEXT, MUTED = "#0b0b0b", "#52514e"
RPS = [2, 5, 10, 25, 50, 100, 200]


def style_axis(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", visible=False)
    ax.tick_params(colors=MUTED, labelsize=9)


def log_rp_axis(ax, ticks: list[int], right: float) -> None:
    ax.set_xscale("log")
    ax.set_xticks(ticks, labels=[str(t) for t in ticks])
    ax.set_xlim(1.7, right)
    ax.set_xlabel("Return period of the design storm (years)", color=MUTED, fontsize=9)


# %% [markdown]
# ## Headline figure
#
# (a) Residents in buildings at pluvial flood risk (either risk index above zero), current
# green cover. (b) The increase from present to future rainfall at each return period.
# (c) The change in short-duration rainfall extremes behind the future scenarios
# (REACHOUT, 15 min) against the Destination Earth Climate DT over La Rioja (1 h; 90 %
# intervals).

# %%
at_risk = pd.read_csv(CLEAN / "at_risk.csv")
either = at_risk[at_risk["risk"] == "either"].pivot(index="rp", columns="climate", values="residents_at_risk")
rain = pd.read_csv(CLEAN / "rainfall.csv", index_col="rp")
plaus = pd.read_csv(RESULTS / "rainfall_plausibility.csv")

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
ax = axes[0]
labels = []
for c, (colour, label) in CLIMATE.items():
    ax.plot(either.index, either[c] / 1000, color=colour, lw=2, marker="o", ms=5, markeredgecolor="white",
            markeredgewidth=1.5)
    labels.append((either.index[-1], either[c].iloc[-1] / 1000, label))
log_rp_axis(ax, RPS, 3000)
ax.set_ylabel("Residents in buildings at risk (thousands)", color=MUTED, fontsize=9)
ax.set_title("(a) Residents at risk", loc="left", fontsize=11, color=TEXT)
style_axis(ax)

ax = axes[1]
x = np.arange(len(RPS))
for k, c in enumerate(["CC_Q50", "CC_Q90"]):
    colour, label = CLIMATE[c]
    ax.bar(x + (k - 0.5) * 0.38, (either.loc[RPS, c] - either.loc[RPS, "present"]), width=0.36, color=colour,
           label=label)
ax.axhline(0, color="#a3a29b", lw=1)
ax.set_xticks(x, labels=[str(r) for r in RPS])
ax.set_xlabel("Return period of the design storm (years)", color=MUTED, fontsize=9)
ax.set_ylabel("More residents at risk than with present rainfall", color=MUTED, fontsize=9)
ax.set_title("(b) Increase at every return period", loc="left", fontsize=11, color=TEXT)
ax.legend(loc="upper left", fontsize=8.5, frameon=False, bbox_to_anchor=(0.0, 1.0), ncol=1)
ax.set_ylim(0, (either[["CC_Q50", "CC_Q90"]].sub(either["present"], axis=0)).max().max() * 1.45)
style_axis(ax)

ax = axes[2]
line_labels = []
for c, ls in (("CC_Q50", "-"), ("CC_Q90", "--")):
    y = 100 * (rain[c] / rain["present"] - 1)
    ax.plot(rain.index, y, color=BLUE, lw=2, ls=ls)
    line_labels.append((rain.index[-1], y.iloc[-1], f"REACHOUT {c[-3:]} (15 min)"))
for source, colour in (("Climate DT projection (IFS-NEMO, SSP3-7.0)", ORANGE),
                       ("Climate DT storylines (+2 °C vs present)", AQUA)):
    p = plaus[(plaus["source"] == source) & (plaus["duration_h"] == 1)].sort_values("rp")
    ax.fill_between(p["rp"], p["ci_lo_pct"], p["ci_hi_pct"], color=colour, alpha=0.13, lw=0)
    ax.plot(p["rp"], p["change_pct"], color=colour, lw=2, marker="o", ms=5, markeredgecolor="white",
            markeredgewidth=1.5)
    short = "Climate DT projection (1 h)" if "projection" in source else "Climate DT storylines, +2 °C (1 h)"
    line_labels.append((p["rp"].iloc[-1], p["change_pct"].iloc[-1], short))
ax.axhline(0, color="#a3a29b", lw=1)
log_rp_axis(ax, [2, 5, 10, 20, 50, 100, 200], 9000)
ax.set_ylabel("Change in rainfall extreme (%)", color=MUTED, fontsize=9)
ax.set_title("(c) How much heavier is the rainfall?", loc="left", fontsize=11, color=TEXT)
style_axis(ax)

fig.suptitle("Logroño (Spain): heavier future rainfall puts more residents in buildings at pluvial flood risk",
             x=0.01, ha="left", fontsize=12.5, color=TEXT)
fig.tight_layout()
spread_labels(axes[0], labels, fontsize=8.5, color=TEXT)
spread_labels(axes[2], line_labels, fontsize=8.5, color=TEXT)
assert_layout(fig)
fig.savefig(FIGURES / "main_result.png", dpi=DPI, bbox_inches="tight")
plt.show()
