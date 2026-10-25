"""Profile selected upstream calls while executing the real module entry point."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import runpy
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--trace', type=Path, required=True)
parser.add_argument('arguments', nargs=argparse.REMAINDER)
args = parser.parse_args()
arguments = args.arguments[1:] if args.arguments[:1] == ['--'] else args.arguments
names = {'cli', 'load_config', '_validate_date_param', 'parse_datetime',
         '_parse_datetime_naive', 'edit', 'todo', '_todo_from_db', 'save',
         'write', '_write_existing', 'serialize', 'normalize_datetime',
         'atomic_write', 'expire_file', 'add_file', 'add_vtodo',
         'save_to_disk', 'detailed'}
events = []

def profile(frame, event, arg):
    if event != 'call':
        return
    module = frame.f_globals.get('__name__', '')
    if module.startswith('todoman.') and frame.f_code.co_name in names:
        filename = 'todoman/' + Path(frame.f_code.co_filename).name
        events.append({'index': len(events) + 1, 'module': module,
                       'function': frame.f_code.co_name, 'source': filename,
                       'first_line': frame.f_code.co_firstlineno})

sys.argv = ['todoman', *arguments]
sys.setprofile(profile)
try:
    runpy.run_module('todoman', run_name='__main__')
finally:
    sys.setprofile(None)
    args.trace.parent.mkdir(parents=True, exist_ok=True)
    args.trace.write_text(json.dumps(events, indent=2) + '\n')
