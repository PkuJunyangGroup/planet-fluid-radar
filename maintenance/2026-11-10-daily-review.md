# Daily maintenance review — 2026-11-10 (Asia/Shanghai)

## Execution and source coverage
Used only the designated PkuJunyangGroup cloud GitHub connection and dot cloud/web reading. Identity, repository admin/push permission, current configuration, topics, journals, README, workflow and prior maintenance were verified. No user computer, alternative account, manual workflow dispatch, new credentials, Worker/D1 changes or source checkpoint reset.

Checks at 10:04, 15:05 and 16:17 Beijing found no November 10 run. Scheduled run [42782246320](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42782246320) then started at 16:23:22 and published successfully at 16:44:11 Beijing. Data commit: e41218abc8e6e24939635114d01a3e5bde5d6605.

All four arXiv API categories succeeded: astro-ph.EP 15, physics.ao-ph 8, physics.geo-ph 5, physics.flu-dyn 13 records (41 category hits; cross-listed duplicates are not independent papers). Exoplanet.eu succeeded: two pages, four recent entries, zero retained additions. All 19 enabled journals succeeded; 201 retrieved and 72 retained in source archives, not 72 public admissions.

| Enabled journal | Retrieved | Retained |
|---|---:|---:|
| Nature | 29 | 0 |
| Science | 1 | 1 |
| PNAS | 27 | 5 |
| Nature Geoscience | 1 | 0 |
| Nature Astronomy | 0 | 0 |
| Nature Climate Change | 3 | 0 |
| Journal of the Atmospheric Sciences | 1 | 1 |
| Atmospheric Chemistry and Physics | 9 | 5 |
| Journal of Geophysical Research: Atmospheres | 47 | 26 |
| Journal of Climate | 20 | 15 |
| Climate Dynamics | 40 | 11 |
| Climate of the Past | 0 | 0 |
| Quarterly Journal of the Royal Meteorological Society | 3 | 2 |
| Astrobiology | 0 | 0 |
| Geophysical Research Letters | 3 | 0 |
| Journal of Geophysical Research: Planets | 3 | 3 |
| The Astrophysical Journal | 9 | 2 |
| The Astrophysical Journal Letters | 2 | 1 |
| Earth and Planetary Science Letters | 3 | 0 |

The four disabled ocean journals remained disabled. Current and previous-month statistics for the 19 enabled journals refreshed successfully. Crossref registrations are not complete publisher research-paper counts. Production source failures: zero. Simulated failures inside the test suite are not source failures. No repeated arXiv/journal ingestion or annual fallback was run.

## Reading review and narrow corrections
The job initially selected seven recent items. Complete original abstracts were read for all seven, plus the newly recovered ridge paper and the existing revised sub-Neptune paper. Official arXiv original pages supplied the five selected arXiv abstracts, recovered ridge paper and existing revision; complete publisher-deposited originals for the two journal papers were read in the source-backed catalog. The ring paper's explicit earlier arXiv original was also read. This is nine reviewed paper records, with ten source/version abstract texts, not an exhaustive reading of the entire incoming archive.

Excluded 2611.12655, “Testing Models of Disk Formation and Gravito-Viscous Evolution Against Observations of Young Protoplanetary Disks,” by Fabiola Antonietta Gerosa, Paola Pinilla, Eduard I. Vorobyov and James McKevitt. Its complete v1 original concerns disk formation, self-gravity, viscosity and gas/dust radii/masses, not a direct planetary process. First submission 2026-11-09 16:24:07 UTC; site first_seen 2026-11-10T08:23:33.861725+00:00. Preserve source archive, DOI 10.1093/mnras/stag2130 and first_seen. Evidence: https://arxiv.org/abs/2611.12655v1 .

Kept 2611.12881 because its explicit result includes planetary companion occurrence and the planet-like/stellar-like mass-ratio boundary. It is not an isolated brown-dwarf characterization study.

Added only the existing recent archive record 2611.12560 with a paper-specific candidate override and intake entry. Recency, complete original abstract, authors, no withdrawal, and catalog duplication were checked. The data-only preflight confirmed that all unrelated configuration and intake fields stayed unchanged. Source archive timestamps and first_seen were not edited. Source changes: intake commit b14ab837380e352915a3726bcd69fac9beaa4ed7 [skip ci], then topics commit d39bb61b47669cd350712add8e50c92a6bef1085. No parsing/classification code or global topic terms changed.

## Retained new site entries
Final intended additions: seven; six retained from the automated selections plus one manually recovered recent record. One-year supplements: zero.

Date classes: two genuinely new arXiv submissions on November 10 Beijing (mass-ratio desert, MarsNet); three November 9 papers first indexed today (rocky-planet devolatilization, TOI-2535 b, Neptunian ridge); one journal publication today with an earlier October preprint (circumplanetary rings); one new arXiv archival upload of 2018 research (Jovian gas accretion). Do not conflate these categories.

### The Brown Dwarf Desert is a Mass-Ratio Desert: Astrometric Demographics of 63,254 Stars
- Authors: William Thompson; Alexandre Bouchard-Côté; Dori Blakely; Trevor Campbell; Jessica Speedie; Judah Van Zandt; Kyle Franson; Jerry Xuan; Doug Johnstone; Emma Turtleboom; Jingwen Zhang; Clarissa Do Ó; Brendan Bowler; Jean-Baptiste Ruffio; Eric Nielsen; Ryan Cloutier; Andre Fogal; Kaitlyn Hessel; Christian Marois; Alexandra Rochon; William Roberson; Simon Blouin.
- Source: arXiv; 2611.12881v1.
- Source publication: 2026-11-09T18:59:28Z; Beijing publication day in catalog: 2026-11-10. Version timestamp: 2026-11-09T18:59:28+00:00.
- Site first_seen: 2026-11-10T08:23:33.861725+00:00 (2026-11-10 16:23:33 Beijing).
- https://arxiv.org/abs/2611.12881

### Simulation of a Jovian Planet Undergoing Gas Accretion
- Authors: Fabian Menezes.
- Source: arXiv; 2611.12819v1.
- Source publication: 2026-11-09T18:21:38Z; Beijing publication day in catalog: 2026-11-10. Version timestamp: 2026-11-09T18:21:38+00:00.
- Site first_seen: 2026-11-10T08:23:33.861725+00:00 (2026-11-10 16:23:33 Beijing).
- https://arxiv.org/abs/2611.12819
- This is a new arXiv upload of an already published 2018 paper: Revista Mackenzie de Engenharia e Computação 18(1), 67–82. The original day/month is not established. The official arXiv abstract and HTML state the 2018 journal reference and a minor typographical correction. Do not call it new 2026 research. Evidence: https://arxiv.org/html/2611.12819v1 ; original publisher link identified by that manuscript: https://editorarevistas.mackenzie.br/rmec/article/view/11018/7357 . The catalog's date describes its arXiv publication, not the 2018 journal date.

### MarsNet: Learning the Martian Atmosphere from Observations Alone
- Authors: Sebastian Mengwall; J. Michael Battalio.
- Source: arXiv; 2611.12787v1.
- Source publication: 2026-11-09T17:57:01Z; Beijing publication day in catalog: 2026-11-10. Version timestamp: 2026-11-09T17:57:01+00:00.
- Site first_seen: 2026-11-10T08:23:33.861725+00:00 (2026-11-10 16:23:33 Beijing).
- https://arxiv.org/abs/2611.12787

### The compositional link between rocky exoplanets and their host stars is consistent with Earth-like devolatilization
- Authors: Yared Reinarz; Lorena Acuña-Aguirre; Haiyang S. Wang.
- Source: arXiv; 2611.12581v1.
- Source publication: 2026-11-09T15:37:31Z; Beijing publication day in catalog: 2026-11-09. Version timestamp: 2026-11-09T15:37:31+00:00.
- Site first_seen: 2026-11-10T08:23:33.861725+00:00 (2026-11-10 16:23:33 Beijing).
- https://arxiv.org/abs/2611.12581

### Entering the Era of Circumplanetary Ring Detection with Direct Imaging
- Authors: Samantha N. Hasler; Alexandra Z. Greenbaum; Geoffrey Bryden; Vanessa Bailey; Jorge Llop-Sayson; Elizabeth Lane; Mary Anne Limbach; Logan Pearce; James G. Ingalls; Patrick Lowrance.
- Source: The Astrophysical Journal; DOI 10.3847/1538-4357/aeb012; doi:10.3847/1538-4357/aeb012.
- Source publication: 2026-11-10; Beijing publication day in catalog: 2026-11-10.
- Site first_seen: 2026-11-10T08:24:00.626988+00:00 (2026-11-10 16:24:00 Beijing).
- https://doi.org/10.3847/1538-4357/aeb012
- Journal dates: online 2026-11-10; print 2026-11-20 (publisher-deposited metadata). Explicit matching preprint https://arxiv.org/abs/2610.23850 was first submitted 2026-10-16 17:58:49 UTC, or October 17 Beijing. Both original abstracts were read. The full current arXiv archive and catalog contain no separate 2610.23850 record, so no duplicate entry or invented earlier site intake was created.

### A TESS Disappearing Act: The Vanishing Transits of TOI-2535 b
- Authors: Samuel W. Yee; Erik A. Petigura; Rafael Brahm; Karen A. Collins; Gregor Srdoc; David W. Latham; Allyson Bieryla; Victoria DiTomasso; Thomas Henning; Andrés Jordán; Trifon Trifonov; Khalid Barkaoui; Phil Evans; Emmanuel Jehin; Mourad Ghachoui; Michaël Gillon; Eric Girardin; Felipe Murgas; Enric Palle; Adam Popowicz; Don J. Radford; Howard M. Relles; Richard P. Schwarz; Avi Shporer; Abderahmane Soubkiou; David Watanabe; Francis P. Wilkin; Carl Ziegler.
- Source: The Astrophysical Journal Letters; DOI 10.3847/2041-8213/aeb4a4; doi:10.3847/2041-8213/aeb4a4.
- Source publication: 2026-11-09; Beijing publication day in catalog: 2026-11-09.
- Site first_seen: 2026-11-10T08:24:00.626988+00:00 (2026-11-10 16:24:00 Beijing).
- https://doi.org/10.3847/2041-8213/aeb4a4
- Journal dates: online 2026-11-09; print 2026-11-10. Read the complete publisher-deposited original abstract, exact author list and dated metadata preserved by the successful source job. Independent publisher-page retrieval was unavailable.

### The Neptunian ridge depends on the choice of linear or logarithmic period
- Authors: Kaiming Cui; David J. Armstrong.
- Source: arXiv; 2611.12560v1.
- Source publication: 2026-11-09T15:25:49Z; Beijing publication day in catalog: 2026-11-09. Version timestamp: 2026-11-09T15:25:49+00:00.
- Site first_seen: 2026-11-10T08:23:33.861725+00:00 (2026-11-10 16:23:33 Beijing).
- https://arxiv.org/abs/2611.12560
- Manually recovered from this run's existing arXiv archive after complete official abstract reading. It directly tests Neptune-size exoplanet occurrence versus orbital-period coordinate and is a relevant companion to indexed 2611.03643. Its automatic keyword score remains 0; there is no score floor for recent papers. The >=65 threshold is solely for one-year fallback. No DOI, exact-title or source-ID catalog duplicate was found. No global keyword or topic rules were broadened.


## Existing revision and historical maintenance
[Composition gradients in sub-Neptunes: K2-18 b and TOI-270 d as case studies](https://arxiv.org/abs/2609.04318v3), Luca Morf and Ravit Helled, advanced from v2 to v3. Original arXiv submission: 2026-09-03 18:00:03 UTC (September 4 Beijing). v3: 2026-11-09 13:15:17 UTC (21:15:17 Beijing), explicitly language compliance with A&A guidelines. The original abstract is unchanged; this is not a new scientific result or new site admission. Original site first_seen remains 2026-11-05T07:53:36.356665+00:00.

All 59 explicit ORCID mappings supplied with the selected records passed format/checksum validation. This is validation of supplied identifiers, not independent name-search identity matching. The scheduled job added 56 ORCID-name cache entries, all with null name_zh. No new Chinese names or institution relationships were invented or manually mapped. The three pre-existing missing public abstracts remain unresolved. No historical abstract supplement was added.

The raw record total rose 2757→2813 (+56). The arXiv archive has 664 records, with 39 first_seen today. Full journal archive reading failed with a connector transport error; only current status, complete selected journal entries and public diff were reviewed. The remaining incoming archival records were not exhaustively original-abstract audited. Do not claim no missed papers or a complete review of all 2813 records.

## Tests, deployment and live verification
Scheduled run and correction push [42798842845](https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42798842845) each passed all 90 Python unit tests. The correction run used offline enrich.py and dates.py, built catalog/network, and published successfully at 18:26:24 Beijing. arXiv, journal ingestion and daily_intake were skipped on this push. The workflow's existing incremental Exoplanet step ran once: one page, zero recent entries/additions, success. No full ingestion was repeated.

Corrected generated data commit: 1c6b8ff84a904abf6625b3998192aa27f13f09d8. Final repository catalog: 220 papers, 217 supplied abstracts, three missing abstracts, 29 linked duplicate variants, 2813 raw records. Complete before/after comparison establishes exactly one removed public ID (2611.12655), one added public ID (2611.12560), and every other 219 paper object unchanged. All source fields on the added item, including abstract, authors, dates and first_seen, exactly match its existing archive. No public intro_* fields.

Independent dot cloud-browser verification confirmed live catalog and network generation time 2026-11-10T10:25:45.897419+00:00, the expected ID swap, seven-entry daily brief, 220 papers, no enabled-source issues, and preserved added-item first_seen. Network: 123 parent institutions, 780 edges, 1584 researchers, 220 papers and 52 without confirmed parent affiliation. Network initially showed the previous cached version, then the corrected version was verified. Search, compact list and full-abstract expansion were checked. No frontend or backend code changed, and no new local/JavaScript test execution is claimed.

The added ridge abstract exposes an existing mixed-TeX-delimiter rendering limitation in its first sentence (visible source symbols around the approximate radius). The original abstract remains intact; not all formula rendering is flawless. This cosmetic issue was not patched without a permitted tested code path.

This final maintenance-record commit uses [skip ci], changes no site data, and does not trigger another retrieval or deployment.

## Remaining limitations
- Three historical missing abstracts and unconfirmed institution mappings remain.
- General Exoplanet parser/withdrawal-detection and older metadata issues remain unchanged.
- Full incoming journal-archive original-abstract audit is incomplete.
- The manual ridge entry retains its empty keyword-derived topic list and score 0; its scope decision is explicit in the override rather than a fabricated automatic match. Mixed-delimiter formula rendering noted above remains.
- Journal dates above are publisher-deposited source metadata; independent publisher-page retrieval was unavailable. IOP's non-retryable block was respected.
- No prior denied shell/checkout path was retried, no uncertain older operation was replayed, and no untested parser or broad rule code was committed.
