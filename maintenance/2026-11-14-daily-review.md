# Daily reading review — 2026-11-14 (Asia/Shanghai)

## Scope and run
Cloud-only, designated authenticated PkuJunyangGroup connection, target repository main only. Current cloud-maintenance.json, topics.json, journals.json, README, workflow and preceding maintenance consulted. No user computer, manual full scrape, source reconfiguration, speculative identity mapping, paid API or shared recommendation vote.
At the morning check no November 14 run existed. The delayed scheduled run [43571801859](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/43571801859) subsequently started at 07:35:17 UTC (15:35:17 Beijing), completed successfully and deployed. Generated-data commit e9c358cd4511dbd2a2907cb136c6619a887c1a0e. All 90 tests passed; simulated fixture errors are not actual fetch failures. No duplicate full ingestion or corrective deployment required.

## Sources and counts
All four enabled arXiv categories succeeded with 0 records in the incremental window. This is not a claim that arXiv has no publications. Exoplanet.eu succeeded: 12 recent entries examined over 2 pages, 0 additions.
All 19 enabled journal queries succeeded. Retrieved/retained archive counts: Nature 17/0; Science 0/0; PNAS 13/0; Nature Geoscience 1/0; Nature Astronomy 5/0; Nature Climate Change 1/0; JAS 2/2; ACP 62/14; JGR Atmospheres 0/0; Journal of Climate 13/12; Climate Dynamics 0/0; Climate of the Past 1/1; QJRMS 3/1; Astrobiology 0/0; GRL 5/1; JGR Planets 0/0; ApJ 11/1; ApJL 2/1; EPSL 0/0.
No source recovery was required. Zero queried/retained records do not imply zero publisher output. No exhaustive independent publisher-TOC audit was performed.
Raw record_count 2980 -> 3002 (+22); public count 229 -> 231 (+2). Catalog diff has only two new paper IDs, no removal or new merged duplicate; linked-duplicate count remains 31. Monthly Crossref registration cache was refreshed at 2026-11-14T07:37:57.121770+00:00 for current/previous months; registrations are not all research publications or site selections, and November remains incomplete.

## Individual abstract-level review
Both newly selected records were read in full from the successfully retrieved publisher-deposited original abstracts in the source-backed catalog/diff. Both pass the existing narrow planetary scope. This is not full-paper peer review. Direct DOI web opens did not return publisher pages; exact-title/DOI web searches did not supply corroborating records. Publication dates and author metadata below therefore rely on the fetched Crossref publisher records, not a claimed independent publisher landing-page verification.

1. [Energy-enstrophy balance and the evolving shape of Jupiter’s Great Red Spot](https://doi.org/10.1175/jas-d-25-0238.1)
   - Authors: A. Constantin; A. Ionescu. Journal of the Atmospheric Sciences.
   - Publisher-deposited published-print date: 2026-11-13. Day precision only; no time invented.
   - first_seen: 2026-11-14T07:35:58.025758+00:00 (15:35:58 Beijing), preserved.
   - Direct Jovian upper-tropospheric vortex dynamics. Variational maximum-energy/fixed-enstrophy circular vortex is an explanatory benchmark, not an inevitable terminal state; the original abstract explicitly notes the mismatch with the observed hollow core and omitted processes.
   - Keep. Existing automatic topic field is empty after public filtering, despite clear planetary relevance; source-preserving scoped topic-label improvement remains pending. Original affiliation strings contain footnote prefixes (aUniversity/b Princeton); no guessed identity or mapping was introduced.

2. [Stellar Flares Rather than High T int as Possible Cause for the Missing Methane in Young Exoplanets: The Case Study of V1298 Tau b](https://doi.org/10.3847/2041-8213/aeb6e0)
   - Authors: Danica Adams; Pierre-Alexis Roy; Hilke E. Schlichting; Björn Benneke. The Astrophysical Journal Letters.
   - Publisher-deposited published-online date: 2026-11-13; published-print date: 2026-11-20. The online date, not the future print date, is used.
   - first_seen: 2026-11-14T07:35:58.025758+00:00 (15:35:58 Beijing), preserved.
   - Direct warm-exoplanet atmospheric photochemistry: flare-driven methane depletion and recovery versus flare recurrence, tested through transmission spectra for V1298 Tau b. Retain, not a generic stellar-activity paper.
   - Source affiliation is only The University of California; campus/individual assignments were not guessed. Existing source-explicit ORCIDs were preserved without new name-based matching. Public title retains source plain-text T int formatting.

No excluded selections, no invented/supplemented/translated abstracts, no one-year fallback, no global-rule changes. Reading decisions recorded here without changing source records.

## Online verification
Live catalog.json read in cloud browser: generated_at 2026-11-14T07:44:41.490774+00:00 (15:44:41 Beijing), 231 papers, daily new_count 2, the two IDs above, older_ids and updated_ids empty, source_issues empty. There are 228 nonempty original abstracts and the same 3 historical missing abstracts.
Live network.json has matching generated_at, 124 parent institutions, 794 edges, 56 papers without confirmed parent. Missing affiliation is not a failed literature fetch.
Homepage shows both new English titles, author metadata, journal/year and collapsed abstracts. The first new paper's complete original abstract was expanded, read with Published 2026-11-13 / Added 2026-11-14, then recollapsed. Recommendation controls were present but no votes were cast; this is not a write-backend test. No UI code changed.

## Limits and remaining work
Only the two new public selections received individual abstract reading in this pass, not all 22 new raw records, all rejected candidates, all 3002 archive records, all historical public papers or every publisher TOC. No exhaustive institution drilldown, all-ORCID click test or independent current source-page/monthly-bar interaction test was performed.
The existing three missing abstracts remain: 10.1038/s41561-026-02094-y; 10.1038/s41561-026-02116-9; 10.1177/15311074261485884. Prior bibliography-parser quarantine, withdrawal handling, formula/accessibility cleanup, and pending 10.1029/2026JE009951 date issue remain unresolved. The two new papers' source affiliation precision and the Jovian paper's topic-filter omission are explicitly pending; no guessed correction was made.
