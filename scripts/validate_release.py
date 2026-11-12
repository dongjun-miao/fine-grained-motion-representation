"""Portable offline public-package checks. No data or training access."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'.md','.py','.json','.txt','.png','.cff',''}

def main():
 files=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ['__pycache__','.git','.venv'])]
 bad=[]
 for p in files:
  rel=p.relative_to(ROOT).as_posix()
  if p.suffix not in ALLOWED or p.is_symlink():bad.append(rel+': forbidden file type')
  if p.suffix in ['.md','.py','.json','.txt','.cff','']:
   t=p.read_text(encoding='utf-8')
   # Split literals so this scanner does not match its own patterns.
   for pattern in [r'[A-Za-z]:[\\/]'+'Users'+r'[\\/]',r'AKIA'+'[0-9A-Z]{16}',r'ghp_'+'[A-Za-z0-9]{30,}',r'-----BEGIN '+'PRIVATE KEY-----']:
    if re.search(pattern,t):bad.append(rel+': private path/credential pattern')
   if p.suffix=='.md':
    for target in re.findall(r'\]\(([^)]+)\)',t):
     if '://' not in target and not target.startswith('#') and not (p.parent/target.split('#')[0]).exists():bad.append(rel+': broken link '+target)
 manifest=ROOT/'MANIFEST.json'
 if manifest.exists():
  for name,h in json.loads(manifest.read_text())['files'].items():
   p=ROOT/name
   if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h:bad.append(name+': manifest mismatch')
 assert not bad,'\n'.join(bad)
 print(json.dumps({'passed':True,'files_checked':len(files),'forbidden_files':0,'broken_local_links':0,'scope':'Heuristic file/path/secret scan and manifest, not a legal or exhaustive security certification'}))
if __name__=='__main__':main()
