"""Tie-aware local recognition metrics, not temporal detection mAP."""
import numpy as np

def average_precision(y, score):
    y=np.asarray(y);score=np.asarray(score)
    if y.ndim!=1 or y.shape!=score.shape or len(y)==0:raise ValueError('Nonempty equal vectors required')
    if not np.isin(y,[0,1]).all() or not np.isfinite(score).all():raise ValueError('Binary labels and finite scores required')
    y=y.astype(np.int64)
    if y.sum()==0:return 0.0  # Historical macro-52 convention; never silently drop absent classes.
    order=np.argsort(-score,kind='stable');s=score[order];positives=np.cumsum(y[order])
    ends=np.r_[np.flatnonzero(s[:-1]!=s[1:]),len(y)-1]
    recall=positives[ends]/y.sum();precision=positives[ends]/(ends+1)
    return float(np.sum(np.diff(np.r_[0.,recall])*precision))

def recognition_metrics(y, scores, target):
    y=np.asarray(y);scores=np.asarray(scores);target=np.asarray(target)
    if y.ndim!=2 or y.shape!=scores.shape or len(y)==0:raise ValueError('Expected nonempty [N,C] arrays')
    if target.shape!=(len(y),) or target.dtype.kind not in 'iu' or np.any(target<0) or np.any(target>=y.shape[1]):raise ValueError('Invalid targets')
    if not np.all(y[np.arange(len(y)),target]==1):raise ValueError('Target must be a positive local label')
    ap=[average_precision(y[:,c],scores[:,c]) for c in range(y.shape[1])]
    t=scores[np.arange(len(y)),target,None];greater=(scores>t).sum(1);equal=(scores==t).sum(1)
    rank=greater+(equal+1)/2
    return {'local_map':float(np.mean(ap)),'target_mrr':float(np.mean(1/rank)),
            'strict_target_top1':float(np.mean((greater==0)&(equal==1))), 'per_class_ap':ap}
