# ISE A3 result summary

This investigation examined Todoman as an unfamiliar repository relevant to the assignment deadline-change workflow established in ISE-A1 and specified in ISE-A2. The study froze upstream commit 78e35788606a0add0c4f99ceb702c3ea0d0b1346, recorded CPython 3.12.14 and Linux environment details, and supplied 30 pinned dependency packages with wheel hashes for offline installation.

A clean environment reproduced dependency installation, wheel construction, application startup, and the upstream test suite. The recorded suite contained 197 cases: 188 passed, six were skipped, and three remained expected failures. These exclusions and their reasons are preserved rather than presented as successful verification. Six additional characterization checks examined a deadline edit, malformed input, stale writes, date-only deadlines, executable configuration, and missing configuration.

The reconstructed path follows the CLI entry point through configuration loading, date parsing, task retrieval, calendar-file replacement, SQLite cache refresh, and displayed feedback. A filtered runtime call trace, before-and-after calendar files, cache observations, and raw command outputs support this reconstruction. Architectural interpretations are distinguished from executed facts.

Three risks concern missing academic verification and stale-version guards, temporal differences from the A2 specification, and accepting executable configuration across an untrusted boundary. An ADR compares modifying the upstream write path with a separate verification service and controlled export adapter. The latter is proposed as the safer future change boundary; no such service is claimed to be implemented.

The package includes source provenance, reproduction instructions, an executable notebook, reports, diagrams, risk records, retained negative evidence, and an AI-use verification log. All study records are synthetic; no live LMS or real student data were used.

## Stable repository reference

After uploading the extracted package contents to your GitHub repository, commit the files and create a tag such as `ise-a3-v1.0`. Submit the URL of that study commit or tag with the summary above. The upstream repository being investigated is https://github.com/pimutils/todoman/tree/78e35788606a0add0c4f99ceb702c3ea0d0b1346. This upstream URL does not replace the URL of your own evidence repository.
