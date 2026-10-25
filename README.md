# ISE A3 Repository Investigation and Reproducible Build

This package investigates **Todoman** as a possible task-storage boundary for the deadline-change problem in A1 and the verification rules in A2. The central result is that ordinary deadline edits work, while academic verification, stale-version protection, and explicit-instant semantics require a separate controlled boundary. This is a repository investigation, not a completed university application.

## Frozen upstream

Repository: https://github.com/pimutils/todoman  
Commit: `78e35788606a0add0c4f99ceb702c3ea0d0b1346`  
Stable source: https://github.com/pimutils/todoman/tree/78e35788606a0add0c4f99ceb702c3ea0d0b1346  
Licence: ISC, retained in `upstream/todoman/LICENCE`. No upstream source changes were made.

The complete source export, original compressed export, and SHA-256 inventories are included. The build label `0.0+g78e35788606a` is a study snapshot identifier supplied through setuptools-scm, not an upstream release name.

## Main contents

| Path | Purpose |
|---|---|
| `report/ISE-A3-Final-Report.pdf` | Main readable report |
| `report/ISE-A3-Final-Report.docx` | Editable report |
| `REPRODUCE.md` | Setup, build, test, start, evidence and platform instructions |
| `environment/` | Runtime record, 30 hash-locked packages, offline wheels and notices |
| `upstream/` | Frozen upstream source, licence, commit and hashes |
| `analysis/ARCHITECTURE.md` | Entry points, modules, data, interfaces and fact/inference distinction |
| `analysis/CALL-PATH.md` | Static locations mapped to the observed runtime calls |
| `analysis/RISK-REGISTER.md` | Three scoped risks and follow-up acceptance criteria |
| `analysis/risk-register.csv` | Machine-readable register |
| `analysis/TRACEABILITY.md` | A1/A2/A3 continuity and deliverable coverage |
| `adr/ADR-001.md` | Two responses compared for the main write-boundary risk |
| `diagrams/` | Architecture, call path and proposed boundary in SVG and PNG |
| `scripts/` | Offline reproducer, workflow probes and runtime tracing |
| `notebook/ISE-A3-Investigation.ipynb` | Executed top-to-bottom investigation notebook |
| `evidence/` | Original setup output, failed harness attempt, tests, trace, raw fixture states |
| `AI-USE-AND-VERIFICATION.md` | Tools, accepted/rejected suggestions and verification limitations |
| `PLATFORM-SUBMISSION.md` | 150–300-word result summary and final URL instructions |

## Reproduce with one command

From the extracted root, using CPython 3.12.14 on Linux x86_64:

```bash
python3 scripts/reproduce.py --output runs/local
```

The command creates a fresh virtual environment, installs the supplied wheels without a network, builds the frozen source, executes the upstream suite, starts the CLI, runs six study probes, and checks dependencies. It preserves all output in a new directory. Native Windows is not supported by upstream; use a suitable Linux/WSL environment. WSL itself was not independently tested here. See `REPRODUCE.md` for version differences and separate commands.

## Verified results

The recorded clean run used CPython 3.12.14, Linux x86_64, UTC, fixed synthetic input, PYTHONHASHSEED=0 and Hypothesis seed 20261025. The upstream suite reports **188 passed, 6 skipped and 3 expected failures**, out of 197 cases. Six study characterization checks also pass; some establish missing safeguards, so these are not six security guarantees. No coverage percentage or production-readiness claim is made.

All data are synthetic. The CLI and local storage path were tested; institutional authentication, live CalDAV/LMS synchronization, interactive terminal usability, native Windows and production deployment were not tested. The retained first probe failure was an investigator-harness API assumption, not an upstream defect.

## Upload and submit

Upload the **contents of this extracted folder**, not only the ZIP, to your study repository. Create your own commit/tag and submit its stable URL plus the summary in `PLATFORM-SUBMISSION.md`. This package does not claim that your A3 evidence has already been pushed to GitHub.
