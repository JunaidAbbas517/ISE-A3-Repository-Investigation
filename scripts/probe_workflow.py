"""Run isolated characterization probes against the installed upstream wheel.

No production records, networks, student identities, or university systems are used.
Checks passing here establish observations, including missing protections.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from datetime import date, datetime, timezone

from icalendar import Calendar
from todoman.model import Database
from todoman.configuration import load_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    workspace = out / 'workspace'
    tasks = workspace / 'lists' / 'Coursework'
    tasks.mkdir(parents=True)
    task_file = tasks / 'assignment.ics'
    shutil.copy2(root / 'data/assignment.ics', task_file)
    config = workspace / 'config.py'
    cache = workspace / 'cache.sqlite3'
    config.write_text(
        f'path = {str(tasks)!r}\ncache_path = {str(cache)!r}\n'
        'date_format = "%Y-%m-%d"\ntime_format = "%H:%M"\n'
        'default_list = "Coursework"\ndefault_due = 0\ncolor = "never"\n'
    )
    env = os.environ.copy()
    env.update(TZ='UTC', LC_ALL='C.UTF-8', PYTHONHASHSEED='0')
    commands = []

    def command(label, arguments, *, expected_code=0, trace=False):
        cmd = ([sys.executable, str(root / 'scripts/trace_cli.py'), '--trace',
                str(out / 'call-trace.json'), '--', *arguments] if trace else
               [sys.executable, '-m', 'todoman', *arguments])
        result = subprocess.run(cmd, cwd=workspace, env=env, capture_output=True, text=True)
        record = {'label': label, 'argv': cmd, 'exit_code': result.returncode,
                  'stdout': result.stdout, 'stderr': result.stderr}
        commands.append(record)
        (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        assert result.returncode == expected_code, record
        return result

    def edit(label, value, expected_code=0):
        return command(label, ['--config', str(config), '--color', 'never',
                               'edit', '--due', value, '1'], expected_code=expected_code,
                       trace=label == 'normal-edit')

    def snapshot(name):
        shutil.copy2(task_file, out / name)
        component = next(iter(Calendar.from_ical(task_file.read_bytes()).walk('VTODO')))
        due = component.decoded('DUE')
        return {'due': due.isoformat(), 'type': type(due).__name__,
                'sequence': int(component.get('SEQUENCE', 0)),
                'sha256': hashlib.sha256(task_file.read_bytes()).hexdigest()}

    results = []
    command('installed-entry-point', ['--version'])
    before = snapshot('01-before.ics')
    listing = command('initial-list', ['--config', str(config), '--porcelain', 'list'])
    assert len(json.loads(listing.stdout)) == 1
    edit('normal-edit', '2026-10-17 16:30')
    after = snapshot('02-after-edit.ics')
    assert after['due'] == '2026-10-17T16:30:00+00:00'
    assert after['sequence'] == before['sequence'] + 1
    show = command('read-after-edit', ['--config', str(config), '--porcelain', 'show', '1'])
    expected_epoch = datetime(2026, 10, 17, 16, 30, tzinfo=timezone.utc).timestamp()
    assert json.loads(show.stdout)['due'] == expected_epoch
    with sqlite3.connect(cache) as conn:
        conn.row_factory = sqlite3.Row
        rows = [dict(row) for row in conn.execute('SELECT id,uid,due,due_dt,sequence FROM todos')]
    (out / 'cache-after-edit.json').write_text(json.dumps(rows, indent=2) + '\n')
    assert rows[0]['sequence'] == after['sequence']
    assert rows[0]['due'] == expected_epoch
    results.append({'id': 'P1', 'observation': 'Normal CLI edit persists due value and increments SEQUENCE; a new CLI process and SQLite cache agree.',
                    'before': before, 'after': after, 'passed': True})

    old_bytes = task_file.read_bytes()
    edit('invalid-date', 'not-a-deadline-XYZ', expected_code=2)
    assert task_file.read_bytes() == old_bytes
    results.append({'id': 'P2', 'observation': 'Malformed date returns exit 2 and leaves the calendar file byte-identical.', 'passed': True})

    # Both references are read before either update; no thread scheduling is needed.
    with Database([str(tasks)], str(cache)) as db:
        stale_a = db.todo(1)
        stale_b = db.todo(1)
        observed_sequence = stale_a.sequence
        stale_a.due = datetime(2026, 10, 21, 16, 30, tzinfo=timezone.utc)
        db.save(stale_a)
        first_sequence = stale_a.sequence
        stale_b.due = datetime(2026, 10, 24, 16, 30, tzinfo=timezone.utc)
        db.save(stale_b)
        second_sequence = stale_b.sequence
    stale = snapshot('03-after-stale-save.ics')
    assert stale['due'] == '2026-10-24T16:30:00+00:00'
    assert first_sequence == second_sequence == observed_sequence + 1
    results.append({'id': 'P3', 'observation': 'A stale Todo object overwrites a newer due date without a version-conflict error.',
                    'base_sequence': observed_sequence, 'first_saved_sequence': first_sequence,
                    'second_saved_sequence': second_sequence, 'final': stale,
                    'claim_falsified': 'SEQUENCE alone prevents stale-writer lost updates.', 'passed': True})

    edit('date-only-edit', '2026-10-25')
    date_only = snapshot('04-date-only.ics')
    assert date_only['type'] == 'date'
    results.append({'id': 'P4', 'observation': 'A date-only due value is accepted and persisted as an all-day date, without a UTC instant.',
                    'final': date_only, 'claim_falsified': 'Every accepted Todoman deadline meets A2 explicit-instant semantics.', 'passed': True})

    marker = workspace / 'synthetic-config-marker.txt'
    executable_config = workspace / 'synthetic-executable-config.py'
    executable_config.write_text('from pathlib import Path\n' +
                                 f'Path({str(marker)!r}).write_text("synthetic config executed")\n' + config.read_text())
    load_config(str(executable_config))
    assert marker.read_text() == 'synthetic config executed'
    results.append({'id': 'P5', 'observation': 'Configuration is executable Python; a harmless synthetic marker is written during load_config.',
                    'claim_falsified': 'A Todoman configuration file is inert data safe to accept from an untrusted source.', 'passed': True})

    missing = workspace / 'does-not-exist.py'
    command('missing-config', ['--config', str(missing), 'list'], expected_code=1)
    results.append({'id': 'P6', 'observation': 'An explicitly missing configuration produces exit 1 and actionable error text.', 'passed': True})
    report = {'dataset_id': 'a3-synthetic-deadline-v1',
              'clock_policy': 'Absolute due values are fixed. Upstream LAST-MODIFIED records actual execution time and is not compared byte-for-byte across runs.',
              'checks_passed': len(results), 'results': results,
              'scope': 'Local CLI and model characterization, not authentication, LMS integration, performance, or network security assurance.'}
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
