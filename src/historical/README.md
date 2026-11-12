# Selected unchanged first-party research utilities

These are original source snapshots, not the full historical training stack. `baseline_metrics.py` implements single-label metrics; `group_folds.py` explicitly uses filename-prefix proxies; `evidence_sampling.py` operates on legacy cached descriptors; `explicit_motion.py` requires OpenCV and contains hand-crafted features, not a learned motion encoder. No data or third-party code is embedded. Dependencies beyond the public smoke path are optional; hashes are in `docs/historical_source_manifest.json`.
