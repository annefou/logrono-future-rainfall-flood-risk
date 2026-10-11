# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
logrono-future-rainfall-flood-risk-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

Human-readable title.

```
Building-level pluvial flood risk in Logroño under present and future design rainfall (REACHOUT scenarios)
```

<!-- field: type -->
### Choose the study type (dropdown, required)

- [x] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results. See `docs/pico-study-outcome-levels.md`.

```
Whether the number of residents living in buildings at pluvial flood risk in Logroño (Spain) increases when present-day design rainfall is replaced by the heavier design rainfall of future climate scenarios, with the city's current green cover held fixed. In scope: every residential building inside the area modelled by all flood scenarios; the seven design storms of REACHOUT (return periods of 2 to 200 years); both future scenarios (EURO-CORDEX median and 90th percentile); both risk indices of the framework (risk to well-being, risk to mobility and accessibility) and either of them; the movement of buildings between risk classes defined on present-day conditions; which future storm carries today's 100-year rainfall. Also in scope, as context, how plausible the future rainfall is, compared with the Destination Earth Climate DT. Out of scope: changes in land cover or nature-based solutions (separate chains), population change (residents fixed at the 2021 census), sewers, absolute flood depths, and the validity of social vulnerability, which no impact data can test. This is an application of the Vogelbacher et al. (2026) framework to climate scenarios, not a re-test of a claim of that paper.
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
Data and pipeline: the shared analysis Logroño flood-adaptation scenarios, release v0.1.0 (10.5281/zenodo.23298913), whose result tables this chain reads (its pipeline can be re-run from the same repository). Flood hazard: REACHOUT pluvial flood maps for Logroño (Staccione and Pal, 10.5281/zenodo.14035876), SaferRAIN, 2 m, 15-minute design storms; present rainfall from local station data, future rainfall scaled by the EURO-CORDEX change (2041-2070 vs 1976-2005, median and 90th percentile). The comparison is restricted to cells modelled in every scenario (NoData marks unmodelled cells, NaN dry ones). Flooded extents at depths of 30 to 100 cm are polygonised on the native grid, without resampling, and water bodies are removed. City inputs from the Logroño replication v0.1.1 (10.5281/zenodo.23285198): Cadastre buildings, census 2021 residents shared among buildings by dwellings, census-section vulnerability proxies, street area. Risk: building-climate-risk v0.2.1 (10.5281/zenodo.23285504) with the paper's settings (TOPSIS with entropy, weights children 0.3 / elderly people living alone 0.7 and welfare 0.5 / education 0.5; flood-sensitivity transform; hazard to well-being from a 2 m ring over depths of 30-100 cm; hazard to mobility from 5 / 15 / 30 m rings at 30 cm; risk = social vulnerability x exposure x hazard). Social vulnerability is ranked over all residential buildings of the city; a building is at risk when a risk index is above zero; classes use the replication's published limits for the 100-year storm and the present-day baseline's limits at other return periods. Measures: residents at risk under present and future rainfall at each return period; class transitions; the future return period whose rainfall equals today's 100-year rainfall. Rainfall plausibility: REACHOUT's change factors against its own EURO-CORDEX IDF data (10.5281/zenodo.14035736) and the Destination Earth Climate DT (10.21957/79c6af3105): generation-2 hourly precipitation (IFS-NEMO, SSP3-7.0, 2030-2049 vs 1990-2009) over La Rioja on HEALPix level 10, regional index-flood GEV (L-moments), 1,000 year resamples; and the storylines (IFS-FESOM nudged to ERA5, 2017-2024, five members, present and +2 °C).
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
From the framework of Vogelbacher et al. (2026): (1) hazard model REACHOUT SaferRAIN (hydrostatic fill-and-spill with Green-Ampt infiltration, no sewer network, 15-minute storms) instead of VISDOM-SWMM; flood depths on a 2 m grid labelled UTM zone 32, not resampled; (2) census-section proxies for the vulnerability indicators, as in the Logroño replication; residents fixed at 2021; (3) comparison restricted to the area modelled by every scenario: 157 buildings (77 with residents, 1,851 residents) are left out; (4) class limits fixed on present-day conditions, so that a uniform increase of risk is not hidden by the authors' relative class rule. Future rainfall: (5) REACHOUT's factors cannot be reproduced exactly from its own EURO-CORDEX IDF file (closest: RCP8.5, 3-hour duration, within 0.055); changes estimated for 3-hour and longer durations are applied to 15-minute storms. Climate DT check: (6) single model (IFS-NEMO; IFS-FESOM and ICON hourly precipitation were not available through Polytope); hourly at best; (7) HEALPix cells selected on the sphere: on the WGS84 ellipsoid 41 of 125 cells (projections) and 10 of 28 (storylines) fall outside La Rioja; all changes are also computed over the cells inside on both conventions.
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

- urban flooding (Q15909735)
- flood risk (Q2288778)
- climate change adaptation (Q260607)
- extreme rainfall (Q111089542)
- Logroño (Q14325)

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

Provide labels.

- hydrology (Q42250)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
