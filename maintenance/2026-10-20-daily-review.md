# Daily reading review — 2026-10-20 (Asia/Shanghai)

## Sources and intake

Cloud-only maintenance using verified GitHub account PkuJunyangGroup (333274266) with repository push permission. Read current maintenance configuration, topics, journal registry, README, daily workflow and recent maintenance records.

Scheduled [run 39354856030](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/39354856030) succeeded at 09:46:39 Beijing; generated snapshot 067a61ddb44fc44283b35d7857c2626eee128a90. All four enabled arXiv categories succeeded with zero retrieved records. All 19 enabled Crossref journal sources succeeded. Exoplanet.eu succeeded, checking two pages and retrieving nine entries with zero retained. Source retrieval/retention counts are metadata processing counts, not new public admission counts. Four disabled journals remain disabled. No failure, retry, duplicate fetch or one-year fallback was needed.

## Reading and primary metadata verification

Exactly one new public admission, first_seen 2026-10-20T01:42:21.792622+00:00 (09:42:21 Beijing):
- [Coupled Orbital and Interior Evolution of Sub-Neptunes](https://doi.org/10.3847/1538-4357/aea905), Ritika Sethi, Sarah Millholland and Tim Hallatt, The Astrophysical Journal.
- Online publication: 2026-10-19; print publication: 2026-10-20. Classified as yesterday's online journal publication collected today, not first publication today.
- Read the entire original publisher-deposited English abstract from the fresh [Crossref record](https://api.crossref.org/works/10.3847%2F1538-4357%2Faea905), not only keywords or title. The model explicitly couples planetary cooling, mass loss and tidal orbital evolution of sub-Neptunes; retain as relevant. Automated score 61 is not a fallback admission: the 65 cutoff applies to older fallback candidates.
- Independently read the full [arXiv abstract](https://arxiv.org/abs/2609.20611). It has the same title and three authors, submitted September 17, 2026, and states accepted for ApJ. This is an earlier preprint of the same work, not an additional new research result. Crossref currently exposes no formal relation entry, and the local source archive has no corresponding preprint record. No fabricated DOI relation or extra historical intake was added; this evidence is retained here for future deduplication.
- Crossref explicitly authenticates all three ORCIDs: Sethi 0000-0002-6576-3346; Millholland 0000-0003-3130-2282; Hallatt 0000-0003-4992-8427. All list Massachusetts Institute of Technology and MIT Kavli Institute for Astrophysics and Space Research. Network correctly counts one MIT parent for this paper. No native-script names were inferred.

Coverage: one newly admitted work, both complete journal and preprint abstracts read. Existing 157 public paper objects are unchanged from yesterday. This is not a claim of rereading every historical abstract. No correction or new native-name alias was necessary.

Today-first-published/updated admissions: 0; yesterday's journal article collected today: 1; one-year supplements: 0; historical corrections: 0. New supplied abstracts: 1 through the scheduled intake; manually repaired historical gaps: 0. Catalog: 158 papers, 155 supplied original abstracts, 3 historical gaps. The gaps remain 10.1038/s41561-026-02094-y, 10.1038/s41561-026-02116-9 and 10.1177/15311074261485884.

## Tests and publication

Python: 89 tests passed. Six frontend JavaScript scripts and six backend test cases passed, using the pinned KaTeX 0.16.22 bundle. All 158 cards were checked for complete, closed-by-default abstracts; 130 formula spans rendered without errors. Existing bilingual display remains on 39 papers. Offline enrichment/date processing and catalog/network builds passed. Only generation timestamps changed during rebuilding; those incidental generated-file changes are not committed.

Network: 109 parent institutions, 507 links, 158 papers, 35 without confirmed parent. Existing first_seen values, archived metadata and duplicate/version records are preserved. No UI, workflow, Worker or D1 modifications.

Only this report is committed, based on a freshly checked main head with a conditional ref update. Scheduled deployment succeeded. The report commit's subsequent Actions/Pages deployment and live catalog.json, network.json and related pages are checked separately before the user briefing; this report commit alone is not represented as deployment success. HTTP/data/renderer checks are not a visual browser audit.
