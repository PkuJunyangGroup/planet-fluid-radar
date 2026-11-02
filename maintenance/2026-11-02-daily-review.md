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
