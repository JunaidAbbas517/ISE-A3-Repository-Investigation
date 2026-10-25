# Execution evidence guide

`01-clean-install.txt` is the initial online dependency resolution and installation. `02-upstream-initial.txt/.xml` retain the initial upstream suite. `03-wheel-download.txt` records acquisition of the exact dependency wheels. `04-probe-attempt-1.txt` retains a failed study-harness run; the error is an investigator assumption about the icalendar API, not an upstream failure. The accompanying `probe-attempt-1/commands.json` records the completed startup command. `05-probe-attempt-2.txt` and its directory retain the corrected, pre-tracing probe run.

`verified/` contains the later clean offline build, test, start, dependency check and traced workflow. `summary.json` reports the outcomes. `execution.json` and `logs/` retain exact commands and exit codes. `upstream-tests.xml` retains every test and reason. `workflow/commands.json` retains stdout/stderr for normal and intentionally failing commands; `call-trace.json` records selected actual calls. Calendar snapshots, cache rows and `results.json` are the independent observation outputs.

Absolute workspace paths in raw logs identify the actual execution context; they are not portable commands or credentials. Use the reproducer to generate equivalent paths locally. Expected upstream failures and skipped tests are limitations, not successful guarantees. Passing study checks include successful observations of absent protections.

`06-notebook-authoring-attempt1.txt` records the first authoring runner being invoked from outside the documented working directories. The executed notebook and `notebook/` evidence retain the successful rerun.
