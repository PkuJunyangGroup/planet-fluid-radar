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
New website admissions: 0. Metadata revisions: 0. Historical missing-abstract supplements: 0. Original abstracts read: 4, all unadmitted leads, not four newly indexed papers. Current missing-abstract count remains 3. No translation or AI abstract summary was added.

Only this truthful maintenance report is submitted. Data/configuration and archives are unchanged. Actual commit, CI, Pages and post-publication checks will be recorded after the normal workflow. The daily review remains partial; current journal/source coverage, actual intake/fallback, historical corrections and prior execution/approval outcomes remain unresolved. No automation pause was performed.
