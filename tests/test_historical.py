"""Synthetic checks of the unchanged historical utilities actually distributed."""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/historical'))
import numpy as np
from baseline_metrics import classification_metrics
from group_folds import check_partition,fold_for
from evidence_sampling import selection_indices

class Historical(unittest.TestCase):
 def test_classification(self):
  m=classification_metrics([0,1],[[3,0],[0,3]],2)
  self.assertEqual(m['macro_f1'],1.)
 def test_group_identity(self):
  self.assertEqual(fold_for('synthetic_01.mp4'),fold_for('synthetic_02.mp4'))
  records=[{'split':'train','path':'synthetic_01.mp4'},{'split':'train','path':'synthetic_02.mp4'}]
  with self.assertRaises(ValueError):check_partition(records,[0],[1])
 def test_fixed_budget_selection(self):
  scores=np.arange(16).reshape(2,8)
  for method in ['uniform4','motion_top4','motion_diverse4','random4','random_diverse4']:
   a=selection_indices(method,scores,['synthetic_a','synthetic_b'])
   self.assertEqual(a.shape,(2,4));self.assertTrue((np.diff(a,axis=1)>0).all())
   np.testing.assert_array_equal(a,selection_indices(method,scores,['synthetic_a','synthetic_b']))
