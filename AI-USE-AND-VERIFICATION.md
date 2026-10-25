# AI use and source verification log

## Assistance and responsibility

ChatGPT/Codex prepared this package in the current conversation using the supplied A1/A2 archives and A3 brief. AI assistance covered repository discovery, source inspection, shell/Python execution, dependency locking, study-harness authoring, evidence interpretation, diagrams, report drafting and packaging. No separate human reviewer or independent student reproduction has been recorded. Student review and the final GitHub upload are still required; no peer review, participant interview or teacher approval is invented.

## Accepted and rejected suggestions

| Suggestion/task | Decision | Verification or reason |
|---|---|---|
| Investigate Todoman's real due-date/persistence path | Accepted | Retrieved source at a full Git commit, retained ISC notice, built and tested it |
| Use the earlier A2 reference model as if it were an unfamiliar existing application | Rejected | It is known project material and lacks the repository/application breadth needed for this investigation |
| Use an initially inspected Flask candidate | Rejected | Its root lacked standalone licence text; additional unrelated frontend/dependency scope was unnecessary |
| Treat SEQUENCE or atomic replacement as stale-write protection | Rejected | P3 demonstrates overwrite from a stale object with the same resulting sequence |
| Treat all-day/local dates as A2-compliant instants | Rejected | P4 persists an all-day date without an exact cutoff instant |
| Treat Python configuration as harmless upload data | Rejected | P5 executes a harmless marker during configuration load |
| Build a source export without explicit SCM version handling | Rejected as incomplete | Export has no Git metadata; the documented snapshot version is supplied explicitly |
| Present skipped or expected failing cases as passes | Rejected | All counts and raw reasons are preserved |
| Use `next(Calendar.walk(...))` in the first probe harness | Rejected after execution | Actual TypeError retained; changed to `next(iter(...))` and reran |
| Freeze the manually typed expected epoch | Replaced | Expected epoch is calculated independently from a UTC datetime in the harness |

## Verification ledger

Source identity is checked through the full upstream commit, archive hash and per-file inventory. Upstream tests inspect many existing behaviors; the additional probes inspect actual files, cache rows, exit codes and selected runtime calls rather than returning a self-reported compliance flag. This is execution-based verification of AI-generated claims, not an assertion that AI execution substitutes for independent human assessment.

The entire offline reproduction was run from a clean environment. The resulting source wheel hash is recorded; two clean builds before notebook/ZIP QA produced the same hash. The final ZIP was extracted into a new directory and the complete offline procedure reproduced the same outcomes and wheel hash; raw extraction validation is retained in evidence/extraction-validation. The notebook was executed sequentially in one Python namespace; its additional clean offline run is retained in evidence/notebook. The first authoring attempt used an unsupported working directory and is documented in evidence/06-notebook-authoring-attempt1.txt. Reproducibility is limited to the recorded environment and tested procedures. Native Windows, WSL itself, live CalDAV/LMS, production identity/security controls, interactive UI usability, fault-window recovery and real-user value were not independently tested.

No real student data, credentials, institutional documents, private messages or account tokens were used. The initial A1 simulated profiles remain simulated. Report conclusions distinguish execution facts, source facts, inference and proposed future changes.
