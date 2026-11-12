# Data and license audit

Audit date: 2026-11-12. This is a packaging inventory, not a grant of dataset/model rights. No third-party media, labels, features, per-video predictions, model weights, paper PDFs or model implementations are distributed. Aggregate research statistics and project-authored utilities are included. A public release must not imply that historical access equals redistribution permission.

| Resource | Evidence / access status | Packaging action |
|---|---|---|
| MA-52 | Local research package and public agreement template were audited historically; executed project authorization was not verified. The template restricts database/derived-information transfers and modifications. | Exclude data and derived per-video records; acquisition through [official repository](https://github.com/VUT-HFUT/Micro-Action) / [data card](https://huggingface.co/datasets/kunli-cs/MA-52). Obtain owner approval for intended use, annotation and institutional transfers. |
| MMA-52 | Local train/validation used; test labels are placeholders. No locally verified video-to-subject mapping. Redistribution permission not established. | No media, annotations, quarantined-video list or per-video outputs. Follow [MMAD owner](https://github.com/kunli-cs/MMAD) instructions; verify terms separately from MA-52. |
| iMiGUE / iMiGUE-3K | Access application pending in the research record; no completed experiment evidence. | No data/results claimed. Follow [iMiGUE official repository](https://github.com/linuxsino/iMiGUE), request current authorized access; do not substitute mirrors. |
| CAS(ME)3 | No completed experiment or local authorization evidence identified in audited outputs. | Not included or claimed as used. Obtain official owner instructions if studied later. |
| KTH | A local folder exists; not used as evidence in this release. | No data copied and no result claim. |
| VideoMAE code | Historical pinned commit `14ef8d856287c94ef1f985fe30f958eb4ec2c55d`; saved license and current [official LICENSE](https://github.com/MCG-NJU/VideoMAE/blob/main/LICENSE) indicate CC BY-NC 4.0. | Third-party source excluded. Record version and attribution; independently obey terms if installing. |
| VideoMAE-S/B pretrained checkpoints | Official-origin checkpoints were used locally. Code license alone is not treated as proof of unrestricted weight or source-dataset redistribution. | No weights. Acquire separately through official model instructions, confirm weight-specific terms and record checksum. |
| MAC_2024 / OpenTAD | Historical code audit recorded Apache-2.0 at pinned commits; not a complete reproduced ICCV-2025 DSTA system. | No vendored code. Links and version metadata only. |
| Project-authored utilities | Selected first-party files and newly packaged audit utilities. | No blanket open-source license has been invented on the author's behalf; see RIGHTS.md. |

Historical official-code pins: MAC_2024 `3c8b4431ead0bf14fde44925f01951461345e0a1`; OpenTAD `346d09d19e2091372cec48172dbe40f7b28bdee6`; MMAD `d06121d2b4eb84cac9758d910816c8597dcc7ec5`. At the historical MMAD pin only a minimal README was available; this is not a claim about all subsequent releases. Current public links were checked for provenance, not for a new reproduction study.

## Acquisition procedure

1. Read the relevant owner's current terms; obtain project/institution-specific permission where required. No email is sent or agreement signed by this package.
2. Download through approved owner channels into an untracked local directory. Never use official test placeholders as labels.
3. Copy `configs/local.example.json` to ignored `configs/local.json`; fill local roots yourself. Do not commit actual paths, credentials, annotations or participant records.
4. Preserve raw data read-only. Build derived caches locally under the same access restrictions. A changed annotation set or checkpoint is a new experiment identity.
5. Do not infer permission for server upload, manual relabeling or redistribution from a publicly reachable download.

Only non-instance aggregate performance numbers are published here; this does not certify contractual approval for every downstream use. The checklist retains owner review of publication scope before any actual push, which this task does not perform.
