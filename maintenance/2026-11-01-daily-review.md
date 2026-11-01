# Daily maintenance review — 2026-11-01 (Asia/Shanghai)

## Scope and current status

Checked the authorized PkuJunyangGroup account (333274266) and target repository push/admin permissions. Read current cloud-maintenance.json, topics.json, journals.json, README, workflow and latest published maintenance record. No user computer or desktop session was used.

At 10:06 Beijing, main remains 8476c10572dfb15e78c92c059473295e7a64b2e9. No November 1 scheduled run is visible in the latest Actions records. The latest completed run is October 31 correction run 41200016063. No duplicate workflow was dispatched.

This is a partial review: no new admission is confirmed today. It does not establish that all sources have no new papers.

## Source and reading coverage

The dot-owned cloud checkout operation was denied by platform review, including one evidence-backed retry clarifying the cloud environment. That route was stopped. Therefore the checkpoint-based arXiv/journal retrieval scripts, daily_intake, 365-day fallback and fresh local build/tests were not executed in this round. Prior data and pending changes were not overwritten.

Read-only checks of the four official arXiv recent-submission pages succeeded. Each currently shows October 30 as its latest listing date. This HTML title-list check is not a successful API incremental fetch, does not establish complete replacement coverage, and is not original-abstract reading. No new original English abstracts were read or newly admitted in this round. No new author, affiliation or ORCID mapping was added; no translation or summary was introduced.

A separate read-only request to https://exoplanet.eu/bibliography/all/ timed out. It is a failed check, not evidence of zero updates. The 19 enabled journal configurations and four disabled journals were preserved; current journal retrieval was not completed. No historical missing abstract was recovered.

## Existing live-site verification

Independent live HTTPS checks found catalog.json and network.json with matching generation time 2026-10-31T12:13:11.778364+00:00: 190 catalog papers, 187 supplied abstracts, 117 institution nodes, 665 links, 44 papers without confirmed parent institutions. Actual cloud-browser checks passed original-abstract expansion/collapse, Recommended filtering (one recommended paper), return to all 190 papers, institution graph/author/ORCID detail, and 19-journal/six-month statistics display. November statistics remain marked incomplete/unavailable rather than fabricated as zero. No recommendation vote or backend state was changed.

The published Gliese 48 withdrawal and white-dwarf-demographics exclusions remain effective; their source archives were preserved by the previously verified October 31 corrections. Four earlier proposed exclusions remain online. Other pending author-affiliation and original-abstract math repairs are not claimed published. The old uncertain Git blob operation was not replayed, and automatic publication is not treated as approval of it.

## Publication boundary and remaining work

Only this maintenance record is submitted. No source record, first_seen, intake, rule, frontend, Worker/D1 or database is changed in this commit. Its normal push workflow can run CI, offline enrichment/dates and builds plus the existing Exoplanet.eu step; by current workflow design it skips arXiv/journal/intake steps. Such CI does not substitute for the unexecuted source checks above. Actual commit, workflow and live results will be verified after submission and reported separately.

Remaining: resolve the denied cloud-checkout execution route before using it again; obtain the actual outcome of earlier pending writes before replaying any old operation; complete current source checks/intake and any needed 365-day fallback; reconcile fresh main before applying any remaining historical correction. No automation pause was performed.
