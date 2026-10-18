"""Minimal, transparent coding harness using the installed Codex CLI.

Requires Codex CLI installed and authenticated separately. This script does
not itself implement an LLM; it orchestrates the agent, tests, and PR steps.
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent

def run(args, *, check=True):
    print('+', ' '.join(args), flush=True)
    return subprocess.run(args, cwd=ROOT, check=check)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ticket', nargs='?', default='ORDER-101')
    parser.add_argument('--create-pr', action='store_true', help='Push branch and open draft PR (requires gh auth)')
    args = parser.parse_args()
    ticket = ROOT / 'tickets' / f'{args.ticket}.md'
    if not ticket.is_file():
        sys.exit(f'Ticket not found: {ticket}')
    if not shutil.which('codex'):
        sys.exit('Install and authenticate Codex CLI first; see README.md')
    if not (ROOT / '.git').exists():
        sys.exit('Initialize Git and commit baseline first; see README.md')
    if subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip():
        sys.exit('Working tree must be clean before running harness')
    branch = 'feature/' + args.ticket.lower()
    run(['git', 'switch', '-c', branch])
    prompt = f'''Implement ticket {args.ticket} from tickets/{args.ticket}.md.
First inspect AGENTS.md, app/, and tests/. Understand existing behavior.
Write a short plan to PLAN.md, then implement the smallest change and add tests.
Do not commit, push, open a PR, or merge. Do not modify the ticket.
Run python -m unittest discover -s tests -v and report results.
'''
    run(['codex', 'exec', '--sandbox', 'workspace-write', prompt])
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT)
    if result.returncode:
        sys.exit('Tests failed. Review changes; no PR created.')
    print('\nTests passed. Review `git diff` before committing.')
    if args.create_pr:
        if not shutil.which('gh'):
            sys.exit('GitHub CLI (gh) required to create PR')
        run(['git', 'add', 'app', 'tests', 'PLAN.md'])
        run(['git', 'commit', '-m', f'Implement {args.ticket}'])
        run(['git', 'push', '-u', 'origin', branch])
        run(['gh', 'pr', 'create', '--draft', '--title', f'{args.ticket}: Cancel an order', '--body', f'Implements {args.ticket}. Automated tests passed. Human review required.'])
    else:
        print('PR not created. Use --create-pr after configuring GitHub and reviewing the generated changes.')

if __name__ == '__main__':
    main()
