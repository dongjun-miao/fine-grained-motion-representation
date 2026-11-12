"""Filename-prefix grouping; never assume these are verified participant identities."""
import hashlib
from pathlib import Path
import numpy as np


def group_key(path):
    return Path(path).stem.split('_')[0]


def fold_for(path):
    return int(hashlib.sha256(group_key(path).encode()).hexdigest(),16)%5


def folds_for(records):
    indices = np.array([i for i,r in enumerate(records) if r['split']=='train'])
    folds = np.array([fold_for(records[i]['path']) for i in indices])
    if set(folds)!=set(range(5)):
        raise ValueError('Require all five prefix folds')
    return indices,folds


def check_partition(records,fit,evaluation):
    if set(fit)&set(evaluation):
        raise ValueError('Clip overlap')
    if {group_key(records[i]['path']) for i in fit}&{group_key(records[i]['path']) for i in evaluation}:
        raise ValueError('Filename prefix overlap')
    if any(records[i]['split']!='train' for i in np.r_[fit,evaluation]):
        raise ValueError('Cross-validation uses original training data only')
