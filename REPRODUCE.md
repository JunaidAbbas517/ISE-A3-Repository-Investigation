# Reproduction guide

## Recorded target and input identity

The verified target is CPython 3.12.14, Linux x86_64, glibc 2.39, SQLite as recorded in `environment/runtime.json`, UTC and C.UTF-8. The host kernel is recorded, not packaged. The offline wheels include Linux-specific CPython 3.12 binaries, so they are not a universal Windows/macOS environment. No container execution is claimed.

Source commit: `78e35788606a0add0c4f99ceb702c3ea0d0b1346`. Source archive SHA-256: `00e147fee9b31de498a08778aeec9d83e66ca99712b426a7de8132f1b8c56089`. `environment/input-sha256.json` locks the source archive, synthetic fixture, requirements and all 30 dependency wheels. `upstream/source-files-sha256.json` covers the extracted original tree. Dataset: `a3-synthetic-deadline-v1`; it contains one synthetic VTODO with a fixed UID and original due instant. No real academic record is needed.

## Clean automatic reproduction

Use an empty output path. Earlier runs are never overwritten:

```bash
python3 --version
python3 scripts/reproduce.py --verify-only
python3 scripts/reproduce.py --output runs/local
```

The script requires Python 3.12.14 by default. A different CPython 3.12 patch level can be tried with `--allow-runtime-difference`; the changed version is recorded, and equivalence is not assumed. Other Python minor versions or CPU/OS targets require a separately resolved and verified wheel set. On Windows, extract the package under WSL/Linux and run these commands there. That route is guidance, not a separately observed WSL run.

## Separate setup, build, test and start commands

The automatic script is authoritative; these are its equivalent commands from the package root. Its raw logs retain the exact absolute paths used in the verified run.

```bash
python3 -m venv runs/manual-venv
runs/manual-venv/bin/python -m pip install --no-index --find-links environment/wheels --require-hashes -r environment/requirements.lock
```

Build in a disposable copy of the original export. The source archive lacks Git metadata, so an explicit snapshot version is required. This is not a claim about a released Todoman version.

```bash
mkdir -p runs/manual-source runs/manual-dist
tar -xzf upstream/todoman-source.tar.gz -C runs/manual-source
export SETUPTOOLS_SCM_PRETEND_VERSION_FOR_TODOMAN=0.0+g78e35788606a
export SOURCE_DATE_EPOCH=1779715654
export TZ=UTC
export LC_ALL=C.UTF-8
export PYTHONHASHSEED=0
export DETERMINISTIC_TESTS=true
runs/manual-venv/bin/python -m build --wheel --no-isolation --outdir runs/manual-dist runs/manual-source
runs/manual-venv/bin/python -m pip install --no-index --no-deps runs/manual-dist/todoman-0.0+g78e35788606a-py3-none-any.whl
```

Tests must run from the disposable source root. The automatic script computes all paths without depending on shell activation:

```bash
cd runs/manual-source
../manual-venv/bin/python -m pytest -o addopts= -q -ra --hypothesis-seed=20261025 --junitxml=../manual-tests.xml
cd ../..
runs/manual-venv/bin/python -m todoman --version
runs/manual-venv/bin/python scripts/probe_workflow.py --output runs/manual-workflow
runs/manual-venv/bin/python -m pip check
```

Todoman is a command-line program, so there is no web server or frontend bundle. Building its Python wheel is the build step. Startup is observed through the installed CLI and a configured list operation. After the automatic run:

```bash
runs/local/venv/bin/todo --version
runs/local/venv/bin/todo --config runs/local/workflow/workspace/config.py list
```

## Expected evidence and exclusions

`summary.json` records 188 passes, 6 skips, 3 expected failures and 6 successful study observations. One skip is the uninstalled optional REPL; four are invalid recurrence combinations; one is a UI case linked to upstream issue 537. The expected failures concern issue 9 and two unimplemented configuration cases. Raw reasons and tracebacks remain in XML/text. The suite's default coverage flags are disabled explicitly because this study does not report coverage. Upstream test logic is unchanged.

The Hypothesis seed and deterministic profile are fixed. Absolute due dates and the synthetic UID are fixed. Upstream LAST-MODIFIED values, filesystem mtimes, temporary paths, elapsed times and test timings legitimately vary. Semantic assertions are reproduced; byte-identical output logs are not promised. SOURCE_DATE_EPOCH controls wheel metadata; the observed wheel hash is in `evidence/verified/summary.json`.

## Evidence preservation

Original evidence in `evidence/verified` is read-only input to review. New runs go under `runs/`. The first harness attempt, in `evidence/04-probe-attempt-1.txt`, failed because an icalendar list was treated as an iterator. The corrected harness uses `iter(...)`. This was not an upstream test failure. The malformed-date and missing-config commands intentionally exit 2 and 1; the probe verifies those codes and preserves stderr. Synthetic config execution writes only a marker within the isolated workspace.

## GitHub handoff

From your extracted study root, use your own Git identity and repository. Do not upload virtual environments or generated `runs/` directories. The included `.gitignore` excludes them. A stable evidence tag can be created after reviewing the package:

```bash
git init
git add .
git commit -m "Record ISE A3 repository investigation"
git tag ise-a3-v1.0
```

Then connect your own remote and push the commit/tag. Submit your study commit/tag URL and the summary in `PLATFORM-SUBMISSION.md`. The investigated upstream source is independently pinned at https://github.com/pimutils/todoman/tree/78e35788606a0add0c4f99ceb702c3ea0d0b1346.
