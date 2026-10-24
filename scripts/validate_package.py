#!/usr/bin/env python3
"""Read-only package checks. No network, installation, or service writes."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

SKILLS = {'pm-define', 'pm-prototype', 'pm-deliver'}

def validate(root):
    root = Path(root).resolve()
    errors = []
    def load(rel):
        try:
            return json.loads((root / rel).read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            errors.append(f'invalid JSON {rel}: {type(exc).__name__}')
            return {}
    a = load('.codex-plugin/plugin.json')
    b = load('.claude-plugin/plugin.json')
    for key in ('name', 'version', 'skills', 'license'):
        if a.get(key) != b.get(key):
            errors.append(f'manifest mismatch: {key}')
    if a.get('name') != 'georgepm' or a.get('skills') != './skills/':
        errors.append('invalid plugin identity/skills path')
    if not re.fullmatch(r'\d+\.\d+\.\d+', a.get('version', '')):
        errors.append('invalid version')
    if a.get('license') != 'MIT' or not (root / 'LICENSE').is_file():
        errors.append('missing/inconsistent license')
    for rel in ('.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
        m = load(rel)
        plugins = m.get('plugins', [])
        if m.get('name') != 'georgepm-marketplace' or len(plugins) != 1:
            errors.append(f'invalid marketplace: {rel}')
        elif plugins[0].get('name') != 'georgepm':
            errors.append(f'invalid marketplace identity: {rel}')
        else:
            source = plugins[0].get('source')
            if source != './' and source != {'source':'local', 'path':'./'}:
                errors.append(f'invalid marketplace path: {rel}')
    found = {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')}
    if found != SKILLS:
        errors.append(f'invalid skill set: {sorted(found)}')
    for name in SKILLS:
        path = root / 'skills' / name / 'SKILL.md'
        if not path.is_file():
            errors.append(f'missing skill: {name}')
            continue
        text = path.read_text(encoding='utf-8')
        front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not front or f'name: {name}\n' not in front.group(1) + '\n' or not re.search(r'^description: .+', front.group(1), re.M):
            errors.append(f'invalid skill frontmatter: {name}')
        ui = path.parent / 'agents/openai.yaml'
        if not ui.is_file() or '$' + name not in ui.read_text(encoding='utf-8'):
            errors.append(f'missing UI invocation metadata: {name}')
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(p in {'.git', '.test-work', '__pycache__'} for p in rel.parts):
            continue
        if path.is_symlink():
            errors.append(f'symlink: {rel}')
            continue
        if not path.is_file():
            continue
        if path.name.startswith(('.env', 'private_')) or path.name in {'auth.json', '.DS_Store'} or path.suffix == '.jsonl':
            errors.append(f'forbidden file: {rel}')
        if path.suffix not in {'.md', '.json', '.yaml', '.py'}:
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'non UTF-8 source: {rel}')
            continue
        if re.search(r'/(?:Users|home)/[^/\s"\')]+|/Volumes/\d+/', content):
            errors.append(f'personal absolute path: {rel}')
        if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----', content):
            errors.append(f'possible secret: {rel}')
        if path.suffix != '.md':
            continue
        # Only inline Markdown file links; not a full Markdown parser or URL checker.
        content = re.sub(r'```.*?```', '', content, flags=re.S)
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            target = raw.strip().strip('<>')
            parsed = urlparse(target)
            if parsed.scheme or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(root):
                errors.append(f'outside package: {rel} -> {target}')
            elif not dest.exists():
                errors.append(f'missing link: {rel} -> {target}')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    print(json.dumps({'result':'FAIL' if errors else 'PASS','errors':errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
