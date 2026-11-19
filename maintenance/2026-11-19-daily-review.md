# November 19 daily review (Asia/Shanghai)

Cloud-only, authorized PkuJunyangGroup public connection. Prior visible briefing was November 18. No duplicate full fetch or workflow dispatch.

Scheduled run 44490289778 started 16:45 Beijing, passed 95 tests and deployed at 16:58:48. All 24 enabled sources succeeded: four arXiv categories (10/4/1/20 returned), 19 journals, Exoplanet.eu (10 recent entries, 0 relevant additions, 2 pages). Source archives grew by 30 arXiv and 20 journal records; Exoplanet archive unchanged. Zero retrieved is not proof of no publisher output. Logs contain intentional failure fixtures during tests, not live source failures.

Automatic catalog: 253, +6 since November 18. Read all six entrants' complete original English abstracts and kept them. Reviewed all 30 new arXiv titles/dates and 10 related/boundary abstracts; all 20 new journal abstracts and five changed historical journal abstracts. No relevant new journal admission. No one-year fallback used.

Two record-scoped missed candidates approved after full-abstract review, retaining real first_seen and scores:
- 2611.24812: A Homogeneous Benchmark of Exoplanet Mass-Radius Relations, first submitted November 19 Beijing; exoplanet composition/interior inference.
- 2610.13200v2: Detailed study of HD 219134: A benchmark K dwarf with a compact planetary system, first submitted October 9; revised November 18. Explicit results for planetary envelope stripping/retention make this more than stellar-only research. Removed the unrelated ice/surface tag only for this record.

Final expected catalog 255 (+8): seven first-seen November 19, plus historical 2610.32815 first_seen October 26 entering the public catalog on a November 18 revision. Three first submissions November 19, two November 18, two older manuscripts revised November 18, plus the historical entry. Existing 2610.18982 revision is historical maintenance, not a new paper. All dates refer to Beijing days; first_seen is not publication date.

Implemented validated record-scoped topic overrides (unknown topic IDs ignored, duplicate IDs removed, no global matcher or fit-score change). Applied planetary topic to Jovian polar-cyclone 2611.21841, preserving original abstract/date/first_seen. Added regression test.

Historical missing abstracts: no invented text. Publisher evidence identifies 10.1038/s41561-026-02094-y as Research Briefing (September 10), 10.1038/s41561-026-02116-9 as Publisher Correction (September 8, Fig.2e/f axis labels), and 10.1177/15311074261485884 as special-collection Foreword (September 1). Sage public page read; Nature publisher search index read, direct Nature page blocked by identity redirect. No independent Abstract section found; source status remains missing, not declared a fetch failure. Links: https://www.nature.com/articles/s41561-026-02094-y ; https://www.nature.com/articles/s41561-026-02116-9 ; https://journals.sagepub.com/doi/10.1177/15311074261485884 .

Verification: 96 local tests passed. Offline enrichment/date/catalog/network rebuild; correction deployment and live checks pending below. No backend, voting, or unrelated layout changes. Incomplete affiliations and some other manual topic classifications remain; no claim of full historic archive review.
