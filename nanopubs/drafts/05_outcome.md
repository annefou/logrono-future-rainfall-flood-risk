# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/` and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
logrono-future-rainfall-flood-risk-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

Descriptive title.

```
Future design rainfall increases residents at pluvial flood risk in Logroño in every scenario and return period
```

<!-- field: study -->
### Choose study (search/select, required)

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: repo -->
### Repository URL (text input, required)

Use the Zenodo **version DOI** URL for the release the results came from — not a
bare branch URL, and not the concept DOI.

> **Why not the bare repo URL.** `https://github.com/ORG/REPO` names a *moving
> branch*. This Outcome asserts "this code produced this number", in a signed,
> immutable record. A branch URL means that assertion points at whatever `main`
> happens to be years from now — code that may never have produced the number
> above. A concept DOI has the same flaw: it resolves to the latest version.
> The version DOI pins the exact release. `docs/chain-decision-tree.md` § Anchor
> ranks the options: SWHID > Zenodo DOI > repo URL > Wayback.
>
> Both DOIs and the SWHID are in `CITATION.cff` under `identifiers:`, recorded
> automatically at release by `.github/workflows/release-identifiers.yml`. Take
> the one described as *"Version DOI"*.

```
https://doi.org/{{ZENODO_VERSION_DOI}}
```

<!-- field: date -->
### Choose completion date (text input, required)

```
2026-10-10
```

<!-- field: validationStatus -->
### Choose validation status (dropdown, required)


This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [ ] partially supported
- [x] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

_Vocabulary not yet captured._

```

```

- [ ] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [x] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

Substantive interpretation. Headline comparison: replication's number vs the paper's number, sign + significance.

```
Validated. In Logroño (Spain), with the current green cover, the heavier future design rainfall of the REACHOUT scenarios puts more residents in buildings at pluvial flood risk than present-day rainfall in every case examined: all seven return periods (2 to 200 years), both future scenarios (EURO-CORDEX median and 90th percentile) and each risk index of the framework. No building moves to a lower risk class. In effect, today's 100-year storm becomes a 50-year storm under the median scenario and a 25-year storm under the 90th-percentile scenario. How large the increase is depends on how much heavier the rainfall becomes: REACHOUT's median scenario is of the same order as the Destination Earth Climate DT estimates for La Rioja, while its 90th-percentile scenario lies above all of them, so the larger increases are a high-end case.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

Numerical results, test statistics, model coefficients. Read directly from `results/`.

```
Residents in buildings at risk (either risk index above zero), present / future median / future 90th percentile: 25,658 / 26,989 / 28,099 for the 2-year storm; 31,852 / 32,842 / 33,459 for the 10-year storm; 35,971 / 37,555 / 38,824 for the 100-year storm; 37,376 / 37,932 / 39,892 for the 200-year storm. Increase over present rainfall: +556 to +1,952 residents (+1.5 to +5.9 %) under the median scenario and +1,607 to +3,021 (+5.0 to +9.5 %) under the 90th percentile; higher in 42 of 42 cases (7 return periods x 3 risk measures x 2 scenarios). Class transitions with present-day class limits: for the 100-year storm, 40 (median) and 83 (90th percentile) buildings move up a mobility-risk class (2,033 and 4,571 residents) and 26 and 56 a well-being class; over all return periods 392 and 843 upward moves, none downward; with census-rate indicators 438 and 959 upward, none downward. Return-period shift: today's 100-year rainfall (26.77 mm in 15 minutes) is matched by the future 50-year storm under the median scenario (26.61 mm) and the 25-year storm under the 90th percentile (26.87 mm), with 35,951 and 36,055 residents at risk against 35,971 today. Rainfall: REACHOUT's future storms are +7 to +17 % (median) and +21 to +53 % (90th percentile) heavier than present ones. Destination Earth Climate DT over La Rioja: generation-2 projection (IFS-NEMO, SSP3-7.0, 2030-2049 vs 1990-2009) -2 % for 1-hour extremes (90 % interval about -15 to +13 %) and +5 to +16 % for 3-hour extremes (2- to 20-year return levels); storylines at +2 °C against the present +5 to +6 % for 1-hour extremes (interval +1 to +10 %). REACHOUT's factors are closest to the EURO-CORDEX RCP8.5 3-hour changes (within 0.055). Figure: figures/main_result.png; checks: results/claim_test.json.
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

Honest caveats. If the result is partial or contradicted, say so plainly. Don't overclaim.

```
These are scenarios, not predictions. One flood model: REACHOUT SaferRAIN (hydrostatic fill-and-spill with Green-Ampt infiltration, no sewer network) on 15-minute design storms; it fills terrain hollows completely, so local depths can be unrealistic, although the risk measures use only depths of 30 cm and more. The future rainfall is observed design rainfall scaled by EURO-CORDEX changes estimated for 3-hour and longer durations; REACHOUT does not state the emission scenario, and its factors cannot be reproduced exactly from its own IDF file. The Climate DT check uses one model (IFS-NEMO; IFS-FESOM and ICON were not available), hourly data at best and cells of about 6 km (projections) and 12 km (storylines), which cannot place a convective storm on a street; on the WGS84 ellipsoid a third of the delivered cells fall outside La Rioja, which changes the regional estimates by a few percentage points only. Residents are fixed at the 2021 census. Social vulnerability uses census-section proxies and was not validated against impact data; with the paper's count-based indicators, building size enters risk twice. 157 buildings near the edge of the modelled area (1,851 residents) are left out. The size of the increase depends strongly on the scenario: the 90th percentile gives about twice the median's.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
