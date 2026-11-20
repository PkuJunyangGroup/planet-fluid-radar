# November 20 daily review (Asia/Shanghai)

Cloud-only, authorized PkuJunyangGroup public connection. Scheduled run [#156](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/44703007283) started 16:29 Beijing, passed 96 tests and deployed 16:42:41. Source status for all 24 enabled sources was successful: four arXiv categories (8/6/0/18 returned), 19 Crossref journals, and Exoplanet.eu (13 entries inspected, 2 retained by that ingest step). No failure-window recovery, duplicate full fetch, or one-year fallback. The automated catalog added seven from the regular recent-date/version intake (255 → 262). Zero results from a source do not imply no papers were published.

Read the complete original English arXiv abstracts and checked title, author and date/version metadata for all seven visible new candidates. Kept six; all first seen on November 20 Beijing:
- November 20 first submission: 2611.26548v1 and 2611.26372v1.
- November 19 first submission: 2611.25803v1.
- November 20 Beijing revisions of older records: 2609.05312v2 and 2510.00124v2.
- November 19 Beijing revision of an older record: 2603.03014v2.
- Excluded 2611.26025 with a record-specific scope override: radio technosignature propagation through a photoionized ionosphere rather than neutral-atmosphere climate, chemistry, circulation or retrieval. Preserved the source archive and first_seen.

No historical corrections or manual abstract backfills in this pass. Review coverage here is all seven automatically admitted new candidates, not a new full audit of raw rejected sources or historic affiliations. Source-provided abstracts remain in English, collapsed by default. No backend or layout changes.

Correction commit fb26cad triggered [#157](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/44722218717): 96 tests passed, catalog and network rebuilt, generated records saved at 92fdbc4, Pages deployment succeeded at 18:49:23 Beijing. Verified homepage, live catalog.json (261 entries, six today's additions, excluded ID absent, no intro fields, all reported sources OK) and network.json (261 paper entries, 129 parent institutions, 873 links). Network log reports 63 papers without confirmed parent institutions; no new affiliation claims made. The final catalog increased by six relative to November 19.
