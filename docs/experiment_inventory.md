# Experiment inventory

This is a completion/artifact audit, not a claim to have retrained all experiments. All numerical figures in this release come only from the separate VERIFIED aggregate file. Stage descriptions below summarize existing reports; numerical historical rankings are intentionally not reprinted without current metric replay.

| Stage | Investigation | Release evidence status |
|---|---|---|
| 1 | Data/annotation intake and isolated synthetic demo | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 2 | Frozen RGB recognition | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 3 | Longer linear/MLP/GRU probes | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 4 | Adjacent differences and optical-flow features | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 5 | RGB–motion fusion | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 6 | Prefix development stress evaluation | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 7 | Sparse evidence sampling | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 8 | Temporal means/order/shuffle | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 9 | Coarse region weighting | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 10 | Pixel/person-relative region audit | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 11 | Five-fold grouped OOF | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 12 | Spatial aggregation controls | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 13 | Guard-region controls | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 14 | Matched-capacity motion comparisons | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 15 | Location/scale factorial controls | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |
| 16 | Temporal-order and normalization motivation | HISTORICAL BUT UNREPRODUCED: report/artifact audit; no new training |

## Later work

| Work | Completion / scope | Release status |
|---|---|---|
| WP1 / Stage17 | Completed normalization × shuffle closure; old results reused, not counted as new runs | HISTORICAL BUT UNREPRODUCED |
| WP2 | Frozen VideoMAE sampling baselines | HISTORICAL BUT UNREPRODUCED |
| WP3 Local Delta | Five-fold negative branch frozen | HISTORICAL BUT UNREPRODUCED |
| Full last block | Target adaptation completed; retained generalization gap | HISTORICAL BUT UNREPRODUCED |
| MMA-52 v1 / resolution | Fixed detector/query studies completed, negative findings retained | HISTORICAL BUT UNREPRODUCED |
| Overnight Oct27 / detection v2 | Evaluation/observation audit and small continuous head; mature ActionFormer not trained | HISTORICAL BUT UNREPRODUCED |
| Representation/generalization Oct27 | Distribution and fixed local evidence studies completed | HISTORICAL BUT UNREPRODUCED except reused latest Small predictions explicitly rescored |
| Local recognition / Overnight Oct28 | Local probes and stronger frozen Base completed | VERIFIED only for the 24 Base metric rows and reused B0 rows re-scored here |
| Method development v1 | Four standard B1/B2 probes completed, two seeds; M1 rejected before natural training | VERIFIED for 54 B0/B1/B2 metric rows; candidate static check synthetic only |
| Evidence annotation / Video-LLM / independent dataset validation | No completed empirical result established | PROPOSED, not evaluated |

## Machine-readable coverage

`evidence/artifact_inventory.json` enumerates every experiment directory with checkpoint/prediction/log counts and selected completion-marker fields. A checkpoint file alone is not evidence that its metric is correct. `source_review_manifest.json` lists all scanned first-party source, configuration, test and Markdown documents with hashes and function definitions. `evidence/provenance.json` records current checks. Binary caches/weights were not exhaustively rehashed; all training runs were not replayed. A full archive text scan is not a line-by-line correctness certification.

No private participant/sample lists or restricted labels are reproduced. Historical “source” terminology is interpreted as an unverified grouping proxy unless official metadata actually supports it.
