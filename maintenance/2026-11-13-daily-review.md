# Daily reading review — 2026-11-13 (Asia/Shanghai)

## Scope and execution
Cloud-only; designated PkuJunyangGroup GitHub connection and PkuJunyangGroup/planet-fluid-radar main only. Current cloud-maintenance.json applies. Latest topics, journals, README, workflow and preceding maintenance were consulted. No user computer, paid API, manual full-ingestion trigger, account/permission changes or recommendation votes were used.

Scheduled run [43389003640](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/43389003640) started 2026-11-13 07:53:34 UTC (15:53:34 Beijing), succeeded and published. Data commit ccf612eb3e0dce174f7377bfe1f6fd4888333b75. All 90 tests passed. Do not confuse test-fixture simulated errors with production ingestion failures.

## Actual source results
Four arXiv feeds succeeded: astro-ph.EP 11, physics.ao-ph 4, physics.geo-ph 1, physics.flu-dyn 19 feed entries (not a deduplicated count). Exoplanet.eu succeeded: 11 recent entries examined, 0 additions, 2 pages.
All 19 enabled journal requests succeeded. Retrieved/retained archive counts: Nature 33/0; Science 49/4; PNAS 5/0; Nature Geoscience 2/0; Nature Astronomy 1/0; Nature Climate Change 0/0; JAS 0/0; ACP 5/4; JGR Atmospheres 2/1; Journal of Climate 0/0; Climate Dynamics 0/0; Climate of the Past 2/2; QJRMS 0/0; Astrobiology 0/0; GRL 11/6; JGR Planets 25/11; ApJ 25/1; ApJL 4/1; EPSL 1/0.
Zero queried records are not evidence of zero publisher publications. Source-state, ISSN/window and live status were checked; not every publisher's current table of contents was independently audited. No failed-source recovery or broad historical backfill was needed. Disabled sources remain disabled.
Source-backed record_count increased 2935 to 2980 (+45); this is not the count of newly published or publicly admitted papers.

## Reading review coverage and decisions
The nine automatic intake selections were read individually using their source-backed complete original abstracts and official arXiv pages. This is an abstract-level scientific scope review, not full-manuscript peer review. WASP-4's official abstract is explicitly marked abridged by its authors. The unversioned Epsilon Indi page supplied a stale v1 in web retrieval, so v2 was read explicitly.
This review does not claim an exhaustive paper-by-paper audit of all rejected raw archive entries, all 2980 source records, all older public papers, or all publisher tables of contents.

Retain:
- [2611.17300v1](https://arxiv.org/abs/2611.17300v1): JWST Rocky Worlds DDT Observations of LTT 1445 A b and c in Secondary Eclipse Using MIRI/F1500W. Direct rocky-exoplanet atmospheric constraints. arXiv submitted 2026-11-12 18:55:27 UTC = 2026-11-13 02:55:27 Beijing; not a confirmed journal publication.
- [2611.16949v1](https://arxiv.org/abs/2611.16949v1): Stellar-Field-Driven Induction Heating Unlikely To Cause Significant Heating in Giant Exoplanets. Direct giant-planet heating. arXiv 2026-11-12 15:26:28 UTC = 23:26:28 Beijing; comments say accepted MNRAS, which is not a verified journal publication date.
- [2611.16782v1](https://arxiv.org/abs/2611.16782v1): Combining TTVs, RVs, and astrometry to characterize distant giant companions of transiting hot Jupiters: Application to WASP-4. Planetary orbital characterization. arXiv 2026-11-12 13:27:03 UTC = 21:27:03 Beijing.
- [2611.16760v1](https://arxiv.org/abs/2611.16760v1): Global climate modeling of the Martian water cycle. I) Improved parameterizations of physical processes. Direct Mars climate/water-cycle modeling. arXiv 2026-11-12 13:09:31 UTC = 21:09:31 Beijing.
- [2609.25784v2](https://arxiv.org/abs/2609.25784v2): Molecular mapping of an exoplanet with JWST: detection of NH$_3$ and HCN in the temperate super-Jupiter Epsilon Indi Ab. Direct planetary chemistry/spectral characterization. First arXiv submission 2026-09-22; v2 2026-11-12 15:45:21 UTC = 23:45:21 Beijing. Newly indexed current revision, not a new independent paper or one-year fallback.

These five retained records have unchanged first_seen 2026-11-13T07:53:45.188625+00:00 (15:53:45 Beijing).

Historical/journal-version progress:
- [2610.18368v1](https://arxiv.org/abs/2610.18368v1), On the Orbital Evolution of Giant Planet Pair Embedded in a Gaseous Disk. III. simultaneous gas accretion and the final mass ratio, Bixuan Zhao, Hui Zhang, Yinhao Wu, Ya-Ping Li. Direct planetary migration/accretion and final mass ratios. Original arXiv 2026-10-13; original archive first_seen 2026-10-15T01:38:21.320708+00:00 preserved.
- Its new ApJ variant [10.3847/1538-4357/aeb2df](https://doi.org/10.3847/1538-4357/aeb2df) has publisher-deposited date 2026-11-12 and first_seen 2026-11-13T07:54:21.348820+00:00. Existing merge evidence is exact normalized title + authors, corroborated by the same four explicit author ORCIDs. The public item retains both variants and earlier first_seen. Direct DOI/Crossref web opens were unavailable in this review, so the journal date relies on the successfully fetched publisher-deposited source record, not a newly read publisher landing page. Do not report this as a sixth first-ever site-indexed paper today.

Exclude through three scoped topics.json overrides (source archive/first_seen untouched):
- [2611.16783v1](https://arxiv.org/abs/2611.16783v1), The Same But Different: SiO2 Clouds in Two L-Dwarfs with JWST: isolated field brown dwarfs, not specific planetary targets.
- [2611.16715v1](https://arxiv.org/abs/2611.16715v1), Resolving Radiogenic Heterogeneity in the Earth's Mantle with Multi-Site Geo-neutrino Measurements: terrestrial geophysics.
- [2611.16548v1](https://arxiv.org/abs/2611.16548v1), Euclid Data Release 1 (DR1): Spacecraft performance in the L2 environment: spacecraft engineering/space environment, not a planetary result.

No recent-paper shortage: no one-year fallback. No abstracts invented, shortened, translated or newly added. No new guessed author/ORCID/institution mappings.

## Correction and deployment
Review commit 622509dc3ce6bcad7f78935871f7816b120ea4bf updates only topics.json. Existing push workflow [43391108612](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/43391108612) skips arXiv, journal ingestion and daily intake; uses offline enrichment/dates and rebuilds catalog/network. Its configured incremental Exoplanet.eu step is retained, not a full duplicate scrape.

## Remaining limits
Three historical abstracts remain unavailable: 10.1038/s41561-026-02094-y; 10.1038/s41561-026-02116-9; 10.1177/15311074261485884. No fabricated replacements.
The previously pending 10.1029/2026JE009951 date/selection issue, bibliography parser quarantine, automatic withdrawal handling and formula/accessibility cleanup were not resolved in this pass. Existing raw source/identity mappings were preserved; no exhaustive identity/ORCID audit claimed. The giant-pair merged record retains parallel source author-affiliation variants; no speculative deduplication of identities was attempted.

## Verified final state
Correction run 43391108612 completed successfully; all 90 tests passed again. The actual incremental Exoplanet.eu step found 0 recent entries and 0 additions in 1 page. Generated-data commit b1df16b8d84a7884645e91319a423567a65baca3. No global matcher/parser/UI code was changed.
Live catalog.json and network.json were read after deployment: matching generated_at 2026-11-13T08:12:14.348506+00:00 (16:12:14 Beijing), 229 public papers, 31 linked duplicates, 226 original abstracts and 3 missing. Daily brief reports exactly 5 newly indexed recent papers, no source issues, no older fallback. All three newly excluded IDs are absent; no intro_* fields exist. Public catalog is +6 compared with yesterday's 223: five first-seen-today papers plus the historical giant-pair record admitted through its recent journal variant.
Live network has 124 parent institutions, 794 links, 229 papers, 55 without a confirmed parent; missing affiliation is not a failed literature fetch. The network page defaults to an overview of up to 30 institutions.
Live homepage shows Papers 229, compact English metadata and collapsed abstracts. The first paper's complete source abstract was expanded and recollapsed successfully, with Published/Added/Version dates visible. Recommendation controls and 0-count states are present; no shared vote was created, so this is not a write-path backend test. Source page shows 5 newly indexed papers and successful current source statuses. More tags, date heatmap, current-month-incomplete statistics, separate Crossref/index measures, and feedback links remain present. Monthly registration statistics retain their prior successful cache (November 12); this was not represented as newly fetched today. No exhaustive author/department drilldown or every ORCID-link click test was performed.
