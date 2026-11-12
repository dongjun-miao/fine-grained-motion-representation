# Research decisions and unresolved questions

The study moved from hand-crafted motion baselines to stronger representations and falsifiable mechanism checks. It did not establish a new learned motion module.

**Local Delta:** freeze the negative branch. Its full-fold evidence did not reproduce the early favorable subset comparison. This is not a proof that all temporal differences are useless.

**Detection:** a small class-aware continuous-boundary head did not eliminate held-out development failure at fixed sparse evidence. OpenTAD/ActionFormer was audited, not fully reproduced. The mature-head confound is therefore reduced only for the tested head, not universally eliminated.

**Representation versus generalization:** stronger frozen representations improve target ranking, but GT-local oracle inputs do not close the partition gap. This supports further study without uniquely choosing observation loss, representation insufficiency or distribution shift as the cause. Domain AUC is not source identity.

**TA-TAC candidate:** task-linked aligned temporal attribution consistency has a static shortcut counterexample. With frozen features and a linear head its evidence penalty is a task-weighted quadratic form. It is not algebraically identical to prediction consistency, yet a different grouping is insufficient evidence of originality. Natural-video M1 training was stopped before scores. The implemented B1/B2 results are ordinary reference methods.

Prior-art review included MMAD/DSTA, VideoMAE, MG-FMs, VideoZoomer, SURGE, CARL, ASCNet, VideoDG, StillMix and Logit Attribution Matching. Their roles differ: detection, pretrained encoding, motion guidance, observation/token selection, and representation/attribution invariance. The closest obstacle to the candidate is existing temporal augmented-view alignment and class-linked attribution matching—not an assertion that those papers solve natural weak-motion preservation. See [CARL](https://arxiv.org/abs/2203.14957) and [LAM](https://proceedings.mlr.press/v244/gao24a.html). Recent-paper coverage is a historical review, not an exhaustive novelty guarantee.

**PROPOSED next question:** when is an appearance transformation admissible for a fine-grained action, and can invariance be enforced without attenuating task-discriminative changes? A useful answer needs independent evidence of retained/disrupted actions and an explicit distinction from augmentation policy or attribution regularization. No new experiments were started for this release. Human evidence annotation, independent datasets and verified source metadata remain unavailable or incomplete.
