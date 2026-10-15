# arXiv author metadata repair audit — 2026-10-15

## Coverage and result

- Screened all 268 arXiv source records and their cached person-level affiliation entries
- Recovered all 115 opaque RSS bylines from individual author links on official, version-specific arXiv abstract pages; 115/115 retrievals succeeded
- These 115 source-archive records intersect 22 of the 152 published catalog papers. Most of the 22 already had usable HTML display authors; this is not a claim that 22 published bylines were visibly broken
- Quarantined 40 demonstrably malformed archival author-affiliation blocks (391 raw extracted person entries), retaining the complete rejected source evidence in affiliations.json under rejected_author_affiliations
- Only three of those quarantined blocks are in the current published catalog: 2609.27622v1, 2609.28847v1, 2609.28001v1
- Sparse payload covers 134 source records: 115 recovered bylines plus 19 additional records with malformed cached mappings
- All first_seen values, DOI fields, title/abstract fields, publication data, paper-level institutions, and all other unrelated source fields remain unchanged

## Three confirmed visible defects

| Version | Verified byline size | Evidence |
|---|---:|---|
| 2609.27622v1 | 33 | https://arxiv.org/abs/2609.27622v1 |
| 2609.28847v1 | 5 | https://arxiv.org/abs/2609.28847v1 |
| 2609.28001v1 | 3 | https://arxiv.org/abs/2609.28001v1 |

The experimental HTML versions contain malformed author/affiliation markup. Their person-level mappings are unavailable rather than inferred. Author names come from individual official byline links. Paper-level institutions remain as independently supplied by the original affiliation blocks. No names, native-script identities, ORCIDs, or person–institution links were invented.

## Parser and regression protection

RSS dc:creator is now retained as authors_raw instead of treated as one person. Enrichment resolves individual authors using the versioned abstract page and caches both names and source URL. Same-version recovered names survive RSS refreshes. Offline enrichment can restore corrected names from cache.

Reconciliation only rejects demonstrable contamination: unverified numeric/TeX fragments in person fields, or multiple complete official author names collapsed into one field. Ordinary initials versus full names, accents, hyphens, comma-containing names, and explicit numeric collaboration names remain valid. A malformed converted page is quarantined as a unit because its author/institution grouping is unreliable; valid associations on other pages are preserved.

Nine added regressions include actual official byline HTML fixtures for the three confirmed cases, source/provenance retention, raw rejection evidence retention, valid name variants, and no institutional-link inference. All 81 Python tests in this workspace pass; git diff --check passes.

## Integration

Apply parser.patch; copy test_author_metadata.py and tests/fixtures/arxiv_author_bylines.json. Apply corrections.json sparsely: match both id and version_id, update only paper_fields and affiliation_fields on the latest source archive. Do not replace whole source files or stale generated catalogs. Preserve all other current data. Rebuild catalog/network afterward. Safe fallback author display may scaffold confirmed byline names with empty institutions and no ORCID.

The rejected original person entries are also available in quarantine.json for review; corrections.json itself retains them in the source cache. Individual byline and HTML source URLs are included in payload/report records.

## Quarantined source keys

- 2610.11637v1 (1 raw entries): https://arxiv.org/html/2610.11637v1
- 2610.11122v1 (4 raw entries): https://arxiv.org/html/2610.11122v1
- 2610.09933v1 (4 raw entries): https://arxiv.org/html/2610.09933v1
- 2610.09881v1 (12 raw entries): https://arxiv.org/html/2610.09881v1
- 2610.09715v1 (5 raw entries): https://arxiv.org/html/2610.09715v1
- 2610.09575v1 (6 raw entries): https://arxiv.org/html/2610.09575v1
- 2610.09543v1 (5 raw entries): https://arxiv.org/html/2610.09543v1
- 2610.09323v1 (1 raw entries): https://arxiv.org/html/2610.09323v1
- 2610.08128v1 (22 raw entries): https://arxiv.org/html/2610.08128v1
- 2610.07636v1 (1 raw entries): https://arxiv.org/html/2610.07636v1
- 2610.01835v1 (31 raw entries): https://arxiv.org/html/2610.01835v1
- 2610.01081v1 (4 raw entries): https://arxiv.org/html/2610.01081v1
- 2609.38468v1 (1 raw entries): https://arxiv.org/html/2609.38468v1
- 2609.38566v1 (20 raw entries): https://arxiv.org/html/2609.38566v1
- 2609.35676v2 (30 raw entries): https://arxiv.org/html/2609.35676v2
- 2609.39354v1 (3 raw entries): https://arxiv.org/html/2609.39354v1
- 2609.39391v1 (5 raw entries): https://arxiv.org/html/2609.39391v1
- 2609.36831v1 (2 raw entries): https://arxiv.org/html/2609.36831v1
- 2609.28847v1 (3 raw entries): https://arxiv.org/html/2609.28847v1
- 2609.29174v1 (5 raw entries): https://arxiv.org/html/2609.29174v1
- 2604.14009v2 (5 raw entries): https://arxiv.org/html/2604.14009v2
- 2609.28884v1 (1 raw entries): https://arxiv.org/html/2609.28884v1
- 2609.28981v1 (2 raw entries): https://arxiv.org/html/2609.28981v1
- 2609.29201v1 (2 raw entries): https://arxiv.org/html/2609.29201v1
- 2609.30116v1 (4 raw entries): https://arxiv.org/html/2609.30116v1
- 2607.15362v2 (2 raw entries): https://arxiv.org/html/2607.15362v2
- 2609.27622v1 (153 raw entries): https://arxiv.org/html/2609.27622v1
- 2609.28001v1 (22 raw entries): https://arxiv.org/html/2609.28001v1
- 2609.27062v1 (1 raw entries): https://arxiv.org/html/2609.27062v1
- 2609.27137v1 (2 raw entries): https://arxiv.org/html/2609.27137v1
- 2609.27292v1 (4 raw entries): https://arxiv.org/html/2609.27292v1
- 2609.27568v1 (3 raw entries): https://arxiv.org/html/2609.27568v1
- 2609.28173v1 (3 raw entries): https://arxiv.org/html/2609.28173v1
- 2605.19796v3 (1 raw entries): https://arxiv.org/html/2605.19796v3
- 2607.25385v2 (2 raw entries): https://arxiv.org/html/2607.25385v2
- 2609.01692v3 (1 raw entries): https://arxiv.org/html/2609.01692v3
- 2608.11440v3 (11 raw entries): https://arxiv.org/html/2608.11440v3
- 2606.28580v2 (3 raw entries): https://arxiv.org/html/2606.28580v2
- 2605.23166v3 (3 raw entries): https://arxiv.org/html/2605.23166v3
- 2512.18289v3 (1 raw entries): https://arxiv.org/html/2512.18289v3
