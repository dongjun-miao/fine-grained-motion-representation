"""Streaming adjacent-frame motion descriptors; no labels enter extraction."""
import cv2
import numpy as np

FLOW_DIM = 768
DIFF_DIM = 64


def gray_small(frame, size=96):
    h,w = frame.shape[:2]
    scale = size/max(h,w)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray,(max(4,round(w*scale)),max(4,round(h*scale))),interpolation=cv2.INTER_AREA)


def pair_descriptor(previous, current):
    if previous.shape != current.shape or previous.ndim != 2 or min(previous.shape)<4:
        raise ValueError('Expected matching grayscale images, at least 4x4')
    delta = cv2.absdiff(previous,current).astype(np.float32)/255
    # Explicit repeated-frame control: avoid numerical solver noise for identical input.
    flow = np.zeros((*previous.shape,2),np.float32) if np.array_equal(previous,current) else cv2.calcOpticalFlowFarneback(previous,current,None,.5,3,15,3,5,1.2,0)
    magnitude = np.linalg.norm(flow,axis=2)
    angle = np.mod(np.arctan2(flow[:,:,1],flow[:,:,0]),2*np.pi)
    bins = np.minimum((angle*(8/(2*np.pi))).astype(np.int32),7)
    diff, features = [], []
    yedges = np.linspace(0,len(previous),5,dtype=int)
    xedges = np.linspace(0,previous.shape[1],5,dtype=int)
    for y0,y1 in zip(yedges[:-1],yedges[1:]):
        for x0,x1 in zip(xedges[:-1],xedges[1:]):
            region = np.s_[y0:y1,x0:x1]
            mag = magnitude[region]
            vector = flow[region]
            hist = np.bincount(bins[region].ravel(),weights=mag.ravel(),minlength=8)/mag.size
            diff.append(delta[region].mean())
            features.extend([vector[:,:,0].mean(),vector[:,:,1].mean(),mag.mean(),mag.std(),*hist])
    return np.asarray(diff,np.float32),np.asarray(features,np.float32)


def aggregate_pairs(differences,flows):
    differences,flows = np.asarray(differences),np.asarray(flows)
    if differences.shape!=(16,16) or flows.shape!=(16,192):
        raise ValueError('Expected 16 pair descriptors')
    return np.concatenate([differences.reshape(4,4,16).mean(1).ravel(),flows.reshape(4,4,192).mean(1).ravel()]).astype(np.float32)


def extract_video(path):
    cv2.setNumThreads(1)
    params = [cv2.CAP_PROP_N_THREADS,1] if hasattr(cv2,'CAP_PROP_N_THREADS') else []
    cap = cv2.VideoCapture(str(path),cv2.CAP_FFMPEG,params)
    if not cap.isOpened():
        raise ValueError(f'Cannot open {path}')
    try:
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        if total<17 or not np.isfinite(fps) or fps<=0:
            raise ValueError(f'Invalid frame count/FPS: {path}')
        targets = np.rint(np.linspace(1,total-1,16)).astype(np.int64)
        needed = set(targets.tolist()) | set((targets-1).tolist())
        pending, diff, flow = {}, [], []
        positions = {int(v):i for i,v in enumerate(targets)}
        for index in range(total):
            if not cap.grab():
                raise ValueError(f'Early EOF {index}/{total}: {path}')
            if index in needed:
                ok,frame = cap.retrieve()
                if not ok:
                    raise ValueError(f'Cannot decode frame {index}: {path}')
                pending[index] = gray_small(frame)
            if index in positions:
                d,f = pair_descriptor(pending[index-1],pending[index])
                diff.append(d)
                flow.append(f)
            # Retain at most the previous/current reduced frames, never the video.
            for key in list(pending):
                if key<index:
                    del pending[key]
        values = aggregate_pairs(diff,flow)
        if not np.isfinite(values).all():
            raise ValueError(f'Nonfinite motion descriptor: {path}')
        energy = float(np.mean(np.asarray(flow)[:,2::12]))
        return values,targets,fps,total,energy
    finally:
        cap.release()
