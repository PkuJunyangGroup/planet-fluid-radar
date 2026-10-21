# Daily reading review — 2026-10-21 (Asia/Shanghai)

## Sources and intake

Cloud-only review using verified GitHub account PkuJunyangGroup (333274266), with admin/push permission on this repository. Read current cloud-maintenance.json, topics.json, journals.json, README, workflow and previous report.

Scheduled [run 39528855642](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/39528855642) succeeded at 09:48:41 Beijing; generated commit b3ee8f97630df22554abdc55d5d170318c0a8871. All four enabled arXiv categories, 19 enabled Crossref journals and Exoplanet.eu succeeded. Exoplanet.eu checked two pages (nine retrieved entries, one retained source entry). All four disabled journals remain disabled. No failed source, targeted retry, duplicate full fetch or one-year fallback was needed. Retrieval/retention numbers are not public admission counts.

Six automatically admitted candidates were reviewed by reading their complete original English abstracts. Five are retained; one space-physics paper is excluded with a sourced override. Original source archives, first_seen and version relationships are preserved. Yesterday's 158 catalog paper objects were unchanged before this review.

## Reading and primary-source verification

### Yesterday's new papers, collected today

1. **When the core ate the atmosphere** — Vera Sparrman; Anders Johansen. arXiv 2610.27788v1, submitted 2026-10-20 07:52:06 UTC, collected 2026-10-21 01:42:29 UTC. [Abstract](https://arxiv.org/abs/2610.27788v1), [author block](https://arxiv.org/html/2610.27788v1). Complete original abstract concerns rocky-planet formation and atmosphere/mantle/core volatile partitioning. Both author mappings to University of Copenhagen and Johansen's additional Lund University affiliation match the paper. No explicit ORCID in the author block; none inferred. Accepted in A&A is not recorded as a dated journal publication.

2. **Exomoonlight Sonata: On the Fate of Exomoons Around Migrating White Dwarf Planets** — Ritvik Sai Narayan; Joseph R. Livesey; Juliette Becker. arXiv 2610.27484v1, submitted 2026-10-20 01:49:34 UTC, collected 2026-10-21 01:42:29 UTC. [Abstract](https://arxiv.org/abs/2610.27484v1), [author block](https://arxiv.org/html/2610.27484v1). Complete abstract concerns exomoon survival during high-eccentricity planetary migration. MIT and University of Wisconsin–Madison author mappings agree; two explicit ORCIDs agree. Submitted to ApJL is not a published ApJL article. Added the narrow phrase high eccentricity migration to the existing orbital topic; existing required planetary-context gating remains unchanged and a regression tests nonplanetary stellar binaries.

3. **A Radio Science Experiment for Dragonfly to Investigate Titan's Rotation and Interior Structure** — Flavio Petricca; Dustin Buccino. Geophysical Research Letters, online 2026-10-20, print 2026-10-28, collected 2026-10-21 01:42:53 UTC. [DOI](https://doi.org/10.1029/2026gl125753), [fresh publisher-deposited Crossref record](https://api.crossref.org/works/10.1029/2026gl125753). Complete original abstract read: proposed Titan geodesy constrains rotation, tides, interior structure and possible subsurface ocean. Both explicit JPL/Caltech affiliations and supplied ORCIDs agree. Crossref does not mark those ORCIDs authenticated; they are explicit publisher associations, not name-search guesses.

### Yesterday's version updates, first collected today

4. **Thermal Evolution of Lava Planets Across System Ages: Predictions for Hell of a Survey** — Mariana Sastre and 24 coauthors (complete source author list retained in catalog). [v2 abstract](https://arxiv.org/abs/2609.20155v2), [v2 author block](https://arxiv.org/html/2609.20155v2). First submitted 2026-09-17 12:45:44 UTC; v2 2026-10-20 09:33:31 UTC; collected 2026-10-21 01:42:29 UTC. All 25 author–institution mappings checked against HTML; no ORCID links supplied. Complete abstract describes coupled lava-planet interior/atmosphere evolution and phase-curve predictions. Removed incidental Ice & surface mechanism tag; retained relevant magma, spectra and numerical tags. Accepted to ApJ has no supplied journal DOI. This is recent-version intake, not one-year fallback.

5. **Resonant lunar tides of Earth's core and basal magma ocean** — Murray B. C. Kiernan; Hamish C. F. C. Hay; David W. Rees Jones; James F. J. Bryson; Richard F. Katz. [v2 abstract](https://arxiv.org/abs/2606.16340v2), [v2 author/ORCID blocks](https://arxiv.org/html/2606.16340v2). First submitted 2026-06-15 07:44:25 UTC; v2 2026-10-20 07:35:38 UTC; collected 2026-10-21 01:42:29 UTC. Complete abstract describes planetary core/BMO tidal resonance and dynamo implications. Corrected malformed converted affiliations in the version-specific cache: Kiernan and Hay both St Andrews/Oxford; Rees Jones St Andrews; Bryson and Katz Oxford. Added the five explicit paper-listed ORCIDs, all with valid check digits. Rejected automatic extraction retained for audit. No inferred native-script names. This is recent-version intake, not fallback. The source says accepted/in press without a journal name.

### Excluded after reading

**Widespread plasma jets in the Martian magnetosheath revealed by dual-spacecraft observations**, DOI 10.1073/pnas.2616582123. Complete [publisher-deposited original abstract](https://api.crossref.org/works/10.1073/pnas.2616582123) and metadata read. The subject is magnetosheath plasma jets, pickup ions, cyclotron waves, bow shocks and solar-wind interaction. Space plasma physics is explicitly out of scope; Mars wording and PNAS venue do not override this boundary. Removed from public catalog via override, not deleted from source archive.

## Corrections and checks

Expected reviewed catalog: 163 papers (net five added), 160 with original abstracts, three historical missing abstracts unchanged. Today-first-published/updated: zero; yesterday first-publication intake: three; yesterday-version-update intake: two; one-year supplements: zero; old catalog corrections: zero. New-candidate metadata/tag corrections are distinct from historical cleanup.

A live browser check exposed adjacent inline formulas in 2610.27788 rendering as raw dollar syntax. Applied the smallest tokenizer fix allowing a closing single-dollar delimiter immediately before the next opening delimiter. Original abstracts are untouched. Regression tests cover the three observed strings, adjacent inline/display formulas, currency, escaped dollars, incomplete formulas and unsafe HTML/TeX.

Validation before commit:
- Scheduled Actions: 89 Python tests and enrichment/date/catalog/network builds passed.
- Six-candidate classification checks passed with five retained/one excluded; Exomoonlight now has the orbital topic.
- Updated Node math regression passed in memory, without saving repository files to disk.
- Real KaTeX 0.16.22 integration passed using its SHA384-verified official bundle; all current catalog abstracts exercised, 22 contained typeset math.
- Cloud browser verified compact English listing, source/added dates, recommendation controls loading, default collapsed abstracts and actual expansion. This caught the adjacent-formula regression above.
- Live catalog.json and network.json were fetched successfully before corrections, matching scheduled generation time and 164-paper pre-review state.

The cloud checkout attempt was denied by the platform's interpretation of the local-path restriction; it was not retried. Repository reads/writes use the verified connector; permitted memory-only checks and live-site reads use dot cloud, never the user's computer. No workflow, Worker/D1, credentials or UI redesign changes.

Only necessary source configuration, versioned affiliations, frontend fix/regressions and this record are committed against a freshly checked main head. The push workflow will run offline enrichment/dates and rebuild both public datasets. Commit, Actions/Pages completion, final live catalog/network and corrected page rendering must be verified after this report commit before the user is told publication succeeded.
