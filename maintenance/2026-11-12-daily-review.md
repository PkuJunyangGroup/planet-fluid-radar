# Daily review — November 12, 2026 (Beijing)

## Scope, identity, and synchronization
Cloud-only review using the designated PkuJunyangGroup GitHub connection. Authenticated login PkuJunyangGroup and repository admin permission verified. Read current cloud-maintenance.json, README, topics.json, journals.json, daily workflow and November 11 maintenance record. Four arXiv categories and 19 enabled journals remain unchanged. No local-user computer, credentials, backend, or database was used or modified.

The delayed [scheduled run 43181773260](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/43181773260) started November 12 at 16:17:50 Beijing and completed successfully at 16:30:28. Data commit: e6bd642a2866963ff3ab1aa36dfdc106437ceac7. Main was rechecked before writing this record; no newer commit or existing November 12 review was present. No duplicate full retrieval or manual dispatch was performed.

## Source coverage and actual intake
All four arXiv categories, all 19 enabled journal sources, and Exoplanet.eu reported success. arXiv returned zero records for the existing incremental window. This does not establish that arXiv published no papers outside that window. Exoplanet checked three pages, found 22 recent entries, and added one source record. Journal requests retrieved 591 records in aggregate including overlap and existing records; these are not new-paper counts.

The final public directory remains 223 papers, with 220 nonempty abstracts. Daily intake explicitly ran one_year_fallback with zero selected and zero search errors. Today's public first-seen entries: zero; recent new entries: zero; one-year supplements: zero; existing-paper scientific revisions: zero.

Raw source archive count rose from 2856 to 2935 (+79): 78 first-seen journal records and one Exoplanet record. The archive includes old works reached by publisher metadata updates; they were not automatically admitted to the public directory. No retrospective fetch was manually initiated.

## Original-abstract reading coverage
The large journal archive could not be read through the connector (empty file response). A cloud-browser raw-file navigation initially timed out but its rendered document subsequently loaded successfully. All 78 newly archived journal records were inspected at title/date/status/score level.

For the 17 newly archived records with publication date between November 1 and November 12 inclusive, including one month-only record, 16 complete source-supplied English abstract strings were read. One Nature record has no abstract available in the archive. This is NOT a complete abstract audit of all 78 records, nor an independent publisher-page verification of all those abstracts.

The 15 day-dated abstracts read concern microbial observables, terrestrial cold-pool parameterization, urban aerosol formation, biogenic SOA, volcanic-cloud emulation, the North Pacific storm track, Antarctic meltwater, tropical-Pacific clouds/SST, Pantanal wetlands, Indian Ocean circulation, Arctic mixing, Antarctic ice-shelf flow, Magellanic gas, chondrite disk chemistry, and embedded protostellar disk structure. None established a new admission within the configured planetary scope. In particular, generic RCE/LES methodology and protoplanetary dust/disk studies alone do not qualify.

Full abstract read but date qualification unresolved:
- [Low Energy Electron Impact Emission Cross Sections of the N2 LBH Band System With Importance to UV Planetary Remote Sensing](https://doi.org/10.1029/2026JE009951). The abstract explicitly concerns Titan and Earth N2 dayglow, measured low-energy excitation cross sections, and a radiative-transfer dayglow model. It has a genuine planetary-atmosphere connection and should not be described as scientifically irrelevant. The archive supplies only 2026-11 (month precision), with automatic score 40. It cannot presently be assigned to the two-day intake window, and it does not meet the existing >=65 fallback threshold. No precise date, score, or admission was invented. Direct DOI lookup was inaccessible and bounded exact-title/DOI search did not resolve publication-day evidence. Retain this as a pending date/scope candidate for a later bounded check, not a newly published or admitted article.

Abstract not obtained:
- [Hadean mantle depletion and 3.95-Gyr subduction implied by North China rocks](https://doi.org/10.1038/s41586-026-11280-2), date November 11. Its archive abstract is empty; the publisher lookup redirected to an inaccessible identity endpoint. No abstract-reading claim is made. It remains excluded by the existing rules.

The other 61 newly archived records (predominantly July 2026 terrestrial GRL papers and February 2018 JGR: Planets papers, plus a December-dated regional-climate item) were not individually abstract-audited. This does not prove absence of all rule-screening omissions. No 2018 record qualifies for the one-year supplement window. No previously excluded item was silently published.

## Historical metadata changes
The Exoplanet source record exoplanet-bib:33410 was linked by exact DOI to the already public [Receiving Exoplanet Messages with Gravitational-wave Carriers: The Gravitational-wave Radial Velocity Method](https://doi.org/10.3847/1538-4357/aea216), Casey McGrath, ApJ. Its original November 11 first_seen is preserved; the new November 12 source provenance is not a new paper or scientific revision. The live original abstract was reread and the merged record inspected.

The complete catalog diff shows this provenance linkage as the only public paper-object change; the remaining changes are generation/source/intake/monthly-statistics metadata. network.json changes only its generation timestamp. Monthly Crossref registration caches were refreshed through November 12; registration counts are not new public admissions. No historical missing abstract was supplied and no author/institution identity was manually guessed.

## Tests, deployment and live validation
All 90 Python tests passed in the scheduled job. Actual source ingestion, one-year fallback, catalog/network build, commit and Pages deploy succeeded. Test-fixture failures printed during unit tests must not be mistaken for actual ingestion failures. No additional local test run is claimed.

Independent cloud-browser DOM checks verified:
- [Live catalog](https://pkujunyanggroup.github.io/planet-fluid-radar/catalog.json): generated_at 2026-11-12T08:30:09.359680+00:00, daily brief date November 12, zero new/older/updated IDs and no source issues, 223 papers / 220 nonempty abstracts.
- [Live network](https://pkujunyanggroup.github.io/planet-fluid-radar/network.json): same generation timestamp, 124 parent institutions, 783 edges, 1590 researchers, 223 paper records, 53 omitted/unconfirmed-parent paper records.
- [Homepage](https://pkujunyanggroup.github.io/planet-fluid-radar/): rendered 223-paper topic/count/list controls, last successful fetch November 12 16:18:33 Beijing, English title/author/journal listing and the linked GW paper. No recommendation state was changed. This round did not repeat a full expand/collapse or every-filter UI regression.

## Remaining limits
Three previously missing public abstracts remain; 53 paper records lack confirmed parent institutions. The Titan/N2 paper's exact publication day and archive scope classification need follow-up. Full historical/new-archive abstract audit remains incomplete. Existing Exoplanet parsing, withdrawn-preprint handling, formula-rendering, and older identity/affiliation limitations were not repaired in this round. No claim of exhaustive source coverage or complete manual review is made.

This review-only commit uses [skip ci]; it changes no site data and intentionally starts no extra retrieval or deployment.
