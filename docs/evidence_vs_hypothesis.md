# Evidence versus hypothesis

Classification is claim-specific. VERIFIED does not mean retrained, independently tested, legally cleared for data redistribution, or universally true.

| Status | Meaning | Application |
|---|---|---|
| VERIFIED | Directly checked in this packaging task against local artifacts/predictions | 78 local mAP/MRR aggregates; corresponding source-prediction hashes; selected historical text hashes; synthetic utility tests |
| HISTORICAL BUT UNREPRODUCED | Existing completion records/results inspected, but the full empirical pipeline was not replayed for this release | Stages 1–16, normalization closure, Local Delta, last-block adaptation, detection mAP, domain AUC, historical bootstrap intervals |
| PROPOSED | Research direction or mechanism without validated implementation/effect | Appearance-robust motion evidence, reliable temporal grounding, server-scale Video-LLM evaluation |
| UNSUPPORTED | Evidence does not justify the statement | SOTA, proven weak-motion preservation, verified subject independence, causal camera/identity attribution from domain AUC, a successful original M1 |

## Negative findings that must survive editing

Local Delta's early favorable subset result did not survive the full five-fold comparison. More temporal queries did not automatically improve detection. A stronger continuous head improved fitting without resolving the validation gap. A larger encoder improved target ranking but did not establish broad class-level AP gains. Standard augmentation/consistency did not beat the unaugmented local probe on clean validation mAP in the displayed two seeds. No omitted failed branch is silently renamed as the proposed method.

## Metric and scope boundaries

Local mAP averages 52 binary AP values, including AP=0 for absent-positive classes. Target MRR ranks one selected positive class; concurrent valid actions make this different from complete multi-label accuracy. MA-52 Macro-F1, MMA-52 detection mAP, and GT-local recognition AP must not share a ranking table. GT-local improvement is an oracle input comparison. Two seeds share videos and do not create independent test populations. Historical video-bootstrap intervals condition on fixed checkpoints; no subject-cluster inference is justified.

The frozen candidate has a constructive static solution with nonzero temporal variance and zero evidence-consistency loss. This disproves the claim that the objective alone guarantees motion use. It neither proves all appearance-robust learning impossible nor supplies a natural-video failure score for an untrained method.
