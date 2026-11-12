"""Evaluate your authorized local arrays; does not download or publish data."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from fgmotion.metrics import recognition_metrics
p=argparse.ArgumentParser();p.add_argument('npz',type=Path);a=p.parse_args()
with np.load(a.npz,allow_pickle=False) as d:
    if 'partition' not in d or str(d['partition']) not in ['fit','inner','val']:raise ValueError('Explicit fit/inner/val required; test forbidden')
    print(json.dumps(recognition_metrics(d['labels'],d['scores'],d['target']),indent=2))
