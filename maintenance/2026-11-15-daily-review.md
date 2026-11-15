# Daily maintenance review — 2026-11-15 (Asia/Shanghai)

## Scope and execution
Only the designated authenticated PkuJunyangGroup cloud connection and target repository were used. Latest topics.json, journals.json, README.md, .github/workflows/daily.yml, cloud-maintenance.json and preceding review/fix context were checked. Configuration unchanged since yesterday's verified Great Red Spot topic fix.
At 09:58 Beijing no November 15 run existed. Delayed scheduled [run 43691656117](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/43691656117) subsequently began 2026-11-15T07:49:29Z (15:49:29 Beijing), completed successfully and deployed. All 91 tests passed. Data commit 29e2df296a6af6ef2666ca7a848b382a3cb972f9. No duplicate full scrape, recovery run, code change, institution guess or manual corrective deployment was performed.

## Sources
Four arXiv categories succeeded, each returning 0 records in its incremental window. Exoplanet.eu succeeded: 8 recent bibliography entries, 0 additions, 2 pages. This does not mean the sources have no publications.
All 19 enabled journal requests succeeded. Retrieved/retained archive counts: Nature 0/0; Science 0/0; PNAS 0/0; Nature Geoscience 0/0; Nature Astronomy 0/0; Nature Climate Change 0/0; JAS 0/0; ACP 75/19; JGR Atmospheres 11/5; Journal of Climate 15/12; Climate Dynamics 0/0; Climate of the Past 0/0; QJRMS 0/0; Astrobiology 0/0; GRL 16/5; JGR Planets 44/27; ApJ 0/0; ApJL 0/0; EPSL 2/0.
No real source failures; failure strings within unit-test fixtures were not production failures. No disabled journal reactivated, no broad historical backfill or retry loop.
The existing daily intake found no new recent selections, then its authorized one-year fallback selected 0 papers with 0 search errors. This means no qualifying additions were returned by the existing process, not proof of an exhaustive literature search.

## Actual changes and review coverage
Raw source record_count 3002 -> 3022 (+20), not 20 new public papers. Public catalog remains 231, with no new or removed top-level paper IDs and 31 linked duplicates.
In public paper content the diff contains 21 changed Crossref metadata updated timestamps, all on historical JGR Planets records. Publication dates, original first_seen, titles, abstracts and authors in these entries did not change. These timestamp refreshes are not new research versions or today's publication dates. No abstract supplementation or new manual paper admission.
No new automatic selections existed to read individually. This pass audited run/source status, intake and public-record diffs, not the original abstracts of all 20 newly archived raw records, all rejected candidates, the full 3022-record archive, or every publisher table of contents. It must not be represented as exhaustive paper-by-paper scientific screening.

## Verified online state
Live sources.html states November 15: 0 newly indexed papers, no reported enabled-source request failure, built at 15:55:52 Beijing. Monthly Crossref registrations were refreshed at 15:52:02; the current month remains explicitly incomplete and registration totals are not the same as relevant indexed papers.
Live catalog.json and network.json were read in the cloud browser, both generated_at 2026-11-15T07:55:52.257462+00:00. Catalog: 231 papers, 228 nonempty abstracts, 3 missing, new_count 0, 31 linked duplicates. The previous Great Red Spot correction remains present as topics ["planetary"].
Network: 124 parent institutions, 794 edges, 56 papers without a confirmed parent. No changes to institution assignments inferred. No shared recommendation vote or exhaustive UI/ORCID/department drilldown test performed today.

## Remaining limitations
Historical missing abstracts remain 10.1038/s41561-026-02094-y, 10.1038/s41561-026-02116-9 and 10.1177/15311074261485884. Prior affiliation precision issues, bibliography parser quarantine, withdrawal handling, formula/accessibility cleanup and 10.1029/2026JE009951 date issue remain unresolved. The absence of today's selected papers does not establish that no relevant paper exists outside the queried/covered records.
