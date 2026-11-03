# Daily maintenance review — 2026-11-03 (Asia/Shanghai)

## Access and current baseline
Verified the authorized 公用 connection as PkuJunyangGroup (333274266) and this repository's push/admin permissions. Read latest cloud-maintenance.json, topics.json, journals.json, README, daily.yml and November 2 maintenance record. At 10:04 Beijing, main remains bcfb92b0be8415dd2f6b4324505d5e22aa7ff9c2; the latest Actions run is the successful November 2 correction run 41443270767. No November 3 scheduled run is visible. No duplicate workflow was dispatched.

Only authorized cloud connector reads and public official source pages were used. Previously denied checkout, shell execution and live-JSON shell routes were not retried; no user computer, desktop, credentials or Worker/D1 changes.

The complete repository catalog and network were read through GitHub fetch_blob without filesystem access. Catalog contains 190 papers and 187 supplied abstracts; network has 117 institution nodes, 665 edges and 44 omitted papers, generated November 2 at 12:17:14 UTC. Independent actual cloud-browser baseline checks confirm 190, working original abstract expansion/collapse, recommendation filtering, institution author/ORCID details and statistics. Gliese 48 b, the white-dwarf population paper and the stellar-flare false positive remain excluded; four older proposed exclusions and historical metadata repairs remain unpublished. Repository blob reads do not establish a complete independent live JSON comparison.

## Source coverage and limitations
All four official arXiv recent HTML lists were inspected. The November 2 announcement lists show 7 EP, 6 ao-ph, no geo-ph and 20 flu-dyn entries. This is list inspection, not a current API/checkpoint run or exhaustive abstract review. A direct public Exoplanet.eu bibliography read timed out today; this is not evidence that its last successful November 2 automated source state failed retroactively.

Today's checkpoint scripts, 19-journal retrieval, daily_intake and 365-day fallback have not been executed in this manual review because the earlier execution boundary is unresolved. No declined route was bypassed. The report push may independently run the ordinary workflow's tests, offline enrichment/builds and Exoplanet retry, but arXiv/journals/intake are skipped on push. Such a rebuild does not replace current scientific retrieval.

## Original-abstract reading: four unadmitted leads
Four complete original English arXiv abstracts were actually read, together with submission history and HTML author-affiliation blocks. All have only v1, without a revised version. Their November 2 announcement-list date must not be relabeled as their submission/publication/update date.

1. Distinguishing N2-Dominated from O2-Dominated Atmospheres on Terrestrial Exoplanets with Reflected-Light Spectroscopy.
   Authors: Nick Burri; Mario Damiano; Renyu Hu. https://arxiv.org/abs/2610.42035 ; https://arxiv.org/html/2610.42035v1 .
   Submitted October 30 at 17:01:07 UTC (October 31 at 01:01:07 Beijing). The authors state accepted in The Astronomical Journal; a formal journal publication date was not verified. Direct atmospheric characterization/retrieval scope. Affiliations explicitly identify JPL/Caltech, ETH Zurich and Rutgers with author-specific mappings.

2. An end-to-end CNN search for ultra-short-period planets in TESS: from the blend ceiling to the independent validation of TOI-6662 b.
   Author: Juan F. Pagés Navarrete (HTML full name Juan Francisco Pagés Navarrete), Independent researcher, Málaga, Spain. https://arxiv.org/abs/2610.42009 ; https://arxiv.org/html/2610.42009v1 .
   Submitted October 30 at 16:47:34 UTC (October 31 at 00:47:34 Beijing). Submitted to Experimental Astronomy, not established accepted. Specific transit detection/validation result; narrow-priority and scoring eligibility still require the existing intake rules.

3. From Anoxic to Oxic Earth: Detectability of Atmospheric Biosignatures across Stellar Hosts with ELT/ANDES.
   Authors: Dwaipayan Dubey; Spandan Dash; Liton Majumdar. https://arxiv.org/abs/2610.41621 ; https://arxiv.org/html/2610.41621v1 .
   Submitted October 30 at 11:58:18 UTC (October 30 at 19:58:18 Beijing). Submitted to AAS, no particular accepted journal established. Direct planetary atmospheric chemistry/biosignature scope. HTML explicitly maps LMU/Origins, Université Paris Cité/IPGP/CNRS and NISER/HBNI authors.

4. Completeness and dynamical stability in exoplanet occurrence rates.
   Authors: Thomas A. Baycroft; Manu Stalport; Romain Eltschinger; Matteo Pinamonti; Jeanne Davoult; Khaled Al Moulla; Yann Alibert. https://arxiv.org/abs/2610.40964 ; https://arxiv.org/html/2610.40964v1 .
   Submitted October 29 at 20:44:13 UTC (October 30 at 04:44:13 Beijing). Abstract-page comments say resubmitted to A&A after revisions, while the HTML header lists an August acceptance; status conflict is unresolved and neither is treated as verified formal publication. Specific planetary stability/occurrence methodology. Explicit author affiliations were read, not inferred.

No native-script names were guessed. No ORCID verification was completed for these four. Complete current catalog and 500-record arXiv archive contain none of the four arXiv IDs; journal equivalents, merged scores and eligibility remain unverified. None is a November 2–3 submitted/updated paper under the source timestamps. A potential 365-day fallback needs existing score >=65, deduplication and the actual approved intake procedure; no score was fabricated or admission made.

## Counts and publication scope
New website admissions: 0. Metadata revisions: 0. Historical missing-abstract supplements: 0. Original abstracts read before the workflow: 4, all unadmitted leads, not four newly indexed papers. Current missing-abstract count remains 3. No translation or AI abstract summary was added.

Only this maintenance report was edited directly. The ordinary workflow subsequently changed the generated catalog/network and Exoplanet candidate archive, as recorded below. Configuration and source scripts were unchanged. The daily review remains partial; current journal/source coverage, actual intake/fallback, historical corrections and prior execution/approval outcomes remain unresolved. No automation pause was performed.


## Ordinary workflow outcome and two candidate-only archive additions
Report commit: 641b525a6fe8c15e32bd333043fc8cca8c664bcf. Push run https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/41563985915 completed successfully. Logs confirm 90 tests passed; Exoplanet incremental retrieval, offline enrichment, builds and Pages deployment succeeded. arXiv retrieval, journal retrieval and daily_intake were skipped, as configured for push. Apparent API failures inside test fixtures are not production source failures. Pages reported success at 02:07:57 UTC, November 3.

The actual Exoplanet production step checked 2 pages, fetched 15 recent bibliography entries and retained 2 new candidate-only records. It succeeded at 10:06:20 Beijing; this supersedes the earlier direct web timeout for production status. Generated commit 4635141f615ff35947f44651d5431f85e505dfe7 changes only catalog.json, network.json and exoplanet_records.json. Source record count is 2,338, up by 2; displayed catalog remains 190 papers, 187 supplied abstracts and daily_brief.new_count 0. Network remains 117 institution nodes, 665 links and 44 papers without confirmed parent institutions. Both JSON files were generated at 2026-11-03T02:07:40.496671+00:00.

1. Evolution of a hypothetical planetesimal disk in the HD 34445 planetary system. Exoplanet bibliography lists TERLUK A.; GARCIA R.; CORREO-OTTO J.; GIL-HUTTON R.; Icarus, in press, year 2026. Bibliography record 33357, first_seen November 3 at 10:06:20 Beijing, bibliography update/creation November 2, stored score 39. https://www.sciencedirect.com/science/article/abs/pii/S0019103526004355 . The official article page returned Cache miss; searches did not yield a readable official abstract. Original abstract, precise publication date and full author names remain unverified. This is not an abstract-reviewed paper or a website admission.
2. Ferropericlase breakdown drives mantle weakening in super-Earths. Nature Communications, DOI 10.1038/s41467-026-79163-8, https://www.nature.com/articles/s41467-026-79163-8 . Official publisher search indexing supplied the complete original abstract, which was read. Published October 31, 2026; accepted October 13, 2026; received October 27, 2025. No publication time was supplied. The accepted early article precedes the final Version of Record. Direct page access redirected to an unavailable identity service; no login bypass was attempted. Reading confirms direct super-Earth mantle mineralogy/rheology relevance. Bibliography record 33356, first_seen November 3 at 10:06:20 Beijing, stored score 31, stored year-only date and empty abstract remain unchanged. Publisher metadata verification in this report is not a silent archive repair, scoring override or admission.

The publisher affiliation block explicitly identifies 16 authors, but complete byline order was not verified: Chaojia Lv, Jin Liu, Mengyu Li, Jun Hu, Penghui Sun, Ao Deng, Guochun Yang, Yongjun Tian, Haotian Chen, Liangxu Xu, Zhaolin Cui, Jian Sun, Guoge Li, Zhigang Zhang, Nico Giordano and Jung-Fu Lin. Liangxu Xu is explicitly affiliated with the Center for High Pressure Science and Technology Advanced Research and Peking University School of Earth and Space Sciences. No native-script names or ORCIDs were inferred.

Final reading coverage: 5 of 6 examined candidate leads have complete original abstracts read; 1 remains inaccessible. None was admitted. Actual website admissions, published metadata revisions, missing-abstract supplements and one-year fallback admissions are all 0. The two bibliography archive additions are not newly published or newly recommended website papers. No today's or yesterday's publication classification is established for the Icarus record; the Nature article is an October 31 publication, not a November 2 publication. The arXiv and 19 enabled-journal production checkpoints still date to November 2; no November 3 full-source coverage or completed fallback is claimed.

## Post-deployment live verification
Independent actual cloud-browser checks passed after ordinary reload: direct online catalog.json and network.json both visibly show generated_at 2026-11-03T02:07:40.496671+00:00. Initial raw-JSON tab navigation showed a cached November 2 timestamp; reload resolved it. This is direct visible timestamp verification, not a full live-array parse or byte-for-byte comparison.

The homepage displays 190 papers. Source page shows November 3, 0 new website papers and build time 10:07:40 Beijing. Original abstract expansion/collapse, shared recommendation filtering, network overview, institution author/ORCID details and statistics were exercised successfully. The network reports 117 institutions and 44 omitted papers; repository/log evidence establishes 665 links. Pages deployment and these observed online checks succeeded, while the scientific maintenance review remains partial for the limitations above. No full November 3 arXiv/journal retrieval, intake/fallback or historical correction completion is claimed.
