# Executed deadline edit path

## Input and oracle

P1 starts from `data/assignment.ics`: UID `ise-a3-assignment-01@example.invalid`, due 10 October 2026 at 16:30 UTC and SEQUENCE 1. The normal edit supplies `--due "2026-10-17 16:30"` under UTC with `%Y-%m-%d` and `%H:%M` formats. The expected persisted due instant is 17 October at 16:30 UTC and SEQUENCE 2. The study fixture is UTC; it is not a conversion of the Asia/Shanghai A2 fixture. Real deployment must preserve A2 explicit zone/offset semantics.

The actual command is preserved in `evidence/verified/workflow/commands.json`. Its wrapper installs a filtered Python call profiler and invokes the real `todoman.__main__` using runpy. It changes neither application source nor task arguments. The 28 observed selected calls are in `call-trace.json`; this filtered trace is not a complete function-coverage record.

| Stage | Static definition | Observed trace positions | Evidence |
|---|---|---|---|
| Entry/config | `__main__.py:6`, `cli.py:329`, `configuration.py:220` | 1–2 | CLI and configuration calls |
| Parse proposed due | `cli.py:99`, `formatters.py:255,262` | 5–9 | Date validator and parser calls |
| Retrieve existing record | `cli.py:497`, `model.py:1136,970,919` | 10–13 | Edit, Database/Cache retrieval and object reconstruction |
| Version and serialize | `model.py:1164,385,393,345` | 14–21 | save, writer, serializer and datetime normalization |
| Replace persistent file | `model.py:273` | 22–23 | Context-manager calls; before/after `.ics` snapshots verify content |
| Refresh and commit cache | `model.py:1012,602,668,453` | 24–27 | Cache expiry, insertion and commit; SQLite row snapshot |
| Display feedback | `formatters.py:213` | 28 | Detailed output; a fresh porcelain show command independently reads the update |

Trace function first-line values may point to the first decorator, whereas source-index.json records the def statement. This explains, for example, trace edit line 471 versus definition line 497; they identify the same decorated function.

## Negative evidence

P2 supplies an unrecognized date, observes exit 2 and compares file bytes before/after. P3 reads the same task twice before either save; the second stale object replaces the newer due value and repeats the same resulting sequence. This is a deterministic stale-object interleaving, not a measured parallel-process race. P4 shows date-only persistence. P5 shows trusted-local Python configuration execution using a harmless marker. P6 records missing-configuration exit 1.

Passing characterization assertions establish that those behaviors were observed. They do not certify conformance to A2, source authenticity, authentication or production safety.
