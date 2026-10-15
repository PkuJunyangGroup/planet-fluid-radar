# Author-name and metadata audit — 2026-10-15

## Coverage

- Inventoried all 152 current public papers, 1093 identity keys and 1043 distinct byline strings. These keys are not a claim of unique people.
- Reverified all 19 previously displayed native-name identities against the publisher-deposited bilingual byline or the same explicitly linked ORCID.
- Verified 87 additional original-script names using primary institutional, author-owned or publisher sources and paper/affiliation identity crossmatches.
- Checked 16 previously uncached, paper-supplied public ORCIDs. None supplied a native name; missing names are not evidence of nationality or ethnicity.
- The resulting catalog has 107 distinct original-byline/native-name pairs, across 38 papers. Repeated aliases are not distinct people.

## Identity rules and evidence

The machine-readable [audit](2026-10-15-author-name-audit.json) separates the full structural census from targeted primary-source web checks and lists evidence, dates, exact paper scopes and unresolved cases. Not every inventoried author received an independent web identity check. Unconfirmed authors keep the source byline.

New overrides require a matching byline plus either a paper-supplied ORCID or a specific verified paper scope. Existing institution-qualified overrides remain supported. No ORCID was inferred by searching a person's name. Japanese Kanji is preserved rather than translated; Chinese simplified/traditional spelling follows the source. The legacy `name_zh` storage field is reused for these original-script Han names.

Examples of important disambiguation include Renyu Hu → 胡人予 and Takao M. Sato → 佐藤隆雄. An inconsistent conference spelling was not used for Sato. Names are never fabricated from pinyin or Romanization. The cloud maintenance instructions now explicitly permit identity-confirmed primary websites beyond ORCID and require provenance.

## Other verified repairs in this batch

Two previously missing abstracts were recovered: the published Mars abstract from Nature Geoscience (10.1038/s41561-026-02090-2), and the icy-moon abstract from NASA's public accepted-manuscript metadata (10.1038/s41550-026-02955-x). Source types are preserved. A research briefing, a publisher correction and one unretrieved research abstract remain explicitly missing; no substitute summary was generated.

The author metadata repair separately recovers structured arXiv bylines and withholds malformed experimental HTML person mappings. Rejected mappings remain in the source cache for audit, not in the public author network. Missing affiliation/ORCID values remain missing.

## Validation and release

Python identity-scope and parser regression tests are included. The catalog and network are rebuilt from current source archives. Publication is considered complete only after the GitHub Actions deployment succeeds and the live catalog/network and author display are checked; see the commit's workflow result for the final deployment status.

Rerun before publication (2026-10-15 12:19 UTC): all 87 Python tests passed; author-display, abstract-math, timeline and compact-list JavaScript checks passed. The pinned KaTeX 0.16.22 whole-catalog test checked all 152 rows: 149 supplied abstracts, 3 missing, 129 formula spans across 20 papers, 0 rendering failures. This is automated renderer verification, not visual browser QA.
