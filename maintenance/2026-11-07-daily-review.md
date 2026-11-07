# Daily review: November 7, 2026 (Beijing)

## Scope and scheduled run
The authorized PkuJunyangGroup connection and repository permissions were verified. Current cloud-maintenance.json, topics.json, journals.json, README, daily workflow, intake policy and maintenance records were checked. Scope remains four arXiv categories, 19 enabled journals and incremental Exoplanet.eu. The four disabled ocean journals remain disabled.

The morning checkpoint found no November 7 scheduled run. The delayed scheduled run subsequently started at 15:05:19 Beijing and completed successfully at 15:13:25:
https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/42349777866

No manual dispatch, duplicate full retrieval or fallback search was performed. Generated data commit: ec26af36fafb9139d729dd1fa356e5587366148f. Main was checked again before this report-only commit.

## Sources and tests
All four arXiv categories succeeded at 15:05:31 Beijing with zero records in their existing incremental windows. All 19 enabled Crossref journal queries succeeded, with the shared checkpoint 15:06:01. Zero query counts are not claims of zero journal publication. Exoplanet.eu succeeded at 15:05:57, checking two pages and 19 recent bibliography entries and retaining four source-archive entries. Two match previously indexed papers; the other two were not admitted by today's intake. No new malformed concatenated entry was found among these four.

Production source failures: 0. Intake search errors: 0. The workflow ran 90 Python tests successfully, followed by enrichment, date processing, recent intake, catalog/network builds and successful Pages publication. Failure strings in unit-test recovery fixtures are not production source failures. Some older arXiv HTML affiliation lookups remained unavailable; source retrieval success does not imply complete affiliation coverage. No code change or independent executor test run is claimed.

## Original abstract reading and retained new item
All selected originals were read: 1 of 1. The complete original English abstract was independently read on the publisher page, with the article information and explicit author/ORCID fields. The source-backed catalog abstract agrees with it. Retain as direct exoplanet mass/composition characterization; this is not a generic stellar-activity paper. Its rule fit score of 31 is a ranking signal, not a quality rating, and the 65-point threshold applies only to one-year fallback.

**“Mega-Earths” are Likely an Artifact of Stellar Activity**
- Authors: Casey L. Brinkman; Nicolas B. Cowan.
- Journal: The Astrophysical Journal Letters, volume 1011, number 2, L62 (2026).
- DOI: 10.3847/2041-8213/aeb5f5.
- Publisher-confirmed online publication: November 6, 2026. Publisher-deposited issue/print date: November 10, 2026.
- First_seen: 2026-11-07T07:06:01.407845+00:00, November 7 at 15:06:01 Beijing.
- Links: https://doi.org/10.3847/2041-8213/aeb5f5 ; https://iopscience.iop.org/article/10.3847/2041-8213/aeb5f5 .
- The publisher explicitly associates both authors with McGill University. Author ORCIDs match the deposited metadata: https://orcid.org/0000-0002-4480-310X and https://orcid.org/0000-0001-6129-5699. No names or affiliations were inferred.

This is a yesterday-published, first-indexed-today paper. It is not a November 7 publication, an arXiv revision or a one-year fallback.

## Earlier-seen links and unadmitted leads
Exoplanet entries 33385 and 29077 were linked to existing arXiv records 2611.08489 and 2411.16879, respectively. Their original first_seen dates, November 6 and October 8, remain unchanged. These are two added provenance variants, not new independent papers or new arXiv revisions. Bibliography journal labels alone do not establish a formal publication date.

The two remaining bibliography leads were checked against complete original abstracts and version histories on official arXiv pages:
- Pierre Auclair-Desrotour; Jacques Laskar; Mohammad Farhat; Gwenaël Boué. “An analytical framework for atmospheric tides on rocky planets. II. Semidiurnal thermotidal torque.” arXiv 2611.07060v1, submitted November 4 at 19:19:17 UTC, November 5 at 03:19:17 Beijing; accepted for Astronomy & Astrophysics according to the arXiv comment. https://arxiv.org/abs/2611.07060v1 .
- Wenqin Wang; Yue Wang; Di-Chang Chen; Hui Zhang; Jian Ge; Bo Ma. “Prospects for detecting hot-Jupiter tidal decay through transit timing with the mission Earth 2.0.” arXiv 2611.07427v1, submitted November 5 at 04:20:55 UTC, November 5 at 12:20:55 Beijing. https://arxiv.org/abs/2611.07427v1 .

Both are relevant in content, but their verified versions precede the November 6–7 recent window. Exoplanet's November 6 update dates are bibliography updates, not paper revision dates. Their source entries were first seen on November 7 at 15:05:57 Beijing, but they are not publicly admitted additions. No fallback was invoked because a suitable recent paper exists. No scores were invented and no intake approval was added. Their incomplete source metadata remains available for a future eligible, bounded intake review.

## Counts, historical changes and publication
Public catalog: 213 papers, 210 supplied original abstracts, versus 212 and 209 previously.
- Newly admitted and retained: 1.
- Published or revised on November 7: 0.
- Published yesterday and first indexed today: 1.
- One-year fallback additions: 0.
- New arXiv versions among existing public records: 0.
- Abstract supplements to existing public records: 0.
- Existing public first_seen values changed: 0.
- Added provenance variants for earlier-seen papers: 2.
- Manual scientific exclusions, code/configuration corrections, author repairs or institution mappings: 0.
- Reading coverage: all 1 selected original plus 2 unadmitted bibliography leads.

Live cloud-browser verification completed after publication. Homepage shows 213 papers. The new paper is compact by default; expanding Abstract shows the complete original and separate Published November 6 / Added November 7 dates. Sources shows today's one new paper and successful source checkpoints; monthly statistics show a November 7 check and mark November incomplete.

Live catalog.json and network.json show build 2026-11-07T07:13:08.557471+00:00 (15:13:08 Beijing). A cached direct network view initially showed the prior build; a fresh URL query verified today's artifact. The ordinary institution page also shows today's new paper under McGill with both matching ORCID links. Its all-institution view has 122 institutions, 765 links, 163 represented papers and 50 papers without verified parent institutions. The default sparse overview remains available. No full byte-for-byte live-array comparison is claimed.

No site-data correction was necessary. This report-only commit uses [skip ci] to record the completed reading review without another fetch or deployment. Historical missing abstracts and incomplete affiliation information remain; the prior quarantined Exoplanet parser/source-format issue is not claimed resolved.
