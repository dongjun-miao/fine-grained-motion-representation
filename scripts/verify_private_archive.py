"""Optional authorized read-only re-scoring of historical predictions. Never exports labels."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from fgmotion.metrics import recognition_metrics

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',required=True,type=Path);a=p.parse_args()
 provenance=json.loads((ROOT/'docs/evidence/provenance.json').read_text());rows=json.loads((ROOT/'docs/evidence/verified_aggregates.json').read_text())
 lp=a.archive/'experiments/local_recognition_probe_v1/labels.npz'
 if hashlib.sha256(lp.read_bytes()).hexdigest()!=provenance['label_source_sha256']:raise ValueError('Label identity mismatch')
 with np.load(lp,allow_pickle=False) as d:y=d['local'];target=d['target'];roles=d['roles']
 n=0
 for src in provenance['inputs']:
  path=a.archive/src['source']
  if hashlib.sha256(path.read_bytes()).hexdigest()!=src['sha256']:raise ValueError('Prediction identity mismatch')
  seed=42 if 'seed42' in src['source'] else 1601
  appearance='method_development_v1' in src['source']
  model=('B0' if 'B0_seed' in src['source'] else ('B1' if '/B1/' in src['source'] else 'B2')) if appearance else 'Base'
  views=['clean','train_photo','stress_photo'] if appearance else ['uniform16','gt16','gt_shuffle16','static_gt_selected']
  with np.load(path,allow_pickle=False) as d:scores=d['style_logits' if appearance else 'logits']
  for part in ['fit','inner','val']:
   ii=np.flatnonzero(roles==part)
   for j,view in enumerate(views):
    got=recognition_metrics(y[ii],scores[ii,j],target[ii]);ref=next(r for r in rows if r['model']==model and r['seed']==seed and r['partition']==part and r['view']==view)
    if abs(got['local_map']-ref['local_map'])>1e-12 or abs(got['target_mrr']-ref['target_mrr'])>1e-12:raise ValueError('Metric mismatch')
    n+=1
 print(json.dumps({'passed':True,'metric_rows':n,'read_only':True,'private_data_exported':False}))
if __name__=='__main__':main()
