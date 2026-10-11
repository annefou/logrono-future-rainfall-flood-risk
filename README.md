# logrono-future-rainfall-flood-risk

[![CI](https://github.com/annefou/logrono-future-rainfall-flood-risk/actions/workflows/ci.yml/badge.svg)](https://github.com/annefou/logrono-future-rainfall-flood-risk/actions/workflows/ci.yml)
[![Jupyter Book](https://github.com/annefou/logrono-future-rainfall-flood-risk/actions/workflows/jupyter-book.yml/badge.svg)](https://annefou.github.io/logrono-future-rainfall-flood-risk/)
[![Docker](https://github.com/annefou/logrono-future-rainfall-flood-risk/actions/workflows/docker.yml/badge.svg)](https://github.com/annefou/logrono-future-rainfall-flood-risk/pkgs/container/logrono-future-rainfall-flood-risk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23299756.svg)](https://doi.org/10.5281/zenodo.23299756)
[![FAIR4RS](https://img.shields.io/badge/FAIR4RS-conformant-brightgreen)](docs/fair4rs-checklist.md)
[![FORRT](https://img.shields.io/badge/FORRT-chain-blue)](https://forrt.org/)
[![Science Live](https://img.shields.io/badge/Science%20Live-nanopub%20chain-purple)](nanopubs/PUBLISHED.md)
[![RO-Crate](https://img.shields.io/badge/RO--Crate-1.2-orange)](ro-crate-metadata.json)
[![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/annefou/logrono-future-rainfall-flood-risk/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/annefou/logrono-future-rainfall-flood-risk)

> **Does heavier future rainfall put more residents of Logroño (Spain) in buildings at pluvial flood risk?** — one FORRT nanopublication chain.
> Built on the [Logroño flood-adaptation scenarios analysis v0.1.0](https://doi.org/10.5281/zenodo.23298913) ([repository](https://github.com/annefou/logrono-flood-adaptation-scenarios)). Method: [Vogelbacher et al. (2026), NHESS](https://doi.org/10.5194/nhess-26-2765-2026).

**Finding (AIDA):** *Heavier future design rainfall increases the number of residents of Logroño living in buildings at pluvial flood risk.* It holds in all 42 cases examined (7 return periods × 3 risk measures × 2 future scenarios), and no building moves to a lower risk class. Today's 100-year storm becomes a 50-year storm (median scenario) or a 25-year storm (90th percentile). REACHOUT's median scenario is of the same order as the Destination Earth Climate DT; its 90th percentile is a high-end case.

![Headline figure](figures/main_result.png)

## Pipeline

| Step | Notebook | What it does |
|---|---|---|
| 1 | [`01_data_download`](notebooks/01_data_download.py) | Downloads the analysis release (MD5-checked) and uses its result tables; `RERUN_ANALYSIS = True` re-runs the analysis itself |
| 2 | [`02_data_clean`](notebooks/02_data_clean.py) | Residents at risk, class transitions, design rainfall and rainfall checks for the current green cover |
| 3 | [`03_analysis`](notebooks/03_analysis.py) | The finding in every case (`results/claim_test.json`), class moves, return-period shift, rainfall plausibility |
| 4 | [`04_figures`](notebooks/04_figures.py) | `figures/main_result.png`, checked for overlapping labels |

```bash
git clone https://github.com/annefou/logrono-future-rainfall-flood-risk.git
cd logrono-future-rainfall-flood-risk
pixi install
pixi run snakemake --cores 1
```

## The chain

Drafts in [`nanopubs/drafts/`](nanopubs/drafts/), the wizard hand-off in [`nanopubs/chain-draft.json`](nanopubs/chain-draft.json), published URIs in [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md). Related: the Logroño replication's chain (<https://w3id.org/sciencelive/np/RAoFYugT7OVk5eoHuxKCO9HeqA08jMfSn7TeUxwZcbezE>) and the study area (<https://w3id.org/sciencelive/np/RAzds1z9t2ac7XFvx_Hsv18__p5nUTNA0NHIsskSyLVPQ>). Sibling chains: [planned nature-based solutions](https://github.com/annefou/logrono-planned-nbs-flood-risk), [greening and social vulnerability](https://github.com/annefou/logrono-greening-flood-risk-vulnerability).

## Data and credits

Flood maps and EURO-CORDEX IDF data: Andrea Staccione, Jeremy S. Pal (REACHOUT, CC BY 4.0). Buildings: Dirección General del Catastro. Census: INE. Climate DT: ECMWF and the Climate DT consortium (led by CSC), Destination Earth — *this data is created based on data of the European Union, using the Destination Earth Platform, but has been modified by Anne Fouilloux.*

## Citation

Cite via [`CITATION.cff`](CITATION.cff) → DOI [10.5281/zenodo.23299756](https://doi.org/10.5281/zenodo.23299756), with the analysis [10.5281/zenodo.23298913](https://doi.org/10.5281/zenodo.23298913) and the method paper [10.5194/nhess-26-2765-2026](https://doi.org/10.5194/nhess-26-2765-2026).

Created from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template); see [`CLAUDE.md`](CLAUDE.md).
