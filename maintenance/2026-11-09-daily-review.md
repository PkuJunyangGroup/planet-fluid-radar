# Daily maintenance review — 2026-11-09 (Asia/Shanghai)

## Scope and execution

Used the authorized PkuJunyangGroup cloud GitHub connection only. Identity and repository push permission were verified. Latest configuration, topics, journals, README, workflow and previous maintenance record were reviewed. No user computer, alternative account, credentials, Worker/D1 changes, duplicate source retrieval or manual workflow dispatch was used.

The morning and 15:28 checks found no November 9 run. Scheduled run [42582388703](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42582388703) subsequently started at 15:55:41 and completed successfully at 16:05:43 Beijing time. Data commit: `0ee252013980b7177e7d334a8c42c18792447e9d`. Main was checked again at that commit before this report-only addition. This commit uses [skip ci] to avoid another retrieval/deployment.

## Actual enabled source results

All four configured arXiv categories succeeded and returned zero records in this run. Exoplanet.eu succeeded: two pages checked, two recent entries, zero relevant additions. The 19 enabled journals succeeded, with 67 retrieved and 38 retained in the source archive. These are source retrieval/archive counts, not public admissions. Disabled ocean journals are not included in these current-run figures.

| Enabled journal | Retrieved | Retained |
|---|---:|---:|
| Nature | 3 | 0 |
| Science | 1 | 1 |
| PNAS | 0 | 0 |
| Nature Geoscience | 0 | 0 |
| Nature Astronomy | 0 | 0 |
| Nature Climate Change | 0 | 0 |
| Journal of the Atmospheric Sciences | 0 | 0 |
| Atmospheric Chemistry and Physics | 19 | 9 |
| Journal of Geophysical Research: Atmospheres | 0 | 0 |
| Journal of Climate | 0 | 0 |
| Climate Dynamics | 0 | 0 |
| Climate of the Past | 3 | 3 |
| Quarterly Journal of the Royal Meteorological Society | 1 | 1 |
| Astrobiology | 1 | 1 |
| Geophysical Research Letters | 3 | 0 |
| Journal of Geophysical Research: Planets | 36 | 23 |
| The Astrophysical Journal | 0 | 0 |
| The Astrophysical Journal Letters | 0 | 0 |
| Earth and Planetary Science Letters | 0 | 0 |

No actual source failure or supplemental retrieval was recorded. Simulated failure messages in the unit-test section are not production source failures. Zero returned records do not establish that a journal published nothing.

## Admissions and review coverage

Public catalog remains 213 papers; raw archive count increased from 2730 to 2757 (+27). Daily intake ran for 2026-11-09 in one_year_fallback mode, selected zero and recorded zero search errors, retaining the configured two-day priority and 365-day / score >=65 / maximum-three fallback policy.

Today-published/updated public additions: 0. Yesterday-published papers newly admitted today: 0. One-year supplements: 0. There are no new admitted bibliographic entries to list. 今日无新增相关文献。

The complete available catalog commit diff contains no per-paper content changes. Public titles, authors, abstracts, publication dates, first_seen and version/duplicate relationships are unchanged; 29 duplicates remain linked. No abstracts were supplemented. Network data changed only its generation timestamp.

This is a source/status and public-diff review, not a claim of complete original-abstract reading. The 27 newly archived records were NOT individually read: the GitHub connector returned empty content for the oversized journal_records.json even with a line range, the commit API supplied no patch for that file, and the separate cloud-browser archive read timed out. Attempts stopped without bypassing earlier restrictions. Their original-abstract and metadata audit remains incomplete; automated rule filtering must not be represented as reading review.

## Historical metadata maintenance

The scheduled job retried 22 unavailable affiliation records; only checked_at changed and status remains unavailable. It added 60 checked ORCID-name cache entries, all with name_zh null; no new Chinese-name or author identity mapping was established. No names or institutions were guessed. Public network remains 122 parent institutions, 765 links and 213 papers, with 50 papers lacking a confirmed parent institution.

## Tests and publication

Scheduled Python unit tests: 90 passed. Source updates, enrichment/date processing, daily intake, catalog/network builds and Pages publication all succeeded. Catalog generated_at: 2026-11-09T08:05:27.157418+00:00. Independent cloud website verification of live catalog.json, network.json and related pages was reported successful to the coordinating dot. The report-only commit does not change public site data or require another deployment.

## Unfinished items

- Individually read and verify the 27 newly archived records when an authorized working read path is available; no full-reading claim is made today.
- Existing three public missing abstracts and 50 missing confirmed parent affiliations remain unresolved.
- Existing Exoplanet parser limitations remain unchanged; no backend or database changes were attempted.
