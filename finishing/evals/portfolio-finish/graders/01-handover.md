---
type: llm
focus: trace
weight: 1
---

The result matches this description: The three drafts are copied with the shared folders they link to, so the copies show no broken images, and the originals are unchanged. Seven editors, one per fault kind, report findings, and a referee merges them into one ranked list per piece, capped at about 45 minutes. One approval page covers all three pieces, and the user approves once. Each of the user's known faults is fixed or on the open list with a reason: the notebook lines on A, the tree map, the winding path and the empty green space on B, and the passport style everywhere, UV-mode readability and the repeated stamp icon on C. The protected details (the sun-dial menu bar, the dog icon, the postcard contact, the ID card, the UV lamp) are still present. A blind judge compares before and after in both orders. A hand-over page shows per piece the finished link, a ledger of approved items, the open list and before/after pairs. No file is written outside finishing-runs/ except the calibration update, and no run file is tracked by git.

Fail the result if a finished page still has the passport style on most sections with no open-list entry for it, or if any file was written outside finishing-runs/<slug>/ other than finishing/calibration/README.md.
