# Daily maintenance review — 2026-11-02 (Asia/Shanghai)

## Access, scope and current status

Verified the authorized PkuJunyangGroup account (333274266) and this repository's push/admin permissions. Read current cloud-maintenance.json, topics.json, journals.json, README, daily workflow and the latest maintenance record. Only authorized cloud connectors and public read-only source pages were used; no user computer or desktop was accessed.

At 10:04 Beijing, current main is e0f0bd2f5830577e6f32375715860d737ed1ac95. The latest Actions run is the completed November 1 scheduled run 41284979222; no November 2 scheduled run is yet visible. No duplicate workflow was dispatched.

No new admission is confirmed in this manual review. This does not establish that sources have no new papers.

## Reconciliation of yesterday's later automatic run

Yesterday's morning report preceded a delayed scheduled run. Run https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/41284979222 later executed arXiv, journal and intake steps, including the 365-day fallback with zero selected, and published successfully at 07:36:03 UTC. Its overall failure was the final source-failure report after Exoplanet.eu URLError, not a Pages deployment failure. The subsequent independent review confirmed 190 papers / 187 abstracts, unchanged paper objects and first_seen values, and read four complete original abstracts from seven new source records; those four were out of scope and three EPSL records lacked abstracts. These are November 1 results, not newly performed November 2 reading or retrieval.

## Current source and abstract coverage

The previously twice-denied cloud checkout/execution route remains stopped. No retry, alternate synchronization route or workaround was attempted today. Therefore this manual review has not executed checkpoint-based arXiv or journal scripts, daily_intake, the 365-day fallback, or local build/tests.

Public read-only checks of all four configured official arXiv recent-submission lists succeeded. Each latest listing is October 30. This is HTML list inspection only, not complete API coverage or full original-abstract reading. A direct public read-only check of https://exoplanet.eu/bibliography/all/ timed out. Failure is not zero updates.

New original abstracts read in this round: 0. New admissions: 0. Metadata revisions: 0. Historical abstract supplements: 0. The 19 enabled and four disabled journal configurations, original archives, first_seen values and version relationships are unchanged. No new translation, summary, native-script name or ORCID mapping was added.

## Current live baseline

Independent live checks confirm catalog.json and network.json generated 2026-11-01T07:35:49.982349+00:00: 190 papers, 187 abstracts, 117 institution nodes, 665 edges and 44 papers without confirmed parent institutions. The two October 31 paper exclusions remain effective; four older proposed exclusions and other historical author-affiliation/math repairs remain unpublished. Three historical abstract gaps remain.

## Publication and remaining work

Only this maintenance record is submitted. No rules, source records, site code, Worker/D1, database or user settings are changed. The ordinary push workflow may run its tests, offline enrichment/dates and builds plus the existing Exoplanet.eu retry; by design it skips arXiv, journals and intake on push. A successful report-triggered rebuild must not be described as completed current scientific retrieval.

Remaining: obtain a valid resolution of the denied cloud execution route before reuse; do not replay old uncertain Git blob operations; reconcile fresh main and Actions before any permitted continuation; complete today's source and abstract review, recent intake and fallback if applicable. Automatic later publication does not resolve platform approval or execution restrictions. No automation pause was performed.

Actual commit, CI, Pages and post-publication live outcomes are to be checked after this report commit.

## Final workflow and verification result at 10:09 Beijing

Report commit 78d7253a73f786c1e35733e770cc792063c0fb14 triggered https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/41375765444 . All 90 Python tests passed. Offline enrichment/dates, catalog/network builds and Pages succeeded; Pages reported success at 02:06:40 UTC. The overall run failure is only the post-publication source report: the actual production Exoplanet.eu attempt failed with URLError at 02:05:31 UTC. ArXiv, journal and intake steps were skipped on this push. Unit-test fixture output is not production retrieval evidence.

Generated-data commit 25f2f2aa27a56bf50abc8577d848839f9b9e4309 is on main. Its complete connector diff changes only catalog/network generation times, daily-brief date/build time and Exoplanet attempt timestamps. No public paper object, first_seen or source-archive content changed. Repository catalog remains 190 papers / 187 abstracts and network 117 nodes / 665 edges / 44 omitted.

Actual cloud-browser checks after deployment show November 2 zero additions, build 10:06:29 Beijing, homepage 190 and working complete original-abstract expansion. Baseline browser checks also covered recommendation filtering, institution author/ORCID details and journal statistics. However, independent full live catalog/network JSON retrieval was not completed: shell retrieval was denied, browser JSON accessibility parsing timed out on size, and the web retrieval tool could not access those resources. No denied read route was retried. Repository diff proof and actual UI checks must not be misrepresented as a full live-array comparison.

This final record-only update uses [skip ci] to avoid another rebuild. The manual review remains partial: source intake and current original-abstract review are unexecuted, full live JSON verification is incomplete, and the earlier platform restrictions and pending historical corrections are unresolved.


## Late scheduled-run reconciliation and correction, 20:20 Beijing

The delayed scheduled run https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/41407661555 started at 07:39 UTC and fully succeeded, including 90 tests, all source steps, intake and Pages at 07:49:44 UTC. Its generated commit was 4873ce4e359f9eeeb793e3bbb16a99624bc9421a. Thus the early manual-stage statements above do not describe the later automated retrieval.

All four arXiv APIs succeeded with zero incoming records, and all 19 enabled journal sources succeeded. Exoplanet.eu recovered: the scheduled run scanned 70 recent entries over five pages and retained four keyword candidates in its source archive. All four bibliography abstracts are empty; they are not four published admissions or four completed reading reviews. Their explicit linked preprints are 2609.05413, 2609.31778, 2610.30243 and 2610.28533. Broader new journal/source-archive abstract review remains incomplete: the connector could not return the large journal file and its oversized patch was omitted. No false full-coverage claim is made.

The rule intake selected one recent paper, DOI 10.3847/1538-4357/aeacc3, published November 2 and first recorded 2026-11-02T07:39:49.873011+00:00. Its title is “Frequent Optical Flares in an M-type Detached Eclipsing Binary TIC 349005337”; authors Xiao Zhou, Liying Zhu, Wei Hu, Gil Nachmani, Jia Zhang, Mikhail Yu. Kovalev and Ergang Zhao; source The Astrophysical Journal. The full publisher-deposited original abstract was actually read in the cloud browser at https://api.crossref.org/works/10.3847/1538-4357/aeacc3 and independently on the live card. It concerns stellar component parameters, stellar superflares, magnetic activity and dynamos; potential exoplanet atmospheres appear only as future motivation. It is outside the existing narrow planetary scope.

A new paper-specific exclusion, and no other rule change, was committed as e12186181168e00a28b62a88f90a9f0075ea3344 through the normal authorized connector. This did not replay any earlier pending mutation. Correction run https://github.com/PkuJunyangGroup/planet-fluid-radar/actions/runs/41443270767 fully succeeded: 90 tests, offline build and Pages at 12:17:48 UTC. Its normal Exoplanet.eu checkpoint retry also succeeded, with 12 recent entries from two pages and zero new candidates. Generated main is 778054246d834fe6698039e4949f7085b1acb57b.

The full repository comparison proves journal_records.json was untouched by the correction, preserving the excluded paper's original abstract and first_seen. Catalog changes remove only aeacc3 plus normal timestamps/status; all other paper objects and first_seen remain unchanged. Build returns 190 papers / 187 abstracts, network 117 institutions / 665 edges / 44 omitted. Actual cloud-browser verification confirms homepage 190, a TIC 349005337 search with no results, the retained Europa abstract expansion, functioning network page, and November 2 zero admissions with build time 20:17:14 Beijing. All displayed enabled source statuses are successful. Complete independent live JSON-array retrieval was not repeated; repository evidence and UI verification remain distinct.

Current retained new admissions are zero; one new mistaken admission was removed. This is not a finding that all sources contain no suitable papers. The automated intake originally stayed in recent mode because of that mistaken admission; the 365-day fallback has NOT been rerun after the exclusion under the unresolved execution boundary. Broader archive reading and this fallback therefore remain incomplete. Historical missing-abstract supplements remain zero; four older exclusions and other historical repairs remain unpublished. Earlier checkout/approval restrictions are not resolved by the successful automated jobs. No user computer, denied route, backend change or credential operation was used.
