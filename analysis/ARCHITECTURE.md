# Repository architecture and evidence classification

## Selection and scope

Todoman was selected because it already edits due dates, serializes persistent task records and has a test suite and redistribution licence. It is a personal POSIX CLI rather than a university application. Its official README explicitly excludes native Windows. A small Flask candidate was inspected but not selected because its root lacked a standalone licence text and its dependency/UI scope would add unrelated investigation. No execution or security conclusion is claimed about that rejected candidate.

All locations below refer to commit `78e35788606a0add0c4f99ceb702c3ea0d0b1346` and the unchanged tree under `upstream/todoman/`. `source-index.json` gives definition lines; stable web links can be formed from https://github.com/pimutils/todoman/blob/78e35788606a0add0c4f99ceb702c3ea0d0b1346/. Source facts are distinguished from runtime facts, inferences and proposals.

| Component | Verified location | Responsibility and status |
|---|---|---|
| CLI entry | `pyproject.toml` project.scripts; `todoman/__main__.py:6` | `todo` delegates to `todoman.cli:cli`; module execution is exercised. Source and runtime fact. |
| Startup/configuration | `cli.py:329`; `configuration.py:220` | Loads Python configuration, discovers list paths, constructs Database and registers close handling. Source fact; exercised in the trace. |
| Commands | `cli.py:428,497,548` | New/edit/show command functions; this study exercises edit, show, list and version. Source fact. |
| Parsing/formatting | `formatters.py:255,262` | Parses configured local datetime/date and natural-language fallback; returns local aware datetime or all-day date. Source fact; absolute datetime/date exercised. |
| Domain object | `model.py:39` | Todo fields, including due, UID and sequence. Source fact. |
| Persistence facade | `model.py:1064,1164` | Database discovers files; save increments sequence, writes VTODO then refreshes cache. Source and runtime fact. |
| Authoritative local files | `model.py:296,393,408` | VtodoWriter serializes and replaces `.ics` records using `atomic_write`. Disk snapshots demonstrate persisted due values. |
| SQLite cache | `model.py:422,453,668` | Derived query/index data and local numeric IDs; cache commit follows file writing. Cache rows are observed directly. |
| Interactive UI | `interactive.py`, `widgets.py` | Urwid editor widgets; inspected structurally, not interactively exercised by this study. |

## Data and external interfaces

The task file is the local durable task representation; SQLite is a derived cache that also assigns local numeric IDs. Those IDs should not be assumed to be stable academic assignment identifiers. JSON porcelain output, CLI arguments, local filesystem operations and optional editor invocation are interface boundaries. The README describes synchronization via a separate tool such as vdirsyncer; no live CalDAV or other network synchronization was executed. There is no LMS API, web server, multi-user login or institutional source-verification service in this traced path.

Critical dependencies are Click/click-log for CLI/error handling, icalendar for parsing and serialization, python-dateutil and parsedatetime for temporal behavior, pyxdg for configuration/cache discovery, and urwid for the optional interactive editor. Humanize affects display. Setuptools, wheel, setuptools-scm, build and vcs-versioning support wheel construction; pytest, Hypothesis and freezegun support tests. All transitive installed versions are locked, with their wheels and licences retained. Standard-library sqlite3 is recorded separately through the runtime.

## Facts and inferences

**Runtime facts:** the wheel builds offline; the CLI starts; the suite has 188 passes, 6 skips and 3 expected failures; P1 persists the expected due value and cache sequence; P3 accepts a stale save; P4 persists an all-day date; P5 executes a harmless marker in configuration. See the retained raw evidence.

**Source facts:** configuration is loaded using `exec_module`; file replacement and the SQLite commit are separate operations; the examined edit/save path has no A2 candidate, owner-confirmation, evidence-authority or base-version contract.

**Inferences:** interruption between file replacement and cache commit could temporarily diverge file and cache state; this particular failure window was not injected. Loss of a named institutional time zone during mapping could affect academic interpretation; no DST transition experiment was performed. These are not measured failures.

**Proposal:** introduce a separate service that owns A2 records, verifies owner/source/version/time and only then exports approved personal deadlines. It is documented in ADR-001 and has not been implemented in A3.
