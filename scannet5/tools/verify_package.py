"""Verify packaged file sizes and SHA-256 hashes. Python standard library only."""
import argparse, hashlib
from pathlib import Path

def verify(root):
    expected={};failures=[]
    for line in (root/'SHA256SUMS.txt').read_text().splitlines():
        digest,rel=line.split('  ',1);expected[rel]=digest
    for n,(rel,digest) in enumerate(expected.items(),1):
        path=root/rel
        if not path.is_file():failures.append((rel,'missing'));continue
        h=hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
        if h.hexdigest()!=digest:failures.append((rel,'sha256 mismatch'))
        if n%3000==0:print(f'Checked {n}/{len(expected)} files',flush=True)
    extra=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in expected and p.name!='SHA256SUMS.txt')
    print(f'Checked {len(expected)} files; failures: {len(failures)}; unlisted files: {len(extra)}')
    for row in failures:print(*row)
    for row in extra:print('Unlisted:',row)
    return 1 if failures or extra else 0
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();raise SystemExit(verify(args.root))
