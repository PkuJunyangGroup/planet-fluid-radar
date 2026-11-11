# Daily maintenance review — 2026-11-11 (Asia/Shanghai)

## Outcome
Three new site entries passed original-abstract review, all published November 10 and first indexed November 11. No accepted entry was first published or revised on November 11 Beijing. One existing arXiv record advanced to v2, dated November 10, and is reported separately. One-year supplements: zero.

Final public catalog: 223 papers, 220 supplied abstracts, three missing abstracts, 29 linked duplicate variants and 2856 raw records. Publication and live verification completed successfully.

## Execution and source coverage
Used only the designated PkuJunyangGroup cloud GitHub connection and dot cloud/web reading. Verified identity, repository permission, current configuration, topics, journals, README, workflow and recent maintenance. No user computer, alternative account, manual workflow dispatch, credentials, Worker/D1 changes or checkpoint reset.

The 10:00 Beijing check found no November 11 run. The scheduled run [42981593624](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42981593624) subsequently started at 15:43:38 and completed successfully at 15:56:18 Beijing. Its generated data commit was e0735d140d9645cd649ae683fc21bad80a3930b0. No duplicate full retrieval was triggered.

All four arXiv categories succeeded: astro-ph.EP 8, physics.ao-ph 4, physics.geo-ph 3 and physics.flu-dyn 19 category hits. These 34 hits include cross-listed records. The arXiv archive grew to 693 records, including 29 first_seen today. Exoplanet.eu's scheduled incremental scan succeeded: two pages, eight recent entries and zero retained additions.

All 19 enabled journal sources succeeded. Their 318 retrieved records and 79 retained source records are not counts of public admissions or unique newly published papers.

| Enabled journal | Retrieved | Retained |
|---|---:|---:|
| Nature | 31 | 0 |
| Science | 0 | 0 |
| PNAS | 18 | 0 |
| Nature Geoscience | 1 | 0 |
| Nature Astronomy | 1 | 0 |
| Nature Climate Change | 4 | 0 |
| Journal of the Atmospheric Sciences | 3 | 3 |
| Atmospheric Chemistry and Physics | 15 | 6 |
| Journal of Geophysical Research: Atmospheres | 6 | 3 |
| Journal of Climate | 4 | 4 |
| Climate Dynamics | 40 | 11 |
| Climate of the Past | 1 | 1 |
| Quarterly Journal of the Royal Meteorological Society | 2 | 1 |
| Astrobiology | 0 | 0 |
| Geophysical Research Letters | 77 | 23 |
| Journal of Geophysical Research: Planets | 40 | 14 |
| The Astrophysical Journal | 21 | 4 |
| The Astrophysical Journal Letters | 7 | 1 |
| Earth and Planetary Science Letters | 47 | 8 |

The four disabled ocean journals stayed disabled. Production source failures: zero. Existing monthly registration statistics for all 19 enabled journals are successful cached values checked November 10; November coverage runs through November 10, not November 11. Current-month totals remain incomplete and Crossref registrations are not complete publisher research-paper counts.

### Zero-record source checks
Read-only Crossref publication-window queries independently returned zero Science and zero Astrobiology records dated November 10–11. These zeros describe the window, not empty journals.

- Science's latest inspected deposited publication was November 8, DOI [10.1126/science.aeh5267](https://doi.org/10.1126/science.aeh5267), outside the recent window. Its official current TOC returned HTTP 403; not retried.
- Astrobiology's latest deposited publication was November 5, DOI [10.1177/15311074261505107](https://doi.org/10.1177/15311074261505107), also outside the window. The [official November issue](https://journals.sagepub.com/toc/asb/current) contains papers first published August 31–September 15. The retrieved [OnlineFirst page](https://journals.sagepub.com/toc/ASB/0/0) was cached and stopped at November 2, so it cannot alone establish completeness.
- Window evidence: [Science Crossref](https://api.crossref.org/journals/0036-8075/works?filter=from-pub-date%3A2026-11-10%2Cuntil-pub-date%3A2026-11-11&rows=100) and [Astrobiology Crossref](https://api.crossref.org/journals/1531-1074/works?filter=from-pub-date%3A2026-11-10%2Cuntil-pub-date%3A2026-11-11&rows=100). No backfill or checkpoint change was made.

## Reading review and narrow corrections
Read the complete source-supplied abstracts of all 29 newly archived arXiv records. Independently checked official arXiv abstracts and version histories for the selected arXiv entries, the recovered ExoPlanetLab record, the outer-Solar-System catalogue boundary case and the existing mass-ratio-desert revision. Read the complete publisher-deposited original abstract and bibliographic metadata for the selected ApJ paper through Crossref. The full incoming journal archive could not be retrieved because of a connector transport error; the selected journal record and feed status were reviewed, not every incoming journal abstract.

The automatic selection contained four records. Applied three paper-specific overrides:
1. Excluded [2611.14441v1](https://arxiv.org/abs/2611.14441v1), “Nucleation of water ice under weak ionization via clustering on negative ions,” by André Nicolov, Efstratios M. Kritikos, William A. Goddard III. and Paul M. Bellan. First submission November 10 18:11:44 UTC (November 11 Beijing). Its laboratory plasma microphysics concerns Earth's mesosphere and protoplanetary disks, with no direct nonterrestrial planetary atmosphere/climate, surface or interior result.
2. Excluded [2609.09063v2](https://arxiv.org/abs/2609.09063v2), “The size and mass distribution of cold classical TNOs for 5<H<13,” by Gary M. Bernstein, Wesley C. Fraser, Marielle R. Eduardo, William M. Grundy, Bryan Hilbert, Matthew J. Holman, Anastasia N. Morgan, Kevin J. Napier, John A. Stansberry and David E. Trilling. v1 September 8 17:17:45 UTC; v2 November 10 18:14:45 UTC (November 11 Beijing), accepted to PSJ. This is planetesimal-remnant population/formation work, rather than the radar's direct planetary-system orbital or planetary-fluid questions.
3. Admitted only the existing archive record 2611.13770, ExoPlanetLab, as a recent paper missed by keywords. Its quantitative planetary injection/recovery validation supports the explicit exoplanet-characterization scope. The automatic score remains 0 and topic list empty; the >=65 threshold applies only to annual fallback. No global keywords or scope rules were broadened.

Both removed entries retain their source records and original first_seen 2026-11-11T07:43:49.541050+00:00. Source-ID, normalized-title and DOI checks found no catalog duplicate for ExoPlanetLab.

[2611.14330v1](https://arxiv.org/abs/2611.14330), “An Archival Search for Outer Solar System Objects in the NOIRLab Source Catalog DR2: 65 Candidates, Including Four L4 Neptune Trojans,” by Gioele Cerati, remained unmatched and was not admitted. Its November 10 16:55:06 UTC submission primarily catalogues small bodies and classifies their orbits; the abstract explicitly reports little Planet Nine constraint. This boundary decision does not broaden the radar into general small-body discovery.

Data-only preflight confirmed all unrelated topic configuration and intake policy fields unchanged. Intake commit: 35e6fd93858d9e41db97a6f46c606984d11e521b [skip ci]. Scope commit: 172562db7c8f0706228464011f325f76538540a6. No parser, classification, frontend or backend code changed.

## Final new entries

### Breaking the Chain: The Dynamical History of the Barnard's Star Planetary System
- Authors: Tian Yi; Qiran Huang; Shuo Huang; Chris W. Ormel.
- Source: arXiv 2611.13771v1; only version listed. No DOI or journal reference listed. Comments say resubmitted to Research in Astronomy and Astrophysics after minor revision; this is not treated as a published journal article.
- First publication/version: 2026-11-10 09:10:41 UTC, or November 10 17:10:41 Beijing.
- Site first_seen: 2026-11-11T07:43:49.541050+00:00, or November 11 15:43:49 Beijing.
- Original: https://arxiv.org/abs/2611.13771 ; manuscript: https://arxiv.org/html/2611.13771v1 .
- Scope: direct planetary orbital architecture, resonance breaking and merger pathways. The disk-driven scenario concerns the observed planetary architecture, rather than disk formation alone.

### ExoPlanetLab: Bayesian orbit fitting of Gaia-DR4 epoch astrometry, radial velocities and relative astrometry
- Author: David Hobbs (manuscript byline D. Hobbs).
- Source: arXiv 2611.13770v1; only version listed. No DOI or journal reference listed.
- First publication/version: 2026-11-10 09:09:59 UTC, or November 10 17:09:59 Beijing.
- Site first_seen: 2026-11-11T07:43:49.541050+00:00, or November 11 15:43:49 Beijing.
- Original: https://arxiv.org/abs/2611.13770 ; manuscript: https://arxiv.org/html/2611.13770v1 .
- Scope: validated exoplanet orbit inference. The original reports 180 injection tests, no false detection in 30 null tests and below-nominal period-interval coverage. Real-data examples include Gaia BH3 and HD 114762; do not describe this as a new planet discovery. Relative astrometry was validated on simulations only.
- Manuscript explicitly supplies Lund Observatory/Department of Physics/Lund University affiliation. That source affiliation is preserved, but no new parent-institution registry mapping or author ORCID was invented.

### Receiving Exoplanet Messages with Gravitational-wave Carriers: The Gravitational-wave Radial Velocity Method
- Author: Casey McGrath.
- Source: The Astrophysical Journal 1012(1), article 17; DOI 10.3847/1538-4357/aea216.
- Publisher-deposited online publication: 2026-11-10. Print date: 2026-11-20. No publication time is supplied, so none is inferred.
- Site first_seen: 2026-11-11T07:44:25.254193+00:00, or November 11 15:44:25 Beijing.
- Original link: https://doi.org/10.3847/1538-4357/aea216 ; metadata/original-abstract evidence: https://api.crossref.org/works/10.3847/1538-4357/aea216 .
- Scope: quantitative exoplanet detection via GW phase modulation, with analytic sensitivity and power-loss calculations, not merely generic GW motivation.
- Crossref explicitly links supplement DOI 10.5281/zenodo.22129575, not an arXiv preprint. No matching preprint identifier was confirmed; no speculative version merge was created. This is distinct from companion DOI 10.3847/1538-4357/aea07d.
- Source-supplied ORCID https://orcid.org/0000-0002-6155-3501 passed format/checksum validation. Explicit source affiliations: University of Maryland, Baltimore County; Center for Research and Exploration in Space Science and Technology II; NASA Goddard Space Flight Center.

## Existing revision and historical progress
[The Brown Dwarf Desert is a Mass-Ratio Desert: Astrometric Demographics of 63,254 Stars](https://arxiv.org/abs/2611.12881v2) advanced v1 to v2. First submission November 9 18:59:28 UTC (November 10 Beijing); v2 November 10 15:18:22 UTC (November 10 23:18:22 Beijing). Original abstract unchanged. The source author list corrects Emma Turtleboom to Emma Turtelboom. Original first_seen remains 2026-11-10T08:23:33.861725+00:00. This is one existing-paper revision, not a fourth new site entry.

The scheduled job added one ORCID-name cache record with no verified Chinese name. No new Chinese author names or manually inferred institution relationships were created. Historical abstract supplements: zero. The three existing missing public abstracts remain unresolved.

## Tests, deployment and live verification
Both scheduled and correction runs passed all 90 Python unit tests. The correction [push run 42987488200](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42987488200) passed in 0.506 seconds for the test step, then ran offline enrich.py/dates.py and built catalog/network. arXiv ingestion, journal ingestion and daily_intake were skipped. The workflow's existing incremental Exoplanet.eu step ran once: two pages, seven recent entries, zero additions, success. No full source retrieval was repeated.

Corrected generated-data commit: d92775a38ed089d5c9d98f52d35c0ceaa524400c. Pages reported success at 16:31:34 Beijing; run completed 16:31:37. Full before/after catalog comparison confirms exactly two public IDs removed and one added, with all other 222 surviving paper objects unchanged from the scheduled output. Added-item abstract, authors, DOI, source dates, version, institutions, author-affiliation evidence and first_seen exactly match the existing source archive. No public intro_* fields.

Independent cloud-browser checks confirmed [live catalog](https://pkujunyanggroup.github.io/planet-fluid-radar/catalog.json) and [live network](https://pkujunyanggroup.github.io/planet-fluid-radar/network.json) share generation time 2026-11-11T08:31:23.573046+00:00. Live catalog contains the intended three-entry brief and 223 papers. Network has 124 parent institutions, 783 edges, 1590 researchers, 223 paper records and 53 without a confirmed parent; no self-edges or repeated institution IDs within a paper. Network initially served the prior cached version; a subsequent reload verified the current one.

[Homepage](https://pkujunyanggroup.github.io/planet-fluid-radar/) compact English listing, default collapsed abstracts, ExoPlanetLab search, full original abstract expansion/re-collapse, and separate publication/added/version dates were checked. Recommendation state was inspected without changing shared stars. No new local or JavaScript test execution is claimed.

## Remaining limits
- Three historical missing abstracts; 53 paper records without confirmed parent institutions. ExoPlanetLab's Lund affiliation still lacks a verified registry mapping.
- The Barnard paper's source affiliation strings contain formatting/contact debris and no explicit parsed author-to-institution map. No relationships were guessed.
- Full incoming journal-archive abstract audit is incomplete. The selected ApJ original was obtained from publisher-deposited Crossref metadata; prior IOP access restrictions were respected.
- Existing mathematical-text normalization/rendering limitations remain, including the GW abstract's stripped superscript formatting. Original source links remain available; no untested parser fix was made.
- Existing Exoplanet parser/withdrawal and older metadata issues are unchanged. Monthly registration caches are through November 10.
- A runtime warning notes older Actions target Node 20 while the runner uses Node 24; the workflow succeeded. No unrelated workflow upgrade was made.

This maintenance record uses [skip ci] and does not change site data or start another retrieval/deployment.
