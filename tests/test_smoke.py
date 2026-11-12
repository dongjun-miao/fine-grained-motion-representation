"""SYNTHETIC engineering fixtures only; no dataset performance evidence."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from fgmotion.metrics import average_precision,recognition_metrics
from fgmotion.protocol import local_labels,fit_scaler,assert_disjoint,prefix_fold

class Smoke(unittest.TestCase):
    def test_tied_ap(self):
        self.assertEqual(average_precision([1,0],[0,0]),.5)
        self.assertEqual(average_precision([0,0],[3,2]),0)
        self.assertAlmostEqual(average_precision([1,0,1],[3,2,1]),5/6)
    def test_rank_ties(self):
        m=recognition_metrics([[1,0,1]],[[1,1,1]],np.array([0]))
        self.assertEqual(m['target_mrr'],.5);self.assertEqual(m['strict_target_top1'],0)
    def test_overlap_and_endpoint(self):
        a=[(0,2,5),(1,4,8),(0,10,11)]
        np.testing.assert_array_equal(local_labels(a,[4],2),[1,1])
        np.testing.assert_array_equal(local_labels(a,[5],2),[0,1])
    def test_fit_only(self):
        x=np.array([[0,0],[2,0],[999,999]])
        m,s=fit_scaler(x,['fit','fit','val']);np.testing.assert_array_equal(m,[1,0]);np.testing.assert_array_equal(s,[1,1])
        with self.assertRaises(ValueError):fit_scaler(x,['fit','inner','test'])
    def test_group_separation(self):
        assert_disjoint([0],[1],['a'],['b'])
        with self.assertRaises(ValueError):assert_disjoint([0],[1],['a'],['a'])
        self.assertEqual(prefix_fold('synthetic'),prefix_fold('synthetic'))
    def test_static_consistency_counterexample(self):
        for seed in [42,1601]:
            rng=np.random.default_rng(seed);a=rng.normal(size=(20,1,12));p=rng.normal(size=(1,8,12));p-=p.mean(1,keepdims=True)
            z=a+p
            self.assertGreater(z.var(1).mean(),0)
            np.testing.assert_allclose(z.mean(1),a[:,0],atol=1e-14)
            self.assertEqual(float(np.square(z-z).mean()),0.)
    def test_reject_invalid(self):
        with self.assertRaises(ValueError):average_precision([1],[float('nan')])
        with self.assertRaises(ValueError):recognition_metrics([[0,1]],[[0,1]],np.array([0]))

if __name__=='__main__':unittest.main()
