# Snakefile — orchestrates the pipeline end-to-end.
#
# Each rule wraps a notebook executed via jupytext (the notebook stays the source of
# truth and the Snakefile just sequences them). Inputs are files that are never
# committed (data/), so a fresh checkout always starts from the download.
#
# Usage:
#   snakemake --cores 1                  # run everything
#   snakemake --cores 1 -n               # dry run

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"


rule all:
    input:
        f"{FIGURES}/main_result.png",
        f"{RESULTS}/claim_test.json",


# ---------- 01: the analysis release (Zenodo) ----------
rule data_download:
    output:
        f"{DATA}/raw/sources.json",
    log:
        f"{RESULTS}/logs/01_data_download.log",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 01_data_download.py 2>&1 | tee ../{{log}}"


# ---------- 02: the inputs of this finding ----------
rule data_clean:
    input:
        f"{DATA}/raw/sources.json",
    output:
        f"{DATA}/clean/at_risk.csv",
        f"{DATA}/clean/transitions.csv",
        f"{DATA}/clean/rainfall.csv",
        f"{DATA}/clean/rainfall_checks.csv",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 02_data_clean.py"


# ---------- 03: the finding ----------
rule analysis:
    input:
        f"{DATA}/clean/at_risk.csv",
        f"{DATA}/clean/transitions.csv",
        f"{DATA}/clean/rainfall.csv",
        f"{DATA}/clean/rainfall_checks.csv",
    output:
        f"{RESULTS}/claim_test.json",
        f"{RESULTS}/residents_at_risk_change.csv",
        f"{RESULTS}/class_moves.csv",
        f"{RESULTS}/return_period_shift.csv",
        f"{RESULTS}/rainfall_plausibility.csv",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 03_analysis.py"


# ---------- 04: figures ----------
rule figures:
    input:
        f"{DATA}/clean/at_risk.csv",
        f"{RESULTS}/rainfall_plausibility.csv",
    output:
        f"{FIGURES}/main_result.png",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 04_figures.py"
