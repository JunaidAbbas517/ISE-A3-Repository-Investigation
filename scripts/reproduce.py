"""Rebuild the frozen repository and run its tests and isolated study probes.

Uses only the Python standard library for bootstrap. Dependencies are installed
from the included, hash-locked Linux x86_64 CPython 3.12 wheel set, without network.
Every invocation writes a new output tree, preserving previously recorded runs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import time
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_counts(xml_path):
    cases = ET.parse(xml_path).getroot().iter('testcase')
    counts = dict(passed=0, skipped=0, xfailed=0, failed=0, errors=0)
    for case in cases:
        skip = case.find('skipped')
        if case.find('failure') is not None:
            counts['failed'] += 1
        elif case.find('error') is not None:
            counts['errors'] += 1
        elif skip is not None:
            key = 'xfailed' if 'xfail' in skip.get('type', '').lower() else 'skipped'
            counts[key] += 1
        else:
            counts['passed'] += 1
    counts['total'] = sum(counts.values())
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--allow-runtime-difference', action='store_true',
                        help='Allow a different 3.12 patch level or Linux release; record the difference.')
    args = parser.parse_args()
    meta = json.loads((ROOT / 'upstream/UPSTREAM.json').read_text())
    recorded = json.loads((ROOT / 'environment/runtime.json').read_text())
    expected = json.loads((ROOT / 'environment/input-sha256.json').read_text())
    for filename, digest in expected.items():
        if sha256(ROOT / filename) != digest:
            raise SystemExit('Input checksum mismatch: ' + filename)
    print('Verified', len(expected), 'frozen input checksums.', flush=True)
    if args.verify_only:
        return
    if sys.version_info[:2] != (3, 12) or platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise SystemExit('This offline wheel set requires CPython 3.12 on Linux x86_64; use a suitable WSL/Linux environment.')
    mismatch = platform.python_version() != recorded['python']
    if mismatch and not args.allow_runtime_difference:
        raise SystemExit('Recorded Python is ' + recorded['python'] + '; use that version or explicitly pass --allow-runtime-difference.')
    out = (args.output or ROOT / 'runs' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')).resolve()
    out.mkdir(parents=True, exist_ok=False)
    logs = out / 'logs'
    logs.mkdir()
    env = os.environ.copy()
    env.update(TZ='UTC', LC_ALL='C.UTF-8', PYTHONHASHSEED='0',
               DETERMINISTIC_TESTS='true', PIP_DISABLE_PIP_VERSION_CHECK='1',
               SETUPTOOLS_SCM_PRETEND_VERSION_FOR_TODOMAN=meta['snapshot_version'],
               SOURCE_DATE_EPOCH=str(int(datetime.fromisoformat(meta['commit_datetime']).timestamp())))
    stages = []

    def run(stage, cmd, cwd=None):
        log = logs / (stage + '.txt')
        start = time.monotonic()
        with log.open('w') as stream:
            stream.write('COMMAND ' + json.dumps([str(c) for c in cmd]) + '\n')
            stream.write('CWD ' + str(cwd or ROOT) + '\n')
            stream.flush()
            result = subprocess.run([str(c) for c in cmd], cwd=cwd or ROOT,
                                    env=env, stdout=stream, stderr=subprocess.STDOUT)
            elapsed = round(time.monotonic() - start, 3)
            stream.write('\nEXIT_CODE ' + str(result.returncode) + '\n')
            stream.write('ELAPSED_SECONDS ' + str(elapsed) + '\n')
        stages.append({'stage': stage, 'argv': [str(c) for c in cmd],
                       'exit_code': result.returncode, 'elapsed_seconds': elapsed,
                       'log': str(log.relative_to(out))})
        (out / 'execution.json').write_text(json.dumps(stages, indent=2) + '\n')
        print(stage + ': exit ' + str(result.returncode), flush=True)
        if result.returncode:
            print(log.read_text()[-4000:], flush=True)
            raise SystemExit('Stopped; failed stage and earlier evidence preserved in ' + str(out))

    source = out / 'source'
    source.mkdir()
    with tarfile.open(ROOT / 'upstream/todoman-source.tar.gz') as archive:
        archive.extractall(source, filter='data')
    run('01-venv', [sys.executable, '-m', 'venv', out / 'venv'])
    py = out / 'venv/bin/python'
    run('02-install-lock', [py, '-m', 'pip', 'install', '--no-index', '--find-links',
                            ROOT / 'environment/wheels', '--require-hashes', '-r',
                            ROOT / 'environment/requirements.lock'])
    run('03-build-wheel', [py, '-m', 'build', '--wheel', '--no-isolation',
                           '--outdir', out / 'dist', source])
    wheel = next((out / 'dist').glob('*.whl'))
    run('04-install-wheel', [py, '-m', 'pip', 'install', '--no-index', '--no-deps', wheel])
    run('05-upstream-tests', [py, '-m', 'pytest', '-o', 'addopts=', '-q', '-ra',
                              '--hypothesis-seed=20261025', '--junitxml=' + str(out / 'upstream-tests.xml')], cwd=source)
    run('06-start-version', [py, '-m', 'todoman', '--version'])
    run('07-study-probes', [py, ROOT / 'scripts/probe_workflow.py', '--output', out / 'workflow'])
    run('08-dependency-check', [py, '-m', 'pip', 'check'])
    counts = test_counts(out / 'upstream-tests.xml')
    probes = json.loads((out / 'workflow/results.json').read_text())
    summary = {'upstream_commit': meta['commit'], 'upstream_source_sha256': meta['source_archive_sha256'],
               'python': platform.python_version(), 'platform': platform.platform(),
               'runtime_differs_from_recorded_python': mismatch,
               'upstream_tests': counts, 'study_checks_passed': probes['checks_passed'],
               'built_wheel_sha256': sha256(wheel), 'offline_install': True,
               'seed': 20261025, 'note': 'Skips and expected failures are retained; characterization checks include missing safeguards.'}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
