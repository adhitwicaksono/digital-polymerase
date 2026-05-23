# Prototype 003A RNA → FANA Run Summary

## RNA-8mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 003A
Chain-preserving RNA → FANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-8mer.pdb
FANA template: /mnt/data/2KP4_FANA_10mer.pdb
Output PDB: /mnt/data/fana_patch_003A_outputs/converted_fana_RNA-8mer_003A.pdb
Report: /mnt/data/fana_patch_003A_outputs/conversion_report_RNA-8mer_003A.md
Converted residues: 8
Source sequence: CUAGGCUC
Mean anchor RMSD: 0.0477 Å
Max anchor RMSD: 0.0726 Å
--------------------------------------------------------------------------------
Validation:
  O3′(i)→P(i+1): PASS (measured=7, failed=0, mean=1.606 Å)
  C2′→F2′: PASS (measured=8, failed=0, mean=1.382 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-12mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 003A
Chain-preserving RNA → FANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-12mer.pdb
FANA template: /mnt/data/2KP4_FANA_10mer.pdb
Output PDB: /mnt/data/fana_patch_003A_outputs/converted_fana_RNA-12mer_003A.pdb
Report: /mnt/data/fana_patch_003A_outputs/conversion_report_RNA-12mer_003A.md
Converted residues: 12
Source sequence: CUAGGCUCGAAA
Mean anchor RMSD: 0.0508 Å
Max anchor RMSD: 0.0726 Å
--------------------------------------------------------------------------------
Validation:
  O3′(i)→P(i+1): PASS (measured=11, failed=0, mean=1.607 Å)
  C2′→F2′: PASS (measured=12, failed=0, mean=1.382 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-16mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 003A
Chain-preserving RNA → FANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-16mer.pdb
FANA template: /mnt/data/2KP4_FANA_10mer.pdb
Output PDB: /mnt/data/fana_patch_003A_outputs/converted_fana_RNA-16mer_003A.pdb
Report: /mnt/data/fana_patch_003A_outputs/conversion_report_RNA-16mer_003A.md
Converted residues: 16
Source sequence: ACCACCUAGGCUCGAA
Mean anchor RMSD: 0.0514 Å
Max anchor RMSD: 0.0726 Å
--------------------------------------------------------------------------------
Validation:
  O3′(i)→P(i+1): PASS (measured=15, failed=0, mean=1.606 Å)
  C2′→F2′: PASS (measured=16, failed=0, mean=1.382 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-22mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 003A
Chain-preserving RNA → FANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-22mer.pdb
FANA template: /mnt/data/2KP4_FANA_10mer.pdb
Output PDB: /mnt/data/fana_patch_003A_outputs/converted_fana_RNA-22mer_003A.pdb
Report: /mnt/data/fana_patch_003A_outputs/conversion_report_RNA-22mer_003A.md
Converted residues: 22
Source sequence: AUACGACCACCUAGGCUCGAAA
Mean anchor RMSD: 0.0551 Å
Max anchor RMSD: 0.0939 Å
--------------------------------------------------------------------------------
Validation:
  O3′(i)→P(i+1): PASS (measured=21, failed=0, mean=1.606 Å)
  C2′→F2′: PASS (measured=22, failed=0, mean=1.382 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## RNA-34mer

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 003A
Chain-preserving RNA → FANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/RNA-34mer.pdb
FANA template: /mnt/data/2KP4_FANA_10mer.pdb
Output PDB: /mnt/data/fana_patch_003A_outputs/converted_fana_RNA-34mer_003A.pdb
Report: /mnt/data/fana_patch_003A_outputs/conversion_report_RNA-34mer_003A.md
Converted residues: 34
Source sequence: GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC
Mean anchor RMSD: 0.0535 Å
Max anchor RMSD: 0.0939 Å
--------------------------------------------------------------------------------
Validation:
  O3′(i)→P(i+1): PASS (measured=33, failed=0, mean=1.606 Å)
  C2′→F2′: PASS (measured=34, failed=0, mean=1.382 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```

## 8t5o-HH-typeI-111mer-full

Return code: `0`

```text
================================================================================
Digital Polymerase Prototype 003A
Chain-preserving RNA → FANA candidate reconstruction
================================================================================
Source RNA: /mnt/data/8t5o-HH-typeI-111mer-full.pdb
FANA template: /mnt/data/2KP4_FANA_10mer.pdb
Output PDB: /mnt/data/fana_patch_003A_outputs/converted_fana_8t5o-HH-typeI-111mer-full_003A.pdb
Report: /mnt/data/fana_patch_003A_outputs/conversion_report_8t5o-HH-typeI-111mer-full_003A.md
Converted residues: 111
Source sequence: GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
Mean anchor RMSD: 0.0520 Å
Max anchor RMSD: 0.0955 Å
--------------------------------------------------------------------------------
Validation:
  O3′(i)→P(i+1): PASS (measured=109, failed=0, mean=1.606 Å)
  C2′→F2′: PASS (measured=111, failed=0, mean=1.382 Å)
================================================================================

STDERR:
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/generated/interface/models.py", line 48821, in hydrate_crdt_from_proto
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/remote.py", line 747, in __call__
  File "/tmp/tmp.9eeVjt35CN/artifact_tool_v2-2.7.5/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```
