"""Input contracts; prefix grouping does not identify participants."""
import hashlib
import numpy as np

def prefix_fold(prefix):
    return int(hashlib.sha256(prefix.encode()).hexdigest(),16)%5

def assert_disjoint(fit_ids, held_ids, fit_groups, held_groups):
    if set(fit_ids)&set(held_ids):raise ValueError('Sample overlap')
    if set(fit_groups)&set(held_groups):raise ValueError('Group overlap')

def local_labels(intervals, frame_indices, classes):
    """intervals=(class,start_frame,end_frame), half-open; preserve overlapping classes."""
    frames=np.asarray(frame_indices);y=np.zeros(classes,dtype=np.int64)
    for c,start,end in intervals:
        if not 0<=c<classes or not start<end:raise ValueError('Invalid interval')
        if np.any((frames>=start)&(frames<end)):y[c]=1
    return y

def fit_scaler(features, roles):
    x=np.asarray(features);roles=np.asarray(roles)
    if x.ndim!=2 or len(x)!=len(roles) or not np.isfinite(x).all():raise ValueError('Invalid feature matrix')
    if not set(roles)<=set(['fit','inner','val']) or not np.any(roles=='fit'):raise ValueError('Fit required; test forbidden')
    mean=x[roles=='fit'].astype('float64').mean(0).astype('float32')
    scale=x[roles=='fit'].astype('float64').std(0).astype('float32');scale[scale<1e-6]=1
    return mean,scale
