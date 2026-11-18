# November 18 review and November 17 recovery (Asia/Shanghai)

## Scheduled run

Run [44267479431](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/44267479431) started 16:29 and deployed successfully at 16:43:57. All 95 tests passed. The 60-minute configuration ran successfully, but this run took approximately 14 minutes, so it does not prove behavior beyond the former 30-minute limit. JAS recovered: 7 retrieved / 6 retained. All four arXiv categories, 19 enabled journals and Exoplanet returned successfully. No duplicate fetch was triggered by this review. Data commit: 32da7b94cfe322151718aab99d822ddcfb886d6b.

arXiv counts by category: 32 / 13 / 5 / 30 (overlap possible). Exoplanet: 24 recent entries, 2 relevant additions from 3 pages. Persistent archive deltas since the last successful data state: arXiv +72, journals +66, Exoplanet +1. These are not public addition counts. The automatic intake selected 11 entries: 10 first seen today and one historical record's newer variant. No one-year fallback search was needed.

## Failed-run recovery and review

November 17's four transient candidates were not persisted and their exact identities cannot be reconstructed reliably. Today's incremental checkpoints cover the missing interval; no first_seen was backdated. All recovered new records retain November 18 16:30 first_seen.

Read all 11 automatic entrants' full source-provided English abstracts. Excluded 2611.22571, 2611.21884 and 2611.21786 as primarily protoplanetary-disc / stellar-accretion studies under the existing narrow scope. Source archives remain intact.

Read full abstracts and approved eight missed relevant source entries (seven additional public records; the atmosphere-interior paper merges into existing 2610.05287) with record-scoped decisions, without changing scores or global matching rules:
- 2611.21841: Jovian polar cyclone 3-D thermal/composition structure.
- 2611.21575: impact ripples across planetary conditions.
- 2611.21758: NEMESIS exoplanet candidate survey.
- 2611.21583: bulk exoplanetary debris composition.
- 2611.20785: Ariel candidate validation, November 16 submission; failed-window recovery.
- 10.1073/pnas.2615294123: Mars atmospheric CO2 isotopes, November 16 publication; failed-window recovery.
- 10.3847/1538-4357/aeb008: atmosphere-interior mixing flux, November 16 publication; failed-window recovery.
- 10.1029/2025je009300: lunar water/ice science mission, November 16 publication; failed-window recovery. The abstract explicitly says spacecraft recovery failed; this is not a report of completed orbital measurements.

The four November 16 recoveries are not one-year fallback admissions. Corrected the missing cached version date for 2606.30644v3 using the official arXiv version history: November 17 11:46:40 UTC. This is a recent revision, not an old-paper fallback. Earliest first_seen for merged historical 2610.22338 remains October 17.

## Coverage and limits

Compared all new arXiv titles/dates and read relevant missed candidates plus key exclusions. Read all 34 new journal records with November 16-17 dates (4 relevant, 30 out of scope), plus four historical Nature Astronomy abstracts. Did not claim full abstract review of all 139 new raw records or the historical archive. Publisher dates are deposited Crossref metadata, not independently checked publisher pages.

Boundary items 2611.22454 (general triple-system inclination method), 2607.10403 (muon detector / particle-transport concept) and 2611.17649 (asteroid kinetic-impact recoil) were read but not admitted in this narrow planetary-atmosphere/interior review. They remain archived, not falsely marked as metadata failures. HAT-P-70b record exoplanet-bib:33449 was checked against official arXiv 2611.18835: full original abstract is relevant, but first submission is November 14 Beijing, outside this failed November 16-17 window. It is not admitted as today's new paper or a fallback while recent relevant papers exist.

Historical abstract recovery: source archive 10.1038/s41550-026-02955-x now contains the full publisher abstract (icy-moon ocean longevity); original September 25 first_seen and August 20 publication are unchanged. This is archive enrichment, not a newly published or newly admitted paper.

## Verification

Local 95 tests passed; offline enrichment/dates and catalog/network rebuild completed. Final local catalog has 247 records: 15 more public records than November 16, consisting of 14 first-seen-today papers and one historical record's new variant. No previous public records were removed. Three historical abstracts remain missing. Network: 127 parent institutions, 857 links, 57 papers without confirmed parent. The atmosphere-interior journal version merges into an existing public paper and is historical metadata enrichment, not a new paper. Correction commit f6aca2bfcfe4b67ea6cbb30f6466854a2358172b deployed successfully via run 44283679113 at 18:17:54 Beijing; CI again passed 95 tests. Live catalog/network independently downloaded and both show 247 records. Browser QA confirmed the 247-count homepage, recovered Jovian polar-cyclone paper search, abstract collapsed by default and complete expansion with Published 2026-11-17 / Added 2026-11-18. Recommendation control loaded without casting a vote. The polar-cyclone paper currently appears under All topics but not Planetary atmospheres, documenting the remaining topic-filter classification limitation. No code or backend changes. Existing missing historical abstracts, incomplete affiliations, formula rendering, and some manually admitted items' topic-filter classification remain limitations. Original full English abstracts remain unchanged and collapsed by default. No recommendation votes cast; no backend changes.
