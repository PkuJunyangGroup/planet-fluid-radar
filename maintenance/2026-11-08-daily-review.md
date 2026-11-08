# Daily review: November 8, 2026 (Beijing)

## Scope and execution
Verified the authorized PkuJunyangGroup identity and repository permissions, current maintenance configuration, topics, journals, README, daily workflow and prior review. Only the authorized cloud/GitHub connection was used. Four arXiv categories, 19 enabled journals and incremental Exoplanet.eu remain the production scope. Disabled journals remain disabled.

The morning check preceded today's delayed scheduled run. Run 42458168750 started at 15:17:18 Beijing and completed successfully at 15:26:13:
https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42458168750

Generated data commit: 00c8999efeeb1d896e46a0037993a568d0fc3c32. No manual dispatch, duplicate retrieval, supplementary full search or prior-denial bypass was performed.

## Source coverage
All four arXiv categories succeeded with zero retrieved records at 15:17:34 Beijing. All 19 enabled journal requests succeeded at the shared 15:18:03 checkpoint. Counts below represent retrieved / source-archive retained records, not new public admissions; retained entries can already exist.

| Journal | Retrieved | Retained |
| --- | ---: | ---: |
| Nature | 26 | 2 |
| Science | 0 | 0 |
| PNAS | 0 | 0 |
| Nature Geoscience | 0 | 0 |
| Nature Astronomy | 1 | 0 |
| Nature Climate Change | 0 | 0 |
| Journal of the Atmospheric Sciences | 0 | 0 |
| Atmospheric Chemistry and Physics | 25 | 13 |
| Journal of Geophysical Research: Atmospheres | 6 | 6 |
| Journal of Physical Oceanography | 46 | 33 |
| Ocean Modelling | 30 | 7 |
| Paleoceanography and Paleoclimatology | 52 | 34 |
| Journal of Geophysical Research: Oceans | 95 | 49 |
| Journal of Climate | 0 | 0 |
| Climate Dynamics | 0 | 0 |
| Climate of the Past | 4 | 4 |
| Quarterly Journal of the Royal Meteorological Society | 1 | 0 |
| Astrobiology | 0 | 0 |
| Geophysical Research Letters | 70 | 28 |
| Journal of Geophysical Research: Planets | 2 | 0 |
| The Astrophysical Journal | 0 | 0 |
| The Astrophysical Journal Letters | 1 | 0 |
| Earth and Planetary Science Letters | 1 | 0 |

Exoplanet.eu succeeded at 15:17:59 Beijing, checking two pages and one recent bibliography entry, retaining zero. Production failures: 0; no failure replenishment was needed. Zero retrieved counts do not imply no publications at those journals.

The scheduled daily intake used one_year_fallback after finding no suitable recent addition. It selected zero items and reported zero search errors. No further fallback search was repeated. Limits remain 365 days, score at least 65, maximum three.

## Review coverage and changes
Public catalog remains 213 papers with 210 nonempty supplied original abstracts. Newly admitted: 0. Selected new originals to read: 0; no new-item abstract-reading claim is made. The catalog still marks automated rule screening separately from reading review. Abstract supplements: 0. No manual scientific exclusions, metadata repairs, institution mappings or author/ORCID changes were made.

A comparison of the public catalog shows one existing paper's Crossref update timestamp changed from 2026-11-04T16:27:43Z to 2026-11-07T16:26:25Z:
- Imaging exoplanets below the telescope stability limit.
- Rodrigo Ferrer-Chavez; Jason J. Wang; Katherine L. Bouman; William T. Freeman; Laurent Pueyo; Brandon Y. Feng; Marshall D. Perrin.
- Nature; https://doi.org/10.1038/s41586-026-11213-z .
- Publication November 4; first indexed November 5 (first_seen 2026-11-05T07:54:11.251929+00:00).
Its title, abstract, authors and publication date are unchanged. This is a deposited metadata timestamp refresh, not a new paper or verified paper revision. No first_seen reset occurred.

Raw record count increased from 2698 to 2730 (+32), but these are not public admissions. Individual fresh raw-journal entries were not completely audited: connector file retrieval returned empty oversized content, and blob retrieval encountered a transport failure. This limits manual archive review, not the successful production source retrieval. No assertion that every fresh archive abstract was read is made.

## Tests and publication
The scheduled workflow passed all 90 Python tests, enrichment/date processing, intake and catalog/network builds, then published Pages successfully. Failure strings in test recovery fixtures are not production failures. No separate executor test run or code change is claimed.

Catalog generated_at: 2026-11-08T07:25:59.137579+00:00 (15:25:59 Beijing). Network content is unchanged apart from generation time: 122 parent institutions, 765 links, 213 catalog papers, 50 without confirmed parent institution. Independent live cloud verification reported catalog.json, network.json and related pages current, 213 papers, zero new items, successful checkpoints and Pages publication.

## Daily classification and unfinished items
- Published/revised today among new admissions: 0.
- Yesterday's paper first admitted today: 0.
- One-year supplement admissions: 0.
- Historical metadata refresh: 1 timestamp only.
- New abstract supplements: 0.
- Today has no newly admitted relevant literature.

Existing three missing public abstracts and incomplete institution coverage remain. The previously quarantined Exoplanet parser/source-format issue is not claimed resolved. Full fresh raw-journal archive reading remains incomplete for the access reason above. No Worker/D1, credentials, layout or configuration changes were made.

This report-only commit uses [skip ci]; it does not initiate another retrieval or deployment. Main was re-read immediately before preparing the commit to preserve the scheduled workflow's data.
