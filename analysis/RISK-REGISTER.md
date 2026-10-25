# Risk register

Priorities are qualitative assessments for the proposed academic workflow, not measured probabilities or CVSS scores. These are adaptation risks; intended personal CLI behavior is distinguished from institutional requirements.

## R1 Direct writes lack the A2 verification and stale-version boundary

**Condition:** The CLI/model is reused as the authoritative academic-deadline writer or multiple stale clients save the same record.

**Evidence:** Source: cli.py edit; model.py Database.save. Runtime: P3 overwrites a newer due value and repeats the resulting sequence.

**Impact:** An unreviewed or stale proposed deadline can replace a personal record without the A2 owner/source/version contract.

**Priority:** High for the proposed academic workflow; not a claim of a remote upstream vulnerability.

**Response:** Use a protected A2 service as record owner and export only approved revisions; compare alternatives in ADR-001.

**Acceptance:** Non-owner/unverified/stale updates rejected; one revision per confirmation; retry creates no duplicate history.

**Residual:** Direct external writers can still change exported calendars; export is not academic authority.

**Owner:** Future implementation maintainer; no person has been assigned.

## R2 Date-only and local-time semantics differ from the A2 explicit-instant contract

**Condition:** A date or locally interpreted value is mapped to an academic deadline without explicit time and institutional zone.

**Evidence:** Source: formatters.py parse_datetime; model.py normalize_datetime. Runtime: P4 persists a date-only DUE value.

**Impact:** The system could display an all-day date where an exact cutoff instant is required.

**Priority:** High when academic cutoffs require exact instants; no incidence rate measured.

**Response:** Validate explicit timestamp, offset and named zone before export; preserve the original source zone in the owning service.

**Acceptance:** Missing time/zone and offset mismatch rejected; UTC and zone round trips checked against A2 examples.

**Residual:** Ambiguous institutional notices require human clarification; no DST study was executed.

**Owner:** Future deadline-domain maintainer; unassigned.

## R3 Executable Python configuration crosses a trust boundary if accepted as uploaded data

**Condition:** A future web/API workflow accepts user-provided Todoman config files or builds config from unchecked text.

**Evidence:** Source: configuration.py load_config uses exec_module. Runtime: P5 writes an isolated harmless marker.

**Impact:** Configuration code runs with process permissions; this is inappropriate for untrusted notices or uploads.

**Priority:** High for untrusted service input; trusted-local CLI configuration is the upstream design.

**Response:** Keep deployment-owned configuration fixed; accept only validated data in the future service and never load uploaded Python.

**Acceptance:** Uploaded config/code is not accepted or executed; service account has limited filesystem access.

**Residual:** A trusted deployment administrator can still run local code; sandbox enforcement was not implemented.

**Owner:** Future deployment/security maintainer; unassigned.
