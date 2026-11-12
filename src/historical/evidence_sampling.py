"""Coarse flow intensity interpolation and label-free fixed-cardinality selectors."""
import hashlib
import json
import numpy as np


def candidate_motion_scores(motion,pair_indices,rgb_indices):
    motion,pair_indices,rgb_indices = np.asarray(motion),np.asarray(pair_indices),np.asarray(rgb_indices)
    if motion.shape[1:]!=(832,) or pair_indices.shape!=(len(motion),16) or rgb_indices.shape!=(len(motion),8):
        raise ValueError('Expected aligned motion832, pairs16, RGB8')
    if not np.isfinite(motion).all() or np.any(np.diff(pair_indices,axis=1)<=0) or np.any(np.diff(rgb_indices,axis=1)<=0):
        raise ValueError('Finite features and strictly chronological candidate indices required')
    energy = motion[:,64:].reshape(-1,4,16,12)[:,:,:,2].mean(2)
    times = pair_indices.reshape(-1,4,4).mean(2)
    scores = np.stack([np.interp(t,x,y) for t,x,y in zip(rgb_indices,times,energy)]).astype(np.float32)
    if np.any(scores<0) or not np.isfinite(scores).all():
        raise ValueError('Motion energy must be finite and nonnegative')
    return scores,energy


def selection_indices(method,scores,paths,realization=0,selection_seed=20261020):
    scores = np.asarray(scores)
    if scores.shape!=(len(paths),8) or not np.isfinite(scores).all():
        raise ValueError('Expected eight finite candidate scores per path')
    if method=='all8':
        return np.tile(np.arange(8),(len(paths),1))
    if method=='uniform4':
        return np.tile(np.linspace(0,7,4).astype(int),(len(paths),1))
    if method in {'motion_top4','motion_low4'}:
        ranked = np.argsort(-scores if method=='motion_top4' else scores,axis=1,kind='stable')
        return np.sort(ranked[:,:4],axis=1)
    if method=='motion_diverse4':
        return scores.reshape(-1,4,2).argmax(2)+2*np.arange(4)[None,:]
    if method in {'random4','random_diverse4'}:
        selected = []
        for path in paths:
            seed = int.from_bytes(hashlib.sha256(json.dumps([method,realization,str(path),selection_seed],separators=(',',':')).encode()).digest()[:8],'little')
            rng = np.random.default_rng(seed)
            row = np.sort(rng.choice(8,4,replace=False)) if method=='random4' else 2*np.arange(4)+rng.integers(0,2,4)
            selected.append(row)
        return np.asarray(selected,np.int64)
    raise ValueError(method)


def pool_selected(features,indices,chunk=256):
    if features.shape[0]!=len(indices) or features.shape[1:]!=(9,512):
        raise ValueError('Expected aligned [N,9,512] frozen cache')
    if indices.ndim!=2 or indices.shape[1] not in {4,8} or np.any(indices<0) or np.any(indices>7) or np.any(np.diff(indices,axis=1)<=0):
        raise ValueError('Selection must be chronological distinct candidate slots0:8')
    result = np.empty((len(features),512),np.float32)
    for start in range(0,len(features),chunk):
        block = np.asarray(features[start:start+chunk],np.float32)
        choices = indices[start:start+len(block)]
        result[start:start+len(block)] = block[np.arange(len(block))[:,None],choices].mean(1)
    return result
