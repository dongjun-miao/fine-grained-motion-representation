# Reproducibility boundaries and instructions

## Three levels of reproduction

1. **Public, self-contained:** synthetic CPU unit tests, aggregate figure regeneration, package hash verification. No data rights or GPU needed. Synthetic tests are not empirical performance evidence.
2. **Authorized local metric replay:** `scripts/evaluate_local.py` reads your own NPZ containing `labels` [N,C] binary, `scores` [N,C] finite logits, `target` [N] integer positive class, `partition` scalar string fit/inner/val. No object arrays, media, IDs or test labels. Local AP ties are grouped at score thresholds; no-positive AP is zero; MRR uses average rank for tied classes. This is recognition, not detection evaluation.
3. **Historical full experiments:** require the original private archive, legally obtained videos/labels, original splits/caches and checkpoints. Those are deliberately not distributed. The portfolio does not promise bitwise training reproduction from the public ZIP alone.

The package audit recomputed 78 selected local mAP/MRR aggregates from original saved predictions and checked their hashes. The public aggregate JSON supports figure regeneration, not independent reconstruction of AP without the restricted labels and scores. No new training was performed for packaging.

An authorized custodian of the unchanged original archive can repeat these exact checks with `python scripts/verify_private_archive.py --archive /path/to/private/archive`. This reads only saved labels/predictions, enforces their hashes and prints an aggregate pass/fail result. It does not train, download or export restricted records.

## Primary historical entry points (not bundled launch commands)

| Study | Original archive entry points | Main dependency/data needs |
|---|---|---|
| Stages 2–3 | `scripts/run_stage2.py`, `run_stage3.py`, `train_baselines.py` | MA-52; frozen RGB cache; torch/torchvision |
| Stages 4–6 | `run_stages4_6.py`, `extract_motion.py` | OpenCV Farneback and frame differences; RGB cache |
| Stages 7–16 | `run_stage7.py` … `run_stage16.py`; `train_temporal_order.py` | private motion/region caches; NumPy/torch/OpenCV |
| Normalization × shuffle | `train_normalization_closure.py`, `verify_normalization_closure.py` | fixed five-prefix folds, fit-only statistics |
| VideoMAE / Local Delta | `extract_videomae_small.py`, `train_videomae_probe.py`, `run_wp3_partial.py` | authorized VideoMAE source/weights, timm, torch CUDA |
| Full last block | `run_fullblock_v1.py`, `verify_fullblock_v1.py` | original frozen protocol and checkpoints |
| MMA-52 detection | `run_mma52_v1.py`, `detection_v2_train.py`, `detection_v2_evaluate.py` | overlapping temporal labels, fixed cached tokens |
| Resolution / evaluation audit | `mma52_resolution_driver.py`, `overnight27_driver_v2.py` | original cache identities; no inferred dense observation |
| Distribution / local evidence | `rg27_distribution_v2.py`, `rg27_encode_v2.py`, `local_probe_v1.py` | Fit/Inner/Val manifests and GT-local labels |
| Strong frozen encoder | `strong28_encode.py`, `strong28_probe.py` | Small/Base K400 weights and same 16 input frames |
| Method eligibility / B1/B2 | `methodv1_structure.py`, `methodv1_encode.py`, `methodv1_probe.py`, `methodv1_audit.py` | fixed appearance views, frozen features, CPU probes |

Source identities and discovered function definitions are in `source_review_manifest.json`. The release includes a small unchanged selection of historical utilities, not a renamed implementation of the entire pipeline. Old scripts have private path/dependency assumptions and are not advertised as portable entry points.

## Data, splitting and input identity

MA-52 is short-video classification; MMA-52 has overlapping multi-label action intervals. Do not collapse intervals to one video label. Historical local labels are the OR of classes whose half-open frame interval [start,end) contains any observed GT-local frame; identical-class intervals are OR-ed. End-point annotation ambiguity was audited historically, not silently rewritten. Target MRR uses one fixed selected action and is not full multi-label accuracy.

The full MMA-52 train/inner protocol has 4,080 Fit and 454 Inner videos; retained Validation has 1,459 after 16 anomalous videos were quarantined. The local evidence protocol uses only a fixed 1,024 Fit subset plus all Inner/retained Validation, totaling 2,937. Their private sample membership is withheld. Do not recreate it from arbitrary random rows and call the result an exact reproduction.

MA-52 grouped development folds use SHA256(filename first underscore field) modulo five, original training data only, fit-only normalization. Those groups are **prefixes, not verified subjects**. Duplicate exclusions and old protocol definitions stay private and unchanged. Do not construct new cross-subject claims from embeddings or filenames. Both official Validation and Inner have substantial development reuse.

VideoMAE diagnostic preprocessing: 16 exact raw frame indices, whole-frame aspect-preserving letterbox to 224, RGB /127.5 −1, tubelet length 2, eight contextual positions. This differs from some official crop/normalization recipes and must not be silently changed. Small feature dimension 384; Base 768. It is not fine-resolution ground-truth motion measurement.

## Seeds, optimization and metrics

Latest local studies: seeds 42/1601, 50 epochs, AdamW .001 / weight decay .0001, batch 64, Fit-only scaler, Inner clean GT-local unweighted BCE every ten epochs (earliest minimum). B1/B2 use two views per update versus historical B0 one; B2 adds unit-weight mean squared sigmoid difference. See `configs/local_probe_protocol.json`. Older Stage 14–17 controls use seeds 42/43/44 and fixed final-epoch OOF evaluation; never merge these protocols.

Recognition: local 52-class mAP, target MRR and strict Top1. Historical MA-52: Macro-F1 and Top1, with early 51/52-class denominator differences explicitly noted in old reports. Detection: class-aware matching, temporal IoU thresholds 0.1–0.9 and within-class suppression; **not implemented by the public recognition metric utility**. Historical detector-order tie audits must accompany any future detector replay.

## Dependencies and compute

Public package: Python 3.10+, NumPy, matplotlib; no torch required. Install from `requirements.txt`. Packaging tests record the actual environment in `docs/release_validation.json`; version ranges express portable intent, not a tested matrix. Historical environment records include torch 2.7.1+cu128, timm 1.0.22, NumPy and OpenCV on Windows with a 12 GB NVIDIA laptop GPU. Full lockfiles contain machine-specific/dated packages and are not presented as a universal installation recipe.

Latest appearance-view study recorded about 0.220 GPU-related hours including decoding/profile allowance, four CPU reference probes and **zero natural-video M1 training**. This is a historical accounting entry, not measured packaging cost or a prediction for another machine. Strong encoders, dense teachers and Video-LLMs may require NTU/NSCC-class resources; no server experiment is claimed complete. Packaging used CPU reads, plotting and tests only.
