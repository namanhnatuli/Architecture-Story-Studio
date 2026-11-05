# Internal review package (what the owner receives)

Generated after the review cut (`tools/longform_reports.py --project <slug>`, `tools/cli.py gates`):

| Item | File |
|---|---|
| Review video (labelled INTERNAL_REVIEW) | `output/<slug>_…_INTERNAL_REVIEW_….mp4` + `.en.srt` |
| Script and source approval package | `review/EDITORIAL_APPROVAL_PACKAGE.md`, `review/EVIDENCE_MATRIX.md`, `research/RESEARCH_REPORT.md` |
| Pronunciation notes | `review/PRONUNCIATION_REVIEW.md` (terms, timecodes, phonemes, ASR hearing) |
| Voice / asset licensing summary | `review/RIGHTS_PROVENANCE.md`, `assets/manifest.json` |
| Timecoded editorial review | `qa/EDITORIAL_REVIEW_TIMECODED.md` |
| Outstanding questions | end of the approval package (UNCERTAIN consistency rows, unresolved sources) |
| Final-approval checklist | `review/FINAL_APPROVAL_CHECKLIST.md` |
| Gates | `qa/gates.json` (technical status separate from publication readiness) |
