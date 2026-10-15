# Full abstract rendering audit — 2026-10-15

Cloud-only review of catalog snapshot at main `18d9254` (152 papers). This is a rendering/data-preservation audit, not independent scientific verification of all papers or a claim to have recovered missing source abstracts.

- 152/152 cards generated and checked for complete abstract insertion, default-closed details, escaped input and no source-data mutation
- 147 supplied abstracts: 20 with math, 127 without math; 5 missing, with explicit missing status retained
- Before this fix: 117 attempted TeX spans, 2 unsupported `\\upmu` failures in arXiv 2610.19081, and 12 raw `\\ce{...}` chemistry commands across 2610.19081 and 2610.05287
- After this fix: 129/129 supported spans rendered through real KaTeX 0.16.22, zero rendering failures
- Explicit small allowlist handles simple undelimited molecular formulas, italic prose, escaped percent and thin-space commands; source strings are unchanged. Complex/unknown chemistry and unknown TeX safely remain source text rather than being guessed
- Monetary text, unmatched delimiters, unknown commands, script/HTML injection, unsafe links and CSS commands tested; trust remains false and expansion/size bounded
- All 152 compact cards remain closed by default and include the entire rendered abstract. Existing bilingual author rendering passed on 10 papers; author identity research is a separate audit
- Long-formula rendering and horizontal-scroll/width CSS guards tested programmatically. Cloud Chromium was unavailable due runtime sandbox/socket/crashpad initialization failures in the preceding check. No claim of visual desktop/mobile browser QA; no user computer used
- 72 Python unit tests and all 5 Node test files passed, including the new `test_abstract_catalog.mjs`

Missing abstracts at this snapshot (independent public-source lookup pending):
- https://doi.org/10.1038/s41561-026-02094-y
- https://doi.org/10.1038/s41561-026-02090-2
- https://doi.org/10.1038/s41561-026-02116-9 (publisher correction)
- https://doi.org/10.1177/15311074261485884
- https://doi.org/10.1038/s41550-026-02955-x

Reproduce: `KATEX_JS=/path/to/katex-0.16.22/dist/katex.min.js node test_abstract_catalog.mjs`.
